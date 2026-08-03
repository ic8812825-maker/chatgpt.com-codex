# Коррекция Этапа 3.1.5

Предыдущий PASS superseded. Исполняемая модель теперь использует строгие enums и broker grid,
неизменяемый EventSnapshot, последовательную reconciliation machine, Economic Ledger из unique
actual deals, tagged Allocation Ledger, Decimal partial-fill allocation, JSON round-trip/replay и
Final Close evaluator, самостоятельно читающий ledger/snapshot.

Positive matrix формируется как список структурированных результатов; pytest действительно собирает
параметризованные cases. Mutations меняют Policy и вычисленные Observables; независимый evaluator
не получает имя mutation/blocker. Validator агрегирует владельцев статусов и возвращает nonzero при
любом вычисленном blocker. Source guards являются только дополнительной защитой.

Production mapping остаётся PARTIAL: runtime MQL5 не изменялся, exact MT5 execution не доказан.

## Final correction acceptance

```text
PREVIOUS_STAGE_3_1_5_PASS=SUPERSEDED
STAGE_3_1_5_CORRECTION_VALIDATION=PASS
CORRECTION_COMMITS_PUBLISHED=19/19
POSITIVE_SCENARIOS_TOTAL=80
POSITIVE_SCENARIOS_FAILED=0
COUNTEREXAMPLES_TOTAL=25
COUNTEREXAMPLES_FAILED=0
STAGE_3_1_5_PYTEST_TESTS_COLLECTED=96
STAGE_3_1_5_PYTEST_FAILED=0
BLOCKING_COUNTERS=NONE
STATIC_NORMATIVE_MONEY_MODEL=PASS
PRODUCTION_MQL5_MAPPING=PARTIAL
PRODUCTION_MQL5_IMPLEMENTATION=NOT_CHANGED
METAEDITOR_COMPILE=NOT_RUN
MT5_STRATEGY_TESTER=NOT_RUN
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
