import os
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())  # Carica variabili d'ambiente da .env se presente

def load_embedding_model(model_name: str = "all-MiniLM-L6-v2") -> SentenceTransformer:
    """
    Inizializza e carica il modello di Sentence Transformer specificato.
    """
    print(f"Caricamento del modello {model_name} in corso...")
    try:
        model = SentenceTransformer(model_name)
        print("✅ Modello caricato con successo.")
        return model
    except Exception as e:
        print(f"❌ Errore nel caricamento del modello: {e}")
        raise e

def compute_embeddings(model: SentenceTransformer, texts: list) -> np.ndarray:
    """
    Calcola gli embedding densi per una lista di testi puliti.
    """
    print(f"Calcolo degli embedding per {len(texts)} documenti...")
    try:
        embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
        print("✅ Calcolo completato con successo.")
        return embeddings
    except Exception as e:
        print(f"❌ Errore durante il calcolo: {e}")
        raise e

def save_embeddings(embeddings: np.ndarray, file_path: str):
    """
    Salva la matrice di embedding in un file binario .npy (NumPy).
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        np.save(file_path, embeddings)
        print(f"✅ Embedding salvati correttamente in: {file_path}")
    except Exception as e:
        print(f"❌ Errore durante il salvataggio degli embedding: {e}")
        raise e

def load_embeddings(file_path: str) -> np.ndarray:
    """
    Carica gli embedding precedentemente salvati in formato .npy.
    """
    print(f"Caricamento embedding da {file_path}...")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File non trovato: {file_path}")
    return np.load(file_path)


if __name__ == "__main__":
    PATH_CLEAN = os.environ.get("DATA_RAW_PATH") + "emails_sample.parquet"
    PATH_OUT_EMB = os.environ.get("MODEL_PATH") + "embeddings/email_embeddings.npy"
    PATH_OUT_META = os.environ.get("DATA_INTERIM_PATH") + "emails_with_embedding_ids.parquet"

    model = load_embedding_model()

    if os.path.exists(PATH_CLEAN):
        print(f"Caricamento dati pre-elaborati da: {PATH_CLEAN}")
        df = pd.read_parquet(PATH_CLEAN)

        # Gestiamo eventuali valori mancanti convertendoli in stringhe vuote
        texts = df["clean_text"].fillna("").tolist()
        
        # Calcolo degli embedding sui testi normalizzati e privi di rumore
        embeddings = compute_embeddings(model, texts)

        save_embeddings(embeddings, PATH_OUT_EMB)

        os.makedirs(os.path.dirname(PATH_OUT_META), exist_ok=True)
        df[['id']].to_parquet(PATH_OUT_META, index=False)
        print(f"✅ Mappatura ID salvata in: {PATH_OUT_META}")
        print("🚀 Pipeline di embedding su testo pulito completata con successo!")
    else:
        print(f"❌ Errore: Il file '{PATH_CLEAN}' non esiste. Esegui prima preprocessing.py.")