# Text Embeddings & Semantic Representation

## From Text to Vectors
I computer e gli algoritmi di machine learning non sono in grado di comprendere direttamente il testo in formato stringa; possono elaborare esclusivamente strutture matematiche come vettori e matrici numeriche. Il processo di conversione del testo in vettori si articola storicamente in due fasi principali:

1. **Tokenizzazione:** Il testo grezzo viene spezzato in unità più piccole (parole, sotto-parole o caratteri) chiamate token.
2. **Vettorizzazione:** A ogni token o sequenza di token viene assegnato uno score numerico o una posizione all'interno di uno spazio geometrico multidimensionale.

L'obiettivo fondamentale delle moderne tecniche di NLP (Natural Language Processing) è fare in modo che questa trasformazione non sia una semplice mappatura arbitraria, ma che riesca a preservare le relazioni sintattiche e semantiche originarie del linguaggio umano.

---

## Sparse vs. Dense Representations
La rappresentazione vettoriale del testo si divide in due grandi paradigmi architetturali:

### Rappresentazioni Sparse (es. TF-IDF, Bag-of-Words)
* **Struttura:** Ogni documento è rappresentato da un vettore la cui lunghezza è pari all'intero vocabolario del dataset. Se una parola non è presente nel documento, il suo valore posizionale è pari a zero.
* **Caratteristiche:** I vettori sono enormi, altamente dimensionali e composti quasi interamente da zeri (*sparsi*).
* **Limiti:** Non catturano il contesto né la semantica. Per un modello TF-IDF, le parole *"acquistare"* e *"comprare"* sono trattate come entità completamente distinte e geometricamente ortogonali, non evidenziando alcuna correlazione logica.

### Rappresentazioni Dense (Vettori di Embedding)
A differenza dei metodi statistici basati sul conteggio, le rappresentazioni dense (o **embedding**) proiettano il testo in uno spazio vettoriale continuo a dimensionalità fissa e ridotta (es. 384 o 768 dimensioni), dove ogni coordinata è un numero decimale (*floating-point*).
* **Caratteristiche:** Tutte le posizioni del vettore memorizzano informazioni, eliminando la presenza massiva di zeri.
* **Vantaggi:** Catturano il significato profondo, i sinonimi e le relazioni contestuali. Concetti semanticamente affini vengono posizionati in punti vicini dello spazio geometrico creato dal modello.

---

## How Dense Embeddings are Created: Mathematical Foundation

[ Testo Grezzo ]
│
▼
[ Tokenizzazione ] ───► Suddivisione in token/sub-words (Vocabolario MiniLM)
│
▼
[ Inizializzazione ] ─► Assegnazione temporanea dei vettori statici di partenza
│
▼
[ Self-Attention ] ──► Calcolo matrici Q, K, V (I pesi cambiano in base al contesto)
│
▼
[ Mean Pooling ] ────► Calcolo del baricentro geometrico di tutti i token della frase
│
▼
[ Vettore Finale ] ──► Array denso a 384 dimensioni pronto per il clustering


I pesi numerici continui che compongono un embedding denso sono il risultato di un processo di ottimizzazione geometrica guidato da reti neurali profonde, basato su tre pilastri:

### 1. L'Ipotesi Distribuzionale (*Distributional Hypothesis*)
L'addestramento si fonda sull'assunto linguistico di John Rupert Firth: *"Riconoscerai una parola dalle compagnie che frequenta"*. Durante il pre-addestramento su miliardi di testi, i modelli apprendono i pesi ottimizzando due task:
* **Masked Language Modeling (MLM):** La rete deve prevedere un token nascosto all'interno di una frase (es. *"Il [MASK] ha firmato l'atto in tribunale"*).
* **Causal Language Modeling:** La rete prevede il token successivo in una sequenza.

Se due termini diversi (es. *"avvocato"* e *"legale"*) appaiono costantemente circondai dagli stessi identici contesti linguistici (*"tribunale"*, *"firmato"*, *"causa"*), l'algoritmo di retropropagazione dell'errore (*backpropagation*) corregge i pesi interni per fare in modo che i loro vettori convergano verso coordinate spaziali vicine.

