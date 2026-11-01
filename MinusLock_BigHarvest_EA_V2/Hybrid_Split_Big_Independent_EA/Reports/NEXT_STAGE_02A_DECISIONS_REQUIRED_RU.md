# HSBI NEXT STAGE 02A — решения администратора

Ни одно из решений ниже не принято автоматически. До их фиксации экономическая модель и production-функции изменяться не должны.

## D-01. Полное или частичное allocation

Выбрать нормативный контракт:

1. Полное: `Reserve + PartialFar + Transition + Carry + Residual + Consumed = AllocatableDealNet` с денежным tolerance.
2. Частичное: сумма может быть меньше; тогда нужны отдельный `Unallocated`, допустимые состояния, срок reconciliation и запрет расходования нераспределённой суммы.

Рекомендация аудитора: полное распределение в устойчивой записи; частичное допустимо только как явно типизированное промежуточное transaction state.

## D-02. Семантика RecoveryMoney

Утвердить разные названия и типы для:

- `ProjectedBasketNetAtControlPrice`;
- `ActualRealizedCycleNet`;
- `AllocatedRecoveryFund`;
- `AvailableReserve`.

Projected basket не должен становиться settled/available без confirmed deals и allocation.

## D-03. Разрешённые источники Reserve

Подтвердить, что Reserve создаётся только из actual positive DealNet разрешённых ролей BigCore/BigTrend. Решить, является ли положительный Small доходом Carry/Residual/Transition или другим bucket. До решения Small не считать Reserve.

## D-04. FarLossIncrease

Выбрать:

- absolute: `max(0,-FarNetCurrent)`;
- incremental: `max(0,LossCurrent-LossBaseline)`.

Зафиксировать baseline snapshot, price side, costs и момент обновления. Для Catch-Up эти определения дают разные результаты.

## D-05. TransitionLoss

Разделить projected risk metric и actual accounting metric. Определить, какая из них применяется к risk cap, какая записывается в ledger, и запрещён ли переход до получения actual fills.

## D-06. Safety buffers

Утвердить назначение per-leg buffer и Catch-Up buffer. Если они независимы, описать покрываемые риски и запрет overlap. Если общий бюджет один, определить агрегацию без повторного вычитания.

## D-07. Idempotent replay outcome

Определить exact replay как отдельный `NO_OP` status либо оставить `REJECT` с NOOP reason. Любой вариант обязан гарантировать отсутствие новой allocation, consumption, state revision и broker action.

## D-08. Авторитетный provenance

Утвердить владельца цепочки `Broker Deal → Actual Ledger → Allocation → Consumption`: терминальная история сделок плюс durable append-only journal рекомендуется как источник истины. Caller-supplied booleans и self-copied identity недостаточны.

## D-09. Допуск этапа 02B

Разрешить remediation только после решений D-01–D-08. Разрешение не включает broker dispatch, торговые заявки или изменение геометрии Big/Small/New Far.
