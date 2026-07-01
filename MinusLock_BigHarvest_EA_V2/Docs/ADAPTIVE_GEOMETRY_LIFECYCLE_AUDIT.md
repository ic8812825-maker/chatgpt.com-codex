# Adaptive Geometry Lifecycle Audit

## Scope

This audit traces Adaptive Geometry through the complete runtime path:

`GeometryMode -> ATR -> calculation -> Work* -> recovery -> harvest -> cycle finish -> ClearCycleGeometry() -> next cycle`.

## Call map

| Entry point | Geometry action | Repeat/skip/late/double risk | Guard |
|---|---|---|---|
| `OnInit()` | Initializes diagnostic geometry through `UseManualGeometryFallback()` for manual mode or `CalculateAdaptiveGeometry()` for ATR modes, then prints diagnostics. | Early calculation can be replaced at real cycle start. | `OpenInitialLock()` calls `ResetCycleGeometryFields()` before initializing cycle geometry. |
| `OpenInitialLock()` existing lock branch | `ResetCycleGeometryFields("OpenInitialLock new cycle")`, then `InitializeCycleGeometry()`. | Avoids stale pre-init geometry; recalculates exactly for the new cycle. | `FreezeGeometryPerCycle` only keeps geometry after cycle fields exist. |
| `OpenInitialLock()` new lock branch | Same reset + initialize path after both initial legs are confirmed. | Prevents using manual values in ATR mode when cycle starts. | `InitializeCycleGeometry()` and diagnostics. |
| `RecoverState()` | Restores `CycleATRRaw`, `CycleATRPoints`, `GeometrySource`, fallback fields, all `Work*`, `GeometryModeUsed`, and `GeometryCalculatedTime` from Global Variables. | If old/missing state has no Work geometry, `EnsureCycleGeometry()` initializes instead of silently reading manual inputs. | `EnsureCycleGeometry("RecoverState restored active or pending context without saved Work geometry")`. |
| Initial-lock recovery | If initial BUY/SELL or partial initial lock is recovered and Work geometry is missing, `InitializeCycleGeometry()` is called. | Prevents first trigger from reading manual parameters after restart. | `HasCycleGeometry()` guard. |
| Runtime reads | All trading math reads `WorkInitialTriggerPoints()`, `WorkBigMoveStartPoints()`, `WorkBigMoveStepPoints()`, or `WorkFarDistancePoints()`. | Missing geometry triggers explicit `EnsureCycleGeometry()` instead of silent manual fallback. | Work accessors. |
| Terminal profitable/loss states | `ClearCycleGeometry(true)` is called after closed profit/recovery loss only when no live/pending/retry context remains, and the cleared geometry is persisted to Global Variables. | Prevents premature clearing during active recovery. | `CanClearCycleGeometry()`. |
| `ResetRecoveryContext()` | Clears all recovery context and calls `ClearCycleGeometry(false)` so recovery loading does not overwrite saved Global Variables before restore. | If live positions exist, `CanClearCycleGeometry()` blocks the clear. | `CountManagedOpenPositions()` and context guards. |

## ATR lifecycle

`ReadClosedBarATR()` performs the ATR chain in this order:

1. `SeriesInfoInteger(_Symbol, ATRTimeframe, SERIES_SYNCHRONIZED, synchronized)`.
2. `Bars(_Symbol, ATRTimeframe)` must be greater than `ATRPeriod + 1`.
3. `iATR(_Symbol, ATRTimeframe, ATRPeriod)` creates a temporary handle.
4. `BarsCalculated(atrHandle)` must be greater than 1.
5. `CopyBuffer(atrHandle, 0, 1, 1, atrBuffer)` reads the last closed bar, not the forming bar.
6. `IndicatorRelease(atrHandle)` releases the handle immediately after copy or before every handle failure return.
7. ATR value must be valid and positive.

The handle is intentionally short-lived; no persistent handle is stored, so there is no stale-handle lifecycle across symbol/timeframe changes.

## Calculation lifecycle

After ATR is read:

1. `ATRPoints = ATRRaw / SymbolInfoDouble(_Symbol, SYMBOL_POINT)`.
2. Preset multipliers are selected by `GeometryMode`:
   - `GEOMETRY_ATR_SAFE`: `1.00 / 1.00 / 0.40 / 1.30`.
   - `GEOMETRY_ATR_BALANCED`: `1.00 / 1.15 / 0.40 / 1.50`.
   - `GEOMETRY_ATR_PROFIT`: `1.05 / 1.20 / 0.45 / 1.60`.
   - `GEOMETRY_ATR_CUSTOM`: input multipliers.
