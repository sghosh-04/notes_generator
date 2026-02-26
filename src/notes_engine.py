def generate_structured_notes(topic_map, max_sentences=5):
    """
    Generates structured notes grouped by topics.
    """

    if not topic_map:   # ✅ REQUIRED FIX (safety)
        return "No topics available."

    notes = []

    for topic, sentences in topic_map.items():
        if not sentences:
            continue

        notes.append(f"\n## {topic.upper()}")

        for sent in sentences[:max_sentences]:
            notes.append(f"• {sent}")

    return "\n".join(notes)


def build_topic_map(sentences, topics):
    """
    Maps sentences to detected topics.
    """

    if not sentences or not topics:   # ✅ REQUIRED FIX
        return {}

    topic_map = {topic: [] for topic in topics}

    for sentence in sentences:
        for topic in topics:
            if topic.lower() in sentence.lower():
                topic_map[topic].append(sentence)

    return topic_map


def smart_notes(sentences, topics):
    """
    Generates insight-style smart notes.
    """

    if not sentences or not topics:   # ✅ REQUIRED FIX
        return "No smart notes available."

    notes = []

    for topic in topics:
        related = [s for s in sentences if topic.lower() in s.lower()]

        if not related:
            continue

        notes.append(f"\n# {topic.title()}")

        notes.append("Key Points:")
        for r in related[:3]:
            notes.append(f"• {r}")

        notes.append("Insight:")
        notes.append(f"→ {related[0]}")

    return "\n".join(notes)
