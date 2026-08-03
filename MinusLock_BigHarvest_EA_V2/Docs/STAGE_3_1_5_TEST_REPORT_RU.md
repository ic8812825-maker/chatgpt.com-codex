# Этап 3.1.5 — классификация исходных и итоговых проверок

## Baseline

Полный root `pytest` остановился на четырёх collection errors: отсутствуют `pandas` и `openpyxl`.
Категория: `PRE_EXISTING_UNRELATED` / environment dependency. Это не маскируется как PASS.
Заявленные предыдущей проверкой 10 standalone failures требуют отдельного воспроизводимого списка;
профильные/optimization проверки относятся к `FUTURE_STAGE`, monetary Docs/Tests/Tools проверяются
новым validator. Production gaps из mapping — `REAL_DEFECT` либо `FUTURE_STAGE`, но не исправляются.

## Денежные конфликты

Этап 3.1.5 нормативно закрывает только: cycle-local P/L, Bid/Ask projected money, signed DealNet,
cost allocation, two-ledger separation, budget conservation и exactly-once reconciliation.
BigRatio, SmallRatio, CloseBigOnSmall, RemainBigOnSmall, CloseFarShare, ReserveShare, NewFar source
и production profile не выбирались: `STATUS=BLOCKED_BY_USER_DECISION` для 3.1.6–3.1.7.

```text
METAEDITOR_COMPILE=NOT_RUN
MT5_STRATEGY_TESTER=NOT_RUN
EXACT_MT5_RUNTIME_EXECUTION=NOT_PROVEN_BY_STAGE_3_1_5
REAL_TRADING_ALLOWED=NO
```

## Correction 3.1.5.35 standalone reproduction

Фактически выполнены все 181 `Tests/*_check.py`: `PASSED=171`, `FAILED=10`. Имена и stderr
сохранены в `Evidence/stage_3_1_5_correction/standalone_checks.log`; все десять классифицированы
в `standalone_classification.log`. Production, `.set`, FSM и profiles не изменялись.
