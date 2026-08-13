# HSB.2C-R1 — journal chain

Append требует `candidate.id == last.id + 1` и строго свежий EventID. Full-chain validator проверяет каждый digest, previous link, ID/event monotonicity, scope и lifecycle: completion требует предшествующую successful reconciliation; повторный completion и pending после completion запрещены.
