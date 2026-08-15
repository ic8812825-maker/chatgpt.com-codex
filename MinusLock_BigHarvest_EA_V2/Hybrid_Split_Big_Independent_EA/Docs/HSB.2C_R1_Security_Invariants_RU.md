# HSB.2C-R1 — security invariants

Intent проверяет finite volumes/price, identity, sources, snapshots, side, timestamps, status и digest. Snapshot не доверяет только внешнему digest: каждый вложенный intent валидируется и сопоставляется со scope snapshot.

Preflight не изменяет Context/ledger. COMPLETED возможен только после runtime-terminal reconciliation с фактически прочитанными position/deal.
