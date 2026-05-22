import json
import tempfile
import unittest
from pathlib import Path

from src.chonker import CreatePaperError, create_paper, store_paper


class StorePaperTests(unittest.TestCase):
    def _paper(self):
        return create_paper(
            source={"source_id": "s1", "source_type": "repo", "source_uri": "file:///repo"},
            lens={"path": "README.md"},
            bias_mode="balanced",
            payload={"text": "hello"},
        )

    def test_store_paper_creates_archive_files(self):
        with tempfile.TemporaryDirectory() as td:
            p = self._paper()
            entry = store_paper(td, p)
            self.assertEqual(entry["paper_id"], p["paper_id"])
            self.assertTrue((Path(td) / "papers" / f"{p['paper_id']}.json").exists())
            self.assertTrue((Path(td) / "index.json").exists())

    def test_store_paper_duplicate_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            p = self._paper()
            store_paper(td, p)
            with self.assertRaises(CreatePaperError):
                store_paper(td, p)

    def test_store_invalid_paper_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(CreatePaperError):
                store_paper(td, {"paper_id": "x"})


if __name__ == "__main__":
    unittest.main()
