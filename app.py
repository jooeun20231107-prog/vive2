import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import base64
import os

# Page Configuration
st.set_page_config(
    page_title="이벤트 아키텍트 AI (Event Architect AI)",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Global Light Theme Styling */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }
    
    header[data-testid="stHeader"] {
        background: transparent;
    }

    .zone-info-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    .stButton>button {
        border-radius: 10px;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"

if "event_name" not in st.session_state:
    st.session_state.event_name = "2026 청춘 드림 페스티벌"
if "event_type" not in st.session_state:
    st.session_state.event_type = "축제"
if "expected_visitors" not in st.session_state:
    st.session_state.expected_visitors = 5000
if "budget" not in st.session_state:
    st.session_state.budget = "5,000만원"
if "location" not in st.session_state:
    st.session_state.location = "서울 평화의 광장 야외공원"
if "event_purpose" not in st.session_state:
    st.session_state.event_purpose = "지역 문화 활성화 및 청년 소통"
if "duration" not in st.session_state:
    st.session_state.duration = "8시간"
if "target_age" not in st.session_state:
    st.session_state.target_age = "10대~30대"
if "mood" not in st.session_state:
    st.session_state.mood = "활기차고 신나는 분위기"
if "entry_fee" not in st.session_state:
    st.session_state.entry_fee = "무료"

if "design_generated" not in st.session_state:
    st.session_state.design_generated = True

if "selected_zone" not in st.session_state:
    st.session_state.selected_zone = "메인무대"

if "show_heatmap_overlay" not in st.session_state:
    st.session_state.show_heatmap_overlay = True

if "show_flow_arrows" not in st.session_state:
    st.session_state.show_flow_arrows = True

if "show_grid_lines" not in st.session_state:
    st.session_state.show_grid_lines = False

if "crowd_seed" not in st.session_state:
    st.session_state.crowd_seed = 42

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "안녕하세요! **이벤트 아키텍트 AI**입니다. 도면 상의 시설물을 직접 클릭하거나 '무대를 뒤쪽으로 5m 이동해줘'와 같이 배치 조정을 요청해 보세요!"}
    ]

ZONE_DATA = {
    "메인무대": {
        "position": [50, 85],
        "color": "#2563eb",
        "icon": "🎭",
        "rationale": "소음 분산 및 관람객 시야 확보를 위해 북쪽 중앙에 배치했습니다. 비상 피난 동선 및 메인 출입구와 공간적 균형을 이루어 혼잡 시 빠른 퇴장이 가능합니다."
    },
    "푸드존": {
        "position": [25, 48],
        "color": "#ea580c",
        "icon": "🍔",
        "rationale": "식품 위생 차량 진출입이 용이한 외곽 서측 인접 구역에 배치했습니다. 취식 공간과 대기 줄 구역을 넓게 확보하여 무대 관람객 동선과의 병목 현상을 원천 차단합니다."
    },
    "체험부스": {
        "position": [22, 78],
        "color": "#7c3aed",
        "icon": "🎪",
        "rationale": "주요 입구에서 메인 무대로 이동하는 동선 길목에 설치하여 방문객 유입률을 극대화했습니다. 규격 부스 간 이격 거리를 충분히 확보하여 안전 피난로 기준을 준수했습니다."
    },
    "휴식공간": {
        "position": [50, 48],
        "color": "#059669",
        "icon": "🌲",
        "rationale": "중앙 잔디 광장에 위치시켜 푸드존 이용객과 무대 관람객 모두가 쉽게 접근할 수 있습니다. 수목 그늘과 차광 시설을 모듈화하여 쾌적성을 극대화했습니다."
    },
    "응급의료센터": {
        "position": [82, 75],
        "color": "#dc2626",
        "icon": "🚑",
        "rationale": "구급차 전용 출입 도로와 즉시 연결되는 동쪽 상단에 배치했습니다. 비상상황 발생 시 3분 이내 응급 이송 및 환자 처치가 가능하도록 경로가 확충되어 있습니다."
    },
    "안내센터": {
        "position": [50, 22],
        "color": "#db2777",
        "icon": "ℹ️",
        "rationale": "메인 출입구 정면에 배치하여 입장객이 미아 보호, 분실물 신고, 행사장 안내 서비스를 최초 진입 시점에 즉시 제공받을 수 있습니다."
    },
    "화장실": {
        "position": [82, 55],
        "color": "#0284c7",
        "icon": "🚻",
        "rationale": "상하수도 배관 인프라가 갖춰진 동측 라인에 세트 설치했습니다. 푸드존 및 무대 관람 구역 중간 지점으로 이동 동선을 최단 거리로 단축했습니다."
    },
    "출입구": {
        "position": [50, 8],
        "color": "#0f172a",
        "icon": "🚪",
        "rationale": "보행자 전용 도로와 직접 연결된 남쪽 메인 게이트입니다. 스피드 게이트 및 보안 검사장 구역을 포함하여 원활한 관람객 입출장이 가능합니다."
    }
}

