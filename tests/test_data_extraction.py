"""Tests for JMAIL data extraction utilities."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import pyarrow as pa
import pyarrow.parquet as pq

from src.utils.data_extraction import _safe_int, extract_sample_from_local_parquet


class DataExtractionTestCase(unittest.TestCase):
    def test_safe_int_handles_valid_and_invalid_values(self) -> None:
        self.assertEqual(_safe_int("42"), 42)
        self.assertIsNone(_safe_int(None))
        self.assertIsNone(_safe_int("not-a-number"))

    def test_extract_sample_from_local_parquet(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            source = root / "source.parquet"
            output = root / "sample.parquet"
            table = pa.table(
                {
                    "id": ["a", "b", "c"],
                    "subject": ["one", "two", "three"],
                }
            )
            pq.write_table(table, source)

            result = extract_sample_from_local_parquet(source, output, limit=2)

            sampled = pq.read_table(result)
            self.assertEqual(result, output)
            self.assertEqual(sampled.num_rows, 2)
            self.assertEqual(sampled.column_names, ["id", "subject"])


if __name__ == "__main__":
    unittest.main()
