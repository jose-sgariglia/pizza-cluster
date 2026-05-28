"""Utilities for extracting raw email data from JMAIL.

Example:
    Run a small reproducible extraction from the project root:

    ```bash
    python -m src.utils.data_extraction
    ```
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urljoin

import pyarrow as pa
import pyarrow.parquet as pq
import requests
from dotenv import dotenv_values


DEFAULT_ENV_FILE = ".env"
DEFAULT_ENDPOINT = "v1/emails.parquet"
DEFAULT_RAW_FILENAME = "jmail_emails.parquet"
DEFAULT_RAW_SAMPLE_FILENAME = "jmail_emails_sample.parquet"
DEFAULT_METADATA_FILENAME = "jmail_extraction_metadata.json"


def _safe_int(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


@dataclass(frozen=True)
class ExtractionConfig:
    """Configuration required to extract data from JMAIL.

    Example:
        ```python
        config = ExtractionConfig.from_env()
        print(config.raw_output_path)
        ```
    """

    jmail_api: str
    raw_output_path: Path
    metadata_output_path: Path
    endpoint: str = DEFAULT_ENDPOINT

    @classmethod
    def from_env(
        cls,
        env_file: str | Path = DEFAULT_ENV_FILE,
        raw_filename: str | None = None,
        metadata_filename: str | None = None,
    ) -> "ExtractionConfig":
        """Build extraction configuration from the project `.env` file.

        Example:
            ```python
            config = ExtractionConfig.from_env(".env")
            ```
        """

        values = dotenv_values(env_file)
        jmail_api = values.get("JMAIL_API")
        raw_path = values.get("DATA_RAW_PATH", "data/raw/")
        metadata_path = values.get("METADATA_PATH", "data/metadata/")
        endpoint = values.get("JMAIL_EMAILS_ENDPOINT", DEFAULT_ENDPOINT)
        raw_name = raw_filename or values.get("RAW_EMAILS_FILENAME", DEFAULT_RAW_FILENAME)
        metadata_name = metadata_filename or values.get("EXTRACTION_METADATA_FILENAME", DEFAULT_METADATA_FILENAME)

        if not jmail_api:
            raise ValueError("Missing JMAIL_API in environment configuration.")

        return cls(
            jmail_api=jmail_api,
            raw_output_path=Path(raw_path) / raw_name,
            metadata_output_path=Path(metadata_path) / metadata_name,
            endpoint=endpoint,
        )

    @property
    def parquet_source(self) -> str:
        """Return the full JMAIL Parquet source URL.

        Example:
            ```python
            source = ExtractionConfig.from_env().parquet_source
            ```
        """

        return urljoin(self.jmail_api.rstrip("/") + "/", self.endpoint)


def inspect_remote_file(parquet_source: str) -> dict[str, object]:
    """Inspect remote file headers without downloading the body.

    Example:
        ```python
        metadata = inspect_remote_file("https://example.com/emails.parquet")
        print(metadata["content_length_bytes"])
        ```
    """

    response = requests.head(parquet_source, timeout=30, allow_redirects=True)
    response.raise_for_status()
    return {
        "status_code": response.status_code,
        "content_type": response.headers.get("content-type"),
        "content_length_bytes": _safe_int(response.headers.get("content-length")),
        "etag": response.headers.get("etag"),
        "last_modified": response.headers.get("last-modified"),
    }


def download_remote_file(
    source_url: str,
    output_path: str | Path,
    expected_size_bytes: int | None = None,
    chunk_size: int = 1024 * 1024,
) -> Path:
    """Download the raw JMAIL Parquet file without transforming it.

    Example:
        ```python
        download_remote_file(source, "data/raw/jmail_emails.parquet")
        ```
    """

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    if (
        expected_size_bytes is not None
        and output.exists()
        and output.stat().st_size == expected_size_bytes
    ):
        return output

    with requests.get(source_url, timeout=30, stream=True) as response:
        response.raise_for_status()
        with output.open("wb") as file_handle:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    file_handle.write(chunk)

    return output


def inspect_local_parquet(parquet_path: str | Path) -> dict[str, object]:
    """Inspect schema and row count from a local Parquet file.

    Example:
        ```python
        metadata = inspect_local_parquet("data/raw/jmail_emails.parquet")
        print(metadata["row_count"])
        ```
    """

    parquet_file = pq.ParquetFile(parquet_path)
    schema = parquet_file.schema_arrow
    return {
        "row_count": parquet_file.metadata.num_rows,
        "column_count": len(schema),
        "columns": [
            {
                "name": field.name,
                "type": str(field.type),
                "nullable": field.nullable,
            }
            for field in schema
        ],
        "num_row_groups": parquet_file.metadata.num_row_groups,
        "created_by": parquet_file.metadata.created_by,
    }


def extract_sample_from_local_parquet(
    parquet_path: str | Path,
    output_path: str | Path,
    limit: int,
) -> Path:
    """Create a deterministic sample from a local raw Parquet file.

    Example:
        ```python
        extract_sample_from_local_parquet("data/raw/jmail_emails.parquet", "data/raw/jmail_emails_sample.parquet", 100)
        ```
    """

    if limit <= 0:
        raise ValueError("limit must be greater than zero.")

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    parquet_file = pq.ParquetFile(parquet_path)
    batches = []
    remaining = limit
    for batch in parquet_file.iter_batches(batch_size=min(limit, 10_000)):
        if remaining <= 0:
            break
        current = batch.slice(0, remaining)
        batches.append(current)
        remaining -= current.num_rows

    table = pa.Table.from_batches(batches)
    pq.write_table(table, output)
    return output


def write_extraction_metadata(
    metadata_path: str | Path,
    metadata: dict[str, object],
) -> Path:
    """Write extraction metadata to JSON.

    Example:
        ```python
        write_extraction_metadata("data/metadata/jmail_extraction_metadata.json", metadata)
        ```
    """

    output = Path(metadata_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    return output


def run_extraction(
    env_file: str | Path = DEFAULT_ENV_FILE,
    sample_limit: int | None = None,
) -> dict[str, object]:
    """Run JMAIL download, local Parquet inspection, and metadata export.

    Example:
        ```python
        result = run_extraction()
        print(result["raw_output_path"])
        ```
    """

    config = ExtractionConfig.from_env(env_file=env_file)
    values = dotenv_values(env_file)
    sample_filename = values.get("RAW_EMAILS_SAMPLE_FILENAME", DEFAULT_RAW_SAMPLE_FILENAME)
    remote_metadata = inspect_remote_file(config.parquet_source)
    raw_output = download_remote_file(
        source_url=config.parquet_source,
        output_path=config.raw_output_path,
        expected_size_bytes=remote_metadata.get("content_length_bytes"),
    )
    local_metadata = inspect_local_parquet(raw_output)

    sample_output = None
    if sample_limit is not None:
        sample_output = extract_sample_from_local_parquet(
            parquet_path=raw_output,
            output_path=raw_output.with_name(sample_filename),
            limit=sample_limit,
        )

    extraction_metadata = {
        "source": "JMAIL",
        "endpoint": config.endpoint,
        "extracted_at_utc": datetime.now(UTC).isoformat(),
        "raw_output_path": str(raw_output),
        "sample_output_path": str(sample_output) if sample_output else None,
        "sample_limit": sample_limit,
        "remote": remote_metadata,
        "local_parquet": local_metadata,
    }
    metadata_output = write_extraction_metadata(
        metadata_path=config.metadata_output_path,
        metadata=extraction_metadata,
    )

    return {
        "endpoint": config.endpoint,
        "raw_output_path": str(raw_output),
        "metadata_output_path": str(metadata_output),
        "sample_output_path": str(sample_output) if sample_output else None,
        "row_count": local_metadata["row_count"],
        "column_count": local_metadata["column_count"],
    }


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for local execution.

    Example:
        ```bash
        python -m src.utils.data_extraction --limit 50
        ```
    """

    parser = argparse.ArgumentParser(description="Download and inspect the JMAIL email dataset.")
    parser.add_argument("--sample-limit", type=int, default=None, help="Optional sample row count.")
    parser.add_argument("--env-file", default=DEFAULT_ENV_FILE, help="Path to .env file.")
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    result = run_extraction(env_file=arguments.env_file, sample_limit=arguments.sample_limit)
    print(json.dumps(result, indent=2, default=str))
