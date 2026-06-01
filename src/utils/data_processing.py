"""Cleaning and rough feature engineering for JMAIL email data.

Example:
    Run the first processing pipeline from the project root:

    ```bash
    python -m src.utils.data_processing
    ```
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd
from dotenv import dotenv_values


DEFAULT_ENV_FILE = ".env"
DEFAULT_RAW_FILENAME = "jmail_emails.parquet"
DEFAULT_PROCESSED_FILENAME = "jmail_emails_processed.parquet"
DEFAULT_METADATA_FILENAME = "jmail_processing_metadata.json"
DEFAULT_TEST_PROCESSED_FILENAME = "jmail_emails_processed_sample.parquet"
DEFAULT_TEST_METADATA_FILENAME = "jmail_processing_sample_metadata.json"
KEEP_COLUMNS = [
    "id",
    "doc_id",
    "message_index",
    "sender",
    "subject",
    "to_recipients",
    "cc_recipients",
    "bcc_recipients",
    "sent_at",
    "content_markdown",
    "attachments",
    "email_drop_id",
    "is_promotional",
    "release_batch",
    "epstein_is_sender",
    "all_participants",
]
REDACTION_PATTERNS = (
    re.compile(r"\bredacted\b", re.IGNORECASE),
    re.compile(r"\bwithheld\b", re.IGNORECASE),
    re.compile(r"\bsealed\b", re.IGNORECASE),
    re.compile(r"\[+\s*(?:redacted|withheld|sealed)\s*\]+", re.IGNORECASE),
    re.compile(r"\bX{4,}\b", re.IGNORECASE),
    re.compile(r"[█■]{2,}"),
)


def build_processing_paths(
    env_file: str | Path = DEFAULT_ENV_FILE,
    raw_filename: str = DEFAULT_RAW_FILENAME,
    processed_filename: str = DEFAULT_PROCESSED_FILENAME,
    metadata_filename: str = DEFAULT_METADATA_FILENAME,
) -> tuple[Path, Path, Path]:
    """Build raw, processed and metadata paths from `.env`.

    Example:
        ```python
        raw_path, processed_path, metadata_path = build_processing_paths()
        ```
    """

    values = dotenv_values(env_file)
    env_root = Path(env_file).resolve().parent
    raw_name = values.get("RAW_EMAILS_FILENAME", raw_filename)
    processed_name = values.get("PROCESSED_EMAILS_FILENAME", processed_filename)
    metadata_name = values.get("PROCESSING_METADATA_FILENAME", metadata_filename)
    raw_path = _resolve_project_path(env_root, values.get("DATA_RAW_PATH", "data/raw/")) / raw_name
    processed_path = _resolve_project_path(env_root, values.get("DATA_PROCESSED_PATH", "data/processed/")) / processed_name
    metadata_path = _resolve_project_path(env_root, values.get("METADATA_PATH", "data/metadata/")) / metadata_name
    return raw_path, processed_path, metadata_path


def _resolve_project_path(root: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return root / path


def normalize_text(value: Any) -> str:
    """Normalize whitespace while preserving the underlying text content.

    This function does not remove or rewrite redacted/censored spans.

    Example:
        ```python
        normalize_text(" Hello\\n  world ")
        ```
    """

    if not isinstance(value, str):
        return ""
    return " ".join(value.split())


def has_redaction_marker(value: Any) -> bool:
    """Detect likely redaction/censorship markers without editing the text.

    Example:
        ```python
        has_redaction_marker("[REDACTED]")
        ```
    """

    if not isinstance(value, str):
        return False
    return any(pattern.search(value) is not None for pattern in REDACTION_PATTERNS)


def count_redaction_markers(value: Any) -> int:
    """Count redaction/censorship markers in the text.

    Example:
        ```python
        count_redaction_markers("[REDACTED] and [SEALED]")
        ```
    """

    if not isinstance(value, str):
        return 0
    combined_pattern = re.compile(
        r"\[+\s*(?:redacted|withheld|sealed)\s*\]+|\bredacted\b|\bwithheld\b|\bsealed\b|\bX{4,}\b|[█■]{2,}",
        re.IGNORECASE
    )
    return len(combined_pattern.findall(value))


def estimate_recipient_count(*values: Any) -> int:
    """Estimate recipient count from raw recipient string fields.

    Example:
        ```python
        estimate_recipient_count("a@example.com, b@example.com", None)
        ```
    """

    recipients: set[str] = set()
    for value in values:
        if not isinstance(value, str) or not value.strip():
            continue
        parts = re.split(r"[,;\n]+", value)
        for part in parts:
            cleaned = part.strip().lower()
            if cleaned:
                recipients.add(cleaned)
    return len(recipients)


def select_supported_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Select the first-pipeline columns available in the raw dataset.

    Example:
        ```python
        selected = select_supported_columns(raw_df)
        ```
    """

    available_columns = [column for column in KEEP_COLUMNS if column in df.columns]
    return df.loc[:, available_columns].copy()


