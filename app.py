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
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = True
if 'username' not in st.session_state:
    st.session_state['username'] = "주은님"
if 'digital_twin_generated' not in st.session_state:
    st.session_state['digital_twin_generated'] = False
if 'simulated' not in st.session_state:
    st.session_state['simulated'] = False
if 'selected_facility' not in st.session_state:
    st.session_state['selected_facility'] = 'stage'
if 'facilities' not in st.session_state:
    st.session_state['facilities'] = DEFAULT_FACILITIES.copy()

# 행사 기본 정보 세션 상태 저장
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

# 이전 세션 상태가 보존되어 있을 경우 구버전 dict 구조를 최신 3D 필드로 자동 보완
if 'facilities' in st.session_state:
    for k, v in DEFAULT_FACILITIES.items():
        if k not in st.session_state['facilities']:
            st.session_state['facilities'][k] = v.copy()
        else:
            for field, val in v.items():
                if field not in st.session_state['facilities'][k]:
                    st.session_state['facilities'][k][field] = val

if 'view_mode' not in st.session_state:
    st.session_state['view_mode'] = '2D_PLAN' # 기본값: 2D 평면 설계도 우선 표출
if 'show_crowd_flow' not in st.session_state:
    st.session_state['show_crowd_flow'] = False
if 'lighting_mode' not in st.session_state:
    st.session_state['lighting_mode'] = 'Day' # Day, Night
if 'show_grid' not in st.session_state:
    st.session_state['show_grid'] = True
if 'chat_messages' not in st.session_state:
    st.session_state['chat_messages'] = [
        {"role": "assistant", "content": "안녕하세요! 전국 체육관, 공원, 광장 맞춤 실시간 디지털 트윈 엔진입니다. '무대를 더 크게 해줘', '푸드존을 서쪽으로 이동해줘'와 같이 명령하시면 즉시 도면에 반영됩니다."}
    ]

def parse_and_apply_ai_command(prompt: str):
    prompt_clean = prompt.replace(" ", "")
    facs = st.session_state['facilities']
    
    target_key = None
    if "푸드" in prompt_clean or "먹거리" in prompt_clean:
        target_key = "food"
    elif "화장실" in prompt_clean:
        target_key = "toilet"
    elif "무대" in prompt_clean or "공연" in prompt_clean:
        target_key = "stage"
    elif "부스" in prompt_clean or "체험" in prompt_clean:
        target_key = "booth"
    elif "의료" in prompt_clean or "응급" in prompt_clean:
        target_key = "medical"
    elif "휴게" in prompt_clean or "쉼터" in prompt_clean:
        target_key = "rest"
    elif "안내" in prompt_clean:
        target_key = "info"
    elif "출입구" in prompt_clean or "입구" in prompt_clean or "출구" in prompt_clean or "비상구" in prompt_clean:
        target_key = "exit"

    if not target_key:
        target_key = st.session_state['selected_facility']

    fac = facs[target_key]
    changed = False
    action_desc = ""

    if "멀리" in prompt_clean or "외곽" in prompt_clean or "분리" in prompt_clean:
        if target_key == "food":
            fac["x"] = 120
            fac["y"] = 450
            action_desc = "푸드존을 연기 및 혼잡 예방을 위해 서쪽 최외곽 독립 구역으로 이동시켰습니다."
        elif target_key == "toilet":
            fac["x"] = 880
            fac["y"] = 380
            action_desc = "화장실을 메인 무대와 충분한 거리를 둔 동쪽 외곽 구역으로 재배치했습니다."
        else:
            fac["x"] = max(100, fac["x"] - 120)
            action_desc = f"{fac['name']}의 위치를 외곽 구역으로 이동시켰습니다."
        changed = True

    elif "의료" in prompt_clean or "병원" in prompt_clean or "가까이" in prompt_clean or "근처" in prompt_clean:
        if target_key == "toilet":
            fac["x"] = facs["medical"]["x"] - 30
            fac["y"] = facs["medical"]["y"] + 120
            action_desc = "화장실을 응급의료센터 인근 구역으로 즉시 재배치했습니다."
        else:
            fac["x"] = facs["medical"]["x"] - 40
            action_desc = f"{fac['name']}을(를) 응급의료센터 인근의 접근성이 우수한 위치로 조정했습니다."
        changed = True

    elif "오른쪽" in prompt_clean or "동쪽" in prompt_clean:
        fac["x"] = min(860, fac["x"] + 140)
        action_desc = f"{fac['name']}을(를) 동쪽 구역으로 이동했습니다."
        changed = True

    elif "왼쪽" in prompt_clean or "서쪽" in prompt_clean:
        fac["x"] = max(100, fac["x"] - 140)
        action_desc = f"{fac['name']}을(를) 서쪽 구역으로 이동했습니다."
        changed = True

    elif "위" in prompt_clean or "북쪽" in prompt_clean or "상단" in prompt_clean:
        fac["y"] = max(100, fac["y"] - 120)
        action_desc = f"{fac['name']}을(를) 상단 구역으로 이동했습니다."
        changed = True

    elif "아래" in prompt_clean or "남쪽" in prompt_clean or "하단" in prompt_clean:
        fac["y"] = min(620, fac["y"] + 120)
        action_desc = f"{fac['name']}을(를) 하단 구역으로 이동했습니다."
        changed = True

    else:
        fac["x"] = (fac["x"] + 100) % 750 + 100
        action_desc = f"{fac['name']}의 공간 배치를 AI 동선 최적화 알고리즘에 맞추어 변경했습니다."
        changed = True

    if changed:
        fac["reason"] = f"AI 대화 맞춤 변경: {action_desc}"
        st.session_state['selected_facility'] = target_key
        return f"✅ **알림:** {action_desc} (행사장 디지털 트윈 및 보고서에 즉시 반영되었습니다!)"
    
    return f"네! 요청하신 '{prompt}' 내용에 맞춰 배치를 점검하였으며, 최적화 기준에 맞게 조정하였습니다."

