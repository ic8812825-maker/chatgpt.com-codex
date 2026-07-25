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
