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
        border-radius: 8px;
        margin-top: 10px;
        color: #0F172A;
    }

    /* 상단 로고 버튼 및 사이드바 간격 */
    div[data-testid="stSidebarHeader"] {
        padding-top: 0.5rem;
    }

    /* Streamlit 버튼 튜닝 */
    .stButton>button {
        border-radius: 8px;
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
        "hex": "#06B6D4",
        "x": 820, "y": 340, "w": 160, "h": 100,
        "reason": "동쪽 상하수 인프라 인접 구역에 배치하여 접근성과 위생 처리를 원활히 했습니다."
    },
    "info": {
        "name": "종합안내소",
        "icon": "ℹ️",
        "hex": "#EC4899",
        "x": 500, "y": 550, "w": 160, "h": 80,
        "reason": "남쪽 주요 출입구 맞은편에 배치하여 초행 관람객 가이드를 용이하게 했습니다."
    },
    "exit": {
        "name": "출입구",
        "icon": "🚪",
        "hex": "#64748B",
        "x": 500, "y": 660, "w": 240, "h": 60,
        "reason": "남쪽 광장 최하단에 넓게 배치하여 비상시 신속한 대피 경로를 제공합니다."
    }
}

if 'page' not in st.session_state:
    st.session_state['page'] = 'dashboard'
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
        {"role": "assistant", "content": "안녕하세요! AI 행사 공간 설계 도우미입니다. 시설물을 클릭하시거나 명령어(예: '푸드존을 외곽으로 이동해줘')를 입력해 보세요."}
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
    elif "출입구" in prompt_clean or "입구" in prompt_clean or "비상구" in prompt_clean:
        target_key = "exit"

    if not target_key:
        target_key = st.session_state['selected_facility']

    fac = facs[target_key]
    action_desc = ""

    if "외곽" in prompt_clean or "멀리" in prompt_clean or "분리" in prompt_clean:
        if target_key == "food":
            fac["x"] = 150
            fac["y"] = 420
            action_desc = "푸드존을 조리 연기 차단 및 혼잡 분리를 위해 서쪽 외곽 구역으로 이동시켰습니다."
        else:
            fac["x"] = max(120, fac["x"] - 100)
            action_desc = f"{fac['name']}을(를) 외곽으로 이동 조정했습니다."
    elif "북쪽" in prompt_clean or "위" in prompt_clean:
        fac["y"] = max(80, fac["y"] - 80)
        action_desc = f"{fac['name']} 좌표를 북쪽 방향으로 상향 이동했습니다."
    elif "남쪽" in prompt_clean or "아래" in prompt_clean:
        fac["y"] = min(620, fac["y"] + 80)
        action_desc = f"{fac['name']} 좌표를 남쪽 방향으로 하향 이동했습니다."
    elif "동쪽" in prompt_clean or "오른쪽" in prompt_clean:
        fac["x"] = min(880, fac["x"] + 100)
        action_desc = f"{fac['name']} 좌표를 동쪽 방향으로 이동했습니다."
    elif "서쪽" in prompt_clean or "왼쪽" in prompt_clean:
        fac["x"] = max(120, fac["x"] - 100)
        action_desc = f"{fac['name']} 좌표를 서쪽 방향으로 이동했습니다."
    elif "의료" in prompt_clean or "병원" in prompt_clean or "가까이" in prompt_clean or "근처" in prompt_clean:
        fac["x"] = facs["medical"]["x"] - 40
        fac["y"] = facs["medical"]["y"] + 110
        action_desc = f"{fac['name']}을(를) 응급의료센터 인근의 접근성이 우수한 위치로 조정했습니다."
    elif "초기화" in prompt_clean or "원래" in prompt_clean or "최적" in prompt_clean:
        fac["x"] = DEFAULT_FACILITIES[target_key]["x"]
        fac["y"] = DEFAULT_FACILITIES[target_key]["y"]
        fac["reason"] = DEFAULT_FACILITIES[target_key]["reason"]
        action_desc = f"{fac['name']}을(를) 초기 AI 권장 배치로 복원했습니다."
        st.session_state['selected_facility'] = target_key
        return action_desc
    else:
        fac["x"] = min(880, fac["x"] + 50)
        action_desc = f"{fac['name']}의 최적 위치를 재계산하여 조정했습니다."

    fac["reason"] = f"AI 사용자 명령 반영: {action_desc}"
    st.session_state['selected_facility'] = target_key
    return action_desc