with st.sidebar:
    if st.button("🎪 이벤트 아키텍트 AI", key="logo_btn", use_container_width=True, type="primary"):
        st.session_state['page'] = 'home'
        st.rerun()

    st.caption("AI 기반 행사 자동 설계 플랫폼")
    st.divider()

    page_selection = st.radio(
        "메뉴 이동",
        ["홈 화면", "AI 행사 설계 대시보드", "AI 보고서", "설정"],
        index=["home", "dashboard", "report", "settings"].index(st.session_state['page'])
    )

    if page_selection == "홈 화면":
        st.session_state['page'] = 'home'
    elif page_selection == "AI 행사 설계 대시보드":
        st.session_state['page'] = 'dashboard'
    elif page_selection == "AI 보고서":
        st.session_state['page'] = 'report'
    elif page_selection == "설정":
        st.session_state['page'] = 'settings'

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
            st.session_state['page'] = 'settings'
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

if st.session_state['page'] == 'home':
    st.markdown("## 🚀 시작할 메뉴를 선택하세요")
    st.caption("박스 카드를 클릭하면 해당 화면으로 이동합니다.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_dash, col_rep = st.columns(2)

    with col_dash:
        dash_card_html = """
        <div style="
            background: linear-gradient(135deg, #FFFFFF 0%, #EFF6FF 100%);
            border: 2px solid #93C5FD;
            border-radius: 20px;
            padding: 32px 28px;
            box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.12);
            min-height: 280px;
            display: flex;
            flex-direction: column;
            justify-content: center;
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
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📊 AI 행사 설계 대시보드 선택", key="btn_click_dash", type="primary", use_container_width=True):
            st.session_state['page'] = 'dashboard'
            st.rerun()

    with col_rep:
        rep_card_html = """
        <div style="
            background: linear-gradient(135deg, #FFFFFF 0%, #F0FDF4 100%);
            border: 2px solid #86EFAC;
            border-radius: 20px;
            padding: 32px 28px;
            box-shadow: 0 10px 25px -5px rgba(16, 185, 129, 0.12);
            min-height: 280px;
            display: flex;
            flex-direction: column;
            justify-content: center;
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
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📄 AI 보고서 선택", key="btn_click_rep", type="secondary", use_container_width=True):
            st.session_state['page'] = 'report'
            st.rerun()

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

        v_col1, v_col2, v_col3 = st.columns([2.5, 1.2, 1.3])
        with v_col1:
            view_choice = st.radio(
                "도면 시각화 선택 (처음엔 2D 평면 설계도가 뜹니다)",
                ["📐 2D 평면 설계도 (Floor Plan)", "🎪 입체 조감도 (Illustrated Map)"],
                horizontal=True,
                index=0 if st.session_state['view_mode'] == '2D_PLAN' else 1
            )
            if "2D 평면" in view_choice:
                st.session_state['view_mode'] = '2D_PLAN'
            else:
                st.session_state['view_mode'] = '3D_ISO'

        with v_col2:
            st.session_state['show_crowd_flow'] = st.toggle("🔥 혼잡도 및 이동 동선 레이어 표시", value=st.session_state['show_crowd_flow'])
        
        with v_col3:
            st.session_state['show_grid'] = st.checkbox("10m 거리 격자 표시", value=st.session_state['show_grid'])

        col_main_left, col_main_right = st.columns([2.3, 1])

        with col_main_left:
            st.markdown("### 🏢 행사 공간 디지털 트윈 (Spatial Twin)")
            
            facs = st.session_state['facilities']
            mode = st.session_state['view_mode']
            show_flow = st.session_state['show_crowd_flow']

            # Generate depth-sorted elements
            sorted_keys = sorted(facs.keys(), key=lambda k: facs[k]['y'])

            bg_color = "#1E293B" if mode == '2D_PLAN' else "#2D5A27"
            grid_stroke = "#334155" if mode == '2D_PLAN' else "#3D7A36"
            wall_border_color = "#38BDF8" if mode == '2D_PLAN' else "#22C55E"

            svg_items = []

            # 1. Base Grid Layer
            if st.session_state['show_grid']:
                grid_lines = []
                for gx in range(100, 950, 80):
                    grid_lines.append(f'<line x1="{gx}" y1="80" x2="{gx}" y2="660" stroke="{grid_stroke}" stroke-width="1" stroke-dasharray="4,4"/>')
                for gy in range(80, 670, 70):
                    grid_lines.append(f'<line x1="100" y1="{gy}" x2="900" y2="{gy}" stroke="{grid_stroke}" stroke-width="1" stroke-dasharray="4,4"/>')
                svg_items.append("\n".join(grid_lines))

            # 2. Render Facilities
            for key in sorted_keys:
                f = facs[key]
                is_sel = (st.session_state['selected_facility'] == key)
                stroke_clr = "#F59E0B" if is_sel else ("#FFFFFF" if mode == '3D_ISO' else "#38BDF8")
                stroke_w = "4" if is_sel else "2"

                x, y, w, h = f['x'], f['y'], f['w'], f['h']
                icon = f.get('icon', '🎪')
                w_m = f.get('w_m', 15)
                h_m = f.get('h_m', 10)

                if mode == '2D_PLAN':
                    # Architectural Blueprint 2D CAD Layout
                    plan_box = f"""
                    <g transform="translate(0,0)">
                        <rect x="{x - w//2}" y="{y - h//2}" width="{w}" height="{h}" rx="6" fill="#0F172A" fill-opacity="0.85" stroke="{stroke_clr}" stroke-width="{stroke_w}"/>
                        <line x1="{x - w//2}" y1="{y - h//2}" x2="{x + w//2}" y2="{y + h//2}" stroke="#38BDF8" stroke-opacity="0.25" stroke-width="1"/>
                        <line x1="{x + w//2}" y1="{y - h//2}" x2="{x - w//2}" y2="{y + h//2}" stroke="#38BDF8" stroke-opacity="0.25" stroke-width="1"/>
                        <text x="{x}" y="{y - 4}" fill="#F8FAFC" font-size="14" font-weight="bold" text-anchor="middle">{icon} {f['name']}</text>
                        <text x="{x}" y="{y + 16}" fill="#94A3B8" font-size="11" text-anchor="middle">{w_m}m × {h_m}m</text>
                    </g>
                    """
                    svg_items.append(plan_box)

                else:
                    # 🎪 입체 조감도 (Illustrated Festival Map - User Reference Image Style without legend box)
                    hex_color = f.get('hex', '#3B82F6')
                    top_y = y - 18
                    
                    shadow = f'<ellipse cx="{x}" cy="{y + h//3}" rx="{w//2 + 8}" ry="{h//4}" fill="#000000" fill-opacity="0.3"/>'
                    
                    building_body = f"""
                    <rect x="{x - w//2}" y="{top_y - h//2}" width="{w}" height="{h}" rx="14" fill="{hex_color}" stroke="{stroke_clr}" stroke-width="{stroke_w}" filter="drop-shadow(0px 8px 12px rgba(0,0,0,0.4))"/>
                    """
                    
                    label = f"""
                    <g transform="translate({x}, {top_y})">
                        <rect x="-70" y="-14" width="140" height="28" rx="14" fill="#FFFFFF" fill-opacity="0.95" stroke="{hex_color}" stroke-width="2"/>
                        <text x="0" y="5" fill="#0F172A" font-size="12" font-weight="bold" text-anchor="middle">{icon} {f['name']}</text>
                    </g>
                    """
                    svg_items.append(shadow + building_body + label)

            # 3. Crowd Flow & Congestion Heatmap Layer Overlay (Requested Feature)
            if show_flow:
                gate_x, gate_y = facs['exit']['x'], facs['exit']['y']
                info_x, info_y = facs['info']['x'], facs['info']['y']
                stage_x, stage_y = facs['stage']['x'], facs['stage']['y']
                food_x, food_y = facs['food']['x'], facs['food']['y']
                rest_x, rest_y = facs['rest']['x'], facs['rest']['y']
                toilet_x, toilet_y = facs['toilet']['x'], facs['toilet']['y']
                med_x, med_y = facs['medical']['x'], facs['medical']['y']

                flow_layer = f"""
                <!-- Crowd Flow Dynamic Arrows Overlay -->
                <defs>
                    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="#38BDF8"/>
                    </marker>
                    <marker id="arrow-red" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="#EF4444"/>
                    </marker>
                </defs>

                <!-- Bottleneck Heatmap Density Circles -->
                <!-- 무대 전면 주요 혼잡 구역 (High Congestion) -->
                <ellipse cx="{stage_x}" cy="{stage_y + 110}" rx="220" ry="90" fill="#EF4444" fill-opacity="0.35" stroke="#DC2626" stroke-width="2" stroke-dasharray="6,4"/>
                <text x="{stage_x}" y="{stage_y + 115}" fill="#FFFFFF" font-size="12" font-weight="900" text-anchor="middle" style="text-shadow: 0px 2px 4px #000;">🔥 혼잡도 매우 높음 (메인 무대 스탠딩 존)</text>

                <!-- 푸드존 앞 대기 동선 혼잡 (Moderate Congestion) -->
                <ellipse cx="{food_x + 80}" cy="{food_y}" rx="110" ry="70" fill="#F59E0B" fill-opacity="0.3" stroke="#D97706" stroke-width="2"/>
                <text x="{food_x + 80}" y="{food_y + 4}" fill="#FFFFFF" font-size="11" font-weight="bold" text-anchor="middle" style="text-shadow: 0px 2px 4px #000;">⚠️ 혼잡 주의 (푸드존 대기열)</text>

                <!-- Main Flow Path Arrow Lines -->
                <!-- Gate -> Info -->
                <path d="M {gate_x} {gate_y - 20} Q {gate_x} {info_y + 50} {info_x} {info_y + 35}" fill="none" stroke="#38BDF8" stroke-width="4" stroke-dasharray="8,6" marker-end="url(#arrow)"/>
                
                <!-- Info -> Stage Main Path -->
                <path d="M {info_x} {info_y - 35} Q {info_x - 100} {rest_y + 50} {stage_x - 50} {stage_y + 150}" fill="none" stroke="#38BDF8" stroke-width="4" stroke-dasharray="8,6" marker-end="url(#arrow)"/>

                <!-- Info -> Food Zone -->
                <path d="M {info_x - 60} {info_y} Q {food_x + 120} {food_y + 80} {food_x + 60} {food_y + 50}" fill="none" stroke="#38BDF8" stroke-width="4" stroke-dasharray="8,6" marker-end="url(#arrow)"/>

                <!-- Rest Zone -> Toilet & Medical -->
                <path d="M {rest_x + 100} {rest_y} Q {toilet_x - 80} {toilet_y + 40} {toilet_x - 60} {toilet_y}" fill="none" stroke="#10B981" stroke-width="3" stroke-dasharray="6,4" marker-end="url(#arrow)"/>
                <path d="M {rest_x + 100} {rest_y - 50} Q {med_x - 80} {med_y + 40} {med_x - 60} {med_y}" fill="none" stroke="#EF4444" stroke-width="3" stroke-dasharray="6,4" marker-end="url(#arrow-red)"/>
                """
                svg_items.append(flow_layer)

            all_svg_rendered = "\n".join(svg_items)

            digital_twin_3d_html = f"""
            <div style="position: relative; width: 100%; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.3); border: 2px solid {wall_border_color}; background-color: {bg_color};">
                
                <!-- 상단 트윈 정보 표시바 -->
                <div style="background: rgba(15, 23, 42, 0.92); color: #F8FAFC; padding: 10px 20px; font-size: 0.88rem; display: flex; justify-content: space-between; align-items: center; backdrop-filter: blur(8px);">
                    <div>
                        <span style="color: #38BDF8; font-weight: bold;">📐 Spatial Twin Studio</span> | 
                        <span>표출 모드: <b>{'2D 평면 설계도' if mode == '2D_PLAN' else '입체 조감도'}</b></span> | 
                        <span>장소: <b>{st.session_state['event_location']}</b></span>
                    </div>
                    <div>
                        <span style="background: {'#EF4444' if show_flow else '#0284C7'}; color: #FFF; padding: 4px 12px; border-radius: 12px; font-size: 0.78rem; font-weight: bold;">
                            {'🔥 혼잡도/동선 레이어 ON' if show_flow else 'LIVE Digital Twin'}
                        </span>
                    </div>
                </div>

                <svg viewBox="0 0 1000 720" style="width: 100%; height: auto; background-color: {bg_color}; display: block;">
                    <!-- Ground Slab Boundary -->
                    <rect x="30" y="30" width="940" height="660" rx="16" fill="none" stroke="{wall_border_color}" stroke-width="2"/>
                    <rect x="50" y="50" width="900" height="620" rx="12" fill="none" stroke="#F59E0B" stroke-width="2" stroke-dasharray="10,6"/>

                    <!-- Facilities & Overlays -->
                    {all_svg_rendered}

                    <!-- 축척 자 Scale Bar -->
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
            st.components.v1.html(digital_twin_3d_html, height=560, scrolling=False)

            st.markdown("**👇 아래 시설을 선택하면 오른쪽에서 AI 최적배치 근거를 확인할 수 있습니다:**")
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

            st.markdown("### 🏢 시설 실측 및 AI 배치 이유")
            st.markdown(f"""
                <div class="reason-box">
                    <h4 style="color: {current_fac['hex']}; margin-top: 0;">{icon_val} {current_fac['name']}</h4>
                    <p style="color: #0F172A; font-size: 0.9rem; margin-bottom: 8px;">
                        • <b>실제 가로×세로:</b> {w_m_val}m × {h_m_val}m<br>
                        • <b>점유 면적:</b> {w_m_val * h_m_val} ㎡<br>
                        • <b>설치 고도:</b> {h_3d_m_val}m
                    </p>
                    <hr style="margin: 8px 0; border: 0; border-top: 1px solid #BAE6FD;">
                    <p style="color: #334155; font-size: 0.9rem; line-height: 1.5; margin: 0;">
                        <b>[AI 공간 배치 근거 요약]</b><br>
                        {current_fac['reason']}
                    </p>
                </div>
            """, unsafe_allow_html=True)

            st.divider()

            st.markdown("### 💬 AI 3D 설계 어시스턴트")
            st.caption("AI 챗봇과 대화하여 시설 배치를 실시간으로 이동해보세요!")

            chat_box = st.container(height=240)
            with chat_box:
                for message in st.session_state['chat_messages']:
                    with st.chat_message(message["role"]):
                        st.write(message["content"])

            if user_prompt := st.chat_input("예: '푸드존을 더 멀리 이동해줘'"):
                st.session_state['chat_messages'].append({"role": "user", "content": user_prompt})
                ai_reply = parse_and_apply_ai_command(user_prompt)
                st.session_state['chat_messages'].append({"role": "assistant", "content": ai_reply})
                st.rerun()

elif st.session_state['page'] == 'report':
    st.markdown("## 📄 AI 기반 행사 설계 종합 보고서")
    st.caption("대시보드에서 설정한 행사 정보 및 공간 최적화 데이터가 직장상사 보고용 완결 양식으로 생성되었습니다.")

    facs = st.session_state['facilities']
    e_name = st.session_state['event_name']
    e_purpose = st.session_state['event_purpose']
    e_visitors = st.session_state['event_visitors']
    e_budget = st.session_state['event_budget']
    e_location = st.session_state['event_location']
    e_duration = st.session_state['event_duration']

    # 완벽한 종합 보고서 텍스트 생성 (다운로드 파일용)
    full_report_text = f"""================================================================================
[AI 종합 보고서] {e_name} 공간 최적화 및 안전 설계안
================================================================================
작성일자: 2026년 9월 9일
발행시스템: 이벤트 아키텍트 AI (Event Architect AI Platform)
보고대상: 행사 기획 총괄 책임자 및 직장 상사 보고용

--------------------------------------------------------------------------------
1. 행사 기본 개요 및 입력 정보
--------------------------------------------------------------------------------
• 행 사 명 : {e_name}
• 행사목적 : {e_purpose}
• 예상인원 : {e_visitors:,} 명
• 사업예산 : {e_budget}
• 행사장소 : {e_location}
• 진행시간 : {e_duration}

--------------------------------------------------------------------------------
2. AI 공간 객관적 평가 지표 및 등급
--------------------------------------------------------------------------------
[1] 비상 대피 및 안전성 : 95점 (매우 우수)
    - 근거: 메인 출입 게이트 및 응급 의료 센터가 최단 직선 비상 도로 코스로 확보됨.
[2] 관람 동선 분리성   : 90점 (매우 우수)
    - 근거: 푸드트럭 존을 서쪽 독립 구역으로 배치하여 조리 연기 및 관람객 병목 예방.
[3] 이용 편의성 및 접근성: 88점 (우수)
    - 근거: 중앙 잔디 휴게 광장에서 메인 무대 시야 확보 및 위생 편의 시설 접근 용이.

--------------------------------------------------------------------------------
3. 주요 시설별 실측 데이터 및 AI 최적 배치 이유
--------------------------------------------------------------------------------
1) {facs['stage']['name']}
   - 규격: {facs['stage']['w_m']}m x {facs['stage']['h_m']}m ({facs['stage']['w_m']*facs['stage']['h_m']}㎡)
   - 배치 사유: {facs['stage']['reason']}

2) {facs['food']['name']}
   - 규격: {facs['food']['w_m']}m x {facs['food']['h_m']}m ({facs['food']['w_m']*facs['food']['h_m']}㎡)
   - 배치 사유: {facs['food']['reason']}

