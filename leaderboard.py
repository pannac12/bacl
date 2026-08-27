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

col1, col2 = st.columns([1, 9])
with col1:
    st.image("baca_logo.webp", use_column_width=True)
with col2:
    st.header("BACL 2026: Season 2") 

worksheetSouth = sh.get_worksheet(2)

names_south = worksheetSouth.get("A2:A26")
played_south = worksheetSouth.get("B2:B26")
points_south = worksheetSouth.get("D2:D26")

nameSouth = [item[0] if item else '' for item in names_south]
pointsSouth = [item[0] if item else '0' for item in points_south]
playedSouth = [item[0] if item else '0' for item in played_south]

dfSouth = pd.DataFrame({
    'Name': nameSouth,
    'Points': pointsSouth,
    'Played': playedSouth
})

dfSouth['Points'] = pd.to_numeric(dfSouth['Points'], errors='coerce').fillna(0)
dfSouth = dfSouth.sort_values(by='Points', ascending=False)


col1, col2 = st.columns(2)

with col1:
    st.subheader("Players")
    st.dataframe(dfSouth.style.set_properties(**{'text-align': 'right'}, subset=['Played']), height=800, hide_index=True)


