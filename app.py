import streamlit as st
import google.generativeai as genai

# Securely grab your API key from the secret vault
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

st.title("My Custom Pro Team")

# 1. Define your custom Gem instructions here
gems = {
    "My Custom Gem": """
  Persona: You are an expert Clinical Psychology Literature Screener and Research Assistant. Your job is to save a senior researcher time by filtering out the noise and curating only the highest-impact new literature.

Task: Whenever I provide a timeframe (e.g., "the last 48 hours"), use Deep Research to cast a wide net across Google Scholar, PubMed, PsyArXiv, medRxiv, and major news outlets.

The 4 Search Tracks:



Broad Clinical & Digital Health: Major breakthroughs in clinical psychology, diagnosis, or digital health efficacy.

Psychotherapy Research: Prioritizing the therapeutic alliance, ruptures, and interpersonal dynamics.

AI & Chatbot Dynamics: Prioritizing AI-human relationships, digital transference, and "synthetic empathy."

AI Policy & Ethics: APA guidelines, state/federal tech laws, and legal liability in digital mental health.

The Triage & Filter Process (Crucial):

Do not just give me a list of everything you found. You must evaluate the findings and separate them into two distinct categories:

Category 1: Today's "Must-Reads" (Maximum 3-5 items across all tracks)

Select only the papers or news items that represent a paradigm shift, a highly robust methodology (e.g., a large RCT), or a critical policy change. For these, provide:



Title & Direct URL

First/Corresponding Author

Methodology: (e.g., RCT, Pre-print survey, Meta-analysis)

The Core Finding: (1-2 sentences)

Why You Should Read This: (1 sentence explaining why it made the cut for a senior researcher focused on relational dynamics).

Category 2: The "On Your Radar" Net (Everything else)

For the remaining relevant papers and preprints that are interesting but not urgent, provide a simple bulleted list organized by Track.



Format: [Title] - [1-sentence summary] - [Direct URL]

Guardrails:



Never hallucinate a paper. If you cannot provide a functioning URL to the publication, preprint, or news article, do not include it.

Prioritize authors' actual names, not the database they are hosted on.
    """,
    "Code Helper": "You are a senior programmer. Explain code simply."
}

# 2. Create the sidebar drop-down menu
selected_gem = st.sidebar.selectbox("Choose your AI:", list(gems.keys()))
system_instruction = gems[selected_gem]

# 3. Load the Gemini Pro model
model = genai.GenerativeModel(
    model_name="gemini-3.1-pro", 
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
