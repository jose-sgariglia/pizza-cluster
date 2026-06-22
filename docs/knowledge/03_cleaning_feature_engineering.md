# Cleaning and Feature Engineering (Phase 1)

## Obiettivo

Trasformare il dataset raw JMAIL in un dataset `processed` ottimizzato per gli embeddings e il clustering. In questa fase abbiamo dato priorità alla modularità, alla pulizia delle feature ridondanti e alla strutturazione del testo per i modelli linguistici.

## Input e output

Input:
- `data/raw/jmail_emails.parquet`

Output:
- `data/processed/jmail_emails_processed.parquet`
- `data/metadata/jmail_processing_metadata.json`

## Pipeline Aggiornata (Phase 1)

La pipeline è stata refactorizzata per essere più modulare e configurabile:

1.  **Caricamento & Blacklist:** Utilizzo di costanti centralizzate in `src/utils/constants/preprocessing.py` e filtraggio basato su domini (Task 1).
2.  **Pulizia Testo:** Normalizzazione whitespace e rimozione email promozionali.
3.  **Feature Engineering "Potato" (Pruning):** Rimozione di feature statistiche granulari a favore di indicatori generici e potenti (Task 2).
4.  **Template Strutturato:** Creazione della colonna `combined_text` tramite un template che include metadati (Task 3).
5.  **Validazione:** Controllo integrità e rimozione righe senza testo.

## Feature Engineering: Cosa abbiamo tenuto e aggiunto

Abbiamo applicato una strategia di **Feature Pruning** per ridurre il rumore e migliorare la condivisibilità del dataset:

### Feature Mantenute (Generic & Core)
- `id`, `sender`, `subject`, `to_recipients`, `sent_at_datetime`: Metadati essenziali.
- `attachment_count`: Conteggio allegati (senza flag booleani ridondanti).
- `has_redaction`, `redaction_count`: Presenza e numero di censure.

### Feature Aggiunte (High Value)
- **`redaction_ratio`**: Rapporto tra marker di censura e lunghezza del testo. È un segnale critico: documenti con alto ratio tendono a raggrupparsi in cluster di "documenti sensibili/riservati".
- **`sender_domain`**: Dominio estratto dal mittente per analisi di network.

### Feature Rimosse (Redundant)
Abbiamo rimosso `sent_hour`, `sent_year`, `is_weekend`, `subject_length`, ecc. poiché sono derivabili dal timestamp e appesantiscono l'analisi senza aggiungere segnale semantico diretto agli embeddings.

## Il Template Strutturato (Task 3)

Per migliorare la comprensione del modello di embedding, non inviamo più solo il corpo della mail, ma un testo formattato:

```text
DATE: {date}
FROM: {sender}
TO: {recipients}
SUBJECT: {subject}

BODY:
{body}
```

**Perché è importante?** I modelli di Sentence Embedding moderni (come BGE o BERT) sono sensibili alla struttura. Includere i metadati direttamente nel testo permette al modello di "vedere" le relazioni temporali e di network durante il calcolo della similarità semantica.

## Modularità: `preprocessing.py` e `.env`

Abbiamo rimosso tutte le costanti "hardcodate" da `data_processing.py`.
- **Regex e Blacklist:** Gestite in `src/utils/constants/preprocessing.py`.
- **Configurabilità:** Il template è salvato nel `.env`. Questo permette di sperimentare diverse strutture di testo senza modificare il codice sorgente.

## Mini spiegazione dei concetti

- **Feature Pruning:** L'arte di rimuovere variabili che non aggiungono informazioni uniche. In ML, meno feature spesso significano modelli più robusti e meno overfitting.
- **Redaction Ratio:** Una metrica di densità. Non ci dice solo *se* c'è una censura, ma quanto il documento è "coperto", riflettendo il livello di segretezza o sensibilità.
- **Structured Prompting for Embeddings:** Tecnica che consiste nel dare una struttura fissa al testo (tipo JSON o template testuale) per aiutare il modello a distinguere tra metadati e contenuto.

## Approfondimenti e Risorse di Studio

