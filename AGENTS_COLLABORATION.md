# AGENTS COLLABORATION

## Scopo

Definire regole operative condivise per far collaborare Codex e Antigravity sul progetto Pizza Cluster senza duplicare lavoro, creare conflitti o prendere decisioni architetturali non approvate.

Questo file integra `AGENT.md`. In caso di conflitto, `AGENT.md` ha priorita'.

## Principi

- Ogni task deve avere un owner esplicito.
- Ogni task deve dichiarare i file su cui puo' scrivere.
- Due agenti non devono modificare lo stesso file nella stessa finestra di lavoro, salvo accordo esplicito.
- Le decisioni architetturali richiedono proposta, pro/contro e approvazione umana.
- Ogni modifica significativa deve lasciare traccia in documentazione, test o diario.
- L'ambiente Python di riferimento e' `uv`.

## Ruoli Di Default

Codex:

- Coordinamento operativo.
- Moduli core in `src/utils`.
- Test unitari.
- Aggiornamento `Diary.md`, `TODO.md`, `DECISIONS.md` e knowledge base.
- Revisione dei contratti dati.

Antigravity:

- Notebook in `src/notebooks`.
- Report, figure e analisi esplorative.
- Validazione visuale dei risultati.
- Supporto a demo e API quando i contratti dati sono stabili.

I ruoli possono cambiare per task specifici, ma il cambio deve essere scritto nel task board.

## File Ownership

Prima di iniziare, ogni agente deve dichiarare:

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

## Task Parallelizzabili

Sono generalmente parallelizzabili:

- utility Python e notebook che consuma output gia' stabile;
- test di un modulo e documentazione di un altro;
- analisi esplorativa e preparazione contratti dati;
- API e demo solo dopo contratto dati approvato;
- knowledge base e pulizia documentale.

## Task Non Parallelizzabili

Richiedono coordinamento esplicito:

- cambio schema colonne;
- cambio path o nomi artefatti;
- cambio variabili `.env`;
- refactor di moduli condivisi;
- aggiornamento simultaneo di diario o task board;
- modifica dello stesso notebook o dello stesso modulo.

## Template Task

```md
Task:
Owner:
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

Quando un agente termina un task deve riportare:

- cosa ha cambiato;
- file toccati;
- test o verifiche eseguite;
- output prodotti;
- rischi residui;
- decisioni ancora aperte.

Formato consigliato:

```md
Handoff:
Owner:
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

## Gestione Conflitti

Se due agenti devono modificare lo stesso file:

1. sospendere una delle due attivita';
2. scegliere un solo owner temporaneo;
3. far produrre all'altro agente solo note o proposta;
4. applicare le modifiche in una sequenza definita;
5. rieseguire test e aggiornare handoff.

