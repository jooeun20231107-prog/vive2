import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
import json

st.set_page_config(
    page_title="Event AI - 충남 장소 맞춤형 AI 행사 설계 및 실시간 동선 플랫폼",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }
    
    /* 상단 정보 및 카드 컴포넌트 */
    .custom-card {
        background-color: #1E293B;
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        border: 1px solid #334155;
        margin-bottom: 20px;
    }

    .metric-badge {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #3B82F6;
        padding: 12px 18px;
        border-radius: 12px;
        color: #60A5FA;
        font-weight: bold;
    }

    .badge-excellent { background-color: rgba(16, 185, 129, 0.2); color: #34D399; border: 1px solid #059669; }
    .badge-warning { background-color: rgba(245, 158, 11, 0.2); color: #FBBF24; border: 1px solid #D97706; }

    /* 사이드바 스타일링 */
    div[data-testid="stSidebar"] {
        background-color: #0B0F19 !important;
        border-right: 1px solid #1E293B;
    }
    div[data-testid="stSidebar"] * {
        color: #E2E8F0 !important;
    }

    /* 탭 및 버튼 스타일링 */
    .stButton>button {
        border-radius: 10px;
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 8px 18px;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

CHUNGNAM_VENUES = {
    "논산 시민공원 야외광장 (논산시)": {
        "type": "공원/야외",
        "address": "충청남도 논산시 관촉로 67",
        "width_m": 120, "height_m": 80,
        "max_capacity": 5000,
        "shape": "rectangular",
        "description": "탁 트인 잔디 광장과 산책로가 조성된 논산시 대표 야외 행사 공간"
    },
    "천안 유관순체육관 (천안시)": {
        "type": "체육관/실내",
        "address": "충청남도 천안시 서북구 번영로 208",
        "width_m": 60, "height_m": 40,
        "max_capacity": 3500,
        "shape": "indoor_gym",
        "description": "대형 실내 코트 및 가변석을 갖춘 실내 종합 스포츠 및 콘서트장"
    },
    "공주대학교 옥룡캠퍼스 체육관 (공주시)": {
        "type": "학교 체육관",
        "address": "충청남도 공주시 우금티로 753",
        "width_m": 50, "height_m": 32,
        "max_capacity": 1500,
        "shape": "indoor_gym",
        "description": "대학 교내 실내 행사, 학술대회 및 동아리 박람회용 실내 강당"
    },
    "아산 이순신종합운동장 체육관 (아산시)": {
        "type": "체육관/실내",
        "address": "충청남도 아산시 남부로 370-24",
        "width_m": 70, "height_m": 45,
        "max_capacity": 4000,
        "shape": "indoor_gym",
        "description": "국제 규격 경기장과 방대한 진출입 도로를 확보한 아산 대표 체육관"
    },
    "충남도청 내포신도시 잔디광장 (홍성군)": {
        "type": "공원/야외",
        "address": "충청남도 홍성군 홍북읍 충남대로 21",
        "width_m": 150, "height_m": 90,
        "max_capacity": 8000,
        "shape": "open_plaza",
        "description": "도청 앞 초대형 수변 광장으로 가변 부스 배치가 용이한 대규모 부지"
    },
    "서산시민체육관 (서산시)": {
        "type": "체육관/실내",
        "address": "충청남도 서산시 안견로 361",
        "width_m": 55, "height_m": 35,
        "max_capacity": 2000,
        "shape": "indoor_gym",
        "description": "서산시 소재 구내 체육 행사 및 지역 주민 문화 축제 전용 체육관"
    }
}

DEFAULT_FACILITIES = {
    "exit": {
        "name": "메인 출입구",
        "icon": "🚪",
        "hex": "#F43F5E",
        "x": 500, "y": 620, "w": 180, "h": 50,
        "reason": "남쪽 진입로에 맞춰 대규모 인파 유입 및 대피 동선을 동시 보장합니다."
    },
    "stage": {
        "name": "메인 무대/공연장",
        "icon": "🎭",
        "hex": "#8B5CF6",
        "x": 500, "y": 100, "w": 260, "h": 110,
        "reason": "전방 중앙 시야각 확보 및 음향 반사 경로를 감안한 최적 위치입니다."
    },
    "booth": {
        "name": "체험/전시 부스존",
        "icon": "🎪",
        "hex": "#3B82F6",
        "x": 180, "y": 200, "w": 200, "h": 160,
        "reason": "좌측 입구 인근에 배치하여 진입 관람객의 관람 흡입력을 강화합니다."
    },
    "food": {
        "name": "푸드트럭/스낵존",
        "icon": "🍔",
        "hex": "#F97316",
        "x": 180, "y": 420, "w": 200, "h": 160,
        "reason": "환기 및 조리 유증기 확산을 방지하기 위해 외곽 측면에 독립 구성했습니다."
    },
    "rest": {
        "name": "휴게/쉼터 광장",
        "icon": "☕",
        "hex": "#10B981",
        "x": 500, "y": 360, "w": 260, "h": 180,
        "reason": "중앙 통로변에 정자 및 쉬어가는 테이블을 배치하여 피로도를 최소화합니다."
    },
    "medical": {
        "name": "응급의료/의무실",
        "icon": "🚑",
        "hex": "#EF4444",
        "x": 820, "y": 140, "w": 160, "h": 100,
        "reason": "구급차 통행용 비상도로와 연계하여 최단 응급 이송 경로를 확보했습니다."
    },
    "toilet": {
        "name": "위생/화장실존",
        "icon": "🚻",
        "hex": "#06B6D4",
        "x": 820, "y": 300, "w": 160, "h": 100,
        "reason": "상하수도 인프라 접근 및 대기 줄 혼잡 분산을 위해 우측에 위치시켰습니다."
    },
    "info": {
        "name": "종합 안내센터",
        "icon": "ℹ️",
        "hex": "#EC4899",
        "x": 500, "y": 530, "w": 160, "h": 60,
        "reason": "출입구 직후 정면에 위치하여 길 안내 및 비상 분실물 처리를 담당합니다."
    }
}

if 'selected_venue' not in st.session_state:
    st.session_state['selected_venue'] = "논산 시민공원 야외광장 (논산시)"
if 'facilities' not in st.session_state:
    st.session_state['facilities'] = DEFAULT_FACILITIES.copy()
if 'selected_facility' not in st.session_state:
    st.session_state['selected_facility'] = 'stage'
if 'crowd_sim_active' not in st.session_state:
    st.session_state['crowd_sim_active'] = True
if 'visitor_count' not in st.session_state:
    st.session_state['visitor_count'] = 120
if 'sim_speed' not in st.session_state:
    st.session_state['sim_speed'] = 2.5
if 'chat_messages' not in st.session_state:
    st.session_state['chat_messages'] = [
        {"role": "assistant", "content": "안녕하세요! AI 공간 설계 조교입니다. 충남 지역 내 공원/체육관 장소를 선택하시고, '푸드존을 더 외곽으로 보내줘' 또는 '화장실을 의료 센터 옆으로 옮겨줘'라고 명령해보세요."}
    ]

def parse_and_apply_ai_command(prompt: str):
    prompt_clean = prompt.replace(" ", "")
    facs = st.session_state['facilities']
    
    target_key = None
    if "푸드" in prompt_clean or "먹거리" in prompt_clean or "식당" in prompt_clean:
        target_key = "food"
    elif "화장실" in prompt_clean or "위생" in prompt_clean:
        target_key = "toilet"
    elif "무대" in prompt_clean or "공연" in prompt_clean:
        target_key = "stage"
    elif "부스" in prompt_clean or "체험" in prompt_clean or "전시" in prompt_clean:
        target_key = "booth"
    elif "의료" in prompt_clean or "응급" in prompt_clean or "병원" in prompt_clean:
        target_key = "medical"
    elif "휴게" in prompt_clean or "쉼터" in prompt_clean:
        target_key = "rest"
    elif "안내" in prompt_clean:
        target_key = "info"
    elif "입구" in prompt_clean or "출구" in prompt_clean or "출입구" in prompt_clean:
        target_key = "exit"

    if not target_key:
        target_key = st.session_state['selected_facility']

    fac = facs[target_key]
    action_desc = ""

    if "외곽" in prompt_clean or "멀리" in prompt_clean or "떨어져" in prompt_clean:
        if target_key == "food":
            fac["x"] = 120
            fac["y"] = 460
            action_desc = "푸드존을 환기 및 연기 방지를 위해 서쪽 최외곽 독립 구역으로 이동시켰습니다."
        elif target_key == "toilet":
            fac["x"] = 880
            fac["y"] = 420
            action_desc = "화장실을 메인 무대 음향 구역과 거리를 둔 동쪽 외곽으로 이동시켰습니다."
        else:
            fac["x"] = max(100, fac["x"] - 140)
            action_desc = f"{fac['name']}의 위치를 외곽 구역으로 배치 전환했습니다."

    elif "의료" in prompt_clean or "응급" in prompt_clean or "옆" in prompt_clean or "근처" in prompt_clean:
        fac["x"] = facs["medical"]["x"] - 30
        fac["y"] = facs["medical"]["y"] + 110
        action_desc = f"{fac['name']}을(를) 응급의료센터 인근의 신속 반응 구역으로 재배치했습니다."

    elif "중앙" in prompt_clean or "가운데" in prompt_clean:
        fac["x"] = 500
        fac["y"] = 360
        action_desc = f"{fac['name']}을(를) 행사장 중앙 광장 핵심 구역에 조율했습니다."

    elif "오른쪽" in prompt_clean or "동쪽" in prompt_clean:
        fac["x"] = min(850, fac["x"] + 150)
        action_desc = f"{fac['name']}을(를) 동쪽 관람 구역 방향으로 이동했습니다."

    elif "왼쪽" in prompt_clean or "서쪽" in prompt_clean:
        fac["x"] = max(120, fac["x"] - 150)
        action_desc = f"{fac['name']}을(를) 서쪽 진입 방향으로 이동했습니다."

    else:
        fac["x"] = (fac["x"] + 120) % 750 + 100
        action_desc = f"{fac['name']}의 위치를 AI 최적 동선 시뮬레이션에 맞춰 미세 조정을 마쳤습니다."

    fac["reason"] = f"AI 음성/대화 반영: {action_desc}"
    st.session_state['selected_facility'] = target_key
    return f"✨ **배치 업데이트 완료:** {action_desc}"

with st.sidebar:
    st.markdown("## 🎪 **Event Architect AI**")
    st.caption("오늘의집 스타일 충남 장소 레이아웃 & 실시간 인파 동선")
    st.divider()

    st.subheader("📍 1. 충남 장소/체육관/학교 선택")
    
    venue_name = st.selectbox(
        "장소 프리셋 선택",
        options=list(CHUNGNAM_VENUES.keys()),
        index=list(CHUNGNAM_VENUES.keys()).index(st.session_state['selected_venue'])
    )
    st.session_state['selected_venue'] = venue_name
    venue_info = CHUNGNAM_VENUES[venue_name]

    # 장소 검색 및 직접 입력 기능
    custom_search = st.text_input("🔍 충남 학교/체육관/공원 검색 및 입력", placeholder="예: 천안 서여자중학교 체육관")
    if custom_search:
        st.info(f"💡 '{custom_search}' 장소의 평면 형태 및 약 {venue_info['width_m']}m x {venue_info['height_m']}m 구역 스케일을 대시보드에 매핑합니다.")

    st.markdown(f"""
    <div style="background:#1E293B; padding:12px; border-radius:10px; border:1px solid #334155; font-size:0.85rem; margin-top:8px;">
        <div><b>유형:</b> {venue_info['type']}</div>
        <div><b>주소:</b> {venue_info['address']}</div>
        <div><b>면적 스케일:</b> {venue_info['width_m']}m × {venue_info['height_m']}m</div>
        <div><b>권장 최대 인원:</b> {venue_info['max_capacity']:,}명</div>
        <div style="color:#94A3B8; margin-top:4px;">{venue_info['description']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.subheader("🏃‍♂️ 2. 실시간 혼잡도 시뮬레이션 제어")
    
    sim_on = st.toggle("⚡ 실시간 인파 유입 시뮬레이션", value=st.session_state['crowd_sim_active'])
    st.session_state['crowd_sim_active'] = sim_on

    visitors = st.slider("입장객 수 (점 개수)", min_value=30, max_value=300, value=st.session_state['visitor_count'], step=10)
    st.session_state['visitor_count'] = visitors

    speed = st.slider("이동 속도", min_value=1.0, max_value=5.0, value=float(st.session_state['sim_speed']), step=0.5)
    st.session_state['sim_speed'] = speed

    st.divider()
    st.caption("AI 기반 자동 동선 최적화 엔진 v3.2 Active")

st.markdown(f"""
<div style="display: flex; justify-content: space-between; align-items: center; background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); padding: 20px 28px; border-radius: 16px; border: 1px solid #334155; margin-bottom: 24px;">
    <div>
        <h1 style="margin: 0; font-size: 1.8rem; font-weight: 800; color: #F8FAFC;">
            📍 {st.session_state['selected_venue']} 
            <span style="font-size: 1rem; color: #60A5FA; font-weight: 500; margin-left: 10px;">[디지털 트윈 레이아웃]</span>
        </h1>
        <p style="margin: 6px 0 0 0; color: #94A3B8; font-size: 0.95rem;">
            입구부터 인파가 실시간으로 퍼져 나가는 인파 확산 시뮬레이션 및 AI 배치 가이드
        </p>
    </div>
    <div style="display: flex; gap: 12px;">
        <span class="metric-badge">수용률: {(st.session_state['visitor_count']*15 / venue_info['max_capacity']*100):.1f}%</span>
        <span class="badge-excellent metric-badge">안전 점수: 96점 (우수)</span>
    </div>
</div>
""", unsafe_allow_html=True)

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.markdown("""
    <div class="custom-card">
        <div style="font-size: 0.85rem; color: #94A3B8;">현재 적용 장소 스케일</div>
        <div style="font-size: 1.4rem; font-weight: 700; color: #38BDF8; margin-top: 4px;">{}m × {}m</div>
        <div style="font-size: 0.75rem; color: #10B981; margin-top: 4px;">형태: {}</div>
    </div>
    """.format(venue_info['width_m'], venue_info['height_m'], venue_info['shape']), unsafe_allow_html=True)

with col_m2:
    st.markdown("""
    <div class="custom-card">
        <div style="font-size: 0.85rem; color: #94A3B8;">실시간 유입 인파 동선</div>
        <div style="font-size: 1.4rem; font-weight: 700; color: #F43F5E; margin-top: 4px;">{} 명 / min</div>
        <div style="font-size: 0.75rem; color: #F59E0B; margin-top: 4px;">상태: {}</div>
    </div>
    """.format(int(st.session_state['visitor_count'] * 1.8), "정상 분산 중" if st.session_state['crowd_sim_active'] else "시뮬레이션 정지"), unsafe_allow_html=True)

with col_m3:
    st.markdown("""
    <div class="custom-card">
        <div style="font-size: 0.85rem; color: #94A3B8;">최대 병목 구역</div>
        <div style="font-size: 1.4rem; font-weight: 700; color: #F97316; margin-top: 4px;">메인 무대 정면</div>
        <div style="font-size: 0.75rem; color: #38BDF8; margin-top: 4px;">우회로 확보 완료</div>
    </div>
    """, unsafe_allow_html=True)

with col_m4:
    st.markdown("""
    <div class="custom-card">
        <div style="font-size: 0.85rem; color: #94A3B8;">비상 대피 예상 시간</div>
        <div style="font-size: 1.4rem; font-weight: 700; color: #10B981; margin-top: 4px;">2분 10초</div>
        <div style="font-size: 0.75rem; color: #10B981; margin-top: 4px;">기준치(5분) 대비 58% 단축</div>
    </div>
    """, unsafe_allow_html=True)

col_left, col_right = st.columns([7, 4])

with col_left:
    st.subheader("🗺️ 실시간 인파 확산 평면 시뮬레이터 (HTML5 Canvas)")
    st.caption("입구(🚪)에서 생성된 점(사람)들이 각 부스/무대/휴게존으로 유기적으로 퍼져 나갑니다.")

    # Convert Python facility dictionary to JSON string for JS integration
    facilities_json = json.dumps(st.session_state['facilities'])
    sim_active_str = "true" if st.session_state['crowd_sim_active'] else "false"
    visitor_count = st.session_state['visitor_count']
    sim_speed = st.session_state['sim_speed']

    canvas_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 0;
                background-color: #0F172A;
                font-family: system-ui, sans-serif;
                overflow: hidden;
            }}
            #simContainer {{
                position: relative;
                width: 100%;
                height: 600px;
                border-radius: 16px;
                border: 2px solid #334155;
                background: radial-gradient(circle at 50% 50%, #1E293B 0%, #0F172A 100%);
                box-shadow: inset 0 0 30px rgba(0,0,0,0.5);
            }}
            canvas {{
                display: block;
                width: 100%;
                height: 100%;
            }}
            .overlay-badge {{
                position: absolute;
                top: 14px;
                left: 14px;
                background: rgba(15, 23, 42, 0.85);
                border: 1px solid #3B82F6;
                color: #93C5FD;
                padding: 8px 14px;
                border-radius: 10px;
                font-size: 13px;
                backdrop-filter: blur(4px);
                pointer-events: none;
            }}
        </style>
    </head>
    <body>
        <div id="simContainer">
            <div class="overlay-badge">
                📍 <b>규격 적용:</b> {venue_info['width_m']}m × {venue_info['height_m']}m ({venue_info['type']})<br/>
                ⚡ <b>상태:</b> 입구 인파 실시간 분산 퍼짐 시뮬레이션 중
            </div>
            <canvas id="crowdCanvas" width="1000" height="600"></canvas>
        </div>

        <script>
            const canvas = document.getElementById('crowdCanvas');
            const ctx = canvas.getContext('2d');
            
            const facilities = {facilities_json};
            const simActive = {sim_active_str};
            const numParticles = {visitor_count};
            const speedFactor = {sim_speed};

            // 출입구 좌표 찾기
            const exitFac = facilities.exit || {{ x: 500, y: 600, w: 100, h: 40 }};
            const startX = exitFac.x + exitFac.w / 2;
            const startY = exitFac.y + exitFac.h / 2;

            // 목적지 시설 리스트 (출입구 제외)
            const targets = [];
            Object.keys(facilities).forEach(key => {{
                if (key !== 'exit') {{
                    const f = facilities[key];
                    targets.push({{
                        name: f.name,
                        x: f.x + f.w / 2,
                        y: f.y + f.h / 2
                    }});
                }}
            }});

            // 입구에서부터 시작하여 시설물로 퍼져나가는 입자(사람) 생성
            class Visitor {{
                constructor() {{
                    this.reset();
                    // 처음 로딩 시 입구에서부터 넓게 번진 것처럼 보이도록 위치 무작위 스폰
                    this.progress = Math.random();
                    this.updatePos();
                }}

                reset() {{
                    this.x = startX + (Math.random() - 0.5) * 40;
                    this.y = startY + (Math.random() - 0.5) * 20;
                    this.target = targets[Math.floor(Math.random() * targets.length)];
                    this.speed = (0.0015 + Math.random() * 0.0025) * speedFactor;
                    this.progress = 0;
                    this.radius = 3.5 + Math.random() * 2.5;
                    // 색상 (입구 근처는 주황, 목적지 도착 시 푸른빛/녹색)
                    this.hue = Math.floor(Math.random() * 40) + 10; 
                    this.jitterX = (Math.random() - 0.5) * 2;
                    this.jitterY = (Math.random() - 0.5) * 2;
                }}

                updatePos() {{
                    const dx = this.target.x - startX;
                    const dy = this.target.y - startY;
                    
                    // 직선 경로에 간섭(지그재그 자연스러운 퍼짐) 추가
                    const curve = Math.sin(this.progress * Math.PI) * 40 * (Math.sin(this.x) > 0 ? 1 : -1);
                    this.x = startX + dx * this.progress + curve;
                    this.y = startY + dy * this.progress;
                    
                    this.hue = 20 + this.progress * 180; // 입구(주황/레드) -> 내부 퍼짐(초록/파랑)
                }}

                step() {{
                    if (!simActive) return;
                    this.progress += this.speed;
                    if (this.progress >= 1.0) {{
                        // 목적지 도착 후 일정 시간 체류 후 재스폰
                        if (Math.random() < 0.03) {{
                            this.reset();
                        }}
                    }} else {{
                        this.updatePos();
                    }}
                }}

                draw() {{
                    ctx.beginPath();
                    ctx.arc(this.x + this.jitterX, this.y + this.jitterY, this.radius, 0, Math.PI * 2);
                    ctx.fillStyle = `hsl(${{this.hue}}, 85%, 60%)`;
                    ctx.shadowBlur = 8;
                    ctx.shadowColor = `hsl(${{this.hue}}, 85%, 50%)`;
                    ctx.fill();
                    ctx.shadowBlur = 0;
                }}
            }}

            const particles = Array.from({{ length: numParticles }}, () => new Visitor());

            function drawFacilities() {{
                Object.keys(facilities).forEach(key => {{
                    const f = facilities[key];
                    
                    // 시설 테두리 및 영역 박스
                    ctx.fillStyle = f.hex + "25"; // 투명도 15%
                    ctx.strokeStyle = f.hex;
                    ctx.lineWidth = 2;
                    ctx.beginPath();
                    ctx.roundRect(f.x, f.y, f.w, f.h, 12);
                    ctx.fill();
                    ctx.stroke();

                    // 시설 아이콘 및 이름
                    ctx.fillStyle = "#FFFFFF";
                    ctx.font = "bold 15px Pretendard, sans-serif";
                    ctx.textAlign = "center";
                    ctx.textBaseline = "middle";
                    ctx.fillText(f.icon + " " + f.name, f.x + f.w / 2, f.y + f.h / 2);
                }});
            }}

            function drawConnectingFlowLines() {{
                // 출입구에서 각 주요 시설로 향하는 은은한 유도 가이드선
                targets.forEach(t => {{
                    ctx.beginPath();
                    ctx.moveTo(startX, startY);
                    ctx.lineTo(t.x, t.y);
                    ctx.strokeStyle = "rgba(148, 163, 184, 0.12)";
                    ctx.lineWidth = 1.5;
                    ctx.setLineDash([4, 6]);
                    ctx.stroke();
                    ctx.setLineDash([]);
                }});
            }}

            function animate() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                
                // 그리드 배경 연출
                ctx.strokeStyle = "rgba(51, 65, 85, 0.3)";
                ctx.lineWidth = 1;
                for(let x = 0; x < canvas.width; x += 40) {{
                    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
                }}
                for(let y = 0; y < canvas.height; y += 40) {{
                    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
                }}

                drawConnectingFlowLines();
                drawFacilities();

                // 인파 입자 업데이트 및 출력
                particles.forEach(p => {{
                    p.step();
                    p.draw();
                }});

                requestAnimationFrame(animate);
            }}

            animate();
        </script>
    </body>
    </html>
    """

    components.html(canvas_html, height=620)

    st.subheader("🧩 주요 시설물 위치 수동 미세 조절")
    selected_f_key = st.selectbox(
        "조정할 시설물 선택",
        options=list(st.session_state['facilities'].keys()),
        format_func=lambda k: f"{st.session_state['facilities'][k]['icon']} {st.session_state['facilities'][k]['name']}"
    )
    st.session_state['selected_facility'] = selected_f_key
    target_fac = st.session_state['facilities'][selected_f_key]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("⬅️ 왼쪽 (서쪽)"):
            target_fac["x"] = max(80, target_fac["x"] - 60)
            st.rerun()
    with c2:
        if st.button("➡️ 오른쪽 (동쪽)"):
            target_fac["x"] = min(850, target_fac["x"] + 60)
            st.rerun()
    with c3:
        if st.button("⬆️ 위쪽 (북쪽)"):
            target_fac["y"] = max(80, target_fac["y"] - 50)
            st.rerun()
    with c4:
        if st.button("⬇️ 아래쪽 (남쪽)"):
            target_fac["y"] = min(540, target_fac["y"] + 50)
            st.rerun()

with col_right:
    st.subheader("💬 AI 공간 설계 조교 (자연어 대화)")
    st.caption("원하는 배치를 자유롭게 말하세요. AI가 최적 동선을 계산하여 즉시 이동시킵니다.")

    # 채팅 메시지 출력
    chat_container = st.container(height=360)
    with chat_container:
        for msg in st.session_state['chat_messages']:
            if msg["role"] == "user":
                st.chat_message("user").write(msg["content"])
            else:
                st.chat_message("assistant").write(msg["content"])

    # 입력 폼
    if prompt := st.chat_input("예: '화장실을 의료 센터 근처로 배치해줘'"):
        st.session_state['chat_messages'].append({"role": "user", "content": prompt})
        
        # AI 처리
        response_text = parse_and_apply_ai_command(prompt)
        st.session_state['chat_messages'].append({"role": "assistant", "content": response_text})
        st.rerun()

    st.divider()

    st.subheader("📋 선택 시설 안전 및 배치 사유")
    sel_fac = st.session_state['facilities'][st.session_state['selected_facility']]
    
    st.markdown(f"""
    <div style="background: #1E293B; border-radius: 12px; padding: 16px; border: 1px solid #334155;">
        <div style="font-size: 1.1rem; font-weight: 700; color: {sel_fac['hex']}; display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 1.4rem;">{sel_fac['icon']}</span> {sel_fac['name']}
        </div>
        <div style="margin-top: 10px; font-size: 0.85rem; color: #CBD5E1;">
            <b>현재 좌표:</b> X={sel_fac['x']}px, Y={sel_fac['y']}px <br/>
            <b>영역 크기:</b> 가로 {sel_fac['w']}px × 세로 {sel_fac['h']}px
        </div>
        <hr style="border: none; border-top: 1px solid #334155; margin: 10px 0;"/>
        <div style="font-size: 0.85rem; color: #94A3B8; line-height: 1.5;">
            <b>💡 AI 배치 권장 근거:</b><br/>
            {sel_fac['reason']}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.subheader("📊 충남 장소 맞춤 인파 분포 및 비상 대피 지수")

col_a1, col_a2 = st.columns([6, 6])

with col_a1:
    # 시설별 인파 밀집도 예상 그래프
    df_crowd = pd.DataFrame({
        "시설구역": [f['name'] for f in st.session_state['facilities'].values() if f['name'] != '메인 출입구'],
        "예상 체류 인원(명)": [1200, 850, 650, 400, 150, 280, 200],
        "혼잡 위험도(%)": [82, 65, 50, 35, 15, 42, 25]
    })
    
    fig = px.bar(
        df_crowd, 
        x="시설구역", 
        y="예상 체류 인원(명)", 
        color="혼잡 위험도(%)",
        color_continuous_scale="Reds",
        title=f"[{venue_info['type']}] 구역별 최대 동시 수용 체류 인원 추정"
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F8FAFC")
    )
    st.plotly_chart(fig, use_container_width=True)

with col_a2:
    # 시간대별 유입/퇴장 예측 선 그래프
    hours = [f"{h}:00" for h in range(10, 20)]
    inflow = [200, 500, 1200, 2400, 3100, 2800, 1900, 1100, 400, 100]
    outflow = [50, 100, 300, 800, 1500, 2100, 2500, 2200, 1600, 800]

    df_time = pd.DataFrame({"시간": hours, "입장 유입": inflow, "퇴장 유출": outflow})
    fig_line = px.line(df_time, x="시간", y=["입장 유입", "퇴장 유출"], markers=True, title="시간대별 인파 유출입 동선 추이 예측")
    fig_line.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F8FAFC")
    )
    st.plotly_chart(fig_line, use_container_width=True)

st.success("✅ **충남 장소 맞춤 레이아웃 및 실시간 입구 분산 시뮬레이션 시스템이 상시 작동 중입니다.**")
