
import streamlit as st
import plotly.graph_objects as go
import random
import math
from datetime import datetime

# =========================================================
# Event Architect AI
# Streamlit single-file prototype
# =========================================================

st.set_page_config(
    page_title="Event Architect AI",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# Session state
# -----------------------------
DEFAULTS = {
    "page": "home",
    "logged_in": False,
    "username": "",
    "users": {},
    "event": {},
    "layout": None,
    "before_layout": None,
    "simulation": False,
    "selected_zone": None,
    "chat": [],
    "report": "",
    "settings_open": False,
    "auth_mode": None,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>
    .stApp {
        background: #f5f7fb;
    }
    header {visibility: hidden;}
    .block-container {
        padding-top: 1.0rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }
    .topbar {
        background: white;
        border: 1px solid #e5e9f2;
        border-radius: 18px;
        padding: 14px 18px;
        margin-bottom: 18px;
        box-shadow: 0 4px 16px rgba(30,50,90,.05);
    }
    .logo {
        font-size: 22px;
        font-weight: 800;
        color: #172554;
    }
    .subtitle {
        color: #64748b;
        font-size: 12px;
        margin-top: 2px;
    }
    .hero {
        padding: 42px 28px;
        background: linear-gradient(135deg, #eef2ff, #ffffff);
        border: 1px solid #e0e7ff;
        border-radius: 24px;
        margin-bottom: 24px;
    }
    .hero h1 {
        font-size: 42px;
        color: #172554;
        margin-bottom: 8px;
    }
    .hero p {
        color: #64748b;
        font-size: 16px;
    }
    .big-card {
        background: white;
        border: 1px solid #e5e9f2;
        border-radius: 22px;
        padding: 30px;
        min-height: 245px;
        box-shadow: 0 5px 20px rgba(30,50,90,.05);
    }
    .big-card h2 {
        color: #172554;
    }
    .metric-card {
        background: white;
        border: 1px solid #e5e9f2;
        border-radius: 16px;
        padding: 16px;
        text-align: center;
    }
    .small-label {
        color: #64748b;
        font-size: 13px;
    }
    .score {
        font-size: 28px;
        font-weight: 800;
        color: #315efb;
    }
    .zone-note {
        background: #f8fafc;
        border-left: 4px solid #315efb;
        padding: 14px;
        border-radius: 8px;
    }
    .report-box {
        background: white;
        padding: 26px;
        border-radius: 18px;
        border: 1px solid #e5e9f2;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Helpers
# -----------------------------
def hash_pw(pw):
    # Demo-only hash. For production, use a proper auth provider.
    import hashlib
    return hashlib.sha256(pw.encode()).hexdigest()

def login_user(username, password):
    users = st.session_state.users
    if username in users and users[username] == hash_pw(password):
        st.session_state.logged_in = True
        st.session_state.username = username
        return True
    return False

def register_user(username, password, confirm):
    if not username or not password:
        return False, "아이디와 비밀번호를 입력해주세요."
    if len(password) < 4:
        return False, "비밀번호는 4자 이상 입력해주세요."
    if password != confirm:
        return False, "비밀번호가 일치하지 않습니다."
    if username in st.session_state.users:
        return False, "이미 존재하는 아이디입니다."
    st.session_state.users[username] = hash_pw(password)
    return True, "회원가입이 완료되었습니다."

def place_profile(place):
    p = place.lower()
    if any(x in p for x in ["공원", "야외", "운동장", "광장", "잔디"]):
        return "outdoor"
    if any(x in p for x in ["학교", "체육관", "강당", "전시장", "컨벤션"]):
        return "indoor"
    return "general"

def make_layout(event, optimized=True):
    people = int(event.get("people", 500))
    purpose = event.get("purpose", "")
    place = event.get("place", "")
    profile = place_profile(place)

    # Venue canvas
    W, H = 100, 64
    if profile == "outdoor":
        canvas = (W, H)
    elif profile == "indoor":
        canvas = (W, H)
    else:
        canvas = (W, H)

    # Zone definitions: x, y, width, height
    if optimized:
        zones = {
            "무대": (30, 47, 40, 13),
            "푸드 존": (5, 36, 20, 13),
            "부스": (5, 17, 20, 15),
            "휴식 구역": (29, 6, 23, 12),
            "정보 센터": (75, 39, 19, 10),
            "의료 센터": (75, 25, 19, 10),
            "화장실": (75, 13, 19, 9),
            "비상구": (42, 2, 16, 6),
        }
    else:
        zones = {
            "무대": (4, 47, 40, 13),
            "푸드 존": (49, 42, 45, 13),
            "부스": (4, 25, 42, 15),
            "휴식 구역": (50, 22, 22, 12),
            "정보 센터": (74, 18, 20, 10),
            "의료 센터": (4, 8, 18, 10),
            "화장실": (30, 7, 18, 10),
            "비상구": (76, 3, 18, 9),
        }

    # Minor adaptation for smaller events
    scale = 1.0 if people >= 300 else 0.82
    if scale != 1.0 and optimized:
        # Keep the core layout readable; zones are still drawn on the same canvas.
        pass

    return {"W": W, "H": H, "zones": zones, "profile": profile}

def zone_reason(zone, event, optimized=True):
    people = int(event.get("people", 500))
    purpose = event.get("purpose", "행사 운영")
    place = event.get("place", "입력 장소")
    reasons = {
        "무대": f"행사의 핵심 프로그램이 집중되는 공간입니다. 약 {people:,}명의 관람객이 한 방향으로 몰리는 상황을 고려해 중앙 상단에 배치하고 전면에 넓은 관람·이동 공간을 확보했습니다.",
        "푸드 존": "체류 시간이 긴 공간이므로 메인 동선과 약간 분리해 대기열이 주 이동로를 막지 않도록 배치했습니다.",
        "부스": "참가자의 자연스러운 순환을 유도하기 위해 한쪽 구역에 연속적으로 배치했습니다. 부스 사이의 통로를 확보해 병목을 줄였습니다.",
        "휴식 구역": "장시간 행사에서 체류자가 잠시 빠져나갈 수 있는 완충 공간입니다. 주요 시설 사이에 배치해 혼잡을 분산하도록 설계했습니다.",
        "정보 센터": "입구와 주요 동선에서 쉽게 찾을 수 있는 위치에 배치했습니다. 안내·분실물·문의 대응을 한 곳에서 처리할 수 있습니다.",
        "의료 센터": "행사장 중심과 외부 접근로 사이에 배치해 응급상황 발생 시 접근 시간을 줄이는 것을 목표로 했습니다.",
        "화장실": "사람이 오래 머무는 시설에서 너무 멀지 않으면서도 메인 동선을 막지 않는 가장자리 쪽에 배치했습니다.",
        "비상구": "비상 상황에서 여러 방향으로 빠르게 대피할 수 있도록 외곽에 배치했습니다. 다른 시설과 겹치지 않는 출구 동선을 확보했습니다.",
    }
    return reasons.get(zone, f"{zone}은(는) {place}의 특성과 '{purpose}' 목적을 고려해 배치했습니다.")

def make_heatmap(event, optimized=True, seed=7):
    random.seed(seed + (1 if optimized else 0))
    people = int(event.get("people", 500))
    base = min(1.0, 0.25 + people / 8000)

    xs, ys, vals = [], [], []
    # Hotspots vary between before/after.
    hotspots = (
        [(50, 48, 1.0), (18, 38, .8), (67, 31, .65), (50, 17, .45)]
        if optimized
        else [(22, 48, .95), (68, 47, .92), (43, 30, .85), (83, 20, .65)]
    )
    for _ in range(900):
        x = random.uniform(3, 97)
        y = random.uniform(3, 61)
        v = base * .25
        for hx, hy, strength in hotspots:
            d = ((x-hx)**2 + (y-hy)**2) ** .5
            v += strength * math.exp(-(d**2)/260)
        v += random.uniform(0, .08)
        xs.append(x); ys.append(y); vals.append(v)
    return xs, ys, vals

def draw_venue(layout, event, heatmap=False, optimized=True):
    W, H = layout["W"], layout["H"]
    fig = go.Figure()

    # Background
    fig.add_shape(
        type="rect", x0=0, y0=0, x1=W, y1=H,
        fillcolor="#eef2f7",
        line=dict(color="#cbd5e1", width=2)
    )

    # Pure Plotly heatmap layer (no Mapbox/API key required)
    if heatmap:
        grid_n = 42
        xs = [i * W / (grid_n - 1) for i in range(grid_n)]
        ys = [i * H / (grid_n - 1) for i in range(grid_n)]
        hotspots = (
            [(50, 48, 1.0), (18, 38, .8), (67, 31, .65), (50, 17, .45)]
            if optimized
            else [(22, 48, .95), (68, 47, .92), (43, 30, .85), (83, 20, .65)]
        )
        people = int(event.get("people", 500))
        base = min(0.32, 0.08 + people / 20000)

        z = []
        for y in ys:
            row = []
            for x in xs:
                v = base
                for hx, hy, strength in hotspots:
                    d2 = (x-hx)**2 + (y-hy)**2
                    v += strength * math.exp(-d2 / 180)
                row.append(v)
            z.append(row)

        fig.add_trace(go.Heatmap(
            x=xs, y=ys, z=z,
            colorscale="Turbo",
            opacity=0.52,
            showscale=True,
            colorbar=dict(title="혼잡도", thickness=12)
        ))

    zone_colors = {
        "무대": "#dbeafe", "푸드 존": "#ffedd5", "부스": "#ede9fe",
        "휴식 구역": "#dcfce7", "정보 센터": "#e0e7ff",
        "의료 센터": "#fee2e2", "화장실": "#f1f5f9", "비상구": "#fef3c7"
    }

    for name, (x, y, w, h) in layout["zones"].items():
        fig.add_shape(
            type="rect", x0=x, y0=y, x1=x+w, y1=y+h,
            fillcolor=zone_colors.get(name, "#ffffff"),
            line=dict(color="#475569", width=1.5)
        )
        fig.add_annotation(
            x=x+w/2, y=y+h/2,
            text=f"<b>{name}</b>", showarrow=False,
            font=dict(size=12, color="#172554")
        )

    # Entrance
    fig.add_shape(
        type="rect", x0=43, y0=0, x1=57, y1=4,
        fillcolor="#bfdbfe", line=dict(color="#2563eb")
    )
    fig.add_annotation(
        x=50, y=2, text="입구", showarrow=False,
        font=dict(size=12, color="#1e3a8a")
    )

    # Main movement routes
    routes = [
        ([50, 50, 50], [4, 20, 47]),
        ([25, 30, 75], [25, 25, 30]),
        ([50, 75], [30, 44]),
    ]
    for rx, ry in routes:
        fig.add_trace(go.Scatter(
            x=rx, y=ry, mode="lines",
            line=dict(color="#2563eb", width=3, dash="dot"),
            hoverinfo="skip", showlegend=False
        ))

    fig.update_xaxes(range=[0, W], visible=False)
    fig.update_yaxes(range=[0, H], visible=False, scaleanchor="x", scaleratio=1)
    fig.update_layout(
        height=590,
        margin=dict(l=5, r=5, t=5, b=5),
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=False
    )
    return fig

def calculate_scores(event, simulation=False):
    people = int(event.get("people", 500))
    budget = int(event.get("budget", 0))
    scores = {
        "안전성": min(98, 88 + (5 if simulation else 0) + (3 if people < 5000 else 0)),
        "접근성": 91,
        "동선 효율성": min(97, 84 + (6 if simulation else 0)),
        "혼잡도 관리": min(96, 78 + (10 if simulation else 0) + (3 if people < 3000 else 0)),
        "예산 효율성": min(95, 82 + (6 if budget and budget >= 3_000_000 else 2)),
    }
    return scores

def generate_report(event, scores):
    name = event.get("name", "행사")
    purpose = event.get("purpose", "")
    people = event.get("people", 0)
    budget = event.get("budget", 0)
    place = event.get("place", "")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"""# AI 행사 설계 보고서

## 1. 행사 개요
- 행사명: {name}
- 행사 목적: {purpose}
- 예상 방문객: {people:,}명
- 예산: {budget:,}원
- 행사 장소: {place}

## 2. AI 설계 결과
AI는 입력된 행사 목적, 예상 방문객 규모, 예산 및 장소 특성을 바탕으로 무대, 푸드 존, 부스, 휴식 구역, 정보 센터, 의료 센터, 화장실, 비상구를 배치했습니다.

주요 동선은 입구에서 메인 행사 공간으로 연결되도록 구성하고, 체류형 시설은 주 동선에서 분리해 혼잡을 줄이는 방향으로 설계했습니다.

## 3. 평가 결과
- 안전성: {scores["안전성"]}점
- 접근성: {scores["접근성"]}점
- 동선 효율성: {scores["동선 효율성"]}점
- 혼잡도 관리: {scores["혼잡도 관리"]}점
- 예산 효율성: {scores["예산 효율성"]}점

## 4. 개선 권장 사항
1. 행사 시작·종료 시간에는 입구 주변 혼잡을 집중적으로 관리합니다.
2. 푸드 존의 대기열이 주 이동 동선을 막지 않도록 대기 공간을 별도로 확보합니다.
3. 의료 센터와 비상구의 안내 표지판을 행사장 곳곳에 배치합니다.
4. 방문객 수가 증가할 경우 휴식 구역과 안내 인력을 추가합니다.

## 5. 결론
본 설계안은 안전성, 접근성, 동선 효율성, 혼잡도 관리 및 예산 효율성을 종합적으로 고려한 AI 기반 행사장 설계안입니다.

작성 시각: {now}
"""

# -----------------------------
# Top navigation
# -----------------------------
def topbar():
    c1, c2, c3, c4 = st.columns([5.5, 1.4, 1.4, 1.4])

    with c1:
        if st.button("🏗️ Event Architect AI", key="logo", help="홈으로 이동"):
            st.session_state.page = "home"
            st.rerun()

    with c2:
        if st.session_state.logged_in:
            st.caption(f"👤 {st.session_state.username}님")
        else:
            if st.button("로그인", key="top_login", use_container_width=True):
                st.session_state.auth_mode = "login"
                st.session_state.page = "home"
                st.rerun()

    with c3:
        if not st.session_state.logged_in:
            if st.button("회원가입", key="top_signup", use_container_width=True):
                st.session_state.auth_mode = "signup"
                st.session_state.page = "home"
                st.rerun()
        else:
            if st.button("🏠 홈", key="top_home", use_container_width=True):
                st.session_state.page = "home"
                st.rerun()

    with c4:
        if st.button("⚙️ 설정", key="settings_btn", use_container_width=True):
            st.session_state.settings_open = not st.session_state.settings_open

    if st.session_state.settings_open:
        with st.expander("⚙️ 설정", expanded=True):
            st.write("### 계정 설정")
            if st.session_state.logged_in:
                st.write(f"현재 로그인: **{st.session_state.username}**")
                if st.button("로그아웃", key="settings_logout"):
                    st.session_state.logged_in = False
                    st.session_state.username = ""
                    st.session_state.page = "home"
                    st.session_state.settings_open = False
                    st.rerun()
            else:
                st.info("현재 로그인하지 않았습니다.")
                if st.button("로그인 / 회원가입", key="settings_auth"):
                    st.session_state.auth_mode = "login"
                    st.session_state.page = "home"
                    st.session_state.settings_open = False
                    st.rerun()

            st.write("### 앱 설정")
            st.toggle("분석 애니메이션 사용", value=True, key="animation")
            st.selectbox("언어", ["한국어"], key="language")

# -----------------------------
# Login / register
# -----------------------------
def auth_area():
    st.markdown("### 🔐 로그인 / 회원가입")
    login_tab, signup_tab = st.tabs(["로그인", "회원가입"])

    with login_tab:
        u = st.text_input("아이디", key="login_u")
        p = st.text_input("비밀번호", type="password", key="login_p")
        if st.button("로그인", use_container_width=True):
            if login_user(u, p):
                st.success("로그인되었습니다.")
                st.rerun()
            else:
                st.error("아이디 또는 비밀번호가 올바르지 않습니다.")

    with signup_tab:
        u2 = st.text_input("새 아이디", key="signup_u")
        p2 = st.text_input("비밀번호", type="password", key="signup_p")
        p3 = st.text_input("비밀번호 확인", type="password", key="signup_c")
        if st.button("회원가입", use_container_width=True):
            ok, msg = register_user(u2, p2, p3)
            (st.success if ok else st.error)(msg)

# -----------------------------
# Home
# -----------------------------
def home():
    st.markdown("""
    <div class="hero">
        <h1>AI 기반 행사 자동 설계 플랫폼</h1>
        <p>행사 정보를 입력하면 디지털 트윈 기반 공간 배치, 군중 시뮬레이션, AI 분석 보고서를 한 번에 제공합니다.</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.logged_in and st.session_state.auth_mode:
        st.divider()
        auth_area()
        st.session_state.auth_mode = None
        st.divider()

    st.subheader("무엇을 하시겠어요?")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="big-card">
            <h2>📊 대시보드</h2>
            <p>행사 정보를 입력하고 AI가 최적의 행사장 공간을 설계합니다.</p>
            <ul>
                <li>디지털 트윈 행사장</li>
                <li>시설 자동 배치</li>
                <li>군중 예측 Heatmap</li>
                <li>Before / After 비교</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("대시보드 열기 →", key="home_dashboard", use_container_width=True):
            if not st.session_state.logged_in:
                st.warning("대시보드를 이용하려면 먼저 로그인해주세요.")
            else:
                st.session_state.page = "dashboard"
                st.rerun()

    with c2:
        st.markdown("""
        <div class="big-card">
            <h2>📄 AI 보고서</h2>
            <p>설계 결과와 평가 내용을 직장 상사에게 보고할 수 있는 형태로 정리합니다.</p>
            <ul>
                <li>행사 개요</li>
                <li>AI 설계 결과</li>
                <li>안전·접근성·동선 점수</li>
                <li>개선 권장 사항</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("AI 보고서 열기 →", key="home_report", use_container_width=True):
            if not st.session_state.logged_in:
                st.warning("보고서를 이용하려면 먼저 로그인해주세요.")
            else:
                st.session_state.page = "report"
                st.rerun()

# -----------------------------
# Dashboard
# -----------------------------
def dashboard():
    st.title("📊 AI 행사 설계 대시보드")
    st.caption("행사 정보를 입력한 뒤 AI 이벤트 디자인을 생성하세요.")

    with st.container(border=True):
        st.subheader("① 행사 정보")
        c1, c2, c3 = st.columns(3)
        with c1:
            name = st.text_input("이벤트 이름", value=st.session_state.event.get("name", "2026 청소년 문화축제"))
            purpose = st.text_area("이벤트 목적", value=st.session_state.event.get("purpose", "청소년 문화 교류와 체험 기회 제공"))
        with c2:
            people = st.number_input("예상 방문객 수", min_value=1, max_value=100000, value=int(st.session_state.event.get("people", 5000)), step=100)
            budget = st.number_input("예산 (원)", min_value=0, max_value=10_000_000_000, value=int(st.session_state.event.get("budget", 50_000_000)), step=1_000_000)
        with c3:
            place = st.text_input("장소", value=st.session_state.event.get("place", "시민공원"))
            duration = st.number_input("진행 시간 (시간)", min_value=1, max_value=24, value=int(st.session_state.event.get("duration", 5)))

        if st.button("✨ AI 이벤트 디자인 생성", type="primary", use_container_width=True):
            st.session_state.event = {
                "name": name, "purpose": purpose, "people": people,
                "budget": budget, "place": place, "duration": duration
            }
            st.session_state.before_layout = make_layout(st.session_state.event, optimized=False)
            st.session_state.layout = make_layout(st.session_state.event, optimized=True)
            st.session_state.simulation = False
            st.session_state.selected_zone = None
            scores = calculate_scores(st.session_state.event, False)
            st.session_state.report = generate_report(st.session_state.event, scores)
            st.session_state.chat = [{
                "role": "assistant",
                "content": f"'{name}' 행사에 맞는 기본 공간 배치를 생성했습니다. 오른쪽의 공간 버튼을 눌러 배치 이유를 확인하거나 AI 시뮬레이션을 실행해보세요."
            }]
            st.rerun()

    if not st.session_state.layout:
        st.info("위의 정보를 입력하고 **AI 이벤트 디자인 생성** 버튼을 눌러주세요.")
        return

    st.divider()

    # Main map + explanation
    left, right = st.columns([7, 3])
    with left:
        st.subheader("② 디지털 트윈 행사장")
        st.caption(f"장소 특성 분석: {st.session_state.layout['profile']} / {st.session_state.event['place']}")
        fig = draw_venue(st.session_state.layout, st.session_state.event,
                         heatmap=st.session_state.simulation, optimized=True)
        st.plotly_chart(fig, use_container_width=True)

        if st.session_state.simulation:
            st.success("AI 군중 시뮬레이션 완료 — 색이 진할수록 예상 체류·이동 밀도가 높습니다.")
        else:
            st.caption("점선은 주요 이동 동선입니다. 아래 공간명을 눌러 배치 이유를 확인하세요.")

        zone_names = list(st.session_state.layout["zones"].keys())
        cols = st.columns(4)
        for i, zone in enumerate(zone_names):
            with cols[i % 4]:
                if st.button(zone, key=f"zone_{zone}", use_container_width=True):
                    st.session_state.selected_zone = zone
                    st.rerun()

    with right:
        st.subheader("③ 공간 배치 이유")
        if st.session_state.selected_zone:
            z = st.session_state.selected_zone
            st.markdown(f"### 📍 {z}")
            st.markdown(
                f'<div class="zone-note">{zone_reason(z, st.session_state.event)}</div>',
                unsafe_allow_html=True
            )
        else:
            st.info("지도 아래의 공간명을 눌러 AI가 왜 해당 위치에 배치했는지 확인하세요.")

        st.divider()
        st.subheader("④ AI 시뮬레이션")
        st.write("예상 방문객 흐름을 분석해 혼잡 예상 구간을 표시합니다.")
        if st.button("🧠 AI 시뮬레이션 실행", type="primary", use_container_width=True):
            st.session_state.simulation = True
            scores = calculate_scores(st.session_state.event, True)
            st.session_state.report = generate_report(st.session_state.event, scores)
            st.rerun()

        if st.session_state.simulation:
            st.markdown("**혼잡도 범례**")
            st.write("🟢 낮음  🟡 보통  🔴 높음")

    st.divider()

    # Chat
    st.subheader("⑤ AI 디자인 상담")
    st.caption("원하는 변경 사항을 자연어로 입력하면 설계 방향을 제안합니다.")

    for msg in st.session_state.chat:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    prompt = st.chat_input("예: 푸드존을 입구에서 멀리 옮겨줘 / 휴식 공간을 더 넓혀줘")
    if prompt:
        st.session_state.chat.append({"role": "user", "content": prompt})

        p = prompt.lower()
        if "푸드" in p or "음식" in p:
            answer = "푸드 존은 대기열이 주 동선을 막지 않도록 현재처럼 가장자리 쪽에 두는 것을 추천합니다. 더 멀리 이동시키고 싶다면 부스와 휴식 구역 사이로 옮기는 방안도 가능합니다."
        elif "휴식" in p:
            answer = "휴식 구역의 면적을 늘리는 방향을 추천합니다. 특히 장시간 행사라면 메인 동선과 가까우면서도 직접적인 병목이 생기지 않는 위치가 좋습니다."
        elif "무대" in p:
            answer = "무대는 관람객이 한 방향으로 모이는 핵심 시설이므로 중앙 상단 배치를 유지하는 것이 안전합니다. 관람 구역을 더 넓히는 설계도 가능합니다."
        elif "의료" in p or "응급" in p:
            answer = "의료 센터는 외곽 접근성과 행사장 중심 접근성을 동시에 고려해 배치했습니다. 비상구와 연결되는 통로를 확보하는 것을 권장합니다."
        elif "부스" in p:
            answer = "부스는 순환형 동선을 만들 수 있도록 한쪽 구역에 연속 배치했습니다. 부스 수를 늘리면 통로 폭과 대기열 공간을 함께 조정해야 합니다."
        elif "화장실" in p:
            answer = "화장실은 체류 공간에서 접근하기 쉬우면서도 메인 동선을 방해하지 않는 외곽 배치를 추천합니다."
        else:
            answer = "요청 내용을 행사 목적, 예상 방문객 수, 안전성, 동선 효율성을 기준으로 검토했습니다. 현재 설계에서 해당 공간을 조정할 수 있습니다. 구체적으로 '무대를 넓혀줘', '푸드존을 옮겨줘'처럼 말씀해 주세요."

        st.session_state.chat.append({"role": "assistant", "content": answer})
        st.rerun()

    # Scores
    st.divider()
    st.subheader("⑥ AI 설계 평가")
    scores = calculate_scores(st.session_state.event, st.session_state.simulation)
    cols = st.columns(len(scores))
    for col, (label, score) in zip(cols, scores.items()):
        with col:
            st.markdown(
                f'<div class="metric-card"><div class="small-label">{label}</div><div class="score">{score}</div><div class="small-label">점</div></div>',
                unsafe_allow_html=True
            )

    # Before / After
    st.divider()
    st.subheader("⑦ 설계 전 / 후 비교")
    b1, b2 = st.columns(2)
    with b1:
        st.markdown("### Before · 기존 배치")
        st.plotly_chart(draw_venue(
            st.session_state.before_layout, st.session_state.event,
            heatmap=False, optimized=False
        ), use_container_width=True)
    with b2:
        st.markdown("### After · AI 최적화 배치")
        st.plotly_chart(draw_venue(
            st.session_state.layout, st.session_state.event,
            heatmap=False, optimized=True
        ), use_container_width=True)

# -----------------------------
# Workflow
# -----------------------------
def workflow():
    st.title("🔄 AI 행사 설계 Workflow")
    st.caption("행사 입력 → 디지털 트윈 → 배치안 생성 → 군중 시뮬레이션 → 다목적 최적화 → 최종 보고서까지의 전체 과정을 시각화합니다.")

    steps = [
        ("1", "행사 정보 입력", "행사명·목적·방문객·예산·장소"),
        ("2", "디지털 트윈 생성", "입력 장소의 특성을 반영한 공간 캔버스 생성"),
        ("3", "배치안 자동 생성", "주요 시설의 후보 위치를 구성"),
        ("4", "군중 이동 시뮬레이션", "방문객 흐름과 혼잡 예상 구간 분석"),
        ("5", "다목적 최적화", "안전성·접근성·동선·예산을 종합 평가"),
        ("6", "최적 설계안 선정", "평가 점수가 높은 배치안 선택"),
        ("7", "AI 설계 이유 설명", "각 공간의 배치 근거 요약"),
        ("8", "배치도 + 분석 리포트", "최종 설계와 평가 결과 생성"),
        ("9", "Before / After", "AI 적용 전후의 차이를 비교"),
    ]

    for i in range(0, len(steps), 3):
        cols = st.columns(3)
        for j, step in enumerate(steps[i:i+3]):
            with cols[j]:
                n, title, desc = step
                st.markdown(f"""
                <div class="big-card" style="min-height:150px;margin-bottom:16px;">
                    <div style="font-size:28px;font-weight:800;color:#315efb;">{n}</div>
                    <h3>{title}</h3>
                    <p style="color:#64748b;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)

# -----------------------------
# Report
# -----------------------------
def report_page():
    st.title("📄 AI 보고서")
    if not st.session_state.event:
        st.info("먼저 대시보드에서 행사를 설계해주세요.")
        if st.button("대시보드로 이동"):
            st.session_state.page = "dashboard"
            st.rerun()
        return

    scores = calculate_scores(st.session_state.event, st.session_state.simulation)
    report = generate_report(st.session_state.event, scores)
    st.session_state.report = report

    st.markdown('<div class="report-box">', unsafe_allow_html=True)
    st.markdown(report)
    st.markdown('</div>', unsafe_allow_html=True)

    st.download_button(
        "⬇️ 상사 보고용 보고서 다운로드",
        data=report,
        file_name=f"{st.session_state.event.get('name','event')}_AI_report.md",
        mime="text/markdown",
        use_container_width=True
    )

# -----------------------------
# App router
# -----------------------------
topbar()

nav = st.columns([1, 1, 1, 1])
with nav[0]:
    if st.button("🏠 홈", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
with nav[1]:
    if st.button("📊 대시보드", use_container_width=True):
        if st.session_state.logged_in:
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.warning("로그인 후 이용할 수 있습니다.")
with nav[2]:
    if st.button("🔄 설계 프로세스", use_container_width=True):
        st.session_state.page = "workflow"
        st.rerun()
with nav[3]:
    if st.button("📄 AI 보고서", use_container_width=True):
        if st.session_state.logged_in:
            st.session_state.page = "report"
            st.rerun()
        else:
            st.warning("로그인 후 이용할 수 있습니다.")

st.divider()

if st.session_state.page == "home":
    home()
elif st.session_state.page == "dashboard":
    dashboard()
elif st.session_state.page == "workflow":
    workflow()
elif st.session_state.page == "report":
    report_page()
