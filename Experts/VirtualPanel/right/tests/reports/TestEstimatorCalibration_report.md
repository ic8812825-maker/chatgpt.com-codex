# Test: TestEstimatorCalibration

## Description
Estimator calibration + Brier + ROC-AUC.

## Input

## Execution
Anchor calibration run.
- timestamp_utc: 2026-03-22T09:15:20.405445+00:00

## Results
- levels_before: N/A
- levels_after: N/A
- delta_before: N/A
- delta_after: N/A
- margin_before: N/A
- margin_after: N/A
- pnl: 0.0
- extra_metrics:
  - calibration_error: 0.16951178066388575
  - brier_score: 0.04344521275754894
  - roc_auc: 1.0
  - predicted: [0.1472920196689477, 0.32651276456269623, 0.6610551811934159, 0.935836123594826, 0.9909149634782348]
  - actual: [0.0011111111111111111, 0.07, 0.31222222222222223, 0.8444444444444444, 0.9955555555555555]

## Validation
Calibration must be within threshold.

## Conclusion
PASS
