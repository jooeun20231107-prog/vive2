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

    /* 상단 로고 버튼 및 사이드바 간격 */
    div[data-testid="stSidebarHeader"] {
        padding-top: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

DEFAULT_FACILITIES = {
    "stage": {
        "name": "공연장",
        "icon": "🎪",
        "hex": "#8B5CF6",
        "x": 500, "y": 100, "w": 240, "h": 110,
        "reason": "북쪽 중앙 상단에 위치시켜 모든 관람객의 시야각과 음향 전달을 극대화했습니다."
    },
    "booth": {
        "name": "체험부스",
        "icon": "🛍️",
        "hex": "#3B82F6",
        "x": 190, "y": 130, "w": 180, "h": 150,
        "reason": "북서쪽 진입 구역에 부스 단지를 형성하여 초기 관람객 유입률을 높였습니다."
    },
    "food": {
        "name": "푸드존",
        "icon": "🍔",
        "hex": "#F97316",
        "x": 190, "y": 380, "w": 180, "h": 150,
        "reason": "서쪽 측면에 독립 배치하여 조리 연기 확산을 막고 관람 동선과 유연하게 분리했습니다."
    },
    "rest": {
        "name": "휴게공간",
        "icon": "🏕️",
        "hex": "#10B981",
        "x": 500, "y": 360, "w": 280, "h": 180,
        "reason": "중앙 잔디 광장에 위치시켜 메인 무대 감상과 쉼터 역할을 동시에 수행합니다."
    },
    "medical": {
        "name": "응급의료센터",
        "icon": "🚑",
        "hex": "#EF4444",
        "x": 820, "y": 120, "w": 160, "h": 100,
        "reason": "동쪽 외곽 비상 도로 옆에 배치하여 구급차의 최단 진출입 코스를 보장합니다."
    },
    "toilet": {
        "name": "화장실",
        "icon": "🚻",
        "hex": "#2563EB",
        "x": 820, "y": 260, "w": 160, "h": 100,
        "reason": "동쪽 측면에 위치시켜 인프라 접근성을 확보하고 대기 줄 최소화를 유도합니다."
    },
    "info": {
        "name": "안내센터",
        "icon": "ℹ️",
        "hex": "#EC4899",
        "x": 500, "y": 580, "w": 160, "h": 60,
        "reason": "주 출입구 정면에 위치시켜 길 안내 및 관람 문의를 신속하게 처리합니다."
    },
    "exit": {
        "name": "출입구",
        "icon": "🚪",
        "hex": "#F43F5E",
        "x": 500, "y": 660, "w": 180, "h": 50,
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
if 'chat_messages' not in st.session_state:
    st.session_state['chat_messages'] = [
        {"role": "assistant", "content": "안녕하세요! AI 이벤트 아키텍트입니다. '푸드존을 더 멀리 이동해줘' 또는 '화장실을 의료 센터 근처로 배치해줘'와 같이 원하시는 배치를 말씀해주세요."}
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
    st.caption("🏞️ 실제 축제장 현장 조감도 기반 입체 디지털 트윈 모드입니다.")

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
                st.text_input("장소", "서울 올림픽공원 잔디마당")
                st.text_input("진행 시간", "5시간")

            btn_gen = st.form_submit_button("✨ AI 이벤트 디자인 생성", type="primary", use_container_width=True)
            if btn_gen:
                st.session_state['digital_twin_generated'] = True
                st.session_state['facilities'] = DEFAULT_FACILITIES.copy()
                st.toast("AI가 실제 장소 규격에 맞는 조감도 디지털 트윈을 생성했습니다!")

    if not st.session_state['digital_twin_generated']:
        st.info("👆 위 '행사 기본 정보 및 예산 설정'을 확인하고 [✨ AI 이벤트 디자인 생성] 버튼을 누르시면 디지털 트윈 도면이 펼쳐집니다.")
    else:
        st.markdown("""
            <div style="background-color: #FFFFFF; padding: 12px 20px; border-radius: 12px; border: 1px solid #CBD5E1; margin-bottom: 15px; display: flex; justify-content: space-between; font-size:0.92rem;">
                <span>🎪 <b>행사명:</b> 2026 청춘 페스티벌</span>
                <span>🎯 <b>목적:</b> 축제/공연</span>
                <span>👥 <b>예상 인원:</b> 5,000명</span>
                <span>💰 <b>예산:</b> 5,000만원</span>
                <span>📍 <b>장소:</b> 올림픽공원 잔디마당</span>
            </div>
        """, unsafe_allow_html=True)

        col_main_left, col_main_right = st.columns([2.3, 1])

        with col_main_left:
            st.markdown("### 🎪 행사장 배치도 (디지털 트윈 기반)")
            st.caption("AI가 구역별 동선과 안전성을 종합 분석하여 입체 조감도 형태로 배치한 현장 도면입니다.")

            facs = st.session_state['facilities']

            svg_elements = []
            for key, f in facs.items():
                is_sel = (st.session_state['selected_facility'] == key)
                stroke_clr = "#0284C7" if is_sel else "#FFFFFF"
                stroke_w = "4" if is_sel else "2"
                
                elem_svg = f"""
                <g transform="translate({f['x'] - f['w']//2}, {f['y'] - f['h']//2})">
                    <rect x="0" y="0" width="{f['w']}" height="{f['h']}" rx="16" fill="{f['hex']}" fill-opacity="0.88" stroke="{stroke_clr}" stroke-width="{stroke_w}" filter="drop-shadow(0px 8px 12px rgba(0,0,0,0.25))"/>
                    <rect x="8" y="8" width="{f['w']-16}" height="{f['h']-16}" rx="12" fill="#FFFFFF" fill-opacity="0.15"/>
                    <text x="{f['w']//2}" y="{f['h']//2 + 6}" fill="#FFFFFF" font-size="16" font-weight="900" text-anchor="middle" style="font-family: sans-serif;">{f['icon']} {f['name']}</text>
                </g>
                """
                svg_elements.append(elem_svg)

            all_svg_items = "\n".join(svg_elements)

            festival_map_html = f"""
            <div style="position: relative; width: 100%; border-radius: 20px; overflow: hidden; box-shadow: 0 12px 30px rgba(0,0,0,0.18); border: 2px solid #38BDF8;">
                <svg viewBox="0 0 1000 720" style="width: 100%; height: auto; background-color: #3D7C47; display: block;">
                    <defs>
                        <pattern id="grassPattern" width="40" height="40" patternUnits="userSpaceOnUse">
                            <rect width="40" height="40" fill="#4B8B52"/>
                            <circle cx="20" cy="20" r="18" fill="#43804A"/>
                        </pattern>
                        <linearGradient id="roadGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#E2E8F0" />
                            <stop offset="100%" stop-color="#CBD5E1" />
                        </linearGradient>
                    </defs>

                    <rect width="1000" height="720" fill="url(#grassPattern)"/>

                    <rect x="30" y="30" width="940" height="660" rx="24" fill="none" stroke="#2D5A33" stroke-width="12"/>

                    <path d="M 500,690 L 500,500 L 220,500 L 220,200 L 500,200 L 820,200 L 820,500 L 500,500" stroke="url(#roadGrad)" stroke-width="48" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
                    
                    <path d="M 500,680 L 500,500 L 220,500 L 220,200 L 500,200 L 820,200 L 820,500 L 500,500" stroke="#0284C7" stroke-width="4" stroke-dasharray="10,8" stroke-linecap="round" stroke-linejoin="round" fill="none"/>

                    <circle cx="500" cy="380" r="110" fill="#22C55E" fill-opacity="0.3" stroke="#86EFAC" stroke-width="3" stroke-dasharray="6,4"/>

                    <circle cx="80" cy="80" r="22" fill="#2D5A33"/>
                    <circle cx="140" cy="60" r="28" fill="#2D5A33"/>
                    <circle cx="920" cy="80" r="24" fill="#2D5A33"/>
                    <circle cx="860" cy="60" r="26" fill="#2D5A33"/>
                    <circle cx="70" cy="640" r="25" fill="#2D5A33"/>
                    <circle cx="930" cy="640" r="25" fill="#2D5A33"/>

                    {all_svg_items}

                    <g transform="translate(40, 520)">
                        <rect x="0" y="0" width="150" height="150" rx="12" fill="#FFFFFF" fill-opacity="0.9" stroke="#CBD5E1" stroke-width="2"/>
                        <text x="12" y="24" font-size="13" font-weight="bold" fill="#0F172A">📍 범례 (Legend)</text>
                        <circle cx="20" cy="44" r="6" fill="#8B5CF6"/><text x="34" y="48" font-size="11" fill="#334155" font-weight="bold">공연장</text>
                        <circle cx="20" cy="62" r="6" fill="#3B82F6"/><text x="34" y="66" font-size="11" fill="#334155" font-weight="bold">체험부스</text>
                        <circle cx="20" cy="80" r="6" fill="#F97316"/><text x="34" y="84" font-size="11" fill="#334155" font-weight="bold">푸드존</text>
                        <circle cx="20" cy="98" r="6" fill="#10B981"/><text x="34" y="102" font-size="11" fill="#334155" font-weight="bold">휴게공간</text>
                        <circle cx="20" cy="116" r="6" fill="#EF4444"/><text x="34" y="120" font-size="11" fill="#334155" font-weight="bold">의료센터/화장실</text>
                        <line x1="14" y1="134" x2="28" y2="134" stroke="#0284C7" stroke-width="3" stroke-dasharray="3,2"/>
                        <text x="34" y="138" font-size="11" fill="#0284C7" font-weight="bold">주요 이동 동선</text>
                    </g>

                </svg>
            </div>
            """
            st.components.v1.html(festival_map_html, height=540, scrolling=False)

            st.markdown("**👇 시설 버튼을 선택하면 오른쪽에 해당 공간의 최적 배치 사유가 안내됩니다:**")
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
            
            st.markdown("### 💡 공간 배치 요약")
            st.markdown(f"""
                <div class="reason-box">
                    <h4 style="color: {current_fac['hex']}; margin-top: 0;">{current_fac['icon']} {current_fac['name']}</h4>
                    <p style="color: #334155; font-size: 0.95rem; line-height: 1.6;">
                        <b>[AI 아키텍처 배치 근거]</b><br>
                        {current_fac['reason']}
                    </p>
                </div>
            """, unsafe_allow_html=True)

            st.divider()

            st.markdown("### 🔥 AI 군중 시뮬레이션")
            if st.button("🚨 AI 군중 예측 (혼잡도 Heatmap 실행)", type="primary", use_container_width=True):
                st.session_state['simulated'] = True

            if st.session_state['simulated']:
                st.caption("구역별 인파 밀집도 예측 (붉은색: 인파 정체 위험 구역)")
                np.random.seed(42)
                sim_grid = np.random.rand(12, 12) * 50
                sim_grid[2, 5] += 40  # 무대 앞 혼잡
                sim_grid[8, 2] += 30  # 푸드존 앞 혼잡
                fig = px.imshow(sim_grid, color_continuous_scale='YlOrRd', labels=dict(color="혼잡도"))
                fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=200)
                st.plotly_chart(fig, use_container_width=True)

            st.divider()

            st.markdown("### 💬 AI 설계 어시스턴트")
            st.caption("AI 대화창에 배치를 명령해보세요!")

            chat_box = st.container(height=260)
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
