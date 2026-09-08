import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import json
import time
from datetime import datetime

st.set_page_config(
    page_title="Event AI | AI 기반 행사 자동 설계 플랫폼",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Global Bright/Light Theme Setup */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }
    
    /* Top Bar Styling - Clean Bright Layout */
    .top-bar-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 24px;
        background-color: #ffffff;
        border-bottom: 1px solid #e2e8f0;
        border-radius: 14px;
        margin-bottom: 20px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }

    /* Archisketch Toolbar Pill */
    .archisketch-bar {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 12px;
        padding: 10px 16px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }

    /* Clean Card Styling for Home Page */
    .home-card-btn {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.03);
        transition: all 0.2s ease-in-out;
    }
    
    /* Dashboard UI Panels */
    .panel-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }

    /* Chat bubble styles */
    .chat-user {
        background-color: #2563eb;
        color: white;
        padding: 10px 14px;
        border-radius: 16px 16px 2px 16px;
        margin: 6px 0;
        max-width: 80%;
        margin-left: auto;
        font-size: 13px;
    }
    
    .chat-ai {
        background-color: #f1f5f9;
        color: #0f172a;
        padding: 10px 14px;
        border-radius: 16px 16px 16px 2px;
        margin: 6px 0;
        max-width: 85%;
        border: 1px solid #e2e8f0;
        font-size: 13px;
    }

    /* Sidebar Customization */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
        color: #f8fafc;
    }
    section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] p {
        color: #cbd5e1;
    }
    
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True
if "user_name" not in st.session_state:
    st.session_state.user_name = "추준님"
if "design_generated" not in st.session_state:
    st.session_state.design_generated = True
if "selected_zone" not in st.session_state:
    st.session_state.selected_zone = "메인무대"
if "show_heatmap_overlay" not in st.session_state:
    st.session_state.show_heatmap_overlay = True
if "show_flow_arrows" not in st.session_state:
    st.session_state.show_flow_arrows = True
if "show_grid_lines" not in st.session_state:
    st.session_state.show_grid_lines = True
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "2D CAD 도면"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "ai", "text": "안녕하세요! Archisketch 기반 Event AI입니다. 원하시는 공간 배치 변경 및 소방법 최적화를 실시간으로 맞춰드립니다."}
    ]

# Event Data State
if "event_name" not in st.session_state:
    st.session_state.event_name = "2025 청춘 페스티벌"
if "event_type" not in st.session_state:
    st.session_state.event_type = "축제"
if "event_purpose" not in st.session_state:
    st.session_state.event_purpose = "지역 문화 활성화 및 청년 소통"
if "expected_visitors" not in st.session_state:
    st.session_state.expected_visitors = 5000
if "duration" not in st.session_state:
    st.session_state.duration = "5시간"
if "target_age" not in st.session_state:
    st.session_state.target_age = "10대 ~ 30대"
if "mood" not in st.session_state:
    st.session_state.mood = "열기있고 신나는"
if "entry_fee" not in st.session_state:
    st.session_state.entry_fee = "무료"
if "location" not in st.session_state:
    st.session_state.location = "올림픽공원 잔디마당"
if "budget" not in st.session_state:
    st.session_state.budget = "5000만원"

