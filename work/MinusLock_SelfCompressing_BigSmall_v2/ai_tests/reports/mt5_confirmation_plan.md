# MT5 Confirmation Plan — Python Candidate 50/50

> 50/50 является кандидатом, найденным Python simulation harness. Финально подтверждается только через MT5 Strategy Tester.

## Общие настройки

- Symbol: EURUSD
- Timeframe: M30
- Period: 2024.09.01 - 2024.11.13
- StartLot: 1.00
- BigRatio: 1.30
- InitialTriggerPoints: 100
- BigMoveLevel1/2/3: 100 / 150 / 200
- FarDistancePoints: 200
- MaxReverseCycles: 10
- EnableCycleMathCsv: true

Для каждого теста сохранить:

- Strategy Tester report
- `MQL5/Files/MinusLock_CycleMath.csv`
- Experts journal with `CYCLE_MATH`
- OnTester value
- Final state
- Last deal comment

## Test 1 — Current bad variant

```text
UseRecommended5050Preset = false
SmallRatio = 0.37
CloseBigOnSmall = 0.30
RemainBigOnSmall = 0.70
CloseFarShare = 0.90
ReserveShare = 0.10
MaxHarvestLevels = 5
```

Expected: `STOP_MAX_LEVELS` or FAIL. Confirm whether `FinalCloseAllowed` never becomes `YES`.

## Test 2 — Python candidate 50/50

```text
UseRecommended5050Preset = true
SmallRatio effective = 0.36
CloseBigOnSmall effective = 0.35
RemainBigOnSmall effective = 0.65
CloseFarShare effective = 0.50
ReserveShare effective = 0.50
MaxHarvestLevels effective = 5
MaxReverseCycles effective = 10
```

Expected from Python model: `STATE_CLOSED_PROFIT`. MT5 must confirm with real spread/commission/swap.

## Test 3 — Neighbor control 60/40

```text
UseRecommended5050Preset = false
SmallRatio = 0.36
CloseBigOnSmall = 0.35
RemainBigOnSmall = 0.65
CloseFarShare = 0.60
ReserveShare = 0.40
MaxHarvestLevels = 5
MaxReverseCycles = 10
```

Expected: compare against 50/50 by final state, OnTester, drawdown, `TotalReserve`, and `FarRemainLoss` before final close.

## Pass / Fail interpretation

- PASS candidate: `STATE_CLOSED_PROFIT`, `FinalCloseAllowed=YES`, no open EA positions at test end, `OnTester > 0`.
- FAIL candidate: `STATE_UNCLOSED_CYCLE`, `STOP_MAX_LEVELS`, `OnTester=-1`, or end-of-test open positions.
