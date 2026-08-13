# 32. Reserve allocation и consumption

Allocation source фиксирует deal/allocation keys, policy version и разбиение allocatable net. Conservation требует, чтобы сумма Reserve, PartialFar, Transition, Carry, residual и already-consumed не превышала allocatable net.

При `alreadyAllocated=true` ReserveGainMoney равен подтверждённому `reserveAllocated` без повторного умножения на ReserveShare. Нужны valid, reconciled и confirmed allocation evidence; consumed source отклоняется.

Consumption key включает deal/allocation keys, PlanID, StateRevision, event и consumer. Идентичный повтор — NO-OP; тот же allocation key/event с иным payload — CONFLICT. Такой повтор не может дать valid Catch-Up или selected candidate.
