# HSB.2E-PREP-R4-R9-R4A-R10 — итоговый отчёт

## Baseline и граница

Baseline: `8237e52bbbd3c7a4822c5189ee72969a43a4df5a`. Финальный SHA и remote parity фиксируются после последнего fast-forward push. R10 доказывает внутреннюю целостность и принадлежность предъявленных historical/current replay sources; SHA-256 не доказывает внешнюю брокерскую подлинность.

## Counterexample и binding

R9 принимал independently resealed historical context с чужим magic. R10 сначала проверяет структуру, certificate digest/claims, затем exact binding account/symbol/magic/cycle/transaction/action, historical revision domains, committed output revision и canonical persisted output.

| Case | R9 | R10 |
|---|---|---|
| foreign historical account | не проверялся | `R10_REPLAY_SOURCE_BINDING` |
| foreign historical symbol | не проверялся | `R10_REPLAY_SOURCE_BINDING` |
| foreign historical magic | ACCEPTED | `R10_REPLAY_SOURCE_BINDING` |
| foreign cycle/transaction/action | не проверялся | `R10_REPLAY_SOURCE_BINDING` |
| historical/current revision mismatch | rejection сохранён | `R10_REPLAY_REVISION_BINDING` |
| unbound persisted output | не проверялся отдельно | `R10_REPLAY_STATE_BINDING` |
| same-operation replay | ACCEPTED | ACCEPTED |
| accumulated history replay | ACCEPTED | ACCEPTED |

Regression suite: 67/67, wrong 0, unexpected infrastructure 0; исходные 58 R9 cases сохранены.

## Изолированные source mutants

Каждый из 8 semantic mutants запускался в собственной fresh temporary copy и в fresh `python -B` process. Для каждого сохранены target, exact-one anchor, before/after hash, единственный changed source path, expected и actual affected case IDs и outcome transitions. Forward/reverse order одинаковы.

Все восемь получили `SEMANTIC_MUTATION_VERDICT=CAUGHT_SEMANTIC`. Integrity указан отдельно и не засчитывался как semantic result. Дополнительные harness probes подтвердили: comment/hash-only mutation = `SURVIVED` semantic + protected mismatch; missing anchor = `NOT_APPLIED`; unrelated syntax defect = `INFRASTRUCTURE_ERROR`. Старое evidence не влияет на fresh regression output; основная копия неизменна.

## Проверки и ограничения

Positive fixtures 28, lifecycle steps 11. Future-step independence, input immutability, metadata isolation и runtime duplicate detection: PASS. Protected registry содержит 85 Git-tracked R5–R9/native artifacts без cache. Scope violations, production diff и historical modifications: 0. MetaEditor/MT5: NOT_RUN.

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
