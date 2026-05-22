#!/usr/bin/env python3
import json, pathlib, sys

try:
    from jsonschema import validate, ValidationError
except ModuleNotFoundError:
    print("ERROR: Missing dependency 'jsonschema'. Run: python3 -m pip install -r requirements-dev.txt", file=sys.stderr)
    raise SystemExit(2)

root = pathlib.Path(__file__).resolve().parents[1]

schemas = {
    "paper": json.loads((root / "schemas/paper.schema.json").read_text()),
    "archive": json.loads((root / "schemas/archive.schema.json").read_text()),
    "container": json.loads((root / "schemas/container.schema.json").read_text()),
}

def check(path, schema_key, should_pass=True):
    obj = json.loads(path.read_text())
    try:
        validate(obj, schemas[schema_key])
        result = True
    except ValidationError:
        result = False
    status = "PASS" if result == should_pass else "FAIL"
    print(f"{status}: {path}")
    return status == "PASS"

ok = True
ok &= check(root / "examples/papers/paper_valid.json", "paper", True)
ok &= check(root / "examples/papers/paper_invalid_missing_id.json", "paper", False)
ok &= check(root / "examples/archives/index.json", "archive", True)
for line in (root / "examples/containers/container.jsonl").read_text().splitlines():
    if not line.strip():
        continue
    obj = json.loads(line)
    try:
        validate(obj, schemas["container"])
    except ValidationError:
        print("FAIL: container event line")
        ok = False
if ok:
    print("All example validations behaved as expected.")
    raise SystemExit(0)
raise SystemExit(1)
