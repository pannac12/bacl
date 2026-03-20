import streamlit as st
import gspread
import google.generativeai as genai
from google.oauth2.service_account import Credentials

# Initialize Google Sheets connection
@st.cache_resource
def get_gsheets_client():
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds_dict["private_key_id"] = creds_dict["private_key"].replace("\\n", "\n")
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    return gspread.authorize(creds)

@st.cache_data(ttl=600)  # Cache data for 10 minutes
def load_tournament_data():
    gc = get_gsheets_client()
    sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1BZ80vE4pwaFBEv3czzK5wYXcxaesJl3Jw9LJWlJ3XU0")
    
    all_data = []
    # Fetch from the first 5 worksheets
    for i in range(5):
        try:
            worksheet = sh.get_worksheet(i)
            if worksheet:
                all_data.extend(worksheet.get_all_values())
        except Exception as e:
            st.error(f"Error loading worksheet {i}: {e}")
    return all_data

# Configure GenAI
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
# Using gemini-1.5-flash as it's reliable and fast. 
# Feel free to change to 'gemini-1.5-pro' for more complex reasoning.
model = genai.GenerativeModel('gemini-3-flash-preview')

data = load_tournament_data()

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
            question = st.session_state.user_question
            # Convert list of rows to a more prompt-friendly string
            context_str = "\n".join([", ".join(row) for row in data])
            
            prompt = f"""
                You are a tournament assistant. Use the following data to answer the user's question.
                If the answer isn't in the data, say you don't know - but also make a calculated guess.
                All the players are male.
                
                Tournament Data:
                {context_str}
                
                User Question: {question}
                """
            try:
                # Log prompt length for debugging
                print(f"Sending prompt to AI (length: {len(prompt)})")
                
                response = model.generate_content(contents=prompt)
                
                # Check for blocked responses or empty candidates
                if response and hasattr(response, 'candidates') and response.candidates:
                    candidate = response.candidates[0]
                    # Check if response was blocked by safety filters
                    if candidate.finish_reason == 3: # SAFETY
                        answer = "The response was blocked by safety filters. Please try rephrasing your question."
                    elif hasattr(candidate.content, 'parts') and candidate.content.parts:
                        answer = response.text
                    else:
                        answer = "The AI returned an empty response. It might be struggling with the context or question."
                else:
                    answer = "No response candidates returned from the AI."
                
                print(f"AI Response: {answer[:100]}...") # Print first 100 chars to console
                st.session_state.ai_answer = answer
                st.session_state.final_answer = answer # Update the text area widget specifically
                
            except Exception as e:
                error_msg = f"An error occurred while communicating with the AI: {str(e)}"
                st.session_state.ai_answer = error_msg
                st.session_state.final_answer = error_msg
                st.error(f"AI Error: {str(e)}")
    else:
        st.warning("Please enter a question first!")

st.divider()

# Large Answer Field (Editable). 
# Note: key="final_answer" ensures that edits made here are saved in session state.
st.markdown(
    st.session_state.ai_answer
    )
