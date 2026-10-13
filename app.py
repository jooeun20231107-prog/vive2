<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>이벤트 아키텍트 AI - 아키스케치 연동 3D/2D 행사 공간 설계 플랫폼</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Alpine.js CDN -->
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <!-- Plotly CDN for charts -->
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <!-- Pretendard Font -->
    <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />
    <style>
        body { font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif; background-color: #F8FAFC; }
        [x-cloak] { display: none !important; }
    </style>
</head>
<body class="min-h-screen text-slate-800 flex flex-col" x-data="appData()" x-init="initApp()">

    <header class="bg-white border-b border-slate-200 sticky top-0 z-50 px-6 py-3.5 flex items-center justify-between shadow-sm">
        <div class="flex items-center space-x-3 cursor-pointer" @click="page = 'home'">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-blue-500 flex items-center justify-center text-white text-xl shadow-md">
                📐
            </div>
            <div>
                <h1 class="font-bold text-lg text-slate-900 leading-tight">이벤트 아키텍트 AI</h1>
                <p class="text-xs text-slate-500 font-medium">아키스케치(ArchiSketch) 연동 3D/2D 스마트 공간 설계</p>
            </div>
        </div>

        <div class="flex items-center space-x-4">
            <!-- Navigation buttons -->
            <nav class="hidden md:flex space-x-1 bg-slate-100 p-1 rounded-xl">
                <button @click="page = 'home'" :class="page === 'home' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'" class="px-4 py-1.5 rounded-lg text-sm font-semibold transition-all">🏠 홈</button>
                <button @click="page = 'dashboard'" :class="page === 'dashboard' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'" class="px-4 py-1.5 rounded-lg text-sm font-semibold transition-all">📊 대시보드</button>
                <button @click="page = 'report'" :class="page === 'report' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'" class="px-4 py-1.5 rounded-lg text-sm font-semibold transition-all">📄 결재 보고서</button>
                <button @click="page = 'settings'" :class="page === 'settings' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-600 hover:text-slate-900'" class="px-4 py-1.5 rounded-lg text-sm font-semibold transition-all">⚙️ 설정</button>
            </nav>

            <!-- User Popover / Profile -->
            <div class="relative" x-data="{ open: false }">
                <button @click="open = !open" class="flex items-center space-x-2 bg-slate-50 hover:bg-slate-100 border border-slate-200 px-3 py-1.5 rounded-xl transition-all">
                    <span class="text-base">👤</span>
                    <span class="text-sm font-semibold text-slate-700" x-text="username + ' 님'"></span>
                </button>
                <div x-show="open" @click.away="open = false" x-cloak class="absolute right-0 mt-2 w-56 bg-white border border-slate-200 rounded-2xl shadow-xl p-3 z-50">
                    <p class="font-bold text-sm text-slate-800 px-2 py-1" x-text="username"></p>
                    <p class="text-xs text-slate-500 px-2 pb-2 border-b border-slate-100">직책: 총괄 기획자</p>
                    <button @click="page = 'settings'; open = false" class="w-full text-left px-2 py-2 text-sm text-slate-600 hover:bg-slate-50 rounded-lg mt-1 font-medium">설정 관리</button>
                    <button @click="loggedIn = false; open = false" class="w-full text-left px-2 py-2 text-sm text-rose-600 hover:bg-rose-50 rounded-lg font-medium">로그아웃</button>
                </div>
            </div>
        </div>
    </header>

    <main class="flex-1 max-w-7xl w-full mx-auto p-6">

        <!-- HOME PAGE -->
        <template x-if="page === 'home'">
            <div class="space-y-8 py-4">
                <div class="text-center max-w-3xl mx-auto space-y-3">
                    <span class="bg-indigo-50 text-indigo-600 font-bold px-4 py-1.5 rounded-full text-xs uppercase tracking-wider border border-indigo-100">ArchiSketch Maps & AI 3D/2D Integration</span>
                    <h2 class="text-3xl md:text-4xl font-extrabold text-slate-900 tracking-tight">공간 맞춤형 행사 조건 설정과<br>실시간 3D/2D 디지털 트윈 스튜디오</h2>
                    <p class="text-slate-500 text-base">올림픽공원 잔디마당, 코엑스 컨벤션, 한강 공원 등 장소별 특성에 최적화된 공간 자동 설계와 아키스케치 기반 뷰어를 경험하세요.</p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4">
                    <!-- Dashboard Card -->
                    <div @click="page = 'dashboard'" class="group bg-gradient-to-br from-white to-blue-50/60 border-2 border-blue-200 hover:border-blue-400 rounded-3xl p-8 shadow-sm hover:shadow-xl transition-all cursor-pointer flex flex-col justify-between">
                        <div>
                            <div class="text-4xl mb-4">📐</div>
                            <h3 class="text-xl font-bold text-blue-900 mb-3 group-hover:text-blue-600 transition-colors">아키스케치 공간 설계 대시보드</h3>
                            <p class="text-slate-600 text-sm leading-relaxed mb-6">
                                행사 장소와 목적을 선택하면 해당 장소 면적과 지형에 맞게 무대, 부스, 푸드존이 자동 재배치됩니다. 2D/3D 뷰 전환과 AI 챗봇 편집을 지원합니다.
                            </p>
                        </div>
                        <button class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-xl transition-colors shadow-md w-full text-center">
                            대시보드 시작하기 →
                        </button>
                    </div>

                    <!-- Report Card -->
                    <div @click="page = 'report'" class="group bg-gradient-to-br from-white to-emerald-50/60 border-2 border-emerald-200 hover:border-emerald-400 rounded-3xl p-8 shadow-sm hover:shadow-xl transition-all cursor-pointer flex flex-col justify-between">
                        <div>
                            <div class="text-4xl mb-4">📄</div>
                            <h3 class="text-xl font-bold text-emerald-900 mb-3 group-hover:text-emerald-600 transition-colors">AI 결재용 기안 보고서 생성기</h3>
                            <p class="text-slate-600 text-sm leading-relaxed mb-6">
                                선택된 장소와 공간 배치 수치, 안전성 평가 결과를 결재 문서 양식으로 즉시 출력하고 텍스트 파일로 다운로드할 수 있습니다.
                            </p>
                        </div>
                        <button class="bg-emerald-600 hover:bg-emerald-700 text-white font-semibold py-3 px-6 rounded-xl transition-colors shadow-md w-full text-center">
                            결재 보고서 확인하기 →
                        </button>
                    </div>
                </div>
            </div>
        </template>

        <!-- DASHBOARD PAGE -->
        <template x-if="page === 'dashboard'">
            <div class="space-y-6">
                <!-- Header Title & Setup Button -->
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div>
                        <h2 class="text-2xl font-extrabold text-slate-900">📐 아키스케치 연동 3D/2D 공간 설계 대시보드</h2>
                        <p class="text-sm text-slate-500">선택한 장소와 조건에 맞춘 맞춤형 공간 배치 및 실시간 디지털 트윈 제어</p>
                    </div>
                    <div class="flex items-center space-x-2">
                        <button @click="showSetupModal = true" class="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-4 py-2.5 rounded-xl text-sm shadow-md transition-all flex items-center space-x-2">
                            <span>✨ 행사 장소 및 조건 변경</span>
                        </button>
                        <a href="https://maps.archisketch.com/" target="_blank" class="bg-white hover:bg-slate-50 border border-slate-200 text-slate-700 font-semibold px-4 py-2.5 rounded-xl text-sm shadow-sm transition-all flex items-center space-x-1.5">
                            <span>🔗 아키스케치 공식맵 열기</span>
                        </a>
                    </div>
                </div>

                <!-- Event Info Banner -->
                <div class="bg-gradient-to-r from-indigo-900 to-slate-900 text-white p-5 rounded-2xl shadow-md flex flex-wrap items-center justify-between gap-4 text-sm font-medium">
                    <div class="flex items-center space-x-2"><span>🎪</span><span><b>행사명:</b> <span x-text="eventName"></span></span></div>
                    <div class="flex items-center space-x-2"><span>🏷️</span><span><b>유형:</b> <span x-text="eventType"></span></span></div>
                    <div class="flex items-center space-x-2"><span>📍</span><span><b>장소:</b> <span x-text="locationName"></span></span></div>
                    <div class="flex items-center space-x-2"><span>👥</span><span><b>예상인원:</b> <span x-text="expectedVisitors.toLocaleString() + '명'"></span></span></div>
                    <div class="flex items-center space-x-2"><span>💰</span><span><b>예산:</b> <span x-text="budget"></span></span></div>
                </div>

                <!-- Main Layout Grid -->
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <!-- Left / Map Area (2 cols) -->
                    <div class="lg:col-span-2 space-y-4">
                        <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm">
                            <div class="flex items-center justify-between mb-3">
                                <div class="flex items-center space-x-2">
                                    <h3 class="font-bold text-slate-800 text-base">🗺️ 아키스케치 기반 공간 조감도</h3>
                                    <span class="text-xs bg-indigo-50 text-indigo-600 font-semibold px-2.5 py-1 rounded-lg border border-indigo-100" x-text="viewMode === '2d' ? '2D 평면 뷰' : '3D 입체 뷰'"></span>
                                </div>
                                <div class="flex space-x-1 bg-slate-100 p-1 rounded-xl text-xs font-semibold">
                                    <button @click="viewMode = '2d'; updateMap()" :class="viewMode === '2d' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-600'" class="px-3 py-1 rounded-lg transition-all">2D 평면도</button>
                                    <button @click="viewMode = '3d'; updateMap()" :class="viewMode === '3d' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-600'" class="px-3 py-1 rounded-lg transition-all">3D 입체 뷰</button>
                                </div>
                            </div>
                            <!-- Plotly Map Container -->
                            <div id="spatialMap" class="w-full h-[460px] rounded-xl overflow-hidden bg-slate-50"></div>
                        </div>

                        <!-- Facility Selection Buttons -->
                        <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm">
                            <p class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">🛠️ 전체 시설 빠른 선택 및 제어</p>
                            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                                <template x-for="(fac, key) in facilities" :key="key">
                                    <button @click="selectedFacility = key" 
                                        :class="selectedFacility === key ? 'bg-indigo-600 text-white shadow-md border-indigo-600' : 'bg-slate-50 hover:bg-slate-100 text-slate-700 border-slate-200'"
                                        class="border font-semibold py-2.5 px-3 rounded-xl text-xs sm:text-sm transition-all flex items-center justify-center space-x-1.5 truncate">
                                        <span x-text="fac.icon"></span>
                                        <span x-text="fac.name" class="truncate"></span>
                                    </button>
                                </template>
                            </div>
                        </div>
                    </div>

                    <!-- Right / Inspector & AI Assistant (1 col) -->
                    <div class="space-y-6">
                        <!-- Selected Facility Card -->
                        <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm" :style="'border-left: 6px solid ' + currentFacility.hex">
                            <div class="flex items-center justify-between mb-2">
                                <h3 class="font-bold text-lg text-slate-900 flex items-center space-x-2">
                                    <span x-text="currentFacility.icon"></span>
                                    <span x-text="currentFacility.name"></span>
                                </h3>
                                <span class="text-xs bg-slate-100 text-slate-600 px-2.5 py-1 rounded-lg font-medium" x-text="selectedFacility"></span>
                            </div>
                            <p class="text-xs text-slate-500 mb-1"><b>중심 좌표:</b> (X: <span x-text="currentFacility.x"></span>, Y: <span x-text="currentFacility.y"></span>)</p>
                            <p class="text-xs text-slate-500 mb-3"><b>규격 크기:</b> <span x-text="currentFacility.w + 'm x ' + currentFacility.h + 'm'"></span></p>
                            <div class="bg-sky-50 border-l-4 border-sky-500 p-3.5 rounded-xl text-xs text-slate-800 leading-relaxed">
                                💡 <b>아키스케치 공간 분석 근거:</b><br>
                                <span x-text="currentFacility.reason"></span>
                            </div>
                        </div>

                        <!-- Simulation Card -->
                        <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
                            <div class="flex items-center justify-between mb-3">
                                <h3 class="font-bold text-slate-900 text-sm">🔥 군중 밀집도 시뮬레이션</h3>
                                <button @click="runSimulation()" class="bg-rose-500 hover:bg-rose-600 text-white text-xs font-semibold px-3 py-1.5 rounded-lg shadow-sm transition-colors">
                                    시뮬레이션 실행
                                </button>
                            </div>
                            <div x-show="simulated" class="space-y-2">
                                <p class="text-xs text-slate-500">구역별 인파 밀집도 예측 (붉은색: 정체 위험 구역)</p>
                                <div id="simHeatmap" class="w-full h-36 rounded-lg overflow-hidden bg-slate-50"></div>
                            </div>
                            <div x-show="!simulated" class="text-center py-6 text-slate-400 text-xs">
                                '시뮬레이션 실행' 버튼을 눌러 인파 밀집도를 확인하세요.
                            </div>
                        </div>

                        <!-- AI Chatbot Assistant -->
                        <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm flex flex-col h-80">
                            <h3 class="font-bold text-slate-900 text-sm mb-3">💬 AI 설계 어시스턴트</h3>
                            <div id="chatContainer" class="flex-1 overflow-y-auto space-y-3 pr-1 text-xs mb-3">
                                <template x-for="msg in chatMessages">
                                    <div :class="msg.role === 'user' ? 'text-right' : 'text-left'">
                                        <div :class="msg.role === 'user' ? 'bg-indigo-600 text-white ml-auto rounded-l-xl rounded-tr-xl' : 'bg-slate-100 text-slate-800 mr-auto rounded-r-xl rounded-tl-xl'" 
                                             class="inline-block p-3 max-w-[85%] text-left leading-relaxed shadow-sm" x-text="msg.content"></div>
                                    </div>
                                </template>
                            </div>
                            <div class="flex items-center space-x-2">
                                <input type="text" x-model="userInput" @keydown.enter="sendChat()" placeholder="예: '푸드존을 외곽으로 이동해줘'" 
                                       class="flex-1 border border-slate-200 rounded-xl px-3 py-2 text-xs focus:outline-none focus:border-indigo-500">
                                <button @click="sendChat()" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-xl text-xs font-semibold shadow-sm transition-colors">
                                    전송
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </template>

        <!-- REPORT PAGE -->
        <template x-if="page === 'report'">
            <div class="space-y-6 max-w-4xl mx-auto py-2">
                <div class="flex items-center justify-between">
                    <div>
                        <h2 class="text-2xl font-extrabold text-slate-900">📄 AI 결재용 보고서 생성기</h2>
                        <p class="text-sm text-slate-500">선택된 장소와 공간 배치 수치, 안전성 평가 결과가 공식 기안서 문서 양식으로 표시됩니다.</p>
                    </div>
                    <div class="flex items-center space-x-2">
                        <button @click="downloadReport()" class="bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold px-4 py-2.5 rounded-xl text-sm transition-all">
                            📥 텍스트 다운로드
                        </button>
                        <button @click="window.print()" class="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-4 py-2.5 rounded-xl text-sm shadow-md transition-all">
                            🖨️ 보고서 인쇄
                        </button>
                    </div>
                </div>

                <!-- Official Document Box -->
                <div class="bg-white border border-slate-200 rounded-3xl p-8 md:p-12 shadow-md space-y-8 text-slate-900">
                    <div class="flex flex-col sm:flex-row justify-between border-b-2 border-slate-900 pb-6 gap-4">
                        <div>
                            <h3 class="text-2xl font-extrabold tracking-tight">[결재 기안서] 행사 공간 배치 타당성 검토서</h3>
                            <p class="text-xs text-slate-500 mt-1">시스템: ArchiSketch & Event Architect AI v4.2</p>
                        </div>
                        <div class="text-xs text-slate-600 space-y-1 sm:text-right">
                            <p><b>문서번호:</b> EA-2026-ARCHI-0913</p>
                            <p><b>기안일자:</b> 2026. 10. 13</p>
                            <p><b>기안자:</b> <span x-text="username"></span> (총괄)</p>
                        </div>
                    </div>

                    <div class="space-y-3">
                        <h4 class="font-bold text-base text-slate-900 border-l-4 border-indigo-600 pl-3">1. 행사 기본 개요 및 장소 분석</h4>
                        <table class="w-full border-collapse text-xs">
                            <tr>
                                <td class="bg-slate-50 border border-slate-200 p-3 font-bold w-1/5">행사명</td>
                                <td class="border border-slate-200 p-3 w-3/10" x-text="eventName"></td>
                                <td class="bg-slate-50 border border-slate-200 p-3 font-bold w-1/5">행사 장소</td>
                                <td class="border border-slate-200 p-3 w-3/10" x-text="locationName"></td>
                            </tr>
                            <tr>
                                <td class="bg-slate-50 border border-slate-200 p-3 font-bold">예상 관람객</td>
                                <td class="border border-slate-200 p-3" x-text="expectedVisitors.toLocaleString() + ' 명'"></td>
                                <td class="bg-slate-50 border border-slate-200 p-3 font-bold">소요 예산</td>
                                <td class="border border-slate-200 p-3" x-text="budget"></td>
                            </tr>
                        </table>
                    </div>

                    <div class="space-y-3">
                        <h4 class="font-bold text-base text-slate-900 border-l-4 border-indigo-600 pl-3">2. 아키스케치 공간 동선 안전성 평가</h4>
                        <table class="w-full border-collapse text-xs">
                            <thead>
                                <tr class="bg-slate-100 text-left">
                                    <th class="p-3 border border-slate-200">평가 항목</th>
                                    <th class="p-3 border border-slate-200">점수</th>
                                    <th class="p-3 border border-slate-200">등급</th>
                                    <th class="p-3 border border-slate-200">상세 검토 및 종합 평가</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td class="p-3 border border-slate-200">비상 피난 및 의료 안전성</td>
                                    <td class="p-3 border border-slate-200"><b>96점</b></td>
                                    <td class="p-3 border border-slate-200"><span class="bg-emerald-100 text-emerald-800 px-2.5 py-1 rounded-full font-bold">매우 우수</span></td>
                                    <td class="p-3 border border-slate-200">선택된 장소 외곽 비상 도로망과 연계되어 응급 차량 진출입 최단 코스 확보 완료.</td>
                                </tr>
                                <tr>
                                    <td class="p-3 border border-slate-200">소음 및 연기 동선 분리성</td>
                                    <td class="p-3 border border-slate-200"><b>93점</b></td>
                                    <td class="p-3 border border-slate-200"><span class="bg-emerald-100 text-emerald-800 px-2.5 py-1 rounded-full font-bold">매우 우수</span></td>
                                    <td class="p-3 border border-slate-200">푸드존 독립 구역 배치로 무대 관람 구역으로의 조리 연기 및 소음 확산 차단.</td>
                                </tr>
                                <tr>
                                    <td class="p-3 border border-slate-200">관람객 편의 및 서비스 접근성</td>
                                    <td class="p-3 border border-slate-200"><b>90점</b></td>
                                    <td class="p-3 border border-slate-200"><span class="bg-blue-100 text-blue-800 px-2.5 py-1 rounded-full font-bold">우수</span></td>
                                    <td class="p-3 border border-slate-200">화장실 및 안내센터가 아키스케치 기반 동선 분석에 따라 균형 배치됨.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="space-y-3">
                        <h4 class="font-bold text-base text-slate-900 border-l-4 border-indigo-600 pl-3">3. 시설물 배치 근거 요약</h4>
                        <ul class="list-disc pl-5 text-xs space-y-2 text-slate-700">
                            <li><b x-text="facilities.stage.name"></b>: <span x-text="facilities.stage.reason"></span></li>
                            <li><b x-text="facilities.food.name"></b>: <span x-text="facilities.food.reason"></span></li>
                            <li><b x-text="facilities.medical.name"></b>: <span x-text="facilities.medical.reason"></span></li>
                            <li><b x-text="facilities.toilet.name"></b>: <span x-text="facilities.toilet.reason"></span></li>
                        </ul>
                    </div>

                    <div class="bg-sky-50 p-4 rounded-xl border border-sky-200 text-xs text-sky-900 leading-relaxed">
                        💡 <b>기안 의견:</b> 본 공간 설계안은 아키스케치 3D/2D 디지털 트윈 시뮬레이션을 통과하였으며, 안전사고 예방과 관람객 편의를 모두 충족하므로 원안대로 상신합니다.
                    </div>
                </div>
            </div>
        </template>

        <!-- SETTINGS PAGE -->
        <template x-if="page === 'settings'">
            <div class="space-y-6 max-w-2xl mx-auto py-4">
                <div class="bg-white border border-slate-200 rounded-3xl p-6 shadow-sm space-y-4">
                    <h3 class="font-bold text-lg text-slate-900">👤 계정 및 사용자 프로필</h3>
                    <div>
                        <label class="block text-xs font-semibold text-slate-600 mb-1">사용자 이름</label>
                        <input type="text" x-model="username" class="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-indigo-500">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-600 mb-1">소속 부서 / 조직</label>
                        <input type="text" value="이벤트 기획 총괄팀" class="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-indigo-500">
                    </div>
                </div>

                <div class="bg-white border border-slate-200 rounded-3xl p-6 shadow-sm space-y-4">
                    <h3 class="font-bold text-lg text-slate-900">🖥️ 아키스케치 3D/2D 엔진 옵션</h3>
                    <div class="flex items-center justify-between">
                        <span class="text-sm font-medium text-slate-700">도면 내 레이블 및 좌표 가이드 표시</span>
                        <input type="checkbox" checked class="w-5 h-5 text-indigo-600 rounded">
                    </div>
                    <div class="flex items-center justify-between">
                        <span class="text-sm font-medium text-slate-700">AI 챗봇 명령 후 실시간 도면 자동 갱신</span>
                        <input type="checkbox" checked class="w-5 h-5 text-indigo-600 rounded">
                    </div>
                </div>
            </div>
        </template>

    </main>

    <div x-show="showSetupModal" x-cloak class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-sm p-4">
        <div @click.away="showSetupModal = false" class="bg-white border border-slate-200 rounded-3xl max-w-xl w-full p-8 shadow-2xl space-y-6">
            <div class="flex items-center justify-between border-b border-slate-100 pb-4">
                <div class="flex items-center space-x-2">
                    <span class="text-2xl">🎪</span>
                    <h3 class="font-bold text-xl text-slate-900">행사 장소 및 조건 설정</h3>
                </div>
                <button @click="showSetupModal = false" class="text-slate-400 hover:text-slate-600 font-bold text-lg">✕</button>
            </div>

            <div class="space-y-4 text-xs font-medium text-slate-700">
                <div>
                    <label class="block mb-1 font-semibold text-slate-600">행사명</label>
                    <input type="text" x-model="tempEventName" class="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-indigo-500">
                </div>

                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block mb-1 font-semibold text-slate-600">이벤트 유형 선택</label>
                        <select x-model="tempEventType" class="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-indigo-500 bg-white">
                            <option value="뮤직 페스티벌 & 공연">뮤직 페스티벌 & 공연</option>
                            <option value="컨벤션 & 박람회">컨벤션 & 박람회</option>
                            <option value="야외 지역 문화 축제">야외 지역 문화 축제</option>
                            <option value="기업 브랜드 팝업 이벤트">기업 브랜드 팝업 이벤트</option>
                        </select>
                    </div>
                    <div>
                        <label class="block mb-1 font-semibold text-slate-600">행사 장소 선택 (아키스케치 템플릿 연동)</label>
                        <select x-model="tempLocationKey" @change="onLocationChange()" class="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-indigo-500 bg-white">
                            <template x-for="(loc, lKey) in locationPresets" :key="lKey">
                                <option :value="lKey" x-text="loc.name"></option>
                            </template>
                        </select>
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block mb-1 font-semibold text-slate-600">예상 관람객 (명)</label>
                        <input type="number" x-model.number="tempExpectedVisitors" step="500" class="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-indigo-500">
                    </div>
                    <div>
                        <label class="block mb-1 font-semibold text-slate-600">소요 예산</label>
                        <input type="text" x-model="tempBudget" class="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-indigo-500">
                    </div>
                </div>

                <div class="bg-indigo-50 border border-indigo-100 p-4 rounded-xl text-indigo-900 leading-relaxed">
                    📍 <b>선택된 장소 공간 특성:</b> <span x-text="locationPresets[tempLocationKey].desc"></span>
                </div>
            </div>

            <div class="flex space-x-3 pt-2">
                <button @click="showSetupModal = false" class="flex-1 bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold py-3 rounded-xl text-sm transition-all">취소</button>
                <button @click="applyEventSettings()" class="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 rounded-xl text-sm transition-all shadow-md">✨ 장소 맞춤 공간 배치 재계산</button>
            </div>
        </div>
    </div>

    <script>
        const LOCATION_PRESETS = {
            "olympic": {
                name: "서울 올림픽공원 잔디마당 (대규모 야외)",
                desc: "탁 트인 잔디 광장으로 대규모 관람객(5,000명 이상) 수용에 최적화되어 있으며, 외곽 도로망이 발달해 응급 및 물류 이동이 유리합니다.",
                facilities: {
                    "stage": { name: "공연장 (메인무대)", icon: "🎪", hex: "#8B5CF6", x: 500, y: 100, w: 240, h: 110, reason: "북쪽 중앙에 위치시켜 관람객 시야각과 음향 전달 극대화" },
                    "booth": { name: "체험부스", icon: "🛍️", hex: "#3B82F6", x: 190, y: 130, w: 180, h: 150, reason: "북서쪽 진입 구역에 배치하여 초기 관람객 유입 증대" },
                    "food": { name: "푸드존", icon: "🍔", hex: "#F97316", x: 190, y: 380, w: 180, h: 150, reason: "서쪽 외곽에 독립 배치하여 조리 연기 및 혼잡도 분산" },
                    "rest": { name: "휴게공간", icon: "🏕️", hex: "#10B981", x: 500, y: 360, w: 280, h: 180, reason: "중앙 잔디 광장에 위치하여 무대 관람 및 휴식 동선 동시 확보" },
                    "medical": { name: "응급의료센터", icon: "🚑", hex: "#EF4444", x: 820, y: 120, w: 160, h: 100, reason: "동쪽 외곽 비상 도로 인접 배치로 구급차 최단 경로 보장" },
                    "toilet": { name: "화장실", icon: "🚻", hex: "#2563EB", x: 820, y: 280, w: 160, h: 100, reason: "동쪽 측면 상하수 인프라 접근성 고려 배치" },
                    "info": { name: "안내센터", icon: "ℹ️", hex: "#EC4899", x: 500, y: 570, x: 500, y: 570, w: 160, h: 70, reason: "주 출입구 정면에 위치하여 길 안내 신속 처리" },
                    "exit": { name: "출입구", icon: "🚪", hex: "#64748B", x: 500, y: 660, w: 220, h: 60, reason: "남쪽 정문 대규모 인파 진출입 및 비상 대피 유도" }
                }
            },
            "coex": {
                name: "코엑스 컨벤션 센터 (실내 전시장)",
                desc: "공조 시설과 완벽한 냉난방이 갖춰진 실내 전시 홀로 박람회 및 기업 팝업 행사에 최적화된 격자형 공간입니다.",
                facilities: {
                    "stage": { name: "메인 프레젠테이션 무대", icon: "🎪", hex: "#8B5CF6", x: 500, y: 90, w: 220, h: 100, reason: "홀 안쪽 중앙에 배치하여 강연 집중도 향상" },
                    "booth": { name: "기업 전시 부스", icon: "🛍️", hex: "#3B82F6", x: 300, y: 260, w: 220, h: 160, reason: "메인 통로 양옆에 격자형으로 배치하여 관람 동선 최적화" },
                    "food": { name: "카페테리아 / 케이터링", icon: "🍔", hex: "#F97316", x: 750, y: 260, w: 160, h: 160, reason: "전시장 우측 독립 공간에 배치하여 식음료 냄새 차단" },
                    "rest": { name: "비즈니스 미팅 라운지", icon: "🏕️", hex: "#10B981", x: 500, y: 450, w: 260, h: 140, reason: "참가자 휴식 및 상담을 위한 중앙 쉼터" },
                    "medical": { name: "응급상황실", icon: "🚑", hex: "#EF4444", x: 150, y: 90, w: 140, h: 90, reason: "로비 출입구 직 인근에 배치" },
                    "toilet": { name: "내부 화장실", icon: "🚻", hex: "#2563EB", x: 850, y: 500, w: 120, h: 100, reason: "건물 고정 상하수도 설비 위치에 밀착 배치" },
                    "info": { name: "인포데스크", icon: "ℹ️", hex: "#EC4899", x: 500, y: 620, w: 180, h: 70, reason: "메인 로비 입구 방문객 등록 및 안내" },
                    "exit": { name: "메인 출입구", icon: "🚪", hex: "#64748B", x: 500, y: 690, w: 240, h: 50, reason: "로비 전면 대형 비상구 및 주 출입구" }
                }
            },
            "han강": {
                name: "여의도 한강공원 이벤트 광장 (수변 야외)",
                desc: "한강변 수변 공간과 자전거 도로가 인접한 야외 특설 행사장으로 푸드트럭과 야간 축제에 적합합니다.",
                facilities: {
                    "stage": { name: "수변 야외 무대", icon: "🎪", hex: "#8B5CF6", x: 500, y: 110, w: 240, h: 100, reason: "한강 조망을 배경으로 한 공연 시야 확보" },
                    "booth": { name: "플리마켓 부스", icon: "🛍️", hex: "#3B82F6", x: 200, y: 280, w: 170, h: 160, reason: "산책로와 연계된 보행자 동선 측면 배치" },
                    "food": { name: "푸드트럭 존", icon: "🍔", hex: "#F97316", x: 800, y: 280, w: 170, h: 160, reason: "취식 공간과 쓰레기 수거 구역 인근 연계 배치" },
                    "rest": { name: "텐트 및 파라솔 쉼터", icon: "🏕️", hex: "#10B981", x: 500, y: 380, w: 280, h: 150, reason: "강바람을 즐길 수 있는 잔디밭 중앙 배치" },
                    "medical": { name: "응급구조 부스", icon: "🚑", hex: "#EF4444", x: 810, y: 110, w: 150, h: 90, reason: "수변 안전사고 신속 대응을 위한 동쪽 외곽 배치" },
                    "toilet": { name: "이동식 화장실", icon: "🚻", hex: "#2563EB", x: 190, y: 520, w: 150, h: 90, reason: "서쪽 상하수도 차량 진입로 인근" },
                    "info": { name: "종합 안내소", icon: "ℹ️", hex: "#EC4899", x: 500, y: 580, w: 160, h: 70, reason: "광장 중앙 진입로 안내" },
                    "exit": { name: "주차장 및 출입구", icon: "🚪", hex: "#64748B", x: 500, y: 670, w: 220, h: 60, reason: "한강공원 주차장 진입로 연계" }
                }
            }
        };

        function appData() {
            return {
                page: 'home',
                loggedIn: true,
                username: '주은님',
                
                // Event Setup State
                eventName: '2026 청춘 페스티벌',
                eventType: '뮤직 페스티벌 & 공연',
                locationKey: 'olympic',
                locationName: '서울 올림픽공원 잔디마당 (대규모 야외)',
                expectedVisitors: 5000,
                budget: '5,000만원',
                
                // Modal Temp State
                showSetupModal: false,
                tempEventName: '2026 청춘 페스티벌',
                tempEventType: '뮤직 페스티벌 & 공연',
                tempLocationKey: 'olympic',
                tempExpectedVisitors: 5000,
                tempBudget: '5,000만원',
                locationPresets: LOCATION_PRESETS,

                // Facilities & Digital Twin State
                facilities: JSON.parse(JSON.stringify(LOCATION_PRESETS['olympic'].facilities)),
                selectedFacility: 'stage',
                viewMode: '2d',
                simulated: false,
                userInput: '',
                chatMessages: [
                    { role: 'assistant', content: "안녕하세요! 아키스케치 연동 AI 공간 설계 도우미입니다. '푸드존을 외곽으로 이동해줘' 또는 '화장실을 의료센터 근처로 배치해줘' 같이 입력해 보세요." }
                ],

                initApp() {
                    this.$watch('page', (val) => {
                        if (val === 'dashboard') {
                            setTimeout(() => this.updateMap(), 150);
                        }
                    });
                },

                onLocationChange() {
                    const preset = LOCATION_PRESETS[this.tempLocationKey];
                    if (preset) {
                        this.locationName = preset.name;
                    }
                },

                applyEventSettings() {
                    this.eventName = this.tempEventName;
                    this.eventType = this.tempEventType;
                    this.locationKey = this.tempLocationKey;
                    this.locationName = LOCATION_PRESETS[this.tempLocationKey].name;
                    this.expectedVisitors = this.tempExpectedVisitors;
                    this.budget = this.tempBudget;
                    
                    // Reset facilities to selected location preset
                    this.facilities = JSON.parse(JSON.stringify(LOCATION_PRESETS[this.tempLocationKey].facilities));
                    this.selectedFacility = 'stage';
                    this.showSetupModal = false;
                    
                    this.chatMessages.push({
                        role: 'assistant',
                        content: `✅ '${this.locationName}' 장소 템플릿과 '${this.eventName}' 조건에 맞추어 아키스케치 공간 배치를 재계산했습니다!`
                    });
                    
                    setTimeout(() => this.updateMap(), 150);
                },

                get currentFacility() {
                    return this.facilities[this.selectedFacility] || Object.values(this.facilities)[0];
                },

                updateMap() {
                    const facs = this.facilities;
                    const xVals = [], yVals = [], textVals = [], colorVals = [], customVals = [], sizeVals = [];

                    for (let k in facs) {
                        let f = facs[k];
                        xVals.push(f.x);
                        yVals.push(f.y);
                        let prefix = (this.selectedFacility === k) ? "📍 " : "";
                        textVals.push(prefix + f.icon + " " + f.name);
                        colorVals.push(f.hex);
                        customVals.push(k);
                        sizeVals.push(this.selectedFacility === k ? 22 : 16);
                    }

                    // Background boundary shape
                    let shapes = [
                        { type: "rect", x0: 40, y0: 40, x1: 960, y1: 720, fillcolor: this.viewMode === '3d' ? '#0F172A' : '#F1F5F9', opacity: 0.9, line: { color: "#94A3B8", width: 3, dash: "dash" } },
                        { type: "rect", x0: 320, y0: 240, x1: 680, y1: 500, fillcolor: "#DCFCE7", opacity: 0.5, line: { color: "#16A34A", width: 2 } }
                    ];

                    // Add individual facility rects
                    for (let k in facs) {
                        let f = facs[k];
                        let isSel = (this.selectedFacility === k);
                        shapes.push({
                            type: "rect",
                            x0: f.x - f.w/2,
                            y0: f.y - f.h/2,
                            x1: f.x + f.w/2,
                            y1: f.y + f.h/2,
                            fillcolor: f.hex,
                            opacity: 0.88,
                            line: { color: isSel ? "#F59E0B" : "#FFFFFF", width: isSel ? 4 : 2 }
                        });
                    }

                    let trace = {
                        x: xVals,
                        y: yVals,
                        mode: 'markers+text',
                        text: textVals,
                        textposition: 'top center',
                        textfont: { size: 12, color: this.viewMode === '3d' ? '#FFFFFF' : '#0F172A', family: 'Pretendard' },
                        customdata: customVals,
                        marker: { size: sizeVals, color: '#2563EB', line: { color: '#FFFFFF', width: 2 } },
                        showlegend: false
                    };

                    let layout = {
                        xaxis: { range: [0, 1000], showgrid: true, gridcolor: this.viewMode === '3d' ? '#334155' : '#E2E8F0', zeroline: false },
                        yaxis: { range: [760, 0], showgrid: true, gridcolor: this.viewMode === '3d' ? '#334155' : '#E2E8F0', zeroline: false },
                        height: 460,
                        margin: { l: 10, r: 10, t: 10, b: 10 },
                        paper_bgcolor: this.viewMode === '3d' ? '#1E293B' : '#FFFFFF',
                        plot_bgcolor: this.viewMode === '3d' ? '#0F172A' : '#FAFAFA',
                        clickmode: 'event+select'
                    };

                    Plotly.newPlot('spatialMap', [trace], layout, {responsive: true, displayModeBar: false}).then(() => {
                        let mapEl = document.getElementById('spatialMap');
                        mapEl.on('plotly_click', (data) => {
                            if (data.points && data.points[0].customdata) {
                                this.selectedFacility = data.points[0].customdata;
                            }
                        });
                    });
                },

                runSimulation() {
                    this.simulated = true;
                    setTimeout(() => {
                        let simData = [{
                            z: [
                                [10, 15, 20, 25, 30, 30, 25, 20, 15, 10],
                                [15, 25, 40, 60, 95, 95, 60, 40, 25, 15],
                                [20, 35, 60, 80, 70, 70, 80, 60, 35, 20],
                                [15, 30, 45, 50, 40, 40, 50, 45, 30, 15],
                                [10, 20, 35, 40, 30, 30, 40, 35, 20, 10],
                                [10, 25, 55, 65, 40, 40, 65, 55, 25, 10],
                                [10, 15, 30, 35, 25, 25, 35, 30, 15, 10],
                                [5, 10, 15, 20, 15, 15, 20, 15, 10, 5],
                                [5, 5, 10, 15, 10, 10, 15, 10, 5, 5],
                                [2, 5, 8, 10, 8, 8, 10, 8, 5, 2]
                            ],
                            type: 'heatmap',
                            colorscale: 'YlOrRd'
                        }];
                        let simLayout = {
                            margin: { l: 10, r: 10, t: 10, b: 10 },
                            height: 140,
                            paper_bgcolor: 'transparent',
                            plot_bgcolor: 'transparent',
                            xaxis: { visible: false },
                            yaxis: { visible: false }
                        };
                        Plotly.newPlot('simHeatmap', simData, simLayout, {displayModeBar: false});
                    }, 50);
                },

                sendChat() {
                    if (!this.userInput.trim()) return;
                    let txt = this.userInput;
                    this.chatMessages.push({ role: 'user', content: txt });
                    this.userInput = '';

                    let clean = txt.replace(/\s+/g, '');
                    let facs = this.facilities;
                    let targetKey = this.selectedFacility;
                    if (clean.includes("푸드") || clean.includes("음식")) targetKey = "food";
                    else if (clean.includes("화장실")) targetKey = "toilet";
                    else if (clean.includes("무대")) targetKey = "stage";
                    else if (clean.includes("의료")) targetKey = "medical";

                    let f = facs[targetKey];
                    let action = "";
                    if (clean.includes("외곽") || clean.includes("멀리")) {
                        f.x = 130; f.y = 400;
                        action = f.name + "을(를) 혼잡 분산을 위해 외곽 독립 구역으로 이동시켰습니다.";
                    } else if (clean.includes("북쪽") || clean.includes("위")) {
                        f.y = Math.max(80, f.y - 100);
                        action = f.name + " 위치를 상단으로 조정했습니다.";
                    } else if (clean.includes("남쪽") || clean.includes("아래")) {
                        f.y = Math.min(640, f.y + 100);
                        action = f.name + " 위치를 하단으로 조정했습니다.";
                    } else {
                        f.x = (f.x + 80) % 800 + 100;
                        action = f.name + "의 좌표를 아키스케치 알고리즘으로 재배치했습니다.";
                    }

                    f.reason = "AI 사용자 대화 반영: " + action;
                    this.selectedFacility = targetKey;

                    setTimeout(() => {
                        this.chatMessages.push({ role: 'assistant', content: "✅ " + action });
                        this.updateMap();
                    }, 300);
                },

                downloadReport() {
                    let content = `[결재 기안서] 행사 장소 및 공간 배치 타당성 검토서\n행사명: ${this.eventName}\n장소: ${this.locationName}\n예상인원: ${this.expectedVisitors}명\n예산: ${this.budget}\n`;
                    let blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
                    let link = document.createElement('a');
                    link.href = URL.createObjectURL(blob);
                    link.download = 'event_architect_report.txt';
                    link.click();
                }
            }
        }
    </script>
</body>
</html>
