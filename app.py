import streamlit as st
import google.generativeai as genai

# Securely grab your API key from the secret vault
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

st.title("My Custom Pro Team")

# 1. Define your custom Gem instructions here
gems = {
  "My Custom Gem": st.secrets["MY_SECRET_PROMPT"],
    "Code Helper": "You are a senior programmer. Explain code simply."
}

# 2. Create the sidebar drop-down menu
selected_gem = st.sidebar.selectbox("Choose your AI:", list(gems.keys()))
system_instruction = gems[selected_gem]

# 3. Load the Gemini Pro model
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash", 
    system_instruction=system_instruction
)

# 4. Set up the chat memory (so it remembers the conversation)
if "current_gem" not in st.session_state or st.session_state.current_gem != selected_gem:
    # If you change the Gem, start a fresh chat history
    st.session_state.current_gem = selected_gem
    st.session_state.chat_session = model.start_chat(history=[])

# 5. Show the chat history on the screen
for message in st.session_state.chat_session.history:
    role = "assistant" if message.role == "model" else "user"
    with st.chat_message(role):
        st.write(message.parts[0].text)

# 6. Handle your new messages
if prompt := st.chat_input("Type your message here..."):
    # Show your message on screen
    st.chat_message("user").write(prompt)
    
    # Send it to Gemini Pro and show the response
    response = st.session_state.chat_session.send_message(prompt)
    st.chat_message("assistant").write(response.text)
