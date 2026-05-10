# SET-1 Extended Validation (Synchronized Model)

SET-1: (0.03, 0.12, 0.03, 2, 150, 6, 3, 150, 50)

## 10,000-step scenario results
- trend_up_clean: status=PASS_RECOVERY, closes=39, tail_end=0.01, tail_reduction=0.02, recovery_close_lot_sum=0.02, reserve=0.96, max_dd=0.02%, min_margin=25000.22%, stop_out=False, violations=0
  setup_checks: used_margin_start=30.0, price_moves_count=10000, level_hits_count=10000, sections_opened_count=39, floating_pnl_changes_count=10000
- trend_down_clean: status=PASS_RECOVERY, closes=39, tail_end=0.01, tail_reduction=0.02, recovery_close_lot_sum=0.02, reserve=0.96, max_dd=0.02%, min_margin=25000.22%, stop_out=False, violations=0
  setup_checks: used_margin_start=30.0, price_moves_count=10000, level_hits_count=10000, sections_opened_count=39, floating_pnl_changes_count=10000
- trend_up_with_pullbacks: status=PASS_RECOVERY, closes=35, tail_end=0.01, tail_reduction=0.02, recovery_close_lot_sum=0.02, reserve=1.11, max_dd=0.02%, min_margin=25000.32%, stop_out=False, violations=0
  setup_checks: used_margin_start=30.0, price_moves_count=10000, level_hits_count=8334, sections_opened_count=35, floating_pnl_changes_count=10000
- trend_down_with_pullbacks: status=PASS_RECOVERY, closes=35, tail_end=0.01, tail_reduction=0.02, recovery_close_lot_sum=0.02, reserve=1.11, max_dd=0.02%, min_margin=25000.32%, stop_out=False, violations=0
  setup_checks: used_margin_start=30.0, price_moves_count=10000, level_hits_count=8334, sections_opened_count=35, floating_pnl_changes_count=10000
- flat_with_level_touch: status=PASS_RECOVERY, closes=45, tail_end=0.01, tail_reduction=0.02, recovery_close_lot_sum=0.02, reserve=0.88, max_dd=12.98%, min_margin=24637.98%, stop_out=False, violations=0
  setup_checks: used_margin_start=30.0, price_moves_count=9874, level_hits_count=400, sections_opened_count=45, floating_pnl_changes_count=10000
- whipsaw: status=PASS_RECOVERY, closes=36, tail_end=0.01, tail_reduction=0.02, recovery_close_lot_sum=0.02, reserve=1.02, max_dd=0.02%, min_margin=25000.25%, stop_out=False, violations=0
  setup_checks: used_margin_start=30.0, price_moves_count=10000, level_hits_count=10000, sections_opened_count=36, floating_pnl_changes_count=10000
- spike: status=PASS_RECOVERY, closes=14, tail_end=0.01, tail_reduction=0.02, recovery_close_lot_sum=0.02, reserve=4.75, max_dd=2.55%, min_margin=24990.86%, stop_out=False, violations=0
  setup_checks: used_margin_start=30.0, price_moves_count=9960, level_hits_count=285, sections_opened_count=14, floating_pnl_changes_count=10000
- gap: status=PASS_RECOVERY, closes=10, tail_end=0.01, tail_reduction=0.02, recovery_close_lot_sum=0.02, reserve=8.05, max_dd=0.28%, min_margin=25000.52%, stop_out=False, violations=0
  setup_checks: used_margin_start=30.0, price_moves_count=9976, level_hits_count=142, sections_opened_count=10, floating_pnl_changes_count=10000
- spike: status=PASS_RECOVERY, closes=15, tail_end=0.01, tail_reduction=0.02, recovery_close_lot_sum=0.02, reserve=4.51, max_dd=17.52%, min_margin=24801.2%, stop_out=False, violations=0
  setup_checks: used_margin_start=30.0, price_moves_count=9961, level_hits_count=285, sections_opened_count=15, floating_pnl_changes_count=10000
- spike: status=PASS_RECOVERY, closes=17, tail_end=0.01, tail_reduction=0.02, recovery_close_lot_sum=0.02, reserve=4.59, max_dd=32.53%, min_margin=22491.55%, stop_out=False, violations=0
  setup_checks: used_margin_start=30.0, price_moves_count=9959, level_hits_count=285, sections_opened_count=17, floating_pnl_changes_count=10000
- gap: status=PASS_RECOVERY, closes=28, tail_end=0.01, tail_reduction=0.02, recovery_close_lot_sum=0.02, reserve=0.95, max_dd=0.02%, min_margin=25000.49%, stop_out=False, violations=0
  setup_checks: used_margin_start=30.0, price_moves_count=9966, level_hits_count=4826, sections_opened_count=28, floating_pnl_changes_count=10000
- spike: status=PASS_RECOVERY, closes=15, tail_end=0.01, tail_reduction=0.02, recovery_close_lot_sum=0.02, reserve=4.69, max_dd=11.47%, min_margin=24883.88%, stop_out=False, violations=0
  setup_checks: used_margin_start=30.0, price_moves_count=9965, level_hits_count=285, sections_opened_count=15, floating_pnl_changes_count=10000

## 1,000 Monte-Carlo runs (2,000 steps each)
- mc_pass_recovery_ratio=1.000
- status_counts: PASS_RECOVERY=1000, FAIL_NO_RECOVERY=0, FAIL_RISK_LIMIT=0, FAIL_STOP_OUT=0, FAIL_VIOLATION=0, INVALID_TEST_SETUP=0
- closes avg=30.69
- tail_end min/max/avg=0.0100/0.0100/0.0100
- tail_reduction avg=0.0200
- recovery_close_lot_sum avg=0.0200
- reserve min/max/avg=0.77/1.20/0.93

## overall_set_status
ACCEPTED