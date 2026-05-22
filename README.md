My Chonker

An append-only context stack for lossless aggregation.

Instead of merging meaning, My Chonker stacks context.

It aggregates structured information without asserting truth, authority, interpretation, or canon.


---

Purpose

My Chonker exists to preserve context safely.

Nothing is overwritten.
Nothing is decided.
Nothing is collapsed.

Interpretation is deferred.


---

What This Is

My Chonker is context infrastructure.

It collects and stacks structured context so it can be interpreted later by humans or downstream systems.


---

What This Is Not

My Chonker is not memory.
My Chonker is not truth.
My Chonker is not canon.
My Chonker is not an agent.
My Chonker is not an authority.

It does not evaluate meaning.
It does not resolve conflicts.
It does not assign importance.


---

Core Principles

Append-only
Lossless
Reversible
Non-canonical
Human-authorized interpretation


---

Conceptual Structure (Plain Language)

My Chonker is composed of three core artifacts:

Paper
A single-source JSON capture. Immutable and traceable.

Archive
A folder containing multiple Papers. No merging. No prioritization.

Container
An append-only aggregation of Papers. Preserves all content verbatim.


---

Controls

ThreadLens
A filter defining what to extract, not what matters.

BiasMode
Controls strictness of selection only. Never alters source data.


---

Usage Pattern

Run an autorun instruction in a source.
Receive a Paper JSON.
Store Papers in an Archive.
Aggregate via a Container.
Interpret later.


---

Design Rule

Structure is allowed.
Meaning is deferred.
Authority stays human.


---

License

MIT


---

My Chonker stacks context.
You decide what it means.


## Repository Structure
- `docs/`: normative specifications, NFRs, test plan, versioning, quickstart.
- `schemas/`: JSON Schema contracts for artifacts.
- `examples/`: valid and invalid sample artifacts.
- `tests/fixtures/`: fixtures for invariant-oriented tests.
- `scripts/`: validation helpers.
- `src/`: implementation placeholder modules.

## End-to-End Usage
1. Capture source into a Paper.
2. Store Paper into an Archive index.
3. Append Paper reference into Container log.
4. Validate schemas and fixtures with `python3 scripts/validate_examples.py`.

## Glossary
- ThreadLens: extraction filter for what is selected.
- BiasMode: extraction strictness control (`strict`, `balanced`, `broad`) only.

## FAQ
- Why non-authoritative? Because My Chonker preserves context without ranking truth.
- Can conflicts coexist? Yes. Conflicting context is preserved as parallel artifacts.


## Developer Setup
- Install validator dependency: `make setup`
- Run example validation: `make validate`
- CI runs the same validator on push and pull requests via `.github/workflows/validate-examples.yml`.


## Runtime Status
- Implemented operation 1: `create_paper(source, lens, bias_mode)` in `src/chonker.py`.
- Operation 2 (`store_paper`) is now implemented. Operations 3-4 are still pending runtime implementation.
