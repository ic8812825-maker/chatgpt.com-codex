# Аудит money/allocation/consumption HSB.2D-V1

Статически подтверждены нормативные инварианты:

1. Initial profit не является Recovery source; opening `IN` не принимается как closing harvest.
2. Reserve и Partial Far имеют раздельные allocation buckets; Partial Far ограничен своим budget.
3. Сумма allocations не превышает allocatable net, а `alreadyConsumed` — allocation.
4. Source deal/allocation key, PlanID и StateRevision входят в consumption binding; reuse/conflict блокируется, duplicate не списывает повторно.
5. Account/Symbol/Magic/CycleID и broker-confirmed proof identity обязательны.
6. Final Reserve допускается только нормативным контрактом; projected/simulated/injected proof не подменяет production actual realized money.
7. Persistence preparation и digest обязательны до advance.

Нормативные ratios, Reserve/Partial Far, Final Reserve, New Far, Future Small и Catch-Up не изменялись.

```text
MONEY_CONSERVATION_STATIC_AUDIT=PASS
ALLOCATION_CONSUMPTION_STATIC_AUDIT=PASS
PERSISTENCE_STATIC_AUDIT=PASS
BROKER_MONEY_RUNTIME_PROOF=NOT_EXECUTED_MT5_UNAVAILABLE
```
