# Спецификация Big Harvest

Версия 1.0. Статус: нормативный.

## Порядок

Big trigger → fresh revalidation → immutable HarvestPlan → persist actions → закрыть плановые BIG_CORE/BIG_TREND/SMALL_BASE legs по контракту → подтвердить все actual deals → Economic Ledger → Allocation Ledger → проверить единый Final Close → иначе Partial Far → reconcile actual Far → следующий CandidatePlan.

- `HSBI-BIG-001`: Harvest использует только roles текущего StateRevision.
- `HSBI-BIG-002`: realized money — сумма непересекающихся confirmed closing deals.
- `HSBI-BIG-003`: allocation выполняется exactly once после завершения всех source deals.
- `HSBI-BIG-004`: Final Close оценивается до Partial Far.
- `HSBI-BIG-005`: Partial Far не использует FinalReserve.
- `HSBI-BIG-006`: следующий basket запрещён до settlement/reconciliation.
- `HSBI-BIG-007`: каждый level имеет уникальные PlanID/ActionID/EventKey.

## Money и directions

FAR SELL: Big BUY profits закрываются по Bid; SMALL_BASE SELL close по Ask. FAR BUY зеркален. Commission/swap/fee включаются в DealNet. Negative eligible harvest не создаёт allocation credits.

## Ошибки/restart

Partial/reject/unknown deal удерживает `STATE_BIG_HARVEST_EXECUTING` или переводит в RECONCILING. Restart восстанавливает список expected actions и source deals; повторная allocation запрещена.

## Контракт

Вход: active basket, trigger, fresh snapshot. Выход: actual harvest ledger, allocations, reconciled Far. Preconditions: no pending, ownership/risk PASS. Postconditions: closed planned roles или explicit pending; conservation. Owner: Scenarios/BigHarvest. Тесты: оба направления, multi-deal fills, costs, duplicate events, restart before/after allocation. Открытые вопросы: точный состав legs каждого Harvest profile.