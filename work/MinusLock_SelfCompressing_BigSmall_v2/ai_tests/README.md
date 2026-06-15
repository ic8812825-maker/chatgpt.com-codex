# AI Simulation Harness — MinusLock BigHarvest

This harness mirrors the MQL5 EA math without requiring MetaTrader. It does **not** replace MT5 Strategy Tester.

## Run

```bash
python work/MinusLock_SelfCompressing_BigSmall_v2/ai_tests/parameter_sweep.py
python -m pytest work/MinusLock_SelfCompressing_BigSmall_v2/ai_tests/test_scenarios.py -q
```

## Outputs

- `reports/ai_cycle_math.csv`
- `reports/ai_cycle_math.md`
- `reports/parameter_sweep_results.csv`
- `reports/best_parameters.md`
- `reports/ai_test_report.md`

## Scope

The model checks Big-harvest, Small-at-Far, reverse geometry, reserve coverage, `FinalCloseAllowed`, `STOP_MAX_LEVELS`, and parameter sweeps. Python results identify candidates only; final confirmation must be done in MT5 Strategy Tester.