# Navigation Top bar
col_nav1, col_nav2 = st.columns([8, 2])
with col_nav1:
    if st.button("📐 이벤트 아키텍트 AI", key="logo_home_btn", type="tertiary"):
        st.session_state.page = "home"
        st.rerun()

with col_nav2:
    st.write("<div style='text-align:right;'>", unsafe_allow_html=True)
    if st.button("⚙️ 설정", key="top_setting_btn", use_container_width=False):
        st.session_state.page = "settings"
        st.rerun()
    st.write("</div>", unsafe_allow_html=True)

st.divider()

if st.session_state.page == "home":
    st.markdown("<div style='text-align: center; padding: 15px 0 25px 0;'>", unsafe_allow_html=True)
    st.markdown("<span style='background:#eff6ff; color:#2563eb; font-weight:700; padding:6px 16px; border-radius:20px; font-size:13px;'>✨ AI Spatial Digital Twin Platform</span>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #0f172a; margin-top:14px; font-weight:800; font-size:36px;'>AI 기반 스마트 행사 공간 설계 플랫폼</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 16px; max-width:680px; margin: 0 auto;'>행사 기본 정보 입력만으로 2D CAD 디지털 트윈 도면, 실시간 혼잡도 시뮬레이션, 상사 결재용 리포트까지 원스톱으로 완벽히 자동 생성합니다.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    col_card1, col_card2 = st.columns(2)

    with col_card1:
        st.markdown("""
        <div style="background:#ffffff; border:2px solid #3b82f6; border-radius:20px; padding:35px 25px; text-align:center; box-shadow:0 10px 25px -5px rgba(59,130,246,0.12); min-height:240px; display:flex; flex-direction:column; justify-content:center; align-items:center;">
            <div style="font-size:52px; margin-bottom:12px;">📊</div>
            <h3 style="color:#0f172a; margin:0 0 10px 0; font-weight:800; font-size:22px;">AI 기반 행사 자동 설계 대시보드</h3>
            <p style="color:#64748b; font-size:14px; line-height:1.6; margin:0 0 15px 0;">
                실제 무대, 푸드트럭, 캐노피 부스 시설물이 2D CAD로 정밀 배치되는 디지털 트윈 도면 편집 및 AI 시뮬레이션 워크스페이스입니다.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("🚀 대시보드 바로가기", key="btn_home_to_dash", type="primary", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()

    with col_card2:
        st.markdown("""
        <div style="background:#ffffff; border:2px solid #8b5cf6; border-radius:20px; padding:35px 25px; text-align:center; box-shadow:0 10px 25px -5px rgba(139,92,246,0.12); min-height:240px; display:flex; flex-direction:column; justify-content:center; align-items:center;">
            <div style="font-size:52px; margin-bottom:12px;">📄</div>
            <h3 style="color:#0f172a; margin:0 0 10px 0; font-weight:800; font-size:22px;">AI 상사 결재용 직인 보고서</h3>
            <p style="color:#64748b; font-size:14px; line-height:1.6; margin:0 0 15px 0;">
                공간 배치 타당성, 소방법 검토, 피난 안전성 평가, 군중 예측 데이터가 포함된 완성형 결재용 기안 문서를 자동 생성합니다.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("📄 AI 보고서 바로가기", key="btn_home_to_report", use_container_width=True):
            st.session_state.page = "report"
            st.rerun()

elif st.session_state.page == "dashboard":
    st.markdown("""
    <div style="margin-bottom:14px;">
        <h2 style="margin:0; color:#0f172a; font-weight:800;">📊 AI 기반 행사 공간 자동 설계 대시보드</h2>
        <p style="margin:4px 0 0 0; color:#64748b; font-size:14px;">행사 기본 정보를 바탕으로 디지털 트윈 도면을 생성하고, 구역 배치 사유 및 실시간 혼잡도 시뮬레이션을 수행합니다.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📝 행사 기본 정보 설정 및 AI 공간 재설계", expanded=not st.session_state.design_generated):
        with st.form("event_info_form"):
            c_in1, c_in2, c_in3, c_in4 = st.columns(4)
            with c_in1:
                event_name_input = st.text_input("행사명", value=st.session_state.event_name)
                event_type_input = st.selectbox("행사 유형", ["축제", "박람회/전시회", "기업 행사", "팝업스토어"], index=0)
            with c_in2:
                expected_visitors_input = st.number_input("예상 인원 (명)", value=st.session_state.expected_visitors, step=500)
                location_input = st.text_input("장소 선택", value=st.session_state.location)
            with c_in3:
                budget_input = st.text_input("예산", value=st.session_state.budget)
                duration_input = st.text_input("진행 시간", value=st.session_state.duration)
            with c_in4:
                event_purpose_input = st.text_input("행사 목적", value=st.session_state.event_purpose)
                st.write("")
                submit_design_btn = st.form_submit_button("🤖 AI 이벤트 디자인 생성", type="primary", use_container_width=True)

            if submit_design_btn:
                st.session_state.event_name = event_name_input
                st.session_state.event_type = event_type_input
                st.session_state.expected_visitors = expected_visitors_input
                st.session_state.location = location_input
                st.session_state.budget = budget_input
                st.session_state.duration = duration_input
                st.session_state.event_purpose = event_purpose_input
                st.session_state.design_generated = True
                st.success("✨ AI가 장소에 맞춘 최적 디지털 트윈 도면 생성을 완료했습니다!")
                st.rerun()

    # Event Summary Info Pill
    st.markdown(f"""
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:12px; padding:10px 18px; margin-bottom:16px; font-size:13px; color:#334155; display:flex; flex-wrap:wrap; gap:16px;">
        <span>🆔 <b>행사명:</b> {st.session_state.event_name}</span>
        <span>🏷️ <b>유형:</b> {st.session_state.event_type}</span>
        <span>👥 <b>예상인원:</b> {st.session_state.expected_visitors:,}명</span>
        <span>📍 <b>장소:</b> {st.session_state.location}</span>
        <span>💰 <b>예산:</b> {st.session_state.budget}</span>
    </div>
    """, unsafe_allow_html=True)

    # Controls Bar
    col_ctrl1, col_ctrl2, col_ctrl3, col_ctrl4 = st.columns([3, 3, 3, 3])
    with col_ctrl1:
        st.session_state.show_heatmap_overlay = st.checkbox("🔥 실시간 혼잡도(Heatmap) 오버레이", value=st.session_state.show_heatmap_overlay)
    with col_ctrl2:
        st.session_state.show_flow_arrows = st.checkbox("🧭 주요 이동 동선 표시", value=st.session_state.show_flow_arrows)
    with col_ctrl3:
        st.session_state.show_grid_lines = st.checkbox("📐 CAD 그리드 선 표시", value=st.session_state.show_grid_lines)
    with col_ctrl4:
        if st.button("🔄 실시간 혼잡도 갱신", key="btn_recalc", use_container_width=True):
            st.session_state.crowd_seed = np.random.randint(1, 1000)
            st.toast("실시간 군중 시뮬레이션 데이터를 업데이트했습니다.")
            st.rerun()

    col_map_main, col_map_side = st.columns([7, 5])

    with col_map_main:
        st.markdown("#### 🗺️ AI 디지털 트윈 행사 설계 도면 (2D CAD 뷰)")
        st.caption("💡 Tip: 도면 상의 각 구역 핀/시설물 아이콘을 클릭하면 오른쪽에서 배치 타당성 요약을 바로 확인하실 수 있습니다.")

        fig_map = go.Figure()

        # Park Environment Canvas (Rich textured park background replacing plain white background)
        fig_map.add_shape(type="rect", x0=0, y0=0, x1=100, y1=100, fillcolor="#1b2e1e", opacity=1, line=dict(width=0))
        fig_map.add_shape(type="rect", x0=2, y0=2, x1=98, y1=98, fillcolor="#27462a", line=dict(color="#3f6e43", width=3))
        
        # Paved Main Plaza & Walkways (Stone texture style)
        fig_map.add_shape(type="rect", x0=10, y0=10, x1=90, y1=92, fillcolor="#3a4149", line=dict(color="#525b66", width=2, dash="dash"))
        fig_map.add_shape(type="rect", x0=40, y0=8, x1=60, y1=92, fillcolor="#474f59", line=dict(width=0))
        fig_map.add_shape(type="rect", x0=10, y0=42, x1=90, y1=54, fillcolor="#474f59", line=dict(width=0))

        # Background Tree & Landscaping Elements
        tree_coords = [(6, 92), (94, 92), (6, 8), (94, 8), (6, 50), (94, 50), (15, 25), (85, 25), (15, 70), (85, 70)]
        for tx, ty in tree_coords:
            fig_map.add_shape(type="circle", x0=tx-3, y0=ty-3, x1=tx+3, y1=ty+3, fillcolor="#14532d", opacity=0.85, line=dict(color="#166534", width=1.5))

        # Dynamic Real-time Crowd Density Heatmap Simulation Overlay
        if st.session_state.show_heatmap_overlay:
            np.random.seed(st.session_state.crowd_seed)
            stage_pos = ZONE_DATA["메인무대"]["position"]
            food_pos = ZONE_DATA["푸드존"]["position"]
            gate_pos = ZONE_DATA["출입구"]["position"]
            
            # Simulated crowd particle concentrations
            x_stage = np.random.normal(stage_pos[0], 8, 450)
            y_stage = np.random.normal(stage_pos[1] - 8, 6, 450)
            
            x_food = np.random.normal(food_pos[0] + 5, 5, 250)
            y_food = np.random.normal(food_pos[1], 5, 250)

            x_gate = np.random.normal(gate_pos[0], 6, 200)
            y_gate = np.random.normal(gate_pos[1] + 6, 4, 200)

            x_crowd = np.concatenate([x_stage, x_food, x_gate])
            y_crowd = np.concatenate([y_stage, y_food, y_gate])
            x_crowd = np.clip(x_crowd, 2, 98)
            y_crowd = np.clip(y_crowd, 2, 98)

            fig_map.add_trace(go.Histogram2dContour(
                x=x_crowd, y=y_crowd,
                colorscale=[
                    [0.0, 'rgba(0,0,0,0)'],
                    [0.2, 'rgba(59,130,246,0.3)'],
                    [0.45, 'rgba(34,197,94,0.55)'],
                    [0.7, 'rgba(245,158,11,0.75)'],
                    [1.0, 'rgba(239,68,68,0.92)']
                ],
                showscale=False,
                ncontours=18,
                line=dict(width=0),
                hoverinfo="none"
            ))

            # Live moving crowd particles (dots)
            fig_map.add_trace(go.Scatter(
                x=x_crowd[::4], y=y_crowd[::4],
                mode="markers",
                marker=dict(size=4, color="#fef08a", opacity=0.7),
                name="군중 위치 시뮬레이션",
                hoverinfo="none",
                showlegend=False
            ))

        # Facility Structures (2D CAD Detailed Geometries)
        # A. 메인무대
        sx, sy = ZONE_DATA["메인무대"]["position"]
        fig_map.add_shape(type="rect", x0=sx-16, y0=sy-5, x1=sx+16, y1=sy+5, fillcolor="#0f172a", line=dict(color="#3b82f6", width=3))
        fig_map.add_shape(type="rect", x0=sx-12, y0=sy+3.5, x1=sx+12, y1=sy+4.8, fillcolor="#60a5fa", line=dict(color="#ffffff", width=1))
        fig_map.add_shape(type="rect", x0=sx-18, y0=sy-4, x1=sx-16.5, y1=sy+2, fillcolor="#0284c7", line=dict(color="#38bdf8", width=1.5))
        fig_map.add_shape(type="rect", x0=sx+16.5, y0=sy-4, x1=sx+18, y1=sy+2, fillcolor="#0284c7", line=dict(color="#38bdf8", width=1.5))

        # B. 푸드존
        fx, fy = ZONE_DATA["푸드존"]["position"]
        for offset_y in [-6, 0, 6]:
            fig_map.add_shape(type="rect", x0=fx-8, y0=fy+offset_y-1.8, x1=fx-2, y1=fy+offset_y+1.8, fillcolor="#c2410c", line=dict(color="#f97316", width=1.5))
            fig_map.add_shape(type="rect", x0=fx-2, y0=fy+offset_y-1.4, x1=fx, y1=fy+offset_y+1.4, fillcolor="#fed7aa", line=dict(color="#f97316", width=1))

        # C. 체험부스
        bx, by = ZONE_DATA["체험부스"]["position"]
        for offset_y in [-5, 0, 5]:
            for offset_x in [-4, 2]:
                fig_map.add_shape(type="rect", x0=bx+offset_x, y0=by+offset_y, x1=bx+offset_x+4, y1=by+offset_y+3.5, fillcolor="#6d28d9", line=dict(color="#a78bfa", width=1.5))

        # D. 휴식공간
        rx, ry = ZONE_DATA["휴식공간"]["position"]
        fig_map.add_shape(type="rect", x0=rx-12, y0=ry-6, x1=rx+12, y1=ry+6, fillcolor="#047857", line=dict(color="#34d399", width=2))

        # E. 응급의료센터
        mx, my = ZONE_DATA["응급의료센터"]["position"]
        fig_map.add_shape(type="rect", x0=mx-6, y0=my-4, x1=mx+2, y1=my+4, fillcolor="#b91c1c", line=dict(color="#fca5a5", width=2))

        # F. 출입구
        gx, gy = ZONE_DATA["출입구"]["position"]
        fig_map.add_shape(type="rect", x0=gx-12, y0=gy-2, x1=gx+12, y1=gy+2, fillcolor="#0f172a", line=dict(color="#94a3b8", width=2))

        # Vector Flow Arrows
        if st.session_state.show_flow_arrows:
            flow_paths = [
                (gx, gy+2, fx, fy-6),
                (gx, gy+2, bx, by-6),
                (fx, fy+6, sx-10, sy-10),
                (bx, by+5, sx-12, sy-10),
                (gx, gy+2, rx-4, ry-6),
            ]
            for x1_p, y1_p, x2_p, y2_p in flow_paths:
                fig_map.add_trace(go.Scatter(
                    x=[x1_p, x2_p], y=[y1_p, y2_p],
                    mode="lines",
                    line=dict(color="#60a5fa", width=2.5, dash="dashdot"),
                    showlegend=False,
                    hoverinfo="none"
                ))

        # Interactive Zone Markers on Plotly
        zone_x = []
        zone_y = []
        zone_names = []
        zone_colors = []
        zone_texts = []

        for zk, zi in ZONE_DATA.items():
            zone_x.append(zi["position"][0])
            zone_y.append(zi["position"][1])
            zone_names.append(zk)
            zone_colors.append(zi["color"])
            
            is_sel = (st.session_state.selected_zone == zk)
            prefix = "📌 " if is_sel else ""
            zone_texts.append(f"{prefix}{zi['icon']} {zk}")

        fig_map.add_trace(go.Scatter(
            x=zone_x,
            y=zone_y,
            mode="markers+text",
            text=zone_texts,
            textposition="top center",
            textfont=dict(color="white", size=13, family="Pretendard"),
            customdata=zone_names,
            marker=dict(
                size=22,
                color=zone_colors,
                line=dict(color="#ffffff", width=3)
            ),
            hoverinfo="text",
            hovertext=[f"클릭하여 '{name}' 정보 보기" for name in zone_names],
            name="구역 아이콘"
        ))

        fig_map.update_layout(
            xaxis=dict(range=[0, 100], showgrid=st.session_state.show_grid_lines, zeroline=False, visible=st.session_state.show_grid_lines),
            yaxis=dict(range=[0, 100], showgrid=st.session_state.show_grid_lines, zeroline=False, visible=st.session_state.show_grid_lines),
            height=580,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="#1b2e1e",
            plot_bgcolor="#1b2e1e",
            showlegend=False,
            clickmode="event+select"
        )

        map_event = st.plotly_chart(
            fig_map,
            use_container_width=True,
            on_select="rerun",
            selection_mode="points",
            key="cad_digital_twin_map"
        )

        # Handle map point selection event
        if map_event and "selection" in map_event and map_event["selection"]["points"]:
            selected_pts = map_event["selection"]["points"]
            if len(selected_pts) > 0 and "customdata" in selected_pts[0]:
                clicked_zone = selected_pts[0]["customdata"]
                if clicked_zone in ZONE_DATA and clicked_zone != st.session_state.selected_zone:
                    st.session_state.selected_zone = clicked_zone
                    st.rerun()

    with col_map_side:
        cur_z = st.session_state.selected_zone
        z_info = ZONE_DATA.get(cur_z, ZONE_DATA["메인무대"])

        st.markdown(f"#### 💡 '{cur_z}' AI 공간 배치 타당성 요약")
        st.markdown(f"""
        <div class="zone-info-box" style="border-left: 6px solid {z_info['color']};">
            <div style="font-size:18px; font-weight:800; color:#0f172a; margin-bottom:10px;">
                {z_info['icon']} {cur_z} 공간 배치 요약
            </div>
            <p style="color:#334155; font-size:14px; line-height:1.7; margin:0;">
                {z_info['rationale']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        st.markdown("#### 💬 AI 실시간 디자인 대화 (Floating Assistant)")
        
        chat_container = st.container(height=280)
        with chat_container:
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

        user_input = st.chat_input("예: '무대를 뒤로 5m 옮겨줘' 또는 '푸드트럭 수 늘려줘'")
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            bot_reply = f"요청하신 **'{user_input}'** 조건에 맞추어 도면 배치를 수정했습니다. 소방법 기준 피난 통로가 확보되었는지 함께 검토를 완료했습니다."
            st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
            st.rerun()

elif st.session_state.page == "report":
    st.markdown("""
    <div style="margin-bottom:16px;">
        <h2 style="margin:0; color:#0f172a; font-weight:800;">📄 AI 상사 결재용 직인 기안 보고서</h2>
        <p style="margin:4px 0 0 0; color:#64748b; font-size:14px;">인쇄 및 직장 상사 결재가 즉시 가능한 완벽한 형태의 행정 기안서입니다.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:#ffffff; border:2px solid #cbd5e1; border-radius:12px; padding:35px; box-shadow:0 4px 15px rgba(0,0,0,0.05); max-width:900px; margin:0 auto;">
        
        <!-- Document Title & Approval Table -->
        <div style="display:flex; justify-content:space-between; align-items:flex-start; border-bottom:2px solid #0f172a; padding-bottom:15px; margin-bottom:25px;">
            <div>
                <h1 style="margin:0; font-size:26px; color:#0f172a; font-weight:900;">[결재 기안서] AI 기반 행사 공간 설계 및 안전 검토서</h1>
                <p style="margin:6px 0 0 0; color:#64748b; font-size:13px;">문서번호: EA-2026-0909 | 기안일자: 2026. 09. 09 | 기안자: 행사 기획팀</p>
            </div>
            <table style="border-collapse:collapse; text-align:center; font-size:12px; border:1px solid #94a3b8;">
                <tr style="background:#f1f5f9;">
                    <th style="border:1px solid #94a3b8; width:60px; padding:4px;">담당</th>
                    <th style="border:1px solid #94a3b8; width:60px; padding:4px;">팀장</th>
                    <th style="border:1px solid #94a3b8; width:60px; padding:4px;">임원</th>
                </tr>
                <tr style="height:45px;">
                    <td style="border:1px solid #94a3b8;">(인)</td>
                    <td style="border:1px solid #94a3b8;">(인)</td>
                    <td style="border:1px solid #94a3b8;">(인)</td>
                </tr>
            </table>
        </div>

        <!-- 1. General Info -->
        <h3 style="color:#2563eb; font-weight:800; margin-bottom:10px;">1. 행사 개요</h3>
        <table style="width:100%; border-collapse:collapse; margin-bottom:25px; font-size:14px; border:1px solid #e2e8f0;">
            <tr style="background:#f8fafc;"><td style="padding:8px; font-weight:bold; width:20%; border:1px solid #e2e8f0;">행사명</td><td style="padding:8px; border:1px solid #e2e8f0;">{st.session_state.event_name}</td></tr>
            <tr><td style="padding:8px; font-weight:bold; background:#f8fafc; border:1px solid #e2e8f0;">행사 목적</td><td style="padding:8px; border:1px solid #e2e8f0;">{st.session_state.event_purpose}</td></tr>
            <tr style="background:#f8fafc;"><td style="padding:8px; font-weight:bold; border:1px solid #e2e8f0;">예상 인원 / 예산</td><td style="padding:8px; border:1px solid #e2e8f0;">{st.session_state.expected_visitors:,}명 / {st.session_state.budget}</td></tr>
            <tr><td style="padding:8px; font-weight:bold; background:#f8fafc; border:1px solid #e2e8f0;">장소 / 진행시간</td><td style="padding:8px; border:1px solid #e2e8f0;">{st.session_state.location} ({st.session_state.duration})</td></tr>
        </table>

        <!-- 2. Spatial AI Design Evaluation -->
        <h3 style="color:#2563eb; font-weight:800; margin-bottom:10px;">2. AI 공간 배치 타당성 및 소방법 검토 요약</h3>
        <ul style="line-height:1.8; color:#334155; font-size:14px; margin-bottom:25px; padding-left:20px;">
            <li><b>메인 무대 & 관람석:</b> 북측 중앙 배치를 통해 소음 분산 및 관람 시야 확보 완료.</li>
            <li><b>피난 및 안전 통로:</b> 메인 도로 폭 5m 이상 확보하여 소방법 제34조(피난구 확보) 기준 통과.</li>
            <li><b>응급의료센터:</b> 비상 구급차 전용 도로(동측)와 직접 인접시켜 골든타임 이내 이송 가능 구조.</li>
            <li><b>군중 예측 혼잡도 시뮬레이션:</b> 피크 시간대 병목 현상이 발생하지 않도록 출입구 게이트 분할 설치.</li>
        </ul>

        <!-- 3. Final Conclusion -->
        <h3 style="color:#2563eb; font-weight:800; margin-bottom:10px;">3. 종합 의견 및 기안 목적</h3>
        <p style="color:#334155; font-size:14px; line-height:1.7; background:#eff6ff; padding:15px; border-radius:8px; border:1px solid #bfdbfe;">
            본 행사는 AI 기반 공간 최적화 알고리즘을 통해 관람객 이동 편의성과 안전성을 모두 준수하는 최적 공간 도안으로 설계되었습니다. 위와 같이 행사를 추진하고자 하오니 검토 후 결재하여 주시기 바랍니다.
        </p>

    </div>
    """, unsafe_allow_html=True)

    st.write("")
    c_rep1, c_rep2 = st.columns(2)
    with c_rep1:
        if st.button("📥 보고서 PDF 다운로드", key="btn_pdf_down", type="primary", use_container_width=True):
            st.toast("기안 보고서 PDF 파일 작성을 완료했습니다!")
    with c_rep2:
        if st.button("🖨️ 결재용 문서 인쇄하기", key="btn_print", use_container_width=True):
            st.toast("인쇄 창을 호출합니다.")

elif st.session_state.page == "settings":
    st.markdown("## ⚙️ 시스템 및 로그인 설정")
    
    with st.container():
        st.markdown("### 👤 사용자 계정 정보")
        st.info("현재 **이벤트 아키텍트 최고 관리자 (Admin)** 계정으로 로그인되어 있습니다.")
        
        st.text_input("계정 이메일", value="admin@eventarchitect.ai")
        st.text_input("소속 부서", value="행사 기획 총괄팀")
        
        st.divider()
        st.markdown("### 🤖 AI 모델 설정")
        st.selectbox("Spatial AI Engine Version", ["Event-Architect-v4.2 (최신 최적화)", "Event-Architect-v4.0", "Legacy CAD Engine"])
        
        st.divider()
        if st.button("🔒 로그아웃", key="btn_logout", type="primary"):
            st.success("로그아웃 되었습니다.")
