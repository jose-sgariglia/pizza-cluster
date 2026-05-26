"""Tests for embedding pipeline helpers."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import numpy as np
import pandas as pd

from src.utils.embedding_pipeline import (
    EmbeddingConfig,
    aggregate_chunk_embeddings,
    build_embedding_jobs,
    chunk_text,
    prepare_embedding_text,
)


class EmbeddingPipelineTestCase(unittest.TestCase):
    def test_prepare_embedding_text_adds_e5_prefix(self) -> None:
        text = prepare_embedding_text(" hello\nworld ", "intfloat/e5-base-v2")
        self.assertEqual(text, "passage: hello world")

    def test_chunk_text_uses_overlap(self) -> None:
        chunks = chunk_text("abcdef", chunk_char_length=4, chunk_char_overlap=1)
        self.assertEqual(chunks, ["abcd", "def"])

    def test_build_embedding_jobs_creates_chunk_index(self) -> None:
        config = _test_config(chunk_char_length=4, chunk_char_overlap=1)
        df = pd.DataFrame({"id": ["email-1"], "combined_text": ["abcdef"]})

        texts, index = build_embedding_jobs(df, config)

        self.assertEqual(texts, ["abcd", "def"])
        self.assertEqual(index.loc[0, "id"], "email-1")
        self.assertEqual(index.loc[0, "chunk_count"], 2)

    def test_aggregate_chunk_embeddings_mean_pools_and_normalizes(self) -> None:
        index = pd.DataFrame(
            [
                {"embedding_row": 0, "id": "a", "chunk_start": 0, "chunk_end": 2, "chunk_count": 2},
                {"embedding_row": 1, "id": "b", "chunk_start": 2, "chunk_end": 3, "chunk_count": 1},
            ]
        )
        chunk_embeddings = np.array([[1.0, 0.0], [1.0, 0.0], [0.0, 2.0]], dtype=np.float32)

        result = aggregate_chunk_embeddings(chunk_embeddings, index)

        np.testing.assert_allclose(result[0], np.array([1.0, 0.0], dtype=np.float32))
        np.testing.assert_allclose(result[1], np.array([0.0, 1.0], dtype=np.float32))

    def test_embedding_config_reads_env_values(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            env_file = root / ".env"
            env_file.write_text(
                "\n".join(
                    [
                        "DATA_PROCESSED_PATH=data/processed/",
                        "DATA_EMBEDDINGS_PATH=data/embeddings/",
                        "METADATA_PATH=data/metadata/",
                        "EMBEDDING_MODEL_NAME=BAAI/bge-small-en-v1.5",
                        "EMBEDDING_CHUNK_CHAR_LENGTH=10",
                        "EMBEDDING_CHUNK_CHAR_OVERLAP=2",
                        "EMBEDDING_BATCH_SIZE=4",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            config = EmbeddingConfig.from_env(env_file)

            self.assertEqual(config.model_name, "BAAI/bge-small-en-v1.5")
            self.assertEqual(config.chunk_char_length, 10)
            self.assertEqual(config.chunk_char_overlap, 2)
            self.assertEqual(config.batch_size, 4)
            self.assertEqual(config.embeddings_output_path, root / "data" / "embeddings" / "email_embeddings.npy")


def _test_config(chunk_char_length: int = 100, chunk_char_overlap: int = 10) -> EmbeddingConfig:
    return EmbeddingConfig(
        model_name="BAAI/bge-small-en-v1.5",
        input_text_column="combined_text",
        embedding_text_column="embedding_text",
        chunk_char_length=chunk_char_length,
        chunk_char_overlap=chunk_char_overlap,
        processed_input_path=Path("processed.parquet"),
        embeddings_output_path=Path("embeddings.npy"),
        embedding_index_output_path=Path("index.parquet"),
        embedding_metadata_output_path=Path("metadata.json"),
        batch_size=2,
    )


if __name__ == "__main__":
    unittest.main()
