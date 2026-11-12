# DG01 — зависимости и безопасная граница

```mermaid
flowchart TD
 A[Owner semantic choices] --> I[Local versioned economic identity API]
 A --> C[Captured codec and MQL domain approval]
 C --> N[Native compile and goldens]
 I --> N
 B[Independent broker namespace/history] --> P[Independent EA-origin provider]
 P --> R[Reconciled immutable economic registry]
 R --> L[Allocation vector identity]
 L --> G[Global source attribution and remaining grant]
 G --> D[Durable journal and atomic commit/CAS]
 D --> V[Journal-aware available funds]
 V --> K[Catch-Up/NewFar composed proof]
 Q[Risk/margin/quotes/costs independent providers] --> K
 K --> F[Full execution FSM and broker reconciliation]
```

Ветви можно проверять независимо. Native-tested local identity не зависит от выбора Transition Loss для чистого comparator, но не разрешает funding/торговлю. Independent provider и durable backend не создаются bool-флагами test fixture. D-01/D-03..D-07/CR-09 могут быть deferred для локального API, но не для дальнейшего финансового использования. Прямые prerequisites Minimal: D-02/D-08, выбранная schema/domain, compatibility policy; serialization требует NUM-CODEC. Нет автоматической цепочки approval→implementation.

Global funding требует source uniqueness по полному broker/account namespace across allocations, логического source lifetime, reversals/transfers policy и реального complete history. Exactly-once требует backend locking/CAS/crash-recovery ordering; serialized Python revision simulation — только specification. Rollback/migration неизвестных records не решаются временным присвоением текущего account.