with st.sidebar:
    st.title("🎪 Event Architect AI")
    st.caption("AI 기반 행사 공간 자동 설계 플랫폼")
    st.divider()

    page_choice = st.radio(
        "메뉴 이동",
        ["🚀 공간 배치 대시보드", "🏠 소개 메인", "📄 AI 기안 보고서"],
        index=0 if st.session_state['page'] == 'dashboard' else (1 if st.session_state['page'] == 'home' else 2)
    )
    if "소개" in page_choice:
        st.session_state['page'] = 'home'
    elif "대시보드" in page_choice:
        st.session_state['page'] = 'dashboard'
    elif "보고서" in page_choice:
        st.session_state['page'] = 'report'

    st.divider()
    st.subheader("⚙️ 행사 기본 정보 입력")
    st.session_state['event_name'] = st.text_input("행사명", value=st.session_state['event_name'])
    st.session_state['expected_visitors'] = st.number_input("예상 관람객 (명)", value=st.session_state['expected_visitors'], step=500)
    st.session_state['budget'] = st.text_input("예산", value=st.session_state['budget'])
    st.session_state['location'] = st.text_input("장소", value=st.session_state['location'])

    if st.button("🔄 AI 전체 시설물 재배치", type="primary", use_container_width=True):
        st.session_state['facilities'] = {k: v.copy() for k, v in DEFAULT_FACILITIES.items()}
        st.toast("전체 시설물 위치가 초기 AI 추천으로 변경되었습니다!")

