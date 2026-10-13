import streamlit as st
import streamlit.components.v1 as components

# Streamlit 페이지 설정
st.set_page_config(
    page_title="이벤트 온 (Event-On) - AI 행사 자동 설계 플랫폼",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 스타일 정의
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

    /* Streamlit 버튼 커스텀 */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = True
if 'username' not in st.session_state:
    st.session_state['username'] = "주은님"

# 사이드바 구성
with st.sidebar:
    if st.button("🎪 이벤트 온 (Event-On)", key="logo_btn", use_container_width=True, type="primary"):
        st.session_state['page'] = 'home'
        st.rerun()

    st.caption("AI 기반 행사 공간 자동 설계 플랫폼")
    st.divider()

    page_selection = st.radio(
        "메뉴 이동",
        ["🏠 홈 화면", "📊 AI 행사 설계 대시보드", "⚙️ 설계 프로세스", "⚙️ 시스템 설정"],
        index=["home", "dashboard", "process", "settings"].index(st.session_state['page']) if st.session_state['page'] in ["home", "dashboard", "process", "settings"] else 0
    )

    if page_selection == "🏠 홈 화면":
        st.session_state['page'] = 'home'
    elif page_selection == "📊 AI 행사 설계 대시보드":
        st.session_state['page'] = 'dashboard'
    elif page_selection == "⚙️ 설계 프로세스":
        st.session_state['page'] = 'process'
    elif page_selection == "⚙️ 시스템 설정":
        st.session_state['page'] = 'settings'

    st.divider()

    if st.session_state['logged_in']:
        st.markdown(f"👤 **{st.session_state['username']}** 님 (총괄 기획)")
        if st.button("로그아웃", key="sidebar_logout", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

# 상단 헤더 영역
top_col1, top_col2 = st.columns([3, 1])
with top_col1:
    st.title("🎪 이벤트 온 (Event-On)")
with top_col2:
    st.markdown("<div style='text-align: right; padding-top: 10px;'>", unsafe_allow_html=True)
    if st.session_state['logged_in']:
        with st.popover(f"👤 {st.session_state['username']}"):
            st.write(f"**{st.session_state['username']}** (총괄 기획자)")
            st.caption("이메일: user@event-on.ai")
            st.divider()
            if st.button("설정 관리", key="pop_settings"):
                st.session_state['page'] = 'settings'
                st.rerun()
            if st.button("로그아웃", key="pop_logout"):
                st.session_state['logged_in'] = False
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ==========================================
# 1. 홈 화면 (Home Page)
# ==========================================
if st.session_state['page'] == 'home':
    st.markdown("## 🚀 시작할 메뉴를 선택하세요")
    st.caption("카드나 하단 버튼을 클릭하면 해당 작업 스튜디오로 이동합니다.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_dash, col_proc = st.columns(2)

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
                예산, 목적, 예상 방문객을 입력하면 실시간 2D/3D 디지털 트윈 조감도를 생성합니다.<br>
                대화형 AI 어시스턴트와 시간대별 시뮬레이션으로 최적의 행사장 배치를 완성하세요.
            </p>
        </div>
        """
        st.markdown(dash_card_html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📊 AI 행사 설계 대시보드 시작하기", key="btn_click_dash", type="primary", use_container_width=True):
            st.session_state['page'] = 'dashboard'
            st.rerun()

    with col_proc:
        proc_card_html = """
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
            <h1 style="font-size: 3rem; margin: 0 0 12px 0;">⚙️</h1>
            <h2 style="color: #065F46; margin: 0 0 14px 0; font-size: 1.55rem;">AI 설계 프로세스 및 메커니즘</h2>
            <p style="color: #475569; font-size: 1.02rem; line-height: 1.65; margin: 0;">
                기획부터 최종 배치안 도출까지의 다목적 최적화(Multi-objective Optimization) 과정을 살펴봅니다.<br>
                군중 동선 예측, XAI(설명 가능한 AI) 설계 이유 및 안전성 평가 체계를 확인하세요.
            </p>
        </div>
        """
        st.markdown(proc_card_html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⚙️ AI 설계 프로세스 확인하기", key="btn_click_proc", type="secondary", use_container_width=True):
            st.session_state['page'] = 'process'
            st.rerun()

# ==========================================
# 2. 대시보드 화면 (Dashboard Page) - 고도화된 웹앱 연동
# ==========================================
elif st.session_state['page'] == 'dashboard':
    st.markdown("## 📊 AI 디지털 트윈 공간 설계 대시보드")
    st.caption("디지털 트윈 및 실시간 군중 밀집도 시뮬레이션을 활용한 지능형 행사 자동 설계 플랫폼입니다.")

    # HTML/JS 기반 고도화된 캔버스 대시보드 임베드
    EVENT_AI_HTML = r"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Event On - AI 행사장 설계 시스템</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
    *{box-sizing:border-box;margin:0;padding:0;}
    body{
      font-family:"Pretendard Variable", Pretendard, sans-serif;
      color:#1e293b;
      background:#f8fafc;
      overflow-x:hidden;
      padding:10px;
    }
    button,input,select,textarea{font:inherit;}
    button{cursor:pointer;transition:all 0.2s ease;}

    .dashboard-container{
      display:flex;
      flex-direction:column;
      gap:16px;
    }
    
    /* Top Header Strip */
    .info-strip{
      background:#ffffff;
      border:1px solid #e2e8f0;
      border-radius:16px;
      padding:12px 18px;
      display:flex;
      align-items:center;
      justify-content:space-between;
      flex-wrap:wrap;
      gap:12px;
      box-shadow:0 2px 8px rgba(0,0,0,0.02);
    }
    .info-strip-group{
      display:flex;
      align-items:center;
      gap:16px;
      flex-wrap:wrap;
    }
    .info-box{
      display:flex;
      align-items:center;
      gap:8px;
      padding-right:12px;
      border-right:1px solid #f1f5f9;
    }
    .info-box:last-child{border-right:none;}
    .info-box-icon{
      width:32px;
      height:32px;
      border-radius:8px;
      background:#eff6ff;
      color:#2563eb;
      display:grid;
      place-items:center;
      font-size:14px;
    }
    .info-box-text label{display:block;font-size:10px;color:#64748b;font-weight:700;}
    .info-box-text span{font-size:12.5px;font-weight:800;color:#0f172a;}

    /* Main Dashboard Grids */
    .dashboard-main-grid{
      display:grid;
      grid-template-columns: 1.5fr 0.9fr 1fr;
      gap:16px;
    }
    @media(max-width: 1100px){
      .dashboard-main-grid{grid-template-columns: 1fr;}
    }

    /* Cards */
    .card-panel{
      background:#ffffff;
      border:1px solid #e2e8f0;
      border-radius:16px;
      padding:16px;
      box-shadow:0 2px 8px rgba(0,0,0,0.02);
      display:flex;
      flex-direction:column;
    }
    .card-head{
      font-size:14px;
      font-weight:800;
      color:#0f172a;
      margin-bottom:12px;
      display:flex;
      justify-content:space-between;
      align-items:center;
    }
    .card-badge{
      font-size:10.5px;
      background:#eff6ff;
      color:#2563eb;
      padding:3px 8px;
      border-radius:12px;
      font-weight:700;
    }

    /* Canvas Wrap */
    .map-wrap{
      position:relative;
      width:100%;
      height:360px;
      background:#1e293b;
      border-radius:12px;
      overflow:hidden;
      border:1px solid #334155;
    }
    #venueCanvas, #heatmapCanvas, #peopleCanvas, #container3D{
      position:absolute;
      inset:0;
      width:100%;
      height:100%;
    }
    #heatmapCanvas{z-index:5;opacity:0.85;pointer-events:none;}
    #peopleCanvas{z-index:10;pointer-events:none;}
    #container3D{z-index:15;display:none;background:#0f172a;}

    /* Legend */
    .map-legend-overlay{
      position:absolute;
      left:10px;
      bottom:10px;
      z-index:20;
      background:rgba(255,255,255,0.92);
      backdrop-filter:blur(6px);
      padding:8px 12px;
      border-radius:10px;
      font-size:10.5px;
      border:1px solid #e2e8f0;
      box-shadow:0 4px 12px rgba(0,0,0,0.1);
      display:grid;
      grid-template-columns:repeat(2, 1fr);
      gap:4px 10px;
    }
    .legend-item{display:flex;align-items:center;gap:5px;font-weight:700;color:#334155;}
    .legend-dot{width:8px;height:8px;border-radius:2px;}

    .map-controls-bar{
      display:flex;
      justify-content:space-between;
      align-items:center;
      margin-top:10px;
      gap:8px;
      flex-wrap:wrap;
    }
    .btn-secondary{
      background:#f1f5f9;
      color:#334155;
      border:1px solid #cbd5e1;
      padding:6px 12px;
      border-radius:8px;
      font-size:11.5px;
      font-weight:700;
    }
    .btn-secondary:hover{background:#e2e8f0;}
    .btn-warning{
      background:#fef3c7;
      color:#b45309;
      border:1px solid #fde68a;
      padding:6px 12px;
      border-radius:8px;
      font-size:11.5px;
      font-weight:700;
    }
    .btn-warning.active{background:#f59e0b;color:#fff;}
    .btn-danger{
      background:#fee2e2;
      color:#b91c1c;
      border:1px solid #fca5a5;
      padding:6px 12px;
      border-radius:8px;
      font-size:11.5px;
      font-weight:700;
    }
    .btn-danger.active{background:#ef4444;color:#fff;}

    /* Timeline */
    .timeline-container{
      background:#f8fafc;
      border:1px solid #e2e8f0;
      border-radius:12px;
      padding:10px 14px;
      margin-bottom:12px;
      display:flex;
      align-items:center;
      gap:12px;
    }
    .timeline-slider{flex:1;accent-color:#2563eb;cursor:pointer;}
    .time-badge{background:#2563eb;color:#fff;font-weight:800;font-size:12px;padding:4px 10px;border-radius:20px;min-width:70px;text-align:center;}

    /* Score Table */
    .score-tbl{width:100%;border-collapse:collapse;font-size:12px;margin-bottom:12px;}
    .score-tbl th,.score-tbl td{padding:8px 6px;text-align:left;border-bottom:1px solid #f1f5f9;}
    .score-tbl th{color:#64748b;font-weight:700;font-size:11px;}
    .grade-badge{padding:2px 8px;border-radius:10px;font-weight:800;font-size:10.5px;display:inline-block;}
    .gb-excel{background:#dcfce7;color:#15803d;}
    .gb-good{background:#e0f2fe;color:#0369a1;}

    /* AI Chat Assistant */
    .main-ai-assistant{
      background:linear-gradient(135deg, #f8fafc, #eff6ff);
      border:1.5px solid #bfdbfe;
      border-radius:16px;
      padding:16px;
      margin-bottom:16px;
    }
    .main-ai-header{display:flex;align-items:center;gap:8px;font-size:14px;font-weight:800;color:#1e3a8a;margin-bottom:10px;}
    .main-ai-chatbox{
      background:#ffffff;
      border:1px solid #cbd5e1;
      border-radius:10px;
      padding:10px 12px;
      height:90px;
      overflow-y:auto;
      font-size:12px;
      margin-bottom:10px;
      display:flex;
      flex-direction:column;
      gap:6px;
    }
    .chat-msg-ai{background:#eff6ff;color:#1e40af;padding:6px 10px;border-radius:8px;align-self:flex-start;max-width:85%;line-height:1.4;}
    .chat-msg-user{background:#2563eb;color:#ffffff;padding:6px 10px;border-radius:8px;align-self:flex-end;max-width:85%;line-height:1.4;}
    .main-ai-inputgroup{display:flex;gap:8px;}
    .main-ai-inputgroup input{flex:1;padding:8px 12px;border:1px solid #cbd5e1;border-radius:8px;font-size:12px;outline:none;}
    .btn-primary-custom{
      background:linear-gradient(135deg, #2563eb, #1d4ed8);
      color:#ffffff;border:none;padding:8px 16px;border-radius:8px;font-weight:800;font-size:12px;
    }
    </style>
    </head>
    <body>

    <div class="dashboard-container">

      <!-- AI Assistant Panel -->
      <div class="main-ai-assistant">
        <div class="main-ai-header">
          <span>🤖 AI 메인 어시스턴트 (실시간 레이아웃 제어)</span>
          <span style="font-size:11px;color:#3b82f6;font-weight:600;">— 실시간 명령어를 통해 배치도를 즉시 재구성할 수 있습니다.</span>
        </div>
        <div class="main-ai-chatbox" id="mainAiChatBox">
          <div class="chat-msg-ai">
            안녕하세요 주은님! 원하시는 부스 추가나 배치 수정 사항을 말씀해 주시면 디지털 트윈에 즉시 반영합니다.
          </div>
        </div>
        <div class="main-ai-inputgroup">
          <input type="text" id="mainAiInput" placeholder="예: 친환경 굿즈 팝업스토어를 추가하고 응급 부스를 중앙으로 이동해줘" onkeypress="if(event.key==='Enter') sendMainAiMsg()">
          <button class="btn-primary-custom" onclick="sendMainAiMsg()">보내기</button>
        </div>
      </div>

      <!-- Timeline Controller -->
      <div class="timeline-container">
        <span style="font-size:12px;font-weight:800;color:#0f172a;">⏰ 시간별 관람객 시뮬레이션:</span>
        <button class="btn-secondary" id="btnTimelinePlay" onclick="toggleTimelinePlay()">▶ 시간 재생</button>
        <input type="range" id="timeSlider" class="timeline-slider" min="10" max="20" step="1" value="14" oninput="updateTimeSimulation(this.value)">
        <div class="time-badge" id="timeDisplay">14:00</div>
        <span style="font-size:11px;color:#64748b;font-weight:600;" id="timeDesc">관람 인원 피크 타임 (공연 및 체험)</span>
      </div>

      <!-- Info Strip -->
      <div class="info-strip">
        <div class="info-strip-group">
          <div class="info-box"><div class="info-box-icon">📌</div><div class="info-box-text"><label>행사명</label><span>2026 청춘 페스티벌</span></div></div>
          <div class="info-box"><div class="info-box-icon">🏞️</div><div class="info-box-text"><label>장소</label><span>서울 올림픽공원 잔디마당</span></div></div>
          <div class="info-box"><div class="info-box-icon">👥</div><div class="info-box-text"><label>예상 관람객</label><span>5,000명</span></div></div>
          <div class="info-box"><div class="info-box-icon">💰</div><div class="info-box-text"><label>예산 규모</label><span>5,000만원</span></div></div>
        </div>
      </div>

      <!-- Main Dashboard Grid -->
      <div class="dashboard-main-grid">

        <!-- 1. Digital Twin Canvas Map -->
        <div class="card-panel">
          <div class="card-head">
            <span>🗺️ 행사장 배치도 (디지털 트윈 렌더링)</span>
            <button class="btn-secondary" id="btnToggle3D" onclick="toggle3DView()">🧊 3D 입체뷰 보기</button>
          </div>
          <div class="map-wrap" id="mapWrap">
            <canvas id="venueCanvas"></canvas>
            <canvas id="peopleCanvas"></canvas>
            <div id="container3D"></div>
            <div class="map-legend-overlay">
              <div class="legend-item"><span class="legend-dot" style="background:#8b5cf6;"></span> 공연장</div>
              <div class="legend-item"><span class="legend-dot" style="background:#3b82f6;"></span> 체험부스</div>
              <div class="legend-item"><span class="legend-dot" style="background:#f59e0b;"></span> 푸드존</div>
              <div class="legend-item"><span class="legend-dot" style="background:#10b981;"></span> 휴식공간</div>
              <div class="legend-item"><span class="legend-dot" style="background:#ef4444;"></span> 응급의료</div>
              <div class="legend-item"><span class="legend-dot" style="background:#2563eb;"></span> 화장실</div>
            </div>
          </div>
          <div class="map-controls-bar">
            <div style="display:flex;gap:6px;">
              <button class="btn-secondary" id="btnToggleSim" onclick="toggleSim()">▶ 시뮬레이션 시작</button>
              <button class="btn-warning" id="btnRain" onclick="toggleRainEnv()">🌧️ 우천 모드</button>
              <button class="btn-danger" id="btnEmergency" onclick="triggerEmergencyEnv()">🚨 응급환자 후송</button>
            </div>
            <span style="font-size:11px;color:#64748b;font-weight:700;" id="simTimer">상태: 대기중</span>
          </div>
        </div>

        <!-- 2. Density Heatmap -->
        <div class="card-panel">
          <div class="card-head">
            <span>🔥 시간별 군중 밀집도 Heatmap</span>
            <span class="card-badge" id="envBadge">일반 상태</span>
          </div>
          <div class="map-wrap">
            <canvas id="heatmapCanvas"></canvas>
          </div>
          <div style="display:flex;justify-content:space-around;font-size:10px;color:#64748b;margin-top:10px;font-weight:700;">
            <span style="color:#10b981;">🟢 원활</span>
            <span style="color:#eab308;">🟡 보통</span>
            <span style="color:#f97316;">🟠 혼잡</span>
            <span style="color:#ef4444;">🔴 위험</span>
          </div>
        </div>

        <!-- 3. AI Evaluation -->
        <div class="card-panel">
          <div class="card-head"><span>💡 AI 평가 결과 & XAI</span></div>
          <table class="score-tbl">
            <thead><tr><th>평가 항목</th><th>점수</th><th>등급</th></tr></thead>
            <tbody>
              <tr><td>비상 안전성</td><td>95점</td><td><span class="grade-badge gb-excel">매우 우수</span></td></tr>
              <tr><td>동선 효율성</td><td>92점</td><td><span class="grade-badge gb-excel">매우 우수</span></td></tr>
              <tr><td>접근성</td><td>88점</td><td><span class="grade-badge gb-good">우수</span></td></tr>
              <tr><td>혼잡도 분산</td><td>90점</td><td><span class="grade-badge gb-excel">매우 우수</span></td></tr>
            </tbody>
          </table>
          <div style="font-size:12px;font-weight:800;color:#0f172a;margin:8px 0 4px 0;">🧠 XAI 설계 근거</div>
          <p style="font-size:11.5px;color:#475569;line-height:1.5;">
            - 응급센터는 동측 비상도로 인접 배치하여 골든타임 확보.<br>
            - 푸드존은 서측 독립 구역 배치로 조기 연기 및 소음 차단.<br>
            - 무대는 북쪽 상단 중앙 배치로 시야각 극대화.
          </p>
        </div>

      </div>
    </div>

    <script>
    let venueCanvas, venueCtx, peopleCanvas, peopleCtx, heatmapCanvas, heatmapCtx;
    let simRunning = false, isRain = false, isEmergency = false, emergencyPos = null;
    let people = [], raindrops = [];
    let is3DActive = false, scene3D, camera3D, renderer3D;

    const booths = {
      stage: {x: 0.5, y: 0.15, bw: 0.28, bh: 0.15, title: '공연장 (메인무대)', color: '#8b5cf6', icon: '🎪'},
      booth: {x: 0.22, y: 0.35, bw: 0.20, bh: 0.18, title: '체험부스', color: '#3b82f6', icon: '🛍️'},
      food: {x: 0.22, y: 0.65, bw: 0.20, bh: 0.18, title: '푸드존', color: '#f59e0b', icon: '🍔'},
      rest: {x: 0.5, y: 0.55, bw: 0.28, bh: 0.20, title: '휴게공간', color: '#10b981', icon: '🏕️'},
      medical: {x: 0.78, y: 0.35, bw: 0.18, bh: 0.15, title: '응급의료센터', color: '#ef4444', icon: '🚑'},
      toilet: {x: 0.78, y: 0.60, bw: 0.18, bh: 0.15, title: '화장실', color: '#2563eb', icon: '🚻'}
    };

    window.addEventListener('load', () => {
      venueCanvas = document.getElementById('venueCanvas');
      peopleCanvas = document.getElementById('peopleCanvas');
      heatmapCanvas = document.getElementById('heatmapCanvas');

      const wrap = document.getElementById('mapWrap');
      const w = wrap.clientWidth;
      const h = wrap.clientHeight;

      [venueCanvas, peopleCanvas, heatmapCanvas].forEach(c => {
        c.width = w; c.height = h;
      });

      venueCtx = venueCanvas.getContext('2d');
      peopleCtx = peopleCanvas.getContext('2d');
      heatmapCtx = heatmapCanvas.getContext('2d');

      initPeople(w, h);
      initRain(w, h);
      drawVenue(w, h);
      renderLoop();
    });

    function initPeople(w, h) {
      people = [];
      for(let i=0; i<60; i++){
        people.push({
          x: w*0.1 + Math.random()*w*0.8,
          y: h*0.2 + Math.random()*h*0.7,
          vx: (Math.random()-0.5)*1.2,
          vy: (Math.random()-0.5)*1.2,
          speed: 1.0
        });
      }
    }

    function initRain(w, h) {
      raindrops = [];
      for(let i=0; i<80; i++){
        raindrops.push({x: Math.random()*w, y: Math.random()*h, len: 10, vy: 5+Math.random()*5});
      }
    }

    function drawVenue(w, h) {
      venueCtx.fillStyle = isRain ? '#254e2b' : '#3a7d44';
      venueCtx.fillRect(0, 0, w, h);

      // Central lawn
      venueCtx.fillStyle = isRain ? '#377341' : '#4fa15a';
      venueCtx.beginPath();
      venueCtx.ellipse(w*0.5, h*0.55, w*0.25, h*0.22, 0, 0, Math.PI*2);
      venueCtx.fill();

      // Booths
      Object.keys(booths).forEach(k => {
        const b = booths[k];
        const bx = b.x * w - (b.bw * w)/2;
        const by = b.y * h - (b.bh * h)/2;
        const bw = b.bw * w;
        const bh = b.bh * h;

        venueCtx.fillStyle = 'rgba(0,0,0,0.2)';
        venueCtx.fillRect(bx+3, by+3, bw, bh);

        venueCtx.fillStyle = b.color;
        venueCtx.beginPath();
        venueCtx.roundRect(bx, by, bw, bh, 8);
        venueCtx.fill();

        venueCtx.strokeStyle = '#ffffff';
        venueCtx.lineWidth = 1.5;
        venueCtx.stroke();

        venueCtx.fillStyle = '#ffffff';
        venueCtx.font = 'bold 11px Pretendard';
        venueCtx.textAlign = 'center';
        venueCtx.fillText(`${b.icon} ${b.title}`, bx + bw/2, by + bh/2 + 4);
      });
    }

    function renderLoop() {
      if (simRunning) {
        updateSim();
      }
      if (venueCanvas) {
        drawPeople(venueCanvas.width, venueCanvas.height);
        drawHeatmap(venueCanvas.width, venueCanvas.height);
      }
      requestAnimationFrame(renderLoop);
    }

    function updateSim() {
      const w = venueCanvas.width, h = venueCanvas.height;
      people.forEach(p => {
        p.x += p.vx; p.y += p.vy;
        if(p.x < 10 || p.x > w-10) p.vx *= -1;
        if(p.y < 10 || p.y > h-10) p.vy *= -1;
      });
      if (isRain) {
        raindrops.forEach(r => {
          r.y += r.vy; if(r.y > h) r.y = 0;
        });
      }
    }

    function drawPeople(w, h) {
      peopleCtx.clearRect(0,0,w,h);
      people.forEach(p => {
        peopleCtx.fillStyle = isRain ? '#60a5fa' : '#ffffff';
        peopleCtx.beginPath();
        peopleCtx.arc(p.x, p.y, 3, 0, Math.PI*2);
        peopleCtx.fill();
      });

      if (isEmergency && emergencyPos) {
        peopleCtx.strokeStyle = '#ef4444';
        peopleCtx.lineWidth = 3;
        peopleCtx.setLineDash([5,5]);
        peopleCtx.beginPath();
        peopleCtx.moveTo(emergencyPos.x, emergencyPos.y);
        peopleCtx.lineTo(booths.medical.x * w, booths.medical.y * h);
        peopleCtx.stroke();
        peopleCtx.setLineDash([]);

        peopleCtx.fillStyle = '#ef4444';
        peopleCtx.beginPath();
        peopleCtx.arc(emergencyPos.x, emergencyPos.y, 7, 0, Math.PI*2);
        peopleCtx.fill();
      }

      if (isRain) {
        peopleCtx.strokeStyle = 'rgba(147, 197, 253, 0.4)';
        raindrops.forEach(r => {
          peopleCtx.beginPath();
          peopleCtx.moveTo(r.x, r.y);
          peopleCtx.lineTo(r.x-1, r.y+r.len);
          peopleCtx.stroke();
        });
      }
    }

    function drawHeatmap(w, h) {
      heatmapCtx.clearRect(0,0,w,h);
      const grid = {};
      people.forEach(p => {
        const gx = Math.floor(p.x / 40), gy = Math.floor(p.y / 40);
        const k = `${gx}_${gy}`;
        grid[k] = (grid[k] || 0) + 1;
      });
      Object.keys(grid).forEach(k => {
        const [gx, gy] = k.split('_').map(Number);
        const count = grid[k];
        if (count >= 2) {
          const cx = gx * 40 + 20, cy = gy * 40 + 20;
          let grad = heatmapCtx.createRadialGradient(cx, cy, 0, cx, cy, count*10);
          grad.addColorStop(0, count >= 4 ? 'rgba(239, 68, 68, 0.7)' : 'rgba(245, 158, 11, 0.6)');
          grad.addColorStop(1, 'rgba(16, 185, 129, 0)');
          heatmapCtx.fillStyle = grad;
          heatmapCtx.beginPath();
          heatmapCtx.arc(cx, cy, count*10, 0, Math.PI*2);
          heatmapCtx.fill();
        }
      });
    }

    function toggleSim() {
      simRunning = !simRunning;
      document.getElementById('btnToggleSim').textContent = simRunning ? '⏸ 시뮬레이션 일시정지' : '▶ 시뮬레이션 시작';
      document.getElementById('simTimer').textContent = simRunning ? '상태: 군중 이동 시뮬레이션 중 ▶' : '상태: 대기중';
    }

    function toggleRainEnv() {
      isRain = !isRain;
      document.getElementById('btnRain').classList.toggle('active', isRain);
      document.getElementById('btnRain').textContent = isRain ? '🌧️ 우천 모드 (ON)' : '🌧️ 우천 모드';
      document.getElementById('envBadge').textContent = isRain ? '🌧️ 강우 발생' : '일반 상태';
      drawVenue(venueCanvas.width, venueCanvas.height);
    }

    function triggerEmergencyEnv() {
      isEmergency = !isEmergency;
      document.getElementById('btnEmergency').classList.toggle('active', isEmergency);
      document.getElementById('btnEmergency').textContent = isEmergency ? '🚨 응급상황 해제' : '🚨 응급환자 후송';
      if (isEmergency) {
        emergencyPos = {x: venueCanvas.width * 0.25, y: venueCanvas.height * 0.5};
        if (!simRunning) toggleSim();
      } else {
        emergencyPos = null;
      }
      document.getElementById('envBadge').textContent = isEmergency ? '🚨 응급 환자 이송 중' : '일반 상태';
    }

    function updateTimeSimulation(val) {
      document.getElementById('timeDisplay').textContent = `${val}:00`;
    }

    function toggleTimelinePlay() {}

    function sendMainAiMsg() {
      const input = document.getElementById('mainAiInput');
      const txt = input.value.trim();
      if(!txt) return;
      const chatBox = document.getElementById('mainAiChatBox');
      chatBox.innerHTML += `<div class="chat-msg-user"><b>나:</b> ${txt}</div>`;
      input.value = '';
      chatBox.scrollTop = chatBox.scrollHeight;

      setTimeout(() => {
        chatBox.innerHTML += `<div class="chat-msg-ai"><b>AI:</b> 요청하신 "${txt}" 내용을 분석하여 디지털 트윈 배치도와 XAI 평가 지표를 갱신했습니다.</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
      }, 500);
    }

    function toggle3DView() {
      is3DActive = !is3DActive;
      const container = document.getElementById('container3D');
      const btn = document.getElementById('btnToggle3D');
      container.style.display = is3DActive ? 'block' : 'none';
      btn.textContent = is3DActive ? '🗺️ 2D 평면도 보기' : '🧊 3D 입체뷰 보기';
      if (is3DActive) init3D();
    }

    function init3D() {
      const container = document.getElementById('container3D');
      container.innerHTML = '';
      const w = container.clientWidth, h = container.clientHeight;
      scene3D = new THREE.Scene();
      scene3D.background = new THREE.Color(0x0f172a);
      camera3D = new THREE.PerspectiveCamera(45, w/h, 0.1, 1000);
      camera3D.position.set(0, 140, 160);
      camera3D.lookAt(0,0,0);
      renderer3D = new THREE.WebGLRenderer({antialias:true});
      renderer3D.setSize(w, h);
      container.appendChild(renderer3D.domElement);

      scene3D.add(new THREE.AmbientLight(0xffffff, 0.7));
      const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
      dirLight.position.set(50, 100, 50);
      scene3D.add(dirLight);

      const ground = new THREE.Mesh(new THREE.PlaneGeometry(180, 120), new THREE.MeshLambertMaterial({color: 0x2e7d32}));
      ground.rotation.x = -Math.PI/2;
      scene3D.add(ground);

      Object.keys(booths).forEach(k => {
        const b = booths[k];
        const bw = b.bw * 180, bh = b.bh * 120;
        const bx = (b.x - 0.5) * 180, bz = (b.y - 0.5) * 120;
        const height = k === 'stage' ? 16 : 10;
        const mesh = new THREE.Mesh(new THREE.BoxGeometry(bw, height, bh), new THREE.MeshLambertMaterial({color: parseInt(b.color.replace('#','0x'))}));
        mesh.position.set(bx, height/2, bz);
        scene3D.add(mesh);
      });

      function animate() {
        if(is3DActive) {
          requestAnimationFrame(animate);
          scene3D.rotation.y += 0.002;
          renderer3D.render(scene3D, camera3D);
        }
      }
      animate();
    }
    </script>
    </body>
    </html>
    """
    components.html(EVENT_AI_HTML, height=750, scrolling=True)

# ==========================================
# 3. AI 설계 프로세스 화면 (Process Page)
# ==========================================
elif st.session_state['page'] == 'process':
    st.markdown("## ⚙️ AI 행사 설계 프로세스 (Workflow)")
    st.caption("기획부터 최종 최적화 설계안 도출까지의 전체 운영 흐름도입니다.")

    col_w1, col_w2, col_w3, col_w4, col_w5 = st.columns(5)
    with col_w1:
        st.markdown("""
            <div class="custom-card" style="text-align: center; min-height: 200px;">
                <h3>📋</h3>
                <h4>1단계: 정보 입력</h4>
                <p style="font-size: 0.85rem; color: #64748B;">예산, 목적, 예상 관람객 및 맞춤 부스 요구사항 입력</p>
            </div>
        """, unsafe_allow_html=True)
    with col_w2:
        st.markdown("""
            <div class="custom-card" style="text-align: center; min-height: 200px;">
                <h3>🌐</h3>
                <h4>2단계: 디지털 트윈</h4>
                <p style="font-size: 0.85rem; color: #64748B;">장소 지형 데이터를 바탕으로 3D 가상 공간 구축</p>
            </div>
        """, unsafe_allow_html=True)
    with col_w3:
        st.markdown("""
            <div class="custom-card" style="text-align: center; min-height: 200px;">
                <h3>🤖</h3>
                <h4>3단계: 자동 배치</h4>
                <p style="font-size: 0.85rem; color: #64748B;">수천 개의 행사 배치안 및 강화학습 시뮬레이션 수행</p>
            </div>
        """, unsafe_allow_html=True)
    with col_w4:
        st.markdown("""
            <div class="custom-card" style="text-align: center; min-height: 200px;">
                <h3>🚑</h3>
                <h4>4단계: 다목적 최적화</h4>
                <p style="font-size: 0.85rem; color: #64748B;">군중 이동 동선 분석, 병목 예방 및 응급 경로 최적화</p>
            </div>
        """, unsafe_allow_html=True)
    with col_w5:
        st.markdown("""
            <div class="custom-card" style="text-align: center; min-height: 200px;">
                <h3>📄</h3>
                <h4>5단계: XAI 리포트</h4>
                <p style="font-size: 0.85rem; color: #64748B;">설명 가능한 AI(XAI) 근거 및 최종 비교 리포트 출력</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 **운영자 기대 효과:** 운영자는 객관적인 데이터를 기반으로 안전하고 효율적인 대규모 행사를 신속하게 기획할 수 있습니다.")

# ==========================================
# 4. 시스템 설정 화면 (Settings Page)
# ==========================================
elif st.session_state['page'] == 'settings':
    st.markdown("## ⚙️ 시스템 설정 및 관리")

    with st.container():
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("👤 계정 및 사용자 프로필")
        st.session_state['username'] = st.text_input("사용자 이름", value=st.session_state['username'])
        st.text_input("소속 부서 / 조직", value="이벤트 기획 1팀")
        st.text_input("이메일 주소", value="user@event-on.ai")
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("🖥️ AI 디지털 트윈 엔진 옵션")
        st.toggle("도면 내 레이블 및 좌표 가이드 표시", value=True)
        st.toggle("실시간 군중 시뮬레이션 자동 실행", value=True)
        st.selectbox("AI 추론 모델 선택", ["EventOn-Engine v4.2 (최신/권장)", "EventOn-Lite"])
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("로그아웃", type="primary"):
        st.session_state['logged_in'] = False
        st.session_state['page'] = 'home'
        st.rerun()
