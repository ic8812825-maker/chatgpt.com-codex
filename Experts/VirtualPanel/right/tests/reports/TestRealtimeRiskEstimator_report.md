# Test: TestRealtimeRiskEstimator

## Description
Estimator vs full MC validation.

## Input

## Execution
Compare anchors.
- timestamp_utc: 2026-03-21T21:34:11.040236+00:00

## Results
- levels_before: N/A
- levels_after: N/A
- delta_before: N/A
- delta_after: N/A
- margin_before: N/A
- margin_after: N/A
- pnl: 0.0
- extra_metrics:
  - estimator: [0.10056160845705997, 0.617747874769249, 0.9807913679466901, 0.9992606503600256]
  - mc: [0.0, 0.30142857142857143, 0.91, 0.9985714285714286]
  - bias: 0.12209037538325616
  - underestimation_rate: 0.0
  - false_safe_signals: 0

## Validation
Estimator should avoid false-safe bias.

## Conclusion
PASS
