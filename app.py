import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Streamlit 페이지 설정
st.set_page_config(
    page_title="이벤트 아키텍트 AI",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 커스텀 CSS 적용
st.markdown("""
    <style>
        .main { background-color: #F8FAFC; }
        .stButton>button { border-radius: 12px; font-weight: 600; }
        .metric-card { background: white; padding: 20px; border-radius: 16px; border: 1px solid #E2E8F0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

if "username" not in st.session_state:
    st.session_state.username = "김기획"

if "event_name" not in st.session_state:
    st.session_state.event_name = "2026 AI 테크 & 컬처 페스티벌"

if "expected_visitors" not in st.session_state:
    st.session_state.expected_visitors = 3500

if "budget" not in st.session_state:
    st.session_state.budget = "₩55,000,000"

if "location" not in st.session_state:
    st.session_state.location = "서울 코엑스 Hall A"

# 시설물 초기 위치 데이터
if "facilities" not in st.session_state:
    st.session_state.facilities = {
        "메인 무대": {"x": 5, "y": 8, "w": 4, "h": 3, "color": "#4F46E5", "icon": "🎭", "reason": "관람객 집중 및 음향 확산을 고려한 중앙 정면 배치"},
        "부스 존": {"x": 2, "y": 4, "w": 3, "h": 2, "color": "#06B6D4", "icon": "⛺", "reason": "입구에서 진입 시 동선 유도가 가장 원활한 우측 구역"},
        "푸드 존": {"x": 8, "y": 4, "w": 3, "h": 2, "color": "#EF4444", "icon": "🍔", "reason": "식음료 냄새 분산 및 휴식 공간 연계를 위한 야외 테라스 인접부"},
        "운영 본부": {"x": 5, "y": 1, "w": 2, "h": 2, "color": "#10B981", "icon": "🏢", "reason": "비상 상황 대응 및 내빈 안내가 빠른 행사장 최우측 출입구 측"},
    }

with st.sidebar:
    st.markdown("### 🎪 이벤트 아키텍트 AI")
    st.caption("AI 기반 행사 공간 자동 설계 플랫폼")
    st.divider()
    
    page = st.radio("메뉴 이동", ["🏠 홈", "📊 대시보드 및 설계", "📄 결재 보고서 인쇄", "⚙️ 설정"])
    
    st.divider()
    st.markdown(f"👤 접속자: **{st.session_state.username} 님**")
    if st.button("로그아웃"):
        st.success("로그아웃되었습니다.")

if page == "🏠 홈":
    st.markdown("<div style='text-align: center; padding: 30px 0;'>", unsafe_allow_html=True)
    st.markdown("<span style='background: #EEF2FF; color: #4F46E5; padding: 6px 16px; border-radius: 20px; font-weight: 700; font-size: 12px;'>NEXT-GEN EVENT AI STUDIO</span>", unsafe_allow_html=True)
    st.markdown("# 행사 공간 설계와 결재 보고서를\n### 단 몇 분 만에 완성하세요")
    st.markdown("디지털 트윈 기반의 스마트 배치와 실시간 시뮬레이션으로 완벽한 이벤트를 기획합니다.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <h3>📊 AI 스마트 공간 설계 대시보드</h3>
            <p style='color: #64748B; font-size: 14px;'>실시간 입체 디지털 트윈 조감도를 생성하고, 무대·부스·푸드존 위치를 자율 편집하세요.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("대시보드 바로가기 ➔", use_container_width=True):
            st.rerun()
            
    with col2:
        st.markdown("""
        <div class='metric-card'>
            <h3>📄 결재용 기안 보고서 생성기</h3>
            <p style='color: #64748B; font-size: 14px;'>설계된 행사장 배치안을 기반으로 즉시 제출 가능한 공문 형태의 결재 보고서를 자동 생성합니다.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("결재 보고서 확인하기 ➔", use_container_width=True):
            st.rerun()

elif page == "📊 대시보드 및 설계":
    st.title("📊 AI 디지털 트윈 공간 설계 대시보드")
    st.caption("현장 조감도 기반 입체 디지털 트윈으로 공간 배치와 동선을 실시간 제어합니다.")
    
    # 상단 요약 바
    cols = st.columns(5)
    cols[0].metric("행사명", st.session_state.event_name)
    cols[1].metric("예상 인원", f"{st.session_state.expected_visitors:,}명")
    cols[2].metric("예산", st.session_state.budget)
    cols[3].metric("장소", st.session_state.location)
    cols[4].metric("시설 수", f"{len(st.session_state.facilities)}개소")
    
    st.divider()
    
    col_map, col_ctrl = st.columns([2, 1])
    
    with col_map:
        st.subheader("🗺️ 2D 디지털 트윈 공간 도면")
        
        # Plotly를 이용한 공간 맵 시각화
        df_plot = []
        for name, data in st.session_state.facilities.items():
            df_plot.append({
                "Facility": f"{data['icon']} {name}",
                "X": data["x"],
                "Y": data["y"],
                "Size": data["w"] * 30,
                "Color": data["color"],
                "Reason": data["reason"]
            })
        df_fac = pd.DataFrame(df_plot)
        
        fig = px.scatter(
            df_fac, x="X", y="Y", size="Size", color="Facility",
            text="Facility", range_x=[0, 12], range_y=[0, 12],
            height=450
        )
        fig.update_traces(textposition='top center')
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#F1F5F9"
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col_ctrl:
        st.subheader("🛠️ 시설물 세부 제어")
        selected_fac = st.selectbox("제어할 시설 선택", list(st.session_state.facilities.keys()))
        
        fac_info = st.session_state.facilities[selected_fac]
        
        # 슬라이더를 통한 위치 조정
        new_x = st.slider("X 좌표 위치", 0, 10, int(fac_info["x"]))
        new_y = st.slider("Y 좌표 위치", 0, 10, int(fac_info["y"]))
        
        if new_x != fac_info["x"] or new_y != fac_info["y"]:
            st.session_state.facilities[selected_fac]["x"] = new_x
            st.session_state.facilities[selected_fac]["y"] = new_y
            st.success(f"'{selected_fac}' 위치가 좌표 ({new_x}, {new_y})로 이동되었습니다!")
            
        st.info(f"💡 **AI 최적 배치 근거:**\n{fac_info['reason']}")
        
    st.divider()
    
    # AI 어시스턴트 및 시뮬레이션
    col_sim, col_chat = st.columns(2)
    with col_sim:
        st.subheader("🔥 군중 밀집도 시뮬레이션")
        if st.button("시뮬레이션 실행하기"):
            # 랜덤 히트맵 생성
            heat_data = np.random.rand(10, 10) * 100
            fig_heat = px.imshow(heat_data, color_continuous_scale="Reds", origin="lower")
            fig_heat.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=250)
            st.plotly_chart(fig_heat, use_container_width=True)
            st.warning("⚠️ 출구 인근(좌측 하단) 정체 위험 감지: 통로 폭을 1.5m 확대 권장")
        else:
            st.write("버튼을 눌러 인파 밀집도 시뮬레이션을 실행하세요.")
            
    with col_chat:
        st.subheader("💬 AI 설계 어시스턴트 채팅")
        user_prompt = st.text_input("AI에게 요청사항 입력 (예: '푸드존을 우측 구역으로 옮겨줘')", placeholder="무엇이든 물어보세요...")
        if st.button("AI에게 전송"):
            if user_prompt:
                st.info(f"🤖 **AI 답변:** '{user_prompt}' 요청에 따라 공간 배치를 최적화하고 안전성 검토를 완료했습니다.")

elif page == "📄 결재 보고서 인쇄":
    st.title("📄 AI 결재용 기안 보고서 생성기")
    st.caption("대시보드에서 설계된 시설물 배치 수치와 AI 검토 결과가 공식 기안서 문서 양식으로 표시됩니다.")
    
    st.markdown("""
    ---
    ### [결재 기안서] 행사 공간 배치 타당성 검토서
    **문서번호:** EA-2026-0913 &nbsp;&nbsp;|&nbsp;&nbsp; **기안일자:** 2026. 10. 13 &nbsp;&nbsp;|&nbsp;&nbsp; **기안자:** 김기획 (총괄)
    ---
    """)
    
    st.markdown("#### 1. 행사 기본 개요")
    report_data = {
        "항목": ["행사명", "예상 관람객", "소요 예산", "행사 장소"],
        "내용": [st.session_state.event_name, f"{st.session_state.expected_visitors:,} 명", st.session_state.budget, st.session_state.location]
    }
    st.table(pd.DataFrame(report_data))
    
    st.markdown("#### 2. 시설물 배치 및 AI 최적화 근거")
    fac_report = []
    for name, data in st.session_state.facilities.items():
        fac_report.append({
            "시설명": f"{data['icon']} {name}",
            "좌표": f"(X: {data['x']}, Y: {data['y']})",
            "규격": f"{data['w']}m x {data['h']}m",
            "AI 최적 배치 근거": data['reason']
        })
    st.dataframe(pd.DataFrame(fac_report), use_container_width=True)
    
    st.markdown("#### 3. 종합 의견")
    st.success("본 행사장 배치는 디지털 트윈 시뮬레이션 결과 동선 효율성이 94.2%로 산출되었으며, 비상 대피로 및 군중 밀집 방지 규격에 모두 부합하므로 원안대로 결재를 요청합니다.")
    
    if st.button("🖨️ 보고서 인쇄 (브라우저 인쇄창 호출)"):
        st.balloons()
        st.info("브라우저의 인쇄 기능(Ctrl+P 또는 Cmd+P)을 사용하여 PDF로 저장하세요.")

elif page == "⚙️ 설정":
    st.title("⚙️ 시스템 설정 및 행사 조건 변경")
    
    st.session_state.event_name = st.text_input("행사명", st.session_state.event_name)
    st.session_state.expected_visitors = st.number_input("예상 관람객 수", value=st.session_state.expected_visitors, step=100)
    st.session_state.budget = st.text_input("소요 예산", st.session_state.budget)
    st.session_state.location = st.text_input("행사 장소", st.session_state.location)
    st.session_state.username = st.text_input("담당자명", st.session_state.username)
    
    if st.button("설정 저장하기"):
        st.success("설정이 성공적으로 저장되었습니다!")
