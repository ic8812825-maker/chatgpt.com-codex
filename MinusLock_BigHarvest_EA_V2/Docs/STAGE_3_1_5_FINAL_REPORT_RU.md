# Этап 3.1.5 — итоговый отчёт

## Git и scope

```text
START_SHA=78fdcbc1bdbc982cde0898e65420cae1f759aa40
FINAL_COMMIT=THIS_REPORT_COMMIT
REMOTE_BRANCH=work
LOCAL_REMOTE_PARITY=VERIFIED_AFTER_PUSH
REPOSITORY_SCOPE_VIOLATION=NO
PRODUCTION_TRADING_LOGIC_CHANGED=NO
PARAMETER_PROFILE_CHANGED=NO
```

Изменены только `Docs`, `Tests`, `Tools`. `.mq5`, `.mqh`, `.set`, FSM и profiles не менялись.
19 последовательных commits имеют сообщения `Этап 3.1.5.1` … `Этап 3.1.5.19`; полный SHA-list
получается непосредственно `git log --reverse 78fdcbc..HEAD` и является источником истины.

## Исполняемые результаты

```text
POSITIVE_SCENARIOS=38/38
COUNTEREXAMPLES_CAUGHT=25/25
BLOCKERS_REGISTERED=25
MISSING_CAUSAL_RULES=0
INEFFECTIVE_CAUSAL_RULES=0
VACUOUS_CAUSAL_RULES=0
BLOCKING_COUNTERS=NONE
```

Oracle доказывает Bid/Ask sides, asymmetric tick value, adverse slippage, signed DealNet,
actual-volume partial fills, opening-cost residual, isolation, RecoveryPLCloseNow, conservation,
duplicate deal/event no-op, restart persistence и reconciled final-close gate.

## MQL5 mapping

IMPLEMENTED: базовые Symbol/Magic routes и Reserve structures. PARTIAL: projected money, CycleID,
realized aggregation, reserve idempotency, RecoveryPL, restart/final-close reconciliation. MISSING:
единое opening-cost allocation, полное разделение ledgers, TransitionBudget/Residual ledger и
composite exactly-once key. Production не исправлялся.

## Ограничения

```text
STATIC_NORMATIVE_MONEY_MODEL=PASS
PRODUCTION_MQL5_MAPPING=PARTIAL
METAEDITOR_COMPILE=NOT_RUN
MT5_STRATEGY_TESTER=NOT_RUN
EXACT_MT5_RUNTIME_EXECUTION=NOT_PROVEN_BY_STAGE_3_1_5
REAL_TRADING_ALLOWED=NO
```

Root pytest baseline ограничен отсутствующими pandas/openpyxl. Этап 3.1.6 не начат.

## FINAL_VERDICT

```text
STAGE_3_1_5_VALIDATION=PASS
NORMATIVE_MONEY_MODEL=PASS
PROJECTED_MONEY_CONTRACT=PASS
REALIZED_MONEY_CONTRACT=PASS
RECOVERY_PL_CLOSE_NOW=PASS
SYMBOL_MAGIC_CYCLE_ISOLATION=PASS
COST_ALLOCATION=PASS
DOUBLE_COUNTING_BLOCKED=PASS
BUDGET_CONSERVATION=PASS
FINAL_RESERVE_TAGGING=PASS
EXACTLY_ONCE_CONTRACT=PASS
RECONCILIATION_CONTRACT=PASS
COUNTEREXAMPLE_SUITE=PASS
BLOCKER_CAUSAL_AUDIT=PASS
BLOCKING_COUNTERS=NONE
PRODUCTION_MQL5_IMPLEMENTATION=NOT_CHANGED
EXACT_MT5_RUNTIME_EXECUTION=NOT_PROVEN_BY_STAGE_3_1_5
REAL_TRADING_ALLOWED=NO
REPOSITORY_SCOPE_VIOLATION=NO
PRODUCTION_TRADING_LOGIC_CHANGED=NO
PARAMETER_PROFILE_CHANGED=NO
STAGE_3_1_5_STATUS=CLOSED
NEXT_ALLOWED_STAGE=3.1.6
STAGE_3_1_6_STARTED=NO
AWAITING_USER_APPROVAL=YES
```

# Correction 3.1.5.20

```text
PREVIOUS_STAGE_3_1_5_PASS=SUPERSEDED
INDEPENDENT_REVIEW_STATUS=FAIL
STAGE_3_1_5_STATUS=REOPENED_FOR_CORRECTION
CORRECTION_BASELINE=66ace3317df41157b4077848ab30e7f94f0ea3e7
NEXT_ALLOWED_STAGE=NONE
STAGE_3_1_6_STARTED=NO
REAL_TRADING_ALLOWED=NO
```

