import streamlit as st
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize


@st.cache_resource
def load_nltk():
    nltk.download('punkt')

load_nltk()


# -----------------------------
# Summarization
# -----------------------------
@st.cache_resource
def get_generator():
    return pipeline(
        "any-to-any",                 # ✅ REQUIRED FIX (Cloud-safe)
        model="google/flan-t5-small"
    )


def chunk_text(text, chunk_size=250):  # ✅ REQUIRED FIX (safer size)
    """
    Splits text into word-based chunks.
    Prevents transformer token overflow.
    """
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def summarize_text(text, max_len=80):

    if not text or len(text.split()) < 30:
        return "Text too short to summarize."

    summarizer = get_generator()

    chunks = chunk_text(text)
    summaries = []

    for chunk in chunks:
        result = summarizer(
            f"summarize: {chunk}",
            max_length=max_len,
            do_sample=False
        )
        summaries.append(result[0]["generated_text"])

    return " ".join(summaries)


# -----------------------------
# Keyword Extraction
# -----------------------------
def extract_keywords(text, top_n=10):

    if not text.strip():              # ✅ REQUIRED FIX (prevents crash)
        return []

    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform([text])

    features = vectorizer.get_feature_names_out()
    scores = np.asarray(X.sum(axis=0)).ravel()

    ranked = sorted(zip(features, scores), key=lambda x: x[1], reverse=True)

    return ranked[:top_n]


# -----------------------------
# Topic Detection
# -----------------------------
def detect_topics(text, top_n=5):

    if not text.strip():              # ✅ REQUIRED FIX (prevents crash)
        return [], []

    sentences = sent_tokenize(text)

    if len(sentences) < 2:            # ✅ REQUIRED FIX (sklearn safety)
        return [], sentences

    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(sentences)

    features = vectorizer.get_feature_names_out()
    scores = np.asarray(X.sum(axis=0)).ravel()

    ranked_topics = sorted(
        zip(features, scores),
        key=lambda x: x[1],
        reverse=True
    )

    top_topics = [topic for topic, _ in ranked_topics[:top_n]]

    return top_topics, sentences
