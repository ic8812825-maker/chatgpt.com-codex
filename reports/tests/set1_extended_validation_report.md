# SET-1 Extended Validation

SET-1: {'BaseLot': 0.03, 'BigRatio': 0.12, 'SmallRatio': 0.03, 'MaxActiveSections': 2, 'StepPoints': 150, 'MaxTotalLot': 6, 'MaxNetLot': 3, 'MinMarginLevelPercent': 150, 'MaxDDPercent': 50}

## 10,000-step scenario results
- trend_up: status=PASS_RECOVERY, closes=86, tail_end=0.01, tail_reduction=0.02, recovery_close_lot_sum=0.02, reserve=0.76, max_dd=10.54%, min_margin=19251.21%, stop_out=False, violations=0
  setup_checks: initial_positions_count=2, initial_tail_lot=0.03, used_margin_start=30.0, price_moves_count=10000, level_hits_count=1000, sections_opened_count=86, floating_pnl_changes_count=10000
- trend_down: status=PASS_RECOVERY, closes=86, tail_end=0.01, tail_reduction=0.02, recovery_close_lot_sum=0.02, reserve=0.76, max_dd=10.54%, min_margin=19251.21%, stop_out=False, violations=0
  setup_checks: initial_positions_count=2, initial_tail_lot=0.03, used_margin_start=30.0, price_moves_count=10000, level_hits_count=1000, sections_opened_count=86, floating_pnl_changes_count=10000
- flat: status=INVALID_TEST_SETUP, closes=0, tail_end=0.03, tail_reduction=0.0, recovery_close_lot_sum=0, reserve=0, max_dd=21.81%, min_margin=26064.92%, stop_out=False, violations=0
  setup_checks: initial_positions_count=2, initial_tail_lot=0.03, used_margin_start=30.0, price_moves_count=9912, level_hits_count=0, sections_opened_count=0, floating_pnl_changes_count=10000
- flat_with_level_touch: status=PASS_RECOVERY, closes=51, tail_end=0.01, tail_reduction=0.02, recovery_close_lot_sum=0.02, reserve=0.88, max_dd=22.19%, min_margin=18444.67%, stop_out=False, violations=0
  setup_checks: initial_positions_count=2, initial_tail_lot=0.03, used_margin_start=30.0, price_moves_count=9870, level_hits_count=333, sections_opened_count=51, floating_pnl_changes_count=10000
- whipsaw: status=PASS_RECOVERY, closes=30, tail_end=0.01, tail_reduction=0.02, recovery_close_lot_sum=0.02, reserve=1.14, max_dd=0.02%, min_margin=19999.78%, stop_out=False, violations=0
  setup_checks: initial_positions_count=2, initial_tail_lot=0.03, used_margin_start=30.0, price_moves_count=10000, level_hits_count=10000, sections_opened_count=30, floating_pnl_changes_count=10000
- spike: status=PASS_RECOVERY, closes=18, tail_end=0.01, tail_reduction=0.02, recovery_close_lot_sum=0.02, reserve=6.75, max_dd=10.94%, min_margin=24868.9%, stop_out=False, violations=0
  setup_checks: initial_positions_count=2, initial_tail_lot=0.03, used_margin_start=30.0, price_moves_count=9961, level_hits_count=285, sections_opened_count=18, floating_pnl_changes_count=10000
- gap: status=PASS_RECOVERY, closes=8, tail_end=0.01, tail_reduction=0.02, recovery_close_lot_sum=0.02, reserve=0.9, max_dd=11.36%, min_margin=19960.47%, stop_out=False, violations=0
  setup_checks: initial_positions_count=2, initial_tail_lot=0.03, used_margin_start=30.0, price_moves_count=9961, level_hits_count=782, sections_opened_count=8, floating_pnl_changes_count=10000
- spike: status=PASS_RECOVERY, closes=20, tail_end=0.01, tail_reduction=0.02, recovery_close_lot_sum=0.02, reserve=6.51, max_dd=34.99%, min_margin=21671.65%, stop_out=False, violations=0
  setup_checks: initial_positions_count=2, initial_tail_lot=0.03, used_margin_start=30.0, price_moves_count=9957, level_hits_count=285, sections_opened_count=20, floating_pnl_changes_count=10000
- spike: status=FAIL_RISK_LIMIT, closes=24, tail_end=0.01, tail_reduction=0.02, recovery_close_lot_sum=0.02, reserve=6.61, max_dd=58.91%, min_margin=13695.4%, stop_out=False, violations=0
  setup_checks: initial_positions_count=2, initial_tail_lot=0.03, used_margin_start=30.0, price_moves_count=9971, level_hits_count=285, sections_opened_count=24, floating_pnl_changes_count=10000
- gap: status=PASS_RECOVERY, closes=5, tail_end=0.01, tail_reduction=0.02, recovery_close_lot_sum=0.02, reserve=0.95, max_dd=7.08%, min_margin=19977.84%, stop_out=False, violations=0
  setup_checks: initial_positions_count=2, initial_tail_lot=0.03, used_margin_start=30.0, price_moves_count=9980, level_hits_count=830, sections_opened_count=5, floating_pnl_changes_count=10000
- spike: status=PASS_RECOVERY, closes=19, tail_end=0.01, tail_reduction=0.02, recovery_close_lot_sum=0.02, reserve=6.64, max_dd=19.95%, min_margin=24707.85%, stop_out=False, violations=0
  setup_checks: initial_positions_count=2, initial_tail_lot=0.03, used_margin_start=30.0, price_moves_count=9973, level_hits_count=285, sections_opened_count=19, floating_pnl_changes_count=10000

## 1,000 Monte-Carlo runs (2,000 steps each)
- invalid_setup_runs=0
- status_counts: PASS_RECOVERY=1000, FAIL_NO_RECOVERY=0, FAIL_RISK_LIMIT=0, FAIL_STOP_OUT=0, FAIL_VIOLATION=0
- closes avg=56.19
- tail_end min/max/avg=0.0100/0.0100/0.0100
- tail_reduction avg=0.0200
- recovery_close_lot_sum avg=0.0200
- reserve min/max/avg=0.66/1.14/0.86
- max_dd avg=1.83%
- min_margin avg=19947.71%
- stop_out runs=0
- violation runs=0

## overall_set_status
REJECTED