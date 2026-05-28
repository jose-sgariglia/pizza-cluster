# Agent Workflow

## Cos'e'

Workflow operativo per coordinare due sviluppatori sul progetto Pizza Cluster. Uno sviluppatore usa Codex, l'altro usa Antigravity. Il lavoro avviene in modo asincrono tramite Git/GitHub.

L'obiettivo e' rendere chiaro quale stream di lavoro porta avanti ciascuno, su quale branch, con quali contratti dati e con quali verifiche prima di aprire o mergiare una pull request.

## Perche' serve

Con due sviluppatori e due assistenti diversi, il rischio principale non e' solo il conflitto Git: e' la divergenza di assunzioni. Uno stream puo' cambiare un contratto dati, un path o una colonna mentre l'altro costruisce embeddings, feature, notebook, API o demo su una versione precedente.

Il workflow riduce questo rischio separando:

- roadmap strategica;
- stream di lavoro;
- branch e pull request;
- decisioni approvate;
- contratti dati;
- handoff tra sviluppatori.

## File Operativi

`ROADMAP.md`

- visione di medio periodo;
- fasi del progetto;
- obiettivi e output attesi.

`AGENTS_COLLABORATION.md`

- regole condivise tra sviluppatori che usano Codex e Antigravity;
- stream;
- branch;
- ownership file;
- protocollo di handoff.

`TASK_BOARD.md`

- task operativi giornalieri;
- owner;
- stream;
- branch;
- stato;
- file scrivibili e file in sola lettura.

`DECISIONS.md`

- decisioni tecniche approvate;
- alternative considerate;
- pro e contro;
- impatto sui file.

`DATA_CONTRACTS.md`

- path e schema degli artefatti dati;
- colonne richieste e prodotte;
- vincoli tra pipeline e consumatori downstream.

## Procedura Prima Di Iniziare

1. Leggere `AGENT.md`.
2. Leggere `ROADMAP.md`.
3. Controllare `TASK_BOARD.md`.
4. Leggere `DECISIONS.md`.
5. Leggere `DATA_CONTRACTS.md`.
6. Eseguire `git fetch` e aggiornarsi dalla branch base concordata.
7. Dichiarare task, owner, stream, branch e file ownership.
8. Se la task cambia architettura, schema o modello, aprire prima una proposta in `DECISIONS.md`.

## Procedura Durante Il Lavoro

- Usare solo l'ambiente `uv`.
- Installare dipendenze con `uv pip install`.
- Eseguire test con `uv run python -m pytest -q`.
- Non modificare file fuori ownership.
- Non cambiare contratti dati senza aggiornare `DATA_CONTRACTS.md`.
- Documentare concetti avanzati in `docs/knowledge`.
- Tenere PR piccole e collegate a uno stream.
- Dichiarare nella PR se gli embeddings vanno rigenerati o se cambia lo schema processed.

## Procedura Di Handoff

Alla fine di una task, l'agente deve comunicare:

- file modificati;
- branch e PR;
- test eseguiti;
- output prodotti;
- rischi residui;
- decisioni ancora aperte;
- prossimo task consigliato.

## Quando Usarlo

Usare sempre questo workflow quando:

- i due sviluppatori lavorano in parallelo asincrono;
- una task tocca dati o schema;
- una task produce output consumato da notebook, API o demo;
- una decisione tecnica ha effetti su piu' fasi della pipeline.

## Strategia Stream

Stream A: embeddings, studio e analisi.

- Owner proposto: sviluppatore con Codex.
- Produce baseline embeddings e confronti.
- Dipende dal contratto processed.
- Dopo feature engineering, rigenera embeddings e confronta i risultati.

Stream B: feature engineering, estrazione feature e documentazione.

- Owner proposto: sviluppatore con Antigravity.
- Produce dataset arricchito e documentazione.
- Aggiorna `DATA_CONTRACTS.md`.
- Non deve rigenerare embeddings salvo accordo.

Stream C: clustering e integrazione.

- Parte dopo ricongiungimento A/B.
- Usa embeddings baseline e arricchiti.
- Produce metriche, cluster e interpretazione.

## Strategia Git/GitHub

- Lavorare su branch dedicate per stream.
- Aprire PR piccole e revisionabili.
- Prima della PR, aggiornarsi dalla branch base concordata.
- Ogni PR deve riportare test, output e cambi a contratti dati.
- Le modifiche a schema dati, `.env.sample`, `requirements.txt` e contratti vanno segnalate esplicitamente.

## Pro

- Riduce conflitti tra branch.
- Rende parallelizzabili task indipendenti.
- Mantiene tracciabili decisioni e contratti.
- Aiuta a riprendere il progetto dopo pause o sessioni diverse.

## Contro

- Richiede aggiornare piu' file Markdown.
- Aggiunge overhead su task piccole.
- Funziona solo se gli sviluppatori rispettano stream, branch, ownership e handoff.

## Alternative

- Usare solo appunti locali come `TODO.md`: piu' semplice, ma insufficiente per coordinare due sviluppatori su branch diverse.
- Usare issue tracker esterno: piu' strutturato, ma meno vicino alla repo locale.
- Usare solo commenti nel diario: utile per storico, ma debole per lavoro in corso.

## Link Utili

Documentazione:

- GitHub Docs, About issues: https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues
- GitHub Docs, About pull requests: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests
- uv documentation: https://docs.astral.sh/uv/
