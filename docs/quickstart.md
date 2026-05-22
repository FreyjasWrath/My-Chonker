# Quickstart

1. Create a Paper JSON matching `schemas/paper.schema.json`.
2. Store it in an Archive folder and append metadata to `examples/archives/index.json` style index.
3. Append a `paper_appended` event to container JSONL.
4. Install development dependency:

```bash
python3 -m pip install -r requirements-dev.txt
```

5. Validate examples:

```bash
python3 scripts/validate_examples.py
```

See `examples/` for end-to-end sample data.
