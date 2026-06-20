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

## Ottimizzazione degli Iperparametri con Optuna (TPE/CMA-ES)

Durante l'evoluzione del progetto, la tradizionale Grid Search per la ricerca dei parametri ottimali di clustering (es. `min_cluster_size`, `min_samples`) è stata sostituita con **Optuna**.

### Perché Optuna?
Effettuare una Grid Search esaustiva su un dataset di grandi dimensioni scala malissimo computazionalmente. Optuna utilizza algoritmi di ricerca euristica (come **TPE - Tree-structured Parzen Estimator** per l'Ottimizzazione Bayesiana, o **CMA-ES** per l'approccio genetico/evolutivo) che esplorano lo spazio dei parametri imparando dai tentativi precedenti. Questo permette di trovare configurazioni sub-ottimali (estremamente performanti) in una frazione del tempo, minimizzando il numero di esecuzioni pesanti della pipeline.

### Strategia di Campionamento (Subsampling)
Per massimizzare l'efficienza, l'ottimizzazione con Optuna **non viene eseguita sull'intero dataset** (che può pesare svariati GB e contenere milioni di righe). 
La best practice applicata consiste nel:
1. Campionare un sottoinsieme stratificato e rappresentativo dei vettori (es. 10.000 o 15.000 righe).
2. Far girare Optuna sul campione per trovare rapidamente i parametri che massimizzano la metrica di Fitness (es. Silhouette Score bilanciato con la percentuale di rumore).
3. Applicare la configurazione di iperparametri "vincente" all'intero dataset originale per l'inferenza (fit) finale.

### Pro e Contro
**Pro:**
- **Velocità ed Efficienza**: Trova ottimi parametri esplorando in modo intelligente le aree promettenti dello spazio di ricerca.
- **Ottimizzazione Multi-obiettivo**: Permette di cercare il Fronte di Pareto tra metriche in conflitto (es. massimizzare la separazione dei cluster minimizzando al contempo l'outlier ratio).
- **Scalabilità**: Consente in futuro di aggiungere nuovi parametri da ottimizzare (es. parametri UMAP) senza far esplodere i tempi di esecuzione, limite invalicabile della Grid Search.

**Contro:**
- Introduce una dipendenza aggiuntiva (`optuna`).
- Richiede la definizione attenta di una funzione obiettivo (Fitness).

## Implementazione
Il codice di riferimento si trova in `src/utils/clustering_hdbscan.py`.
