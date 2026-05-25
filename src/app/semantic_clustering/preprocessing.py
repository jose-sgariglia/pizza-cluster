import os
import re
import pandas as pd

def normalize_text(text: str) -> str:
    """Converte il testo in minuscolo per standardizzare il vocabolario."""
    if not isinstance(text, str):
        return ""
    return text.lower()

def remove_urls(text: str) -> str:
    """Rimuove URL e link web (http, https, www)."""
    url_pattern = r'https?://\S+|www\.\S+'
    return re.sub(url_pattern, '', text)

def remove_emails(text: str) -> str:
    """Rimuove gli indirizzi email dal testo per evitare rumore sui mittenti."""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.sub(email_pattern, '', text)

def remove_extra_spaces(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()

def build_clean_text(subject: str, body: str) -> str:
    # Uniamo i campi gestendo eventuali valori nulli (NaN)
    full_text = f"{str(subject) if pd.notna(subject) else ''} {str(body) if pd.notna(body) else ''}"
    
    # Pipeline di pulizia
    text = normalize_text(full_text)
    text = remove_urls(text)
    text = remove_emails(text)
    text = remove_extra_spaces(text)
    
    return text

if __name__ == "__main__":
    PATH_RAW = "data/raw/emails_sample.parquet"
    PATH_OUT = "data/clean/emails_sample_clean.parquet"

    if os.path.exists(PATH_RAW):
        print(f"Caricamento dati grezzi da: {PATH_RAW}")
        df = pd.read_parquet(PATH_RAW)
        
        print("Applicazione della pipeline di preprocessing...")
        # Applichiamo la funzione riga per riga su subject e content_markdown
        df["clean_text"] = df.apply(
            lambda row: build_clean_text(row["subject"], row["content_markdown"]), 
            axis=1
        )
        
        # Salvataggio del dataset pulito (Deliverable Tecnico)
        os.makedirs(os.path.dirname(PATH_OUT), exist_ok=True)
        df.to_parquet(PATH_OUT, index=False)
        print(f"✅ Dataset pulito salvato in: {PATH_OUT}")
        
        # Stampa di un esempio rapido di controllo nel terminale
        print("\n--- ESEMPIO DI CONTROLLO PRIMA/DOPO ---")
        print(f"ORIGINALE (Subject): {df['subject'].iloc[0]}")
        print(f"PULITO (Primi 150 caratteri): {df['clean_text'].iloc[0][:150]}...")
    else:
        print(f"❌ Errore: File {PATH_RAW} non trovato.")