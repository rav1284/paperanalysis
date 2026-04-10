import networkx as nx
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import numpy as np

def clean_sentences(sentences):
    return [s.strip() for s in sentences if s.strip() and len(s.split()) > 2]

def summarize(sentences, top_n=5):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(sentences)

    similarity_matrix = cosine_similarity(tfidf_matrix)

    graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(graph)

    ranked = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)
    
    return " ".join([s for _, s in ranked[:top_n]])

def summarize_text(text, min_words=50, max_words=120):
    if not text or not text.strip():
        return "No content found"

    text = " ".join(text.split()[:2000])

    sentences = re.split(r'(?<=[.!?])\s+', text)

    sentences = [s.strip() for s in sentences if len(s.split()) > 6]

    if len(sentences) == 0:
        return "No meaningful sentences found"

    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf = vectorizer.fit_transform(sentences)
    except ValueError:
        return "Text not suitable for summarization"

    similarity = cosine_similarity(tfidf)

    scores = similarity.sum(axis=1)

    scores = scores / np.max(scores)

    n = len(sentences)
    position_weight = np.array([
        1.2 if i < n * 0.2 else (1.1 if i > n * 0.8 else 1.0)
        for i in range(n)
    ])

    final_scores = scores * position_weight

    ranked = sorted(
        [(final_scores[i], i, s) for i, s in enumerate(sentences)],
        reverse=True
    )

    selected = []
    word_count = 0
    used_indices = set()

    for score, idx, sentence in ranked:
        words = sentence.split()

        if word_count + len(words) > max_words:
            continue

        if any(abs(idx - u) < 2 for u in used_indices):
            continue

        selected.append((idx, sentence))
        used_indices.add(idx)
        word_count += len(words)

        if word_count >= min_words:
            break

    if not selected:
        return "Could not generate meaningful summary"

    selected = sorted(selected, key=lambda x: x[0])

    summary = " ".join([s for _, s in selected])

    return summary

def generate_suggestions(conclusion_text):
    if not conclusion_text.strip():
        return "No conclusion found"

    sentences = re.split(r'(?<=[.!?]) +', conclusion_text)

    suggestions = []

    keywords = [
        "should", "can be improved", "future", "recommend",
        "suggest", "needs to", "could be", "further research", "conclusions"
    ]

    for sent in sentences:
        if any(k in sent.lower() for k in keywords):
            suggestions.append(sent.strip())

    if not suggestions:
        suggestions = sentences[:3]

    return " ".join(suggestions)