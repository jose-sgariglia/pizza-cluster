# Text Preprocessing

## Goal
L'obiettivo di questo modulo è implementare una pipeline di pulizia testuale deterministica per trasformare i campi grezzi delle email (`subject` e `content_markdown`) in un unico campo standardizzato denominato `clean_text`. Questo campo servirà da base coerente per le successive fasi di estrazione delle feature (TF-IDF, Dense Embeddings) e clustering.

## Cleaning operations
La pipeline esegue in modo sequenziale le seguenti operazioni logiche tramite espressioni regolari:
1. **Normalizzazione:** Conversione dell'intero testo in caratteri minuscoli.
2. **Rimozione URL:** Eliminazione di stringhe di protocollo web per evitare che stringhe casuali di link alterino la frequenza delle parole.
3. **Rimozione Email:** Pulizia degli indirizzi email per evitare aggregazioni errate basate sui soli indirizzi dei mittenti/destinatari.
4. **Rimozione Spazi Extra:** Compressione di tabulazioni, spazi multipli e rinvii a capo in singoli spazi standard.

## Stop words
Le stop words sono parole estremamente frequenti in una lingua (articoli, preposizioni, congiunzioni) che non aggiungono informazioni discriminanti sul contenuto del testo. 
* *Nota di progetto:* Nella nostra pipeline attuale non rimuoviamo attivamente le stop words nel file `.py` perché i modelli di Transformer (come `all-MiniLM-L6-v2`) sfruttano l'ordine delle parole e la struttura della frase per generare l'embedding corretto. La rimozione selettiva verrà delegata eventualmente alla sola vectorization TF-IDF.

## Email-specific noise
Il dataset JMAIL presenta anomalie tipiche della corrispondenza elettronica:
* Pattern ripetitivi di inoltro/risposta (`Re:`, `Fwd:`).
* Firme automatiche e indirizzi di posta elettronica all'interno del corpo del testo.
L'eliminazione di questi elementi impedisce agli algoritmi di clustering (come il K-Means) di raggruppare erroneamente le email solo perché condividono la stessa firma o lo stesso dominio mail di provenienza.

## Our preprocessing choices
Si è scelto di mantenere un approccio conservativo: non è stata applicata la lemmatizzazione o lo stemming in questa fase per non distruggere le relazioni sintattiche profonde necessarie ai modelli neurali densi, garantendo al contempo prestazioni fulminee durante l'elaborazione su CPU.

## Examples before/after cleaning
* **Prima:** `Re: Meeting tomorrow! Please check https://jmail.world/schedule or contact team@jmail.world.`
* **Dopo:** `re: meeting tomorrow! please check or contact` *(seguito dalla rimozione degli spazi in eccesso)*.