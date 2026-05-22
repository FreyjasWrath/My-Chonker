# My Chonker Specification v1

## 1. Scope
This document defines the normative v1 contract for My Chonker artifacts and operations.

## 2. Core Artifacts

### 2.1 Paper
A Paper is an immutable JSON capture from a source.

Required fields:
- `paper_id` (string, UUID)
- `schema_version` (string, e.g. `1.0.0`)
- `created_at` (RFC3339 timestamp)
- `source` (object: `source_id`, `source_type`, `source_uri`)
- `thread_lens` (object)
- `bias_mode` (string enum: `strict`, `balanced`, `broad`)
- `payload` (object)
- `content_hash` (string, sha256 hex)

Optional fields:
- `tags` (array of strings)
- `trace` (object)

Invariants:
- Paper content is immutable after creation.
- `content_hash` must match canonicalized payload+metadata hash.
- No field may imply truth ranking.

### 2.2 Archive
An Archive is a folder of Papers with no semantic merge.

Structure:
- `papers/` directory of JSON files named `<paper_id>.json`
- `index.json` listing paper refs and metadata

Invariants:
- Adding a Paper updates index by append only.
- Existing Paper files are never rewritten.

### 2.3 Container
A Container is an append-only event log of Paper references.

Structure:
- `container.jsonl` with one event per line

Event fields:
- `event_id` (UUID)
- `event_time` (RFC3339)
- `event_type` (`paper_appended`)
- `paper_ref` (path or URI)
- `paper_hash` (sha256)

Invariants:
- Events are append-only and ordered by write position.
- Rebuild from first event must produce same reference set.

## 3. Operations

### 3.1 create_paper(source, lens, bias_mode) -> Paper
Validation:
- `bias_mode` in enum.
- `source` contains stable `source_id`.
Output:
- New immutable Paper JSON.
Failure modes:
- invalid source metadata
- unsupported bias mode
Idempotency:
- Non-idempotent by default (new `paper_id` each invocation).

### 3.2 store_paper(archive_path, paper) -> archive_entry
Validation:
- `paper_id` unique in archive.
Output:
- appended index entry with file path.
Failure modes:
- duplicate paper ID
- schema validation failure
Idempotency:
- Idempotent only when duplicate content + same id is rejected as no-op by policy.

### 3.3 append_container(container, paper_ref) -> container_event
Validation:
- referenced paper exists and hash matches.
Output:
- appended `paper_appended` event.
Failure modes:
- missing paper ref
- hash mismatch
Idempotency:
- Not idempotent; duplicate refs are allowed as distinct events.

### 3.4 query_container(container, lens) -> result_set
Validation:
- lens is syntactically valid.
Output:
- ordered projection of matching event refs.
Failure modes:
- unreadable log
- invalid lens syntax
Idempotency:
- Idempotent for fixed container state and lens.

## 4. Concurrency and Ordering
- Single-writer mode is required for v1 normative behavior.
- Multi-writer support is implementation-defined and must preserve total order.

## 5. Valid vs Invalid Examples
Valid:
- Paper with all required fields and a correct hash.
Invalid:
- Paper missing `paper_id`.
- Container event with non-append rewrite semantics.
