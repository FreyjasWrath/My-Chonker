import copy
import hashlib
import json
import re
import unittest

from src.chonker import CreatePaperError, _canonical_json_bytes, create_paper


class CreatePaperTests(unittest.TestCase):
    def test_create_paper_happy_path(self):
        p = create_paper(
            source={"source_id": "s1", "source_type": "repo", "source_uri": "file:///repo"},
            lens={"path": "README.md"},
            bias_mode="balanced",
            payload={"text": "hello"},
        )
        self.assertIn("paper_id", p)
        self.assertEqual(p["schema_version"], "1.0.0")
        self.assertTrue(p["content_hash"].startswith("sha256:"))
        self.assertEqual(p["bias_mode"], "balanced")
        self.assertRegex(p["created_at"], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

    def test_content_hash_matches_canonical_material(self):
        p = create_paper(
            source={"source_id": "s1", "source_type": "repo", "source_uri": "file:///repo"},
            lens={"path": "README.md"},
            bias_mode="strict",
            payload={"text": "hello"},
            tags=["a"],
            trace={"x": 1},
        )
        material = {k: v for k, v in p.items() if k != "content_hash"}
        expected = "sha256:" + hashlib.sha256(_canonical_json_bytes(material)).hexdigest()
        self.assertEqual(p["content_hash"], expected)

    def test_returns_detached_copy(self):
        source = {"source_id": "s1", "source_type": "repo", "source_uri": "file:///repo"}
        lens = {"path": "README.md"}
        payload = {"text": "hello"}
        p = create_paper(source=source, lens=lens, bias_mode="balanced", payload=payload)
        source["source_id"] = "changed"
        lens["path"] = "CHANGED"
        payload["text"] = "changed"
        self.assertEqual(p["source"]["source_id"], "s1")
        self.assertEqual(p["thread_lens"]["path"], "README.md")
        self.assertEqual(p["payload"]["text"], "hello")

    def test_invalid_bias_mode(self):
        with self.assertRaises(CreatePaperError):
            create_paper(
                source={"source_id": "s1", "source_type": "repo", "source_uri": "file:///repo"},
                lens={},
                bias_mode="aggressive",
            )

    def test_missing_source_field(self):
        with self.assertRaises(CreatePaperError):
            create_paper(source={"source_id": "s1", "source_type": "repo"}, lens={}, bias_mode="strict")

    def test_invalid_tags_type(self):
        with self.assertRaises(CreatePaperError):
            create_paper(
                source={"source_id": "s1", "source_type": "repo", "source_uri": "file:///repo"},
                lens={},
                bias_mode="strict",
                tags=[1],
            )


if __name__ == "__main__":
    unittest.main()
