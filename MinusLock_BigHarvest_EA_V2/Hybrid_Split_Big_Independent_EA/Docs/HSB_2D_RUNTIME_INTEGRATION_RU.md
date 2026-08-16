# HSB.2D — Runtime Integration

Runtime decision context является immutable DTO: identity, revision, actual residual, aggregate/candidate/Catch-Up, allocation, persistence и proof identities входят в fingerprint. Admission gate fail-closed проверяет runtime policy, identity, версии, freshness, reconciliation, actual position, полный aggregate, independent proofs, conservation, consumption и digest. Математика HSB.2A/2B повторно не рассчитывается.

`VALID` возможен только при runtime-confirmed money/margin/risk, полном Future Small aggregate, полном NewFar candidate и Catch-Up. Broker dispatch отсутствует.
