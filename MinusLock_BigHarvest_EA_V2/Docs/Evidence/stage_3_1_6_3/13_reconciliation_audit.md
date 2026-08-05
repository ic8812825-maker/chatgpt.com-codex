# 3.1.6.3.13 — reconciliation и восстановление состояния

## Точки запуска

- `OnInit` после `RecoverState`, orphan/state/integrity checks.
- `OnTick` через `RunPeriodicReconciliation()`.
- Отдельные Small/close handlers вызывают локальные reconciliation/verification functions.
- Mismatch routes используют `STATE_RECOVERY_MISMATCH`, `STATE_POSITION_RESOLUTION_ERROR`, `STATE_INTEGRITY_ERROR`, `STATE_SMALL_RECONCILIATION_FAILED` и manual intervention.

## Что проверяется

Symbol, Magic, tickets, identifiers, directions, actual volume, role topology, orphan positions, missing positions, Reserve reconstruction/consistency и некоторые persisted transaction fields.

## Ограничения

- Общего transaction-event source с состояниями DISCOVERED→RECONCILED→APPLIED→PERSISTED для actual deals в production MQL5 нет.
- Reconciliation основан на snapshot polling positions/history и не знает parent request EventID.
- Делayed/duplicate transaction не обрабатывается в момент события.
- При двух потенциальных Far безопасный deterministic ownership contract не доказан; topology mismatch блокируется, но автоматический выбор запрещён не единым typed outcome.
- Outcomes представлены множеством FSM states/reason strings, а не единым enum `RECONCILED/PENDING/CONFLICT/REJECTED/TERMINAL_SAFE/CLEAN_START`.
- Periodic запуск tick-dependent.

## Замечания

- `RECON-001 P1`: reconciliation не связан с OnTradeTransaction и parent events.
- `RECON-002 P1`: altered/delayed history exactly-once validation неполна.
- `RECON-003 P1`: единая typed outcome model отсутствует.
- `RECON-004 P1`: FSM может выполнить synchronous state advance до reconciliation.
- `RECON-005 P2`: periodic reconciliation зависит от ticks.

Классификация: `MAPPED_PARTIAL / MIXED_MODE / UNSAFE`.
