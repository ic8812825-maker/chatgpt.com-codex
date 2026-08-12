# HSB.2C — Preflight и lifecycle

Preflight fail-closed проверяет полный aggregate, independent Catch-Up/Far proof, runtime-confirmed sources, digests, Context identity, revision/cycle, freshness, broker grid, Bid/Ask side и отсутствие active/conflicting intent.

Lifecycle допускает только статические CREATED → PREFLIGHT_PASSED → PERSISTED → DISPATCH_BLOCKED → OUTCOME_PENDING/RECONCILING. COMPLETED возможен только после валидной reconciliation. Dispatch к брокеру отсутствует.
