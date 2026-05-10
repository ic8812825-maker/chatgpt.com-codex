# SET-1 Extended Validation

SET-1: {'BaseLot': 0.03, 'BigRatio': 0.12, 'SmallRatio': 0.03, 'MaxActiveSections': 2, 'StepPoints': 150, 'MaxTotalLot': 6, 'MaxNetLot': 3, 'MinMarginLevelPercent': 150, 'MaxDDPercent': 50}

## 10,000-step scenario results
- trend_up: status=FAIL, closes=0, tail_end=0.03, tail_reduction=0.0, reserve=0, max_dd=26.68%, min_margin=9999%, stop_out=False, violations=0
  setup_checks: initial_positions_count=2, initial_tail_lot=0.03, used_margin_start=30.0, price_moves_count=10000, level_hits_count=1000, sections_opened_count=2, floating_pnl_changes_count=10000
- trend_down: status=FAIL, closes=0, tail_end=0.03, tail_reduction=0.0, reserve=0, max_dd=26.68%, min_margin=9999%, stop_out=False, violations=0
  setup_checks: initial_positions_count=2, initial_tail_lot=0.03, used_margin_start=30.0, price_moves_count=10000, level_hits_count=1000, sections_opened_count=2, floating_pnl_changes_count=10000
- flat: status=INVALID_TEST_SETUP, closes=0, tail_end=0.03, tail_reduction=0.0, reserve=0, max_dd=34.78%, min_margin=9999%, stop_out=False, violations=0
  setup_checks: initial_positions_count=2, initial_tail_lot=0.03, used_margin_start=30.0, price_moves_count=9912, level_hits_count=0, sections_opened_count=0, floating_pnl_changes_count=10000
- whipsaw: status=FAIL, closes=0, tail_end=0.03, tail_reduction=0.0, reserve=0, max_dd=17.42%, min_margin=9999%, stop_out=False, violations=0
  setup_checks: initial_positions_count=2, initial_tail_lot=0.03, used_margin_start=30.0, price_moves_count=10000, level_hits_count=10000, sections_opened_count=2, floating_pnl_changes_count=10000
- spike: status=FAIL, closes=28, tail_end=0.01, tail_reduction=0.02, reserve=6.68, max_dd=26.91%, min_margin=9999%, stop_out=False, violations=0
  setup_checks: initial_positions_count=2, initial_tail_lot=0.03, used_margin_start=30.0, price_moves_count=9961, level_hits_count=285, sections_opened_count=28, floating_pnl_changes_count=10000
- gap: status=FAIL, closes=29, tail_end=0.01, tail_reduction=0.02, reserve=11.49, max_dd=27.11%, min_margin=9999%, stop_out=False, violations=0
  setup_checks: initial_positions_count=2, initial_tail_lot=0.03, used_margin_start=30.0, price_moves_count=9961, level_hits_count=782, sections_opened_count=29, floating_pnl_changes_count=10000
- spike: status=FAIL, closes=40, tail_end=0.01, tail_reduction=0.02, reserve=6.5, max_dd=62.93%, min_margin=9999%, stop_out=False, violations=0
  setup_checks: initial_positions_count=2, initial_tail_lot=0.03, used_margin_start=30.0, price_moves_count=9957, level_hits_count=285, sections_opened_count=40, floating_pnl_changes_count=10000
- spike: status=PASS, closes=39, tail_end=0.01, tail_reduction=0.02, reserve=6.78, max_dd=98.87%, min_margin=376.09%, stop_out=False, violations=0
  setup_checks: initial_positions_count=2, initial_tail_lot=0.03, used_margin_start=30.0, price_moves_count=9971, level_hits_count=285, sections_opened_count=39, floating_pnl_changes_count=10000
- gap: status=FAIL, closes=27, tail_end=0.01, tail_reduction=0.02, reserve=23.29, max_dd=23.84%, min_margin=9999%, stop_out=False, violations=0
  setup_checks: initial_positions_count=2, initial_tail_lot=0.03, used_margin_start=30.0, price_moves_count=9980, level_hits_count=830, sections_opened_count=27, floating_pnl_changes_count=10000
- spike: status=FAIL, closes=30, tail_end=0.01, tail_reduction=0.02, reserve=6.59, max_dd=35.91%, min_margin=9999%, stop_out=False, violations=0
  setup_checks: initial_positions_count=2, initial_tail_lot=0.03, used_margin_start=30.0, price_moves_count=9973, level_hits_count=285, sections_opened_count=30, floating_pnl_changes_count=10000

## 1,000 Monte-Carlo runs (2,000 steps each)
- invalid_setup_runs=0
- closes avg=8.13
- tail_end min/max/avg=0.0300/0.0300/0.0300
- reserve min/max/avg=0.00/0.02/0.01
- max_dd avg=5.14%
- min_margin avg=9999.00%
- stop_out runs=0
- violation runs=0

## Verdict
SET-1 is valid only for scenarios without INVALID_TEST_SETUP and with closes>0, tail_reduction>0, reserve>0, max_dd>0, used_margin>0, min_margin<9999, stop_out=False, violations=0.