def filter_promotional_emails(df: pd.DataFrame) -> pd.DataFrame:
    """Remove emails explicitly marked as promotional.

    Null values are retained because they represent unknown status, not confirmed promotion.

    Example:
        ```python
        filtered = filter_promotional_emails(df)
        ```
    """

    if "is_promotional" not in df.columns:
        return df.copy()
    return df.loc[df["is_promotional"] != True].copy()


def add_text_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add normalized text columns and rough text features.

    Redaction markers are only detected through `has_redaction`; they are not removed.

    Example:
        ```python
        enriched = add_text_features(df)
        ```
    """

    result = df.copy()
    result["subject_clean"] = result.get("subject", "").map(normalize_text)
    result["content_clean"] = result.get("content_markdown", "").map(normalize_text)
    result["combined_text"] = (
        result["subject_clean"].where(result["subject_clean"] != "", "")
        + "\n\n"
        + result["content_clean"].where(result["content_clean"] != "", "")
    ).str.strip()
    result["subject_length"] = result["subject_clean"].str.len().fillna(0).astype("Int64")
    result["content_length"] = result["content_clean"].str.len().fillna(0).astype("Int64")
    result["combined_text_length"] = result["combined_text"].str.len().fillna(0).astype("Int64")
    result["has_subject"] = result["subject_clean"] != ""
    result["has_redaction"] = result["subject"].map(has_redaction_marker) | result["content_markdown"].map(
        has_redaction_marker
    )
    result["redaction_count"] = result["subject"].map(count_redaction_markers).fillna(0).astype("Int64") + result["content_markdown"].map(count_redaction_markers).fillna(0).astype("Int64")
    result["word_count"] = result["combined_text"].str.split().str.len().fillna(0).astype("Int64")
    
    combined_len = result["combined_text_length"]
    upper_count = result["combined_text"].str.count(r"[A-Z]")
    result["uppercase_ratio"] = (upper_count / combined_len.where(combined_len > 0)).fillna(0.0)
    
    return result


def add_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    """Parse `sent_at` and add coarse temporal features.

    Example:
        ```python
        enriched = add_temporal_features(df)
        ```
    """

    result = df.copy()
    if "sent_at" not in result.columns:
        result["sent_at_datetime"] = pd.NaT
    else:
        result["sent_at_datetime"] = pd.to_datetime(result["sent_at"], errors="coerce", utc=True)

    result["sent_year"] = result["sent_at_datetime"].dt.year.astype("Int64")
    result["sent_month"] = result["sent_at_datetime"].dt.month.astype("Int64")
    result["sent_dayofweek"] = result["sent_at_datetime"].dt.dayofweek.astype("Int64")
    result["sent_hour"] = result["sent_at_datetime"].dt.hour.astype("Int64")
    result["is_weekend"] = result["sent_dayofweek"].isin([5, 6])
    return result


def add_metadata_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add rough metadata features from sender, recipients and attachments.

    Example:
        ```python
        enriched = add_metadata_features(df)
        ```
    """

    result = df.copy()
    sender = result.get("sender")
    attachments = result.get("attachments")

    result["has_sender"] = sender.map(lambda value: isinstance(value, str) and bool(value.strip())) if sender is not None else False
    result["has_attachments"] = attachments.fillna(0).astype("Int64") > 0 if attachments is not None else False
    result["attachment_count"] = attachments.fillna(0).astype("Int64") if attachments is not None else 0
    result["recipient_count_estimate"] = estimate_recipient_counts(
        result.get("to_recipients"),
        result.get("cc_recipients"),
        result.get("bcc_recipients"),
        row_count=len(result),
    )
    
    sender_series = result.get("sender", pd.Series("", index=result.index)).fillna("").astype(str)
    result["sender_domain"] = sender_series.str.extract(r"@([a-zA-Z0-9.-]+)", expand=False).str.lower()
    
    epstein_sender = result.get("epstein_is_sender", pd.Series(False, index=result.index)).fillna(False).astype(bool)
    all_parts = result.get("all_participants", pd.Series("", index=result.index)).fillna("").astype(str).str.lower()
    result["is_epstein_involved"] = epstein_sender | all_parts.str.contains("epstein", regex=False)
    
    return result


