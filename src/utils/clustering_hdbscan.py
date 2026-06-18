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
    n_neighbors: int = 30,
    n_components: int = 5,
    min_cluster_size: int = 15,
    min_samples: int = 3,
    cluster_selection_method: str = 'leaf',
    sample_size: int = 100000
) -> Tuple[np.ndarray, np.ndarray, hdbscan.HDBSCAN, any]:
    import umap
    
    total_samples = embeddings.shape[0]
    
    if total_samples > sample_size:
        logger.info(f"Dataset enorme ({total_samples} vettori). Eseguo sub-sampling a {sample_size} per addestramento UMAP e HDBSCAN.")
        np.random.seed(42)
        train_indices = np.random.choice(total_samples, size=sample_size, replace=False)
        train_embeddings = embeddings[train_indices]
    else:
        train_embeddings = embeddings
        
    logger.info(f"Avvio addestramento UMAP su {train_embeddings.shape[0]} vettori da {embeddings.shape[1]} dimensioni...")
    logger.info(f"Parametri UMAP: n_neighbors={n_neighbors}, n_components={n_components}, min_dist=0.01")
    
    reducer = umap.UMAP(
        n_neighbors=n_neighbors, 
        n_components=n_components, 
        metric='cosine', 
        min_dist=0.01,
        random_state=42
    )
    
    # Train UMAP on sample
    reduced_train = reducer.fit_transform(train_embeddings)
    logger.info(f"UMAP addestrato. Nuova dimensionalità: {reduced_train.shape}")
    
    logger.info("Avvio addestramento HDBSCAN sui vettori ridotti...")
    logger.info(f"Parametri HDBSCAN: min_cluster_size={min_cluster_size}, min_samples={min_samples}, method='{cluster_selection_method}'")
    
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        metric='euclidean',
        cluster_selection_method=cluster_selection_method,
        prediction_data=True,
        core_dist_n_jobs=-1
    )
    clusterer.fit(reduced_train)
    
    n_clusters = len(set(clusterer.labels_)) - (1 if -1 in clusterer.labels_ else 0)
    n_noise = list(clusterer.labels_).count(-1)
    logger.info(f"Addestramento HDBSCAN completato sul campione. Cluster trovati: {n_clusters}, Rumore: {n_noise}")
    
    if total_samples > sample_size:
        logger.info(f"Proiezione dei restanti {total_samples} vettori nei cluster...")
        # Reduce all embeddings using the trained UMAP
        logger.info("Trasformazione UMAP di tutto il dataset in corso (potrebbe richiedere tempo)...")
        reduced_embeddings = reducer.transform(embeddings)
        
        # FIX: UMAP transform può generare NaN a causa di approssimazioni di virgola mobile.
        if np.isnan(reduced_embeddings).any():
            nan_count = np.isnan(reduced_embeddings).sum()
            logger.warning(f"Attenzione: UMAP transform ha generato {nan_count} valori NaN. Verranno sostituiti con 0 per non bloccare HDBSCAN.")
            reduced_embeddings = np.nan_to_num(reduced_embeddings, nan=0.0)
        
        # Predict clusters for all embeddings using approximate_predict
        logger.info("Assegnazione HDBSCAN di tutto il dataset in corso...")
        labels, probabilities = hdbscan.approximate_predict(clusterer, reduced_embeddings)
        logger.info("Proiezione completata.")
    else:
        reduced_embeddings = reduced_train
        labels = clusterer.labels_
        probabilities = clusterer.probabilities_
        
    final_n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    final_n_noise = list(labels).count(-1)
    logger.info(f"Clustering finale completato. Cluster totali trovati: {final_n_clusters}, Rumore: {final_n_noise}")
    
    return labels, probabilities, clusterer, reduced_embeddings

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Test HDBSCAN locale con vettori fittizi L2 normalizzati...")
    # Crea 500 vettori a 384 dimensioni normalizzati
    np.random.seed(42)
    X = np.random.randn(500, 384)
    X = X / np.linalg.norm(X, axis=1, keepdims=True)
    
    labels, probs, model = run_hdbscan_direct(X, min_cluster_size=10)
    print(f"Test completato. Cluster trovati: {len(set(labels)) - (1 if -1 in labels else 0)}")
