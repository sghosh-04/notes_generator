import re
import os
import random
import nltk
from nltk.tokenize import sent_tokenize
os.environ["HF_HOME"] = "D:/hf_cache"
os.environ["TRANSFORMERS_CACHE"] = "D:/hf_cache"
from transformers import pipeline

# -----------------------------
# Load Local Text Generation Model
# -----------------------------
generator = pipeline(
    "text-generation",
    model="google/flan-t5-small"
)

# -----------------------------
# Flashcards
# -----------------------------

# -----------------------------
# Flashcards (Structured / Compact)
# -----------------------------
def generate_flashcards(text, num_cards=5):
    """
    Generates compact topic-based flashcards locally.
    """

    MAX_INPUT_CHARS = 1500
    safe_text = text[:MAX_INPUT_CHARS]

    prompt = f"""
Create {num_cards} concise study flashcards.

STRICT FORMAT — FOLLOW EXACTLY:

Card 1:
Title: <short topic name>
Point 1: <very short concept>
Point 2: <very short concept>
Point 3: <very short concept>

Card 2:
Title: <short topic name>
Point 1: <very short concept>
Point 2: <very short concept>
Point 3: <very short concept>

RULES:
- MAX 3 points per card
- Each point MUST be short (1 line)
- NO long explanations
- Titles must be short
- NO extra commentary

Text:
{safe_text}
"""

    output = generator(
        prompt,
        max_length=512,
        do_sample=False
    )[0]['generated_text']

    # ✅ Safety fallback
    if "Card 1:" not in output:
        return """Card 1:
Title: Key Concept
Point 1: Core idea summary
Point 2: Important supporting detail
Point 3: Practical implication"""

    return output

# -----------------------------
# Quiz / Questions
# -----------------------------
def generate_quiz(text, num_questions=5):

    sentences = sent_tokenize(text)

    # Filter usable sentences
    candidates = [
        s for s in sentences
        if 40 < len(s) < 160
    ]

    if len(candidates) < num_questions:
        candidates = sentences[:num_questions]

    selected = candidates[:num_questions]

    quiz_output = []

    for i, sentence in enumerate(selected, start=1):

        question = f"Q{i}: What is meant by:\n\"{sentence}\""

        correct = sentence

        distractors = random.sample(sentences, min(3, len(sentences)))
        options = [correct] + distractors
        random.shuffle(options)

        letters = ["A", "B", "C", "D"]

        quiz_output.append(question)

        correct_letter = None

        for letter, option in zip(letters, options):
            quiz_output.append(f"{letter}) {option}")
            if option == correct:
                correct_letter = letter

        quiz_output.append(f"Answer: {correct_letter}\n")

    return "\n".join(quiz_output)
