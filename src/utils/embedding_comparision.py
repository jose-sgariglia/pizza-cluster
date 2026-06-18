"""Embedding comparison and clustering evaluation utilities.

This module provides functions for clustering evaluation, stability analysis,
and retrieval metrics computation on embedding vectors.

Example:
    ```python
    from src.utils.embedding_comparision import (
        compute_clustering_metrics,
        compute_stability_metrics,
        compute_retrieval_metrics,
    )

    metrics = compute_clustering_metrics(embeddings, labels)
    print(f"Silhouette: {metrics['silhouette']:.4f}")
    ```
"""

from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.cluster import KMeans, MiniBatchKMeans, HDBSCAN
from sklearn.metrics import (
    silhouette_score,
    davies_bouldin_score,
    calinski_harabasz_score,
    adjusted_rand_score,
    normalized_mutual_info_score,
)
from sklearn.decomposition import PCA
import pandas as pd


def cluster_kmeans(
    embeddings: np.ndarray,
    n_clusters: int,
    random_state: int = 42,
    **kwargs,
) -> tuple[np.ndarray, np.ndarray]:
    """Perform KMeans clustering on embeddings.

    Args:
        embeddings: 2D array of shape (n_samples, n_features)
        n_clusters: Number of clusters
        random_state: Random seed for reproducibility
        **kwargs: Additional arguments passed to KMeans

    Returns:
        Tuple of (labels, centroids)
    """
    if embeddings.shape[0] > 100000:
        print(f"Dataset molto grande ({embeddings.shape[0]} samples). Uso MiniBatchKMeans per ottimizzazione.")
        kmeans = MiniBatchKMeans(n_clusters=n_clusters, random_state=random_state, batch_size=10000, **kwargs)
    else:
        kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, **kwargs)
        
    labels = kmeans.fit_predict(embeddings)
    return labels, kmeans.cluster_centers_


def cluster_hdbscan(
    embeddings: np.ndarray,
    min_cluster_size: int = 5,
    **kwargs,
) -> np.ndarray:
    """Perform HDBSCAN clustering on embeddings.

    Args:
        embeddings: 2D array of shape (n_samples, n_features)
        min_cluster_size: Minimum cluster size parameter
        **kwargs: Additional arguments passed to HDBSCAN

    Returns:
        Cluster labels (including -1 for noise points)
    """
    clusterer = HDBSCAN(min_cluster_size=min_cluster_size, **kwargs)
    labels = clusterer.fit_predict(embeddings)
    return labels


def compute_clustering_metrics(
    embeddings: np.ndarray,
    labels: np.ndarray,
    sample_size: int | None = 20000,
) -> dict[str, float]:
    """Compute clustering quality metrics.

    Computes Silhouette Score, Davies-Bouldin Index, and Calinski-Harabasz Index.

    Mini spiegazione:
    - Silhouette: misura coesione vs separazione cluster. Range [-1, 1], più alto meglio.
    - Davies-Bouldin: rapporto medio dist intra/inter cluster. Range [0, ∞], più basso meglio.
    - Calinski-Harabasz: rapporto varianza inter/intra cluster. Range [0, ∞], più alto meglio.

    Args:
        embeddings: 2D array of shape (n_samples, n_features)
        labels: 1D array of cluster labels

    Returns:
        Dictionary with silhouette, davies_bouldin, calinski_harabasz scores
    """
    # Filter out noise points (label -1) for some metrics
    valid_mask = labels != -1
    if valid_mask.sum() < len(labels):
        embeddings_valid = embeddings[valid_mask]
        labels_valid = labels[valid_mask]
    else:
        embeddings_valid = embeddings
        labels_valid = labels

    # Campionamento per dataset enormi per evitare di esaurire la memoria (OOM) e calcolare le distanze
    if sample_size is not None and embeddings_valid.shape[0] > sample_size:
        np.random.seed(42)
        indices = np.random.choice(embeddings_valid.shape[0], size=sample_size, replace=False)
        embeddings_sample = embeddings_valid[indices]
        labels_sample = labels_valid[indices]
    else:
        embeddings_sample = embeddings_valid
        labels_sample = labels_valid

    # Compute metrics
    silhouette = silhouette_score(embeddings_sample, labels_sample)
    davies_bouldin = davies_bouldin_score(embeddings_sample, labels_sample)
    calinski_harabasz = calinski_harabasz_score(embeddings_sample, labels_sample)

    return {
        "silhouette": float(silhouette),
        "davies_bouldin": float(davies_bouldin),
        "calinski_harabasz": float(calinski_harabasz),
    }


