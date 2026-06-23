#!/usr/bin/env python3
"""Generate full_pipeline_orchestration.ipynb from scratch (fixed paths + embedding logic)."""

import nbformat as nbf
from pathlib import Path

cells = []
md   = nbf.v4.new_markdown_cell
code = nbf.v4.new_code_cell

# ══════════════════════════════════════════════════════════════════
#  TITLE
# ══════════════════════════════════════════════════════════════════
cells.append(md("""\
# Pizza Cluster — Full Pipeline Orchestrator

End-to-end: JMAIL raw → preprocessing → embeddings (BGE-small) → clustering (UMAP+HDBSCAN) → labelling (LLM) → dataset etichettato → validazione manuale.

**Utilizzo:**
- `DEV_MODE = True` → smoke test locale (usa file esistenti, evita re-download).
- `DEV_MODE = False` → run completo sul server del laboratorio.
- Prima di passare a FULL, impostare anche `FORCE_RERUN = True` per rigenerare tutto.
- Assicurarsi che `ollama serve` sia attivo prima della Fase 5.
"""))

# ══════════════════════════════════════════════════════════════════
#  CELL 1 — CONFIG (carica _env e deriva TUTTI i path qui)
# ══════════════════════════════════════════════════════════════════
cells.append(code("""\
import sys
from pathlib import Path
from dotenv import dotenv_values

# ─── Trova la root del progetto (contiene .env) ───
def _find_root(start=Path.cwd()):
    for p in [start] + list(start.parents):
        if (p / '.env').exists():
            return p
    return start

ROOT     = _find_root()
ENV_FILE = str(ROOT / '.env')

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Carica variabili d'ambiente
_env = dotenv_values(ENV_FILE)

# ──────────────────────────────────────────
#  CONFIGURAZIONE — modifica solo questa sezione
# ──────────────────────────────────────────
DEV_MODE     = True    # True = smoke test; False = run completo
SEED         = 42
RERUN_OPTUNA = False   # False = usa BEST_PARAMS (DECISIONS.md 2026-06-19)
LLM_MODEL    = 'llama3'

# Parametri UMAP + HDBSCAN ottimali (DECISIONS.md 2026-06-19, CMA-ES su 15k)
BEST_PARAMS = {
    'n_neighbors'            : 51,
    'n_components'           : 12,
    'min_cluster_size'       : 71,
    'min_samples'            : 100,
    'cluster_selection_method': 'eom',
}

# Subsample per operazioni O(n²) — ridotti in DEV_MODE
SILHOUETTE_SAMPLE = 20_000
SCATTER_SAMPLE    = 50_000
OPTUNA_SAMPLE     = 150_000
KMEANS_K_VALUES   = [3, 5, 10, 15, 20]

if DEV_MODE:
    DEV_SAMPLE_SIZE   = 1_000      # righe da processare se non esiste già un sample
    DEV_EMBED_LIMIT   = 500        # righe da usare per embedding/clustering in DEV (CPU è lento)
    SILHOUETTE_SAMPLE = 200
    SCATTER_SAMPLE    = 300
    OPTUNA_SAMPLE     = 500
    KMEANS_K_VALUES   = [3, 5]
    FORCE_RERUN       = False      # usa checkpoints esistenti; raw non viene mai ri-scaricato
    # Parametri HDBSCAN ridotti per campioni piccoli
    DEV_CLUSTER_PARAMS = {
        'n_neighbors': 10, 'n_components': 5,
        'min_cluster_size': 5, 'min_samples': 2,
        'cluster_selection_method': 'eom',
    }
    print(f'[DEV_MODE] Smoke test — FORCE_RERUN={FORCE_RERUN}  DEV_EMBED_LIMIT={DEV_EMBED_LIMIT}')
else:
    DEV_SAMPLE_SIZE    = None
    DEV_EMBED_LIMIT    = None      # None = usa tutte le righe
    FORCE_RERUN        = False     # imposta True al primo run completo
    DEV_CLUSTER_PARAMS = None      # usa BEST_PARAMS
    print('[FULL_MODE] Pipeline completa — assicurarsi FORCE_RERUN=True al primo run')

# ──────────────────────────────────────────
#  PATHS — derivati da .env
# ──────────────────────────────────────────
# Directory
RAW_DIR        = ROOT / _env.get('DATA_RAW_PATH',        'data/raw/')
PROC_DIR       = ROOT / _env.get('DATA_PROCESSED_PATH',  'data/processed/')
EMB_DIR        = ROOT / _env.get('DATA_EMBEDDINGS_PATH', 'data/embeddings/')
META_DIR       = ROOT / _env.get('METADATA_PATH',        'data/metadata/')
FIGURES_BASE   = ROOT / _env.get('FIGURES_PATH',         'reports/figures/')

# File raw
RAW_FILE       = RAW_DIR / _env.get('RAW_EMAILS_FILENAME', 'jmail_emails.parquet')

# File processed — full vs sample (DEV)
PROC_FULL_FILE   = PROC_DIR / _env.get('PROCESSED_EMAILS_FILENAME',        'jmail_emails_processed.parquet')
PROC_SAMPLE_FILE = PROC_DIR / _env.get('PROCESSED_EMAILS_SAMPLE_FILENAME', 'jmail_emails_processed_sample.parquet')
ACTIVE_PROC_FILE = PROC_SAMPLE_FILE if DEV_MODE else PROC_FULL_FILE

# File embeddings
EMB_FILE       = EMB_DIR  / _env.get('EMBEDDINGS_FILENAME',         'email_embeddings.npy')
EMB_INDEX_FILE = META_DIR / _env.get('EMBEDDING_INDEX_FILENAME',    'email_embedding_index.parquet')
EMB_META_FILE  = META_DIR / _env.get('EMBEDDING_METADATA_FILENAME', 'email_embedding_metadata.json')

# Output pipeline
FIGURES_PATH        = FIGURES_BASE / 'full_pipeline'
VALIDATION_PATH     = ROOT / 'data' / 'validation'
CLUSTER_META_FILE   = META_DIR  / 'cluster_labeling_metadata.json'
CLUSTERED_FILE      = PROC_DIR  / 'jmail_emails_clustered.parquet'
CLUSTERED_SOFT_FILE = PROC_DIR  / 'jmail_emails_clustered_soft.parquet'

# Checkpoint intermedi (non versionati)
CKPT_LABELS  = PROC_DIR / '_pipeline_labels.npy'
CKPT_PROBS   = PROC_DIR / '_pipeline_probs.npy'
CKPT_REDUCED = PROC_DIR / '_pipeline_umap_reduced.npy'
CKPT_SOFT    = PROC_DIR / '_pipeline_soft_membership.npy'

for _d in [FIGURES_PATH, VALIDATION_PATH, PROC_DIR, META_DIR, EMB_DIR]:
    _d.mkdir(parents=True, exist_ok=True)

print(f'ROOT:             {ROOT}')
print(f'ACTIVE_PROC_FILE: {ACTIVE_PROC_FILE}')
print(f'EMB_FILE:         {EMB_FILE}')
print(f'CLUSTERED_FILE:   {CLUSTERED_FILE}')
"""))

