"""Tests for local data profiling utilities."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import pyarrow as pa
import pyarrow.parquet as pq

from src.utils.data_profiling import profile_parquet


class DataProfilingTestCase(unittest.TestCase):
    def test_profile_parquet_returns_basic_column_metadata(self) -> None:
        with TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "emails.parquet"
            table = pa.table(
                {
                    "id": ["1", "2"],
                    "subject": ["Hello", None],
                    "is_promotional": [False, True],
                }
            )
            pq.write_table(table, path)

            profile = profile_parquet(path)

            self.assertEqual(profile["row_count"], 2)
            self.assertEqual(profile["column_count"], 3)
            subject = next(column for column in profile["columns"] if column["name"] == "subject")
            self.assertEqual(subject["null_count"], 1)
            self.assertEqual(subject["sample_values"], ["Hello"])


if __name__ == "__main__":
    unittest.main()
