# Embedding Evaluation and Clustering

## 1. Introduzione

Questa sezione documenta le metriche e i metodi utilizzati per valutare la qualità degli embeddings e dei cluster risultanti dalla pipeline Pizza Cluster.

L'obiettivo è fornire metriche confrontabili e ripetibili per scegliere il modello embedding più adatto al contesto e alle priorità del progetto.

## 2. Metriche di Valutazione Clustering

Quando generiamo embeddings e li clusterizziamo, dobbiamo rispondere a una domanda fondamentale: **Quanto buoni sono i cluster generati?**

Le metriche di seguito rispondono a questo tramite diverse prospettive.

### 2.1 Silhouette Score

**Mini spiegazione:**
Il Silhouette Score misura per ogni punto la coesione (quanto è vicino ai punti del suo cluster) e la separazione (quanto è lontano dai punti di altri cluster). Range [-1, 1]: +1 = perfetto, 0 = ambiguo, -1 = male assegnato.

**Quando usarlo:** Valutazione generale clustering, comparazione modelli.

**Pro:** Intuitivo, singolo numero, calcolabile per qualsiasi clustering.
**Contro:** Computazionalmente costoso su dataset grandi, sensibile a outliers.

**Interpretazione:** Silhouette > 0.5 (buono), 0.2-0.5 (accettabile), < 0.2 (debole).

**Paper:** https://www.researchgate.net/publication/312502334_Silhouette_Coefficient

### 2.2 Davies-Bouldin Index (DB Index)

**Mini spiegazione:**
Misura il rapporto medio tra dimensione (scatter) di cluster e distanza tra centroidi. Range [0, ∞): 0 = ideale, basso = cluster ben definiti, alto = mal separati.

**Quando usarlo:** Decision su numero ottimale cluster, dataset grandi.

**Pro:** Più veloce di Silhouette, calcolabile su dataset grandi, invariante a scala.
**Contro:** Meno intuitivo, penalizza cluster allungati.

**Interpretazione:** DB < 1 (buono), 1-1.5 (accettabile), > 1.5 (scadente).

### 2.3 Calinski-Harabasz Index (CH Index)

**Mini spiegazione:**
Rapporto tra varianza tra cluster e varianza dentro cluster. Range [0, ∞): valori alti = cluster ben separati.

**Quando usarlo:** Sweep su K, dataset grandi (veloce).

**Pro:** Molto efficiente, scala bene, agnostico geometria.
**Contro:** Favorisce cluster convessi, non auto-seleziona K.

**Interpretazione:** CH > 300 (buono), 100-300 (accettabile), < 100 (scadente).

## 3. Metriche di Stabilità

### 3.1 Adjusted Rand Index (ARI)

**Mini spiegazione:**
Confronta due clustering (es. dataset intero vs bootstrap). Range [-1, 1]: +1 = identici, 0 = indipendenti, -1 = opposti.

**Interpretazione:** ARI > 0.9 (eccellente), 0.7-0.9 (buono), < 0.7 (possibile instabilità).

### 3.2 Normalized Mutual Information (NMI)

**Mini spiegazione:**
Mutua informazione tra due clustering. Range [0, 1]: 1 = identici, 0 = indipendenti.

**Vantaggio:** Meno sensibile a distribuzioni sbilanciate rispetto ad ARI.

## 4. Metriche di Retrieval

### 4.1 Recall@K

**Mini spiegazione:**
Frazione di query che trovano un vero neighbor in top-K risultati. Range [0, 1].

**Quando usarlo:** Se task finale è semantic search / information retrieval.

### 4.2 Mean Reciprocal Rank (MRR)

**Mini spiegazione:**
Media di 1/rank del primo vero neighbor trovato. Range [0, 1].

**Vantaggio:** Penalizza fortemente risultati lontani.

## 5. Implementazione

Le metriche sono implementate in `src/utils/embedding_comparision.py` con test in `tests/test_embedding_comparision.py` (9 test all passed).

```python
from src.utils.embedding_comparision import compute_clustering_metrics
labels, _ = cluster_kmeans(embeddings, n_clusters=5)
metrics = compute_clustering_metrics(embeddings, labels)
print(f"Silhouette: {metrics['silhouette']:.4f}")
```

## 6. Link Risorse

**Paper:**
- Silhouette: https://www.researchgate.net/publication/312502334_Silhouette_Coefficient
- Davies-Bouldin: https://en.wikipedia.org/wiki/Davies%E2%80%93Bouldin_index
- Calinski-Harabasz: https://en.wikipedia.org/wiki/Calinski%E2%80%93Harabasz_index

**Librerie:**
- scikit-learn: https://scikit-learn.org/stable/modules/model_evaluation.html#clustering-metrics

## 7. Note Finali

Per dataset > 10k: usare Calinski-Harabasz (più veloce), subsampling per retrieval, considerare HDBSCAN per K dinamico.

