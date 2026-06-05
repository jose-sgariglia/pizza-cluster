"""
Utility module for clustering embeddings using HDBSCAN directly.
"""
import hdbscan
import numpy as np
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

def run_hdbscan_direct(
    embeddings: np.ndarray,
    min_cluster_size: int = 50,
    min_samples: int = None,
    metric: str = 'euclidean'
) -> Tuple[np.ndarray, np.ndarray, hdbscan.HDBSCAN]:
    """
    Run HDBSCAN directly on embeddings without dimensionality reduction.
    
    Args:
        embeddings: NumPy array of shape (n_samples, n_features). 
                   MUST be L2 normalized if using euclidean metric to approximate cosine distance.
        min_cluster_size: Minimum size of clusters.
        min_samples: Number of samples in a neighborhood for a point to be considered a core point.
                     If None, defaults to min_cluster_size.
        metric: Distance metric to use. Default 'euclidean'.
        
    Returns:
        labels: Cluster labels (-1 means noise/outlier).
        probabilities: Cluster assignment probabilities.
        clusterer: The fitted HDBSCAN object.
    """
    if min_samples is None:
        min_samples = min_cluster_size
        
    logger.info(f"Running HDBSCAN directly on embeddings of shape {embeddings.shape}")
    logger.info(f"Parameters: min_cluster_size={min_cluster_size}, min_samples={min_samples}, metric={metric}")
    
    # Calculate norms to verify L2 normalization if euclidean is used
    if metric == 'euclidean':
        norms = np.linalg.norm(embeddings, axis=1)
        if not np.allclose(norms, 1.0, atol=1e-3):
            logger.warning("Embeddings are NOT L2 normalized. Euclidean distance will not approximate Cosine distance.")
        else:
            logger.info("Embeddings are L2 normalized. Euclidean distance correctly approximates Cosine distance.")

    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        metric=metric,
        cluster_selection_method='eom',
        prediction_data=True,
        core_dist_n_jobs=-1
    )
    
    clusterer.fit(embeddings)
    
    n_clusters = len(set(clusterer.labels_)) - (1 if -1 in clusterer.labels_ else 0)
    n_noise = list(clusterer.labels_).count(-1)
    
    logger.info(f"Clustering complete. Found {n_clusters} clusters and {n_noise} noise points.")
    
    return clusterer.labels_, clusterer.probabilities_, clusterer

def run_umap_hdbscan(
    embeddings: np.ndarray,
    n_components: int = 15,
    min_cluster_size: int = 100,
    min_samples: int = 50
) -> Tuple[np.ndarray, np.ndarray, hdbscan.HDBSCAN, any]:
    import umap
    
    logger.info(f"Avvio UMAP su {embeddings.shape[0]} vettori da {embeddings.shape[1]} dimensioni...")
    # UMAP usa metric='cosine' perché è ideale per gli embeddings testuali
    reducer = umap.UMAP(
        n_neighbors=15, 
        n_components=n_components, 
        metric='cosine', 
        random_state=42
    )
    reduced_embeddings = reducer.fit_transform(embeddings)
    logger.info(f"UMAP completato. Nuova dimensionalità: {reduced_embeddings.shape}")
    
    logger.info("Avvio HDBSCAN sui vettori ridotti...")
    # HDBSCAN lavora sui 15D usando la distanza euclidea classica in modo rapidissimo
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        metric='euclidean',
        cluster_selection_method='eom',
        prediction_data=True,
        core_dist_n_jobs=8
    )
    clusterer.fit(reduced_embeddings)
    
    n_clusters = len(set(clusterer.labels_)) - (1 if -1 in clusterer.labels_ else 0)
    n_noise = list(clusterer.labels_).count(-1)
    logger.info(f"Clustering completato. Cluster trovati: {n_clusters}, Rumore: {n_noise}")
    
    return clusterer.labels_, clusterer.probabilities_, clusterer, reduced_embeddings

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Test HDBSCAN locale con vettori fittizi L2 normalizzati...")
    # Crea 500 vettori a 384 dimensioni normalizzati
    np.random.seed(42)
    X = np.random.randn(500, 384)
    X = X / np.linalg.norm(X, axis=1, keepdims=True)
    
    labels, probs, model = run_hdbscan_direct(X, min_cluster_size=10)
    print(f"Test completato. Cluster trovati: {len(set(labels)) - (1 if -1 in labels else 0)}")
