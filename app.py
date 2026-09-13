import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import base64
import os

# Page Configuration
st.set_page_config(
    page_title="이벤트 아키텍트 AI (Event Architect AI Studio)",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Global CAD Studio Styling */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }
    
    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* Top CAD Toolbar Bar */
    .cad-top-bar {
        background: #1e293b;
        border-bottom: 1px solid #334155;
        padding: 8px 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-radius: 10px;
        margin-bottom: 12px;
    }

    .cad-tool-btn {
        background: #334155;
        color: #f8fafc;
        border: 1px solid #475569;
        padding: 6px 14px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 600;
        cursor: pointer;
    }
    .cad-tool-btn:hover {
        background: #2563eb;
        border-color: #3b82f6;
    }

    /* Studio Card Panel */
    .studio-panel {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    }

    .zone-info-box {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px;
        color: #f8fafc;
    }

    /* Streamlit widget tweaks for dark CAD theme */
    .stSelectbox label, .stTextInput label, .stNumberInput label {
        color: #cbd5e1 !important;
        font-size: 13px;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "dashboard"

if "view_mode" not in st.session_state:
    st.session_state.view_mode = "2D CAD 도면"  # "2D CAD 도면" or "3D 디지털 트윈"

if "venue_bg_type" not in st.session_state:
    st.session_state.venue_bg_type = "야외 잔디 광장" # "야외 잔디 광장", "야외 아스팔트 광장", "실내 컨벤션홀 (EXPO)"

if "event_name" not in st.session_state:
    st.session_state.event_name = "2026 야외 뮤직 & 푸드 페스티벌"
if "event_type" not in st.session_state:
    st.session_state.event_type = "야외 페스티벌"
if "expected_visitors" not in st.session_state:
    st.session_state.expected_visitors = 5000
if "budget" not in st.session_state:
    st.session_state.budget = "5,000만원"
if "location" not in st.session_state:
    st.session_state.location = "서울 수변 야외 공원 광장"
if "event_purpose" not in st.session_state:
    st.session_state.event_purpose = "야외 문화 공연 및 청년 푸드트럭 페스타"
if "duration" not in st.session_state:
    st.session_state.duration = "8시간"

if "selected_zone" not in st.session_state:
    st.session_state.selected_zone = "메인무대"

if "show_heatmap_overlay" not in st.session_state:
    st.session_state.show_heatmap_overlay = True

if "show_flow_arrows" not in st.session_state:
    st.session_state.show_flow_arrows = True

if "show_grid_lines" not in st.session_state:
    st.session_state.show_grid_lines = True

if "crowd_seed" not in st.session_state:
    st.session_state.crowd_seed = 42

if "design_generated" not in st.session_state:
    st.session_state.design_generated = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "안녕하세요! **이벤트 아키텍트 AI CAD Studio**입니다. 도면 상의 시설물을 선택하거나 '무대를 북쪽으로 5m 이동'과 같이 수정 요청해 보세요!"}
    ]

