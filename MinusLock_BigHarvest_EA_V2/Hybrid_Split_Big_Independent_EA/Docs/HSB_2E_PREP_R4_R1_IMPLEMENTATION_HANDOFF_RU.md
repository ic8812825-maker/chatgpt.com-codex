# HSB.2E PREP-R4-R1 — implementation handoff

Следующий этап может быть только отдельно разрешённым `HSB.2E-IMPL-01`: immutable status/reason, identity/snapshot/position/deal/policy/broker-intent DTO, serialization, digest и compile-only tests. Торговые формулы, FSM mutation и dispatch исключены.

Дальнейшие блоки: grid → deal money → Initial Lock → Big allocation → Small shares → Reserve/exactly-once → persistence/restart → FSM → disabled request builder. Demo review и real trading требуют отдельных административных решений.

`BROKER_DISPATCH_ALLOWED=NO`; `REAL_TRADING_ALLOWED=NO`; `TRADING_LOGIC_START_ALLOWED=NO`.
