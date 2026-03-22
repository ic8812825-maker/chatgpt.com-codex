# Test: TestALCVsNoALC

## Description
Compare ALE vs ALE+ALC.

## Input
- mode: shock

## Execution
Run both configs.
- timestamp_utc: 2026-03-21T19:45:33.815104+00:00

## Results
- levels_before: N/A
- levels_after: N/A
- delta_before: N/A
- delta_after: N/A
- margin_before: N/A
- margin_after: N/A
- pnl: 0.0
- extra_metrics:
  - p_no_alc: 0.9995454545454545
  - p_alc: 0.9954545454545455
  - ttc_no_alc: 184.925
  - ttc_alc: 241.28272727272727

## Validation
ALC should not worsen collapse probability.

## Conclusion
PASS
