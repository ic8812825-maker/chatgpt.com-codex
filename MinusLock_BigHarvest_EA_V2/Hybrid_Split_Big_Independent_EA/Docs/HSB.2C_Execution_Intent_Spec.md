# HSB.2C — Execution Intent

`HSBI_ExecutionIntent` — immutable DTO между доказанным планом и будущим transaction engine. Digest охватывает Plan/Candidate/Aggregate proofs, identity, volumes, control price, snapshots, source IDs, ActionID, lifecycle и сроки. Все `ulong` сериализуются lossless.

Intent не создаёт request и не меняет Context, ledger, роли или FSM. Изменение payload требует нового intent; одинаковый idempotency key с другим payload является конфликтом.
