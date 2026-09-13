import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Streamlit page setup
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
        border-radius: 12px;
        margin-top: 10px;
        color: #0F172A;
    }

    /* 상단 로고 버튼 및 사이드바 간격 */
    div[data-testid="stSidebarHeader"] {
        padding-top: 0.5rem;
    }

    /* Streamlit 버튼 커스텀 */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

DEFAULT_FACILITIES = {
    "stage": {
        "name": "공연장 (메인무대)",
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
        "x": 820, "y": 280, "w": 160, "h": 100,
        "reason": "동쪽 측면에 위치시켜 상하수 인프라 접근성을 확보하고 대기 줄 정체를 방지합니다."
    },
    "info": {
        "name": "안내센터",
        "icon": "ℹ️",
        "hex": "#EC4899",
        "x": 500, "y": 570, "w": 160, "h": 70,
        "reason": "주 출입구 정면에 위치시켜 길 안내 및 관람 문의를 신속하게 처리합니다."
    },
    "exit": {
        "name": "출입구",
        "icon": "🚪",
        "hex": "#64748B",
        "x": 500, "y": 660, "w": 220, "h": 60,
        "reason": "남쪽 정문에 넓게 위치하여 대규모 인파의 효율적 진출입 및 비상 대피를 유도합니다."
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
    st.session_state['facilities'] = {k: v.copy() for k, v in DEFAULT_FACILITIES.items()}
if 'event_name' not in st.session_state:
    st.session_state['event_name'] = "2026 청춘 페스티벌"
if 'expected_visitors' not in st.session_state:
    st.session_state['expected_visitors'] = 5000
if 'budget' not in st.session_state:
    st.session_state['budget'] = "5,000만원"
if 'location' not in st.session_state:
    st.session_state['location'] = "서울 올림픽공원 잔디마당"
if 'chat_messages' not in st.session_state:
    st.session_state['chat_messages'] = [
        {"role": "assistant", "content": "안녕하세요! AI 행사 공간 설계 도우미입니다. '푸드존을 외곽으로 이동해줘' 또는 '화장실을 의료 센터 근처로 배치해줘' 같이 입력해 보세요."}
    ]

def parse_and_apply_ai_command(prompt: str):
    prompt_clean = prompt.replace(" ", "")
    facs = st.session_state['facilities']
    
    target_key = None
    if "푸드" in prompt_clean or "음식" in prompt_clean or "먹거리" in prompt_clean:
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
    action_desc = ""

    if "외곽" in prompt_clean or "멀리" in prompt_clean or "분리" in prompt_clean:
        if target_key == "food":
            fac["x"] = 140
            fac["y"] = 420
            action_desc = "푸드존을 조리 연기 차단 및 혼잡 분리를 위해 서쪽 최외곽 독립 구역으로 이동시켰습니다."
        elif target_key == "toilet":
            fac["x"] = 880
            fac["y"] = 380
            action_desc = "화장실을 메인 무대와 거리를 둔 동쪽 외곽 구역으로 재배치했습니다."
        else:
            fac["x"] = max(120, fac["x"] - 120)
            action_desc = f"{fac['name']}을(를) 외곽 구역으로 이동 조정했습니다."
    elif "북쪽" in prompt_clean or "위" in prompt_clean:
        fac["y"] = max(90, fac["y"] - 100)
        action_desc = f"{fac['name']} 위치를 상단(북쪽)으로 이동했습니다."
    elif "남쪽" in prompt_clean or "아래" in prompt_clean:
        fac["y"] = min(630, fac["y"] + 100)
        action_desc = f"{fac['name']} 위치를 하단(남쪽)으로 이동했습니다."
    elif "동쪽" in prompt_clean or "오른쪽" in prompt_clean:
        fac["x"] = min(880, fac["x"] + 120)
        action_desc = f"{fac['name']} 위치를 우측(동쪽)으로 이동했습니다."
    elif "서쪽" in prompt_clean or "왼쪽" in prompt_clean:
        fac["x"] = max(120, fac["x"] - 120)
        action_desc = f"{fac['name']} 위치를 좌측(서쪽)으로 이동했습니다."
    elif "의료" in prompt_clean or "병원" in prompt_clean or "가까이" in prompt_clean or "근처" in prompt_clean:
        fac["x"] = facs["medical"]["x"] - 30
        fac["y"] = facs["medical"]["y"] + 120
        action_desc = f"{fac['name']}을(를) 응급의료센터 인근의 접근성이 우수한 위치로 조정했습니다."
    elif "초기화" in prompt_clean or "원래" in prompt_clean or "복원" in prompt_clean:
        fac["x"] = DEFAULT_FACILITIES[target_key]["x"]
        fac["y"] = DEFAULT_FACILITIES[target_key]["y"]
        fac["reason"] = DEFAULT_FACILITIES[target_key]["reason"]
        st.session_state['selected_facility'] = target_key
        return f"복원 완료: {fac['name']}을(를) 초기 권장 공간으로 복구했습니다."
    else:
        fac["x"] = (fac["x"] + 80) % 800 + 100
        action_desc = f"{fac['name']}의 최적 좌표를 AI 알고리즘으로 재계산했습니다."

    fac["reason"] = f"AI 사용자 대화 반영: {action_desc}"
    st.session_state['selected_facility'] = target_key
    return f"✅ **조정 완료:** {action_desc}"

with st.sidebar:
    if st.button("🎪 이벤트 아키텍트 AI", key="logo_btn", use_container_width=True, type="primary"):
        st.session_state['page'] = 'home'
        st.rerun()

    st.caption("AI 기반 행사 공간 자동 설계 플랫폼")
    st.divider()

    page_selection = st.radio(
        "메뉴 이동",
        ["🏠 홈 화면", "📊 AI 행사 설계 대시보드", "📄 AI 결재 보고서", "⚙️ 시스템 설정"],
        index=["home", "dashboard", "report", "settings"].index(st.session_state['page'])
    )

    if page_selection == "🏠 홈 화면":
        st.session_state['page'] = 'home'
    elif page_selection == "📊 AI 행사 설계 대시보드":
        st.session_state['page'] = 'dashboard'
    elif page_selection == "📄 AI 결재 보고서":
        st.session_state['page'] = 'report'
    elif page_selection == "⚙️ 시스템 설정":
        st.session_state['page'] = 'settings'

    st.divider()

    if st.session_state['logged_in']:
        st.markdown(f"👤 **{st.session_state['username']}** 님 (기획 총괄)")
        if st.button("로그아웃", key="sidebar_logout", use_container_width=True):
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
                if st.button("설정 관리", key="pop_settings"):
                    st.session_state['page'] = 'settings'
                    st.rerun()
                if st.button("로그아웃", key="pop_logout"):
                    st.session_state['logged_in'] = False
                    st.rerun()
        else:
            with st.popover("🔑 로그인"):
                u_in = st.text_input("아이디", value="주은님")
                p_in = st.text_input("비밀번호", type="password")
                if st.button("로그인 실행"):
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
    st.caption("카드나 하단 버튼을 클릭하면 해당 작업 스튜디오로 이동합니다.")
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
            min-height: 270px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <h1 style="font-size: 3rem; margin: 0 0 12px 0;">📊</h1>
            <h2 style="color: #1E3A8A; margin: 0 0 14px 0; font-size: 1.55rem;">AI 스마트 공간 설계 대시보드</h2>
            <p style="color: #475569; font-size: 1.02rem; line-height: 1.65; margin: 0;">
                이벤트 목적과 예산을 입력하면 실시간 입체 디지털 트윈 조감도를 생성합니다.<br>
                AI 챗봇 대화를 통해 행사장의 무대, 부스, 푸드존 배치를 실시간으로 자율 편집하세요.
            </p>
        </div>
        """
        st.markdown(dash_card_html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📊 AI 행사 설계 대시보드 시작하기", key="btn_click_dash", type="primary", use_container_width=True):
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
            min-height: 270px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        ">
            <h1 style="font-size: 3rem; margin: 0 0 12px 0;">📄</h1>
            <h2 style="color: #065F46; margin: 0 0 14px 0; font-size: 1.55rem;">AI 결재용 기안 보고서 생성기</h2>
            <p style="color: #475569; font-size: 1.02rem; line-height: 1.65; margin: 0;">
                설계된 행사장 배치안을 기반으로 직장 상사에게 즉시 제출 가능한 보고서를 자동 생성합니다.<br>
                공간 안전성, 동선 효율성 및 AI 개선 검토 내역을 결재 보고서로 인쇄하세요.
            </p>
        </div>
        """
        st.markdown(rep_card_html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📄 AI 결재 보고서 확인하기", key="btn_click_rep", type="secondary", use_container_width=True):
            st.session_state['page'] = 'report'
            st.rerun()

elif st.session_state['page'] == 'dashboard':
    st.markdown("## 📊 AI 디지털 트윈 공간 설계 대시보드")
    st.caption("🏞️ 현장 조감도 기반 입체 디지털 트윈으로 공간 배치와 동선을 실시간 제어합니다.")

    with st.expander("📌 행사 기본 정보 및 조건 설정", expanded=not st.session_state['digital_twin_generated']):
        with st.form("event_input_form"):
            ic1, ic2, ic3 = st.columns(3)
            with ic1:
                st.session_state['event_name'] = st.text_input("행사명", value=st.session_state['event_name'])
                st.selectbox("이벤트 목적", ["축제/공연", "박람회/전시", "지역 문화 행사", "기업 이벤트"])
            with ic2:
                st.session_state['expected_visitors'] = st.number_input("예상 관람객 (명)", value=st.session_state['expected_visitors'], step=500)
                st.session_state['budget'] = st.text_input("예산", value=st.session_state['budget'])
            with ic3:
                st.session_state['location'] = st.text_input("장소", value=st.session_state['location'])
                st.text_input("진행 시간", "5시간")

            btn_gen = st.form_submit_button("✨ AI 최적 공간 배치 재계산", type="primary", use_container_width=True)
            if btn_gen:
                st.session_state['digital_twin_generated'] = True
                st.session_state['facilities'] = {k: v.copy() for k, v in DEFAULT_FACILITIES.items()}
                st.toast("AI가 조건에 맞는 최적 디지털 트윈 배치를 생성했습니다!")

    st.markdown(f"""
        <div style="background-color: #FFFFFF; padding: 12px 20px; border-radius: 12px; border: 1px solid #CBD5E1; margin-bottom: 15px; display: flex; justify-content: space-between; font-size:0.92rem; flex-wrap: wrap; gap: 8px;">
            <span>🎪 <b>행사명:</b> {st.session_state['event_name']}</span>
            <span>🎯 <b>목적:</b> 축제/공연</span>
            <span>👥 <b>예상 인원:</b> {st.session_state['expected_visitors']:,}명</span>
            <span>💰 <b>예산:</b> {st.session_state['budget']}</span>
            <span>📍 <b>장소:</b> {st.session_state['location']}</span>
        </div>
    """, unsafe_allow_html=True)

    col_main_left, col_main_right = st.columns([2.3, 1])

    with col_main_left:
        st.markdown("### 🗺️ 2D digital Twin 공간 도면")
        
        fig = go.Figure()

        # 외곽 공원 경계
        fig.add_shape(type="rect", x0=40, y0=40, x1=960, y1=720,
                      fillcolor="#F1F5F9", line=dict(color="#94A3B8", width=3, dash="dash"))

        # 중앙 잔디 광장
        fig.add_shape(type="rect", x0=320, y0=240, x1=680, y1=500,
                      fillcolor="#DCFCE7", opacity=0.6, line=dict(color="#16A34A", width=2))
        
        # 도로 / 주 동선 가이드
        fig.add_shape(type="path",
                      path="M 500,720 L 500,570 L 220,570 L 220,180 L 500,180 L 820,180 L 820,570 L 500,570",
                      line=dict(color="#93C5FD", width=14))

        # 시설물 그리기
        for f_key, f_data in st.session_state['facilities'].items():
            is_selected = (st.session_state['selected_facility'] == f_key)
            line_w = 4 if is_selected else 2
            line_color = "#F59E0B" if is_selected else f_data["hex"]

            fig.add_shape(
                type="rect",
                x0=f_data["x"] - f_data["w"]/2,
                y0=f_data["y"] - f_data["h"]/2,
                x1=f_data["x"] + f_data["w"]/2,
                y1=f_data["y"] + f_data["h"]/2,
                fillcolor=f_data["hex"],
                opacity=0.88,
                line=dict(color=line_color, width=line_w)
            )

        # 시설물 레이블 및 마커
        f_x, f_y, f_labels, f_keys = [], [], [], []
        for f_key, f_data in st.session_state['facilities'].items():
            f_x.append(f_data["x"])
            f_y.append(f_data["y"])
            prefix = "📍 " if st.session_state['selected_facility'] == f_key else ""
            f_labels.append(f"{prefix}{f_data['icon']} {f_data['name']}")
            f_keys.append(f_key)

        fig.add_trace(go.Scatter(
            x=f_x, y=f_y,
            mode="markers+text",
            text=f_labels,
            textposition="top center",
            textfont=dict(size=13, color="#0F172A", family="Pretendard"),
            customdata=f_keys,
            marker=dict(size=18, color="#2563EB", line=dict(color="#FFFFFF", width=2)),
            showlegend=False
        ))

        fig.update_layout(
            xaxis=dict(range=[0, 1000], showgrid=True, gridcolor="#E2E8F0", zeroline=False),
            yaxis=dict(range=[760, 0], showgrid=True, gridcolor="#E2E8F0", zeroline=False),
            height=520,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FAFAFA",
            clickmode="event+select"
        )

        map_event = st.plotly_chart(fig, use_container_width=True, on_select="rerun", selection_mode="points", key="main_map")

        if map_event and "selection" in map_event and map_event["selection"]["points"]:
            pts = map_event["selection"]["points"]
            if len(pts) > 0 and "customdata" in pts[0]:
                sel_k = pts[0]["customdata"]
                if sel_k in st.session_state['facilities'] and sel_k != st.session_state['selected_facility']:
                    st.session_state['selected_facility'] = sel_k
                    st.rerun()

        st.markdown("**👇 아래 시설을 클릭하여 상세 정보와 최적 배치 근거를 확인하세요:**")
        f_cols = st.columns(4)
        fac_items = list(st.session_state['facilities'].items())
        for idx, (f_k, f_v) in enumerate(fac_items):
            with f_cols[idx % 4]:
                btn_type = "primary" if st.session_state['selected_facility'] == f_k else "secondary"
                if st.button(f"{f_v['icon']} {f_v['name']}", key=f"btn_fac_sel_{f_k}", type=btn_type, use_container_width=True):
                    st.session_state['selected_facility'] = f_k
                    st.rerun()

    with col_main_right:
        selected_key = st.session_state['selected_facility']
        current_fac = st.session_state['facilities'][selected_key]

        st.markdown("### 💡 선택 시설 및 AI 근거")
        st.markdown(f"""
        <div class="custom-card" style="border-left: 5px solid {current_fac['hex']}; padding: 18px;">
            <h4 style="margin: 0 0 8px 0; color: #0F172A;">{current_fac['icon']} {current_fac['name']}</h4>
            <p style="font-size: 13px; color: #64748B; margin-bottom: 6px;"><b>중심 좌표:</b> (X: {current_fac['x']}, Y: {current_fac['y']})</p>
            <p style="font-size: 13px; color: #64748B; margin-bottom: 6px;"><b>크기:</b> {current_fac['w']}m x {current_fac['h']}m</p>
            <div class="reason-box">
                💡 <b>AI 최적 배치 근거:</b><br>{current_fac['reason']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        st.markdown("### 🔥 AI 군중 밀집도 시뮬레이션")
        if st.button("🚨 혼잡도 시뮬레이션 실행", type="primary", use_container_width=True):
            st.session_state['simulated'] = True

        if st.session_state['simulated']:
            st.caption("구역별 인파 밀집도 예측 (붉은색: 정체 위험 구역)")
            np.random.seed(42)
            sim_grid = np.random.rand(10, 10) * 40
            sim_grid[1, 5] += 50  # 무대 앞 혼잡
            sim_grid[5, 2] += 35  # 푸드존 앞 혼잡
            sim_fig = px.imshow(sim_grid, color_continuous_scale='YlOrRd', labels=dict(color="혼잡도"))
            sim_fig.update_layout(margin=dict(l=5, r=5, t=5, b=5), height=180)
            st.plotly_chart(sim_fig, use_container_width=True)

        st.divider()

        st.markdown("### 💬 AI 설계 어시스턴트")
        chat_box = st.container(height=200)
        with chat_box:
            for message in st.session_state['chat_messages']:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

        if user_prompt := st.chat_input("예: '푸드존을 외곽으로 이동해줘'"):
            st.session_state['chat_messages'].append({"role": "user", "content": user_prompt})
            ai_reply = parse_and_apply_ai_command(user_prompt)
            st.session_state['chat_messages'].append({"role": "assistant", "content": ai_reply})
            st.rerun()

elif st.session_state['page'] == 'report':
    st.markdown("## 📄 AI 결재용 보고서 생성기")
    st.caption("대시보드에서 설계된 시설물 배치 수치와 AI 검토 결과가 공식 기안서 문서 양식으로 표시됩니다.")

    facs = st.session_state['facilities']

    st.markdown(f"""
    <div style="background:#FFFFFF; border:1px solid #CBD5E1; border-radius:12px; padding:32px; max-width:850px; margin:0 auto; color:#0F172A; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
        <div style="display:flex; justify-content:space-between; border-bottom:2px solid #0F172A; padding-bottom:12px; margin-bottom:20px;">
            <div>
                <h2 style="margin:0; font-size: 1.5rem;">[결재 기안서] 행사 공간 배치 타당성 검토서</h2>
                <span style="font-size:12px; color:#64748B;">시스템: Event Architect AI v4.2</span>
            </div>
            <div style="font-size:12px; color:#64748B; text-align:right; line-height:1.5;">
                <b>문서번호:</b> EA-2026-0913<br>
                <b>기안일자:</b> 2026. 09. 13<br>
                <b>기안자:</b> {st.session_state['username']} (총괄)
            </div>
        </div>

        <p style="font-size:15px; font-weight:bold; margin-bottom:8px;">1. 행사 기본 개요</p>
        <table style="width:100%; border-collapse:collapse; margin-bottom:24px; font-size:13px;">
            <tr>
                <td style="padding:8px 12px; border:1px solid #E2E8F0; background:#F8FAFC; width:20%;"><b>행사명</b></td>
                <td style="padding:8px 12px; border:1px solid #E2E8F0; width:30%;">{st.session_state['event_name']}</td>
                <td style="padding:8px 12px; border:1px solid #E2E8F0; background:#F8FAFC; width:20%;"><b>예상 관람객</b></td>
                <td style="padding:8px 12px; border:1px solid #E2E8F0; width:30%;">{st.session_state['expected_visitors']:,} 명</td>
            </tr>
            <tr>
                <td style="padding:8px 12px; border:1px solid #E2E8F0; background:#F8FAFC;"><b>소요 예산</b></td>
                <td style="padding:8px 12px; border:1px solid #E2E8F0;">{st.session_state['budget']}</td>
                <td style="padding:8px 12px; border:1px solid #E2E8F0; background:#F8FAFC;"><b>행사 장소</b></td>
                <td style="padding:8px 12px; border:1px solid #E2E8F0;">{st.session_state['location']}</td>
            </tr>
        </table>

        <p style="font-size:15px; font-weight:bold; margin-bottom:8px;">2. AI 실시간 공간 안전 및 동선 평가 결과</p>
        <table style="width:100%; border-collapse:collapse; margin-bottom:24px; font-size:13px;">
            <thead>
                <tr style="background:#F1F5F9; text-align:left;">
                    <th style="padding:8px 12px; border:1px solid #CBD5E1;">평가 항목</th>
                    <th style="padding:8px 12px; border:1px solid #CBD5E1;">점수</th>
                    <th style="padding:8px 12px; border:1px solid #CBD5E1;">등급</th>
                    <th style="padding:8px 12px; border:1px solid #CBD5E1;">상세 검토 및 종합 평가</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="padding:8px 12px; border:1px solid #E2E8F0;">비상 피난 및 의료 안전성</td>
                    <td style="padding:8px 12px; border:1px solid #E2E8F0;"><b>95점</b></td>
                    <td style="padding:8px 12px; border:1px solid #E2E8F0;"><span class="badge badge-excellent">매우 우수</span></td>
                    <td style="padding:8px 12px; border:1px solid #E2E8F0;">응급의료센터({facs['medical']['x']}, {facs['medical']['y']})가 비상 도로와 연계되어 구급차 최단 경로 확보.</td>
                </tr>
                <tr>
                    <td style="padding:8px 12px; border:1px solid #E2E8F0;">소음 및 연기 동선 분리성</td>
                    <td style="padding:8px 12px; border:1px solid #E2E8F0;"><b>92점</b></td>
                    <td style="padding:8px 12px; border:1px solid #E2E8F0;"><span class="badge badge-excellent">매우 우수</span></td>
                    <td style="padding:8px 12px; border:1px solid #E2E8F0;">푸드존({facs['food']['x']}, {facs['food']['y']}) 독립 배치로 무대 관람 구역으로의 조리 연기 진입 차단.</td>
                </tr>
                <tr>
                    <td style="padding:8px 12px; border:1px solid #E2E8F0;">관람객 편의 및 서비스 접근성</td>
                    <td style="padding:8px 12px; border:1px solid #E2E8F0;"><b>88점</b></td>
                    <td style="padding:8px 12px; border:1px solid #E2E8F0;"><span class="badge badge-good">우수</span></td>
                    <td style="padding:8px 12px; border:1px solid #E2E8F0;">화장실 및 안내센터가 주요 동선 주변에 균형 있게 위치함.</td>
                </tr>
            </tbody>
        </table>

        <p style="font-size:15px; font-weight:bold; margin-bottom:8px;">3. AI 시설물 배치 근거 요약</p>
        <ul style="font-size:13px; line-height:1.7; color:#334155; margin-bottom:24px; padding-left:20px;">
            <li><b>{facs['stage']['name']}:</b> {facs['stage']['reason']}</li>
            <li><b>{facs['food']['name']}:</b> {facs['food']['reason']}</li>
            <li><b>{facs['medical']['name']}:</b> {facs['medical']['reason']}</li>
            <li><b>{facs['toilet']['name']}:</b> {facs['toilet']['reason']}</li>
        </ul>

        <div style="background-color: #F0F9FF; padding: 14px 18px; border-radius: 8px; border: 1px solid #BAE6FD; font-size: 13px; color: #0369A1;">
            💡 <b>기안 의견:</b> 본 설계안은 AI 최적 공간 시뮬레이션을 통과하였으며, 안전사고 예방과 관람객 편의를 모두 만족하므로 원안대로 상신합니다.
        </div>

        <div style="margin-top:36px; text-align:center; font-size:13px; color:#64748B;">
            위와 같이 AI 기반 행사 공간 배치 타당성을 상신하오니 검토 후 결재하여 주시기 바랍니다.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        rep_text_content = f"행사명: {st.session_state['event_name']}\n예상인원: {st.session_state['expected_visitors']}명\n예산: {st.session_state['budget']}\n장소: {st.session_state['location']}\n"
        st.download_button("📥 보고서 텍스트 파일 다운로드 (.txt)", data=rep_text_content, file_name="event_ai_report.txt", type="primary", use_container_width=True)
    with c_btn2:
        if st.button("🔄 최신 AI 배치 수치로 보고서 갱신", use_container_width=True):
            st.toast("대시보드의 시설 위치 정보가 성공적으로 업데이트되었습니다!")

elif st.session_state['page'] == 'settings':
    st.markdown("## ⚙️ 시스템 설정 및 관리")

    with st.container():
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("👤 계정 및 사용자 프로필")
        st.session_state['username'] = st.text_input("사용자 이름", value=st.session_state['username'])
        st.text_input("소속 부서 / 조직", value="이벤트 기획 1팀")
        st.text_input("이메일 주소", value="user@event-architect.ai")
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("🖥️ AI 디지털 트윈 엔진 옵션")
        st.toggle("도면 내 레이블 및 좌표 가이드 표시", value=True)
        st.toggle("AI 챗봇 명령 후 실시간 Rerun 실행", value=True)
        st.selectbox("AI 추론 모델 선택", ["EventArchitect-v4.2 (최신/권장)", "EventArchitect-Lite"])
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("로그아웃", type="primary"):
        st.session_state['logged_in'] = False
        st.session_state['page'] = 'home'
        st.rerun()
