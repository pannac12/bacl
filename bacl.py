import streamlit as st
import os
import google.generativeai as genai

leaderboard_page = st.Page("leaderboard.py", title="Leaderboard")
ask_question_page = st.Page("ask_question.py", title="Ask a Question")
pg = st.navigation([leaderboard_page, ask_question_page])
st.set_page_config(page_title="BACL 2026: Season 1")
pg.run()