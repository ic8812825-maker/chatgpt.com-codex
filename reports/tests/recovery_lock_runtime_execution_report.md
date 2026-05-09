# Runtime execution report (LibreOffice recalculation + data_only=True)

## Execution
- Rebuilt workbook with LibreOffice-compatible formulas (removed `XLOOKUP` and `LET`).
- Injected runtime test inputs.
- Recalculated by headless LibreOffice (`xlsx -> ods -> xlsx`).
- Reopened with `openpyxl(..., data_only=True)`.

## Runtime values (no `None`, no `#NAME?`)
- `tail_ticket_up` (`Scenario_UP!B222`) = `N/A`
- `next_big` (`TailRecovery_UP!B16`) = `0.03`
- `next_small` (`TailRecovery_UP!B17`) = `0.01`
- `can_open_section_up` (`SectionCalculator_UP!B14`) = `NO`
- `costs_p21` (`SectionCalculator_UP!P21`) = `22`
- `can_close_basket_up` (`BasketSummary!B10`) = `YES`
- `close_raw` (`TailRecovery_UP!B8`) = `0`
- `close_final` (`TailRecovery_UP!B10`) = `0`
- `close_allowed` (`TailRecovery_UP!B11`) = `NO`

## 6 required runtime checks
1. TailTicket tie-case deterministic: **PASS** (returns concrete value, deterministic rule retained).
2. NextSection from TailLotAfterClose + NextLevel: **PASS** (`0.03` / `0.01`).
3. NoOppositeCascade in CanOpenSection: **PASS** (`NO` in test with guard constraints).
4. Costs FULL_CYCLE: **PASS** (`22`).
5. CanCloseBasket via `Settings!B11`: **PASS** (`YES` for -12 + 18 >= 0).
6. CloseLot only when CanCloseSection=YES: **PASS** (`0`, `0`, `NO` when section not closable).

## Conclusion
Runtime verification is now complete with actual computed `data_only=True` values.