- **Feature Engineering & Selection:** [Google ML Crash Course - Feature Engineering](https://developers.google.com/machine-learning/data-prep/transform/feature-engineering)
- **Sentence Embeddings Context:** [SBERT Contextual Information](https://www.sbert.net/examples/applications/semantic-search/README.html)
- **Redaction in NLP:** [Handling Sensitive Data in NLP](https://arxiv.org/abs/2010.06053) (Paper sulla de-identificazione).
- **Pythonic Constants:** [Best Practices for Constants in Python](https://realpython.com/python-constants/)

---

## Boilerplate Detection: Separazione del Disclaimer Legale

### Cos'è il problema

Le email corporate contengono frequentemente, in coda al corpo, un blocco di disclaimer legale standardizzato:

> *"This e-mail is intended only for the use of the individual to whom it is addressed and may contain information that is privileged, confidential..."*

Questo testo:
- È **semanticamente identico** in migliaia di email → introduce rumore massivo per gli embeddings
- Crea un **cluster artificiale** che raggruppa email per presenza di disclaimer piuttosto che per contenuto
- Aggiunge token ripetitivi che abbassano la qualità della rappresentazione vettoriale

### Approccio: euristica posizionale a due strategie

Non è necessario un modello ML. Le email di JMAIL sono email corporate (periodo 1999–2002) con disclaimer standardizzati e struttura prevedibile. Vengono applicate due strategie in cascata con postura **safe by default**: in caso di incertezza il testo originale viene restituito invariato.

**Strategia 1 — Delimitatore strutturale + conferma keyword**

Si cerca una riga separatore composta esclusivamente da caratteri ripetuti (`---`, `___`, `===`, ...). Se trovata, si verifica che nei primi 500 caratteri del testo successivo sia presente almeno una keyword di disclaimer. La conferma è obbligatoria: un `---` senza keyword (firma personale, separatore Markdown) viene ignorato.

**Strategia 2 — Keyword anchor posizionale**

Se nessun delimitatore strutturale è trovato, si cerca una keyword di disclaimer nell'**ultimo 30% delle righe**. Il vincolo posizionale è il principale presidio contro i falsi positivi: un'email che discute di clausole di riservatezza le avrà nel corpo centrale, non in coda.

In entrambe le strategie: se il corpo residuo risulterebbe vuoto, il testo viene restituito invariato.

### Keyword anchors censiti

Tutti i pattern sono phrase-level per ridurre i falsi positivi. I termini ambigui come `disclaimer` o `legal notice` sono accettati solo se seguiti da `:`.

| Pattern | Esempio tipico |
|---|---|
| `this e-mail is intended/confidential/privileged` | "This e-mail is intended only for..." |
| `privileged and confidential` | "PRIVILEGED AND CONFIDENTIAL" |
| `if you received this e-mail in error` | "If you have received this message in error..." |
| `the information contained in this e-mail` | "The information contained in this communication..." |
| `disclaimer:` | "Disclaimer: This email and any files..." |
| `confidentiality notice:` | "Confidentiality Notice: ..." |
| `delete it/this from your system/computer` | "...please delete it from your system." |

### Impatto sul dataset processed

| Feature | Tipo | Descrizione |
|---|---|---|
| `content_clean` | `string` | Corpo dell'email senza disclaimer |
| `has_disclaimer` | `bool` | `True` se un disclaimer è stato rilevato e separato |

`combined_text` e il template di embedding beneficiano automaticamente della pulizia di `content_clean`, in quanto `combined_text` viene costruito da `content_clean`.

### Limiti noti

- **Forward headers** (`----- Original Message -----`, catene di risposta): fuori scope qui, implementati separatamente — vedi sezione **"Thread/Quote Stripping"** più sotto. **Vincolo d'ordine**: `split_body_disclaimer` deve girare su testo con newline intatti (cerca righe separatore e posizione nell'ultimo 30% delle righe), quindi qualunque step venga aggiunto a monte o a valle nella stessa fase "Pulizia Testo" deve preservare i newline fino a quando entrambi gli step posizionali (disclaimer e thread-split) non sono stati eseguiti — la normalizzazione whitespace (che collassa i `\n`) deve avvenire dopo entrambi, non in mezzo. Questo ordine è stato verificato a seguito di un bug analogo riscontrato sul thread-split (v. sotto).
- **Falsi negativi**: disclaimer senza delimitatori strutturali e senza le keyword censite non vengono rilevati. Preferibile a un falso positivo che strippa contenuto reale.
- **Calibrazione posizionale**: la soglia del 30% è un valore di partenza ragionevole; può essere abbassata se i test su dati reali mostrano falsi negativi sistematici.

### Dove si trova nel codice

- **Costanti**: `src/utils/constants/preprocessing.py` → `DISCLAIMER_DELIMITER_RE`, `DISCLAIMER_KEYWORD_ANCHORS`
- **Funzione**: `src/utils/data_processing.py` → `split_body_disclaimer(text) -> tuple[str, str | None]`
- **Integrazione**: chiamata dentro `add_text_features()`, prima della normalizzazione del testo

### Mini spiegazione: perché non ML?

Un classificatore ML per la segmentazione email (es. CRF, BERT fine-tuned) richiederebbe dati annotati, dipendenze pesanti e pipeline di inferenza. Per questo dataset le regole heuristiche sono preferibili perché:
1. Il dominio è ristretto (email corporate US, anni 1999–2002)
2. I disclaimer sono strutturalmente uniformi
3. Il costo di un falso positivo (testo utile rimosso) è alto → meglio sbagliare in direzione conservativa
4. Le regole sono ispezionabili e modificabili senza retraining

### Approfondimenti

Paper:
Carvalho, V. R., & Cohen, W. W. (2004). *Learning to Extract Signature and Reply Lines from Email*. CEAS 2004.
[Citato in Mailgun Talon](https://github.com/mailgun/talon) — libreria open source che formalizza questo problema con approccio ML ibrido.

Documentazione:
RFC 2822 — *Internet Message Format* (struttura formale delle email, include la convenzione `-- ` come separatore firma):
https://www.ietf.org/rfc/rfc2822.txt

Risorsa studio:
[Real Python — Regex in Python](https://realpython.com/regex-python/) — guida pratica all'uso di `re` per text processing strutturato.

---

## Thread/Quote Stripping: Separazione del Contenuto Citato

### Cos'è il problema

Le email di JMAIL sono in larga parte reply/forward che includono, dentro il body, il testo della conversazione precedente (quote di reply, blocchi di forward). Questo contenuto:

- È spesso **duplicato** rispetto a un'altra email già presente nel dataset (l'originale quotata), introducendo ridondanza per il clustering
- Aumenta artificialmente la lunghezza del testo da inviare agli embeddings, sprecando token-budget su contenuto già rappresentato altrove
- Rende ambiguo cosa stia effettivamente "dicendo" il mittente di una specifica email, mescolando voce propria e voce citata

A differenza del disclaimer (blocco fisso, sempre uguale, sempre in coda), il contenuto citato è strutturalmente vario: può comparire con marker diversi, annidato a più livelli (reply di una reply), e occupare una porzione qualsiasi del body — non solo la coda.

### Approccio: rilevamento marker per posizione, niente parsing ricorsivo dei sotto-blocchi

Come per il disclaimer, si è scelto un approccio basato su regole piuttosto che ML, per le stesse motivazioni di dominio ristretto e struttura prevedibile. La differenza principale rispetto al disclaimer è che qui i marker possono comparire ovunque nel testo, non solo in coda, quindi la logica è basata su **posizione del primo marker trovato**, non su ancoraggio a fine documento.

La funzione individua il **primo marker di quote/forward che compare nel testo, per posizione** (indipendentemente da quale dei tipi sotto elencati sia), e usa quel punto come taglio:

- **`content_new`**: tutto il testo prima del primo marker — il contenuto scritto dal mittente di questa specifica email.
- **`content_quoted`**: tutto il testo dal marker in poi, **conservato per intero in un unico blocco**. Non viene fatto parsing ricorsivo dei sotto-blocchi annidati (reply-di-reply-di-reply): il contenuto viene preservato ma non ulteriormente strutturato, per due motivi validati sui dati — (1) il contenuto "nuovo" sepolto in catene profonde è risultato mediamente marginale (~2% del body totale su un campione di annidamento profondo), quindi il guadagno di un parsing ricorsivo completo non giustifica la complessità; (2) conservare il blocco intero (anziché scartarlo) evita perdita di informazione nei casi in cui l'email originale quotata non sia presente nel dataset come riga a sé stante.

**Postura sui risultati corti o vuoti — scelta deliberatamente diversa da quella del disclaimer**: un `content_new` vuoto o molto corto dopo lo split **non viene considerato un fallimento e non comporta fallback al testo originale**. È stato verificato sui dati che è un risultato legittimo e frequente: forward puri senza commento aggiunto, o reply brevissime ("ok", "+1"). Per questo motivo non si applica qui la stessa regola "safe by default" del disclaimer (restituire il testo invariato se il residuo è vuoto) — quella regola ha senso per il disclaimer perché un disclaimer non occupa mai il 100% di un corpo email legittimo, mentre un `content_new` vuoto/corto è un esito normale e informativo, non un sintomo di rilevamento fallito.

### Marker rilevati, per forza del segnale osservata sui dati

| Marker | % email con thread che lo contengono | Esempio tipico |
|---|---|---|
| `ON_DATE_WROTE` | ~82% | "On Jan 12, 2019, at 10:11 AM, Nili Priell wrote:" |
| `OUTLOOK_HEADER_BLOCK` | ~22% | "From: ... ↵ Date: ... ↵ Subject: ... ↵ To: ..." (ancorato a inizio riga, non precedute da `>`) |
| `CHEVRON_QUOTE` | ~19% | righe che iniziano con `>` |
| `BEGIN_FORWARDED` | ~13% | "Begin forwarded message:" |
| `ORIGINAL_MSG_DASHES` | ~5% | "-----Original Message-----" (varianti tolleranti su n° dash) |
| `FORWARDED_DASHES` | ~1% | "------- Forwarded message -------" |
| `FWD_BY_LINE` | ~1% | "----- Forwarded by [nome] on [data] -----" |

Nota: `OUTLOOK_HEADER_BLOCK` e `CHEVRON_QUOTE` sono stati verificati empiricamente come **sempre blocchi distinti**, non annidati l'uno nell'altro — la regex dell'header Outlook richiede `^From:` a inizio riga esatto, che non matcha mai `> From:`. I due tipi sono quindi gestiti come marker separati, ciascuno can la propria regex, valutati insieme per trovare quale compare prima nel testo.

Sono gestite anche varianti minori corrotte da OCR (numero di dash asimmetrico, es. `---Original Message` senza chiusura) — fenomeno marginale (<1% del campione), gestito con tolleranza nella regex su spazi/dash, senza fuzzy-matching pesante.

### Impatto sul dataset processed

| Feature | Tipo | Descrizione |
|---|---|---|
| `content_new` | `string` | Testo prima del primo marker di quote/forward (può essere vuoto) |
| `content_quoted` | `string` | Testo dal marker in poi, conservato per intero (vuoto se nessun marker trovato) |
| `has_thread` | `bool` | `True` se è stato trovato almeno un marker |
| `content_new_is_short` | `bool` | `True` se `content_new` ha meno di 20 caratteri dopo strip — **flag diagnostico per QA, non modifica il comportamento del parsing** |

`content_quoted` non viene scartato: resta disponibile come colonna a parte per eventuale uso downstream (es. context-building, recupero di informazione quando l'email originale non è presente come riga separata nel dataset). Il template di embedding (Task 3) oggi usa il body completo; resta da decidere — in coordinamento con la fase Embedding — se passare `content_new` al posto del body intero nel template, e se/come sfruttare `content_quoted` e `has_thread` come segnale aggiuntivo.

### Bug noto e risolto: ordine delle operazioni rispetto alla normalizzazione whitespace

Durante la validazione è emerso che il thread-splitting, se eseguito **dopo** la normalizzazione whitespace (che collassa ogni sequenza di whitespace incluso `\n` in un singolo spazio), perde il 96.5% dei segnali: i pattern usano ancore `^` in modalità multiline, che senza newline non matchano (eccetto a inizio stringa). Il sintomo osservato era un crollo di `has_thread` dal ~20% atteso a un 1.7% osservato, con il flag `content_new_is_short` risultante sempre `True` per le poche email rilevate (falso segnale diagnostico, non rappresentativo del fenomeno reale).

**Fix adottato**: il thread-splitting opera su testo **pre-normalizzazione** (newline intatti), non sul testo già passato dalla normalizzazione whitespace. Stessa logica di vincolo d'ordine già presente per `split_body_disclaimer` (v. sezione disclaimer, "Limiti noti") — entrambi gli step posizionali devono precedere il collasso dei whitespace nella pipeline.

> **Nota per revisione**: l'ordine esatto e attuale tra `split_body_disclaimer`, thread-splitting e normalizzazione whitespace nel codice va riverificato a valle di questo fix, per assicurarsi che il thread-splitting riceva testo già passato dallo strip del disclaimer (evitando falsi marker generati da testo di disclaimer) ma non ancora normalizzato. Verifica lasciata in carico a chi revisiona.

### Limiti noti

- **Nessun parsing ricorsivo dei sotto-blocchi annidati**: scelta deliberata, vedi sopra (guadagno marginale, validato sui dati).
- **Falso positivo isolato osservato**: un caso su ~2000 in cui un marker è scattato per un match accidentale dentro il testo di un link/URL in una newsletter, non per un vero quote. Frequenza bassa, non ancora affrontato con una regola dedicata.
- **Entity Normalization** (es. "Joe Doe" / "Mr Joe" / "Joe Jack Doe" come stessa persona) è stata valutata e **deliberatamente posticipata in fondo al backlog**: utile in linea di principio ma costosa da fare bene su scala, con beneficio marginale incerto rispetto alla priorità di pulizia quote/disclaimer.

### Dove si trova nel codice

- **Costanti**: `src/utils/constants/preprocessing.py` (regex dei 7 marker)
- **Funzione**: `src/utils/data_pr# Cleaning and Feature Engineering (Phase 1)

## Obiettivo

Trasformare il dataset raw JMAIL in un dataset `processed` ottimizzato per gli embeddings e il clustering. In questa fase abbiamo dato priorità alla modularità, alla pulizia delle feature ridondanti e alla strutturazione del testo per i modelli linguistici.

## Input e output

Input:
- `data/raw/jmail_emails.parquet`

Output:
- `data/processed/jmail_emails_processed.parquet`
- `data/metadata/jmail_processing_metadata.json`

## Pipeline Aggiornata (Phase 1)

La pipeline è stata refactorizzata per essere più modulare e configurabile:

1.  **Caricamento & Blacklist:** Utilizzo di costanti centralizzate in `src/utils/constants/preprocessing.py` e filtraggio basato su domini (Task 1).
2.  **Pulizia Testo:** Normalizzazione whitespace e rimozione email promozionali.
3.  **Feature Engineering "Potato" (Pruning):** Rimozione di feature statistiche granulari a favore di indicatori generici e potenti (Task 2).
4.  **Template Strutturato:** Creazione della colonna `combined_text` tramite un template che include metadati (Task 3).
5.  **Validazione:** Controllo integrità e rimozione righe senza testo.

## Feature Engineering: Cosa abbiamo tenuto e aggiunto

Abbiamo applicato una strategia di **Feature Pruning** per ridurre il rumore e migliorare la condivisibilità del dataset:

### Feature Mantenute (Generic & Core)
- `id`, `sender`, `subject`, `to_recipients`, `sent_at_datetime`: Metadati essenziali.
- `attachment_count`: Conteggio allegati (senza flag booleani ridondanti).
- `has_redaction`, `redaction_count`: Presenza e numero di censure.

### Feature Aggiunte (High Value)
- **`redaction_ratio`**: Rapporto tra marker di censura e lunghezza del testo. È un segnale critico: documenti con alto ratio tendono a raggrupparsi in cluster di "documenti sensibili/riservati".
- **`sender_domain`**: Dominio estratto dal mittente per analisi di network.

### Feature Rimosse (Redundant)
Abbiamo rimosso `sent_hour`, `sent_year`, `is_weekend`, `subject_length`, ecc. poiché sono derivabili dal timestamp e appesantiscono l'analisi senza aggiungere segnale semantico diretto agli embeddings.

## Il Template Strutturato (Task 3)

Per migliorare la comprensione del modello di embedding, non inviamo più solo il corpo della mail, ma un testo formattato:

```text
DATE: {date}
FROM: {sender}
TO: {recipients}
SUBJECT: {subject}

BODY:
{body}
```

**Perché è importante?** I modelli di Sentence Embedding moderni (come BGE o BERT) sono sensibili alla struttura. Includere i metadati direttamente nel testo permette al modello di "vedere" le relazioni temporali e di network durante il calcolo della similarità semantica.

## Modularità: `preprocessing.py` e `.env`

Abbiamo rimosso tutte le costanti "hardcodate" da `data_processing.py`.
- **Regex e Blacklist:** Gestite in `src/utils/constants/preprocessing.py`.
- **Configurabilità:** Il template è salvato nel `.env`. Questo permette di sperimentare diverse strutture di testo senza modificare il codice sorgente.

## Mini spiegazione dei concetti

- **Feature Pruning:** L'arte di rimuovere variabili che non aggiungono informazioni uniche. In ML, meno feature spesso significano modelli più robusti e meno overfitting.
- **Redaction Ratio:** Una metrica di densità. Non ci dice solo *se* c'è una censura, ma quanto il documento è "coperto", riflettendo il livello di segretezza o sensibilità.
- **Structured Prompting for Embeddings:** Tecnica che consiste nel dare una struttura fissa al testo (tipo JSON o template testuale) per aiutare il modello a distinguere tra metadati e contenuto.

## Approfondimenti e Risorse di Studio

- **Feature Engineering & Selection:** [Google ML Crash Course - Feature Engineering](https://developers.google.com/machine-learning/data-prep/transform/feature-engineering)
- **Sentence Embeddings Context:** [SBERT Contextual Information](https://www.sbert.net/examples/applications/semantic-search/README.html)
- **Redaction in NLP:** [Handling Sensitive Data in NLP](https://arxiv.org/abs/2010.06053) (Paper sulla de-identificazione).
- **Pythonic Constants:** [Best Practices for Constants in Python](https://realpython.com/python-constants/)

---

## Boilerplate Detection: Separazione del Disclaimer Legale

### Cos'è il problema

Le email corporate contengono frequentemente, in coda al corpo, un blocco di disclaimer legale standardizzato:

> *"This e-mail is intended only for the use of the individual to whom it is addressed and may contain information that is privileged, confidential..."*

Questo testo:
- È **semanticamente identico** in migliaia di email → introduce rumore massivo per gli embeddings
- Crea un **cluster artificiale** che raggruppa email per presenza di disclaimer piuttosto che per contenuto
- Aggiunge token ripetitivi che abbassano la qualità della rappresentazione vettoriale

### Approccio: euristica posizionale a due strategie

Non è necessario un modello ML. Le email di JMAIL sono email corporate (periodo 1999–2002) con disclaimer standardizzati e struttura prevedibile. Vengono applicate due strategie in cascata con postura **safe by default**: in caso di incertezza il testo originale viene restituito invariato.

**Strategia 1 — Delimitatore strutturale + conferma keyword**

Si cerca una riga separatore composta esclusivamente da caratteri ripetuti (`---`, `___`, `===`, ...). Se trovata, si verifica che nei primi 500 caratteri del testo successivo sia presente almeno una keyword di disclaimer. La conferma è obbligatoria: un `---` senza keyword (firma personale, separatore Markdown) viene ignorato.

**Strategia 2 — Keyword anchor posizionale**

Se nessun delimitatore strutturale è trovato, si cerca una keyword di disclaimer nell'**ultimo 30% delle righe**. Il vincolo posizionale è il principale presidio contro i falsi positivi: un'email che discute di clausole di riservatezza le avrà nel corpo centrale, non in coda.

In entrambe le strategie: se il corpo residuo risulterebbe vuoto, il testo viene restituito invariato.

### Keyword anchors censiti

Tutti i pattern sono phrase-level per ridurre i falsi positivi. I termini ambigui come `disclaimer` o `legal notice` sono accettati solo se seguiti da `:`.

| Pattern | Esempio tipico |
|---|---|
| `this e-mail is intended/confidential/privileged` | "This e-mail is intended only for..." |
| `privileged and confidential` | "PRIVILEGED AND CONFIDENTIAL" |
| `if you received this e-mail in error` | "If you have received this message in error..." |
| `the information contained in this e-mail` | "The information contained in this communication..." |
| `disclaimer:` | "Disclaimer: This email and any files..." |
| `confidentiality notice:` | "Confidentiality Notice: ..." |
| `delete it/this from your system/computer` | "...please delete it from your system." |

### Impatto sul dataset processed

| Feature | Tipo | Descrizione |
|---|---|---|
| `content_clean` | `string` | Corpo dell'email senza disclaimer |
| `has_disclaimer` | `bool` | `True` se un disclaimer è stato rilevato e separato |

`combined_text` e il template di embedding beneficiano automaticamente della pulizia di `content_clean`, in quanto `combined_text` viene costruito da `content_clean`.

### Limiti noti

- **Forward headers** (`----- Original Message -----`, catene di risposta): fuori scope, gestiti in una task separata del backlog.
- **Falsi negativi**: disclaimer senza delimitatori strutturali e senza le keyword censite non vengono rilevati. Preferibile a un falso positivo che strippa contenuto reale.
- **Calibrazione posizionale**: la soglia del 30% è un valore di partenza ragionevole; può essere abbassata se i test su dati reali mostrano falsi negativi sistematici.

### Dove si trova nel codice

- **Costanti**: `src/utils/constants/preprocessing.py` → `DISCLAIMER_DELIMITER_RE`, `DISCLAIMER_KEYWORD_ANCHORS`
- **Funzione**: `src/utils/data_processing.py` → `split_body_disclaimer(text) -> tuple[str, str | None]`
- **Integrazione**: chiamata dentro `add_text_features()`, prima della normalizzazione del testo

### Mini spiegazione: perché non ML?

Un classificatore ML per la segmentazione email (es. CRF, BERT fine-tuned) richiederebbe dati annotati, dipendenze pesanti e pipeline di inferenza. Per questo dataset le regole heuristiche sono preferibili perché:
1. Il dominio è ristretto (email corporate US, anni 1999–2002)
2. I disclaimer sono strutturalmente uniformi
3. Il costo di un falso positivo (testo utile rimosso) è alto → meglio sbagliare in direzione conservativa
4. Le regole sono ispezionabili e modificabili senza retraining

### Approfondimenti

Paper:
Carvalho, V. R., & Cohen, W. W. (2004). *Learning to Extract Signature and Reply Lines from Email*. CEAS 2004.
[Citato in Mailgun Talon](https://github.com/mailgun/talon) — libreria open source che formalizza questo problema con approccio ML ibrido.

Documentazione:
RFC 2822 — *Internet Message Format* (struttura formale delle email, include la convenzione `-- ` come separatore firma):
https://www.ietf.org/rfc/rfc2822.txt

Risorsa studio:
[Real Python — Regex in Python](https://realpython.com/regex-python/) — guida pratica all'uso di `re` per text processing strutturato.

---

## Prossimi Passi: Phase 2 - Embedding Strategy

Nella Phase 2 ci occuperemo di trasformare il testo strutturato in vettori matematici:
1.  **Scelta del Modello:** Validazione del modello `BAAI/bge-small-en-v1.5` (ottimo rapporto prestazioni/velocità).
2.  **Chunking Strategy:** Gestione delle email molto lunghe che superano il limite di token del modello (512 token).
3.  **Vettorizzazione:** Generazione degli embeddings e salvataggio in formato NumPy per alte prestazioni.
4.  **Validazione Semantica:** Test di similarità per assicurarci che email simili finiscano "vicine" nello spazio vettoriale.
ocessing.py` (funzione di thread-splitting, integrata in `add_text_features()`)
- **Notebook**: `src/notebook/pipeling_processing.ipynb` — celle di esecuzione e validazione (grafici distribuzione lunghezza, breakdown frequenza marker)

---



Nella Phase 2 ci occuperemo di trasformare il testo strutturato in vettori matematici:
1.  **Scelta del Modello:** Validazione del modello `BAAI/bge-small-en-v1.5` (ottimo rapporto prestazioni/velocità).
2.  **Chunking Strategy:** Gestione delle email molto lunghe che superano il limite di token del modello (512 token).
3.  **Vettorizzazione:** Generazione degli embeddings e salvataggio in formato NumPy per alte prestazioni.
4.  **Validazione Semantica:** Test di similarità per assicurarci che email simili finiscano "vicine" nello spazio vettoriale.