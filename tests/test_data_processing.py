"""Tests for cleaning and rough feature engineering."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd

from src.utils.data_processing import (
    add_text_features,
    build_processing_paths,
    estimate_recipient_count,
    estimate_recipient_counts,
    fill_unknown_recipients,
    filter_promotional_emails,
    has_redaction_marker,
    normalize_text,
    process_emails,
    run_processing_with_limit,
)


class DataProcessingTestCase(unittest.TestCase):
    def test_normalize_text_preserves_redaction_words(self) -> None:
        self.assertEqual(normalize_text("  Hello\n [REDACTED]   world "), "Hello [REDACTED] world")

    def test_has_redaction_marker_detects_without_mutating_text(self) -> None:
        text = "This line contains [REDACTED] content"
        self.assertTrue(has_redaction_marker(text))
        self.assertEqual(text, "This line contains [REDACTED] content")

    def test_has_redaction_marker_detects_lowercase_bracket_marker(self) -> None:
        self.assertTrue(has_redaction_marker("Recipient: [redacted]"))

    def test_count_redaction_markers_counts_correctly(self) -> None:
        from src.utils.data_processing import count_redaction_markers
        self.assertEqual(count_redaction_markers("Here is a [REDACTED] and another [SEALED]"), 2)
        self.assertEqual(count_redaction_markers("Recipient: [redacted]"), 1)
        self.assertEqual(count_redaction_markers("Clean text"), 0)
        self.assertEqual(count_redaction_markers(None), 0)

    def test_estimate_recipient_count_deduplicates_basic_recipients(self) -> None:
        count = estimate_recipient_count("A@example.com, b@example.com", "a@example.com; c@example.com", None)
        self.assertEqual(count, 3)

    def test_estimate_recipient_counts_vectorized(self) -> None:
        counts = estimate_recipient_counts(
            pd.Series(["a@example.com, b@example.com", ""]),
            pd.Series(["c@example.com", None]),
            None,
            row_count=2,
        )
        self.assertEqual(counts.tolist(), [3, 0])

    def test_estimate_recipient_counts_preserves_filtered_index(self) -> None:
        counts = estimate_recipient_counts(
            pd.Series(["a@example.com", "b@example.com"], index=[2, 6]),
            pd.Series(["[]", "[]"], index=[2, 6]),
            pd.Series([None, "[]"], index=[2, 6]),
        )
        self.assertEqual(counts.index.tolist(), [2, 6])
        self.assertEqual(counts.tolist(), [1, 1])
        self.assertFalse(counts.isna().any())

    def test_fill_unknown_recipients_marks_rows_without_any_recipient(self) -> None:
        df = pd.DataFrame(
            {
                "to_recipients": ["[]", "[\"a@example.com\"]"],
                "cc_recipients": ["[]", "[]"],
                "bcc_recipients": [None, "[]"],
            }
        )
        result = fill_unknown_recipients(df)
        self.assertEqual(result.loc[0, "to_recipients"], "Unknown")
        self.assertTrue(result.loc[0, "person_unknown"])
        self.assertEqual(result.loc[1, "to_recipients"], "[\"a@example.com\"]")
        self.assertFalse(result.loc[1, "person_unknown"])

    def test_filter_promotional_emails_keeps_null_status(self) -> None:
        df = pd.DataFrame({"id": [1, 2, 3], "is_promotional": [True, False, None]})
        result = filter_promotional_emails(df)
        self.assertEqual(result["id"].tolist(), [2, 3])

    def test_add_text_features_preserves_redacted_content(self) -> None:
        df = pd.DataFrame({"subject": ["Notice"], "content_markdown": ["A [REDACTED] value"]})
        result = add_text_features(df)
        self.assertEqual(result.loc[0, "content_clean"], "A [REDACTED] value")
        self.assertTrue(result.loc[0, "has_redaction"])

    def test_process_emails_adds_expected_features(self) -> None:
        df = pd.DataFrame(
            {
                "id": ["1", "2"],
                "doc_id": ["d1", "d2"],
                "message_index": [0, 1],
                "sender": ["sender@example.com", ""],
                "subject": ["Hello", None],
                "to_recipients": ["a@example.com, b@example.com", "c@example.com"],
                "cc_recipients": ["", ""],
                "bcc_recipients": ["", ""],
                "sent_at": ["2020-01-02T03:04:05Z", None],
                "content_markdown": ["Body", ""],
                "attachments": [1, 0],
                "email_drop_id": ["drop", "drop"],
                "is_promotional": [False, True],
                "release_batch": [1, 1],
                "epstein_is_sender": [False, None],
                "all_participants": ["sender@example.com,a@example.com", "c@example.com"],
            }
        )

        processed, metadata = process_emails(df)

        self.assertEqual(len(processed), 1)
        self.assertIn("combined_text", processed.columns)
        self.assertIn("recipient_count_estimate", processed.columns)
        self.assertIn("redaction_count", processed.columns)
        self.assertIn("sent_hour", processed.columns)
        self.assertIn("is_weekend", processed.columns)
        self.assertIn("sender_domain", processed.columns)
        self.assertIn("is_epstein_involved", processed.columns)
        self.assertIn("attachment_count", processed.columns)
        self.assertIn("person_unknown", processed.columns)
        self.assertFalse(processed["recipient_count_estimate"].isna().any())
        self.assertEqual(metadata["removed_promotional_rows"], 1)

    def test_run_processing_with_limit_rejects_invalid_negative_limit(self) -> None:
        with self.assertRaises(ValueError):
            run_processing_with_limit(limit=-2)

    def test_build_processing_paths_resolves_relative_paths_from_env_file(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            env_file = root / ".env"
            env_file.write_text(
                "\n".join(
                    [
                        "DATA_RAW_PATH=data/raw/",
                        "DATA_PROCESSED_PATH=data/processed/",
                        "METADATA_PATH=data/metadata/",
                        "RAW_EMAILS_FILENAME=custom_raw.parquet",
                        "PROCESSED_EMAILS_FILENAME=custom_processed.parquet",
                        "PROCESSING_METADATA_FILENAME=custom_metadata.json",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            raw_path, processed_path, metadata_path = build_processing_paths(env_file=env_file)

            self.assertEqual(raw_path, root / "data" / "raw" / "custom_raw.parquet")
            self.assertEqual(processed_path, root / "data" / "processed" / "custom_processed.parquet")
            self.assertEqual(metadata_path, root / "data" / "metadata" / "custom_metadata.json")


if __name__ == "__main__":
    unittest.main()
