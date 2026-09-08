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
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'home'  # 'home', 'dashboard', 'report', 'settings', 'login'
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_name' not in st.session_state:
    st.session_state['user_name'] = "홍길동 기획관"
if 'design_generated' not in st.session_state:
    st.session_state['design_generated'] = False
if 'simulation_active' not in st.session_state:
    st.session_state['simulation_active'] = True
if 'selected_facility' not in st.session_state:
    st.session_state['selected_facility'] = "무대"

# 기본 이벤트 정보 상태
if 'event_name' not in st.session_state:
    st.session_state['event_name'] = "2026 충남 청춘 문화 축제"
if 'event_purpose' not in st.session_state:
    st.session_state['event_purpose'] = "축제/공연"
if 'visitor_count' not in st.session_state:
    st.session_state['visitor_count'] = 5000
if 'budget' not in st.session_state:
    st.session_state['budget'] = "5,000만원"
if 'venue' not in st.session_state:
    st.session_state['venue'] = "논산 시민공원 야외광장 (논산시)"

if 'chat_messages' not in st.session_state:
    st.session_state['chat_messages'] = [
        {"role": "assistant", "content": "안녕하세요! AI 공간 설계 어시스턴트입니다. 원하시는 배치를 말씀하시면 디지털 트윈 상에서 즉시 최적화해 드립니다."}
    ]

