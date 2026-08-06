# HSBI-DEC-005 — objective NewFar Solver

Статус: `RESOLVED`.

Solver перечисляет broker-valid остатки исходного BigCore от `MinimumOperationalFarLot` до `<OldFar`, с шагом SYMBOL_VOLUME_STEP. Candidate допускается только после compression, next basket, RecoveryPL, Reserve Catch-Up, risk, margin, Future Small, finite catch-up и terminal-operability gates.

Нормативный выбор: минимальный безопасный actual target residual. Solver планирует requested close, но NewFar создаётся только из фактического остатка того же BigCore ticket/identifier после fills. Tie-break: меньший RiskNext, меньшая MarginNext, меньше expected transitions, больший safety buffer, меньший N.

Reject: пустое ValidCandidates; кандидат ниже operational lot; следующий цикл невозможен; actual residual не совпадает с допустимым broker candidate. Owner: `Planning/NewFarSolver`. Tests: deterministic enumeration, tie-break, requested-vs-actual, coarse step, no-candidate.
