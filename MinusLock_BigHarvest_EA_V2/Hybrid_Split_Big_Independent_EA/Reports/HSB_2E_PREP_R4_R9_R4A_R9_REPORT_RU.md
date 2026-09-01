# HSB.2E-PREP-R4-R9-R4A-R9 — итоговый отчёт

## Baseline и граница

Baseline: `db47f2c091ac900323b14452b321e8e7581a30cc`. Финальный SHA и parity фиксируются после fast-forward публикации. R9 доказывает только внутреннюю согласованность представленных execution records и тестового outcome contract; SHA-256 не доказывает внешнюю брокерскую подлинность.

## Контрпримеры R8

| Контрпример | R8 | R9 |
|---|---|---|
| deal/event `confirmed=false` | ACCEPTED | `R9_EXECUTION_CONFIRMATION/EXECUTION_NOT_CONFIRMED` |
| foreign stateRevision | ACCEPTED | `R9_EXECUTION_REVISION/STATE_REVISION_CONTEXT_MISMATCH` |
| foreign snapshotRevision | ACCEPTED | `R9_EXECUTION_REVISION/SNAPSHOT_REVISION_CONTEXT_MISMATCH` |
| REPLAY_COMMITTED + COMMITTED | ACCEPTED | `R9_SCENARIO_PHASE/REPLAY_SCENARIO_REQUIRES_REPLAY` |
| result-only rows | acceptance PASS | `ACTUAL_FIELDS_MISSING` |
| contradictory actual + PASS | acceptance PASS | `OUTCOME_MISMATCH` и `CONTRADICTORY_DIAGNOSTIC_RESULT` |

Historical reproduction: 6/6. Positive fixtures: 28; lifecycle steps: 11.

## Outcome contract и coverage

Независимый catalog содержит для каждого из 58 cases `caseId`, `requirementId`, expected class/check/reason и fixture variant. Runner публикует actual class/check/reason и `executionStatus=EXECUTED`. Acceptance самостоятельно сравнивает значения и не доверяет диагностическому `result`. Все 86 historical obligations имеют fresh-executed target; самостоятельны LARGE_EXACT_IDENTIFIER, MISSING_CONTEXT_ACCOUNT, METADATA_MODIFIED, METADATA_REMOVED, VALID_PRECOMMIT, ORPHAN_DEAL и certificate phase variants.

## Реальные mutations

В изолированной копии реально изменялись source predicates position ownership, event/deal binding, Far ticket, commit revision, confirmed, context revision и scenario/phase. Для каждого зафиксированы before/after SHA-256 и acceptance exit 1. Старое зелёное evidence оставалось рядом и не использовалось как источник истины. Основная копия не менялась.

## Проверки и ограничения

Regression: 58/58; wrong 0; unexpected infrastructure errors 0. Format probes 5/5, source mutants 7/7. Input immutability, metadata erasure, runtime duplicates и future-step independence: PASS. Protected registry: 69 Git-tracked R5–R8/native artifacts, cache исключён. Scope violations 0; production/native/historical diff 0. MetaEditor/MT5: NOT_RUN.

```text
FULL_ECONOMIC_CORRECTNESS=NOT_PROVEN
LIFECYCLE_EXECUTED_BY_NATIVE_MODEL=NO
QUALIFICATION_CORE_READY=NO
ORACLE_V3_FINAL_ACCEPTANCE=NOT_GRANTED
MODEL_CHANGES_ALLOWED=NO
TRADING_LOGIC_START_ALLOWED=NO
TRADE_REQUESTS_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
```
