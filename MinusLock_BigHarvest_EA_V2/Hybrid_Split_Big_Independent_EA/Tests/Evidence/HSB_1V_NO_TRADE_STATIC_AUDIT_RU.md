# HSB.1V — статический аудит запрета торгового исполнения

Дата повторной проверки: 2026-08-11 UTC. Область: все `*.mq5` и `*.mqh` независимого каталога.

## Выполненные команды

```bash
rg -n 'OrderSend(Async)?\s*\(|\bCTrade\b|Position(Open|Close|ClosePartial)\s*\(|\b(Buy|Sell)\s*\(|TRADE_ACTION_(DEAL|PENDING)' MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA --glob '*.{mq5,mqh}'
rg -n 'Trade/Trade\.mqh|Legacy|ReverseSmall|TradeEngine|DUAL_TAIL|#include.*MinusLock_BigHarvest_EA_V2' MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA --glob '*.{mq5,mqh}'
rg -n 'REAL_TRADING_ALLOWED|realAccountAllowed|brokerRequestsAllowed' MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include --glob '*.mqh'
```

Первые две команды не нашли совпадений. Третья подтвердила compile-time `HSBI_REAL_TRADING_ALLOWED=false`, fail-closed runtime policy и проверки context. Собственный `HSBI_StateMachine.mqh` не является старым production StateMachine и содержит только pure transitions. Структура допускает хранение ровно одного Far; попытка наблюдать второй Far отклоняется context/invariant validators как conflict.

```text
PRODUCTION_TRADE_CALLS=0
TRADE_ACTION_CONSTANTS=0
FORBIDDEN_TRADE_INCLUDE=0
LEGACY_DEPENDENCIES=0
OLD_STATE_MACHINE_DEPENDENCIES=0
OLD_TRADE_ENGINE_DEPENDENCIES=0
DUAL_TAIL=0
SECOND_FAR_ALLOWED=NO
TRADING_IMPLEMENTED=NO
REAL_TRADING_ALLOWED=NO
NO_TRADE_GUARD=PASS
```
