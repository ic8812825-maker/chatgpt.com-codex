# Аудит Runtime Decision Validator HSB.2D-V1

Проверены immutable context; Account/Symbol/Magic/CycleID/PlanID; schema, money-state и state revision; EventID/ActionID; market/cost/allocation freshness; reconciliation; фактическое чтение и ownership position; residual identifier/ticket/volume; aggregate Future Small; New Far binding; independent Catch-Up; money/margin/risk proof identity; allocation/consumption; persistence и digest. Все отказы возвращаются fail-closed с `valid=false`.

`HSBI_DECISION_VALID` означает только успешную валидацию решения и **не** разрешает trade request. `requiredNextState=HSBI_STATE_RECONCILING` намеренно требует последующей сверки: validator не мутирует FSM и не подтверждает broker outcome.

`RUNTIME_DECISION_STATIC_AUDIT=PASS`; runtime confirmation не выполнялась.
