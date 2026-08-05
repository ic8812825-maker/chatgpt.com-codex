# State Machine Hybrid Split Big

Версия 1.0. Статус: нормативный.

## Состояния

`STATE_DISABLED, STATE_IDLE, STATE_INITIAL_PLAN_READY, STATE_INITIAL_OPENING_BUY, STATE_INITIAL_OPENING_SELL, STATE_INITIAL_LOCK_ACTIVE, STATE_INITIAL_PLUS_CLOSING, STATE_FAR_ACTIVE, STATE_CANDIDATE_PLANNED, STATE_BASKET_OPENING_CORE, STATE_BASKET_OPENING_TREND, STATE_BASKET_OPENING_SMALL, STATE_BASKET_ACTIVE, STATE_BIG_HARVEST_PLANNED, STATE_BIG_HARVEST_EXECUTING, STATE_ALLOCATION_PENDING, STATE_FINAL_CLOSE_PLANNED, STATE_FINAL_CLOSE_EXECUTING, STATE_PARTIAL_FAR_PLANNED, STATE_PARTIAL_FAR_EXECUTING, STATE_SMALL_TRANSITION_PLANNED, STATE_SMALL_CLOSING, STATE_OLD_FAR_CLOSING, STATE_BIG_TREND_CLOSING, STATE_BIG_CORE_REDUCING, STATE_NEW_FAR_VALIDATING, STATE_RECONCILING, STATE_TERMINAL_SAFE, STATE_CYCLE_CLOSED`.

- `HSBI-FSM-001`: FSM не продвигается после send request.
- `HSBI-FSM-002`: переход разрешён только после persisted confirmed transaction outcome.
- `HSBI-FSM-003`: в каждый момент разрешена максимум одна pending irreversible action.
- `HSBI-FSM-004`: restart входит через RECONCILING, кроме доказанного CLEAN_START.
- `HSBI-FSM-005`: TERMINAL_SAFE запрещает opens/promotions/allocation; допускает только явно разрешённые защитные действия.
- `HSBI-FSM-006`: transition table не содержит Legacy/Split states.

## Контракт состояния

Каждое состояние определяет допустимые roles, persisted fields, входные events, одну action authority, timeout и выходы. Opening states требуют persisted PlanID/ActionID и accumulated fills. Closing states требуют ownership tuple и expected volume. `STATE_NEW_FAR_VALIDATING` допускает ровно один BIG_CORE residual и не отправляет сделки.

## Ошибки и restart

Reject оставляет state в planned/pending до явного outcome; timeout → RECONCILING; conflict → TERMINAL_SAFE. Restart восстанавливает snapshot, action registry и actual MT5 facts до любого перехода.

## Owner и тесты

Owner: `Core/StateMachine`; Execution лишь публикует typed outcomes. Тесты: полный transition matrix, forbidden transitions, duplicate event, partial fill, restart в каждом state. Открытые вопросы: timeouts и emergency permissions.