import streamlit as st

st.set_page_config(
    page_title="BACL 2026: Season 2",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        [data-testid="stSidebarCollapsedControl"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

leaderboard_page = st.Page("leaderboard.py", title="Leaderboard", default=True)
ask_question_page = st.Page("ask_question.py", title="AI Insights")
pg = st.navigation([leaderboard_page, ask_question_page], position="hidden")
pg.run()