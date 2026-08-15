# Traceability HSB.2C-R1-P2

- Canonical policy: `HSBI_RuntimePolicy.mqh`.
- Compatibility enum facade: `HSBI_RuntimeMode.mqh`.
- Consumers: Context/main EA, Preflight, ExternalOutcome, FutureSmall, NewFar, ReserveCatchUp.
- Include graph: 69 headers, 110 local edges, zero cycles and duplicate guards.
- Tests: T401–T430; full declared range T01–T430.
- Audits: duplicate definitions, no-trade, shortcuts, allocation and scope.
- Runtime compile/tests: user verification required.