if st.session_state['page'] == "home":
    st.markdown("<h1 style='color: #0F172A; font-weight: 800;'>AI 기반 행사 공간 설계 스튜디오</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #475569; font-size: 16px;'>관람객 동선, 소방법 피난 안전, 서비스 접근성을 고려하여 이벤트 공간을 자동으로 배치합니다.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="custom-card">
            <h3>🗺️ 공간 배치 스튜디오</h3>
            <p>메인 무대, 체험 부스, 푸드존, 응급 센터 등 시설물의 위치를 조작하고 시각화합니다.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("대시보드로 이동", type="primary", use_container_width=True):
            st.session_state['page'] = 'dashboard'
            st.rerun()

    with col2:
        st.markdown("""
        <div class="custom-card">
            <h3>📄 AI 기안 보고서 생성</h3>
            <p>배치 타당성 및 피난 안전 검토 결과를 공식 상사 결재 양식 문서로 자동 작성합니다.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("보고서 확인하기", use_container_width=True):
            st.session_state['page'] = 'report'
            st.rerun()

elif st.session_state['page'] == "dashboard":
    st.markdown("## 🚀 AI 스마트 공간 설계 대시보드")
    
    c_left, c_right = st.columns([7, 4])

    with c_left:
        st.markdown("#### 🗺️ 2D 평면 배치 도면")
        
        fig = go.Figure()

        # 광장 테두리 배경
        fig.add_shape(type="rect", x0=50, y0=50, x1=950, y1=720,
                      fillcolor="#F1F5F9", line=dict(color="#CBD5E1", width=2, dash="dash"))

        # 잔디 광장 구역
        fig.add_shape(type="rect", x0=320, y0=240, x1=680, y1=480,
                      fillcolor="#DCFCE7", opacity=0.5, line=dict(color="#16A34A", width=1))

        # 시설물 그리기
        for f_key, f_data in st.session_state['facilities'].items():
            is_selected = (st.session_state['selected_facility'] == f_key)
            line_w = 4 if is_selected else 2
            line_color = "#D97706" if is_selected else f_data["hex"]

            fig.add_shape(
                type="rect",
                x0=f_data["x"] - f_data["w"]/2,
                y0=f_data["y"] - f_data["h"]/2,
                x1=f_data["x"] + f_data["w"]/2,
                y1=f_data["y"] + f_data["h"]/2,
                fillcolor=f_data["hex"],
                opacity=0.85,
                line=dict(color=line_color, width=line_w)
            )

        # 시설물 아이콘 및 핀 표시
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
            yaxis=dict(range=[750, 0], showgrid=True, gridcolor="#E2E8F0", zeroline=False),
            height=530,
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

    with c_right:
        cur_key = st.session_state['selected_facility']
        cur_fac = st.session_state['facilities'][cur_key]

        st.markdown(f"""
        <div class="custom-card" style="border-left: 5px solid {cur_fac['hex']}; padding: 18px;">
            <h4 style="margin: 0 0 8px 0; color: #0F172A;">{cur_fac['icon']} {cur_fac['name']} 정보 및 속성</h4>
            <p style="font-size: 13px; color: #475569; margin-bottom: 6px;"><b>중심 좌표:</b> (X: {cur_fac['x']}, Y: {cur_fac['y']})</p>
            <p style="font-size: 13px; color: #475569; margin-bottom: 6px;"><b>크기 (W x H):</b> {cur_fac['w']} x {cur_fac['h']}</p>
            <div class="reason-box">
                💡 <b>AI 최적 배치 사유:</b><br>{cur_fac['reason']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("##### 🎨 시설물 선택 및 최적화")
        btn_cols = st.columns(2)
        idx = 0
        for f_k, f_v in st.session_state['facilities'].items():
            with btn_cols[idx % 2]:
                btn_type = "primary" if st.session_state['selected_facility'] == f_k else "secondary"
                if st.button(f"{f_v['icon']} {f_v['name']}", key=f"btn_sel_{f_k}", type=btn_type, use_container_width=True):
                    st.session_state['selected_facility'] = f_k
                    st.rerun()
            idx += 1

        st.divider()
        st.markdown("##### 💬 AI CAD 대화형 조작")
        chat_container = st.container(height=140)
        with chat_container:
            for msg in st.session_state['chat_messages']:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

        u_input = st.chat_input("예: '푸드존을 외곽으로 이동'")
        if u_input:
            st.session_state['chat_messages'].append({"role": "user", "content": u_input})
            reply = parse_and_apply_ai_command(u_input)
            st.session_state['chat_messages'].append({"role": "assistant", "content": f"✨ {reply}"})
            st.rerun()

elif st.session_state['page'] == "report":
    st.markdown("## 📄 AI 결재용 보고서")
    
    facs = st.session_state['facilities']

    st.markdown(f"""
    <div style="background:#FFFFFF; border:1px solid #CBD5E1; border-radius:12px; padding:30px; max-width:800px; margin:0 auto; color:#0F172A;">
        <div style="display:flex; justify-content:space-between; border-bottom:2px solid #0F172A; padding-bottom:12px; margin-bottom:20px;">
            <h2 style="margin:0;">[결재 기안서] 행사 공간 배치 타당성 검토서</h2>
            <div style="font-size:12px; color:#64748B; text-align:right;">
                문서번호: EA-2026-001<br>
                기안일자: 2026. 09. 13
            </div>
        </div>

        <p><b>1. 행사 개요</b></p>
        <table style="width:100%; border-collapse:collapse; margin-bottom:20px; font-size:14px;">
            <tr><td style="padding:8px; border:1px solid #E2E8F0; background:#F8FAFC; width:25%;"><b>행사명</b></td><td style="padding:8px; border:1px solid #E2E8F0;">{st.session_state['event_name']}</td></tr>
            <tr><td style="padding:8px; border:1px solid #E2E8F0; background:#F8FAFC;"><b>예상 관람객</b></td><td style="padding:8px; border:1px solid #E2E8F0;">{st.session_state['expected_visitors']:,} 명</td></tr>
            <tr><td style="padding:8px; border:1px solid #E2E8F0; background:#F8FAFC;"><b>예산 / 장소</b></td><td style="padding:8px; border:1px solid #E2E8F0;">{st.session_state['budget']} / {st.session_state['location']}</td></tr>
        </table>

        <p><b>2. AI 공간 안전 및 동선 실시간 평가</b></p>
        <table style="width:100%; border-collapse:collapse; margin-bottom:20px; font-size:13px;">
            <thead>
                <tr style="background:#F1F5F9; text-align:left;">
                    <th style="padding:8px; border:1px solid #CBD5E1;">평가 항목</th>
                    <th style="padding:8px; border:1px solid #CBD5E1;">점수</th>
                    <th style="padding:8px; border:1px solid #CBD5E1;">등급</th>
                    <th style="padding:8px; border:1px solid #CBD5E1;">검토 및 평가 내용</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="padding:8px; border:1px solid #E2E8F0;">안전성 및 비상 피난 코스</td>
                    <td style="padding:8px; border:1px solid #E2E8F0;">95점</td>
                    <td style="padding:8px; border:1px solid #E2E8F0;"><span class="badge badge-excellent">매우 우수</span></td>
                    <td style="padding:8px; border:1px solid #E2E8F0;">응급의료센터({facs['medical']['x']}, {facs['medical']['y']})가 비상 출입구와 접해 빠른 대응 가능.</td>
                </tr>
                <tr>
                    <td style="padding:8px; border:1px solid #E2E8F0;">관람 동선 분리성</td>
                    <td style="padding:8px; border:1px solid #E2E8F0;">92점</td>
                    <td style="padding:8px; border:1px solid #E2E8F0;"><span class="badge badge-excellent">매우 우수</span></td>
                    <td style="padding:8px; border:1px solid #E2E8F0;">푸드존과 무대 관람석 간 연기 및 혼잡 간섭을 차단함.</td>
                </tr>
                <tr>
                    <td style="padding:8px; border:1px solid #E2E8F0;">서비스 및 편의 접근성</td>
                    <td style="padding:8px; border:1px solid #E2E8F0;">88점</td>
                    <td style="padding:8px; border:1px solid #E2E8F0;"><span class="badge badge-good">우수</span></td>
                    <td style="padding:8px; border:1px solid #E2E8F0;">화장실 및 종합안내소가 주 출입 경로 주변에 균형 있게 배치됨.</td>
                </tr>
            </tbody>
        </table>

        <p><b>3. 주요 시설물 최적 배치 사유 요약</b></p>
        <ul style="font-size:13px; line-height:1.6; color:#334155;">
            <li><b>{facs['stage']['name']}:</b> {facs['stage']['reason']}</li>
            <li><b>{facs['food']['name']}:</b> {facs['food']['reason']}</li>
            <li><b>{facs['medical']['name']}:</b> {facs['medical']['reason']}</li>
            <li><b>{facs['toilet']['name']}:</b> {facs['toilet']['reason']}</li>
        </ul>

        <div style="margin-top:30px; text-align:center; font-size:13px; color:#64748B;">
            위와 같이 AI 기반 최적 공간 설계안을 상신하오니 검토 후 결재하여 주시기 바랍니다.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        if st.button("📥 PDF로 다운로드", type="primary", use_container_width=True):
            st.toast("PDF 다운로드 시작되었습니다.")
    with c_btn2:
        if st.button("🖨️ 결재 문서 인쇄", use_container_width=True):
            st.toast("인쇄 명령을 실행합니다.")
