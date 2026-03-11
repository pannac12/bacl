import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

creds_dict = dict(st.secrets["gcp_service_account"])
creds_dict["private_key_id"] = creds_dict["private_key"].replace("\\n", "\n")
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
gc = gspread.authorize(creds)
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1BZ80vE4pwaFBEv3czzK5wYXcxaesJl3Jw9LJWlJ3XU0")

col1, col2 = st.columns([1, 9])
with col1:
    st.image("baca_logo.webp", use_column_width=True)
with col2:
    st.header("BACL 2026: Season 1") 

worksheetEast = sh.get_worksheet(4)
worksheetSouth = sh.get_worksheet(2)

names_east = worksheetEast.get("A2:A21")
points_east = worksheetEast.get("D2:D21")
played_east = worksheetEast.get("B2:B21")

names_south = worksheetSouth.get("A2:A22")
points_south = worksheetSouth.get("D2:D22")
played_south = worksheetSouth.get("B2:B22")

nameEast = [item[0] if item else '' for item in names_east]
pointsEast = [item[0] if item else '0' for item in points_east]
playedEast = [item[0] if item else '0' for item in played_east]

nameSouth = [item[0] if item else '' for item in names_south]
pointsSouth = [item[0] if item else '0' for item in points_south]
playedSouth = [item[0] if item else '0' for item in played_south]

dfEast = pd.DataFrame({
    'Name': nameEast,
    'Points': pointsEast,
    'Played': playedEast
})

dfEast['Points'] = pd.to_numeric(dfEast['Points'], errors='coerce').fillna(0)
dfEast = dfEast.sort_values(by='Points', ascending=False)

dfSouth = pd.DataFrame({
    'Name': nameSouth,
    'Points': pointsSouth,
    'Played': playedSouth
})

dfSouth['Points'] = pd.to_numeric(dfSouth['Points'], errors='coerce').fillna(0)
dfSouth = dfSouth.sort_values(by='Points', ascending=False)


col1, col2 = st.columns(2)

with col1:
    st.subheader("East pool")
    st.dataframe(dfEast.style.set_properties(**{'text-align': 'right'}, subset=['Played']), height=800, hide_index=True)

with col2:
    st.subheader("South pool")
    st.dataframe(dfSouth.style.set_properties(**{'text-align': 'right'}, subset=['Played']), height=800, hide_index=True)


