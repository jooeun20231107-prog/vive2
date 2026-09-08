import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(
    page_title="이벤트 아키텍트 AI",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (첨부 이미지 스타일링 적용)
st.markdown("""
    <style>
    .main {
        background-color: #F8FAFC;
    }
    .stCard {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #F1F5F9;
        border-radius: 8px;
        padding: 10px 15px;
        text-align: center;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 세션 상태 초기화 (로그인 및 화면 전환 관리)
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = True  # 기본 로그인 상태 (테스트용)
if 'username' not in st.session_state:
    st.session_state['username'] = "주은님"
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'
if 'digital_twin_generated' not in st.session_state:
    st.session_state['digital_twin_generated'] = False
if 'simulated' not in st.session_state:
    st.session_state['simulated'] = False
if 'selected_facility' not in st.session_state:
    st.session_state['selected_facility'] = None
if 'chat_messages' not in st.session_state:
    st.session_state['chat_messages'] = []

# 3. 사이드바 및 네비게이션
with st.sidebar:
    # 로고 클릭 시 홈으로 이동
    if st.button("🎪 이벤트 아키텍트 AI", use_container_width=True, type="tertiary"):
        st.session_state['page'] = 'home'
        st.rerun()
    
    st.caption("AI 기반 행사 자동 설계 플랫폼")
    st.divider()

    # 회원가입/로그인 및 상단 사용자 정보
    if st.session_state['logged_in']:
        st.success(f"👤 **{st.session_state['username']}** 로그인 중")
        if st.button("로그아웃", key="logout_btn"):
            st.session_state['logged_in'] = False
            st.rerun()
    else:
        st.warning("로그인이 필요합니다.")
        with st.popover("🔑 로그인 / 회원가입"):
            user_input = st.text_input("아이디", value="주은님")
            pass_input = st.text_input("비밀번호", type="password")
            if st.button("로그인하기"):
                st.session_state['logged_in'] = True
                st.session_state['username'] = user_input
                st.rerun()

    st.divider()
    
    # 메뉴 선택
    menu = st.radio("메뉴", ["홈", "대시보드", "AI 보고서", "설정"], index=["home", "dashboard", "report", "settings"].index(st.session_state['page']))
    if menu == "홈":
        st.session_state['page'] = 'home'
    elif menu == "대시보드":
        st.session_state['page'] = 'dashboard'
    elif menu == "AI 보고서":
        st.session_state['page'] = 'report'
    elif menu == "설정":
        st.session_state['page'] = 'settings'


# -------------------------------------------------------------------
# PAGE 1: 홈 화면
# -------------------------------------------------------------------
if st.session_state['page'] == 'home':
    st.title("🎪 이벤트 아키텍트 AI")
    st.subheader("AI로 안전하고 효율적인 최적의 행사장 공간을 자동 설계하세요.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 AI 기반 행사 자동 설계 대시보드")
        st.write("이벤트 정보를 입력하여 디지털 트윈 환경을 구성하고, AI 배치 및 군중 시뮬레이션을 수행합니다.")
        if st.button("대시보드로 이동 ➡️", key="btn_to_dash", use_container_width=True):
            st.session_state['page'] = 'dashboard'
            st.rerun()

    with col2:
        st.markdown("### 📄 AI 종합 분석 보고서")
        st.write("생성된 행사장 배치안 및 안전성/동선 분석 결과를 바탕으로 직장상사 제출용 보고서를 즉시 생성합니다.")
        if st.button("AI 보고서 생성하기 ➡️", key="btn_to_rep", use_container_width=True):
            st.session_state['page'] = 'report'
            st.rerun()


# -------------------------------------------------------------------
# PAGE 2: 대시보드 화면
# -------------------------------------------------------------------
elif st.session_state['page'] == 'dashboard':
    st.title("🛠️ 행사 설계 대시보드")
    
    # 1. 이벤트 정보 입력 Form
    with st.expander("📝 행사 기본 정보 입력", expanded=not st.session_state['digital_twin_generated']):
        with st.form("event_info_form"):
            c1, c2, c3 = st.columns(3)
            with c1:
                event_name = st.text_input("이벤트 이름", "2026 청춘 페스티벌")
                event_purpose = st.selectbox("이벤트 목적", ["축제/공연", "박람회/전시", "기업 행사", "지역 문화 소통"])
            with c2:
                visitors = st.number_input("예상 방문객 수 (명)", value=5000, step=500)
                budget = st.text_input("예산", "5,000만원")
            with c3:
                location = st.text_input("장소", "서울 올림픽공원 잔디마당 (실외)")
                duration = st.text_input("진행 시간", "5시간")

            btn_submit = st.form_submit_button("✨ AI 이벤트 디자인 생성")
            if btn_submit:
                st.session_state['digital_twin_generated'] = True
                st.success("디지털 트윈 및 AI 최적 공간 배치가 완료되었습니다!")

    # 2. 메인 화면 (디지털 트윈 & 시뮬레이션)
    if not st.session_state['digital_twin_generated']:
        st.info("👆 위 입력창에서 행사의 기본 정보를 입력하고 'AI 이벤트 디자인 생성' 버튼을 눌러주세요.")
    else:
        # 주요 시설 데이터 정의
        facilities = [
            {"id": "stage", "name": "공연장 (무대)", "lat": 37.521, "lon": 127.121, "height": 25, "color": [138, 43, 226], "reason": "메인 무대는 시야 확보가 용이하고 소음 영향이 적은 북쪽 상단에 배치했습니다."},
            {"id": "food", "name": "푸드 존", "lat": 37.520, "lon": 127.120, "height": 10, "color": [255, 140, 0], "reason": "음식 조리 및 수용 인원을 감안해 무대와 일정 거리를 두고 동선 분리를 유도했습니다."},
            {"id": "booth", "name": "체험 부스", "lat": 37.5195, "lon": 127.1202, "height": 8, "color": [30, 144, 255], "reason": "입구 근처에 배치하여 관람객들의 유입 및 초기 참여도를 높였습니다."},
            {"id": "rest", "name": "휴게 공간", "lat": 37.5202, "lon": 127.1215, "height": 5, "color": [46, 139, 87], "reason": "공연장과 푸드존 사이 중심부에 배치하여 접근성을 극대화했습니다."},
            {"id": "medical", "name": "의료 센터", "lat": 37.5208, "lon": 127.1223, "height": 12, "color": [220, 20, 60], "reason": "비상 차량 출입이 수월한 외곽 통로 및 출입구 직통 경로에 배치했습니다."},
            {"id": "info", "name": "정보 센터", "lat": 37.5192, "lon": 127.1212, "height": 7, "color": [255, 105, 180], "reason": "주 출입구 바로 전면에 위치시켜 인포메이션 접근성을 확보했습니다."},
            {"id": "toilet", "name": "화장실", "lat": 37.5200, "lon": 127.1225, "height": 6, "color": [70, 130, 180], "reason": "상하수도 관로 인근 및 혼잡하지 않은 측면에 분산 배치했습니다."},
            {"id": "exit", "name": "비상구", "lat": 37.5188, "lon": 127.1218, "height": 15, "color": [255, 215, 0], "reason": "비상시 대피가 가장 빠른 최단 외곽선 상에 지정했습니다."}
        ]

        # 레이아웃 분할: 왼쪽 3D/2D 모니터링, 오른쪽 상세 정보 & AI 챗봇
        col_left, col_right = st.columns([2.2, 1])

        with col_left:
            st.subheader("🌐 디지털 트윈 기반 행사장 입체 공간 (3D View)")
            
            # PyDeck을 활용한 입체(3D) 디지털 트윈 시각화
            df_fac = pd.DataFrame(facilities)
            layer = pdk.Layer(
                "ColumnLayer",
                df_fac,
                get_position=["lon", "lat"],
                get_elevation="height",
                elevation_scale=5,
                radius=15,
                get_fill_color="color",
                pickable=True,
                auto_highlight=True
            )
            
            view_state = pdk.ViewState(
                latitude=37.5201,
                longitude=127.1212,
                zoom=16.8,
                pitch=55,
                bearing=-15
            )

            r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"html": "<b>{name}</b>"})
            st.pydeck_chart(r)

            # 시설물 선택 버튼 모음 (글자 클릭 시 배치 이유 안내)
            st.markdown("**📌 배치 시설 선택 (클릭 시 오른쪽에 최적화 이유 출력):**")
            btn_cols = st.columns(4)
            for idx, fac in enumerate(facilities):
                with btn_cols[idx % 4]:
                    if st.button(fac["name"], key=f"fac_btn_{fac['id']}", use_container_width=True):
                        st.session_state['selected_facility'] = fac

            # AI 시뮬레이션 및 히트맵
            st.markdown("---")
            c_sim1, c_sim2 = st.columns([1, 2])
            with c_sim1:
                if st.button("🤖 AI 시뮬레이션 실행 (군중 예측)", type="primary", use_container_width=True):
                    st.session_state['simulated'] = True

            if st.session_state['simulated']:
                st.subheader("🔥 군중 혼잡도 Heatmap (시뮬레이션 결과)")
                # 히트맵 더미 데이터 생성
                np.random.seed(42)
                heatmap_data = pd.DataFrame(
                    np.random.randn(20, 20) + np.outer(np.linspace(-1, 1, 20)**2, np.linspace(-1, 1, 20)**2),
                    columns=[f"X{i}" for i in range(20)]
                )
                fig = px.imshow(heatmap_data, color_continuous_scale='YlOrRd', title="구역별 동선 병목 및 혼잡 위험도")
                fig.update_layout(height=300, margin=dict(l=10, r=10, t=30, b=10))
                st.plotly_chart(fig, use_container_width=True)

        with col_right:
            # 시설 배치 이유 출력 카드
            st.subheader("💡 공간 배치 AI 요약")
            if st.session_state['selected_facility']:
                fac = st.session_state['selected_facility']
                st.info(f"**[{fac['name']}] 배치 이유**\n\n{fac['reason']}")
            else:
                st.write("왼쪽에서 시설 버튼(예: 공연장, 푸드 존 등)을 누르면 AI 최적화 이유를 확인할 수 있습니다.")

            st.markdown("---")

            # AI 어시스턴트 챗봇
            st.subheader("💬 AI 설계 어시스턴트")
            chat_container = st.container(height=320)
            
            with chat_container:
                for msg in st.session_state['chat_messages']:
                    st.chat_message(msg["role"]).write(msg["content"])

            if prompt := st.chat_input("디자인 수정이나 배치를 요청하세요..."):
                st.session_state['chat_messages'].append({"role": "user", "content": prompt})
                
                # AI 답변 응답 예시
                ai_reply = f"요청하신 '{prompt}' 사항을 반영하여 무대와의 안전거리를 고려해 공간 재배치를 진행했습니다."
                st.session_state['chat_messages'].append({"role": "assistant", "content": ai_reply})
                st.rerun()


# -------------------------------------------------------------------
# PAGE 3: AI 보고서 화면
# -------------------------------------------------------------------
elif st.session_state['page'] == 'report':
    st.title("📄 AI 기반 행사 설계 종합 보고서")
    st.caption("직장상사 보고용 자동 생성 보고서")

    st.markdown("""
    <div class="stCard">
        <h2>[보고서] 2026 청춘 페스티벌 공간 최적화 및 안전 설계안</h2>
        <p><b>작성자:</b> 이벤트 아키텍트 AI 시스템 | <b>보고 대상:</b> 총괄 담당자</p>
        <hr>
        <h3>1. 행사 개요 및 목표</h3>
        <ul>
            <li><b>행사명:</b> 2026 청춘 페스티벌</li>
            <li><b>예상 인원:</b> 5,000명 수용 예정</li>
            <li><b>설계 목표:</b> 병목현상 최소화, 비상시 대응 경로 확보, 공간 활용성 극대화</li>
        </ul>
        
        <h3>2. AI 종합 공간 평가 결과</h3>
        <ul>
            <li><b>안전성 평점:</b> 92점 (매우 우수) - 비상구 및 응급의료센터 최적 경로 확보</li>
            <li><b>동선 효율성:</b> 87점 (우수) - 주요 부스 분산 배치로 병목 구간 30% 감소 예상</li>
            <li><b>예산 효율성:</b> 88점 (우수)</li>
        </ul>

        <h3>3. AI 핵심 개선 권장사항</h3>
        <ol>
            <li>공연장과 푸드존 사이 혼잡도 예방을 위한 추가 휴식 구조물 설치 권장</li>
            <li>응급의료센터 진입 통로에 보안요원 2명 우선 배치 제안</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    col_down1, col_down2 = st.columns(2)
    with col_down1:
        st.download_button("📥 PDF/문서 다운로드", data="행사 설계 보고서 내용...", file_name="event_report.txt", use_container_width=True)
    with col_down2:
        if st.button("🔄 AI 보고서 재생성", use_container_width=True):
            st.toast("최신 데이터로 보고서를 재생성했습니다!")


# -------------------------------------------------------------------
# PAGE 4: 설정 화면
# -------------------------------------------------------------------
elif st.session_state['page'] == 'settings':
    st.title("⚙️ 시스템 설정")
    
    st.subheader("👤 계정 설정")
    st.text_input("사용자 이름", value=st.session_state['username'], disabled=True)
    st.text_input("계정 권한", value="행사 총괄 관리자", disabled=True)
    
    st.subheader("🎨 앱 환경 설정")
    st.toggle("3D 입체 그래픽 가속 모드", value=True)
    st.toggle("AI 시뮬레이션 알림 받기", value=True)
    
    st.divider()
    if st.button("로그아웃", type="primary"):
        st.session_state['logged_in'] = False
        st.session_state['page'] = 'home'
        st.rerun()
