# HSB.2A — no-trade static audit

Дата: 2026-08-11 UTC. Проверены все `*.mq5`/`*.mqh` независимого каталога командой нормативного regex для запрещённых trade calls/constants. Результат: `0 matches`. Отдельный dependency guard для Trade library, legacy engine/roles и dual-tail также дал `0 matches`.

Единственные broker API calls расчётного слоя:

- `OrderCalcProfit` — 1 вызов в `HSBI_BrokerMoneyModel.mqh`;
- `OrderCalcMargin` — 1 вызов в `HSBI_BrokerMarginModel.mqh`.

Они только возвращают projected DTO, не принимают Context/ledger/FSM и не отправляют заявки.

```text
PRODUCTION_TRADE_CALLS=0
TRADE_ACTION_CONSTANTS=0
FORBIDDEN_TRADE_INCLUDE=0
LEGACY_DEPENDENCIES=0
TRADING_IMPLEMENTED=NO
TRADE_REQUESTS_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
HSB_2B_STARTED=NO
STATIC_NO_TRADE_AUDIT=PASS
```
