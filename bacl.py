import streamlit as st

leaderboard_page = st.Page("leaderboard.py", title="Leaderboard")
ask_question_page = st.Page("ask_question.py", title="Ask a Question")
pg = st.navigation([leaderboard_page, ask_question_page])
st.set_page_config(page_title="BACL 2026: Season 2")
pg.run()