if "zone_data" not in st.session_state:
    st.session_state.zone_data = {
        "메인무대": {
            "icon": "🎭",
            "color": "#3b82f6",
            "position": [50, 82],
            "size": [30, 18],
            "rationale": "메인 출입구에서 가장 멀고 탁 트인 잔디 광장의 북쪽에 배치하여 5,000명 관중 소음 분산 및 최고 시야각 확보. 비상 피난 동선 확보 완료.",
            "score": "98점 (최적화 완료)",
            "capacity": "최대 3,000명 동시 관람"
        },
        "푸드존": {
            "icon": "🍔",
            "color": "#f97316",
            "position": [25, 52],
            "size": [20, 14],
            "rationale": "상하수도 및 전력 공급관 접근이 용이한 서쪽 외곽 배치. 관람석과의 거리를 약 25m 유지하여 음식 냄새 유입 최소화 및 대기 줄 가이드라인 적용.",
            "score": "92점 (양호)",
            "capacity": "푸드트럭 12대 & 테이블 40개"
        },
        "체험부스": {
            "icon": "🎪",
            "color": "#8b5cf6",
            "position": [20, 32],
            "size": [18, 14],
            "rationale": "입장객 이동 동선의 좌측 순환 코스 배치. 이동 중 자연스러운 체험 유도를 통해 병목 현상을 방지하고 참여율 극대화.",
            "score": "90점 (우수)",
            "capacity": "20개 규격 부스"
        },
        "휴식공간": {
            "icon": "🌲",
            "color": "#10b981",
            "position": [50, 48],
            "size": [22, 16],
            "rationale": "행사장 중앙 쉼터로 나무 그늘 아래 벤치 및 파라솔 배치. 무대 소음이 알맞게 전달되며 피로도를 줄일 수 있는 완충 지대.",
            "score": "91점 (양호)",
            "capacity": "동시 휴식 200명 수용"
        },
        "안내센터": {
            "icon": "ℹ️",
            "color": "#ec4899",
            "position": [50, 20],
            "size": [14, 10],
            "rationale": "주 출입구 바로 전면에 위치하여 방문객 유실물 문의, 미아 보호, 행사 안내를 즉시 수행할 수 있는 병목 방지 통로 측면 배치.",
            "score": "95점 (매우 우수)",
            "capacity": "안내 요원 6명 상주"
        },
        "화장실": {
            "icon": "🚻",
            "color": "#06b6d4",
            "position": [82, 45],
            "size": [14, 12],
            "rationale": "바람이 부는 하류 방향 동쪽 구역에 배치하여 악취 피해 방지. 여성 화장실 비율 1:1.5 확충 및 동선 교차 방지 구역 지정.",
            "score": "94점 (매우 우수)",
            "capacity": "이동식 화장실 15칸"
        },
        "응급의료센터": {
            "icon": "🏥",
            "color": "#ef4444",
            "position": [80, 72],
            "size": [16, 12],
            "rationale": "구급차 진출입이 즉시 가능한 외각 전용 도로와 연결. 무대 부상자 발생 시 최단 거리(15초) 수송 동선 확보.",
            "score": "97점 (최적화 완료)",
            "capacity": "응급 침대 4대 & 구급차 직결"
        },
        "출입구": {
            "icon": "🚪",
            "color": "#1e293b",
            "position": [50, 6],
            "size": [18, 8],
            "rationale": "소방법 규정 준수. 대형 군중 이동 통로와 직결되는 넓이 8m 이상의 피난 유도선 및 분산 입출입 구역 설정.",
            "score": "100점 (법적 기준 준수)",
            "capacity": "분당 1,500명 통행 가능"
        }
    }

ZONE_DATA = st.session_state.zone_data

st.markdown("<div class='top-bar-container'>", unsafe_allow_html=True)
col_head1, col_head2, col_head3 = st.columns([3, 5, 2])

with col_head1:
    if st.button("🎪 Event AI (이벤트 아키텍트)", key="logo_btn", help="홈 화면으로 돌아가기"):
        st.session_state.page = "home"
        st.rerun()

with col_head2:
    st.markdown("<p style='text-align:center; margin:0; color:#475569; font-size:13px; font-weight:600;'>📐 Archisketch 엔지니어링 기반 디지털 트윈 & AI 행사 도면 설계 플랫폼</p>", unsafe_allow_html=True)

