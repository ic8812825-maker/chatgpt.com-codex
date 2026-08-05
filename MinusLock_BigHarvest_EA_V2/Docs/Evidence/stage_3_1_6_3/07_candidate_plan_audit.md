# 3.1.6.3.7 — CandidatePlan и Hybrid Decision Engine

`EvaluateHybridCandidate()` создаёт `HybridCandidatePlan`, присваивает `planId=TimeCurrent()`, `cycleId`, timestamp и snapshot fingerprint. Проверяются identity, config, role lots, rounding, volume, Law 1, Law 2, projected money, finite catch-up, NewFar compression, NextBig, gross, risk, margin, worst case и Future Small depth 1.

## Доказанные недостатки

1. PlanID строится из секундного `TimeCurrent()`, поэтому уникальность нескольких планов в одну секунду не доказана.
2. В plan отсутствует доказанная StateRevision binding как обязательный execution gate.
3. `EvaluateHybridCandidate()` зануляет plan и строит fixed raw NewFar от `TargetNewFarRatio`; minimum-safe дискретный solver здесь не выполняется.
4. Risk определяется как `oldRisk=max(0,-projectedHarvestNet)`, затем `nextRisk=oldRisk*TargetNewFarRatio`; это запрещённая упрощённая формула, а не broker-money risk до control price.
5. Future Small проверяется только `Depth1`.
6. Final Close preview безусловно помечается PASS при `finalCloseAvailable=false`; реальный gate этим evaluator не доказан.
7. Decision engine формирует preview, но irreversible execution остаётся в `StateMachine.mqh` и может повторно рассчитывать target/close lots.
8. Persistence immutable plan до первого ордера и сравнение полного gate mask непосредственно в open handler не доказаны.

## Замечания

- `PLAN-001 P1`: CandidatePlan не соответствует полному immutable production contract.
- `PLAN-002 P1`: fixed `TargetNewFarRatio` используется вместо minimum-safe solver.
- `PLAN-003 P1`: risk формула не соответствует нормативному broker-money control-price risk.
- `PLAN-004 P1`: Final Close gate фактически заглушен в aggregate evaluator.
- `PLAN-005 P2`: Future Small ограничен depth 1.
- `PLAN-006 P2`: PlanID/StateRevision/fingerprint lifecycle неполон.

Классификация: `HYBRID_PREVIEW_ONLY / PARTIAL / CONFLICTING`.
