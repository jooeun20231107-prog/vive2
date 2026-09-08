import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import json
import time
from datetime import datetime

st.set_page_config(
    page_title="이벤트 아키텍트 AI | Event Architect AI",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling to match dark modern AI dashboard theme
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #0e1117;
        color: #e0e6ed;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }
    
    /* Header Styling */
    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 20px;
        background-color: #161b22;
        border-bottom: 1px solid #30363d;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    
    /* Main Cards */
    .main-card {
        background: linear-gradient(135deg, #1f242d 0%, #161b22 100%);
        border: 1px solid #30363d;
        border-radius: 16px;
        padding: 28px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        cursor: pointer;
    }
    .main-card:hover {
        border-color: #58a6ff;
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(88, 166, 255, 0.2);
    }
    
    .card-icon {
        font-size: 48px;
        margin-bottom: 12px;
    }
    
    .card-title {
        font-size: 22px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 8px;
    }
    
    .card-desc {
        font-size: 14px;
        color: #8b949e;
        line-height: 1.5;
    }

    /* Badge & Status Styles */
    .status-badge {
        background-color: #238636;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }

    .info-box {
        background-color: #161b22;
        border-left: 4px solid #58a6ff;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 15px;
    }

    /* Chat bubble styles */
    .chat-user {
        background-color: #238636;
        color: white;
        padding: 10px 14px;
        border-radius: 16px 16px 2px 16px;
        margin: 6px 0;
        max-width: 80%;
        margin-left: auto;
        font-size: 14px;
    }
    
    .chat-ai {
        background-color: #21262d;
        color: #e0e6ed;
        padding: 10px 14px;
        border-radius: 16px 16px 16px 2px;
        margin: 6px 0;
        max-width: 85%;
        border: 1px solid #30363d;
        font-size: 14px;
    }

    /* Sidebar Customization */
    section[data-testid="stSidebar"] {
        background-color: #12161f;
        border-right: 1px solid #21262d;
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
    st.session_state.design_generated = False
if "simulation_active" not in st.session_state:
    st.session_state.simulation_active = False
if "selected_zone" not in st.session_state:
    st.session_state.selected_zone = "무대"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "ai", "text": "안녕하세요! 이벤트 아키텍트 AI입니다. 원하시는 행사 배치 및 조율 요청사항을 말씀해 주세요."}
    ]

# Default Event Data
if "event_name" not in st.session_state:
    st.session_state.event_name = "2026 청춘 페스티벌"
if "event_type" not in st.session_state:
    st.session_state.event_type = "축제/콘서트"
if "event_purpose" not in st.session_state:
    st.session_state.event_purpose = "지역 문화 활성화 및 청년 소통"
if "expected_visitors" not in st.session_state:
    st.session_state.expected_visitors = 5000
if "budget" not in st.session_state:
    st.session_state.budget = "5,000만원"
if "location" not in st.session_state:
    st.session_state.location = "서울 올림픽공원 잔디마당"

ZONE_DATA = {
    "무대": {
        "color": "#FF4B4B",
        "position": [50, 85],
        "rationale": "메인 출입구에서 가장 멀고 탁 트인 잔디 광장의 중앙 북쪽에 배치하여 5,000명의 관중 소음 분산 및 최고 시야각 확보. 비상 상황 시 후방 탈출 동선 확보.",
        "score": "98점 (최적화 완료)",
        "capacity": "최대 3,000명 동시 수용 가능"
    },
    "푸드 존": {
        "color": "#FFA500",
        "position": [25, 55],
        "rationale": "상하수도 및 전력 공급관 접근이 용이한 서쪽 외곽 배치. 관람석과의 거리를 약 25m 유지하여 음식 냄새 유입 최소화 및 대기 줄 전용 안전 가이드라인 적용.",
        "score": "92점 (양호)",
        "capacity": "푸드트럭 12대 & 테이블 40개"
    },
    "비상구": {
        "color": "#00FF7F",
        "position": [10, 90],
        "rationale": "소방법 규정 준수. 대형 군중 이동 통로와 직결되는 4개 코너 지점에 넓이 6m 이상의 피난 유도선과 함께 개설.",
        "score": "100점 (법적 기준 준수)",
        "capacity": "분당 1,200명 신속 대피 가능"
    },
    "정보 센터": {
        "color": "#1E90FF",
        "position": [50, 20],
        "rationale": "주 출입구 바로 전면에 위치하여 방문객 유실물 문의, 미아 보호, 행사 안내를 즉시 수행할 수 있는 병목 방지 통로 측면 배치.",
        "score": "95점 (매우 우수)",
        "capacity": "안내 요원 6명 배치 공간"
    },
    "체험 부스": {
        "color": "#9370DB",
        "position": [20, 35],
        "rationale": "입장객 이동 동선의 좌측 순환 코스 배치. 이동 중 자연스러운 체험 유도를 통해 정체를 방지하고 참여율 극대화.",
        "score": "90점 (우수)",
        "capacity": "20개 규격 부스 설치 가능"
    },
    "화장실": {
        "color": "#00CED1",
        "position": [85, 45],
        "rationale": "바람이 부는 하류 방향 동쪽 구역에 배치하여 악취 피해 방지. 여성 화장실 비율 1:1.5 확충 및 동선 교차 방지 구역 지정.",
        "score": "94점 (매우 우수)",
        "capacity": "이동식 화장실 15칸"
    },
    "의료 센터": {
        "color": "#FF1493",
        "position": [80, 75],
        "rationale": "구급차 진출입이 즉시 가능한 외각 전용 도로와 연결. 무대 부상자 발생 시 최단 거리(15초) 수송 동선 확보.",
        "score": "97점 (최적화 완료)",
        "capacity": "응급 침대 4대 & 응급차 직결"
    },
    "휴식 구역": {
        "color": "#32CD32",
        "position": [50, 50],
        "rationale": "행사장 중앙 쉼터로 나무 그늘 아래 벤치 및 파라솔 배치. 무대 소음이 알맞게 전달되며 피로도를 줄일 수 있는 완충 지대.",
        "score": "91점 (양호)",
        "capacity": "동시 휴식 200명 수용"
    }
}

st.markdown("<div class='top-bar'>", unsafe_allow_html=True)
col_head1, col_head2, col_head3 = st.columns([3, 4, 3])

with col_head1:
    # Logo button - Returns to Home
    if st.button("🎪 이벤트 아키텍트 AI", key="logo_btn", help="홈으로 돌아가기"):
        st.session_state.page = "home"
        st.rerun()

with col_head2:
    st.markdown("<p style='text-align:center; margin:0; color:#8b949e; font-size:13px;'>AI 기반 차세대 스마트 행사 자동 설계 & 공간 디지털 트윈 플랫폼</p>", unsafe_allow_html=True)

with col_head3:
    c1, c2, c3 = st.columns([2, 2, 2])
    with c1:
        if st.button("📊 대시보드", key="nav_dash"):
            st.session_state.page = "dashboard"
            st.rerun()
    with c2:
        if st.button("📄 AI 보고서", key="nav_report"):
            st.session_state.page = "report"
            st.rerun()
    with c3:
        if st.button("⚙️ 설정", key="nav_settings"):
            st.session_state.page = "settings"
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 👤 사용자 정보")
    if st.session_state.logged_in:
        st.success(f"**{st.session_state.user_name}** 님 (인증됨)")
        if st.button("로그아웃", key="sidebar_logout"):
            st.session_state.logged_in = False
            st.rerun()
    else:
        st.info("로그인이 필요합니다.")
        if st.button("로그인 / 회원가입", key="sidebar_login"):
            st.session_state.page = "settings"
            st.rerun()

    st.divider()
    st.markdown("### 📌 메뉴 이동")
    if st.button("🏠 홈 화면", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
    if st.button("🏗️ 행사 설계 대시보드", use_container_width=True):
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
    <div style="background-color:#161b22; padding:12px; border-radius:10px; font-size:12px; border:1px solid #30363d;">
        <span style="color:#58a6ff; font-weight:bold;">💡 AI 안내</span><br>
        AI가 행사장 평면도를 분석하여 안전 법규 및 동선 효율성을 계산하고 최적 배치를 제안합니다.
    </div>
    """, unsafe_allow_html=True)

if st.session_state.page == "home":
    st.markdown("<h1 style='text-align: center; color: #ffffff;'>AI 기반 행사 자동 설계 플랫폼</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8b949e; font-size: 16px; margin-bottom: 40px;'>행사 정보를 입력하면 AI가 공간 디지털 트윈, 동선 시뮬레이션, 보고서 작성까지 자동으로 완성합니다.</p>", unsafe_allow_html=True)

    col_box1, col_box2 = st.columns(2)

    with col_box1:
        st.markdown("""
        <div class='main-card'>
            <div class='card-icon'>📊</div>
            <div class='card-title'>AI 행사 설계 대시보드</div>
            <div class='card-desc'>
                행사 기본 정보를 입력하고 디지털 트윈 기반 실시간 2D/3D 지도 배치, 무대 및 부스 자동 생성, 군중 예측 시뮬레이션을 수행합니다.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("🚀 대시보드 바로가기", key="btn_go_dashboard", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()

    with col_box2:
        st.markdown("""
        <div class='main-card'>
            <div class='card-icon'>📄</div>
            <div class='card-title'>AI 상사 보고용 리포트</div>
            <div class='card-desc'>
                설계된 공간 배치 이유, 동선 안전성 검토 결과, 예산 대비 효율성 평가가 포함된 원클릭 결재용 보고서를 생성합니다.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("📑 AI 보고서 바로가기", key="btn_go_report", use_container_width=True):
            st.session_state.page = "report"
            st.rerun()

    st.divider()
    
    # Feature showcase row
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.markdown("#### 🎯 디지털 트윈 최적 배치")
        st.caption("소방법 및 동선 혼잡도를 고려하여 무대, 푸드존, 화장실, 비상구를 지능적으로 자동 배치합니다.")
    with col_f2:
        st.markdown("#### 🔥 군중 시뮬레이션 (Heatmap)")
        st.caption("AI 알고리즘이 5,000명 이상의 군중 이동 경로를 예측하여 밀집 위험 구간을 미리 경고합니다.")
    with col_f3:
        st.markdown("#### 💬 AI 대화형 디자인 조율")
        st.caption("채팅창에 원하는 요구사항을 입력하면 실시간으로 객체 위치와 설계를 재조정합니다.")

elif st.session_state.page == "dashboard":
    st.markdown("## 🏗️ AI 기반 행사 설계 대시보드")
    st.caption("행사 정보를 입력하면 AI가 최적의 행사장을 설계해 드립니다.")

    # 1. Input Panel Card
    with st.expander("📝 행사 기본 정보 입력 및 수정", expanded=not st.session_state.design_generated):
        with st.form("event_info_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                event_name_input = st.text_input("이벤트 이름", value=st.session_state.event_name)
                event_purpose_input = st.text_input("이벤트 목적", value=st.session_state.event_purpose)
            with col2:
                expected_visitors_input = st.number_input("예상 방문객 수 (명)", value=st.session_state.expected_visitors, step=500)
                budget_input = st.text_input("예산", value=st.session_state.budget)
            with col3:
                location_input = st.text_input("장소", value=st.session_state.location)
                event_type_input = st.selectbox("행사 유형", ["축제/콘서트", "박람회/전시회", "기업 행사장", "지역 팝업스토어"])

            submit_design_btn = st.form_submit_button("🤖 AI 이벤트 디자인 생성", use_container_width=True)
            if submit_design_btn:
                st.session_state.event_name = event_name_input
                st.session_state.event_purpose = event_purpose_input
                st.session_state.expected_visitors = expected_visitors_input
                st.session_state.budget = budget_input
                st.session_state.location = location_input
                st.session_state.design_generated = True
                st.session_state.simulation_active = False
                st.success("✨ 디지털 트윈 및 AI 최적 공간 배치가 완료되었습니다!")
                st.rerun()

    # If Design is not generated yet -> Blank Canvas state
    if not st.session_state.design_generated:
        st.info("👆 상단의 'AI 이벤트 디자인 생성' 버튼을 누르면 이 빈 사각형 공간에 디지털 트윈 행사장 공간이 구축됩니다.")
        
        # Empty rect placeholder
        st.markdown("""
        <div style="border:2px dashed #30363d; border-radius:16px; height:450px; display:flex; flex-direction:column; justify-content:center; align-items:center; background-color:#161b22; color:#8b949e;">
            <span style="font-size:48px; margin-bottom:10px;">📐</span>
            <h3 style="color:#ffffff;">대시보드 공간 (대기 중)</h3>
            <p>이벤트 정보를 입력하고 AI 디자인을 생성해주세요.</p>
        </div>
        """, unsafe_allow_html=True)

    else:
        # Display Banner Summary
        st.markdown(f"""
        <div class='info-box'>
            <b>📌 행사 개요:</b> {st.session_state.event_name} | <b>장소:</b> {st.session_state.location} | <b>예상 인원:</b> {st.session_state.expected_visitors:,}명 | <b>예산:</b> {st.session_state.budget}
        </div>
        """, unsafe_allow_html=True)

        col_map, col_details = st.columns([7, 5])

        # Left Column: Map or Heatmap
        with col_map:
            st.markdown("### 🗺️ 행사장 배치도 (디지털 트윈)")
            
            # Interactive Map plotting using Plotly
            fig = go.Figure()

            # Background Field Boundary
            fig.add_shape(
                type="rect", x0=0, y0=0, x1=100, y1=100,
                fillcolor="#1a2332" if not st.session_state.simulation_active else "#121212",
                line=dict(color="#30363d", width=2)
            )

            if st.session_state.simulation_active:
                # Add Heatmap density simulation
                x_heat = np.random.uniform(10, 90, 300)
                y_heat = np.random.uniform(10, 90, 300)
                # Concentration around Stage (50, 85) & Food Zone (25, 55)
                x_heat = np.append(x_heat, np.random.normal(50, 8, 400))
                y_heat = np.append(y_heat, np.random.normal(80, 8, 400))
                x_heat = np.append(x_heat, np.random.normal(25, 6, 250))
                y_heat = np.append(y_heat, np.random.normal(55, 6, 250))

                fig.add_trace(go.Histogram2dContour(
                    x=x_heat, y=y_heat,
                    colorscale='Hot',
                    showscale=True,
                    opacity=0.6,
                    name="군중 밀집도"
                ))

            # Add Zone Markers
            for zone_name, info in ZONE_DATA.items():
                x_pos, y_pos = info["position"]
                is_selected = (st.session_state.selected_zone == zone_name)

                fig.add_trace(go.Scatter(
                    x=[x_pos],
                    y=[y_pos],
                    mode="markers+text",
                    name=zone_name,
                    text=[f"<b>{zone_name}</b>"],
                    textposition="bottom center",
                    textfont=dict(size=13, color="white" if not is_selected else "#FFD700"),
                    marker=dict(
                        size=28 if is_selected else 22,
                        color=info["color"],
                        line=dict(width=3 if is_selected else 1, color="#FFFFFF")
                    )
                ))

            # Main Entrances Visual
            fig.add_annotation(x=50, y=5, text="🚪 메인 출입구", showarrow=False, font=dict(size=14, color="#00FF7F"))

            fig.update_layout(
                xaxis=dict(range=[-5, 105], showgrid=False, zeroline=False, visible=False),
                yaxis=dict(range=[-5, 105], showgrid=False, zeroline=False, visible=False),
                height=480,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False
            )

            st.plotly_chart(fig, use_container_width=True)

            # Bottom Right Controls: Simulation & Chat Trigger
            col_b1, col_b2 = st.columns([1, 1])
            with col_b1:
                sim_label = "❌ 시뮬레이션 끄기" if st.session_state.simulation_active else "🔥 AI 군중 시뮬레이션 실행"
                if st.button(sim_label, key="toggle_sim", use_container_width=True):
                    st.session_state.simulation_active = not st.session_state.simulation_active
                    st.rerun()
            with col_b2:
                st.caption("💡 지도의 객체를 선택하거나 아래 버튼으로 상세 배치를 확인할 수 있습니다.")

        # Right Column: Rationale & AI Chat
        with col_details:
            st.markdown("### 🔍 구역 선택 및 AI 배치 근거 요약")

            # Zone Selection buttons
            st.write("배치된 구역을 클릭하여 AI 설계 이유를 확인하세요:")
            zone_cols = st.columns(4)
            for idx, zone_k in enumerate(ZONE_DATA.keys()):
                with zone_cols[idx % 4]:
                    if st.button(zone_k, key=f"z_btn_{zone_k}", use_container_width=True):
                        st.session_state.selected_zone = zone_k
                        st.rerun()

            # Rationale Detail Box
            sel_zone = st.session_state.selected_zone
            zone_info = ZONE_DATA[sel_zone]

            st.markdown(f"""
            <div style="background-color:#161b22; border:1px solid #30363d; border-radius:12px; padding:18px; margin-top:12px;">
                <h4 style="color:{zone_info['color']}; margin-top:0;">📍 선택 구역: {sel_zone}</h4>
                <p><b>배치 적합도 평가:</b> <span style="color:#238636; font-weight:bold;">{zone_info['score']}</span></p>
                <p><b>수용 능력:</b> {zone_info['capacity']}</p>
                <hr style="border-color:#30363d;">
                <b>🧠 AI 공간 배치 최적화 사유:</b><br>
                <p style="color:#c9d1d9; font-size:14px; line-height:1.6; margin-top:6px;">{zone_info['rationale']}</p>
            </div>
            """, unsafe_allow_html=True)

            st.divider()

            # 3. AI Interactive Chat Assistant
            st.markdown("### 💬 AI 커스텀 디자인 조율 채팅")
            
            # Chat Display Box
            chat_container = st.container(height=200)
            with chat_container:
                for msg in st.session_state.chat_history:
                    if msg["role"] == "user":
                        st.markdown(f"<div class='chat-user'>{msg['text']}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='chat-ai'>🤖 <b>AI:</b> {msg['text']}</div>", unsafe_allow_html=True)

            # Chat Input Form
            with st.form("chat_form", clear_on_submit=True):
                user_msg = st.text_input("AI에게 추가 요구사항 전달 (예: '무대를 5m 뒤로 이동해줘')", placeholder="원하시는 설계를 말씀해주세요...")
                send_chat = st.form_submit_button("전송")

                if send_chat and user_msg:
                    st.session_state.chat_history.append({"role": "user", "text": user_msg})
                    
                    # Simulated AI Agent smart response
                    ai_reply = f"요청하신 '{user_msg}' 사항을 분석했습니다. 소방법 및 동선 혼잡도를 재계산하여 {st.session_state.selected_zone} 배치를 재조정했습니다."
                    st.session_state.chat_history.append({"role": "ai", "text": ai_reply})
                    st.rerun()

elif st.session_state.page == "report":
    st.markdown("## 📄 직장상사 보고용 결재 리포트")
    st.caption("AI가 생성한 자동 분석 보고서입니다. 즉시 복사하거나 보고서로 활용할 수 있습니다.")

    if not st.session_state.design_generated:
        st.warning("⚠️ 대시보드에서 먼저 'AI 이벤트 디자인 생성'을 실행해 주세요.")
    else:
        # Printable Executive Summary Document Layout
        st.markdown(f"""
        <div style="background-color:#ffffff; color:#111111; padding:40px; border-radius:12px; font-family:'Pretendard', sans-serif;">
            <div style="text-align:center; border-bottom:2px solid #111; padding-bottom:15px; margin-bottom:25px;">
                <h2 style="margin:0; color:#111;">[기획 보고서] {st.session_state.event_name} AI 최적 공간 설계안</h2>
                <p style="color:#555; font-size:14px; margin-top:5px;">작성일시: {datetime.now().strftime('%Y년 %m월 %d일')} | 작성자: {st.session_state.user_name} (이벤트 아키텍트 AI)</p>
            </div>

            <h3>1. 행사 개요</h3>
            <table style="width:100%; border-collapse:collapse; margin-bottom:20px; font-size:14px;">
                <tr style="background:#f2f2f2;"><th style="border:1px solid #ccc; padding:8px;">행사명</th><td style="border:1px solid #ccc; padding:8px;">{st.session_state.event_name}</td><th style="border:1px solid #ccc; padding:8px;">장소</th><td style="border:1px solid #ccc; padding:8px;">{st.session_state.location}</td></tr>
                <tr><th style="border:1px solid #ccc; padding:8px;">예상 관람객</th><td style="border:1px solid #ccc; padding:8px;">{st.session_state.expected_visitors:,} 명</td><th style="border:1px solid #ccc; padding:8px;">총 예산</th><td style="border:1px solid #ccc; padding:8px;">{st.session_state.budget}</td></tr>
                <tr style="background:#f2f2f2;"><th style="border:1px solid #ccc; padding:8px;">행사 목적</th><td colspan="3" style="border:1px solid #ccc; padding:8px;">{st.session_state.event_purpose}</td></tr>
            </table>

            <h3>2. 공간 배치 AI 시뮬레이션 및 설계 근거</h3>
            <ul>
                <li><b>무대 (Stage):</b> 관중 소음 분산 및 최우수 시야각 확보를 위해 북측 중앙에 배치.</li>
                <li><b>푸드 존 (Food Zone):</b> 상하수도 관로 인접 서측 배치, 음식 냄새 유입 방지 완충 지대 확보.</li>
                <li><b>안전 및 비상구 (Safety Exit):</b> 소방법 기준 100% 준수, 4개 코너 지점 대피로 확보.</li>
                <li><b>의료 센터 (Medical Center):</b> 구급차 진출입 도로와 직결 (응급 수송 15초 내 가능).</li>
            </ul>

            <h3>3. AI 평가 점수 및 핵심 종합 의견</h3>
            <div style="background:#f8f9fa; border:1px solid #ddd; padding:15px; border-radius:8px; margin-bottom:20px;">
                <p style="margin:4px 0;">✔️ <b>전체 공간 안전성 점수:</b> 98점 / 100점 (매우 우수)</p>
                <p style="margin:4px 0;">✔️ <b>동선 효율성 및 병목 방지:</b> 92점 / 100점 (우수)</p>
                <p style="margin:4px 0;">✔️ <b>예산 대비 공간 활용률:</b> 95점 / 100점 (최적화 완료)</p>
            </div>

            <p style="font-size:13px; color:#666;">본 보고서는 이벤트 아키텍트 AI 군중 흐름 예측 시뮬레이션을 기반으로 작성되었습니다.</p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        col_rep1, col_rep2 = st.columns(2)
        with col_rep1:
            st.button("📥 보고서 PDF / 텍스트 다운로드 (준비 완료)", use_container_width=True)
        with col_rep2:
            st.button("📋 전체 내용 복사하기", use_container_width=True)

elif st.session_state.page == "settings":
    st.markdown("## ⚙️ 시스템 설정 및 계정 관리")

    col_set1, col_set2 = st.columns(2)

    with col_set1:
        st.markdown("### 🔑 로그인 / 회원가입 설정")
        if st.session_state.logged_in:
            st.success(f"현재 로그인 계정: **{st.session_state.user_name}**")
            new_username = st.text_input("사용자 이름 변경", value=st.session_state.user_name)
            if st.button("프로필 변경 저장"):
                st.session_state.user_name = new_username
                st.success("변경되었습니다!")
                st.rerun()
            
            st.divider()
            if st.button("로그아웃 실행", type="primary"):
                st.session_state.logged_in = False
                st.rerun()
        else:
            with st.form("login_form"):
                st.subheader("로그인")
                email = st.text_input("이메일 주소")
                pw = st.text_input("비밀번호", type="password")
                login_submit = st.form_submit_button("로그인")
                if login_submit:
                    st.session_state.logged_in = True
                    st.session_state.user_name = email.split("@")[0] if "@" in email else "사용자"
                    st.success("로그인 성공!")
                    st.rerun()

    with col_set2:
        st.markdown("### 🤖 AI 엔진 & 서비스 설정")
        st.selectbox("AI 디지털 트윈 엔진 선택", ["Event-Architect-v4 (기본)", "Claude-3.5-Sonnet-Spatial", "GPT-4o-Venue-Engine"])
        st.slider("군중 예측 시뮬레이션 정밀도", min_value=1, max_value=10, value=8)
        st.toggle("소방법 및 실시간 안전 법규 알림 활성화", value=True)
        st.toggle("다크 모드 고해상도 그래픽 적용", value=True)
