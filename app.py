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
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* 전체 배경 및 폰트 - 라이트 모드 적용 */
    .stApp {
        background-color: #F8FAFC;
        color: #0F172A;
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }
    
    /* 상단 네비게이션 및 헤더 */
    div[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
    }
    div[data-testid="stSidebar"] * {
        color: #1E293B !important;
    }

    /* 카드 스타일링 */
    .custom-card {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
        border: 1px solid #E2E8F0;
        margin-bottom: 16px;
    }

    /* 우측 지표 카드 디자인 (이미지 매칭) */
    .metric-card-green {
        background: linear-gradient(135deg, #059669 0%, #10B981 100%);
        color: white;
        border-radius: 14px;
        padding: 16px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
    }

    .metric-card-yellow {
        background: linear-gradient(135deg, #D97706 0%, #F59E0B 100%);
        color: white;
        border-radius: 14px;
        padding: 16px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.2);
    }

    .metric-card-blue {
        background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
        color: white;
        border-radius: 14px;
        padding: 16px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
    }

    .pill-stat-blue {
        background-color: #EFF6FF;
        border: 1px solid #BFDBFE;
        color: #1D4ED8;
        border-radius: 12px;
        padding: 12px;
        text-align: center;
        font-weight: bold;
    }

    .pill-stat-yellow {
        background-color: #FEF3C7;
        border: 1px solid #FDE68A;
        color: #B45309;
        border-radius: 12px;
        padding: 12px;
        text-align: center;
        font-weight: bold;
    }

    .opt-badge {
        background-color: #065F46;
        color: #FFFFFF;
        padding: 10px 16px;
        border-radius: 20px;
        font-weight: bold;
        text-align: center;
        display: inline-block;
        width: 100%;
        box-shadow: 0 4px 10px rgba(6, 95, 70, 0.2);
    }

    /* 상단 버튼 스타일 */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    /* 입력 폼 투명 배경 */
    .stTextInput input, .stSelectbox select {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        color: #0F172A !important;
        border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

CHUNGNAM_VENUES = {
    "논산 시민공원 야외광장 (논산시)": {
        "type": "공원/야외", "address": "충청남도 논산시 관촉로 67",
        "width_m": 120, "height_m": 80, "max_capacity": 5000,
        "description": "탁 트인 잔디 광장과 산책로가 조성된 논산시 대표 야외 행사 공간"
    },
    "천안 유관순체육관 (천안시)": {
        "type": "체육관/실내", "address": "충청남도 천안시 서북구 번영로 208",
        "width_m": 60, "height_m": 40, "max_capacity": 3500,
        "description": "대형 실내 코트 및 가변석을 갖춘 실내 종합 스포츠 및 콘서트장"
    },
    "공주대학교 옥룡캠퍼스 체육관 (공주시)": {
        "type": "학교 체육관", "address": "충청남도 공주시 우금티로 753",
        "width_m": 50, "height_m": 32, "max_capacity": 1500,
        "description": "대학 교내 실내 행사, 학술대회 및 동아리 박람회용 실내 강당"
    },
    "아산 이순신종합운동장 체육관 (아산시)": {
        "type": "체육관/실내", "address": "충청남도 아산시 남부로 370-24",
        "width_m": 70, "height_m": 45, "max_capacity": 4000,
        "description": "국제 규격 경기장과 방대한 진출입 도로를 확보한 아산 대표 체육관"
    },
    "충남도청 내포신도시 잔디광장 (홍성군)": {
        "type": "공원/야외", "address": "충청남도 홍성군 홍북읍 충남대로 21",
        "width_m": 150, "height_m": 90, "max_capacity": 8000,
        "description": "도청 앞 초대형 수변 광장으로 가변 부스 배치가 용이한 대규모 부지"
    },
    "서산시민체육관 (서산시)": {
        "type": "체육관/실내", "address": "충청남도 서산시 안견로 361",
        "width_m": 55, "height_m": 35, "max_capacity": 2000,
        "description": "서산시 소재 구내 체육 행사 및 지역 주민 문화 축제 전용 체육관"
    }
}

# 기본 세션 상태 초기화
if 'current_nav' not in st.session_state:
    st.session_state['current_nav'] = '대시보드'
if 'selected_venue' not in st.session_state:
    st.session_state['selected_venue'] = "논산 시민공원 야외광장 (논산시)"
if 'event_name' not in st.session_state:
    st.session_state['event_name'] = "2026 충남 청춘 축제"
if 'event_purpose' not in st.session_state:
    st.session_state['event_purpose'] = "축제/공연"
if 'visitor_count' not in st.session_state:
    st.session_state['visitor_count'] = 5000
if 'budget' not in st.session_state:
    st.session_state['budget'] = "5,000만원"
if 'is_after_mode' not in st.session_state:
    st.session_state['is_after_mode'] = True  # 이전(Before) / 이후(After) 토글
if 'chat_messages' not in st.session_state:
    st.session_state['chat_messages'] = [
        {"role": "assistant", "content": "안녕하세요! AI 공간 설계 조교입니다. '푸드존을 남쪽으로 이동해줘' 또는 '화장실을 의료 센터 옆으로 옮겨줘'라고 명령해 보세요."}
    ]

with st.sidebar:
    st.markdown("### 🎪 **이벤트 아키텍트 AI**")
    st.caption("AI 기반 행사 자동 설계 및 디지털 트윈")
    st.divider()

    nav_options = ["대시보드", "이벤트 디자인", "디지털 트윈", "AI 시뮬레이션", "AI 보고서", "설정"]
    st.session_state['current_nav'] = st.radio("메뉴 선택", nav_options, index=nav_options.index(st.session_state['current_nav']))

    st.divider()
    st.markdown("#### 📍 충남 장소/체육관 선택")
    venue_choice = st.selectbox("장소 선택", list(CHUNGNAM_VENUES.keys()), index=list(CHUNGNAM_VENUES.keys()).index(st.session_state['selected_venue']))
    st.session_state['selected_venue'] = venue_choice
    
    custom_search = st.text_input("🔍 학교/체육관 직접 검색", placeholder="예: 천안 서여자중학교 체육관")
    if custom_search:
        st.info(f"💡 '{custom_search}' 장소의 평면 및 동선 규격을 적용합니다.")

    venue_data = CHUNGNAM_VENUES[st.session_state['selected_venue']]
    st.markdown(f"""
    <div style="background:#F1F5F9; padding:12px; border-radius:10px; font-size:0.85rem; border:1px solid #CBD5E1;">
        <div><b>유형:</b> {venue_data['type']}</div>
        <div><b>규격:</b> {venue_data['width_m']}m × {venue_data['height_m']}m</div>
        <div><b>수용 인원:</b> {venue_data['max_capacity']:,}명</div>
        <div style="color:#64748B; margin-top:4px;">{venue_data['description']}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("### 🏛️ AI 행사 공간 설계 대시보드")

# 상단 입력 필드 및 버튼 바 (이미지 상단 배치 매칭)
top_col1, top_col2, top_col3, top_col4, top_col5, top_col6 = st.columns([1.5, 1.2, 1.2, 1.0, 1.5, 1.6])

with top_col1:
    st.text_input("이벤트 이름", value=st.session_state['event_name'], key="input_ev_name")
with top_col2:
    st.selectbox("이벤트 목적", ["축제/공연", "박람회/전시", "학술/대회", "체육 대회"], key="input_ev_purpose")
with top_col3:
    st.number_input("예상 방문객 수", value=st.session_state['visitor_count'], step=500, key="input_ev_visitors")
with top_col4:
    st.text_input("예산", value=st.session_state['budget'], key="input_ev_budget")
with top_col5:
    st.selectbox("장소", list(CHUNGNAM_VENUES.keys()), index=0, key="input_ev_venue")
with top_col6:
    st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
    if st.button("✨ AI 이벤트 디자인 생성", type="primary", use_container_width=True):
        st.toast("AI가 최적화된 디지털 트윈 공간 조감도를 재구성했습니다!", icon="🚀")

st.divider()

if st.session_state['current_nav'] == "대시보드":
    
    col_center_canvas, col_right_metrics = st.columns([7.2, 2.8])

    # ------------------ [중앙 2.5D ISOMETRIC 디지털 트윈 캔버스] ------------------
    with col_center_canvas:
        
        # 이전/이후 모드 설정 및 캔버스 연동
        is_after = st.session_state['is_after_mode']

        canvas_js_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    background-color: #F8FAFC;
                    font-family: 'Pretendard', system-ui, sans-serif;
                    overflow: hidden;
                }}
                #canvasContainer {{
                    position: relative;
                    width: 100%;
                    height: 580px;
                    background: #FFFFFF;
                    border-radius: 20px;
                    border: 2px solid #E2E8F0;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.06);
                }}
                canvas {{
                    display: block;
                    width: 100%;
                    height: 100%;
                }}
                
                /* 상단 플로팅 배지 노드 (이미지 상의 노드들) */
                .node-badge {{
                    position: absolute;
                    background: #FFFFFF;
                    border: 1px solid #CBD5E1;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                    padding: 5px 12px;
                    border-radius: 20px;
                    font-size: 12px;
                    font-weight: bold;
                    color: #1E293B;
                    display: flex;
                    align-items: center;
                    gap: 6px;
                    z-index: 10;
                }}
                .node-dot {{
                    width: 8px;
                    height: 8px;
                    border-radius: 50%;
                    background-color: #3B82F6;
                }}
                .node-dot-red {{ background-color: #EF4444; }}

                /* 이전 / 이후 토글 스위치 (이미지 하단 매칭) */
                .toggle-container {{
                    position: absolute;
                    bottom: 16px;
                    left: 50%;
                    transform: translateX(-50%);
                    background: #FFFFFF;
                    border: 1px solid #CBD5E1;
                    box-shadow: 0 4px 16px rgba(0,0,0,0.1);
                    padding: 6px 16px;
                    border-radius: 30px;
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    font-size: 13px;
                    font-weight: bold;
                    z-index: 20;
                }}
                .switch {{
                    position: relative;
                    display: inline-block;
                    width: 44px;
                    height: 22px;
                }}
                .switch input {{ opacity: 0; width: 0; height: 0; }}
                .slider {{
                    position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0;
                    background-color: #CBD5E1; transition: .3s; border-radius: 22px;
                }}
                .slider:before {{
                    position: absolute; content: ""; height: 16px; width: 16px; left: 3px; bottom: 3px;
                    background-color: white; transition: .3s; border-radius: 50%;
                }}
                input:checked + .slider {{ background-color: #2563EB; }}
                input:checked + .slider:before {{ transform: translateX(22px); }}
            </style>
        </head>
        <body>
            <div id="canvasContainer">
                
                <!-- 이미지와 동일한 위치의 AI 플로팅 노드 라벨들 -->
                <div class="node-badge" style="top: 25px; left: 240px;">
                    <div class="node-dot"></div> 군중 예측
                </div>
                <div class="node-badge" style="top: 60px; right: 220px;">
                    <div class="node-dot"></div> AI 최적화
                </div>
                <div class="node-badge" style="bottom: 80px; left: 200px;">
                    <div class="node-dot node-dot-red"></div> 군중 예측 🚨
                </div>
                <div class="node-badge" style="bottom: 70px; right: 240px;">
                    <div class="node-dot"></div> 디지털 트윈
                </div>

                <canvas id="isoCanvas" width="950" height="580"></canvas>
            </div>

            <script>
                const canvas = document.getElementById('isoCanvas');
                const ctx = canvas.getContext('2d');
                
                let isAfterMode = {str(is_after).lower()};

                // 실시간 유입 군중 입자 설정
                const particles = [];
                const numParticles = 80;

                for (let i = 0; i < numParticles; i++) {{
                    particles.push({{
                        x: 520 + (Math.random() - 0.5) * 30,
                        y: 430 + (Math.random() - 0.5) * 20,
                        progress: Math.random(),
                        speed: 0.002 + Math.random() * 0.003,
                        targetIndex: Math.floor(Math.random() * 4)
                    }});
                }}

                // 2.5D Isometric 변환 좌표 계산 함수
                function isoProject(x, y, z) {{
                    const isoX = (x - y) * 0.75 + 475;
                    const isoY = (x + y) * 0.38 - z + 120;
                    return {{ x: isoX, y: isoY }};
                }}

                function drawIsometricBlock(x, y, w, h, z, colorTop, colorLeft, colorRight, label, icon) {{
                    const p1 = isoProject(x, y, z);
                    const p2 = isoProject(x + w, y, z);
                    const p3 = isoProject(x + w, y + h, z);
                    const p4 = isoProject(x, y + h, z);

                    const p1_b = isoProject(x, y, 0);
                    const p2_b = isoProject(x + w, y, 0);
                    const p3_b = isoProject(x + w, y + h, 0);
                    const p4_b = isoProject(x, y + h, 0);

                    // 좌측 면
                    ctx.fillStyle = colorLeft;
                    ctx.beginPath();
                    ctx.moveTo(p1.x, p1.y);
                    ctx.lineTo(p4.x, p4.y);
                    ctx.lineTo(p4_b.x, p4_b.y);
                    ctx.lineTo(p1_b.x, p1_b.y);
                    ctx.closePath();
                    ctx.fill();

                    // 우측 면
                    ctx.fillStyle = colorRight;
                    ctx.beginPath();
                    ctx.moveTo(p4.x, p4.y);
                    ctx.lineTo(p3.x, p3.y);
                    ctx.lineTo(p3_b.x, p3_b.y);
                    ctx.lineTo(p4_b.x, p4_b.y);
                    ctx.closePath();
                    ctx.fill();

                    // 상단 면
                    ctx.fillStyle = colorTop;
                    ctx.beginPath();
                    ctx.moveTo(p1.x, p1.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.lineTo(p3.x, p3.y);
                    ctx.lineTo(p4.x, p4.y);
                    ctx.closePath();
                    ctx.fill();
                    ctx.strokeStyle = "rgba(255,255,255,0.4)";
                    ctx.stroke();

                    // 텍스트 라벨
                    if (label) {{
                        const center = isoProject(x + w/2, y + h/2, z);
                        ctx.fillStyle = "#FFFFFF";
                        ctx.font = "bold 12px Pretendard, sans-serif";
                        ctx.textAlign = "center";
                        ctx.shadowColor = "rgba(0,0,0,0.5)";
                        ctx.shadowBlur = 4;
                        ctx.fillText((icon || "") + " " + label, center.x, center.y + 4);
                        ctx.shadowBlur = 0;
                    }}
                }}

                function drawScene() {{
                    ctx.clearRect(0, 0, canvas.width, canvas.height);

                    // 1. 외곽 3D Wall (이미지 상의 네이비 입체 외벽)
                    const wallColorTop = "#1E293B";
                    const wallColorLeft = "#0F172A";
                    const wallColorRight = "#334155";
                    drawIsometricBlock(0, 0, 480, 20, 40, wallColorTop, wallColorLeft, wallColorRight, "", "");
                    drawIsometricBlock(0, 0, 20, 360, 40, wallColorTop, wallColorLeft, wallColorRight, "", "");

                    // 2. 바닥 잔디/체육관 평면
                    const pGround1 = isoProject(20, 20, 0);
                    const pGround2 = isoProject(480, 20, 0);
                    const pGround3 = isoProject(480, 360, 0);
                    const pGround4 = isoProject(20, 360, 0);

                    ctx.fillStyle = "#E2E8F0";
                    ctx.beginPath();
                    ctx.moveTo(pGround1.x, pGround1.y);
                    ctx.lineTo(pGround2.x, pGround2.y);
                    ctx.lineTo(pGround3.x, pGround3.y);
                    ctx.lineTo(pGround4.x, pGround4.y);
                    ctx.closePath();
                    ctx.fill();

                    // 그리드 라인 (밝고 모던한 느낌)
                    ctx.strokeStyle = "#CBD5E1";
                    ctx.lineWidth = 1;
                    for (let step = 60; step < 460; step += 40) {{
                        const lineStart = isoProject(step, 20, 0);
                        const lineEnd = isoProject(step, 360, 0);
                        ctx.beginPath(); ctx.moveTo(lineStart.x, lineStart.y); ctx.lineTo(lineEnd.x, lineEnd.y); ctx.stroke();
                    }}

                    // 3. 주요 시설물 입체 배치 (이미지와 유사한 배치)
                    
                    // [무대/Stage] (북쪽 상단)
                    drawIsometricBlock(60, 40, 110, 60, 30, "#312E81", "#1E1B4B", "#4338CA", "무대", "🎭");

                    // [푸드 존 / Food Zone] (서쪽 - 이전 모드 시 병목 유발)
                    const foodGlowColor = isAfterMode ? "rgba(59, 130, 246, 0.25)" : "rgba(239, 68, 68, 0.4)";
                    const foodCenter = isoProject(100, 240, 0);
                    
                    // 혼잡도 Heatmap Glow
                    ctx.fillStyle = foodGlowColor;
                    ctx.beginPath();
                    ctx.arc(foodCenter.x, foodCenter.y, isAfterMode ? 50 : 80, 0, Math.PI * 2);
                    ctx.fill();

                    drawIsometricBlock(60, 220, 80, 70, 18, "#D97706", "#B45309", "#F59E0B", "푸드 존", "🍔");

                    // [부스 / Booths] (중앙 통로 단지)
                    for(let b = 0; b < 3; b++) {{
                        drawIsometricBlock(200, 100 + b*60, 50, 40, 15, "#2563EB", "#1D4ED8", "#3B82F6", b === 1 ? "부스" : "", "🎪");
                        drawIsometricBlock(270, 100 + b*60, 50, 40, 15, "#2563EB", "#1D4ED8", "#3B82F6", "", "");
                    }}

                    // [휴식 구역 / Rest Area] (동쪽 잔디 쉼터)
                    drawIsometricBlock(360, 40, 90, 80, 8, "#059669", "#047857", "#10B981", "휴식 구역", "☕");

                    // [의료 센터 / Medical]
                    drawIsometricBlock(280, 30, 60, 40, 16, "#059669", "#047857", "#34D399", "의료 센터", "🚑");

                    // [정보 센터 / Info]
                    drawIsometricBlock(220, 300, 50, 35, 12, "#D97706", "#B45309", "#FBBF24", "정보 센터", "ℹ️");

                    // [화장실 / Toilets]
                    drawIsometricBlock(380, 220, 60, 45, 14, "#475569", "#334155", "#64748B", "화장실", "🚻");

                    // [비상구 / Exits]
                    drawIsometricBlock(440, 140, 20, 40, 25, "#DC2626", "#991B1B", "#EF4444", "비상구", "🚨");

                    // 4. 동선 유도선 및 실시간 군중 입자 (Particles)
                    const targets = [
                        isoProject(115, 70, 0),   // 무대
                        isoProject(100, 255, 0),  // 푸드존
                        isoProject(235, 160, 0),  // 부스
                        isoProject(405, 80, 0)    // 휴식구역
                    ];

                    const startPos = isoProject(240, 340, 0);

                    particles.forEach(p => {{
                        p.progress += p.speed;
                        if (p.progress >= 1.0) p.progress = 0;

                        const target = targets[p.targetIndex];
                        const currX = startPos.x + (target.x - startPos.x) * p.progress;
                        const currY = startPos.y + (target.y - startPos.y) * p.progress;

                        ctx.beginPath();
                        ctx.arc(currX, currY, 3, 0, Math.PI * 2);
                        ctx.fillStyle = isAfterMode ? "#2563EB" : "#EF4444";
                        ctx.fill();
                    }});

                    requestAnimationFrame(drawScene);
                }}

                drawScene();
            </script>
        </body>
        </html>
        """

        components.html(canvas_js_code, height=600)

        # AI 실시간 자연어 명령 창
        with st.expander("💬 AI 대화형 공간 재배치 어시스턴트", expanded=True):
            chat_col1, chat_col2 = st.columns([8, 2])
            with chat_col1:
                cmd_input = st.text_input("원하는 배치를 자유롭게 명령하세요", placeholder="예: '푸드존을 남쪽으로 20m 이동해줘'", label_visibility="collapsed")
            with chat_col2:
                if st.button("배치 반영", type="primary", use_container_width=True):
                    if cmd_input:
                        st.session_state['chat_messages'].append({"role": "user", "content": cmd_input})
                        st.session_state['chat_messages'].append({"role": "assistant", "content": f"✨ **반영 완료:** '{cmd_input}' 명령에 따라 디지털 트윈 동선을 재계산했습니다."})
                        st.rerun()

            for msg in st.session_state['chat_messages'][-2:]:
                if msg["role"] == "user":
                    st.chat_message("user").write(msg["content"])
                else:
                    st.chat_message("assistant").write(msg["content"])

    # ------------------ [우측 실시간 핵심 지표 대시보드 (이미지 2 우측 매칭)] ------------------
    with col_right_metrics:
        
        st.markdown("#### 📊 실시간 공간 평가")

        # 1. 안전 점수 카드 (Green)
        st.markdown("""
        <div class="metric-card-green">
            <div>
                <div style="font-size:0.85rem; opacity:0.9;">🛡️ 안전 점수</div>
                <div style="font-size:0.75rem; opacity:0.8;">비상 대피로 확보</div>
            </div>
            <div style="font-size: 2.2rem; font-weight: 900;">94</div>
        </div>
        """, unsafe_allow_html=True)

        # 2. 접근성 카드 (Yellow/Amber)
        st.markdown("""
        <div class="metric-card-yellow">
            <div>
                <div style="font-size:0.85rem; opacity:0.9;">🚶‍♂️ 접근성</div>
                <div style="font-size:0.75rem; opacity:0.8;">주요 시설 간 거리</div>
            </div>
            <div style="font-size: 2.2rem; font-weight: 900;">96</div>
        </div>
        """, unsafe_allow_html=True)

        # 3. 흐름 효율성 카드 (Blue)
        st.markdown("""
        <div class="metric-card-blue">
            <div>
                <div style="font-size:0.85rem; opacity:0.9;">🔄 흐름 효율성</div>
                <div style="font-size:0.75rem; opacity:0.8;">병목 현상 방지 지수</div>
            </div>
            <div style="font-size: 2.2rem; font-weight: 900;">91</div>
        </div>
        """, unsafe_allow_html=True)

        # 4. 하단 서브 알약 지표 (대기 시간 / 예산 효율성)
        s_col1, s_col2 = st.columns(2)
        with s_col1:
            st.markdown("""
            <div class="pill-stat-blue">
                <div style="font-size:0.75rem; color:#3B82F6;">대기 시간</div>
                <div style="font-size:1.2rem; font-weight:bold;">-38%</div>
            </div>
            """, unsafe_allow_html=True)
        with s_col2:
            st.markdown("""
            <div class="pill-stat-yellow">
                <div style="font-size:0.75rem; color:#D97706;">예산 효율성</div>
                <div style="font-size:1.2rem; font-weight:bold;">+18%</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 5. AI 권장 사항 체크리스트
        st.markdown("""
        <div class="custom-card">
            <div style="font-weight: bold; font-size: 0.95rem; margin-bottom: 10px; color: #1E293B;">💡 AI 권장 사항</div>
            <ul style="padding-left: 18px; margin: 0; font-size: 0.85rem; color: #475569; line-height: 1.8;">
                <li>🚚 <b>푸드 존</b> 남쪽으로 이동 추천</li>
                <li>🏕️ <b>휴식 구역</b> 2개 추가 권장</li>
                <li>🎪 <b>무대 입구</b> 진입로 확장</li>
                <li>ℹ️ <b>정보 센터</b> 정문 전면 이전</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # 6. 최적화 완료 상태 바
        st.markdown("""
        <div class="opt-badge">
            🟢 93% 최적화된 레이아웃
        </div>
        """, unsafe_allow_html=True)

elif st.session_state['current_nav'] == "이벤트 디자인":
    st.markdown("### 🎨 AI 이벤트 디자인 가이드")
    st.info("이벤트 콘셉트 및 브랜드 테마 색상을 설정할 수 있습니다.")

elif st.session_state['current_nav'] == "디지털 트윈":
    st.markdown("### 🌐 디지털 트윈 현장 정밀 스캔")
    st.success("충남 지역 선택 장소의 GIS 지형 정보 및 실내 평면도가 정밀하게 연동되어 있습니다.")

elif st.session_state['current_nav'] == "AI 시뮬레이션":
    st.markdown("### 🏃‍♂️ AI 군중 동선 시뮬레이션 상세 분석")
    st.caption("시간대별 인파 밀집도 그래프 및 병목 구역 예측 데이터입니다.")
    
    df_sim = pd.DataFrame({
        "구역": ["무대 정면", "푸드 존", "체험 부스", "휴게실", "화장실"],
        "평균 체류 시간(분)": [45, 25, 18, 30, 5],
        "혼잡 위험도(%)": [85, 62, 40, 20, 35]
    })
    fig = px.bar(df_sim, x="구역", y="혼잡 위험도(%)", color="혼잡 위험도(%)", color_continuous_scale="Reds", title="구역별 피크 타임 혼잡 위험도")
    st.plotly_chart(fig, use_container_width=True)

elif st.session_state['current_nav'] == "AI 보고서":
    st.markdown("### 📋 AI 공간 최적화 종합 보고서")
    st.caption("상사 및 관계 부서 제출용 자동 생성 보고서입니다.")
    st.download_button("📄 PDF 보고서 다운로드 (가상)", data="Report content", file_name="event_layout_report.pdf")

elif st.session_state['current_nav'] == "설정":
    st.markdown("### ⚙️ 시스템 및 시뮬레이션 설정")
    st.slider("시뮬레이션 인파 파티클 속도", 1.0, 5.0, 2.5)
