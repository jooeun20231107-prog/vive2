import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit.components.v1 as components
import json

# 페이지 세팅
st.set_page_config(
    page_title="이벤트 아키텍트 AI - AI 기반 행사 자동 설계 플랫폼",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    /* 전체 배경 및 폰트 - 화사한 라이트 모드 적용 */
    .stApp {
        background-color: #F8FAFC;
        color: #0F172A;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }
    
    /* 상단 네비게이션 헤더 */
    .top-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 24px;
        background-color: #FFFFFF;
        border-bottom: 1px solid #E2E8F0;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    /* 홈 대형 카드 디자인 */
    .home-card {
        background: #FFFFFF;
        border: 2px solid #E2E8F0;
        border-radius: 20px;
        padding: 36px 28px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 8px 24px rgba(0,0,0,0.04);
        cursor: pointer;
        height: 100%;
    }
    .home-card:hover {
        border-color: #2563EB;
        transform: translateY(-4px);
        box-shadow: 0 12px 32px rgba(37, 99, 235, 0.12);
    }
    
    /* 카드 및 패널 스타일 */
    .custom-card {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
        border: 1px solid #E2E8F0;
        margin-bottom: 16px;
    }

    /* 배치 사유 패널 하이라이트 */
    .reasoning-box {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border: 1px solid #93C5FD;
        border-radius: 14px;
        padding: 18px;
        color: #1E3A8A;
        margin-top: 10px;
    }

    /* 지표 알약 바 */
    .pill-stat {
        background-color: #F1F5F9;
        border: 1px solid #CBD5E1;
        border-radius: 12px;
        padding: 10px;
        text-align: center;
        font-weight: bold;
    }

    /* 입력 폼 디자인 */
    .stTextInput input, .stSelectbox select, .stNumberInput input {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        color: #0F172A !important;
        border-radius: 10px !important;
    }

    /* 기본 버튼 커스텀 */
    </style>
""", unsafe_allow_html=True)

# 대한민국 전국 주요 광역시·도 및 대학교/고등학교/체육관 축제 장소 데이터베이스
EVENT_VENUES = {
    # [특수 / 교육기관 & 고등학교 / 대학교 축제 장소]
    "[충청권] 건양대학교 병설 건양고등학교 체육관 (충남 논산)": {
        "type": "학교체육관/실내", "address": "충청남도 논산시 대학로 121 (건양고등학교)",
        "width_m": 50, "height_m": 35, "max_capacity": 1500,
        "description": "건양고등학교 실내 대강당 및 체육관으로 학교 축제 및 실내 학술/문화 행사용"
    },
    "[충청권] 건양대학교 논산 창의융합캠퍼스 중앙광장 (충남 논산)": {
        "type": "대학교/야외광장", "address": "충청남도 논산시 대학로 121",
        "width_m": 140, "height_m": 95, "max_capacity": 8000,
        "description": "건양대 대표 야외 대축제 및 메인 무대/체험 부스 설치 최적화 부지"
    },
    "[충청권] 건양대학교 대전 메디컬캠퍼스 야외광장 (대전 서구)": {
        "type": "대학교/야외광장", "address": "대전광역시 서구 관저동로 158",
        "width_m": 110, "height_m": 75, "max_capacity": 5000,
        "description": "대전 메디컬캠퍼스 동아리 축제 및 대학 보건/문화 페스티벌 전용 광장"
    },
    "[수도권] 연세대학교 신촌캠퍼스 노천극장 (서울 서대문)": {
        "type": "대학교/야외공연장", "address": "서울특별시 서대문구 연세로 50",
        "width_m": 100, "height_m": 80, "max_capacity": 10000,
        "description": "대한민국 대표 대학 축제(아카라카)가 열리는 계단식 대형 야외 대공연장"
    },
    "[수도권] 고려대학교 서울캠퍼스 중앙광장 및 화정체육관 (서울 성북)": {
        "type": "대학교/복합", "address": "서울특별시 성북구 안암로 145",
        "width_m": 130, "height_m": 90, "max_capacity": 12000,
        "description": "고대 입실렌티 축제 및 대형 돔 체육관 겸용 대규모 이벤트 공간"
    },
    "[수도권] 서울대학교 관악캠퍼스 잔디광장 (서울 관악)": {
        "type": "대학교/잔디광장", "address": "서울특별시 관악구 관악로 1",
        "width_m": 150, "height_m": 100, "max_capacity": 9000,
        "description": "관악캠퍼스 중심 잔디 광장으로 대학 축제 및 대형 부스단지 구성 용이"
    },
    "[수도권] 성균관대학교 자연과학캠퍼스 잔디밭 (경기 수원)": {
        "type": "대학교/잔디광장", "address": "경기도 수원시 장안구 서부로 2066",
        "width_m": 120, "height_m": 85, "max_capacity": 7000,
        "description": "수원 캠퍼스 대표 대학 축제 및 야외 팝업/푸드존 설치 부지"
    },
    "[충청권] KAIST 대전 본원 스포츠콤플렉스 및 야외무대 (대전 유성)": {
        "type": "대학교/체육관·광장", "address": "대전광역시 유성구 대학로 291",
        "width_m": 120, "height_m": 80, "max_capacity": 6500,
        "description": "카이스트 석림태울제 대학 축제 및 첨단 기술 체험 부스 전용 공간"
    },
    "[영남권] 경북대학교 대구캠퍼스 야외강당 (대구 북구)": {
        "type": "대학교/야외공연장", "address": "대구광역시 북구 대학로 80",
        "width_m": 110, "height_m": 75, "max_capacity": 8000,
        "description": "대구 대동제 및 영남권 최대 규모 대학 축제 메인 무대 공간"
    },
    "[영남권] 부산대학교 금정캠퍼스 넉넉한터 (부산 금정)": {
        "type": "대학교/야외광장", "address": "부산광역시 금정구 부산대학로63번길 2",
        "width_m": 100, "height_m": 70, "max_capacity": 6000,
        "description": "부산대 전통의 대형 광장 공간으로 축제 및 총학생회 행사 전용"
    },
    "[호남권] 전남대학교 광주캠퍼스 용봉탑 광장 (광주 북구)": {
        "type": "대학교/야외광장", "address": "광주광역시 북구 용봉로 77",
        "width_m": 115, "height_m": 80, "max_capacity": 7500,
        "description": "용봉 대동제 중심 무대 및 학생 참여형 부스 조성 최적지"
    },

    # [수도권 대형 전문 장소]
    "[수도권] 서울 COEX 전시장 Hall A/B (서울 강남)": {
        "type": "컨벤션/실내", "address": "서울특별시 강남구 영동대로 513",
        "width_m": 180, "height_m": 120, "max_capacity": 15000,
        "description": "대한민국 대표 국제 박람회 및 초대형 학술/전시 전용 컨벤션 홀"
    },
    "[수도권] 서울 올림픽공원 평화의 광장 (서울 송파)": {
        "type": "공원/야외", "address": "서울특별시 송파구 올림픽로 424",
        "width_m": 160, "height_m": 100, "max_capacity": 10000,
        "description": "넓은 보도 블록 광장 및 대형 문화 축제/공연 연출에 최적화된 야외 부지"
    },
    "[수도권] 서울 잠실종합운동장 보조경기장 (서울 송파)": {
        "type": "경기장/야외", "address": "서울특별시 송파구 올림픽로 25",
        "width_m": 140, "height_m": 90, "max_capacity": 15000,
        "description": "대형 뮤직 페스티벌 및 글로벌 팝 콘서트 전용 대표 야외 경기장"
    },
    "[수도권] 서울 여의도 한강공원 이벤트광장 (서울 영등포)": {
        "type": "수변공원/야외", "address": "서울특별시 영등포구 여의동로 330",
        "width_m": 200, "height_m": 110, "max_capacity": 15000,
        "description": "한강변 대표 야외 축제 및 대규모 페스티벌/불꽃축제 메인 광장"
    },
    "[수도권] 경기 고양 KINTEX 제1전시장 (경기 고양)": {
        "type": "컨벤션/실내", "address": "경기도 고양시 일산서구 Kintex로 217-60",
        "width_m": 200, "height_m": 150, "max_capacity": 20000,
        "description": "국내 최대 규모 실내 평면 전시 공간으로 초대형 부스 단지 구성 용이"
    },
    "[수도권] 인천 송도 컨벤시아 (인천 연수)": {
        "type": "컨벤션/실내", "address": "인천광역시 연수구 센트럴로 123",
        "width_m": 140, "height_m": 90, "max_capacity": 10000,
        "description": "송도 국제도시 중심의 첨단 MICE 전시 및 국제행사 전용 컨벤션"
    },

    # [충청권 대표 장소]
    "[충청권] 충남 논산 시민공원 야외광장 (충남 논산)": {
        "type": "공원/야외", "address": "충청남도 논산시 관촉로 67",
        "width_m": 120, "height_m": 80, "max_capacity": 5000,
        "description": "탁 트인 잔디 광장과 산책로가 조성된 논산시 대표 야외 행사 공간"
    },
    "[충청권] 충남 천안 유관순체육관 (충남 천안)": {
        "type": "체육관/실내", "address": "충청남도 천안시 서북구 번영로 208",
        "width_m": 60, "height_m": 40, "max_capacity": 3500,
        "description": "대형 실내 코트 및 가변석을 갖춘 실내 종합 스포츠 및 콘서트장"
    },
    "[충청권] 대전 컨벤션센터 DCC (대전 유성)": {
        "type": "컨벤션/실내", "address": "대전광역시 유성구 엑스포로 107",
        "width_m": 100, "height_m": 70, "max_capacity": 6000,
        "description": "중부권 대표 첨단 학술 및 산학연 박람회 전용 컨벤션 홀"
    },
    "[충청권] 세종 호수공원 메인광장 (세종특별자치시)": {
        "type": "공원/야외", "address": "세종특별자치시 다솜로 216",
        "width_m": 150, "height_m": 100, "max_capacity": 12000,
        "description": "국내 최대 인공호수공원 전면의 쾌적한 친수 야외 이벤트 공간"
    },

    # [영남 / 호남 / 강원 / 제주 장소]
    "[영남권] 부산 BEXCO 제1전시장 (부산 해운대)": {
        "type": "컨벤션/실내", "address": "부산광역시 해운대구 APEC로 55",
        "width_m": 160, "height_m": 110, "max_capacity": 12000,
        "description": "영남권 대표 국제 컨벤션 센터로 접근성과 대규모 인파 수용력 우수"
    },
    "[영남권] 대구 EXCO 전시장 (대구 북구)": {
        "type": "컨벤션/실내", "address": "대구광역시 북구 엑스코로 10",
        "width_m": 130, "height_m": 85, "max_capacity": 8000,
        "description": "대구·경북권 최대 MICE 복합 공간 및 전문 전시장"
    },
    "[호남권] 광주 김대중컨벤션센터 (광주 서구)": {
        "type": "컨벤션/실내", "address": "광주광역시 서구 상무누리로 30",
        "width_m": 120, "height_m": 80, "max_capacity": 7000,
        "description": "호남권 최대 국제 MICE 시설로 다양한 국제 박람회 및 콘서트 개최"
    },
    "[호남권] 전남 여수세계박람회장 엑스포광장 (전남 여수)": {
        "type": "수변공원/야외", "address": "전라남도 여수시 박람회길 1",
        "width_m": 180, "height_m": 100, "max_capacity": 15000,
        "description": "남해안 해양 문화 축제 및 대규모 국제 행사가 개최되는 대형 수변 광장"
    },
    "[강원권] 강원 강릉 올림픽파크 야외광장 (강원 강릉)": {
        "type": "체육공원/야외", "address": "강원특별자치도 강릉시 수리골길 102",
        "width_m": 140, "height_m": 90, "max_capacity": 8000,
        "description": "동계올림픽 유산 기반의 넓은 광장과 최첨단 스포츠/이벤트 인프라"
    },
    "[제주권] 제주 ICC 국제컨벤션센터 (제주 서귀포)": {
        "type": "컨벤션/실내", "address": "제주특별자치도 서귀포시 중문관광로 224",
        "width_m": 120, "height_m": 80, "max_capacity": 5000,
        "description": "중문관광단지 내 위치한 휴양형 국제 컨벤션 및 종합 행사장"
    },
    "[자유 지정] 전국 사용자 직접 입력 규격": {
        "type": "사용자 정의", "address": "전국 현장 주소 자유 입력",
        "width_m": 100, "height_m": 70, "max_capacity": 5000,
        "description": "전국 어디서나 행사장의 가로/세로 규격을 커스텀 설정하여 AI 공간 배치를 실행합니다."
    }
}

# 시설별 AI 배치 이유 상세 설명 DB
FACILITY_REASONING = {
    "무대": {
        "icon": "🎭",
        "title": "북측 시야 확보 및 메인 출입구 대치 배치",
        "reason": "바람의 방향과 관람객 시야각을 고려하여 북쪽 상단 중심부에 배치했습니다. 입구에서 진입한 인원이 자연스럽게 중앙 무대를 중심으로 좌우에 분산되도록 유도합니다."
    },
    "푸드 존": {
        "icon": "🍔",
        "title": "남서쪽 주 동선 인근 및 환기 구역 배치",
        "reason": "음식 조리 시 발생하는 연기와 냄새 배출이 쉬운 야외 바람길 상류(서쪽)에 배치했으며, 무대 인파와의 병목 현상을 방지하기 위해 40m 이상 이격했습니다."
    },
    "비상구": {
        "icon": "🚨",
        "title": "동측 외곽 및 넓은 진출입로 연계",
        "reason": "소방차 및 구급차의 접근성이 우수한 외곽 도로와 직선으로 연결된 동쪽 및 남쪽 2개소에 수용 인원 기준 안전 규격(폭 4m 이상)으로 분산 배치했습니다."
    },
    "정보 센터": {
        "icon": "ℹ️",
        "title": "남측 주 진입로 전면 시가화 지역 연계",
        "reason": "방문객이 행사장 입장 즉시 리플렛 및 길 안내를 받을 수 있도록 남쪽 정문 인근 통로 중앙에 배치했습니다."
    },
    "부스": {
        "icon": "🎪",
        "title": "중앙 순환형 동선 복도 단지 구성",
        "reason": "관람객 흐름이 끊기지 않는 2열 도보 스트리트 형태(폭 6m)로 배치하여 부스 체류 시간을 극대화하고 체증을 최소화했습니다."
    },
    "화장실": {
        "icon": "🚻",
        "title": "남동측 위생 배수관 연계 및 오수 처리 용이 구역",
        "reason": "상하수도 배관 인프라가 가까운 동남쪽 외곽에 배치하여 위생 안전을 확보하고, 메인 무대 음향 영향권을 벗어나 편안하게 이용 가능합니다."
    },
    "의료 센터": {
        "icon": "🚑",
        "title": "북동측 응급차량 골든타임 확보 구역",
        "reason": "응급 환자 발생 시 앰뷸런스 진입이 즉시 가능한 외곽 도로 인접 지역에 위치하며, 무대 및 푸드존 양쪽 모두에서 1분 이내 접근 가능한 중앙 균형 위치입니다."
    },
    "휴식 구역": {
        "icon": "☕",
        "title": "동측 녹지 쉼터 및 소음 저감 구역",
        "reason": "무대 소음 레벨이 60dB 이하로 감소하는 동쪽 녹지 공간에 배치하여 방문객들에게 쾌적한 피크닉 및 쉬는 공간을 제공합니다."
    }
}

header_col1, header_col2 = st.columns([6, 4])

with header_col1:
    if st.button("🎪 **이벤트 아키텍트 AI**", type="tertiary"):
        st.session_state['current_page'] = 'home'
        st.rerun()

with header_col2:
    top_btn_c1, top_btn_c2 = st.columns([1, 1])
    with top_btn_c1:
        if st.session_state['logged_in']:
            if st.button(f"👤 {st.session_state['user_name']}", use_container_width=True):
                st.session_state['current_page'] = 'settings'
                st.rerun()
        else:
            if st.button("🔑 로그인 / 회원가입", use_container_width=True):
                st.session_state['current_page'] = 'login'
                st.rerun()
    with top_btn_c2:
        if st.button("⚙️ 설정", use_container_width=True):
            st.session_state['current_page'] = 'settings'
            st.rerun()

st.divider()

if st.session_state['current_page'] == 'home':
    st.markdown("<h2 style='text-align: center; margin-bottom: 8px;'>AI 기반 행사 자동 설계 플랫폼</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748B; margin-bottom: 40px;'>디지털 트윈 기반 공간 자동 배치, 실시간 군중 동선 시뮬레이션 및 상사 보고서 자동 생성</p>", unsafe_allow_html=True)

    col_home1, col_home2 = st.columns(2)

    with col_home1:
        st.markdown("""
        <div class="home-card">
            <div style="font-size: 3.5rem; margin-bottom: 16px;">🏛️</div>
            <h2 style="color: #1E293B; margin-bottom: 12px;">AI 공간 설계 대시보드</h2>
            <p style="color: #64748B; font-size: 0.95rem; line-height: 1.6;">
                행사 사양을 입력하면 디지털 트윈 캔버스에 무대, 푸드존, 부스, 의료센터 등을 입체 자동 배치하고 AI 군중 동선을 시뮬레이션합니다.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("👉 대시보드 바로가기", type="primary", use_container_width=True, key="btn_to_dash"):
            st.session_state['current_page'] = 'dashboard'
            st.rerun()

    with col_home2:
        st.markdown("""
        <div class="home-card">
            <div style="font-size: 3.5rem; margin-bottom: 16px;">📋</div>
            <h2 style="color: #1E293B; margin-bottom: 12px;">AI 종합 보고서</h2>
            <p style="color: #64748B; font-size: 0.95rem; line-height: 1.6;">
                최적화된 디지털 트윈 결과 및 안전·동선 평가 지표를 직장 상사 및 관계 부서에 즉시 제출할 수 있는 정식 보고서 형태로 자동 출력합니다.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("👉 AI 보고서 바로가기", type="secondary", use_container_width=True, key="btn_to_rep"):
            st.session_state['current_page'] = 'report'
            st.rerun()

elif st.session_state['current_page'] == 'dashboard':
    st.markdown("### 🏛️ AI 행사 공간 설계 대시보드")
    
    # 상단 입력 필드 바
    in_col1, in_col2, in_col3, in_col4, in_col5, in_col6 = st.columns([1.5, 1.2, 1.2, 1.0, 2.2, 1.3])
    
    with in_col1:
        st.session_state['event_name'] = st.text_input("이벤트 이름", value=st.session_state['event_name'])
    with in_col2:
        st.session_state['event_purpose'] = st.selectbox("이벤트 목적", ["축제/공연", "박람회/전시", "학술/대회", "체육 대회", "학교/대학 축제"])
    with in_col3:
        st.session_state['visitor_count'] = st.number_input("예상 방문객 수", value=st.session_state['visitor_count'], step=500)
    with in_col4:
        st.session_state['budget'] = st.text_input("예산", value=st.session_state['budget'])
    with in_col5:
        st.session_state['venue'] = st.selectbox("장소 선택 (전국/대학/체육관)", list(EVENT_VENUES.keys()))
    with in_col6:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        if st.button("✨ AI 이벤트 디자인 생성", type="primary", use_container_width=True):
            st.session_state['design_generated'] = True
            st.toast("AI가 선택하신 장소에 맞춰 이미지 스타일의 3D 입체 디지털 트윈 배치를 연출했습니다!", icon="🎨")
            st.rerun()

    st.divider()

    # 메인 캔버스 및 레이아웃 영역
    dash_left, dash_right = st.columns([7, 3])

    with dash_left:
        if not st.session_state['design_generated']:
            st.markdown("""
            <div style="height: 540px; border: 2px dashed #CBD5E1; border-radius: 20px; display: flex; flex-direction: column; justify-content: center; align-items: center; background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);">
                <div style="font-size: 4.5rem; color: #94A3B8; margin-bottom: 12px;">📐</div>
                <h3 style="color: #334155; margin-bottom: 8px; font-weight: 700;">3D 공간 디지털 트윈 대기 중</h3>
                <p style="color: #64748B; font-size: 0.95rem; max-width: 480px; text-align: center; line-height: 1.5;">
                    상단에서 <b>건양고등학교 체육관, 대학 축제 광장</b> 등 장소와 사양을 선택한 후 <b>[✨ AI 이벤트 디자인 생성]</b>을 누르시면 고화질 그래픽 조감도가 구동됩니다.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            sim_flag = str(st.session_state['simulation_active']).lower()
            selected_venue_info = EVENT_VENUES.get(st.session_state['venue'], EVENT_VENUES["[수도권] 서울 COEX 전시장 Hall A/B (서울 강남)"])
            
            # 고화질 이미지 느낌의 정밀 3D Isometric HTML Canvas
            canvas_code = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ margin: 0; padding: 0; background: #F1F5F9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; overflow: hidden; user-select: none; }}
                    #canvasContainer {{
                        position: relative; width: 100%; height: 540px; 
                        background: radial-gradient(circle at 50% 30%, #FFFFFF 0%, #E2E8F0 100%);
                        border-radius: 20px; border: 1.5px solid #CBD5E1; box-shadow: 0 12px 36px rgba(15,23,42,0.08);
                        overflow: hidden;
                    }}
                    canvas {{ display: block; width: 100%; height: 100%; cursor: grab; }}
                    
                    /* 이미지 스타일 입체 오버레이 태그 */
                    .graphic-badge {{
                        position: absolute; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px);
                        border: 1px solid #CBD5E1; box-shadow: 0 6px 18px rgba(0,0,0,0.08);
                        padding: 6px 14px; border-radius: 20px; font-size: 11px; font-weight: 800; color: #0F172A;
                        display: flex; align-items: center; gap: 6px; pointer-events: none;
                    }}
                    .graphic-dot {{ width: 8px; height: 8px; border-radius: 50%; background-color: #2563EB; box-shadow: 0 0 10px #3B82F6; }}
                    .graphic-dot.red {{ background-color: #EF4444; box-shadow: 0 0 10px #F87171; }}
                    .graphic-dot.green {{ background-color: #10B981; box-shadow: 0 0 10px #34D399; }}

                    .top-ctrl-bar {{
                        position: absolute; top: 16px; left: 16px; right: 16px; display: flex; justify-content: space-between; align-items: center; pointer-events: none;
                    }}
                    .ctrl-pill {{
                        background: rgba(255,255,255,0.92); backdrop-filter: blur(10px); padding: 8px 16px; border-radius: 12px;
                        border: 1px solid #CBD5E1; font-size: 12px; font-weight: 700; color: #1E293B; pointer-events: auto;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
                    }}
                </style>
            </head>
            <body>
                <div id="canvasContainer">
                    <div class="top-ctrl-bar">
                        <div class="ctrl-pill">🏛️ {st.session_state['venue']} ({selected_venue_info['width_m']}m x {selected_venue_info['height_m']}m)</div>
                        <div class="ctrl-pill" style="color: #2563EB;">🎨 3D 디지털 트윈 이미지 조감도</div>
                    </div>

                    <div class="graphic-badge" style="top: 75px; left: 230px;"><div class="graphic-dot"></div> 군중 예측 동선</div>
                    <div class="graphic-badge" style="top: 105px; right: 220px;"><div class="graphic-dot green"></div> AI 최적화 완료</div>
                    <div class="graphic-badge" style="bottom: 45px; right: 250px;"><div class="graphic-dot"></div> 실시간 센서 레이아웃</div>

                    <canvas id="isoCanvas" width="920" height="540"></canvas>
                </div>

                <script>
                    const canvas = document.getElementById('isoCanvas');
                    const ctx = canvas.getContext('2d');
                    let simActive = {sim_flag};

                    const particles = [];
                    for (let i = 0; i < 90; i++) {{
                        particles.push({{
                            progress: Math.random(),
                            speed: 0.0018 + Math.random() * 0.0028,
                            targetIndex: Math.floor(Math.random() * 5),
                            offset: (Math.random() - 0.5) * 14
                        }});
                    }}

                    function isoProject(x, y, z) {{
                        return {{
                            x: (x - y) * 0.74 + 460,
                            y: (x + y) * 0.37 - z + 110
                        }};
                    }}

                    // 그래픽 3D 블록 연출
                    function draw3DBlock(x, y, w, h, z, colorTop, colorLeft, colorRight, label, icon) {{
                        const p1 = isoProject(x, y, z);
                        const p2 = isoProject(x + w, y, z);
                        const p3 = isoProject(x + w, y + h, z);
                        const p4 = isoProject(x, y + h, z);

                        const p1_b = isoProject(x, y, 0);
                        const p2_b = isoProject(x + w, y, 0);
                        const p3_b = isoProject(x + w, y + h, 0);
                        const p4_b = isoProject(x, y + h, 0);

                        // 그림자 효과
                        ctx.fillStyle = "rgba(15, 23, 42, 0.12)";
                        ctx.beginPath();
                        ctx.moveTo(p1_b.x + 10, p1_b.y + 8); ctx.lineTo(p2_b.x + 10, p2_b.y + 8);
                        ctx.lineTo(p3_b.x + 10, p3_b.y + 8); ctx.lineTo(p4_b.x + 10, p4_b.y + 8);
                        ctx.closePath(); ctx.fill();

                        // 좌측면
                        ctx.fillStyle = colorLeft;
                        ctx.beginPath();
                        ctx.moveTo(p1.x, p1.y); ctx.lineTo(p4.x, p4.y); ctx.lineTo(p4_b.x, p4_b.y); ctx.lineTo(p1_b.x, p1_b.y);
                        ctx.closePath(); ctx.fill();

                        // 우측면
                        ctx.fillStyle = colorRight;
                        ctx.beginPath();
                        ctx.moveTo(p4.x, p4.y); ctx.lineTo(p3.x, p3.y); ctx.lineTo(p3_b.x, p3_b.y); ctx.lineTo(p4_b.x, p4_b.y);
                        ctx.closePath(); ctx.fill();

                        // 윗면
                        ctx.fillStyle = colorTop;
                        ctx.beginPath();
                        ctx.moveTo(p1.x, p1.y); ctx.lineTo(p2.x, p2.y); ctx.lineTo(p3.x, p3.y); ctx.lineTo(p4.x, p4.y);
                        ctx.closePath(); ctx.fill();
                        ctx.strokeStyle = "rgba(255,255,255,0.5)"; ctx.lineWidth = 1.2; ctx.stroke();

                        if (label) {{
                            const center = isoProject(x + w/2, y + h/2, z);
                            ctx.fillStyle = "#FFFFFF";
                            ctx.shadowColor = "rgba(0,0,0,0.2)"; ctx.shadowBlur = 8;
                            ctx.beginPath(); ctx.roundRect(center.x - 34, center.y - 13, 68, 22, 11); ctx.fill();
                            ctx.shadowBlur = 0;

                            ctx.fillStyle = "#0F172A";
                            ctx.font = "bold 11px -apple-system, sans-serif";
                            ctx.textAlign = "center";
                            ctx.fillText((icon || "") + " " + label, center.x, center.y + 3);
                        }}
                    }}

                    function drawTree(x, y) {{
                        const trunk = isoProject(x, y, 14);
                        const trunk_b = isoProject(x, y, 0);
                        ctx.strokeStyle = "#78350F"; ctx.lineWidth = 3.5;
                        ctx.beginPath(); ctx.moveTo(trunk_b.x, trunk_b.y); ctx.lineTo(trunk.x, trunk.y); ctx.stroke();

                        const top = isoProject(x, y, 24);
                        ctx.fillStyle = "#10B981"; ctx.beginPath(); ctx.arc(top.x, top.y, 9, 0, Math.PI * 2); ctx.fill();
                        ctx.fillStyle = "#059669"; ctx.beginPath(); ctx.arc(top.x - 2, top.y - 2, 6, 0, Math.PI * 2); ctx.fill();
                    }}

                    function drawHeatmap(x, y, radius) {{
                        const p = isoProject(x, y, 0);
                        const grad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, radius);
                        grad.addColorStop(0, "rgba(239, 68, 68, 0.45)");
                        grad.addColorStop(0.6, "rgba(59, 130, 246, 0.2)");
                        grad.addColorStop(1, "rgba(59, 130, 246, 0)");
                        ctx.fillStyle = grad;
                        ctx.beginPath(); ctx.ellipse(p.x, p.y, radius * 1.5, radius * 0.75, 0, 0, Math.PI * 2); ctx.fill();
                    }}

                    function render() {{
                        ctx.clearRect(0, 0, canvas.width, canvas.height);

                        // 3D 이미지 외벽 (딥 블루 모던 프레임)
                        draw3DBlock(0, 0, 470, 16, 42, "#1E293B", "#0F172A", "#334155", "", "");
                        draw3DBlock(0, 0, 16, 350, 42, "#1E293B", "#0F172A", "#334155", "", "");

                        // 메인 바닥 타일
                        const g1 = isoProject(16, 16, 0); const g2 = isoProject(470, 16, 0);
                        const g3 = isoProject(470, 350, 0); const g4 = isoProject(16, 350, 0);
                        
                        ctx.fillStyle = "#E2E8F0";
                        ctx.beginPath(); ctx.moveTo(g1.x, g1.y); ctx.lineTo(g2.x, g2.y); ctx.lineTo(g3.x, g3.y); ctx.lineTo(g4.x, g4.y); ctx.closePath(); ctx.fill();

                        // 녹지 피크닉 존
                        const r1 = isoProject(330, 25, 0); const r2 = isoProject(450, 25, 0);
                        const r3 = isoProject(450, 130, 0); const r4 = isoProject(330, 130, 0);
                        ctx.fillStyle = "#D1FAE5";
                        ctx.beginPath(); ctx.moveTo(r1.x, r1.y); ctx.lineTo(r2.x, r2.y); ctx.lineTo(r3.x, r3.y); ctx.lineTo(r4.x, r4.y); ctx.closePath(); ctx.fill();

                        // 그리드 그릿
                        ctx.strokeStyle = "rgba(148, 163, 184, 0.3)"; ctx.lineWidth = 1;
                        for(let s = 60; s < 450; s += 35) {{
                            const ls = isoProject(s, 16, 0); const le = isoProject(s, 350, 0);
                            ctx.beginPath(); ctx.moveTo(ls.x, ls.y); ctx.lineTo(le.x, le.y); ctx.stroke();
                        }}

                        drawHeatmap(90, 240, 55);

                        // 시설 3D 배치 모델링
                        draw3DBlock(50, 35, 120, 65, 34, "#312E81", "#1E1B4B", "#4338CA", "무대", "🎭");
                        draw3DBlock(50, 210, 85, 75, 22, "#D97706", "#92400E", "#F59E0B", "푸드 존", "🍔");
                        
                        for(let b=0; b<3; b++) {{
                            draw3DBlock(195, 95 + b*55, 48, 40, 18, "#2563EB", "#1E40AF", "#3B82F6", b===1 ? "부스" : "", "🎪");
                            draw3DBlock(260, 95 + b*55, 48, 40, 18, "#2563EB", "#1E40AF", "#3B82F6", "", "");
                        }}

                        draw3DBlock(340, 35, 90, 80, 12, "#059669", "#065F46", "#10B981", "휴식 구역", "☕");
                        drawTree(350, 125); drawTree(420, 125); drawTree(435, 45);

                        draw3DBlock(275, 28, 55, 40, 18, "#10B981", "#047857", "#34D399", "의료 센터", "🚑");
                        draw3DBlock(210, 285, 55, 38, 16, "#F59E0B", "#B45309", "#FBBF24", "정보 센터", "ℹ️");
                        draw3DBlock(375, 205, 65, 45, 16, "#475569", "#1E293B", "#64748B", "화장실", "🚻");
                        draw3DBlock(435, 135, 20, 42, 26, "#EF4444", "#991B1B", "#F87171", "비상구", "🚨");

                        if (simActive) {{
                            const targets = [
                                isoProject(110, 70, 0), isoProject(95, 250, 0),
                                isoProject(230, 155, 0), isoProject(385, 75, 0), isoProject(240, 300, 0)
                            ];
                            const startPos = isoProject(235, 330, 0);

                            particles.forEach(p => {{
                                p.progress += p.speed;
                                if (p.progress >= 1.0) p.progress = 0;
                                const t = targets[p.targetIndex];
                                const cx = startPos.x + (t.x - startPos.x) * p.progress + p.offset;
                                const cy = startPos.y + (t.y - startPos.y) * p.progress + p.offset * 0.5;
                                
                                ctx.beginPath(); ctx.arc(cx, cy, 3.8, 0, Math.PI * 2);
                                ctx.fillStyle = p.targetIndex === 1 ? "#EF4444" : "#2563EB"; 
                                ctx.shadowColor = ctx.fillStyle; ctx.shadowBlur = 5;
                                ctx.fill(); ctx.shadowBlur = 0;
                            }});
                        }}

                        requestAnimationFrame(render);
                    }}
                    render();
                </script>
            </body>
            </html>
            """
            components.html(canvas_code, height=560)

        # 캔버스 아래 제어 버튼 및 시설 선택
        st.markdown("#### 🎯 시설 배치 사유 확인 및 시뮬레이션 제어")
        
        sim_col1, sim_col2 = st.columns([4, 6])
        with sim_col1:
            if st.button("🏃‍♂️ AI 군중 동선 시뮬레이션 (ON/OFF)", type="secondary", use_container_width=True):
                st.session_state['simulation_active'] = not st.session_state['simulation_active']
                st.rerun()

        st.caption("아래 시설 버튼을 클릭하시면 우측 패널에서 왜 그 공간에 배치했는지 AI 사유를 요약해 드립니다:")
        fac_cols = st.columns(8)
        facility_list = ["무대", "푸드 존", "비상구", "정보 센터", "부스", "화장실", "의료 센터", "휴식 구역"]
        
        for idx, fac in enumerate(facility_list):
            with fac_cols[idx]:
                if st.button(fac, key=f"btn_fac_{fac}", use_container_width=True):
                    st.session_state['selected_facility'] = fac
                    st.rerun()

        # 대화형 AI 통합 창
        with st.expander("💬 AI 대화형 공간 디자인 조교", expanded=True):
            chat_in1, chat_in2 = st.columns([8, 2])
            with chat_in1:
                user_cmd = st.text_input("디자인 명령 입력", placeholder="예: '푸드 존을 남쪽으로 15m 이동시키고 휴식 공간 늘려줘'", label_visibility="collapsed")
            with chat_in2:
                if st.button("요청 반영", type="primary", use_container_width=True):
                    if user_cmd:
                        st.session_state['chat_messages'].append({"role": "user", "content": user_cmd})
                        st.session_state['chat_messages'].append({"role": "assistant", "content": f"✨ '{user_cmd}' 요청을 반영하여 디지털 트윈 배치를 재계산했습니다."})
                        st.session_state['design_generated'] = True
                        st.rerun()

            for msg in st.session_state['chat_messages'][-2:]:
                st.chat_message(msg["role"]).write(msg["content"])

    with dash_right:
        # 우측: 시설 배치 사유 요약 패널만 깔끔하게 유지 (요청에 따라 실시간 공간 지표 평가 삭제)
        selected = st.session_state['selected_facility']
        fac_info = FACILITY_REASONING.get(selected, FACILITY_REASONING["무대"])
        venue_info = EVENT_VENUES.get(st.session_state['venue'], EVENT_VENUES["[수도권] 서울 COEX 전시장 Hall A/B (서울 강남)"])

        st.markdown(f"#### 💡 선택 시설: {fac_info['icon']} {selected}")
        st.markdown(f"""
        <div class="reasoning-box">
            <div style="font-weight: bold; font-size: 1rem; margin-bottom: 6px;">📌 AI 공간 배치 사유 요약</div>
            <div style="font-weight: 700; font-size: 0.95rem; color: #1E40AF; margin-bottom: 10px;">{fac_info['title']}</div>
            <div style="font-size: 0.88rem; line-height: 1.65; color: #334155;">{fac_info['reason']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        st.markdown("#### 📐 선택 장소 사양 브리핑")
        st.markdown(f"""
        <div class="custom-card">
            <div style="font-size: 0.85rem; color: #64748B; margin-bottom: 4px;">선택 장소</div>
            <div style="font-size: 1.05rem; font-weight: bold; color: #0F172A; margin-bottom: 8px;">{st.session_state['venue']}</div>
            <div style="font-size: 0.85rem; color: #334155; line-height: 1.6;">
                • <b>공간 규격:</b> 가로 {venue_info['width_m']}m × 세로 {venue_info['height_m']}m<br>
                • <b>권장 수용 인원:</b> 약 {venue_info['max_capacity']:,}명<br>
                • <b>시설 유형:</b> {venue_info['type']}<br>
                • <b>특징:</b> {venue_info['description']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        st.markdown("#### 📐 장소 및 공간 규격 브리핑")
        st.markdown(f"""
        <div class="custom-card">
            <div style="font-size: 0.85rem; color: #64748B; margin-bottom: 4px;">선택 장소 규격</div>
            <div style="font-size: 1.1rem; font-weight: bold; color: #0F172A; margin-bottom: 8px;">{st.session_state['venue']}</div>
            <div style="font-size: 0.85rem; color: #334155; line-height: 1.5;">
                • <b>부지 크기:</b> 가로 {venue_info['width_m']}m × 세로 {venue_info['height_m']}m<br>
                • <b>최대 권장 수용 인원:</b> 약 {venue_info['max_capacity']:,}명<br>
                • <b>공간 유형:</b> {venue_info['type']}<br>
                • <b>특징:</b> {venue_info['description']}
            </div>
        </div>
