# MinusLock BigHarvest EA Build Info

Build date: 2026-06-14 10:17 UTC
Branch: work
Target folder: MinusLock_BigHarvest_EA
Commit purpose: MT5-ready top-level EA refresh

Included features:
- Initial BUY/SELL lock
- Initial profit ignored
- Big-Harvest
- Small-at-Far
- FarDistanceMode
- REAL_PRICE_DISTANCE
- EffectiveFarDistancePoints
- Cycle Math CSV report
- Reverse Geometry Validator
- STOP_MAX_LEVELS / UNCLOSED_CYCLE
- OnTester fail on unclosed cycle
- Internal SIMULATION engine
- Real Recovery P/L Validation
- REAL_CYCLE_MATH log and CSV fields

## 2026-06-16 Big-Harvest comments/panel audit
- Added dynamic WorkBigRatio usage and PRESET_ACTIVE logging.
- Added CommentUtils.mqh for all open/close system comments.
- Added Panel.mqh online status panel.
- Extended CYCLE_MATH/CSV with comment and panel audit columns.

## 2026-06-18 V2.4.4 FSM safety patch
- Terminal states are isolated from pending open retries.
- Added saved Small context and old Far cleanup guards for Small-at-Far.
- Added ValidateTerminalStateSafety and V2.4.4 static tests.
