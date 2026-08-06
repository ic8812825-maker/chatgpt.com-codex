# HSB.1 — статический аудит отсутствия торговли

Проверена область production-каркаса: `Hybrid_Split_Big_Independent_EA.mq5` и `Include/**/*.mqh`.

Запрещённые broker-execution зависимости и вызовы не используются. `Trade/Trade.mqh` не подключён. Execution-слой содержит только нейтральные DTO, outcome contracts и no-trade stub.

Результат:

```text
PRODUCTION_TRADE_CALLS=0
TRADE_LIBRARY_INCLUDED=NO
REAL_TRADING_PATH=ABSENT
HSBI_TRADING_IMPLEMENTED=false
HSBI_REAL_TRADING_ALLOWED=false
```

В документации и названии тестовых требований слова, описывающие будущие торговые действия, являются текстом и не считаются production-вызовами. No-trade stub всегда возвращает `success=false` и `HSBI_REASON_TRADING_NOT_IMPLEMENTED`.

Статус: PASS для статической архитектурной проверки HSB.1. Runtime broker proof не применим, поскольку broker execution отсутствует.