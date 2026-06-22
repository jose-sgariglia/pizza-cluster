"""Tests for cleaning and rough feature engineering."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd

from src.utils.data_processing import (
    add_text_features,
    add_thread_features,
    apply_embedding_template,
    build_processing_paths,
    estimate_recipient_count,
    estimate_recipient_counts,
    fill_unknown_recipients,
    filter_promotional_emails,
    has_redaction_marker,
    normalize_text,
    process_emails,
    run_processing_with_limit,
    split_body_disclaimer,
    split_body_thread,
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
        self.assertIn("redaction_ratio", processed.columns)
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


class DisclaimerSplitTestCase(unittest.TestCase):
    def test_split_detects_structural_delimiter_with_keyword_confirmation(self) -> None:
        text = "Hello team.\nPlease see the attached report.\n---\nDisclaimer: This email is confidential."
        body, disclaimer = split_body_disclaimer(text)
        self.assertEqual(body, "Hello team.\nPlease see the attached report.")
        self.assertIsNotNone(disclaimer)
        self.assertIn("Disclaimer", disclaimer)

    def test_split_ignores_delimiter_without_keyword_confirmation(self) -> None:
        text = "Hello team.\n---\nBest regards,\nJohn Smith"
        body, disclaimer = split_body_disclaimer(text)
        self.assertEqual(body, text)
        self.assertIsNone(disclaimer)

    def test_split_detects_keyword_anchor_in_last_30_percent(self) -> None:
        lines = ["Line one.", "Line two.", "Line three.", "Line four.", "Line five."]
        footer = "This e-mail is intended only for the use of the individual to whom it is addressed."
        text = "\n".join(lines) + "\n" + footer
        body, disclaimer = split_body_disclaimer(text)
        self.assertEqual(body, "\n".join(lines))
        self.assertIsNotNone(disclaimer)

    def test_split_does_not_trigger_keyword_in_first_70_percent(self) -> None:
        # keyword in line 0 of a 10-line email — well above the 30% threshold
        lines = ["Privileged and Confidential — Project Alpha"] + [f"Line {i}." for i in range(9)]
        text = "\n".join(lines)
        body, disclaimer = split_body_disclaimer(text)
        self.assertEqual(body, text)
        self.assertIsNone(disclaimer)

    def test_split_returns_original_when_no_disclaimer_found(self) -> None:
        text = "Hi, just wanted to follow up on the meeting.\nThanks,\nAlice"
        body, disclaimer = split_body_disclaimer(text)
        self.assertEqual(body, text)
        self.assertIsNone(disclaimer)

    def test_split_safe_when_body_would_be_empty_after_delimiter(self) -> None:
        # delimiter is the first line — resulting body would be empty, must NOT strip
        text = "---\nDisclaimer: This email is confidential.\nPlease delete if received in error."
        body, disclaimer = split_body_disclaimer(text)
        # Strategy 1: body before delimiter would be "" → falls through
        # Strategy 2: keyword at line 1 → body = "---" (truthy) → splits
        # Both are acceptable; what matters is original content is not lost
        self.assertNotEqual(body, "")

    def test_split_returns_original_for_non_string_input(self) -> None:
        body, disclaimer = split_body_disclaimer(None)  # type: ignore[arg-type]
        self.assertEqual(body, "")
        self.assertIsNone(disclaimer)

    def test_split_returns_original_for_short_text(self) -> None:
        text = "---\nDisclaimer: This email is privileged and confidential."
        body, disclaimer = split_body_disclaimer(text)
        # Only 2 lines — n < 3 guard returns unchanged
        self.assertEqual(body, text)
        self.assertIsNone(disclaimer)

    def test_add_text_features_adds_has_disclaimer_column(self) -> None:
        df = pd.DataFrame({
            "subject": ["Re: meeting"],
            "content_markdown": [
                "Hi,\nSee you tomorrow.\nBest,\nBob\n---\nDisclaimer: This e-mail is confidential."
            ],
        })
        result = add_text_features(df)
        self.assertIn("has_disclaimer", result.columns)
        self.assertTrue(result.loc[0, "has_disclaimer"])

    def test_add_text_features_false_when_no_disclaimer(self) -> None:
        df = pd.DataFrame({
            "subject": ["Hello"],
            "content_markdown": ["Just a normal email body with no footer."],
        })
        result = add_text_features(df)
        self.assertFalse(result.loc[0, "has_disclaimer"])


class ThreadSplitTestCase(unittest.TestCase):
    """Tests for split_body_thread() and add_thread_features().

    Examples are taken verbatim from thread_pattern_census.md and
    thread_validation.md to exercise real-world data instead of clean
    synthetic fixtures.
    """

    # ── 1. ON_DATE_WROTE ──────────────────────────────────────────────────────

    def test_split_on_date_wrote_single_line(self) -> None:
        # Verbatim pattern from validation Esempio 1
        body = (
            "Hi Lesley,\n\n"
            "On Aug 17, 2011, at 1:34 PM, Feierstein, Kimberly wrote:\n\n"
            "> Glenn just said he can do 4:00 NY time. Let me know if that works."
        )
        new, quoted, has_thread, is_short = split_body_thread(body)
        self.assertTrue(has_thread)
        self.assertEqual(new.strip(), "Hi Lesley,")
        self.assertIsNotNone(quoted)
        self.assertIn("Feierstein", quoted)
        self.assertTrue(is_short)  # "Hi Lesley," is 10 chars < 20

    def test_split_on_date_wrote_month_name(self) -> None:
        body = (
            "i'll try\n\n"
            "On Jan 12, 2019, at 10:11 AM, Nili Priell <nili@example.com> wrote:\n\n"
            "> Hi Lesley,"
        )
        new, quoted, has_thread, is_short = split_body_thread(body)
        self.assertTrue(has_thread)
        self.assertEqual(new.strip(), "i'll try")
        self.assertIn("Nili Priell", quoted)

    # ── 2. OUTLOOK_HEADER_BLOCK ───────────────────────────────────────────────

    def test_split_outlook_header_block(self) -> None:
        # From validation Esempio 1 — Outlook block separate from chevron lines
        body = (
            "Perfect....sorry one little call took so much planning for!!!\n\n"
            "From: Lesley Groff [mailto:lesley@nysgllc.com]\n"
            "Sent: Wednesday, August 17, 2011 1:48 PM\n"
            "To: Feierstein, Kimberly\n"
            "Subject: Re: Jeffrey Epstein\n\n"
            "HI again! Jeffrey will call Glenn through the office at 4pm today."
        )
        new, quoted, has_thread, is_short = split_body_thread(body)
        self.assertTrue(has_thread)
        self.assertIn("Perfect", new)
        self.assertNotIn("From:", new)
        self.assertIn("From: Lesley Groff", quoted)
        self.assertFalse(is_short)

    def test_split_outlook_header_date_variant(self) -> None:
        # "Date:" instead of "Sent:" (Gmail forward inline style)
        body = (
            "FYI.\n\n"
            "From: Jeffrey Epstein <jeevacation@gmail.com>\n"
            "Date: Tue, 5 Mar 2013 09:41:06 -0400\n"
            "To: recipient@example.com\n"
            "Subject: Re: meeting\n\n"
            "Content of forwarded email."
        )
        new, quoted, has_thread, is_short = split_body_thread(body)
        self.assertTrue(has_thread)
        self.assertEqual(new.strip(), "FYI.")
        self.assertIn("Jeffrey Epstein", quoted)

    # ── 3. CHEVRON_QUOTE ──────────────────────────────────────────────────────

    def test_split_chevron_quote(self) -> None:
        # From census example 1 (validation STEP 1)
        body = (
            "ok, I also just sent JE an email asking if 2pm would be ok.\n\n"
            "> Glenn just said he can do 4:00 NY time. Let me know if that works.\n"
            ">\n"
            "> -----Original Message-----"
        )
        new, quoted, has_thread, is_short = split_body_thread(body)
        self.assertTrue(has_thread)
        self.assertIn("2pm", new)
        self.assertNotIn(">", new)
        self.assertTrue(quoted.startswith(">"))

    # ── 4. BEGIN_FORWARDED ────────────────────────────────────────────────────

    def test_split_begin_forwarded(self) -> None:
        # From validation Esempio 2
        body = (
            "FYI — see below.\n\n"
            "Begin forwarded message:\n\n"
            "From: Stephen Hanson <s.hanson@example.com>\n"
            "Date: March 12, 2018 at 5:09:06 PM EDT\n"
            "Subject: Re: Life Hotel - Rosenthal Note\n\n"
            "Punch line is that 50k loan does not help."
        )
        new, quoted, has_thread, is_short = split_body_thread(body)
        self.assertTrue(has_thread)
        self.assertEqual(new.strip(), "FYI — see below.")
        self.assertIn("Begin forwarded message", quoted)

    # ── 5. ORIGINAL_MSG_DASHES ────────────────────────────────────────────────

    def test_split_original_msg_dashes(self) -> None:
        # Standard five-dash variant from census
        body = (
            "I'll try.\n\n"
            "-----Original Message-----\n"
            "From: Cecilia Steen <cecilia.steen@gmail.com>\n"
            "Sent: Wednesday, August 8, 2007 5:35 PM\n"
            "To: J. Epstein\n\n"
            "Dear Jeffrey, it would be great if you could come."
        )
        new, quoted, has_thread, is_short = split_body_thread(body)
        self.assertTrue(has_thread)
        self.assertEqual(new.strip(), "I'll try.")
        self.assertIn("-----Original Message-----", quoted)

    # ── 6. FORWARDED_DASHES ───────────────────────────────────────────────────

    def test_split_forwarded_dashes(self) -> None:
        # From census verbatim: "------- Forwarded message -------"
        body = (
            "Sharing this with you.\n\n"
            "------- Forwarded message -------\n"
            "From: sender@example.com\n"
            "Date: Mon, 15 Jan 2007\n\n"
            "The original content goes here."
        )
        new, quoted, has_thread, is_short = split_body_thread(body)
        self.assertTrue(has_thread)
        self.assertEqual(new.strip(), "Sharing this with you.")
        self.assertIn("Forwarded message", quoted)

    # ── 7. FWD_BY_LINE ────────────────────────────────────────────────────────

    def test_split_fwd_by_line(self) -> None:
        # Verbatim from census: real Kirkland-Ellis forward header
        body = (
            "Please review.\n\n"
            "----- Forwarded by Ami Sheth/New York/Kirkland-Ellis on 08/21/2008 11:27 AM -----\n\n"
            "From: Some Sender\n"
            "Sent: Thu, 21 Aug 2008 09:00:00\n\n"
            "Content of the forwarded email."
        )
        new, quoted, has_thread, is_short = split_body_thread(body)
        self.assertTrue(has_thread)
        self.assertEqual(new.strip(), "Please review.")
        self.assertIn("Forwarded by Ami Sheth", quoted)

    # ── 8. Nested markers — content_quoted preserves everything ───────────────

    def test_split_nested_markers_all_preserved_in_quoted(self) -> None:
        # Real chain from validation Esempio 1 (truncated for test clarity)
        body = (
            "Perfect.\n\n"
            "On Aug 17, 2011, at 1:34 PM, Kimberly wrote:\n\n"
            "> Glenn can do 4pm.\n"
            ">\n"
            "> -----Original Message-----\n"
            "> From: Lesley Groff\n"
            "> Sent: Wed Aug 17, 2011 1:34 PM\n"
            "> To: Kimberly\n"
            ">\n"
            "> ok, let me check JE's schedule.\n"
            ">\n"
            "> On Aug 17, 2011, at 1:27 PM, Kimberly wrote:\n"
            ">> Ok, how is 2:00 NY time?"
        )
        new, quoted, has_thread, is_short = split_body_thread(body)
        self.assertTrue(has_thread)
        self.assertEqual(new.strip(), "Perfect.")
        # All nested markers must be verbatim inside content_quoted
        self.assertIn("-----Original Message-----", quoted)
        self.assertIn(">> Ok, how is 2:00", quoted)
        self.assertIn("On Aug 17, 2011, at 1:27 PM", quoted)

    # ── 9. No marker — body returned unchanged ────────────────────────────────

    def test_split_no_marker_returns_body_unchanged(self) -> None:
        # Short email with no thread markers from pipeline_processing.ipynb row 0
        body = "prefer OUR COUNTRY , MY LIFE or MOMENTS"
        new, quoted, has_thread, is_short = split_body_thread(body)
        self.assertFalse(has_thread)
        self.assertEqual(new, body)
        self.assertIsNone(quoted)
        self.assertFalse(is_short)

    # ── 10. OCR-corrupted dashes (BROKEN_SEP from census) ────────────────────

    def test_split_ocr_corrupted_dashes_two_left(self) -> None:
        # "---Original Message-----" — 3 dashes left, 5 right (from BROKEN_SEP)
        body = (
            "ok super...now just let me know the time.\n\n"
            "---Original Message-----\n"
            "From: Lesley Groff [mailto:lesley@nysgllc.com]\n"
            "Sent: Wednesday, August 17, 2011 12:45 PM\n\n"
            "Hi, see if JE is available."
        )
        new, quoted, has_thread, is_short = split_body_thread(body)
        self.assertTrue(has_thread)
        self.assertIn("ok super", new)
        self.assertIn("Original Message", quoted)

    # ── 11. content_new_is_short flag ─────────────────────────────────────────

    def test_split_short_reply_sets_is_short_flag(self) -> None:
        body = "ok.\n\nOn Jan 1, 2020, Alice wrote:\n\n> Yes, let's meet."
        new, quoted, has_thread, is_short = split_body_thread(body)
        self.assertTrue(has_thread)
        self.assertTrue(is_short)          # "ok." is 3 chars < 20
        self.assertEqual(new.strip(), "ok.")
        self.assertIsNotNone(quoted)       # short does NOT prevent the split

    def test_split_is_short_false_for_long_content_new(self) -> None:
        body = (
            "This is a longer reply that definitely exceeds twenty characters.\n\n"
            "On Jan 1, 2020, Alice wrote:\n> Yes."
        )
        _, _, has_thread, is_short = split_body_thread(body)
        self.assertTrue(has_thread)
        self.assertFalse(is_short)

    # ── 12. add_thread_features ───────────────────────────────────────────────

    def test_add_thread_features_populates_all_columns(self) -> None:
        df = pd.DataFrame({
            "content_clean": [
                "Hi!\n\nOn Jan 1, 2020, Alice wrote:\n> Yes.",
                "No quotes here at all.",
                "",
            ]
        })
        result = add_thread_features(df)
        for col in ("content_new", "content_quoted", "has_thread", "content_new_is_short"):
            self.assertIn(col, result.columns)
        self.assertTrue(result.loc[0, "has_thread"])
        self.assertFalse(result.loc[1, "has_thread"])
        # pandas stores None as NaN in object Series
        self.assertTrue(pd.isna(result.loc[1, "content_quoted"]) or result.loc[1, "content_quoted"] is None)
        self.assertFalse(result.loc[2, "has_thread"])

    def test_add_thread_features_uses_content_markdown_primary(self) -> None:
        # content_markdown is the primary source (raw, preserves newlines for ^ anchors)
        df = pd.DataFrame({
            "content_markdown": [
                "reply\n\n-----Original Message-----\nFrom: A\nSent: Mon\nTo: B\nBody."
            ]
        })
        result = add_thread_features(df)
        self.assertTrue(result.loc[0, "has_thread"])
        self.assertEqual(result.loc[0, "content_new"].strip(), "reply")

    def test_add_thread_features_prefers_content_markdown_over_clean(self) -> None:
        # When both columns are present, content_markdown wins (it has newlines).
        # content_clean is whitespace-collapsed and would miss most markers.
        df = pd.DataFrame({
            "content_markdown": ["reply\n\n> Quoted line from original."],
            "content_clean": ["cleaned text no markers"],
        })
        result = add_thread_features(df)
        # content_markdown has a chevron marker → must detect thread
        self.assertTrue(result.loc[0, "has_thread"])
        self.assertEqual(result.loc[0, "content_new"].strip(), "reply")

    def test_add_thread_features_regression_normalize_text_bug(self) -> None:
        # Regression: before the fix, add_thread_features used content_clean which
        # went through normalize_text() → " ".join(value.split()), collapsing all
        # newlines. MULTILINE ^ anchors then only matched at position 0, destroying
        # 96.5% of thread signals (see reports/thread_discrepancy_analysis.md).
        # After the fix, content_markdown (raw) is used and must detect the marker.
        raw = "Hi.\n\nOn Jan 1, 2020, Alice wrote:\n> yes."
        normalized = " ".join(raw.split())  # simulates old normalize_text behaviour

        # The parser must succeed on raw
        _, _, has_thread_raw, _ = split_body_thread(raw)
        self.assertTrue(has_thread_raw, "split_body_thread must detect thread on raw text")

        # The parser must fail on whitespace-collapsed text (documents the old bug)
        _, _, has_thread_norm, _ = split_body_thread(normalized)
        self.assertFalse(has_thread_norm, "normalized text should NOT match (no newlines for ^ anchors)")

        # add_thread_features must use raw and succeed
        df = pd.DataFrame({"content_markdown": [raw], "content_clean": [normalized]})
        result = add_thread_features(df)
        self.assertTrue(result.loc[0, "has_thread"],
                        "add_thread_features must use content_markdown, not content_clean")


class ApplyEmbeddingTemplateTestCase(unittest.TestCase):
    """Tests for the thread-aware apply_embedding_template()."""

    _TEMPLATE = (
        "DATE: {date}\nFROM: {sender}\nTO: {recipients}\nSUBJECT: {subject}"
        "\n\nBODY:\n{body}{thread_section}"
    )

    def _make_df(self, **kwargs) -> pd.DataFrame:
        defaults = {
            "sent_at": "2020-01-01T00:00:00Z",
            "sender": "a@example.com",
            "to_recipients": "b@example.com",
            "subject_clean": "Hello",
            "content_clean": "Full body text.",
            "content_new": "",
            "content_quoted": None,
            "has_thread": False,
        }
        defaults.update(kwargs)
        return pd.DataFrame([defaults])

    def test_no_thread_uses_content_clean(self) -> None:
        df = self._make_df(has_thread=False, content_clean="Full body.", content_new="")
        result = apply_embedding_template(df, self._TEMPLATE)
        combined = result.loc[0, "combined_text"]
        self.assertIn("Full body.", combined)
        self.assertNotIn("THREAD:", combined)

    def test_thread_uses_content_new_as_body(self) -> None:
        df = self._make_df(
            has_thread=True,
            content_new="Short reply.",
            content_quoted="> Previous message.",
            content_clean="Short reply. > Previous message.",
        )
        result = apply_embedding_template(df, self._TEMPLATE)
        combined = result.loc[0, "combined_text"]
        self.assertIn("Short reply.", combined)
        # content_clean (flat full text) must NOT appear verbatim
        self.assertNotIn("Short reply. > Previous message.", combined)

    def test_thread_appends_thread_section(self) -> None:
        df = self._make_df(
            has_thread=True,
            content_new="Short reply.",
            content_quoted="> Previous message.",
            content_clean="Short reply. > Previous message.",
        )
        result = apply_embedding_template(df, self._TEMPLATE)
        combined = result.loc[0, "combined_text"]
        self.assertIn("THREAD:", combined)
        self.assertIn("> Previous message.", combined)

    def test_empty_content_new_falls_back_to_content_clean(self) -> None:
        df = self._make_df(
            has_thread=True,
            content_new="",
            content_quoted="> Something.",
            content_clean="Full body including thread.",
        )
        result = apply_embedding_template(df, self._TEMPLATE)
        combined = result.loc[0, "combined_text"]
        self.assertIn("Full body including thread.", combined)

    def test_combined_text_length_is_updated(self) -> None:
        df = self._make_df(has_thread=False, content_clean="Hello.")
        result = apply_embedding_template(df, self._TEMPLATE)
        self.assertGreater(int(result.loc[0, "combined_text_length"]), 0)


if __name__ == "__main__":
    unittest.main()