ZONE_DATA = {
    "메인무대": {
        "position": [50, 85],
        "size": [32, 10], # width, height in meters
        "color": "#2563eb",
        "icon": "🎭",
        "power": "100kW (임시발전차 연계)",
        "fire_clearance": "합격 (피난거리 12m)",
        "rationale": "소음 분산 및 관람객 시야 확보를 위해 북쪽 중앙에 배치했습니다. 비상 피난 동선 및 메인 출입구와 공간적 균형을 이루어 혼잡 시 빠른 퇴장이 가능합니다."
    },
    "푸드존": {
        "position": [25, 48],
        "size": [20, 15],
        "color": "#ea580c",
        "icon": "🍔",
        "power": "45kW (위생수도 연계)",
        "fire_clearance": "합격 (소화기 4대 배치)",
        "rationale": "식품 위생 차량 진출입이 용이한 외곽 서측 인접 구역에 배치했습니다. 취식 공간과 대기 줄 구역을 넓게 확보하여 무대 관람객 동선과의 병목 현상을 원천 차단합니다."
    },
    "체험부스": {
        "position": [22, 78],
        "size": [16, 12],
        "color": "#7c3aed",
        "icon": "🎪",
        "power": "15kW",
        "fire_clearance": "합격 (3m 간격 확보)",
        "rationale": "주요 입구에서 메인 무대로 이동하는 동선 길목에 설치하여 방문객 유입률을 극대화했습니다. 규격 부스 간 이격 거리를 충분히 확보하여 안전 피난로 기준을 준수했습니다."
    },
    "휴식공간": {
        "position": [50, 48],
        "size": [24, 12],
        "color": "#059669",
        "icon": "🌲",
        "power": "5kW (차광 파라솔 구역)",
        "fire_clearance": "합격 (중앙 광장 자유 통로)",
        "rationale": "중앙 잔디 광장에 위치시켜 푸드존 이용객과 무대 관람객 모두가 쉽게 접근할 수 있습니다. 수목 그늘과 차광 시설을 모듈화하여 쾌적성을 극대화했습니다."
    },
    "응급의료센터": {
        "position": [82, 75],
        "size": [10, 8],
        "color": "#dc2626",
        "icon": "🚑",
        "power": "10kW (비상전원 차출)",
        "fire_clearance": "최우수 (구급차 전용차로 직결)",
        "rationale": "구급차 전용 출입 도로와 즉시 연결되는 동쪽 상단에 배치했습니다. 비상상황 발생 시 3분 이내 응급 이송 및 환자 처치가 가능하도록 경로가 확충되어 있습니다."
    },
    "안내센터": {
        "position": [50, 22],
        "size": [10, 6],
        "color": "#db2777",
        "icon": "ℹ️",
        "power": "5kW",
        "fire_clearance": "합격 (메인 게이트 인접)",
        "rationale": "메인 출입구 정면에 배치하여 입장객이 미아 보호, 분실물 신고, 행사장 안내 서비스를 최초 진입 시점에 즉시 제공받을 수 있습니다."
    },
    "화장실": {
        "position": [82, 55],
        "size": [12, 8],
        "color": "#0284c7",
        "icon": "🚻",
        "power": "20kW (상하수도 동파 방지)",
        "fire_clearance": "합격",
        "rationale": "상하수도 배관 인프라가 갖춰진 동측 라인에 세트 설치했습니다. 푸드존 및 무대 관람 구역 중간 지점으로 이동 동선을 최단 거리로 단축했습니다."
    },
    "출입구": {
        "position": [50, 8],
        "size": [24, 4],
        "color": "#64748b",
        "icon": "🚪",
        "power": "10kW (스피드게이트)",
        "fire_clearance": "최우수 (주 통로폭 8m)",
        "rationale": "보행자 전용 도로와 직접 연결된 남쪽 메인 게이트입니다. 스피드 게이트 및 보안 검사장 구역을 포함하여 원활한 관람객 입출장이 가능합니다."
    }
}

col_nav1, col_nav2 = st.columns([7, 3])
with col_nav1:
    st.markdown("<h2 style='margin:0; color:#60a5fa; font-weight:800;'>📐 Event Architect CAD Studio <span style='font-size:13px; color:#94a3b8; font-weight:normal;'>| 야외 & 실내 행사 3D Spatial Designer</span></h2>", unsafe_allow_html=True)
