import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(
    page_title="이벤트 온 (Event-On) - AI 행사 자동 설계 플랫폼",
    page_icon="🎪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

EVENT_AI_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Event AI - AI 행사장 설계 시스템</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
<!-- Three.js Library for 3D View Engine -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{
  font-family:"Pretendard Variable", Pretendard, -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
  color:#1e293b;
  background:#f8fafc;
  overflow-x:hidden;
}
button,input,select,textarea{font:inherit;}
button{cursor:pointer;transition:all 0.2s ease;}

/* Custom Scrollbar */
::-webkit-scrollbar {width:6px;height:6px;}
::-webkit-scrollbar-track {background:#f1f5f9;}
::-webkit-scrollbar-thumb {background:#cbd5e1;border-radius:4px;}
::-webkit-scrollbar-thumb:hover {background:#94a3b8;}

/* App Layout */
.app-container{
  display:flex;
  min-height:100vh;
  background:#f1f5f9;
}

/* Sidebar */
.sidebar{
  width:240px;
  background:#0f172a;
  color:#94a3b8;
  padding:20px 14px;
  display:flex;
  flex-direction:column;
  gap:20px;
  flex-shrink:0;
  border-right:1px solid #1e293b;
}
.brand{
  display:flex;
  align-items:center;
  gap:10px;
  padding:0 8px;
  color:#fff;
}
.brand-icon{
  width:36px;
  height:36px;
  background:linear-gradient(135deg,#2563eb,#3b82f6);
  border-radius:10px;
  display:grid;
  place-items:center;
  font-size:18px;
  font-weight:900;
  box-shadow:0 4px 12px rgba(37,99,235,0.4);
}
.brand-title{font-size:18px;font-weight:800;letter-spacing:-0.5px;color:#ffffff;}
.brand-sub{font-size:10px;color:#64748b;margin-top:1px;font-weight:500;}

.nav-group{display:flex;flex-direction:column;gap:4px;}
.nav-item{
  display:flex;
  align-items:center;
  gap:10px;
  padding:11px 14px;
  border-radius:10px;
  font-size:13.5px;
  font-weight:600;
  color:#94a3b8;
  cursor:pointer;
}
.nav-item:hover{background:rgba(255,255,255,0.05);color:#f1f5f9;}
.nav-item.active{
  background:linear-gradient(135deg, #2563eb, #3b82f6);
  color:#ffffff;
  box-shadow:0 4px 12px rgba(37,99,235,0.3);
}
.nav-icon{font-size:15px;width:18px;text-align:center;}

.side-profile{
  margin-top:auto;
  background:#1e293b;
  border-radius:12px;
  padding:12px;
  display:flex;
  align-items:center;
  gap:10px;
}
.side-avatar{
  width:32px;
  height:32px;
  background:#3b82f6;
  border-radius:50%;
  color:#fff;
  display:grid;
  place-items:center;
  font-weight:700;
  font-size:12px;
}
.side-user-info{flex:1;}
.side-user-name{font-size:12px;font-weight:700;color:#f8fafc;}
.side-user-btn{font-size:10px;color:#94a3b8;background:none;border:none;padding:0;margin-top:2px;cursor:pointer;}

.side-banner{
  background:linear-gradient(135deg, rgba(37,99,235,0.2), rgba(15,23,42,0.8));
  border:1px solid rgba(59,130,246,0.25);
  padding:14px;
  border-radius:12px;
  color:#e2e8f0;
}
.side-banner h5{font-size:12px;font-weight:800;color:#60a5fa;margin-bottom:4px;}
.side-banner p{font-size:10.5px;color:#94a3b8;line-height:1.4;}

/* Main Area */
.main-content{
  flex:1;
  padding:20px;
  display:flex;
  flex-direction:column;
  gap:16px;
  min-width:0;
  overflow-y:auto;
}

/* Header */
.top-header{
  display:flex;
  justify-content:space-between;
  align-items:center;
  background:#ffffff;
  padding:14px 20px;
  border-radius:16px;
  border:1px solid #e2e8f0;
  box-shadow:0 2px 8px rgba(0,0,0,0.02);
}
.top-title h2{font-size:20px;font-weight:800;color:#0f172a;display:flex;align-items:center;gap:8px;}
.top-title p{font-size:12px;color:#64748b;margin-top:2px;}

/* Page Views */
.page-view{display:none;}
.page-view.active{display:block;}

/* Form Card */
.form-card{
  background:#ffffff;
  border:1px solid #e2e8f0;
  border-radius:16px;
  padding:24px;
  box-shadow:0 2px 10px rgba(0,0,0,0.02);
}
.form-section-head{
  font-size:16px;
  font-weight:800;
  color:#0f172a;
  margin-bottom:18px;
  display:flex;
  align-items:center;
  gap:8px;
}
.form-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit, minmax(210px, 1fr));
  gap:16px;
  margin-bottom:20px;
}
.form-group{
  display:flex;
  flex-direction:column;
  gap:6px;
}
.form-group label{
  font-size:12px;
  font-weight:700;
  color:#334155;
  display:flex;
  align-items:center;
  gap:4px;
}
.form-group input, .form-group select, .form-group textarea{
  padding:10px 12px;
  border:1.5px solid #cbd5e1;
  border-radius:10px;
  background:#f8fafc;
  color:#0f172a;
  font-size:13px;
  font-weight:600;
  outline:none;
}
.form-group input:focus, .form-group select:focus, .form-group textarea:focus{
  border-color:#2563eb;
  background:#ffffff;
  box-shadow:0 0 0 3px rgba(37,99,235,0.1);
}

.btn-primary{
  background:linear-gradient(135deg, #2563eb, #1d4ed8);
  color:#ffffff;
  border:none;
  padding:12px 24px;
  border-radius:12px;
  font-weight:800;
  font-size:13.5px;
  box-shadow:0 4px 14px rgba(37,99,235,0.3);
  display:inline-flex;
  align-items:center;
  gap:8px;
}
.btn-primary:hover{transform:translateY(-1px);box-shadow:0 6px 18px rgba(37,99,235,0.4);}

.btn-secondary{
  background:#f1f5f9;
  color:#334155;
  border:1px solid #cbd5e1;
  padding:6px 12px;
  border-radius:8px;
  font-size:11.5px;
  font-weight:700;
  display:inline-flex;
  align-items:center;
  gap:4px;
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
.btn-warning.active{background:#f59e0b;color:#fff;border-color:#d97706;}

.btn-danger{
  background:#fee2e2;
  color:#b91c1c;
  border:1px solid #fca5a5;
  padding:6px 12px;
  border-radius:8px;
  font-size:11.5px;
  font-weight:700;
}
.btn-danger.active{background:#ef4444;color:#fff;border-color:#dc2626;animation:pulse 1s infinite;}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.7; }
  100% { opacity: 1; }
}

/* Info Strip */
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
.dashboard-bottom-grid{
  display:grid;
  grid-template-columns: 1fr 1.2fr 0.9fr;
  gap:16px;
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

/* Map Overlay Legend */
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

/* Controls Bar */
.map-controls-bar{
  display:flex;
  justify-content:space-between;
  align-items:center;
  margin-top:10px;
  gap:8px;
  flex-wrap:wrap;
}

/* Timeline Controls */
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
.timeline-slider{
  flex:1;
  accent-color:#2563eb;
  cursor:pointer;
}
.time-badge{
  background:#2563eb;
  color:#fff;
  font-weight:800;
  font-size:12px;
  padding:4px 10px;
  border-radius:20px;
  min-width:70px;
  text-align:center;
}

/* History Toolbar */
.history-bar{
  background:#f8fafc;
  border:1px solid #e2e8f0;
  padding:8px 12px;
  border-radius:10px;
  margin-bottom:12px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  font-size:12px;
}
.history-select{
  padding:4px 8px;
  border:1px solid #cbd5e1;
  border-radius:6px;
  font-size:11.5px;
  font-weight:700;
  background:#fff;
  color:#0f172a;
}

/* Score Table */
.score-tbl{width:100%;border-collapse:collapse;font-size:12px;margin-bottom:12px;}
.score-tbl th,.score-tbl td{padding:8px 6px;text-align:left;border-bottom:1px solid #f1f5f9;}
.score-tbl th{color:#64748b;font-weight:700;font-size:11px;}
.grade-badge{
  padding:2px 8px;
  border-radius:10px;
  font-weight:800;
  font-size:10.5px;
  display:inline-block;
}
.gb-excel{background:#dcfce7;color:#15803d;}
.gb-good{background:#e0f2fe;color:#0369a1;}
.gb-warn{background:#fef3c7;color:#b45309;}

/* AI Recommendations list */
.ai-recom-list{
  list-style:none;
  display:flex;
  flex-direction:column;
  gap:8px;
  font-size:11.5px;
  color:#334155;
}
.ai-recom-list li{
  display:flex;
  align-items:flex-start;
  gap:6px;
  line-height:1.4;
  background:#f8fafc;
  padding:8px 10px;
  border-radius:8px;
  border:1px solid #f1f5f9;
}
.ai-recom-list li::before{
  content:"✔";
  color:#10b981;
  font-weight:900;
}

/* Compare Box */
.compare-grid{
  display:grid;
  grid-template-columns:1fr 20px 1fr;
  align-items:center;
  gap:8px;
  background:#f8fafc;
  padding:12px;
  border-radius:12px;
  border:1px solid #e2e8f0;
}
.comp-col h5{font-size:11px;color:#64748b;margin-bottom:6px;font-weight:700;}
.comp-val{display:flex;justify-content:space-between;font-size:11.5px;font-weight:700;margin-bottom:4px;}
.text-red{color:#ef4444;}
.text-green{color:#10b981;}

/* Main Dashboard Inline AI Assistant Box */
.main-ai-assistant{
  background:linear-gradient(135deg, #f8fafc, #eff6ff);
  border:1.5px solid #bfdbfe;
  border-radius:16px;
  padding:16px;
  margin-bottom:16px;
  box-shadow:0 2px 8px rgba(37,99,235,0.05);
}
.main-ai-header{
  display:flex;
  align-items:center;
  gap:8px;
  font-size:14px;
  font-weight:800;
  color:#1e3a8a;
  margin-bottom:10px;
}
.main-ai-chatbox{
  background:#ffffff;
  border:1px solid #cbd5e1;
  border-radius:10px;
  padding:10px 12px;
  height:100px;
  overflow-y:auto;
  font-size:12px;
  margin-bottom:10px;
  display:flex;
  flex-direction:column;
  gap:6px;
}
.chat-msg-ai{
  background:#eff6ff;
  color:#1e40af;
  padding:6px 10px;
  border-radius:8px;
  align-self:flex-start;
  max-width:85%;
  line-height:1.4;
}
.chat-msg-user{
  background:#2563eb;
  color:#ffffff;
  padding:6px 10px;
  border-radius:8px;
  align-self:flex-end;
  max-width:85%;
  line-height:1.4;
}
.main-ai-inputgroup{
  display:flex;
  gap:8px;
}
.main-ai-inputgroup input{
  flex:1;
  padding:8px 12px;
  border:1px solid #cbd5e1;
  border-radius:8px;
  font-size:12px;
  outline:none;
}
.main-ai-inputgroup input:focus{
  border-color:#2563eb;
  box-shadow:0 0 0 2px rgba(37,99,235,0.15);
}

/* Workflow Steps */
.wf-container{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:4px;
  margin-top:6px;
}
.wf-card{
  flex:1;
  background:#f8fafc;
  border:1px solid #e2e8f0;
  padding:8px 4px;
  border-radius:8px;
  text-align:center;
}
.wf-card .wf-icon{font-size:14px;margin-bottom:2px;}
.wf-card .wf-title{font-size:10px;font-weight:800;color:#1e293b;}
.wf-arrow{color:#cbd5e1;font-weight:900;font-size:11px;}

.wf-sub-tags{
  display:flex;
  justify-content:space-between;
  gap:4px;
  margin-top:8px;
}
.wf-tag{
  flex:1;
  background:#eff6ff;
  color:#2563eb;
  font-size:9.5px;
  font-weight:700;
  text-align:center;
  padding:4px 2px;
  border-radius:6px;
}

/* Report Summary Panel */
.report-sum-box{
  background:#eff6ff;
  border:1px solid #bfdbfe;
  border-radius:10px;
  padding:10px;
  font-size:11.5px;
  color:#1e3a8a;
  line-height:1.4;
  margin-bottom:10px;
}

/* Modals */
.modal-bg{
  position:fixed;
  inset:0;
  background:rgba(15,23,42,0.65);
  backdrop-filter:blur(5px);
  z-index:999;
  display:none;
  place-items:center;
  padding:20px;
}
.modal-bg.active{display:grid;}
.modal-content{
  background:#ffffff;
  width:min(95%, 880px);
  max-height:85vh;
  border-radius:20px;
  padding:28px;
  box-shadow:0 20px 40px rgba(0,0,0,0.2);
  display:flex;
  flex-direction:column;
  overflow:hidden;
}
.modal-body{flex:1;overflow-y:auto;padding-right:6px;display:flex;flex-direction:column;gap:18px;}
</style>
</head>
<body>

<div class="app-container">

  <!-- SIDEBAR -->
  <aside class="sidebar">
    <div class="brand">
      <div class="brand-icon">✦</div>
      <div>
        <div class="brand-title">Event On</div>
        <div class="brand-sub">AI 기반 행사 설계 플랫폼</div>
      </div>
    </div>

    <nav class="nav-group">
      <div class="nav-item" onclick="switchPage('home', this)">
        <span class="nav-icon">🏠</span> 홈 / 조건 입력
      </div>
      <div class="nav-item active" onclick="switchPage('design', this)">
        <span class="nav-icon">📋</span> 행사 설계 메인
      </div>
      <div class="nav-item" onclick="switchPage('process', this)">
        <span class="nav-icon">⚙️</span> 설계 프로세스
      </div>
      <div class="nav-item" onclick="openReportModal()">
        <span class="nav-icon">📊</span> 비전 설계 리포트
      </div>
    </nav>

    <div class="side-banner">
      <h5>AI 지도 생성기</h5>
      <p>AI가 만든 지도, 더 빠르고 효율적인 행사 운영을 지원합니다.</p>
    </div>

    <div class="side-profile">
      <div class="side-avatar">운</div>
      <div class="side-user-info">
        <div class="side-user-name" id="sideUserName">운영자님</div>
        <button class="side-user-btn" onclick="openAuthModal()">로그아웃</button>
      </div>
    </div>
  </aside>

  <!-- MAIN CONTENT -->
  <main class="main-content">

    <!-- Top Header -->
    <header class="top-header">
      <div class="top-title">
        <h2 id="topTitleText">📋 행사 설계 메인</h2>
        <p id="topSubText">실시간 AI 지능형 행사장 최적화 및 동선 분석 시스템입니다.</p>
      </div>
      <button class="btn-primary" onclick="runAIGenerate()">
        ✦ AI 재배치 실행하기
      </button>
    </header>

    <!-- PAGE 1: HOME / FORM -->
    <section id="pageHome" class="page-view">
      <div class="form-card">
        <div class="form-section-head">📝 행사 기본 정보 및 상세 요구사항 설정</div>
        <div class="form-grid">
          <div class="form-group">
            <label>📌 행사명</label>
            <input type="text" id="inEventName" value="2026 서울 스마트 시티 페스티벌">
          </div>
          <div class="form-group">
            <label>🏞️ 행사장 유형</label>
            <select id="inVenueType">
              <option value="야외" selected>야외 잔디 광장</option>
              <option value="실내 컨벤션">실내 컨벤션 홀</option>
              <option value="체육관">실내 체육관</option>
              <option value="도심 거리">도심 스트리트/광장</option>
            </select>
          </div>
          <div class="form-group">
            <label>📍 행사장 위치</label>
            <input type="text" id="inLocation" value="여의도 한강공원 이벤트광장">
          </div>
          <div class="form-group">
            <label>👥 예상 관람객 수</label>
            <select id="inVisitors">
              <option value="1,000명">1,000명</option>
              <option value="3,000명">3,000명</option>
              <option value="5,000명" selected>5,000명</option>
              <option value="10,000명">10,000명 이상</option>
            </select>
          </div>
          <div class="form-group">
            <label>📐 행사장 면적</label>
            <input type="text" id="inArea" value="50,000m²">
          </div>
          <div class="form-group">
            <label>⏰ 운영 시간</label>
            <input type="text" id="inTime" value="10시 - 20시">
          </div>
          <div class="form-group">
            <label>🎯 주 타겟 연령대</label>
            <select id="inTargetAge">
              <option value="올댓/전 연령층" selected>올댓 / 전 연령층</option>
              <option value="10~20대 청소년">10~20대 청소년 및 대학생</option>
              <option value="30~40대 가족">30~40대 가족 단위</option>
              <option value="50대 이상">50대 이상 시니어</option>
            </select>
          </div>
          <div class="form-group">
            <label>🎪 행사 성격 / 컨셉</label>
            <select id="inCategory">
              <option value="휴식/힐링" selected>휴식 & 힐링 페스티벌</option>
              <option value="학술/박람회">학술 & 산업 박람회</option>
              <option value="음악/공연">음악 & 대형 공연</option>
              <option value="플리마켓/체험">체험 & 플리마켓</option>
            </select>
          </div>
          <div class="form-group">
            <label>🎫 입장료 정책</label>
            <input type="text" id="inTicket" value="무료">
          </div>
          <div class="form-group">
            <label>💰 예산 규모</label>
            <input type="text" id="inBudget" value="15,000만원">
          </div>
          <div class="form-group">
            <label>🚪 출입구 / 비상구 수</label>
            <select id="inGates">
              <option value="2개 (주출입구+비상구)">2개 (주출입구 + 비상구)</option>
              <option value="4개 (동서남북)" selected>4개 (동서남북 사방 출입)</option>
              <option value="6개 이상">6개 이상 (대형 관람객용)</option>
            </select>
          </div>
          <div class="form-group">
            <label>🏥 필수 안전/의료 구역</label>
            <select id="inSafetyReq">
              <option value="입구 근처 전진배치" selected>입구 근처 전진 배치 (골든타임 확보)</option>
              <option value="중앙 분산 배치">중앙 분산 배치</option>
              <option value="음향/무대 주변">무대 및 메인 관람구역 집중</option>
            </select>
          </div>
          <div class="form-group" style="grid-column:1 / -1;">
            <label>💬 AI 공간 배치 세부 프롬프트 / 요구사항 (원하는 부스 입력)</label>
            <textarea id="inPrompt" rows="3">친환경 굿즈 팝업스토어, 푸드트럭존, 포토존을 포함하여 메인 무대는 중앙 상단에 배치하고, Central Lawn 주변으로 부스들을 원형으로 둘러싸 배치해주세요. 응급 의료센터는 접근성이 좋은 위치에 배치하여 비상시 이송을 최적화하세요.</textarea>
          </div>
        </div>
        <div style="display:flex;justify-content:flex-end;">
          <button class="btn-primary" onclick="runAIGenerate()">
            ✦ 입력 정보 기반 AI 설계 생성
          </button>
        </div>
      </div>
    </section>

    <!-- PAGE 2: DESIGN DASHBOARD (MAIN PAGE) -->
    <section id="pageDesign" class="page-view active">

      <!-- MAIN PAGE INLINE AI ASSISTANT PANEL -->
      <div class="main-ai-assistant">
        <div class="main-ai-header">
          <span>🤖 AI 메인 어시스턴트 (실시간 레이아웃 제어)</span>
          <span style="font-size:11px;color:#3b82f6;font-weight:600;">— 실시간 명령어를 통해 배치도를 즉시 재구성할 수 있습니다.</span>
        </div>
        <div class="main-ai-chatbox" id="mainAiChatBox">
          <div class="chat-msg-ai">
            안녕하세요 운영자님! 원하시는 부스 추가나 배치 수정 사항을 말씀해 주시면 즉시 반영하여 새로운 최적안을 설계합니다[cite: 1].
          </div>
        </div>
        <div class="main-ai-inputgroup">
          <input type="text" id="mainAiInput" placeholder="예: 굿즈 팝업스토어를 추가하고 응급 부스를 중앙 통로 근처로 배치해줘" onkeypress="if(event.key==='Enter') sendMainAiMsg()">
          <button class="btn-primary" style="padding:8px 16px;font-size:12px;" onclick="sendMainAiMsg()">보내기</button>
        </div>
      </div>

      <!-- History Bar -->
      <div class="history-bar">
        <div style="display:flex;align-items:center;gap:8px;">
          <span>📜 <b>설계 히스토리 (기록):</b></span>
          <select id="historySelect" class="history-select" onchange="loadSelectedHistory(this.value)">
            <!-- Dynamic Options -->
          </select>
        </div>
        <span id="historyStatusBadge" style="font-size:11px;color:#2563eb;font-weight:700;">현재 버전: v1 (기본 설계안)</span>
      </div>

      <!-- Time-based Simulation Controller -->
      <div class="timeline-container">
        <span style="font-size:12px;font-weight:800;color:#0f172a;display:flex;align-items:center;gap:4px;">
          ⏰ <b>시간별 관람객 시뮬레이션:</b>
        </span>
        <button class="btn-secondary" id="btnTimelinePlay" onclick="toggleTimelinePlay()">▶ 시간 재생</button>
        <input type="range" id="timeSlider" class="timeline-slider" min="10" max="20" step="1" value="14" oninput="updateTimeSimulation(this.value)">
        <div class="time-badge" id="timeDisplay">14:00</div>
        <span style="font-size:11px;color:#64748b;font-weight:600;" id="timeDesc">관람 인원 피크 타임 (공연 및 체험)</span>
      </div>

      <!-- Top Header Strip -->
      <div class="info-strip">
        <div class="info-strip-group">
          <div class="info-box">
            <div class="info-box-icon">📌</div>
            <div class="info-box-text"><label>행사명</label><span id="outEventName">2026 서울 스마트 시티 페스티벌</span></div>
          </div>
          <div class="info-box">
            <div class="info-box-icon">🏞️</div>
            <div class="info-box-text"><label>행사장 유형</label><span id="outVenueType">야외</span></div>
          </div>
          <div class="info-box">
            <div class="info-box-icon">📍</div>
            <div class="info-box-text"><label>행사장 위치</label><span id="outLocation">여의도 한강공원 이벤트광장</span></div>
          </div>
          <div class="info-box">
            <div class="info-box-icon">👥</div>
            <div class="info-box-text"><label>예상 관람객</label><span id="outVisitors">5,000명</span></div>
          </div>
          <div class="info-box">
            <div class="info-box-icon">📐</div>
            <div class="info-box-text"><label>행사장 면적</label><span id="outArea">50,000m²</span></div>
          </div>
          <div class="info-box">
            <div class="info-box-icon">⏰</div>
            <div class="info-box-text"><label>운영 시간</label><span id="outTime">10시 - 20시</span></div>
          </div>
          <div class="info-box">
            <div class="info-box-icon">🎯</div>
            <div class="info-box-text"><label>관람객 연령대</label><span id="outAge">올댓 / 전 연령층</span></div>
          </div>
          <div class="info-box">
            <div class="info-box-icon">🎪</div>
            <div class="info-box-text"><label>행사 성격</label><span id="outCategory">휴식</span></div>
          </div>
        </div>
      </div>

      <!-- Main Dashboard Grid -->
      <div class="dashboard-main-grid" style="margin-top:14px;">

        <!-- 1. Digital Twin Canvas Map (2D & 3D Supported) -->
        <div class="card-panel">
          <div class="card-head">
            <span>🗺️ 행사장 배치도 (디지털 트윈 렌더링)</span>
            <div style="display:flex;gap:6px;align-items:center;">
              <button class="btn-secondary" id="btnToggle3D" onclick="toggle3DView()">🧊 3D 입체뷰 보기</button>
              <span class="card-badge" id="layoutBadge">v1.0 AI 설계</span>
            </div>
          </div>

          <div class="map-wrap" id="mapWrap">
            <canvas id="venueCanvas"></canvas>
            <canvas id="peopleCanvas"></canvas>
            <div id="container3D"></div>

            <!-- Legend -->
            <div class="map-legend-overlay">
              <div class="legend-item"><span class="legend-dot" style="background:#8b5cf6;"></span> 무대존</div>
              <div class="legend-item"><span class="legend-dot" style="background:#3b82f6;"></span> 체험존</div>
              <div class="legend-item"><span class="legend-dot" style="background:#f59e0b;"></span> 푸드존</div>
              <div class="legend-item"><span class="legend-dot" style="background:#10b981;"></span> 휴식공간</div>
              <div class="legend-item"><span class="legend-dot" style="background:#ef4444;"></span> 응급의료</div>
              <div class="legend-item"><span class="legend-dot" style="background:#06b6d4;"></span> 화장실</div>
              <div class="legend-item"><span class="legend-dot" style="background:#64748b;"></span> 출입구</div>
            </div>
          </div>

          <div class="map-controls-bar">
            <div style="display:flex;gap:6px;">
              <button class="btn-secondary" id="btnToggleSim" onclick="toggleSim()">
                ▶ 시뮬레이션 시작
              </button>
              <button class="btn-warning" id="btnRain" onclick="toggleRainEnv()">
                🌧️ 우천 모드
              </button>
              <button class="btn-danger" id="btnEmergency" onclick="triggerEmergencyEnv()">
                🚨 응급환자 발생 (의료부스 후송)
              </button>
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

        <!-- 3. AI Evaluation & Suggestions -->
        <div class="card-panel">
          <div class="card-head">
            <span>💡 AI 평가 결과 & XAI</span>
          </div>
          <table class="score-tbl">
            <thead>
              <tr><th>평가 항목</th><th>점수</th><th>등급</th></tr>
            </thead>
            <tbody id="evalScoreTable">
              <tr><td>비상 안전성</td><td id="scSafety">92점</td><td><span class="grade-badge gb-excel" id="gbSafety">매우 우수</span></td></tr>
              <tr><td>동선 효율성</td><td id="scFlow">87점</td><td><span class="grade-badge gb-good" id="gbFlow">우수</span></td></tr>
              <tr><td>접근성</td><td id="scAccess">96점</td><td><span class="grade-badge gb-excel" id="gbAccess">매우 우수</span></td></tr>
              <tr><td>혼잡도 분산</td><td id="scCong">84점</td><td><span class="grade-badge gb-good" id="gbCong">우수</span></td></tr>
              <tr><td>공간 활용성</td><td id="scSpace">88점</td><td><span class="grade-badge gb-good" id="gbSpace">우수</span></td></tr>
            </tbody>
          </table>

          <div style="font-size:12px;font-weight:800;color:#0f172a;margin:10px 0 6px 0;">🧠 XAI (설명 가능한 AI) 설계 이유</div>
          <ul class="ai-recom-list" id="aiRecomList">
            <li><b>응급 의료 센터 위치 선정:</b> 출입구 및 메인 무대에서 반경 30m 이내에 배치하여 응급 상황 시 골든타임(3분 이내) 확보</li>
            <li><b>푸드존과 휴게공간 분산:</b> 취식으로 인한 밀집도를 낮추기 위해 메인 무대와 대각선 방향 이격 배치</li>
            <li><b>군중 동선 최적화:</b> 방문객 이동 동선이 겹치지 않도록 일방통행 로드 설계 반영</li>
            <li>사용자 맞춤형 부스(팝업스토어 등) 실시간 최적 좌표 자동 연산 완료</li>
          </ul>
        </div>

      </div>

      <!-- Bottom Dashboard Grid -->
      <div class="dashboard-bottom-grid" style="margin-top:14px;">

        <!-- 1. Before / After Comparison -->
        <div class="card-panel">
          <div class="card-head">
            <span>⚖️ 설계 전 / 후 비교</span>
          </div>
          <div class="compare-grid">
            <div class="comp-col">
              <h5>AI 설계 전 (기존)</h5>
              <div class="comp-val"><span>평균 대기 시간</span><span class="text-red">25분</span></div>
              <div class="comp-val"><span>비상 탈출 시간</span><span>8분 30초</span></div>
              <div class="comp-val"><span>공간 활용률</span><span class="text-red">65%</span></div>
            </div>
            <div style="text-align:center;font-weight:900;color:#cbd5e1;">→</div>
            <div class="comp-col">
              <h5>AI 최적화 설계</h5>
              <div class="comp-val"><span>평균 대기 시간</span><span class="text-green">10분</span></div>
              <div class="comp-val"><span>비상 탈출 시간</span><span class="text-green">4분 15초</span></div>
              <div class="comp-val"><span>공간 활용률</span><span class="text-green">92%</span></div>
            </div>
          </div>
        </div>

        <!-- 2. AI Workflow Process -->
        <div class="card-panel">
          <div class="card-head">
            <span>⚙️ AI 행사 설계 프로세스 (Workflow)</span>
          </div>
          <div class="wf-container">
            <div class="wf-card"><div class="wf-icon">📋</div><div class="wf-title">행사 정보 입력</div></div>
            <span class="wf-arrow">›</span>
            <div class="wf-card"><div class="wf-icon">🌐</div><div class="wf-title">디지털 트윈 생성</div></div>
            <span class="wf-arrow">›</span>
            <div class="wf-card"><div class="wf-icon">🤖</div><div class="wf-title">수천개 배치안 시뮬</div></div>
            <span class="wf-arrow">›</span>
            <div class="wf-card"><div class="wf-icon">🚑</div><div class="wf-title">XAI 최적안 도출</div></div>
            <span class="wf-card"><div class="wf-icon">📄</div><div class="wf-title">리포트 출력</div></div>
          </div>
          <div class="wf-sub-tags">
            <span class="wf-tag">다목적 최적화</span>
            <span class="wf-tag">군중 동선 예측</span>
            <span class="wf-tag">설명 가능한 AI</span>
          </div>
        </div>

        <!-- 3. Report Summary -->
        <div class="card-panel">
          <div class="card-head">
            <span>📄 분석 리포트 요약</span>
          </div>
          <div class="report-sum-box" id="reportSummaryBox">
            AI 분석 결과, <b>2026 서울 스마트 시티 페스티벌</b>은 맞춤형 부스 요구사항 및 군중 밀집도 시뮬레이션을 거쳐 최적의 안전성과 효율성을 확보했습니다[cite: 1].
          </div>
          <button class="btn-primary" style="width:100%;justify-content:center;padding:10px;font-size:12px;margin-top:auto;" onclick="openReportModal()">
            📌 최종 설계안 다운로드 (PDF)
          </button>
        </div>

      </div>

    </section>

    <!-- PAGE 3: PROCESS -->
    <section id="pageProcess" class="page-view">
      <div class="form-card">
        <div class="form-section-head">⚙️ AI 행사 공간 설계 및 멀티오브젝티브 최적화 메커니즘</div>
        <p style="font-size:13px;line-height:1.7;color:#334155;">
          1. <b>정보 입력 및 NLP 분석:</b> 예산, 목적, 방문객 수 및 사용자가 직접 입력한 커스텀 부스 요구사항을 자연어 처리 엔진으로 분석합니다.<br>
          2. <b>디지털 트윈 환경 생성:</b> 선택된 장소의 지형 데이터를 기반으로 가상 공간(디지털 트윈)을 구축합니다.<br>
          3. <b>다목적 최적화 및 군중 시뮬레이션:</b> 수천 개의 배치안 중 병목 현상을 최소화하고 안전 거리를 확보하는 최적의 배치를 산출합니다.<br>
          4. <b>XAI 및 실시간 피드백:</b> AI가 해당 배치를 도출한 이유를 명확히 제시하며, 메인 어시스턴트를 통해 실시간 레이아웃 수정이 가능합니다.
        </p>
      </div>
    </section>

  </main>
</div>

<!-- DETAILED PDF REPORT MODAL -->
<div class="modal-bg" id="reportModal">
  <div class="modal-content">
    <div style="display:flex;justify-content:space-between;align-items:center;padding-bottom:12px;border-bottom:2px solid #f1f5f9;margin-bottom:16px;">
      <h3 style="font-size:18px;font-weight:800;color:#0f172a;">📊 AI 행사장 종합 최적화 상세 보고서 (XAI 리포트)</h3>
      <button onclick="closeReportModal()" style="border:none;background:none;font-size:20px;font-weight:800;color:#64748b;">✕</button>
    </div>

    <div class="modal-body">
      <div style="background:#f8fafc;padding:16px;border-radius:12px;border:1px solid #e2e8f0;">
        <h4 style="font-size:14px;font-weight:800;margin-bottom:8px;color:#1e293b;">1. 종합 평가 요약</h4>
        <p style="font-size:12.5px;color:#334155;line-height:1.6;" id="modalSummaryText">
          본 보고서는 <b>2026 서울 스마트 시티 페스티벌</b>의 AI 멀티오브젝티브 최적화 설계 결과입니다. 종합 안전성 점수 <b>92점</b>을 기록하였으며, 사용자 맞춤 부스 배치가 완벽하게 반영되었습니다.
        </p>
      </div>

      <div style="background:#f8fafc;padding:16px;border-radius:12px;border:1px solid #e2e8f0;">
        <h4 style="font-size:14px;font-weight:800;margin-bottom:8px;color:#1e293b;">2. XAI 설계 근거</h4>
        <ul style="font-size:12px;color:#334155;line-height:1.7;padding-left:18px;">
          <li><b>응급 의료 센터:</b> 메인 무대 및 출입구에서 반경 30m 이내 배치로 골든타임 3분 이내 확보.</li>
          <li><b>맞춤 부스 배치:</b> 운영자가 요청한 팝업스토어 및 푸드트럭존을 동선 분산형으로 최적 배치 완료.</li>
        </ul>
      </div>
    </div>

    <div style="margin-top:16px;display:flex;justify-content:flex-end;gap:10px;">
      <button style="padding:10px 16px;background:#e2e8f0;border:none;border-radius:8px;font-weight:700;font-size:12px;" onclick="closeReportModal()">닫기</button>
      <button class="btn-primary" onclick="alert('설계 리포트 PDF가 다운로드되었습니다.');closeReportModal();">PDF 다운로드</button>
    </div>
  </div>
</div>

<script>
/* Navigation Switching */
function switchPage(pageId, el){
  document.querySelectorAll('.page-view').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));

  if(el) el.classList.add('active');

  const t = document.getElementById('topTitleText');
  const s = document.getElementById('topSubText');

  if(pageId === 'home'){
    document.getElementById('pageHome').classList.add('active');
    t.textContent = '📝 행사 조건 입력';
    s.textContent = '상세 기본 정보 및 요구사항을 입력하시면 AI가 자동 설계합니다.';
  } else if(pageId === 'design'){
    document.getElementById('pageDesign').classList.add('active');
    t.textContent = '📋 행사 설계 메인';
    s.textContent = '실시간 AI 지능형 행사장 최적화 및 동선 분석 시스템입니다.';
    setTimeout(initCanvases, 50);
  } else if(pageId === 'process'){
    document.getElementById('pageProcess').classList.add('active');
    t.textContent = '⚙️ 설계 프로세스';
    s.textContent = 'AI 멀티오브젝티브 최적화 및 디지털 트윈 시뮬레이션 메커니즘입니다.';
  }
}

function openReportModal(){ document.getElementById('reportModal').classList.add('active'); }
function closeReportModal(){ document.getElementById('reportModal').classList.remove('active'); }
function openAuthModal(){ alert('로그아웃 되었습니다.'); }

/* APP STATE & BLUEPRINT HISTORY SYSTEM */
let layoutHistory = [];
let currentLayoutIndex = -1;

const layoutPresets = [
  {
    versionName: "v1.0 - 기본 최적안",
    timestamp: "기본",
    booths: {
      stage: {x: 0.38, y: 0.08, bw: 0.24, bh: 0.16, title: '메인 무대', color: '#8b5cf6', icon: '🎭'},
      popup: {x: 0.12, y: 0.22, bw: 0.16, bh: 0.14, title: '친환경 굿즈샵', color: '#3b82f6', icon: '🛍️'},
      photo: {x: 0.72, y: 0.22, bw: 0.16, bh: 0.14, title: '포토존', color: '#3b82f6', icon: '📸'},
      food: {x: 0.10, y: 0.48, bw: 0.16, bh: 0.15, title: '푸드트럭존', color: '#f59e0b', icon: '🍔'},
      medical: {x: 0.72, y: 0.48, bw: 0.16, bh: 0.14, title: '응급 의료센터', color: '#ef4444', icon: '🏥'},
      restroom: {x: 0.72, y: 0.70, bw: 0.14, bh: 0.12, title: '안내센터/화장실', color: '#06b6d4', icon: 'ℹ️'}
    },
    scores: { safety: 92, flow: 87, access: 96, cong: 84, space: 88 }
  },
  {
    versionName: "v2.0 - 맞춤 부스 최적화안",
    timestamp: "AI 추천",
    booths: {
      stage: {x: 0.35, y: 0.08, bw: 0.30, bh: 0.18, title: '메인 대형무대', color: '#8b5cf6', icon: '🎪'},
      popup: {x: 0.08, y: 0.25, bw: 0.20, bh: 0.14, title: '친환경 굿즈샵', color: '#3b82f6', icon: '🛍️'},
      photo: {x: 0.72, y: 0.25, bw: 0.20, bh: 0.14, title: '포토존', color: '#3b82f6', icon: '📸'},
      food: {x: 0.08, y: 0.55, bw: 0.20, bh: 0.15, title: '푸드트럭존', color: '#f59e0b', icon: '🍔'},
      medical: {x: 0.42, y: 0.52, bw: 0.16, bh: 0.14, title: '응급 의료센터 (중앙)', color: '#ef4444', icon: '🏥'},
      restroom: {x: 0.75, y: 0.72, bw: 0.16, bh: 0.12, title: '안내센터', color: '#06b6d4', icon: 'ℹ️'}
    },
    scores: { safety: 98, flow: 91, access: 94, cong: 90, space: 85 }
  }
];

function initLayoutHistory() {
  if (layoutHistory.length === 0) {
    layoutHistory.push(JSON.parse(JSON.stringify(layoutPresets[0])));
    currentLayoutIndex = 0;
    updateHistorySelectUI();
  }
}

function updateHistorySelectUI() {
  const sel = document.getElementById('historySelect');
  if(!sel) return;
  sel.innerHTML = '';
  layoutHistory.forEach((ly, idx) => {
    const opt = document.createElement('option');
    opt.value = idx;
    opt.textContent = `${ly.versionName} (${ly.timestamp})`;
    if (idx === currentLayoutIndex) opt.selected = true;
    sel.appendChild(opt);
  });
  document.getElementById('historyStatusBadge').textContent = `현재 버전: ${layoutHistory[currentLayoutIndex].versionName}`;
}

function loadSelectedHistory(index) {
  currentLayoutIndex = parseInt(index);
  const layout = layoutHistory[currentLayoutIndex];

  document.getElementById('layoutBadge').textContent = layout.versionName;
  document.getElementById('historyStatusBadge').textContent = `현재 버전: ${layout.versionName}`;

  document.getElementById('scSafety').textContent = layout.scores.safety + '점';
  document.getElementById('scFlow').textContent = layout.scores.flow + '점';
  document.getElementById('scAccess').textContent = layout.scores.access + '점';
  document.getElementById('scCong').textContent = layout.scores.cong + '점';
  document.getElementById('scSpace').textContent = layout.scores.space + '점';

  if (venueCanvas) {
    drawDetailedOutdoorVenue(venueCanvas.width, venueCanvas.height);
  }
  if (is3DActive) {
    update3DScene();
  }
}

function runAIGenerate(customTitle){
  initLayoutHistory();

  const nextPresetIndex = layoutHistory.length % layoutPresets.length;
  const newLayout = JSON.parse(JSON.stringify(layoutPresets[nextPresetIndex]));

  const d = new Date();
  const timeStr = `${d.getHours()}:${d.getMinutes() < 10 ? '0' : ''}${d.getMinutes()}`;
  newLayout.versionName = customTitle || `v${layoutHistory.length + 1}.0 - AI 최적 재배치안`;
  newLayout.timestamp = timeStr;

  layoutHistory.push(newLayout);
  currentLayoutIndex = layoutHistory.length - 1;

  updateHistorySelectUI();
  loadSelectedHistory(currentLayoutIndex);

  if(!document.getElementById('pageDesign').classList.contains('active')){
    switchPage('design', document.querySelectorAll('.nav-item')[1]);
  }
}

/* MAIN PAGE AI CHAT ASSISTANT */
function sendMainAiMsg(){
  const input = document.getElementById('mainAiInput');
  const txt = input.value.trim();
  if(!txt) return;

  const chatBox = document.getElementById('mainAiChatBox');
  chatBox.innerHTML += `<div class="chat-msg-user"><b>나:</b> ${txt}</div>`;
  input.value = '';
  chatBox.scrollTop = chatBox.scrollHeight;

  setTimeout(() => {
    chatBox.innerHTML += `<div class="chat-msg-ai"><b>AI:</b> 요청하신 "${txt}" 내용을 반영하여 디지털 트윈 배치도를 새롭게 설계하고 XAI 분석 결과를 갱신했습니다[cite: 1].</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
    runAIGenerate(`v${layoutHistory.length + 1}.0 - 사용자 맞춤 재배치`);
  }, 600);
}

/* TIME-BASED SIMULATION SYSTEM */
let timeInterval = null;
let currentTime = 14;

function updateTimeSimulation(timeVal) {
  currentTime = parseInt(timeVal);
  document.getElementById('timeDisplay').textContent = `${currentTime}:00`;

  const desc = document.getElementById('timeDesc');
  if (currentTime >= 10 && currentTime < 12) {
    desc.textContent = '개장 초반 - 관람객 순차 입장 (여유)';
    setCrowdDensityFactor(0.5);
  } else if (currentTime >= 12 && currentTime < 15) {
    desc.textContent = '피크 타임 - 푸드존 및 공연 관람객 집중 (혼잡)';
    setCrowdDensityFactor(1.5);
  } else if (currentTime >= 15 && currentTime < 18) {
    desc.textContent = '오후 시간대 - 체험부스 및 휴게공간 분산';
    setCrowdDensityFactor(1.0);
  } else {
    desc.textContent = '야간 폐장 전 - 메인 무대 집중 및 퇴장';
    setCrowdDensityFactor(1.2);
  }
}

function setCrowdDensityFactor(factor) {
  if(!venueCanvas) return;
  const targetCount = Math.floor(70 * factor);
  if (people.length < targetCount) {
    const w = venueCanvas.width;
    const h = venueCanvas.height;
    for(let i = people.length; i < targetCount; i++){
      people.push({
        x: w*0.1 + Math.random()*w*0.8,
        y: h*0.15 + Math.random()*h*0.7,
        vx: (Math.random()-0.5)*1.5,
        vy: (Math.random()-0.5)*1.5,
        targetX: Math.random()*w,
        targetY: Math.random()*h,
        speed: 0.8 + Math.random()*0.8
      });
    }
  } else if (people.length > targetCount) {
    people = people.slice(0, targetCount);
  }
}

function toggleTimelinePlay() {
  const btn = document.getElementById('btnTimelinePlay');
  if (timeInterval) {
    clearInterval(timeInterval);
    timeInterval = null;
    btn.textContent = '▶ 시간 재생';
  } else {
    btn.textContent = '⏸ 일시정지';
    timeInterval = setInterval(() => {
      let nextTime = currentTime + 1;
      if (nextTime > 20) nextTime = 10;
      document.getElementById('timeSlider').value = nextTime;
      updateTimeSimulation(nextTime);
    }, 2000);
  }
}

/* 2D CANVAS & SIMULATION ENGINE */
let venueCanvas, venueCtx;
let peopleCanvas, peopleCtx;
let heatmapCanvas, heatmapCtx;

let simRunning = false;
let animFrameId = null;
let isRain = false;
let isEmergency = false;
let emergencyPos = null;
let people = [];
let raindrops = [];

function initCanvases(){
  initLayoutHistory();

  venueCanvas = document.getElementById('venueCanvas');
  peopleCanvas = document.getElementById('peopleCanvas');
  heatmapCanvas = document.getElementById('heatmapCanvas');

  if(!venueCanvas) return;

  const wrap = document.getElementById('mapWrap');
  const w = wrap.clientWidth;
  const h = wrap.clientHeight;

  [venueCanvas, peopleCanvas, heatmapCanvas].forEach(c => {
    c.width = w;
    c.height = h;
  });

  venueCtx = venueCanvas.getContext('2d');
  peopleCtx = peopleCanvas.getContext('2d');
  heatmapCtx = heatmapCanvas.getContext('2d');

  initPeopleData(w, h);
  initRainData(w, h);

  loadSelectedHistory(currentLayoutIndex);

  if (!animFrameId) {
    renderLoop();
  }
}

function initPeopleData(w, h){
  people = [];
  for(let i=0; i<70; i++){
    people.push({
      x: w*0.1 + Math.random()*w*0.8,
      y: h*0.15 + Math.random()*h*0.7,
      vx: (Math.random()-0.5)*1.5,
      vy: (Math.random()-0.5)*1.5,
      targetX: Math.random()*w,
      targetY: Math.random()*h,
      speed: 0.8 + Math.random()*0.8
    });
  }
}

function initRainData(w, h){
  raindrops = [];
  for(let i=0; i<100; i++){
    raindrops.push({
      x: Math.random()*w,
      y: Math.random()*h,
      len: 8 + Math.random()*12,
      vy: 6 + Math.random()*6
    });
  }
}

function updateSimulationLogic(){
  if(!venueCanvas) return;
  const w = venueCanvas.width;
  const h = venueCanvas.height;

  const currentBooths = layoutHistory[currentLayoutIndex].booths;
  const med = currentBooths.medical;
  const medCenterX = med.x * w + med.bw * w * 0.5;
  const medCenterY = med.y * h + med.bh * h * 0.5;

  if (isEmergency && emergencyPos) {
    const dx = medCenterX - emergencyPos.x;
    const dy = medCenterY - emergencyPos.y;
    const dist = Math.sqrt(dx*dx + dy*dy);

    if (dist > 8) {
      emergencyPos.x += (dx / dist) * 2.8;
      emergencyPos.y += (dy / dist) * 2.8;
    }
  }

  people.forEach(p => {
    if (isRain) {
      const stage = currentBooths.stage;
      const targetX = stage.x * w + stage.bw * w * 0.5;
      const targetY = stage.y * h + stage.bh * h * 0.5;
      p.vx += (targetX - p.x) * 0.0005;
      p.vy += (targetY - p.y) * 0.0005;
      p.speed = 2.0;
    } else {
      p.speed = 1.0;
      if (Math.random() < 0.02) {
        p.targetX = Math.random() * w;
        p.targetY = Math.random() * h;
      }
      p.vx += (p.targetX - p.x) * 0.0002;
      p.vy += (p.targetY - p.y) * 0.0002;
    }

    p.x += p.vx;
    p.y += p.vy;

    if(p.x < 15) { p.x = 15; p.vx *= -1; }
    if(p.x > w-15) { p.x = w-15; p.vx *= -1; }
    if(p.y < 15) { p.y = 15; p.vy *= -1; }
    if(p.y > h-15) { p.y = h-15; p.vy *= -1; }
  });

  if (isRain) {
    raindrops.forEach(r => {
      r.y += r.vy;
      r.x -= 1;
      if (r.y > h) { r.y = 0; r.x = Math.random() * w; }
    });
  }
}

function renderLoop(){
  if (simRunning) {
    updateSimulationLogic();
  }

  if (peopleCanvas && venueCanvas) {
    const w = venueCanvas.width;
    const h = venueCanvas.height;
    drawPeople(w, h);
    drawDynamicHeatmap(w, h);
  }

  animFrameId = requestAnimationFrame(renderLoop);
}

function drawDetailedOutdoorVenue(w, h){
  if(!venueCtx || currentLayoutIndex < 0) return;
  const currentBooths = layoutHistory[currentLayoutIndex].booths;

  venueCtx.fillStyle = isRain ? '#254e2b' : '#3a7d44';
  venueCtx.fillRect(0, 0, w, h);

  // Pedestrian Pathways
  venueCtx.strokeStyle = isRain ? '#b0a898' : '#e2d9c8';
  venueCtx.lineWidth = 26;
  venueCtx.lineCap = 'round';
  venueCtx.beginPath();
  venueCtx.moveTo(w*0.5, h*0.88);
  venueCtx.lineTo(w*0.5, h*0.5);
  venueCtx.stroke();

  // Draw Booths
  Object.keys(currentBooths).forEach(key => {
    const b = currentBooths[key];
    drawGraphicBooth(venueCtx, b.x*w, b.y*h, b.bw*w, b.bh*h, b.title, b.color, b.icon);
  });

  // Gates
  venueCtx.fillStyle = '#1e293b';
  venueCtx.fillRect(w*0.42, h*0.86, w*0.16, h*0.08);
  venueCtx.fillStyle = '#ffffff';
  venueCtx.font = 'bold 10px Pretendard, sans-serif';
  venueCtx.textAlign = 'center';
  venueCtx.fillText('🚪 주출입구', w*0.5, h*0.91);
}

function drawGraphicBooth(ctx, x, y, bw, bh, title, color, icon){
  ctx.fillStyle = 'rgba(0,0,0,0.25)';
  ctx.fillRect(x+3, y+3, bw, bh);

  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.roundRect(x, y, bw, bh, 6);
  ctx.fill();

  ctx.strokeStyle = '#ffffff';
  ctx.lineWidth = 1.5;
  ctx.stroke();

  ctx.fillStyle = '#ffffff';
  ctx.font = 'bold 10.5px Pretendard, sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText(`${icon} ${title}`, x + bw/2, y + bh/2 + 4);
}

function drawPeople(w, h){
  if(!peopleCtx) return;
  peopleCtx.clearRect(0,0,w,h);

  people.forEach(p => {
    peopleCtx.fillStyle = isRain ? '#60a5fa' : '#ffffff';
    peopleCtx.beginPath();
    peopleCtx.arc(p.x, p.y, 3.5, 0, Math.PI*2);
    peopleCtx.fill();
  });

  if (isEmergency && emergencyPos) {
    const currentBooths = layoutHistory[currentLayoutIndex].booths;
    const med = currentBooths.medical;
    const medCenterX = med.x * w + med.bw * w * 0.5;
    const medCenterY = med.y * h + med.bh * h * 0.5;

    peopleCtx.strokeStyle = '#ef4444';
    peopleCtx.lineWidth = 3;
    peopleCtx.setLineDash([6, 6]);
    peopleCtx.beginPath();
    peopleCtx.moveTo(emergencyPos.x, emergencyPos.y);
    peopleCtx.lineTo(medCenterX, medCenterY);
    peopleCtx.stroke();
    peopleCtx.setLineDash([]);

    peopleCtx.fillStyle = '#ef4444';
    peopleCtx.beginPath();
    peopleCtx.arc(emergencyPos.x, emergencyPos.y, 8, 0, Math.PI*2);
    peopleCtx.fill();
  }
}

function drawDynamicHeatmap(w, h){
  if(!heatmapCtx) return;
  heatmapCtx.clearRect(0,0,w,h);

  const grid = {};
  const gridSize = 40;

  people.forEach(p => {
    const gx = Math.floor(p.x / gridSize);
    const gy = Math.floor(p.y / gridSize);
    const key = `${gx}_${gy}`;
    grid[key] = (grid[key] || 0) + 1;
  });

  Object.keys(grid).forEach(key => {
    const [gx, gy] = key.split('_').map(Number);
    const count = grid[key];
    const cx = gx * gridSize + gridSize/2;
    const cy = gy * gridSize + gridSize/2;

    if (count >= 2) {
      let radius = count * 12;
      let alpha = Math.min(0.8, count * 0.15);
      let grad = heatmapCtx.createRadialGradient(cx, cy, 0, cx, cy, radius);
      if (count >= 5) {
        grad.addColorStop(0, `rgba(239, 68, 68, ${alpha})`);
      } else {
        grad.addColorStop(0, `rgba(245, 158, 11, ${alpha})`);
      }
      grad.addColorStop(1, 'rgba(16, 185, 129, 0)');
      heatmapCtx.fillStyle = grad;
      heatmapCtx.beginPath();
      heatmapCtx.arc(cx, cy, radius, 0, Math.PI*2);
      heatmapCtx.fill();
    }
  });
}

function toggleSim(){
  simRunning = !simRunning;
  const btn = document.getElementById('btnToggleSim');
  const timer = document.getElementById('simTimer');

  if (simRunning) {
    btn.textContent = '⏸ 시뮬레이션 일시정지';
    timer.textContent = '상태: 실시간 군중 시뮬레이션 연산 중 ▶';
  } else {
    btn.textContent = '▶ 시뮬레이션 시작';
    timer.textContent = '상태: 대기중';
  }
}

function toggleRainEnv(){
  isRain = !isRain;
  const btn = document.getElementById('btnRain');
  const badge = document.getElementById('envBadge');

  if (isRain) {
    btn.classList.add('active');
    btn.textContent = '🌧️ 우천 모드 (ON)';
    badge.textContent = '🌧️ 기상변수: 강우 발생';
  } else {
    btn.classList.remove('active');
    btn.textContent = '🌧️ 우천 모드';
    if(!isEmergency) badge.textContent = '일반 상태';
  }
  if (venueCanvas) drawDetailedOutdoorVenue(venueCanvas.width, venueCanvas.height);
}

function triggerEmergencyEnv(){
  isEmergency = !isEmergency;
  const btn = document.getElementById('btnEmergency');
  const badge = document.getElementById('envBadge');

  if (isEmergency) {
    btn.classList.add('active');
    btn.textContent = '🚨 응급상황 해제';
    badge.textContent = '🚨 응급환자 발생! 의료부스로 이송 중';

    const w = venueCanvas.width;
    const h = venueCanvas.height;
    emergencyPos = { x: w * 0.15, y: h * 0.25 };

    if(!simRunning) toggleSim();
  } else {
    btn.classList.remove('active');
    btn.textContent = '🚨 응급환자 발생 (의료부스 후송)';
    emergencyPos = null;
    if(!isRain) badge.textContent = '일반 상태';
  }
}

/* THREE.JS 3D VIEW ENGINE INTEGRATION */
let is3DActive = false;
let scene3D, camera3D, renderer3D;

function toggle3DView(){
  is3DActive = !is3DActive;
  const container3D = document.getElementById('container3D');
  const btn = document.getElementById('btnToggle3D');

  if (is3DActive) {
    container3D.style.display = 'block';
    btn.textContent = '🗺️ 2D 평면도 보기';
    init3DScene();
  } else {
    container3D.style.display = 'none';
    btn.textContent = '🧊 3D 입체뷰 보기';
  }
}

function init3DScene(){
  const container = document.getElementById('container3D');
  container.innerHTML = '';

  const w = container.clientWidth;
  const h = container.clientHeight;

  scene3D = new THREE.Scene();
  scene3D.background = new THREE.Color(0x0f172a);

  camera3D = new THREE.PerspectiveCamera(45, w / h, 0.1, 1000);
  camera3D.position.set(0, 150, 180);
  camera3D.lookAt(0, 0, 0);

  renderer3D = new THREE.WebGLRenderer({ antialias: true });
  renderer3D.setSize(w, h);
  container.appendChild(renderer3D.domElement);

  scene3D.add(new THREE.AmbientLight(0xffffff, 0.7));
  const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
  dirLight.position.set(50, 100, 50);
  scene3D.add(dirLight);

  const groundGeo = new THREE.PlaneGeometry(200, 140);
  const groundMat = new THREE.MeshLambertMaterial({ color: 0x2e7d32 });
  const ground = new THREE.Mesh(groundGeo, groundMat);
  ground.rotation.x = -Math.PI / 2;
  scene3D.add(ground);

  update3DScene();

  function animate3D() {
    if (is3DActive) {
      requestAnimationFrame(animate3D);
      scene3D.rotation.y += 0.003;
      renderer3D.render(scene3D, camera3D);
    }
  }
  animate3D();
}

function update3DScene(){
  if (!scene3D) return;

  for(let i = scene3D.children.length - 1; i >= 0; i--) {
    if(scene3D.children[i].userData.isBooth) {
      scene3D.remove(scene3D.children[i]);
    }
  }

  const currentBooths = layoutHistory[currentLayoutIndex].booths;

  Object.keys(currentBooths).forEach(key => {
    const b = currentBooths[key];
    const bw = b.bw * 200;
    const bh = b.bh * 140;
    const bx = (b.x - 0.5) * 200 + bw/2;
    const bz = (b.y - 0.5) * 140 + bh/2;

    const height = key === 'stage' ? 18 : 10;
    const geo = new THREE.BoxGeometry(bw, height, bh);
    const colorHex = parseInt(b.color.replace('#', '0x'));
    const mat = new THREE.MeshLambertMaterial({ color: colorHex });

    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.set(bx, height/2, bz);
    mesh.userData.isBooth = true;
    scene3D.add(mesh);
  });
}

window.addEventListener('load', () => {
  switchPage('design', document.querySelectorAll('.nav-item')[1]);
});
</script>
</body>
</html>
"""

components.html(EVENT_AI_HTML, height=1300, scrolling=True)
