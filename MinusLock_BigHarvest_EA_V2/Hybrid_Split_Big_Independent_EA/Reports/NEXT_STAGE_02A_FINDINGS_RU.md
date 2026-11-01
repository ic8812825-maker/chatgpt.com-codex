# HSBI NEXT STAGE 02A — реестр выводов

Baseline: `6bb6a2f75f8fb0d5d51b1259476ddc47477eaaa3`. Аудит выполнен без изменения production-кода.

| ID | Приоритет | Статус | Вывод | Влияние |
|---|---:|---|---|---|
| M-01 | P0 | FAIL | `consumptionKey.sourceDealKey/sourceAllocationKey` не сравниваются с соответствующими ключами `reserveAllocationSource` | Чужой allocation source может быть использован как формально допустимый Reserve; New Far получает ложный Catch-Up PASS |
| M-02 | P0 | FAIL | New Far формирует expected identity копированием identity из проверяемого proof | Equality не доказывает существование broker deal/event и provenance суммы |
| M-03 | P1 | CONFLICT / DECISION_REQUIRED | Allocation validator требует `sum <= allocatableNet`; документ 08 подразумевает полное распределение, документ 32 допускает верхнюю границу | Возможен необъяснённый остаток либо ложный reject после ужесточения |
| M-04 | P1 | UNPROVEN | `recoveryMoney=basketNetMoney` обозначает projected сумму четырёх ног, а не settled fund | Прогноз может быть ошибочно принят за доступные деньги |
| M-05 | P1 | FAIL | `reserveGainMoney=max(0, Core+Trend+Small)` включает Small, хотя допустимый Reserve proof ограничен BigCore/BigTrend | При `0+0+10` поле даёт 10 без разрешённого Reserve source |
| M-06 | P1 | DECISION_REQUIRED | `farLossIncreaseMoney` реализован как absolute loss; название допускает incremental interpretation | Catch-Up margin различается на baseline loss |
| M-07 | P1 | DECISION_REQUIRED | Projected transition loss и actual realized transition loss используют одну семантическую область | Риск-оценка может быть смешана с accounting |
| M-08 | P1 | DECISION_REQUIRED | Buffer вычитается в каждой ноге и дополнительно в Catch-Up | Возможно корректное независимое покрытие либо двойное вычитание |
| PERSIST-01 | P0 | UNPROVEN | Production persistence — stub; SHA-256 persistence не реализован | Restart guarantees не существуют end-to-end |
| REPLAY-01 | P0 | UNPROVEN | Catch-Up видит только один caller-supplied prior key; `hasPriorConsumption=false` снимает replay check | Reserve может снова стать доступным после неполного восстановления |
| BROKER-01 | P1 | NOT_RUN | Нет свежего `OrderCalcProfit/OrderCalcMargin` на реальном symbol/account | Broker-specific money и margin не доказаны |
| TEST-01 | P1 | FAIL as full proof | R12A canonicalizer при прямом запуске хеширует пустой ledger и не читает production MQL5 | Его exit 0 нельзя считать proof денежной реализации |
| TEST-02 | P1 | UNPROVEN | R12A causal checks подтверждают Python evaluator, но source mutations второго блока не начаты | `SECOND_BLOCK_ACCEPTANCE=NOT_GRANTED` |
| TEST-03 | P2 | FAIL | Frozen R7 verifier на текущем дереве: 57/62; status/manifest markers устарели | Исторический seal нельзя применять как актуальный acceptance gate |
| TRADE-01 | — | PASS | В 74 production-файлах нет `OrderSend`, `CTrade`, `PositionOpen/Close`, `TRADE_ACTION_`, `OnTradeTransaction` | No-trade guard сохранён |

## Минимальный контрпример M-01

Пусть allocation source содержит `sourceDealKey=D1`, `sourceAllocationKey=A1`, а consumption key — `sourceDealKey=D2`, `sourceAllocationKey=A2`, при корректных `planId`, `stateRevision`, ненулевом `consumptionEventId` и непустом `consumer`. `HSBI_ValidateReserveAllocationSource(source)` и `HSBI_ValidateReserveConsumption(key, plan, revision)` могут одновременно вернуть true. В `HSBI_EvaluateReserveCatchUp` нет cross-object equality для D1/D2 и A1/A2. При остальных положительных условиях Catch-Up способен пройти.

## Минимальный контрпример M-02

Создать projected proof с синтаксически валидным, но несуществующим `sourceDealId=999999` и `sourceEventId=888888`. New Far присваивает эту identity proof, затем передаёт `expectedReserveIdentity=reserveSourceProof.identity`. Проверка same-identity проходит, хотя authoritative ledger не запрашивался.

## Граница вывода

Локальные validators в основном fail-closed и полезны. Дефекты относятся к provenance и связи объектов, а не к отсутствию всех защит. Аудит не утверждает, что реальный double spend уже происходил: торговый и persistence pipeline отсутствуют. Он доказывает, что текущие контракты не способны запретить его при будущем подключении pipeline.
