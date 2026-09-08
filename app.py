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

    /* 홈 화면 대형 박스 히어로 버튼 스타일 (전체 클릭 가능) */
    div.stButton > button.hero-card-btn {
        width: 100% !important;
        height: 280px !important;
        background: linear-gradient(135deg, #FFFFFF 0%, #EFF6FF 100%) !important;
        border: 2px solid #BFDBFE !important;
        border-radius: 20px !important;
        padding: 28px !important;
        text-align: left !important;
        box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.1) !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        white-space: normal !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-start !important;
    }
    div.stButton > button.hero-card-btn:hover {
        transform: translateY(-4px) !important;
        border-color: #3B82F6 !important;
        box-shadow: 0 20px 30px -10px rgba(59, 130, 246, 0.25) !important;
        background: linear-gradient(135deg, #FFFFFF 0%, #DBEAFE 100%) !important;
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
    </style>
""", unsafe_allow_html=True)

# DEFAULT FACILITY DATA WITH ARCHISKETCH COORDINATES
DEFAULT_FACILITIES = {
    "stage": {
        "name": "공연장",
        "icon": "🎪",
        "hex": "#8B5CF6",
        "x": 500, "y": 100, "w": 260, "h": 100,
        "reason": "북쪽 중앙에 위치시켜 관람객 시야각을 극대화했습니다."
    },
    "booth": {
        "name": "체험부스",
        "icon": "🛍️",
        "hex": "#3B82F6",
        "x": 180, "y": 120, "w": 200, "h": 180,
        "reason": "북서쪽 구역에 부스 단지를 형성하여 유입률을 최적화했습니다."
    },
    "food": {
        "name": "푸드존",
        "icon": "🍔",
        "hex": "#F97316",
        "x": 180, "y": 360, "w": 200, "h": 180,
        "reason": "서쪽 측면에 배치하여 조리 연기 확산을 방지하고 관람 동선과 분리했습니다."
    },
    "rest": {
        "name": "휴게공간",
        "icon": "🏕️",
        "hex": "#10B981",
        "x": 500, "y": 350, "w": 300, "h": 220,
        "reason": "중앙 잔디 광장에 위치시켜 누구나 편히 쉴 수 있도록 조성했습니다."
    },
    "medical": {
        "name": "응급의료센터",
        "icon": "🚑",
        "hex": "#EF4444",
        "x": 820, "y": 110, "w": 160, "h": 100,
        "reason": "동쪽 외곽 진입로 옆에 배치하여 구급차 최단 진출입을 보장합니다."
    },
    "toilet": {
        "name": "화장실",
        "icon": "🚻",
        "hex": "#2563EB",
        "x": 820, "y": 270, "w": 160, "h": 110,
        "reason": "동쪽 측면 배관 인근에 위치시켜 이용 편리성과 배수 효율을 극대화했습니다."
    },
    "info": {
        "name": "안내센터",
        "icon": "ℹ️",
        "hex": "#EC4899",
        "x": 500, "y": 590, "w": 160, "h": 60,
        "reason": "주 출입구 정면에 배치하여 길 안내 및 관람 문의를 신속 처리합니다."
    },
    "exit": {
        "name": "출입구",
        "icon": "🚪",
        "hex": "#F43F5E",
        "x": 500, "y": 660, "w": 180, "h": 50,
        "reason": "남쪽 정문에 위치하여 대규모 인파의 빠른 진출입 및 대피를 유도합니다."
    }
}

if 'page' not in st.session_state:
    st.session_state['page'] = 'home'
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = True
if 'username' not in st.session_state:
    st.session_state['username'] = "주은님"
if 'digital_twin_generated' not in st.session_state:
    st.session_state['digital_twin_generated'] = True
if 'simulated' not in st.session_state:
    st.session_state['simulated'] = False
if 'selected_facility' not in st.session_state:
    st.session_state['selected_facility'] = 'stage'
if 'facilities' not in st.session_state:
    st.session_state['facilities'] = DEFAULT_FACILITIES.copy()
if 'chat_messages' not in st.session_state:
    st.session_state['chat_messages'] = [
        {"role": "assistant", "content": "안녕하세요! AI 이벤트 아키텍트입니다. 배치 변경을 원하시면 말씀해주세요. (예: '푸드존을 더 멀리 이동해줘', '화장실을 의료 센터 근처로 이동해줘', '체험부스를 오른쪽으로 옮겨줘')"}
    ]

# AI NATURAL LANGUAGE PARSER FOR DIRECT FACILITY MODIFICATION
def parse_and_apply_ai_command(prompt: str):
    prompt_clean = prompt.replace(" ", "")
    facs = st.session_state['facilities']
    
    # Identify target facility
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
    elif "출입구" in prompt_clean or "입구" in prompt_clean or "출구" in prompt_clean:
        target_key = "exit"

    if not target_key:
        target_key = st.session_state['selected_facility']

    fac = facs[target_key]
    changed = False
    action_desc = ""

    # Direction / Position Rules
    if "멀리" in prompt_clean or "외곽" in prompt_clean or "분리" in prompt_clean:
        if target_key == "food":
            fac["x"] = 100
            fac["y"] = 420
            action_desc = "푸드존을 연기 및 혼잡 방지를 위해 서쪽 최외곽 구역(X:100, Y:420)으로 이동 배치했습니다."
        elif target_key == "toilet":
            fac["x"] = 880
            fac["y"] = 380
            action_desc = "화장실을 메인 무대와 충분한 거리를 둔 동쪽 외곽 구역(X:880, Y:380)으로 이동시켰습니다."
        else:
            fac["x"] = max(80, fac["x"] - 100)
            action_desc = f"{fac['name']}의 위치를 외곽 구역(X:{fac['x']}, Y:{fac['y']})으로 이동시켰습니다."
        changed = True

    elif "의료" in prompt_clean or "병원" in prompt_clean or "가까이" in prompt_clean:
        if target_key == "toilet":
            fac["x"] = facs["medical"]["x"] - 20
            fac["y"] = facs["medical"]["y"] + 110
            action_desc = "화장실을 응급의료센터 옆 구역으로 즉시 재배치했습니다."
        else:
            fac["x"] = facs["medical"]["x"] - 30
            action_desc = f"{fac['name']}을(를) 의료 센터 인근 접근하기 쉬운 위치로 조정했습니다."
        changed = True

    elif "오른쪽" in prompt_clean or "동쪽" in prompt_clean:
        fac["x"] = min(880, fac["x"] + 120)
        action_desc = f"{fac['name']}을(를) 동쪽 구역(X:{fac['x']}, Y:{fac['y']})으로 이동했습니다."
        changed = True

    elif "왼쪽" in prompt_clean or "서쪽" in prompt_clean:
        fac["x"] = max(90, fac["x"] - 120)
        action_desc = f"{fac['name']}을(를) 서쪽 구역(X:{fac['x']}, Y:{fac['y']})으로 이동했습니다."
        changed = True

    elif "위" in prompt_clean or "북쪽" in prompt_clean or "상단" in prompt_clean:
        fac["y"] = max(90, fac["y"] - 100)
        action_desc = f"{fac['name']}을(를) 상단 구역(X:{fac['x']}, Y:{fac['y']})으로 상향 이동했습니다."
        changed = True

    elif "아래" in prompt_clean or "남쪽" in prompt_clean or "하단" in prompt_clean:
        fac["y"] = min(600, fac["y"] + 100)
        action_desc = f"{fac['name']}을(를) 하단 입구 방향(X:{fac['x']}, Y:{fac['y']})으로 이동했습니다."
        changed = True

    else:
        # Default smart layout tweak
        fac["x"] = (fac["x"] + 80) % 800 + 100
        action_desc = f"{fac['name']}의 공간 좌표를 AI 동선 최적화 공식에 따라 (X:{fac['x']}, Y:{fac['y']})로 수정 적용했습니다."
        changed = True

    if changed:
        fac["reason"] = f"AI 사용자 대화 맞춤 변경: {action_desc}"
        st.session_state['selected_facility'] = target_key
        return f"✅ **알림:** {action_desc} (디지털 트윈 도면 및 안전 분석 보고서에 즉시 반영되었습니다!)"
    
    return f"네! 요청하신 '{prompt}' 내용에 맞춰 배치를 점검하였으며, 최적화 기준에 맞게 조정하였습니다."

    .hero-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #EFF6FF 100%);
        border: 2px solid #BFDBFE;
        border-radius: 20px;
        padding: 32px;
        box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.1);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .hero-card:hover {
        transform: translateY(-4px);
        border-color: #3B82F6;
        box-shadow: 0 20px 30px -10px rgba(59, 130, 246, 0.2);
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

    /* 상단 로고 버튼 스타일링 */
    div[data-testid="stSidebarHeader"] {
        padding-top: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

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
if 'map_view_mode' not in st.session_state:
    st.session_state['map_view_mode'] = '2D'  # '2D', '3D', or 'CAD'
if 'chat_messages' not in st.session_state:
    st.session_state['chat_messages'] = [
        {"role": "assistant", "content": "안녕하세요! AI 이벤트 아키텍트입니다. 공간 배치에 대해 원하시는 점을 말씀해주세요 (예: '푸드존을 무대와 더 멀리 배치해줘')."}
    ]

FACILITIES = {
    "stage": {
        "name": "공연장",
        "icon": "🎪",
        "color": [139, 92, 246],
        "hex": "#8B5CF6",
        "lat": 37.5215, "lon": 127.1210, "height": 30,
        "reason": "북쪽 중앙 상단에 배치하여 관람객 시야각을 극대화했습니다. 주요 소음 및 진동이 대기선/푸드존에 미치는 영향을 최적 차단하는 위치입니다."
    },
    "booth": {
        "name": "체험부스",
        "icon": "🛍️",
        "color": [59, 130, 246],
        "hex": "#3B82F6",
        "lat": 37.5210, "lon": 127.1192, "height": 10,
        "reason": "북서쪽 구역에 독립적 부스 단지를 형성하여 체험 유입률을 높이고 혼잡도를 유연하게 관리합니다."
    },
    "food": {
        "name": "푸드존",
        "icon": "🍔",
        "color": [249, 115, 22],
        "hex": "#F97316",
        "lat": 37.5198, "lon": 127.1195, "height": 12,
        "reason": "서쪽 측면에 배치하여 조리 연기 확산을 방지하고 메인 공연 관람 동선과 분리했습니다."
    },
    "rest": {
        "name": "휴게공간",
        "icon": "🏕️",
        "color": [16, 185, 129],
        "hex": "#10B981",
        "lat": 37.5202, "lon": 127.1212, "height": 8,
        "reason": "행사장 중앙 잔디 광장에 위치시켜 공연 관람 및 푸드존 이용객 모두가 신속히 쉬어갈 수 있도록 조성했습니다."
    },
    "medical": {
        "name": "응급의료센터",
        "icon": "🚑",
        "color": [239, 68, 68],
        "hex": "#EF4444",
        "lat": 37.5212, "lon": 127.1228, "height": 15,
        "reason": "동쪽 외곽 진입로 옆에 배치하여 긴급 상황 시 구급차 최단 진출입을 보장합니다."
    },
    "toilet": {
        "name": "화장실",
        "icon": "🚻",
        "color": [99, 102, 241],
        "hex": "#6366F1",
        "lat": 37.5202, "lon": 127.1230, "height": 10,
        "reason": "동쪽 측면 배관 인근에 위치시켜 이용객 접근성을 높이고 상하수도 효율을 극대화했습니다."
    },
    "info": {
        "name": "안내센터",
        "icon": "ℹ️",
        "color": [236, 72, 153],
        "hex": "#EC4899",
        "lat": 37.5190, "lon": 127.1215, "height": 10,
        "reason": "주 출입구 정면에 배치하여 관람객 문의 및 미아/길 안내를 최우선으로 처리합니다."
    },
    "exit": {
        "name": "출입구",
        "icon": "🚪",
        "color": [30, 41, 59],
        "hex": "#1E293B",
        "lat": 37.5185, "lon": 127.1210, "height": 18,
        "reason": "남쪽 정문에 위치하여 대규모 인파의 주 진출입 및 비상시 신속 대피를 유도합니다."
    }
}

# -------------------------------------------------------------------
# HEADER & SIDEBAR NAVIGATION
# -------------------------------------------------------------------
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

# Top Header Bar
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
    with c_set:
        if st.button("⚙️", help="설정으로 이동"):
            st.session_state['page'] = 'settings'
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# -------------------------------------------------------------------
# PAGE 1: 홈 화면 (네모 박스 전체 클릭으로 바로 이동)
# -------------------------------------------------------------------
if st.session_state['page'] == 'home':
    st.markdown("## 🚀 시작할 메뉴를 선택하세요")
    st.caption("박스 카드를 클릭하면 해당하는 작업 화면으로 바로 이동합니다.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_dash, col_rep = st.columns(2)

    with col_dash:
        # Styled full-box button for Dashboard
        dash_card_html = """
        <div style="
            background: linear-gradient(135deg, #FFFFFF 0%, #EFF6FF 100%);
            border: 2px solid #93C5FD;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.12);
            height: 240px;
        ">
            <h1 style="font-size: 2.8rem; margin:0 0 10px 0;">📊</h1>
            <h2 style="color: #1E3A8A; margin: 0 0 12px 0; font-size: 1.5rem;">AI 기반 행사 자동 설계 대시보드</h2>
            <p style="color: #475569; font-size: 0.98rem; line-height: 1.6; margin:0;">
                이벤트 목적과 예산을 입력하면 <b>오늘의 집(아키스케치) 스타일 디지털 트윈 도면</b>을 생성합니다.<br>
                AI 챗봇과 대화하여 실제 공간 배치를 실시간으로 자유롭게 변경하세요.
            </p>
        </div>
        """
        st.markdown(dash_card_html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📊 대시보드 카드 선택 (클릭하여 이동)", key="btn_click_dash", type="primary", use_container_width=True):
            st.session_state['page'] = 'dashboard'
            st.rerun()

    with col_rep:
        rep_card_html = """
        <div style="
            background: linear-gradient(135deg, #FFFFFF 0%, #F0FDF4 100%);
            border: 2px solid #86EFAC;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 25px -5px rgba(16, 185, 129, 0.12);
            height: 240px;
        ">
            <h1 style="font-size: 2.8rem; margin:0 0 10px 0;">📄</h1>
            <h2 style="color: #065F46; margin: 0 0 12px 0; font-size: 1.5rem;">AI 종합 분석 보고서</h2>
            <p style="color: #475569; font-size: 0.98rem; line-height: 1.6; margin:0;">
                설계된 행사장 배치안을 기반으로 <b>직장 상사에게 즉시 보고 가능한 보고서</b>를 자동 생성합니다.<br>
                안전성, 동선 효율성 및 AI 개선 권장사항을 자동 반영합니다.
            </p>
        </div>
        """
        st.markdown(rep_card_html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📄 AI 보고서 카드 선택 (클릭하여 이동)", key="btn_click_rep", type="secondary", use_container_width=True):
            st.session_state['page'] = 'report'
            st.rerun()

# -------------------------------------------------------------------
# PAGE 2: 대시보드 화면 (단일 1번 모드: 오늘의 집 아키스케치 2D 디지털 트윈)
# -------------------------------------------------------------------
elif st.session_state['page'] == 'dashboard':
    st.markdown("## 📊 AI 디지털 트윈 공간 설계 대시보드")
    st.caption("🏠 오늘의 집(아키스케치) 스타일의 2D 평면 도면 기반 스마트 공간 인테리어 / 행사장 설계 모드입니다.")

    # 1. 상단 이벤트 정보 입력 칸
    with st.expander("📌 행사 기본 정보 및 예산 설정", expanded=False):
        with st.form("event_input_form"):
            ic1, ic2, ic3 = st.columns(3)
            with ic1:
                st.text_input("이벤트 이름", "2026 청춘 페스티벌")
                st.selectbox("이벤트 목적", ["축제/공연", "박람회/전시", "지역 문화 활성화", "기업 행사"])
            with ic2:
                st.number_input("예상 방문객 수 (명)", value=5000, step=500)
                st.text_input("예산", "5,000만원")
            with ic3:
                st.text_input("장소", "서울 올림픽공원 잔디마당")
                st.text_input("진행 시간", "5시간")

            btn_gen = st.form_submit_button("✨ AI 공간 리셋 및 최적화 실행", type="primary", use_container_width=True)
            if btn_gen:
                st.session_state['facilities'] = DEFAULTFACILITIES.copy()
                st.toast("AI가 장소 규격에 맞는 디지털 트윈 도면을 초기 배치했습니다!")

    # Summary bar
    st.markdown("""
        <div style="background-color: #FFFFFF; padding: 12px 20px; border-radius: 12px; border: 1px solid #CBD5E1; margin-bottom: 15px; display: flex; justify-content: space-between; font-size:0.92rem;">
            <span>🎪 <b>행사명:</b> 2026 청춘 페스티벌</span>
            <span>🎯 <b>목적:</b> 축제/공연</span>
            <span>👥 <b>예상 인원:</b> 5,000명</span>
            <span>💰 <b>예산:</b> 5,000만원</span>
            <span>📍 <b>도면 규격:</b> 100m x 70m (실습 평면)</span>
        </div>
    """, unsafe_allow_html=True)

    col_main_left, col_main_right = st.columns([2.3, 1])

    with col_main_left:
        st.markdown("### 🏠 2D 평면 도면 (오늘의 집 / 아키스케치 스타일)")
        st.caption("📐 격자(Grid) 규격과벽체 치수가 측정되는 스마트 2D 건축 디지털 트윈 도면입니다.")

        # Build dynamic SVG based on st.session_state['facilities']
        facs = st.session_state['facilities']

        svg_elements = []
        for key, f in facs.items():
            is_sel = (st.session_state['selected_facility'] == key)
            stroke_clr = "#0284C7" if is_sel else f['hex']
            stroke_w = "4" if is_sel else "2"
            
            # Element SVG Block
            elem_svg = f"""
            <g transform="translate({f['x'] - f['w']//2}, {f['y'] - f['h']//2})">
                <!-- Archisketch Room Box -->
                <rect x="0" y="0" width="{f['w']}" height="{f['h']}" rx="8" fill="{f['hex']}" fill-opacity="0.18" stroke="{stroke_clr}" stroke-width="{stroke_w}"/>
                <!-- Dimension Marker -->
                <text x="{f['w']//2}" y="-8" font-size="11" font-weight="bold" fill="#0284C7" text-anchor="middle">{f['w']*10}mm x {f['h']*10}mm</text>
                <!-- Badge Pin -->
                <rect x="10" y="10" width="{f['w']-20}" height="32" rx="16" fill="{f['hex']}"/>
                <text x="{f['w']//2}" y="31" fill="#FFFFFF" font-size="14" font-weight="bold" text-anchor="middle">{f['icon']} {f['name']}</text>
                <!-- Coordinate Label -->
                <text x="{f['w']//2}" y="{f['h']-10}" font-size="11" fill="#475569" font-weight="bold" text-anchor="middle">X:{f['x']}, Y:{f['y']}</text>
            </g>
            """
            svg_elements.append(elem_svg)

        all_svg_items = "\n".join(svg_elements)

        # Archisketch Canvas Floorplan
        archisketch_html = f"""
        <div style="position: relative; width: 100%; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.12); border: 2px solid #0284C7;">
            <svg viewBox="0 0 1000 720" style="width: 100%; height: auto; background-color: #F8FAFC; display: block;">
                <!-- Archisketch Blueprint Grid Pattern -->
                <defs>
                    <pattern id="archGrid" width="40" height="40" patternUnits="userSpaceOnUse">
                        <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#E2E8F0" stroke-width="1.5"/>
                        <circle cx="0" cy="0" r="1.5" fill="#94A3B8"/>
                    </pattern>
                </defs>
                <rect width="1000" height="720" fill="url(#archGrid)"/>

                <!-- Outer Venue Wall Boundary (오늘의 집 도면 외벽) -->
                <rect x="40" y="40" width="920" height="640" fill="none" stroke="#1E293B" stroke-width="8" rx="12"/>
                
                <!-- Wall Dimension Labels (Archisketch Architectural Measurement) -->
                <text x="500" y="28" font-size="14" font-weight="bold" fill="#0284C7" text-anchor="middle">📏 가로 벽체 길이: 100.0 m (100,000 mm)</text>
                <text x="20" y="360" font-size="14" font-weight="bold" fill="#0284C7" text-anchor="middle" transform="rotate(-90 20 360)">📏 세로 벽체 길이: 70.0 m (70,000 mm)</text>

                <!-- Zone Inner Dividers -->
                <line x1="40" y1="260" x2="380" y2="260" stroke="#94A3B8" stroke-width="3" stroke-dasharray="6,6"/>
                <line x1="380" y1="40" x2="380" y2="680" stroke="#94A3B8" stroke-width="3" stroke-dasharray="6,6"/>
                <line x1="780" y1="40" x2="780" y2="680" stroke="#94A3B8" stroke-width="3" stroke-dasharray="6,6"/>

                <!-- Zone Titles -->
                <text x="210" y="65" font-size="13" font-weight="bold" fill="#64748B" text-anchor="middle">[구역 A: 체험 & 푸드존]</text>
                <text x="580" y="65" font-size="13" font-weight="bold" fill="#64748B" text-anchor="middle">[구역 B: 메인 공연 & 중앙 광장]</text>
                <text x="880" y="65" font-size="13" font-weight="bold" fill="#64748B" text-anchor="middle">[구역 C: 지원 & 편의시설]</text>

                <!-- Flow Pedestrian Lines -->
                <path d="M 500,660 L 500,480 L 280,480 L 280,200 L 500,200 L 880,200" stroke="#0284C7" stroke-width="4" stroke-dasharray="8,6" fill="none"/>

                <!-- Dynamic Facilities Layer -->
                {all_svg_items}

            </svg>
        </div>
        """
        st.components.v1.html(archisketch_html, height=540, scrolling=False)

        # Facility quick selector buttons
        st.markdown("**👇 아래 시설을 선택하여 위치 수치를 직접 조율하거나 오른쪽 AI 챗봇에게 변경을 요청하세요:**")
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

        # Coordinate Tuner Form for precise control
        selected_key = st.session_state['selected_facility']
        cur_fac = facs[selected_key]
        with st.expander(f"⚙️ 선택된 [{cur_fac['name']}] 정밀 좌표 직접 조율하기", expanded=True):
            tc1, tc2, tc3 = st.columns(3)
            with tc1:
                new_x = st.slider("X 좌표 (가로)", min_value=80, max_value=900, value=cur_fac['x'], step=10, key=f"sl_x_{selected_key}")
            with tc2:
                new_y = st.slider("Y 좌표 (세로)", min_value=80, max_value=650, value=cur_fac['y'], step=10, key=f"sl_y_{selected_key}")
            with tc3:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("📍 위치 적용", type="primary", use_container_width=True):
                    facs[selected_key]['x'] = new_x
                    facs[selected_key]['y'] = new_y
                    facs[selected_key]['reason'] = f"사용자가 직접 X:{new_x}, Y:{new_y} 좌표로 수정 조정함."
                    st.toast(f"{cur_fac['name']} 위치가 도면에 반영되었습니다!")
                    st.rerun()

    with col_main_right:
        # Reason Summary Card
        selected_key = st.session_state['selected_facility']
        current_fac = facs[selected_key]
        
        st.markdown(f"### 💡 공간 배치 분석")
        st.markdown(f"""
            <div class="reason-box">
                <h4 style="color: {current_fac['hex']}; margin-top: 0;">{current_fac['icon']} {current_fac['name']} (X:{current_fac['x']}, Y:{current_fac['y']})</h4>
                <p style="color: #334155; font-size: 0.93rem; line-height: 1.5;">
                    <b>[AI 아키텍처 배치 근거]</b><br>
                    {current_fac['reason']}
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.divider()

        # AI Assistant Chatbot (Working & Dynamic Layout Modification)
        st.markdown("### 💬 AI 설계 어시스턴트")
        st.caption("AI와 대화하여 도면 배치를 실시간으로 자유롭게 명령하세요!")

        chat_box = st.container(height=280)
        with chat_box:
            for message in st.session_state['chat_messages']:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

        if user_prompt := st.chat_input("예: '푸드존을 더 멀리 이동해줘' 또는 '화장실을 의료센터 옆으로'"):
            st.session_state['chat_messages'].append({"role": "user", "content": user_prompt})
            
            # Apply dynamic change to state
            ai_reply = parse_and_apply_ai_command(user_prompt)
            st.session_state['chat_messages'].append({"role": "assistant", "content": ai_reply})
            st.rerun()

# -------------------------------------------------------------------
# PAGE 3: AI 보고서 화면 (최신 배치 상태 실시간 반영)
# -------------------------------------------------------------------
elif st.session_state['page'] == 'report':
    st.markdown("## 📄 AI 기반 행사 설계 종합 보고서")
    st.caption("설계 대시보드의 최신 배치와 AI 대화 결과가 자동으로 즉시 종합 작성된 상사 보고용 문서입니다.")

    facs = st.session_state['facilities']
    food_pos = f"X:{facs['food']['x']}, Y:{facs['food']['y']}"
    stage_pos = f"X:{facs['stage']['x']}, Y:{facs['stage']['y']}"
    toilet_pos = f"X:{facs['toilet']['x']}, Y:{facs['toilet']['y']}"

    st.markdown(f"""
        <div class="custom-card">
            <h2 style="color: #0F172A; text-align: center;">[보고서] 2026 청춘 페스티벌 공간 최적화 및 안전 설계안</h2>
            <p style="text-align: center; color: #64748B;">작성일: 2026년 9월 8일 | 시스템: 이벤트 아키텍트 AI | 보고 대상: 행사 총괄 책임자</p>
            <hr>
            
            <h3>1. 행사 개요</h3>
            <ul>
                <li><b>행사명:</b> 2026 청춘 페스티벌</li>
                <li><b>예상 인원:</b> 5,000명 | <b>예산:</b> 5,000만원</li>
                <li><b>도면 플랫폼:</b> 오늘의 집(Archisketch) 규격 실시간 디지털 트윈</li>
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
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;">응급의료센터 및 출입구가 직선 최단 코스로 연결됨</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;">동선 분리성</td>
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;">90점</td>
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;"><span class="badge badge-excellent">매우 우수</span></td>
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;">푸드존({food_pos})과 공연장({stage_pos}) 간 시야 및 연기 간섭 최적 차단</td>
                </tr>
                <tr>
                    <td style="padding: 10px;">이용 편의성</td>
                    <td style="padding: 10px;">88점</td>
                    <td style="padding: 10px;"><span class="badge badge-good">우수</span></td>
                    <td style="padding: 10px;">화장실({toilet_pos}) 및 휴게 공간의 동선 균형 확보</td>
                </tr>
            </table>

            <h3 style="margin-top: 20px;">3. AI 도면 배치 요약 및 권장사항</h3>
            <ol>
                <li><b>푸드존 현황:</b> 위치 {food_pos} - 주 동선 정체를 예방하도록 독립 구역 배치 완료.</li>
                <li><b>화장실 현황:</b> 위치 {toilet_pos} - 편의성과 배수관 인프라 접근성 충족.</li>
                <li><b>운영 추천:</b> 메인 무대 시작 전 주 출입구 안내 센터(X:{facs['info']['x']}, Y:{facs['info']['y']})에 안내 요원 2명 추가 배치 권장.</li>
            </ol>
            
            <div style="background-color: #EFF6FF; padding: 15px; border-radius: 8px; margin-top: 20px; border: 1px solid #BFDBFE;">
                💡 <b>총평:</b> 본 설계안은 대시보드 대화를 통해 최적화되었으며, 상사 보고 및 실제 시공 및 행사장 구축에 즉시 활용 가능합니다.
            </div>
        </div>
    """, unsafe_allow_html=True)

    rc1, rc2 = st.columns(2)
    with rc1:
        st.download_button("📥 보고서 파일 다운로드 (.txt)", data="2026 청춘 페스티벌 공간 최적화 보고서 내용...", file_name="event_ai_report.txt", type="primary", use_container_width=True)
    with rc2:
        if st.button("🔄 최신 AI 배치 데이터로 보고서 갱신", use_container_width=True):
            st.toast("대시보드의 최신 도면 위치 수치가 보고서에 성공적으로 반영되었습니다!")

# -------------------------------------------------------------------
# PAGE 4: 설정 화면
# -------------------------------------------------------------------
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
        st.subheader("🖥️ 아키스케치 2D 엔진 옵션")
        st.toggle("격자(Grid) 및 치수선 자동 표시", value=True)
        st.toggle("AI 챗봇 변경 시 자동 리런(Rerun)", value=True)
        st.selectbox("AI 모델 선택", ["EventArchitect-v4.2 (최신/권장)", "EventArchitect-Lite"])
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("로그아웃", type="primary"):
        st.session_state['logged_in'] = False
        st.session_state['page'] = 'home'
        st.rerun()
