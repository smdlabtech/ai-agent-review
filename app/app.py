# --- Supprime les warnings gRPC/ALTS *avant* tout import Google/gRPC ---
import os
os.environ.setdefault("GRPC_VERBOSITY", "ERROR")   # gRPC: afficher seulement les erreurs
os.environ.setdefault("GLOG_minloglevel", "2")     # Abseil/GLOG: ERROR et plus

import json
import streamlit as st
from dotenv import load_dotenv

from src.agent_builder import SmartAgent

# Charge les variables d'environnement (.env)
load_dotenv()

# ---------------- UI & Config ----------------
st.set_page_config(page_title="AI Agent Review", page_icon="🧠", layout="wide")

st.title("🧠 AI Agent Review - Chatbot")
st.caption("Streamlit · OpenAI / Gemini · Memory (buffer) · Cloud Run-ready")

with st.sidebar:
    st.header("⚙️ Configuration")

    provider = st.selectbox("Provider", ["gemini", "openai"], index=0)

    # Valeur par défaut du modèle selon le provider + .env
    default_model = (
        os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        if provider == "gemini"
        else os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    )
    model = st.text_input("Model", value=default_model)

    # Contrôles optionnels (appliqués après instanciation si supportés)
    temperature = st.slider("temperature", 0.0, 1.5, 0.2, 0.1)
    max_tokens = st.number_input(
        "max_tokens (réponse)", min_value=128, max_value=8192, value=1024, step=64
    )
    memory_mode = st.selectbox("Mémoire", ["short_term", "none"], index=0)

    st.markdown("---")
    st.write("🔐 Assurez-vous d'avoir configuré votre `.env`.")
    st.code("cp .env.example .env", language="bash")
    st.markdown("---")
    st.write("💡 Astuce: gardez `temperature` faible pour des réponses stables.")

    col_a, col_b = st.columns(2)
    with col_a:
        reset_chat = st.button("♻️ Réinitialiser la conversation", use_container_width=True)
    with col_b:
        reset_agent = st.button("🔄 Réinitialiser l’agent", use_container_width=True)

# ---------------- Session State & Reset ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if reset_chat:
    st.session_state.messages = []
    st.rerun()

# ---------------- Création / Recréation de l'agent ----------------
need_new_agent = (
    "agent" not in st.session_state
    or st.session_state.get("provider") != provider
    or st.session_state.get("model") != model
    or reset_agent
)

if need_new_agent:
    # Si tu utilises google.generativeai (Gemini), forcer REST évite gRPC et ALTS.
    if provider == "gemini":
        os.environ.setdefault("GENAI_TRANSPORT", "rest")  # à lire dans SmartAgent si applicable

    # IMPORTANT: ne pas passer temperature/max_tokens ici (rupture de signature)
    agent = SmartAgent(
        tools=[],                   # branche tes tools ici si besoin
        memory=memory_mode,         # "short_term" / "none"
        planner="reactive",         # ex: "plan_act_reflect" si dispo
        provider_name=provider,
        model=model,
    )

    # Couche de compatibilité : appliquer temperature/max_tokens si supportés
    applied = False
    try:
        if hasattr(agent, "set_generation_params") and callable(agent.set_generation_params):
            agent.set_generation_params(temperature=temperature, max_tokens=max_tokens)
            applied = True
        elif hasattr(agent, "configure") and callable(agent.configure):
            # Beaucoup de classes exposent une méthode configure(**kwargs)
            agent.configure(temperature=temperature, max_tokens=max_tokens)
            applied = True
        else:
            # Dernier recours : set d’attributs s’ils existent / sont acceptés
            setattr(agent, "temperature", temperature)
            setattr(agent, "max_tokens", max_tokens)
            applied = True
    except Exception:
        # On ignore proprement si l’agent ne supporte pas ces options
        applied = False

    st.session_state["agent"] = agent
    st.session_state["provider"] = provider
    st.session_state["model"] = model

    # Info discrète côté UI si l’application des paramètres a réussi/échoué
    with st.sidebar:
        if applied:
            st.caption("✅ Paramètres de génération appliqués à l’agent.")
        else:
            st.caption("ℹ️ Paramètres non pris en charge par SmartAgent (ignorés).")

# ---------------- Chat UI ----------------
# Historique
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Entrée utilisateur
user_input = st.chat_input("Posez votre question à l'agent…")

if user_input:
    # Affiche + stocke le message utilisateur
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Réponse de l'agent
    with st.chat_message("assistant"):
        with st.spinner("Réflexion de l'agent…"):
            try:
                reply = st.session_state.agent.run(user_input)

                # Si l'agent retourne un dict (citations, sources...), rendre proprement
                if not isinstance(reply, str):
                    reply = "```json\n" + json.dumps(reply, ensure_ascii=False, indent=2) + "\n```"
            except Exception as e:
                reply = f"❌ Erreur: {e}"

        st.markdown(reply)

    # Stocke la réponse
    st.session_state.messages.append({"role": "assistant", "content": reply})