# 충남 장소 데이터베이스
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
    in_col1, in_col2, in_col3, in_col4, in_col5, in_col6 = st.columns([1.5, 1.2, 1.2, 1.0, 1.5, 1.6])
    
    with in_col1:
        st.session_state['event_name'] = st.text_input("이벤트 이름", value=st.session_state['event_name'])
    with in_col2:
        st.session_state['event_purpose'] = st.selectbox("이벤트 목적", ["축제/공연", "박람회/전시", "학술/대회", "체육 대회"])
    with in_col3:
        st.session_state['visitor_count'] = st.number_input("예상 방문객 수", value=st.session_state['visitor_count'], step=500)
    with in_col4:
        st.session_state['budget'] = st.text_input("예산", value=st.session_state['budget'])
    with in_col5:
        st.session_state['venue'] = st.selectbox("장소", list(CHUNGNAM_VENUES.keys()))
    with in_col6:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        if st.button("✨ AI 이벤트 디자인 생성", type="primary", use_container_width=True):
            st.session_state['design_generated'] = True
            st.toast("AI가 장소 규격에 맞춰 최적의 3D 공간 배치를 완료했습니다!", icon="🚀")
            st.rerun()

    st.divider()

    # 메인 캔버스 및 레이아웃 영역
    dash_left, dash_right = st.columns([7, 3])

    with dash_left:
        # 디자인 생성 전 빈 프레임과 생성 후 3D Isometric 캔버스 분기
        if not st.session_state['design_generated']:
            st.markdown("""
            <div style="height: 520px; border: 2px dashed #CBD5E1; border-radius: 20px; display: flex; flex-direction: column; justify-content: center; align-items: center; background-color: #FFFFFF;">
                <div style="font-size: 4rem; color: #94A3B8; margin-bottom: 12px;">📐</div>
                <h3 style="color: #64748B; margin-bottom: 8px;">빈 공간 상태입니다</h3>
                <p style="color: #94A3B8; font-size: 0.95rem;">상단의 이벤트 정보 입력 후 <b>[✨ AI 이벤트 디자인 생성]</b> 버튼을 누르면 디지털 트윈 3D 배치가 수행됩니다.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            sim_flag = str(st.session_state['simulation_active']).lower()
            
            # 3D Isometric HTML/JS Canvas
            canvas_code = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ margin: 0; padding: 0; background: #F8FAFC; font-family: system-ui, sans-serif; overflow: hidden; }}
                    #canvasContainer {{
                        position: relative; width: 100%; height: 520px; background: #FFFFFF;
                        border-radius: 20px; border: 2px solid #E2E8F0; box-shadow: 0 8px 24px rgba(0,0,0,0.05);
                    }}
                    canvas {{ display: block; width: 100%; height: 100%; }}
                    .node-badge {{
                        position: absolute; background: #FFFFFF; border: 1px solid #CBD5E1;
                        box-shadow: 0 4px 10px rgba(0,0,0,0.08); padding: 4px 10px; border-radius: 16px;
                        font-size: 11px; font-weight: bold; color: #1E293B; display: flex; align-items: center; gap: 5px;
                    }}
                    .node-dot {{ width: 7px; height: 7px; border-radius: 50%; background-color: #3B82F6; }}
                </style>
            </head>
            <body>
                <div id="canvasContainer">
                    <div class="node-badge" style="top: 20px; left: 220px;"><div class="node-dot"></div> 군중 동선 예측</div>
                    <div class="node-badge" style="top: 50px; right: 200px;"><div class="node-dot"></div> AI 자동 최적화</div>
                    <div class="node-badge" style="bottom: 40px; right: 220px;"><div class="node-dot"></div> 디지털 트윈 연동</div>

                    <canvas id="isoCanvas" width="900" height="520"></canvas>
                </div>

                <script>
                    const canvas = document.getElementById('isoCanvas');
                    const ctx = canvas.getContext('2d');
                    let simActive = {sim_flag};

                    const particles = [];
                    for (let i = 0; i < 70; i++) {{
                        particles.push({{
                            progress: Math.random(),
                            speed: 0.002 + Math.random() * 0.003,
                            targetIndex: Math.floor(Math.random() * 4)
                        }});
                    }}

                    function isoProject(x, y, z) {{
                        return {{
                            x: (x - y) * 0.72 + 450,
                            y: (x + y) * 0.36 - z + 110
                        }};
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

                        ctx.fillStyle = colorLeft;
                        ctx.beginPath();
                        ctx.moveTo(p1.x, p1.y); ctx.lineTo(p4.x, p4.y); ctx.lineTo(p4_b.x, p4_b.y); ctx.lineTo(p1_b.x, p1_b.y);
                        ctx.closePath(); ctx.fill();

                        ctx.fillStyle = colorRight;
                        ctx.beginPath();
                        ctx.moveTo(p4.x, p4.y); ctx.lineTo(p3.x, p3.y); ctx.lineTo(p3_b.x, p3_b.y); ctx.lineTo(p4_b.x, p4_b.y);
                        ctx.closePath(); ctx.fill();

                        ctx.fillStyle = colorTop;
                        ctx.beginPath();
                        ctx.moveTo(p1.x, p1.y); ctx.lineTo(p2.x, p2.y); ctx.lineTo(p3.x, p3.y); ctx.lineTo(p4.x, p4.y);
                        ctx.closePath(); ctx.fill();
                        ctx.strokeStyle = "rgba(255,255,255,0.5)"; ctx.stroke();

                        if (label) {{
                            const center = isoProject(x + w/2, y + h/2, z);
                            ctx.fillStyle = "#FFFFFF";
                            ctx.font = "bold 11px system-ui, sans-serif";
                            ctx.textAlign = "center";
                            ctx.fillText((icon || "") + " " + label, center.x, center.y + 4);
                        }}
                    }}

                    function render() {{
                        ctx.clearRect(0, 0, canvas.width, canvas.height);

                        // 외벽
                        drawIsometricBlock(0, 0, 460, 18, 35, "#1E293B", "#0F172A", "#334155", "", "");
                        drawIsometricBlock(0, 0, 18, 340, 35, "#1E293B", "#0F172A", "#334155", "", "");

                        // 바닥
                        const g1 = isoProject(18, 18, 0); const g2 = isoProject(460, 18, 0);
                        const g3 = isoProject(460, 340, 0); const g4 = isoProject(18, 340, 0);
                        ctx.fillStyle = "#E2E8F0";
                        ctx.beginPath(); ctx.moveTo(g1.x, g1.y); ctx.lineTo(g2.x, g2.y); ctx.lineTo(g3.x, g3.y); ctx.lineTo(g4.x, g4.y); ctx.closePath(); ctx.fill();

                        // 격자
                        ctx.strokeStyle = "#CBD5E1"; ctx.lineWidth = 1;
                        for(let s = 60; s < 440; s += 40) {{
                            const ls = isoProject(s, 18, 0); const le = isoProject(s, 340, 0);
                            ctx.beginPath(); ctx.moveTo(ls.x, ls.y); ctx.lineTo(le.x, le.y); ctx.stroke();
                        }}

                        // 주요 시설
                        drawIsometricBlock(50, 35, 110, 60, 28, "#312E81", "#1E1B4B", "#4338CA", "무대", "🎭");
                        drawIsometricBlock(50, 210, 80, 70, 18, "#D97706", "#B45309", "#F59E0B", "푸드 존", "🍔");
                        
                        for(let b=0; b<3; b++) {{
                            drawIsometricBlock(190, 90 + b*55, 45, 38, 14, "#2563EB", "#1D4ED8", "#3B82F6", b===1 ? "부스" : "", "🎪");
                            drawIsometricBlock(255, 90 + b*55, 45, 38, 14, "#2563EB", "#1D4ED8", "#3B82F6", "", "");
                        }}

                        drawIsometricBlock(350, 35, 85, 75, 8, "#059669", "#047857", "#10B981", "휴식 구역", "☕");
                        drawIsometricBlock(270, 28, 55, 38, 15, "#059669", "#047857", "#34D399", "의료 센터", "🚑");
                        drawIsometricBlock(210, 280, 50, 35, 12, "#D97706", "#B45309", "#FBBF24", "정보 센터", "ℹ️");
                        drawIsometricBlock(370, 200, 60, 42, 14, "#475569", "#334155", "#64748B", "화장실", "🚻");
                        drawIsometricBlock(425, 130, 18, 38, 22, "#DC2626", "#991B1B", "#EF4444", "비상구", "🚨");

                        // 인파 시뮬레이션 파티클
                        if (simActive) {{
                            const targets = [
                                isoProject(105, 65, 0), isoProject(90, 245, 0),
                                isoProject(222, 150, 0), isoProject(392, 72, 0)
                            ];
                            const startPos = isoProject(235, 320, 0);

                            particles.forEach(p => {{
                                p.progress += p.speed;
                                if (p.progress >= 1.0) p.progress = 0;
                                const t = targets[p.targetIndex];
                                const cx = startPos.x + (t.x - startPos.x) * p.progress;
                                const cy = startPos.y + (t.y - startPos.y) * p.progress;
                                ctx.beginPath(); ctx.arc(cx, cy, 3, 0, Math.PI * 2);
                                ctx.fillStyle = "#2563EB"; ctx.fill();
                            }});
                        }}

                        requestAnimationFrame(render);
                    }}
                    render();
                </script>
            </body>
            </html>
            """
            components.html(canvas_code, height=540)

        # 캔버스 아래 시뮬레이션 및 시설 클릭 버튼
        st.markdown("#### 🎯 시설 배치 사유 확인 및 시뮬레이션 제어")
        
        sim_col1, sim_col2 = st.columns([4, 6])
        with sim_col1:
            if st.button("🏃‍♂️ AI 군중 동선 시뮬레이션 (ON/OFF)", type="secondary", use_container_width=True):
                st.session_state['simulation_active'] = not st.session_state['simulation_active']
                st.rerun()

        st.caption("아래 글자를 누르시면 해당 시설의 AI 자동 배치 근거 요약을 확인하실 수 있습니다:")
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
        # 우측: AI 요약 및 실시간 평가
        selected = st.session_state['selected_facility']
        fac_info = FACILITY_REASONING.get(selected, FACILITY_REASONING["무대"])

        st.markdown(f"#### 💡 선택 시설: {fac_info['icon']} {selected}")
        st.markdown(f"""
        <div class="reasoning-box">
            <div style="font-weight: bold; font-size: 1rem; margin-bottom: 6px;">📌 AI 배치 사유 요약</div>
            <div style="font-weight: 600; font-size: 0.9rem; color: #1E40AF; margin-bottom: 8px;">{fac_info['title']}</div>
            <div style="font-size: 0.85rem; line-height: 1.6; color: #334155;">{fac_info['reason']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        st.markdown("#### 📊 실시간 공간 지표 평가")
        
        st.markdown("""
        <div class="custom-card" style="border-left: 6px solid #10B981;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="font-size:0.85rem; color:#64748B;">🛡️ 안전 점수</div>
                    <div style="font-size:0.75rem; color:#94A3B8;">비상 대피로 확보 지수</div>
                </div>
                <div style="font-size:2rem; font-weight:bold; color:#059669;">94</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="custom-card" style="border-left: 6px solid #F59E0B;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="font-size:0.85rem; color:#64748B;">🚶‍♂️ 접근성</div>
                    <div style="font-size:0.75rem; color:#94A3B8;">주요 시설 평균 거동 거리</div>
                </div>
                <div style="font-size:2rem; font-weight:bold; color:#D97706;">96</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="custom-card" style="border-left: 6px solid #3B82F6;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="font-size:0.85rem; color:#64748B;">🔄 흐름 효율성</div>
                    <div style="font-size:0.75rem; color:#94A3B8;">병목 방지 및 시야율</div>
                </div>
                <div style="font-size:2rem; font-weight:bold; color:#2563EB;">91</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        p_col1, p_col2 = st.columns(2)
        with p_col1:
            st.markdown("""
            <div class="pill-stat">
                <div style="font-size:0.75rem; color:#64748B;">대기 시간</div>
                <div style="font-size:1.1rem; color:#2563EB;">-38% 감소</div>
            </div>
            """, unsafe_allow_html=True)
        with p_col2:
            st.markdown("""
            <div class="pill-stat">
                <div style="font-size:0.75rem; color:#64748B;">예산 효율성</div>
                <div style="font-size:1.1rem; color:#D97706;">+18% 절감</div>
            </div>
            """, unsafe_allow_html=True)

elif st.session_state['current_page'] == 'report':
    st.markdown("### 📋 직장 상사 및 정식 제출용 AI 보고서")
    st.caption("이벤트 아키텍트 AI가 자동으로 작성한 행사 공간 설계 및 디지털 트윈 종합 보고서입니다.")

    st.markdown("""
    <div style="background:#FFFFFF; border:1px solid #CBD5E1; padding:30px; border-radius:16px; box-shadow:0 4px 20px rgba(0,0,0,0.05);">
        <div style="text-align:center; border-bottom:2px solid #0F172A; padding-bottom:16px; margin-bottom:24px;">
            <h2 style="margin:0; color:#0F172A;">[결재 보고서] 행사 공간 설계 및 디지털 트윈 최적화 안</h2>
            <p style="color:#64748B; margin-top:8px;">기획안 작성자: 홍길동 기획관 | 작성 일시: 2026년 9월 9일</p>
        </div>
        
        <table style="width:100%; border-collapse:collapse; margin-bottom:20px; font-size:0.9rem;">
            <tr style="background:#F1F5F9;">
                <td style="padding:10px; border:1px solid #CBD5E1; font-weight:bold; width:20%;">행사명</td>
                <td style="padding:10px; border:1px solid #CBD5E1;">""" + st.session_state['event_name'] + """</td>
                <td style="padding:10px; border:1px solid #CBD5E1; font-weight:bold; width:20%;">행사 목적</td>
                <td style="padding:10px; border:1px solid #CBD5E1;">""" + st.session_state['event_purpose'] + """</td>
            </tr>
            <tr>
                <td style="padding:10px; border:1px solid #CBD5E1; font-weight:bold;">예상 방문객 수</td>
                <td style="padding:10px; border:1px solid #CBD5E1;">""" + f"{st.session_state['visitor_count']:,}" + """ 명</td>
                <td style="padding:10px; border:1px solid #CBD5E1; font-weight:bold;">설정 예산</td>
                <td style="padding:10px; border:1px solid #CBD5E1;">""" + st.session_state['budget'] + """</td>
            </tr>
            <tr style="background:#F1F5F9;">
                <td style="padding:10px; border:1px solid #CBD5E1; font-weight:bold;">대상 장소</td>
                <td style="padding:10px; border:1px solid #CBD5E1;" colspan="3">""" + st.session_state['venue'] + """</td>
            </tr>
        </table>

        <h4>1. AI 디지털 트윈 최적화 요약</h4>
        <p style="font-size:0.9rem; color:#334155; line-height:1.7;">
            본 설계안은 군중 밀집도 예측 파티클 알고리즘을 기반으로 무대, 푸드존, 체험 부스, 휴식 구역 및 비상구를 최적 배치했습니다. 
            기존 수동 배치 대비 <b>대기 시간을 38% 감소</b>시키고 <b>안전 대피 지수를 94점</b>으로 대폭 개선하였습니다.
        </p>

        <h4>2. 주요 핵심 지표</h4>
        <ul>
            <li><b>안전 점수:</b> 94점 (비상구 2개소 분산 배치 및 폭 4m 진출입로 확보)</li>
            <li><b>접근성 평가:</b> 96점 (의료 센터 및 정보 센터 중심 연계)</li>
            <li><b>동선 효율성:</b> 91점 (2열 도보 스트리트 단지 구성으로 병목 현상 해소)</li>
        </ul>

        <h4>3. 상사 결재 및 종합 의견</h4>
        <p style="font-size:0.9rem; color:#475569; background:#F8FAFC; padding:12px; border-radius:8px;">
            "본 공간 배치는 국토교통부 행사 안전 가이드라인을 충족하며, 충남 지역 장소 규격에 맞추어 현장 실무 적용 준비가 완료되었습니다."
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.br = st.markdown("<br>", unsafe_allow_html=True)
    r_col1, r_col2 = st.columns(2)
    with r_col1:
        st.download_button("📄 PDF 정식 보고서 다운로드", data=f"AI Event Layout Report for {st.session_state['event_name']}", file_name="event_layout_report.pdf", type="primary", use_container_width=True)
    with r_col2:
        if st.button("🏠 홈으로 돌아가기", use_container_width=True):
            st.session_state['current_page'] = 'home'
            st.rerun()

elif st.session_state['current_page'] == 'settings':
    st.markdown("### ⚙️ 시스템 및 로그인 정보 설정")

    st.markdown("""
    <div class="custom-card">
        <h4>👤 계정 및 사용자 프로필</h4>
    </div>
    """, unsafe_allow_html=True)

    set_col1, set_col2 = st.columns(2)
    with set_col1:
        st.session_state['user_name'] = st.text_input("사용자 이름/직급", value=st.session_state['user_name'])
        st.text_input("소속 기관/부서", value="충청남도 행사기획과")
    with set_col2:
        st.text_input("이메일 주소", value="planner@chungnam.go.kr")
        st.selectbox("권한 등급", ["기획관 (최고 관리자)", "실무 담당자", "게스트"])

    st.divider()

    st.markdown("#### 🎮 시뮬레이션 파라미터")
    st.slider("인파 흐름 시뮬레이션 파티클 속도", 1.0, 5.0, 2.5)
    st.toggle("고해상도 3D Isometric 랜더링 사용", value=True)

    st.divider()

    if st.session_state['logged_in']:
        if st.button("🚪 로그아웃", type="secondary"):
            st.session_state['logged_in'] = False
            st.toast("로그아웃 되었습니다.")
            st.session_state['current_page'] = 'home'
            st.rerun()
    else:
        if st.button("🔑 로그인 페이지로 이동", type="primary"):
            st.session_state['current_page'] = 'login'
            st.rerun()

elif st.session_state['current_page'] == 'login':
    st.markdown("### 🔑 이벤트 아키텍트 AI 로그인 / 회원가입")

    login_card = st.container()
    with login_card:
        l_col1, l_col2, l_col3 = st.columns([2, 3, 2])
        with l_col2:
            st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
            st.text_input("아이디 (이메일)", value="planner@chungnam.go.kr")
            st.text_input("비밀번호", type="password", value="••••••••")
            
            if st.button("로그인 실행", type="primary", use_container_width=True):
                st.session_state['logged_in'] = True
                st.toast("성공적으로 로그인되었습니다!", icon="✅")
                st.session_state['current_page'] = 'dashboard'
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