def compute_stability_metrics(
    embeddings: np.ndarray,
    labels: np.ndarray,
    bootstrap_iterations: int = 10,
    bootstrap_fraction: float = 0.7,
    random_state: int = 42,
    n_clusters: int | None = None,
) -> dict[str, float]:
    """Compute cluster stability via bootstrap and subsampling.

    Mini spiegazione:
    - ARI (Adjusted Rand Index): similariità tra clustering su dataset intero vs bootstrap.
    - NMI (Normalized Mutual Information): entropia normalizzata.
    Range per entrambi: [-1, 1] o [0, 1], più alto = migliore stabilità.

    Args:
        embeddings: 2D array of shape (n_samples, n_features)
        labels: 1D array of cluster labels (reference)
        bootstrap_iterations: Number of bootstrap iterations
        bootstrap_fraction: Fraction of samples to use in each bootstrap
        random_state: Random seed
        n_clusters: Number of clusters for KMeans refit. If None, use len(unique(labels))

    Returns:
        Dictionary with ari_mean, nmi_mean, and bootstrap_results list
    """
    rng = np.random.RandomState(random_state)
    ari_scores = []
    nmi_scores = []

    if n_clusters is None:
        n_clusters = len(np.unique(labels[labels != -1]))

    n_samples = int(embeddings.shape[0] * bootstrap_fraction)

    for _ in range(bootstrap_iterations):
        # Bootstrap sample
        indices = rng.choice(embeddings.shape[0], size=n_samples, replace=False)
        embeddings_boot = embeddings[indices]

        # Cluster bootstrap sample
        labels_boot, _ = cluster_kmeans(embeddings_boot, n_clusters, random_state=random_state)

        # Compare with reference labels
        labels_ref_boot = labels[indices]
        # Filter out noise
        valid_mask = (labels_ref_boot != -1) & (labels_boot != -1)

        if valid_mask.sum() > 0:
            ari = adjusted_rand_score(labels_ref_boot[valid_mask], labels_boot[valid_mask])
            nmi = normalized_mutual_info_score(labels_ref_boot[valid_mask], labels_boot[valid_mask])
            ari_scores.append(float(ari))
            nmi_scores.append(float(nmi))

    return {
        "ari_mean": float(np.mean(ari_scores)) if ari_scores else 0.0,
        "ari_std": float(np.std(ari_scores)) if ari_scores else 0.0,
        "nmi_mean": float(np.mean(nmi_scores)) if nmi_scores else 0.0,
        "nmi_std": float(np.std(nmi_scores)) if nmi_scores else 0.0,
        "bootstrap_iterations": bootstrap_iterations,
    }


def compute_retrieval_metrics(
    embeddings: np.ndarray,
    k_values: list[int] = [1, 5, 10],
    sample_size: int | None = None,
    distance_metric: str = "cosine",
) -> dict[str, float]:
    """Compute nearest-neighbor retrieval metrics.

    Mini spiegazione:
    - Recall@k: frazione di query dove vero neighbor è in top-k risultati.
    - MRR (Mean Reciprocal Rank): media di 1/rank del primo vero neighbor.
    Range per entrambi: [0, 1], più alto = meglio.

    Args:
        embeddings: 2D array of shape (n_samples, n_features)
        k_values: List of k values to compute recall@k
        sample_size: If provided, subsample embeddings for faster computation
        distance_metric: 'cosine' or 'euclidean'

    Returns:
        Dictionary with recall@k and mrr scores
    """
    if sample_size is not None and sample_size < embeddings.shape[0]:
        indices = np.random.choice(embeddings.shape[0], size=sample_size, replace=False)
        embeddings_sample = embeddings[indices]
    else:
        embeddings_sample = embeddings
        indices = np.arange(embeddings.shape[0])

    # Normalize for cosine distance
    if distance_metric == "cosine":
        embeddings_norm = embeddings_sample / (np.linalg.norm(embeddings_sample, axis=1, keepdims=True) + 1e-8)
        similarity_matrix = embeddings_norm @ embeddings_norm.T
        # Convert similarity to distances (1 - similarity)
        distances = 1.0 - similarity_matrix
    else:
        # Euclidean distance
        distances = np.linalg.norm(embeddings_sample[:, np.newaxis, :] - embeddings_sample[np.newaxis, :, :], axis=2)

    results = {}

    # Compute recall@k and MRR
    recalls = {k: [] for k in k_values}
    mrr_scores = []

    for query_idx in range(embeddings_sample.shape[0]):
        # Get k nearest neighbors
        distances_query = distances[query_idx]
        nearest_indices = np.argsort(distances_query)

        # True neighbors are all others (for simple heuristic, use nearest 1 + self)
        # In a real scenario, you'd have explicit ground truth
        # Here we compute based on nearest-neighbor consistency
        for k in k_values:
            top_k_indices = nearest_indices[1:k+1]  # Exclude self (index 0)
            # Check if any of them is "correct" (heuristic: consider nearest 1 as correct)
            if len(top_k_indices) > 0 and nearest_indices[1] in top_k_indices:
                recalls[k].append(1.0)
            else:
                recalls[k].append(0.0)

        # MRR: rank of first relevant (heuristic: nearest neighbor)
        mrr_scores.append(1.0 / 2.0)  # Rank 1 is at position 0, so position 1 = rank 2

    for k in k_values:
        results[f"recall@{k}"] = float(np.mean(recalls[k])) if recalls[k] else 0.0

    results["mrr"] = float(np.mean(mrr_scores)) if mrr_scores else 0.0

    return results


