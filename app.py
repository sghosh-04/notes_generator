import streamlit as st
import tempfile
import os
import time
import re   # ✅ FIXED

# -----------------------------
# Page Config (FIRST)
# -----------------------------
st.set_page_config(
    page_title="AI Voice Intelligence System",
    page_icon="🎙",
    layout="wide"
)

# ✅ Optional: Slightly bigger tabs
st.markdown("""
<style>
button[data-baseweb="tab"] p {
    font-size: 18px !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🎙 AI Voice Intelligence & Knowledge Extraction System")
st.markdown("Convert speech into structured knowledge, summaries, quizzes and flashcards.")

from src.asr import transcribe_audio
from src.nlp_pipeline import summarize_text, extract_keywords, detect_topics
from src.notes_engine import build_topic_map, generate_structured_notes, smart_notes
from src.study_tools import generate_flashcards, generate_quiz
from src.export_utils import export_to_pdf, export_to_docx

# -----------------------------
# Session State
# -----------------------------
if "results" not in st.session_state:
    st.session_state.results = None

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("⚙ Controls")

uploaded_file = st.sidebar.file_uploader(
    "Upload Audio File",
    type=["wav", "mp3", "m4a"]
)

model_choice = st.sidebar.selectbox(
    "Select Whisper Model",
    ["Base (Fastest)", "Small (Balanced)"]
)

model_map = {
    "Base (Fastest)": "base",
    "Small (Balanced)": "small"
}

model_size = model_map[model_choice]

generate_btn = st.sidebar.button("🚀 Generate Insights")

# -----------------------------
# Audio Handling
# -----------------------------
audio_path = None

if uploaded_file:
    st.subheader("🎧 Uploaded Audio")
    st.audio(uploaded_file)

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        audio_path = tmp_file.name

# -----------------------------
# Processing
# -----------------------------
if uploaded_file and generate_btn and audio_path:

    with st.spinner("🧠 Transcribing audio..."):
        segments, info, full_text, inference_time = transcribe_audio(
            audio_path,
            model_size=model_size
        )

    with st.spinner("✨ Generating AI insights..."):
        summary = summarize_text(full_text)
        keywords = extract_keywords(full_text)
        topics, sentences = detect_topics(full_text)

        topic_map = build_topic_map(sentences, topics)
        structured_notes = generate_structured_notes(topic_map)
        smart_notes_output = smart_notes(sentences, topics)

        flashcards = generate_flashcards(full_text)
        quiz = generate_quiz(full_text)

    st.session_state.results = {
        "segments": segments,
        "info": info,
        "full_text": full_text,
        "summary": summary,
        "keywords": keywords,
        "structured_notes": structured_notes,
        "smart_notes": smart_notes_output,
        "flashcards": flashcards,
        "quiz": quiz,
        "audio_name": uploaded_file.name,
        "inference_time": inference_time
    }

    st.rerun()

# -----------------------------
# Display Results
# -----------------------------
if st.session_state.results:

    r = st.session_state.results

    report_content = f"""
Note: AI-generated report based on "{r['audio_name']}".

SUMMARY
{r['summary']}

STRUCTURED NOTES
{r['structured_notes']}

SMART NOTES
{r['smart_notes']}

FLASHCARDS
{r['flashcards']}

QUIZ
{r['quiz']}
"""

    col1, col2, col3 = st.columns(3)
    col1.metric("🌐 Detected Language", r["info"].language)
    col2.metric("⏱ Inference Time (sec)", round(r["inference_time"], 2))
    col3.metric("📝 Transcript Length", len(r["full_text"]))

    tabs = st.tabs([
        "📝 Transcript",
        "📌 Structured Notes",
        "🧠 Smart Notes",
        "📊 Summary",
        "🔑 Keywords",
        "📚 Flashcards",
        "❓ Quiz",
        "📥 Export"
    ])

    with tabs[0]:
        for seg in r["segments"]:
            st.write(f"**[{seg.start:.2f}s → {seg.end:.2f}s]** {seg.text}")

    with tabs[1]:
        st.text(r["structured_notes"])

    with tabs[2]:
        st.text(r["smart_notes"])

    with tabs[3]:
        st.write(r["summary"])

    with tabs[4]:
        for word, score in r["keywords"]:
            st.write(f"**{word}** — {round(score, 3)}")

    with tabs[5]:
        st.markdown("### 📚 Study Flashcards")

        raw_cards = r["flashcards"]
        card_blocks = re.split(r"\n(?=Card\s\d+:)", raw_cards)

        colors = ["#1E88E5", "#43A047", "#E53935", "#8E24AA", "#FB8C00"]
        cols = st.columns(3)

        for i, block in enumerate(card_blocks):

            if not block.strip():
                continue

            lines = [l.strip() for l in block.split("\n") if l.strip()]

            title = None
            points = []

            for line in lines:
                if line.startswith("Title:"):
                    title = line.replace("Title:", "").strip()

                elif line.startswith("Point"):
                    points.append(line.split(":", 1)[1].strip())

            if title:
                color = colors[i % len(colors)]

                with cols[i % 3]:
                    st.markdown(
                        f"""
                        <div style="
                            background-color:{color};
                            padding:18px;
                            border-radius:16px;
                            margin-bottom:15px;
                            color:white;
                        ">
                            <h4>📌 {title}</h4>
                            <p>{"<br>".join(points[:3])}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    with tabs[6]:
        st.text(r["quiz"])

    with tabs[7]:
        os.makedirs("outputs", exist_ok=True)

        pdf_path = "outputs/AI_Report.pdf"
        docx_path = "outputs/AI_Report.docx"

        export_to_pdf(pdf_path, report_content)
        export_to_docx(docx_path, report_content)

        with open(pdf_path, "rb") as f:
            st.download_button("⬇ Download PDF", f.read(), "AI_Report.pdf")

        with open(docx_path, "rb") as f:
            st.download_button("⬇ Download DOCX", f.read(), "AI_Report.docx")

# -----------------------------
# Cleanup Temp File
# -----------------------------
if audio_path and os.path.exists(audio_path):
    try:
        os.unlink(audio_path)
    except:
        pass
