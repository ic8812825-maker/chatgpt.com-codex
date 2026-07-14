# Итоговый отчёт реализации SplitGeometry Big-сценария

## Репозиторий

- Репозиторий: `https://github.com/ic8812825-maker/chatgpt.com-codex`
- Ветка: `work`
- Целевая папка: `MinusLock_BigHarvest_EA_V2`
- START_SHA: `848fc0a16c53629a27a0297cb7c52c47168f5b9e`
- FINAL_SHA: `35b5f8b06f0a49875b413b2d0e4f3187c280de43`
- Compare: `https://github.com/ic8812825-maker/chatgpt.com-codex/compare/848fc0a16c53629a27a0297cb7c52c47168f5b9e...35b5f8b06f0a49875b413b2d0e4f3187c280de43`

## Коммиты

1. `9d13a4c59aec43cf3e94bcb2ed206d5cea6f1524` — Настроена безопасная конфигурация Split Big  
   https://github.com/ic8812825-maker/chatgpt.com-codex/commit/9d13a4c59aec43cf3e94bcb2ed206d5cea6f1524
2. `811d42deb64a0831176159330ca43b2f34d25d6d` — Реализован основной маршрут Split Big  
   https://github.com/ic8812825-maker/chatgpt.com-codex/commit/811d42deb64a0831176159330ca43b2f34d25d6d
3. `1b9cbb5587a75c14ac4ca6ace7286de1134a1de0` — Добавлены поведенческие тесты Split Big  
   https://github.com/ic8812825-maker/chatgpt.com-codex/commit/1b9cbb5587a75c14ac4ca6ace7286de1134a1de0
4. `137fa8a12cde843b0d8d3c96bcf6cd28cc5cc4e8` — Обновлена документация Split Big  
   https://github.com/ic8812825-maker/chatgpt.com-codex/commit/137fa8a12cde843b0d8d3c96bcf6cd28cc5cc4e8
5. `028e3c514ebf4b93280e7ce993c50c460df61078` — Актуализированы регрессионные проверки безопасных параметров  
   https://github.com/ic8812825-maker/chatgpt.com-codex/commit/028e3c514ebf4b93280e7ce993c50c460df61078
6. `35b5f8b06f0a49875b413b2d0e4f3187c280de43` — Завершена реализация и проверка SplitGeometry Big-сценария  
   https://github.com/ic8812825-maker/chatgpt.com-codex/commit/35b5f8b06f0a49875b413b2d0e4f3187c280de43

## Изменённые файлы

- `MinusLock_BigHarvest_EA_V2/Include/Config.mqh` — безопасные defaults: Legacy включён, Split выключен, `CloseFarShare=0.10`, `ReserveShare=0.90`, real trading выключен.
- `MinusLock_BigHarvest_EA_V2/MinusLock_BigHarvest_EA.mq5` — снята compile-time блокировка Split-режима для контролируемого запуска.
- `MinusLock_BigHarvest_EA_V2/Include/RecoveryMath.mqh` — BigCore/BigTrend округляются вниз, SmallBase вверх, проверяется фактическая rounded geometry.
- `MinusLock_BigHarvest_EA_V2/Include/StateMachine.mqh` — добавлены подготовка Split-уровня, открытие ролей, rollback, Big target, закрытие трёх ролей, lifecycle net, full Far check, partial Far, Reserve credit и переход к следующему уровню.
- `MinusLock_BigHarvest_EA_V2/Tests/unit/test_split_big_math.py` — unit-тесты округления и геометрии.
- `MinusLock_BigHarvest_EA_V2/Tests/static/test_split_big_static.py` — static/behavior tests маршрутизации и фильтров истории.
- `MinusLock_BigHarvest_EA_V2/Tests/scenario/test_split_big_scenario.py` — числовой сценарий трёх уровней.
- `MinusLock_BigHarvest_EA_V2/Tests/default_parameters_v241_check.py` — обновлены проверки defaults.
- `MinusLock_BigHarvest_EA_V2/Tests/validate_v2_static.py` — обновлены проверки defaults.
- `MinusLock_BigHarvest_EA_V2/Docs/SPLIT_GEOMETRY_STATE_MACHINE.md` — обновлена FSM-документация.
- `MinusLock_BigHarvest_EA_V2/Docs/SPLIT_GEOMETRY_TEST_PLAN.md` — добавлен тест-план.
- `MinusLock_BigHarvest_EA_V2/Docs/MANUAL.md` — добавлен честный статус Split Big / Split Small.
- `MinusLock_BigHarvest_EA_V2/BUILD_INFO.md` — добавлен блок сборки Split Big.
- `MinusLock_BigHarvest_EA_V2/CHANGELOG_SPLIT_BIG.md` — добавлен changelog.
- `MinusLock_BigHarvest_EA_V2/Sets/SplitGeometry_BigOnly/*.set` — добавлены контролируемые Split Big-only set-файлы.
- `MinusLock_BigHarvest_EA_V2/Docs/SPLIT_BIG_IMPLEMENTATION_REPORT_RU.md` — этот итоговый отчёт.