# ══════════════════════════════════════════════════════════════════
#  CELL 2 — HARDWARE AUTO-DETECT
# ══════════════════════════════════════════════════════════════════
cells.append(code("""\
import platform, subprocess, psutil

def detect_hardware():
    info = {
        'platform'    : platform.system(),
        'cpu_physical': psutil.cpu_count(logical=False),
        'cpu_logical' : psutil.cpu_count(logical=True),
        'ram_gb'      : round(psutil.virtual_memory().total / 1e9, 1),
        'gpu_name'    : None,
        'vram_gb'     : None,
    }
    try:
        r = subprocess.run(
            ['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv,noheader'],
            capture_output=True, text=True, timeout=10,
        )
        if r.returncode == 0:
            parts = r.stdout.strip().split('\\n')[0].split(',')
            info['gpu_name'] = parts[0].strip()
            info['vram_gb']  = round(int(parts[1].strip().split()[0]) / 1024, 1)
    except Exception:
        pass
    return info

hw = detect_hardware()
print('Hardware rilevato:')
for k, v in hw.items():
    print(f'  {k}: {v}')

USE_GPU  = hw['gpu_name'] is not None
HAS_CUML = False
if USE_GPU:
    try:
        import cuml  # noqa: F401
        HAS_CUML = True
        print(f'\\ncuML disponibile — UMAP/HDBSCAN GPU ({hw[\"gpu_name\"]})')
    except ImportError:
        print(f'\\nGPU rilevata ma cuML non installato — fallback CPU')
        USE_GPU = False
else:
    print('\\nNessuna GPU — CPU mode')
"""))

# ══════════════════════════════════════════════════════════════════
#  CELL 3 — IMPORTS
# ══════════════════════════════════════════════════════════════════
cells.append(code("""\
import json, time, logging, warnings
from datetime import datetime, timezone

import numpy as np
import pandas as pd

import matplotlib
if not DEV_MODE:
    matplotlib.use('Agg')  # headless sul server — deve essere prima di pyplot
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

from src.utils.data_extraction  import run_extraction
from src.utils.data_processing  import run_processing_with_limit
from src.utils.embedding_pipeline import (
    EmbeddingConfig,
    build_embedding_jobs,
    load_embedding_model,
    encode_texts,
    aggregate_chunk_embeddings,
)
from src.utils.optuna_clustering import run_clustering_optimization
from src.utils.topic_labeling import (
    calculate_ctfidf,
    extract_keywords_yake,
    extract_keywords_textrank,
)
from src.utils.llm_naming import get_llm_cluster_name

if HAS_CUML:
    from cuml.manifold import UMAP
    from cuml.cluster  import HDBSCAN as cuHDBSCAN
else:
    from umap import UMAP
    import hdbscan as hdbscan_lib

print(f'pandas {pd.__version__}  numpy {np.__version__}')
print('Imports OK')
"""))

# ══════════════════════════════════════════════════════════════════
#  CELL 4 — HELPERS
# ══════════════════════════════════════════════════════════════════
cells.append(code("""\
def checkpoint_exists(*paths):
    '''Restituisce True se tutti i path esistono E FORCE_RERUN è False.'''
    if FORCE_RERUN:
        return False
    return all(Path(str(p)).exists() for p in paths)

def save_figure(fig, name: str, meta: dict = None):
    '''Salva PNG + JSON metadati in FIGURES_PATH.'''
    png  = FIGURES_PATH / f'{name}.png'
    jf   = FIGURES_PATH / f'{name}.json'
    fig.savefig(png, dpi=150, bbox_inches='tight')
    m = {'name': name, 'seed': SEED, 'dev_mode': DEV_MODE, **(meta or {})}
    jf.write_text(json.dumps(m, indent=2, default=str), encoding='utf-8')
    print(f'  Figure salvata: {png.name}')

def subsample(arr: np.ndarray, labels: np.ndarray, n: int):
    '''Sottocampionamento casuale per metriche pesanti.'''
    n = min(n, len(arr))
    idx = np.random.default_rng(SEED).choice(len(arr), size=n, replace=False)
    return arr[idx], labels[idx]

def normalize_rows(arr: np.ndarray) -> np.ndarray:
    '''Normalizzazione L2 per riga.'''
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    norms[norms == 0] = 1
    return arr / norms

print('Helper OK')
"""))

