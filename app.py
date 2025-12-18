import streamlit as st

st.set_page_config(
    page_title="AI Cover Letter Bot",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -----------------------
# Custom CSS
# -----------------------
st.markdown("""
<style>

/* Page background */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: #f5f5f5;
}

/* Main container */
.block-container {
    max-width: 820px;
    padding-top: 2rem;
}

/* Title */
h1 {
    text-align: center;
    color: #ffffff;
    font-weight: 600;
}

/* Subheaders */
h2, h3 {
    color: #e5e7eb;
}

/* -------------------------
   Chat Message Styling
-------------------------- */

/* Chat bubble base */
.stChatMessage {
    padding: 0.8rem 1rem;
    border-radius: 12px;
    margin-bottom: 0.6rem;
    color: #ffffff !important; /* FORCE WHITE TEXT */
}

/* User bubble */
.stChatMessage.user {
    background-color: #1f2933;
    border-left: 4px solid #4f9cff;
}

/* Bot bubble */
.stChatMessage.assistant {
    background-color: #111827;
    border-left: 4px solid #22c55e;
}

/* Chat message text */
.stChatMessage p {
    color: #ffffff !important;
}

/* -------------------------
   Chat Input Styling
-------------------------- */

.stChatInput textarea {
    background-color: #0b1220 !important;
    color: #ffffff !important;
    border-radius: 10px;
    border: 1px solid #374151;
}

/* Placeholder text */
.stChatInput textarea::placeholder {
    color: #9ca3af !important;
}

/* -------------------------
   Text Inputs & Text Areas
-------------------------- */

input, textarea {
    background-color: #0b1220 !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    border: 1px solid #374151 !important;
}

/* -------------------------
   Buttons
-------------------------- */

button {
    background-color: #2563eb !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    font-weight: 500;
}

button:hover {
    background-color: #1d4ed8 !important;
}

/* Divider */
hr {
    border-color: #374151;
}

/* Download buttons spacing */
.stDownloadButton {
    margin-top: 0.5rem;
}

</style>
""", unsafe_allow_html=True)
from prompts import build_prompt
from llm_client import generate_cover_letter
from export_utils import export_pdf, export_word

st.set_page_config(page_title="AI Cover Letter Bot", layout="centered")
st.title("AI Cover Letter Assistant")
st.caption("A conversational AI bot that creates ATS-optimized cover letters")

# -------------------------------
# Initialize Session State SAFELY
# -------------------------------
if "state" not in st.session_state:
    st.session_state.state = {}

REQUIRED_KEYS = [
    "candidate_name",
    "company_name",
    "experience",
    "skills",
    "projects",
    "job_description",
    "focus"
]

for key in REQUIRED_KEYS:
    if key not in st.session_state.state:
        st.session_state.state[key] = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "cover_letter" not in st.session_state:
    st.session_state.cover_letter = None

# -------------------------------
# Chat UI
# -------------------------------
st.subheader("Candidate & Company Details")

col1, col2 = st.columns(2)

with col1:
    st.session_state.state["candidate_name"] = st.text_input(
        "Candidate Name",
        value=st.session_state.state.get("candidate_name", "")
    )

with col2:
    st.session_state.state["company_name"] = st.text_input(
        "Company Name",
        value=st.session_state.state.get("company_name", "")
    )

st.subheader("Chat with the Bot")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input(
    "Tell me about your experience, skills, or focus area…"
)

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    lower = user_input.lower()
    reply = "Noted."

    if "year" in lower:
        st.session_state.state["experience"] = user_input
        st.session_state.cover_letter = None
        reply = "Experience recorded."

    elif "," in user_input:
        st.session_state.state["skills"] = user_input
        st.session_state.cover_letter = None
        reply = "Skills captured."

    elif "project" in lower:
        st.session_state.state["projects"] = user_input
        reply = "Project details noted."

    elif "focus" in lower or "emphasize" in lower:
        st.session_state.state["focus"] = user_input
        reply = "Focus preference noted."

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    with st.chat_message("assistant"):
        st.write(reply)

# -------------------------------
# Job Description (Persistent)
# -------------------------------
st.divider()
st.subheader("Job Description")

jd_input = st.text_area(
    "Paste Job Description",
    value=st.session_state.state["job_description"],
    height=220
)

# Detect change and invalidate derived state
if jd_input != st.session_state.state["job_description"]:
    st.session_state.state["job_description"] = jd_input
    st.session_state.cover_letter = None

# -------------------------------
# Generate Cover Letter
# -------------------------------
ready = all([
    st.session_state.state.get("experience"),
    st.session_state.state.get("skills"),
    st.session_state.state.get("job_description")
])

if ready:
    st.divider()
    st.subheader("Generated Cover Letter")

    if st.session_state.cover_letter is None:
        prompt = build_prompt(st.session_state.state)
        st.session_state.cover_letter = generate_cover_letter(prompt)

    st.text_area(
        "",
        st.session_state.cover_letter,
        height=360
    )

    col1, col2 = st.columns(2)

    with col1:
        pdf_bytes = export_pdf(st.session_state.cover_letter)
        st.download_button(
            label="Download as PDF",
            data=pdf_bytes,
            file_name="cover_letter.pdf",
            mime="application/pdf"
        )

    with col2:
        word_bytes = export_word(st.session_state.cover_letter)
        st.download_button(
            label="Download as Word",
            data=word_bytes,
            file_name="cover_letter.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

# -------------------------------
# Reset Button
# -------------------------------
st.divider()
if st.button("Start New Conversation"):
    st.session_state.clear()
    st.rerun()
