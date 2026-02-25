from click import style
import streamlit as st
st.write("✅ App started")
import tempfile
st.write("✅ Imports successful")
import os
import time

from src.asr import transcribe_audio
from src.nlp_pipeline import summarize_text, extract_keywords, detect_topics
from src.notes_engine import build_topic_map, generate_structured_notes, smart_notes
from src.study_tools import generate_flashcards, generate_quiz
from src.export_utils import export_to_pdf, export_to_docx



# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AI Voice Intelligence System",
    page_icon="🎙",
    layout="wide"
)

st.markdown("""
<style>

/* Expand tab list across full width */
div[data-baseweb="tab-list"] {
    justify-content: flex-start !important;
    width: 100% !important;
}

/* Remove weird centering constraints */
div[data-baseweb="tab-list"] > div {
    width: 100% !important;
}

/* Increase tab font */
button[data-baseweb="tab"] p {
    font-size: 20px !important;
    font-weight: 600 !important;
}

/* Optional: reduce side padding if tabs feel shifted */
.block-container {
    max-width: 100% !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
}
/* Center content inside each tab */
button[data-baseweb="tab"] {
    display: flex !important;
    justify-content: center !important;
}

/* Center the label wrapper */
button[data-baseweb="tab"] > div {
    display: flex !important;
    justify-content: center !important;
    width: 100% !important;
}

/* Center the actual text */
button[data-baseweb="tab"] p {
    text-align: center !important;
    width: 100% !important;
    font-size: 20px !important;
    font-weight: 600 !important;
}

</style>
""", unsafe_allow_html=True)

st.title("🎙 AI Voice Intelligence & Knowledge Extraction System: Audio to Notes Generator")
st.markdown("Convert speech into structured knowledge, summaries, quizzes and flashcards.")


# -----------------------------
# Session State Initialization
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
    [
        "Base (Fastest)",
        "Small (Balanced)"
    ]
)

model_map = {
    "Base (Fastest)": "base",
    "Small (Balanced)": "small"
}

model_size = model_map[model_choice]

generate_btn = st.sidebar.button("Generate Insights")


# -----------------------------
# Audio Handling
# -----------------------------
if uploaded_file:
    st.subheader("Uploaded Audio")
    st.audio(uploaded_file)

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        audio_path = tmp_file.name


# -----------------------------
# Processing (ONLY on button)
# -----------------------------
if uploaded_file and generate_btn:

    with st.spinner("Go through the audio while we transcribe..."):
        segments, info, full_text, inference_time = transcribe_audio(
            audio_path,
            model_size=model_size
        )

    with st.spinner("Almost there generating AI insights..."):
        summary = summarize_text(full_text)
        keywords = extract_keywords(full_text)
        topics, sentences = detect_topics(full_text)

        topic_map = build_topic_map(sentences, topics)
        structured_notes = generate_structured_notes(topic_map)
        smart_notes_output = smart_notes(sentences, topics)

        flashcards = generate_flashcards(full_text)
        quiz = generate_quiz(full_text)

    # Store results
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

    # -----------------------------
    # Build Full AI Report Content
    # -----------------------------
    report_content = f"""
Note: This is an AI-generated report based on the audio file "{r['audio_name']}". The content is structured into sections for easy review and study.

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

    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Detected Language", r["info"].language)
    col2.metric("Inference Time (sec)", r["inference_time"])
    col3.metric("Transcript Length", len(r["full_text"]))

    tabs = st.tabs([
        "Transcript",
        "Structured Notes",
        "Smart Notes",
        "Summary",
        "Keywords",
        "Flashcards",
        "Quiz",
        "Export"
        
    ])

    # Transcript
    with tabs[0]:
        for seg in r["segments"]:
            st.write(f"**[{seg.start:.2f}s → {seg.end:.2f}s]** {seg.text}")

    # Notes
    with tabs[1]:
        st.text(r["structured_notes"])

    with tabs[2]:
        st.text(r["smart_notes"])

    # Summary
    with tabs[3]:
        st.write(r["summary"])

    # Keywords
    with tabs[4]:
        for word, score in r["keywords"]:
            st.write(f"**{word}** — {round(score, 3)}")

    # Flashcards
    with tabs[5]:
        st.markdown("### Study Flashcards")

        notes = r["structured_notes"].split("\n")

        flashcards = []
        current_topic = None
        current_points = []

        for line in notes:

            if line.startswith("##"):
                if current_topic:
                    flashcards.append((current_topic, current_points))

                current_topic = line.replace("##", "").strip().title()
                current_points = []

            elif line.startswith("•"):
                current_points.append(line.replace("•", "").strip())

        if current_topic:
            flashcards.append((current_topic, current_points))

        colors = ["#1E88E5", "#43A047", "#E53935", "#8E24AA", "#FB8C00"]

        cols = st.columns([1,1,1])

        for i, (topic, points) in enumerate(flashcards):

            color = colors[i % len(colors)]

            with cols[i % 3]:
                st.markdown(
                    f"""
                    <div style="
                        padding:16px;
                        border-radius:14px;
                        margin-bottom:15px;
                        background-color:{color};
                        min-height:140px;
                        color:white;
                    ">
                        <h4>{topic}</h4>
                        <p style="font-size:13px;">
                            {"<br>".join(points[:3])}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # -------------------------
    # ✅ Simplified Quiz Section
    # -------------------------
    with tabs[6]:
        st.subheader("❓ Quiz")
        st.markdown("### Generated MCQs")
        st.markdown(f"```\n{r['quiz']}\n```")

    # Export
    with tabs[7]:
        st.subheader("Export Full Report")

        pdf_path = "outputs/AI_Report.pdf"
        docx_path = "outputs/AI_Report.docx"

        os.makedirs("outputs", exist_ok=True)

        export_to_pdf(pdf_path, report_content)
        export_to_docx(docx_path, report_content)

        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button(
                    "⬇ Download PDF Report",
                    data=f.read(),
                    file_name="AI_Report.pdf",
                    mime="application/pdf"
                )

        if os.path.exists(docx_path):
            with open(docx_path, "rb") as f:
                st.download_button(
                    "⬇ Download DOCX Report",
                    data=f.read(),
                    file_name="AI_Report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
    



if uploaded_file and "audio_path" in locals():
    try:
        os.unlink(audio_path)
    except:
        pass