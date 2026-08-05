# 3.1.6.3.14 — Risk Manager и terminal-safe routes

## Проверенные категории

Spread, margin, drawdown, managed-position limit, invalid geometry, max harvest levels, reverse limit, mismatch, position resolution, state integrity, persistence/recovery failure, orphan positions и manual intervention.

## Фактическое поведение

- `IsTradingAllowedSafe()` формирует risk gate; OnTick сохраняет результат в `Ctx.riskGateOk`.
- Risk gate проектировался так, чтобы не блокировать closes/retry, но blocking новых opens распределён по handlers.
- Mismatch/integrity/position-resolution states дают ранний return в OnTick.
- Существуют inputs `CloseAllOnInvalidGeometry`, `CloseFarOnMaxLevels`, `StopOnRiskGateBlocked`, `StopOnReverseLimit`.
- Invalid/max-limit paths могут инициировать реальные close actions, но единый normative RecoveryPL gate перед safety close не доказан.
- Trade close wrapper проверяет current Symbol+Magic после ticket selection, что снижает foreign-close риск, однако CycleID+identifier не проверяются непосредственно в wrapper.

## Риски

- `RISK-001 P0`: generic ticket close не выполняет атомарную проверку Symbol+Magic+CycleID+identifier+role; защита зависит от корректности caller context.
- `RISK-002 P1`: `CloseAllOnInvalidGeometry` может превратить validation failure в irreversible close без единого Hybrid money/risk plan.
- `RISK-003 P1`: `CloseFarOnMaxLevels` может закрыть Far по policy, не доказывая positive RecoveryPL.
- `RISK-004 P1`: terminal reason/state taxonomy смешивает Legacy/Split/Hybrid.
- `RISK-005 P2`: risk gate не централизован; каждый open handler должен корректно применять его отдельно.

## Итог

Terminal-safe infrastructure существует, но часть routes является emergency-close policy, а не доказанным Hybrid terminal-safe contract. Классификация: `PARTIAL / UNSAFE`.
