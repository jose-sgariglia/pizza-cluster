from __future__ import annotations
from src.utils.constants.preprocessing import (
    KEEP_COLUMNS,
    REDACTION_PATTERNS,
    COMBINED_REDACTION_PATTERN,
    BLACKLIST_DOMAINS,
    EMBEDDING_TEXT_TEMPLATE,
    DISCLAIMER_DELIMITER_RE,
    DISCLAIMER_KEYWORD_ANCHORS,
)

"""Cleaning and rough feature engineering for JMAIL email data.

Example:
    Run the first processing pipeline from the project root:

    ```bash
    python -m src.utils.data_processing
    ```
"""



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
    """Count redaction/censorship markers in the text."""
    if not isinstance(value, str):
        return 0
    return len(COMBINED_REDACTION_PATTERN.findall(value))

def split_body_disclaimer(text: str) -> tuple[str, str | None]:
    """Split email text into body and legal disclaimer using position-aware heuristics.

    Two strategies are tried in order, both with a safe-by-default posture:
    if confidence is low, the original text is returned unchanged.

    Strategy 1: structural delimiter line (e.g. ---) confirmed by a keyword anchor
    in the first 500 chars of the remaining text.
    Strategy 2: keyword anchor found in the last 30% of lines, when no delimiter exists.

    Forward headers (Original Message blocks, reply chains) are out of scope.

    Example:
        ```python
        body, disc = split_body_disclaimer("Hi team\\n---\\nDisclaimer: This email is confidential.")
        ```
    """
    if not isinstance(text, str) or not text.strip():
        return text if isinstance(text, str) else "", None

    lines = text.splitlines()
    n = len(lines)
    if n < 3:
        return text, None

    for i, line in enumerate(lines):
        stripped = line.strip()
        if DISCLAIMER_DELIMITER_RE.match(stripped):
            remaining = "\n".join(lines[i + 1 :])
            if any(anchor.search(remaining[:500]) for anchor in DISCLAIMER_KEYWORD_ANCHORS):
                body = "\n".join(lines[:i]).strip()
                if body:
                    return body, remaining.strip() or None

    threshold = max(0, int(n * 0.70))
    for i in range(threshold, n):
        if any(anchor.search(lines[i]) for anchor in DISCLAIMER_KEYWORD_ANCHORS):
            body = "\n".join(lines[:i]).strip()
            if body:
                return body, "\n".join(lines[i:]).strip() or None

    return text, None


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


def _recipient_field_has_known_value(series: pd.Series) -> pd.Series:
    normalized = series.fillna("").astype(str).str.strip()
    return ~normalized.isin(["", "[]", "Unknown"])


def fill_unknown_recipients(df: pd.DataFrame) -> pd.DataFrame:
    """Mark rows where all recipient fields are missing or empty.

    The raw recipient columns are otherwise preserved. When no recipient is available in
    any field, `to_recipients` is set to `Unknown` as the least ambiguous placeholder.
    """

    result = df.copy()
    recipient_columns = ["to_recipients", "cc_recipients", "bcc_recipients"]
    known_recipient = pd.Series(False, index=result.index)

    for column in recipient_columns:
        if column not in result.columns:
            result[column] = ""
        known_recipient = known_recipient | _recipient_field_has_known_value(result[column])

    result["person_unknown"] = ~known_recipient
    result.loc[result["person_unknown"], "to_recipients"] = "Unknown"
    return result


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

    raw_content = (
        result["content_markdown"].fillna("")
        if "content_markdown" in result.columns
        else pd.Series("", index=result.index)
    )
    split_results = raw_content.map(split_body_disclaimer)
    result["content_clean"] = split_results.map(lambda x: normalize_text(x[0]))
    result["has_disclaimer"] = split_results.map(lambda x: x[1] is not None)

    result["combined_text"] = (
        result["subject_clean"].where(result["subject_clean"] != "", "")
        + "\n\n"
        + result["content_clean"].where(result["content_clean"] != "", "")
    ).str.strip()
    # Mantieni lunghezza combinata come feature utile per modelli
    result["combined_text_length"] = result["combined_text"].str.len().fillna(0).astype("Int64")
    
    # Rilevazione e densità delle redazioni/censure
    result["has_redaction"] = result["subject"].map(has_redaction_marker) | result["content_markdown"].map(
        has_redaction_marker
    )
    result["redaction_count"] = result["subject"].map(count_redaction_markers).fillna(0).astype("Int64") + \
                                result["content_markdown"].map(count_redaction_markers).fillna(0).astype("Int64")
    
    # Redaction ratio: rapporto tra numero di censure e lunghezza testo (densità del segnale di oscuramento)
    result["redaction_ratio"] = (result["redaction_count"] / result["combined_text_length"].where(result["combined_text_length"] > 0)).fillna(0.0)
    
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

