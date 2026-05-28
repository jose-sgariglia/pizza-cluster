# Agent Workflow

## Cos'e'

Workflow operativo per coordinare piu' agenti di coding sul progetto Pizza Cluster.

L'obiettivo e' rendere chiaro chi lavora su cosa, quali file puo' modificare e quali verifiche deve eseguire prima di consegnare il lavoro.

## Perche' serve

Con due agenti attivi, il rischio principale non e' solo il conflitto Git: e' la divergenza di assunzioni. Un agente puo' cambiare un contratto dati, un path o una colonna mentre l'altro costruisce notebook, API o demo su una versione precedente.

Il workflow riduce questo rischio separando:

- roadmap strategica;
- task operativi;
- decisioni approvate;
- contratti dati;
- handoff tra agenti.

## File Operativi

`ROADMAP.md`

- visione di medio periodo;
- fasi del progetto;
- obiettivi e output attesi.

`AGENTS_COLLABORATION.md`

- regole condivise tra Codex e Antigravity;
- ruoli;
- ownership file;
- protocollo di handoff.

`TASK_BOARD.md`

- task operativi giornalieri;
- owner;
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
2. Leggere `Diary.md`.
3. Leggere `TODO.md`.
4. Leggere `ROADMAP.md`.
5. Controllare `TASK_BOARD.md`.
6. Dichiarare task, owner e file ownership.
7. Se la task cambia architettura, schema o modello, aprire prima una proposta in `DECISIONS.md`.

## Procedura Durante Il Lavoro

- Usare solo l'ambiente `uv`.
- Installare dipendenze con `uv pip install`.
- Eseguire test con `uv run python -m pytest -q`.
- Non modificare file fuori ownership.
- Non cambiare contratti dati senza aggiornare `DATA_CONTRACTS.md`.
- Documentare concetti avanzati in `docs/knowledge`.

## Procedura Di Handoff

Alla fine di una task, l'agente deve comunicare:

- file modificati;
- test eseguiti;
- output prodotti;
- rischi residui;
- decisioni ancora aperte;
- prossimo task consigliato.

## Quando Usarlo

Usare sempre questo workflow quando:

- Codex e Antigravity lavorano nella stessa sessione;
- una task tocca dati o schema;
- una task produce output consumato da notebook, API o demo;
- una decisione tecnica ha effetti su piu' fasi della pipeline.

## Pro

- Riduce conflitti.
- Rende parallelizzabili task indipendenti.
- Mantiene tracciabili decisioni e contratti.
- Aiuta a riprendere il progetto dopo pause o sessioni diverse.

## Contro

- Richiede aggiornare piu' file Markdown.
- Aggiunge overhead su task piccole.
- Funziona solo se gli agenti rispettano ownership e handoff.

## Alternative

- Usare solo `TODO.md`: piu' semplice, ma insufficiente per coordinare due agenti.
- Usare issue tracker esterno: piu' strutturato, ma meno vicino alla repo locale.
- Usare solo commenti nel diario: utile per storico, ma debole per lavoro in corso.

## Link Utili

Documentazione:

- GitHub Docs, About issues: https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues
- GitHub Docs, About pull requests: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests
- uv documentation: https://docs.astral.sh/uv/