# ══════════════════════════════════════════════════════════════════
#  PHASE 1 — EXTRACTION
# ══════════════════════════════════════════════════════════════════
cells.append(md('## Fase 1 — Estrazione dati raw da JMAIL\n\nSe il file raw è già presente, l\'estrazione viene saltata (mai re-scaricato in DEV_MODE).'))

cells.append(code("""\
# Estrazione NON viene mai forzata — il re-download richiede ore
if RAW_FILE.exists():
    print(f'[SKIP] Raw già presente: {RAW_FILE}')
    import pyarrow.parquet as pq
    print(f'       Righe: {pq.read_metadata(str(RAW_FILE)).num_rows:,}')
else:
    print('Scaricamento dati raw da JMAIL...')
    t0 = time.time()
    _res = run_extraction(ENV_FILE, sample_limit=DEV_SAMPLE_SIZE if DEV_MODE else None)
    print(f'Estrazione completata in {time.time()-t0:.1f}s — {_res[\"row_count\"]:,} righe')
    print(f'Output: {_res[\"raw_output_path\"]}')
"""))

# ══════════════════════════════════════════════════════════════════
#  PHASE 2 — PREPROCESSING
# ══════════════════════════════════════════════════════════════════
cells.append(md('## Fase 2 — Preprocessing\n\n- **DEV_MODE**: usa `PROCESSED_EMAILS_SAMPLE_FILENAME` (da `.env`).\n- **FULL_MODE**: usa `PROCESSED_EMAILS_FILENAME` (da `.env`). In FULL run `run_processing_with_limit(limit=None)`.'))

cells.append(code("""\
if checkpoint_exists(ACTIVE_PROC_FILE):
    print(f'[SKIP] Processed già presente: {ACTIVE_PROC_FILE}')
    df_processed = pd.read_parquet(ACTIVE_PROC_FILE)
else:
    print(f'Avvio preprocessing (limit={DEV_SAMPLE_SIZE if DEV_MODE else \"full\"})...')
    t0 = time.time()
    _res = run_processing_with_limit(ENV_FILE, limit=DEV_SAMPLE_SIZE if DEV_MODE else None)
    df_processed = pd.read_parquet(ACTIVE_PROC_FILE)
    print(f'Preprocessing completato in {time.time()-t0:.1f}s')
    print(f'  Input:  {_res[\"input_rows\"]:,}')
    print(f'  Output: {_res[\"output_rows\"]:,}')
    print(f'  Promo rimossi:      {_res[\"removed_promotional_rows\"]:,}')
    print(f'  Testo vuoto rimossi:{_res[\"removed_empty_text_rows\"]:,}')

print(f'\\nDataset processato: {df_processed.shape}')
df_processed[['combined_text', 'has_thread', 'has_redaction', 'sender_domain']].head(3)
"""))

cells.append(code("""\
# ─── Analisi raw vs processed ───
_raw_df = pd.read_parquet(RAW_FILE)

fig, axes = plt.subplots(2, 2, figsize=(14, 9))
fig.suptitle('Raw vs Processed — Overview', fontsize=14, fontweight='bold')

# 1. Dimensioni dataset
ax = axes[0, 0]
_bars = ax.bar(['Raw', 'Processed'], [len(_raw_df), len(df_processed)], color=['#4C72B0', '#55A868'])
ax.bar_label(_bars, fmt='{:,.0f}', padding=3)
ax.set_title('Numero email')
ax.set_ylabel('Count')

# 2. Lunghezza combined_text
ax = axes[0, 1]
df_processed['combined_text_length'].clip(upper=5000).hist(bins=40, ax=ax, color='#4C72B0', alpha=0.8)
ax.set_title('Lunghezza combined_text (clip 5k)')
ax.set_xlabel('Caratteri')

# 3. Flag diagnostici
ax = axes[1, 0]
_flags = {k: int(df_processed[k].sum()) for k in ['has_thread', 'has_redaction', 'has_disclaimer', 'person_unknown']}
ax.barh(list(_flags.keys()), list(_flags.values()), color='#4C72B0', alpha=0.8)
ax.set_title('Flag diagnostici')
ax.set_xlabel('Count')

# 4. Null ratio colonne chiave
ax = axes[1, 1]
_cols  = ['subject_clean', 'content_clean', 'sender_domain', 'sent_at_datetime']
_nulls = [df_processed[c].isnull().mean() for c in _cols]
ax.bar(_cols, _nulls, color='#C44E52', alpha=0.8)
ax.set_title('Null ratio colonne chiave')
ax.set_ylabel('Ratio (0–1)')
ax.set_ylim(0, 1)
plt.setp(ax.get_xticklabels(), rotation=20, ha='right')

plt.tight_layout()
save_figure(fig, '01_raw_vs_processed', {'raw': len(_raw_df), 'processed': len(df_processed)})
plt.show()

# Tabella shape
print('\\n── Shape ──')
print(pd.DataFrame({'dataset': ['raw', 'processed'],
                    'rows': [len(_raw_df), len(df_processed)],
                    'cols': [len(_raw_df.columns), len(df_processed.columns)]}).to_string(index=False))

# Campione 10 email
print('\\n── Campione (5 con thread + 5 senza) ──')
_s = pd.concat([df_processed[df_processed['has_thread']].head(5),
                df_processed[~df_processed['has_thread']].head(5)])
print(_s[['id', 'has_thread', 'combined_text']].assign(
    preview=lambda d: d['combined_text'].str[:80] + '...'
)[['id', 'has_thread', 'preview']].to_string(index=False))
"""))

