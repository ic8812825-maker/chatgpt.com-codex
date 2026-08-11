# HSB.1V — статический аудит запрета торговли

Дата: 2026-08-10 UTC. Область: все `*.mq5` и `*.mqh` независимого каталога.

## Команды

```bash
rg -n -i 'OrderSendAsync|OrderSend|CTrade|PositionOpen|PositionClosePartial|PositionClose|TRADE_ACTION_DEAL|TRADE_ACTION_PENDING|trade[ _-]?request' . --glob '*.{mq5,mqh}'
rg -n -i 'Trade/Trade\.mqh|Legacy|ReverseSmall|DUAL_TAIL|\.\./\.\./.*MinusLock|TradeEngine' . --glob '*.{mq5,mqh}'
rg -n '\b(Buy|Sell)\s*\(' . --glob '*.{mq5,mqh}'
rg -n '^#include' . --glob '*.{mq5,mqh}'
```

## Результат

- Production trade calls: `0`.
- Торговые request/action constants: `0`.
- Вызовы `Buy(...)` / `Sell(...)`: `0`. Имена `HSBI_DIRECTION_BUY/SELL` и документальные state/role identifiers не являются вызовами.
- `Trade/Trade.mqh`, внешние/старые include, Legacy, ReverseSmall, старый TradeEngine и DUAL_TAIL: `0`.
- Include directives проверено: `84`; они остаются внутри независимого проекта или стандартного MQL5 compile context.
- Старый StateMachine не подключён; `HSBI_StateMachine.mqh` является собственным чистым контрактом текущего проекта.
- Второй Far отклоняется validator-ом; policy всегда запрещает broker requests и real account.

```text
HSB_STAGE_1_NO_TRADE_GUARD=PASS
PRODUCTION_TRADE_CALLS=0
TRADING_IMPLEMENTED=NO
TRADE_REQUESTS_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
```
