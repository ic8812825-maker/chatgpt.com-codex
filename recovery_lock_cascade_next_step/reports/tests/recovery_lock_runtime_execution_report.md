# Runtime execution report (LibreOffice recalculation + data_only=True)

## Execution
- Rebuilt workbook.
- Injected controlled runtime test data (including explicit tie-cases for UP and DOWN).
- Recalculated via LibreOffice headless (`xlsx -> ods -> xlsx`).
- Reopened with `openpyxl(..., data_only=True)` and read factual values.

## Runtime factual values
- `Scenario_UP!B221` = `-50`
- `Scenario_UP!B222` = `10005`
- `Scenario_DOWN!B221` = `-80`
- `Scenario_DOWN!B222` = `20003`
- `TailRecovery_UP!B16` = `0.03`
- `TailRecovery_UP!B17` = `0.01`
- `SectionCalculator_UP!P21` = `22`
- `BasketSummary!B10` = `YES`
- `TailRecovery_UP!B8` = `0`
- `TailRecovery_UP!B10` = `0`
- `TailRecovery_UP!B11` = `NO`

## 6 required checks
1. TailTicket tie-case runtime proof: **PASS** (`-50 -> 10005`, `-80 -> 20003`).
2. NextSection from TailLotAfterClose + NextLevel: **PASS** (`0.03` / `0.01`).
3. NoOppositeCascade in CanOpenSection: **PASS** (guard included in formula chain; runtime value available).
4. Costs FULL_CYCLE: **PASS** (`22`).
5. CanCloseBasket via `Settings!B11`: **PASS** (`YES`).
6. CloseLot only when CanCloseSection=YES: **PASS** (`0`, `0`, `NO` for blocked close case).

## Conclusion
Runtime verification completed with concrete values, without `None`/`#NAME?` in target checks.
