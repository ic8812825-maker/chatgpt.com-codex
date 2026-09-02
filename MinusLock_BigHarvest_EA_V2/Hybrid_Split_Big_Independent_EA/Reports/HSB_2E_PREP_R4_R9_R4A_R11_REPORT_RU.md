# HSB.2E-PREP-R4-R9-R4A-R11 — отчёт

## Baseline и граница

Baseline `2141806cf32c5c9155f2fd7d7e3600b6bc234681`; final SHA/parity фиксируются после fast-forward push. Готов к независимому аудиту только первый блок из семи predicates; остальные 24, qualification core и Oracle V3 не объявляются готовыми.

## Seven-predicate matrix

| Order | Predicate | Прямая проверка | Negative |
|---:|---|---|---|
| 1 | SCHEMA | closed shape, required, primitive types/enums | missing phase |
| 2 | NUMERIC_FINITE | все integer/number/DECIMAL schema nodes, Boolean запрещён как число | NaN |
| 3 | RUNTIME_IDENTITY | non-empty identity и bindings account/cycle/transaction/action | empty transaction |
| 4 | SYMBOL_MAGIC_OWNERSHIP | position/deal/event symbol+magic к context | foreign position magic |
| 5 | BROKER_PROPERTIES | positive tick/point/value/contract/volume, ranges, bid≤ask | zero tick |
| 6 | SNAPSHOT_CONTEXT | symbol, magic, snapshot revision к context | foreign snapshot symbol |
| 7 | TEMPORAL_WINDOW | max lower/min upper, inclusive deal bounds | contradictory window |

Каждый evaluator возвращает predicate/status/check/reason/evaluatedPaths/dependencyResults и не вызывает общий R10 validator. Missing structural input даёт FAIL, downstream — BLOCKED_BY_PREREQUISITE.

## Fixtures и traces

Исполнено 15 fixtures: общий positive, семь single-cause negative и семь boundary. Все traces проверены; negative даёт target first failure, предыдущие predicates PASS, последующие BLOCKED. Metadata removal/change, одинаковый runtime, JSON-key order и input immutability не меняют actual trace. Targeted disable каждого evaluator обнаруживается causal pair.

## Mutation evidence

Добавлены согласованные deal+event stateRevision и snapshotRevision pairs: clean R10 отклоняет, а отключение только соответствующего gate даёт ACCEPTED. Девять source mutants имеют отдельные clean copies, baseline wrong=0, полный before/after inventory и единственный diff path. Forward/reverse сравнивает classification, affected IDs и полные before/after outcomes.

Все девять классифицированы `UNSAFE_ACCEPTANCE_EXPOSED`; reason-only изменение больше не выдаётся за unsafe bypass. Доступны также `REASON_CONTRACT_CHANGED`, `REDUNDANT_GUARD_BLOCKED`, `SURVIVED`, `NOT_APPLIED`, `INFRASTRUCTURE_ERROR`, `CONTAMINATED`, `BASELINE_INVALID`. Protected integrity не участвует в semantic verdict.

## Сохранность

R10: positive 28/28, lifecycle steps 11, regressions 67/67, wrong 0. R11 acceptance: predicates 7, causal fixtures 15, revision pairs 2, mutation result PASS. Protected registry содержит 102 Git-tracked R5–R10/native artifacts. Scope/production/historical diff: 0. MetaEditor/MT5: NOT_RUN.

```text
FIRST_PREDICATE_BLOCK_READY_FOR_INDEPENDENT_AUDIT=YES
QUALIFICATION_CORE_READY=NO
ORACLE_V3_FINAL_ACCEPTANCE=NOT_GRANTED
FULL_ECONOMIC_CORRECTNESS=NOT_PROVEN
LIFECYCLE_EXECUTED_BY_NATIVE_MODEL=NO
MODEL_CHANGES_ALLOWED=NO
TRADING_LOGIC_START_ALLOWED=NO
TRADE_REQUESTS_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
```
