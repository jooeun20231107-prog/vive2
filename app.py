# 사이드바 구성 (메뉴 이동 라디오 버튼 제거 버전)
with st.sidebar:
    if st.button("🎪 이벤트 온 (Event-On)", key="logo_btn", use_container_width=True, type="primary"):
        st.session_state['page'] = 'home'
        st.rerun()

    st.caption("AI 기반 행사 공간 자동 설계 플랫폼")
    st.divider()

    # [삭제 완료] 기존 page_selection = st.radio(...) 구문을 삭제했습니다.

    if st.session_state['logged_in']:
        st.markdown(f"👤 **{st.session_state['username']}** 님 (총괄 기획)")
        if st.button("로그아웃", key="sidebar_logout", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()