# ══════════════════════════════════════════════════════════════════
#  df_active: subset usato per embedding/clustering/labelling/validazione
# ══════════════════════════════════════════════════════════════════
cells.append(code("""\
# In DEV_MODE limita le righe per tenere il smoke test veloce (<5 min su CPU).
# In FULL_MODE usa tutto df_processed.
if DEV_MODE and DEV_EMBED_LIMIT and len(df_processed) > DEV_EMBED_LIMIT:
    df_active = df_processed.head(DEV_EMBED_LIMIT).copy().reset_index(drop=True)
    print(f'[DEV_MODE] df_active: {len(df_active)} righe (da {len(df_processed)} nel sample)')
else:
    df_active = df_processed
    print(f'df_active: {len(df_active)} righe')
"""))

# ══════════════════════════════════════════════════════════════════
#  PHASE 3 — EMBEDDINGS
# ══════════════════════════════════════════════════════════════════
cells.append(md("""\
## Fase 3 — Generazione Embeddings

Modello: `BAAI/bge-small-en-v1.5` con Token-Aware Chunking (400 token, overlap 15%) e Weighted Decay Pooling (DECISIONS.md 2026-06-17).

La pipeline embedding usa `ACTIVE_PROC_FILE` esplicitamente (fix rispetto a `run_embedding_pipeline()` che legge sempre `PROCESSED_EMAILS_SAMPLE_FILENAME`).
"""))

cells.append(code("""\
if checkpoint_exists(EMB_FILE, EMB_INDEX_FILE):
    print(f'[SKIP] Embeddings già presenti: {EMB_FILE}')
else:
    _cfg = EmbeddingConfig.from_env(ENV_FILE)
    print(f'Generazione embeddings da {ACTIVE_PROC_FILE.name}')
    print(f'  Modello: {_cfg.model_name}')
    print(f'  Chunk char length: {_cfg.chunk_char_length}  overlap: {_cfg.chunk_char_overlap}')

    _df_emb = df_active
    print(f'  Email da processare: {len(_df_emb):,}')

    t0 = time.time()
    _chunk_texts, _emb_index = build_embedding_jobs(_df_emb, _cfg)
    print(f'  Chunking completato: {len(_chunk_texts):,} chunk in {time.time()-t0:.1f}s')

    _model    = load_embedding_model(_cfg.model_name)
    t0 = time.time()
    _chunk_embs = encode_texts(_model, _chunk_texts, batch_size=_cfg.batch_size)
    print(f'  Encoding completato in {time.time()-t0:.1f}s')

    _email_embs = aggregate_chunk_embeddings(_chunk_embs, _emb_index)
    _email_embs = normalize_rows(_email_embs)

    EMB_DIR.mkdir(parents=True, exist_ok=True)
    np.save(EMB_FILE, _email_embs)
    _emb_index.to_parquet(EMB_INDEX_FILE, index=False)

    import json as _json
    EMB_META_FILE.write_text(_json.dumps({
        'created_at_utc'     : datetime.now(timezone.utc).isoformat(),
        'model_name'         : _cfg.model_name,
        'source_file'        : str(ACTIVE_PROC_FILE),
        'row_count'          : int(_email_embs.shape[0]),
        'embedding_dimensions': int(_email_embs.shape[1]),
        'chunk_count'        : len(_chunk_texts),
        'dev_mode'           : DEV_MODE,
    }, indent=2), encoding='utf-8')
    print(f'  Salvato: {EMB_FILE}  shape={_email_embs.shape}')

embeddings      = np.load(EMB_FILE)
embedding_index = pd.read_parquet(EMB_INDEX_FILE)
print(f'\\nEmbeddings caricati: {embeddings.shape}')
"""))

cells.append(code("""\
# ─── Verifica allineamento + diagnostica ───
assert len(embeddings) == len(df_active), (
    f'MISMATCH: {len(embeddings)} embeddings vs {len(df_active)} email in df_active.\\n'
    f'In DEV_MODE: elimina {EMB_FILE.name} e riesegui la Fase 3 dopo aver cambiato DEV_EMBED_LIMIT.'
)

norms = np.linalg.norm(embeddings, axis=1)
_chunk_counts = embedding_index.groupby('embedding_row').size()

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
# range esplicito +/-epsilon per evitare errore numpy su dati costanti
axes[0].hist(norms, bins=30,
             range=(float(norms.min()) - 1e-3, float(norms.max()) + 1e-3),
             color='#4C72B0', alpha=0.8)
axes[0].set_title('Distribuzione norme L2')
axes[0].set_xlabel('Norma L2')

axes[1].hist(_chunk_counts,
             bins=min(30, max(1, int(_chunk_counts.max()))),
             range=(float(_chunk_counts.min()) - 0.5, float(_chunk_counts.max()) + 0.5),
             color='#55A868', alpha=0.8)
axes[1].set_title('Chunk per email')
axes[1].set_xlabel('N chunk')

plt.tight_layout()
save_figure(fig, '02_embedding_diagnostics', {'shape': list(embeddings.shape)})
plt.show()

print(f'Embedding dim:  {embeddings.shape[1]}')
print(f'Norma media:    {norms.mean():.4f}')
print(f'Norma std:      {norms.std():.6f}')
print(f'Chunk totali:   {len(embedding_index):,}')
"""))

