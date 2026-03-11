import streamlit as st
import gspread
import google.generativeai as genai
from google.oauth2.service_account import Credentials

# Need to switch to new GenAI module
# https://github.com/google-gemini/deprecated-generative-ai-python/blob/main/README.md

print("BACL 2026: Season 1") 
print("Getting data...")

creds_dict = dict(st.secrets["gcp_service_account"])
creds_dict["private_key_id"] = creds_dict["private_key"].replace("\\n", "\n")
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
gc = gspread.authorize(creds)
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1BZ80vE4pwaFBEv3czzK5wYXcxaesJl3Jw9LJWlJ3XU0")

worksheet = sh.get_worksheet(1)
all_values = worksheet.get_all_values()

# Manually process headers to handle duplicates
headers = []
seen_headers = {}
for header in all_values[0]:
    original_header = header
    count = 0
    while header in seen_headers:
        count += 1
        header = f"{original_header}_{count}"
    seen_headers[header] = True
    headers.append(header)

# Convert remaining rows into a list of dictionaries
data = []
for row_index in range(1, len(all_values)):
    row_data = {}
    for col_index, cell_value in enumerate(all_values[row_index]):
        if col_index < len(headers):
            row_data[headers[col_index]] = cell_value
    data.append(row_data)


question = "Who all has Chandu beaten so far?"
context = f"Here is the tournament data: {str(data)}"

prompt = f"""
    You are a tournament assistant. Use the following data to answer the user's question.
    If the answer isn't in the data, just say you don't know.
    
    {context}
    
    User Question: {question}
    """

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-3-flash-preview')
response = model.generate_content(
        contents=prompt)

print(response.text)