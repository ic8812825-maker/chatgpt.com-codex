# Отчёт Этапа 2 — исправление архитектурной целостности SplitGeometry Big

## Репозиторий

- Репозиторий: `https://github.com/ic8812825-maker/chatgpt.com-codex`
- Ветка: `work`
- Целевая папка: `MinusLock_BigHarvest_EA_V2`
- START_SHA: `177062bac1ab5cfb4aa41de09912e1d3ac0f914a`
- FINAL_SHA: будет указан в финальном сообщении после публикации итогового коммита отчёта.
- Compare: `https://github.com/ic8812825-maker/chatgpt.com-codex/compare/177062bac1ab5cfb4aa41de09912e1d3ac0f914a...FINAL_SHA`

## Созданные коммиты

1. `becdfca08a9cb478c55b92592ad8ef4b5e860342` — Добавлены отдельные состояния Split pending и лимитов  
   https://github.com/ic8812825-maker/chatgpt.com-codex/commit/becdfca08a9cb478c55b92592ad8ef4b5e860342
2. `fe0310b9c983d11acde137b36a2f4166e7529df9` — Исправлена проверка топологий Split Big  
   https://github.com/ic8812825-maker/chatgpt.com-codex/commit/fe0310b9c983d11acde137b36a2f4166e7529df9
3. `36ae80d782b2ff8265bc6579961ec02fb18ecff2` — Добавлено разрешение Split-позиций  
   https://github.com/ic8812825-maker/chatgpt.com-codex/commit/36ae80d782b2ff8265bc6579961ec02fb18ecff2
4. `096457f1c6447f208fa52e77bbd15c624888e6c5` — Расширена сверка Split-топологий  
   https://github.com/ic8812825-maker/chatgpt.com-codex/commit/096457f1c6447f208fa52e77bbd15c624888e6c5
5. `4c92bee312d78c26189101c74db3057b7a2733e8` — Реализованы pending и денежные защиты Split Big  
   https://github.com/ic8812825-maker/chatgpt.com-codex/commit/4c92bee312d78c26189101c74db3057b7a2733e8
6. `6485ac375cafb5a1fb67be519d520fff15f25ee6` — Реализовано восстановление Split Big после перезапуска  
   https://github.com/ic8812825-maker/chatgpt.com-codex/commit/6485ac375cafb5a1fb67be519d520fff15f25ee6
7. `a4c7c74740d90f389152c0c6223f56cde9786abe` — Добавлены архитектурные тесты Split Big  
   https://github.com/ic8812825-maker/chatgpt.com-codex/commit/a4c7c74740d90f389152c0c6223f56cde9786abe

## Изменённые файлы

- `Include/Types.mqh` — добавлены отдельные Split pending states, `STATE_SPLIT_PARTIAL_HISTORY_PENDING`, `STATE_SPLIT_MAX_LEVELS_DECISION`.
- `Include/StateIntegrityEngine.mqh` — добавлена Split topology matrix и `ValidateSplitStateIntegrityLeg`; Split-состояния больше не требуют legacy Big/Small.
- `Include/PositionResolutionEngine.mqh` — добавлены `ResolveBigCorePosition`, `ResolveBigTrendPosition`, `ResolveSmallBasePosition` с приоритетом ticket → identifier → role comment/CycleId/Level → time-window fallback.
- `Include/ReconciliationEngine.mqh` — добавлена сверка Split-топологий, распознавание Split-ролей как known context и split orphan diagnostics.
- `Include/PendingContractEngine.mqh` — добавлены контракты для Split open/close pending states.
- `Include/StateMachine.mqh` — добавлены retry handlers, actual partial Far accounting, min residual guard, `SPLIT_FINAL_CLOSE_PROFIT`, Reserve Ledger restore check, Split ClosedProfit guard cleanup.
- `Tests/unit/test_split_architecture_model.py` — unit-модель idempotent Reserve Ledger, actual partial carry, минимального остатка Far.
- `Tests/static/test_split_architecture_static.py` — static architecture tests по StateIntegrity, PositionResolution, Reconciliation, Pending, partial accounting, final guard, Reserve persistence.
- `Tests/scenario/test_split_architecture_restart.py` — restart/idempotency и multicurrency key isolation scenarios.
- `CHANGELOG_SPLIT_BIG.md` — добавлен журнал Этапа 2.
- `Docs/SPLIT_BIG_ARCHITECTURE_FIX_REPORT_RU.md` — этот отчёт.

