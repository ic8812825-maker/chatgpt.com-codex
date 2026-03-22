# Test: TestRiskControlFSM

## Description
Zone transition mapping.

## Input
- p_values: [0.05, 0.15, 0.4, 0.75]

## Execution
Map p->zone->k.
- timestamp_utc: 2026-03-21T21:34:11.040674+00:00

## Results
- levels_before: N/A
- levels_after: N/A
- delta_before: N/A
- delta_after: N/A
- margin_before: N/A
- margin_after: N/A
- pnl: 0.0
- extra_metrics:
  - zones: ['SAFE', 'WARNING', 'DANGER', 'CRITICAL']
  - k_eff: [1.3, 1.25, 1.2, 1.1]

## Validation
Mapping matches spec.

## Conclusion
PASS
