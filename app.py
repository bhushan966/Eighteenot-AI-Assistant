import warnings
warnings.filterwarnings("ignore")

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from dotenv import load_dotenv
from chatbot import initialize_Eighteenot, ask

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
    .main { background-color: #0f0f0f; }
    .stApp { background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 100%); }
    
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

    .stats-bar {
        display: flex;
        justify-content: center;
        gap: 30px;
        padding: 15px;
        background: rgba(255,255,255,0.04);
        border-radius: 12px;
        margin: 15px 0;
        flex-wrap: wrap;
    }
    .stat-item {
        text-align: center;
    }
    .stat-num {
        font-size: 1.4rem;
        font-weight: 700;
        color: #f5a623;
    }
    .stat-label {
        font-size: 0.7rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .chat-bubble-user {
        background: linear-gradient(135deg, #e8173a, #c0102b);
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
        font-size: 0.95rem;
    }
    .chat-bubble-bot {
        background: rgba(255,255,255,0.06);
        color: #f0f0f0;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        max-width: 85%;
        font-size: 0.95rem;
        border: 1px solid rgba(255,255,255,0.08);
    }

    .suggestion-btn {
        background: rgba(245, 166, 35, 0.1);
        border: 1px solid rgba(245, 166, 35, 0.3);
        border-radius: 20px;
        padding: 6px 14px;
        color: #f5a623;
        font-size: 0.82rem;
        cursor: pointer;
        margin: 4px;
    }

    div[data-testid="stTextInput"] input {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 25px !important;
        color: white !important;
        padding: 12px 20px !important;
    }

    .footer {
        text-align: center;
        color: #444;
        font-size: 0.75rem;
        padding: 20px 0 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# INITIALIZE CHATBOT (cached)
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_chatbot():
    return initialize_Eighteenot()

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="kohli-header">
    <h1>🏏 EIGHTEENOT</h1>
    <p>Your AI-powered Virat Kohli cricket assistant</p>
</div>
""", unsafe_allow_html=True)

# Stats bar
st.markdown("""
<div class="stats-bar">
    <div class="stat-item">
        <div class="stat-num">85</div>
        <div class="stat-label">International Centuries</div>
    </div>
    <div class="stat-item">
        <div class="stat-num">14,797</div>
        <div class="stat-label">ODI Runs</div>
    </div>
    <div class="stat-item">
        <div class="stat-num">58.72</div>
        <div class="stat-label">ODI Average</div>
    </div>
    <div class="stat-item">
        <div class="stat-num">9,230</div>
        <div class="stat-label">Test Runs</div>
    </div>
    <div class="stat-item">
        <div class="stat-num">9,336</div>
        <div class="stat-label">IPL Runs</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ─────────────────────────────────────────────
# LOAD CHATBOT
# ─────────────────────────────────────────────
with st.spinner("🏏 Loading KohliBot..."):
    chain = load_chatbot()

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hey there! 👋 I'm Eighteenot — your personal Virat Kohli expert! 🏏\n\nAsk me anything about King Kohli — his centuries, records, stats, personal life, or legendary innings! 🔥"
    })

# ─────────────────────────────────────────────
# SUGGESTED QUESTIONS
# ─────────────────────────────────────────────
if len(st.session_state.messages) == 1:
    st.markdown("**💡 Try asking:**")
    suggestions = [
        "Who is Virat Kohli?",
        "Tell me about his first ODI century",
        "How many Test centuries does he have?",
        "What are his IPL stats?",
        "His best innings ever?",
        "World Cup performances?",
    ]
    cols = st.columns(3)
    for i, suggestion in enumerate(suggestions):
        with cols[i % 3]:
            if st.button(suggestion, key=f"sug_{i}", use_container_width=True):
                st.session_state.messages.append({
                    "role": "user",
                    "content": suggestion
                })
                with st.spinner("🏏 Thinking..."):
                    response = ask(chain, suggestion)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })
                st.rerun()

st.markdown("")

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
# CHAT INPUT
# ─────────────────────────────────────────────
if prompt := st.chat_input("Ask anything about Virat Kohli..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.write(prompt)

    with st.chat_message("assistant", avatar="🏏"):
        with st.spinner("🏏 Thinking..."):
            response = ask(chain, prompt)
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Built by Bhushan Khaire "Die heart fan of Virat Kohli" | EIGHTEENOT 🏏
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🏏 Eighteenot")
    st.markdown("AI cricket assistant powered by RAG")
    st.divider()
    st.markdown("**🔧 Tech Stack**")
    st.markdown("- LangChain + LangSmith")
    st.markdown("- Groq LLM")
    st.markdown("- FAISS Vector Store")
    st.markdown("- HuggingFace Embeddings")
    st.markdown("- Streamlit UI")
    st.divider()
    st.markdown("**📊 Knowledge Base**")
    st.markdown("- Wikipedia biography")
    st.markdown("- Tavily web search")
    st.markdown("- 84,000+ characters of data")
    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()