# Risk Parameter Optimization Report (Synchronized Model)

- candidates_evaluated: 5
- accepted_sets_found: 2

## accept-gate
- no INVALID_TEST_SETUP in mandatory scenarios
- no FAIL_STOP_OUT
- no FAIL_VIOLATION
- max_dd <= MaxDDPercent in all stress variants
- Monte-Carlo PASS_RECOVERY >= 95%

## SET-1 (ACCEPTED)
- params: (0.02, 0.1, 0.02, 1, 150, 4, 2, 120, 60)
- mc_pass_recovery_ratio=1.000, score=14.63
  - trend_up_clean: PASS_RECOVERY, closes=39, tail_reduction=0.02, reserve=0.96, max_dd=0.02, min_margin=33333.63
  - trend_down_clean: PASS_RECOVERY, closes=39, tail_reduction=0.02, reserve=0.96, max_dd=0.02, min_margin=33333.63
  - trend_up_with_pullbacks: PASS_RECOVERY, closes=35, tail_reduction=0.02, reserve=1.11, max_dd=0.02, min_margin=33333.76
  - trend_down_with_pullbacks: PASS_RECOVERY, closes=35, tail_reduction=0.02, reserve=1.11, max_dd=0.02, min_margin=33333.76
  - flat_with_level_touch: PASS_RECOVERY, closes=45, tail_reduction=0.02, reserve=0.88, max_dd=3.25, min_margin=32850.63
  - whipsaw: PASS_RECOVERY, closes=36, tail_reduction=0.02, reserve=1.02, max_dd=0.02, min_margin=33333.67
  - spike: PASS_RECOVERY, closes=14, tail_reduction=0.02, reserve=4.75, max_dd=0.62, min_margin=33321.14
  - gap: PASS_RECOVERY, closes=10, tail_reduction=0.02, reserve=8.05, max_dd=0.22, min_margin=33334.02

## SET-2 (ACCEPTED)
- params: (0.03, 0.12, 0.03, 2, 150, 6, 3, 150, 50)
- mc_pass_recovery_ratio=1.000, score=14.63
  - trend_up_clean: PASS_RECOVERY, closes=39, tail_reduction=0.02, reserve=0.96, max_dd=0.02, min_margin=25000.22
  - trend_down_clean: PASS_RECOVERY, closes=39, tail_reduction=0.02, reserve=0.96, max_dd=0.02, min_margin=25000.22
  - trend_up_with_pullbacks: PASS_RECOVERY, closes=35, tail_reduction=0.02, reserve=1.11, max_dd=0.02, min_margin=25000.32
  - trend_down_with_pullbacks: PASS_RECOVERY, closes=35, tail_reduction=0.02, reserve=1.11, max_dd=0.02, min_margin=25000.32
  - flat_with_level_touch: PASS_RECOVERY, closes=45, tail_reduction=0.02, reserve=0.88, max_dd=3.25, min_margin=24637.98
  - whipsaw: PASS_RECOVERY, closes=36, tail_reduction=0.02, reserve=1.02, max_dd=0.02, min_margin=25000.25
  - spike: PASS_RECOVERY, closes=14, tail_reduction=0.02, reserve=4.75, max_dd=0.62, min_margin=24990.86
  - gap: PASS_RECOVERY, closes=10, tail_reduction=0.02, reserve=8.05, max_dd=0.22, min_margin=25000.52

