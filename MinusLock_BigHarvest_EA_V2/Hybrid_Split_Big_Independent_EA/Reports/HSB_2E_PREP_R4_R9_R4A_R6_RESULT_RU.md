# HSB.2E-PREP-R4-R9-R4A-R6 — восстановление регрессий и приёмки

R6 восстановил temporal, identity, close-direction и DUAL_TAIL проверки; усилил Far uniqueness, replay exactly-once data bindings и полное объявленное lifecycle state с пересчитываемым digest. Исторические R4/R5 artifacts не изменялись.

| Дефект | Исправление | Regression |
|---|---|---|
| Противоречивое/stale/future окно | effective bounds из snapshot, policy и intent | `CONTRADICTORY_WINDOW`, `STALE_DEAL`, `FUTURE_DEAL` |
| Одинаковое направление закрытия | position–intent–deal direction и Bid/Ask close side | `SAME_CLOSE_DIRECTION` |
| Чужой Magic | deal независимо связан с context | `FOREIGN_MAGIC` |
| Второй Far/DUAL_TAIL | все owned FAR positions и tailCount | `SECOND_FAR`, `DUAL_TAIL` |
| Посторонние replay IDs/revision mutation | точные deal/event/binding sets и invariant revision/state | `FOREIGN_REPLAY_IDS`, `REPLAY_REVISION_INCREMENT` |
| Произвольные lifecycle operation/digest | allow-list, scenario binding, canonical stateBody digest, full continuity | `UNKNOWN_OPERATION`, `BAD_STATE_DIGEST`, `LIFECYCLE_DISCONTINUITY` |
| Metadata-based coverage | runtime/semantic hashes и derived boundary properties | `RUNTIME_DUPLICATES_METADATA_DISTINCT`, `METADATA_ERASURE_INDEPENDENT` |
| Stale evidence | acceptance вызывает текущий regression `run()` | `STALE_EVIDENCE_NOT_TRUSTED`, validator sensitivity probes |

Фактически: 28 fixtures, 11 lifecycle steps, 20/20 fresh regressions, 8/8 acceptance sensitivity cases, wrong failures 0, unexpected infrastructure errors 0, findings 0. Обычные acceptance/regression запуски read-only; evidence публикуется только через `--publish-evidence`.

```text
R4A_R5_INDEPENDENT_ACCEPTANCE=REJECTED_BY_TARGETED_AUDIT
R4A_R6_SCHEMA_AND_INTERNAL_CONSISTENCY=PASS
R4A_R6_ACCEPTANCE_REGRESSIONS=PASS
LIFECYCLE_EXECUTED_BY_NATIVE_MODEL=NO
FULL_ECONOMIC_CORRECTNESS=NOT_PROVEN
QUALIFICATION_CORE_READY=NO
ORACLE_V3_CANDIDATE=NOT_YET_FROZEN
MODEL_CHANGES_ALLOWED=NO
TRADING_LOGIC_START_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
```

Python checks do not replace MetaEditor, MQL5 runtime, Strategy Tester or broker-money proof; all are `NOT_RUN`. Следующий шаг — независимый аудит R6, не Oracle freeze.
