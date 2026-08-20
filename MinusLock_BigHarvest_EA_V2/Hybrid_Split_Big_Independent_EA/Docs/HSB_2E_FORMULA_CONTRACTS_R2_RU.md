# HSB.2E-PREP-R2 — нормативные formula contracts

Формулы здесь специфицируются, но не реализуются. Источником realized P&L служат только подтверждённые deals; partial Far не использует Reserve; прибыль закрытой плюсовой стартовой позиции исключается.

| ID | Formula | Units | Rounding | Fail closed |
|---|---|---|---|---|
| F001 | InitialLockSelection | account currency and lots | money to currency digits only after deal aggregation | nonfinite input, stale identity, invalid grid, or missing ticket |
| F002 | PositiveStartProfitIgnored | account currency and lots | money to currency digits only after deal aggregation | nonfinite input, stale identity, invalid grid, or missing ticket |
| F003 | RemainingNegativeBecomesFar | account currency and lots | money to currency digits only after deal aggregation | nonfinite input, stale identity, invalid grid, or missing ticket |
| F004 | Big | account currency and lots | money to currency digits only after deal aggregation | nonfinite input, stale identity, invalid grid, or missing ticket |
| F005 | Small | account currency and lots | money to currency digits only after deal aggregation | nonfinite input, stale identity, invalid grid, or missing ticket |
| F006 | BigCore | account currency and lots | money to currency digits only after deal aggregation | nonfinite input, stale identity, invalid grid, or missing ticket |
| F007 | BigTrend | account currency and lots | money to currency digits only after deal aggregation | nonfinite input, stale identity, invalid grid, or missing ticket |
| F008 | CloseBigOnSmall | account currency and lots | money to currency digits only after deal aggregation | nonfinite input, stale identity, invalid grid, or missing ticket |
| F009 | RemainBigOnSmall | account currency and lots | money to currency digits only after deal aggregation | nonfinite input, stale identity, invalid grid, or missing ticket |
| F010 | CloseFarShare | account currency and lots | money to currency digits only after deal aggregation | nonfinite input, stale identity, invalid grid, or missing ticket |
| F011 | ReserveShare | account currency and lots | money to currency digits only after deal aggregation | nonfinite input, stale identity, invalid grid, or missing ticket |
| F012 | SmallReserveShare | account currency and lots | money to currency digits only after deal aggregation | nonfinite input, stale identity, invalid grid, or missing ticket |
| F013 | RecoveryPL | account currency and lots | money to currency digits only after deal aggregation | nonfinite input, stale identity, invalid grid, or missing ticket |
| F014 | ReserveCoverage | account currency and lots | money to currency digits only after deal aggregation | nonfinite input, stale identity, invalid grid, or missing ticket |
| F015 | PartialFar | account currency and lots | money to currency digits only after deal aggregation | nonfinite input, stale identity, invalid grid, or missing ticket |
| F016 | FinalFarClose | account currency and lots | money to currency digits only after deal aggregation | nonfinite input, stale identity, invalid grid, or missing ticket |
| F017 | BigScenario | account currency and lots | money to currency digits only after deal aggregation | nonfinite input, stale identity, invalid grid, or missing ticket |
| F018 | SmallScenario | account currency and lots | money to currency digits only after deal aggregation | nonfinite input, stale identity, invalid grid, or missing ticket |
| F019 | Reverse | account currency and lots | money to currency digits only after deal aggregation | nonfinite input, stale identity, invalid grid, or missing ticket |
| F020 | NewFar | account currency and lots | money to currency digits only after deal aggregation | nonfinite input, stale identity, invalid grid, or missing ticket |
| F021 | FutureSmall | account currency and lots | money to currency digits only after deal aggregation | nonfinite input, stale identity, invalid grid, or missing ticket |
| F022 | ReserveCatchUp | account currency and lots | money to currency digits only after deal aggregation | nonfinite input, stale identity, invalid grid, or missing ticket |
| F023 | MaximumReversals | account currency and lots | money to currency digits only after deal aggregation | nonfinite input, stale identity, invalid grid, or missing ticket |
| F024 | RecoveryPLMonotonic | account currency and lots | money to currency digits only after deal aggregation | nonfinite input, stale identity, invalid grid, or missing ticket |
| F025 | FarReduction | account currency and lots | money to currency digits only after deal aggregation | nonfinite input, stale identity, invalid grid, or missing ticket |
| F026 | ReserveAccumulation | account currency and lots | money to currency digits only after deal aggregation | nonfinite input, stale identity, invalid grid, or missing ticket |
| F027 | BigToSmall | account currency and lots | money to currency digits only after deal aggregation | nonfinite input, stale identity, invalid grid, or missing ticket |
| F028 | SymbolMagicTicketOwnership | account currency and lots | money to currency digits only after deal aggregation | nonfinite input, stale identity, invalid grid, or missing ticket |
