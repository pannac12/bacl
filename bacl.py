import streamlit as st
import os
import google.generativeai as genai

home_page = st.Page("home.py", title="Home")
ask_question_page = st.Page("ask_question.py", title="Ask a Question")
pg = st.navigation([home_page, ask_question_page])
st.set_page_config(page_title="BACL 2026: Season 1")
pg.run()