### 2. Il Meccanismo di Attenzione Dinamica (*Self-Attention*)
I modelli tradizionali assegnavano a una parola un vettore statico, indipendente dal contesto. L'architettura Transformer supera questo limite introducendo il meccanismo di **Self-Attention**, che permette ai pesi di modificarsi dinamicamente in base alle parole circostanti.

Per ogni token, la rete calcola tre matrici: **Query ($Q$)**, **Key ($K$)** e **Value ($V$)**. Il peso finale e la direzione del vettore vengono determinati calcolando il prodotto scalare normalizzato:

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

*Esempio:* Nella frase *"La fiera del libro"*, l'attenzione sposterà i pesi del token *"fiera"* verso il concetto geometrico di *"evento/mercato"*, mentre in *"Una fiera feroce"*, i pesi verranno direzionati verso il quadrante semantico degli *"animali"*.

### 3. Struttura Siamese e Mean Pooling per l'Embedding di Frase
Il modello da noi utilizzato, **`all-MiniLM-L6-v2`**, fa parte della famiglia dei **Sentence Transformers** (SBERT). Utilizza strutture a rete siamese per elaborare coppie di frasi contemporaneamente in fase di fine-tuning, ottimizzando i pesi per riflettere direttamente la similarità tra interi blocchi di testo.

Poiché il Transformer restituisce nativamente un vettore denso per *ciascun token* della frase, per generare un unico embedding finale a **384 dimensioni** che rappresenti l'intero documento si applica un'operazione di **Mean Pooling**:

$$\text{Embedding}_{\text{final}} = \frac{1}{N}\sum_{i=1}^{N} \vec{v}_i$$

L'operazione calcola la media matematica di tutti i vettori dei singoli token (escludendo i token di padding), estraendo il baricentro geometrico del significato complessivo del testo.

---

## Semantic Similarity
Una volta trasformati i testi in vettori densi, la similarità semantica tra due documenti viene calcolata misurando l'angolo formato dai due vettori nello spazio a 384 dimensioni tramite la **Cosine Similarity** (Similarità del Coseno), indipendente dalla lunghezza del testo originario:

$$\text{Cosine Similarity}(A, B) = \frac{A \cdot B}{\|A\| \|B\|}$$

* **Coseno = 1 (Angolo di 0°):** I vettori puntano nella stessa direzione; i testi esprimono un significato semantico identico.
* **Coseno = 0 (Angolo di 90°):** I vettori sono ortogonali; i testi trattano argomenti completamente indipendenti e privi di correlazione logica.

---

## Project Context: Application to Pizza-Cluster

All'interno del progetto **Pizza-Cluster**, incentrato sull'analisi del dataset JMAIL (legato al caso Epstein), l'utilizzo degli embedding densi rispetto alle rappresentazioni sparse rappresenta una scelta architetturale critica:

1. **Gestione dell'eterogeneità linguistica:** I documenti includono email informali, comunicazioni frammentate e atti giudiziari in burocratese. I vettori densi permettono di collegare un'email colloquiale a un documento formale che trattano lo stesso tema, superando il limite dei sinonimi.
2. **Aggregazione per il Clustering:** Fornendo vettori a dimensionalità fissa e densa (384), gli algoritmi di clustering (come il K-Means) possono calcolare le distanze geometriche in modo efficiente, raggruppando le email per contesti d'affari e temi caldi reali.
3. **Robustezza al rumore:** Errori di battitura minimi o formattazioni residue non distruggono la struttura del vettore denso, garantendo stabilità alla pipeline.

## Limitations and Constraints
* **Costo Computazionale:** L'inferenza tramite Sentence Transformers richiede l'esecuzione di una rete neurale profonda. Rispetto alla velocità istantanea del TF-IDF, il calcolo sequenziale su CPU richiede tempo e memoria RAM significativi.
* **Limite di Contesto (Token Limit):** Il modello `all-MiniLM-L6-v2` ha una finestra di contesto massima di **256 token** (circa 150-200 parole). I testi che superano questa soglia vengono troncati automaticamente, rischiando di perdere dettagli situati in fondo alle email più lunghe.
* **Interpretabilità (Scatola Nera):** Un vettore di 384 numeri continui non è direttamente interpretabile. Non è possibile determinare con precisione immediata quale specifica parola abbia pesato di più nel posizionamento del vettore.