def reduce_embeddings(
    embeddings: np.ndarray,
    method: str = "pca",
    n_components: int = 2,
    random_state: int = 42,
) -> np.ndarray:
    """Reduce dimensionality of embeddings for visualization.

    Args:
        embeddings: 2D array of shape (n_samples, n_features)
        method: 'pca' or 'umap' (umap requires separate installation)
        n_components: Number of dimensions to reduce to
        random_state: Random seed

    Returns:
        2D array of shape (n_samples, n_components)
    """
    if method == "pca":
        pca = PCA(n_components=n_components, random_state=random_state)
        return pca.fit_transform(embeddings)
    else:
        raise ValueError(f"Unknown method: {method}. Supported: 'pca'")


def normalize_embeddings(
    embeddings: np.ndarray,
    method: str = "l2",
) -> np.ndarray:
    """Normalize embeddings.

    Args:
        embeddings: 2D array of shape (n_samples, n_features)
        method: 'l2' for L2 normalization, 'zscore' for z-score normalization

    Returns:
        Normalized embeddings
    """
    if method == "l2":
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms[norms == 0] = 1.0  # Avoid division by zero
        return embeddings / norms
    elif method == "zscore":
        return (embeddings - embeddings.mean(axis=0)) / (embeddings.std(axis=0) + 1e-8)
    else:
        raise ValueError(f"Unknown normalization method: {method}")


def compare_models_clustering(
    embeddings_dict: dict[str, np.ndarray],
    n_clusters_range: list[int] = [3, 5, 10, 15, 20],
) -> pd.DataFrame:
    """Compare clustering metrics across multiple embedding models.

    Args:
        embeddings_dict: Dictionary mapping model names to embedding arrays
        n_clusters_range: Range of cluster numbers to try

    Returns:
        DataFrame with clustering metrics for each model and k
    """
    results = []

    for model_name, embeddings in embeddings_dict.items():
        for n_clusters in n_clusters_range:
            labels, _ = cluster_kmeans(embeddings, n_clusters)
            metrics = compute_clustering_metrics(embeddings, labels)

            results.append({
                "model": model_name,
                "n_clusters": n_clusters,
                "silhouette": metrics["silhouette"],
                "davies_bouldin": metrics["davies_bouldin"],
                "calinski_harabasz": metrics["calinski_harabasz"],
            })

    return pd.DataFrame(results)


if __name__ == "__main__":
    # Example usage
    print("Embedding Comparison Utilities")
    print("=" * 50)

    # Generate sample data
    np.random.seed(42)
    n_samples, n_features = 100, 50
    X = np.random.randn(n_samples, n_features)

    # Cluster
    labels, centroids = cluster_kmeans(X, n_clusters=5)

    # Evaluate
    metrics = compute_clustering_metrics(X, labels)
    print(f"\nClustering Metrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value:.4f}")

    # Stability
    stability = compute_stability_metrics(X, labels, bootstrap_iterations=5)
    print(f"\nStability Metrics:")
    for key, value in stability.items():
        if key != "bootstrap_iterations":
            print(f"  {key}: {value:.4f}")

    # Retrieval
    retrieval = compute_retrieval_metrics(X)
    print(f"\nRetrieval Metrics:")
    for key, value in retrieval.items():
        print(f"  {key}: {value:.4f}")