cells.append(code("""\
# ─── UMAP 2D scatter (visualizzazione, campione) ───
_n  = min(SCATTER_SAMPLE, len(embeddings))
_idx = np.random.default_rng(SEED).choice(len(embeddings), size=_n, replace=False)

print(f'UMAP 2D su {_n} punti (solo visualizzazione)...')
t0 = time.time()
_r2d = (UMAP(n_components=2, n_neighbors=min(30, _n - 1), min_dist=0.1, metric='cosine', random_state=SEED)
        if HAS_CUML else
        UMAP(n_components=2, n_neighbors=min(30, _n - 1), min_dist=0.1, metric='cosine',
             random_state=SEED, low_memory=len(embeddings) > 100_000))
_e2d = np.array(_r2d.fit_transform(embeddings[_idx]))
print(f'  completato in {time.time()-t0:.1f}s')

fig, ax = plt.subplots(figsize=(10, 8))
ax.scatter(_e2d[:, 0], _e2d[:, 1], s=2, alpha=0.4, color='#4C72B0', rasterized=True)
ax.set_title(f'UMAP 2D — {_n} email (campione)')
ax.set_xlabel('UMAP-1')
ax.set_ylabel('UMAP-2')
save_figure(fig, '03_umap_2d_scatter', {'sample_size': _n})
plt.show()
"""))

cells.append(code("""\
# ─── MiniBatchKMeans sweep ───
_n_sil   = min(SILHOUETTE_SAMPLE, len(embeddings))
_emb_sil = embeddings[np.random.default_rng(SEED).choice(len(embeddings), size=_n_sil, replace=False)]

_km_rows = []
print(f'MiniBatchKMeans K={KMEANS_K_VALUES} su {_n_sil} campioni...')
for k in KMEANS_K_VALUES:
    _km  = MiniBatchKMeans(n_clusters=k, random_state=SEED, n_init=3,
                           batch_size=min(10_000, _n_sil))
    _lk  = _km.fit_predict(_emb_sil)
    _sil = silhouette_score(_emb_sil, _lk, sample_size=min(5_000, _n_sil), random_state=SEED)
    _db  = davies_bouldin_score(_emb_sil, _lk)
    _ch  = calinski_harabasz_score(_emb_sil, _lk)
    _km_rows.append({'K': k, 'Silhouette': round(_sil, 4),
                     'Davies-Bouldin': round(_db, 4), 'Calinski-Harabasz': round(_ch, 1)})
    print(f'  K={k:2d}: Sil={_sil:.4f}  DB={_db:.4f}  CH={_ch:.1f}')

df_kmeans = pd.DataFrame(_km_rows)
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, col in zip(axes, ['Silhouette', 'Davies-Bouldin', 'Calinski-Harabasz']):
    ax.plot(df_kmeans['K'], df_kmeans[col], marker='o', color='#4C72B0')
    ax.set_title(col)
    ax.set_xlabel('K')
plt.tight_layout()
save_figure(fig, '04_kmeans_sweep', {'k_values': KMEANS_K_VALUES, 'sample_size': _n_sil})
plt.show()
print(df_kmeans.to_string(index=False))
"""))

# ══════════════════════════════════════════════════════════════════
#  PHASE 4 — CLUSTERING
# ══════════════════════════════════════════════════════════════════
cells.append(md("""\
## Fase 4 — Clustering (UMAP + HDBSCAN)

Parametri ottimali da `DECISIONS.md` 2026-06-19. In `DEV_MODE` vengono usati parametri ridotti adatti a campioni piccoli.
"""))

cells.append(code("""\
# Seleziona parametri: DEV ridotti vs BEST_PARAMS completi
if DEV_MODE and DEV_CLUSTER_PARAMS:
    _active_params = DEV_CLUSTER_PARAMS
    print('[DEV_MODE] Parametri HDBSCAN ridotti per campione piccolo:')
elif RERUN_OPTUNA:
    _n_opt = min(OPTUNA_SAMPLE, len(embeddings))
    _idx_o = np.random.default_rng(SEED).choice(len(embeddings), size=_n_opt, replace=False)
    print(f'Optuna CMA-ES su {_n_opt} campioni (n_trials=30)...')
    _study = run_clustering_optimization(
        embeddings[_idx_o], n_trials=30, use_umap=True, sampler_type='CMA-ES'
    )
    _active_params = _study.best_params
    print(f'Best params trovati: {_active_params}')
else:
    _active_params = BEST_PARAMS
    print('Parametri da DECISIONS.md 2026-06-19:')

for k, v in _active_params.items():
    print(f'  {k}: {v}')
"""))

cells.append(code("""\
# ─── UMAP + HDBSCAN con checkpoint ───
if checkpoint_exists(CKPT_LABELS, CKPT_PROBS, CKPT_REDUCED):
    print('[SKIP] Checkpoint clustering — caricamento...')
    labels        = np.load(CKPT_LABELS)
    cluster_probs = np.load(CKPT_PROBS)
    emb_reduced   = np.load(CKPT_REDUCED)
else:
    _nn  = _active_params['n_neighbors']
    _nc  = _active_params['n_components']
    _mcs = _active_params['min_cluster_size']
    _ms  = _active_params['min_samples']
    _csm = _active_params['cluster_selection_method']

    print(f'UMAP {_nc}D su {len(embeddings):,} vettori...')
    t0 = time.time()
    _reducer = (
        UMAP(n_components=_nc, n_neighbors=_nn, metric='cosine', min_dist=0.01, random_state=SEED)
        if HAS_CUML else
        UMAP(n_components=_nc, n_neighbors=min(_nn, len(embeddings)-1), metric='cosine',
             min_dist=0.01, random_state=SEED,
             low_memory=len(embeddings) > 100_000)
    )
    emb_reduced = np.array(_reducer.fit_transform(embeddings))
    print(f'  UMAP completato in {time.time()-t0:.1f}s  shape={emb_reduced.shape}')

    print(f'HDBSCAN (min_cluster_size={_mcs}, min_samples={_ms})...')
    t0 = time.time()
    if HAS_CUML:
        _clust = cuHDBSCAN(min_cluster_size=_mcs, min_samples=_ms,
                           cluster_selection_method=_csm)
        _clust.fit(emb_reduced)
        labels        = np.array(_clust.labels_.get() if hasattr(_clust.labels_, 'get') else _clust.labels_)
        cluster_probs = np.array(_clust.probabilities_.get() if hasattr(_clust.probabilities_, 'get') else _clust.probabilities_)
    else:
        _clust = hdbscan_lib.HDBSCAN(
            min_cluster_size=_mcs, min_samples=_ms,
            metric='euclidean', cluster_selection_method=_csm,
            prediction_data=True, core_dist_n_jobs=-1,
        )
        _clust.fit(emb_reduced)
        labels        = _clust.labels_
        cluster_probs = _clust.probabilities_
    print(f'  HDBSCAN completato in {time.time()-t0:.1f}s')

    np.save(CKPT_LABELS,  labels)
    np.save(CKPT_PROBS,   cluster_probs)
    np.save(CKPT_REDUCED, emb_reduced)
    print('  Checkpoint salvato.')

n_clusters  = len(set(labels)) - (1 if -1 in labels else 0)
noise_ratio = float((labels == -1).mean())
print(f'\\nCluster trovati: {n_clusters}')
print(f'Noise ratio:     {noise_ratio:.2%}')
print(f'Email nel noise: {int((labels == -1).sum()):,}')
"""))

