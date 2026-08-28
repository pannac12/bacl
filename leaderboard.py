import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

creds_dict = dict(st.secrets["gcp_service_account"])
creds_dict["private_key_id"] = creds_dict["private_key"].replace("\\n", "\n")
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
gc = gspread.authorize(creds)
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1dw86Z--kwti3m-jhfUQfkZT-cnX-Aqp05jK-4ZIzEW0")

col1, col2, col3 = st.columns([1, 6, 3])
with col1:
    st.image("baca_logo.webp", width="stretch")
with col2:
    st.header("BACL 2026: Season 2") 
with col3:
    st.write("")
    if st.button("💬 Ask a Question", key="nav_ask_question"):
        st.switch_page("ask_question.py") 

worksheetSouth = sh.get_worksheet(2)

names_south = worksheetSouth.get("A2:A26")
played_south = worksheetSouth.get("B2:B26")
points_south = worksheetSouth.get("D2:D26")

nameSouth = [item[0] if item else '' for item in names_south]
pointsSouth = [item[0] if item else '0' for item in points_south]
playedSouth = [item[0] if item else '0' for item in played_south]

dfSouth = pd.DataFrame({
    'Name': nameSouth,
    'Matches Played': playedSouth,
    'Matches Won': pointsSouth
})

dfSouth['Matches Won'] = pd.to_numeric(dfSouth['Matches Won'], errors='coerce').fillna(0)
dfSouth = dfSouth.sort_values(by='Matches Won', ascending=False)


col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("Players")
    st.dataframe(
        dfSouth,
        column_config={
            "Matches Played": st.column_config.Column(alignment="center"),
            "Matches Won": st.column_config.Column(alignment="center"),
        },
        height=900,
        hide_index=True,
    )