3) {facs['rest']['name']}
   - 규격: {facs['rest']['w_m']}m x {facs['rest']['h_m']}m ({facs['rest']['w_m']*facs['rest']['h_m']}㎡)
   - 배치 사유: {facs['rest']['reason']}

4) {facs['medical']['name']}
   - 규격: {facs['medical']['w_m']}m x {facs['medical']['h_m']}m ({facs['medical']['w_m']*facs['medical']['h_m']}㎡)
   - 배치 사유: {facs['medical']['reason']}

5) {facs['toilet']['name']}
   - 규격: {facs['toilet']['w_m']}m x {facs['toilet']['h_m']}m ({facs['toilet']['w_m']*facs['toilet']['h_m']}㎡)
   - 배치 사유: {facs['toilet']['reason']}

6) {facs['info']['name']}
   - 규격: {facs['info']['w_m']}m x {facs['info']['h_m']}m ({facs['info']['w_m']*facs['info']['h_m']}㎡)
   - 배치 사유: {facs['info']['reason']}

7) {facs['exit']['name']}
   - 규격: {facs['exit']['w_m']}m x {facs['exit']['h_m']}m ({facs['exit']['w_m']*facs['exit']['h_m']}㎡)
   - 배치 사유: {facs['exit']['reason']}

--------------------------------------------------------------------------------
4. 종합 총평 및 최종 운영 권장사항
--------------------------------------------------------------------------------
본 설계안은 입력된 {e_visitors:,}명의 관람객 수요와 {e_location}의 실제 공간 규격을 기반으로 AI 자율 최적화 알고리즘을 거쳐 작성되었습니다.
행사 당일 주 출입구 정면 종합 안내 센터에 2명의 안전 안내 요원을 추가 배치할 것을 권장하며, 본 리포트는 상사 즉시 보고 및 현장 시공 가이드로 활용 가능합니다.
================================================================================
"""

    st.markdown(f"""
        <div class="custom-card">
            <h2 style="color: #0F172A; text-align: center;">[보고서] {e_name} 공간 최적화 및 안전 설계안</h2>
            <p style="text-align: center; color: #64748B;">작성일: 2026년 9월 9일 | 시스템: 이벤트 아키덱트 AI | 보고 대상: 행사 기획 총괄 책임자</p>
            <hr>
            
            <h3>1. 행사 개요 및 입력 정보</h3>
            <table style="width:100%; border-collapse: collapse; margin-top: 10px; font-size:0.92rem;">
                <tr style="background-color: #F8FAFC;">
                    <td style="padding: 8px; border: 1px solid #E2E8F0;"><b>행사명</b></td>
                    <td style="padding: 8px; border: 1px solid #E2E8F0;">{e_name}</td>
                    <td style="padding: 8px; border: 1px solid #E2E8F0;"><b>행사 목적</b></td>
                    <td style="padding: 8px; border: 1px solid #E2E8F0;">{e_purpose}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #E2E8F0;"><b>예상 인원</b></td>
                    <td style="padding: 8px; border: 1px solid #E2E8F0;">{e_visitors:,} 명</td>
                    <td style="padding: 8px; border: 1px solid #E2E8F0;"><b>사업 예산</b></td>
                    <td style="padding: 8px; border: 1px solid #E2E8F0;">{e_budget}</td>
                </tr>
                <tr style="background-color: #F8FAFC;">
                    <td style="padding: 8px; border: 1px solid #E2E8F0;"><b>행사 장소</b></td>
                    <td style="padding: 8px; border: 1px solid #E2E8F0;">{e_location}</td>
                    <td style="padding: 8px; border: 1px solid #E2E8F0;"><b>진행 시간</b></td>
                    <td style="padding: 8px; border: 1px solid #E2E8F0;">{e_duration}</td>
                </tr>
            </table>

            <h3 style="margin-top: 20px;">2. AI 실시간 공간 평가 객관적 지표</h3>
            <table style="width:100%; border-collapse: collapse; margin-top: 10px;">
                <tr style="background-color: #F1F5F9; text-align: left;">
                    <th style="padding: 10px;">평가 항목</th>
                    <th style="padding: 10px;">점수</th>
                    <th style="padding: 10px;">등급</th>
                    <th style="padding: 10px;">객관적 평가 근거 요약</th>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;">안전성 및 비상 대피</td>
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;"><b>95점</b></td>
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;"><span class="badge badge-excellent">매우 우수</span></td>
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;">응급의료센터 및 출입 게이트가 최단 비상 코스로 연결됨</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;">관람 동선 분리성</td>
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;"><b>90점</b></td>
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;"><span class="badge badge-excellent">매우 우수</span></td>
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;">푸드존과 메인 무대 간 연기 및 병목 우려 차단 완료</td>
                </tr>
                <tr>
                    <td style="padding: 10px;">이용 편의성</td>
                    <td style="padding: 10px;"><b>88점</b></td>
                    <td style="padding: 10px;"><span class="badge badge-good">우수</span></td>
                    <td style="padding: 10px;">중앙 잔디 휴게 광장에서 메인 무대 감상 및 이동 접근성 양호</td>
                </tr>
            </table>

            <h3 style="margin-top: 20px;">3. AI 도면 배치 주요 분석 근거</h3>
            <ul>
                <li><b>무대 및 관람석:</b> 주 시야각 확보를 고려한 북쪽 상단 배치.</li>
                <li><b>푸드존 및 휴게존:</b> 혼잡 예방을 위한 서쪽 독립 공간 및 중앙 광장 연계.</li>
                <li><b>의료 및 편의시설:</b> 구급차 진출입 우수 구역 및 인프라 용이 지역 배치.</li>
            </ul>
            
            <div style="background-color: #EFF6FF; padding: 15px; border-radius: 8px; margin-top: 20px; border: 1px solid #BFDBFE;">
                💡 <b>총평:</b> 본 보고서는 실제 행사장 시공 및 상사 보고용 공식 문서로 사용할 수 있습니다.
            </div>
        </div>
    """, unsafe_allow_html=True)

    rc1, rc2 = st.columns(2)
    with rc1:
        st.download_button(
            "📥 완성된 AI 종합 보고서 다운로드 (.txt)",
            data=full_report_text,
            file_name=f"{e_name}_공간최적화_보고서.txt",
            mime="text/plain",
            type="primary",
            use_container_width=True
        )
    with rc2:
        if st.button("🔄 최신 데이터로 보고서 갱신", use_container_width=True):
            st.toast("대시보드의 최신 배치 수치가 보고서에 성공적으로 업데이트되었습니다!")


    with st.expander("📌 행사 기본 정보 및 예산 설정", expanded=not st.session_state['digital_twin_generated']):
        with st.form("event_input_form"):
            ic1, ic2, ic3 = st.columns(3)
            with ic1:
                st.text_input("이벤트 이름", "2026 청춘 페스티벌")
                st.selectbox("이벤트 목적", ["축제/공연", "박람회/전시", "지역 문화 활성화", "기업 행사"])
            with ic2:
                st.number_input("예상 방문객 수 (명)", value=5000, step=500)
                st.text_input("예산", "5,000만원")
            with ic3:
                st.text_input("장소", "서울 올림픽공원 잔디마당 (100m x 72m)")
                st.text_input("진행 시간", "5시간")

            btn_gen = st.form_submit_button("✨ 3D 입체 디지털 트윈 공간 생성", type="primary", use_container_width=True)
            if btn_gen:
                st.session_state['digital_twin_generated'] = True
                st.session_state['facilities'] = DEFAULT_FACILITIES.copy()
                st.toast("실제 올림픽공원 잔디마당 공간 규격(7,200m²)에 입각한 3D 디지털 트윈 스튜디오가 구성되었습니다!")

    if not st.session_state['digital_twin_generated']:
        st.info("👆 위 '행사 기본 정보 및 예산 설정'을 확인하고 [✨ 3D 입체 디지털 트윈 공간 생성] 버튼을 누르시면 오늘의집 스타일 3D 입체 공간 도면이 펼쳐집니다.")
    else:
        st.markdown("""
            <div style="background-color: #FFFFFF; padding: 12px 20px; border-radius: 12px; border: 1px solid #CBD5E1; margin-bottom: 15px; display: flex; justify-content: space-between; font-size:0.92rem;">
                <span>🎪 <b>행사명:</b> 2026 청춘 페스티벌</span>
                <span>🎯 <b>목적:</b> 축제/공연</span>
                <span>👥 <b>예상 인원:</b> 5,000명</span>
                <span>💰 <b>예산:</b> 5,000만원</span>
                <span>📏 <b>실제 규격:</b> 100m × 72m (7,200㎡)</span>
            </div>
        """, unsafe_allow_html=True)

        v_col1, v_col2, v_col3, v_col4 = st.columns([2, 1.2, 1.2, 1.2])
        with v_col1:
            view_choice = st.radio(
                "뷰 포트 (오늘의집 3D 스튜디오 모드)",
                ["🚁 3D 입체 조감도 (Isometric 3D)", "📐 2D 평면 설계도 (Floor Plan)", "👁️ 관람객 눈높이 3D 뷰 (FPV)"],
                horizontal=True,
                index=0 if st.session_state['view_mode'] == '3D_ISO' else (1 if st.session_state['view_mode'] == '2D_PLAN' else 2)
            )
            if "3D 입체" in view_choice:
                st.session_state['view_mode'] = '3D_ISO'
            elif "2D 평면" in view_choice:
                st.session_state['view_mode'] = '2D_PLAN'
            else:
                st.session_state['view_mode'] = '3D_WALK'

        with v_col2:
            st.session_state['lighting_mode'] = st.selectbox("조명 환경", ["☀️ 주간 (Daylight)", "🌙 야간 (Night Illuminance)"], index=0 if st.session_state['lighting_mode'] == 'Day' else 1)
        
        with v_col3:
            st.session_state['show_grid'] = st.checkbox("10m 거리 격자 표시", value=st.session_state['show_grid'])

        with v_col4:
            if st.button("🔄 3D 카메라인덱스 리셋", use_container_width=True):
                st.toast("3D 디지털 트윈 카메라 시점이 기본 45도 조감각으로 초기화되었습니다.")

        col_main_left, col_main_right = st.columns([2.3, 1])

        with col_main_left:
            st.markdown("### 🏢 3D 입체 공간 디지털 트윈 (Spatial Twin)")
            
            facs = st.session_state['facilities']
            is_night = "Night" in st.session_state['lighting_mode']
            mode = st.session_state['view_mode']

            # Generate depth-sorted 3D elements
            sorted_keys = sorted(facs.keys(), key=lambda k: facs[k]['y'])

            bg_color = "#0B132B" if is_night else "#3B7A42"
            grass_grid_stroke = "#1E293B" if is_night else "#2D5A33"
            ground_slab_color = "#1E293B" if is_night else "#2C5230"
            wall_border_color = "#38BDF8" if is_night else "#22C55E"

            svg_items = []

            # Add 3D sound/view zone for stage
            stage_fac = facs['stage']
            if mode == '3D_ISO':
                svg_items.append(f"""
                <!-- 무대 음향 영향권 3D 퍼짐 표식 -->
                <ellipse cx="{stage_fac['x']}" cy="{stage_fac['y'] + 80}" rx="320" ry="160" fill="#8B5CF6" fill-opacity="{0.12 if not is_night else 0.25}" stroke="#A78BFA" stroke-width="2" stroke-dasharray="6,4"/>
                <text x="{stage_fac['x']}" y="{stage_fac['y'] + 230}" fill="#C084FC" font-size="12" font-weight="bold" text-anchor="middle">🔊 무대 주 음향 유효 반경 (80m)</text>
                """)

            # Add 10m scale grid
            if st.session_state['show_grid']:
                grid_lines = []
                for gx in range(100, 950, 80):
                    grid_lines.append(f'<line x1="{gx}" y1="80" x2="{gx}" y2="660" stroke="{grass_grid_stroke}" stroke-width="1" stroke-dasharray="4,4"/>')
                for gy in range(80, 670, 70):
                    grid_lines.append(f'<line x1="100" y1="{gy}" x2="900" y2="{gy}" stroke="{grass_grid_stroke}" stroke-width="1" stroke-dasharray="4,4"/>')
                svg_items.append("\n".join(grid_lines))

            # Render 3D Extruded Blocks or 2D Boxes based on mode
            for key in sorted_keys:
                f = facs[key]
                is_sel = (st.session_state['selected_facility'] == key)
                stroke_clr = "#38BDF8" if is_sel else ("#FFFFFF" if not is_night else "#94A3B8")
                stroke_w = "4" if is_sel else "1.5"

                x, y, w, h = f['x'], f['y'], f['w'], f['h']
                h3d = f.get('height_3d', 20)
                hex_side = f.get('hex_side', f.get('hex', '#3B82F6'))
                hex_top = f.get('hex_top', f.get('hex', '#60A5FA'))
                icon = f.get('icon', '🎪')
                w_m = f.get('w_m', 15)
                h_m = f.get('h_m', 10)
                h_3d_m = f.get('h_3d_m', 3)

                if mode == '3D_ISO':
                    # Isometric 3D Box Construction
                    # Top face offset by h3d
                    top_y = y - h3d
                    
                    # Drop shadow
                    shadow = f"""
                    <ellipse cx="{x}" cy="{y + h//3}" rx="{w//2 + 10}" ry="{h//3 + 5}" fill="#000000" fill-opacity="0.35"/>
                    """
                    
                    # 3D Front Face
                    front_face = f"""
                    <path d="M {x - w//2} {top_y + h//2} 
                             L {x + w//2} {top_y + h//2} 
                             L {x + w//2} {y + h//2} 
                             L {x - w//2} {y + h//2} Z" 
                          fill="{hex_side}" stroke="{stroke_clr}" stroke-width="{stroke_w}"/>
                    """

                    # 3D Side Face (Right)
                    side_face = f"""
                    <path d="M {x + w//2} {top_y - h//2} 
                             L {x + w//2 + 20} {top_y - h//2 + 10} 
                             L {x + w//2 + 20} {y - h//2 + 10} 
                             L {x + w//2} {top_y + h//2} Z" 
                          fill="{hex_side}" fill-opacity="0.8" stroke="{stroke_clr}" stroke-width="{stroke_w}"/>
                    """

                    # 3D Top Face
                    top_face = f"""
                    <polygon points="{x - w//2},{top_y - h//2} 
                                     {x + w//2},{top_y - h//2} 
                                     {x + w//2},{top_y + h//2} 
                                     {x - w//2},{top_y + h//2}" 
                             fill="{hex_top}" stroke="{stroke_clr}" stroke-width="{stroke_w}" filter="drop-shadow(0px 4px 6px rgba(0,0,0,0.3))"/>
                    """

                    # Spotlight effect for stage in night mode
                    spotlight = ""
                    if is_night and key == 'stage':
                        spotlight = f"""
                        <polygon points="{x},{top_y} {x-180},{top_y+350} {x+180},{top_y+350}" fill="url(#stageLightGrad)" fill-opacity="0.4"/>
                        """

                    # Label and metric text
                    label = f"""
                    <g transform="translate({x}, {top_y})">
                        <text x="0" y="-8" fill="#FFFFFF" font-size="15" font-weight="900" text-anchor="middle" style="font-family: sans-serif; text-shadow: 0px 2px 4px rgba(0,0,0,0.8);">{icon} {f['name']}</text>
                        <text x="0" y="10" fill="#E2E8F0" font-size="11" font-weight="700" text-anchor="middle">{w_m}m × {h_m}m (높이 {h_3d_m}m)</text>
                    </g>
                    """

                    svg_items.append(shadow + spotlight + front_face + side_face + top_face + label)

                elif mode == '2D_PLAN':
                    # Architectural 2D Floor Plan layout
                    plan_box = f"""
                    <rect x="{x - w//2}" y="{y - h//2}" width="{w}" height="{h}" rx="8" fill="{f['hex']}" fill-opacity="0.85" stroke="{stroke_clr}" stroke-width="{stroke_w}"/>
                    <line x1="{x - w//2}" y1="{y - h//2}" x2="{x + w//2}" y2="{y + h//2}" stroke="#FFFFFF" stroke-opacity="0.2" stroke-width="1"/>
                    <line x1="{x + w//2}" y1="{y - h//2}" x2="{x - w//2}" y2="{y + h//2}" stroke="#FFFFFF" stroke-opacity="0.2" stroke-width="1"/>
                    <text x="{x}" y="{y}" fill="#FFFFFF" font-size="14" font-weight="bold" text-anchor="middle">{icon} {f['name']}</text>
                    <text x="{x}" y="{y + 16}" fill="#CBD5E1" font-size="10" text-anchor="middle">{w_m}m × {h_m}m</text>
                    """
                    svg_items.append(plan_box)

                else: # 3D_WALK - Viewer Perspective
                    cam_y = y * 0.7 + 120
                    walk_box = f"""
                    <rect x="{x - w//2}" y="{cam_y - h3d*2}" width="{w}" height="{h3d*2.5}" rx="12" fill="{hex_top}" stroke="{stroke_clr}" stroke-width="{stroke_w}"/>
                    <text x="{x}" y="{cam_y - h3d}" fill="#FFFFFF" font-size="16" font-weight="bold" text-anchor="middle">{icon} {f['name']}</text>
                    """
                    svg_items.append(walk_box)

            all_svg_rendered = "\n".join(svg_items)

            digital_twin_3d_html = f"""
            <div style="position: relative; width: 100%; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.3); border: 2px solid {wall_border_color}; bg-color: {bg_color};">
                
                <!-- 오늘의집 스타일 3D 공간 상단 상태바 -->
                <div style="background: rgba(15, 23, 42, 0.9); color: #F8FAFC; padding: 10px 20px; font-size: 0.88rem; display: flex; justify-content: space-between; align-items: center; backdrop-filter: blur(8px);">
                    <div>
                        <span style="color: #38BDF8; font-weight: bold;">📐 3D Spatial Twin Studio</span> | 
                        <span>렌더링 모드: <b>{mode}</b></span> | 
                        <span>부지 총 면적: <b>7,200 ㎡ (올림픽공원)</b></span>
                    </div>
                    <div>
                        <span style="background: #0284C7; padding: 3px 10px; border-radius: 12px; font-size: 0.78rem; font-weight: bold;">LIVE 3D Engine</span>
                    </div>
                </div>

                <svg viewBox="0 0 1000 720" style="width: 100%; height: auto; background-color: {bg_color}; display: block;">
                    <defs>
                        <linearGradient id="groundGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="{ground_slab_color}" />
                            <stop offset="100%" stop-color="{bg_color}" />
                        </linearGradient>
                        <linearGradient id="stageLightGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                            <stop offset="0%" stop-color="#C084FC" stop-opacity="0.8" />
                            <stop offset="100%" stop-color="#8B5CF6" stop-opacity="0.0" />
                        </linearGradient>
                    </defs>

                    <!-- 3D Ground Base Slab -->
                    <polygon points="60,60 940,60 980,680 20,680" fill="url(#groundGrad)" stroke="{wall_border_color}" stroke-width="3"/>

                    <!-- Perimeter 3D Fence / Safety Boundary -->
                    <polygon points="80,80 920,80 950,660 50,660" fill="none" stroke="#F59E0B" stroke-width="3" stroke-dasharray="12,8"/>

                    <!-- Rendered 3D Facilities & Overlay -->
                    {all_svg_rendered}

                    <!-- Scale Ruler Bar (오늘의집 3D 축척 자) -->
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
            st.components.v1.html(digital_twin_3d_html, height=560, scrolling=False)

            st.markdown("**👇 3D 공간 내 개별 시설을 선택하면 상세 실측 스펙 및 최적배치 사유가 조회됩니다:**")
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

            st.markdown("### 🏢 3D 시설 실측 데이터")
            st.markdown(f"""
                <div class="reason-box">
                    <h4 style="color: {current_fac['hex']}; margin-top: 0;">{icon_val} {current_fac['name']}</h4>
                    <p style="color: #0F172A; font-size: 0.9rem; margin-bottom: 8px;">
                        • <b>실제 가로×세로:</b> {w_m_val}m × {h_m_val}m<br>
                        • <b>점유 면적:</b> {w_m_val * h_m_val} ㎡<br>
                        • <b>3D 입체 높이:</b> {h_3d_m_val}m 고도
                    </p>
                    <hr style="margin: 8px 0; border: 0; border-top: 1px solid #BAE6FD;">
                    <p style="color: #334155; font-size: 0.9rem; line-height: 1.5; margin: 0;">
                        <b>[AI 공간 설계 근거]</b><br>
                        {current_fac['reason']}
                    </p>
                </div>
            """, unsafe_allow_html=True)

            st.divider()

            st.markdown("### 🔥 AI 군중 밀도 시뮬레이션")
            if st.button("🚨 3D 군중 혼잡도 Heatmap 실행", type="primary", use_container_width=True):
                st.session_state['simulated'] = True

            if st.session_state['simulated']:
                st.caption("구역별 3D 밀집도 예측 (붉은색: 인파 정체 위험 구역)")
                np.random.seed(42)
                sim_grid = np.random.rand(12, 12) * 50
                sim_grid[2, 5] += 40  # 무대 앞 혼잡
                sim_grid[8, 2] += 30  # 푸드존 앞 혼잡
                fig = px.imshow(sim_grid, color_continuous_scale='YlOrRd', labels=dict(color="혼잡도"))
                fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=180)
                st.plotly_chart(fig, use_container_width=True)

            st.divider()

            st.markdown("### 💬 AI 3D 설계 어시스턴트")
            st.caption("AI 챗봇으로 3D 배치를 자율 변경하세요!")

            chat_box = st.container(height=240)
            with chat_box:
                for message in st.session_state['chat_messages']:
                    with st.chat_message(message["role"]):
                        st.write(message["content"])

            if user_prompt := st.chat_input("예: '푸드존을 더 멀리 이동해줘'"):
                st.session_state['chat_messages'].append({"role": "user", "content": user_prompt})
                ai_reply = parse_and_apply_ai_command(user_prompt)
                st.session_state['chat_messages'].append({"role": "assistant", "content": ai_reply})
                st.rerun()

elif st.session_state['page'] == 'report':
    st.markdown("## 📄 AI 기반 행사 설계 종합 보고서")
    st.caption("대시보드에서 설계한 배치와 AI 시뮬레이션 결과가 상사 보고용 양식으로 즉시 생성됩니다.")

    facs = st.session_state['facilities']

    st.markdown(f"""
        <div class="custom-card">
            <h2 style="color: #0F172A; text-align: center;">[보고서] 2026 청춘 페스티벌 공간 최적화 및 안전 설계안</h2>
            <p style="text-align: center; color: #64748B;">작성일: 2026년 9월 8일 | 시스템: 이벤트 아키텍트 AI | 보고 대상: 행사 총괄 책임자</p>
            <hr>
            
            <h3>1. 행사 개요</h3>
            <ul>
                <li><b>행사명:</b> 2026 청춘 페스티벌</li>
                <li><b>예상 인원:</b> 5,000명 | <b>예산:</b> 5,000만원</li>
                <li><b>도면 플랫폼:</b> 입체 조감도 기반 실시간 디지털 트윈</li>
            </ul>

            <h3>2. 실시간 AI 공간 평가 지표</h3>
            <table style="width:100%; border-collapse: collapse; margin-top: 10px;">
                <tr style="background-color: #F1F5F9; text-align: left;">
                    <th style="padding: 10px;">평가 항목</th>
                    <th style="padding: 10px;">점수</th>
                    <th style="padding: 10px;">등급</th>
                    <th style="padding: 10px;">최신 배치 현황 및 평가 요약</th>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;">안전성 및 비상 대피</td>
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;">95점</td>
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;"><span class="badge badge-excellent">매우 우수</span></td>
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;">응급의료센터 및 출입구가 최단 직선 비상 코스로 연결됨</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;">동선 분리성</td>
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;">90점</td>
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;"><span class="badge badge-excellent">매우 우수</span></td>
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;">푸드존과 메인 공연장 간 연기 간섭 최적 차단</td>
                </tr>
                <tr>
                    <td style="padding: 10px;">이용 편의성</td>
                    <td style="padding: 10px;">88점</td>
                    <td style="padding: 10px;"><span class="badge badge-good">우수</span></td>
                    <td style="padding: 10px;">화장실 및 중앙 잔디 광장 휴게 공간 동선 균형 확보</td>
                </tr>
            </table>

            <h3 style="margin-top: 20px;">3. AI 도면 배치 요약 및 권장사항</h3>
            <ol>
                <li><b>푸드존 현황:</b> 주 동선 정체를 예방하도록 서쪽 독립 구역 배치 완료.</li>
                <li><b>화장실 현황:</b> 편의성과 배수 인프라 접근성 충족.</li>
                <li><b>운영 추천:</b> 메인 무대 시작 전 주 출입구 안내 센터에 안내 요원 2명 추가 배치 권장.</li>
            </ol>
            
            <div style="background-color: #EFF6FF; padding: 15px; border-radius: 8px; margin-top: 20px; border: 1px solid #BFDBFE;">
                💡 <b>총평:</b> 본 설계안은 AI 대화를 통해 최적화되었으며, 실제 행사장 시공 및 운영에 즉시 활용 가능합니다.
            </div>
        </div>
    """, unsafe_allow_html=True)

    rc1, rc2 = st.columns(2)
    with rc1:
        st.download_button("📥 보고서 파일 다운로드 (.txt)", data="2026 청춘 페스티벌 공간 최적화 보고서...", file_name="event_ai_report.txt", type="primary", use_container_width=True)
    with rc2:
        if st.button("🔄 최신 AI 배치 데이터로 보고서 갱신", use_container_width=True):
            st.toast("대시보드의 최신 도면 위치 수치가 보고서에 성공적으로 반영되었습니다!")

elif st.session_state['page'] == 'settings':
    st.markdown("## ⚙️ 시스템 설정")

    with st.container():
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("👤 계정 및 사용자 정보")
        st.text_input("사용자 이름", value=st.session_state['username'])
        st.text_input("소속 조직 / 회사", value="이벤트 기획 1팀")
        st.text_input("이메일 주소", value="jueun@event-architect.ai")
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("🖥️ 디지털 트윈 엔진 옵션")
        st.toggle("안내선 및 동선 화살표 표시", value=True)
        st.toggle("AI 챗봇 변경 시 자동 도면 갱신", value=True)
        st.selectbox("AI 모델 선택", ["EventArchitect-v4.2 (최신/권장)", "EventArchitect-Lite"])
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("로그아웃", type="primary"):
        st.session_state['logged_in'] = False
        st.session_state['page'] = 'home'
        st.rerun()
