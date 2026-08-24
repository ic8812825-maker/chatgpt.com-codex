# HSB.2E PREP-R4-R6 — corrected executable specification handoff

R4-R6 остаётся исключительно offline specification. Production MQL5, broker dispatch и торговые requests не создавались.

## Исправленные первопричины

- Каждая deal связывается с context, position и executable intent.
- Price range выводится только из sealed quote snapshot и sealed versioned policy.
- Persisted records полностью перевалидируются до пересчёта cache.
- Commit certificate связан с deal/event ledger, full fills, economic/allocation/persistence digests и revisions.
- Sealed economic policy проверяет share ranges и disjoint share sum.
- Initial profit изолирован; Partial Far рассчитывается; New Far выводится из Big residual; Final списывает Reserve.
- 104 historical vectors исполняются только `hsb_2e_reference_model_r4_r6`.
- 10 exact false-pass fixtures имеют сохранённый input hash и explicit adapter.
- 30 source mutations выполняются в одноразовых копиях и требуют конкретный Check ID.

Следующий этап требует отдельного письменного административного решения.
