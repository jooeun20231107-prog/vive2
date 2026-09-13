import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="이벤트 아키텍트 AI - AI 기반 행사 자동 설계 플랫폼",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    /* 전체 배경 및 폰트 */
    .stApp {
        background-color: #F8FAFC;
        color: #0F172A;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }
    
    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* 카드 컨테이너 스타일 */
    .custom-card {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
    }

    /* CAD 툴바 스타일 */
    .cad-top-bar {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        padding: 10px 18px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-radius: 12px;
        margin-bottom: 16px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
    }

    /* AI 요약 박스 */
    .reason-box {
        background-color: #F0F9FF;
        border-left: 4px solid #0284C7;
        padding: 14px 16px;
        border-radius: 8px;
        margin-top: 10px;
        font-size: 0.9rem;
        color: #0F172A;
    }

    /* Streamlit 버튼 튜닝 */
    .stButton>button {
        border-radius: 8px;
        font-weight: 700;
    }

    /* 로고 타이틀 버튼 */
    div[data-testid="stButton"] button[key="btn_home_logo_title"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        font-size: 22px !important;
        font-weight: 800 !important;
        color: #2563EB !important;
        text-align: left !important;
        box-shadow: none !important;
    }
    </style>
""", unsafe_allow_html=True)

OPTIMAL_FACILITY_PRESETS = {
    "stage": {
        "name": "공연장 (메인무대)",
        "icon": "🎭",
        "hex": "#2563EB",
        "x": 50, "y": 85, "w": 32, "h": 10,
        "power": "100kW (임시발전차 연계)",
        "fire_clearance": "합격 (피난거리 12m)",
        "reason": "✨ AI 최적 배치: 북쪽 중앙 상단에 배치하여 관람 시야각(170°)과 음향 명확도를 극대화했습니다."
    },
    "booth": {
        "name": "체험부스 단지",
        "icon": "🎪",
        "hex": "#7C3AED",
        "x": 22, "y": 78, "w": 18, "h": 12,
        "power": "15kW",
        "fire_clearance": "합격 (3m 간격 통로 확보)",
        "reason": "✨ AI 최적 배치: 북서쪽 주요 보행 동선에 모듈형으로 형성하여 초기 유입률을 35% 향상시켰습니다."
    },
    "food": {
        "name": "푸드트럭 존",
        "icon": "🍔",
        "hex": "#EA580C",
        "x": 20, "y": 48, "w": 22, "h": 16,
        "power": "45kW (위생수도 인프라 직결)",
        "fire_clearance": "합격 (소화기 6대 배치)",
        "reason": "✨ AI 최적 배치: 서쪽 측면 외곽에 독립 배치하여 조리 연기 확산을 막고 메인 통로 병목 현상을 방지합니다."
    },
    "rest": {
        "name": "잔디 휴게공간",
        "icon": "🌲",
        "hex": "#059669",
        "x": 50, "y": 48, "w": 24, "h": 14,
        "power": "5kW (차광 파라솔 구역)",
        "fire_clearance": "합격 (중앙 피난 통로 유지)",
        "reason": "✨ AI 최적 배치: 무대와 푸드존 중간 구역에 시야를 가리지 않도록 배치하여 휴식 및 무대 관람을 동시 제공합니다."
    },
    "medical": {
        "name": "응급의료센터",
        "icon": "🚑",
        "hex": "#DC2626",
        "x": 84, "y": 75, "w": 12, "h": 8,
        "power": "10kW (비상전원 차출)",
        "fire_clearance": "최우수 (구급차 비상차로 1m 직결)",
        "reason": "✨ AI 최적 배치: 동쪽 비상 전용도로에 직결 배치하여 3분 이내 응급 이송 골든타임을 확보했습니다."
    },
    "toilet": {
        "name": "이동식 화장실",
        "icon": "🚻",
        "hex": "#0284C7",
        "x": 84, "y": 52, "w": 12, "h": 8,
        "power": "20kW (상하수 배관 동파 방지)",
        "fire_clearance": "합격",
        "reason": "✨ AI 최적 배치: 동쪽 상하수도 인프라 인접 구역에 배치하고 대기 줄이 메인 동선을 침범하지 않도록 유도했습니다."
    },
    "info": {
        "name": "종합 안내센터",
        "icon": "ℹ️",
        "hex": "#DB2777",
        "x": 50, "y": 22, "w": 12, "h": 6,
        "power": "5kW",
        "fire_clearance": "합격 (주 출입구 5m 거리)",
        "reason": "✨ AI 최적 배치: 남쪽 정문 진입구 정면에 배치하여 관람객 길안내 및 잃어버린 아이 안내를 즉시 처리합니다."
    },
    "exit": {
        "name": "메인 게이트 (출입구)",
        "icon": "🚪",
        "hex": "#64748B",
        "x": 50, "y": 8, "w": 26, "h": 5,
        "power": "100kW (스피드게이트)",
        "fire_clearance": "최우수 (주 피난 통로 폭 10m)",
        "reason": "✨ AI 최적 배치: 남쪽 광장 최하단에 배치하여 대규모 인파 진출입 및 소방법 비상 대피를 원활하게 수행합니다."
    }
}

if 'page' not in st.session_state:
    st.session_state['page'] = 'dashboard'
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = True
if 'username' not in st.session_state:
    st.session_state['username'] = "주은님"
if 'digital_twin_generated' not in st.session_state:
    st.session_state['digital_twin_generated'] = False
if 'selected_facility' not in st.session_state:
    st.session_state['selected_facility'] = 'stage'
if 'facilities' not in st.session_state:
    st.session_state['facilities'] = {k: v.copy() for k, v in OPTIMAL_FACILITY_PRESETS.items()}
if 'view_mode' not in st.session_state:
    st.session_state['view_mode'] = "2D CAD 도면"
if 'venue_bg_type' not in st.session_state:
    st.session_state['venue_bg_type'] = "야외 잔디 광장"
if 'show_heatmap_overlay' not in st.session_state:
    st.session_state['show_heatmap_overlay'] = True
if 'show_flow_arrows' not in st.session_state:
    st.session_state['show_flow_arrows'] = True
if 'crowd_frame' not in st.session_state:
    st.session_state['crowd_frame'] = 0
if 'event_name' not in st.session_state:
    st.session_state['event_name'] = "2026 야외 뮤직 & 푸드 페스티벌"
if 'expected_visitors' not in st.session_state:
    st.session_state['expected_visitors'] = 5000
if 'budget' not in st.session_state:
    st.session_state['budget'] = "5,000만원"
if 'location' not in st.session_state:
    st.session_state['location'] = "서울 수변 야외 공원 광장"
if 'duration' not in st.session_state:
    st.session_state['duration'] = "8시간"
if 'event_purpose' not in st.session_state:
    st.session_state['event_purpose'] = "야외 문화 공연 및 청년 푸드트럭 페스타"
if 'chat_messages' not in st.session_state:
    st.session_state['chat_messages'] = [
        {"role": "assistant", "content": "안녕하세요! **이벤트 아키텍트 AI Studio**입니다. 시설물을 클릭하시거나 '푸드존을 외곽으로 이동'과 같이 대화해 보세요."}
    ]

def apply_ai_optimal_placement(key: str):
    """Calculates and updates facility coordinates to its AI optimal location."""
    if key in OPTIMAL_FACILITY_PRESETS:
        preset = OPTIMAL_FACILITY_PRESETS[key]
        st.session_state['facilities'][key]['x'] = preset['x']
        st.session_state['facilities'][key]['y'] = preset['y']
        st.session_state['facilities'][key]['w'] = preset['w']
        st.session_state['facilities'][key]['h'] = preset['h']
        st.session_state['facilities'][key]['reason'] = preset['reason']
        st.session_state['selected_facility'] = key
        st.toast(f"✨ {preset['name']} 최적 배치 적용 완료!")

def parse_and_apply_ai_command(prompt: str):
    prompt_clean = prompt.replace(" ", "")
    facs = st.session_state['facilities']
    
    target_key = None
    if "푸드" in prompt_clean or "먹거리" in prompt_clean or "음식" in prompt_clean:
        target_key = "food"
    elif "화장실" in prompt_clean:
        target_key = "toilet"
    elif "무대" in prompt_clean or "공연" in prompt_clean:
        target_key = "stage"
    elif "부스" in prompt_clean or "체험" in prompt_clean:
        target_key = "booth"
    elif "의료" in prompt_clean or "응급" in prompt_clean or "구급" in prompt_clean:
        target_key = "medical"
    elif "휴게" in prompt_clean or "쉼터" in prompt_clean or "휴식" in prompt_clean:
        target_key = "rest"
    elif "안내" in prompt_clean:
        target_key = "info"
    elif "출입구" in prompt_clean or "입구" in prompt_clean or "출구" in prompt_clean:
        target_key = "exit"

    if not target_key:
        target_key = st.session_state['selected_facility']

    fac = facs[target_key]
    action_desc = ""

    if "최적" in prompt_clean or "자동" in prompt_clean or "추천" in prompt_clean:
        apply_ai_optimal_placement(target_key)
        return f"{fac['name']}의 AI 최적 권장 배치를 적용했습니다."

    if "멀리" in prompt_clean or "외곽" in prompt_clean or "분리" in prompt_clean:
        if target_key == "food":
            fac["x"] = 18
            fac["y"] = 48
            action_desc = "푸드존을 조리 연기 차단 및 혼잡 예방을 위해 서쪽 최외곽 구역으로 이동했습니다."
        elif target_key == "toilet":
            fac["x"] = 86
            fac["y"] = 45
            action_desc = "화장실을 배관 인프라 및 대기 공간 확보를 위해 동쪽 외곽 구역으로 재배치했습니다."
        else:
            fac["x"] = max(12, fac["x"] - 15)
            action_desc = f"{fac['name']}을(를) 외곽 구역으로 이동 조작했습니다."
    elif "근처" in prompt_clean or "인접" in prompt_clean or "옆" in prompt_clean:
        if target_key == "toilet":
            ref_fac = facs["medical"]
            fac["x"] = ref_fac["x"]
            fac["y"] = ref_fac["y"] - 18
            action_desc = "화장실을 응급의료센터 인근 동쪽 서비스 라인으로 이동 배치했습니다."
        else:
            fac["x"] = min(85, fac["x"] + 10)
            action_desc = f"{fac['name']} 위치를 인접 구역으로 최적 조정했습니다."
    elif "북쪽" in prompt_clean or "위" in prompt_clean:
        fac["y"] = min(90, fac["y"] + 10)
        action_desc = f"{fac['name']} 좌표를 북쪽 방향(+10m)으로 이동했습니다."
    elif "남쪽" in prompt_clean or "아래" in prompt_clean:
        fac["y"] = max(10, fac["y"] - 10)
        action_desc = f"{fac['name']} 좌표를 남쪽 방향(-10m)으로 이동했습니다."
    elif "확장" in prompt_clean or "키워" in prompt_clean or "넓혀" in prompt_clean:
        fac["w"] = int(fac["w"] * 1.2)
        fac["h"] = int(fac["h"] * 1.2)
        action_desc = f"{fac['name']} 면적 규격을 20% 확대 설정했습니다."
    else:
        fac["x"] = min(90, fac["x"] + 5)
        action_desc = f"{fac['name']}의 최적 CAD 위치 좌표를 조정 계산했습니다."

    fac["reason"] = f"AI 알고리즘 분석 결과: {action_desc} ({prompt} 요청 반영)"
    st.session_state['selected_facility'] = target_key
    return action_desc

if st.button("🎪 Event Architect AI | AI 기반 행사 공간 CAD & 3D 설계 플랫폼", key="btn_home_logo_title"):
    st.session_state['page'] = 'home'
    st.rerun()

st.divider()

if st.session_state['page'] == "home":
    st.markdown("<div style='text-align: center; padding: 20px 0;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color: #0F172A; font-weight: 800; font-size: 36px;'>AI 기반 스마트 행사 공간 CAD 및 3D 배치 스튜디오</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #475569; font-size: 16px; max-width: 760px; margin: 0 auto;'>야외 잔디 광장, 아스팔트 공원, 실내 엑스포 홀 등 원하는 행사 배경에서 시설물 배치, 3D 디지털 트윈, 실시간 군중 밀도 시뮬레이션 및 행정 보고서를 원스톱으로 제공합니다.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="custom-card" style="text-align: center; border-top: 4px solid #2563EB;">
            <div style="font-size: 48px; margin-bottom: 12px;">🗺️</div>
            <h3 style="margin: 0 0 8px 0; font-weight: 800; color: #0F172A;">2D/3D CAD 스튜디오</h3>
            <p style="color: #64748B; font-size: 14px; line-height: 1.6;">
                무대, 푸드트럭, 체험 부스, 응급 센터를 자유롭게 조작하고 실시간 피난 안전 및 동선을 시뮬레이션합니다.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 CAD 스튜디오 바로가기", key="home_to_dash", type="primary", use_container_width=True):
            st.session_state['page'] = 'dashboard'
            st.rerun()

    with col2:
        st.markdown("""
        <div class="custom-card" style="text-align: center; border-top: 4px solid #7C3AED;">
            <div style="font-size: 48px; margin-bottom: 12px;">📄</div>
            <h3 style="margin: 0 0 8px 0; font-weight: 800; color: #0F172A;">AI 상사 결재용 보고서</h3>
            <p style="color: #64748B; font-size: 14px; line-height: 1.6;">
                공간 타당성, 소방법 피난 안전 검토, 군중 밀도 예측 데이터가 포함된 공식 직인 기안 문서를 자동 작성합니다.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("📄 AI 기안 보고서 생성", key="home_to_report", use_container_width=True):
            st.session_state['page'] = 'report'
            st.rerun()

elif st.session_state['page'] == "dashboard":
    
    # CAD Top Control Ribbon
    st.markdown("""
    <div class="cad-top-bar">
        <div style="display:flex; align-items:center; gap:12px;">
            <span style="font-weight:800; color:#0284C7; font-size:14px;">🛠️ 스마트 CAD 스튜디오</span>
            <span style="color:#CBD5E1;">|</span>
            <span style="font-size:12px; color:#334155;">단위: <b>mm / m</b></span>
            <span style="font-size:12px; color:#334155;">스냅: <b>ON (Grid 1m)</b></span>
        </div>
        <div style="display:flex; gap:8px;">
            <span style="background:#F1F5F9; border:1px solid #CBD5E1; padding:4px 10px; border-radius:6px; font-size:12px; color:#0284C7; font-weight:600;">
                📐 전체 면적: <b>5,000 m² (50m x 100m)</b>
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Event Settings Form Header Expander
    with st.expander("⚙️ 행사 정보 및 공간 배경 설정", expanded=not st.session_state['digital_twin_generated']):
        with st.form("event_info_form"):
            c_in1, c_in2, c_in3, c_in4 = st.columns(4)
            with c_in1:
                event_name_in = st.text_input("행사명", value=st.session_state['event_name'])
                venue_bg_in = st.selectbox("공간 배경", ["야외 잔디 광장", "야외 아스팔트 광장", "실내 컨벤션홀 (EXPO)"], index=0)
            with c_in2:
                visitors_in = st.number_input("예상 관람객 (명)", value=st.session_state['expected_visitors'], step=500)
                location_in = st.text_input("장소", value=st.session_state['location'])
            with c_in3:
                budget_in = st.text_input("예산", value=st.session_state['budget'])
                duration_in = st.text_input("행사 진행 시간", value=st.session_state['duration'])
            with c_in4:
                purpose_in = st.text_input("행사 목적", value=st.session_state['event_purpose'])
                st.write("")
                submit_btn = st.form_submit_button("🤖 전체 시설물 AI 최적 재배치", type="primary", use_container_width=True)

            if submit_btn:
                st.session_state['event_name'] = event_name_in
                st.session_state['venue_bg_type'] = venue_bg_in
                st.session_state['expected_visitors'] = visitors_in
                st.session_state['location'] = location_in
                st.session_state['budget'] = budget_in
                st.session_state['duration'] = duration_in
                st.session_state['event_purpose'] = purpose_in
                st.session_state['digital_twin_generated'] = True
                
                # Re-apply all presets
                for k in OPTIMAL_FACILITY_PRESETS:
                    apply_ai_optimal_placement(k)
                st.toast("✨ 전체 시설물 AI 공간 최적 배치가 완료되었습니다!")
                st.rerun()

    # Dynamic Crowd Simulation Control Top Bar
    c_crowd1, c_crowd2, c_crowd3 = st.columns([4, 4, 4])
    with c_crowd1:
        if st.button("👥 군중 예측 시뮬레이션 (인파 이동)", type="primary", use_container_width=True, key="btn_run_crowd_sim"):
            st.session_state['crowd_frame'] += 1
            st.toast(f"🏃 군중 예측 시뮬레이션 Step {st.session_state['crowd_frame']}: 관람객 이동 점 반영!")
            st.rerun()
    with c_crowd2:
        if st.button("🎯 전체 시설물 AI 최적 위치 일괄 적용", use_container_width=True, key="btn_all_opt"):
            for k in OPTIMAL_FACILITY_PRESETS:
                apply_ai_optimal_placement(k)
            st.toast("✨ 시설물 전체 최적 좌표가 일괄 적용되었습니다!")
            st.rerun()
    with c_crowd3:
        if st.button("📄 AI 기안 보고서 페이지 이동", use_container_width=True, key="btn_to_rep_top"):
            st.session_state['page'] = 'report'
            st.rerun()

    st.write("")

    col_tools, col_canvas, col_inspector = st.columns([2.6, 6.4, 3.0])

    with col_tools:
        st.markdown("<div class='custom-card' style='padding:16px;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='margin:0 0 12px 0; font-weight:800; color:#0F172A;'>🎨 CAD 시설물 라이브러리</h4>", unsafe_allow_html=True)
        
        tab_fac, tab_bg, tab_safety = st.tabs(["🎪 시설물 최적배치", "🏞️ 공간 테마", "📐 안전 검토"])

        with tab_fac:
            st.caption("시설물을 클릭하면 해당 시설의 AI 최적 위치 및 설명이 적용됩니다.")
            for f_key, f_data in st.session_state['facilities'].items():
                is_selected = (st.session_state['selected_facility'] == f_key)
                b_type = "primary" if is_selected else "secondary"
                
                c_btn1, c_btn2 = st.columns([3, 1])
                with c_btn1:
                    if st.button(f"{f_data['icon']} {f_data['name']}", key=f"btn_fac_sel_{f_key}", use_container_width=True, type=b_type):
                        st.session_state['selected_facility'] = f_key
                        st.rerun()
                with c_btn2:
                    if st.button("✨최적", key=f"btn_opt_single_{f_key}", use_container_width=True):
                        apply_ai_optimal_placement(f_key)
                        st.rerun()

        with tab_bg:
            st.markdown("**배경 테마 선택**")
            bg_choice = st.radio("장소 모드", ["야외 잔디 광장", "야외 아스팔트 광장", "실내 컨벤션홀 (EXPO)"], index=["야외 잔디 광장", "야외 아스팔트 광장", "실내 컨벤션홀 (EXPO)"].index(st.session_state['venue_bg_type']))
            if bg_choice != st.session_state['venue_bg_type']:
                st.session_state['venue_bg_type'] = bg_choice
                st.rerun()

        with tab_safety:
            st.markdown("**소방법 & 피난 안전성**")
            st.success("✅ 피난통로 최소 폭: 10m (기준 5m 이상)")
            st.info("🚑 구급차 골든타임 진입로: 동측 비상도로 1m 연결")
            st.warning("⚡ 임시 전력 통로: 메인 무대 100kW 차단기 수용")

        st.markdown("</div>", unsafe_allow_html=True)

    with col_canvas:
        c_m1, c_m2, c_m3 = st.columns([4, 4, 4])
        with c_m1:
            st.session_state['view_mode'] = st.radio("뷰 모드", ["2D CAD 도면", "3D 디지털 트윈"], horizontal=True)
        with c_m2:
            st.session_state['show_heatmap_overlay'] = st.checkbox("🔥 관람객 인파 히트맵", value=st.session_state['show_heatmap_overlay'])
        with c_m3:
            st.session_state['show_flow_arrows'] = st.checkbox("🧭 피난 동선 화살표", value=st.session_state['show_flow_arrows'])

        # -------------------------------------------------------------
        # 2D CAD Canvas View
        # -------------------------------------------------------------
        if st.session_state['view_mode'] == "2D CAD 도면":
            fig = go.Figure()

            # Canvas Color Styling based on Venue Type
            if st.session_state['venue_bg_type'] == "야외 잔디 광장":
                bg_col = "#E2E8F0"
                inner_col = "#DCFCE7"
                border_col = "#16A34A"
            elif st.session_state['venue_bg_type'] == "야외 아스팔트 광장":
                bg_col = "#CBD5E1"
                inner_col = "#E2E8F0"
                border_col = "#64748B"
            else:
                bg_col = "#E2E8F0"
                inner_col = "#F1F5F9"
                border_col = "#2563EB"

            # Canvas Boundary
            fig.add_shape(type="rect", x0=0, y0=0, x1=100, y1=100, fillcolor=bg_col, opacity=1, line=dict(width=0))
            fig.add_shape(type="rect", x0=2, y0=2, x1=98, y1=98, fillcolor=inner_col, line=dict(color=border_col, width=3))

            # Dimension Annotations
            fig.add_annotation(x=50, y=99, text="📐 50,000 mm (가로 50m)", showarrow=False, font=dict(color="#1D4ED8", size=12, family="monospace"))
            fig.add_annotation(x=1, y=50, text="📐 100,000 mm (세로 100m)", showarrow=False, font=dict(color="#1D4ED8", size=12, family="monospace"), textangle=-90)

            # Main Walkway Corridors
            fig.add_shape(type="rect", x0=10, y0=10, x1=90, y1=92, fillcolor="#CBD5E1", opacity=0.3, line=dict(color="#94A3B8", width=2, dash="dash"))
            fig.add_shape(type="rect", x0=42, y0=8, x1=58, y1=92, fillcolor="#94A3B8", opacity=0.3, line=dict(width=0))

            # Dynamic Crowd Density Simulation (Moving Dots)
            if st.session_state['show_heatmap_overlay']:
                frame = st.session_state['crowd_frame']
                np.random.seed(42 + frame)
                
                stg_p = st.session_state['facilities']['stage']
                fd_p = st.session_state['facilities']['food']
                gt_p = st.session_state['facilities']['exit']

                # Animated crowd shift calculated from crowd_frame
                shift_x = np.sin(frame * 0.5) * 4.0
                shift_y = np.cos(frame * 0.5) * 4.0

                x_stg = np.random.normal(stg_p["x"] + shift_x, 7, 350)
                y_stg = np.random.normal(stg_p["y"] - 8 + shift_y, 6, 350)
                
                x_fd = np.random.normal(fd_p["x"] + 5 - shift_x, 5, 220)
                y_fd = np.random.normal(fd_p["y"] + shift_y, 5, 220)
                
                x_gt = np.random.normal(gt_p["x"], 6, 180)
                y_gt = np.random.normal(gt_p["y"] + 6 + (frame % 3)*2, 4, 180)

                x_crowd = np.clip(np.concatenate([x_stg, x_fd, x_gt]), 3, 97)
                y_crowd = np.clip(np.concatenate([y_stg, y_fd, y_gt]), 3, 97)

                # Heatmap Contour Layer
                fig.add_trace(go.Histogram2dContour(
                    x=x_crowd, y=y_crowd,
                    colorscale=[
                        [0.0, 'rgba(255,255,255,0)'],
                        [0.15, 'rgba(59,130,246,0.35)'],
                        [0.45, 'rgba(34,197,94,0.6)'],
                        [0.75, 'rgba(245,158,11,0.85)'],
                        [1.0, 'rgba(239,68,68,0.95)']
                    ],
                    showscale=True,
                    ncontours=20,
                    line=dict(width=0),
                    hoverinfo="none",
                    colorbar=dict(title=dict(text="인파 밀도", font=dict(size=11)), thickness=10, len=0.6, x=1.02)
                ))

                # Moving Crowd Prediction Dots
                fig.add_trace(go.Scatter(
                    x=x_crowd[::2], y=y_crowd[::2],
                    mode="markers",
                    marker=dict(size=6, color="#DC2626", opacity=0.8, line=dict(color="#FFFFFF", width=0.5)),
                    name="실시간 이동 관람객 점",
                    hoverinfo="text",
                    hovertext=[f"👥 예측 관람객 #{i+1} (Frame {frame})" for i in range(len(x_crowd[::2]))]
                ))

            # Facility Geometries (Rectangles)
            for f_key, f_data in st.session_state['facilities'].items():
                px_val, py_val = f_data["x"], f_data["y"]
                w_val, h_val = f_data["w"], f_data["h"]
                is_sel = (st.session_state['selected_facility'] == f_key)
                l_width = 4 if is_sel else 2
                l_color = "#D97706" if is_sel else f_data["hex"]

                fig.add_shape(
                    type="rect",
                    x0=px_val - w_val/2, y0=py_val - h_val/2,
                    x1=px_val + w_val/2, y1=py_val + h_val/2,
                    fillcolor=f_data["hex"],
                    opacity=0.85,
                    line=dict(color=l_color, width=l_width)
                )

            # Evacuation Flow Arrows
            if st.session_state['show_flow_arrows']:
                gt = st.session_state['facilities']['exit']
                stg = st.session_state['facilities']['stage']
                fd = st.session_state['facilities']['food']
                med = st.session_state['facilities']['medical']

                paths = [
                    (gt["x"], gt["y"] + 2, fd["x"], fd["y"] - 6),
                    (gt["x"], gt["y"] + 2, med["x"] - 5, med["y"] - 5),
                    (fd["x"], fd["y"] + 6, stg["x"] - 10, stg["y"] - 10),
                ]
                for x1_p, y1_p, x2_p, y2_p in paths:
                    fig.add_trace(go.Scatter(
                        x=[x1_p, x2_p], y=[y1_p, y2_p],
                        mode="lines",
                        line=dict(color="#0284C7", width=3, dash="dashdot"),
                        showlegend=False,
                        hoverinfo="none"
                    ))

            # Facility Interactive Pin Markers
            f_x, f_y, f_names, f_colors, f_texts = [], [], [], [], []
            for f_key, f_data in st.session_state['facilities'].items():
                f_x.append(f_data["x"])
                f_y.append(f_data["y"])
                f_names.append(f_key)
                f_colors.append(f_data["hex"])
                prefix = "📍 " if st.session_state['selected_facility'] == f_key else ""
                f_texts.append(f"{prefix}{f_data['icon']} {f_data['name']}")

            fig.add_trace(go.Scatter(
                x=f_x, y=f_y,
                mode="markers+text",
                text=f_texts,
                textposition="top center",
                textfont=dict(color="#0F172A", size=13, family="Pretendard"),
                customdata=f_names,
                marker=dict(size=22, color=f_colors, line=dict(color="#FFFFFF", width=3)),
                hoverinfo="text",
                hovertext=[f"클릭하여 {name} 편집" for name in f_texts],
                name="시설물 핀"
            ))

            fig.update_layout(
                xaxis=dict(range=[0, 100], showgrid=True, gridcolor="#CBD5E1", zeroline=False),
                yaxis=dict(range=[0, 100], showgrid=True, gridcolor="#CBD5E1", zeroline=False),
                height=570,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="#FFFFFF",
                plot_bgcolor=bg_col,
                showlegend=False,
                clickmode="event+select"
            )

            map_event = st.plotly_chart(fig, use_container_width=True, on_select="rerun", selection_mode="points", key="cad_map_chart")

            if map_event and "selection" in map_event and map_event["selection"]["points"]:
                pts = map_event["selection"]["points"]
                if len(pts) > 0 and "customdata" in pts[0]:
                    sel_key = pts[0]["customdata"]
                    if sel_key in st.session_state['facilities'] and sel_key != st.session_state['selected_facility']:
                        st.session_state['selected_facility'] = sel_key
                        st.rerun()

        # -------------------------------------------------------------
        # 3D Digital Twin View
        # -------------------------------------------------------------
        else:
            fig_3d = go.Figure()

            # 3D Ground Mesh
            fig_3d.add_trace(go.Mesh3d(
                x=[0, 100, 100, 0],
                y=[0, 0, 100, 100],
                z=[0, 0, 0, 0],
                color='#F1F5F9' if st.session_state['venue_bg_type'] == "실내 컨벤션홀 (EXPO)" else '#BBF7D0',
                opacity=0.9,
                name="3D 지면"
            ))

            for f_key, f_data in st.session_state['facilities'].items():
                px_val, py_val = f_data["x"], f_data["y"]
                w_val, h_val = f_data["w"], f_data["h"]
                z_h = 9 if f_key == "stage" else (4.5 if f_key in ["food", "booth"] else 2.5)

                x_c = [px_val-w_val/2, px_val+w_val/2, px_val+w_val/2, px_val-w_val/2, px_val-w_val/2, px_val+w_val/2, px_val+w_val/2, px_val-w_val/2]
                y_c = [py_val-h_val/2, py_val-h_val/2, py_val+h_val/2, py_val+h_val/2, py_val-h_val/2, py_val-h_val/2, py_val+h_val/2, py_val+h_val/2]
                z_c = [0, 0, 0, 0, z_h, z_h, z_h, z_h]

                i_f = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2]
                j_f = [4, 5, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3]
                k_f = [6, 1, 5, 3, 6, 7, 1, 3, 5, 2, 7, 7]

                fig_3d.add_trace(go.Mesh3d(
                    x=x_c, y=y_c, z=z_c,
                    i=i_f, j=j_f, k=k_f,
                    color=f_data["hex"],
                    opacity=0.85,
                    name=f_data["name"]
                ))

            fig_3d.update_layout(
                scene=dict(
                    xaxis=dict(range=[0, 100], backgroundcolor="#F8FAFC", gridcolor="#CBD5E1"),
                    yaxis=dict(range=[0, 100], backgroundcolor="#F8FAFC", gridcolor="#CBD5E1"),
                    zaxis=dict(range=[0, 20], backgroundcolor="#F8FAFC", gridcolor="#CBD5E1"),
                    aspectratio=dict(x=1, y=1, z=0.3),
                    camera=dict(eye=dict(x=1.3, y=-1.3, z=0.9))
                ),
                height=570,
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor="#FFFFFF"
            )

            st.plotly_chart(fig_3d, use_container_width=True)

    with col_inspector:
        cur_key = st.session_state['selected_facility']
        cur_fac = st.session_state['facilities'][cur_key]

        # Selected Facility Detail Card
        st.markdown(f"""
        <div class="custom-card" style="border-left: 5px solid {cur_fac['hex']}; margin-bottom: 12px; padding: 18px;">
            <div style="font-size: 16px; font-weight: 800; color: #0F172A; margin-bottom: 8px;">
                {cur_fac['icon']} {cur_fac['name']} 속성 검토
            </div>
            <table style="width:100%; font-size:12px; color:#334155; border-collapse:collapse;">
                <tr><td style="padding:3px 0; color:#64748B;">위치 좌표 (X, Y):</td><td style="font-weight:bold; text-align:right;">({cur_fac['x']}m, {cur_fac['y']}m)</td></tr>
                <tr><td style="padding:3px 0; color:#64748B;">점유 규격 (W x H):</td><td style="font-weight:bold; text-align:right;">{cur_fac['w']}m x {cur_fac['h']}m</td></tr>
                <tr><td style="padding:3px 0; color:#64748B;">전력 인프라:</td><td style="font-weight:bold; text-align:right; color:#D97706;">{cur_fac.get('power', '5kW')}</td></tr>
                <tr><td style="padding:3px 0; color:#64748B;">소방 피난 검토:</td><td style="font-weight:bold; text-align:right; color:#16A34A;">{cur_fac.get('fire_clearance', '합격')}</td></tr>
            </table>
            <div class="reason-box">
                💡 <b>AI 최적 배치 사유:</b><br>{cur_fac['reason']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"✨ {cur_fac['name']} AI 최적 위치 재배치", type="primary", use_container_width=True, key=f"btn_opt_detail_{cur_key}"):
            apply_ai_optimal_placement(cur_key)
            st.rerun()

        st.write("")

        # AI Assistant Chat Box
        st.markdown("##### 💬 AI CAD Assistant")
        chat_box = st.container(height=170)
        with chat_box:
            for msg in st.session_state['chat_messages']:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

        user_input = st.chat_input("예: '푸드존을 더 외곽으로 이동해줘'")
        if user_input:
            st.session_state['chat_messages'].append({"role": "user", "content": user_input})
            reply_desc = parse_and_apply_ai_command(user_input)
            st.session_state['chat_messages'].append({"role": "assistant", "content": f"✨ {reply_desc}"})
            st.rerun()

elif st.session_state['page'] == "report":
    st.markdown("""
    <div style="margin-bottom: 16px;">
        <h2 style="margin:0; color:#0F172A; font-weight:800;">📄 AI 결재용 직인 기안 보고서</h2>
        <p style="margin:4px 0 0 0; color:#475569; font-size:14px;">행사장 CAD 공간 배치 타당성 및 소방법 피난 안전 검토 보고서입니다.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:#FFFFFF; color:#0F172A; border:2px solid #CBD5E1; border-radius:12px; padding:35px; box-shadow:0 4px 15px rgba(0,0,0,0.06); max-width:850px; margin:0 auto;">
        
        <!-- Header & Stamp Box -->
        <div style="display:flex; justify-content:space-between; align-items:flex-start; border-bottom:2px solid #0F172A; padding-bottom:15px; margin-bottom:25px;">
            <div>
                <h1 style="margin:0; font-size:24px; color:#0F172A; font-weight:900;">[결재 기안서] AI 공간 배치 및 피난 안전 검토서</h1>
                <p style="margin:6px 0 0 0; color:#64748B; font-size:13px;">문서번호: EA-2026-0913 | 기안일자: 2026. 09. 13 | 기안자: {st.session_state['username']}</p>
            </div>
            <table style="border-collapse:collapse; text-align:center; font-size:12px; border:1px solid #94A3B8;">
                <tr style="background:#F1F5F9;">
                    <th style="border:1px solid #94A3B8; width:55px; padding:4px;">담당</th>
                    <th style="border:1px solid #94A3B8; width:55px; padding:4px;">팀장</th>
                    <th style="border:1px solid #94A3B8; width:55px; padding:4px;">임원</th>
                </tr>
                <tr style="height:42px;">
                    <td style="border:1px solid #94A3B8; color:#2563EB; font-weight:bold;">(인)</td>
                    <td style="border:1px solid #94A3B8;">(인)</td>
                    <td style="border:1px solid #94A3B8;">(인)</td>
                </tr>
            </table>
        </div>

        <!-- Section 1 -->
        <h3 style="color:#2563EB; font-weight:800; margin-bottom:10px;">1. 행사 개요</h3>
        <table style="width:100%; border-collapse:collapse; margin-bottom:25px; font-size:13px; border:1px solid #E2E8F0;">
            <tr style="background:#F8FAFC;"><td style="padding:8px; font-weight:bold; width:22%; border:1px solid #E2E8F0;">행사명</td><td style="padding:8px; border:1px solid #E2E8F0;">{st.session_state['event_name']}</td></tr>
            <tr><td style="padding:8px; font-weight:bold; background:#F8FAFC; border:1px solid #E2E8F0;">공간 배경</td><td style="padding:8px; border:1px solid #E2E8F0;">{st.session_state['venue_bg_type']}</td></tr>
            <tr style="background:#F8FAFC;"><td style="padding:8px; font-weight:bold; border:1px solid #E2E8F0;">예상 인원 / 예산</td><td style="padding:8px; border:1px solid #E2E8F0;">{st.session_state['expected_visitors']:,}명 / {st.session_state['budget']}</td></tr>
            <tr><td style="padding:8px; font-weight:bold; background:#F8FAFC; border:1px solid #E2E8F0;">장소 / 진행시간</td><td style="padding:8px; border:1px solid #E2E8F0;">{st.session_state['location']} ({st.session_state['duration']})</td></tr>
        </table>

        <!-- Section 2 -->
        <h3 style="color:#2563EB; font-weight:800; margin-bottom:10px;">2. AI CAD 공간 배치 분석 요약</h3>
        <ul style="line-height:1.8; color:#334155; font-size:13px; margin-bottom:25px; padding-left:20px;">
            <li><b>메인 무대:</b> 북측 중앙 위치로 수용 인원 시야각 확보 및 소음 제어 최적화.</li>
            <li><b>피난 통로:</b> 비상통로폭 10m 확보로 소방법 기준 완전 통과.</li>
            <li><b>응급의료센터:</b> 비상 차로 직결 배치로 3분 이내 응급 이송 경로 단축.</li>
            <li><b>푸드트럭 존 & 위생:</b> 풍향 연기 확산 및 병목 차단을 고려한 외곽 구역 분리.</li>
        </ul>

        <!-- Section 3 -->
        <h3 style="color:#2563EB; font-weight:800; margin-bottom:10px;">3. 종합 기안 의견</h3>
        <p style="color:#334155; font-size:13px; line-height:1.7; background:#EFF6FF; padding:12px; border-radius:8px; border:1px solid #BFDBFE;">
            본 사업 계획은 AI 기반 Digital Twin CAD 솔루션을 통하여 관람객 안전, 소방법 피난 요건 및 관람 편의성을 종합 검토하였습니다. 위와 같이 상신하오니 결재하여 주시기 바랍니다.
        </p>

    </div>
    """, unsafe_allow_html=True)

    st.write("")
    c_r1, c_r2 = st.columns(2)
    with c_r1:
        if st.button("📥 보고서 PDF 다운로드", key="btn_pdf_export", type="primary", use_container_width=True):
            st.toast("PDF 기안서 파일 생성이 완료되었습니다!")
    with c_r2:
        if st.button("🖨️ 결재서 인쇄하기", key="btn_print_export", use_container_width=True):
            st.toast("인쇄 시스템을 호출합니다.")
