# -*- coding: utf-8 -*-
import streamlit as st

st.set_page_config(
    page_title="이벤트 온 (Event On) - AI 기반 행사 자동 설계 플랫폼",
    page_icon="🎪",
    layout="wide"
)

# HTML / JS / CSS 전체 코드를 담은 템플릿 (이모지 유니코드 이스케이프 처리로 파이썬 문법 에러 원천 차단)
HTML_CONTENT = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>이벤트 온 (Event On) - AI 기반 행사 자동 설계 플랫폼</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
<style>
  body { font-family: Pretendard, -apple-system, sans-serif; background: #0f172a; color: #f8fafc; }
  .screen { display: none; }
  .screen.active { display: block; }
  .wrap { position: relative; width: 100%; background: #1e293b; border-radius: 12px; overflow: hidden; }
  #wrap { aspect-ratio: 1.85; }
  #wrap2 { aspect-ratio: 1.6; }
  .c3 { cursor: grab; background: linear-gradient(#e0f2fe, #f8fafc); position: absolute; inset: 0; width: 100%; height: 100%; }
</style>
</head>
<body class="min-h-screen flex flex-col">

  <!-- 네비게이션 바 -->
  <header class="bg-slate-900 border-b border-slate-800 px-6 py-4 flex justify-between items-center">
    <div class="flex items-center gap-3 cursor-pointer" onclick="goHome()">
      <span class="text-2xl">&#127915;</span>
      <h1 class="text-xl font-black bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent">&#이벤트 온 (Event On)</h1>
      <span class="text-xs bg-blue-500/20 text-blue-400 px-2.5 py-1 rounded-full font-bold">AI Digital Twin Platform</span>
    </div>
    <div class="flex items-center gap-3">
      <button onclick="goHome()" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-sm font-bold rounded-lg transition">&#127968; 홈으로</button>
      <button onclick="openWorkflowModal()" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-sm font-bold rounded-lg transition">&#9881;&#65039; AI 설계 프로세스</button>
    </div>
  </header>

  <!-- 메인 컨테이너 -->
  <main class="flex-1 max-w-7xl w-full mx-auto p-6">

    <!-- 1. 홈 화면 (설계 정보 입력) -->
    <div id="screen-home" class="screen active space-y-8">
      <div class="text-center space-y-3 py-6">
        <h2 class="text-3xl font-extrabold tracking-tight">AI가 완성하는 스마트 행사장 설계</h2>
        <p class="text-slate-400 text-sm max-w-xl mx-auto">행사 정보를 입력하면 AI 디지털 트윈과 수천 가지 최적화 알고리즘이 완벽한 배치도와 안전 시뮬레이션을 제공합니다.</p>
      </div>

      <div class="bg-slate-800/60 border border-slate-700/80 rounded-2xl p-6 md:p-8 shadow-xl max-w-3xl mx-auto">
        <h3 class="text-lg font-bold mb-6 flex items-center gap-2">&#10024; 행사장 기본 정보 입력</h3>
        <form id="designForm" onsubmit="startDesign(event)" class="grid grid-cols-1 md:grid-cols-2 gap-5">
          <div>
            <label class="block text-xs font-bold text-slate-400 mb-2">행사명</label>
            <input type="text" id="evName" required value="2026 청춘 힐링 문화 박람회" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-blue-500">
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-400 mb-2">행사 목적</label>
            <input type="text" id="evPurpose" required value="청소년 및 시민 문화 체험 및 심리 힐링" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-blue-500">
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-400 mb-2">총 예산 (원)</label>
            <input type="number" id="evBudget" required value="50000000" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-blue-500">
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-400 mb-2">예상 방문객 수 (명)</label>
            <input type="number" id="evVisitors" required value="3500" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-blue-500">
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-400 mb-2">행사 장소</label>
            <input type="text" id="evLocation" required value="춘천 의암공원 일대 (야외 광장)" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-blue-500">
          </div>
          <div>
            <label class="block text-xs font-bold text-slate-400 mb-2">원하는 분위기</label>
            <select id="evVibe" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-blue-500">
              <option value="healing">&#127807; 힐링 및 자연 친화적</option>
              <option value="dynamic">&#128293; 활기찬 축제 및 공연 중심</option>
              <option value="tech">&#128161; 스마트 테크 및 체험 중심</option>
            </select>
          </div>
          <div class="md:col-span-2 pt-4">
            <button type="submit" class="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold py-4 rounded-xl shadow-lg shadow-blue-600/20 transition text-base">
              &#128640; AI 디지털 트윈 행사장 자동 설계 시작하기
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- 2. 워크스페이스 화면 (디지털 트윈 & 시뮬레이션) -->
    <div id="screen-workspace" class="screen space-y-6">
      <!-- 상단 컨트롤 바 -->
      <div class="flex flex-wrap gap-2 items-center bg-slate-800/80 p-3 rounded-xl border border-slate-700">
        <button id="bMode" class="px-3 py-2 bg-blue-600 text-white text-xs font-bold rounded-lg" onclick="setMode('after')">&#10022; AI 최적 배치</button>
        <button id="bModeB" class="px-3 py-2 bg-slate-700 text-slate-300 text-xs font-bold rounded-lg" onclick="setMode('before')">설계 전(기존) 배치</button>
        <div class="h-5 w-[1px] bg-slate-700 mx-1"></div>
        <button id="b3d" class="px-3 py-2 bg-blue-600 text-white text-xs font-bold rounded-lg" onclick="setView(true)">&#129482;&#127995; 3D 입체 설계도</button>
        <button id="b2d" class="px-3 py-2 bg-slate-700 text-slate-300 text-xs font-bold rounded-lg" onclick="setView(false)">&#128506;&#65039; 2D 평면도</button>
        <button id="bHeat3" class="px-3 py-2 bg-slate-700 text-slate-300 text-xs font-bold rounded-lg" onclick="togHeat3()">&#128293; 히트맵 겹치기</button>
        <div class="flex-1"></div>
        <button id="bPlay" class="px-3 py-2 bg-slate-700 text-slate-300 text-xs font-bold rounded-lg" onclick="togSim()">&#9208; 시뮬레이션 정지</button>
        <button id="bRain" class="px-3 py-2 bg-amber-600/30 text-amber-300 border border-amber-500/40 text-xs font-bold rounded-lg" onclick="togRain()">&#127783;&#65039; 우천</button>
        <button id="bEmg" class="px-3 py-2 bg-red-600/30 text-red-300 border border-red-500/40 text-xs font-bold rounded-lg" onclick="togEmg()">&#128680; 응급환자 발생</button>
      </div>

      <!-- 타임라인 -->
      <div class="flex items-center gap-4 bg-slate-800/60 border border-slate-700 p-3 rounded-xl text-xs font-bold">
        <span>&#9232; 시간대</span>
        <button id="bTl" onclick="togTl()" class="px-3 py-1.5 bg-blue-600 text-white rounded-lg">&#9654; 재생</button>
        <input type="range" id="tSl" min="10" max="20" step="1" value="14" oninput="setTime(+this.value)" class="flex-1 accent-blue-500">
        <span class="bg-blue-600 text-white px-3 py-1 rounded-full" id="tTxt">14:00</span>
        <span id="tDesc" class="text-slate-400 font-medium"></span>
      </div>

      <!-- 메인 디지털 트윈 뷰 -->
      <div class="bg-slate-800/80 border border-slate-700 rounded-2xl p-4 shadow-xl">
        <div class="flex justify-between items-center mb-3">
          <h4 class="text-sm font-bold flex items-center gap-2">
            <span>&#128506;&#65039; 행사장 디지털 트윈</span>
            <span id="verTxt" class="text-slate-400 font-normal"></span>
          </h4>
          <div class="flex gap-2">
            <span id="peopleTxt" class="text-xs bg-blue-500/20 text-blue-400 px-3 py-1 rounded-full font-bold"></span>
            <span id="status" class="text-xs bg-emerald-500/20 text-emerald-400 px-3 py-1 rounded-full font-bold">실시간 군중 시뮬레이션</span>
          </div>
        </div>
        <div class="wrap" id="wrap">
          <canvas id="cv" style="display:none"></canvas>
          <canvas id="hm" style="display:none;opacity:.75;pointer-events:none"></canvas>
          <canvas id="pp" style="display:none;pointer-events:none"></canvas>
          <div class="c3" id="c3"></div>
          <div id="legend" class="absolute left-2 bottom-2 bg-slate-900/90 border border-slate-700 rounded-lg p-2 text-[10px] grid grid-cols-3 gap-x-3 gap-y-1 z-10 pointer-events-none"></div>
          <div id="hint" class="absolute right-2 top-2 bg-slate-900/80 text-slate-300 text-[10px] px-2 py-1 rounded-md z-10 pointer-events-none">드래그: 회전 · 휠: 확대/축소</div>
        </div>
      </div>

      <!-- 하단 그리드 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="bg-slate-800/80 border border-slate-700 rounded-2xl p-4 shadow-xl space-y-4">
          <h4 class="text-sm font-bold flex items-center justify-between">
            <span>&#10133; 맞춤형 부스/시설 추가</span>
            <span class="text-xs text-slate-400">사용자 정의 구역</span>
          </h4>
          <div class="space-y-3">
            <div>
              <label class="block text-xs text-slate-400 mb-1">부스 이름</label>
              <input type="text" id="customBoothName" placeholder="예: AI 심리상담 부스" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs focus:outline-none focus:border-blue-500">
            </div>
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-xs text-slate-400 mb-1">카테고리</label>
                <select id="customBoothType" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs focus:outline-none focus:border-blue-500">
                  <option value="booth">체험부스</option>
                  <option value="food">푸드존</option>
                  <option value="rest">휴게공간</option>
                </select>
              </div>
              <div>
                <label class="block text-xs text-slate-400 mb-1">아이콘 (이모지)</label>
                <input type="text" id="customBoothIcon" value="&#129302;" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-center focus:outline-none focus:border-blue-500">
              </div>
            </div>
            <button onclick="addCustomBooth()" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-2.5 rounded-xl text-xs transition">디지털 트윈에 부스 배치하기</button>
          </div>
        </div>

        <div class="bg-slate-800/80 border border-slate-700 rounded-2xl p-4 shadow-xl space-y-4">
          <h4 class="text-sm font-bold">&#128202; AI 분석 리포트 & 구역 현황</h4>
          <div class="grid grid-cols-2 gap-3">
            <div class="bg-slate-900/60 border border-slate-700/60 p-3 rounded-xl text-xs text-slate-400 font-semibold">
              현재 최대 밀도 <b id="kPeak" class="block text-base text-white mt-1">-</b>
            </div>
            <div class="bg-slate-900/60 border border-slate-700/60 p-3 rounded-xl text-xs text-slate-400 font-semibold">
              응급 최대 도달 <b id="kMed" class="block text-base text-white mt-1">-</b>
            </div>
          </div>
          <div>
            <div class="text-xs font-bold mb-2">&#128205; 배치된 구역 <span id="zCnt" class="text-slate-400"></span></div>
            <div id="zlist" class="grid grid-cols-2 gap-2 max-h-32 overflow-auto text-xs font-bold"></div>
          </div>
        </div>
      </div>
    </div>
  </main>

  <!-- AI Workflow 모달 -->
  <div id="workflowModal" class="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
    <div class="bg-slate-900 border border-slate-700 rounded-2xl max-w-2xl w-full p-6 space-y-6 shadow-2xl">
      <div class="flex justify-between items-center">
        <h3 class="text-lg font-extrabold text-blue-400">&#9881;&#65039; AI 행사 설계 프로세스 (Workflow)</h3>
        <button onclick="closeWorkflowModal()" class="text-slate-400 hover:text-white font-bold text-lg">&#10005;</button>
      </div>
      <div class="space-y-4 text-xs text-slate-300 leading-relaxed">
        <div class="bg-slate-800/60 p-3 rounded-xl border border-slate-700">
          <b class="text-blue-400 block mb-1">1단계: 운영 정보 입력 및 디지털 트윈 생성</b>
          사용자가 입력한 행사 목적, 예산, 방문객 수, 장소 특성을 바탕으로 160x100 규모의 3D 가상 공간(디지털 트윈)을 실시간으로 구축합니다.
        </div>
        <div class="bg-slate-800/60 p-3 rounded-xl border border-slate-700">
          <b class="text-blue-400 block mb-1">2단계: 수천 개 배치안 자동 생성 및 최적화</b>
          다목적 최적화(Multi-objective Optimization) 알고리즘을 통해 혼잡도를 최소화하고 접근성을 최대화하는 최적의 구역 배치를 도출합니다.
        </div>
        <div class="bg-slate-800/60 p-3 rounded-xl border border-slate-700">
          <b class="text-blue-400 block mb-1">3단계: 실시간 군중 이동 시뮬레이션 및 Explainable AI (XAI)</b>
          시간대별 인구 유입, 우천 및 응급 상황 시나리오를 반영한 시뮬레이션을 거쳐 최종 설계 리포트와 전후 비교 데이터를 제공합니다.
        </div>
      </div>
      <button onclick="closeWorkflowModal()" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 rounded-xl text-xs">확인 완료</button>
    </div>
  </div>

  <script>
    let D = {
      theme: { kind: 'outdoor', ground: '#1e3a2f', groundRain: '#172554', path: '#334155' },
      mpu: 1.5, total: 94.5, before_total: 68.2,
      params: { visitors: 3500 },
      detail: { t_max: 42, risk_zones: 1 },
      before_detail: { t_max: 98, risk_zones: 4 },
      gates: [
        { name: '정문 (북쪽)', x: 80, y: 5 },
        { name: '서문 (주차장)', x: 5, y: 50 },
        { name: '동문 (역 출구)', x: 155, y: 50 }
      ],
      zones: [
        { name: '메인 공연장', type: 'stage', x: 60, y: 20, w: 40, h: 22, color: '#8b5cf6', icon: '\ud83c\udfa4', attract: 90, ht: 4 },
        { name: '청춘 체험부스', type: 'booth', x: 20, y: 55, w: 35, h: 18, color: '#ec4899', icon: '\ud83c\udfa8', attract: 70 },
        { name: '푸드트럭 존', type: 'food', x: 105, y: 55, w: 35, h: 18, color: '#f59e0b', icon: '\ud83c\udf54', attract: 85 },
        { name: '힐링 휴게공간', type: 'rest', x: 65, y: 78, w: 30, h: 16, color: '#10b981', icon: '\ud83c\udf33', attract: 40 },
        { name: '응급의료센터', type: 'medical', x: 10, y: 15, w: 18, h: 14, color: '#ef4444', icon: '\ud83d\ude91', attract: 10 },
        { name: '종합 안내소', type: 'info', x: 132, y: 15, w: 18, h: 14, color: '#0ea5e9', icon: '\u2139\ufe0f', attract: 30 },
        { name: '화장실', type: 'restroom', x: 73, y: 50, w: 14, h: 12, color: '#06b6d4', icon: '\', attract: 50 }
      ],
      before_zones: [
        { name: '메인 공연장', type: 'stage', x: 10, y: 10, w: 35, h: 20, color: '#8b5cf6', icon: '\ud83c\udfa4', attract: 90, ht: 4 },
        { name: '푸드트럭 존', type: 'food', x: 50, y: 10, w: 35, h: 20, color: '#f59e0b', icon: '\ud83c\udf54', attract: 85 },
        { name: '체험부스', type: 'booth', x: 90, y: 10, w: 35, h: 20, color: '#ec4899', icon: '\ud83c\udfa8', attract: 70 },
        { name: '응급의료센터', type: 'medical', x: 130, y: 70, w: 18, h: 14, color: '#ef4444', icon: '\ud83d\ude91', attract: 10 }
      ]
    };

    const WW = 160, WH = 100, GX = 40, GY = 25;
    let mode = 'after', sim = true, rain = false, emg = null, tHour = 14, tlTimer = null, is3d = true, heat3 = false;
    const $ = id => document.getElementById(id);

    function goHome() {
      $('screen-home').classList.add('active');
      $('screen-workspace').classList.remove('active');
      if (tlTimer) { clearInterval(tlTimer); tlTimer = null; }
    }

    function startDesign(e) {
      e.preventDefault();
      D.params.visitors = +$('evVisitors').value;
      $('screen-home').classList.remove('active');
      $('screen-workspace').classList.add('active');
      setTimeout(() => { resize(); initR3(); setView(true); setMode('after'); }, 100);
    }

    function openWorkflowModal() { $('workflowModal').classList.remove('hidden'); }
    function closeWorkflowModal() { $('workflowModal').classList.add('hidden'); }

    function addCustomBooth() {
      const name = $('customBoothName').value.trim();
      if (!name) { alert('부스 이름을 입력해주세요.'); return; }
      const type = $('customBoothType').value;
      const icon = $('customBoothIcon').value || '\ud83d\udccc';
      const colors = { booth: '#ec4899', food: '#f59e0b', rest: '#10b981' };
      
      Z().push({ name, type, x: 65, y: 45, w: 22, h: 14, color: colors[type] || '#3b82f6', icon, attract: 50 });
      $('customBoothName').value = '';
      drawBase();
      if (R3) buildScene3();
      updateZList();
      alert(`"${name}" 부스가 행사장 중앙에 성공적으로 배치되었습니다!`);
    }

    $('legend').innerHTML =
      [['#8b5cf6','공연장'],['#ec4899','체험부스'],['#f59e0b','푸드존'],['#10b981','휴게공간'],['#ef4444','응급의료'],['#0ea5e9','안내센터'],['#06b6d4','화장실'],['#334155','출입구']]
      .map(a => `<span><i style="background:${a[0]};display:inline-block;width:8px;height:8px;border-radius:2px;margin-right:4px;"></i>${a[1]}</span>`).join('');

    const cv = $('cv'), hm =$('hm'), pp = $('pp'), hm2 =$('hm2');
    const cx = cv.getContext('2d'), hx = hm.getContext('2d'), px = pp.getContext('2d'), h2 = hm2.getContext('2d');
    const wrap = $('wrap'), wrap2 =$('wrap2');
    let W = 0, H = 0, S = 1, W2 = 0, H2 = 0;
    const Z = () => mode === 'after' ? D.zones : D.before_zones;
    const mpu = D.mpu, cellArea = (WW/GX)*(WH/GY)*mpu*mpu;
    const NAG = 280; let agents = []; let raindrops = [];
    let heat = new Float32Array(GX*GY);

    function resize() {
      W = wrap.clientWidth; H = wrap.clientHeight; S = W/WW;
      [cv,hm,pp].forEach(c => { c.width = W; c.height = H; });
      W2 = wrap2 ? wrap2.clientWidth : 300; H2 = wrap2 ? wrap2.clientHeight : 200;
      drawBase(); if (R3) size3();
    }

    function factor(h) { return h < 12 ? .55 : h < 15 ? 1.0 : h < 18 ? .8 : .65; }
    function descT(h) { return h < 12 ? '개장 초반 - 순차 입장(여유)' : h < 15 ? '피크 - 푸드·공연 집중(혼잡)' : h < 18 ? '오후 - 체험·휴게 분산' : '폐장 전 - 공연 집중 및 퇴장'; }
    
    function pickZone() {
      const Zs = Z(); let tot = 0;
      const w = Zs.map(z => { const a = z.type === 'medical' ? 0 : z.attract; tot += a; return a; });
      let r = Math.random() * tot;
      for (let i = 0; i < Zs.length; i++) { r -= w[i]; if (r <= 0) return i; }
      return 0;
    }

    function spawn(a) {
      const g = D.gates[Math.floor(Math.random() * D.gates.length)];
      a.x = g.x + (Math.random()-.5)*4; a.y = g.y + (Math.random()-.5)*4; a.leaving = false; a.dwell = 0; a.zone = pickZone(); setTarget(a);
    }
    function setTarget(a) {
      const z = Z()[a.zone]; if (!z) return;
      a.tx = z.x - 1.5 + Math.random()*(z.w+3); a.ty = z.y - 1.5 + Math.random()*(z.h+3);
      a.sp = .28 + Math.random()*.2;
    }
    function initAgents() {
      agents = [];
      for (let i = 0; i < NAG; i++) {
        const a = {}; spawn(a);
        const t = Math.random(); a.x = a.x + (a.tx - a.x)*t; a.y = a.y + (a.ty - a.y)*t;
        a.active = i < NAG * factor(tHour); agents.push(a);
      }
      raindrops = []; for (let i = 0; i < 90; i++) raindrops.push({ x: Math.random()*W, y: Math.random()*H, l: 7+Math.random()*10, v: 6+Math.random()*6 });
    }

    function step(dt) {
      const f = factor(tHour); const n = Math.floor(NAG * f);
      agents.forEach((a, i) => {
        a.active = i < n; if (!a.active) return;
        if (a.dwell > 0) {
          a.dwell -= dt;
          if (a.dwell <= 0) { if (Math.random() < .35) { a.leaving = true; const g = D.gates[Math.floor(Math.random()*D.gates.length)]; a.tx = g.x; a.ty = g.y; } else { a.zone = pickZone(); setTarget(a); } }
          return;
        }
        let dx = a.tx - a.x, dy = a.ty - a.y, d = Math.hypot(dx, dy);
        let sp = a.sp * (rain ? 1.5 : 1);
        if (d < 1.2) { if (a.leaving) spawn(a); else a.dwell = 3 + Math.random()*8; }
        else { a.x += dx/d*sp; a.y += dy/d*sp; }
      });
      if (emg) {
        const meds = Z().filter(z => z.type === 'medical'); let best = meds[0], bd = 1e9;
        meds.forEach(m => { const d = Math.hypot(m.x+m.w/2 - emg.x, m.y+m.h/2 - emg.y); if (d < bd) { bd = d; best = m; } });
        emg.target = best;
        if (best && bd > 1.5) {
          emg.x += (best.x+best.w/2 - emg.x)/bd * .9; emg.y += (best.y+best.h/2 - emg.y)/bd * .9;
          $('status').textContent = '\ud83d\ude91 응급 이송 중… 의료센터까지 ' + Math.round(bd * mpu) + 'm';
        } else if (best) {
          $('status').textContent = '\u2705 의료센터 도착 완료';
        }
      }
    }

    function updateHeat() {
      const n = Math.floor(NAG * factor(tHour)); const per = D.params.visitors * .5 / Math.max(1, n) * factor(tHour);
      const g = new Float32Array(GX * GY);
      agents.forEach(a => {
        if (!a.active) return;
        const ix = Math.min(GX-1, Math.max(0, Math.floor(a.x/(WW/GX)))), iy = Math.min(GY-1, Math.max(0, Math.floor(a.y/(WH/GY))));
        g[iy*GX + ix] += per;
      });
      const o = new Float32Array(GX * GY);
      for (let y = 0; y < GY; y++) for (let x = 0; x < GX; x++) {
        let s = 0, c = 0;
        for (let j = -1; j <= 1; j++) for (let i = -1; i <= 1; i++) {
          const xx = x + i, yy = y + j;
          if (xx >= 0 && xx < GX && yy >= 0 && yy < GY) { const w = (i===0&&j===0)?2:1; s += g[yy*GX + xx]*w; c += w; }
        }
        o[y*GX + x] = s / c / cellArea;
      }
      for (let k = 0; k < o.length; k++) heat[k] = heat[k]*.85 + o[k]*.15;
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
      const cw = w/GX, ch = h/GY; let peak = 0, hot = 0, act = 0;
      for (let y = 0; y < GY; y++) for (let x = 0; x < GX; x++) {
        const d = heat[y*GX + x]; peak = Math.max(peak, d); if (d >= .12) act++; if (d >= .5) hot++;
        const c = heatColor(d); if (c) { ctx.fillStyle = c; ctx.fillRect(x*cw, y*ch, cw+.5, ch+.5); }
      }
      return [peak, hot, act];
    }

    function drawBase() {
      const T = D.theme; cx.clearRect(0, 0, W, H);
      cx.fillStyle = rain ? T.groundRain : T.ground; cx.fillRect(0, 0, W, H);
      Z().forEach(z => {
        const x = z.x*S, y = z.y*S, w = z.w*S, h = z.h*S;
        cx.fillStyle = z.color; cx.beginPath(); cx.roundRect(x, y, w, h, 6); cx.fill();
        cx.strokeStyle = '#fff'; cx.lineWidth = 2; cx.stroke();
        cx.textAlign = 'center'; cx.fillStyle = '#fff';
        cx.font = 'bold 13px Pretendard'; cx.fillText(z.icon + ' ' + z.name, x + w/2, y + h/2 + 4, w - 4);
      });
      D.gates.forEach(g => {
        cx.fillStyle = '#1e293b'; cx.beginPath(); cx.arc(g.x*S, g.y*S, 8, 0, 7); cx.fill();
        cx.strokeStyle = '#fff'; cx.lineWidth = 2; cx.stroke();
      });
    }

    function drawPeople() {
      px.clearRect(0, 0, W, H);
      agents.forEach(a => {
        if (!a.active) return;
        px.fillStyle = '#fff'; px.beginPath(); px.arc(a.x*S, a.y*S, 3, 0, 7); px.fill();
      });
      if (emg) {
        px.fillStyle = '#ef4444'; px.beginPath(); px.arc(emg.x*S, emg.y*S, 8, 0, 7); px.fill();
        px.fillStyle = '#fff'; px.font = 'bold 11px Pretendard'; px.textAlign = 'center'; px.fillText('\ud83d\ude91 응급', emg.x*S, emg.y*S - 12);
      }
    }

    let R3 = null, S3, C3, G3, bodyM, headM, rainPts, emgGrp, heatPlane, heatTex;
    let yaw = .55, pitch = .72, zoom3 = 1, drag = false, lx = 0, ly = 0;
    const DUM = new THREE.Object3D();

    function M(c, o) { return new THREE.MeshLambertMaterial(Object.assign({ color: new THREE.Color(c) }, o || {})); }
    function bx(p, w, h, d, c, x, y, z, o) {
      const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), M(c, o)); m.position.set(x, y, z); p.add(m); return m;
    }
    function labelSprite(text, color) {
      const c = document.createElement('canvas'); c.width = 640; c.height = 150; const t = c.getContext('2d');
      t.fillStyle = 'rgba(255,255,255,.95)'; t.beginPath(); t.roundRect(4, 4, 632, 142, 24); t.fill();
      t.fillStyle = color; t.beginPath(); t.roundRect(4, 4, 26, 142, 12); t.fill();
      t.fillStyle = '#0f172a'; t.font = 'bold 60px Pretendard'; t.textAlign = 'center'; t.textBaseline = 'middle'; t.fillText(text, 340, 78, 560);
      const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(c), depthTest: false, transparent: true }));
      sp.renderOrder = 10; return sp;
    }

    function buildZone3(z) {
      const g = new THREE.Group(); const cxz = z.x + z.w/2 - WW/2, czz = z.y + z.h/2 - WH/2; g.position.set(cxz, 0, czz); G3.add(g);
      const w = z.w, h = z.h; const pale = new THREE.Color(z.color).lerp(new THREE.Color('#ffffff'), .65).getStyle();
      bx(g, w, .5, h, pale, 0, .25, 0);
      if (z.type === 'stage') {
        bx(g, w*.9, 3, h*.4, '#7c3aed', 0, 2, -h*.25);
      } else {
        bx(g, w*.8, 3.5, h*.8, z.color, 0, 2, 0);
      }
      const sp = labelSprite(z.icon + ' ' + z.name, z.color);
      sp.scale.set(32, 32*150/640, 1); sp.position.set(0, 6, 0); g.add(sp);
    }

    function buildScene3() {
      if (G3) S3.remove(G3); G3 = new THREE.Group(); S3.add(G3);
      const T = D.theme;
      bx(G3, WW, .7, WH, rain ? T.groundRain : T.ground, 0, -.35, 0);
      Z().forEach(buildZone3);
    }

    function initR3() {
      const el = $('c3'); if (R3) return;
      try { R3 = new THREE.WebGLRenderer({ antialias: true }); } catch (e) { return; }
      el.appendChild(R3.domElement);
      S3 = new THREE.Scene(); S3.add(new THREE.AmbientLight(0xffffff, .8));
      const dl = new THREE.DirectionalLight(0xffffff, .6); dl.position.set(-50, 100, 50); S3.add(dl);
      C3 = new THREE.OrthographicCamera(-1, 1, 1, -1, -500, 1000);
      
      const N = NAG;
      bodyM = new THREE.InstancedMesh(new THREE.CylinderGeometry(.5, .6, 2, 8), M('#f97316'), N);
      headM = new THREE.InstancedMesh(new THREE.SphereGeometry(.6, 8, 8), M('#fde68a'), N);
      bodyM.frustumCulled = false; headM.frustumCulled = false; S3.add(bodyM); S3.add(headM);

      emgGrp = new THREE.Mesh(new THREE.SphereGeometry(1.5, 12, 12), new THREE.MeshBasicMaterial({ color: 0xef4444 }));
      emgGrp.visible = false; S3.add(emgGrp);

      heatTex = new THREE.CanvasTexture(hm);
      heatPlane = new THREE.Mesh(new THREE.PlaneGeometry(WW, WH), new THREE.MeshBasicMaterial({ map: heatTex, transparent: true, opacity: .8 }));
      heatPlane.rotation.x = -Math.PI/2; heatPlane.position.y = .5; heatPlane.visible = false; S3.add(heatPlane);

      const e = R3.domElement;
      e.onmousedown = ev => { drag = true; lx = ev.clientX; ly = ev.clientY; };
      window.addEventListener('mouseup', () => drag = false);
      e.onmousemove = ev => { if (!drag) return; yaw -= (ev.clientX - lx)*.008; pitch = Math.min(1.3, Math.max(.3, pitch + (ev.clientY - ly)*.006)); lx = ev.clientX; ly = ev.clientY; };
      e.addEventListener('wheel', ev => { ev.preventDefault(); zoom3 = Math.min(2.5, Math.max(.6, zoom3*(ev.deltaY < 0 ? 1.1 : .9))); }, { passive: false });

      size3(); buildScene3();
    }

    function size3() {
      if (!R3) return;
      const el = $('c3'); const w = el.clientWidth, h = el.clientHeight;
      R3.setSize(w, h); const f = 70, asp = w/h;
      C3.left = -f*asp; C3.right = f*asp; C3.top = f; C3.bottom = -f; C3.updateProjectionMatrix();
    }

    function render3() {
      if (!R3) return; const Rr = 380;
      C3.position.set(Math.sin(yaw)*Math.cos(pitch)*Rr, Math.sin(pitch)*Rr, Math.cos(yaw)*Math.cos(pitch)*Rr);
      C3.lookAt(0, 0, 0); C3.zoom = zoom3; C3.updateProjectionMatrix();

      agents.forEach((a, i) => {
        const s = a.active ? 1 : 0.0001;
        DUM.rotation.set(0, 0, 0); DUM.scale.set(s, s, s);
        DUM.position.set(a.x - WW/2, 1.5, a.y - WH/2); DUM.updateMatrix(); bodyM.setMatrixAt(i, DUM.matrix);
        DUM.position.y = 3.2; DUM.updateMatrix(); headM.setMatrixAt(i, DUM.matrix);
      });
      bodyM.instanceMatrix.needsUpdate = true; headM.instanceMatrix.needsUpdate = true;

      if (emg) {
        emgGrp.visible = true; emgGrp.position.set(emg.x - WW/2, 2.5, emg.y - WH/2);
      } else {
        emgGrp.visible = false;
      }
      heatPlane.visible = heat3; if (heat3) heatTex.needsUpdate = true;
      R3.render(S3, C3);
    }

    let last = performance.now(), kt = 0;
    function loop(now) {
      const dt = (now - last)/1000; last = now;
      if (sim) step(dt);
      updateHeat();
      const r = drawHeat(hx, W, H, false); drawHeat(h2, W2, H2, true);
      if (is3d) render3(); else drawPeople();

      const n = Math.round(D.params.visitors * .5 * factor(tHour));
      $('peopleTxt').textContent = '시뮬레이션 군중 ≈ ' + n.toLocaleString() + '명';
      
      kt += dt;
      if (kt > .4) {
        kt = 0; $('kPeak').textContent = r[0].toFixed(2) + ' 명/㎡';
        $('kMed').textContent = Math.round(D.detail.t_max) + '초';
      }
      requestAnimationFrame(loop);
    }

    function setView(v3) {
      is3d = v3; $('c3').style.display = v3 ? 'block' : 'none';
      [cv, hm, pp].forEach(c => c.style.display = v3 ? 'none' : 'block');
      hm.style.display = v3 ? 'none' : 'block';
      $('b3d').className = v3 ? 'px-3 py-2 bg-blue-600 text-white text-xs font-bold rounded-lg' : 'px-3 py-2 bg-slate-700 text-slate-300 text-xs font-bold rounded-lg';
      $('b2d').className = !v3 ? 'px-3 py-2 bg-blue-600 text-white text-xs font-bold rounded-lg' : 'px-3 py-2 bg-slate-700 text-slate-300 text-xs font-bold rounded-lg';
      if (v3) size3();
    }

    function togHeat3() {
      heat3 = !heat3;
      $('bHeat3').className = heat3 ? 'px-3 py-2 bg-blue-600 text-white text-xs font-bold rounded-lg' : 'px-3 py-2 bg-slate-700 text-slate-300 text-xs font-bold rounded-lg';
    }

    function setMode(m) {
      mode = m;
      $('bMode').className = m === 'after' ? 'px-3 py-2 bg-blue-600 text-white text-xs font-bold rounded-lg' : 'px-3 py-2 bg-slate-700 text-slate-300 text-xs font-bold rounded-lg';
      $('bModeB').className = m === 'before' ? 'px-3 py-2 bg-blue-600 text-white text-xs font-bold rounded-lg' : 'px-3 py-2 bg-slate-700 text-slate-300 text-xs font-bold rounded-lg';$('verTxt').textContent = m === 'after' ? '· AI 최적 배치 (점수: ' + D.total + '점)' : '· 기존 배치 (점수: ' + D.before_total + '점)';
      heat.fill(0); initAgents(); emg = null;
      drawBase(); if (R3) buildScene3();
      updateZList();
    }

    function updateZList() {
      $('zlist').innerHTML = Z().map(z => `<div class="bg-slate-900 border border-slate-700 p-2 rounded-lg flex items-center gap-2"><span style="color:${z.color}">${z.icon}</span> <span>${z.name}</span></div>`).join('');
      $('zCnt').textContent = '(' + Z().length + '개소)';
    }

    function togSim() { sim = !sim; $('bPlay').textContent = sim ? '\u23f8 시뮬레이션 정지' : '\u25b6 시뮬레이션 시작'; }
    function togRain() { rain = !rain; drawBase(); if (R3) buildScene3(); }
    function togEmg() {
      if (emg) { emg = null; $('status').textContent = '실시간 군중 시뮬레이션'; return; }
      const z = Z()[0]; emg = { x: z.x + z.w/2, y: z.y + z.h/2, target: null };
      sim = true; $('status').textContent = '\ud83d\udea8 응급환자 발생! 의료센터로 이송 중';
    }
    function setTime(h) { tHour = h; $('tSl').value = h; $('tTxt').textContent = h + ':00';$('tDesc').textContent = descT(h); }
    function togTl() {
      if (tlTimer) { clearInterval(tlTimer); tlTimer = null; $('bTl').textContent = '\u25b6 재생'; }
      else { $('bTl').textContent = '\u23f8 일시정지'; tlTimer = setInterval(() => { let n = tHour + 1; if (n > 20) n = 10; setTime(n); }, 2500); }
    }

    window.addEventListener('resize', resize);
    setTime(14);
    updateZList();
    requestAnimationFrame(loop);
  </script>
</body>
</html>
"""

# Streamlit을 통해 HTML 렌더링
st.components.v1.html(HTML_CONTENT, height=900, scrolling=True)
