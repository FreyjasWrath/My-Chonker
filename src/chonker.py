#!/usr/bin/env python3
"""My Chonker core runtime (v1): operation 1 implementation.

Implements:
- create_paper(source, lens, bias_mode) -> Paper
"""

from __future__ import annotations

import copy
import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from jsonschema import ValidationError, validate

BIAS_MODES = {"strict", "balanced", "broad"}
SCHEMA_VERSION = "1.0.0"
PAPER_SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas/paper.schema.json"


class CreatePaperError(ValueError):
    """Raised when create_paper receives invalid inputs."""


def _canonical_json_bytes(obj: Dict[str, Any]) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _now_rfc3339() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _load_paper_schema() -> Dict[str, Any]:
    return json.loads(PAPER_SCHEMA_PATH.read_text(encoding="utf-8"))


def _validate_source(source: Dict[str, Any]) -> None:
    if not isinstance(source, dict):
        raise CreatePaperError("source must be an object")
    required = ("source_id", "source_type", "source_uri")
    for key in required:
        val = source.get(key)
        if not isinstance(val, str) or not val.strip():
            raise CreatePaperError(f"source.{key} must be a non-empty string")


def _validate_lens(lens: Dict[str, Any]) -> None:
    if not isinstance(lens, dict):
        raise CreatePaperError("lens must be an object")


def _validate_bias_mode(bias_mode: str) -> None:
    if bias_mode not in BIAS_MODES:
        raise CreatePaperError(f"unsupported bias_mode '{bias_mode}', expected one of {sorted(BIAS_MODES)}")


def _compute_content_hash(paper_without_hash: Dict[str, Any]) -> str:
    digest = hashlib.sha256(_canonical_json_bytes(paper_without_hash)).hexdigest()
    return f"sha256:{digest}"


def create_paper(
    source: Dict[str, Any],
    lens: Dict[str, Any],
    bias_mode: str,
    payload: Dict[str, Any] | None = None,
    tags: list[str] | None = None,
    trace: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """Create an immutable Paper record and validate against v1 schema."""
    _validate_source(source)
    _validate_lens(lens)
    _validate_bias_mode(bias_mode)

    payload_obj: Dict[str, Any] = copy.deepcopy(payload if payload is not None else {})
    if not isinstance(payload_obj, dict):
        raise CreatePaperError("payload must be an object when provided")

    source_obj = copy.deepcopy(source)
    lens_obj = copy.deepcopy(lens)

    paper: Dict[str, Any] = {
        "paper_id": str(uuid.uuid4()),
        "schema_version": SCHEMA_VERSION,
        "created_at": _now_rfc3339(),
        "source": source_obj,
        "thread_lens": lens_obj,
        "bias_mode": bias_mode,
        "payload": payload_obj,
    }

    if tags is not None:
        if not isinstance(tags, list) or any(not isinstance(t, str) for t in tags):
            raise CreatePaperError("tags must be an array of strings")
        paper["tags"] = copy.deepcopy(tags)
    if trace is not None:
        if not isinstance(trace, dict):
            raise CreatePaperError("trace must be an object")
        paper["trace"] = copy.deepcopy(trace)

    paper["content_hash"] = _compute_content_hash(paper)

    schema = _load_paper_schema()
    try:
        validate(paper, schema)
    except ValidationError as exc:
        raise CreatePaperError(f"generated paper failed schema validation: {exc.message}") from exc

    return copy.deepcopy(paper)


ARCHIVE_SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas/archive.schema.json"


def _load_archive_schema() -> Dict[str, Any]:
    return json.loads(ARCHIVE_SCHEMA_PATH.read_text(encoding="utf-8"))


def _validate_paper_with_schema(paper: Dict[str, Any]) -> None:
    schema = _load_paper_schema()
    validate(paper, schema)


def _utc_now() -> str:
    return _now_rfc3339()


def store_paper(archive_path: str, paper: Dict[str, Any]) -> Dict[str, Any]:
    """Store a Paper in archive and append index entry.

    - Writes paper to <archive>/papers/<paper_id>.json
    - Appends metadata entry to <archive>/index.json
    """
    if not isinstance(archive_path, str) or not archive_path.strip():
        raise CreatePaperError("archive_path must be a non-empty string")
    if not isinstance(paper, dict):
        raise CreatePaperError("paper must be an object")

    try:
        _validate_paper_with_schema(paper)
    except ValidationError as exc:
        raise CreatePaperError(f"paper failed schema validation: {exc.message}") from exc

    pid = paper.get("paper_id")
    if not isinstance(pid, str) or not pid.strip():
        raise CreatePaperError("paper.paper_id must be a non-empty string")

    archive_dir = Path(archive_path)
    papers_dir = archive_dir / "papers"
    index_path = archive_dir / "index.json"
    papers_dir.mkdir(parents=True, exist_ok=True)

    paper_path = papers_dir / f"{pid}.json"
    if paper_path.exists():
        raise CreatePaperError(f"duplicate paper ID '{pid}' in archive")

    if index_path.exists():
        try:
            index = json.loads(index_path.read_text(encoding="utf-8"))
        except Exception as exc:
            raise CreatePaperError(f"invalid archive index file: {exc}") from exc
    else:
        index = {"archive_id": f"archive-{uuid.uuid4()}", "papers": []}

    if not isinstance(index, dict) or not isinstance(index.get("papers"), list):
        raise CreatePaperError("archive index must be an object with array field 'papers'")

    for entry in index["papers"]:
        if isinstance(entry, dict) and entry.get("paper_id") == pid:
            raise CreatePaperError(f"duplicate paper ID '{pid}' in archive index")

    index_entry = {
        "paper_id": pid,
        "path": f"papers/{pid}.json",
        "created_at": _utc_now(),
    }

    candidate = copy.deepcopy(index)
    candidate["papers"].append(index_entry)

    try:
        validate(candidate, _load_archive_schema())
    except ValidationError as exc:
        raise CreatePaperError(f"archive index failed schema validation: {exc.message}") from exc

    paper_path.write_text(json.dumps(paper, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    index_path.write_text(json.dumps(candidate, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return copy.deepcopy(index_entry)