## Что исправлено

- `StateIntegrityEngine` теперь проверяет Split-роли отдельно от legacy Big/Small.
- `PositionResolutionEngine` умеет восстанавливать BigCore, BigTrend и SmallBase.
- `ReconciliationEngine` знает Split-топологии и не считает корректные Split-роли orphan.
- `RecoverState` вызывает восстановление Split-ролей и сверку Reserve Ledger.
- Reserve Ledger event keys сохраняются через существующий persistent state и сверяются при restore.
- Partial Far carry считается по actual deals; если история не найдена, Reserve не начисляется и состояние переводится в `STATE_SPLIT_PARTIAL_HISTORY_PENDING`.
- Partial Far защищён от остатка ниже `SYMBOL_VOLUME_MIN`.
- Immediate full Far close использует `SPLIT_FINAL_CLOSE_PROFIT`, очищает Split/Far context, списывает Reserve один раз и только затем входит в `STATE_CLOSED_PROFIT`.
- Split pending/retry покрывает open BigCore/SmallBase/BigTrend и close Core/Trend/SmallBase/Far partial/Far full.
- Split max levels изолирован через `STATE_SPLIT_MAX_LEVELS_DECISION`.

## Результаты тестов

```text
pytest -q Tests/unit Tests/static Tests/scenario
24 passed
```

```text
python Tests/validate_v2_static.py
PASS
```

```text
python Tests/default_parameters_v241_check.py
PASS
```

```text
python Tests/fsm_integrity_check.py
PASS
```

```text
python Tests/terminal_states_separated_from_pending_check.py
PASS
```

## MetaEditor / MT5

MetaTrader 5 / MetaEditor недоступны в Linux-контейнере.

```text
METAEDITOR_COMPILE = NOT_RUN
MT5_STRATEGY_TESTER = NOT_RUN
REAL_TRADING_ALLOWED = NO
```

Python/static/scenario tests не заменяют реальную компиляцию и Strategy Tester.

## Статусы

```text
SPLIT_STATE_INTEGRITY = PASS
SPLIT_RECONCILIATION = PASS
SPLIT_RESTART_RECOVERY = PASS
RESERVE_LEDGER_PERSISTENCE = PASS
PARTIAL_FAR_ACTUAL_ACCOUNTING = PASS
SPLIT_PENDING_RETRY = PASS
SPLIT_FINAL_CLOSE_GUARD = PASS
LEGACY_REGRESSION = PASS
PYTHON_TESTS = PASS
METAEDITOR_COMPILE = NOT_RUN
MT5_STRATEGY_TESTER = NOT_RUN
REAL_TRADING_ALLOWED = NO
```

## Известные ограничения

- Split Small / DynamicReverseSmall / Small-пила / BigCore remainder → NewFar не реализованы.
- MT5 compile/tester не запускались из-за отсутствия MetaEditor в контейнере.
- Runtime restart подтверждён модельными pytest и code-path интеграцией, но терминальный restart в MT5 должен быть выполнен отдельно.

## Итоговый вердикт

Архитектурная целостность Split Big замкнута на StateIntegrity, Reconciliation, PositionResolution, Pending/Retry, SaveState/RecoverState, Reserve Ledger и actual partial accounting на уровне кода и локальных pytest. Для полной приёмки остаются внешние MT5 compile/tester проверки.
