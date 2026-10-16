
import json
import os
import urllib.request
import urllib.error

import streamlit as st

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


st.set_page_config(
    page_title="LearnPilot AI",
    page_icon="🎓",
    layout="wide",
)


def ask_ai(prompt, system_message):
    """Use Ollama locally by default, or OpenAI when configured."""
    provider = os.getenv("AI_PROVIDER", "ollama").lower()

    if provider == "openai":
        key = os.getenv("OPENAI_API_KEY")

        if not key or OpenAI is None:
            st.error("Configure OPENAI_API_KEY and install the openai package.")
            return None

        try:
            client = OpenAI(api_key=key)
            response = client.responses.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
                instructions=system_message,
                input=prompt,
            )
            return response.output_text
        except Exception as exc:
            st.error(f"OpenAI request failed: {exc}")
            return None

    model = os.getenv("OLLAMA_MODEL", "gemma3:1b")
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
    }

    request = urllib.request.Request(
        os.getenv("OLLAMA_HOST", "http://localhost:11434")
        + "/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            result = json.loads(response.read().decode("utf-8"))
        return result["message"]["content"]
    except Exception as exc:
        st.error(
            "Ollama could not respond. Check that Ollama is running "
            "and the configured model is installed."
        )
        with st.expander("Technical details"):
            st.code(str(exc))
        return None


st.sidebar.title("🎓 LearnPilot AI")
page = st.sidebar.radio(
    "Navigate",
    ["Home", "AI Tutor", "Smart Quiz", "Progress"],
)

if "questions_answered" not in st.session_state:
    st.session_state.questions_answered = 0
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0

st.title("🎓 LearnPilot AI")
st.caption("Your personal AI-powered learning companion")

if page == "Home":
    st.header("Welcome to LearnPilot AI!")
    st.write(
        "Learn concepts, practise with quizzes, and track your learning."
    )
    col1, col2, col3 = st.columns(3)
    col1.metric("Questions asked", st.session_state.questions_answered)
    col2.metric("Quiz points", st.session_state.quiz_score)
    col3.metric("AI provider", os.getenv("AI_PROVIDER", "ollama").title())

    st.info(
        "Local mode uses Ollama on your computer. "
        "For cloud deployment, configure a cloud-accessible AI provider."
    )

elif page == "AI Tutor":
    st.header("Ask your AI Tutor")
    subject = st.selectbox(
        "Choose a subject",
        ["General", "Mathematics", "Physics", "Chemistry", "Biology", "Computer Science"],
    )
    level = st.selectbox(
        "Explanation level",
        ["Beginner", "School", "College"],
    )
    question = st.text_area(
        "What would you like to learn?",
        placeholder="Example: Explain photosynthesis in simple words.",
    )

    if st.button("Explain", type="primary"):
        if not question.strip():
            st.warning("Please enter a question first.")
        else:
            with st.spinner("Preparing your explanation..."):
                answer = ask_ai(
                    f"Subject: {subject}\nLevel: {level}\nQuestion: {question}",
                    "You are LearnPilot AI, a patient educational tutor. "
                    "Explain concepts clearly with examples. If uncertain, say so.",
                )
            if answer:
                st.markdown("### Explanation")
                st.write(answer)
                st.session_state.questions_answered += 1

elif page == "Smart Quiz":
    st.header("Quick knowledge check")
    st.write("Answer this sample science question.")

    answer = st.radio(
        "Which process do plants use to make food?",
        ["Respiration", "Photosynthesis", "Digestion", "Evaporation"],
        index=None,
    )

    if st.button("Check answer"):
        if answer is None:
            st.warning("Choose an answer first.")
        elif answer == "Photosynthesis":
            st.success("Correct! Plants use photosynthesis to make food.")
            st.session_state.quiz_score += 1
        else:
            st.error("Not quite. The correct answer is Photosynthesis.")

elif page == "Progress":
    st.header("Your learning progress")
    st.metric("Questions answered this session", st.session_state.questions_answered)
    st.metric("Correct quiz answers this session", st.session_state.quiz_score)
    st.caption("This starter version keeps progress for the current session only.")
