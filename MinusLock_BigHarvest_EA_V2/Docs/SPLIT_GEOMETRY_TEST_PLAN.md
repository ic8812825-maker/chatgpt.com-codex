# Split Geometry Test Plan

Status: **SPLIT BIG IMPLEMENTED** / **SPLIT SMALL NOT IMPLEMENTED**.

## Local pytest

```bash
pytest -q MinusLock_BigHarvest_EA_V2/Tests/unit MinusLock_BigHarvest_EA_V2/Tests/static MinusLock_BigHarvest_EA_V2/Tests/scenario
```

Covered checks:

1. safe defaults and Legacy regression guard;
2. `STATE_FAR_ACTIVE` Split routing;
3. no `OpenBigSmall()` inside Split branch;
4. BigCore → SmallBase → BigTrend open sequence;
5. BigCore → BigTrend → SmallBase close sequence;
6. BUY/SELL target formula presence through BigCore open price logic;
7. lifecycle net filters by `DEAL_SYMBOL`, `DEAL_MAGIC`, `DEAL_POSITION_ID`;
8. commission, swap and fee included;
9. full Far check before partial;
10. Reserve is not used for partial budget;
11. numeric three-level Split Big scenario;
12. Small direction does not enter Legacy Small.

## MT5 required checks

MetaEditor compile and Strategy Tester remain required outside this Linux container. If not run, report:

```text
METAEDITOR_COMPILE = NOT_RUN
MT5_STRATEGY_TESTER = NOT_RUN
REAL_TRADING_ALLOWED = NO
```
