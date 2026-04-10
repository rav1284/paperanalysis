from gensim.models import Word2Vec
import numpy as np

def train_word2vec(sentences):
    tokenized = [s.split() for s in sentences]
    model = Word2Vec(tokenized, vector_size=100, window=5, min_count=1)
    return model

def sentence_vector(model, sentence):
    words = sentence.split()
    vectors = [model.wv[w] for w in words if w in model.wv]

    if len(vectors) == 0:
        return np.zeros(100)

    return np.mean(vectors, axis=0)

def find_similar_sentence(question, sentences, model):
    q_vec = sentence_vector(model, question)

    similarities = []
    for sent in sentences:
        s_vec = sentence_vector(model, sent)
        sim = np.dot(q_vec, s_vec) / (np.linalg.norm(q_vec) * np.linalg.norm(s_vec) + 1e-9)
        similarities.append(sim)

    return sentences[np.argmax(similarities)]