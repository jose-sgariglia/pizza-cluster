"""Tests for embedding_comparision utilities.

Example:
    ```bash
    uv run python -m pytest tests/test_embedding_comparision.py -v
    ```
"""

import numpy as np
import pytest

from src.utils.embedding_comparision import (
    cluster_kmeans,
    cluster_hdbscan,
    compute_clustering_metrics,
    compute_stability_metrics,
    compute_retrieval_metrics,
    normalize_embeddings,
    reduce_embeddings,
    compare_models_clustering,
)


@pytest.fixture
def sample_embeddings():
    """Generate sample embeddings for testing."""
    np.random.seed(42)
    n_samples, n_features = 100, 50
    # Create embeddings with some clustering structure
    X1 = np.random.randn(50, n_features) + np.array([1, 1] + [0] * (n_features - 2))
    X2 = np.random.randn(50, n_features) + np.array([-1, -1] + [0] * (n_features - 2))
    embeddings = np.vstack([X1, X2])
    return embeddings


def test_cluster_kmeans(sample_embeddings):
    """Test KMeans clustering."""
    labels, centroids = cluster_kmeans(sample_embeddings, n_clusters=2)

    assert labels.shape == (sample_embeddings.shape[0],)
    assert len(np.unique(labels)) == 2
    assert centroids.shape == (2, sample_embeddings.shape[1])


def test_cluster_hdbscan(sample_embeddings):
    """Test HDBSCAN clustering."""
    labels = cluster_hdbscan(sample_embeddings, min_cluster_size=5)

    assert labels.shape == (sample_embeddings.shape[0],)
    # May have noise points (label -1)
    assert len(np.unique(labels)) >= 1


def test_compute_clustering_metrics(sample_embeddings):
    """Test clustering metrics computation."""
    labels, _ = cluster_kmeans(sample_embeddings, n_clusters=2)
    metrics = compute_clustering_metrics(sample_embeddings, labels)

    # Check all metrics are present
    assert "silhouette" in metrics
    assert "davies_bouldin" in metrics
    assert "calinski_harabasz" in metrics

    # Check value ranges
    assert -1 <= metrics["silhouette"] <= 1
    assert metrics["davies_bouldin"] >= 0
    assert metrics["calinski_harabasz"] >= 0


def test_compute_stability_metrics(sample_embeddings):
    """Test stability metrics computation."""
    labels, _ = cluster_kmeans(sample_embeddings, n_clusters=2)
    stability = compute_stability_metrics(sample_embeddings, labels, bootstrap_iterations=3)

    # Check metrics exist
    assert "ari_mean" in stability
    assert "nmi_mean" in stability
    assert "bootstrap_iterations" in stability

    # Check value ranges
    assert -1 <= stability["ari_mean"] <= 1
    assert -1 <= stability["nmi_mean"] <= 1


def test_compute_retrieval_metrics(sample_embeddings):
    """Test retrieval metrics computation."""
    retrieval = compute_retrieval_metrics(sample_embeddings, k_values=[1, 5])

    # Check metrics exist
    assert "recall@1" in retrieval
    assert "recall@5" in retrieval
    assert "mrr" in retrieval

    # Check value ranges
    assert 0 <= retrieval["recall@1"] <= 1
    assert 0 <= retrieval["recall@5"] <= 1
    assert 0 <= retrieval["mrr"] <= 1


def test_normalize_embeddings(sample_embeddings):
    """Test L2 normalization."""
    normalized = normalize_embeddings(sample_embeddings, method="l2")

    # Check shape is preserved
    assert normalized.shape == sample_embeddings.shape

    # Check L2 norm is 1 for each sample
    norms = np.linalg.norm(normalized, axis=1)
    np.testing.assert_array_almost_equal(norms, np.ones(len(norms)))


def test_normalize_embeddings_zscore(sample_embeddings):
    """Test z-score normalization."""
    normalized = normalize_embeddings(sample_embeddings, method="zscore")

    # Check shape is preserved
    assert normalized.shape == sample_embeddings.shape

    # Check mean ≈ 0 and std ≈ 1
    assert np.abs(normalized.mean()) < 0.1
    assert np.abs(normalized.std() - 1.0) < 0.1


def test_reduce_embeddings(sample_embeddings):
    """Test PCA dimensionality reduction."""
    reduced = reduce_embeddings(sample_embeddings, method="pca", n_components=2)

    # Check output shape
    assert reduced.shape == (sample_embeddings.shape[0], 2)


def test_compare_models_clustering(sample_embeddings):
    """Test multi-model clustering comparison."""
    embeddings_dict = {
        "model_a": sample_embeddings,
        "model_b": sample_embeddings + np.random.randn(*sample_embeddings.shape) * 0.1,
    }

    comparison_df = compare_models_clustering(embeddings_dict, n_clusters_range=[2, 3])

    # Check DataFrame structure
    assert "model" in comparison_df.columns
    assert "n_clusters" in comparison_df.columns
    assert "silhouette" in comparison_df.columns

    # Check number of rows
    assert len(comparison_df) == 4  # 2 models × 2 k values


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

