import streamlit as st
import gspread
import google.generativeai as genai
from google.oauth2.service_account import Credentials

# Need to switch to new GenAI module
# https://github.com/google-gemini/deprecated-generative-ai-python/blob/main/README.md

creds_dict = dict(st.secrets["gcp_service_account"])
creds_dict["private_key_id"] = creds_dict["private_key"].replace("\\n", "\n")
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
gc = gspread.authorize(creds)
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1BZ80vE4pwaFBEv3czzK5wYXcxaesJl3Jw9LJWlJ3XU0")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-3-flash-preview')

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


# Initialize Session State so fields persist
if "user_question" not in st.session_state:
    st.session_state.user_question = ""
if "ai_answer" not in st.session_state:
    st.session_state.ai_answer = "The answer will appear here..."

# Large Question Field. We link it to session_state using the 'key' parameter.
st.text_area(
    "Ask a question", 
    height=150, 
    placeholder="e.g., Who is going to win the tournament?",
    key="user_question"
)

# Action Button
if st.button("Ask AI"):
    if st.session_state.user_question:
        with st.spinner("Thinking..."):
            # This is where you'd call your ask_tournament_bot(st.session_state.user_question)
            # For now, we'll simulate a response:
            question = st.session_state.user_question
            context = f"Here is the tournament data: {str(data)}"
            prompt = f"""
                You are a tournament assistant. Use the following data to answer the user's question.
                If the answer isn't in the data, just say you don't know.
                
                {context}
                
                User Question: {question}
                """
            response = model.generate_content(contents=prompt)
            st.session_state.ai_answer = response.text
    else:
        st.warning("Please enter a question first!")

st.divider()

# Large Answer Field (Editable). Note: Making it editable allows you to 'clean up' or add notes to the AI's response.
st.text_area(
    "AI Response", 
    value=st.session_state.ai_answer, 
    height=300, 
    key="final_answer"
)


