
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.word2vec_engine import find_similar_sentence
import re

def answer_question(question, sentences, model=None):

    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf = vectorizer.fit_transform([question] + sentences)
    except ValueError:
        return "Text not suitable for QA"

    sim_scores = cosine_similarity(tfidf[0:1], tfidf[1:])
    
    top_indices = sim_scores[0].argsort()[-3:][::-1]
    tfidf_sentences = [sentences[i] for i in top_indices]

    main_answer = ""
    for sent in tfidf_sentences:
        if "conclusion" in sent.lower() or "proposed system" in sent.lower():
            main_answer = sent
            break

    if not main_answer:
        main_answer = " ".join(tfidf_sentences)

    return main_answer.strip()
