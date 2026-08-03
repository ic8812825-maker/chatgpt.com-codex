# Этап 3.1.5 — нормативная денежная модель

```text
STAGE_3_1_4_STATUS=CLOSED
STAGE_3_1_5_AUTHORIZED=YES
STAGE_3_1_5_STARTED=YES
START_EXPECTED_HEAD=78fdcbc1bdbc982cde0898e65420cae1f759aa40
REPOSITORY_SCOPE=MinusLock_BigHarvest_EA_V2/{Docs,Tests,Tools}
PRODUCTION_TRADING_LOGIC_CHANGED=NO
```

Нормативный документ определяет статическую денежную семантику, но не доказывает исполнение MT5.

## Baseline проверок

Начальная ветка `work` синхронизирована с `origin/work`. Полный `pytest` до изменений остановлен
на collection: отсутствуют внешние `pandas` и `openpyxl`; это ограничение окружения и соседних
repository suites, а не результат Этапа 3.1.5.

## Термины, размерности и идентичность

Допустимые размерности: `LOT`, `PRICE`, `POINT`, `TICK`, `ACCOUNT_MONEY`, `RATIO`,
`INTEGER_RANK`, `BOOLEAN`, `EVENT_ID`, `DEAL_TICKET`, `POSITION_IDENTIFIER`.
`ProjectedMoney` — оценка; `DealNet` — подтверждённый экономический результат;
`RealizedCycleNet` — сумма уникальных managed deals; `FloatingLegCloseNow` — прогноз закрытия
actual volume; `RecoveryPLCloseNow` — realized плюс floating. Денежная идентичность задаётся
`AccountLogin + Symbol + Magic + CycleID`; позиция дополнительно имеет `PositionIdentifier/LegID`.
Сравнение lot с money, requested с actual и points с price без явного преобразования запрещено.

## Изоляция managed cycle

В Economic Ledger допускаются только записи с точным совпадением Account, Symbol, Magic и CycleID.
Manual trade, другой советник/символ/цикл, deposit, withdrawal, credit/balance correction исключаются.
`AccountBalanceNow-CycleStartBalance` запрещён как источник cycle P/L. При Initial Lock прибыль
закрытой плюсовой стартовой ноги помечается `INITIAL_IGNORED` до старта recovery cycle и не может
попасть в realized, Reserve, PartialFarBudget, Carry либо final-close gate.

## Projected broker money

Production semantic source — `OrderCalcProfit`. BUY закрывается по Bid, SELL — по Ask;
`SpreadPrice=Ask-Bid`, обе цены лежат на TickSize grid. Worst-case slippage сначала неблагоприятно
смещает control price и только затем вызывается расчёт. Oracle воспроизводит эту side-aware
семантику через Decimal и раздельные TickValueProfit/TickValueLoss; он не заменяет MT5.

## Actual deals и realized money

`DealNet=DEAL_PROFIT+DEAL_SWAP+DEAL_COMMISSION+DEAL_FEE` с фактическими знаками MT5.
IN, OUT, INOUT и OUT_BY сохраняются как entry type; каждый фактический DealTicket применяется
ровно один раз. Несколько fills агрегируются по actual volume/price/cost, а requested volume не
подменяет actual. Preview никогда не кредитует realized ledger и не завершает действие.

## Costs без двойного учёта

Spread учитывается только Bid/Ask. Projected slippage включается только в control price; actual
slippage — диагностическая разница, поскольку actual deal profit уже использует deal price.
Projected commission/fee являются estimate и заменяются actual после reconciliation. Commission,
swap и fee суммируются с их broker sign; знак по имени поля не инвертируется.

## Opening costs, partial fills и residual

`AllocatedEntryCost=UnallocatedEntryCost*ActualClosedVolume/PositionVolumeBefore`.
Распределение ведётся Decimal; последняя закрывающая часть получает весь rounding residual.
Частичный fill оставляет остаток volume и unallocated cost открытой позиции. Полное закрытие требует
нулевого остатка обоих полей после reconciliation.

## RecoveryPLCloseNow и EventSnapshot

`FloatingLegCloseNow=ProjectedProfit(actual lot, actual open, adverse control Bid/Ask)+CurrentSwap+ProjectedExitCommission+ProjectedExitFee`.
`RecoveryPLCloseNow=RealizedCycleNet+sum(FloatingLegCloseNow)`. Reserve, Carry, PartialFarBudget,
TransitionBudget и account balance delta не прибавляются. Before/after используют одну функцию.
Snapshot содержит identity, EventID, level/scenario/phase, Bid/Ask/spread, managed positions и actual
lots, economic totals, все allocation ledgers, costs/slippage diagnostic и reconciliation status.

