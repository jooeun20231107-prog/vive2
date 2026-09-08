import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="이벤트 아키텍트 AI - AI 기반 행사 자동 설계 플랫폼",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* 전체 배경 및 폰트 */
    .stApp {
        background-color: #F8FAFC;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
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

    /* 뱃지 및 태그 디자인 */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 700;
    }
    .badge-excellent { background-color: #DCFCE7; color: #15803D; }
    .badge-good { background-color: #DBEAFE; color: #1E40AF; }
    .badge-warning { background-color: #FEF3C7; color: #B45309; }

    /* AI 요약 박스 */
    .reason-box {
        background-color: #F0F9FF;
        border-left: 4px solid #0284C7;
        padding: 16px;
        border-radius: 8px;
        margin-top: 10px;
    }

    /* 3D 디지털 트윈 스토리지 컨트롤 바 */
    .view-control-bar {
        background: #0F172A;
        color: #F8FAFC;
        padding: 12px 18px;
        border-radius: 12px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    /* 혼잡도 범례 HUD 카드 */
    .legend-card {
        background: rgba(15, 23, 42, 0.95);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 12px 16px;
        color: #F8FAFC;
        font-size: 0.85rem;
        margin-bottom: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25);
    }
    .legend-item {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        margin-right: 16px;
        font-weight: 600;
    }
    .legend-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        display: inline-block;
    }

    /* 상단 로고 버튼 및 사이드바 간격 */
    div[data-testid="stSidebarHeader"] {
        padding-top: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

DEFAULT_FACILITIES = {
    "stage": {
        "name": "메인 무대 (Main Stage)",
        "icon": "🎪",
        "hex": "#8B5CF6",
        "hex_side": "#6D28D9",
        "hex_top": "#A78BFA",
        "x": 500, "y": 120, "w": 260, "h": 120, "height_3d": 45,
        "w_m": 26, "h_m": 12, "h_3d_m": 8,
        "reason": "북쪽 중앙 상단에 위치시켜 모든 관람객의 시야각과 음향 전달을 극대화했습니다."
    },
    "booth": {
        "name": "체험 부스 단지",
        "icon": "🛍️",
        "hex": "#3B82F6",
        "hex_side": "#1D4ED8",
        "hex_top": "#60A5FA",
        "x": 200, "y": 180, "w": 180, "h": 140, "height_3d": 25,
        "w_m": 18, "h_m": 14, "h_3d_m": 3.5,
        "reason": "북서쪽 진입 구역에 부스 단지를 형성하여 초기 관람객 유입률을 높였습니다."
    },
    "food": {
        "name": "푸드트럭 존",
        "icon": "🍔",
        "hex": "#F97316",
        "hex_side": "#C2410C",
        "hex_top": "#FB923C",
        "x": 200, "y": 420, "w": 180, "h": 150, "height_3d": 30,
        "w_m": 18, "h_m": 15, "h_3d_m": 4,
        "reason": "서쪽 측면에 독립 배치하여 조리 연기 확산을 막고 관람 동선과 유연하게 분리했습니다."
    },
    "rest": {
        "name": "잔디 휴게 광장",
        "icon": "🏕️",
        "hex": "#10B981",
        "hex_side": "#047857",
        "hex_top": "#34D399",
        "x": 500, "y": 380, "w": 300, "h": 180, "height_3d": 12,
        "w_m": 30, "h_m": 18, "h_3d_m": 1.5,
        "reason": "중앙 잔디 광장에 위치시켜 메인 무대 감상과 쉼터 역할을 동시에 수행합니다."
    },
    "medical": {
        "name": "응급 의료 센터",
        "icon": "🚑",
        "hex": "#EF4444",
        "hex_side": "#B91C1C",
        "hex_top": "#F87171",
        "x": 820, "y": 150, "w": 160, "h": 100, "height_3d": 22,
        "w_m": 16, "h_m": 10, "h_3d_m": 3,
        "reason": "동쪽 외곽 비상 도로 옆에 배치하여 구급차의 최단 진출입 코스를 보장합니다."
    },
    "toilet": {
        "name": "위생 편의 시설",
        "icon": "🚻",
        "hex": "#0284C7",
        "hex_side": "#0369A1",
        "hex_top": "#38BDF8",
        "x": 820, "y": 300, "w": 160, "h": 100, "height_3d": 20,
        "w_m": 16, "h_m": 10, "h_3d_m": 2.8,
        "reason": "동쪽 측면에 위치시켜 인프라 접근성을 확보하고 대기 줄 최소화를 유도합니다."
    },
    "info": {
        "name": "종합 안내 센터",
        "icon": "ℹ️",
        "hex": "#EC4899",
        "hex_side": "#BE185D",
        "hex_top": "#F472B6",
        "x": 500, "y": 590, "w": 180, "h": 70, "height_3d": 18,
        "w_m": 18, "h_m": 7, "h_3d_m": 2.5,
        "reason": "주 출입구 정면에 위치시켜 길 안내 및 관람 문의를 신속하게 처리합니다."
    },
    "exit": {
        "name": "메인 출입 게이트",
        "icon": "🚪",
        "hex": "#64748B",
        "hex_side": "#334155",
        "hex_top": "#94A3B8",
        "x": 500, "y": 670, "w": 200, "h": 40, "height_3d": 15,
        "w_m": 20, "h_m": 4, "h_3d_m": 3,
        "reason": "남쪽 정문에 위치하여 대규모 인파의 효율적 진출입 및 비상 대피를 유도합니다."
    }
}

if 'page' not in st.session_state:
    st.session_state['page'] = 'home'
if 'previous_page' not in st.session_state:
    st.session_state['previous_page'] = 'home'
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = True
if 'username' not in st.session_state:
    st.session_state['username'] = "주은님"
if 'digital_twin_generated' not in st.session_state:
    st.session_state['digital_twin_generated'] = False
if 'selected_facility' not in st.session_state:
    st.session_state['selected_facility'] = 'stage'
if 'facilities' not in st.session_state:
    st.session_state['facilities'] = DEFAULT_FACILITIES.copy()

# 행사 기본 정보 세션 상태
if 'event_name' not in st.session_state:
    st.session_state['event_name'] = "2026 청춘 페스티벌"
if 'event_purpose' not in st.session_state:
    st.session_state['event_purpose'] = "축제/공연"
if 'event_visitors' not in st.session_state:
    st.session_state['event_visitors'] = 5000
if 'event_budget' not in st.session_state:
    st.session_state['event_budget'] = "5,000만원"
if 'event_location' not in st.session_state:
    st.session_state['event_location'] = "서울 올림픽공원 잔디마당 (100m x 72m)"
if 'event_duration' not in st.session_state:
    st.session_state['event_duration'] = "5시간"

if 'view_mode' not in st.session_state:
    st.session_state['view_mode'] = '2D_PLAN'
if 'show_crowd_flow' not in st.session_state:
    st.session_state['show_crowd_flow'] = True
if 'show_grid' not in st.session_state:
    st.session_state['show_grid'] = True
if 'chat_messages' not in st.session_state:
    st.session_state['chat_messages'] = [
        {"role": "assistant", "content": "🤖 **Claude-Spatial v3.5 AI 공간 에이전트** 가 가동되었습니다.\n'푸드존을 메인무대와 멀리 서쪽으로 이동해줘', '화장실을 의료 센터 근처로 보내줘' 등의 자연어 공간 명령을 입력해 주세요."}
    ]

def parse_and_apply_ai_command(prompt: str):
    prompt_clean = prompt.lower().replace(" ", "")
    facs = st.session_state['facilities']
    
    targets = []
    if "푸드" in prompt_clean or "먹거리" in prompt_clean or "식음료" in prompt_clean:
        targets.append("food")
    if "화장실" in prompt_clean or "위생" in prompt_clean:
        targets.append("toilet")
    if "무대" in prompt_clean or "공연" in prompt_clean or "메인" in prompt_clean:
        targets.append("stage")
    if "부스" in prompt_clean or "체험" in prompt_clean:
        targets.append("booth")
    if "의료" in prompt_clean or "응급" in prompt_clean or "병원" in prompt_clean:
        targets.append("medical")
    if "휴게" in prompt_clean or "쉼터" in prompt_clean or "잔디" in prompt_clean:
        targets.append("rest")
    if "안내" in prompt_clean or "인포" in prompt_clean:
        targets.append("info")
    if "출입구" in prompt_clean or "게이트" in prompt_clean or "입구" in prompt_clean:
        targets.append("exit")

    if not targets:
        targets = [st.session_state['selected_facility']]

    actions_summary = []
    safety_delta = "+8.5%"
    bottleneck_reduction = "32.4%"

    for target_key in targets:
        fac = facs[target_key]
        
        if "멀리" in prompt_clean or "외곽" in prompt_clean or "분리" in prompt_clean:
            if target_key == "food":
                fac["x"], fac["y"] = 150, 480
                fac["reason"] = "AI 동선 제어: 소음 및 조리 연기 유입 차단을 위한 서쪽 독립 구역 이동."
                actions_summary.append("🍔 **푸드트럭 존**: 연기 및 정체 방지를 위해 서쪽 독립 구역(x:150, y:480)으로 이동")
            elif target_key == "toilet":
                fac["x"], fac["y"] = 880, 400
                fac["reason"] = "AI 위생 제어: 메인 관람 구역과 충분한 거리를 둔 동쪽 외곽 배치."
                actions_summary.append("🚻 **위생 시설**: 메인 무대와 거리를 둔 동쪽 외곽 구역으로 재배치")
            else:
                fac["x"] = max(120, fac["x"] - 150)
                actions_summary.append(f"📍 **{fac['name']}**: 외곽 안전 구역으로 위치 변경")

        elif "의료" in prompt_clean or "근처" in prompt_clean or "가까이" in prompt_clean or "옆" in prompt_clean:
            ref_x, ref_y = facs["medical"]["x"], facs["medical"]["y"]
            fac["x"], fac["y"] = ref_x - 120, ref_y + 40
            fac["reason"] = "AI 긴급 대응: 비상 시 최단 동선 확보를 위해 응급 의료 센터 인근 배치."
            actions_summary.append(f"🚑 **{fac['name']}**: 비상 대피로 확보를 위해 응급의료센터 옆 구역으로 최적 이동")

        elif "동쪽" in prompt_clean or "오른쪽" in prompt_clean:
            fac["x"] = min(860, fac["x"] + 180)
            actions_summary.append(f"➡️ **{fac['name']}**: 동쪽 구역(x:{fac['x']})으로 재배치")

        elif "서쪽" in prompt_clean or "왼쪽" in prompt_clean:
            fac["x"] = max(140, fac["x"] - 180)
            actions_summary.append(f"⬅️ **{fac['name']}**: 서쪽 구역(x:{fac['x']})으로 재배치")

        elif "북쪽" in prompt_clean or "위" in prompt_clean or "상단" in prompt_clean:
            fac["y"] = max(110, fac["y"] - 140)
            actions_summary.append(f"⬆️ **{fac['name']}**: 상단 구역(y:{fac['y']})으로 이동")

        elif "남쪽" in prompt_clean or "아래" in prompt_clean or "하단" in prompt_clean:
            fac["y"] = min(610, fac["y"] + 140)
            actions_summary.append(f"⬇️ **{fac['name']}**: 하단 구역(y:{fac['y']})으로 이동")

        else:
            fac["x"] = (fac["x"] + 120) % 700 + 150
            fac["y"] = (fac["y"] + 80) % 450 + 150
            actions_summary.append(f"✨ **{fac['name']}**: AI 시뮬레이션 기반 공간 균형 좌표로 재구성")

        st.session_state['selected_facility'] = target_key

    actions_bullet = "\n".join([f"- {act}" for act in actions_summary])
    
    response = f"""🧠 **[Claude-Spatial AI 분석 및 도면 적용 완료]**

요청하신 spatial prompt 의도를 분석하여 디지털 트윈 레이아웃을 실시간 수정했습니다.

📐 **공간 재배치 실행 결과:**
{actions_bullet}

📊 **공간 안전성 시뮬레이션 영향평가:**
• **병목 위험 감소율:** `🔻 {bottleneck_reduction}` (관람객 이동 유연성 증가)
• **비상 대피 효율성:** `🟢 {safety_delta}` 상승 (최단 비상 진출입로 간섭 최소화)
• **음향 및 시야각 종합 만족도:** `98.2점` (최상위 등급)

💡 *실시간 디지털 트윈 2D/3D 도면 및 보고서 데이터에 즉시 반영되었습니다.*"""

    return response

with st.sidebar:
    if st.button("🎪 이벤트 아키텍트 AI", key="logo_btn", use_container_width=True, type="primary"):
        st.session_state['previous_page'] = st.session_state['page']
        st.session_state['page'] = 'home'
        st.rerun()

    st.caption("AI 기반 행사 자동 설계 플랫폼")
    st.divider()

    page_selection = st.radio(
        "메뉴 이동",
        ["홈 화면", "AI 행사 설계 대시보드", "AI 보고서", "설정"],
        index=["home", "dashboard", "report", "settings"].index(st.session_state['page'])
    )

    if page_selection == "홈 화면" and st.session_state['page'] != 'home':
        st.session_state['previous_page'] = st.session_state['page']
        st.session_state['page'] = 'home'
        st.rerun()
    elif page_selection == "AI 행사 설계 대시보드" and st.session_state['page'] != 'dashboard':
        st.session_state['previous_page'] = st.session_state['page']
        st.session_state['page'] = 'dashboard'
        st.rerun()
    elif page_selection == "AI 보고서" and st.session_state['page'] != 'report':
        st.session_state['previous_page'] = st.session_state['page']
        st.session_state['page'] = 'report'
        st.rerun()
    elif page_selection == "설정" and st.session_state['page'] != 'settings':
        st.session_state['previous_page'] = st.session_state['page']
        st.session_state['page'] = 'settings'
        st.rerun()

    st.divider()

    if st.session_state['logged_in']:
        st.markdown(f"👤 **{st.session_state['username']}** 님 로그인 중")
        if st.button("로그아웃", key="sidebar_logout"):
            st.session_state['logged_in'] = False
            st.rerun()

top_col1, top_col2 = st.columns([3, 1])
with top_col1:
    st.title("🎪 AI 기반 행사 자동 설계 플랫폼")
with top_col2:
    st.markdown("<div style='text-align: right; padding-top: 10px;'>", unsafe_allow_html=True)
    c_user, c_set = st.columns([2, 1])
    with c_user:
        if st.session_state['logged_in']:
            with st.popover(f"👤 {st.session_state['username']}"):
                st.write(f"**{st.session_state['username']}** (총괄 기획자)")
                st.caption("이메일: user@event-architect.ai")
                st.divider()
                if st.button("설정 관리"):
                    st.session_state['previous_page'] = st.session_state['page']
                    st.session_state['page'] = 'settings'
                    st.rerun()
                if st.button("로그아웃"):
                    st.session_state['logged_in'] = False
                    st.rerun()
        else:
            with st.popover("🔑 로그인 / 회원가입"):
                u_in = st.text_input("아이디", value="주은님")
                p_in = st.text_input("비밀번호", type="password")
                if st.button("로그인"):
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = u_in
                    st.rerun()
    with c_set:
        if st.button("⚙️", help="설정으로 이동"):
            st.session_state['previous_page'] = st.session_state['page']
            st.session_state['page'] = 'settings'
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

if st.session_state['page'] == 'home':
    st.markdown("## 🚀 시작할 메뉴를 선택하세요")
    st.caption("아래 박스 카드를 누르시면 해당 기능 화면으로 즉시 이동합니다.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_dash, col_rep = st.columns(2)

    with col_dash:
        dash_card_html = """
        <div style="
            background: linear-gradient(135deg, #FFFFFF 0%, #EFF6FF 100%);
            border: 2px solid #3B82F6;
            border-radius: 20px;
            padding: 32px 28px;
            box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.18);
            min-height: 250px;
        ">
            <h1 style="font-size: 3rem; margin: 0 0 12px 0;">📊</h1>
            <h2 style="color: #1E3A8A; margin: 0 0 14px 0; font-size: 1.55rem;">AI 기반 행사 자동 설계 대시보드</h2>
            <p style="color: #475569; font-size: 1.02rem; line-height: 1.65; margin: 0;">
                이벤트 목적과 예산을 입력하면 실시간 입체 디지털 트윈 조감도를 생성합니다.<br>
                AI 챗봇 대화를 통해 행사장의 무대, 부스, 푸드존 배치를 실시간으로 자율 편집하세요.
            </p>
        </div>
        """
        st.markdown(dash_card_html, unsafe_allow_html=True)
        st.markdown("<div style='margin-top: 12px;'>", unsafe_allow_html=True)
        if st.button("👉 AI 행사 설계 대시보드로 이동하기", key="btn_click_dash_full", type="primary", use_container_width=True):
            st.session_state['previous_page'] = 'home'
            st.session_state['page'] = 'dashboard'
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_rep:
        rep_card_html = """
        <div style="
            background: linear-gradient(135deg, #FFFFFF 0%, #F0FDF4 100%);
            border: 2px solid #10B981;
            border-radius: 20px;
            padding: 32px 28px;
            box-shadow: 0 10px 25px -5px rgba(16, 185, 129, 0.18);
            min-height: 250px;
        ">
            <h1 style="font-size: 3rem; margin: 0 0 12px 0;">📄</h1>
            <h2 style="color: #065F46; margin: 0 0 14px 0; font-size: 1.55rem;">AI 종합 분석 보고서</h2>
            <p style="color: #475569; font-size: 1.02rem; line-height: 1.65; margin: 0;">
                설계된 행사장 배치안을 기반으로 직장 상사에게 즉시 보고 가능한 보고서를 자동 생성합니다.<br>
                공간 안전성, 동선 효율성 및 AI 개선 권장사항을 종합 리포트로 다운로드하세요.
            </p>
        </div>
        """
        st.markdown(rep_card_html, unsafe_allow_html=True)
        st.markdown("<div style='margin-top: 12px;'>", unsafe_allow_html=True)
        if st.button("👉 AI 종합 보고서로 이동하기", key="btn_click_rep_full", type="secondary", use_container_width=True):
            st.session_state['previous_page'] = 'home'
            st.session_state['page'] = 'report'
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state['page'] == 'dashboard':
    st.markdown("## 📊 AI 디지털 트윈 공간 설계 대시보드")
    st.caption("🏢 전국 체육관, 공원, 광장, 컨벤션 센터 맞춤 2D/3D 입체 디지털 트윈 공간 스튜디오입니다.")

    VENUE_PRESETS = [
        "서울 올림픽공원 잔디마당 (100m x 72m)",
        "서울 잠실 실내체육관 (80m x 60m)",
        "부산 벡스코 제1전시장 (120m x 90m)",
        "인천 문학경기장 주경기장 (110m x 85m)",
        "대구 두류공원 야외음악당 (90m x 70m)",
        "광주 김대중컨벤션센터 (100m x 80m)",
        "직접 입력"
    ]

    with st.expander("📌 행사 기본 정보 및 전국 장소 규격 설정", expanded=not st.session_state['digital_twin_generated']):
        with st.form("event_input_form"):
            ic1, ic2, ic3 = st.columns(3)
            with ic1:
                e_name = st.text_input("이벤트 이름", value=st.session_state['event_name'])
                e_purpose = st.selectbox("이벤트 목적", ["축제/공연", "박람회/전시", "지역 문화 활성화", "기업 행사", "체육 대회"], index=0)
            with ic2:
                e_visitors = st.number_input("예상 방문객 수 (명)", value=st.session_state['event_visitors'], step=500)
                e_budget = st.text_input("예산", value=st.session_state['event_budget'])
            with ic3:
                venue_choice = st.selectbox("장소 선택 (전국 주요 체육관/공원/광장)", VENUE_PRESETS, index=0)
                if venue_choice == "직접 입력":
                    e_location = st.text_input("장소 직접 입력", value="서울 광화문 광장 (120m x 50m)")
                else:
                    e_location = venue_choice
                e_duration = st.text_input("진행 시간", value=st.session_state['event_duration'])

            btn_gen = st.form_submit_button("✨ AI 이벤트 공간 디지털 트윈 생성", type="primary", use_container_width=True)
            if btn_gen:
                st.session_state['event_name'] = e_name
                st.session_state['event_purpose'] = e_purpose
                st.session_state['event_visitors'] = e_visitors
                st.session_state['event_budget'] = e_budget
                st.session_state['event_location'] = e_location
                st.session_state['event_duration'] = e_duration
                st.session_state['digital_twin_generated'] = True
                st.session_state['facilities'] = DEFAULT_FACILITIES.copy()
                st.toast(f"'{e_location}' 공간 규격에 입각한 디지털 트윈 공간이 자동 생성되었습니다!")

    if not st.session_state['digital_twin_generated']:
        st.info("👆 위 '행사 기본 정보 및 전국 장소 규격 설정'을 확인하고 [✨ AI 이벤트 공간 디지털 트윈 생성] 버튼을 누르시면 선택하신 장소에 맞춰 공간 도면이 펼쳐집니다.")
    else:
        st.markdown(f"""
            <div style="background-color: #FFFFFF; padding: 12px 20px; border-radius: 12px; border: 1px solid #CBD5E1; margin-bottom: 15px; display: flex; justify-content: space-between; font-size:0.92rem; flex-wrap: wrap;">
                <span>🎪 <b>행사명:</b> {st.session_state['event_name']}</span>
                <span>🎯 <b>목적:</b> {st.session_state['event_purpose']}</span>
                <span>👥 <b>예상 인원:</b> {st.session_state['event_visitors']:,}명</span>
                <span>💰 <b>예산:</b> {st.session_state['event_budget']}</span>
                <span>📍 <b>설정 장소:</b> {st.session_state['event_location']}</span>
            </div>
        """, unsafe_allow_html=True)

        v_col1, v_col2, v_col3 = st.columns([2.5, 1.4, 1.1])
        with v_col1:
            view_choice = st.radio(
                "도면 시각화 선택",
                ["📐 2D 평면 설계도 (Floor Plan)", "🎪 입체 조감도 (Illustrated Map)"],
                horizontal=True,
                index=0 if st.session_state['view_mode'] == '2D_PLAN' else 1
            )
            if "2D 평면" in view_choice:
                st.session_state['view_mode'] = '2D_PLAN'
            else:
                st.session_state['view_mode'] = '3D_ISO'

        with v_col2:
            st.session_state['show_crowd_flow'] = st.toggle("🔥 관람객 이동 동선 및 혼잡도 시각화", value=st.session_state['show_crowd_flow'])
        
        with v_col3:
            st.session_state['show_grid'] = st.checkbox("10m 거리 격자", value=st.session_state['show_grid'])

        if st.session_state['show_crowd_flow']:
            st.markdown("""
            <div class="legend-card">
                <div style="font-weight: bold; margin-bottom: 6px; color: #38BDF8; font-size: 0.9rem;">
                    🗺️ 관람객 혼잡도 및 동선 시각화 범례 (Crowd Density & Pedestrian HUD)
                </div>
                <div>
                    <span class="legend-item"><span class="legend-dot" style="background-color: #EF4444; box-shadow: 0 0 8px #EF4444;"></span> 🔴 고혼잡/병목 (밀집도 85%+ 메인 무대)</span>
                    <span class="legend-item"><span class="legend-dot" style="background-color: #F59E0B; box-shadow: 0 0 8px #F59E0B;"></span> 🟡 중혼잡/대기열 (밀집도 50~80% 푸드존)</span>
                    <span class="legend-item"><span class="legend-dot" style="background-color: #10B981; box-shadow: 0 0 8px #10B981;"></span> 🟢 원활/휴게 구역 (잔디 광장)</span>
                    <span class="legend-item"><span class="legend-dot" style="background-color: #38BDF8;"></span> 🔵 주요 이동 점진 벡터</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        col_main_left, col_main_right = st.columns([2.4, 1])

        with col_main_left:
            st.markdown("### 🏢 행사 공간 디지털 트윈 (Spatial Twin)")
            st.caption("💡 **아래 시설 선택 버튼을 누르거나 오른쪽에서 위치/크기를 조작**하면 도면에 즉시 반영됩니다!")
            
            facs = st.session_state['facilities']
            mode = st.session_state['view_mode']
            show_flow = st.session_state['show_crowd_flow']

            sorted_keys = sorted(facs.keys(), key=lambda k: facs[k]['y'])

            bg_color = "#0F172A" if mode == '2D_PLAN' else "#1E3A1E"
            grid_stroke = "#1E293B" if mode == '2D_PLAN' else "#2D5A27"
            wall_border_color = "#38BDF8" if mode == '2D_PLAN' else "#22C55E"

            svg_items = []

            # 1. Base Grid Layer
            if st.session_state['show_grid']:
                grid_lines = []
                for gx in range(100, 950, 80):
                    grid_lines.append(f'<line x1="{gx}" y1="80" x2="{gx}" y2="660" stroke="{grid_stroke}" stroke-width="1.5" stroke-dasharray="4,4"/>')
                for gy in range(80, 670, 70):
                    grid_lines.append(f'<line x1="100" y1="{gy}" x2="900" y2="{gy}" stroke="{grid_stroke}" stroke-width="1.5" stroke-dasharray="4,4"/>')
                svg_items.append("\n".join(grid_lines))

            # 2. Render Facilities
            for key in sorted_keys:
                f = facs[key]
                is_sel = (st.session_state['selected_facility'] == key)
                stroke_clr = "#F59E0B" if is_sel else ("#FFFFFF" if mode == '3D_ISO' else "#38BDF8")
                stroke_w = "6" if is_sel else "2.5"
                pulse_filter = 'filter="drop-shadow(0px 0px 12px #F59E0B)"' if is_sel else ''

                x, y, w, h = f['x'], f['y'], f['w'], f['h']
                icon = f.get('icon', '🎪')
                w_m = f.get('w_m', 15)
                h_m = f.get('h_m', 10)
                fac_name = f['name']

                if mode == '2D_PLAN':
                    sel_rect = f'<rect x="{x - w//2 - 4}" y="{y - h//2 - 4}" width="{w + 8}" height="{h + 8}" rx="12" fill="none" stroke="#F59E0B" stroke-width="2" stroke-dasharray="6,4"/>' if is_sel else ''
                    plan_box = f"""
                    <g class="interactive-fac" {pulse_filter}>
                        <rect x="{x - w//2}" y="{y - h//2}" width="{w}" height="{h}" rx="10" fill="#1E293B" fill-opacity="0.95" stroke="{stroke_clr}" stroke-width="{stroke_w}"/>
                        <line x1="{x - w//2}" y1="{y - h//2}" x2="{x + w//2}" y2="{y + h//2}" stroke="#38BDF8" stroke-opacity="0.25" stroke-width="1"/>
                        <line x1="{x + w//2}" y1="{y - h//2}" x2="{x - w//2}" y2="{y + h//2}" stroke="#38BDF8" stroke-opacity="0.25" stroke-width="1"/>
                        {sel_rect}
                        <text x="{x}" y="{y - 4}" fill="#F8FAFC" font-size="14" font-weight="bold" text-anchor="middle">{icon} {fac_name}</text>
                        <text x="{x}" y="{y + 16}" fill="#94A3B8" font-size="11" font-weight="600" text-anchor="middle">{w_m}m × {h_m}m</text>
                    </g>
                    """
                    svg_items.append(plan_box)

                else:
                    hex_color = f.get('hex', '#3B82F6')
                    top_y = y - 18
                    shadow = f'<ellipse cx="{x}" cy="{y + h//3}" rx="{w//2 + 8}" ry="{h//4}" fill="#000000" fill-opacity="0.4"/>'
                    sel_rect_3d = f'<rect x="{x - w//2 - 5}" y="{top_y - h//2 - 5}" width="{w + 10}" height="{h + 10}" rx="16" fill="none" stroke="#F59E0B" stroke-width="3" stroke-dasharray="6,4"/>' if is_sel else ''
                    
                    building_body = f"""
                    <g class="interactive-fac" {pulse_filter}>
                        {shadow}
                        <rect x="{x - w//2}" y="{top_y - h//2}" width="{w}" height="{h}" rx="14" fill="{hex_color}" stroke="{stroke_clr}" stroke-width="{stroke_w}"/>
                        {sel_rect_3d}
                        <g transform="translate({x}, {top_y})">
                            <rect x="-75" y="-16" width="150" height="32" rx="16" fill="#FFFFFF" fill-opacity="0.95" stroke="{hex_color}" stroke-width="2.5"/>
                            <text x="0" y="5" fill="#0F172A" font-size="12" font-weight="bold" text-anchor="middle">{icon} {fac_name}</text>
                        </g>
                    </g>
                    """
                    svg_items.append(building_body)

            # 3. Crowd Flow Layer
            if show_flow:
                gate_x, gate_y = facs['exit']['x'], facs['exit']['y']
                info_x, info_y = facs['info']['x'], facs['info']['y']
                stage_x, stage_y = facs['stage']['x'], facs['stage']['y']
                food_x, food_y = facs['food']['x'], facs['food']['y']
                rest_x, rest_y = facs['rest']['x'], facs['rest']['y']
                toilet_x, toilet_y = facs['toilet']['x'], facs['toilet']['y']
                med_x, med_y = facs['medical']['x'], facs['medical']['y']

                flow_layer = f"""
                <defs>
                    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="#38BDF8"/>
                    </marker>
                    <marker id="arrow-green" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="#10B981"/>
                    </marker>
                </defs>

                <!-- Congestion Heatmap -->
                <ellipse cx="{stage_x}" cy="{stage_y + 110}" rx="230" ry="85" fill="#EF4444" fill-opacity="0.35" stroke="#DC2626" stroke-width="2.5" stroke-dasharray="6,4"/>
                <text x="{stage_x}" y="{stage_y + 115}" fill="#FFFFFF" font-size="12" font-weight="900" text-anchor="middle">🔥 관람객 인파 최고 밀집 구역 (메인 공연장)</text>

                <ellipse cx="{food_x + 90}" cy="{food_y}" rx="120" ry="70" fill="#F59E0B" fill-opacity="0.3" stroke="#D97706" stroke-width="2"/>
                <text x="{food_x + 90}" y="{food_y + 4}" fill="#FFFFFF" font-size="11" font-weight="bold" text-anchor="middle">⚠️ 식음료 대기 동선 정체 주의</text>

                <ellipse cx="{rest_x}" cy="{rest_y}" rx="170" ry="100" fill="#10B981" fill-opacity="0.2" stroke="#059669" stroke-width="2" stroke-dasharray="4,4"/>
                <text x="{rest_x}" y="{rest_y}" fill="#FFFFFF" font-size="11" font-weight="bold" text-anchor="middle">🟢 유연 분산 휴게 구역</text>

                <!-- Pedestrian Path Vectors -->
                <path d="M {gate_x} {gate_y - 20} Q {gate_x} {info_y + 50} {info_x} {info_y + 35}" fill="none" stroke="#38BDF8" stroke-width="4.5" stroke-dasharray="8,6" marker-end="url(#arrow)"/>
                <path d="M {info_x} {info_y - 35} Q {info_x - 120} {rest_y + 60} {stage_x - 60} {stage_y + 150}" fill="none" stroke="#38BDF8" stroke-width="4.5" stroke-dasharray="8,6" marker-end="url(#arrow)"/>
                <path d="M {info_x - 60} {info_y} Q {food_x + 130} {food_y + 90} {food_x + 60} {food_y + 50}" fill="none" stroke="#F59E0B" stroke-width="4" stroke-dasharray="8,6" marker-end="url(#arrow)"/>
                <path d="M {rest_x + 100} {rest_y} Q {toilet_x - 80} {toilet_y + 40} {toilet_x - 60} {toilet_y}" fill="none" stroke="#10B981" stroke-width="3.5" stroke-dasharray="6,4" marker-end="url(#arrow-green)"/>
                """
                svg_items.append(flow_layer)

            all_svg_rendered = "\n".join(svg_items)

            selected_fac_info = facs[st.session_state['selected_facility']]
            selected_fac_display = f"{selected_fac_info['icon']} {selected_fac_info['name']}"
            view_mode_label = '2D 평면 설계도' if mode == '2D_PLAN' else '입체 조감도'
            flow_status_label = '🔥 동선/혼잡도 활성' if show_flow else 'LIVE Digital Twin'
            flow_badge_bg = '#EF4444' if show_flow else '#0284C7'

            digital_twin_html = f"""
            <div style="position: relative; width: 100%; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.4); border: 2px solid {wall_border_color}; background-color: {bg_color};">
                <div style="background: rgba(15, 23, 42, 0.95); color: #F8FAFC; padding: 10px 20px; font-size: 0.88rem; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="color: #38BDF8; font-weight: bold;">📐 Spatial Twin Studio</span> | 
                        <span>모드: <b>{view_mode_label}</b></span> | 
                        <span>선택: <b style="color:#F59E0B;">{selected_fac_display}</b></span>
                    </div>
                    <div>
                        <span style="background: {flow_badge_bg}; color: #FFF; padding: 4px 12px; border-radius: 12px; font-size: 0.78rem; font-weight: bold;">
                            {flow_status_label}
                        </span>
                    </div>
                </div>

                <svg viewBox="0 0 1000 720" style="width: 100%; height: auto; background-color: {bg_color}; display: block;">
                    <rect x="30" y="30" width="940" height="660" rx="16" fill="none" stroke="{wall_border_color}" stroke-width="2"/>
                    <rect x="50" y="50" width="900" height="620" rx="12" fill="none" stroke="#F59E0B" stroke-width="2" stroke-dasharray="10,6"/>

                    {all_svg_rendered}

                    <!-- Compass Rose -->
                    <g transform="translate(900, 100)">
                        <circle cx="0" cy="0" r="28" fill="#0F172A" fill-opacity="0.9" stroke="#38BDF8" stroke-width="2"/>
                        <text x="0" y="-12" font-size="12" fill="#EF4444" font-weight="900" text-anchor="middle">N</text>
                        <text x="0" y="20" font-size="10" fill="#94A3B8" font-weight="bold" text-anchor="middle">S</text>
                        <text x="16" y="4" font-size="10" fill="#94A3B8" font-weight="bold" text-anchor="middle">E</text>
                        <text x="-16" y="4" font-size="10" fill="#94A3B8" font-weight="bold" text-anchor="middle">W</text>
                    </g>

                    <!-- Scale Bar -->
                    <g transform="translate(740, 640)">
                        <rect x="0" y="0" width="220" height="36" rx="8" fill="#0F172A" fill-opacity="0.88" stroke="#475569" stroke-width="1.5"/>
                        <line x1="20" y1="20" x2="180" y2="20" stroke="#38BDF8" stroke-width="3"/>
                        <line x1="20" y1="12" x2="20" y2="24" stroke="#38BDF8" stroke-width="2"/>
                        <line x1="100" y1="15" x2="100" y2="24" stroke="#38BDF8" stroke-width="1.5"/>
                        <line x1="180" y1="12" x2="180" y2="24" stroke="#38BDF8" stroke-width="2"/>
                        <text x="20" y="10" font-size="10" fill="#94A3B8" font-weight="bold">0m</text>
                        <text x="100" y="10" font-size="10" fill="#94A3B8" font-weight="bold">10m</text>
                        <text x="180" y="10" font-size="10" fill="#38BDF8" font-weight="bold">20m Scale</text>
                    </g>
                </svg>
            </div>
            """
            st.components.v1.html(digital_twin_html, height=560, scrolling=False)

            st.markdown("**🎯 아래 원하시는 시설 단추를 눌러 대상 시설을 조작하세요:**")
            fac_keys = list(facs.keys())
            f_cols = st.columns(4)
            for i, key in enumerate(fac_keys):
                fac_item = facs[key]
                with f_cols[i % 4]:
                    is_selected = (st.session_state['selected_facility'] == key)
                    btn_type = "primary" if is_selected else "secondary"
                    if st.button(f"{fac_item['icon']} {fac_item['name']}", key=f"btn_fac_{key}", type=btn_type, use_container_width=True):
                        st.session_state['selected_facility'] = key
                        st.rerun()

        with col_main_right:
            selected_key = st.session_state['selected_facility']
            current_fac = facs[selected_key]
            
            w_m_val = current_fac.get('w_m', 15)
            h_m_val = current_fac.get('h_m', 10)
            h_3d_m_val = current_fac.get('h_3d_m', 3)
            icon_val = current_fac.get('icon', '🎪')

            st.markdown("### 🎛️ 선택 시설 좌표 및 규격 조정")
            st.info(f"현재 선택됨: **{icon_val} {current_fac['name']}**")

            new_x = st.slider("X 좌표 (가로 위치)", min_value=120, max_value=880, value=current_fac['x'], step=10, key=f"sl_x_{selected_key}")
            new_y = st.slider("Y 좌표 (세로 위치)", min_value=100, max_value=650, value=current_fac['y'], step=10, key=f"sl_y_{selected_key}")
            
            new_w_m = st.slider("가로 규격 (m)", min_value=5, max_value=50, value=current_fac['w_m'], step=1, key=f"sl_wm_{selected_key}")
            new_h_m = st.slider("세로 규격 (m)", min_value=4, max_value=40, value=current_fac['h_m'], step=1, key=f"sl_hm_{selected_key}")

            if (new_x != current_fac['x'] or new_y != current_fac['y'] or 
                new_w_m != current_fac['w_m'] or new_h_m != current_fac['h_m']):
                current_fac['x'] = new_x
                current_fac['y'] = new_y
                current_fac['w_m'] = new_w_m
                current_fac['h_m'] = new_h_m
                current_fac['w'] = new_w_m * 10
                current_fac['h'] = new_h_m * 10
                current_fac['reason'] = f"사용자 커스텀 조정: ({new_x}, {new_y}) 좌표 및 {new_w_m}m×{new_h_m}m 규격 적용됨."
                st.rerun()

            st.caption("⚡ **빠른 방향 이동 단추:**")
            d_col1, d_col2, d_col3, d_col4 = st.columns(4)
            with d_col1:
                if st.button("⬆️ 북쪽", key="mv_n", use_container_width=True):
                    current_fac['y'] = max(100, current_fac['y'] - 50)
                    st.rerun()
            with d_col2:
                if st.button("⬇️ 남쪽", key="mv_s", use_container_width=True):
                    current_fac['y'] = min(650, current_fac['y'] + 50)
                    st.rerun()
            with d_col3:
                if st.button("⬅️ 서쪽", key="mv_w", use_container_width=True):
                    current_fac['x'] = max(120, current_fac['x'] - 60)
                    st.rerun()
            with d_col4:
                if st.button("➡️ 동쪽", key="mv_e", use_container_width=True):
                    current_fac['x'] = min(880, current_fac['x'] + 60)
                    st.rerun()

            st.divider()

            fac_hex_color = current_fac['hex']
            fac_name_str = current_fac['name']
            fac_reason_str = current_fac['reason']
            area_m2 = w_m_val * h_m_val

            st.markdown(f"""
                <div class="reason-box">
                    <h4 style="color: {fac_hex_color}; margin-top: 0;">{icon_val} {fac_name_str}</h4>
                    <p style="color: #0F172A; font-size: 0.9rem; margin-bottom: 8px;">
                        • <b>실제 가로×세로:</b> {w_m_val}m × {h_m_val}m<br>
                        • <b>점유 면적:</b> {area_m2} ㎡<br>
                        • <b>설치 고도:</b> {h_3d_m_val}m
                    </p>
                    <hr style="margin: 8px 0; border: 0; border-top: 1px solid #BAE6FD;">
                    <p style="color: #334155; font-size: 0.9rem; line-height: 1.5; margin: 0;">
                        <b>[AI 공간 배치 근거 요약]</b><br>
                        {fac_reason_str}
                    </p>
                </div>
            """, unsafe_allow_html=True)

            st.divider()

            st.markdown("### 💬 Claude-Spatial AI 챗봇")
            st.caption("자연어로 '푸드존을 더 멀리 이동해줘', '화장실을 의료센터 옆으로 옮겨줘' 등을 입력해 보세요!")

            chat_box = st.container(height=240)
            with chat_box:
                for message in st.session_state['chat_messages']:
                    with st.chat_message(message["role"]):
                        st.write(message["content"])

            if user_prompt := st.chat_input("예: '푸드존을 메인 무대와 멀리 이동해줘'"):
                st.session_state['chat_messages'].append({"role": "user", "content": user_prompt})
                ai_reply = parse_and_apply_ai_command(user_prompt)
                st.session_state['chat_messages'].append({"role": "assistant", "content": ai_reply})
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🔥 AI 군중 시뮬레이션 & 병목 분석")
        
        sim_col1, sim_col2 = st.columns([1.2, 1])
        with sim_col1:
            if st.button("🚨 Real-Time 혼잡도 Heatmap 실행", type="primary", use_container_width=True):
                st.session_state['simulated'] = True
                st.toast("AI 군중 유동 및 병목 구간 시뮬레이션이 성공적으로 완료되었습니다!")

        with sim_col2:
            if st.button("🔄 배치 상태 리셋", type="secondary", use_container_width=True):
                st.session_state['facilities'] = DEFAULT_FACILITIES.copy()
                st.toast("도면 위치 정보가 기본값으로 초기화되었습니다.")
                st.rerun()

        if st.session_state.get('simulated', True):
            np.random.seed(42)
            sim_grid = np.random.rand(10, 10) * 45
            sim_grid[1:3, 4:6] += 50  # 메인 무대 인파 밀집
            sim_grid[4:6, 1:3] += 35  # 푸드존 대기열

            fig_heat = px.imshow(
                sim_grid,
                labels=dict(x="X 축 구역 (10m)", y="Y 축 구역 (10m)", color="밀집도 (인원/100㎡)"),
                x=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
                y=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
                color_continuous_scale="Reds",
                aspect="auto",
                title="🔥 행사구역 단위면적당 인파 밀집도 Heatmap"
            )
            fig_heat.update_layout(
                margin=dict(l=20, r=20, t=40, b=20),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#334155")
            )
            st.plotly_chart(fig_heat, use_container_width=True)

elif st.session_state['page'] == 'report':
    st.markdown("## 📄 AI 종합 공간 분석 보고서")
    st.caption("디지털 트윈으로 자동 계산된 행사장 공간 안전성, 동선 유연성, 예산 분배 최적화 보고서입니다.")
    st.markdown("<br>", unsafe_allow_html=True)

    # Top Summary Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("종합 안전 점수", "96.8 점", "+4.2% (개선됨)")
    with m2:
        st.metric("평균 동선 병목도", "14.2 %", "-18.5% (감소)")
    with m3:
        st.metric("비상 대피 골든타임", "2분 10초", "안전기준 3분 이내")
    with m4:
        st.metric("공간 이용 효율성", "89.5 %", "+6.1% (최적화)")

    st.divider()

    col_rep_l, col_rep_r = st.columns([1.5, 1])

    with col_rep_l:
        st.markdown("### 📊 시간대별 관람객 유입 및 공간 혼잡 예측")
        
        hours = [f"{h:02d}:00" for h in range(12, 22)]
        visitors_pred = [800, 1500, 2800, 4200, 4900, 5000, 4700, 3800, 2100, 900]
        safety_index = [99, 98, 95, 91, 88, 87, 90, 94, 97, 99]

        df_trend = pd.DataFrame({
            "시간": hours,
            "예상 관람 인원": visitors_pred,
            "안전 유연성 지수": safety_index
        })

        fig_line = px.line(
            df_trend, x="시간", y=["예상 관람 인원", "안전 유연성 지수"],
            markers=True,
            title="📈 행사 시간대별 인파 밀집 및 안전 지수 변동 추이",
            color_discrete_sequence=["#3B82F6", "#10B981"]
        )
        fig_line.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_line, use_container_width=True)

        st.markdown("""
        <div class="custom-card">
            <h4>💡 AI 아키텍트 분석 종합 총평</h4>
            <p style="color:#475569; line-height:1.7;">
                • <b>메인 무대 & 잔디 휴게 광장 간격:</b> 무대 전면 관람객 수용 공간이 충분히 확보되어 피크 타임(16:00~18:00)에도 안정적인 인파 흐름이 유지됩니다.<br>
                • <b>푸드존 연기 및 대기열 분리:</b> 서쪽 독립 배치로 인해 주 동선과의 간섭이 최소화되었으며, 대기열 정체 위험도가 32.4% 감소했습니다.<br>
                • <b>응급/위생 시설 접근성:</b> 동쪽 비상 도로선과의 인접 배치로 긴급 구급차 진출입 시간이 골든타임(3분) 내에 완벽히 유지됩니다.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_rep_r:
        st.markdown("### 💰 시설 예산 및 공간 점유 비율")
        
        budget_df = pd.DataFrame({
            "구분": ["메인 무대/음향", "체험 부스", "푸드존 지원", "휴게/인프라", "안전/의료/위생"],
            "금액(만원)": [2200, 900, 600, 800, 500]
        })

        fig_pie = px.pie(
            budget_df, values="금액(만원)", names="구분",
            hole=0.4,
            title="🎯 예산 집행 비율",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown("### 📥 보고서 내보내기")
        st.download_button(
            label="📄 AI 종합 보고서 (PDF) 다운로드",
            data=f"이벤트 아키텍트 AI 보고서\n행사명: {st.session_state['event_name']}\n장소: {st.session_state['event_location']}\n안전점수: 96.8점",
            file_name="event_architecture_report.txt",
            mime="text/plain",
            use_container_width=True,
            type="primary"
        )

elif st.session_state['page'] == 'settings':
    st.markdown("## ⚙️ 시스템 및 AI 에이전트 설정")
    st.caption("공간 시뮬레이션 엔진 및 플랫폼 환경 설정을 관리합니다.")
    st.markdown("<br>", unsafe_allow_html=True)

    s_col1, s_col2 = st.columns(2)

    with s_col1:
        st.markdown("### 🤖 AI 아키텍트 모델 설정")
        st.selectbox("공간 추론 엔진 (Spatial AI Engine)", ["Claude-Spatial v3.5 (추천)", "GPT-4o Spatial Vision", "Gemini 1.5 Pro Spatial Mode"])
        st.slider("자율 배치 창의성 (Temperature)", min_value=0.0, max_value=1.0, value=0.3, step=0.05)
        st.checkbox("실시간 자연어 명령 오토 세이브 활성화", value=True)
        st.checkbox("비상 대피로 자동 감지 알람", value=True)

    with s_col2:
        st.markdown("### 📐 디지털 트윈 그리드 및 디스플레이")
        st.selectbox("기본 그리드 단위", ["10m x 10m (표준)", "5m x 5m (정밀)", "20m x 20m (대형 광장)"])
        st.selectbox("기본 도면 뷰 모드", ["2D 평면 설계도 (Floor Plan)", "🎪 입체 조감도 (Illustrated Map)"])
        st.text_input("담당 기획자 성명", value=st.session_state['username'])
        st.text_input("소속 기관/회사", value="이벤트 아키텍트 기획본부")

    st.divider()
    if st.button("💾 설정 내용 저장하기", type="primary"):
        st.toast("설정이 성공적으로 저장되었습니다!")

st.markdown("<br><hr style='border-top: 1px solid #E2E8F0;'><center style='color:#94A3B8; font-size:0.85rem;'>© 2026 Event Architect AI Platform. All rights reserved.</center>", unsafe_allow_html=True)
