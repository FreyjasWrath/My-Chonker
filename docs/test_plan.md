# Invariant Test Plan

## Append-only invariants
1. Existing Paper file bytes never change after write.
2. Container only grows by line append.

## Reversibility invariants
3. Reconstructing reference set from `container.jsonl` yields deterministic output.

## Non-collapse invariants
4. Conflicting Papers are both preserved and retrievable.

## Fixtures
- `tests/fixtures/paper_valid.json`
- `tests/fixtures/paper_invalid_missing_id.json`
- `tests/fixtures/container_events.jsonl`

## Expected outcomes
- Valid fixture passes schema.
- Invalid fixture fails schema with missing required property.
- Replay check returns stable ordered references.
