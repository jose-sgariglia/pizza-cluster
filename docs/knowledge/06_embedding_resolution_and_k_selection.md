# Risoluzione Semantica degli Embedding e Scelta di K nel Clustering

## Cos'è
Questo documento approfondisce il comportamento di diversi modelli di embedding (es. leggeri come `all-MiniLM-L6-v2` vs più profondi come `e5-base-v2` o `bge-small`) rispetto agli algoritmi di clustering (come K-Means). Spiega in particolare perché la selezione del parametro $K$ ottimale (tramite metriche come il Silhouette Score) varia in base alla capacità di risoluzione del modello stesso e alla densità dello spazio latente.

## Quando usarlo
Quando si confrontano pipeline di embedding differenti, per interpretare correttamente risultati apparentemente paradossali: ad esempio, quando un modello predilige un numero bassissimo di cluster (es. $K=3$) mostrando metriche formalmente migliori ma cluster altamente instabili, rispetto a modelli che preferiscono una divisione più granulare ($K=15$).

## Dettaglio Tecnico: Risoluzione Semantica (Macro-topic vs Micro-topic)
Modelli leggeri come `all-MiniLM-L6-v2` (384 dimensioni) sono ottimizzati per mappare testi su concetti molto vasti e generalisti. Lo spazio vettoriale generato si presta meglio a una suddivisione in poche macro-categorie. Forzando un'alta granularità (es. $K=15$), il modello non trova confini semantici chiari, facendo crollare i punteggi di qualità (come il Silhouette Score).
Al contrario, modelli con maggiore dimensionalità e complessità come `e5-base-v2` (768 dimensioni) riescono a preservare sfumature e differenze più sottili nei testi. Questo permette all'algoritmo di trovare raggruppamenti coerenti e ben separati anche ad alta granularità.

## Dettaglio Tecnico: Silhouette Score e Spazi Densi
Nei task di NLP reali su corpora complessi (come un archivio di email), è comune osservare Silhouette Score molto bassi per tutti i modelli (es. 0.02 - 0.04). Questo accade perché i testi formano una "nuvola" semantica continua e molto compatta, senza ampi spazi vuoti a separare i cluster.
In spazi ad alta densità (alta "isotropia"):
* Dividere arbitrariamente la nuvola in 2 o 3 parti può restituire un Silhouette matematicamente più alto rispetto a divisioni maggiori, ma non rappresenta la reale topologia tematica dei dati (è un "artefatto matematico").
* Punteggi apparentemente "migliori" a K bassi sono spesso accompagnati da un'altissima instabilità, rilevabile tramite forte deviazione standard in metriche di stabilità (Adjusted Rand Index - ARI, NMI) calcolate tramite bootstrap. In questi casi, la posizione dei centroidi cambia drasticamente ad ogni iterazione.
* Un $K$ maggiore (es. 15), pur con un Silhouette leggermente inferiore, restituisce spesso partizioni molto più stabili e coerenti per l'analisi.

## Pro
* Comprendere queste dinamiche evita di affidarsi ciecamente alla metrica del Silhouette Score come unico "oracolo" per la scelta del numero di cluster.
* Aiuta a giustificare l'adozione di modelli più complessi per recuperare granularità.

## Contro
* L'analisi richiede tecniche aggiuntive costose computazionalmente (come il bootstrap e il calcolo della stabilità tramite ARI/NMI) per smascherare K apparentemente buoni ma in realtà instabili.

## Alternative
Oltre a K-Means, si possono impiegare algoritmi basati sulla densità (es. HDBSCAN o DBSCAN) o tool come BERTopic. Questi gestiscono meglio le distribuzioni non sferiche e la nuvola continua, inferendo automaticamente il numero di cluster dal rumore di fondo.

## Link utili

**Articolo:**
[How to evaluate clustering without ground truth](https://towardsdatascience.com/clustering-evaluation-strategies-98a4006fcfc) (Spiega le dinamiche del Silhouette e perché a volte favorisca K bassi).

**Video:**
[K-Means & The Silhouette Score Explained](https://www.youtube.com/watch?v=Qh_t1I7k41k)

# Argomenti da studiare / approfondire per la comprensione
- Clustering gerarchico
- K-Means e maledizione della dimensionalità (Curse of Dimensionality)
- DBSCAN / HDBSCAN e Clustering basato sulla densità
- Embedding NLP e Isotropia nello spazio latente
- Metriche di stabilità (Adjusted Rand Index, Normalized Mutual Information)
- BERTopic
