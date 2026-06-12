import pytest
import numpy as np
import pandas as pd
from src.utils.topic_labeling import (
    extract_keywords_yake,
    calculate_ctfidf,
    get_cluster_representative_docs
)

@pytest.fixture
def sample_texts():
    return [
        "Pizza is a traditional Italian dish consisting of a flat base of dough.",
        "The Margherita pizza is typical of Naples and made with tomatoes and mozzarella.",
        "Clustering is the task of grouping a set of objects in such a way that objects in the same group are more similar.",
        "Data science uses scientific methods, processes, algorithms and systems to extract knowledge from data."
    ]

def test_extract_keywords_yake():
    text = "Pizza is delicious and Italian. I love eating pizza in Naples."
    # We might need to mock yake if it's not installed, but let's assume requirements are met
    try:
        keywords = extract_keywords_yake(text, top_n=2)
        assert isinstance(keywords, list)
    except ImportError:
        pytest.skip("yake not installed")

def test_calculate_ctfidf():
    docs_per_cluster = {
        0: "pizza mozzarella tomatoes dough naples",
        1: "clustering algorithms data science systems"
    }
    results = calculate_ctfidf(docs_per_cluster, top_n=2)
    assert 0 in results
    assert 1 in results
    assert len(results[0]) <= 2

def test_get_cluster_representative_docs():
    docs = ["Doc A", "Doc B", "Doc C"]
    embeddings = np.array([[1.0, 0.0], [0.1, 0.1], [10.0, 10.0]])
    center = np.array([0.0, 0.0])
    rep_docs = get_cluster_representative_docs(docs, embeddings, center, n=2)
    assert len(rep_docs) == 2
    assert rep_docs[0] == "Doc B"

def test_extract_keywords_textrank():
    text = "Pizza is delicious and Italian. I love eating pizza in Naples. It is a traditional dish."
    try:
        from src.utils.topic_labeling import extract_keywords_textrank
        keywords = extract_keywords_textrank(text, top_n=2)
        assert isinstance(keywords, list)
        assert len(keywords) > 0
    except ImportError:
        pytest.skip("pytextrank or spacy not installed")

def test_extract_keywords_keybert():
    from src.utils.topic_labeling import extract_keywords_keybert
    word_embeddings = {
        "pizza": np.array([1.0, 0.0]),
        "data": np.array([0.0, 1.0]),
        "science": np.array([0.1, 0.9])
    }
    cluster_embedding = np.array([0.0, 1.0]) # Orientato verso data/science
    keywords = extract_keywords_keybert([], cluster_embedding, word_embeddings, top_n=2)
    assert "data" in keywords
    assert "science" in keywords
    assert "pizza" not in keywords
