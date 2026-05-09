# Runtime execution report (recalculated via LibreOffice + data_only=True)

## Steps executed
1. Opened `recovery_lock_cascade_next_step.xlsx`.
2. Injected runtime test inputs into `reports/tests/recovery_lock_runtime_case.xlsx`.
3. Recalculated by round-trip through LibreOffice headless (`xlsx -> ods -> xlsx`).
4. Reopened the recalculated workbook with `openpyxl(..., data_only=True)`.

## Runtime values read from workbook
- `Scenario_UP!B222 (TailTicket)` = `N/A`
- `TailRecovery_UP!B16 (NextBigLotAfterRecovery)` = `#NAME?`
- `TailRecovery_UP!B17 (NextSmallLotAfterRecovery)` = `#NAME?`
- `SectionCalculator_UP!B14 (CanOpenSection)` = `#NAME?`
- `SectionCalculator_UP!K21 (Costs)` = `#NAME?`
- `BasketSummary!B10 (CanCloseBasket)` = `YES`
- `TailRecovery_UP!B8 (CloseLotRaw)` = `0`
- `TailRecovery_UP!B10 (CloseLotFinal)` = `0`
- `TailRecovery_UP!B11 (CloseAllowed)` = `NO`

## Interpretation
- Runtime recalculation is now **executed** (not blocked).
- Cells using newer Excel functions (`XLOOKUP`, `LET`) are not fully compatible in this LibreOffice path and evaluate to `#NAME?`.
- Cells not depending on unsupported functions are computed and returned as concrete values (`YES`, `0`, `NO`).

## Conclusion
- The runtime pipeline with recalculation + `data_only=True` is confirmed working.
- For fully numeric PASS on all 6 checks in LibreOffice, formulas must be refactored to LibreOffice-compatible alternatives (replace `XLOOKUP`/`LET`).
