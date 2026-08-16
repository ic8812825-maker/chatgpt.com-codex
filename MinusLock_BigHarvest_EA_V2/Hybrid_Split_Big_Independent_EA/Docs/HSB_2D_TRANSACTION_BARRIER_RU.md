# HSB.2D — Transaction Decision Barrier

`HSBI_CanAdvanceRuntimeDecision` требует admission PASS, свежие snapshots/event, ожидаемый ActionID, reconciliation, actual position/ticket/volume/direction/ownership, runtime money/margin/risk, persistence и digest. Retry сохраняет ActionID/PlanID/CycleID/StateRevision. Завершённый идентичный payload даёт `NO_OP`, изменённый — `CONFLICT`. Торговый request не создаётся.