cells.append(code("""\
# ─── Metriche clustering ───
_mask_cl  = labels != -1
_n_cl     = _mask_cl.sum()

if _n_cl >= 2 and n_clusters >= 2:
    _emb_m, _lab_m = subsample(emb_reduced[_mask_cl], labels[_mask_cl], SILHOUETTE_SAMPLE)
    sil = silhouette_score(_emb_m, _lab_m)
    db  = davies_bouldin_score(_emb_m, _lab_m)
    ch  = calinski_harabasz_score(_emb_m, _lab_m)
    print('── Metriche clustering ──')
    print(f'  Silhouette Score:        {sil:.4f}')
    print(f'  Davies-Bouldin Score:    {db:.4f}')
    print(f'  Calinski-Harabasz Score: {ch:.1f}')
    print(f'  N cluster:               {n_clusters}')
    print(f'  Noise ratio:             {noise_ratio:.2%}')
else:
    sil, db, ch = 0.0, 0.0, 0.0
    print(f'Metriche non calcolabili: n_clusters={n_clusters}, email clustered={_n_cl}')
    print('  Aumentare i dati o ridurre min_cluster_size (DEV_CLUSTER_PARAMS).')
"""))

cells.append(code("""\
# ─── Scatter 2D colorato per cluster ───
_n_sc  = min(SCATTER_SAMPLE, len(emb_reduced))
_idx_s = np.random.default_rng(SEED).choice(len(emb_reduced), size=_n_sc, replace=False)

if emb_reduced.shape[1] > 2:
    print(f'UMAP 2D (da {emb_reduced.shape[1]}D reduced) per scatter cluster...')
    t0 = time.time()
    _red2d = (UMAP(n_components=2, n_neighbors=min(30, _n_sc-1), min_dist=0.05, random_state=SEED)
              if HAS_CUML else
              UMAP(n_components=2, n_neighbors=min(30, _n_sc-1), min_dist=0.05,
                   random_state=SEED, low_memory=_n_sc > 100_000))
    _e2d_cl = np.array(_red2d.fit_transform(emb_reduced[_idx_s]))
    print(f'  completato in {time.time()-t0:.1f}s')
else:
    _e2d_cl = emb_reduced[_idx_s]

_lab2d = labels[_idx_s]
_unique = sorted(set(_lab2d))
_cmap   = cm.get_cmap('tab20', max(len(_unique), 1))

fig, ax = plt.subplots(figsize=(13, 10))
for i, cl in enumerate(_unique):
    _m     = _lab2d == cl
    _color = 'lightgray' if cl == -1 else _cmap(i % 20)
    _alpha = 0.2 if cl == -1 else 0.5
    ax.scatter(_e2d_cl[_m, 0], _e2d_cl[_m, 1], s=2, alpha=_alpha,
               color=_color, rasterized=True,
               label='noise' if cl == -1 else str(cl))
ax.set_title(f'Cluster scatter 2D — {_n_sc:,} email, {n_clusters} cluster')
ax.set_xlabel('UMAP-1')
ax.set_ylabel('UMAP-2')
save_figure(fig, '05_cluster_scatter_2d',
            {'n_clusters': n_clusters, 'noise_ratio': noise_ratio, 'sample_size': _n_sc})
plt.show()
"""))

