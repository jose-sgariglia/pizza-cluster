import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timezone
from src.utils.llm_naming import get_llm_cluster_name_from_emails
import shutil
import sys

root = Path('/home/filippo/Scrivania/pizza-cluster')
clustered_file = root / 'data/processed/jmail_emails_clustered.parquet'
validation_path = root / 'data/validation'
SEED = 42
LLM_MODEL = "mannix/llama3.1-8b-abliterated"

print("Caricamento dataset...")
df = pd.read_parquet(clustered_file)

_cids = sorted(c for c in set(df['cluster']) if c != -1)
print(f"Rigenerazione nomi per {len(_cids)} cluster usando {LLM_MODEL}...")

cluster_names = {}
for i, cid in enumerate(_cids):
    _idx_cluster = np.where(df['cluster'] == cid)[0]
    _idx_sorted = _idx_cluster[np.argsort(df['cluster_prob'].values[_idx_cluster])[::-1]]
    _top_20_idx = _idx_sorted[:20]
    _top_emails = df.iloc[_top_20_idx]['combined_text'].fillna('').tolist()
    
    try:
        _name = get_llm_cluster_name_from_emails(_top_emails, model=LLM_MODEL)
    except Exception as e:
        print(f"  Errore per cluster {cid}: {e}")
        _name = "Fallback Name"
        
    cluster_names[cid] = _name
    print(f"  [{cid:3d}] {_name} ({i+1}/{len(_cids)})")

print("Salvataggio dataset etichettato...")
df['cluster_name'] = df['cluster'].map(cluster_names).fillna('Outlier')
df.to_parquet(clustered_file, index=False)
print("Fase 6 Completata.")

print("Generazione all_label.md...")
validation_path.mkdir(parents=True, exist_ok=True)
_lines = [
    '# Cluster Labels\n\n',
    f'Generato: {datetime.now(timezone.utc).isoformat()}\n',
    f'SEED: {SEED} | LLM: {LLM_MODEL}\n\n',
    '| Cluster | Nome | N email |\n',
    '|---------|------|---------|\n',
]
for cid in sorted(cluster_names.keys()):
    _n = int((df['cluster'] == cid).sum())
    _lines.append(f'| {cid} | {cluster_names[cid]} | {_n} |\n')
(validation_path / 'all_label.md').write_text(''.join(_lines), encoding='utf-8')

print("Pulizia vecchia cartella validation (rimozione cartelle fallite)...")
for item in validation_path.iterdir():
    if item.is_dir() and item.name.startswith('_EFTA'):
        shutil.rmtree(item)

print('Estrazione 10.000 email per validazione...')
_valid_df = df[df['cluster'] != -1]
_n_val  = min(10000, len(_valid_df))
_sample = _valid_df.sample(n=_n_val, random_state=SEED)

for _, row in _sample.iterrows():
    _eid  = str(row.get('id', row.name))
    _edir = validation_path / f'_{_eid}'
    _edir.mkdir(parents=True, exist_ok=True)

    _mail  = (f'# Email {_eid}\n\n'
              f'**Date:** {row.get("sent_at", "N/A")}\n'
              f'**From:** {row.get("sender", "N/A")}\n'
              f'**To:** {row.get("to_recipients", "N/A")}\n'
              f'**Subject:** {row.get("subject", "N/A")}\n\n---\n\n'
              + str(row.get('content_clean', row.get('combined_text', ''))))
    (_edir / 'mail.md').write_text(_mail, encoding='utf-8')

    _label = (f'# Label — Email {_eid}\n\n'
              f'**Cluster ID:** {row.get("cluster", "N/A")}\n'
              f'**Cluster Name:** {row.get("cluster_name", "N/A")}\n'
              f'**Probability:** {float(row.get("cluster_prob", 0)):.4f}\n')
    (_edir / 'label.md').write_text(_label, encoding='utf-8')

print(f"Completato! Generate {_n_val} cartelle in {validation_path}")
