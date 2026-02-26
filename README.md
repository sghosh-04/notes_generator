# 🎙 Lecture Voice-to-Notes Generator
### AI-Powered Lecture Transcription & Intelligent Structured Notes System

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

Designed as an **AIML internship-level project**, it showcases real-world ML pipeline engineering and model integration.

---

## 🧠 How It Works

Audio Input  
↓  
Whisper ASR (faster-whisper)  
↓  
Transcript Cleaning  
↓  
Sentence Segmentation  
↓  
TF-IDF Keyword Extraction  
↓  
Sentence Embeddings (MiniLM)  
↓  
KMeans Topic Clustering  
↓  
Transformer Summarization (T5)  
↓  
Structured Notes Output  

---

## ✨ Features

### 🎙 Automatic Speech Recognition
- High-quality transcription using Whisper
- Timestamped segments
- CPU compatible

### 🧠 Intelligent Notes Generation
- Automatic topic detection
- Sentence clustering into themes
- Important sentence ranking
- Definition extraction
- Clean structured headings

### 📚 Study Support
- Abstractive summary generation
- Chunked summarization for long lectures
- Keyword highlighting

---

## 🛠 Tech Stack

### Speech Recognition
- faster-whisper

### NLP & Transformers
- transformers (T5)
- sentence-transformers (MiniLM)
- scikit-learn

### Data Processing
- NumPy
- Regex-based text cleaning

### Evaluation
- jiwer (Word Error Rate)

---

## 📂 Project Structure
