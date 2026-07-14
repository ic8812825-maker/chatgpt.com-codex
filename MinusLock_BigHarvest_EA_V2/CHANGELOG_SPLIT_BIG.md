# CHANGELOG Split Big

## 2026-07-14

Status: **SPLIT BIG IMPLEMENTED** / **SPLIT SMALL NOT IMPLEMENTED**.

- Safe defaults restored: Legacy enabled, Split disabled, real trading disabled.
- Added Split Big route from `STATE_FAR_ACTIVE`.
- Added `PrepareSplitBigLevel()` from actual Far lot.
- Added BigCore, SmallBase and BigTrend role opening.
- Added rollback paths for SmallBase and BigTrend opening failures.
- Added Big target from BigCore open price.
- Added separate full-close states for BigCore, BigTrend and SmallBase.
- Added Split lifecycle net by position identifiers with symbol/magic isolation.
- Added immediate full Far check before partial.
- Added partial Far budget/carry handling and Reserve credit after partial/skip.
- Added local pytest suites for unit/static/scenario behavior.
- Added Split Big-only set files.

Limitations:

- Split Small / DynamicReverseSmall is not implemented.
- MetaEditor and Strategy Tester were not run in the Linux container.
