# HSB.2B-R — no-trade и shortcut audit

Дата: 2026-08-11 UTC.

Нормативный regex запрещённых trade APIs по всем `*.mq5`/`*.mqh` дал `0 matches`. Разрешённые calculation-only calls находятся только в `HSBI_BrokerMoneyModel.mqh` (`OrderCalcProfit`) и `HSBI_BrokerMarginModel.mqh` (`OrderCalcMargin`); execution functions отсутствуют.

Отдельный поиск production `Include` по прежним линейным полям (`projectedRecoveryMoneyPerLevel`, `riskDecreasePerLevel`, `transitionLossPerLevel`, `reserveGainPerLot`, `farLossPerLot`, `marginPerLot`, `riskImprovementPerLot`, `transitionLossPerLot`, `grossExposurePerLot`) дал `0 matches`.

```text
PRODUCTION_TRADE_CALLS=0
ALLOWED_CALCULATION_CALLS=2
LINEAR_SHORTCUT_REFERENCES_IN_INCLUDE=0
LINEAR_SHORTCUT_GUARD=PASS_STATIC
TRADING_IMPLEMENTED=NO
REAL_TRADING_ALLOWED=NO
HSB.2C=NOT_STARTED
NO_TRADE_GUARD=PASS
```
