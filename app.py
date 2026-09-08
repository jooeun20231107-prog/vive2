import streamlit as st
import plotly.graph_objects as go
import hashlib
import math
from datetime import datetime


# =========================================================
# Event Architect AI
# =========================================================

st.set_page_config(
    page_title="Event Architect AI",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# Session State
# =========================================================

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

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f5f7fb;
    }

    header {
        visibility: hidden;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }

    .hero {
        background: linear-gradient(135deg, #eef2ff, #ffffff);
        border: 1px solid #dfe5ff;
        border-radius: 24px;
        padding: 45px 35px;
        margin-bottom: 25px;
    }

    .hero h1 {
        color: #172554;
        font-size: 40px;
        margin-bottom: 10px;
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
        min-height: 260px;
        box-shadow: 0 5px 20px rgba(30,50,90,.05);
    }

    .big-card h2 {
        color: #172554;
    }

    .metric-card {
        background: white;
        border: 1px solid #e5e9f2;
        border-radius: 16px;
        padding: 18px;
        text-align: center;
    }

    .score {
        font-size: 30px;
        font-weight: 800;
        color: #315efb;
    }

    .small-label {
        color: #64748b;
        font-size: 13px;
    }

    .zone-note {
        background: #f8fafc;
        border-left: 4px solid #315efb;
        padding: 15px;
        border-radius: 8px;
        line-height: 1.7;
    }

    .report-box {
        background: white;
        padding: 30px;
        border-radius: 18px;
        border: 1px solid #e5e9f2;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 회원 관련 함수
# =========================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def login_user(username, password):

    users = st.session_state.users

    if username in users:

        if users[username] == hash_password(password):

            st.session_state.logged_in = True
            st.session_state.username = username

            return True

    return False


def register_user(username, password, confirm):

    if not username:
        return False, "아이디를 입력해주세요."

    if not password:
        return False, "비밀번호를 입력해주세요."

    if len(password) < 4:
        return False, "비밀번호는 4자리 이상 입력해주세요."

    if password != confirm:
        return False, "비밀번호가 서로 다릅니다."

    if username in st.session_state.users:
        return False, "이미 존재하는 아이디입니다."

    st.session_state.users[username] = hash_password(password)

    return True, "회원가입이 완료되었습니다."


# =========================================================
# 장소 유형 분석
# =========================================================

def place_profile(place):

    place = place.lower()

    if any(
        word in place
        for word in [
            "공원",
            "야외",
            "운동장",
            "광장",
            "잔디",
            "마당"
        ]
    ):
        return "야외"

    if any(
        word in place
        for word in [
            "학교",
            "체육관",
            "강당",
            "전시장",
            "컨벤션"
        ]
    ):
        return "실내"

    return "일반"


# =========================================================
# 행사장 배치 생성
# =========================================================

def make_layout(event, optimized=True):

    people = int(event.get("people", 500))

    W = 100
    H = 64

    if optimized:

        zones = {

            "무대":
                (30, 47, 40, 13),

            "푸드 존":
                (5, 36, 20, 13),

            "부스":
                (5, 17, 20, 15),

            "휴식 구역":
                (29, 6, 23, 12),

            "정보 센터":
                (75, 39, 19, 10),

            "의료 센터":
                (75, 25, 19, 10),

            "화장실":
                (75, 13, 19, 9),

            "비상구":
                (42, 2, 16, 6),
        }

    else:

        zones = {

            "무대":
                (4, 47, 40, 13),

            "푸드 존":
                (49, 42, 45, 13),

            "부스":
                (4, 25, 42, 15),

            "휴식 구역":
                (50, 22, 22, 12),

            "정보 센터":
                (74, 18, 20, 10),

            "의료 센터":
                (4, 8, 18, 10),

            "화장실":
                (30, 7, 18, 10),

            "비상구":
                (76, 3, 18, 9),
        }

    return {
        "W": W,
        "H": H,
        "zones": zones,
        "profile": place_profile(
            event.get("place", "")
        )
    }


# =========================================================
# 공간 배치 이유
# =========================================================

def zone_reason(zone, event):

    people = int(
        event.get("people", 500)
    )

    purpose = event.get(
        "purpose",
        "행사 운영"
    )

    reasons = {

        "무대":
            f"행사의 핵심 프로그램이 진행되는 공간입니다. 약 {people:,}명의 방문객이 한 방향으로 모일 가능성을 고려해 넓은 관람 공간을 확보할 수 있는 위치에 배치했습니다.",

        "푸드 존":
            "음식 공간은 대기열이 발생할 수 있기 때문에 주요 이동 동선과 약간 떨어진 위치에 배치했습니다. 이를 통해 식음 공간의 대기줄이 행사장 전체의 이동을 방해하는 것을 줄였습니다.",

        "부스":
            "방문객들이 자연스럽게 여러 부스를 돌아볼 수 있도록 한쪽 영역에 연속적으로 배치했습니다. 부스 사이의 이동 통로도 확보했습니다.",

        "휴식 구역":
            "장시간 행사에 참여하는 방문객이 잠시 쉬어갈 수 있는 완충 공간입니다. 주요 시설 사이에 배치해 방문객을 분산시키는 역할을 합니다.",

        "정보 센터":
            "방문객이 쉽게 찾을 수 있도록 주요 동선에서 접근하기 쉬운 위치에 배치했습니다. 안내와 문의를 한 곳에서 처리할 수 있습니다.",

        "의료 센터":
            "응급상황에 빠르게 대응할 수 있도록 행사장 외곽 접근성과 내부 접근성을 모두 고려한 위치에 배치했습니다.",

        "화장실":
            "방문객이 쉽게 접근할 수 있으면서도 주요 이동 동선을 방해하지 않도록 외곽에 배치했습니다.",

        "비상구":
            "비상상황 발생 시 신속한 대피가 가능하도록 외곽에 배치했습니다. 다른 시설과 겹치지 않는 대피 동선을 확보했습니다."
    }

    return reasons.get(
        zone,
        f"'{purpose}'라는 행사 목적과 방문객 동선을 고려하여 배치했습니다."
    )


# =========================================================
# 행사장 그래프
# =========================================================

def draw_venue(
    layout,
    event,
    heatmap=False,
    optimized=True
):

    W = layout["W"]
    H = layout["H"]

    fig = go.Figure()

    # 행사장 배경

    fig.add_shape(

        type="rect",

        x0=0,
        y0=0,
        x1=W,
        y1=H,

        fillcolor="#eef2f7",

        line=dict(
            color="#cbd5e1",
            width=2
        )
    )

    # =====================================================
    # Heatmap
    # =====================================================

    if heatmap:

        grid_n = 45

        xs = [
            i * W / (grid_n - 1)
            for i in range(grid_n)
        ]

        ys = [
            i * H / (grid_n - 1)
            for i in range(grid_n)
        ]

        if optimized:

            hotspots = [
                (50, 48, 1.0),
                (18, 38, .8),
                (67, 31, .65),
                (50, 17, .45)
            ]

        else:

            hotspots = [
                (22, 48, .95),
                (68, 47, .92),
                (43, 30, .85),
                (83, 20, .65)
            ]

        people = int(
            event.get("people", 500)
        )

        base = min(
            0.32,
            0.08 + people / 20000
        )

        z = []

        for y in ys:

            row = []

            for x in xs:

                value = base

                for hx, hy, strength in hotspots:

                    distance = (
                        (x - hx) ** 2
                        +
                        (y - hy) ** 2
                    )

                    value += (
                        strength
                        *
                        math.exp(
                            -distance / 180
                        )
                    )

                row.append(value)

            z.append(row)

        fig.add_trace(

            go.Heatmap(

                x=xs,
                y=ys,
                z=z,

                colorscale="Turbo",

                opacity=0.55,

                showscale=True,

                colorbar=dict(
                    title="혼잡도"
                )
            )
        )

    # =====================================================
    # 시설
    # =====================================================

    zone_colors = {

        "무대":
            "#dbeafe",

        "푸드 존":
            "#ffedd5",

        "부스":
            "#ede9fe",

        "휴식 구역":
            "#dcfce7",

        "정보 센터":
            "#e0e7ff",

        "의료 센터":
            "#fee2e2",

        "화장실":
            "#f1f5f9",

        "비상구":
            "#fef3c7"
    }

    for name, (
        x,
        y,
        w,
        h
    ) in layout["zones"].items():

        fig.add_shape(

            type="rect",

            x0=x,
            y0=y,

            x1=x+w,
            y1=y+h,

            fillcolor=zone_colors.get(
                name,
                "#ffffff"
            ),

            line=dict(
                color="#475569",
                width=1.5
            )
        )

        fig.add_annotation(

            x=x+w/2,
            y=y+h/2,

            text=f"<b>{name}</b>",

            showarrow=False,

            font=dict(
                size=12,
                color="#172554"
            )
        )

    # =====================================================
    # 입구
    # =====================================================

    fig.add_shape(

        type="rect",

        x0=43,
        y0=0,

        x1=57,
        y1=4,

        fillcolor="#bfdbfe",

        line=dict(
            color="#2563eb"
        )
    )

    fig.add_annotation(

        x=50,
        y=2,

        text="입구",

        showarrow=False,

        font=dict(
            size=12,
            color="#1e3a8a"
        )
    )

    # =====================================================
    # 주요 이동 동선
    # =====================================================

    routes = [

        (
            [50, 50, 50],
            [4, 20, 47]
        ),

        (
            [25, 30, 75],
            [25, 25, 30]
        ),

        (
            [50, 75],
            [30, 44]
        )
    ]

    for rx, ry in routes:

        fig.add_trace(

            go.Scatter(

                x=rx,
                y=ry,

                mode="lines",

                line=dict(
                    color="#2563eb",
                    width=3,
                    dash="dot"
                ),

                hoverinfo="skip",

                showlegend=False
            )
        )

    fig.update_xaxes(
        range=[0, W],
        visible=False
    )

    fig.update_yaxes(
        range=[0, H],
        visible=False,
        scaleanchor="x",
        scaleratio=1
    )

    fig.update_layout(

        height=590,

        margin=dict(
            l=5,
            r=5,
            t=5,
            b=5
        ),

        paper_bgcolor="white",

        plot_bgcolor="white",

        showlegend=False
    )

    return fig


# =========================================================
# 평가 점수
# =========================================================

def calculate_scores(
    event,
    simulation=False
):

    people = int(
        event.get("people", 500)
    )

    budget = int(
        event.get("budget", 0)
    )

    scores = {

        "안전성":
            min(
                98,
                88
                + (5 if simulation else 0)
                + (3 if people < 5000 else 0)
            ),

        "접근성":
            91,

        "동선 효율성":
            min(
                97,
                84
                + (6 if simulation else 0)
            ),

        "혼잡도 관리":
            min(
                96,
                78
                + (10 if simulation else 0)
                + (3 if people < 3000 else 0)
            ),

        "예산 효율성":
            min(
                95,
                82
                + (
                    6
                    if budget >= 3_000_000
                    else 2
                )
            )
    }

    return scores


# =========================================================
# 보고서
# =========================================================

def generate_report(
    event,
    scores
):

    name = event.get(
        "name",
        "행사"
    )

    purpose = event.get(
        "purpose",
        ""
    )

    people = event.get(
        "people",
        0
    )

    budget = event.get(
        "budget",
        0
    )

    place = event.get(
        "place",
        ""
    )

    duration = event.get(
        "duration",
        0
    )

    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M"
    )

    return f"""
# AI 행사 설계 보고서

## 1. 행사 개요

- 행사명: {name}
- 행사 목적: {purpose}
- 예상 방문객: {people:,}명
- 예산: {budget:,}원
- 행사 장소: {place}
- 진행 시간: {duration}시간

---

## 2. AI 행사장 설계 결과

AI는 입력된 행사 목적, 예상 방문객 수, 예산 및 행사 장소를 기반으로 행사장 공간을 자동 설계했습니다.

주요 배치 시설:

- 무대
- 푸드 존
- 부스
- 휴식 구역
- 정보 센터
- 의료 센터
- 화장실
- 비상구

주요 시설 간 이동 동선을 확보하고 방문객이 특정 공간에 집중되는 현상을 줄이는 방향으로 설계했습니다.

---

## 3. AI 평가 결과

- 안전성: {scores["안전성"]}점
- 접근성: {scores["접근성"]}점
- 동선 효율성: {scores["동선 효율성"]}점
- 혼잡도 관리: {scores["혼잡도 관리"]}점
- 예산 효율성: {scores["예산 효율성"]}점

---

## 4. AI 개선 권장 사항

1. 행사 시작 및 종료 시간에 입구 주변의 혼잡도를 집중적으로 관리합니다.
2. 푸드 존의 대기열이 주요 이동 동선을 막지 않도록 별도의 대기 공간을 확보합니다.
3. 의료 센터와 비상구 위치를 쉽게 확인할 수 있도록 안내 표지판을 설치합니다.
4. 방문객 수가 증가할 경우 휴식 공간과 안내 인력을 추가하는 것을 권장합니다.

---

## 5. 결론

본 설계안은 안전성, 접근성, 동선 효율성, 혼잡도 관리 및 예산 효율성을 종합적으로 고려한 AI 기반 행사장 설계안입니다.

작성 시각: {now}
"""


# =========================================================
# ⭐ 로그인 / 회원가입
# =========================================================

def auth_area():

    st.markdown("## 🔐 계정")

    # 현재 선택한 메뉴를 먼저 보여줌
    if st.session_state.auth_mode == "signup":

        signup_tab, login_tab = st.tabs(
            ["회원가입", "로그인"]
        )

    else:

        login_tab, signup_tab = st.tabs(
            ["로그인", "회원가입"]
        )

    # =====================================================
    # 로그인
    # =====================================================

    with login_tab:

        # ⭐ form을 사용해서 입력 중 rerun 방지
        with st.form(
            "login_form",
            clear_on_submit=False
        ):

            username = st.text_input(
                "아이디",
                placeholder="아이디를 입력하세요"
            )

            password = st.text_input(
                "비밀번호",
                type="password",
                placeholder="비밀번호를 입력하세요"
            )

            login_submit = st.form_submit_button(
                "로그인",
                use_container_width=True
            )

        if login_submit:

            if login_user(
                username,
                password
            ):

                st.session_state.logged_in = True

                st.session_state.username = username

                st.session_state.auth_mode = None

                st.success(
                    "로그인되었습니다!"
                )

                st.rerun()

            else:

                st.error(
                    "아이디 또는 비밀번호가 올바르지 않습니다."
                )

    # =====================================================
    # 회원가입
    # =====================================================

    with signup_tab:

        # ⭐ 회원가입도 form 사용
        with st.form(
            "signup_form",
            clear_on_submit=False
        ):

            new_username = st.text_input(
                "아이디",
                placeholder="사용할 아이디를 입력하세요"
            )

            new_password = st.text_input(
                "비밀번호",
                type="password",
                placeholder="비밀번호를 입력하세요"
            )

            confirm_password = st.text_input(
                "비밀번호 확인",
                type="password",
                placeholder="비밀번호를 다시 입력하세요"
            )

            signup_submit = st.form_submit_button(
                "회원가입",
                use_container_width=True
            )

        if signup_submit:

            success, message = register_user(
                new_username,
                new_password,
                confirm_password
            )

            if success:

                st.success(
                    "회원가입이 완료되었습니다!"
                )

                st.info(
                    "이제 로그인 탭에서 로그인해주세요."
                )

            else:

                st.error(message)


# =========================================================
# 상단 메뉴
# =========================================================

def topbar():

    col1, col2, col3, col4 = st.columns(
        [5.5, 1.4, 1.4, 1.4]
    )

    # =====================================================
    # 로고
    # =====================================================

    with col1:

        if st.button(
            "🏗️ Event Architect AI",
            key="logo_button"
        ):

            st.session_state.page = "home"

            st.session_state.auth_mode = None

            st.rerun()

    # =====================================================
    # 로그인
    # =====================================================

    with col2:

        if st.session_state.logged_in:

            st.caption(
                f"👤 {st.session_state.username}님"
            )

        else:

            if st.button(
                "로그인",
                key="top_login",
                use_container_width=True
            ):

                st.session_state.page = "home"

                st.session_state.auth_mode = "login"

                st.rerun()

    # =====================================================
    # 회원가입
    # =====================================================

    with col3:

        if not st.session_state.logged_in:

            if st.button(
                "회원가입",
                key="top_signup",
                use_container_width=True
            ):

                st.session_state.page = "home"

                st.session_state.auth_mode = "signup"

                st.rerun()

        else:

            if st.button(
                "🏠 홈",
                key="top_home",
                use_container_width=True
            ):

                st.session_state.page = "home"

                st.rerun()

    # =====================================================
    # 설정
    # =====================================================

    with col4:

        if st.button(
            "⚙️ 설정",
            key="settings_button",
            use_container_width=True
        ):

            st.session_state.settings_open = not st.session_state.settings_open

    # =====================================================
    # 설정창
    # =====================================================

    if st.session_state.settings_open:

        with st.expander(
            "⚙️ 설정",
            expanded=True
        ):

            st.markdown("### 계정 설정")

            if st.session_state.logged_in:

                st.write(
                    f"현재 로그인: **{st.session_state.username}**"
                )

                if st.button(
                    "로그아웃",
                    key="logout_button"
                ):

                    st.session_state.logged_in = False

                    st.session_state.username = ""

                    st.session_state.page = "home"

                    st.session_state.settings_open = False

                    st.rerun()

            else:

                st.info(
                    "현재 로그인하지 않았습니다."
                )

            st.markdown("### 앱 설정")

            st.toggle(
                "분석 애니메이션 사용",
                value=True
            )

            st.selectbox(
                "언어",
                ["한국어"]
            )


# =========================================================
# 홈 화면
# =========================================================

def home():

    st.markdown(
        """
        <div class="hero">

            <h1>
                AI 기반 행사 자동 설계 플랫폼
            </h1>

            <p>
                행사 정보를 입력하면 AI가 행사장 공간을 설계하고
                군중 흐름과 혼잡도를 분석합니다.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # 로그인 / 회원가입 화면
    # =====================================================

    if (
        not st.session_state.logged_in
        and st.session_state.auth_mode
    ):

        auth_area()

        st.divider()

    # =====================================================
    # 홈 카드
    # =====================================================

    st.subheader(
        "무엇을 하시겠어요?"
    )

    col1, col2 = st.columns(2)

    # =====================================================
    # Dashboard
    # =====================================================

    with col1:

        st.markdown(
            """
            <div class="big-card">

                <h2>📊 대시보드</h2>

                <p>
                    행사 정보를 입력하고 AI가
                    최적의 행사장 공간을 설계합니다.
                </p>

                <ul>
                    <li>디지털 트윈 행사장</li>
                    <li>시설 자동 배치</li>
                    <li>군중 예측 Heatmap</li>
                    <li>Before / After 비교</li>
                </ul>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "대시보드 열기 →",
            key="dashboard_home",
            use_container_width=True
        ):

            if not st.session_state.logged_in:

                st.warning(
                    "대시보드를 사용하려면 먼저 로그인해주세요."
                )

                st.session_state.auth_mode = "login"

                st.rerun()

            else:

                st.session_state.page = "dashboard"

                st.rerun()

    # =====================================================
    # AI Report
    # =====================================================

    with col2:

        st.markdown(
            """
            <div class="big-card">

                <h2>📄 AI 보고서</h2>

                <p>
                    완성된 행사 설계를 상사에게
                    보고할 수 있는 형태로 정리합니다.
                </p>

                <ul>
                    <li>행사 개요</li>
                    <li>AI 설계 결과</li>
                    <li>안전·접근성·동선 분석</li>
                    <li>개선 권장 사항</li>
                </ul>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "AI 보고서 열기 →",
            key="report_home",
            use_container_width=True
        ):

            if not st.session_state.logged_in:

                st.warning(
                    "AI 보고서를 사용하려면 먼저 로그인해주세요."
                )

                st.session_state.auth_mode = "login"

                st.rerun()

            else:

                st.session_state.page = "report"

                st.rerun()


# =========================================================
# Dashboard
# =========================================================

def dashboard():

    st.title(
        "📊 AI 행사 설계 대시보드"
    )

    st.caption(
        "행사 정보를 입력하고 AI 이벤트 디자인을 생성하세요."
    )

    # =====================================================
    # 행사 정보
    # =====================================================

    with st.container(border=True):

        st.subheader(
            "① 행사 정보"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            name = st.text_input(
                "이벤트 이름",
                value=st.session_state.event.get(
                    "name",
                    "2026 청소년 문화축제"
                )
            )

            purpose = st.text_area(
                "이벤트 목적",
                value=st.session_state.event.get(
                    "purpose",
                    "청소년 문화 교류와 체험 기회 제공"
                )
            )

        with col2:

            people = st.number_input(
                "예상 방문객 수",
                min_value=1,
                max_value=100000,
                value=int(
                    st.session_state.event.get(
                        "people",
                        5000
                    )
                ),
                step=100
            )

            budget = st.number_input(
                "예산 (원)",
                min_value=0,
                max_value=10_000_000_000,
                value=int(
                    st.session_state.event.get(
                        "budget",
                        50_000_000
                    )
                ),
                step=1_000_000
            )

        with col3:

            place = st.text_input(
                "장소",
                value=st.session_state.event.get(
                    "place",
                    "시민공원"
                )
            )

            duration = st.number_input(
                "진행 시간",
                min_value=1,
                max_value=24,
                value=int(
                    st.session_state.event.get(
                        "duration",
                        5
                    )
                )
            )

        # =================================================
        # AI 디자인 생성
        # =================================================

        if st.button(
            "✨ AI 이벤트 디자인 생성",
            type="primary",
            use_container_width=True
        ):

            st.session_state.event = {

                "name": name,

                "purpose": purpose,

                "people": people,

                "budget": budget,

                "place": place,

                "duration": duration
            }

            st.session_state.before_layout = make_layout(
                st.session_state.event,
                optimized=False
            )

            st.session_state.layout = make_layout(
                st.session_state.event,
                optimized=True
            )

            st.session_state.simulation = False

            st.session_state.selected_zone = None

            st.session_state.chat = [

                {
                    "role": "assistant",

                    "content":
                        f"'{name}' 행사에 맞는 AI 행사장 배치를 생성했습니다. 시설 버튼을 눌러 배치 이유를 확인해보세요."
                }
            ]

            scores = calculate_scores(
                st.session_state.event
            )

            st.session_state.report = generate_report(
                st.session_state.event,
                scores
            )

            st.rerun()

    # =====================================================
    # 설계 전이면 종료
    # =====================================================

    if not st.session_state.layout:

        st.info(
            "행사 정보를 입력하고 **AI 이벤트 디자인 생성** 버튼을 눌러주세요."
        )

        return

    st.divider()

    # =====================================================
    # 디지털 트윈
    # =====================================================

    left, right = st.columns(
        [7, 3]
    )

    with left:

        st.subheader(
            "② 디지털 트윈 행사장"
        )

        st.caption(
            f"장소 유형: {st.session_state.layout['profile']} | "
            f"{st.session_state.event['place']}"
        )

        fig = draw_venue(

            st.session_state.layout,

            st.session_state.event,

            heatmap=st.session_state.simulation,

            optimized=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        if st.session_state.simulation:

            st.success(
                "AI 군중 시뮬레이션 완료 — 색이 진할수록 혼잡도가 높은 구간입니다."
            )

        else:

            st.caption(
                "점선은 주요 이동 동선입니다."
            )

        # =================================================
        # 시설 버튼
        # =================================================

        st.markdown(
            "### 시설 선택"
        )

        zone_names = list(
            st.session_state.layout[
                "zones"
            ].keys()
        )

        cols = st.columns(4)

        for i, zone in enumerate(zone_names):

            with cols[i % 4]:

                if st.button(
                    zone,
                    key=f"zone_{zone}",
                    use_container_width=True
                ):

                    st.session_state.selected_zone = zone

                    st.rerun()

    # =====================================================
    # 오른쪽 설명
    # =====================================================

    with right:

        st.subheader(
            "③ 공간 배치 이유"
        )

        if st.session_state.selected_zone:

            zone = st.session_state.selected_zone

            st.markdown(
                f"### 📍 {zone}"
            )

            st.markdown(
                f"""
                <div class="zone-note">
                {zone_reason(
                    zone,
                    st.session_state.event
                )}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.info(
                "시설명을 클릭하면 AI가 해당 공간을 왜 그 위치에 배치했는지 설명합니다."
            )

        st.divider()

        st.subheader(
            "④ AI 시뮬레이션"
        )

        st.write(
            "AI가 예상 방문객 흐름을 분석하여 혼잡 예상 구간을 표시합니다."
        )

        if st.button(
            "🧠 AI 시뮬레이션 실행",
            type="primary",
            use_container_width=True
        ):

            st.session_state.simulation = True

            scores = calculate_scores(
                st.session_state.event,
                True
            )

            st.session_state.report = generate_report(
                st.session_state.event,
                scores
            )

            st.rerun()

        if st.session_state.simulation:

            st.markdown(
                "**혼잡도 범례**"
            )

            st.write(
                "🟢 낮음　🟡 보통　🔴 높음"
            )

    # =====================================================
    # AI Chat
    # =====================================================

    st.divider()

    st.subheader(
        "⑤ AI 디자인 상담"
    )

    st.caption(
        "원하는 행사장 변경사항을 AI에게 자연어로 입력해보세요."
    )

    for message in st.session_state.chat:

        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )

    prompt = st.chat_input(
        "예: 푸드존을 입구에서 멀리 옮겨줘"
    )

    if prompt:

        st.session_state.chat.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        p = prompt.lower()

        if (
            "푸드" in p
            or "음식" in p
        ):

            answer = (
                "푸드 존은 대기열이 주요 이동 동선을 "
                "막지 않도록 가장자리 쪽에 배치하는 것이 좋습니다."
            )

        elif "휴식" in p:

            answer = (
                "휴식 구역을 확대하면 장시간 행사에서 "
                "방문객의 체류 부담을 줄이고 혼잡을 분산할 수 있습니다."
            )

        elif "무대" in p:

            answer = (
                "무대는 행사 핵심 시설이므로 관람객의 시야와 "
                "대피 동선을 고려해 중앙 상단에 배치하는 것을 추천합니다."
            )

        elif (
            "의료" in p
            or "응급" in p
        ):

            answer = (
                "의료 센터는 행사장 중심과 외부 접근성을 "
                "동시에 확보할 수 있는 위치에 배치하는 것이 좋습니다."
            )

        elif "부스" in p:

            answer = (
                "부스는 방문객이 자연스럽게 순환할 수 있도록 "
                "연속 배치하고 부스 사이에 충분한 통로를 확보하는 것이 좋습니다."
            )

        elif "화장실" in p:

            answer = (
                "화장실은 방문객이 쉽게 접근할 수 있으면서 "
                "주요 이동 동선을 방해하지 않는 외곽 배치를 추천합니다."
            )

        else:

            answer = (
                "요청 내용을 행사 목적, 방문객 수, 안전성, "
                "동선 효율성을 기준으로 분석했습니다. "
                "예를 들어 '무대를 넓혀줘', "
                "'푸드존을 옮겨줘'처럼 구체적으로 말씀해주세요."
            )

        st.session_state.chat.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        st.rerun()

    # =====================================================
    # 점수
    # =====================================================

    st.divider()

    st.subheader(
        "⑥ AI 설계 평가"
    )

    scores = calculate_scores(
        st.session_state.event,
        st.session_state.simulation
    )

    score_cols = st.columns(
        len(scores)
    )

    for col, (
        label,
        score
    ) in zip(
        score_cols,
        scores.items()
    ):

        with col:

            st.markdown(
                f"""
                <div class="metric-card">

                    <div class="small-label">
                        {label}
                    </div>

                    <div class="score">
                        {score}
                    </div>

                    <div class="small-label">
                        점
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    # =====================================================
    # Before / After
    # =====================================================

    st.divider()

    st.subheader(
        "⑦ Before / After"
    )

    before_col, after_col = st.columns(2)

    with before_col:

        st.markdown(
            "### Before · 기존 배치"
        )

        st.plotly_chart(

            draw_venue(

                st.session_state.before_layout,

                st.session_state.event,

                heatmap=False,

                optimized=False
            ),

            use_container_width=True
        )

    with after_col:

        st.markdown(
            "### After · AI 최적화 배치"
        )

        st.plotly_chart(

            draw_venue(

                st.session_state.layout,

                st.session_state.event,

                heatmap=False,

                optimized=True
            ),

            use_container_width=True
        )


# =========================================================
# Workflow
# =========================================================

def workflow():

    st.title(
        "🔄 AI 행사 설계 Workflow"
    )

    st.caption(
        "행사 입력부터 최종 보고서까지의 전체 과정을 보여줍니다."
    )

    steps = [

        (
            "1",
            "행사 정보 입력",
            "행사명·목적·방문객·예산·장소"
        ),

        (
            "2",
            "디지털 트윈 생성",
            "행사 장소의 특성을 반영한 공간 생성"
        ),

        (
            "3",
            "배치안 자동 생성",
            "주요 시설의 위치 자동 구성"
        ),

        (
            "4",
            "군중 이동 시뮬레이션",
            "방문객 흐름과 혼잡 구간 분석"
        ),

        (
            "5",
            "다목적 최적화",
            "안전·접근성·동선·예산 분석"
        ),

        (
            "6",
            "최적 설계안 선정",
            "평가 결과를 기반으로 설계안 선정"
        ),

        (
            "7",
            "AI 설계 이유 설명",
            "각 시설의 배치 근거 설명"
        ),

        (
            "8",
            "배치도 + 분석 리포트",
            "최종 행사장과 분석 결과 생성"
        ),

        (
            "9",
            "Before / After",
            "AI 적용 전후 비교"
        )
    ]

    for i in range(
        0,
        len(steps),
        3
    ):

        cols = st.columns(3)

        for j, step in enumerate(
            steps[i:i+3]
        ):

            with cols[j]:

                number, title, description = step

                st.markdown(
                    f"""
                    <div class="big-card"
                         style="min-height:150px;
                                margin-bottom:16px;">

                        <div style="
                            font-size:28px;
                            font-weight:800;
                            color:#315efb;">
                            {number}
                        </div>

                        <h3>
                            {title}
                        </h3>

                        <p style="
                            color:#64748b;">
                            {description}
                        </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


# =========================================================
# AI Report
# =========================================================

def report_page():

    st.title(
        "📄 AI 보고서"
    )

    if not st.session_state.event:

        st.info(
            "먼저 대시보드에서 행사를 설계해주세요."
        )

        if st.button(
            "대시보드로 이동"
        ):

            st.session_state.page = "dashboard"

            st.rerun()

        return

    scores = calculate_scores(
        st.session_state.event,
        st.session_state.simulation
    )

    report = generate_report(
        st.session_state.event,
        scores
    )

    st.markdown(
        '<div class="report-box">',
        unsafe_allow_html=True
    )

    st.markdown(report)

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    st.download_button(

        "⬇️ 상사 보고용 보고서 다운로드",

        data=report,

        file_name=
            f"{st.session_state.event.get('name', 'event')}_AI_report.md",

        mime="text/markdown",

        use_container_width=True
    )


# =========================================================
# 상단 메뉴 실행
# =========================================================

topbar()


# =========================================================
# 메뉴
# =========================================================

nav1, nav2, nav3, nav4 = st.columns(4)


with nav1:

    if st.button(
        "🏠 홈",
        use_container_width=True
    ):

        st.session_state.page = "home"

        st.rerun()


with nav2:

    if st.button(
        "📊 대시보드",
        use_container_width=True
    ):

        if st.session_state.logged_in:

            st.session_state.page = "dashboard"

            st.rerun()

        else:

            st.session_state.page = "home"

            st.session_state.auth_mode = "login"

            st.rerun()


with nav3:

    if st.button(
        "🔄 설계 프로세스",
        use_container_width=True
    ):

        st.session_state.page = "workflow"

        st.rerun()


with nav4:

    if st.button(
        "📄 AI 보고서",
        use_container_width=True
    ):

        if st.session_state.logged_in:

            st.session_state.page = "report"

            st.rerun()

        else:

            st.session_state.page = "home"

            st.session_state.auth_mode = "login"

            st.rerun()


st.divider()


# =========================================================
# 페이지 이동
# =========================================================

if st.session_state.page == "home":

    home()

elif st.session_state.page == "dashboard":

    dashboard()

elif st.session_state.page == "workflow":

    workflow()

elif st.session_state.page == "report":

    report_page()
