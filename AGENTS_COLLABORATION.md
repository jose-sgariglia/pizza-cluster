# AGENTS COLLABORATION

## Scopo

Definire regole operative condivise per far collaborare due sviluppatori sul progetto Pizza Cluster. Uno sviluppatore usa Codex, l'altro usa Antigravity. Il lavoro e' asincrono e passa da Git/GitHub, branch, pull request, review e merge.

Questo file integra `AGENT.md`. In caso di conflitto, `AGENT.md` ha priorita'.

## Principi

- Ogni task deve avere uno sviluppatore owner esplicito.
- Ogni task deve dichiarare stream, branch e file principali.
- Gli assistenti supportano gli sviluppatori, ma non sono owner autonomi delle decisioni.
- Due branch possono procedere in parallelo se hanno contratti dati chiari.
- Le PR devono dichiarare cambi a schema, path, dipendenze e artefatti.
- Le decisioni architetturali richiedono proposta, pro/contro e approvazione umana.
- Ogni modifica significativa deve lasciare traccia in documentazione, test o diario.
- L'ambiente Python di riferimento e' `uv`.

## Stream Di Lavoro

### Stream A - Embeddings, Studio, Analisi

Owner proposto: sviluppatore con Codex.

Responsabilita':

- ricerca modelli embedding;
- pipeline embeddings;
- generazione baseline;
- confronto embeddings prima/dopo feature engineering;
- studio metriche sugli embeddings;
- documentazione tecnica su modelli e parametri.

Branch consigliate:

- `feature/embeddings-baseline`
- `feature/embedding-analysis`

### Stream B - Feature Engineering, Estrazione Feature, Documentazione

Owner proposto: sviluppatore con Antigravity.

Responsabilita':

- miglioramento preprocessing;
- feature engineering testuale e metadata;
- estrazione feature interpretabili;
- documentazione contenutistica;
- aggiornamento contratti dati processed/features.

Branch consigliate:

- `feature/feature-engineering`
- `feature/processed-contracts`

### Stream C - Integrazione Clustering

Owner: da assegnare dopo ricongiungimento degli stream A e B.

Responsabilita':

- usare embeddings e feature stabili;
- confrontare clustering su baseline e dati arricchiti;
- produrre metriche e report;
- proporre modello candidato.

## File Ownership

Prima di iniziare, ogni sviluppatore deve dichiarare:

- branch di lavoro;
- stream;
- file che intende modificare;
- file che intende solo leggere;
- output attesi;
- test o controlli che eseguira'.

File sensibili da modificare uno alla volta:

- `Diary.md`
- `TODO.md`
- `ROADMAP.md`
- `DECISIONS.md`
- `DATA_CONTRACTS.md`
- `.env`
- `.env.sample`
- `requirements.txt`
- moduli condivisi in `src/utils`

## Git/GitHub

Branch consigliate:

- `main`: stato stabile.
- `develop` o `integration`: integrazione, se il team decide di usarla.
- `feature/embeddings-*`: stream A.
- `feature/feature-engineering-*`: stream B.
- `feature/clustering-*`: stream C.
- `docs/*`: documentazione trasversale.

Regole:

- prima di iniziare, eseguire `git fetch` e aggiornarsi dalla base concordata;
- lavorare su branch piccole e tematiche;
- aprire PR con descrizione di obiettivo, stream, test e impatti;
- evitare PR che mescolano refactor, nuova logica, notebook e documentazione non collegata;
- prima del merge, rieseguire `uv run python -m pytest -q`;
- se una PR cambia contratti dati, aggiornare `DATA_CONTRACTS.md`.

## Parallelizzazione

Parallelizzabili:

- stream A genera embeddings baseline mentre stream B migliora feature engineering;
- stream A studia modelli embedding mentre stream B documenta e testa feature;
- stream B stabilizza `processed` e `DATA_CONTRACTS.md` mentre stream A prepara confronto;
- notebook diagnostici su artefatti gia' prodotti;
- documentazione non sovrapposta.

Da serializzare o integrare con attenzione:

- cambio schema processed;
- cambio colonna input per embeddings;
- introduzione dipendenze pesanti;
- refactor path `.env`;
- clustering finale;
- API/demo basate sui cluster.

## Template Task

```md
Task:
Owner:
Stream:
Branch:
Stato: Ready | In progress | Blocked | Done
File scrivibili:
File in sola lettura:
Input attesi:
Output attesi:
Test/comandi:
Documentazione da aggiornare:
Dipendenze:
Rischi:
```

## Handoff

Quando uno sviluppatore termina un task deve riportare:

- cosa ha cambiato;
- branch e PR, se presenti;
- file toccati;
- test o verifiche eseguite;
- output prodotti;
- rischi residui;
- decisioni ancora aperte.

Formato consigliato:

```md
Handoff:
Owner:
Stream:
Branch:
PR:
Task:
File modificati:
Test:
Output:
Rischi:
Prossimo passo:
```

## Comandi Standard

Installare dipendenze:

```bash
uv pip install <package>
```

Eseguire test completi:

```bash
uv run python -m pytest -q
```

Eseguire un singolo file di test:

```bash
uv run python -m pytest tests/test_nome.py -q
```

## Ricongiungimento Stream A/B

Quando embeddings e feature engineering sono entrambi pronti:

1. mergiare lo stream B su branch di integrazione;
2. verificare `DATA_CONTRACTS.md`;
3. rigenerare embeddings sul processed/features aggiornato;
4. confrontare baseline vs dataset arricchito;
5. documentare differenze;
6. aprire stream C clustering.

## Gestione Conflitti Git

Se due branch modificano lo stesso file:

1. identificare quale stream possiede il contratto del file;
2. fare merge/rebase dalla base concordata;
3. risolvere conflitti mantenendo il contratto dati aggiornato;
4. rieseguire test;
5. dichiarare nella PR come e' stato risolto il conflitto.
