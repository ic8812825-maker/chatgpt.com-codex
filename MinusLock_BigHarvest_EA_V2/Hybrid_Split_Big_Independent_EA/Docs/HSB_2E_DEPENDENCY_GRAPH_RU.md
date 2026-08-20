# HSB.2E dependency graph

```text
Core → Planning/Money/Risk → Scenario decisions → Execution intent
→ Persistence journal → Simulated transaction adapter → Reconciliation → FSM commit
```

Broker adapter не изменяет FSM, Context, EconomicLedger, AllocationLedger, Reserve, Far или scenario state. Только подтверждённый outcome проходит через reconciliation и затем FSM commit. Циклические зависимости и прямые scenario→broker edges запрещены.
