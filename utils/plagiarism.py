from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def get_sentence_vector(text, model):
    words = text.lower().split()
    word_vectors = []

    for word in words:
        if word in model.wv:
            word_vectors.append(model.wv[word])

    if len(word_vectors) == 0:
        return np.zeros(model.vector_size)

    return np.mean(word_vectors, axis=0)


def check_plagiarism(text1, text2, model=None):
    # TF-IDF similarity
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([text1, text2])
    tfidf_score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

    # Word2Vec similarity
    if model:
        vec1 = get_sentence_vector(text1, model)
        vec2 = get_sentence_vector(text2, model)

        w2v_score = cosine_similarity([vec1], [vec2])[0][0]
    else:
        w2v_score = 0

    # Final hybrid score (average)
    final_score = (tfidf_score + w2v_score) / 2

    return final_score