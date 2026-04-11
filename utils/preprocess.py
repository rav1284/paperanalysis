import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def preprocess(text):
    sentences = sent_tokenize(text)

    cleaned_sentences = []
    for sent in sentences:
        words = word_tokenize(sent.lower())
        words = [w for w in words if w.isalnum() and w not in stop_words]
        cleaned_sentences.append(" ".join(words))

    return sentences, cleaned_sentences