# Text Embeddings

## From text to vectors
I computer e gli algoritmi di machine learning non sono in grado di comprendere direttamente il testo in formato stringa; possono elaborare esclusivamente strutture matematiche come vettori e matrici numeriche. Il processo di conversione del testo in vettori si articola storicamente in due fasi principali:
1. **Tokenizzazione:** Il testo viene spezzato in unità più piccole (parole, sotto-parole o caratteri) chiamate token.
2. **Vettorizzazione:** A ogni token o sequenza di token viene assegnato uno score numerico o una posizione all'interno di uno spazio geometrico multidimensionale.

L'obiettivo fondamentale delle moderne tecniche di NLP (Natural Language Processing) è fare in modo che questa trasformazione non sia una semplice mappatura arbitraria, ma che riesca a preservare le relazioni sintattiche e semantiche originarie del linguaggio umano.

## Sparse vs dense representations
La rappresentazione del testo si divide in due grandi paradigmi:

### Rappresentazioni Sparse (es. TF-IDF, Bag-of-Words)
* **Struttura:** Ogni documento è rappresentato da un vettore la cui lunghezza è pari all'intero vocabolario del dataset. Se una parola non è presente nel documento, il suo valore è zero.
* **Caratteristiche:** I vettori sono enormi e composti quasi interamente da zeri (da qui il termine "sparsi").
* **Limiti:** Non catturano il contesto né la semantica. Per un modello TF-IDF, le parole "acquistare" e "comprare" sono trattate come entità completamente distinte e ortogonali, non evidenziando alcuna correlazione logica.

### Rappresentazioni Dense (es. Word2Vec, Sentence Transformers)
* **Struttura:** Ogni testo viene mappato in un vettore di dimensione fissa e relativamente piccola (es. 384 o 768 dimensioni), dove ogni posizione contiene un numero decimale continuo (valore floating-point).
* **Caratteristiche:** Tutte le posizioni del vettore memorizzano informazioni astratte, eliminando la presenza massiva di zeri.
* **Vantaggi:** Catturano il significato profondo, i sinonimi e le relazioni contestuali. Concetti semanticamente affini vengono posizionati in punti vicini dello spazio geometrico creato dal modello.

## Sentence Transformers
I Sentence Transformers rappresentano un'evoluzione dei modelli di linguaggio basati sull'architettura Transformer (come BERT). Mentre il BERT standard è progettato per compiti a livello di singola parola o classificazione, i Sentence Transformers utilizzano strutture a rete siamese (Siamese BERT Networks) per calcolare embedding ottimizzati per intere frasi, paragrafi o brevi documenti.

Nel nostro progetto utilizziamo il modello **`all-MiniLM-L6-v2`**:
* **Architettura:** È un modello distillato, compatto e ottimizzato per la velocità di esecuzione su CPU (ideale per workstation locali come il ThinkPad).
* **Output:** Genera vettori densi compresi esattamente in uno spazio a **384 dimensioni**.
* **Performance:** Offre un eccellente compromesso tra accuratezza semantica e tempi di calcolo durante la conversione di grossi quantitativi di testo.

## Semantic similarity
Una volta trasformati i testi in vettori densi, la similarità semantica tra due documenti viene calcolata misurando la loro vicinanza geometrica all'interno dello spazio vettoriale multidimensionale.

La metrica standard utilizzata è la **Cosine Similarity** (Similarità del Coseno). Essa valuta l'angolo formato dai due vettori, indipendentemente dalla loro lunghezza (ovvero dalla lunghezza del testo originario):

$$\text{Cosine Similarity}(A, B) = \frac{A \cdot B}{\|A\| \|B\|}$$

* **Coseno = 1 (Angolo di 0°):** I vettori puntano nella stessa identica direzione; i testi esprimono un significato semantico identico.
* **Coseno = 0 (Angolo di 90°):** I vettori sono ortogonali; i testi trattano argomenti completamente indipendenti o privi di correlazione logica.
* **Coseno = -1 (Angolo di 180°):** I vettori sono opposti (raro nel contesto testuale standard, dove i valori oscillano solitamente tra 0 e 1).

## Why embeddings are useful for our project
All'interno del progetto **Pizza-Cluster**, basato sull'analisi del dataset JMAIL (legato al caso Epstein), l'utilizzo degli embedding densi è un requisito critico per i seguenti motivi:
1. **Eterogeneità del linguaggio:** I documenti includono email informali, comunicazioni frammentate e atti giudiziari scritti in burocratese. Un approccio a parole chiave (TF-IDF) fallirebbe nel collegare un'email colloquiale a un documento formale che trattano lo stesso identico evento.
2. **Rilevamento di pattern nascosti:** Gli embedding permettono agli algoritmi di clustering (come K-Means o DBSCAN) di aggregare le email in base ai temi caldi effettivi e ai contesti d'affari sottostanti, superando il limite dei sinonimi o dei tentativi di elusione testuale.
3. **Robustezza al rumore:** Errori di battitura minimi o formattazioni markdown residue non distruggono il vettore denso, garantendo stabilità alla pipeline di clustering.

## Limitations and computational cost
Nonostante la loro efficacia, gli embedding densi presentano dei vincoli tecnici da monitorare:
* **Costo Computazionale:** A differenza del calcolo statistico istantaneo di TF-IDF, l'inferenza tramite Sentence Transformers richiede l'esecuzione di una rete neurale profonda. Su dataset di grandi dimensioni (es. 5000+ documenti), il calcolo sequenziale su CPU richiede tempo e memoria RAM significativi.
* **Limite di Contesto (Token Limit):** Il modello `all-MiniLM-L6-v2` ha una finestra di contesto massima di **256 token** (circa 150-200 parole). I testi che superano questa soglia vengono troncati automaticamente durante l'operazione di encoding, rischiando di perdere dettagli importanti situati in fondo alle email più lunghe.
* **Scatola Nera (Interpretabilità):** Un vettore di 384 numeri continui non è direttamente interpretabile. A differenza di TF-IDF, non è possibile determinare con precisione immediata quale specifica parola abbia pesato di più nello spostamento del documento verso un determinato cluster semantico.