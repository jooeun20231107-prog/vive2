# ... existing code ...
    st.divider()
    st.markdown("""
    <div style="background-color:#1e293b; color:#f8fafc; padding:14px; border-radius:10px; font-size:12px; line-height:1.5;">
        <span style="color:#60a5fa; font-weight:bold;">💡 Archisketch 스마트 가이드</span><br>
        2D/3D 도면 위에서 혼잡도 Heatmap을 바로 확인하고, 구역별 좌표 및 동선을 자유롭게 조율할 수 있습니다.
    </div>
    """, unsafe_allow_html=True)

if st.session_state.page == "home":
    st.markdown("<div style='text-align: center; padding: 20px 0 10px 0;'>", unsafe_allow_html=True)
    st.markdown("<span style='background:#eff6ff; color:#2563eb; font-weight:700; padding:6px 14px; border-radius:20px; font-size:13px;'>✨ Archisketch Smart Spatial AI Powered</span>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #0f172a; margin-top:14px; font-weight:800; font-size:36px;'>AI 기반 스마트 행사 공간 설계 플랫폼</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; font-size: 16px; max-width:700px; margin: 0 auto 35px auto;'>행사 기본 정보만 입력하면 Archisketch 기반 2D CAD 도면 설계, 실시간 혼잡도 시뮬레이션, 상사 결재용 리포트까지 원스톱으로 완성합니다.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    col_box1, col_box2 = st.columns(2)

    with col_box1:
        st.markdown("""
        <div style="background:#ffffff; border:2px solid #3b82f6; border-radius:20px; padding:32px 24px; text-align:center; box-shadow:0 10px 25px -5px rgba(59,130,246,0.1); min-height:220px; display:flex; flex-direction:column; justify-content:center; align-items:center;">
            <div style="font-size:48px; margin-bottom:12px;">📐</div>
            <h3 style="color:#0f172a; margin:0 0 10px 0; font-weight:800; font-size:22px;">Archisketch 스마트 도면 대시보드</h3>
            <p style="color:#64748b; font-size:14px; line-height:1.6; margin:0;">
                푸드트럭, 캐노피 천막 부스, 메인무대 트러스 등 실제 행사 구조물이 세밀하게 구현된 2D/3D CAD 도면을 직관적으로 확인하고 조율합니다.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("🚀 Archisketch 도면 대시보드 바로가기", key="btn_go_dash", type="primary", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()

    with col_box2:
        st.markdown("""
        <div style="background:#ffffff; border:2px solid #8b5cf6; border-radius:20px; padding:32px 24px; text-align:center; box-shadow:0 10px 25px -5px rgba(139,92,246,0.1); min-height:220px; display:flex; flex-direction:column; justify-content:center; align-items:center;">
            <div style="font-size:48px; margin-bottom:12px;">📑</div>
            <h3 style="color:#0f172a; margin:0 0 10px 0; font-weight:800; font-size:22px;">AI 상사 결재용 직인 보고서</h3>
            <p style="color:#64748b; font-size:14px; line-height:1.6; margin:0;">
                Archisketch 도면 분석 타당성, 소방법 검토, 피난 안전성 평가가 포함된 완벽한 직장 상사 결재용 기안서를 자동 생성합니다.
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("📄 AI 결재용 보고서 바로가기", key="btn_go_report", use_container_width=True):
            st.session_state.page = "report"
            st.rerun()

elif st.session_state.page == "dashboard":
    
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <div>
            <h2 style="margin:0; color:#0f172a; font-weight:800;">📐 Archisketch 스마트 행사 도면 설계</h2>
            <p style="margin:4px 0 0 0; color:#64748b; font-size:14px;">행사 도면 위에서 실제 시설물(푸드트럭, 캐노피 천막, 무대) 배치, 혼잡도 Heatmap, 동선 시뮬레이션을 편집합니다.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Event Form Expander
    with st.expander("📝 행사 기본 정보 설정 및 수정", expanded=not st.session_state.design_generated):
        with st.form("event_info_form"):
            c_in1, c_in2, c_in3, c_in4 = st.columns(4)
            with c_in1:
                event_name_input = st.text_input("행사명", value=st.session_state.event_name)
                event_type_input = st.selectbox("행사 유형", ["축제", "박람회/전시회", "기업 행사", "팝업스토어"], index=0)
                event_purpose_input = st.text_input("행사 목적", value=st.session_state.event_purpose)
            with c_in2:
                expected_visitors_input = st.number_input("예상 인원 (명)", value=st.session_state.expected_visitors, step=500)
                duration_input = st.text_input("진행 시간", value=st.session_state.duration)
                target_age_input = st.text_input("대상 연령대", value=st.session_state.target_age)
            with c_in3:
                mood_input = st.text_input("원하는 분위기", value=st.session_state.mood)
                entry_fee_input = st.text_input("입장료", value=st.session_state.entry_fee)
                location_input = st.text_input("장소 선택", value=st.session_state.location)
            with c_in4:
                budget_input = st.text_input("예산", value=st.session_state.budget)
                st.write("")
                submit_design_btn = st.form_submit_button("✨ Archisketch AI 도면 생성", type="primary", use_container_width=True)

            if submit_design_btn:
                st.session_state.event_name = event_name_input
                st.session_state.event_type = event_type_input
                st.session_state.event_purpose = event_purpose_input
                st.session_state.expected_visitors = expected_visitors_input
                st.session_state.duration = duration_input
                st.session_state.target_age = target_age_input
                st.session_state.mood = mood_input
                st.session_state.entry_fee = entry_fee_input
                st.session_state.location = location_input
                st.session_state.budget = budget_input
                st.session_state.design_generated = True
                st.success("✨ Archisketch 도면 및 공간 최적 배치가 완료되었습니다!")
                st.rerun()

    # Info summary bar
    st.markdown(f"""
    <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:10px 18px; margin-bottom:16px; font-size:13px; color:#334155;">
        🆔 <b>행사명:</b> {st.session_state.event_name} &nbsp;|&nbsp;
        🏷️ <b>유형:</b> {st.session_state.event_type} &nbsp;|&nbsp;
        👥 <b>예상인원:</b> {st.session_state.expected_visitors:,}명 &nbsp;|&nbsp;
        📍 <b>장소:</b> {st.session_state.location} &nbsp;|&nbsp;
        💰 <b>예산:</b> {st.session_state.budget}
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.design_generated:
        
        # Archisketch Canvas Controls Bar
        st.markdown("<div class='archisketch-bar'>", unsafe_allow_html=True)
        col_ctrl1, col_ctrl2, col_ctrl3, col_ctrl4, col_ctrl5 = st.columns([2, 2, 2, 2, 2])
        
        with col_ctrl1:
            st.session_state.show_heatmap_overlay = st.checkbox("🔥 혼잡도(Heatmap) 오버레이", value=st.session_state.show_heatmap_overlay)
        with col_ctrl2:
            st.session_state.show_flow_arrows = st.checkbox("🧭 주요 순환 동선 유도선", value=st.session_state.show_flow_arrows)
        with col_ctrl3:
            st.session_state.show_grid_lines = st.checkbox("📐 CAD Grid 그리드 표시", value=st.session_state.show_grid_lines)
        with col_ctrl4:
            st.session_state.view_mode = st.selectbox("뷰 모드", ["2D CAD 상세 도면", "3D 입체 조감도"], index=0, label_visibility="collapsed")
        with col_ctrl5:
            if st.button("🔄 AI 도면 재배치", key="reset_archisketch", use_container_width=True):
                st.toast("Archisketch AI가 최적 배치를 다시 계산했습니다!")
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        col_main_map, col_side_eval = st.columns([7, 5])

        with col_main_map:
            st.markdown("#### 🗺️ Archisketch 2D CAD 실제 행사 설계 도면")

            uploaded_map_img = st.file_uploader("🖼️ 배경 행사 도면 / 입체 이미지 업로드", type=["png", "jpg", "jpeg"], key="map_img_uploader")

            fig_map = go.Figure()

            # 1. Base Park Boundary & Realistic Paved Roadway Infrastructure
            fig_map.add_shape(type="rect", x0=0, y0=0, x1=100, y1=100, fillcolor="#ecfdf5", opacity=1, line=dict(color="#a7f3d0", width=2)) # Natural grass field base
            
            # Paved perimeter roads and walkways (Realistic Site Ground)
            fig_map.add_shape(type="rect", x0=2, y0=2, x1=98, y1=98, fillcolor="rgba(0,0,0,0)", line=dict(color="#cbd5e1", width=12)) # Outer paved service road
            fig_map.add_shape(type="rect", x0=24, y0=30, x1=76, y1=72, fillcolor="#f1f5f9", opacity=0.9, line=dict(color="#94a3b8", width=2, dash="dash")) # Central paved plaza

            # 2. Detailed Realistic Facility Structures

            # A. メイン무대 (Stage Setup with Speakers, LED Screen & Truss)
            stage_pos = ZONE_DATA["메인무대"]["position"]
            sx, sy = stage_pos[0], stage_pos[1]
            # Stage Deck
            fig_map.add_shape(type="rect", x0=sx-16, y0=sy-6, x1=sx+16, y1=sy+6, fillcolor="#1e293b", line=dict(color="#3b82f6", width=3))
            # LED Back Screen
            fig_map.add_shape(type="rect", x0=sx-12, y0=sy+4, x1=sx+12, y1=sy+5.5, fillcolor="#60a5fa", line=dict(color="#ffffff", width=1))
            # Speaker Line Arrays (Left & Right)
            fig_map.add_shape(type="rect", x0=sx-18, y0=sy-4, x1=sx-16.5, y1=sy+2, fillcolor="#0f172a", line=dict(color="#38bdf8", width=1.5))
            fig_map.add_shape(type="rect", x0=sx+16.5, y0=sy-4, x1=sx+18, y1=sy+2, fillcolor="#0f172a", line=dict(color="#38bdf8", width=1.5))
            # FOH Audio Control Booth
            fig_map.add_shape(type="rect", x0=sx-4, y0=sy-18, x1=sx+4, y1=sy-12, fillcolor="#334155", line=dict(color="#3b82f6", width=1.5))

            # B. 푸드존 (Actual Food Trucks with Cab, Canopy Awning & Picnic Tables)
            food_pos = ZONE_DATA["푸드존"]["position"]
            fx, fy = food_pos[0], food_pos[1]
            for offset_y in [-5, 0, 5]:
                # Truck Cargo Body
                fig_map.add_shape(type="rect", x0=fx-9, y0=fy+offset_y-1.8, x1=fx-2, y1=fy+offset_y+1.8, fillcolor="#f97316", line=dict(color="#ea580c", width=1.5))
                # Truck Cab (Front)
                fig_map.add_shape(type="rect", x0=fx-2, y0=fy+offset_y-1.4, x1=fx, y1=fy+offset_y+1.4, fillcolor="#fdba74", line=dict(color="#ea580c", width=1))
                # Striped Canopy Awning
                fig_map.add_shape(type="rect", x0=fx-8, y0=fy+offset_y-3.2, x1=fx-3, y1=fy+offset_y-1.8, fillcolor="#fde047", line=dict(color="#ca8a04", width=1))
                # Picnic Outdoor Tables
                fig_map.add_shape(type="circle", x0=fx+2, y0=fy+offset_y-1, x1=fx+4, y1=fy+offset_y+1, fillcolor="#a16207", line=dict(color="#ffffff", width=1))

            # C. 체험부스 (Row of 3x3 Canopy Tents with Diagonal Peak Roofs)
            booth_pos = ZONE_DATA["체험부스"]["position"]
            bx, by = booth_pos[0], booth_pos[1]
            for offset_y in [-6, -1, 4]:
                for offset_x in [-5, 2]:
                    # Tent Square Base
                    fig_map.add_shape(type="rect", x0=bx+offset_x, y0=by+offset_y, x1=bx+offset_x+5, y1=by+offset_y+4, fillcolor="#ddd6fe", line=dict(color="#7c3aed", width=1.5))
                    # Tent Roof Canopy Cross Lines
                    fig_map.add_shape(type="line", x0=bx+offset_x, y0=by+offset_y, x1=bx+offset_x+5, y1=by+offset_y+4, line=dict(color="#7c3aed", width=1, dash="dot"))
                    fig_map.add_shape(type="line", x0=bx+offset_x, y0=by+offset_y+4, x1=bx+offset_x+5, y1=by+offset_y, line=dict(color="#7c3aed", width=1, dash="dot"))

            # D. 휴식공간 (Lawn Deck with Trees & Parasols)
            rest_pos = ZONE_DATA["휴식공간"]["position"]
            rx, ry = rest_pos[0], rest_pos[1]
            # Rest Zone Wooden Deck Area
            fig_map.add_shape(type="rect", x0=rx-10, y0=ry-7, x1=rx+10, y1=ry+7, fillcolor="#d1fae5", line=dict(color="#10b981", width=2))
            # Trees (Layered Green Circles)
            fig_map.add_shape(type="circle", x0=rx-8, y0=ry+2, x1=rx-4, y1=ry+6, fillcolor="#059669", opacity=0.85, line=dict(color="#047857", width=1))
            fig_map.add_shape(type="circle", x0=rx+4, y0=ry-5, x1=rx+8, y1=ry-1, fillcolor="#059669", opacity=0.85, line=dict(color="#047857", width=1))
            # Lounge Umbrellas
            fig_map.add_shape(type="circle", x0=rx-2, y0=ry-2, x1=rx+2, y1=ry+2, fillcolor="#34d399", line=dict(color="#ffffff", width=2))

            # E. 응급의료센터 (Medical Marquee Tent + Ambulance Bay)
            med_pos = ZONE_DATA["응급의료센터"]["position"]
            mx, my = med_pos[0], med_pos[1]
            fig_map.add_shape(type="rect", x0=mx-7, y0=my-5, x1=mx+3, y1=my+5, fillcolor="#fef2f2", line=dict(color="#ef4444", width=2))
            # Red Cross Symbol Lines
            fig_map.add_shape(type="line", x0=mx-3, y0=my, x1=mx-1, y1=my, line=dict(color="#ef4444", width=4))
            fig_map.add_shape(type="line", x0=mx-2, y0=my-1.5, x1=mx-2, y1=my+1.5, line=dict(color="#ef4444", width=4))
            # Ambulance Vehicle Shape
            fig_map.add_shape(type="rect", x0=mx+4, y0=my-3, x1=mx+8, y1=my+3, fillcolor="#ffffff", line=dict(color="#dc2626", width=1.5))

            # F. 출입구 (Gate Archway & Turnstile Lanes)
            gate_pos = ZONE_DATA["출입구"]["position"]
            gx, gy = gate_pos[0], gate_pos[1]
            fig_map.add_shape(type="rect", x0=gx-10, y0=gy-2, x1=gx+10, y1=gy+2, fillcolor="#334155", line=dict(color="#0f172a", width=2))
            # Security Turnstile Lane Indicators
            for lane_x in range(int(gx-8), int(gx+9), 4):
                fig_map.add_shape(type="line", x0=lane_x, y0=gy-2, x1=lane_x, y1=gy+2, line=dict(color="#38bdf8", width=2))

            # Custom Image Layer Overlay if uploaded
            if uploaded_map_img is not None:
                import base64
                encoded_img = base64.b64encode(uploaded_map_img.read()).decode("utf-8")
                img_data_url = f"data:image/png;base64,{encoded_img}"
                fig_map.add_layout_image(dict(source=img_data_url, xref="x", yref="y", x=0, y=100, sizex=100, sizey=100, opacity=0.85, layer="below"))

            # 3. Crowd Density Heatmap (Smooth contour overlay)
            if st.session_state.show_heatmap_overlay:
                np.random.seed(42)
                x_h = np.random.normal(sx, 8, 350)
                y_h = np.random.normal(sy-8, 6, 350)
                x_h = np.append(x_h, np.random.normal(fx, 5, 200))
                y_h = np.append(y_h, np.random.normal(fy, 5, 200))
                x_h = np.clip(x_h, 2, 98)
                y_h = np.clip(y_h, 2, 98)

                fig_map.add_trace(go.Histogram2dContour(
                    x=x_h, y=y_h,
                    colorscale=[
                        [0, 'rgba(255,255,255,0)'],
                        [0.25, 'rgba(59,130,246,0.2)'],
                        [0.6, 'rgba(245,158,11,0.45)'],
                        [1.0, 'rgba(239,68,68,0.75)']
                    ],
                    showscale=False, ncontours=12, line=dict(width=0)
                ))

            # 4. Clean Flow Pathways (Smooth Vector Guided Lines instead of harsh arrows)
            if st.session_state.show_flow_arrows:
                flow_paths = [
                    (gx, gy+2, fx, fy-7),
                    (gx, gy+2, bx, by-8),
                    (fx, fy+7, sx-10, sy-10),
                    (bx, by+6, sx-12, sy-10),
                    (gx, gy+2, rx-5, ry-7),
                ]
                for x1_p, y1_p, x2_p, y2_p in flow_paths:
                    fig_map.add_trace(go.Scatter(
                        x=[x1_p, x2_p], y=[y1_p, y2_p],
                        mode="lines",
                        line=dict(color="#2563eb", width=2.5, dash="dashdot"),
                        showlegend=False,
                        hoverinfo="none"
                    ))

            # 5. Stylish Sleek Zone Label Badges
            for zone_k, info in ZONE_DATA.items():
                x_p = float(np.clip(info["position"][0], 5, 95))
                y_p = float(np.clip(info["position"][1], 5, 95))
                is_sel = (st.session_state.selected_zone == zone_k)

                fig_map.add_trace(go.Scatter(
                    x=[x_p], y=[y_p],
                    mode="text",
                    name=zone_k,
                    text=[f"<span style='background-color:{info['color']}; color:white; padding:4px 10px; border-radius:12px; font-weight:bold; font-size:11px; border:{'3px solid #0f172a' if is_sel else '2px solid white'}; box-shadow:0 2px 8px rgba(0,0,0,0.15);'>{info['icon']} {zone_k}</span>"],
                    textposition="middle center",
                    showlegend=False
                ))

            fig_map.update_layout(
                xaxis=dict(range=[0, 100], showgrid=st.session_state.show_grid_lines, zeroline=False, visible=st.session_state.show_grid_lines, gridcolor="#cbd5e1"),
                yaxis=dict(range=[0, 100], showgrid=st.session_state.show_grid_lines, zeroline=False, visible=st.session_state.show_grid_lines, gridcolor="#cbd5e1"),
                height=540,
                margin=dict(l=5, r=5, t=5, b=5),
                paper_bgcolor="#ffffff",
                plot_bgcolor="#f8fafc",
                showlegend=False
            )

            st.plotly_chart(fig_map, use_container_width=True)

            if st.session_state.show_heatmap_overlay:
                st.markdown("<div style='text-align:center; font-size:12px; color:#64748b; margin-top:-10px;'>🟢 원활 &nbsp; 🟡 보통 &nbsp; 🟠 주의 &nbsp; 🔴 매우 혼잡</div>", unsafe_allow_html=True)

        with col_side_eval:
# ... existing code ...
```

위의 모든 변경 사항이 반영되어 홈 화면의 구성과 대시보드 도면의 리얼리티가 확실히 강화되었습니다. 편안하게 수정 결과를 확인해 보세요!
