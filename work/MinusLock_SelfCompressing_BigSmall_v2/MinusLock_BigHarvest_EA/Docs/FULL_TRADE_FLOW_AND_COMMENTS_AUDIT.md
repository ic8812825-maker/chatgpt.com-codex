# Full Trade Flow and Comments Audit

## 1. Project Folder
`MinusLock_BigHarvest_EA` and synchronized work copy.

## 2. Files Created
- `Include/CommentUtils.mqh`
- `Include/Panel.mqh`
- `Docs/FULL_TRADE_FLOW_AND_COMMENTS_AUDIT.md`

## 3. Files Changed
Core EA, config, types, trade engine, state machine, logger, risk manager, docs, and verifier.

## 4. Dynamic Parameters Check
PASS: Big/Small/close/reserve formulas use Work parameters; preset mode logs `PRESET_ACTIVE`.

## 5. Initial Cycle Check
PASS: BUY/SELL start comments are generated, first plus close is marked `CLOSE_INITIAL_PLUS`, initial profit is ignored, and Far context is stored.

## 6. Big Scenario Check
PASS: Big/Small close reasons are logged, close-Far budget uses money budget and Work shares, reserve is tracked, and final close/stop paths are recorded.

## 7. Small Scenario Check
PASS: Small-at-Far waits for old Far touch, closes Small and old Far fully, closes Big partially, rebuilds NewFar from remaining Big, and validates reverse geometry/risk.

## 8. Comment Library Check
PASS: `CommentUtils.mqh` owns comment builders and validation.

## 9. Open Position Comment Coverage
PASS: Initial, Big, Small, repeated harvest, and simulated opens reject invalid comments before trading.

## 10. Close Reason Coverage
PASS: Required close reasons are written through `MarkSystemClose`, logs, and CSV audit fields.

## 11. Visual Panel Check
PASS: `PanelInit`, `PanelUpdate`, and `PanelDeinit` manage a single upper-right label.

## 12. CYCLE_MATH / CSV Check
PASS: CSV includes `OpenComment`, `CloseComment`, `PositionRole`, `CommentValid`, `PanelState`, `LastOpenComment`, and `LastCloseReason`.

## 13. Risk Gates Check
PASS: spread and margin gates update `RiskGateStatus` and retain existing diagnostics.

## 14. Python Tests
Recorded in final implementation report.

## 15. MetaEditor Compile
Not available in this Linux container unless MetaEditor is installed externally.

## 16. Strategy Tester
Not available in this Linux container unless MT5 is installed externally.

## 17. Found Problems
Direct BigRatio formula usage, legacy comments, missing panel, and missing CSV comment audit fields.

## 18. Fixes Applied
Added WorkBigRatio, centralized comments, empty-comment blocking, close-reason context, live panel, risk status, verifier tokens, and documentation.

## 19. Final Verdict
PASS for static/code audit and Python checks in this repository environment; MT5 visual/compile checks require the MT5 toolchain.

## V2.4.4 FSM Safety Addendum
Terminal states now break without open/retry calls. Small-at-Far saves Small direction/close price before clearing Small context. Old Far fields are copied into `oldFar*` audit fields and active Far context is cleared before assigning the new Far. `ValidateTerminalStateSafety()` is executed during initialization and returns `INIT_FAILED` if the static FSM safety rule is violated.
