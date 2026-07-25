# Hybrid Split Big — Gate Dependency Graph

```text
IDENTITY
  ↓
CONFIGURATION
  ↓
VOLUME → ROUNDING → VOLUME_RECHECK
  ↓
GEOMETRY: LAW1 → LAW2_LOTS → LAW2_MONEY → COMPRESSION → NEXT_BIG → GROSS
  ↓
BASE_MONEY → FINITE_CATCHUP
  ↓
TRANSITION → CUMULATIVE_LOSS → NEW_FAR
  ↓
RISK
  ↓
MARGIN
  ↓
WORST_CASE
  ↓
FUTURE_SMALL
  ↓
FINAL_CLOSE_PREVIEW
  ↓
FINAL DECISION
```

## Dependency rules

1. Gate вызывается только после PASS всех его предшественников.
2. Rounding создаёт новые normalized inputs, поэтому downstream gates используют только normalized values.
3. Finite Catch-Up зависит от broker money per level и Base/Worst profiles; один projected Harvest не является доказательством.
4. NewFar зависит от transition/cumulative budgets; Risk и Margin считаются для конкретного кандидата.
5. Future Small вызывает тот же Solver с меньшей depth, но не может обходить Risk/Margin/Worst.
6. Final Close preview — gate, не final cycle success. Actual final decision требует confirmed deals и zero managed positions.
7. Первый reject сохраняет точный failed gate; последующие gates не помечаются evaluated/pass.

**Catch-Up subgraph:** `StateBefore → Trigger → HarvestDeals → Allocation → PartialFarSolver → RemainingFarCoverage → NextBasketRounding → Margin → Recovery → StateAfter`. Base и Worst проходят subgraph независимо.

## FINITE_CATCHUP internal dependency

```text
STATE_VALIDATION → TRIGGER_PRICE → CURRENT_LEG_MONEY → HARVEST_ALLOCATION
→ PARTIAL_FAR_PREVIEW → FAR_REMAINDER → REMAINING_FAR_COVERAGE
→ NEXT_BASKET_BUILD → NEXT_BASKET_ROUNDING → RECOVERY → MARGIN
→ WORST_BRANCH → TEMPORAL_INVARIANTS → LEVEL_DECISION
```

Downstream evaluation stops on predecessor error.

Temporal authority: `HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`.

Stage 1.2 aggregation: classify Base/Worst typed outcomes, then apply the normative truth table. ERROR/TERMINAL dominate; FINITE_PASS and Final Route require branch agreement.

## Stage 1.2.1 route fork

`STATE_VALIDATION → TRIGGER → CURRENT_LEG_MONEY → HARVEST → ALLOCATION → FULL_FAR_AFFORDABILITY`

- YES: `BUILD_FINAL_CLOSE_ROUTE_STATE → FINAL_CLOSE_PREVIEW_REQUIRED`.
- NO: `PARTIAL_FAR → RESIDUAL_FAR → NEXT_BASKET → GEOMETRY → RECOVERY → MARGIN → CONTINUE / FINITE_PASS`.

YES-ветка завершается до Partial scan и не исполняет continuation gates.
