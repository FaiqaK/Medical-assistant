from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

import streamlit as st
from dotenv import load_dotenv, find_dotenv


# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Medical Assistant",
    page_icon="🤖"
)


# -----------------------------------
# CUSTOM CSS
# -----------------------------------

st.markdown(
    """
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #fff7ed 0%,
        #fdf2f8 25%,
        #eef2ff 55%,
        #ecfeff 100%
    );
}

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #ede9fe,
        #dbeafe,
        #fce7f3
    );
}

section[data-testid="stSidebar"] * {
    color: #1e293b;
}

div[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.88);
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 10px;
    margin-bottom: 10px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.05);
}

div[data-testid="stChatMessage"] p {
    color: #1e293b;
}

div[data-testid="stChatInput"] {
    background: white;
    border-radius: 18px;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.08);
}

</style>
""",
    unsafe_allow_html=True
)

# -----------------------------------
# LOAD ENV
# -----------------------------------

load_dotenv(find_dotenv(), override=True)


# -----------------------------------
# TITLE
# -----------------------------------

st.markdown(
    "<h1 style='text-align: center;'>🩺 Medical Assistant</h1>",
    unsafe_allow_html=True
)


# -----------------------------------
# SIDEBAR
# -----------------------------------

with st.sidebar:

    # -------------------------------
    # APP INFO
    # -------------------------------

    st.markdown("## 🩺 MediGuide AI")

    st.caption(
        "Your AI-powered health information assistant."
    )

    st.divider()


    # -------------------------------
    # API SETTINGS
    # -------------------------------

    st.markdown("### 🔑 API Settings")

    api_key = st.text_input(
        "Enter OpenAI API Key",
        type="password",
        placeholder="sk-..."
    )

    if api_key:
        st.success("API key added ✓")
    else:
        st.info("Enter your API key to start chatting.")

    st.divider()


    # -------------------------------
    # WHAT I CAN HELP WITH
    # -------------------------------

    st.markdown("### 🩺 I can help with")

    st.markdown("""
    - 🤒 Symptoms & health concerns
    - 💊 General medication information
    - 🥗 Nutrition & healthy habits
    - 🧪 Medical tests & terminology
    - 🚨 Warning signs to watch for
    """)

    st.divider()


    # -------------------------------
    # CLEAR CHAT
    # -------------------------------

    if st.button("🗑️ Clear Conversation"):

        st.session_state.messages = []

        st.rerun()


    st.divider()


    # -------------------------------
    # DISCLAIMER
    # -------------------------------

    st.warning(
        "⚠️ This assistant provides general health information "
        "and is not a substitute for professional medical advice."
    )

# -----------------------------------
# FIXED MEDICAL SYSTEM ROLE
# -----------------------------------

system_message = """
You are a medical assistant.

Only answer questions related to medicine, health, symptoms,
diseases, medications, nutrition, and healthcare.

If the user asks a question outside the medical field,
reply:
"I am a medical assistant and can only help with health-related questions."

Do not provide a definitive diagnosis.
If symptoms may be serious or urgent, advise the user to seek
appropriate professional medical care.
"""


# -----------------------------------
# SESSION STATE
# -----------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------------
# SHOW CHAT HISTORY
# -----------------------------------

for msg in st.session_state.messages:

    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)

    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.write(msg.content)


# -----------------------------------
# CHAT INPUT
# -----------------------------------

user_prompt = st.chat_input(
    "Ask a medical question..."
)


# -----------------------------------
# PROCESS USER MESSAGE
# -----------------------------------

if user_prompt:

    if not api_key:
        st.warning(
            "Please enter your OpenAI API key in the sidebar."
        )
        st.stop()

    chat = ChatOpenAI(
        model="gpt-5.2",
        api_key=api_key
    )

    # Save user message ONCE
    st.session_state.messages.append(
        HumanMessage(content=user_prompt)
    )

    # Build conversation
    conversation = [
        SystemMessage(content=system_message)
    ] + st.session_state.messages

    # Get AI response
    with st.spinner("Working on your request..."):
        response = chat.invoke(conversation)

    # Save AI response ONCE
    st.session_state.messages.append(
        AIMessage(content=response.content)
    )

    # Refresh page
    st.rerun()




