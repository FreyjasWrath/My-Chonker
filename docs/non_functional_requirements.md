# Non-Functional Requirements

## Integrity
- All Papers and container events carry sha256 hash references.
- Acceptance: hash verification passes for 100% of files in validation run.

## Durability
- Append operations must fsync before success return.
- Acceptance: crash simulation after ack causes 0 acknowledged-event loss.

## Performance
- Target append throughput: >= 500 events/sec on baseline dev machine.
- Query target: filter 100k events in <= 2s.
- Acceptance: benchmark scripts produce values meeting targets.

## Scalability
- Support at least 10 million events per container via JSONL streaming.
- Acceptance: memory stays bounded (<512MB) in sequential scan.

## Observability
- Required metrics: append latency, append failures, query latency.
- Required logs: operation name, artifact ids, timestamp, outcome.
- Acceptance: metrics exposed and logs emitted in all operations.
