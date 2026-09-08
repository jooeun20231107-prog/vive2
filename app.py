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
        padding: 12px 24px;
        background-color: #ffffff;
        border-bottom: 1px solid #e2e8f0;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    
    /* Full Clickable Big Card Styling for Home Page */
    div[data-testid="stColumn"] button[aria-label*="대시보드"],
    div[data-testid="stColumn"] button[aria-label*="상사 보고용 리포트"] {
        height: 250px !important;
        background: #ffffff !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 16px !important;
        padding: 24px !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
        color: #334155 !important;
        white-space: pre-wrap !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03) !important;
        transition: all 0.25s ease-in-out !important;
        cursor: pointer !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    div[data-testid="stColumn"] button[aria-label*="대시보드"]:hover,
    div[data-testid="stColumn"] button[aria-label*="상사 보고용 리포트"]:hover {
        border-color: #2563eb !important;
        background-color: #f0f6ff !important;
        color: #0f172a !important;
        transform: translateY(-6px) !important;
        box-shadow: 0 12px 28px rgba(37, 99, 235, 0.16) !important;
    }

    /* Metric Badges & Info Pill Bar */
    .info-pill {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 10px 14px;
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 13px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    .info-label {
        color: #64748b;
        font-size: 11px;
        font-weight: 500;
    }
    .info-value {
        color: #0f172a;
        font-weight: 600;
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
    
    /* Button custom overrides */
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
if "simulation_active" not in st.session_state:
    st.session_state.simulation_active = True
if "selected_zone" not in st.session_state:
    st.session_state.selected_zone = "메인무대"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "ai", "text": "안녕하세요! Event AI입니다. 원하시는 행사 공간 요구사항이나 변경하고 싶은 배치를 말씀해 주세요."}
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

# Detailed Zone Data definitions
ZONE_DATA = {
    "메인무대": {
        "color": "#3b82f6",
        "position": [50, 85],
        "rationale": "메인 출입구에서 가장 멀고 탁 트인 잔디 광장의 중앙 북쪽에 배치하여 5,000명 관중 소음 분산 및 최고 시야각 확보. 비상 상황 시 후방 탈출 동선 확보.",
        "score": "98점 (최적화 완료)",
        "capacity": "최대 3,000명 동시 관람"
    },
    "푸드존": {
        "color": "#f97316",
        "position": [25, 55],
        "rationale": "상하수도 및 전력 공급관 접근이 용이한 서쪽 외곽 배치. 관람석과의 거리를 약 25m 유지하여 음식 냄새 유입 최소화 및 대기 줄 전용 가이드라인 적용.",
        "score": "92점 (양호)",
        "capacity": "푸드트럭 12대 & 테이블 40개"
    },
    "체험부스": {
        "color": "#8b5cf6",
        "position": [20, 35],
        "rationale": "입장객 이동 동선의 좌측 순환 코스 배치. 이동 중 자연스러운 체험 유도를 통해 병목 현상을 방지하고 참여율 극대화.",
        "score": "90점 (우수)",
        "capacity": "20개 규격 부스"
    },
    "휴식공간": {
        "color": "#10b981",
        "position": [50, 48],
        "rationale": "행사장 중앙 쉼터로 나무 그늘 아래 벤치 및 파라솔 배치. 무대 소음이 알맞게 전달되며 피로도를 줄일 수 있는 완충 지대.",
        "score": "91점 (양호)",
        "capacity": "동시 휴식 200명 수용"
    },
    "안내센터": {
        "color": "#ec4899",
        "position": [50, 20],
        "rationale": "주 출입구 바로 전면에 위치하여 방문객 유실물 문의, 미아 보호, 행사 안내를 즉시 수행할 수 있는 병목 방지 통로 측면 배치.",
        "score": "95점 (매우 우수)",
        "capacity": "안내 요원 6명 상주"
    },
    "화장실": {
        "color": "#06b6d4",
        "position": [85, 45],
        "rationale": "바람이 부는 하류 방향 동쪽 구역에 배치하여 악취 피해 방지. 여성 화장실 비율 1:1.5 확충 및 동선 교차 방지 구역 지정.",
        "score": "94점 (매우 우수)",
        "capacity": "이동식 화장실 15칸"
    },
    "응급의료센터": {
        "color": "#ef4444",
        "position": [80, 75],
        "rationale": "구급차 진출입이 즉시 가능한 외각 전용 도로와 연결. 무대 부상자 발생 시 최단 거리(15초) 수송 동선 확보.",
        "score": "97점 (최적화 완료)",
        "capacity": "응급 침대 4대 & 구급차 직결"
    },
    "출입구": {
        "color": "#1e293b",
        "position": [50, 5],
        "rationale": "소방법 규정 준수. 대형 군중 이동 통로와 직결되는 넓이 8m 이상의 피난 유도선 및 분산 입출입 구역 설정.",
        "score": "100점 (법적 기준 준수)",
        "capacity": "분당 1,500명 통행 가능"
    }
}

st.markdown("<div class='top-bar-container'>", unsafe_allow_html=True)
col_head1, col_head2, col_head3 = st.columns([3, 5, 2])

with col_head1:
    if st.button("🎪 Event AI (이벤트 아키텍트)", key="logo_btn", help="홈 화면으로 돌아가기"):
        st.session_state.page = "home"
        st.rerun()

with col_head2:
    st.markdown("<p style='text-align:center; margin:0; color:#64748b; font-size:13px; font-weight:500;'>AI 기반 차세대 공간 디지털 트윈 & 스마트 행사 자동 설계 플랫폼</p>", unsafe_allow_html=True)

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
    <div style="background-color:#1e293b; color:#f8fafc; padding:14px; border-radius:10px; font-size:12px;">
        <span style="color:#60a5fa; font-weight:bold;">💡 AI 가이드</span><br>
        AI가 공간 법규 및 안전성을 다각도로 검토하여 10초 만에 optimal 디지털 트윈 배치를 구축합니다.
    </div>
    """, unsafe_allow_html=True)


if st.session_state.page == "home":
    st.markdown("<h1 style='text-align: center; color: #0f172a; margin-top:20px; font-weight:800;'>AI 기반 행사 자동 설계 플랫폼</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 16px; margin-bottom: 35px;'>행사 정보를 입력하면 AI가 공간 디지털 트윈, 동선 시뮬레이션, 상사 결재용 보고서까지 자동으로 완성합니다.</p>", unsafe_allow_html=True)

    col_box1, col_box2 = st.columns(2)

    with col_box1:
        dash_card_click = st.button(
            "📊\n\nAI 기반 행사 자동 설계 대시보드\n\n행사 기본 정보를 바탕으로 디지털 트윈 2D/3D 지도 배치, 무대 및 부스 자동 생성, 군중 이동 및 혼잡도 예측 시뮬레이션을 수행합니다.\n\n👉 [ 네모를 클릭하여 대시보드 이동 ]",
            key="card_btn_dashboard",
            use_container_width=True
        )
        if dash_card_click:
            st.session_state.page = "dashboard"
            st.rerun()

    with col_box2:
        report_card_click = st.button(
            "📄\n\nAI 상사 보고용 리포트\n\n설계된 공간 배치 사유, 동선 안전성 검토 결과, 예산 대비 효율성 평가가 포함된 원클릭 직장 상사 결재용 보고서를 생성합니다.\n\n👉 [ 네모를 클릭하여 AI 보고서 이동 ]",
            key="card_btn_report",
            use_container_width=True
        )
        if report_card_click:
            st.session_state.page = "report"
            st.rerun()

    st.divider()
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.markdown("#### 🎯 디지털 트윈 최적 배치")
        st.caption("소방법 및 동선 혼잡도를 고려하여 무대, 푸드존, 화장실, 비상구를 지능적으로 자동 배치합니다.")
    with col_f2:
        st.markdown("#### 🔥 군중 시뮬레이션 (Heatmap)")
        st.caption("AI 알고리즘이 군중 이동 경로를 예측하여 밀집 위험 구간을 미리 계산하고 경고합니다.")
    with col_f3:
        st.markdown("#### 💬 AI 대화형 디자인 조율")
        st.caption("채팅창에 원하는 요구사항을 입력하면 실시간으로 객체 위치와 설계를 재조정합니다.")


elif st.session_state.page == "dashboard":
    
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <div>
            <h2 style="margin:0; color:#0f172a; font-weight:700;">📑 행사 설계</h2>
            <p style="margin:4px 0 0 0; color:#64748b; font-size:14px;">행사 정보를 입력하면 AI가 최적의 행사장을 설계해드립니다.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
                st.write("")
                submit_design_btn = st.form_submit_button("✨ AI 행사장 설계하기", type="primary", use_container_width=True)

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
                st.success("✨ 디지털 트윈 및 공간 최적 배치가 완료되었습니다!")
                st.rerun()

    st.markdown(f"""
    <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:12px 18px; margin-bottom:18px; display:flex; flex-wrap:wrap; gap:16px; align-items:center; justify-content:space-between;">
        <div style="display:flex; flex-wrap:wrap; gap:12px; align-items:center; font-size:13px;">
            <span>🆔 <b>행사명:</b> {st.session_state.event_name}</span> |
            <span>🏷️ <b>유형:</b> {st.session_state.event_type}</span> |
            <span>🎯 <b>목적:</b> {st.session_state.event_purpose}</span> |
            <span>👥 <b>예상인원:</b> {st.session_state.expected_visitors:,}명</span> |
            <span>⏰ <b>시간:</b> {st.session_state.duration}</span> |
            <span>🎂 <b>연령대:</b> {st.session_state.target_age}</span> |
            <span>📍 <b>장소:</b> {st.session_state.location}</span> |
            <span>💰 <b>예산:</b> {st.session_state.budget}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.design_generated:
        st.info("👆 상단의 'AI 행사장 설계하기' 버튼을 누르면 이 공간에 디지털 트윈 행사장과 최적 배치가 생성됩니다.")
        st.markdown("""
        <div style="border:2px dashed #cbd5e1; border-radius:16px; height:450px; display:flex; flex-direction:column; justify-content:center; align-items:center; background-color:#ffffff; color:#64748b;">
            <span style="font-size:48px; margin-bottom:10px;">📐</span>
            <h3 style="color:#0f172a;">대시보드 공간 (대기 중)</h3>
            <p>행사 기본 정보를 확인 후 생성 버튼을 클릭해주세요.</p>
        </div>
        """, unsafe_allow_html=True)

    else:
        # Main Dashboard Grid
        col_map, col_heat, col_eval = st.columns([5, 3, 4])

        # 1. Map Panel
        with col_map:
            st.markdown("""
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <h4 style="margin:0; font-weight:700;">🗺️ 행사장 배치도 <span style="font-size:12px; color:#64748b; font-weight:normal;">(디지털 트윈 기반)</span></h4>
            </div>
            """, unsafe_allow_html=True)

            fig_map = go.Figure()

            fig_map.add_shape(
                type="rect", x0=0, y0=0, x1=100, y1=100,
                fillcolor="#f0fdf4",
                line=dict(color="#bbf7d0", width=2)
            )

            fig_map.add_shape(
                type="rect", x0=15, y0=15, x1=85, y1=85,
                fillcolor="rgba(0,0,0,0)",
                line=dict(color="#cbd5e1", width=3, dash="dash")
            )

            for zone_k, info in ZONE_DATA.items():
                x_p, y_p = info["position"]
                is_sel = (st.session_state.selected_zone == zone_k)

                fig_map.add_trace(go.Scatter(
                    x=[x_p],
                    y=[y_p],
                    mode="markers+text",
                    name=zone_k,
                    text=[f"<b>{zone_k}</b>"],
                    textposition="bottom center",
                    textfont=dict(size=12, color="#0f172a" if not is_sel else "#2563eb"),
                    marker=dict(
                        size=26 if is_sel else 20,
                        color=info["color"],
                        line=dict(width=3 if is_sel else 1, color="#FFFFFF")
                    )
                ))

            fig_map.add_annotation(x=50, y=8, text="⬆️ 주 이동 동선", showarrow=False, font=dict(size=12, color="#2563eb"))

            fig_map.update_layout(
                xaxis=dict(range=[-5, 105], showgrid=False, zeroline=False, visible=False),
                yaxis=dict(range=[-5, 105], showgrid=False, zeroline=False, visible=False),
                height=360,
                margin=dict(l=5, r=5, t=5, b=5),
                paper_bgcolor="#ffffff",
                plot_bgcolor="#f0fdf4",
                showlegend=False
            )

            st.plotly_chart(fig_map, use_container_width=True)

        # 2. Crowd Heatmap Panel
        with col_heat:
            st.markdown("<h4 style='margin:0 0 8px 0; font-weight:700;'>🔥 혼잡도 Heatmap</h4>", unsafe_allow_html=True)

            fig_heat = go.Figure()
            
            x_h = np.random.uniform(10, 90, 200)
            y_h = np.random.uniform(10, 90, 200)
            x_h = np.append(x_h, np.random.normal(50, 10, 300))
            y_h = np.append(y_h, np.random.normal(82, 8, 300))
            x_h = np.append(x_h, np.random.normal(25, 8, 150))
            y_h = np.append(y_h, np.random.normal(55, 8, 150))

            fig_heat.add_trace(go.Histogram2dContour(
                x=x_h, y=y_h,
                colorscale='YlOrRd',
                showscale=False,
                opacity=0.85
            ))

            fig_heat.update_layout(
                xaxis=dict(range=[0, 100], visible=False),
                yaxis=dict(range=[0, 100], visible=False),
                height=360,
                margin=dict(l=5, r=5, t=5, b=5),
                paper_bgcolor="#ffffff",
                plot_bgcolor="#fef2f2",
                showlegend=False
            )

            st.plotly_chart(fig_heat, use_container_width=True)
            st.markdown("<div style='text-align:center; font-size:12px; color:#64748b;'>🟢 원활 &nbsp; 🟡 보통 &nbsp; 🔴 혼잡</div>", unsafe_allow_html=True)

        # 3. AI Evaluation Scores
        with col_eval:
            st.markdown("<h4 style='margin:0 0 8px 0; font-weight:700;'>💡 AI 평가 결과</h4>", unsafe_allow_html=True)

            eval_df = pd.DataFrame({
                "평가 항목": ["안전성", "동선 효율성", "접근성", "혼잡도 관리", "비상 효율성"],
                "점수": ["92", "87", "90", "84", "88"],
                "등급": ["매우 우수", "우수", "매우 우수", "우수", "우수"]
            })
            
            st.dataframe(
                eval_df,
                use_container_width=True,
                hide_index=True
            )

            st.markdown("<h5 style='margin:12px 0 6px 0; font-weight:700;'>💡 AI 개선 요청사항</h5>", unsafe_allow_html=True)
            st.markdown("""
            <div style="font-size:12px; color:#334155; line-height:1.6; background:#f8fafc; padding:10px; border-radius:8px; border:1px solid #e2e8f0;">
                ✔️ 공연관람용 부스를 사이에 추가 휴식 공간을 배치하면 혼잡도를 더 낮출 수 있습니다.<br>
                ✔️ 응급의료센터를 주요 정문 근처로 이동시키면 대응 시간이 더 단축됩니다.<br>
                ✔️ 체험부스 구역의 동선을 일방통행으로 설정하면 병목을 줄일 수 있습니다.<br>
                ✔️ 화장실 수를 2개 추가하면 대기 시간을 줄일 수 있습니다.
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # Dynamic Placement Rationale Section
        st.markdown("### 🔍 클릭하여 구역별 AI 배치 사유 확인")
        z_cols = st.columns(8)
        for idx, (z_name, z_val) in enumerate(ZONE_DATA.items()):
            with z_cols[idx]:
                if st.button(z_name, key=f"btn_z_{z_name}", use_container_width=True):
                    st.session_state.selected_zone = z_name
                    st.rerun()

        sel_z = st.session_state.selected_zone
        sel_info = ZONE_DATA[sel_z]

        st.markdown(f"""
        <div class='panel-card' style='background:#f0f9ff; border-left:4px solid #2563eb;'>
            <h4 style='color:#1e40af; margin:0 0 6px 0;'>📍 선택 구역: {sel_z}</h4>
            <p style='margin:0 0 8px 0; font-size:13px;'><b>배치 적합도 점수:</b> <span style='color:#166534; font-weight:bold;'>{sel_info['score']}</span> | <b>수용 능력:</b> {sel_info['capacity']}</p>
            <p style='margin:0; font-size:14px; color:#334155; line-height:1.6;'><b>🧠 AI 공간 배치 사유:</b> {sel_info['rationale']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        # 4. Interactive AI Chat Drawer
        with st.expander("💬 AI 대화형 맞춤 디자인 조율 (클릭하여 열기)"):
            c_chat_list, c_chat_input = st.columns([2, 1])
            with c_chat_list:
                for msg in st.session_state.chat_history:
                    if msg["role"] == "user":
                        st.markdown(f"<div class='chat-user'>{msg['text']}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='chat-ai'>🤖 <b>AI:</b> {msg['text']}</div>", unsafe_allow_html=True)
            with c_chat_input:
                with st.form("chat_form_dash", clear_on_submit=True):
                    u_msg = st.text_input("AI 요구사항 입력", placeholder="예: '무대를 5m 뒤로 이동해줘'")
                    u_send = st.form_submit_button("전송")
                    if u_send and u_msg:
                        st.session_state.chat_history.append({"role": "user", "text": u_msg})
                        reply = f"요청하신 '{u_msg}' 사항을 분석했습니다. 소방법 및 동선을 재계산하여 {st.session_state.selected_zone} 구역 배치를 안전하게 재조정했습니다."
                        st.session_state.chat_history.append({"role": "ai", "text": reply})
                        st.rerun()

        st.divider()

        # Lower Grid Section
        col_bot1, col_bot2, col_bot3 = st.columns([4, 5, 3])

        with col_bot1:
            st.markdown("#### ⚖️ 설계 전 / 후 비교")
            st.markdown("""
            <div style="font-size:13px; background:#ffffff; padding:14px; border-radius:12px; border:1px solid #e2e8f0; box-shadow:0 1px 3px rgba(0,0,0,0.02);">
                <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                    <div style="width:48%; background:#fef2f2; padding:10px; border-radius:8px; border:1px solid #fecaca;">
                        <b style="color:#dc2626;">❌ 설계 전 (기존 방식)</b>
                        <ul style="margin:6px 0 0 16px; padding:0; color:#475569; font-size:12px;">
                            <li>공연장과 푸드존이 너무 가까움</li>
                            <li>동선이 엉켜 병목 구간 자주 발생</li>
                            <li>휴식 공간 부족</li>
                        </ul>
                    </div>
                    <div style="width:48%; background:#f0fdf4; padding:10px; border-radius:8px; border:1px solid #bbf7d0;">
                        <b style="color:#16a34a;">✅ AI 설계 후 (최적화 완료)</b>
                        <ul style="margin:6px 0 0 16px; padding:0; color:#475569; font-size:12px;">
                            <li>주요 시설의 균등한 공간 배치</li>
                            <li>효율적인 동선으로 혼잡도 감소</li>
                            <li>휴식 공간 및 편의시설 확충</li>
                        </ul>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_bot2:
            st.markdown("#### ⚙️ AI 행사 설계 프로세스")
            st.markdown("""
            <div style="font-size:12px; background:#ffffff; padding:14px; border-radius:12px; border:1px solid #e2e8f0;">
                <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; text-align:center;">
                    <div style="background:#f1f5f9; padding:8px; border-radius:8px; flex:1;">
                        <b>1. 행사 정보 입력</b><br><span style="color:#64748b; font-size:11px;">행사명, 목적, 장소 등</span>
                    </div>
                    <span>➡️</span>
                    <div style="background:#f1f5f9; padding:8px; border-radius:8px; flex:1;">
                        <b>2. 디지털 트윈 생성</b><br><span style="color:#64748b; font-size:11px;">장소 기반 3D/2D 모델링</span>
                    </div>
                    <span>➡️</span>
                    <div style="background:#f1f5f9; padding:8px; border-radius:8px; flex:1;">
                        <b>3. AI 공간 최적화</b><br><span style="color:#64748b; font-size:11px;">무대/부스 등 지능형 배치</span>
                    </div>
                    <span>➡️</span>
                    <div style="background:#f1f5f9; padding:8px; border-radius:8px; flex:1;">
                        <b>4. 군중 시뮬레이션</b><br><span style="color:#64748b; font-size:11px;">혼잡도 예측 & 동선 검토</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_bot3:
            st.markdown("#### 📊 분석 리포트 요약")
            st.markdown("""
            <div style="font-size:12px; background:#eff6ff; padding:14px; border-radius:12px; border:1px solid #bfdbfe; color:#1e3a8a;">
                <b style="font-size:13px;">📊 분석 리포트 요약</b>
                <p style="margin:6px 0 10px 0; line-height:1.5;">
                    AI 시뮬레이션 결과, 총 관중 5,000명 기준 최대 대기시간 65% 감소, 비상 이탈 동선 2.4배 향상되었습니다.
                </p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("📄 결재용 AI 보고서 바로가기", key="btn_to_report", use_container_width=True):
                st.session_state.page = "report"
                st.rerun()


elif st.session_state.page == "report":
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
        <div>
            <h2 style="margin:0; color:#0f172a; font-weight:800;">📄 AI 상사 결재용 직인 보고서</h2>
            <p style="margin:4px 0 0 0; color:#64748b; font-size:14px;">설계된 행사 디지털 트윈 결과와 안전 검토 분석 내용을 포함한 자동 보고서입니다.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:12px; padding:28px; box-shadow:0 4px 12px rgba(0,0,0,0.04);">
        <div style="text-align:center; border-bottom:2px solid #0f172a; padding-bottom:16px; margin-bottom:20px;">
            <h2 style="margin:0; color:#0f172a;">[기안서] {st.session_state.event_name} 공간 배치 및 안전 검토안</h2>
            <p style="margin:8px 0 0 0; color:#64748b; font-size:13px;">작성일: {datetime.now().strftime('%Y-%m-%d')} | 기안자: {st.session_state.user_name} | AI 검토 승인 완료</p>
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
            <tr style="background:#f8fafc; border-bottom:1px solid #e2e8f0;">
                <td style="padding:8px; font-weight:bold;">행사 목적</td>
                <td style="padding:8px;" colspan="3">{st.session_state.event_purpose}</td>
            </tr>
        </table>

        <h4 style="color:#2563eb; margin-top:20px;">2. AI 기반 공간 배치 타당성 검토</h4>
        <p style="font-size:13px; color:#334155; line-height:1.7;">
            본 행사장 배치는 <b>AI 공간 시뮬레이션 알고리즘</b>에 따라 법적 소방법, 피난 동선, 관람객 편의성을 통합 검토하여 작성되었습니다.<br>
            • <b>메인 무대:</b> 최대 시야각 및 관중 분산을 고려하여 북쪽 중앙 배치 (안전점수 98점)<br>
            • <b>응급의료센터:</b> 구급차 진출입 전용 통로 및 무대 최단 거리(15초) 동선 확보 (안전점수 97점)<br>
            • <b>화장실 및 푸드존:</b> 바람 방향 및 대기 줄 가이드라인 적용으로 혼잡도 최소화
        </p>

        <h4 style="color:#2563eb; margin-top:20px;">3. 군중 이동 및 혼잡도 예측 평가</h4>
        <div style="background:#f0fdf4; border:1px solid #bbf7d0; padding:12px; border-radius:8px; font-size:13px; color:#166534; margin-bottom:16px;">
            <b>✅ 시뮬레이션 총평:</b> 전체 위험도 '낮음(Safe)'. 병목 현상 예상 구간인 출입구 및 메인 무대 전면에 넓이 8m 이상의 순환형 가이드라인 설치를 권장합니다.
        </div>

        <div style="margin-top:28px; text-align:right;">
            <p style="font-weight:bold; font-size:14px; margin-bottom:4px;">위와 같이 AI 기반 행사 설계안을 보고합니다.</p>
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
    st.markdown("<h2 style='color:#0f172a; font-weight:800;'>⚙️ 시스템 및 로그인 설정</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b;'>사용자 계정 정보 및 AI 플랫폼 설정을 관리합니다.</p>", unsafe_allow_html=True)

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
            st.divider()
            if st.button("로그아웃 (Logout)", type="secondary"):
                st.session_state.logged_in = False
                st.rerun()
        else:
            st.warning("현재 로그아웃 상태입니다.")
            st.markdown("#### 🔑 로그인 / 회원가입")
            with st.form("login_form"):
                u_email = st.text_input("이메일 주소", placeholder="user@example.com")
                u_pw = st.text_input("비밀번호", type="password")
                sub_login = st.form_submit_button("로그인")
                if sub_login:
                    st.session_state.logged_in = True
                    st.session_state.user_name = u_email.split("@")[0] if "@" in u_email else "사용자"
                    st.success("로그인되었습니다!")
                    st.rerun()

    with col_s2:
        st.markdown("### 🤖 AI 엔진 & 디스플레이 설정")
        st.selectbox("AI 디지털 트윈 엔진 버젼", ["EventTwin AI v3.5 (최신)", "EventTwin AI v3.0", "Fast-Sim Lite"])
        st.slider("군중 시뮬레이션 밀도 정밀도", 1, 10, 8)
        st.toggle("화면 밝은 테마 (Light Mode)", value=True)
        st.toggle("자동 AI 배치 최적화 알림 수신", value=True)
