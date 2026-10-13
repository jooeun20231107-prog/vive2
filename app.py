<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>이벤트 온 (Event On) - AI 기반 행사 자동 설계 및 디지털 트윈 관제 플랫폼</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
    <style>
        body { font-family: Pretendard, -apple-system, system-ui, sans-serif; }
        .glass-panel { background: rgba(255, 255, 255, 0.92); backdrop-filter: blur(14px); border: 1px solid rgba(226, 232, 240, 0.8); }
        .dark .glass-panel { background: rgba(15, 23, 42, 0.92); border: 1px solid rgba(51, 65, 85, 0.8); }
        .wrap { position: relative; width: 100%; background: #1e293b; border-radius: 12px; overflow: hidden; aspect-ratio: 1.85; }
        .wrap canvas, .wrap .c3 { position: absolute; inset: 0; width: 100%; height: 100%; }
        .c3 { cursor: grab; background: linear-gradient(#e0f2fe, #f8fafc); }
        .dark .c3 { background: linear-gradient(#0f172a, #1e293b); }
        .legend { position: absolute; left: 12px; bottom: 12px; background: rgba(255, 255, 255, 0.95); border-radius: 8px; padding: 8px 12px; font-size: 11px; font-weight: 700; display: grid; grid-template-columns: repeat(3, auto); gap: 4px 12px; z-index: 5; pointer-events: none; }
        .dark .legend { background: rgba(15, 23, 42, 0.95); color: #f8fafc; }
        .legend i { display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: 4px; }
        .hint { position: absolute; right: 12px; top: 12px; background: rgba(15, 23, 42, 0.7); color: #fff; font-size: 11px; padding: 4px 10px; border-radius: 8px; z-index: 5; pointer-events: none; }
        .zl { display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 6px; font-size: 11px; font-weight: 700; max-height: 160px; overflow: auto; }
        .zl span { background: #f8fafc; border: 1px solid #e2e8f0; border-left: 5px solid var(--c); border-radius: 6px; padding: 5px 8px; }
        .dark .zl span { background: #1e293b; border-color: #334155; color: #f8fafc; }
        .modal-backdrop { background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(6px); }
        .screen { display: none; }
        .screen.active { display: flex; }
    </style>
</head>
<body class="bg-slate-50 dark:bg-slate-950 text-slate-800 dark:text-slate-100 min-h-screen flex flex-col p-3 md:p-5 transition-colors duration-300">

    <!-- 0. 홈 화면 (Landing & Dashboard Hub) -->
    <div id="screen-home" class="screen active flex-col flex-1 max-w-7xl mx-auto w-full gap-6">
        <!-- Hero Header -->
        <header class="glass-panel rounded-3xl p-6 md:p-10 shadow-lg relative overflow-hidden flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="absolute -right-16 -bottom-16 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none"></div>
            <div class="space-y-3 max-w-2xl z-10">
                <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-100 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300 text-xs font-bold">
                    <i class="fa-solid fa-wand-magic-sparkles"></i> AI 디지털 트윈 스마트 관제 솔루션
                </div>
                <h1 class="text-3xl md:text-5xl font-black tracking-tight text-slate-900 dark:text-white leading-tight">
                    행사의 모든 순간을 <br><span class="text-indigo-600 dark:text-indigo-400">지능형 디지털 트윈</span>으로 설계하다
                </h1>
                <p class="text-sm md:text-base text-slate-600 dark:text-slate-300 leading-relaxed">
                    예산, 방문객, 장소 조건만 입력하면 AI가 수천 가지 공간 배치안과 군중 시뮬레이션을 분석하여 완벽한 행사장을 자동 완성하고 실시간 모니터링합니다.
                </p>
                <div class="flex flex-wrap gap-3 pt-2">
                    <button onclick="goToWorkspace()" class="px-6 py-3 text-sm font-bold rounded-2xl bg-gradient-to-r from-indigo-600 to-violet-600 text-white shadow-xl shadow-indigo-500/30 hover:opacity-95 transition flex items-center gap-2">
                        <i class="fa-solid fa-play"></i> 새 행사 디지털 트윈 시작하기
                    </button>
                    <button onclick="openWorkflowModal()" class="px-6 py-3 text-sm font-bold rounded-2xl bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-200 border border-slate-200 dark:border-slate-800 hover:bg-slate-50 transition flex items-center gap-2">
                        <i class="fa-solid fa-diagram-project text-indigo-500"></i> AI 프로세스 살펴보기
                    </button>
                </div>
            </div>
            
            <div class="grid grid-cols-2 gap-3 w-full md:w-auto z-10">
                <div class="glass-panel p-5 rounded-2xl text-center shadow-sm">
                    <div class="text-2xl md:text-3xl font-black text-indigo-600 dark:text-indigo-400">92.4점</div>
                    <div class="text-xs font-bold text-slate-500 mt-1">AI 평균 설계 최적화율</div>
                </div>
                <div class="glass-panel p-5 rounded-2xl text-center shadow-sm">
                    <div class="text-2xl md:text-3xl font-black text-emerald-600 dark:text-emerald-400">42%↓</div>
                    <div class="text-xs font-bold text-slate-500 mt-1">병목 및 대기시간 감소</div>
                </div>
                <div class="glass-panel p-5 rounded-2xl text-center shadow-sm">
                    <div class="text-2xl md:text-3xl font-black text-violet-600 dark:text-violet-400">실시간</div>
                    <div class="text-xs font-bold text-slate-500 mt-1">군중 이동 및 히트맵 연산</div>
                </div>
                <div class="glass-panel p-5 rounded-2xl text-center shadow-sm">
                    <div class="text-2xl md:text-3xl font-black text-amber-600 dark:text-amber-400">100%</div>
                    <div class="text-xs font-bold text-slate-500 mt-1">비상 대피로 최적 검증</div>
                </div>
            </div>
        </header>

        <!-- Feature Cards Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="glass-panel rounded-2xl p-6 shadow-sm flex flex-col justify-between">
                <div>
                    <div class="w-12 h-12 rounded-xl bg-indigo-50 dark:bg-indigo-950 text-indigo-600 dark:text-indigo-400 flex items-center justify-center text-xl font-bold mb-4">
                        <i class="fa-solid fa-sliders"></i>
                    </div>
                    <h3 class="font-bold text-base mb-2">AI 자동 파라미터 설계</h3>
                    <p class="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                        행사 목적, 규모, 장소 특성에 맞추어 부스와 편의시설 배치를 AI가 스스로 최적화하고 점수를 산출합니다.
                    </p>
                </div>
                <button onclick="openConfigModal()" class="mt-4 text-xs font-bold text-indigo-600 dark:text-indigo-400 hover:underline flex items-center gap-1">
                    설정 파라미터 편집 <i class="fa-solid fa-arrow-right"></i>
                </button>
            </div>

            <div class="glass-panel rounded-2xl p-6 shadow-sm flex flex-col justify-between">
                <div>
                    <div class="w-12 h-12 rounded-xl bg-emerald-50 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400 flex items-center justify-center text-xl font-bold mb-4">
                        <i class="fa-solid fa-cube"></i>
                    </div>
                    <h3 class="font-bold text-base mb-2">3D 디지털 트윈 관제</h3>
                    <p class="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                        Three.js 기반의 입체적 행사장 뷰와 2D 평면 맵을 전환하며 실시간 군중 밀집도와 우천·응급 상황을 시뮬레이션합니다.
                    </p>
                </div>
                <button onclick="goToWorkspace()" class="mt-4 text-xs font-bold text-emerald-600 dark:text-emerald-400 hover:underline flex items-center gap-1">
                    관제실 바로가기 <i class="fa-solid fa-arrow-right"></i>
                </button>
            </div>

            <div class="glass-panel rounded-2xl p-6 shadow-sm flex flex-col justify-between">
                <div>
                    <div class="w-12 h-12 rounded-xl bg-amber-50 dark:bg-amber-950 text-amber-600 dark:text-amber-400 flex items-center justify-center text-xl font-bold mb-4">
                        <i class="fa-solid fa-robot"></i>
                    </div>
                    <h3 class="font-bold text-base mb-2">설명 가능한 AI (XAI) 리포트</h3>
                    <p class="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                        왜 이 위치에 부스를 배치했는지, 병목 현상과 대피 시간 단축 근거를 명쾌하게 설명하는 리포트를 제공합니다.
                    </p>
                </div>
                <button onclick="openWorkflowModal()" class="mt-4 text-xs font-bold text-amber-600 dark:text-amber-400 hover:underline flex items-center gap-1">
                    프로세스 확인하기 <i class="fa-solid fa-arrow-right"></i>
                </button>
            </div>
        </div>
    </div>

    <!-- 1. 관제실 워크스페이스 화면 (Workspace Screen) -->
    <div id="screen-workspace" class="screen flex-col flex-1 max-w-7xl mx-auto w-full gap-4">
        <header class="glass-panel rounded-2xl p-4 shadow-sm flex flex-wrap gap-3 items-center justify-between">
            <div class="flex items-center space-x-3">
                <button onclick="goToHome()" class="w-9 h-9 rounded-xl bg-slate-200 dark:bg-slate-800 flex items-center justify-center text-slate-700 dark:text-slate-300 hover:bg-slate-300 transition" title="홈으로 이동">
                    <i class="fa-solid fa-house text-sm"></i>
                </button>
                <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center text-white shadow-lg shadow-indigo-500/30">
                    <i class="fa-solid fa-wand-magic-sparkles text-xl"></i>
                </div>
                <div>
                    <div class="flex items-center gap-2">
                        <h1 class="font-black text-lg tracking-tight text-indigo-600 dark:text-indigo-400">이벤트 온 (Event On)</h1>
                        <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-indigo-100 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300">AI 자동 설계 플랫폼</span>
                    </div>
                    <p class="text-xs text-slate-500 dark:text-slate-400">디지털 트윈 기반 지능형 행사장 자동 배치 및 군중 시뮬레이터</p>
                </div>
            </div>

            <div class="flex flex-wrap gap-2 items-center">
                <button onclick="openConfigModal()" class="px-3.5 py-2 text-xs font-bold rounded-xl bg-gradient-to-r from-indigo-600 to-violet-600 text-white shadow-md shadow-indigo-500/20 hover:opacity-95 transition flex items-center gap-1.5">
                    <i class="fa-solid fa-sliders"></i> AI 행사 설계 설정 & 재생성
                </button>
                <button onclick="openWorkflowModal()" class="px-3.5 py-2 text-xs font-bold rounded-xl bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-300 transition flex items-center gap-1.5">
                    <i class="fa-solid fa-diagram-project"></i> AI 프로세스(Workflow)
                </button>
                <button onclick="openCustomBoothModal()" class="px-3.5 py-2 text-xs font-bold rounded-xl bg-amber-500 text-white shadow hover:opacity-95 transition flex items-center gap-1.5">
                    <i class="fa-solid fa-plus"></i> 맞춤형 부스 추가
                </button>
            </div>
        </header>

        <div class="glass-panel rounded-xl p-3 shadow-sm flex items-center gap-3 flex-wrap text-xs font-bold">
            <span class="flex items-center gap-1.5"><i class="fa-solid fa-clock text-indigo-500"></i> 타임라인 제어</span>
            <button id="bTl" class="px-3 py-1 bg-slate-200 dark:bg-slate-800 rounded-lg hover:bg-slate-300 transition" onclick="togTl()">▶ 재생</button>
            <input type="range" id="tSl" min="10" max="20" step="1" value="14" class="flex-1 min-w-[140px] accent-indigo-600" oninput="setTime(+this.value)">
            <span class="px-3 py-1 bg-indigo-600 text-white rounded-full min-w-[56px] text-center" id="tTxt">14:00</span>
            <span id="tDesc" class="text-slate-500 dark:text-slate-400 font-semibold"></span>
        </div>

        <main class="grid grid-cols-1 lg:grid-cols-3 gap-4 flex-1">
            <div class="lg:col-span-2 flex flex-col gap-4">
                <div class="glass-panel rounded-2xl p-4 shadow-xl flex flex-col">
                    <div class="flex items-center justify-between mb-3">
                        <div>
                            <h2 class="font-bold text-sm flex items-center gap-2">
                                <span>🗺️ 디지털 트윈 행사장 관제</span>
                                <span id="verTxt" class="text-xs text-indigo-600 dark:text-indigo-400 font-normal">· AI 최적 배치 (점수: 92.4점)</span>
                            </h2>
                            <p id="eventMetaDesc" class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">행사명: 2026 미래 기술 페스티벌 | 예상 방문객: 3,500명 | 야외형 숲속 공원</p>
                        </div>
                        <div class="flex gap-2">
                            <span class="px-2.5 py-1 text-[11px] font-bold rounded-lg bg-indigo-50 dark:bg-indigo-950/50 text-indigo-600 dark:text-indigo-300" id="peopleTxt">군중 계산 중…</span>
                            <span class="px-2.5 py-1 text-[11px] font-bold rounded-lg bg-emerald-50 dark:bg-emerald-950/50 text-emerald-600 dark:text-emerald-300" id="status">실시간 동선 추적중</span>
                        </div>
                    </div>
                    
                    <div class="wrap" id="wrap">
                        <canvas id="cv" style="display:none"></canvas>
                        <canvas id="hm" style="display:none;opacity:.75;pointer-events:none"></canvas>
                        <canvas id="pp" style="display:none;pointer-events:none"></canvas>
                        <div class="c3" id="c3"></div>
                        <div class="legend" id="legend"></div>
                        <div class="hint" id="hint">드래그: 3D 회전 · 휠: 확대/축소</div>
                    </div>

                    <div class="flex flex-wrap gap-2 items-center justify-between mt-3 pt-3 border-t border-slate-200 dark:border-slate-800 text-xs font-bold">
                        <div class="flex items-center gap-2">
                            <button id="bMode" class="px-3 py-1.5 rounded-lg bg-indigo-600 text-white shadow transition" onclick="setMode('after')">✦ AI 최적 배치</button>
                            <button id="bModeB" class="px-3 py-1.5 rounded-lg bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 transition" onclick="setMode('before')">설계 전(기존) 비교</button>
                        </div>
                        <div class="flex items-center gap-2">
                            <button id="b3d" class="px-3 py-1.5 rounded-lg bg-indigo-600 text-white transition" onclick="setView(true)">🧊 3D 입체</button>
                            <button id="b2d" class="px-3 py-1.5 rounded-lg bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 transition" onclick="setView(false)">🗺️ 2D 평면</button>
                            <button id="bHeat3" class="px-3 py-1.5 rounded-lg bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 hidden transition" onclick="togHeat3()">🔥 히트맵</button>
                        </div>
                        <div class="flex items-center gap-2">
                            <button id="bPlay" class="px-3 py-1.5 rounded-lg bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 transition" onclick="togSim()">⏸ 정지</button>
                            <button id="bRain" class="px-3 py-1.5 rounded-lg bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300 transition" onclick="togRain()">🌧️ 우천시뮬</button>
                            <button id="bEmg" class="px-3 py-1.5 rounded-lg bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300 transition" onclick="togEmg()">🚨 응급상황</button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="flex flex-col gap-4">
                <div class="glass-panel rounded-2xl p-4 shadow-xl flex flex-col">
                    <div class="flex items-center justify-between mb-3">
                        <h2 class="font-bold text-sm flex items-center gap-2">
                            <i class="fa-solid fa-fire text-orange-500"></i> 실시간 군중 밀집도 & XAI 설명
                        </h2>
                        <span class="px-2.5 py-1 text-[11px] font-bold rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300" id="envTxt">일반 상태</span>
                    </div>
                    <div class="wrap mb-2" id="wrap2" style="aspect-ratio:1.6;">
                        <canvas id="hm2"></canvas>
                    </div>
                    <div class="flex justify-around text-[10px] font-bold text-slate-500 mb-3">
                        <span class="text-emerald-500">🟢 원활</span>
                        <span class="text-yellow-500">🟡 보통</span>
                        <span class="text-orange-500">🟠 혼잡</span>
                        <span class="text-red-500">🔴 위험</span>
                    </div>

                    <div class="grid grid-cols-2 gap-2 mb-3">
                        <div class="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-[11px] font-bold text-slate-500">
                            현재 최대 밀도 <b id="kPeak" class="text-sm block text-slate-800 dark:text-slate-100 mt-0.5">-</b>
                        </div>
                        <div class="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-[11px] font-bold text-slate-500">
                            혼잡 구역 비율 <b id="kBott" class="text-sm block text-slate-800 dark:text-slate-100 mt-0.5">-</b>
                        </div>
                        <div class="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-[11px] font-bold text-slate-500">
                            응급 최대 도달 <b id="kMed" class="text-sm block text-slate-800 dark:text-slate-100 mt-0.5">-</b>
                        </div>
                        <div class="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-[11px] font-bold text-slate-500">
                            위험 구역 <b id="kRisk" class="text-sm block text-slate-800 dark:text-slate-100 mt-0.5">-</b>
                        </div>
                    </div>

                    <div class="p-3 rounded-xl bg-indigo-50 dark:bg-indigo-950/40 border border-indigo-100 dark:border-indigo-900 text-xs mb-3 text-indigo-900 dark:text-indigo-200">
                        <div class="font-bold flex items-center gap-1.5 mb-1"><i class="fa-solid fa-robot"></i> XAI (설명 가능한 AI) 리포트</div>
                        <p id="xaiText" class="text-[11px] leading-relaxed text-slate-600 dark:text-slate-300">공연장과 푸드트럭 존 사이의 이격 거리를 25m 확보하여 병목 현상을 42% 감소시켰으며, 정문 진입로 분산 배치로 대기 시간을 최소화했습니다.</p>
                    </div>

                    <div class="text-xs font-bold mb-2 flex items-center justify-between">
                        <span>📍 배치된 구역 목록 <span id="zCnt" class="text-slate-500 font-normal"></span></span>
                    </div>
                    <div class="zl" id="zlist"></div>
                </div>
            </div>
        </main>
    </div>

    <!-- 1. AI 행사 설계 설정 모달 -->
    <div id="configModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 modal-backdrop hidden">
        <div class="glass-panel rounded-2xl p-6 max-w-lg w-full shadow-2xl relative max-h-[90vh] overflow-y-auto">
            <div class="flex items-center justify-between mb-4">
                <h3 class="font-bold text-base flex items-center gap-2 text-indigo-600 dark:text-indigo-400">
                    <i class="fa-solid fa-wand-magic-sparkles"></i> AI 행사 자동 설계 파라미터 설정
                </h3>
                <button onclick="closeConfigModal()" class="text-slate-400 hover:text-slate-600 transition"><i class="fa-solid fa-xmark text-lg"></i></button>
            </div>
            <form id="configForm" onsubmit="applyAIConfig(event)" class="space-y-4 text-xs font-bold">
                <div>
                    <label class="block mb-1 text-slate-600 dark:text-slate-300">행사명</label>
                    <input type="text" id="cfgName" value="2026 미래 기술 페스티벌" class="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100" required>
                </div>
                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="block mb-1 text-slate-600 dark:text-slate-300">행사 목적</label>
                        <select id="cfgPurpose" class="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100">
                            <option value="tech">기술 전시 및 체험</option>
                            <option value="music">대규모 음악 콘서트</option>
                            <option value="expo">산업 박람회 및 B2B</option>
                            <option value="festival">지역 문화 축제</option>
                        </select>
                    </div>
                    <div>
                        <label class="block mb-1 text-slate-600 dark:text-slate-300">예산 규모</label>
                        <select id="cfgBudget" class="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100">
                            <option value="large">대규모 (5억 이상)</option>
                            <option value="medium" selected>중규모 (1억~5억)</option>
                            <option value="small">소규모 (1억 미만)</option>
                        </select>
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="block mb-1 text-slate-600 dark:text-slate-300">예상 방문객 수 (명)</label>
                        <input type="number" id="cfgVisitors" value="3500" min="500" max="20000" step="100" class="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100" required>
                    </div>
                    <div>
                        <label class="block mb-1 text-slate-600 dark:text-slate-300">행사 장소 타입</label>
                        <select id="cfgVenueType" class="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100">
                            <option value="outdoor">야외 숲속 공원 (그린)</option>
                            <option value="plaza">도심 대형 광장 (아스팔트)</option>
                            <option value="indoor">컨벤션 센터 실내 (홀)</option>
                        </select>
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="block mb-1 text-slate-600 dark:text-slate-300">원하는 분위기</label>
                        <select id="cfgVibe" class="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100">
                            <option value="dynamic">활기차고 역동적인 분위기</option>
                            <option value="relax">친환경적이고 힐링되는 분위기</option>
                            <option value="modern">모던하고 스마트한 하이테크</option>
                        </select>
                    </div>
                    <div>
                        <label class="block mb-1 text-slate-600 dark:text-slate-300">주요 타겟 연령층</label>
                        <select id="cfgAge" class="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100">
                            <option value="all">전 연령 가족 단위</option>
                            <option value="mz">2030 MZ 세대 중심</option>
                            <option value="biz">전문 비즈니스 방문객</option>
                        </select>
                    </div>
                </div>
                <div class="pt-3 flex justify-end gap-2">
                    <button type="button" onclick="closeConfigModal()" class="px-4 py-2 rounded-xl bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 transition">취소</button>
                    <button type="submit" class="px-5 py-2 rounded-xl bg-indigo-600 text-white shadow hover:bg-indigo-700 transition">AI 최적 배치안 생성</button>
                </div>
            </form>
        </div>
    </div>

    <!-- 2. AI 프로세스 (Workflow) 모달 -->
    <div id="workflowModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 modal-backdrop hidden">
        <div class="glass-panel rounded-2xl p-6 max-w-3xl w-full shadow-2xl relative max-h-[90vh] overflow-y-auto">
            <div class="flex items-center justify-between mb-4">
                <h3 class="font-bold text-base flex items-center gap-2 text-indigo-600 dark:text-indigo-400">
                    <i class="fa-solid fa-diagram-project"></i> AI 행사 설계 프로세스 (Workflow)
                </h3>
                <button onclick="closeWorkflowModal()" class="text-slate-400 hover:text-slate-600 transition"><i class="fa-solid fa-xmark text-lg"></i></button>
            </div>
            <p class="text-xs text-slate-500 dark:text-slate-400 mb-6 leading-relaxed">
                행사 기획부터 최종 설계안 산출까지, AI가 디지털 트윈과 다목적 최적화 알고리즘을 통해 수천 가지 경우의 수를 분석하여 가장 안전하고 효율적인 최적의 공간 배치도를 완성합니다.
            </p>
            
            <div class="grid grid-cols-1 md:grid-cols-5 gap-3 text-center text-xs mb-6">
                <div class="p-3 rounded-xl bg-indigo-50 dark:bg-slate-900 border border-indigo-200 dark:border-slate-800 flex flex-col items-center">
                    <div class="w-8 h-8 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold mb-2">1</div>
                    <div class="font-bold mb-1">정보 입력</div>
                    <p class="text-[10px] text-slate-500">예산, 방문객, 목적, 분위기 조건 입력</p>
                </div>
                <div class="p-3 rounded-xl bg-indigo-50 dark:bg-slate-900 border border-indigo-200 dark:border-slate-800 flex flex-col items-center">
                    <div class="w-8 h-8 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold mb-2">2</div>
                    <div class="font-bold mb-1">트윈 생성</div>
                    <p class="text-[10px] text-slate-500">지형 및 장소 기반 3D 디지털 트윈 구축</p>
                </div>
                <div class="p-3 rounded-xl bg-indigo-50 dark:bg-slate-900 border border-indigo-200 dark:border-slate-800 flex flex-col items-center">
                    <div class="w-8 h-8 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold mb-2">3</div>
                    <div class="font-bold mb-1">배치 시뮬레이션</div>
                    <p class="text-[10px] text-slate-500">수천 개 배치안 생성 및 군중 이동 연산</p>
                </div>
                <div class="p-3 rounded-xl bg-indigo-50 dark:bg-slate-900 border border-indigo-200 dark:border-slate-800 flex flex-col items-center">
                    <div class="w-8 h-8 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold mb-2">4</div>
                    <div class="font-bold mb-1">다목적 최적화</div>
                    <p class="text-[10px] text-slate-500">안전성·효율성·만족도 동시 최적화 산출</p>
                </div>
                <div class="p-3 rounded-xl bg-indigo-50 dark:bg-slate-900 border border-indigo-200 dark:border-slate-800 flex flex-col items-center">
                    <div class="w-8 h-8 rounded-full bg-indigo-600 text-white flex items-center justify-center font-bold mb-2">5</div>
                    <div class="font-bold mb-1">XAI 리포트</div>
                    <p class="text-[10px] text-slate-500">설계 이유 설명 및 전후 비교 리포트 제공</p>
                </div>
            </div>

            <div class="flex justify-end">
                <button onclick="closeWorkflowModal()" class="px-4 py-2 rounded-xl bg-indigo-600 text-white text-xs font-bold shadow transition">확인 완료</button>
            </div>
        </div>
    </div>

    <!-- 3. 맞춤형 부스 추가 모달 -->
    <div id="customBoothModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 modal-backdrop hidden">
        <div class="glass-panel rounded-2xl p-6 max-w-md w-full shadow-2xl relative">
            <div class="flex items-center justify-between mb-4">
                <h3 class="font-bold text-base flex items-center gap-2 text-indigo-600 dark:text-indigo-400">
                    <i class="fa-solid fa-plus-circle"></i> 사용자 맞춤형 부스/시설 추가
                </h3>
                <button onclick="closeCustomBoothModal()" class="text-slate-400 hover:text-slate-600 transition"><i class="fa-solid fa-xmark text-lg"></i></button>
            </div>
            <form id="boothForm" onsubmit="addCustomBooth(event)" class="space-y-4 text-xs font-bold">
                <div>
                    <label class="block mb-1 text-slate-600 dark:text-slate-300">부스/시설 명칭</label>
                    <input type="text" id="cbName" placeholder="예: 스폰서 VIP 라운지" class="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100" required>
                </div>
                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <label class="block mb-1 text-slate-600 dark:text-slate-300">시설 유형</label>
                        <select id="cbType" class="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100">
                            <option value="booth">체험/스폰서 부스</option>
                            <option value="food">푸드 및 케이터링</option>
                            <option value="rest">휴게 및 포토존</option>
                            <option value="medical">의료/안전 부스</option>
                        </select>
                    </div>
                    <div>
                        <label class="block mb-1 text-slate-600 dark:text-slate-300">방문객 선호도 (매력도)</label>
                        <input type="number" id="cbAttract" value="75" min="10" max="100" class="w-full p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100" required>
                    </div>
                </div>
                <p class="text-[11px] text-slate-500 font-normal">AI가 최적의 동선과 혼잡도를 계산하여 행사장 빈 공간에 자동으로 최적 위치를 선정합니다.</p>
                <div class="pt-3 flex justify-end gap-2">
                    <button type="button" onclick="closeCustomBoothModal()" class="px-4 py-2 rounded-xl bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 transition">취소</button>
                    <button type="submit" class="px-5 py-2 rounded-xl bg-indigo-600 text-white shadow hover:bg-indigo-700 transition">AI 자동 배치 추가</button>
                </div>
            </form>
        </div>
    </div>

    <script>
        let D = {
            "title": "2026 미래 기술 페스티벌",
            "total": 92.4,
            "before_total": 71.8,
            "mpu": 1.2,
            "params": { "visitors": 3500 },
            "theme": { "kind": "outdoor", "ground": "#166534", "groundRain": "#14532d", "path": "#fde047" },
            "gates": [
                { "name": "정문 (North)", "x": 80, "y": 2 },
                { "name": "후문 (South)", "x": 80, "y": 98 },
                { "name": "서문 (West)", "x": 2, "y": 50 },
                { "name": "동문 (East)", "x": 158, "y": 50 }
            ],
            "zones": [
                { "name": "대공연장", "type": "stage", "x": 60, "y": 10, "w": 40, "h": 22, "ht": 6, "color": "#8b5cf6", "icon": "🎤", "attract": 95 },
                { "name": "메인 체험부스 A", "type": "booth", "x": 15, "y": 38, "w": 25, "h": 18, "ht": 4, "color": "#3b82f6", "icon": "🏷️", "attract": 70 },
                { "name": "메인 체험부스 B", "type": "booth", "x": 120, "y": 38, "w": 25, "h": 18, "ht": 4, "color": "#3b82f6", "icon": "🏷️", "attract": 65 },
                { "name": "푸드트럭 존", "type": "food", "x": 60, "y": 42, "w": 40, "h": 16, "ht": 4, "color": "#f59e0b", "icon": "🍔", "attract": 88 },
                { "name": "중앙 휴게공간", "type": "rest", "x": 65, "y": 68, "w": 30, "h": 18, "ht": 3, "color": "#10b981", "icon": "🌳", "attract": 40 },
                { "name": "응급의료센터", "type": "medical", "x": 15, "y": 72, "w": 18, "h": 14, "ht": 4, "color": "#ef4444", "icon": "🚑", "attract": 10 },
                { "name": "종합 안내센터", "type": "info", "x": 127, "y": 72, "w": 18, "h": 14, "ht": 4, "color": "#0ea5e9", "icon": "ℹ️", "attract": 30 },
                { "name": "화장실 (북측)", "type": "restroom", "x": 15, "y": 15, "w": 14, "h": 10, "ht": 4, "color": "#06b6d4", "icon": "🚻", "attract": 50 },
                { "name": "화장실 (남측)", "type": "restroom", "x": 131, "y": 15, "w": 14, "h": 10, "ht": 4, "color": "#06b6d4", "icon": "🚻", "attract": 50 }
            ],
            "before_zones": [
                { "name": "공연장 (구)", "type": "stage", "x": 10, "y": 10, "w": 35, "h": 20, "ht": 5, "color": "#8b5cf6", "icon": "🎤", "attract": 90 },
                { "name": "푸드존 (구)", "type": "food", "x": 110, "y": 10, "w": 35, "h": 20, "ht": 4, "color": "#f59e0b", "icon": "🍔", "attract": 80 },
                { "name": "부스 A", "type": "booth", "x": 10, "y": 50, "w": 30, "h": 20, "ht": 4, "color": "#3b82f6", "icon": "🏷️", "attract": 60 },
                { "name": "부스 B", "type": "booth", "x": 110, "y": 50, "w": 30, "h": 20, "ht": 4, "color": "#3b82f6", "icon": "🏷️", "attract": 60 },
                { "name": "의료/안내", "type": "medical", "x": 70, "y": 75, "w": 20, "h": 15, "ht": 4, "color": "#ef4444", "icon": "🚑", "attract": 10 }
            ],
            "detail": { "t_max": 185, "risk_zones": 1, "xai": "공연장과 푸드트럭 존 사이의 이격 거리를 25m 확보하여 병목 현상을 42% 감소시켰으며, 정문 진입로 분산 배치로 대기 시간을 최소화했습니다." },
            "before_detail": { "t_max": 340, "risk_zones": 4, "xai": "설계 전 기존 배치는 공연장과 푸드존 인접으로 인한 대규모 병목 현상 및 비상 대피로 확보 실패 위험이 감지되었습니다." }
        };

        const WW = 160, WH = 100, GX = 40, GY = 25;
        let mode = 'after', sim = true, rain = false, emg = null, tHour = 14, tlTimer = null, is3d = true, heat3 = false;
        let workspaceInitialized = false;
        const $ = id => document.getElementById(id);
        const cv = $('cv'), hm = $('hm'), pp = $('pp'), hm2 = $('hm2');
        const cx = cv.getContext('2d'), hx = hm.getContext('2d'), px = pp.getContext('2d'), h2 = hm2.getContext('2d');
        const wrap = $('wrap'), wrap2 = $('wrap2');
        let W = 0, H = 0, S = 1, W2 = 0, H2 = 0;
        const Z = () => mode === 'after' ? D.zones : D.before_zones;
        const mpu = D.mpu, cellArea = (WW / GX) * (WH / GY) * mpu * mpu;
        const NAG = 320; let agents = []; let raindrops = [];
        let heat = new Float32Array(GX * GY);

        $('legend').innerHTML = [
            ['#8b5cf6', '공연장'], ['#3b82f6', '체험부스'], ['#f59e0b', '푸드존'],
            ['#10b981', '휴게공간'], ['#ef4444', '응급의료'], ['#0ea5e9', '안내센터'],
            ['#06b6d4', '화장실'], ['#1e293b', '출입구']
        ].map(a => `<span><i style="background:${a[0]}"></i>${a[1]}</span>`).join('');

        // Navigation Controllers
        function goToWorkspace() {
            $('screen-home').classList.remove('active');
            $('screen-workspace').classList.add('active');
            if (!workspaceInitialized) {
                workspaceInitialized = true;
                resize();
                initR3();
                setView(true);
                requestAnimationFrame(loop);
            } else {
                resize();
                if (R3) size3();
            }
        }

        function goToHome() {
            $('screen-workspace').classList.remove('active');
            $('screen-home').classList.add('active');
        }

        function resize() {
            if (!$('screen-workspace').classList.contains('active')) return;
            W = wrap.clientWidth; H = wrap.clientHeight; S = W / WW;
            [cv, hm, pp].forEach(c => { c.width = W; c.height = H; });
            W2 = wrap2.clientWidth; H2 = wrap2.clientHeight; hm2.width = W2; hm2.height = H2;
            drawBase(); if (R3) { size3(); }
        }

        function factor(h) { if (h < 12) return .55; if (h < 15) return 1.0; if (h < 18) return .8; return .65; }
        function descT(h) { return h < 12 ? '개장 초반 - 순차 입장(여유)' : h < 15 ? '피크 - 푸드·공연 집중(혼잡)' : h < 18 ? '오후 - 체험·휴게 분산' : '폐장 전 - 공연 집중 및 퇴장'; }

        function pickZone() {
            const Zs = Z(); let tot = 0;
            const w = Zs.map(z => {
                const a = (z.type === 'medical') ? 0 : z.attract * (z.type === 'stage' && tHour >= 18 ? 1.5 : 1) * (z.type === 'food' && tHour >= 12 && tHour < 15 ? 1.5 : 1);
                tot += a; return a;
            });
            let r = Math.random() * tot;
            for (let i = 0; i < Zs.length; i++) { r -= w[i]; if (r <= 0) return i; }
            return 0;
        }

        function spawn(a) {
            const g = D.gates[Math.floor(Math.random() * D.gates.length)];
            a.x = g.x + (Math.random() - .5) * 4; a.y = g.y + (Math.random() - .5) * 4;
            a.leaving = false; a.dwell = 0; a.zone = pickZone(); setTarget(a);
        }

        function setTarget(a) {
            const z = Z()[a.zone];
            a.tx = z.x - 1.5 + Math.random() * (z.w + 3);
            a.ty = z.y - 1.5 + Math.random() * (z.h + 3);
            a.sp = .28 + Math.random() * .2;
        }

        function initAgents() {
            agents = [];
            for (let i = 0; i < NAG; i++) {
                const a = {}; spawn(a);
                const t = Math.random();
                a.x = a.x + (a.tx - a.x) * t; a.y = a.y + (a.ty - a.y) * t;
                a.active = i < NAG * factor(tHour);
                agents.push(a);
            }
            raindrops = [];
            for (let i = 0; i < 110; i++) raindrops.push({ x: Math.random() * W, y: Math.random() * H, l: 7 + Math.random() * 10, v: 6 + Math.random() * 6 });
        }

        function step(dt) {
            const f = factor(tHour); const n = Math.floor(NAG * f);
            agents.forEach((a, i) => {
                a.active = i < n; if (!a.active) return;
                if (a.dwell > 0) {
                    a.dwell -= dt; a.x += (Math.random() - .5) * .06; a.y += (Math.random() - .5) * .06;
                    if (a.dwell <= 0) {
                        if (Math.random() < .35) {
                            a.leaving = true;
                            const g = D.gates[Math.floor(Math.random() * D.gates.length)];
                            a.tx = g.x; a.ty = g.y;
                        } else { a.zone = pickZone(); setTarget(a); }
                    }
                    return;
                }
                let dx = a.tx - a.x, dy = a.ty - a.y, d = Math.hypot(dx, dy);
                let sp = a.sp * (rain ? 1.6 : 1);
                if (rain && !a.leaving) {
                    const st = Z().find(z => z.type === 'stage');
                    if (st) { a.tx = st.x + st.w / 2; a.ty = st.y + st.h / 2 + st.h * .7; dx = a.tx - a.x; dy = a.ty - a.y; d = Math.hypot(dx, dy); }
                }
                if (emg) {
                    const ex = a.x - emg.x, ey = a.y - emg.y, ed = Math.hypot(ex, ey);
                    if (ed < 9 && ed > 0) { a.x += ex / ed * .5; a.y += ey / ed * .5; }
                }
                if (d < 1.2) {
                    if (a.leaving) { spawn(a); } else { a.dwell = 3 + Math.random() * 9; }
                } else {
                    a.x += dx / d * sp; a.y += dy / d * sp;
                }
            });

            for (let i = 0; i < agents.length; i += 2) {
                const a = agents[i]; if (!a.active) continue;
                const b = agents[(i * 7 + 3) % agents.length]; if (!b.active) continue;
                const dx = a.x - b.x, dy = a.y - b.y, d = Math.hypot(dx, dy);
                if (d > 0 && d < 1.2) { a.x += dx / d * .1; a.y += dy / d * .1; }
            }

            if (emg) {
                const meds = Z().filter(z => z.type === 'medical');
                let best = null, bd = 1e9;
                meds.forEach(m => {
                    const d = Math.hypot(m.x + m.w / 2 - emg.x, m.y + m.h / 2 - emg.y);
                    if (d < bd) { bd = d; best = m; }
                });
                emg.target = best;
                if (best && bd > 1.5) {
                    emg.x += (best.x + best.w / 2 - emg.x) / bd * .9;
                    emg.y += (best.y + best.h / 2 - emg.y) / bd * .9;
                    $('status').textContent = '🚑 응급 이송 중… 의료센터까지 ' + (bd * mpu).toFixed(0) + 'm';
                } else if (best) {
                    $('status').textContent = '✅ 의료센터 도착 · 이송 완료';
                }
            }
            raindrops.forEach(r => { r.y += r.v; r.x -= 1; if (r.y > H) { r.y = 0; r.x = Math.random() * W; } });
        }

        function updateHeat() {
            const n = Math.floor(NAG * factor(tHour));
            const per = D.params.visitors * .5 / Math.max(1, n) * factor(tHour);
            const g = new Float32Array(GX * GY);
            agents.forEach(a => {
                if (!a.active) return;
                const ix = Math.min(GX - 1, Math.max(0, Math.floor(a.x / (WW / GX))));
                const iy = Math.min(GY - 1, Math.max(0, Math.floor(a.y / (WH / GY))));
                g[iy * GX + ix] += per;
            });
            const o = new Float32Array(GX * GY);
            for (let y = 0; y < GY; y++) for (let x = 0; x < GX; x++) {
                let s = 0, c = 0;
                for (let j = -1; j <= 1; j++) for (let i = -1; i <= 1; i++) {
                    const xx = x + i, yy = y + j;
                    if (xx >= 0 && xx < GX && yy >= 0 && yy < GY) {
                        const w = (i == 0 && j == 0) ? 2 : 1;
                        s += g[yy * GX + xx] * w; c += w;
                    }
                }
                o[y * GX + x] = s / c / cellArea;
            }
            for (let k = 0; k < o.length; k++) heat[k] = heat[k] * .85 + o[k] * .15;
        }

        function heatColor(d) {
            if (d < .12) return null;
            if (d < .25) return 'rgba(16,185,129,.5)';
            if (d < .5) return 'rgba(234,179,8,.65)';
            if (d < .9) return 'rgba(249,115,22,.75)';
            return 'rgba(239,68,68,.88)';
        }

        function drawHeat(ctx, w, h, bg) {
            ctx.clearRect(0, 0, w, h);
            if (bg) { ctx.fillStyle = '#0f172a'; ctx.fillRect(0, 0, w, h); }
            const cw = w / GX, ch = h / GY;
            let peak = 0, hot = 0, act = 0;
            for (let y = 0; y < GY; y++) for (let x = 0; x < GX; x++) {
                const d = heat[y * GX + x];
                peak = Math.max(peak, d);
                if (d >= .12) act++;
                if (d >= .5) hot++;
                const c = heatColor(d);
                if (c) { ctx.fillStyle = c; ctx.fillRect(x * cw, y * ch, cw + .5, ch + .5); }
            }
            if (bg) {
                Z().forEach(z => {
                    ctx.strokeStyle = 'rgba(255,255,255,.45)'; ctx.lineWidth = 1;
                    ctx.strokeRect(z.x * w / WW, z.y * h / WH, z.w * w / WW, z.h * h / WH);
                    ctx.fillStyle = 'rgba(255,255,255,.85)'; ctx.font = 'bold 10px Pretendard';
                    ctx.textAlign = 'center';
                    ctx.fillText(z.name, (z.x + z.w / 2) * w / WW, (z.y + z.h / 2) * h / WH + 3, z.w * w / WW);
                });
            }
            return [peak, hot, act];
        }

        function drawBase() {
            const T = D.theme; cx.clearRect(0, 0, W, H);
            cx.fillStyle = rain ? T.groundRain : T.ground; cx.fillRect(0, 0, W, H);
            cx.strokeStyle = T.path; cx.globalAlpha = .6; cx.lineCap = 'round'; cx.lineWidth = Math.max(4, S * 1.6);
            Z().forEach(z => {
                const g = nearestGate(z);
                cx.beginPath(); cx.moveTo(g.x * S, g.y * S);
                cx.lineTo((z.x + z.w / 2) * S, (z.y + z.h / 2) * S); cx.stroke();
            });
            cx.globalAlpha = 1;
            Z().forEach(z => {
                const x = z.x * S, y = z.y * S, w = z.w * S, h = z.h * S;
                cx.fillStyle = 'rgba(0,0,0,.28)'; cx.fillRect(x + 3, y + 3, w, h);
                cx.fillStyle = z.color; cx.beginPath(); cx.roundRect(x, y, w, h, 7); cx.fill();
                cx.strokeStyle = '#fff'; cx.lineWidth = 2; cx.stroke();
                cx.textAlign = 'center'; cx.fillStyle = '#fff';
                cx.font = Math.max(14, Math.min(26, h * .4)) + 'px sans-serif';
                cx.fillText(z.icon, x + w / 2, y + h / 2 - 2);
                cx.font = 'bold ' + Math.max(11, Math.min(15, w / 6.5)) + 'px Pretendard';
                cx.fillText(z.name, x + w / 2, y + h / 2 + 16, w - 6);
            });
            D.gates.forEach(g => {
                cx.fillStyle = '#1e293b'; cx.beginPath(); cx.arc(g.x * S, g.y * S, 10, 0, 7); cx.fill();
                cx.strokeStyle = '#fff'; cx.lineWidth = 2; cx.stroke();
                cx.fillStyle = '#fff'; cx.font = '12px sans-serif'; cx.textAlign = 'center';
                cx.fillText('🚪', g.x * S, g.y * S + 4);
            });
        }

        function nearestGate(z) {
            let b = D.gates[0], bd = 1e9;
            D.gates.forEach(g => {
                const d = Math.hypot(g.x - (z.x + z.w / 2), g.y - (z.y + z.h / 2));
                if (d < bd) { bd = d; b = g; }
            });
            return b;
        }

        function drawPeople() {
            px.clearRect(0, 0, W, H);
            agents.forEach(a => {
                if (!a.active) return;
                px.fillStyle = rain ? '#93c5fd' : '#fff'; px.strokeStyle = 'rgba(0,0,0,.4)'; px.lineWidth = .8;
                px.beginPath(); px.arc(a.x * S, a.y * S, 3.2, 0, 7); px.fill(); px.stroke();
            });
            if (emg) {
                px.strokeStyle = '#ef4444'; px.lineWidth = 3; px.setLineDash([6, 5]);
                if (emg.target) {
                    px.beginPath(); px.moveTo(emg.x * S, emg.y * S);
                    px.lineTo((emg.target.x + emg.target.w / 2) * S, (emg.target.y + emg.target.h / 2) * S); px.stroke();
                }
                px.setLineDash([]); px.fillStyle = '#ef4444';
                px.beginPath(); px.arc(emg.x * S, emg.y * S, 9, 0, 7); px.fill();
            }
        }

        // Three.js Isometric 3D Engine Setup
        let R3 = null, S3, C3, G3, bodyM, headM, heatPlane, heatTex;
        let yaw = .55, pitch = .72, zoom3 = 1, drag = false, lx = 0, ly = 0;
        const DUM = new THREE.Object3D();

        function M(c, o) { return new THREE.MeshLambertMaterial(Object.assign({ color: new THREE.Color(c) }, o || {})); }
        function bx(p, w, h, d, c, x, y, z, o) { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), M(c, o)); m.position.set(x, y, z); p.add(m); return m; }
        function cyl(p, rt, rb, h, c, x, y, z, seg) { const m = new THREE.Mesh(new THREE.CylinderGeometry(rt, rb, h, seg || 12), M(c)); m.position.set(x, y, z); p.add(m); return m; }
        function cone(p, r, h, c, x, y, z, seg) { const m = new THREE.Mesh(new THREE.ConeGeometry(r, h, seg || 8), M(c)); m.position.set(x, y, z); p.add(m); return m; }
        function tree(p, x, z) { cyl(p, .5, .6, 2.4, '#7c4a21', x, 1.4, z, 8); cone(p, 2.3, 4.6, '#2f855a', x, 4.8, z, 8); }

        function labelSprite(text, color) {
            const c = document.createElement('canvas'); c.width = 640; c.height = 150; const t = c.getContext('2d');
            t.fillStyle = 'rgba(255,255,255,.96)'; t.beginPath(); t.roundRect(4, 4, 632, 142, 28); t.fill();
            t.fillStyle = color; t.beginPath(); t.roundRect(4, 4, 30, 142, 14); t.fill();
            t.fillStyle = '#0f172a'; t.font = 'bold 66px Pretendard,sans-serif'; t.textAlign = 'center'; t.textBaseline = 'middle'; t.fillText(text, 340, 78, 570);
            const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(c), depthTest: false, transparent: true }));
            sp.renderOrder = 10; return sp;
        }

        function buildZone3(z) {
            const g = new THREE.Group(); const cxz = z.x + z.w / 2 - WW / 2, czz = z.y + z.h / 2 - WH / 2;
            g.position.set(cxz, 0, czz); G3.add(g);
            const w = z.w, h = z.h;
            const pale = new THREE.Color(z.color).lerp(new THREE.Color('#ffffff'), .65).getStyle();
            bx(g, w, .5, h, pale, 0, .25, 0);
            let top = 8;
            switch (z.type) {
                case 'stage':
                    bx(g, w * .96, 3, h * .42, '#7c3aed', 0, 2, -h * .28);
                    break;
                case 'food':
                    bx(g, w * .9, 3, 2, '#92400e', 0, 2, -h * .33);
                    break;
                case 'rest':
                    tree(g, -w * .4, -h * .3); tree(g, w * .4, h * .3);
                    break;
                case 'medical':
                    bx(g, w * .8, 5, h * .7, '#ffffff', 0, 3, 0);
                    bx(g, w * .82, 1, h * .72 + .1, '#ef4444', 0, 2.4, 0);
                    break;
                default:
                    const px_ = w * .38, pz = h * .38;
                    [[-1, -1], [1, -1], [-1, 1], [1, 1]].forEach(a => cyl(g, .25, .25, 4.8, '#475569', a[0] * px_, 2.9, a[1] * pz, 8));
                    const roof = new THREE.Mesh(new THREE.ConeGeometry(1, 3.4, 4), M(z.color));
                    roof.rotation.y = Math.PI / 4; roof.scale.set(w * .72, 1, h * .72); roof.position.set(0, 6.7, 0); g.add(roof);
                    top = 9.5;
            }
            const sp = labelSprite(z.icon + ' ' + z.name, z.color);
            sp.scale.set(40, 40 * 150 / 640, 1); sp.position.set(0, top + 4, 0); g.add(sp);
        }

        function buildScene3() {
            if (G3) S3.remove(G3); G3 = new THREE.Group(); S3.add(G3);
            const T = D.theme;
            bx(G3, WW + 8, 4, WH + 8, '#e5e7eb', 0, -2.7, 0);
            bx(G3, WW, .7, WH, rain ? T.groundRain : T.ground, 0, -.35, 0);

            Z().forEach(buildZone3);
            D.gates.forEach(g => {
                const x = g.x - WW / 2, zz = g.y - WH / 2;
                bx(G3, 1.6, 8, 1.6, '#1e293b', x, 4, zz);
            });

            $('zlist').innerHTML = Z().map(z => `<span style="--c:${z.color}">${z.icon} ${z.name}</span>`).join('');
            $('zCnt').textContent = '(' + Z().length + '개)';
        }

        function initR3() {
            const el = $('c3');
            try { R3 = new THREE.WebGLRenderer({ antialias: true }); } catch (e) { R3 = null; is3d = false; return; }
            el.appendChild(R3.domElement);
            S3 = new THREE.Scene();
            S3.add(new THREE.AmbientLight(0xffffff, .85));
            const dl = new THREE.DirectionalLight(0xffffff, .65); dl.position.set(-60, 120, 50); S3.add(dl);
            C3 = new THREE.OrthographicCamera(-1, 1, 1, -1, -800, 1200);

            const N = NAG;
            bodyM = new THREE.InstancedMesh(new THREE.CylinderGeometry(.55, .65, 2.4, 8), M('#f97316'), N);
            headM = new THREE.InstancedMesh(new THREE.SphereGeometry(.7, 10, 8), M('#fde68a'), N);
            bodyM.frustumCulled = false; headM.frustumCulled = false;
            S3.add(bodyM); S3.add(headM);

            heatTex = new THREE.CanvasTexture(hm);
            heatPlane = new THREE.Mesh(new THREE.PlaneGeometry(WW, WH), new THREE.MeshBasicMaterial({ map: heatTex, transparent: true, opacity: .8, depthWrite: false }));
            heatPlane.rotation.x = -Math.PI / 2; heatPlane.position.y = .5; heatPlane.visible = false; S3.add(heatPlane);

            const e = R3.domElement;
            e.onmousedown = ev => { drag = true; lx = ev.clientX; ly = ev.clientY; };
            window.addEventListener('mouseup', () => drag = false);
            e.onmousemove = ev => {
                if (!drag) return;
                yaw -= (ev.clientX - lx) * .008;
                pitch = Math.min(1.35, Math.max(.3, pitch + (ev.clientY - ly) * .006));
                lx = ev.clientX; ly = ev.clientY;
            };
            e.addEventListener('wheel', ev => {
                ev.preventDefault();
                zoom3 = Math.min(3.2, Math.max(.6, zoom3 * (ev.deltaY < 0 ? 1.1 : .9)));
            }, { passive: false });

            size3(); buildScene3();
        }

        function size3() {
            if (!R3) return;
            const el = $('c3'); const w = el.clientWidth, h = el.clientHeight;
            R3.setPixelRatio(Math.min(2, window.devicePixelRatio || 1));
            R3.setSize(w, h);
            const f = 72, asp = w / h;
            C3.left = -f * asp; C3.right = f * asp; C3.top = f; C3.bottom = -f;
            C3.updateProjectionMatrix();
        }

        function render3() {
            if (!R3) return;
            const Rr = 400;
            C3.position.set(Math.sin(yaw) * Math.cos(pitch) * Rr, Math.sin(pitch) * Rr, Math.cos(yaw) * Math.cos(pitch) * Rr);
            C3.lookAt(0, 0, 0); C3.zoom = zoom3; C3.updateProjectionMatrix();

            for (let i = 0; i < agents.length; i++) {
                const a = agents[i]; const s = a.active ? 1 : 0.0001;
                DUM.rotation.set(0, 0, 0); DUM.scale.set(s, s, s);
                DUM.position.set(a.x - WW / 2, 1.7, a.y - WH / 2); DUM.updateMatrix();
                bodyM.setMatrixAt(i, DUM.matrix);
                DUM.position.y = 3.6; DUM.updateMatrix();
                headM.setMatrixAt(i, DUM.matrix);
            }
            bodyM.instanceMatrix.needsUpdate = true; headM.instanceMatrix.needsUpdate = true;

            heatPlane.visible = heat3; if (heat3) heatTex.needsUpdate = true;
            R3.render(S3, C3);
        }

        let last = performance.now(), kt = 0;
        function loop(now) {
            const dt = (now - last) / 1000; last = now;
            if ($('screen-workspace').classList.contains('active')) {
                if (sim) { step(dt); }
                updateHeat();
                const r = drawHeat(hx, W, H, false);
                drawHeat(h2, W2, H2, true);
                if (is3d) render3(); else drawPeople();

                const n = Math.round(D.params.visitors * .5 * factor(tHour));
                $('peopleTxt').textContent = '실시간 유동인구 ≈ ' + n.toLocaleString() + '명';

                kt += dt;
                if (kt > .4) {
                    kt = 0;
                    $('kPeak').textContent = r[0].toFixed(2) + ' 명/㎡';
                    $('kBott').textContent = (r[2] ? Math.round(100 * r[1] / r[2]) : 0) + '%';
                    const de = mode === 'after' ? D.detail : D.before_detail;
                    $('kMed').textContent = Math.round(de.t_max) + '초';
                    $('kRisk').textContent = de.risk_zones + '개소';
                    $('xaiText').textContent = de.xai;
                }
            }
            requestAnimationFrame(loop);
        }

        function setView(v3) {
            if (v3 && !R3) return;
            is3d = v3;
            $('c3').style.display = v3 ? 'block' : 'none';
            [cv, hm, pp].forEach(c => c.style.display = v3 ? 'none' : 'block');
            hm.style.display = v3 ? 'none' : 'block';
            $('b3d').className = v3 ? 'px-3 py-1.5 rounded-lg bg-indigo-600 text-white transition' : 'px-3 py-1.5 rounded-lg bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 transition';
            $('b2d').className = v3 ? 'px-3 py-1.5 rounded-lg bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 transition' : 'px-3 py-1.5 rounded-lg bg-indigo-600 text-white transition';
            $('bHeat3').style.display = v3 ? 'inline-block' : 'none';
            if (v3) size3();
        }

        function togHeat3() { heat3 = !heat3; $('bHeat3').className = heat3 ? 'px-3 py-1.5 rounded-lg bg-indigo-600 text-white transition' : 'px-3 py-1.5 rounded-lg bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 transition'; }

        function setMode(m) {
            mode = m;
            $('bMode').className = m === 'after' ? 'px-3 py-1.5 rounded-lg bg-indigo-600 text-white shadow transition' : 'px-3 py-1.5 rounded-lg bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 transition';
            $('bModeB').className = m === 'before' ? 'px-3 py-1.5 rounded-lg bg-indigo-600 text-white shadow transition' : 'px-3 py-1.5 rounded-lg bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 transition';
            $('verTxt').textContent = m === 'after' ? '· AI 최적 배치 (점수: ' + D.total + '점)' : '· 설계 전 배치 비교 (점수: ' + D.before_total + '점)';
            heat.fill(0); initAgents(); emg = null;
            drawBase(); if (R3) buildScene3();
        }

        function togSim() { sim = !sim; $('bPlay').textContent = sim ? '⏸ 정지' : '▶ 재생'; }
        function togRain() { rain = !rain; $('envTxt').textContent = rain ? '🌧️ 우천 상황' : '일반 상태'; drawBase(); if (R3) buildScene3(); }
        function togEmg() {
            if (emg) { emg = null; $('status').textContent = '실시간 동선 추적중'; return; }
            const Zs = Z().filter(z => z.type !== 'medical');
            const z = Zs[Math.floor(Math.random() * Zs.length)];
            emg = { x: z.x + z.w / 2, y: z.y + z.h + 2, t0: performance.now(), target: null };
            sim = true;
        }
        function setTime(h) { tHour = h; $('tSl').value = h; $('tTxt').textContent = h + ':00'; $('tDesc').textContent = descT(h); }
        function togTl() {
            const b = $('bTl');
            if (tlTimer) { clearInterval(tlTimer); tlTimer = null; b.textContent = '▶ 재생'; }
            else { b.textContent = '⏸ 일시정지'; tlTimer = setInterval(() => { let n = tHour + 1; if (n > 20) n = 10; setTime(n); }, 2500); }
        }

        // Modal Handlers
        function openConfigModal() { $('configModal').classList.remove('hidden'); }
        function closeConfigModal() { $('configModal').classList.add('hidden'); }
        function openWorkflowModal() { $('workflowModal').classList.remove('hidden'); }
        function closeWorkflowModal() { $('workflowModal').classList.add('hidden'); }
        function openCustomBoothModal() { $('customBoothModal').classList.remove('hidden'); }
        function closeCustomBoothModal() { $('customBoothModal').classList.add('hidden'); }

        function applyAIConfig(e) {
            e.preventDefault();
            const name = $('cfgName').value;
            const visitors = parseInt($('cfgVisitors').value);
            const venue = $('cfgVenueType').value;
            D.title = name;
            D.params.visitors = visitors;
            if (venue === 'outdoor') {
                D.theme = { "kind": "outdoor", "ground": "#166534", "groundRain": "#14532d", "path": "#fde047" };
            } else if (venue === 'plaza') {
                D.theme = { "kind": "plaza", "ground": "#334155", "groundRain": "#1e293b", "path": "#38bdf8" };
            } else {
                D.theme = { "kind": "indoor", "ground": "#475569", "groundRain": "#334155", "path": "#f43f5e" };
            }
            $('eventMetaDesc').textContent = '행사명: ' + name + ' | 예상 방문객: ' + visitors.toLocaleString() + '명 | AI 자동 최적 설계 적용 완료';
            closeConfigModal();
            heat.fill(0); initAgents(); drawBase(); if (R3) buildScene3();
        }

        function addCustomBooth(e) {
            e.preventDefault();
            const name = $('cbName').value;
            const type = $('cbType').value;
            const attract = parseInt($('cbAttract').value);
            const colors = { booth: '#3b82f6', food: '#f59e0b', rest: '#10b981', medical: '#ef4444' };
            const icons = { booth: '🏷️', food: '🍔', rest: '🌳', medical: '🚑' };
            
            const newZone = {
                "name": name,
                "type": type,
                "x": 45 + Math.random() * 60,
                "y": 55 + Math.random() * 20,
                "w": 20,
                "h": 14,
                "ht": 4,
                "color": colors[type] || '#6366f1',
                "icon": icons[type] || '⭐',
                "attract": attract
            };
            D.zones.push(newZone);
            closeCustomBoothModal();
            $('boothForm').reset();
            drawBase(); if (R3) buildScene3();
        }

        window.addEventListener('resize', resize);
        setTime(14);
    </script>
</body>
</html>
