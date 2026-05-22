# Versioning and Compatibility Policy

## Versioning
- Spec uses semantic versioning: MAJOR.MINOR.PATCH.
- Schema files are versioned independently but mapped to spec version.

## Compatibility
- PATCH: no schema-breaking changes.
- MINOR: additive fields allowed; existing required fields unchanged.
- MAJOR: may introduce breaking schema or operation contract changes.

## Migration
- Breaking changes require migration notes and tool guidance.
- Dual-read periods are recommended for one minor cycle.

## Deprecation
- Deprecated fields are announced in MINOR release and removed no earlier than next MAJOR.
