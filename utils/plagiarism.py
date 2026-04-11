from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re

def get_sentence_vector(text, model):
    words = text.lower().split()
    word_vectors = []

    for word in words:
        if word in model.wv:
            word_vectors.append(model.wv[word])

    if len(word_vectors) == 0:
        return np.zeros(model.vector_size)

    return np.mean(word_vectors, axis=0)

def check_plagiarism(input_text, document_text, Model=None):
    sentences = re.split(r'(?<=[.!?])\s+', document_text)
    sentences = [s.strip() for s in sentences if len(s.split()) > 3]

    best_score = 0
    best_sentence = ""

    for sent in sentences:
        try:
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf = vectorizer.fit_transform([input_text, sent])
            tfidf_score = cosine_similarity(tfidf)[0][1]

            if Model:
                vec1 = get_sentence_vector(input_text, Model)
                vec2 = get_sentence_vector(sent, Model)
                w2v_score = cosine_similarity([vec1], [vec2])[0][0]
            else:
                w2v_score = 0

            final_score = (tfidf_score + w2v_score) / 2

            if final_score > best_score:
                best_score = final_score
                best_sentence = sent

        except:
            continue

    return best_score, best_sentence