Прежние evidence сохранены как исторические, но их ложноположительный executable verdict отменён:
счётчик scenarios был константой, blockers формировались из имён, pytest collection отсутствовала,
а reconciliation/restart/final-close не были связаны с экономическими ledger.

## Superseding verdict 3.1.5.58

Вторая executable correction supersedes все предыдущие Stage 3.1.5 PASS markers. Итоговый источник
статуса — `STAGE_3_1_5_SECOND_CORRECTION_RU.md` и evidence `stage_3_1_5_second_correction`.
`STAGE_3_1_5_STATUS=CLOSED`; `NEXT_ALLOWED_STAGE=3.1.6`; `REAL_TRADING_ALLOWED=NO`.

### Статус после третьей корректирующей приёмки (3.1.5.72)

```text
STAGE_3_1_5_VALIDATION=PASS
STAGE_3_1_5_STATUS=CLOSED
FRESH_CLONE_VERIFICATION=PASS
BLOCKING_COUNTERS=NONE
NEXT_ALLOWED_STAGE=3.1.6
STAGE_3_1_6_STARTED=NO
AWAITING_USER_APPROVAL=YES
REAL_TRADING_ALLOWED=NO
PRODUCTION_MQL5_IMPLEMENTATION=NOT_CHANGED
PRODUCTION_MQL5_MAPPING=PARTIAL
METAEDITOR_COMPILE=NOT_RUN
MT5_STRATEGY_TESTER=NOT_RUN
```

### Четвёртая корректирующая проверка 3.1.5.87

Исполняемые Python-доказательства прошли полную локальную проверку; независимая fresh-clone приёмка 3.1.5.88 ещё не завершена. Production MQL5 не изменялся.

```text
STAGE_3_1_5_STATUS=REOPENED_FOR_CORRECTION
NEXT_ALLOWED_STAGE=NONE
STAGE_3_1_6_START_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
PRODUCTION_MQL5_IMPLEMENTATION=NOT_CHANGED
PRODUCTION_MQL5_MAPPING=PARTIAL
METAEDITOR_COMPILE=NOT_RUN
MT5_STRATEGY_TESTER=NOT_RUN
```

### Итог 3.1.5.88

```text
FRESH_CLONE_VERIFICATION=PASS
BLOCKING_COUNTERS=NONE
STAGE_3_1_5_STATUS=CLOSED
NEXT_ALLOWED_STAGE=3.1.6
STAGE_3_1_6_STARTED=NO
AWAITING_USER_APPROVAL=YES
REAL_TRADING_ALLOWED=NO
```

### Пятая корректирующая проверка 3.1.5.105

```text
STAGE_3_1_5_STATUS=REOPENED_FOR_CORRECTION
FRESH_CLONE_VERIFICATION=PENDING
NEXT_ALLOWED_STAGE=NONE
STAGE_3_1_6_START_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
PRODUCTION_MQL5_IMPLEMENTATION=NOT_CHANGED
METAEDITOR_COMPILE=NOT_RUN
MT5_STRATEGY_TESTER=NOT_RUN
```

### Итог 3.1.5.106

```text
FRESH_CLONE_VERIFICATION=PASS
BLOCKING_COUNTERS=NONE
STAGE_3_1_5_STATUS=CLOSED
NEXT_ALLOWED_STAGE=3.1.6
STAGE_3_1_6_STARTED=NO
AWAITING_USER_APPROVAL=YES
REAL_TRADING_ALLOWED=NO
```

## Шестая корректирующая приёмка

Verdict 3.1.5.106 был superseded; новый executable oracle блокирует over-allocation, foreign source pools/events, невозможные event revisions, повреждённые opening costs и correlated persistence attacks точными `IntegrityCode`. Независимый fresh clone подтвердил 347 stage и 738 project pytest, causal/source/final owners и неизменный standalone manifest. Production MQL5 не изменялся; реальная торговля запрещена.

## Седьмая корректирующая приёмка

Verdict 3.1.5.124 superseded. Закрытая schema 7, transition history certificate, полный fill/event/source digest, реальные corrupted-store Final Close probes и семантический FaultEvidence audit прошли независимый fresh clone. Production MQL5 не изменялся; Python proof не разрешает реальную торговлю.

## Восьмая корректирующая приёмка

Deal/Event replay теперь различает идемпотентность и exact conflict; opening-cost ledger проверяет пропорциональную Decimal-формулу и broker grid; reference вычисления отделены от actual oracle; final validator исполняет специализированные owners. Production MQL5 не изменялся.
