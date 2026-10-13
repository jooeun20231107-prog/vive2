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
    # [수정 완료] min_p -> min_value로 수정
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
    col1, col2 = st.columns([2, 1])

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
            booths = [b.strip() for b in custom_booths.split(",")]
            for b in booths:
                st.markdown(f"- ✅ `{b}` 자동 최적 배치 완료")
        else:
            st.markdown("- ℹ️ 기본 추천 부스가 적용되었습니다.")

with tab2:
    st.markdown("### 🔄 AI 행사 설계 프로세스 (Workflow)")
    st.markdown(
        "행사 기획부터 최종 설계안이 도출되기까지의 전체 자동화 파이프라인입니다."
    )

    workflow_steps = [
        {
            "단계": "1단계: 정보 입력 및 분석",
            "설명": "운영자가 입력한 예산, 목적, 방문객 수 및 맞춤형 부스 요구사항을 자연어 처리(NLP) 및 규칙 기반 엔진으로 분석합니다.",
        },
        {
            "단계": "2단계: 디지털 트윈 환경 생성",
            "설명": "선택된 장소의 지형 데이터를 바탕으로 3D 가상 공간(디지털 트윈)을 구축합니다.",
        },
        {
            "단계": "3단계: 수천 개 배치안 자동 생성",
            "설명": "강화학습 알고리즘을 통해 안전 거리, 접근성, 공간 효율성을 고려한 수천 가지의 대안 배치를 시뮬레이션합니다.",
        },
        {
            "단계": "4단계: 군중 동선 및 다목적 최적화",
            "설명": "군중 이동 시뮬레이션을 돌려 병목 현상을 예측하고, 안전성과 편의성을 동시에 만족하는 최적안을 도출합니다.",
        },
        {
            "단계": "5단계: XAI 설명 및 최종 리포트 제공",
            "설명": "AI가 왜 이러한 배치를 선택했는지 이유를 설명(XAI)하고, 전·후 비교 분석 결과와 함께 최종 리포트를 제공합니다.",
        },
    ]

    for step in workflow_steps:
        with st.container():
            st.markdown(
                f"""
                <div class="card">
                    <h4>{step["단계"]}</h4>
                    <p>{step["설명"]}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

with tab3:
    st.markdown("### 📊 분석 리포트 및 설명 가능한 AI (XAI) 결과")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### 🧠 XAI (설명 가능한 AI) 설계 이유")
        st.markdown(
            """
        - **응급 의료 센터 위치 선정**: 출입구 및 메인 무대에서 반경 30m 이내에 배치하여 응급 상황 시 **골든타임(3분 이내)** 확보.
        - **푸드존과 휴게공간 분산**: 흡연 및 취식으로 인한 밀집도를 낮추기 위해 메인 공연장과 대각선 방향으로 이격 배치.
        - **군중 동선 최적화**: 방문객 이동 동선이 겹치지 않도록 일방통행 형태의 보행자 로드 설계 반영.
        """
        )

    with col_b:
        st.markdown("#### 📈 설계 전·후 비교 분석")
        comparison_data = {
            "평가지표": ["평균 대기 시간", "비상 탈출 소요 시간", "공간 활용률", "안전사고 위험도"],
            "기존 수동 설계": ["25분", "8분 30초", "65%", "주의 (중간)"],
            "AI 최적화 설계": ["10분", "4분 15초", "92%", "안전 (낮음)"],
        }
        df_comp = pd.DataFrame(comparison_data)
        st.table(df_comp)

    st.markdown("---")
    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        if st.button("📥 최종 설계안 다운로드 (PDF)"):
            st.success("설계 리포트
