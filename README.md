# 🎙 Lecture Voice-to-Notes Generator
### AI-Powered Lecture Transcription & Intelligent Structured Notes System

---

## 🧠 System Architecture

<p align="center">
  <img src="assets/architecture.jpg" width="100%" />
</p>

---

## 🚀 Overview

The **Lecture Voice-to-Notes Generator** is an end-to-end AI system that converts lecture audio into structured, study-ready notes using Automatic Speech Recognition (ASR) and Natural Language Processing (NLP).

This project demonstrates practical implementation of:

- Speech-to-Text using Whisper
- Transformer-based summarization
- Sentence embeddings
- Unsupervised topic clustering
- Keyword extraction
- Structured note generation
- Study tools & export functionality

Designed as an **AIML internship-level project**, it showcases real-world ML pipeline engineering and model integration.

---

## 🔄 Processing Pipeline

1. **Input Layer**
   - WAV / MP3 / M4A audio upload
   - Streamlit interface

2. **ASR Layer**
   - Faster-Whisper (CTranslate2 backend)
   - Speech-to-text conversion

3. **Transcript Layer**
   - Full transcript generation
   - Text preprocessing

4. **NLP Intelligence**
   - Summarization (T5/BART)
   - Keyword extraction (TF-IDF)
   - Topic detection (KMeans clustering)
   - Sentence embeddings (MiniLM)

5. **Knowledge Layer**
   - Structured notes generation
   - Concept grouping
   - Important sentence ranking

6. **Export & Study Tools**
   - PDF export
   - DOCX export
   - Flashcards & Quiz generation

---

## 🛠 Tech Stack

### Core
- Python
- Streamlit

### Speech Recognition
- faster-whisper
- CTranslate2

### NLP
- Transformers (T5 / BART)
- Sentence-Transformers (MiniLM)
- Scikit-learn
- NumPy

### Export
- ReportLab
- python-docx

---

## 📂 Project Structure
