import os
import sys
import warnings

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from dotenv import load_dotenv
from chatbot import initialize_Eighteenot, ask

warnings.filterwarnings("ignore")

load_dotenv()

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="EIGHTEENOT 🏏",
    page_icon="🏏",
    layout="centered",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(
            135deg,
            #0f0f0f 0%,
            #1a1a2e 100%
        );
    }

    .kohli-header {
        text-align: center;
        padding: 20px 0 10px 0;
    }

    .kohli-header h1 {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #f5a623, #e8173a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    .kohli-header p {
        color: #888;
        font-size: 0.95rem;
        margin-top: 5px;
    }

    .footer {
        text-align: center;
        color: #666;
        font-size: 0.8rem;
        padding: 20px 0 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# INITIALIZE CHATBOT
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_chatbot():
    return initialize_Eighteenot()

# ─────────────────────────────────────────────
# WELCOME MESSAGE
# ─────────────────────────────────────────────
WELCOME_MESSAGE = (
    "Hey there! 👋 I'm Eighteenot — your personal Virat Kohli expert! 🏏\n\n"
    "Ask me anything about King Kohli — his centuries, records, stats, "
    "career journey, IPL performances, World Cups, or legendary innings! 🔥"
)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="kohli-header">
    <h1>🏏 EIGHTEENOT</h1>
    <p>Your AI-powered Virat Kohli Assistant</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ─────────────────────────────────────────────
# LOAD CHATBOT
# ─────────────────────────────────────────────
# with st.spinner("🏏 Initializing Eighteenot AI..."):
#     chain = load_chatbot()

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": WELCOME_MESSAGE
        }
    ]

# ─────────────────────────────────────────────
# CHATBOT SESSION
# ─────────────────────────────────────────────
if "chain" not in st.session_state:
    st.session_state.chain = None

# ─────────────────────────────────────────────
# CHAT HISTORY
# ─────────────────────────────────────────────
for message in st.session_state.messages:

    if message["role"] == "user":
        with st.chat_message("user", avatar="🧑"):
            st.write(message["content"])

    else:
        with st.chat_message("assistant", avatar="🏏"):
            st.write(message["content"])

# ─────────────────────────────────────────────
# SUGGESTED QUESTIONS
# ─────────────────────────────────────────────
if len(st.session_state.messages) == 1:

    st.markdown("### 💡 Try Asking")

    suggestions = [
        "Who is Virat Kohli?",
        "Tell me about his first ODI century",
        "How many Test centuries does he have?",
        "What are Virat Kohli's IPL records?",
        "What is Virat Kohli's greatest innings?",
        "World Cup performances?"
    ]

    cols = st.columns(3)

    for i, suggestion in enumerate(suggestions):
        with cols[i % 3]:

            if st.button(
                suggestion,
                key=f"suggestion_{i}",
                use_container_width=True
            ):
                st.session_state.messages.append({
                    "role": "user",
                    "content": suggestion
                })
                if st.session_state.chain is None:
                    with st.spinner("🏏 Initializing Eighteenot AI..."):
                        st.session_state.chain = load_chatbot()

                with st.spinner("🏏 Thinking..."):
                    response = ask(st.session_state.chain, suggestion)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

                st.rerun()

# ─────────────────────────────────────────────
# CHAT INPUT
# ─────────────────────────────────────────────
if prompt := st.chat_input(
    "Ask anything about Virat Kohli..."
):

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user", avatar="🧑"):
        st.write(prompt)

    with st.chat_message("assistant", avatar="🏏"):

        if st.session_state.chain is None:
            with st.spinner("🏏 Initializing Eighteenot AI..."):
                st.session_state.chain = load_chatbot()

        with st.spinner("🏏 Thinking..."):
            response = ask(st.session_state.chain, prompt)

        st.write(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:

    st.markdown("## 🏏 EIGHTEENOT")

    st.markdown("""
### Ask About

- Career Journey
- ODI Statistics
- Test Records
- IPL Performances
- World Cup Campaigns
- Famous Innings
- Records & Milestones
""")

    st.divider()

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": WELCOME_MESSAGE
            }
        ]

        st.session_state.chain = None
        st.rerun()

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Built by Bhushan Khaire • Inspired by Virat Kohli 🏏
</div>
""", unsafe_allow_html=True)