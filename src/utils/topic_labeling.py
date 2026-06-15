import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_keywords_yake(text: str, top_n: int = 10, language: str = "en") -> List[str]:
    import yake
    kw_extractor = yake.KeywordExtractor(lan=language, n=1, top=top_n, features=None)
    keywords = kw_extractor.extract_keywords(text)
    return [kw[0] for kw in keywords]

def extract_keywords_textrank(text: str, top_n: int = 10) -> List[str]:
    import pytextrank
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        from spacy.cli import download
        download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")
    
    if "textrank" not in nlp.pipe_names:
        nlp.add_pipe("textrank")
    doc = nlp(text)
    return [phrase.text for phrase in doc._.phrases[:top_n]]

def calculate_ctfidf(documents_per_cluster: Dict[int, str], top_n: int = 10) -> Dict[int, List[str]]:
    cluster_ids = list(documents_per_cluster.keys())
    corpus = [documents_per_cluster[cid] for cid in cluster_ids]
    
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(corpus)
    words = vectorizer.get_feature_names_out()
    
    results = {}
    for i, cid in enumerate(cluster_ids):
        row = tfidf_matrix.getrow(i).toarray()[0]
        top_indices = row.argsort()[-top_n:][::-1]
        results[cid] = [words[idx] for idx in top_indices]
    return results

def extract_keywords_keybert(cluster_docs: List[str], cluster_embedding: np.ndarray, word_embeddings: Dict[str, np.ndarray], top_n: int = 10) -> List[str]:
    """
    Simula KeyBERT: calcola la similarità tra l'embedding del cluster e quello delle singole parole.
    """
    words = list(word_embeddings.keys())
    embeddings = np.array([word_embeddings[w] for w in words])
    
    # Cosine similarity tra il cluster_embedding (1, D) e word_embeddings (N, D)
    similarities = cosine_similarity(cluster_embedding.reshape(1, -1), embeddings)[0]
    top_indices = similarities.argsort()[-top_n:][::-1]
    
    return [words[idx] for idx in top_indices]

def get_cluster_representative_docs(docs: List[str], embeddings: np.ndarray, center: np.ndarray, n: int = 5) -> List[str]:
    distances = np.linalg.norm(embeddings - center, axis=1)
    closest_indices = distances.argsort()[:n]
    return [docs[i] for i in closest_indices]
