# Итоговый отчёт этапа денежной Split системы

## Идентификаторы

- START_SHA: `671c023dc22b5476a2a71319ede424901f28e0f0`
- FINAL_SHA: будет равен HEAD после коммита этого отчёта и финальной проверки Git.
- Ветка: `work`
- Папка: `MinusLock_BigHarvest_EA_V2`
- Compare: `https://github.com/ic8812825-maker/chatgpt.com-codex/compare/671c023dc22b5476a2a71319ede424901f28e0f0...work`

## Коммиты текущего этапа

| № | SHA | Подпись | Пункт |
| - | --- | --- | --- |
| 1 | `11c39d5` | Зафиксировано исходное состояние этапа денежной модели | Baseline audit |
| 2 | `757c9a2` | Исправлен безопасный отказ восстановления в OnInit | RecoverState failure guard |
| 3 | `e5b352e` | Добавлена денежная модель брокера через OrderCalcProfit | Broker Money Model |
| 4 | `fcb2ba1` | Добавлен единый денежный шлюз финального закрытия | Final Close Gate |
| 5 | `e91b3e7` | Добавлены изолированные тестовые настройки Split системы | Split test presets |

## Изменённые файлы

| Файл | Что изменено | Риск, который закрывается | Тест |
| --- | --- | --- | --- |
| `Docs/NEXT_STAGE_BASELINE_AUDIT_RU.md` | Зафиксирован baseline, defaults, тесты и ограничения | Потеря исходной точки | Ручная проверка + pytest baseline |
| `MinusLock_BigHarvest_EA.mq5` | OnInit больше не сбрасывает контекст при recovery failure; добавлена проверка новых money inputs; подключён BrokerMoneyModel | Потеря RecoveryContext и ложный clean start | static test `test_next_stage_oninit_recovery_failure_never_resets_unless_clean_start` |
| `Include/StateMachine.mqh` | Добавлены `IsProvenCleanStart`, money-model usage для projected close, `EvaluateFinalCloseGate` | Unsafe recovery reset, point fallback, разрозненный final-close gate | static tests + pytest |
| `Include/BrokerMoneyModel.mqh` | Новый единый модуль прогнозных денежных расчётов через `OrderCalcProfit`/`OrderCalcMargin` | Ручная point-value модель без broker properties | static test `test_money_model_file_and_inputs_exist_and_ordercalc_is_primary` |
| `Include/Config.mqh` | Добавлены inputs комиссий, swap/spread/slippage/execution buffers и `MinimumBigRecoveryImprovementMoney` | Невозможность учитывать execution costs | static tests |
| `Include/Types.mqh` | Добавлена `FinalCloseEvaluation` | Нет единой структуры оценки final close | static test `test_final_close_gate_exists_and_small_reserve_uses_it` |
| `Sets/SPLIT_TEST_SAFE.set` | Безопасный Split test preset | Смешивание Legacy/Split в тестах | static test `test_isolated_split_test_sets_and_geometry_assert` |
| `Sets/SPLIT_TEST_BALANCED.set` | Balanced Split test preset | Смешивание Legacy/Split в тестах | static test `test_isolated_split_test_sets_and_geometry_assert` |
| `Tests/static/test_split_architecture_static.py` | Добавлены guards для OnInit, money model, final gate и presets | Регрессии порядка recovery и money gates | pytest |
| `Docs/SPLIT_MONEY_MODEL_FINAL_REPORT_RU.md` | Настоящий отчёт | Прозрачность выполненного/невыполненного | Ручная проверка |

## Что выполнено

- Baseline зафиксирован.
- RecoverState failure в `OnInit()` больше не приводит к безусловному `ResetRecoveryContext()` и `STATE_IDLE`.
- Добавлен начальный `BrokerMoneyModel.mqh` с `OrderCalcProfit`/`OrderCalcMargin` как обязательным источником прогнозных денежных расчётов.
- Projected close path переведён на Broker Money Model без silent fallback на ручной point-value при недоступном `OrderCalcProfit`.
- Добавлен единый `FinalCloseEvaluation`/`EvaluateFinalCloseGate` и подключён к Small reserve check.
- Добавлены изолированные Split test presets.
- Python/static тесты проходят.

## Что не выполнено полностью

Следующие пункты технического задания требуют отдельного продолжения и/или Windows/MT5 окружения:

- Полный перевод всех финансовых решений с point-based функций на деньги: выполнен частично.
- Partial Far полностью на денежный бюджет: не завершено.
- Big Recovery Improvement proof в коде: не завершено.
- Reserve Catch-Up proof document: не создан.
- Small NewFar compression rewrite: не выполнено.
- Полная денежная модель Small Transition: не выполнено.
- Proof конечного числа Small-разворотов: не создан.
- False Reverse Protocol: не создан.
- MQL5 internal test harness: не создан.
- MetaEditor compile: NOT_RUN.
- MT5 Strategy Tester: NOT_RUN.
- Big/Small compatibility report с реальными логами: не создан.
- Legacy removal plan: не создан.
- Полная актуализация всей документации: не завершена.

## Результаты проверок

```text
pytest -q Tests/unit Tests/static Tests/scenario = PASS, 83 passed
python Tests/validate_v2_static.py = PASS
python Tests/default_parameters_v241_check.py = PASS
python Tests/fsm_integrity_check.py = PASS
python Tests/terminal_states_separated_from_pending_check.py = PASS
METAEDITOR_COMPILE = NOT_RUN
MT5_STRATEGY_TESTER = NOT_RUN
```

## Проверка Big и Small

```text
BIG_SCENARIO_BROKEN = UNKNOWN
SMALL_SCENARIO_BROKEN = UNKNOWN
BIG_SMALL_INTERACTION_BROKEN = UNKNOWN
```

Причина: реальные MetaEditor/MT5 Strategy Tester сценарии Big/Small не выполнены в текущем Linux-контейнере.

## Финальный блок статусов

```text
BIG_RECOVERY_IMPROVEMENT = FAIL
RESERVE_CATCH_UP = FAIL
PARTIAL_FAR_MONEY_SAFETY = FAIL
FINAL_CLOSE_MONEY_SAFETY = PARTIAL
SMALL_TRANSITION_MONEY_SAFETY = FAIL
NEW_FAR_COMPRESSION = FAIL
FINITE_REVERSE_COUNT = FAIL
FALSE_REVERSE_PROTOCOL = FAIL
BIG_SCENARIO_BROKEN = UNKNOWN
SMALL_SCENARIO_BROKEN = UNKNOWN
BIG_SMALL_INTERACTION_BROKEN = UNKNOWN
METAEDITOR_COMPILE = NOT_RUN
MT5_STRATEGY_TESTER = NOT_RUN
REAL_TRADING_ALLOWED = NO
```

## Вердикт

Текущий инкремент пригоден только для дальнейшей разработки и локальных Python/static проверок. Demo/forward/cent/real trading не разрешены. `REAL_TRADING_ALLOWED = NO` остаётся обязательным до полного завершения money-model migration, MetaEditor `0 errors / 0 warnings` и MT5 Strategy Tester PASS.
