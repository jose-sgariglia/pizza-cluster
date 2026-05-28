"""Email embedding generation pipeline.

Example:
    Build the default configuration:

    ```python
    from src.utils.embedding_pipeline import EmbeddingConfig

    config = EmbeddingConfig.from_env()
    print(config.model_name)
    ```
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from dotenv import dotenv_values
from sentence_transformers import SentenceTransformer


DEFAULT_ENV_FILE = ".env"
DEFAULT_MODEL_NAME = "BAAI/bge-small-en-v1.5"
DEFAULT_INPUT_TEXT_COLUMN = "combined_text"
DEFAULT_EMBEDDING_TEXT_COLUMN = "embedding_text"
DEFAULT_CHUNK_CHAR_LENGTH = 1800
DEFAULT_CHUNK_CHAR_OVERLAP = 200
DEFAULT_EMBEDDINGS_FILENAME = "email_embeddings.npy"
DEFAULT_EMBEDDING_INDEX_FILENAME = "email_embedding_index.parquet"
DEFAULT_EMBEDDING_METADATA_FILENAME = "email_embedding_metadata.json"
DEFAULT_EMBEDDING_BATCH_SIZE = 32


MODEL_REGISTRY: dict[str, dict[str, Any]] = {
    "BAAI/bge-small-en-v1.5": {
        "embedding_dimensions": 384,
        "max_sequence_length": 512,
        "recommended_role": "primary_baseline",
        "input_prefix": "",
    },
    "sentence-transformers/all-MiniLM-L6-v2": {
        "embedding_dimensions": 384,
        "max_sequence_length": 256,
        "recommended_role": "fast_baseline",
        "input_prefix": "",
    },
    "intfloat/e5-base-v2": {
        "embedding_dimensions": 768,
        "max_sequence_length": 512,
        "recommended_role": "quality_candidate",
        "input_prefix": "passage: ",
    },
}


@dataclass(frozen=True)
class EmbeddingConfig:
    """Configuration for the future embedding generation pipeline.

    Example:
        ```python
        config = EmbeddingConfig.from_env()
        assert config.chunk_char_length > config.chunk_char_overlap
        ```
    """

    model_name: str
    input_text_column: str
    embedding_text_column: str
    chunk_char_length: int
    chunk_char_overlap: int
    processed_input_path: Path
    embeddings_output_path: Path
    embedding_index_output_path: Path
    embedding_metadata_output_path: Path
    batch_size: int

    @classmethod
    def from_env(cls, env_file: str | Path = DEFAULT_ENV_FILE) -> "EmbeddingConfig":
        """Create an embedding config from `.env`.

        Example:
            ```python
            config = EmbeddingConfig.from_env(".env")
            ```
        """

        values = dotenv_values(env_file)
        root = Path(env_file).resolve().parent

        model_name = values.get("EMBEDDING_MODEL_NAME", DEFAULT_MODEL_NAME)
        input_text_column = values.get("EMBEDDING_INPUT_TEXT_COLUMN", DEFAULT_INPUT_TEXT_COLUMN)
        embedding_text_column = values.get("EMBEDDING_TEXT_COLUMN", DEFAULT_EMBEDDING_TEXT_COLUMN)
        chunk_char_length = int(values.get("EMBEDDING_CHUNK_CHAR_LENGTH", str(DEFAULT_CHUNK_CHAR_LENGTH)))
        chunk_char_overlap = int(values.get("EMBEDDING_CHUNK_CHAR_OVERLAP", str(DEFAULT_CHUNK_CHAR_OVERLAP)))
        batch_size = int(values.get("EMBEDDING_BATCH_SIZE", str(DEFAULT_EMBEDDING_BATCH_SIZE)))

        processed_path = _resolve_path(root, values.get("DATA_PROCESSED_PATH", "data/processed/"))
        metadata_path = _resolve_path(root, values.get("METADATA_PATH", "data/metadata/"))
        embeddings_path = _resolve_path(
            root,
            values.get("DATA_EMBEDDINGS_PATH", values.get("MODEL_EMBEDDINGS_PATH", "data/embeddings/")),
        )

        processed_filename = values.get("PROCESSED_EMAILS_SAMPLE_FILENAME", "jmail_emails_processed_sample.parquet")
        embeddings_filename = values.get("EMBEDDINGS_FILENAME", DEFAULT_EMBEDDINGS_FILENAME)
        index_filename = values.get("EMBEDDING_INDEX_FILENAME", DEFAULT_EMBEDDING_INDEX_FILENAME)
        metadata_filename = values.get("EMBEDDING_METADATA_FILENAME", DEFAULT_EMBEDDING_METADATA_FILENAME)

        config = cls(
            model_name=model_name,
            input_text_column=input_text_column,
            embedding_text_column=embedding_text_column,
            chunk_char_length=chunk_char_length,
            chunk_char_overlap=chunk_char_overlap,
            processed_input_path=processed_path / processed_filename,
            embeddings_output_path=embeddings_path / embeddings_filename,
            embedding_index_output_path=metadata_path / index_filename,
            embedding_metadata_output_path=metadata_path / metadata_filename,
            batch_size=batch_size,
        )
        validate_embedding_config(config)
        return config


def validate_embedding_config(config: EmbeddingConfig) -> None:
    """Validate embedding configuration values.

    Example:
        ```python
        validate_embedding_config(config)
        ```
    """

    if config.model_name not in MODEL_REGISTRY:
        known = ", ".join(sorted(MODEL_REGISTRY))
        raise ValueError(f"Unsupported embedding model: {config.model_name}. Known models: {known}")
    if config.chunk_char_length <= 0:
        raise ValueError("chunk_char_length must be greater than zero.")
    if config.chunk_char_overlap < 0:
        raise ValueError("chunk_char_overlap cannot be negative.")
    if config.chunk_char_overlap >= config.chunk_char_length:
        raise ValueError("chunk_char_overlap must be smaller than chunk_char_length.")
    if config.batch_size <= 0:
        raise ValueError("batch_size must be greater than zero.")


def load_embedding_model(model_name: str) -> SentenceTransformer:
    """Load a SentenceTransformer model.

    Example:
        ```python
        model = load_embedding_model("BAAI/bge-small-en-v1.5")
        ```
    """

    return SentenceTransformer(model_name)


def prepare_embedding_text(value: Any, model_name: str) -> str:
    """Prepare text for an embedding model without destructive preprocessing.

    Redacted spans are preserved. Some models, such as E5, use an input prefix.

    Example:
        ```python
        prepare_embedding_text("Email body", "intfloat/e5-base-v2")
        ```
    """

    text = normalize_embedding_text(value)
    prefix = MODEL_REGISTRY.get(model_name, {}).get("input_prefix", "")
    return f"{prefix}{text}" if text else ""


def normalize_embedding_text(value: Any) -> str:
    """Normalize whitespace while preserving original textual information.

    Example:
        ```python
        normalize_embedding_text(" hello\\n world ")
        ```
    """

    if not isinstance(value, str):
        return ""
    return " ".join(value.split())


def chunk_text(text: str, chunk_char_length: int, chunk_char_overlap: int) -> list[str]:
    """Split text into overlapping character chunks.

    This is a conservative first approximation before token-aware chunking.

    Example:
        ```python
        chunks = chunk_text("abcdef", chunk_char_length=4, chunk_char_overlap=1)
        ```
    """

    if chunk_char_length <= 0:
        raise ValueError("chunk_char_length must be greater than zero.")
    if chunk_char_overlap < 0:
        raise ValueError("chunk_char_overlap cannot be negative.")
    if chunk_char_overlap >= chunk_char_length:
        raise ValueError("chunk_char_overlap must be smaller than chunk_char_length.")

    normalized = normalize_embedding_text(text)
    if not normalized:
        return []
    if len(normalized) <= chunk_char_length:
        return [normalized]

    chunks = []
    start = 0
    step = chunk_char_length - chunk_char_overlap
    while start < len(normalized):
        chunk = normalized[start : start + chunk_char_length].strip()
        if chunk:
            chunks.append(chunk)
        if start + chunk_char_length >= len(normalized):
            break
        start += step
    return chunks


def build_embedding_jobs(df: pd.DataFrame, config: EmbeddingConfig) -> tuple[list[str], pd.DataFrame]:
    """Build chunk-level embedding jobs and an email-level index.

    Example:
        ```python
        texts, index = build_embedding_jobs(processed_df, config)
        ```
    """

    required_columns = {"id", config.input_text_column}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns for embeddings: {sorted(missing_columns)}")

    chunk_texts: list[str] = []
    index_rows: list[dict[str, Any]] = []

    for output_position, row in enumerate(df.itertuples(index=False)):
        row_data = row._asdict()
        email_id = row_data["id"]
        source_text = row_data[config.input_text_column]
        prepared_text = prepare_embedding_text(source_text, config.model_name)
        chunks = chunk_text(
            prepared_text,
            chunk_char_length=config.chunk_char_length,
            chunk_char_overlap=config.chunk_char_overlap,
        )

        start = len(chunk_texts)
        chunk_texts.extend(chunks)
        index_rows.append(
            {
                "embedding_row": output_position,
                "id": email_id,
                "chunk_start": start,
                "chunk_end": start + len(chunks),
                "chunk_count": len(chunks),
                "embedding_text_length": len(prepared_text),
            }
        )

    return chunk_texts, pd.DataFrame(index_rows)


def encode_texts(model: SentenceTransformer, texts: list[str], batch_size: int) -> np.ndarray:
    """Encode texts with a SentenceTransformer model.

    Example:
        ```python
        vectors = encode_texts(model, ["hello"], batch_size=32)
        ```
    """

    if not texts:
        return np.empty((0, 0), dtype=np.float32)
    return model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).astype(np.float32)


def aggregate_chunk_embeddings(chunk_embeddings: np.ndarray, embedding_index: pd.DataFrame) -> np.ndarray:
    """Aggregate chunk embeddings into one embedding per email using mean pooling.

    Example:
        ```python
        email_vectors = aggregate_chunk_embeddings(chunk_vectors, embedding_index)
        ```
    """

    if embedding_index.empty:
        return np.empty((0, 0), dtype=np.float32)
    if chunk_embeddings.ndim != 2:
        raise ValueError("chunk_embeddings must be a 2D array.")

    dimensions = chunk_embeddings.shape[1]
    email_embeddings = np.zeros((len(embedding_index), dimensions), dtype=np.float32)

    for row in embedding_index.itertuples(index=False):
        if row.chunk_count == 0:
            continue
        email_embeddings[row.embedding_row] = chunk_embeddings[row.chunk_start : row.chunk_end].mean(axis=0)

    return _normalize_rows(email_embeddings)


def run_embedding_pipeline(env_file: str | Path = DEFAULT_ENV_FILE) -> dict[str, Any]:
    """Generate email embeddings and write vectors, index and metadata.

    Example:
        ```python
        result = run_embedding_pipeline(".env")
        ```
    """

    config = EmbeddingConfig.from_env(env_file=env_file)
    df = pd.read_parquet(config.processed_input_path)
    chunk_texts, embedding_index = build_embedding_jobs(df, config)
    model = load_embedding_model(config.model_name)
    chunk_embeddings = encode_texts(model, chunk_texts, batch_size=config.batch_size)
    email_embeddings = aggregate_chunk_embeddings(chunk_embeddings, embedding_index)

    config.embeddings_output_path.parent.mkdir(parents=True, exist_ok=True)
    np.save(config.embeddings_output_path, email_embeddings)

    config.embedding_index_output_path.parent.mkdir(parents=True, exist_ok=True)
    embedding_index.to_parquet(config.embedding_index_output_path, index=False)

    metadata = {
        "created_at_utc": datetime.now(UTC).isoformat(),
        "model_name": config.model_name,
        "model_registry": MODEL_REGISTRY[config.model_name],
        "input_path": str(config.processed_input_path),
        "embeddings_output_path": str(config.embeddings_output_path),
        "embedding_index_output_path": str(config.embedding_index_output_path),
        "row_count": int(email_embeddings.shape[0]),
        "embedding_dimensions": int(email_embeddings.shape[1]) if email_embeddings.size else 0,
        "chunk_count": len(chunk_texts),
        "chunk_char_length": config.chunk_char_length,
        "chunk_char_overlap": config.chunk_char_overlap,
        "batch_size": config.batch_size,
        "normalization": "L2 row normalization after mean chunk aggregation.",
    }
    config.embedding_metadata_output_path.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return metadata


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for embedding generation.

    Example:
        ```bash
        python -m src.utils.embedding_pipeline --env-file .env
        ```
    """

    parser = argparse.ArgumentParser(description="Generate email embeddings from processed JMAIL data.")
    parser.add_argument("--env-file", default=DEFAULT_ENV_FILE, help="Path to .env file.")
    return parser.parse_args()


def _normalize_rows(values: np.ndarray) -> np.ndarray:
    if values.size == 0:
        return values.astype(np.float32)
    norms = np.linalg.norm(values, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return (values / norms).astype(np.float32)


def _resolve_path(root: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return root / path


if __name__ == "__main__":
    arguments = parse_args()
    result = run_embedding_pipeline(env_file=arguments.env_file)
    print(json.dumps(result, indent=2))
