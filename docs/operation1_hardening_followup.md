# Operation 1 Hardening Follow-up (Issue/PR Draft)

## Title
Operation 1 hardening: schema strictness, resilience, and edge-case coverage

## Context
`create_paper(source, lens, bias_mode) -> Paper` is functional and test-backed, but we want a short hardening pass before declaring operation 1 production-complete.

## Scope (5 items)

1. **Cache schemas in memory**
   - Avoid re-reading schema files on every call.
   - Add lazy-load cache with explicit reload option for tests.

2. **Tighten schema constraints**
   - `paper_id`: enforce UUID format.
   - `content_hash`: enforce `^sha256:[0-9a-f]{64}$`.
   - `source_uri`: enforce URI format.

3. **Add missing edge-case tests**
   - Blank/whitespace source values.
   - Non-object `lens`/`payload`/`trace`.
   - Unicode stability in canonical hashing.
   - Timestamp parseability and format consistency.

4. **Harden schema load failure paths**
   - Clear typed errors for missing/corrupt schema files.
   - Ensure `CreatePaperError` wraps actionable context.

5. **Clarify immutability semantics in docs**
   - Document that returned dict is detached copy but still mutable by caller unless frozen externally.

## Acceptance criteria
- Unit tests added for all new edge cases and failure paths.
- `create_paper` no longer performs per-call disk reads for schema loading.
- Schema files updated and validator/tests pass.
- README/spec note updated to clarify immutability semantics.

## Out of scope
- Operations 2-4 behavior changes.
- Archive/container schema redesign beyond required strictness improvements.
