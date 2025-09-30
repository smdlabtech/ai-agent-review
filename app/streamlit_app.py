import os
import streamlit as st
from dotenv import load_dotenv

from src.agent_builder import SmartAgent

load_dotenv()

st.set_page_config(page_title="AI Agent Review", page_icon="🧠", layout="wide")

st.title("🧠 AI Agent Review - Chatbot")
st.caption("Streamlit · OpenAI / Gemini · Memory (buffer) · Cloud Run-ready")

with st.sidebar:
    st.header("⚙️ Configuration")
    provider = st.selectbox("Provider", ["gemini", "openai"], index=0)
    model = st.text_input("Model", value=os.getenv("GEMINI_MODEL" if provider=="gemini" else "OPENAI_MODEL", "gemini-1.5-flash"))
    st.markdown("---")
    st.write("🔐 Assurez-vous d'avoir configuré votre `.env`.")
    st.code("cp .env.example .env")
    st.markdown("---")
    st.write("💡 Astuce: gardez `temperature` faible pour des réponses stables.")

if "agent" not in st.session_state or st.session_state.get("provider") != provider or st.session_state.get("model") != model:
    st.session_state["agent"] = SmartAgent(tools=[], memory="short_term", planner="reactive",
                                           provider_name=provider, model=model)
    st.session_state["provider"] = provider
    st.session_state["model"] = model

# Chat UI
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

user_input = st.chat_input("Posez votre question à l'agent…")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Réflexion de l'agent…"):
            try:
                reply = st.session_state.agent.run(user_input)
            except Exception as e:
                reply = f"❌ Erreur: {e}"
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})