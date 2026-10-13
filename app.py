import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="이벤트 온 (Event-On) - AI 행사 자동 설계 플랫폼",
    page_icon="🎪",
    layout="wide",
)

# 커스텀 CSS 적용
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #64748B;
        margin-bottom: 20px;
    }
    .card {
        padding: 20px;
        border-radius: 10px;
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 헤더 영역
st.markdown(
    '<p class="main-title">🎪 이벤트 온 (Event-On)</p>', unsafe_allow_html=True
)
st.markdown(
    '<p class="sub-title">디지털 트윈 및 AI 멀티오브젝티브 최적화 기반 행사 자동 설계 플랫폼</p>',
    unsafe_allow_html=True,
)

# ----------------------------------------------------
# 1. 사이드바: 사용자 입력 정보
# ----------------------------------------------------
st.sidebar.header("🎯 행사 기획 조건 설정")

with st.sidebar.form("event_form"):
    event_name = st.text_input("행사명", "2026 서울 스마트 시티 페스티벌")
    event_purpose = st.selectbox(
        "행사 목적",
        ["문화 예술 공연", "기술 전시 및 박람회", "지역 축제", "기업 행사"],
    )
    budget = st.slider(
        "예산 (원)",
        min_value=10000000,
        max_value=500000000,
        value=150000000,
        step=10000000,
        format="%d원",
    )
    expected_visitors = st.number_input(
        "예상 방문객 수 (명)", min_value=500, max_value=50000, value=5000, step=500
    )
    location = st.text_input("행사 장소", "여의도 한강공원 이벤트광장")
    atmosphere = st.selectbox(
        "원하는 분위기", ["활기찬/역동적인", "차분한/힐링되는", "전문적인/세련된"]
    )
    target_age = st.multiselect(
        "예상 연령대", ["10대", "20대", "30대", "40대", "50대 이상"], default=["20대", "30대"]
    )

    # 사용자가 추가로 원하는 부스 입력
    custom_booths = st.text_area(
        "원하는 추가 부스 입력 (쉼표로 구분)",
        "친환경 굿즈 팝업스토어, 푸드트럭존, 포토존",
    )

    submit_button = st.form_submit_button(
        label="🚀 AI 최적화 행사장 설계 시작"
    )

# ----------------------------------------------------
# 2. 메인 화면 구성
# ----------------------------------------------------
tab1, tab2, tab3 = st.tabs(
    ["🗺️ 디지털 트윈 배치도", "⚙️ AI 설계 프로세스", "📊 분석 리포트 & XAI"]
)

with tab1:
    st.markdown("### 디지털 트윈 기반 실시간 행사장 배치 및 군중 시뮬레이션")

    if submit_button:
        with st.spinner("🤖 AI가 디지털 트윈 환경을 분석하고 최적의 배치를 계산 중입니다..."):
            time.sleep(1.5)
        st.success("✨ 최적의 행사장 설계가 완료되었습니다!")

    # 레이아웃 분할 (좌측: 배치도 시각화, 우측: 실시간 군중 및 구역 정보)
    col1, col2 = st.column([2, 1])

    with col1:
        # 가상의 행사장 좌표 데이터 생성 (디지털 트윈 배치도)
        data = {
            "구역명": [
                "메인 공연장",
                "푸드존 A",
                "푸드존 B",
                "체험부스 1",
                "체험부스 2",
                "휴게공간",
                "응급의료센터",
                "안내센터",
            ],
            "X좌표": [50, 20, 80, 35, 65, 50, 10, 90],
            "Y좌표": [80, 40, 40, 20, 20, 55, 10, 10],
            "혼잡도": ["보통", "혼잡", "주의", "여유", "여유", "여유", "안전", "안전"],
            "규모 (m²)": [500, 200, 200, 150, 150, 300, 50, 50],
            "유형": [
                "공연장",
                "푸드존",
                "푸드존",
                "체험부스",
                "체험부스",
                "휴게공간",
                "의료",
                "안내",
            ],
        }
        df_zones = pd.DataFrame(data)

        # Plotly를 이용한 시각적 배치도 구현
        fig = px.scatter(
            df_zones,
            x="X좌표",
            y="Y좌표",
            size="규모 (m²)",
            color="유형",
            hover_name="구역명",
            text="구역명",
            size_max=40,
            range_x=[0, 100],
            range_y=[0, 100],
            title="[Digital Twin] 실시간 행사장 공간 배치 및 동선 시뮬레이션",
        )
        fig.update_traces(
            textposition="top center", marker=dict(opacity=0.85, line=dict(width=2, color="DarkSlateGray"))
        )
        fig.update_layout(
            height=500,
            xaxis_title="행사장 가로 축 (m)",
            yaxis_title="행사장 세로 축 (m)",
            legend_title="시설 유형",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 📌 실시간 구역 모니터링")
        st.info(
            "📍 **현재 시뮬레이션 상태**\n- 예상 밀집도: **㎡당 1.8명 (안전)**\n- 병목 현상 예상 구역: **푸드존 A 입구**\n- 추천 조치: *푸드존 대기 라인 분산 배치*"
        )

        st.markdown("#### 🛠️ 입력된 맞춤 부스 반영 결과")
        if custom_booths:
            booths = [b.strip() for b in custom_booths.split(",
