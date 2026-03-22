# ALE_FUNCTION_AUDIT

## Function-level testing matrix (critical groups)

| Group | Function | Edge cases tested | Result |
|---|---|---|---|
| Geometry | `CALFixedStep::BuildGrid`, `CALLogGeometry::BuildGrid` | monotonic levels, large depth, extreme step/base | PASS |
| Volume ordering | lot progression checks (sim audit + geometry rebuild) | large depth, growth pressure, over-control case | PASS/PARTIAL (depends on config) |
| Average price / exposure | `CALPositionBook::PnLAtPrice`, `CALExposureFlow::Recalculate` | position add/update invariance, extreme prices | PASS |
| PnL | `PnLAtPrice` + simulator PnL invariants | sign checks, linearity trend, stress spreads/slippage | PASS |
| Collapse logic | simulator `L1/L2/L3` conditions | boundary and adversarial edges | PASS |
| Risk control | `adaptive_k`, block/allow actions, preemptive compression behavior | normal, overkill, delayed control | PASS |
| FSM | `CALStateMachine::TransitionBySignal` | legal/illegal transitions, SAFE fallback | PASS |
| Estimator quality | `estimate_realtime_pcollapse` | calibration error, Brier, ROC-AUC | PASS (bounded) |

## Mandatory fails captured

1. **Lyapunov function-level tests unavailable** (`V(state)` not found in repo code).
2. In overkill setup, strategy degrades to near no-trade; correctly flagged as bad regime.

## Structure-agnostic compliance

No architecture rewrite performed. All checks were adapted to existing files and execution surface.
