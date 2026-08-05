# Initial Lock и создание исходного Far

Версия 1.0. Статус: нормативный.

## Последовательность

1. Создать immutable InitialPlan.
2. Persist BUY Action; отправить BUY; дождаться actual fill.
3. Persist SELL Action; отправить SELL; дождаться actual fill.
4. При невозможности SELL создать отдельный rollback BUY action и подтвердить close deal.
5. В `INITIAL_LOCK_ACTIVE` отслеживать trigger broker-money моделью.
6. При trigger определить прибыльную leg, persist close action, подтвердить actual close.
7. Mark closed leg INITIAL_PLUS и исключить её DealNet из recovery.
8. Оставшуюся actual position назначить FAR и commit cycle snapshot.

- `HSBI-INIT-001`: FAR не создаётся до actual close INITIAL_PLUS.
- `HSBI-INIT-002`: Initial Profit не попадает в RealizedCycleNet, FinalReserve или PartialFarBudget.
- `HSBI-INIT-003`: rollback подтверждается transaction outcome.
- `HSBI-INIT-004`: обе initial legs имеют один CycleID, разные identifiers/tickets и строгие roles.
- `HSBI-INIT-005`: clean start доказан только при отсутствии managed positions, pending actions и persisted active cycle.

## BUY/SELL и ошибки

BUY fill использует Ask, SELL fill Bid; close BUY Bid, close SELL Ask. Partial fill каждой opening action остаётся pending. Foreign/duplicate legs → reconciliation. Restart допустим после любого шага и восстанавливает InitialPlan/Action/fills.

## Контракт

Вход: StartLot broker-valid, fresh market, risk PASS. Выход: ровно один FAR. Preconditions: IDLE, clean start. Postconditions: initial plus excluded, ledgers empty для recovery, Far identity persisted. Запрещено: эвристически выбирать Far, продолжать после failed rollback, создавать basket до commit Far. Owner: Scenarios/InitialLock + Execution. Тесты: BUY/SELL failure, partial fill, restart each phase, same Magic foreign position. Открытые вопросы: trigger и timeout policy.