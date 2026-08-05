# 3.1.6.3.4 — аудит OnTick и FSM dispatch

## Фактический путь

```text
OnTick
→ CountManagedOpenPositions
→ IsTradingAllowedSafe (результат только записывается в Ctx.riskGateOk)
→ RunPeriodicReconciliation
→ early return только для RECOVERY_MISMATCH / INTEGRITY_ERROR / POSITION_RESOLUTION_ERROR
→ UpdateGeometryPanel
→ при STATE_IDLE и 0 positions: OpenInitialLock напрямую
→ иначе RunStateMachine
```

`RunStateMachine()` сначала вызывает `ValidateScenarioIsolation()` и `TradingOperationAllowedDuringRecovery()`, затем dispatch по глобальному `State`.

Для `STATE_FAR_ACTIVE` выбор режима начинается с `UseSplitBigGeometry`. При true вызывается `PrepareSplitBigLevel()` и переход к `STATE_SPLIT_BIG_OPEN_CORE`; Hybrid не имеет отдельной верхней ветки, а модифицирует Split functions через `UseHybridSplitBigGeometry`.

## Доказанные ответы

- Сценарий выбирает монолитный `RunStateMachine` плюс state-specific functions.
- Legacy/Split выбирается в FSM по bool flags; Hybrid является условием внутри Split path.
- `HybridDecisionEngine` не является верхним dispatcher OnTick.
- Hybrid preview может существовать внутри `PrepareSplitBigLevel`, но irreversible action выполняется state functions из смешанного `StateMachine.mqh`.
- При `STATE_IDLE` `OpenInitialLock()` вызывается напрямую до общего FSM validation этого тика.
- `riskOk` сам по себе не создаёт ранний return; закрытия и часть FSM продолжаются, а разрешение открытия зависит от внутренних caller gates.
- Повторный tick потенциально повторно входит в state action; защита зависит от немедленного изменения State/pending fields и не основана на transaction event.

## Замечания

| ID | Критичность | Содержание |
|---|---|---|
| TICK-001 | P1 | Hybrid не является самостоятельным production dispatcher; он встроен в Split FSM. |
| TICK-002 | P1 | Direct emergency `OpenInitialLock()` вызывается до `RunStateMachine` и общей scenario-isolation проверки. |
| TICK-003 | P1 | FSM допускает advance на основании synchronous trade wrapper, так как transaction-confirmed barrier отсутствует. |
| TICK-004 | P2 | Risk gate result записывается в context, но OnTick не блокирует dispatch централизованно; безопасность распределена по state handlers. |
| TICK-005 | P2 | Reconciliation periodicity зависит от поступления ticks; отдельный timer path не доказан. |

## Классификация

- OnTick: `MIXED_MODE`, `PARTIAL`, `UNSAFE`.
- FSM dispatch: `LEGACY_ACTIVE + SPLIT_ACTIVE + HYBRID_PARTIAL`.
- Production MQL5 не изменялся.
