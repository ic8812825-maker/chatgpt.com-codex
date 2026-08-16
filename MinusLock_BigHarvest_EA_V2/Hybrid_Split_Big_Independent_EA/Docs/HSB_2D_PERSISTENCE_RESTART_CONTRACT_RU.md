# HSB.2D — Persistence и Restart

`HSBI_ValidateRestartedRuntimeState` является чистым validator. Он сопоставляет snapshot identity/digest, PlanID, revision, event/action, actual position, allocation и consumption. История, reused source, conflicting payload, изменённые ticket/volume/role/direction и unresolved pending блокируют решение. Идентичное повторное consumption возвращает `NO_OP`. Context/FSM/ledger/persistence не мутируются.
