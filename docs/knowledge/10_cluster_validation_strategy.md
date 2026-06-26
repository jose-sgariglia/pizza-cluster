# Strategia di Validazione Cluster

## Cos'è

La validazione cluster è il processo che verifica se le email assegnate a un cluster dal modello (HDBSCAN) appartengono davvero allo stesso tema, e se il nome assegnato dall'LLM è accurato. È l'ultimo stadio della pipeline prima di considerare il risultato affidabile.

La validazione risponde a tre domande:
1. **Coerenza interna**: le email di questo cluster parlano davvero dello stesso argomento?
2. **Accuratezza del nome**: il label assegnato dall'LLM descrive correttamente il contenuto?
3. **Sovrapposizione**: questo cluster va unito a un altro con nome simile?

---

## Approccio precedente (deprecato)

100 email estratte casualmente dall'intero dataset, senza considerare la struttura per cluster. Ogni email veniva salvata in una cartella `_{{id}}/` con due file:
- `mail.md` — contenuto dell'email
- `label.md` — cluster assegnato dal modello

**Problema principale**: con 289 cluster e 100 email totali, la maggior parte dei cluster non veniva mai campionata. Il campione era dominato dai cluster grandi (es. *Epstein*, *Private Matters*) e i cluster piccoli erano invisibili.

---

## Approccio attuale: Validazione Stratificata per Cluster

Per ogni cluster vengono selezionate **5 email** con criteri opposti:

| Tipo | N | Criterio | Cosa misura |
|------|---|----------|-------------|
| `exemplar` | 3 | Probabilità HDBSCAN più **alta** | Il "cuore" del cluster — email più rappresentative |
| `boundary` | 2 | Probabilità HDBSCAN più **bassa** (> 0) | I casi ambigui — email che il modello ha assegnato con incertezza |

**Perché questa scelta?**

Gli *exemplar* validano il nome: se le 3 email più centrali non corrispondono al label, il naming è sbagliato.

Le *boundary* validano i confini: se le email più incerte hanno un tema diverso, il cluster è rumoroso o va splittato.

### Struttura cartelle

```
data/validation/
  all_label.md                      ← tabella globale cluster_id → nome → n_email
  cluster_{id}/
    cluster_info.md                 ← stats: nome, size, prob min/max/media
    exemplar_1_{eid}.md             ← email più rappresentativa
    exemplar_2_{eid}.md
    exemplar_3_{eid}.md
    boundary_1_{eid}.md             ← email più ambigua
    boundary_2_{eid}.md
```

Ogni file email contiene: type, probabilità, mittente, destinatario, oggetto, corpo.

**Totale**: 289 cluster × 6 file ≈ 1.734 file. Configurabile via `N_EXEMPLARS` e `N_BOUNDARY` nel notebook.

---

## Fase 8 — Validazione LLM (Tramite Claude)

Invece della lettura manuale, un LLM valida ogni cluster in modo autonomo. Il processo segue lo stesso flusso della revisione umana, ma automatizzato:

1. Legge il file `all_label.md`
2. L'LLM legge i 5 file email della cartella `cluster_{id}/`
3. **Prima** di vedere il nome assegnato, propone autonomamente una label possibile tra le tutte le label messe a disposizione
4. Fa delle ulteriori proposte di nuovi label mai usati e/o creati
5. Vede il nome assegnato dal modello e lo confronta con i propri
6. Produce un verdict strutturato in `llm_validation.md`


### Rischio di bias circolare

L'LLM che valida e l'LLM che ha assegnato i nomi condividono bias simili — rischiano di accordarsi per motivi sbagliati. **Mitigazione**: il prompt forza il ragionamento bottom-up (proporre label prima di vedere quello assegnato) e usa un modello diverso o temperature più alta per il validatore.

Un **spot-check umano su ~20 cluster** (campionati stratificati per size) è comunque raccomandato per calibrare il validatore LLM.

---

## Pro

- **Copertura totale**: tutti i 289 cluster vengono validati, non solo quelli grandi
- **Informatività**: le boundary email sono più utili degli exemplar per trovare errori
- **Scalabile**: la struttura per-cartella è autonoma e parallelizzabile per la validazione LLM
- **Zero rerun**: usa `df_clustered` dal checkpoint, non ricalcola nulla

## Contro

- **Volume**: ~1.734 file generati (gestibile, ma da non versionare tutti)
- **Bias LLM**: il validatore può essere troppo permissivo se usa lo stesso modello del labeler. Nel nostro caso usiamo llama:3.1 per l'etichettatura e Claude Sonet4.6 per la validazione

## Alternative

- **Cluster-level spot check manuale**: revisione a campione di 50 cluster prioritizzati per dimensione (top 50 coprono ~80% delle email)
- **Inter-annotator agreement**: due LLM diversi validano indipendentemente, si calcola il Cohen's Kappa

## Link utili

- HDBSCAN probabilities (membership strength): https://hdbscan.readthedocs.io/en/latest/soft_clustering.html
- Cluster quality evaluation survey: https://arxiv.org/abs/2109.13563

# Argomenti da studiare / approfondire

- Prompt engineering per valutazione bottom-up (chain-of-thought vincolato)
- Cohen's Kappa — metrica di accordo tra annotatori
- Soft clustering vs hard clustering per la selezione dei boundary samples
- LLM-as-a-Judge: tecniche di valutazione automatica con LLM (riferimento: https://arxiv.org/abs/2306.05685)
