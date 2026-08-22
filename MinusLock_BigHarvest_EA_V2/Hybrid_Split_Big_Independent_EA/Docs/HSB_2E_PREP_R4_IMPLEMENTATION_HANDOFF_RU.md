# HSB.2E PREP-R4 — implementation handoff

`START_BASELINE` назначает Администратор после независимой проверки. Для всех этапов до отдельного разрешения: `BROKER_DISPATCH_ALLOWED=NO`, `REAL_TRADING_ALLOWED=NO`.

| Этап | Содержание | Reference acceptance |
|---|---|---|
| HSB.2E-IMPL-01 | Immutable status/reason, identity, snapshot, position/deal и broker-intent DTO; serialization, digest, compile-only tests | typed R4 context/result; deterministic digest; без формул, FSM mutation и dispatch |
| IMPL-02 | Grid и broker properties | `normalize_volume`, directional price vectors |
| IMPL-03 | Money evaluator | `deal_money`, money conservation |
| IMPL-04 | Geometry | price/volume validation и boundary vectors |
| IMPL-05 | Initial Lock | `initial_lock`, `IGNORED_INITIAL_POSITIVE_PROFIT` |
| IMPL-06 | Big settlement | `execute_big_level_scenario`, SBIG vectors |
| IMPL-07 | Small settlement | `execute_small_reversal_scenario`, SSMALL vectors |
| IMPL-08 | Reserve/allocation | Reserve isolation и exactly-once invariants |
| IMPL-09 | Partial Far | grid floor, volume conservation |
| IMPL-10 | Final-close gates | RecoveryPL и coverage invariants |
| IMPL-11 | NewFar/Future Small/Catch-Up | strict compression и no dual tail |
| IMPL-12 | Persistence/restart | RST crash-point vectors |
| IMPL-13 | FSM orchestration | typed scenario engine и persistence order |
| IMPL-14 | Broker request builder | validated offline intent DTO only |
| IMPL-15 | Disabled broker adapter | compile-only hard-disabled adapter |
| IMPL-16 | Demo-only dispatch review | отдельное административное решение; real trading остаётся запрещённым |

Каждый этап обязан использовать связанные `FORMULA_ID`, `SCENARIO_ID`, `VECTOR_ID`, `T465–T1149`, зависимости и acceptance checks из R4 JSON. Следующий разрешаемый этап — только `HSB.2E-IMPL-01`.
