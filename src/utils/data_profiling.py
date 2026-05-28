"""Utilities for profiling local JMAIL Parquet datasets.

Example:
    Run a profile from the project root:

    ```bash
    python -m src.utils.data_profiling
    ```
"""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq
from dotenv import dotenv_values


DEFAULT_ENV_FILE = ".env"
DEFAULT_RAW_FILENAME = "jmail_emails.parquet"
DEFAULT_PROFILE_FILENAME = "jmail_profile.json"
TEXT_COLUMNS = ("subject", "content_markdown", "content_html")
PARTICIPANT_COLUMNS = ("sender", "to_recipients", "cc_recipients", "bcc_recipients", "all_participants")


def build_profile_paths(
    env_file: str | Path = DEFAULT_ENV_FILE,
    raw_filename: str = DEFAULT_RAW_FILENAME,
    profile_filename: str = DEFAULT_PROFILE_FILENAME,
) -> tuple[Path, Path]:
    """Build input and output paths from `.env`.

    Example:
        ```python
        raw_path, profile_path = build_profile_paths()
        ```
    """

    values = dotenv_values(env_file)
    raw_name = values.get("RAW_EMAILS_FILENAME", raw_filename)
    profile_name = values.get("PROFILE_METADATA_FILENAME", profile_filename)
    raw_path = Path(values.get("DATA_RAW_PATH", "data/raw/")) / raw_name
    metadata_path = Path(values.get("METADATA_PATH", "data/metadata/")) / profile_name
    return raw_path, metadata_path


def profile_parquet(parquet_path: str | Path) -> dict[str, Any]:
    """Profile a Parquet file with column-level completeness and basic statistics.

    Example:
        ```python
        profile = profile_parquet("data/raw/jmail_emails.parquet")
        print(profile["row_count"])
        ```
    """

    path = Path(parquet_path)
    table = pq.read_table(path)
    row_count = table.num_rows

    columns = []
    for field in table.schema:
        column = table[field.name]
        null_count = column.null_count
        non_null_count = row_count - null_count
        column_profile: dict[str, Any] = {
            "name": field.name,
            "type": str(field.type),
            "nullable": field.nullable,
            "null_count": null_count,
            "null_ratio": round(null_count / row_count, 6) if row_count else None,
            "non_null_count": non_null_count,
        }

        if field.name in TEXT_COLUMNS:
            lengths = _string_lengths(column)
            column_profile.update(_numeric_summary(lengths, prefix="length"))
            column_profile["sample_values"] = _sample_strings(column)

        if field.name in PARTICIPANT_COLUMNS:
            column_profile["sample_values"] = _sample_strings(column)

        if str(field.type) in {"bool", "int64", "int32", "double", "float"}:
            column_profile.update(_numeric_summary(column.to_pylist()))

        columns.append(column_profile)

    return {
        "profiled_at_utc": datetime.now(UTC).isoformat(),
        "source_path": str(path),
        "row_count": row_count,
        "column_count": table.num_columns,
        "columns": columns,
        "candidate_text_columns": [name for name in TEXT_COLUMNS if name in table.column_names],
        "candidate_participant_columns": [name for name in PARTICIPANT_COLUMNS if name in table.column_names],
        "candidate_filter_columns": [
            name for name in ("is_promotional", "epstein_is_sender", "release_batch") if name in table.column_names
        ],
    }


def write_profile(profile: dict[str, Any], output_path: str | Path) -> Path:
    """Write a dataset profile to JSON.

    Example:
        ```python
        write_profile(profile, "data/metadata/jmail_profile.json")
        ```
    """

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(profile, indent=2, ensure_ascii=False), encoding="utf-8")
    return output


def run_profile(env_file: str | Path = DEFAULT_ENV_FILE) -> dict[str, Any]:
    """Profile the configured raw JMAIL Parquet dataset and save metadata.

    Example:
        ```python
        result = run_profile()
        print(result["profile_output_path"])
        ```
    """

    raw_path, profile_path = build_profile_paths(env_file=env_file)
    profile = profile_parquet(raw_path)
    output = write_profile(profile, profile_path)
    return {
        "raw_path": str(raw_path),
        "profile_output_path": str(output),
        "row_count": profile["row_count"],
        "column_count": profile["column_count"],
    }


def _string_lengths(column: Any) -> list[int]:
    return [len(value) for value in column.to_pylist() if isinstance(value, str)]


def _sample_strings(column: Any, limit: int = 3, max_length: int = 160) -> list[str]:
    samples = []
    for value in column.to_pylist():
        if not isinstance(value, str) or not value.strip():
            continue
        normalized = " ".join(value.split())
        samples.append(normalized[:max_length])
        if len(samples) >= limit:
            break
    return samples


def _numeric_summary(values: list[Any], prefix: str | None = None) -> dict[str, Any]:
    clean_values = [value for value in values if isinstance(value, (int, float)) and value is not None]
    key = f"{prefix}_" if prefix else ""
    if not clean_values:
        return {
            f"{key}min": None,
            f"{key}max": None,
            f"{key}mean": None,
        }

    return {
        f"{key}min": min(clean_values),
        f"{key}max": max(clean_values),
        f"{key}mean": round(sum(clean_values) / len(clean_values), 4),
    }


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for local profiling.

    Example:
        ```bash
        python -m src.utils.data_profiling --env-file .env
        ```
    """

    parser = argparse.ArgumentParser(description="Profile the local JMAIL raw Parquet dataset.")
    parser.add_argument("--env-file", default=DEFAULT_ENV_FILE, help="Path to .env file.")
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    result = run_profile(env_file=arguments.env_file)
    print(json.dumps(result, indent=2))