cells.append(code("""\
# ─── Soft clustering + overlap network ───
_has_clust   = '_clust' in dir()
_has_pred    = _has_clust and not HAS_CUML and hasattr(_clust, 'all_points_membership_vectors')
_soft_ckpt   = checkpoint_exists(CKPT_SOFT)

if _has_pred or _soft_ckpt:
    if _soft_ckpt:
        print('[SKIP] Soft checkpoint — caricamento...')
        _membership = np.load(CKPT_SOFT)
    else:
        print('Calcolo soft membership vectors...')
        try:
            _membership = hdbscan_lib.all_points_membership_vectors(_clust)
            np.save(CKPT_SOFT, _membership)
            print(f'  Salvato: {CKPT_SOFT}')
        except Exception as e:
            print(f'  Soft clustering non disponibile: {e}')
            _membership = None

    if _membership is not None and n_clusters > 0:
        _top10_idx   = np.argsort(_membership, axis=1)[:, ::-1][:, :10]
        _top10_probs = np.sort(_membership, axis=1)[:, ::-1][:, :10]

        _df_soft = df_processed.copy()
        _df_soft['cluster']         = labels
        _df_soft['cluster_prob']    = cluster_probs
        _df_soft['top_10_clusters'] = list(_top10_idx)
        _df_soft['top_10_probs']    = list(_top10_probs)
        _df_soft.to_parquet(CLUSTERED_SOFT_FILE, index=False)
        print(f'Soft dataset salvato: {CLUSTERED_SOFT_FILE}')

        # Network graph cluster-level
        try:
            import networkx as nx
            _OVERLAP_THR = 0.05
            _cids = [c for c in sorted(set(labels)) if c != -1]
            G = nx.Graph()
            G.add_nodes_from(_cids)
            for _i, _ci in enumerate(_cids):
                _pi = _membership[labels == _ci]
                for _j, _cj in enumerate(_cids):
                    if _j <= _i:
                        continue
                    _ov = float(_pi[:, _cj].mean()) if _pi.shape[1] > _cj else 0.0
                    if _ov > _OVERLAP_THR:
                        G.add_edge(_ci, _cj, weight=_ov)

            fig, ax = plt.subplots(figsize=(13, 10))
            _pos = nx.spring_layout(G, seed=SEED, k=2)
            _ew  = [G[u][v]['weight'] * 5 for u, v in G.edges()]
            nx.draw_networkx(G, pos=_pos, ax=ax, node_size=300, font_size=8,
                             edge_color='#888', width=_ew, alpha=0.85)
            ax.set_title(f'Cluster overlap network (overlap > {_OVERLAP_THR:.0%})')
            ax.axis('off')
            save_figure(fig, '06_cluster_overlap_network', {'overlap_threshold': _OVERLAP_THR})
            plt.show()
        except ImportError:
            print('networkx non installato — uv pip install networkx')
else:
    print('Soft clustering disponibile solo con hdbscan CPU (prediction_data=True). Saltato.')
"""))

# ══════════════════════════════════════════════════════════════════
#  PHASE 5 — LABELLING
# ══════════════════════════════════════════════════════════════════
cells.append(md("""\
## Fase 5 — Labelling (keyword + LLM naming)

Keyword extraction con 3 algoritmi (c-TF-IDF, YAKE, TextRank). Naming via Ollama/llama3.

> **KeyBERT omesso**: richiede word-embeddings precomputati per ogni parola del vocabolario — costo proibitivo su dataset grandi.
"""))

cells.append(code("""\
_cids = sorted(c for c in set(labels) if c != -1)
print(f'Estrazione keyword per {len(_cids)} cluster...')

_docs = {}
for cid in _cids:
    _texts = df_active.loc[labels == cid, 'combined_text'].fillna('').tolist()
    _docs[cid] = ' '.join(_texts)

print('  c-TF-IDF...')
ctfidf_kw = calculate_ctfidf(_docs, top_n=20)

print('  YAKE...')
yake_kw = {}
for cid, doc in _docs.items():
    try:
        yake_kw[cid] = extract_keywords_yake(doc[:50_000], top_n=20)
    except Exception as e:
        yake_kw[cid] = []
        logging.warning(f'YAKE cluster {cid}: {e}')

print('  TextRank...')
textrank_kw = {}
for cid, doc in _docs.items():
    try:
        textrank_kw[cid] = extract_keywords_textrank(doc[:30_000], top_n=20)
    except Exception as e:
        textrank_kw[cid] = []
        logging.warning(f'TextRank cluster {cid}: {e}')

print('Keyword extraction completata.')
"""))

cells.append(code("""\
# ─── Tabella keyword ───
_rows = [{
    'cluster' : cid,
    'n_email' : int((labels == cid).sum()),
    'ctfidf'  : ', '.join(ctfidf_kw.get(cid, [])[:5]),
    'yake'    : ', '.join(yake_kw.get(cid, [])[:5]),
    'textrank': ', '.join(textrank_kw.get(cid, [])[:5]),
} for cid in _cids]
df_kw = pd.DataFrame(_rows)
print('── Keyword top 5 per algoritmo ──')
print(df_kw.to_string(index=False, max_colwidth=45))
"""))

cells.append(code("""\
# ─── LLM naming (Ollama) ───
cluster_names = {}
if _cids:
    print(f'LLM naming su {len(_cids)} cluster (modello: {LLM_MODEL})...')
    print('Assicurarsi che ollama serve sia attivo\\n')
    for cid in _cids:
        _combined = (ctfidf_kw.get(cid, [])[:7] +
                     yake_kw.get(cid, [])[:7] +
                     textrank_kw.get(cid, [])[:7])
        _seen, _uniq = set(), []
        for _k in _combined:
            if _k.lower() not in _seen:
                _seen.add(_k.lower())
                _uniq.append(_k)
        try:
            _name = get_llm_cluster_name(_uniq[:20], model=LLM_MODEL)
        except Exception as e:
            logging.warning(f'LLM fallback cluster {cid}: {e}')
            _name = ' / '.join(_uniq[:2]) if len(_uniq) >= 2 else (str(cid))
        cluster_names[cid] = _name
        print(f'  [{cid:3d}] {_name}')
else:
    print('Nessun cluster trovato — nessun naming necessario.')

cluster_names[-1] = 'Outlier'

# Salva metadata labelling
_meta = {
    'created_at_utc': datetime.now(timezone.utc).isoformat(),
    'n_clusters'    : len(_cids),
    'llm_model'     : LLM_MODEL,
    'seed'          : SEED,
    'clusters': {str(cid): {
        'n_email' : int((labels == cid).sum()),
        'ctfidf'  : ctfidf_kw.get(cid, []),
        'yake'    : yake_kw.get(cid, []),
        'textrank': textrank_kw.get(cid, []),
        'llm_name': cluster_names.get(cid, ''),
    } for cid in _cids},
}
CLUSTER_META_FILE.parent.mkdir(parents=True, exist_ok=True)
CLUSTER_META_FILE.write_text(json.dumps(_meta, indent=2, ensure_ascii=False), encoding='utf-8')
print(f'\\nMetadata salvati: {CLUSTER_META_FILE}')
"""))

