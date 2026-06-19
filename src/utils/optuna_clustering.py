import optuna
import numpy as np
import logging
from typing import Dict, Any
from sklearn.metrics import silhouette_score
import hdbscan

try:
    import umap
    HAS_UMAP = True
except ImportError:
    HAS_UMAP = False

logger = logging.getLogger(__name__)

def hdbscan_objective(trial: optuna.Trial, embeddings: np.ndarray, use_umap: bool = False, penalty_weight: float = 0.5) -> float:
    """
    Optuna objective function for clustering.
    Returns a fitness score to maximize.
    """
    
    if use_umap and HAS_UMAP:
        # Hyperparameters for UMAP
        n_neighbors = trial.suggest_int('n_neighbors', 10, 100)
        n_components = trial.suggest_int('n_components', 2, 15)
        
        reducer = umap.UMAP(
            n_neighbors=n_neighbors, 
            n_components=n_components, 
            metric='cosine', 
            min_dist=0.01,
            random_state=42
        )
        try:
            reduced_data = reducer.fit_transform(embeddings)
        except Exception as e:
            logger.warning(f"UMAP failed: {e}")
            return -1.0
    else:
        reduced_data = embeddings
        
    # Hyperparameters for HDBSCAN
    min_cluster_size = trial.suggest_int('min_cluster_size', 10, 200)
    # Limiti statici per far lavorare correttamente CMA-ES
    min_samples_raw = trial.suggest_int('min_samples', 5, 200)
    # Applichiamo il vincolo logico a valle
    min_samples = min(min_samples_raw, min_cluster_size)
    
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        metric='euclidean',
        cluster_selection_method='eom',
        core_dist_n_jobs=-1
    )
    
    try:
        clusterer.fit(reduced_data)
    except Exception as e:
        logger.warning(f"HDBSCAN failed: {e}")
        return -1.0
        
    labels = clusterer.labels_
    
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    
    # We want at least 2 macro-clusters to consider it a valid clustering
    if n_clusters < 2:
        return -1.0 
        
    # Calculate noise ratio
    n_noise = list(labels).count(-1)
    noise_ratio = n_noise / len(labels)
    
    # We don't want a clustering where almost everything is noise
    if noise_ratio > 0.8:
        return -1.0
        
    # Calculate silhouette score only on clustered points
    mask = labels != -1
    
    if sum(mask) < 2:
        return -1.0
        
    try:
        # Use reduced data for silhouette to evaluate the shape of the clusters formed
        # If use_umap is False, this uses the original embeddings
        score = silhouette_score(reduced_data[mask], labels[mask], metric='euclidean')
    except Exception as e:
        logger.warning(f"Silhouette calculation failed: {e}")
        return -1.0
        
    # Fitness formula: Silhouette score penalized by noise ratio
    # Silhouette is between -1 and 1. Noise ratio is between 0 and 1.
    fitness = score - (penalty_weight * noise_ratio)
    
    # Save useful metrics in the trial for post-analysis
    trial.set_user_attr("n_clusters", n_clusters)
    trial.set_user_attr("noise_ratio", float(noise_ratio))
    trial.set_user_attr("silhouette", float(score))
    
    return fitness

def run_clustering_optimization(
    embeddings: np.ndarray, 
    n_trials: int = 50, 
    use_umap: bool = False, 
    sampler_type: str = 'TPE', 
    penalty_weight: float = 0.5
) -> optuna.Study:
    """
    Run Optuna optimization for clustering hyperparameters.
    
    Args:
        embeddings: The data to cluster (suggested to use a sample of 10k-15k)
        n_trials: Number of configurations to test
        use_umap: Whether to also optimize UMAP parameters before HDBSCAN
        sampler_type: 'TPE' (Bayesian) or 'CMA-ES' (Evolutionary)
        penalty_weight: Weight of the noise penalty in the fitness function
        
    Returns:
        optuna.Study object containing the results.
    """
    logger.info(f"Avvio ottimizzazione Optuna con {n_trials} trials, sampler={sampler_type}, use_umap={use_umap}")
    
    if sampler_type.upper() == 'CMA-ES':
        # CMA-ES is great for continuous optimization
        sampler = optuna.samplers.CmaEsSampler(seed=42)
    else:
        # TPE is the standard for hyperparameter tuning
        sampler = optuna.samplers.TPESampler(seed=42)
        
    study = optuna.create_study(direction="maximize", sampler=sampler)
    
    objective = lambda trial: hdbscan_objective(trial, embeddings, use_umap=use_umap, penalty_weight=penalty_weight)
    
    # Optimize
    study.optimize(objective, n_trials=n_trials, show_progress_bar=True)
    
    if len(study.best_trials) > 0:
        logger.info(f"Miglior trial: {study.best_trial.number}")
        logger.info(f"Migliori parametri: {study.best_params}")
        logger.info(f"Miglior fitness: {study.best_value}")
    else:
        logger.warning("Nessun trial ha avuto successo.")
        
    return study
