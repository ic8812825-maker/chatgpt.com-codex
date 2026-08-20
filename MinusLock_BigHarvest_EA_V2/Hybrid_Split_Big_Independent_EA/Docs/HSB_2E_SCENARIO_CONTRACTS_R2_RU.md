# HSB.2E-PREP-R2 — scenario decision contracts

Каждый сценарий проходит identity → snapshot → immutable intent → persistence → simulation → reconciliation → FSM commit. Реальные broker calls запрещены.

| ID | Scenario | Initial | Status/reason | Negative path | Tests |
|---|---|---|---|---|---|
| SC01 | Initial Lock | HSBI_STATE_READY | HSBI_DECISION_VALID/HSBI_RD_OK | identity mismatch fails before intent | T465, T600 |
| SC02 | Big level | HSBI_STATE_READY | HSBI_DECISION_VALID/HSBI_RD_OK | identity mismatch fails before intent | T466, T601 |
| SC03 | Small reversal | HSBI_STATE_READY | HSBI_DECISION_VALID/HSBI_RD_OK | identity mismatch fails before intent | T467, T602 |
| SC04 | partial Far | HSBI_STATE_READY | HSBI_DECISION_VALID/HSBI_RD_OK | identity mismatch fails before intent | T468, T603 |
| SC05 | final Far close | HSBI_STATE_READY | HSBI_DECISION_VALID/HSBI_RD_OK | identity mismatch fails before intent | T469, T604 |
| SC06 | restart/reconciliation | HSBI_STATE_RECONCILIATION_REQUIRED | HSBI_DECISION_RECONCILIATION_REQUIRED/HSBI_RD_RECONCILIATION_CONFLICT | identity mismatch fails before intent | T470, T605 |
| SC07 | transaction retry | HSBI_STATE_RECONCILIATION_REQUIRED | HSBI_DECISION_RECONCILIATION_REQUIRED/HSBI_RD_RECONCILIATION_CONFLICT | identity mismatch fails before intent | T471, T606 |
| SC08 | invalid geometry | HSBI_STATE_RECONCILIATION_REQUIRED | HSBI_DECISION_RECONCILIATION_REQUIRED/HSBI_RD_RECONCILIATION_CONFLICT | identity mismatch fails before intent | T472, T607 |
| SC09 | maximum levels | HSBI_STATE_RECONCILIATION_REQUIRED | HSBI_DECISION_RECONCILIATION_REQUIRED/HSBI_RD_RECONCILIATION_CONFLICT | identity mismatch fails before intent | T473, T608 |
| SC10 | risk gate | HSBI_STATE_RECONCILIATION_REQUIRED | HSBI_DECISION_RECONCILIATION_REQUIRED/HSBI_RD_RECONCILIATION_CONFLICT | identity mismatch fails before intent | T474, T609 |
| SC11 | stale snapshot | HSBI_STATE_RECONCILIATION_REQUIRED | HSBI_DECISION_RECONCILIATION_REQUIRED/HSBI_RD_RECONCILIATION_CONFLICT | identity mismatch fails before intent | T475, T610 |
| SC12 | broker rejection/partial fill | HSBI_STATE_RECONCILIATION_REQUIRED | HSBI_DECISION_RECONCILIATION_REQUIRED/HSBI_RD_RECONCILIATION_CONFLICT | identity mismatch fails before intent | T476, T611 |