# ══════════════════════════════════════════════════════════════════
#  PHASE 6 — FINAL DATASET
# ══════════════════════════════════════════════════════════════════
cells.append(md('## Fase 6 — Dataset finale etichettato\n\nSchema: `DATA_CONTRACTS.md — Clustered Emails`.'))

cells.append(code("""\
if checkpoint_exists(CLUSTERED_FILE):
    print(f'[SKIP] Clustered già presente: {CLUSTERED_FILE}')
    df_clustered = pd.read_parquet(CLUSTERED_FILE)
else:
    df_clustered = df_active.copy()
    df_clustered['cluster']      = labels
    df_clustered['cluster_prob'] = cluster_probs
    df_clustered['cluster_name'] = df_clustered['cluster'].map(cluster_names).fillna('Outlier')
    df_clustered.to_parquet(CLUSTERED_FILE, index=False)
    print(f'Dataset salvato: {CLUSTERED_FILE}')

print(f'Shape finale: {df_clustered.shape}')
print('\\n── Distribuzione cluster (top 15) ──')
print(df_clustered.groupby(['cluster', 'cluster_name'])
      .size().reset_index(name='count')
      .sort_values('count', ascending=False).head(15).to_string(index=False))
"""))

# ══════════════════════════════════════════════════════════════════
#  PHASE 7 — VALIDATION
# ══════════════════════════════════════════════════════════════════
cells.append(md('## Fase 7 — Validazione manuale\n\nOutput: `data/validation/all_label.md` + `data/validation/_{{id}}/mail.md` + `label.md` (100 email, seed fisso).'))

cells.append(code("""\
# ─── all_label.md ───
_all_label = VALIDATION_PATH / 'all_label.md'
_lines = [
    '# Cluster Labels\\n\\n',
    f'Generato: {datetime.now(timezone.utc).isoformat()}\\n',
    f'SEED: {SEED} | LLM: {LLM_MODEL}\\n\\n',
    '| Cluster | Nome | N email |\\n',
    '|---------|------|---------|\\n',
]
for cid in sorted(cluster_names.keys()):
    _n = int((df_clustered['cluster'] == cid).sum())
    _lines.append(f'| {cid} | {cluster_names[cid]} | {_n} |\\n')

_all_label.write_text(''.join(_lines), encoding='utf-8')
print(f'Salvato: {_all_label}')
print(''.join(_lines[:8]))
"""))

cells.append(code("""\
# ─── 100 email casuali con seed fisso ───
_n_val  = min(100, len(df_clustered))
_sample = df_clustered.sample(n=_n_val, random_state=SEED)

for _, row in _sample.iterrows():
    _eid  = str(row.get('id', row.name))
    _edir = VALIDATION_PATH / f'_{_eid}'
    _edir.mkdir(parents=True, exist_ok=True)

    _mail  = (f'# Email {_eid}\\n\\n'
              f'**Date:** {row.get(\"sent_at\", \"N/A\")}\\n'
              f'**From:** {row.get(\"sender\", \"N/A\")}\\n'
              f'**To:** {row.get(\"to_recipients\", \"N/A\")}\\n'
              f'**Subject:** {row.get(\"subject\", \"N/A\")}\\n\\n---\\n\\n'
              + str(row.get('content_clean', row.get('combined_text', ''))))
    (_edir / 'mail.md').write_text(_mail, encoding='utf-8')

    _label = (f'# Label — Email {_eid}\\n\\n'
              f'**Cluster ID:** {row.get(\"cluster\", \"N/A\")}\\n'
              f'**Cluster Name:** {row.get(\"cluster_name\", \"N/A\")}\\n'
              f'**Probability:** {float(row.get(\"cluster_prob\", 0)):.4f}\\n')
    (_edir / 'label.md').write_text(_label, encoding='utf-8')

print(f'Generazione completata: {_n_val} cartelle in {VALIDATION_PATH}')
print(f'  {_all_label}')
print(f'  {VALIDATION_PATH}/_{{id}}/mail.md + label.md')
"""))

# ══════════════════════════════════════════════════════════════════
#  SUMMARY
# ══════════════════════════════════════════════════════════════════
cells.append(code("""\
print('=' * 55)
print('PIPELINE COMPLETATA')
print('=' * 55)
for k, v in {
    'mode'              : 'DEV' if DEV_MODE else 'FULL',
    'seed'              : SEED,
    'n_emails_processed': len(df_processed),
    'n_embeddings'      : len(embeddings),
    'embedding_dim'     : embeddings.shape[1],
    'n_clusters'        : n_clusters,
    'noise_ratio'       : f'{noise_ratio:.2%}',
    'silhouette'        : round(sil, 4),
    'davies_bouldin'    : round(db, 4),
    'calinski_harabasz' : round(ch, 1),
    'llm_model'         : LLM_MODEL,
    'output_clustered'  : str(CLUSTERED_FILE),
    'output_validation' : str(VALIDATION_PATH),
    'output_figures'    : str(FIGURES_PATH),
}.items():
    print(f'  {k:<26}: {v}')
print('=' * 55)
"""))

# ══════════════════════════════════════════════════════════════════
#  ASSEMBLE & WRITE
# ══════════════════════════════════════════════════════════════════
nb = nbf.v4.new_notebook()
nb.metadata = {
    'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
    'language_info': {'name': 'python', 'version': '3.10.0'},
}
nb.cells = cells

out = Path('src/notebooks/full_pipeline_orchestration.ipynb')
out.parent.mkdir(parents=True, exist_ok=True)
with open(out, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f'Notebook generato: {out}  ({len(cells)} celle)')
