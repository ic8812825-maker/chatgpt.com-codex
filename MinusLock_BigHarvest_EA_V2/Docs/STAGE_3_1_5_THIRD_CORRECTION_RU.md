# Третья корректирующая серия Этапа 3.1.5

```text
THIRD_INDEPENDENT_REVIEW=FAIL
PUBLISHED_3_1_5_58_PASS=SUPERSEDED
STAGE_3_1_5_STATUS=REOPENED_FOR_CORRECTION
NEXT_ALLOWED_STAGE=NONE
STAGE_3_1_6_START_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
```

Воспроизведены: потеря source pools и managed positions после restart; повторное финансирование
source; allocation из opening IN; пропуск side effects ранними restart; unrelated consume;
hardcoded extended probes; label-only mutations; self-comparison rename audit; отсутствие обязательных
scenario categories и неспособность validator обнаружить эти нарушения.

## Итог третьей корректирующей серии (3.1.5.60–3.1.5.72)

Исполняемая модель теперь сохраняет source pools и managed positions, сверяет восстановленные pools с actual history и allocation records, исключает opening `IN` из harvest, связывает каждое потребление с parent allocation через immutable `ConsumptionKey`, а restart-orchestrator завершает обязательный allocation side effect exactly once.

Проверка из отдельного свежего clone опубликованной ветки `work`:

```text
FRESH_CLONE_VERIFICATION=PASS
STAGE_TESTS=212/212 PASS
PROJECT_TESTS=603/603 PASS
POSITIVE_SCENARIOS_TOTAL=145
UNIQUE_FINGERPRINTS=145
REQUIRED_SCENARIO_CATEGORIES_MISSING=0
LOSS_MONEY_SCENARIOS=2
MUTATIONS_TOTAL=25
EXTENDED_COUNTEREXAMPLES=16
STANDALONE_TOTAL=181
STANDALONE_PASSED=171
STANDALONE_KNOWN_FAILURES=10
STANDALONE_NEW_FAILURES=0
BLOCKING_COUNTERS=NONE
STAGE_3_1_5_STATUS=CLOSED
NEXT_ALLOWED_STAGE=3.1.6
STAGE_3_1_6_STARTED=NO
AWAITING_USER_APPROVAL=YES
REAL_TRADING_ALLOWED=NO
```

Production MQL5 не изменялся. `METAEDITOR_COMPILE=NOT_RUN`; `MT5_STRATEGY_TESTER=NOT_RUN`; точное MT5 runtime execution этим этапом не доказано.
