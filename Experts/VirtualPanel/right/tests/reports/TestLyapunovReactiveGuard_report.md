# Test: TestLyapunovReactiveGuard

## Description
Control loop reacts to rising instability proxies (expansion blocking + compression).

## Input

## Execution
A/B on adversarial jump cluster.
- timestamp_utc: 2026-03-22T13:54:45.041300+00:00

## Results
- levels_before: N/A
- levels_after: N/A
- delta_before: N/A
- delta_after: N/A
- margin_before: N/A
- margin_after: N/A
- pnl: -81.20436416533033
- extra_metrics:
  - p_no_ctrl: 1.0
  - p_ctrl: 0.44083333333333335
  - expansions_blocked: 377.9275
  - compressions_triggered: 382.4675

## Validation
Must react and not worsen collapse probability.

## Conclusion
PASS
