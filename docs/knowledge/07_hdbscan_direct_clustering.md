# HDBSCAN Diretto (Senza Riduzione Dimensionale)

## Cos'è
Questo documento descrive la configurazione e il workflow per l'applicazione di **HDBSCAN** direttamente sugli embeddings ad alta dimensionalità (384 dimensioni di `bge-small-en-v1.5`), saltando la fase di riduzione dimensionale con UMAP.

## Perché usare HDBSCAN direttamente?
Usare UMAP comporta inevitabilmente una perdita di informazione, poiché comprime lo spazio topologico sacrificando alcune relazioni globali per preservare quelle locali. Applicare HDBSCAN direttamente sui vettori originali garantisce che i cluster siano formati al 100% sulla base della semantica nativa del modello.

## La Sfida: Maledizione della Dimensionalità
A 384 dimensioni, la distanza Euclidea classica perde di significato (tutti i punti sembrano equidistanti). HDBSCAN, basandosi sulla densità, potrebbe fallire (classificando tutto come rumore o creando un solo mega-cluster).

## La Soluzione: Normalizzazione L2 e Distanza Coseno
Per far funzionare HDBSCAN ad alta dimensionalità:
1. Gli embeddings devono essere **L2 normalizzati** (tutti i vettori hanno lunghezza 1.0).
2. Si utilizza la metrica `euclidean` in HDBSCAN.

**Magia matematica**: La distanza euclidea tra due vettori normalizzati L2 è strettamente proporzionale alla loro **distanza Coseno**. La distanza Coseno misura l'angolo tra i vettori, ignorando la magnitudine, ed è estremamente robusta in alta dimensionalità. In questo modo HDBSCAN raggruppa i documenti per "orientamento" semantico.

## Workflow di Clustering

1. **Caricamento Dati**: Caricare gli embeddings da `data/embeddings/email_embeddings.npy` (generati dal branch A).
2. **Verifica Normalizzazione**: Assicurarsi che le norme dei vettori siano ~1.0.
3. **Esecuzione HDBSCAN**:
   - `min_cluster_size`: Parte da 50-100. Definisce la granularità semantica.
   - `min_samples`: Mantenuto uguale a `min_cluster_size` o leggermente inferiore per gestire la sparsità locale.
   - `metric`: `euclidean` (che agisce da proxy per il coseno grazie alla normalizzazione).
   - `cluster_selection_method`: `eom` (Excess of Mass).
4. **Analisi Outlier**: Tutti i punti etichettati con `-1` sono rumore/outlier. Nelle email reali, questo isola spam, boilerplate univoco o contesti troppo rari.
5. **Incrocio Feature**: I cluster estratti vengono incrociati con le feature strutturali in `processed` (es. `is_weekend`, `redaction_count`) per l'interpretazione.

## Implementazione
Il codice di riferimento si trova in `src/utils/clustering_hdbscan.py`.