# Task 2: Rimossa granularità temporale (anno, mese, ora, weekend) per mantenere solo il timestamp generico
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

    # Conserviamo il conteggio allegati (generico) ma non il flag booleano ridondante
    result["attachment_count"] = attachments.fillna(0).astype("Int64") if attachments is not None else 0
    result = fill_unknown_recipients(result)
    result["recipient_count_estimate"] = estimate_recipient_counts(
        result.get("to_recipients"),
        result.get("cc_recipients"),
        result.get("bcc_recipients"),
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
    row_count: int | None = None,
) -> pd.Series:
    """Estimate recipient counts with vectorized string operations.

    Example:
        ```python
        counts = estimate_recipient_counts(df["to_recipients"], df["cc_recipients"], None)
        ```
    """

    series_values = [series for series in (to_recipients, cc_recipients, bcc_recipients) if series is not None]
    if series_values:
        index = series_values[0].index
    else:
        index = range(row_count or 0)

    counts = pd.Series(0, index=index, dtype="Int64")
    for series in (to_recipients, cc_recipients, bcc_recipients):
        if series is None:
            continue
        series = series.reindex(index)
        normalized = series.fillna("").astype(str).str.strip()
        non_empty = ~normalized.isin(["", "[]"])
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



def apply_embedding_template(df: pd.DataFrame, template: str) -> pd.DataFrame:
    """Apply a structured template to create the final text for embeddings.
    
    Placeholder names in template should match column names.
    """
    result = df.copy()
    
    def format_row(row):
        return template.format(
            date=row.get("sent_at", "Unknown"),
            sender=row.get("sender", "Unknown"),
            recipients=row.get("to_recipients", "Unknown"),
            subject=row.get("subject_clean", "No Subject"),
            body=row.get("content_clean", "No Content")
        )
    
    result["combined_text"] = result.apply(format_row, axis=1)
    result["combined_text_length"] = result["combined_text"].str.len().fillna(0).astype("Int64")
    return result


def process_emails(df: pd.DataFrame, env_values: dict[str, str] | None = None) -> tuple[pd.DataFrame, dict[str, Any]]:
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
    # 1. Pulizia e feature engineering di base
    with_text = add_text_features(filtered)
    with_time = add_temporal_features(with_text)
    enriched = add_metadata_features(with_time)
    
    # 2. Applicazione template strutturato (Task 3)
    template = (env_values or {}).get("EMBEDDING_TEXT_TEMPLATE", EMBEDDING_TEXT_TEMPLATE)
    # Gestione escape per newline se caricato da .env
    template = template.replace("\\n", "\n") 
    
    templated = apply_embedding_template(enriched, template)
    
    # 3. Pulizia finale righe vuote
    processed = remove_empty_text_rows(templated)

    metadata = {
        "processed_at_utc": datetime.now(UTC).isoformat(),
        "input_rows": input_rows,
        "selected_rows": selected_rows,
        "after_promotional_filter_rows": after_promotional_filter,
        "output_rows": len(processed),
        "removed_promotional_rows": selected_rows - after_promotional_filter,
        "removed_empty_text_rows": after_promotional_filter - len(processed),
        "output_columns": list(processed.columns),
        "redaction_policy": "Redaction markers including [redacted] are detected in has_redaction but text spans are preserved.",
        "recipient_unknown_policy": "Rows without usable recipient fields are marked with person_unknown and to_recipients=Unknown.",
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

    processed, metadata = process_emails(raw, env_values=values)
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