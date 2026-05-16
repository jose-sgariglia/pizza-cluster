import duckdb
import pandas as pd
import time
from pathlib import Path
from urllib.parse import urljoin

DEFAULT_FALLBACK_FILE = Path(__file__).resolve().parents[1] / "data" / "raw" / "emails_sample.parquet"


def _build_parquet_source(api_url: str | None, local_path: str | None) -> str:
    if local_path:
        source_path = Path(local_path)
        if not source_path.exists():
            raise FileNotFoundError(f"Local parquet file not found: {source_path}")
        return str(source_path)

    if not api_url:
        raise ValueError("api_url is required when local_path is not provided.")

    return urljoin(api_url, "v1/emails.parquet")


def _read_parquet_with_retries(parquet_source: str, limit: int = 100, retries: int = 2, backoff_seconds: float = 2.0) -> pd.DataFrame:
    last_exc = None
    for attempt in range(1, retries + 1):
        conn = duckdb.connect()
        try:
            return conn.sql(
                f"""
                SELECT *
                FROM read_parquet('{parquet_source}')
                LIMIT {limit}
                """
            ).df()
        except Exception as exc:
            last_exc = exc
            if attempt == retries:
                raise
            time.sleep(backoff_seconds)
    raise last_exc


def fetch_and_clean_emails(api_url: str | None = None, local_path: str | None = None, limit: int = 100) -> pd.DataFrame:
    """
    Carica un sample del dataset JMAIL tramite DuckDB e applica i filtri iniziali.

    Se la connessione HTTP fallisce, tenta di riprovare creando una nuova connessione DuckDB.
    Se esiste un file di fallback locale, lo usa come seconda chance.
    """
    parquet_source = _build_parquet_source(api_url=api_url, local_path=local_path)

    try:
        df_mail = _read_parquet_with_retries(parquet_source, limit=limit)
    except Exception as exc:
        if local_path is None and DEFAULT_FALLBACK_FILE.exists():
            df_mail = _read_parquet_with_retries(str(DEFAULT_FALLBACK_FILE), limit=limit, retries=1)
        else:
            raise

    df_mail = df_mail.loc[df_mail["is_promotional"] == False]
    df_mail.drop(columns=["is_promotional", "content_html", "release_batch"], inplace=True)
    return df_mail