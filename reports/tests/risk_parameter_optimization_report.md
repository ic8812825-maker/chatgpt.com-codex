# Risk Parameter Optimization Report (Synchronized Model)

- candidates_evaluated: 5
- accepted_sets_found: 0

## accept-gate
- no FAIL_RISK_LIMIT
- no FAIL_STOP_OUT
- no FAIL_VIOLATION
- no INVALID_TEST_SETUP
- no FAIL_NO_RECOVERY
- Monte-Carlo PASS_RECOVERY >= 95%

## SET-1 (REJECTED)
- params: (0.05, 0.14, 0.04, 2, 180, 8, 4, 120, 60)
- mc_pass_recovery_ratio=1.000, score=10.83
  - trend_up: INVALID_TEST_SETUP, closes=0, tail_reduction=0.0, reserve=0, max_dd=0.32, min_margin=19936.77
  - trend_down: INVALID_TEST_SETUP, closes=0, tail_reduction=0.0, reserve=0, max_dd=0.32, min_margin=19936.77
  - flat_with_level_touch: INVALID_TEST_SETUP, closes=0, tail_reduction=0.0, reserve=0, max_dd=3.99, min_margin=19201.44
  - whipsaw: PASS_RECOVERY, closes=90, tail_reduction=0.04, reserve=2.06, max_dd=0.02, min_margin=16666.79
  - spike: PASS_RECOVERY, closes=28, tail_reduction=0.04, reserve=9.33, max_dd=1.28, min_margin=16604.28
  - gap: PASS_RECOVERY, closes=21, tail_reduction=0.04, reserve=16.78, max_dd=0.75, min_margin=16629.05

## SET-2 (REJECTED)
- params: (0.04, 0.12, 0.03, 2, 180, 6, 3, 150, 60)
- mc_pass_recovery_ratio=1.000, score=7.12
  - trend_up: INVALID_TEST_SETUP, closes=0, tail_reduction=0.0, reserve=0, max_dd=0.32, min_margin=24920.96
  - trend_down: INVALID_TEST_SETUP, closes=0, tail_reduction=0.0, reserve=0, max_dd=0.32, min_margin=24920.96
  - flat_with_level_touch: INVALID_TEST_SETUP, closes=0, tail_reduction=0.0, reserve=0, max_dd=3.99, min_margin=24001.8
  - whipsaw: PASS_RECOVERY, closes=68, tail_reduction=0.03, reserve=1.51, max_dd=0.02, min_margin=20000.14
  - spike: PASS_RECOVERY, closes=21, tail_reduction=0.03, reserve=6.77, max_dd=1.32, min_margin=19945.89
  - gap: PASS_RECOVERY, closes=16, tail_reduction=0.03, reserve=12.78, max_dd=0.79, min_margin=19970.89

## SET-3 (REJECTED)
- params: (0.02, 0.1, 0.02, 1, 150, 4, 2, 120, 60)
- mc_pass_recovery_ratio=1.000, score=6.24
  - trend_up: INVALID_TEST_SETUP, closes=0, tail_reduction=0.0, reserve=0, max_dd=0.0, min_margin=49999.65
  - trend_down: INVALID_TEST_SETUP, closes=0, tail_reduction=0.0, reserve=0, max_dd=0.0, min_margin=49999.65
  - flat_with_level_touch: PASS_RECOVERY, closes=45, tail_reduction=0.02, reserve=0.88, max_dd=3.23, min_margin=32856.28
  - whipsaw: PASS_RECOVERY, closes=36, tail_reduction=0.02, reserve=1.02, max_dd=0.02, min_margin=33333.67
  - spike: PASS_RECOVERY, closes=14, tail_reduction=0.02, reserve=4.75, max_dd=0.62, min_margin=33319.21
  - gap: PASS_RECOVERY, closes=10, tail_reduction=0.02, reserve=8.05, max_dd=0.23, min_margin=33331.97

## SET-4 (REJECTED)
- params: (0.03, 0.12, 0.03, 2, 150, 6, 3, 150, 50)
- mc_pass_recovery_ratio=1.000, score=6.24
  - trend_up: INVALID_TEST_SETUP, closes=0, tail_reduction=0.0, reserve=0, max_dd=0.0, min_margin=33333.1
  - trend_down: INVALID_TEST_SETUP, closes=0, tail_reduction=0.0, reserve=0, max_dd=0.0, min_margin=33333.1
  - flat_with_level_touch: PASS_RECOVERY, closes=45, tail_reduction=0.02, reserve=0.88, max_dd=3.23, min_margin=24642.21
  - whipsaw: PASS_RECOVERY, closes=36, tail_reduction=0.02, reserve=1.02, max_dd=0.02, min_margin=25000.25
  - spike: PASS_RECOVERY, closes=14, tail_reduction=0.02, reserve=4.75, max_dd=0.62, min_margin=24989.41
  - gap: PASS_RECOVERY, closes=10, tail_reduction=0.02, reserve=8.05, max_dd=0.23, min_margin=24998.98

## SET-5 (REJECTED)
- params: (0.03, 0.14, 0.03, 2, 180, 6, 3, 120, 60)
- mc_pass_recovery_ratio=1.000, score=3.46
  - trend_up: INVALID_TEST_SETUP, closes=0, tail_reduction=0.0, reserve=0, max_dd=0.32, min_margin=33227.94
  - trend_down: INVALID_TEST_SETUP, closes=0, tail_reduction=0.0, reserve=0, max_dd=0.32, min_margin=33227.94
  - flat_with_level_touch: INVALID_TEST_SETUP, closes=0, tail_reduction=0.0, reserve=0, max_dd=3.99, min_margin=32002.39
  - whipsaw: PASS_RECOVERY, closes=45, tail_reduction=0.02, reserve=1.03, max_dd=0.02, min_margin=25000.18
  - spike: PASS_RECOVERY, closes=14, tail_reduction=0.02, reserve=4.67, max_dd=1.33, min_margin=24964.23
  - gap: PASS_RECOVERY, closes=11, tail_reduction=0.02, reserve=8.79, max_dd=0.83, min_margin=24987.01

## overall_set_status
REJECTED