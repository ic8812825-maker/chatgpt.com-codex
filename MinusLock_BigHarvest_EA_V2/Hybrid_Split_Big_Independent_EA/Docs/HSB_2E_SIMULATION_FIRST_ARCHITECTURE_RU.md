# HSB.2E simulation-first architecture

`IHSBI_BrokerAdapter` задаёт immutable intent/outcome API. `HSBI_SimulatedBrokerAdapter` — единственная разрешённая первая реализация; она моделирует fills, partial fills, rejection, timeout, duplicate и out-of-order events детерминированно. `HSBI_DemoBrokerAdapter=NOT_IMPLEMENTED`; `HSBI_RealLimitedBrokerAdapter=NOT_IMPLEMENTED`. Scenario engines создают decisions/intents и никогда не вызывают торговый API. Demo adapter допускается лишь в 2E.13 после отдельного решения; real adapter не разрешён этим планом.
