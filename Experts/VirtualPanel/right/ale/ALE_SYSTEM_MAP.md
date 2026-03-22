# ALE_SYSTEM_MAP

## Pipeline (as-discovered)

`positions → geometry → ALE stream process → ALC compression → FSM transition → risk evaluation → control gating`

## Module Map

| Module | File | Function | Purpose | Inputs | Outputs | Dependencies |
|---|---|---|---|---|---|---|
| Core ALE stream | `core/CALFlowEngine.mqh` | `CALStreamEngine::Process` | Main runtime pipeline and orchestration | `price`, internal stream state | updated `CALStreamContext`, FSM state, SAFE flag | GridBuilder, PositionBook, CompressionEngine, ExposureFlow, RiskEngine, StateMachine |
| Core orchestration | `core/CALEngine.mqh` | `OnPriceUpdate` | BUY/SELL dual-stream processing + global SAFE/harvest | market price | updated global context/event | `CBuyEngine`, `CSellEngine`, `CALContext` |
| ALC compression | `compression/CALCompressionEngine.mqh` | `ProcessCompression` | Trigger compression, lock matching, rebuild geometry | `book`, `ctx`, `equity`, `safe_rescue` | compressed book, updated ctx + history event | LockCompression, CompressionHistory, PositionBook |
| FSM | `core/CALStateMachine.mqh` | `TransitionBySignal` | State transitions by runtime signals | signal enum + current state | next state | Allowed transition matrix in class |
| Geometry fixed | `geometry/CALFixedStep.mqh` | `BuildGrid` | Linear levels/lots build | direction, center, levels | `CALGrid` | `CALGeometryBase` |
| Geometry log | `geometry/CALLogGeometry.mqh` | `BuildGrid` | Log-distance grid and lot scaling | direction, center, levels, base | `CALGrid` | `CALGeometryBase` |
| Position math | `positions/CALPositionBook.mqh` | `EffectiveDelta`, `PnLAtPrice`, `RebuildGeometryLots` | delta/PnL/lot geometry invariants | positions + price params | aggregate metrics | `CALVirtualPosition` |
| Exposure | `exposure/CALExposureFlow.mqh` | `Recalculate` | exposure/gamma/convexity update | book + price | exposure metrics | PositionBook |
| Risk engine | `risk/CALRiskEngine.mqh` | `Evaluate` | dd/margin/probability/SAFE decision | stream context + exposure + market | `CALRiskReport` | MarginModel, WorstCase, SafeMode, ReturnProbability, PhaseDiagram |
| SAFE policy | `risk/CALSafeMode.mqh` | `EvaluateTriggers`, `EvaluatePhase` | SAFE / critical gating logic | margin/dd/atr/spread/probability/phase terms | bool trigger | risk config params |
| Python control audit | `tests/run_unit_tests.py` | `simulate` | structure-agnostic stress/risk-control simulator | mode + config + seed | system metrics (collapse, pnl, activity, control) | local helper functions |

## Discovery status (mandatory blocks)

- ALE logic: **FOUND**
- ALC logic: **FOUND**
- FSM: **FOUND**
- Risk control / predictive layer: **FOUND** (Python audit layer)
- Geometry (`L0, k, R, depth`): **FOUND**
- Exposure (`total volume`, weighted effect via book/exposure, unrealized PnL): **FOUND**
- Risk engine (`L1/L2/L3`, margin, drawdown, SAFE): **FOUND**
- Lyapunov `V(state)`: **NOT FOUND** → **FAIL**

