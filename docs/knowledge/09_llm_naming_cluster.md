# LLM Naming per Riassumere i Cluster

## Cos'è
L'LLM Naming è una tecnica di *Generative Topic Labeling*. Dopo aver estratto statisticamente le parole chiave grezze di un cluster (usando algoritmi come c-TF-IDF, YAKE o KeyBERT), si passa questa lista di keyword a un Large Language Model (nel nostro caso Ollama locale con modello Qwen). Si chiede all'LLM di leggere le keyword e sintetizzarle in un unico "titolo" o etichetta descrittiva di 1-2 parole.

## Quando usarlo
È estremamente utile nell'ultima fase di una pipeline di clustering testuale, quando si deve presentare il risultato finale a un essere umano o esporlo su una dashboard. Le keyword grezze (es. `['fed', 'crim', 'sdny', 'confidential']`) richiedono un forte sforzo di interpretazione, mentre l'LLM può generare un titolo immediato e leggibile (es. `Legal Subpoenas`).

## Pro
- **Alta Interpretabilità**: Produce etichette umanamente leggibili e dirette.
- **Sintesi Semantica**: Un LLM riesce a trovare un concetto "cappello" che raggruppa le varie keyword sfaccettate.
- **Zero-Shot**: Non richiede addestramento o fine-tuning, basta configurare correttamente il prompt.

## Contro
- **Latenza e Costo Computazionale**: Richiede una chiamata API per ogni cluster, che può essere lenta se fatta localmente senza GPU.
- **Rischio Allucinazioni**: Se il prompt non è vincolante o la temperatura del modello non è bassa (es. 0.1), l'LLM potrebbe iniziare a spiegare, aggiungere punteggiatura inutile o inventare titoli fuori contesto.

## Alternative
- Usare la top-1 keyword del c-TF-IDF come titolo.
- Estrarre l'entità più frequente tramite NER (Named Entity Recognition).

## Link utili
- Ollama API Documentation: https://github.com/ollama/ollama/blob/main/docs/api.md
- Riferimento teorico (Generative Topic Labeling): https://arxiv.org/abs/2309.00161

# Argomenti da studiare / approfondire per la comprensione
- Prompt Engineering restrittivo (manipolazione di temperature, vincoli di lunghezza e formato output).
- Zero-Shot Summarization.
- Gestione chiamate HTTP asincrone/sincrone tramite API REST (libreria `requests`).
