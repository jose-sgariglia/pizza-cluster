import duckdb
import pandas as pd

def fetch_and_clean_emails(api_url: str, limit: int = 100) -> pd.DataFrame:
    """
    Carica un sample del dataset JMAIL tramite DuckDB e applica 
    i filtri iniziali per la pulizia dei dati.
    """
    # Connessione e definizione URL
    conn = duckdb.connect()
    url_mail = api_url + "v1/emails.parquet"

    # Estrazione con DuckDB
    df_mail = conn.sql(f"""
      SELECT * FROM read_parquet('{url_mail}')
      LIMIT {limit}
    """).df()

    # Filtering
    df_mail = df_mail.loc[df_mail["is_promotional"] == False]
    df_mail.drop(columns=["is_promotional", "content_html", "release_batch"], inplace=True)
    
    return df_mail