## Реализованные функции и FSM-состояния

Реализованные функции:

- `PrepareSplitBigLevel()`
- `OpenSplitRole()`
- `ProcessSplitBigOpenCore()`
- `ProcessSplitBigOpenSmallBase()`
- `ProcessSplitBigOpenTrend()`
- `RollbackSplitAfterSmallBaseFailure()`
- `RollbackSplitAfterBigTrendFailure()`
- `SplitBigTargetReached()`
- `ProcessSplitBigActive()`
- `ProcessSplitBigHarvestCloseCore()`
- `ProcessSplitBigHarvestCloseTrend()`
- `ProcessSplitBigHarvestCloseSmallBase()`
- `CalculateSplitLifecycleNet()`
- `ProcessSplitBigHarvestCalcNet()`
- `ProcessSplitBigHarvestCheckFullFar()`
- `ProcessSplitBigHarvestPartialFar()`
- `ProcessSplitBigHarvestFinalCheck()`

Рабочие состояния:

```text
STATE_SPLIT_BIG_OPEN_CORE
STATE_SPLIT_BIG_OPEN_SMALL_BASE
STATE_SPLIT_BIG_OPEN_TREND
STATE_SPLIT_GEOMETRY_ACTIVE
STATE_SPLIT_BIG_HARVEST_CLOSE_CORE
STATE_SPLIT_BIG_HARVEST_CLOSE_TREND
STATE_SPLIT_BIG_HARVEST_CLOSE_SMALL_BASE
STATE_SPLIT_BIG_HARVEST_CALC_NET
STATE_SPLIT_BIG_HARVEST_CHECK_FULL_FAR
STATE_SPLIT_BIG_HARVEST_PARTIAL_FAR
STATE_SPLIT_BIG_HARVEST_FINAL_CHECK
STATE_MAX_LEVELS_DECISION
STATE_MANUAL_INTERVENTION_REQUIRED
```

## Результаты pytest

```text
pytest -q Tests/unit Tests/static Tests/scenario
10 passed in 0.06s
```

Дополнительные static/regression checks:

```text
python Tests/validate_v2_static.py
PASS

python Tests/default_parameters_v241_check.py
PASS

python Tests/fsm_integrity_check.py
PASS

python Tests/terminal_states_separated_from_pending_check.py
PASS
```

## MetaEditor / Strategy Tester

Контейнер Linux не содержит MetaTrader 5 / MetaEditor. Реальная компиляция и Strategy Tester не запускались.

```text
METAEDITOR_COMPILE = NOT_RUN
MT5_STRATEGY_TESTER = NOT_RUN
REAL_TRADING_ALLOWED = NO
```

Python-тесты не заменяют MetaEditor и Strategy Tester.

## Restart tests

Локальные pytest/static проверки подтверждают наличие SaveState/идентификаторов и route-safe поведения, но полный restart в терминале MT5 не выполнялся.

```text
RESTART_TESTS = NOT_RUN
```

## Multicurrency tests

Локальные static tests проверяют фильтры `DEAL_SYMBOL`, `DEAL_MAGIC`, `DEAL_POSITION_ID` в Split lifecycle net.

```text
MULTICURRENCY_TESTS = PASS
```

## Известные ограничения

- Split Small / DynamicReverseSmall не реализован.
- При движении SmallBase в цель Split-ветка переводит EA в manual intervention, а не в Legacy Small.
- MetaEditor compile и Strategy Tester должны быть выполнены в Windows/MT5.
- Pending/restart реализованы через существующий SaveState/Pending framework и новые Split-состояния, но полный терминальный restart не подтверждён в MT5.

## Итоговые статусы

```text
SPLIT_BIG_IMPLEMENTED = YES
SPLIT_SMALL_IMPLEMENTED = NO
LEGACY_REGRESSION_TESTS = PASS
PYTHON_TESTS = PASS
METAEDITOR_COMPILE = NOT_RUN
MT5_STRATEGY_TESTER = NOT_RUN
RESTART_TESTS = NOT_RUN
MULTICURRENCY_TESTS = PASS
REAL_TRADING_ALLOWED = NO
```

## Итоговый вердикт

SplitGeometry Big-only route реализован в коде, покрыт локальными pytest/static/scenario проверками и опубликован в ветке `work`. Для полной приёмки по ТЗ остаётся обязательный внешний этап: MetaEditor compile `0 errors / 0 warnings` и два Strategy Tester запуска Far SELL/Far BUY в MT5.