## Два независимых ledger

Economic P/L Ledger хранит unique actual deals и floating close-now и единственный формирует
RecoveryPL. Allocation Ledger хранит tagged распределение уже realized positive harvest: PartialFar,
FinalReserve, Carry, TransitionBudget, Residual. Перемещение/расход allocation не создаёт P/L;
экономическая потеря закрытия Far появляется только в actual deal.

## Budgets и conservation

`AllocatableHarvestNet=PartialFarBudgetAdd+FinalReserveCredit+CarryAdd+TransitionBudgetAdd+Residual`.
Кредит разрешён только для positive, actual и reconciled harvest. FinalReserve — tagged subset,
только для final Far; PartialFar использует только PartialFarBudget. Projected/negative harvest не
кредитует бюджеты. Final Close требует reconciled managed state, актуальные prices/costs, отсутствие
pending/unknown fills, покрытие deficit Reserve, threshold RecoveryPLCloseNow и отдельные risk/margin gates.

## Exactly-once и restart reconciliation

Event key: AccountLogin, Symbol, Magic, CycleID, EventType, Level, Phase, PositionIdentifier,
DealTicket, AllocationType. Состояния: DISCOVERED, PENDING_RECONCILIATION, RECONCILED,
ALLOCATION_PENDING, APPLIED, PERSISTED. Повторный DealTicket/EventID — no-op. После restart ledger
и applied keys восстанавливаются до history replay; завершается только незавершённый transition,
credits/residual не повторяются. Следующее FSM-действие запрещено до reconciliation.

## Исполняемая коррекция 3.1.5.20–38

Normative proof теперь требует enum validation, broker grids, actual DealEntry semantics, immutable
EventSnapshot, полный reconciliation path, tagged allocation sources, serialized restart/replay и
ledger-derived Final Close. Имя mutation не является экономическим входом invariant evaluator.

## DealEntry semantics correction

IN открывает/увеличивает exposure и его price profit не является closing realized harvest. OUT и
OUT_BY закрывают, INOUT одновременно закрывает старую и открывает новую сторону; realized component
берётся из actual deal. BALANCE/CREDIT/CHARGE/CORRECTION исключены; standalone COMMISSION хранит
actual signed cost. Initial ignored и foreign identity исключаются до aggregation.

## Reconciliation terminal semantics

CONFLICT означает подтверждённое несовпадение identity/deals и является fail-closed terminal;
REJECTED означает нормативное отклонение события до allocation и также terminal. Оба запрещают
APPLIED и irreversible action. Повтор текущего состояния — idempotent no-op; PERSISTED terminal.

### Статус после третьей корректирующей приёмки (3.1.5.72)

```text
STAGE_3_1_5_VALIDATION=PASS
STAGE_3_1_5_STATUS=CLOSED
FRESH_CLONE_VERIFICATION=PASS
BLOCKING_COUNTERS=NONE
NEXT_ALLOWED_STAGE=3.1.6
STAGE_3_1_6_STARTED=NO
AWAITING_USER_APPROVAL=YES
REAL_TRADING_ALLOWED=NO
PRODUCTION_MQL5_IMPLEMENTATION=NOT_CHANGED
PRODUCTION_MQL5_MAPPING=PARTIAL
METAEDITOR_COMPILE=NOT_RUN
MT5_STRATEGY_TESTER=NOT_RUN
```

### Четвёртая корректирующая проверка 3.1.5.87

Исполняемые Python-доказательства прошли полную локальную проверку; независимая fresh-clone приёмка 3.1.5.88 ещё не завершена. Production MQL5 не изменялся.

```text
STAGE_3_1_5_STATUS=REOPENED_FOR_CORRECTION
NEXT_ALLOWED_STAGE=NONE
STAGE_3_1_6_START_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
PRODUCTION_MQL5_IMPLEMENTATION=NOT_CHANGED
PRODUCTION_MQL5_MAPPING=PARTIAL
METAEDITOR_COMPILE=NOT_RUN
MT5_STRATEGY_TESTER=NOT_RUN
```

### Итог 3.1.5.88

```text
FRESH_CLONE_VERIFICATION=PASS
BLOCKING_COUNTERS=NONE
STAGE_3_1_5_STATUS=CLOSED
NEXT_ALLOWED_STAGE=3.1.6
STAGE_3_1_6_STARTED=NO
AWAITING_USER_APPROVAL=YES
REAL_TRADING_ALLOWED=NO
```
