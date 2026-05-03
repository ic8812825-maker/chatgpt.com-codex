# Detailed Final Verdict (All Test Reports)

Date: 2026-05-02

## 1. Automated Test Execution
- Command: `pytest -q tests`
- Result: 53 passed

## 2. Backtest Reports Status Matrix
| Report | Status | Note |
|---|---|---|
| backtest_report_BTCUSD_H1.md | FAIL | real OHLCV (Yahoo) |
| backtest_report_BTCUSD_M15.md | INSUFFICIENT_DATA | real OHLCV (Yahoo) |
| backtest_report_BTCUSD_M5.md | INSUFFICIENT_DATA | real OHLCV (Yahoo) |
| backtest_report_EURUSD_H1.md | FAIL | real OHLCV (Yahoo) |
| backtest_report_EURUSD_M15.md | INSUFFICIENT_DATA | real OHLCV (Yahoo) |
| backtest_report_EURUSD_M5.md | INSUFFICIENT_DATA | real OHLCV (Yahoo) |
| backtest_report_GBPUSD_H1.md | FAIL | real OHLCV (Yahoo) |
| backtest_report_GBPUSD_M15.md | INSUFFICIENT_DATA | real OHLCV (Yahoo) |
| backtest_report_GBPUSD_M5.md | INSUFFICIENT_DATA | real OHLCV (Yahoo) |

## 3. Reports/tests Templates Presence
- backtest_report.md: present
- excel_validation_report.md: present
- forward_test_report.md: present
- risk_test_report.md: present
- scenario_test_report.md: present
- unit_test_report.md: present

## 4. Consolidated Findings
- Unit/Scenario/Integration/Regression/Stress suites pass (53/53).
- Real-market reports exist for 3x3 matrix (EURUSD/GBPUSD/BTCUSD x M5/M15/H1).
- M5/M15 remain data-depth constrained at Yahoo source; statuses should not be treated as market-proof validation when coverage is low.
- H1 runs on 500-day window per current provider constraint.

## 5. Final Global Verdict
**Current System Status: PRE-PRODUCTION / MODIFY**

Rationale:
1. Calculation and logic tests pass.
2. Reporting pipeline is complete.
3. Market profitability is not yet confirmed as production-grade due data-depth/source constraints for full 3-year intraday validation.