def estimate_recipient_counts(
    to_recipients: pd.Series | None,
    cc_recipients: pd.Series | None,
    bcc_recipients: pd.Series | None,
    row_count: int,
) -> pd.Series:
    """Estimate recipient counts with vectorized string operations.

    Example:
        ```python
        counts = estimate_recipient_counts(df["to_recipients"], df["cc_recipients"], None, len(df))
        ```
    """

    counts = pd.Series(0, index=range(row_count), dtype="Int64")
    for series in (to_recipients, cc_recipients, bcc_recipients):
        if series is None:
            continue
        normalized = series.fillna("").astype(str).str.strip()
        non_empty = normalized != ""
        separators = normalized.str.count(r"[,;\n]+")
        counts = counts + non_empty.astype("Int64") + separators.where(non_empty, 0).astype("Int64")
    return counts


def remove_empty_text_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows without usable combined text.

    Example:
        ```python
        usable = remove_empty_text_rows(df)
        ```
    """

    if "combined_text" not in df.columns:
        return df.copy()
    return df.loc[df["combined_text"].str.len() > 0].copy()


def process_emails(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Run the first cleaning and rough feature-engineering pipeline.

    Example:
        ```python
        processed, metadata = process_emails(raw_df)
        ```
    """

    input_rows = len(df)
    selected = select_supported_columns(df)
    selected_rows = len(selected)
    filtered = filter_promotional_emails(selected)
    after_promotional_filter = len(filtered)
    with_text = add_text_features(filtered)
    with_time = add_temporal_features(with_text)
    enriched = add_metadata_features(with_time)
    processed = remove_empty_text_rows(enriched)

    metadata = {
        "processed_at_utc": datetime.now(UTC).isoformat(),
        "input_rows": input_rows,
        "selected_rows": selected_rows,
        "after_promotional_filter_rows": after_promotional_filter,
        "output_rows": len(processed),
        "removed_promotional_rows": selected_rows - after_promotional_filter,
        "removed_empty_text_rows": after_promotional_filter - len(processed),
        "output_columns": list(processed.columns),
        "redaction_policy": "Redaction markers are detected in has_redaction but text spans are preserved.",
    }
    return processed, metadata


def run_processing(env_file: str | Path = DEFAULT_ENV_FILE) -> dict[str, Any]:
    """Process configured raw JMAIL data and write processed output plus metadata.

    Example:
        ```python
        result = run_processing()
        print(result["processed_output_path"])
        ```
    """

    return run_processing_with_limit(env_file=env_file, limit=None)


def run_processing_with_limit(
    env_file: str | Path = DEFAULT_ENV_FILE,
    limit: int | None = None,
) -> dict[str, Any]:
    """Process configured raw JMAIL data, optionally limiting rows for testing.

    Use `limit=-1` to explicitly process the full dataset.

    Example:
        ```python
        result = run_processing_with_limit(limit=1000)
        full_result = run_processing_with_limit(limit=-1)
        ```
    """

    raw_path, processed_path, metadata_path = build_processing_paths(env_file=env_file)
    values = dotenv_values(env_file)
    if limit is not None and limit < -1:
        raise ValueError("limit must be positive, -1, or None.")

    is_sample = limit is not None and limit != -1
    if is_sample:
        if limit <= 0:
            raise ValueError("sample limit must be greater than zero.")
        processed_path = processed_path.with_name(
            values.get("PROCESSED_EMAILS_SAMPLE_FILENAME", DEFAULT_TEST_PROCESSED_FILENAME)
        )
        metadata_path = metadata_path.with_name(
            values.get("PROCESSING_SAMPLE_METADATA_FILENAME", DEFAULT_TEST_METADATA_FILENAME)
        )

    raw = pd.read_parquet(raw_path)
    if is_sample:
        raw = raw.head(limit).copy()

    processed, metadata = process_emails(raw)
    metadata["execution_mode"] = "sample" if is_sample else "full"
    metadata["input_limit"] = limit

    processed_path.parent.mkdir(parents=True, exist_ok=True)
    processed.to_parquet(processed_path, index=False)

    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

    return {
        "raw_path": str(raw_path),
        "processed_output_path": str(processed_path),
        "metadata_output_path": str(metadata_path),
        "input_rows": metadata["input_rows"],
        "output_rows": metadata["output_rows"],
        "removed_promotional_rows": metadata["removed_promotional_rows"],
        "removed_empty_text_rows": metadata["removed_empty_text_rows"],
    }


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for local processing.

    Example:
        ```bash
        python -m src.utils.data_processing --env-file .env
        ```
    """

    parser = argparse.ArgumentParser(description="Clean and enrich the local JMAIL raw dataset.")
    parser.add_argument("--env-file", default=DEFAULT_ENV_FILE, help="Path to .env file.")
    parser.add_argument("--limit", type=int, default=None, help="Optional row limit. Use -1 for full dataset.")
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    result = run_processing_with_limit(env_file=arguments.env_file, limit=arguments.limit)
    print(json.dumps(result, indent=2))
