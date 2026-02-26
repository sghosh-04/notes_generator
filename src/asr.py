import streamlit as st
from faster_whisper import WhisperModel
import time


@st.cache_resource
def load_whisper_model(model_size):
    """
    Loads Faster-Whisper model ONCE per session.
    Prevents reload on every rerun.
    """
    return WhisperModel(
        model_size,
        device="cpu",          # Streamlit Cloud = CPU only
        compute_type="int8"    # 🔥 Huge RAM reduction
    )


def transcribe_audio(audio_path, model_size="base"):
    """
    Transcribes audio using Faster-Whisper.

    Returns:
        segments (list)
        info (metadata)
        full_text (str)
        inference_time (float)
    """

    model = load_whisper_model(model_size)

    start_time = time.time()

    segments, info = model.transcribe(audio_path)
    segments = list(segments)

    end_time = time.time()

    full_text = " ".join(seg.text for seg in segments)
    inference_time = round(end_time - start_time, 2)

    return segments, info, full_text, inference_time
