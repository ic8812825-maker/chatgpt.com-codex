# MQL5-like Big Scenario Engineering Audit

No MQL5 trading logic was changed. This document describes the Python replay model and its MT5 L1 gate.

## Flow audited

Initial Lock -> positive initial close is recorded as `InitialIgnoredProfit` and excluded from BigScenarioNet -> remaining losing initial position is Far -> Big opens opposite Far -> Small opens with Far -> Big closes -> Small closes -> `BigScenarioNet = ClosedBigNet + ClosedSmallNet` -> `CloseFarBudget = BigScenarioNet * CloseFarShare` -> `ReserveAdd = BigScenarioNet * ReserveShare` -> partial Far close uses only CloseFarBudget -> reserve is accumulated for full cycle completion -> RecoveryPL/ReserveCoverage decide final close or next level.

## MT5 L1 gate

The search is aborted unless Python reproduces the supplied MT5 L1 values for BigNet, SmallNet, BigScenarioNet, CloseFarBudget, ReserveAdd, CloseFarLot, RemainingFar, RecoveryPL direction and next state.

| Metric | Python | MT5 | Diff | Status |
|---|---:|---:|---:|---|
| BigNet | 147.73 | 147.73 | 0.0 | PASS |
| SmallNet | -40.9 | -40.9 | 0.0 | PASS |
| BigScenarioNet | 106.83 | 106.83 | 0.0 | PASS |
| CloseFarBudget | 80.1225 | 80.1225 | 0.0 | PASS |
| ReserveAdd | 26.7075 | 26.7075 | 0.0 | PASS |
| CloseFarLot | 0.29 | 0.29 | 0.0 | PASS |
| RemainingFar | 0.71 | 0.71 | 0.0 | PASS |
| NextState | OPEN_BIG_L2 | OPEN_BIG_L2 | MATCH | PASS |

## Reserve audit

The Python model mirrors the audited invariant: partial Far close uses `CloseFarBudget` only. `ReserveAfter` is updated separately from `ReserveAdd`; reserve participates only in the final completion check through remaining-loss coverage.

## Formula audit

- `BigLot = NormalizeLotNearest(FarLot * BigRatio)`.
- `SmallLot = NormalizeLotUp(BigLot * SmallRatio)`.
- `BigScenarioNet = ClosedBigNet + ClosedSmallNet`.
- `CloseFarBudget = BigScenarioNet * CloseFarShare`.
- `ReserveAdd = BigScenarioNet * ReserveShare`.
- `CloseFarShare + ReserveShare = 1.00`.
- `CloseFarLot = NormalizeLotDown(CloseFarBudget / FarLossPerLot)`.
- `RecoveryPL = ReserveAfter - RemainingFarLoss`.
- `ReserveCoverage = ReserveAfter / RemainingFarLoss` when remaining loss is positive.