3. Raw point distances are rounded by independent round steps.
4. Rounded values are clamped to min/max bounds.
5. Clamped values populate `Ctx.workInitialTriggerPoints`, `Ctx.workBigMoveStartPoints`, `Ctx.workBigMoveStepPoints`, and `Ctx.workFarDistancePoints`.
6. `Ctx.geometryModeUsed`, `Ctx.geometrySource`, fallback fields, and `Ctx.geometryCalculatedTime` are updated.

## Work field lifecycle

| Field | Created | First filled | Mutated | Saved | Restored | Cleared |
|---|---|---|---|---|---|---|
| `workInitialTriggerPoints` | `RecoveryContext` | `UseManualGeometryFallback()` or `CalculateAdaptiveGeometry()` | `ResetCycleGeometryFields()` clears; recalculation refills | `SaveState()` as `WorkInitialTriggerPoints` | `RecoverState()` | `ClearCycleGeometry()` via `ResetCycleGeometryFields()` |
| `workBigMoveStartPoints` | `RecoveryContext` | same | same | `WorkBigMoveStartPoints` | same | same |
| `workBigMoveStepPoints` | `RecoveryContext` | same | same | `WorkBigMoveStepPoints` | same | same |
| `workFarDistancePoints` | `RecoveryContext` | same | same | `WorkFarDistancePoints` | same | same |
| `cycleATRRaw` | `RecoveryContext` | `CalculateAdaptiveGeometry()` or zero in manual fallback | reset/refill per cycle | `CycleATRRaw` | same | same |
| `cycleATRPoints` | `RecoveryContext` | `CalculateAdaptiveGeometry()` or zero in manual fallback | reset/refill per cycle | `CycleATRPoints` | same | same |
| `geometryModeUsed` | `RecoveryContext` | manual fallback or active ATR mode | reset/refill per cycle | `GeometryModeUsed` | same | same |
| `geometryCalculatedTime` | `RecoveryContext` | calculation/fallback time | reset/refill per cycle | `GeometryCalculatedTime` | same | same |

## Geometry read table

| Runtime area | Required accessor | Status |
|---|---|---|
| Initial trigger close checks | `WorkInitialTriggerPoints()` | OK |
| Initial far distance capture | `WorkInitialTriggerPoints()` | OK |
| Big movement level formula | `WorkBigMoveStartPoints() + (level - 1) * WorkBigMoveStepPoints()` | OK |
| Fixed far distance mode | `WorkFarDistancePoints()` | OK |
| FAR logging/panel/CSV diagnostics | Work accessors | OK |
| Input validation and manual diagnostics | Manual input names | OK; not runtime recovery math |

## Freeze per cycle

When `FreezeGeometryPerCycle=true`, `InitializeCycleGeometry()` returns the existing values if all Work fields and `geometryCalculatedTime` are populated. Runtime reads therefore cannot drift when ATR changes during an active cycle. A new cycle first calls `ResetCycleGeometryFields("OpenInitialLock new cycle")`, then initializes fresh geometry.

## Clear policy

`ClearCycleGeometry()` may clear only when:

- no managed open positions exist;
- Far, Big, Small, initial BUY and initial SELL tickets are zero;
- no pending action exists;
- no retry ticket exists.

If any active context remains, it logs `CLEAR_CYCLE_GEOMETRY_SKIPPED reason=ACTIVE_CONTEXT_OR_POSITIONS` and keeps frozen geometry.

## Restart and reconciliation

Restart uses `RecoverState()` to restore Work geometry from Global Variables. Reconciliation reads the restored Work accessors and logs a context summary. It does not replace Work fields with manual parameters. If an older state lacks Work geometry, `EnsureCycleGeometry()` performs an explicit initialize/fallback path and immediately saves the repaired state.

## Diagnostics contract

Each diagnostic row/log has enough information to reconstruct the lifecycle:

- `GeometryMode`
- `GeometrySource`
- `ATRRaw`
- `ATRPoints`
- `WorkInitialTriggerPoints`
- `WorkBigMoveStartPoints`
- `WorkBigMoveStepPoints`
- `WorkFarDistancePoints`
- `FreezeGeometryPerCycle`
- `Fallback`
- `FallbackReason`

## Residual runtime validation required

This repository environment cannot run MetaTrader Strategy Tester, produce Experts logs, or capture chart `Comment()` screenshots. The static audit verifies code paths and diagnostics fields. Final production acceptance still requires the documented MT5 runs for `GEOMETRY_MANUAL`, `GEOMETRY_ATR_SAFE`, `GEOMETRY_ATR_BALANCED`, `GEOMETRY_ATR_PROFIT`, and `GEOMETRY_ATR_CUSTOM`.
