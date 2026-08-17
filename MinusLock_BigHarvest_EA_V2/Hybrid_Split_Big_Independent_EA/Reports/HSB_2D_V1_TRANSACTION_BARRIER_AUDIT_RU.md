# Аудит Transaction Barrier HSB.2D-V1

Admission validator вызывается первым. Проверены completed Action, одинаковый payload → `NO_OP`, иной payload → conflict, freshness/reconciliation, новый EventID, ActionID, фактическая position и ticket/volume/direction/ownership, money/margin/risk, persistence и digest. Barrier не отправляет сделки, не мутирует FSM/ledger и не признаёт simulated outcome завершением.

`expectedEventId` — последний уже применённый Event ID, `context.eventId` — новый кандидат; поэтому `context.eventId <= expectedEventId` корректно блокирует stale/replay. Retry сохраняет ожидаемый ActionID; новый ActionID не трактуется как retry.

`TRANSACTION_BARRIER_STATIC_AUDIT=PASS`; broker dispatch отсутствует.
