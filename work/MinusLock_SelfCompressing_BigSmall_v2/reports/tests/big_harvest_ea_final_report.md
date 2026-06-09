# Big-Harvest MQL5 EA — Final Placement and Verification Report

## Project Folder

```text
work/MinusLock_SelfCompressing_BigSmall_v2/MinusLock_BigHarvest_EA/
```

The EA was copied into the required working project folder:

```text
work/MinusLock_SelfCompressing_BigSmall_v2
```

## Required Target Folder Entries

Verified present locally:

```text
README.md
MANUAL_v2.md
TEST_REPORT_MinusLock_SelfCompressing_BigSmall_v2.md
MinusLock_SelfCompressing_BigSmall_v2.xlsx
tests/
MinusLock_BigHarvest_EA/
```

## Compile Result

Blocked by environment limitation.

Checked commands:

```bash
command -v metaeditor64
command -v MetaEditor64.exe
command -v metaeditor
```

Result: no MetaEditor executable is installed in this Linux container.

Required external FULL PASS step on Windows/MetaTrader:

```text
Open work/MinusLock_SelfCompressing_BigSmall_v2/MinusLock_BigHarvest_EA/MinusLock_BigHarvest_EA.mq5
Compile in MetaEditor
Expected: 0 errors, 0 critical warnings
```

## Strategy Tester Result

Blocked by environment limitation.

Checked commands:

```bash
command -v terminal64
command -v terminal64.exe
command -v metatester64
```

Result: no MetaTrader Strategy Tester executable is installed in this Linux container.

Required external FULL PASS settings:

```text
Mode: Every tick based on real ticks
Symbol: EURUSD
Timeframe: H1 or M15
Period: 2018.03.31 – 2018.04.30
StartLot: 1.00, 2.00, 5.00
AllowRealTrading: false
UseMarketOrders: true
```

## Repository-Local Tests Passed

The following available checks passed for both the root EA and the target-folder EA copy:

```bash
python scripts/verify_big_harvest_ea.py
python work/MinusLock_SelfCompressing_BigSmall_v2/scripts/verify_big_harvest_ea.py
git diff --check
```

Coverage:

```text
static checks
math verification
Big-harvest verification for StartLot 1/2/5
Small-scenario verification
DUAL_TAIL expectation verification
FinalClose math verification
journal field verification
risk-gate static verification
no formula violations in local harness
no cycle violations in local harness
```

## Big-Harvest Result

Verified locally by harness:

```text
StartLot 1.00: Level 3 FinalCloseAllowed = true, FinalClosePL = +4.80
StartLot 2.00: Level 3 FinalCloseAllowed = true, FinalClosePL = +11.40
StartLot 5.00: Level 3 FinalCloseAllowed = true, FinalClosePL = +29.15
```

## Small-Scenario Result

Verified locally by harness:

```text
Far = 1.00
Big = 1.30
Small = 0.48
CloseBig = 0.39
RemainBig = 0.91
NetSmall = +9.00
```

## DUAL_TAIL Result

Verified statically and by harness expectation:

```text
old Far still exists + remaining 70% Big > 0
=> dualTailDetected = true
=> State = STATE_DUAL_TAIL
=> new Big/Small level is not opened
```

## FinalClose Result

Verified locally by harness:

```text
FinalCloseAllowed = YES on Level 3 for StartLot 1/2/5
FarRemainLoss is covered by TotalReserve
State-machine code closes Far and transitions to STATE_CLOSED_PROFIT
STATE_CLOSED_PROFIT branch does not open new levels
```

## InitialProfitIgnored

Verified statically:

```text
Ctx.initialProfitIgnored = true
Ctx.totalReserve = 0.0
Ctx.cycleFinalPL = 0.0
```

The first initial-lock profit is logged and is not added to Reserve, Recovery, or CloseFar.

## CloseFarLotRounded Confirmed

Verified locally by harness and static code path:

```text
CloseFarBudget = NetProfit × 0.90
CloseFarLotRaw = CloseFarBudget / (FarDistancePoints × PointValuePerLot)
CloseFarLotRounded = FLOOR(CloseFarLotRaw, LotStep)
FarLotAfter = FarLotBefore - CloseFarLotRounded
```

No `FarLot × 90%` close formula is used by the harness or state-machine close path.

## Risk Gates Result

Verified statically:

```text
MaxSpreadPoints
MaxMarginPercent
AllowRealTrading
UseMarketOrders
IsTradingAllowedSafe()
```

`OnTick()` returns before `RunStateMachine()` if risk gates fail.

## Git Remote Result

Executed:

```bash
git remote -v
git remote add origin https://github.com/ic8812825-maker/chatgpt.com-codex.git
git fetch origin work --prune
```

Result: `origin` is now configured and `git fetch origin work` succeeded.

## Push Status

Not pushed.

Reason: the user's instruction says push is allowed only after FULL PASS, and FULL PASS requires MetaEditor compile-check and Strategy Tester. Those executables are not installed in this container, so pushing would violate the task's own safety gate.

Required next step on a Windows/MetaTrader host after successful MetaEditor + Strategy Tester FULL PASS:

```bash
git push origin work
```

## What Was Done

1. Ensured `origin` remote exists and fetched `origin/work`.
2. Copied `MinusLock_BigHarvest_EA/` into `work/MinusLock_SelfCompressing_BigSmall_v2/MinusLock_BigHarvest_EA/`.
3. Copied verification harness and reports into `work/MinusLock_SelfCompressing_BigSmall_v2/`.
4. Updated target project README with links to the EA and report.
5. Re-ran available local checks from both root and target folders.
6. Did not push because FULL PASS is blocked by missing MetaEditor/Strategy Tester.

## GitHub URL

```text
https://github.com/ic8812825-maker/chatgpt.com-codex/tree/work/work/MinusLock_SelfCompressing_BigSmall_v2
```
