# HSB.2C — Idempotency и restart safety

Ключ: IntentID + ActionID + PlanDigest + StateRevision. Retry использует тот же ActionID и разрешён только в OUTCOME_PENDING, RECONCILING или DISPATCH_BLOCKED. После COMPLETED/REJECTED/EXPIRED/CONFLICT retry запрещён.

Restart принимает только свежий snapshot с валидным journal digest. Pending после completion, revision rollback, несколько active intents и повреждённая цепочка отклоняются.
