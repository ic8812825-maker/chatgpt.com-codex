# ALE TEST AUDIT REPORT (`Experts/VirtualPanel/right/ale`)

## 1) Scope and constraints

This iteration addresses the technical assignment with changes focused on the ALE right-side engine and tests.
Main implementation scope:

- `Experts/VirtualPanel/right/ale/*`
- `Experts/VirtualPanel/right/tests/*` (unit test harness and ALE-specific tests)

In addition, this report is updated at:

- `Experts/VirtualPanel/ALE_TEST_AUDIT_REPORT.md`

## 2) Implemented improvements

### P0 — Critical reliability

1. **Unified ALE runner inside `right/ale`**
   - Added:
     - `right/ale/tests/RunAllTests.mqh`
     - `right/ale/tests/RunAllTests.mq5`
   - Runner executes ALE suite in sequence: `TestALE`, `TestGeometry`, `TestRisk`.
   - Added explicit BUY/SELL isolation checks and consolidated pass/fail summary.

2. **Runtime invariants + safe rollback in position book**
   - `right/ale/positions/CALPositionBook.mqh` now includes:
     - invariant checker (`CheckInvariants`),
     - limits (`max positions`, `min lot`) with configurable `SetLimits`,
     - mutation API `Edit(...)` and `Remove(...)`,
     - rollback behavior on invariant violation.
   - Invariants validated:
     - position count bounded,
     - lot not below minimum,
     - direction in `{ALE_FLOW_BUY, ALE_FLOW_SELL}`,
     - finite valid price/lot values.

3. **SAFE thresholds through config + boundary regression**
   - SAFE continues to use `CALRiskConfig` in risk/engine wiring.
   - Added boundary test (`==` vs `>`) for global SAFE trigger:
     - `TestRisk_GlobalSafeThresholdBoundaries`.

4. **Strict inequality documented**
   - In `CALEngine::CheckGlobalSAFE()` added explicit comment explaining why `>` is intentional and `==` is admissible boundary.

### P1 — Maintainability and quality

5. **VP_DEBUG logging macro**
   - Added `right/ale/core/CALDebug.mqh` with `VP_DEBUG` and `VP_DEBUG_LOG(...)`.
   - Hooked into `CALEngine` for global SAFE debug trace.

6. **ALE module map README**
   - Added `right/ale/README.md` with module dependency map and debug usage snippet.

### P2 — Behavioral regression infrastructure

7. **Extended deterministic/behavioral coverage**
   - Existing deterministic replay tests are now integrated into both runners.
   - Added dual-flow isolation tests:
     - `TestALE_BuyFlowIsolation`
     - `TestALE_SellFlowIsolation`

8. **New Python ALE unit checks**
   - Added `right/tests/test_ale_p0_behavior.py` to ensure new P0/P1 mechanisms remain wired and not accidentally removed.

## 3) Detailed test results

### 3.1 ALE-targeted unit tests

Command:

- `pytest -q Experts/VirtualPanel/right/tests`

Result:

- **21 passed**.

What is validated now:

- Architecture wiring of dual-flow engine;
- Includes validity for all MQL files in right subtree;
- FSM state presence and runtime entry signatures;
- Risk config wiring and propagation to BUY/SELL streams;
- Unified ALE runner presence in `right/ale/tests` and sequence order;
- BUY/SELL isolation tests registration;
- Runtime invariant/rollback API presence in `CALPositionBook`;
- strict inequality documentation in global SAFE logic;
- debug macro presence;
- risk boundary test registration.

### 3.2 Repository-level smoke test

Command:

- `pytest -q`

Result:

- **21 passed**.

### 3.3 Git/repository integrity check

Command:

- `bash verify-all.sh work`

Result:

- Completed successfully.
- `origin/work` reachable and synchronized.
- Dry-run push/pull succeeded.
- Optional warnings for absent probe files (`test-file.txt`, `test-file-2.txt`) are expected by script design.

## 4) Key observations after improvements

1. **Reliability improved at mutation level**
   - Position mutations now have explicit post-condition checks and rollback path.

2. **Determinism baseline is practical**
   - Replay scenarios provide consistent regression hooks and finite-metric checks.

3. **Dual-flow isolation became testable as a requirement**
   - BUY-only and SELL-only tests now assert no accidental cross-flow influence (except designed global SAFE).

4. **Documentation-to-runtime consistency improved**
   - Global SAFE threshold semantics are now documented where the decision is made.

## 5) Proposed next improvements

### Next P0

- Add explicit NaN/Inf guard asserts directly in `CALFlowEngine::Process` after each major stage (geometry/exposure/risk/math).
- Add configurable invariants profile in `CALRiskConfig` for:
  - max positions,
  - min lot,
  - strict runtime checks toggle.

### Next P1

- Add CSV export helper under `right/ale/core/` for:
  - virtual positions snapshot,
  - `CALContext` snapshot per replay step.
- Add required-state-trace matcher in deterministic runner:
  - expected `(state_buy, state_sell)` timeline comparison.

### Next P2

- Add replay scenario `V-shape` directly to `CALDeterministicRunner` enum and builder.
- Add machine-readable report generation (JUnit XML equivalent for MQL-runner logs + parser).

## 6) Final status

- ALE right-side now has a dedicated runner in `right/ale/tests`, stronger reliability guards in the position book, stricter test registration for BUY/SELL isolation and SAFE threshold boundaries, and updated documentation.
- Current automated status: **green** on all available local unit/smoke checks.
