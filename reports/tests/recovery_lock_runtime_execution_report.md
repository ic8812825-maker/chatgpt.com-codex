# Runtime execution report (data_only=True)

## What was executed
1. Loaded `recovery_lock_cascade_next_step.xlsx`.
2. Injected test inputs (NextLevel/TailLotAfterClose, BasketFloating/Reserve, CostMode, etc.).
3. Saved runtime case as `reports/tests/recovery_lock_runtime_case.xlsx`.
4. Reopened with `data_only=True` and read target cells.

## Raw runtime readout
All formula cells returned `None` in this environment:
- `Scenario_UP!B222`
- `TailRecovery_UP!B16`
- `TailRecovery_UP!B17`
- `SectionCalculator_UP!B14`
- `SectionCalculator_UP!K21`
- `BasketSummary!B10`
- `TailRecovery_UP!B8`
- `TailRecovery_UP!B10`
- `TailRecovery_UP!B11`

Reason: `openpyxl` does not calculate Excel formulas; it only reads cached values written by Excel/Calc.
No local spreadsheet recalculation engine (LibreOffice/Excel) is available in this container.

## Result status
- Runtime `data_only=True` recalculation proof: **BLOCKED by environment**.
- Formula logic proof remains covered by explicit formula checks and deterministic scenario math in prior reports.
