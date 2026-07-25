# Hybrid Split Big — Money Flow

```text
Confirmed Harvest deals
          │
          ▼
   Actual HarvestNet
          │ max(net, 0)
          ▼
  Eligible Harvest E
          │
   ┌──────┼──────────────┐
   ▼      ▼              ▼
Partial  FinalReserve   Carry
 α=10%     β=90%       γ=0% + residual
   │         │             │
   ▼         ▼             ▼
Partial   Final Far      Rounding residual /
Far only  Close only     approved carry policy

Confirmed Transition credits ──► TransitionBudget ──► Transition close cost only
Confirmed deals ───────────────► RealizedCyclePL
Negative TransitionNet ────────► CumulativeTransitionLoss
```

## Forbidden edges

```text
FinalReserve -X-> Partial Far
FinalReserve -X-> Transition
FinalReserve -X-> Margin / Opens
PartialBudget -X-> Final Close / Transition / Opens
TransitionBudget -X-> Opens / Final Close
Projected money -X-> persisted bucket
```

Каждое ребро существует только после confirmed event. Allocation residual всегда идёт Carry. Reserve — защищённая классификация уже реализованной прибыли, а не новая прибыль.

## Sequential Harvest refinement

Каждый Harvest credit возникает из нового непересекающегося close set. `PartialBudgetBefore + PartialAdd - PartialFarCost = PartialBudgetAfter`; `PartialFarNet` одновременно входит в RealizedCyclePL. FinalReserve не является source или parameter Partial Far solver.

Open commission provenance: already-realized old-leg open costs are never debited again; projected reopen cost is recorded once in the new state; each projected close cost belongs to one disjoint close event.

Temporal authority: `HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`.
