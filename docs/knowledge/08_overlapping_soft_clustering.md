# Overlapping (Soft) Clustering

## Cos'è
L'Overlapping Clustering (conosciuto anche come **Soft Clustering** o **Fuzzy Clustering**) è un approccio in cui un singolo dato (es. un'email) non viene assegnato a un unico e solo cluster in modo esclusivo (Hard Clustering), ma possiede un **vettore di probabilità** o "gradi di appartenenza" a più cluster contemporaneamente. 
Ad esempio, un'email potrebbe appartenere al 70% al cluster "Finanza" e al 30% al cluster "Risorse Umane".

## Quando usarlo
È ideale nei dati testuali e semantici (come le email degli Epstein Files), perché le conversazioni umane raramente trattano un solo argomento puro. Si usa quando si vuole catturare la natura multi-tematica dei documenti o quando si analizzano reti di nodi con connessioni sovrapposte.

## Pro
- **Realismo Semantico**: Rispecchia la realtà umana, dove un'email spesso tocca più argomenti.
- **Recupero del Rumore**: I punti ai confini tra due cluster (spesso scartati come rumore in algoritmi rigidi) vengono salvati e classificati come "argomenti ibridi".
- **Analisi di Rete (Knowledge Graph)**: Permette di trovare documenti o persone "ponte" tra due macro-argomenti, permettendo la costruzione di reti semantiche e costellazioni di cluster.

## Contro
- **Esplosione dei Dati**: Invece di salvare un solo ID per email (1.75M di valori), si rischia di dover salvare le probabilità per *ogni* cluster. 
- **Complessità Computazionale**: Algoritmi come la funzione nativa di HDBSCAN (`membership_vector`) possono richiedere ore o giorni su dataset Big Data (>1M vettori) a causa del calcolo della distanza contro tutti i punti rappresentativi (exemplars) di ogni cluster.

---

## L'Ottimizzazione nel Progetto "Pizza Cluster"

Durante la nostra analisi, abbiamo implementato due enormi miglioramenti (Hack) per superare i limiti matematici di HDBSCAN su 1.75 milioni di email:

### 1. Centroid-based Softmax Clustering (La Soluzione al Collo di Bottiglia)
La funzione nativa `membership_vector` di HDBSCAN impiegava stimate ~10 ore a causa del calcolo distanze-esemplari.
Abbiamo scavalcato la funzione scrivendo noi la matematica:
- **Centroidi**: Abbiamo calcolato il punto medio (centroide) di ciascuno dei 900 cluster.
- **Euclidean + Softmax**: Usando NumPy e `scipy.spatial.distance.cdist`, abbiamo calcolato la distanza euclidea al quadrato tra ogni email e i centroidi. Dopodiché, abbiamo applicato una funzione **Softmax** (con temperatura `0.5`) per convertire istantaneamente la distanza in una "Probabilità di Affinità".
- **Risultato**: Il tempo di esecuzione per 1.75 milioni di documenti è sceso da **10 ore a meno di 1 minuto**.

### 2. Estrazione Top-10 (La Soluzione all'Esplosione dei Dati)
Invece di salvare matrici gigantesche, il codice ordina le probabilità dal più grande al più piccolo e mantiene **solo i 10 cluster più probabili** per ogni email, scartando gli altri. Questi vengono salvati elegantemente nel formato Parquet come liste compatte (`top_10_clusters`, `top_10_probs`), occupando solo pochi Megabyte in più.

---

## Analisi dei Risultati

L'applicazione del nostro Centroid Soft Clustering ha rivelato insight investigativi eccezionali, superando i limiti del vecchio Hard Clustering:

1. **La "Parentela" Gerarchica dei Cluster**: Molte email hanno mostrato probabilità ripartite in cluster sequenziali (es. 7% al Cluster 557, 7% al 559, 7% al 560). Essendo la numerazione derivata dall'albero di densità, questo indica l'incertezza del modello tra "sotto-rami" fratelli.
2. **Identificazione delle Email "Ponte" Pure**: Molti documenti uniscono al 50% / 50% due cluster che numericamente sono lontanissimi (es. 157 e 258). Queste sono le vere email investigative che collegano enti o argomenti separati.
3. **Smentita dei "Falsi Deboli"**: In zone molto sparse dello spazio vettoriale, HDBSCAN (che lavora sulla densità) aveva assegnato una bassissima fiducia (Hard clustering = 5%), mentre il calcolo geometrico della distanza ha rivelato che quel punto isolato, pur lontano, puntava in modo univoco e 100% diretto verso un singolo centro.

### Visualizzazione: Knowledge Graph
L'overlapping ha permesso di creare una rappresentazione a rete (`NetworkX`) in cui i Cluster sono Nodi e le "email condivise/ponte" sono gli Archi che li uniscono, permettendo di analizzare visivamente il grado di parentela tra macro-argomenti.

### Il ruolo delle "Email Pure" vs "Email Ponte"
Questa scoperta ha rivoluzionato il nostro approccio all'etichettatura (Topic Labeling) tramite LLM:
1. **Email Pure (Dizionari)**: Per dare il *Nome* a un cluster (Topic Labeling), le email ponte vanno ignorate. Bisogna passare all'LLM solo le email "purissime" (es. probabilità > 85% sul cluster primario) in modo che l'AI non si faccia distrarre da argomenti secondari e restituisca etichette nette (es. *"Traffico Aereo"*).
2. **Email Ponte (Investigazioni)**: Una volta che i cluster hanno un nome, le email ponte diventano lo strumento investigativo principale. Interrogando l'LLM esclusivamente sulle email ponte tra il cluster *"Traffico Aereo"* e *"Pagamenti Legali"*, si scoprono i collegamenti reali (es. *"queste email parlano di spese legali per coprire l'acquisto di jet privati"*). Le email pure definiscono il dizionario; le email ponte definiscono la trama criminale.

---

## Link Utili
- **Documentazione HDBSCAN Soft Clustering**: https://hdbscan.readthedocs.io/en/latest/soft_clustering.html
- **Video (Soft Clustering vs Hard Clustering)**: https://www.youtube.com/watch?v=kYJv8Z1kZ5E

## Argomenti da studiare / approfondire per la comprensione
- Soft vs Hard Clustering
- Funzione di attivazione Softmax e parametro Temperatura
- Calcolo Distanze Geometriche vs Calcolo Densità topologica
- Algoritmi di Network Analysis e Knowledge Graphs