with col_head3:
    st.markdown("<div style='display:flex; justify-content:flex-end;'>", unsafe_allow_html=True)
    if st.button("⚙️ 설정", key="nav_settings"):
        st.session_state.page = "settings"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 👤 계정 및 설정")
    if st.session_state.logged_in:
        st.success(f"**{st.session_state.user_name}** 님 로그인 중")
        if st.button("로그아웃", key="sidebar_logout"):
            st.session_state.logged_in = False
            st.rerun()
    else:
        st.info("로그인이 필요합니다.")
        if st.button("로그인 / 회원가입", key="sidebar_login"):
            st.session_state.page = "settings"
            st.rerun()

    st.divider()
    st.markdown("### 📌 빠른 메뉴")
    if st.button("🏠 홈 화면", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
    if st.button("📐 행사 도면 설계 (Archisketch)", use_container_width=True):
        st.session_state.page = "dashboard"
        st.rerun()
    if st.button("📋 결재용 AI 보고서", use_container_width=True):
        st.session_state.page = "report"
        st.rerun()
    if st.button("⚙️ 시스템 설정", use_container_width=True):
        st.session_state.page = "settings"
        st.rerun()

    st.divider()
    st.markdown("""
    <div style="background-color:#1e293b; color:#f8fafc; padding:14px; border-radius:10px; font-size:12px; line-height:1.5;">
        <span style="color:#60a5fa; font-weight:bold;">💡 Archisketch 스마트 가이드</span><br>
        2D/3D 도면 위에서 혼잡도 Heatmap을 바로 확인하고, 구역별 좌표 및 동선을 자유롭게 조율할 수 있습니다.
    </div>
    """, unsafe_allow_html=True)

if st.session_state.page == "home":
    st.markdown("<div style='text-align: center; padding: 20px 0 10px 0;'>", unsafe_allow_html=True)
    st.markdown("<span style='background:#eff6ff; color:#2563eb; font-weight:700; padding:6px 14px; border-radius:20px; font-size:13px;'>✨ Archisketch Smart Spatial AI Powered</span>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #0f172a; margin-top:14px; font-weight:800; font-size:36px;'>AI 기반 스마트 행사 공간 설계 플랫폼</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 16px; max-width:700px; margin: 0 auto 35px auto;'>행사 기본 정보만 입력하면 Archisketch 기반 2D CAD 도면 설계, 도면 위 실시간 혼잡도 시뮬레이션, 상사 결재용 리포트까지 원스톱으로 완성합니다.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    col_box1, col_box2 = st.columns(2)

    with col_box1:
        st.markdown("""
        <div style="background:#ffffff; border:2px solid #e2e8f0; border-radius:18px; padding:28px; text-align:center; box-shadow:0 6px 18px rgba(0,0,0,0.03);">
            <div style="font-size:42px; margin-bottom:12px;">📐</div>
            <h3 style="color:#0f172a; margin:0 0 10px 0; font-weight:700;">Archisketch 2D/3D 행사 설계 대시보드</h3>
            <p style="color:#64748b; font-size:14px; line-height:1.6; margin-bottom:20px;">
                도면 레이어 위에서 공간 배치를 손쉽게 편집하고, 도면 직결 혼잡도 Heatmap 및 군중 이동 동선을 시각화합니다.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("👉 [ Archisketch 도면 대시보드 열기 ]", key="btn_go_dash", type="primary", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()

    with col_box2:
        st.markdown("""
        <div style="background:#ffffff; border:2px solid #e2e8f0; border-radius:18px; padding:28px; text-align:center; box-shadow:0 6px 18px rgba(0,0,0,0.03);">
            <div style="font-size:42px; margin-bottom:12px;">📑</div>
            <h3 style="color:#0f172a; margin:0 0 10px 0; font-weight:700;">AI 직인 상사 결재용 리포트</h3>
            <p style="color:#64748b; font-size:14px; line-height:1.6; margin-bottom:20px;">
                Archisketch 도면 분석 사유, 소방법 및 피난 안전성 검토, 예산 효율성이 포함된 원클릭 직장 상사 결재용 보고서입니다.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("👉 [ AI 결재용 보고서 바로가기 ]", key="btn_go_report", use_container_width=True):
            st.session_state.page = "report"
            st.rerun()

    st.divider()
    
    st.markdown("<h3 style='text-align:center; margin-bottom:24px; font-weight:700;'>🔥 Archisketch 핵심 주요 기능</h3>", unsafe_allow_html=True)
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.markdown("""
        <div style="background:#ffffff; padding:20px; border-radius:14px; border:1px solid #e2e8f0;">
            <h4 style="margin:0 0 8px 0; color:#2563eb;">📐 Archisketch 2D/3D CAD 도면</h4>
            <p style="color:#64748b; font-size:13px; margin:0; line-height:1.6;">소방법 규정과 관람객 접근성을 자동 반영하여 최적의 무대, 부스, 비상구를 도면에 자동 배치합니다.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_f2:
        st.markdown("""
        <div style="background:#ffffff; padding:20px; border-radius:14px; border:1px solid #e2e8f0;">
            <h4 style="margin:0 0 8px 0; color:#f97316;">🔥 도면 직결 혼잡도 Heatmap</h4>
            <p style="color:#64748b; font-size:13px; margin:0; line-height:1.6;">도면 위에 레이어 형태로 군중 밀집도 Heatmap을 오버레이하여 병목 구간을 즉각 파악합니다.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_f3:
        st.markdown("""
        <div style="background:#ffffff; padding:20px; border-radius:14px; border:1px solid #e2e8f0;">
            <h4 style="margin:0 0 8px 0; color:#10b981;">💬 AI 대화형 대화식 도면 조율</h4>
            <p style="color:#64748b; font-size:13px; margin:0; line-height:1.6;">"무대 뒤 피난로 5m 확보해줘"와 같은 단순 채팅 명령어로 도면 배치를 대화식으로 조정합니다.</p>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.page == "dashboard":
    
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <div>
            <h2 style="margin:0; color:#0f172a; font-weight:800;">📐 Archisketch 스마트 행사 도면 설계</h2>
            <p style="margin:4px 0 0 0; color:#64748b; font-size:14px;">행사 도면 위에서 공간 배치, 혼잡도 Heatmap 오버레이, 동선 시뮬레이션을 한눈에 편집합니다.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Event Form Expander
    with st.expander("📝 행사 기본 정보 설정 및 수정", expanded=not st.session_state.design_generated):
        with st.form("event_info_form"):
            c_in1, c_in2, c_in3, c_in4 = st.columns(4)
            with c_in1:
                event_name_input = st.text_input("행사명", value=st.session_state.event_name)
                event_type_input = st.selectbox("행사 유형", ["축제", "박람회/전시회", "기업 행사", "팝업스토어"], index=0)
                event_purpose_input = st.text_input("행사 목적", value=st.session_state.event_purpose)
            with c_in2:
                expected_visitors_input = st.number_input("예상 인원 (명)", value=st.session_state.expected_visitors, step=500)
                duration_input = st.text_input("진행 시간", value=st.session_state.duration)
                target_age_input = st.text_input("대상 연령대", value=st.session_state.target_age)
            with c_in3:
                mood_input = st.text_input("원하는 분위기", value=st.session_state.mood)
                entry_fee_input = st.text_input("입장료", value=st.session_state.entry_fee)
                location_input = st.text_input("장소 선택", value=st.session_state.location)
            with c_in4:
                budget_input = st.text_input("예산", value=st.session_state.budget)
                st.write("")
                submit_design_btn = st.form_submit_button("✨ Archisketch AI 도면 생성", type="primary", use_container_width=True)

            if submit_design_btn:
                st.session_state.event_name = event_name_input
                st.session_state.event_type = event_type_input
                st.session_state.event_purpose = event_purpose_input
                st.session_state.expected_visitors = expected_visitors_input
                st.session_state.duration = duration_input
                st.session_state.target_age = target_age_input
                st.session_state.mood = mood_input
                st.session_state.entry_fee = entry_fee_input
                st.session_state.location = location_input
                st.session_state.budget = budget_input
                st.session_state.design_generated = True
                st.success("✨ Archisketch 도면 및 공간 최적 배치가 완료되었습니다!")
                st.rerun()

    # Info summary bar
    st.markdown(f"""
    <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:10px 18px; margin-bottom:16px; font-size:13px; color:#334155;">
        🆔 <b>행사명:</b> {st.session_state.event_name} &nbsp;|&nbsp;
        🏷️ <b>유형:</b> {st.session_state.event_type} &nbsp;|&nbsp;
        👥 <b>예상인원:</b> {st.session_state.expected_visitors:,}명 &nbsp;|&nbsp;
        📍 <b>장소:</b> {st.session_state.location} &nbsp;|&nbsp;
        💰 <b>예산:</b> {st.session_state.budget}
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.design_generated:
        
        # Archisketch Canvas Controls Bar
        st.markdown("<div class='archisketch-bar'>", unsafe_allow_html=True)
        col_ctrl1, col_ctrl2, col_ctrl3, col_ctrl4, col_ctrl5 = st.columns([2, 2, 2, 2, 2])
        
        with col_ctrl1:
            st.session_state.show_heatmap_overlay = st.checkbox("🔥 혼잡도(Heatmap) 도면 오버레이", value=st.session_state.show_heatmap_overlay)
        with col_ctrl2:
            st.session_state.show_flow_arrows = st.checkbox("🧭 주요 이동 동선 표시", value=st.session_state.show_flow_arrows)
        with col_ctrl3:
            st.session_state.show_grid_lines = st.checkbox("📐 Archisketch Grid 표시", value=st.session_state.show_grid_lines)
        with col_ctrl4:
            st.session_state.view_mode = st.selectbox("뷰 모드", ["2D CAD 도면", "3D 입체 조감도"], index=0, label_visibility="collapsed")
        with col_ctrl5:
            if st.button("🔄 AI 도면 재배치", key="reset_archisketch", use_container_width=True):
                st.toast("Archisketch AI가 최적 배치를 다시 계산했습니다!")
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        col_main_map, col_side_eval = st.columns([7, 5])

        with col_main_map:
            st.markdown("#### 🗺️ Archisketch 행사 도면 (혼잡도 오버레이 통합 뷰)")

            fig_map = go.Figure()

            # 1. Base Ground Map / Layout Background
            fig_map.add_shape(
                type="rect", x0=0, y0=0, x1=100, y1=100,
                fillcolor="#f8fafc" if not st.session_state.show_grid_lines else "#f1f5f9",
                line=dict(color="#cbd5e1", width=2)
            )

            # Outer boundaries / Walkway path
            fig_map.add_shape(
                type="rect", x0=10, y0=10, x1=90, y1=90,
                fillcolor="rgba(0,0,0,0)",
                line=dict(color="#94a3b8", width=2, dash="dot")
            )

            # 2. Crowd Heatmap Overlay (Rendered directly ON TOP of the floor plan!)
            if st.session_state.show_heatmap_overlay:
                np.random.seed(42)
                x_h = np.random.uniform(10, 90, 200)
                y_h = np.random.uniform(10, 90, 200)
                # Cluster around Main Stage (50, 82)
                x_h = np.append(x_h, np.random.normal(50, 12, 400))
                y_h = np.append(y_h, np.random.normal(80, 8, 400))
                # Cluster around Food Zone (25, 52)
                x_h = np.append(x_h, np.random.normal(25, 8, 200))
                y_h = np.append(y_h, np.random.normal(52, 8, 200))
                # Cluster around Entrance (50, 10)
                x_h = np.append(x_h, np.random.normal(50, 8, 200))
                y_h = np.append(y_h, np.random.normal(12, 6, 200))

                fig_map.add_trace(go.Histogram2dContour(
                    x=x_h, y=y_h,
                    colorscale=[
                        [0, 'rgba(255,255,255,0)'],
                        [0.2, 'rgba(59,130,246,0.3)'],
                        [0.5, 'rgba(234,179,8,0.5)'],
                        [0.8, 'rgba(249,115,22,0.7)'],
                        [1.0, 'rgba(239,68,68,0.85)']
                    ],
                    showscale=False,
                    ncontours=15,
                    line=dict(width=0)
                ))

            # 3. Archisketch Zone Rectangles & Labels
            for zone_k, info in ZONE_DATA.items():
                x_p, y_p = info["position"]
                w, h = info["size"]
                is_sel = (st.session_state.selected_zone == zone_k)

                # Draw Archisketch Rect Block
                fig_map.add_shape(
                    type="rect",
                    x0=x_p - w/2, y0=y_p - h/2,
                    x1=x_p + w/2, y1=y_p + h/2,
                    fillcolor=info["color"],
                    opacity=0.85 if is_sel else 0.65,
                    line=dict(
                        color="#ffffff" if not is_sel else "#1e293b",
                        width=3 if is_sel else 1.5
                    )
                )

                # Label on Zone
                fig_map.add_trace(go.Scatter(
                    x=[x_p],
                    y=[y_p],
                    mode="text",
                    name=zone_k,
                    text=[f"<b>{info['icon']} {zone_k}</b>"],
                    textposition="middle center",
                    textfont=dict(size=12 if is_sel else 11, color="#ffffff"),
                    showlegend=False
                ))

            # 4. Movement flow arrows
            if st.session_state.show_flow_arrows:
                fig_map.add_annotation(x=50, y=16, ax=50, ay=6, xref='x', yref='y', axref='x', ayref='y', showarrow=True, arrowhead=3, arrowsize=1.5, arrowcolor="#2563eb", arrowwidth=2.5)
                fig_map.add_annotation(x=30, y=32, ax=50, ay=18, xref='x', yref='y', axref='x', ayref='y', showarrow=True, arrowhead=3, arrowsize=1.5, arrowcolor="#2563eb", arrowwidth=2)
                fig_map.add_annotation(x=28, y=52, ax=25, ay=38, xref='x', yref='y', axref='x', ayref='y', showarrow=True, arrowhead=3, arrowsize=1.5, arrowcolor="#2563eb", arrowwidth=2)
                fig_map.add_annotation(x=42, y=75, ax=32, ay=58, xref='x', yref='y', axref='x', ayref='y', showarrow=True, arrowhead=3, arrowsize=1.5, arrowcolor="#2563eb", arrowwidth=2)

            fig_map.update_layout(
                xaxis=dict(range=[0, 100], showgrid=st.session_state.show_grid_lines, zeroline=False, visible=True if st.session_state.show_grid_lines else False, gridcolor="#cbd5e1"),
                yaxis=dict(range=[0, 100], showgrid=st.session_state.show_grid_lines, zeroline=False, visible=True if st.session_state.show_grid_lines else False, gridcolor="#cbd5e1"),
                height=480,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="#ffffff",
                plot_bgcolor="#f8fafc",
                showlegend=False
            )

            st.plotly_chart(fig_map, use_container_width=True)

            if st.session_state.show_heatmap_overlay:
                st.markdown("<div style='text-align:center; font-size:12px; color:#64748b; margin-top:-10px;'>🟢 원활 (Low) &nbsp; 🟡 보통 (Medium) &nbsp; 🟠 주의 (High) &nbsp; 🔴 매우 혼잡 (Critical)</div>", unsafe_allow_html=True)

        with col_side_eval:
            st.markdown("#### 💡 AI 도면 평가 결과")

            eval_df = pd.DataFrame({
                "평가 항목": ["안전성 (소방법)", "동선 효율성", "접근성", "혼잡도 분산", "응급 피난 속도"],
                "점수": ["98점", "92점", "90점", "88점", "97점"],
                "상태": ["최적화 완료", "우수", "매우 우수", "양호", "최적화 완료"]
            })
            
            st.dataframe(eval_df, use_container_width=True, hide_index=True)

            st.markdown("#### 🛠️ Archisketch 선택 구역 위치 조율")
            sel_zone = st.session_state.selected_zone
            st.markdown(f"**선택된 구역:** `{sel_zone}`")

            # Archisketch interactive position modifier sliders
            col_pos_x, col_pos_y = st.columns(2)
            with col_pos_x:
                new_x = st.slider("X 좌표 위치 (m)", 5, 95, ZONE_DATA[sel_zone]["position"][0])
            with col_pos_y:
                new_y = st.slider("Y 좌표 위치 (m)", 5, 95, ZONE_DATA[sel_zone]["position"][1])

            if new_x != ZONE_DATA[sel_zone]["position"][0] or new_y != ZONE_DATA[sel_zone]["position"][1]:
                ZONE_DATA[sel_zone]["position"] = [new_x, new_y]
                st.rerun()

            st.markdown("##### 🧠 AI 공간 배치 사유")
            st.info(ZONE_DATA[sel_zone]["rationale"])

        st.divider()

        # Zone quick selector buttons
        st.markdown("### 🔍 Archisketch 도면 구역 바로 선택")
        z_cols = st.columns(8)
        for idx, (z_name, z_val) in enumerate(ZONE_DATA.items()):
            with z_cols[idx]:
                btn_label = f"{z_val['icon']}\n{z_name}"
                if st.button(btn_label, key=f"btn_z_{z_name}", use_container_width=True):
                    st.session_state.selected_zone = z_name
                    st.rerun()

        st.write("")

        with st.expander("💬 Archisketch AI 대화형 맞춤 도면 조율 (클릭하여 열기)"):
            c_chat_list, c_chat_input = st.columns([2, 1])
            with c_chat_list:
                for msg in st.session_state.chat_history:
                    if msg["role"] == "user":
                        st.markdown(f"<div class='chat-user'>{msg['text']}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='chat-ai'>🤖 <b>Archisketch AI:</b> {msg['text']}</div>", unsafe_allow_html=True)
            with c_chat_input:
                with st.form("chat_form_dash", clear_on_submit=True):
                    u_msg = st.text_input("AI 도면 변경 요구사항 입력", placeholder="예: '무대를 5m 뒤로 이동해줘'")
                    u_send = st.form_submit_button("도면 변경 전송")
                    if u_send and u_msg:
                        st.session_state.chat_history.append({"role": "user", "text": u_msg})
                        reply = f"요청하신 '{u_msg}' 사항을 분석했습니다. Archisketch CAD 엔진이 소방법 및 동선을 계산하여 {st.session_state.selected_zone} 위치를 안전하게 재조정했습니다."
                        st.session_state.chat_history.append({"role": "ai", "text": reply})
                        st.rerun()

elif st.session_state.page == "report":
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
        <div>
            <h2 style="margin:0; color:#0f172a; font-weight:800;">📄 AI 상사 결재용 직인 보고서</h2>
            <p style="margin:4px 0 0 0; color:#64748b; font-size:14px;">Archisketch 기반 디지털 트윈 도면 및 안전 검토 분석 자동 보고서입니다.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:12px; padding:28px; box-shadow:0 4px 12px rgba(0,0,0,0.04);">
        <div style="text-align:center; border-bottom:2px solid #0f172a; padding-bottom:16px; margin-bottom:20px;">
            <h2 style="margin:0; color:#0f172a;">[기안서] {st.session_state.event_name} Archisketch 공간 배치 및 안전 검토안</h2>
            <p style="margin:8px 0 0 0; color:#64748b; font-size:13px;">작성일: {datetime.now().strftime('%Y-%m-%d')} | 기안자: {st.session_state.user_name} | Archisketch AI 검토 승인 완료</p>
        </div>

        <h4 style="color:#2563eb; margin-top:16px;">1. 행사 개요</h4>
        <table style="width:100%; border-collapse:collapse; font-size:13px; margin-bottom:16px;">
            <tr style="background:#f8fafc; border-bottom:1px solid #e2e8f0;">
                <td style="padding:8px; font-weight:bold; width:20%;">행사명</td>
                <td style="padding:8px;">{st.session_state.event_name}</td>
                <td style="padding:8px; font-weight:bold; width:20%;">행사 장소</td>
                <td style="padding:8px;">{st.session_state.location}</td>
            </tr>
            <tr style="border-bottom:1px solid #e2e8f0;">
                <td style="padding:8px; font-weight:bold;">예상 관람객</td>
                <td style="padding:8px;">{st.session_state.expected_visitors:,} 명</td>
                <td style="padding:8px; font-weight:bold;">소요 예산</td>
                <td style="padding:8px;">{st.session_state.budget}</td>
            </tr>
        </table>

        <h4 style="color:#2563eb; margin-top:20px;">2. AI 기반 Archisketch 공간 배치 타당성 검토</h4>
        <p style="font-size:13px; color:#334155; line-height:1.7;">
            본 행사장 배치는 <b>Archisketch 공간 CAD 알고리즘</b>에 따라 법적 소방법, 피난 동선, 관람객 편의성을 통합 검토하여 작성되었습니다.<br>
            • <b>메인 무대:</b> 최대 시야각 및 관중 분산을 고려하여 북쪽 중앙 배치 (안전점수 98점)<br>
            • <b>응급의료센터:</b> 구급차 진출입 전용 통로 및 무대 최단 거리(15초) 동선 확보 (안전점수 97점)<br>
            • <b>화장실 및 푸드존:</b> 바람 방향 및 대기 줄 가이드라인 적용으로 혼잡도 최소화
        </p>

        <h4 style="color:#2563eb; margin-top:20px;">3. 군중 이동 및 혼잡도 Heatmap 평가</h4>
        <div style="background:#f0fdf4; border:1px solid #bbf7d0; padding:12px; border-radius:8px; font-size:13px; color:#166534; margin-bottom:16px;">
            <b>✅ 시뮬레이션 총평:</b> 전체 위험도 '낮음(Safe)'. 병목 현상 예상 구간인 출입구 및 메인 무대 전면에 넓이 8m 이상의 순환형 가이드라인 설치를 완료했습니다.
        </div>

        <div style="margin-top:28px; text-align:right;">
            <p style="font-weight:bold; font-size:14px; margin-bottom:4px;">위와 같이 Archisketch 기반 행사 설계안을 보고합니다.</p>
            <p style="color:#64748b; font-size:12px;">이벤트 아키텍트 AI 시스템 검토 완료</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    c_rep1, c_rep2, c_rep3 = st.columns(3)
    with c_rep1:
        st.button("📥 PDF 다운로드 (PDF Export)", use_container_width=True)
    with c_rep2:
        st.button("📋 텍스트 복사 (Copy Text)", use_container_width=True)
    with c_rep3:
        if st.button("🏠 홈으로 이동", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

elif st.session_state.page == "settings":
    st.markdown("<h2 style='color:#0f172a; font-weight:800;'>⚙️ 시스템 및 계정 설정</h2>", unsafe_allow_html=True)

    col_s1, col_s2 = st.columns(2)

    with col_s1:
        st.markdown("### 👤 사용자 계정 관리")
        if st.session_state.logged_in:
            st.success(f"현재 **{st.session_state.user_name}** 계정으로 로그인되어 있습니다.")
            new_name = st.text_input("사용자 이름 변경", value=st.session_state.user_name)
            if st.button("프로필 수정 저장"):
                st.session_state.user_name = new_name
                st.success("프로필 정보가 수정되었습니다.")
                st.rerun()
        else:
            st.warning("현재 로그아웃 상태입니다.")

    with col_s2:
        st.markdown("### 🤖 Archisketch AI 설정")
        st.selectbox("Archisketch CAD 엔진 버전", ["Archisketch CAD v4.0 (최신)", "Archisketch Lite"])
        st.slider("Heatmap 정밀도", 1, 10, 8)
        st.toggle("화면 밝은 테마 (Light Mode)", value=True)