## SET-3 (REJECTED)
- params: (0.05, 0.14, 0.04, 2, 180, 8, 4, 120, 60)
- mc_pass_recovery_ratio=1.000, score=27.65
  - trend_up_clean: PASS_RECOVERY, closes=98, tail_reduction=0.04, reserve=1.92, max_dd=0.02, min_margin=16666.76
  - trend_down_clean: PASS_RECOVERY, closes=98, tail_reduction=0.04, reserve=1.92, max_dd=0.02, min_margin=16666.76
  - trend_up_with_pullbacks: PASS_RECOVERY, closes=83, tail_reduction=0.04, reserve=2.23, max_dd=0.02, min_margin=16666.83
  - trend_down_with_pullbacks: PASS_RECOVERY, closes=83, tail_reduction=0.04, reserve=2.23, max_dd=0.02, min_margin=16666.83
  - flat_with_level_touch: INVALID_TEST_SETUP, closes=0, tail_reduction=0.0, reserve=0, max_dd=4.0, min_margin=19199.03
  - whipsaw: PASS_RECOVERY, closes=90, tail_reduction=0.04, reserve=2.06, max_dd=0.02, min_margin=16666.79
  - spike: PASS_RECOVERY, closes=28, tail_reduction=0.04, reserve=9.33, max_dd=1.28, min_margin=16608.17
  - gap: PASS_RECOVERY, closes=21, tail_reduction=0.04, reserve=16.78, max_dd=0.73, min_margin=16629.75

## SET-4 (REJECTED)
- params: (0.04, 0.12, 0.03, 2, 180, 6, 3, 150, 60)
- mc_pass_recovery_ratio=1.000, score=19.72
  - trend_up_clean: PASS_RECOVERY, closes=72, tail_reduction=0.03, reserve=1.43, max_dd=0.02, min_margin=20000.12
  - trend_down_clean: PASS_RECOVERY, closes=72, tail_reduction=0.03, reserve=1.43, max_dd=0.02, min_margin=20000.12
  - trend_up_with_pullbacks: PASS_RECOVERY, closes=62, tail_reduction=0.03, reserve=1.65, max_dd=0.02, min_margin=20000.2
  - trend_down_with_pullbacks: PASS_RECOVERY, closes=62, tail_reduction=0.03, reserve=1.65, max_dd=0.02, min_margin=20000.2
  - flat_with_level_touch: INVALID_TEST_SETUP, closes=0, tail_reduction=0.0, reserve=0, max_dd=4.0, min_margin=23998.79
  - whipsaw: PASS_RECOVERY, closes=68, tail_reduction=0.03, reserve=1.51, max_dd=0.02, min_margin=20000.14
  - spike: PASS_RECOVERY, closes=21, tail_reduction=0.03, reserve=6.77, max_dd=1.32, min_margin=19951.72
  - gap: PASS_RECOVERY, closes=16, tail_reduction=0.03, reserve=12.78, max_dd=0.77, min_margin=19971.44

## SET-5 (REJECTED)
- params: (0.03, 0.14, 0.03, 2, 180, 6, 3, 120, 60)
- mc_pass_recovery_ratio=1.000, score=11.87
  - trend_up_clean: PASS_RECOVERY, closes=51, tail_reduction=0.02, reserve=0.96, max_dd=0.02, min_margin=25000.15
  - trend_down_clean: PASS_RECOVERY, closes=51, tail_reduction=0.02, reserve=0.96, max_dd=0.02, min_margin=25000.15
  - trend_up_with_pullbacks: PASS_RECOVERY, closes=43, tail_reduction=0.02, reserve=1.12, max_dd=0.02, min_margin=25000.25
  - trend_down_with_pullbacks: PASS_RECOVERY, closes=43, tail_reduction=0.02, reserve=1.12, max_dd=0.02, min_margin=25000.25
  - flat_with_level_touch: INVALID_TEST_SETUP, closes=0, tail_reduction=0.0, reserve=0, max_dd=4.0, min_margin=31998.39
  - whipsaw: PASS_RECOVERY, closes=45, tail_reduction=0.02, reserve=1.03, max_dd=0.02, min_margin=25000.18
  - spike: PASS_RECOVERY, closes=14, tail_reduction=0.02, reserve=4.67, max_dd=1.33, min_margin=24966.63
  - gap: PASS_RECOVERY, closes=11, tail_reduction=0.02, reserve=8.79, max_dd=0.81, min_margin=24981.23

## overall_set_status
ACCEPTED