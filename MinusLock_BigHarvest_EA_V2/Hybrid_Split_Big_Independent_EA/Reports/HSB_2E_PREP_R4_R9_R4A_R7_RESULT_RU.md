# R4A-R7 — прямой schema/replay/lifecycle контур

R7 проверяет предъявленный input без подмены schemaVersion, удаления полей, revision rewrite или reseal certificate. Шесть R6 counterexamples воспроизведены и закрыты.

| Дефект | Исправление | Regression |
|---|---|---|
| replay certificate исправлялся validator | прямой digest/source check исходного certificate | `REPLAY_ZERO_CERT` |
| неизвестная schemaVersion | исполнимая закрытая R7 schema | `INVALID_SCHEMA_VERSION` |
| historical revision 900→1 | exact `r→r+1` и связь historical sources | `HISTORICAL_REVISION_REVERSED` |
| вымышленный Reserve | before/after связаны с authoritative persisted state | `REPLAY_FAKE_RESERVE` |
| пустой lifecycle | минимум два шага | `EMPTY_LIFECYCLE` |
| ложный последний output | FSM allow-list, canonical digest и output binding каждого шага | `BAD_LAST_OUTPUT` |
| cache registry | только `git ls-files`, без pyc/cache/temp/log | clean-checkout acceptance |
| stale evidence | acceptance вызывает свежий regression `run()` | mutant validator + stale green evidence |

Фактически: 28 fixtures, 11 lifecycle steps, 38/38 cumulative regressions, 8/8 sensitivity cases, findings 0. Mapping охватывает 28 R5 и 20 R6 requirements, lostRequirements=0. Обычные запуски read-only; evidence пишется только с `--publish-evidence`.

SHA-256 доказывает внутреннюю связность предъявленных источников, но не внешнюю брокерскую подлинность. `FULL_ECONOMIC_CORRECTNESS=NOT_PROVEN`, `LIFECYCLE_EXECUTED_BY_NATIVE_MODEL=NO`.

```text
QUALIFICATION_CORE_READY=NO
ORACLE_V3_FINAL_ACCEPTANCE=NOT_GRANTED
MODEL_CHANGES_ALLOWED=NO
TRADING_LOGIC_START_ALLOWED=NO
TRADE_REQUESTS_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
```
