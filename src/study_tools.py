import random
import nltk
from nltk.tokenize import sent_tokenize
import streamlit as st
from transformers import pipeline


@st.cache_resource
def get_generator():
    return pipeline(
        "text2text-generation",   # ✅ FIXED (correct task)
        model="google/flan-t5-small"
    )


def generate_flashcards(text, num_cards=5):

    if not text.strip():
        return "No content available."

    generator = get_generator()

    MAX_INPUT_CHARS = 1500
    safe_text = text[:MAX_INPUT_CHARS]

    prompt = f"""Create {num_cards} concise study flashcards...
Text:
{safe_text}
"""

    output = generator(
        prompt,
        max_length=512,
        do_sample=False
    )[0]['generated_text']

    if "Card 1:" not in output:
        return """Card 1:
Title: Key Concept
Point 1: Core idea summary
Point 2: Important supporting detail
Point 3: Practical implication"""

    return output


def generate_quiz(text, num_questions=5):

    sentences = sent_tokenize(text)

    if not sentences:
        return "No content available."

    candidates = [s for s in sentences if 40 < len(s) < 160]

    if len(candidates) < num_questions:
        candidates = sentences[:num_questions]

    selected = candidates[:num_questions]

    quiz_output = []

    for i, sentence in enumerate(selected, start=1):

        question = f"Q{i}: What is meant by:\n\"{sentence}\""

        correct = sentence

        distractors = random.sample(
            sentences,
            k=min(3, max(1, len(sentences) - 1))
        )

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
