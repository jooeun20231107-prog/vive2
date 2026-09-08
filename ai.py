import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go

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
    # 1. 왼쪽 위 이벤트 아키텍트 AI 로고 (클릭 시 홈으로 돌아감)
    if st.button("🎪 이벤트 아키텍트 AI", key="logo_btn", use_container_width=True, type="primary"):
        st.session_state['page'] = 'home'
        st.rerun()

    st.caption("AI 기반 행사 자동 설계 플랫폼")
    st.divider()

    # 네비게이션 메뉴
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

    # 사이드바 하단 로그인 사용자 정보
    if st.session_state['logged_in']:
        st.markdown(f"👤 **{st.session_state['username']}** 님 로그인 중")
        if st.button("로그아웃", key="sidebar_logout"):
            st.session_state['logged_in'] = False
            st.rerun()
    else:
        st.warning("로그인이 필요합니다.")

# 상단 우측 로그인/회원가입/설정 빠른 접근 바
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
                st.subheader("로그인")
                u_id = st.text_input("아이디", value="주은님")
                u_pw = st.text_input("비밀번호", type="password")
                if st.button("로그인하기", type="primary"):
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = u_id
                    st.rerun()
    with c_set:
        if st.button("⚙️", help="설정으로 이동"):
            st.session_state['page'] = 'settings'
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# -------------------------------------------------------------------
# PAGE 1: 홈 화면 (2개의 큰 박스 카드가 위치)
# -------------------------------------------------------------------
if st.session_state['page'] == 'home':
    st.markdown("## 🚀 시작할 메뉴를 선택하세요")
    st.caption("AI를 기반으로 입체적인 디지털 트윈 행사장 공간을 설계하거나, 상사 보고용 보고서를 자동 작성합니다.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2개의 대형 박스 (대시보드칸, AI 보고서칸)
    col_dash, col_rep = st.columns(2)

    with col_dash:
        st.markdown("""
            <div class="hero-card">
                <h1 style="font-size: 2.5rem; margin-bottom: 10px;">📊</h1>
                <h2 style="color: #1E3A8A; margin-bottom: 12px;">AI 기반 행사 자동 설계 대시보드</h2>
                <p style="color: #475569; font-size: 1.05rem; line-height: 1.6;">
                    이벤트 목적, 예산, 예상 인원을 입력하면 AI가 최적화된 <b>입체 3D 디지털 트윈 공간</b>을 자동 생성합니다.<br>
                    군중 예측 시뮬레이션 및 AI 챗봇 맞춤 설계 기능을 제공합니다.
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("대시보드 바로가기 ➡️", key="go_dash_btn", type="primary", use_container_width=True):
            st.session_state['page'] = 'dashboard'
            st.rerun()

    with col_rep:
        st.markdown("""
            <div class="hero-card">
                <h1 style="font-size: 2.5rem; margin-bottom: 10px;">📄</h1>
                <h2 style="color: #1E3A8A; margin-bottom: 12px;">AI 종합 분석 보고서</h2>
                <p style="color: #475569; font-size: 1.05rem; line-height: 1.6;">
                    설계된 행사장 배치안을 기반으로 <b>직장상사에게 즉시 보고할 수 있는 보고서</b>를 자동 생성합니다.<br>
                    안전성, 동선 효율성, 예산 적합성 지표 및 AI 개선 권장사항을 한눈에 확인할 수 있습니다.
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("AI 보고서 바로가기 ➡️", key="go_rep_btn", type="secondary", use_container_width=True):
            st.session_state['page'] = 'report'
            st.rerun()

# -------------------------------------------------------------------
# PAGE 2: 대시보드 화면
# -------------------------------------------------------------------
elif st.session_state['page'] == 'dashboard':
    st.markdown("## 📊 AI 기반 행사 자동 설계 대시보드")

    # 1. 상단 이벤트 정보 입력 칸
    with st.expander("📌 행사 기본 정보 입력", expanded=not st.session_state['digital_twin_generated']):
        with st.form("event_input_form"):
            ic1, ic2, ic3 = st.columns(3)
            with ic1:
                e_name = st.text_input("이벤트 이름", "2026 청춘 페스티벌")
                e_purpose = st.selectbox("이벤트 목적", ["축제/공연", "박람회/전시", "지역 문화 활성화", "기업 행사"])
            with ic2:
                e_visitors = st.number_input("예상 방문객 수 (명)", value=5000, step=500)
                e_budget = st.text_input("예산", "5,000만원")
            with ic3:
                e_location = st.text_input("장소 (실외/실내)", "서울 올림픽공원 잔디마당 (실외)")
                e_duration = st.text_input("진행 시간", "5시간")

            btn_gen = st.form_submit_button("✨ AI 이벤트 디자인 생성", type="primary", use_container_width=True)
            if btn_gen:
                st.session_state['digital_twin_generated'] = True
                st.toast("AI가 장소 환경 데이터를 기반으로 디지털 트윈 배치를 완료했습니다!")

    # 2. 메인 디지털 트윈 대시보드 구역
    if not st.session_state['digital_twin_generated']:
        st.info("💡 상단의 행사 기본 정보를 확인하신 후 **[✨ AI 이벤트 디자인 생성]** 버튼을 눌러 디지털 트윈 공간을 생성하세요.")
    else:
        # 주요 요약 정보 태그 바
        st.markdown("""
            <div style="background-color: #FFFFFF; padding: 12px 20px; border-radius: 12px; border: 1px solid #E2E8F0; margin-bottom: 15px; display: flex; justify-content: space-between;">
                <span>🎪 <b>행사명:</b> 2026 청춘 페스티벌</span>
                <span>🎯 <b>목적:</b> 축제/공연</span>
                <span>👥 <b>예상 인원:</b> 5,000명</span>
                <span>💰 <b>예산:</b> 5,000만원</span>
                <span>📍 <b>장소:</b> 올림픽공원</span>
            </div>
        """, unsafe_allow_html=True)

        col_main_left, col_main_right = st.columns([2.3, 1])

        with col_main_left:
            m_col1, m_col2 = st.columns([2, 1])
            with m_col1:
                st.markdown("### 🌐 행사장 배치도 (디지털 트윈 기반)")
            with m_col2:
                # Map View Mode Switcher buttons
                v_col1, v_col2, v_col3 = st.columns(3)
                with v_col1:
                    if st.button("🖼️ 2D 지도", type="primary" if st.session_state['map_view_mode'] == '2D' else "secondary", use_container_width=True):
                        st.session_state['map_view_mode'] = '2D'
                        st.rerun()
                with v_col2:
                    if st.button("🧊 3D 보기", type="primary" if st.session_state['map_view_mode'] == '3D' else "secondary", use_container_width=True):
                        st.session_state['map_view_mode'] = '3D'
                        st.rerun()
                with v_col3:
                    if st.button("📐 CAD 도면", type="primary" if st.session_state['map_view_mode'] == 'CAD' else "secondary", use_container_width=True):
                        st.session_state['map_view_mode'] = 'CAD'
                        st.rerun()

            # 1) 2D Map View Mode (Matching Image 2 Layout)
            if st.session_state['map_view_mode'] == '2D':
                # SVG Visual Map matching Image 2 perfectly
                map_html = """
                <div style="position: relative; width: 100%; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.15); border: 1px solid #CBD5E1;">
                    <svg viewBox="0 0 1000 700" style="width: 100%; height: auto; background-color: #7CA962; display: block;">
                        <!-- Outer roads and terrain -->
                        <path d="M 0,0 L 1000,0 L 1000,700 L 0,700 Z" fill="#60964A" />
                        <!-- Peripheral Trees / Park Boundary -->
                        <path d="M 20,20 Q 500,-10 980,20 L 980,680 Q 500,710 20,680 Z" fill="#4C7E3A" stroke="#3A632B" stroke-width="8" />
                        <path d="M 50,50 L 950,50 L 950,650 L 50,650 Z" fill="#75A65A" />
                        
                        <!-- Main Asphalt Roads -->
                        <path d="M 900,20 C 950,200 950,500 900,680" stroke="#94A3B8" stroke-width="24" fill="none" stroke-linecap="round"/>
                        <path d="M 900,20 C 950,200 950,500 900,680" stroke="#CBD5E1" stroke-width="2" stroke-dasharray="6,6" fill="none"/>
                        
                        <!-- Internal Walkways / Pedestrian Pathways -->
                        <path d="M 500,650 L 500,500 L 320,500 L 320,180 L 500,180 L 500,80" stroke="#E2E8F0" stroke-width="32" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M 500,500 L 680,500 L 680,180 L 500,180" stroke="#E2E8F0" stroke-width="32" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M 320,340 L 680,340" stroke="#E2E8F0" stroke-width="28" fill="none"/>
                        
                        <!-- Pedestrian Guided Flow Lines (Blue Dashed Arrow Routes) -->
                        <path d="M 460,650 L 460,520 L 310,520 L 310,160 L 690,160 L 690,520 L 540,520" stroke="#0284C7" stroke-width="5" stroke-dasharray="10,8" fill="none"/>
                        <circle cx="460" cy="620" r="6" fill="#0284C7"/>
                        <polygon points="460,640 452,620 468,620" fill="#0284C7"/>
                        <polygon points="310,340 302,355 318,355" fill="#0284C7"/>
                        <polygon points="500,160 515,152 515,168" fill="#0284C7"/>
                        <polygon points="690,340 682,325 698,325" fill="#0284C7"/>

                        <!-- Center Rest Area (Green Grass Field + Trees + Fountain) -->
                        <rect x="340" y="200" width="320" height="280" rx="20" fill="#5E9946" stroke="#487834" stroke-width="4"/>
                        <!-- Fountain in Rest Area -->
                        <circle cx="580" cy="420" r="22" fill="#38BDF8" stroke="#0284C7" stroke-width="3"/>
                        <circle cx="580" cy="420" r="10" fill="#BAE6FD"/>
                        <!-- Park Umbrellas & Trees -->
                        <circle cx="380" cy="240" r="12" fill="#22C55E"/>
                        <circle cx="420" cy="230" r="10" fill="#16A34A"/>
                        <circle cx="620" cy="240" r="14" fill="#22C55E"/>
                        <circle cx="380" cy="440" r="12" fill="#EAB308"/>
                        <circle cx="450" cy="420" r="11" fill="#EF4444"/>
                        <circle cx="520" cy="440" r="12" fill="#3B82F6"/>

                        <!-- TOP CENTER: 공연장 (Stage Zone) -->
                        <g transform="translate(370, 60)">
                            <rect x="0" y="0" width="260" height="100" rx="12" fill="#818CF8" stroke="#4F46E5" stroke-width="3"/>
                            <rect x="20" y="10" width="220" height="45" rx="8" fill="#C084FC"/>
                            <!-- Audience Chairs -->
                            <rect x="30" y="62" width="200" height="30" fill="#6366F1" opacity="0.4" rx="4"/>
                        </g>

                        <!-- TOP LEFT: 체험부스 (Booths Zone) -->
                        <g transform="translate(80, 80)">
                            <rect x="0" y="0" width="200" height="180" rx="10" fill="#3B82F6" opacity="0.15"/>
                            <!-- Booth Tents -->
                            <rect x="10" y="10" width="40" height="40" rx="4" fill="#60A5FA" stroke="#2563EB" stroke-width="2"/>
                            <rect x="60" y="10" width="40" height="40" rx="4" fill="#60A5FA" stroke="#2563EB" stroke-width="2"/>
                            <rect x="110" y="10" width="40" height="40" rx="4" fill="#60A5FA" stroke="#2563EB" stroke-width="2"/>
                            <rect x="10" y="60" width="40" height="40" rx="4" fill="#FBBF24" stroke="#D97706" stroke-width="2"/>
                            <rect x="60" y="60" width="40" height="40" rx="4" fill="#FBBF24" stroke="#D97706" stroke-width="2"/>
                            <rect x="110" y="60" width="40" height="40" rx="4" fill="#FBBF24" stroke="#D97706" stroke-width="2"/>
                            <rect x="10" y="110" width="40" height="40" rx="4" fill="#34D399" stroke="#059669" stroke-width="2"/>
                            <rect x="60" y="110" width="40" height="40" rx="4" fill="#34D399" stroke="#059669" stroke-width="2"/>
                        </g>

                        <!-- MID LEFT: 푸드존 (Food Zone) -->
                        <g transform="translate(80, 310)">
                            <rect x="0" y="0" width="200" height="180" rx="10" fill="#F97316" opacity="0.15"/>
                            <rect x="10" y="10" width="50" height="35" rx="4" fill="#FB923C" stroke="#EA580C" stroke-width="2"/>
                            <rect x="70" y="10" width="50" height="35" rx="4" fill="#FB923C" stroke="#EA580C" stroke-width="2"/>
                            <rect x="10" y="55" width="50" height="35" rx="4" fill="#FACC15" stroke="#CA8A04" stroke-width="2"/>
                            <rect x="70" y="55" width="50" height="35" rx="4" fill="#FACC15" stroke="#CA8A04" stroke-width="2"/>
                            <rect x="10" y="100" width="120" height="60" rx="6" fill="#FED7AA" stroke="#F97316" stroke-width="2"/>
                        </g>

                        <!-- TOP RIGHT: 응급의료센터 (Medical Center) -->
                        <g transform="translate(730, 80)">
                            <rect x="0" y="0" width="160" height="100" rx="10" fill="#F87171" stroke="#DC2626" stroke-width="3"/>
                            <circle cx="80" cy="45" r="22" fill="#FFFFFF"/>
                            <path d="M 80,33 L 80,57 M 68,45 L 92,45" stroke="#DC2626" stroke-width="7" stroke-linecap="round"/>
                        </g>

                        <!-- MID RIGHT: 화장실 (Restroom Zone) -->
                        <g transform="translate(730, 220)">
                            <rect x="0" y="0" width="160" height="110" rx="10" fill="#60A5FA" stroke="#2563EB" stroke-width="3"/>
                            <rect x="15" y="15" width="60" height="80" rx="6" fill="#EFF6FF"/>
                            <rect x="85" y="15" width="60" height="80" rx="6" fill="#EFF6FF"/>
                        </g>

                        <!-- BOTTOM CENTER: 안내센터 & 출입구 (Info Center & Entrance) -->
                        <g transform="translate(420, 520)">
                            <rect x="0" y="0" width="160" height="60" rx="8" fill="#F472B6" stroke="#DB2777" stroke-width="3"/>
                        </g>
                        <g transform="translate(420, 600)">
                            <rect x="0" y="0" width="160" height="60" rx="8" fill="#334155" stroke="#0F172A" stroke-width="3"/>
                        </g>

                        <!-- FLOATING PIN BADGES (Matching Image 2 Badge Overlay Style) -->
                        <!-- 공연장 Badge -->
                        <g transform="translate(500, 100)">
                            <rect x="-60" y="-18" width="120" height="36" rx="18" fill="#8B5CF6" stroke="#FFFFFF" stroke-width="3"/>
                            <text x="0" y="5" fill="#FFFFFF" font-size="15" font-weight="bold" text-anchor="middle">🎪 공연장</text>
                        </g>

                        <!-- 체험부스 Badge -->
                        <g transform="translate(180, 120)">
                            <rect x="-60" y="-18" width="120" height="36" rx="18" fill="#3B82F6" stroke="#FFFFFF" stroke-width="3"/>
                            <text x="0" y="5" fill="#FFFFFF" font-size="15" font-weight="bold" text-anchor="middle">🛍️ 체험부스</text>
                        </g>

                        <!-- 푸드존 Badge -->
                        <g transform="translate(180, 340)">
                            <rect x="-55" y="-18" width="110" height="36" rx="18" fill="#F97316" stroke="#FFFFFF" stroke-width="3"/>
                            <text x="0" y="5" fill="#FFFFFF" font-size="15" font-weight="bold" text-anchor="middle">🍔 푸드존</text>
                        </g>

                        <!-- 휴게공간 Badge -->
                        <g transform="translate(500, 340)">
                            <rect x="-60" y="-18" width="120" height="36" rx="18" fill="#10B981" stroke="#FFFFFF" stroke-width="3"/>
                            <text x="0" y="5" fill="#FFFFFF" font-size="15" font-weight="bold" text-anchor="middle">🏕️ 휴게공간</text>
                        </g>

                        <!-- 응급의료센터 Badge -->
                        <g transform="translate(810, 110)">
                            <rect x="-70" y="-18" width="140" height="36" rx="18" fill="#EF4444" stroke="#FFFFFF" stroke-width="3"/>
                            <text x="0" y="5" fill="#FFFFFF" font-size="14" font-weight="bold" text-anchor="middle">🚑 응급의료센터</text>
                        </g>

                        <!-- 화장실 Badge -->
                        <g transform="translate(810, 260)">
                            <rect x="-55" y="-18" width="110" height="36" rx="18" fill="#2563EB" stroke="#FFFFFF" stroke-width="3"/>
                            <text x="0" y="5" fill="#FFFFFF" font-size="15" font-weight="bold" text-anchor="middle">🚻 화장실</text>
                        </g>

                        <!-- 안내센터 Badge -->
                        <g transform="translate(500, 550)">
                            <rect x="-55" y="-18" width="110" height="36" rx="18" fill="#EC4899" stroke="#FFFFFF" stroke-width="3"/>
                            <text x="0" y="5" fill="#FFFFFF" font-size="15" font-weight="bold" text-anchor="middle">ℹ️ 안내센터</text>
                        </g>

                        <!-- 출입구 Badge -->
                        <g transform="translate(500, 615)">
                            <rect x="-50" y="-16" width="100" height="32" rx="16" fill="#F43F5E" stroke="#FFFFFF" stroke-width="2"/>
                            <text x="0" y="5" fill="#FFFFFF" font-size="14" font-weight="bold" text-anchor="middle">🚪 출입구</text>
                        </g>

                        <!-- BOTTOM-LEFT LEGEND CARD (범례 - Matching Image 2) -->
                        <g transform="translate(30, 420)">
                            <rect x="0" y="0" width="160" height="250" rx="12" fill="#FFFFFF" opacity="0.92" stroke="#CBD5E1" stroke-width="2"/>
                            
                            <circle cx="20" cy="22" r="8" fill="#8B5CF6"/>
                            <text x="36" y="26" font-size="13" font-weight="bold" fill="#1E293B">공연장</text>

                            <circle cx="20" cy="48" r="8" fill="#F97316"/>
                            <text x="36" y="52" font-size="13" font-weight="bold" fill="#1E293B">푸드존</text>

                            <circle cx="20" cy="74" r="8" fill="#3B82F6"/>
                            <text x="36" y="78" font-size="13" font-weight="bold" fill="#1E293B">체험부스</text>

                            <circle cx="20" cy="100" r="8" fill="#10B981"/>
                            <text x="36" y="104" font-size="13" font-weight="bold" fill="#1E293B">휴게공간</text>

                            <circle cx="20" cy="126" r="8" fill="#EF4444"/>
                            <text x="36" y="130" font-size="13" font-weight="bold" fill="#1E293B">응급의료센터</text>

                            <circle cx="20" cy="152" r="8" fill="#EC4899"/>
                            <text x="36" y="156" font-size="13" font-weight="bold" fill="#1E293B">안내센터</text>

                            <circle cx="20" cy="178" r="8" fill="#2563EB"/>
                            <text x="36" y="182" font-size="13" font-weight="bold" fill="#1E293B">화장실</text>

                            <circle cx="20" cy="204" r="8" fill="#1E293B"/>
                            <text x="36" y="208" font-size="13" font-weight="bold" fill="#1E293B">출입구</text>

                            <line x1="12" y1="230" x2="28" y2="230" stroke="#0284C7" stroke-width="4" stroke-dasharray="4,3"/>
                            <text x="36" y="234" font-size="13" font-weight="bold" fill="#0284C7">이동 동선</text>
                        </g>
                    </svg>
                </div>
                """
                st.components.v1.html(map_html, height=520, scrolling=False)

            # 2) 3D View Mode (PyDeck 3D Isometric View)
            elif st.session_state['map_view_mode'] == '3D':
                df_fac = pd.DataFrame(list(FACILITIES.values()))
                
                layer_3d = pdk.Layer(
                    "ColumnLayer",
                    df_fac,
                    get_position=["lon", "lat"],
                    get_elevation="height",
                    elevation_scale=6,
                    radius=14,
                    get_fill_color="color",
                    pickable=True,
                    auto_highlight=True
                )

                layer_text = pdk.Layer(
                    "TextLayer",
                    df_fac,
                    get_position=["lon", "lat"],
                    get_text="name",
                    get_size=15,
                    get_color=[255, 255, 255],
                    get_angle=0,
                    get_text_anchor="'middle'",
                    get_alignment_baseline="'center'"
                )

                view_state = pdk.ViewState(
                    latitude=37.5200,
                    longitude=127.1210,
                    zoom=16.5,
                    pitch=50,
                    bearing=-20
                )

                deck = pdk.Deck(
                    layers=[layer_3d, layer_text],
                    initial_view_state=view_state,
                    tooltip={"html": "<b>{name}</b><br/>아이콘: {icon}"}
                )
                st.pydeck_chart(deck)

            # 3) CAD Drawing Mode (Matching Image 1 CAD Floor Plan Layout Tool)
            elif st.session_state['map_view_mode'] == 'CAD':
                st.info("📐 **도면 그려보기 (CAD 모드)**: 2D 실내/실외 공간 벽면 및 구역의 수치를 정밀 측정하고 편집합니다.")
                
                cad_html = """
                <div style="background-color: #F1F5F9; border-radius: 12px; padding: 20px; border: 2px dashed #94A3B8; text-align: center;">
                    <svg viewBox="0 0 800 450" style="width: 100%; height: 380px; background-color: #FFFFFF; border-radius: 8px;">
                        <!-- Grid Lines -->
                        <defs>
                            <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                                <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#E2E8F0" stroke-width="1"/>
                            </pattern>
                        </defs>
                        <rect width="100%" height="100%" fill="url(#grid)" />
                        
                        <!-- Floor Plan Outline (Image 1 Style Room) -->
                        <rect x="250" y="80" width="300" height="280" fill="none" stroke="#334155" stroke-width="8"/>
                        <line x1="250" y1="200" x2="550" y2="200" stroke="#334155" stroke-width="6"/>
                        <line x1="400" y1="80" x2="400" y2="200" stroke="#334155" stroke-width="6"/>
                        
                        <!-- Dimension Annotations (Image 1 Style) -->
                        <text x="400" y="70" font-size="14" font-weight="bold" fill="#0284C7" text-anchor="middle">3,016 mm</text>
                        <text x="230" y="140" font-size="14" font-weight="bold" fill="#0284C7" text-anchor="end">1,531 mm</text>
                        <text x="570" y="270" font-size="14" font-weight="bold" fill="#0284C7" text-anchor="start">2,407 mm</text>

                        <!-- Room Labels -->
                        <text x="325" y="140" font-size="16" font-weight="bold" fill="#475569" text-anchor="middle">무대 대기실 (3m²)</text>
                        <text x="475" y="140" font-size="16" font-weight="bold" fill="#475569" text-anchor="middle">음향 제어실</text>
                        <text x="400" y="280" font-size="18" font-weight="bold" fill="#1E293B" text-anchor="middle">메인 실내 홀 (8m²)</text>
                    </svg>
                </div>
                """
                st.components.v1.html(cad_html, height=420, scrolling=False)
                
                up_file = st.file_uploader("📂 새로운 캐드 도면 이미지 업로드 (.png, .jpg, .dxf)", type=["png", "jpg", "jpeg"])
                if up_file:
                    st.success(f"도면 파일 '{up_file.name}' 업로드 완료! AI 분석이 시작됩니다.")

            # 시설 누름 버튼 모음 (누르면 오른쪽에 배치 이유 설명)
            st.markdown("**👇 아래 시설 명칭을 클릭하면 오른쪽에 AI 배치 이유 요약이 나타납니다:**")
            fac_keys = list(FACILITIES.keys())
            f_cols = st.columns(4)
            for i, key in enumerate(fac_keys):
                fac_item = FACILITIES[key]
                with f_cols[i % 4]:
                    is_selected = (st.session_state['selected_facility'] == key)
                    btn_type = "primary" if is_selected else "secondary"
                    if st.button(f"{fac_item['icon']} {fac_item['name']}", key=f"btn_fac_{key}", type=btn_type, use_container_width=True):
                        st.session_state['selected_facility'] = key
                        st.rerun()

            st.divider()

            # 하단 AI 시뮬레이션 버튼 및 혼잡도 히트맵
            c_sim_btn, c_sim_desc = st.columns([1, 2])
            with c_sim_btn:
                if st.button("🔥 AI 시뮬레이션 실행 (군중 예측)", type="primary", use_container_width=True):
                    st.session_state['simulated'] = True
                    st.toast("군중 동선 및 병목 구간 예측 완료!")

            if st.session_state['simulated']:
                st.markdown("#### 📈 군중 이용 예측 히트맵 (Heatmap)")
                np.random.seed(42)
                sim_matrix = np.random.rand(15, 15) * 60 + 20
                sim_matrix[5:8, 6:10] += 40  # 무대 및 푸드존 주변 병목 형성

                fig_heat = px.imshow(
                    sim_matrix,
                    labels=dict(x="가로 구역", y="세로 구역", color="혼잡도(%)"),
                    color_continuous_scale="YlOrRd",
                    title="동선상 몰리는 정도 (주요 병목 예측 구간)"
                )
                fig_heat.update_layout(height=320, margin=dict(l=10, r=10, t=30, b=10))
                st.plotly_chart(fig_heat, use_container_width=True)

        with col_main_right:
            # 선택된 공간 배치 이유 요약 카드
            selected_key = st.session_state['selected_facility']
            current_fac = FACILITIES.get(selected_key, FACILITIES['stage'])
            
            st.markdown(f"### 💡 공간 배치 이유 요약")
            st.markdown(f"""
                <div class="reason-box">
                    <h4 style="color: {current_fac['hex']}; margin-top: 0;">{current_fac['icon']} {current_fac['name']}</h4>
                    <p style="color: #334155; font-size: 0.95rem; line-height: 1.5;">
                        <b>[AI 공간 최적화 근거]</b><br>
                        {current_fac['reason']}
                    </p>
                </div>
            """, unsafe_allow_html=True)

            if st.session_state['simulated']:
                st.markdown("#### 📊 AI 평가 결과")
                st.markdown("""
                - **안전성:** <span class="badge badge-excellent">92점 (매우 우수)</span>
                - **동선 효율성:** <span class="badge badge-good">87점 (우수)</span>
                - **접근성:** <span class="badge badge-excellent">90점 (매우 우수)</span>
                - **혼잡도 관리:** <span class="badge badge-good">84점 (우수)</span>
                """, unsafe_allow_html=True)

            st.divider()

            # AI 시뮬레이션 및 디자인 채팅 기능
            st.markdown("### 💬 AI 설계 어시스턴트")
            st.caption("AI와 대화하며 자신만의 이벤트 디자인을 완성하세요.")
            
            chat_box = st.container(height=300)
            with chat_box:
                for message in st.session_state['chat_messages']:
                    with st.chat_message(message["role"]):
                        st.write(message["content"])

            if user_prompt := st.chat_input("예: '화장실 배치를 의료 센터 근처로 이동해줘'"):
                st.session_state['chat_messages'].append({"role": "user", "content": user_prompt})
                
                # AI 답변 반응
                ai_response = f"네! 요청하신 '{user_prompt}' 내용을 분석하여 동선의 안전성과 접근성을 고려해 최적화 재배치를 완료했습니다."
                st.session_state['chat_messages'].append({"role": "assistant", "content": ai_response})
                st.rerun()

# -------------------------------------------------------------------
# PAGE 3: AI 보고서 화면
# -------------------------------------------------------------------
elif st.session_state['page'] == 'report':
    st.markdown("## 📄 AI 기반 행사 설계 종합 보고서")
    st.caption("직장 상사에게 바로 제출할 수 있는 자동 생성 보고서입니다.")

    st.markdown("""
        <div class="custom-card">
            <h2 style="color: #0F172A; text-align: center;">[보고서] 2026 청춘 페스티벌 공간 최적화 및 안전 설계안</h2>
            <p style="text-align: center; color: #64748B;">작성일: 2026년 9월 8일 | 작성 시스템: 이벤트 아키텍트 AI | 보고 대상: 행사 총괄 책임자</p>
            <hr>
            
            <h3>1. 행사 개요</h3>
            <ul>
                <li><b>행사명:</b> 2026 청춘 페스티벌</li>
                <li><b>예상 인원:</b> 5,000명 | <b>예산:</b> 5,000만원</li>
                <li><b>목적:</b> 지역 문화 활성화 및 청년 소통 기회 확대</li>
            </ul>

            <h3>2. AI 종합 공간 평가 결과</h3>
            <table style="width:100%; border-collapse: collapse; margin-top: 10px;">
                <tr style="background-color: #F1F5F9; text-align: left;">
                    <th style="padding: 10px;">평가 항목</th>
                    <th style="padding: 10px;">점수</th>
                    <th style="padding: 10px;">등급</th>
                    <th style="padding: 10px;">주요 평가 요약</th>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;">안전성</td>
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;">92점</td>
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;"><span class="badge badge-excellent">매우 우수</span></td>
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;">비상구 및 응급 의료센터의 최단 진출입로 확보</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;">동선 효율성</td>
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;">87점</td>
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;"><span class="badge badge-good">우수</span></td>
                    <td style="padding: 10px; border-bottom: 1px solid #E2E8F0;">무대와 푸드존 관람 동선 교차 최소화</td>
                </tr>
                <tr>
                    <td style="padding: 10px;">혼잡도 관리</td>
                    <td style="padding: 10px;">84점</td>
                    <td style="padding: 10px;"><span class="badge badge-good">우수</span></td>
                    <td style="padding: 10px;">중앙 휴게공간을 통한 인파 자연 분산 유도</td>
                </tr>
            </table>

            <h3 style="margin-top: 20px;">3. AI 개선 권장사항</h3>
            <ol>
                <li><b>휴식 공간 확충:</b> 공연장과 푸드존 사이 인파 밀집을 완화하기 위해 차양막 의자 추가 설치 권장.</li>
                <li><b>안내 요원 배치:</b> 체험 부스 대기선 정체 예방을 위해 주 출입구에 2명의 동선 유도 요원 우선 배치.</li>
            </ol>
            
            <div style="background-color: #EFF6FF; padding: 15px; border-radius: 8px; margin-top: 20px; border: 1px solid #BFDBFE;">
                💡 <b>총평:</b> 본 설계안을 바탕으로 실제 행사 운영 시 안전사고 위험을 극대화하여 감소시킬 수 있으며, 관람객 만족도가 대폭 향상될 것으로 기대됩니다.
            </div>
        </div>
    """, unsafe_allow_html=True)

    rc1, rc2 = st.columns(2)
    with rc1:
        st.download_button("📥 보고서 PDF/Text 다운로드", data="2026 청춘 페스티벌 공간 최적화 보고서 내용...", file_name="event_ai_report.txt", type="primary", use_container_width=True)
    with rc2:
        if st.button("🔄 최신 AI 데이터로 보고서 재생성", use_container_width=True):
            st.toast("최신 설계안 지표를 반영하여 보고서를 업데이트했습니다!")

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
        st.subheader("🖥️ 시각화 및 AI 엔진 옵션")
        st.toggle("3D 디지털 트윈 GPU 그래픽 가속", value=True)
        st.toggle("실시간 군중 밀도 예측 알림 수신", value=True)
        st.selectbox("AI 모델 선택", ["EventArchitect-v4.2 (최신/권장)", "EventArchitect-Lite"])
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("로그아웃", type="primary"):
        st.session_state['logged_in'] = False
        st.session_state['page'] = 'home'
        st.rerun()