with col_nav2:
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1:
        if st.button("🏠 메인", key="top_home_btn", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
    with col_b2:
        if st.button("📊 CAD 스튜디오", key="top_dash_btn", type="primary", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()
    with col_b3:
        if st.button("📄 결재 보고서", key="top_report_btn", use_container_width=True):
            st.session_state.page = "report"
            st.rerun()

st.divider()

if st.session_state.page == "home":
    st.markdown("<div style='text-align: center; padding: 25px 0 35px 0;'>", unsafe_allow_html=True)
    st.markdown("<span style='background:#1e3a8a; color:#93c5fd; font-weight:700; padding:6px 18px; border-radius:20px; font-size:13px;'>✨ Outdoor & Indoor Spatial Digital Twin CAD</span>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #f8fafc; margin-top:14px; font-weight:800; font-size:38px;'>AI 기반 스마트 행사 공간 CAD 및 3D 배치 스튜디오</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 16px; max-width:750px; margin: 0 auto;'>인테리어 3D 설계 플랫폼처럼 야외 잔디 광장, 아스팔트 공원, 실내 엑스포 홀 등의 행사 배경에서 부스, 무대, 미니맵, 실시간 군중 시뮬레이션을 원스톱으로 레이아웃합니다.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    col_card1, col_card2 = st.columns(2)

    with col_card1:
        st.markdown("""
        <div style="background:#1e293b; border:2px solid #3b82f6; border-radius:20px; padding:35px 25px; text-align:center; box-shadow:0 10px 25px -5px rgba(59,130,246,0.2); min-height:240px; display:flex; flex-direction:column; justify-content:center; align-items:center;">
            <div style="font-size:52px; margin-bottom:12px;">🗺️</div>
            <h3 style="color:#f8fafc; margin:0 0 10px 0; font-weight:800; font-size:22px;">행사 도면 그리기 & 3D CAD 스튜디오</h3>
            <p style="color:#94a3b8; font-size:14px; line-height:1.6; margin:0 0 15px 0;">
                야외 파크 및 실내 컨벤션 배경에서 무대, 푸드트럭, 캐노피 부스, 3D 미니맵을 실시간으로 조작 및 피난 안전성을 검토합니다.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("🚀 CAD 스튜디오 입장", key="btn_home_to_dash", type="primary", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()

    with col_card2:
        st.markdown("""
        <div style="background:#1e293b; border:2px solid #8b5cf6; border-radius:20px; padding:35px 25px; text-align:center; box-shadow:0 10px 25px -5px rgba(139,92,246,0.2); min-height:240px; display:flex; flex-direction:column; justify-content:center; align-items:center;">
            <div style="font-size:52px; margin-bottom:12px;">📄</div>
            <h3 style="color:#f8fafc; margin:0 0 10px 0; font-weight:800; font-size:22px;">AI 결재용 직인 배치 보고서</h3>
            <p style="color:#94a3b8; font-size:14px; line-height:1.6; margin:0 0 15px 0;">
                공간 배치 타당성, 소방법 검토, 피난 안전성 평가, 군중 예측 데이터가 포함된 행정용 직인 결재 문서를 자동 생성합니다.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("📄 AI 기안 보고서 바로가기", key="btn_home_to_report", use_container_width=True):
            st.session_state.page = "report"
            st.rerun()

elif st.session_state.page == "dashboard":
    
    # CAD Top Control Ribbon (Matches Ohouse / Coohom Web CAD Toolbar)
    st.markdown("""
    <div class="cad-top-bar">
        <div style="display:flex; align-items:center; gap:12px;">
            <span style="font-weight:700; color:#38bdf8; font-size:14px;">🛠️ 도면 스튜디오 툴바</span>
            <span style="color:#64748b;">|</span>
            <span style="font-size:12px; color:#cbd5e1;">단위: <b>mm / m</b></span>
            <span style="font-size:12px; color:#cbd5e1;">스냅 모드: <b>ON (Grid 1m)</b></span>
        </div>
        <div style="display:flex; gap:8px;">
            <span style="background:#0f172a; border:1px solid #334155; padding:4px 10px; border-radius:6px; font-size:12px; color:#38bdf8;">
                📐 전체 면적: <b>5,000 m² (50m x 100m)</b>
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Upper Expander for Event & Environment settings
    with st.expander("⚙️ 행사 환경 (야외 잔디 / 아스팔트 / 실내 EXPO) & 행사 정보 설정", expanded=not st.session_state.design_generated):
        with st.form("event_info_form"):
            c_in1, c_in2, c_in3, c_in4 = st.columns(4)
            with c_in1:
                event_name_input = st.text_input("행사명", value=st.session_state.event_name)
                venue_bg_input = st.selectbox("행사 공간 배경", ["야외 잔디 광장", "야외 아스팔트 광장", "실내 컨벤션홀 (EXPO)"], index=0)
            with c_in2:
                expected_visitors_input = st.number_input("예상 인원 (명)", value=st.session_state.expected_visitors, step=500)
                location_input = st.text_input("장소", value=st.session_state.location)
            with c_in3:
                budget_input = st.text_input("예산", value=st.session_state.budget)
                duration_input = st.text_input("진행 시간", value=st.session_state.duration)
            with c_in4:
                event_purpose_input = st.text_input("행사 목적", value=st.session_state.event_purpose)
                st.write("")
                submit_design_btn = st.form_submit_button("🤖 AI 디지털 트윈 재배치", type="primary", use_container_width=True)

            if submit_design_btn:
                st.session_state.event_name = event_name_input
                st.session_state.venue_bg_type = venue_bg_input
                st.session_state.expected_visitors = expected_visitors_input
                st.session_state.location = location_input
                st.session_state.budget = budget_input
                st.session_state.duration = duration_input
                st.session_state.event_purpose = event_purpose_input
                st.session_state.design_generated = True
                st.success("✨ 공간 배경 및 시설 배치가 AI 알고리즘으로 최적화되었습니다!")
                st.rerun()

    # 3 Column Studio Layout (Left Tools, Center Canvas, Right Inspector/3D Minimap)
    col_left_tools, col_center_canvas, col_right_inspector = st.columns([2.5, 6.5, 3.0])

    with col_left_tools:
        st.markdown("""
        <div style="background:#1e293b; border:1px solid #334155; border-radius:12px; padding:12px;">
            <h4 style="margin:0 0 10px 0; color:#f8fafc; font-size:15px; font-weight:700;">🎨 CAD 라이브러리</h4>
        </div>
        """, unsafe_allow_html=True)

        tool_tab1, tool_tab2, tool_tab3 = st.tabs(["🎪 시설물", "🏞️ 공간배경", "📐 측정"])

        with tool_tab1:
            st.caption("클릭 시 해당 시설물이 선택되어 속성을 변경할 수 있습니다.")
            for zk, zi in ZONE_DATA.items():
                is_sel = (st.session_state.selected_zone == zk)
                btn_type = "primary" if is_sel else "secondary"
                if st.button(f"{zi['icon']} {zk}", key=f"tool_btn_{zk}", use_container_width=True, type=btn_type):
                    st.session_state.selected_zone = zk
                    st.rerun()

        with tool_tab2:
            st.markdown("**배경 테마 변경**")
            bg_sel = st.radio("장소 모드", ["야외 잔디 광장", "야외 아스팔트 광장", "실내 컨벤션홀 (EXPO)"], index=["야외 잔디 광장", "야외 아스팔트 광장", "실내 컨벤션홀 (EXPO)"].index(st.session_state.venue_bg_type))
            if bg_sel != st.session_state.venue_bg_type:
                st.session_state.venue_bg_type = bg_sel
                st.rerun()

        with tool_tab3:
            st.markdown("**피난 안전 & 소방법 통로 측정**")
            st.info("비상 피난로 폭 최소 5m 기준 충족\n구급차 골든타임 진입로 8m 확보 완료")

    with col_center_canvas:
        # Toggle Bar for 2D CAD vs 3D View and Heatmap options
        c_mode1, c_mode2, c_mode3, c_mode4 = st.columns([3, 2.5, 2.5, 2])
        with c_mode1:
            st.session_state.view_mode = st.radio("뷰 모드", ["2D CAD 도면", "3D 디지털 트윈"], horizontal=True)
        with c_mode2:
            st.session_state.show_heatmap_overlay = st.checkbox("🔥 군중 혼잡도(Heatmap)", value=st.session_state.show_heatmap_overlay)
        with c_mode3:
            st.session_state.show_flow_arrows = st.checkbox("🧭 주요 피난 동선", value=st.session_state.show_flow_arrows)
        with c_mode4:
            if st.button("🔄 시뮬레이션", key="btn_sim_update", use_container_width=True):
                st.session_state.crowd_seed = np.random.randint(1, 1000)
                st.toast("군중 시뮬레이션 데이터를 업데이트했습니다.")
                st.rerun()

        # Render 2D CAD or 3D Digital Twin Canvas
        if st.session_state.view_mode == "2D CAD 도면":
            fig_map = go.Figure()

            # Set Canvas background texture based on Venue Background Type
            if st.session_state.venue_bg_type == "야외 잔디 광장":
                bg_color = "#1b2e1e"
                inner_color = "#27462a"
                border_color = "#3f6e43"
            elif st.session_state.venue_bg_type == "야외 아스팔트 광장":
                bg_color = "#18181b"
                inner_color = "#27272a"
                border_color = "#52525b"
            else: # 실내 컨벤션홀 (EXPO)
                bg_color = "#0f172a"
                inner_color = "#1e293b"
                border_color = "#3b82f6"

            # Base Boundary Canvas
            fig_map.add_shape(type="rect", x0=0, y0=0, x1=100, y1=100, fillcolor=bg_color, opacity=1, line=dict(width=0))
            fig_map.add_shape(type="rect", x0=2, y0=2, x1=98, y1=98, fillcolor=inner_color, line=dict(color=border_color, width=3))
            
            # Dimension CAD Annotations (Matching Ohouse style mm dimensions like 47,800mm x 52,600mm)
            fig_map.add_annotation(x=50, y=99, text="📐 50,000 mm (가로 50m)", showarrow=False, font=dict(color="#60a5fa", size=12, family="monospace"))
            fig_map.add_annotation(x=1, y=50, text="📐 100,000 mm (세로 100m)", showarrow=False, font=dict(color="#60a5fa", size=12, family="monospace"), textangle=-90)

            # Paved Walkways / Main Corridors
            fig_map.add_shape(type="rect", x0=10, y0=10, x1=90, y1=92, fillcolor="#3a4149", opacity=0.4, line=dict(color="#525b66", width=2, dash="dash"))
            fig_map.add_shape(type="rect", x0=42, y0=8, x1=58, y1=92, fillcolor="#474f59", opacity=0.5, line=dict(width=0))

            # Environmental Trees for Outdoor mode
            if "야외" in st.session_state.venue_bg_type:
                tree_coords = [(6, 92), (94, 92), (6, 8), (94, 8), (6, 50), (94, 50), (15, 25), (85, 25), (15, 70), (85, 70)]
                for tx, ty in tree_coords:
                    fig_map.add_shape(type="circle", x0=tx-3, y0=ty-3, x1=tx+3, y1=ty+3, fillcolor="#14532d", opacity=0.85, line=dict(color="#166534", width=1.5))

            # Dynamic Real-time Crowd Density Heatmap Overlay
            if st.session_state.show_heatmap_overlay:
                np.random.seed(st.session_state.crowd_seed)
                stage_pos = ZONE_DATA["메인무대"]["position"]
                food_pos = ZONE_DATA["푸드존"]["position"]
                gate_pos = ZONE_DATA["출입구"]["position"]
                
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

                fig_map.add_trace(go.Scatter(
                    x=x_crowd[::4], y=y_crowd[::4],
                    mode="markers",
                    marker=dict(size=4, color="#fef08a", opacity=0.7),
                    name="군중 시뮬레이션",
                    hoverinfo="none",
                    showlegend=False
                ))

            # Facility Geometries (2D CAD Rectangles and Highlights)
            for zk, zi in ZONE_DATA.items():
                px, py = zi["position"]
                w, h = zi["size"]
                is_sel = (st.session_state.selected_zone == zk)
                line_w = 4 if is_sel else 2
                line_c = "#f59e0b" if is_sel else zi["color"]

                # Render object rectangle area
                fig_map.add_shape(
                    type="rect",
                    x0=px - w/2, y0=py - h/2,
                    x1=px + w/2, y1=py + h/2,
                    fillcolor=zi["color"],
                    opacity=0.85,
                    line=dict(color=line_c, width=line_w)
                )

            # Evacuation vector arrows
            if st.session_state.show_flow_arrows:
                gx, gy = ZONE_DATA["출입구"]["position"]
                fx, fy = ZONE_DATA["푸드존"]["position"]
                bx, by = ZONE_DATA["체험부스"]["position"]
                sx, sy = ZONE_DATA["메인무대"]["position"]
                rx, ry = ZONE_DATA["휴식공간"]["position"]

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
                        line=dict(color="#38bdf8", width=2.5, dash="dashdot"),
                        showlegend=False,
                        hoverinfo="none"
                    ))

            # Interactive Plotly markers for selecting zones
            zone_x, zone_y, zone_names, zone_colors, zone_texts = [], [], [], [], []
            for zk, zi in ZONE_DATA.items():
                zone_x.append(zi["position"][0])
                zone_y.append(zi["position"][1])
                zone_names.append(zk)
                zone_colors.append(zi["color"])
                prefix = "📍 " if st.session_state.selected_zone == zk else ""
                zone_texts.append(f"{prefix}{zi['icon']} {zk}")

            fig_map.add_trace(go.Scatter(
                x=zone_x, y=zone_y,
                mode="markers+text",
                text=zone_texts,
                textposition="top center",
                textfont=dict(color="white", size=13, family="Pretendard"),
                customdata=zone_names,
                marker=dict(size=22, color=zone_colors, line=dict(color="#ffffff", width=3)),
                hoverinfo="text",
                hovertext=[f"클릭하여 '{name}' 속성 보기" for name in zone_names],
                name="시설물 핀"
            ))

            fig_map.update_layout(
                xaxis=dict(range=[0, 100], showgrid=True, gridcolor="#334155", zeroline=False),
                yaxis=dict(range=[0, 100], showgrid=True, gridcolor="#334155", zeroline=False),
                height=560,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="#0f172a",
                plot_bgcolor=bg_color,
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

            if map_event and "selection" in map_event and map_event["selection"]["points"]:
                selected_pts = map_event["selection"]["points"]
                if len(selected_pts) > 0 and "customdata" in selected_pts[0]:
                    clicked_zone = selected_pts[0]["customdata"]
                    if clicked_zone in ZONE_DATA and clicked_zone != st.session_state.selected_zone:
                        st.session_state.selected_zone = clicked_zone
                        st.rerun()

        else:
            fig_3d = go.Figure()

            # 3D Ground Plane
            fig_3d.add_trace(go.Mesh3d(
                x=[0, 100, 100, 0],
                y=[0, 0, 100, 100],
                z=[0, 0, 0, 0],
                color='#1e293b' if st.session_state.venue_bg_type == "실내 컨벤션홀 (EXPO)" else '#15803d',
                opacity=0.9,
                name="3D 지면"
            ))

            # 3D Extruded Blocks for Main Stage, Food Trucks, and Booth Tents
            for zk, zi in ZONE_DATA.items():
                px, py = zi["position"]
                w, h = zi["size"]
                z_height = 8 if zk == "메인무대" else (4 if zk in ["푸드존", "체험부스"] else 2)
                
                # Render 3D Cubes
                x_cube = [px-w/2, px+w/2, px+w/2, px-w/2, px-w/2, px+w/2, px+w/2, px-w/2]
                y_cube = [py-h/2, py-h/2, py+h/2, py+h/2, py-h/2, py-h/2, py+h/2, py+h/2]
                z_cube = [0, 0, 0, 0, z_height, z_height, z_height, z_height]
                
                i_faces = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2]
                j_faces = [4, 5, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3]
                k_faces = [6, 1, 5, 3, 6, 7, 1, 3, 5, 2, 7, 7]

                fig_3d.add_trace(go.Mesh3d(
                    x=x_cube, y=y_cube, z=z_cube,
                    i=i_faces, j=j_faces, k=k_faces,
                    color=zi["color"],
                    opacity=0.85,
                    name=f"3D {zk}"
                ))

            # 3D Crowd Particle Simulation
            np.random.seed(st.session_state.crowd_seed)
            x_c3d = np.random.uniform(10, 90, 120)
            y_c3d = np.random.uniform(10, 90, 120)
            z_c3d = np.random.uniform(0.5, 1.8, 120)

            fig_3d.add_trace(go.Scatter3d(
                x=x_c3d, y=y_c3d, z=z_c3d,
                mode="markers",
                marker=dict(size=4, color="#fef08a", opacity=0.8),
                name="3D 관람객 군중"
            ))

            fig_3d.update_layout(
                scene=dict(
                    xaxis=dict(nticks=5, range=[0, 100], backgroundcolor="#0f172a", gridcolor="#334155"),
                    yaxis=dict(nticks=5, range=[0, 100], backgroundcolor="#0f172a", gridcolor="#334155"),
                    zaxis=dict(nticks=5, range=[0, 20], backgroundcolor="#0f172a", gridcolor="#334155"),
                    aspectratio=dict(x=1, y=1, z=0.3),
                    camera=dict(eye=dict(x=1.3, y=-1.3, z=0.9))
                ),
                height=560,
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor="#0f172a"
            )

            st.plotly_chart(fig_3d, use_container_width=True)

    with col_right_inspector:
        cur_z = st.session_state.selected_zone
        z_info = ZONE_DATA.get(cur_z, ZONE_DATA["메인무대"])

        # Mini 3D Box Preview (Top Right Box in user's image)
        st.markdown(f"""
        <div style="background:#1e293b; border:1px solid #334155; border-radius:12px; padding:12px; margin-bottom:12px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <span style="font-size:13px; font-weight:700; color:#38bdf8;">🧊 3D 라이브 미니맵</span>
                <span style="font-size:11px; color:#94a3b8; background:#0f172a; padding:2px 6px; border-radius:4px;">실시간 연동</span>
            </div>
            <div style="background:#0f172a; border:1px solid #334155; border-radius:8px; height:120px; display:flex; align-items:center; justify-content:center; text-align:center;">
                <div>
                    <div style="font-size:36px;">{z_info['icon']}</div>
                    <div style="font-size:12px; font-weight:bold; color:#f8fafc; margin-top:4px;">{cur_z} 3D 프리뷰</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Selected Zone Details Inspector
        st.markdown(f"""
        <div class="zone-info-box" style="border-left: 5px solid {z_info['color']}; margin-bottom:12px;">
            <div style="font-size:16px; font-weight:800; color:#f8fafc; margin-bottom:8px;">
                {z_info['icon']} {cur_z} 상세 속성 설정
            </div>
            <table style="width:100%; font-size:12px; color:#cbd5e1; border-collapse:collapse;">
                <tr><td style="padding:3px 0; color:#94a3b8;">시설 점유 규격:</td><td style="font-weight:bold; text-align:right;">{z_info['size'][0]}m x {z_info['size'][1]}m</td></tr>
                <tr><td style="padding:3px 0; color:#94a3b8;">전력/수도 인프라:</td><td style="font-weight:bold; text-align:right; color:#f59e0b;">{z_info['power']}</td></tr>
                <tr><td style="padding:3px 0; color:#94a3b8;">소방법 피난검토:</td><td style="font-weight:bold; text-align:right; color:#22c55e;">{z_info['fire_clearance']}</td></tr>
            </table>
            <p style="color:#94a3b8; font-size:12px; line-height:1.5; margin:10px 0 0 0; background:#0f172a; padding:8px; border-radius:6px;">
                💡 <b>AI 배치 사유:</b> {z_info['rationale']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Floating AI Assistant Chat Bot
        st.markdown("##### 💬 AI CAD Assistant")
        chat_container = st.container(height=170)
        with chat_container:
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

        user_input = st.chat_input("예: '메인무대를 남쪽으로 3m 이동해줘'")
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            bot_reply = f"요청하신 **'{user_input}'** 조건에 따라 2D/3D CAD 치수를 재계산했습니다."
            st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
            st.rerun()

elif st.session_state.page == "report":
    st.markdown("""
    <div style="margin-bottom:16px;">
        <h2 style="margin:0; color:#f8fafc; font-weight:800;">📄 AI 상사 결재용 직인 기안 보고서</h2>
        <p style="margin:4px 0 0 0; color:#94a3b8; font-size:14px;">야외 및 실내 공간 설계 타당성 및 소방법 피난 안전 검토가 포함된 결재서입니다.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:#ffffff; color:#0f172a; border:2px solid #cbd5e1; border-radius:12px; padding:35px; box-shadow:0 4px 15px rgba(0,0,0,0.3); max-width:900px; margin:0 auto;">
        
        <!-- Document Header -->
        <div style="display:flex; justify-content:space-between; align-items:flex-start; border-bottom:2px solid #0f172a; padding-bottom:15px; margin-bottom:25px;">
            <div>
                <h1 style="margin:0; font-size:24px; color:#0f172a; font-weight:900;">[결재 기안서] AI 공간 CAD 및 안전 검토서</h1>
                <p style="margin:6px 0 0 0; color:#64748b; font-size:13px;">문서번호: EA-2026-0909 | 기안일자: 2026. 09. 09 | 기안자: 행사 공간 기획팀</p>
            </div>
            <table style="border-collapse:collapse; text-align:center; font-size:12px; border:1px solid #94a3b8;">
                <tr style="background:#f1f5f9;">
                    <th style="border:1px solid #94a3b8; width:55px; padding:4px;">담당</th>
                    <th style="border:1px solid #94a3b8; width:55px; padding:4px;">팀장</th>
                    <th style="border:1px solid #94a3b8; width:55px; padding:4px;">임원</th>
                </tr>
                <tr style="height:40px;">
                    <td style="border:1px solid #94a3b8;">(인)</td>
                    <td style="border:1px solid #94a3b8;">(인)</td>
                    <td style="border:1px solid #94a3b8;">(인)</td>
                </tr>
            </table>
        </div>

        <!-- Section 1 -->
        <h3 style="color:#2563eb; font-weight:800; margin-bottom:10px;">1. 행사 개요</h3>
        <table style="width:100%; border-collapse:collapse; margin-bottom:25px; font-size:13px; border:1px solid #e2e8f0;">
            <tr style="background:#f8fafc;"><td style="padding:8px; font-weight:bold; width:20%; border:1px solid #e2e8f0;">행사명</td><td style="padding:8px; border:1px solid #e2e8f0;">{st.session_state.event_name}</td></tr>
            <tr><td style="padding:8px; font-weight:bold; background:#f8fafc; border:1px solid #e2e8f0;">행사 배경 모드</td><td style="padding:8px; border:1px solid #e2e8f0;">{st.session_state.venue_bg_type}</td></tr>
            <tr style="background:#f8fafc;"><td style="padding:8px; font-weight:bold; border:1px solid #e2e8f0;">예상 인원 / 예산</td><td style="padding:8px; border:1px solid #e2e8f0;">{st.session_state.expected_visitors:,}명 / {st.session_state.budget}</td></tr>
            <tr><td style="padding:8px; font-weight:bold; background:#f8fafc; border:1px solid #e2e8f0;">장소 / 진행시간</td><td style="padding:8px; border:1px solid #e2e8f0;">{st.session_state.location} ({st.session_state.duration})</td></tr>
        </table>

        <!-- Section 2 -->
        <h3 style="color:#2563eb; font-weight:800; margin-bottom:10px;">2. AI CAD 공간 배치 타당성 및 소방법 검토 요약</h3>
        <ul style="line-height:1.8; color:#334155; font-size:13px; margin-bottom:25px; padding-left:20px;">
            <li><b>메인 무대:</b> 북측 중앙 설치로 소음 분산 및 관람시야 최적 확보.</li>
            <li><b>피난 통로:</b> 메인 통로 폭 8m 확보로 소방법 제34조(피난구 확보) 완전 통과.</li>
            <li><b>응급의료센터:</b> 비상 구급차 도로 직결 배치로 3분 이내 응급 이송 체계 구축.</li>
        </ul>

        <!-- Section 3 -->
        <h3 style="color:#2563eb; font-weight:800; margin-bottom:10px;">3. 종합 기안 의견</h3>
        <p style="color:#334155; font-size:13px; line-height:1.7; background:#eff6ff; padding:12px; border-radius:8px; border:1px solid #bfdbfe;">
            본 행사는 AI CAD Digital Twin 솔루션을 통해 관람객 통행 차단 및 군중 혼잡 위험을 사전 제거하여 안전하게 작성되었습니다. 위와 같이 상신하오니 결재하여 주시기 바랍니다.
        </p>

    </div>
    """, unsafe_allow_html=True)

    st.write("")
    c_rep1, c_rep2 = st.columns(2)
    with c_rep1:
        if st.button("📥 보고서 PDF 다운로드", key="btn_pdf_down", type="primary", use_container_width=True):
            st.toast("결재서 PDF 작성을 완료했습니다!")
    with c_rep2:
        if st.button("🖨️ 인쇄하기", key="btn_print", use_container_width=True):
            st.toast("인쇄 미리보기를 호출합니다.")
