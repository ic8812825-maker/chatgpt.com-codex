# SET-1 Extended Validation

SET-1: {'BaseLot': 0.03, 'BigRatio': 0.12, 'SmallRatio': 0.03, 'MaxActiveSections': 2, 'StepPoints': 150, 'MaxTotalLot': 6, 'MaxNetLot': 3, 'MinMarginLevelPercent': 150, 'MaxDDPercent': 50}

## 10,000-step scenario results
- trend_up: closes=0, tail_end=0.03, tail_reduction=0.0, reserve=0, max_dd=0%, min_margin=9999%, stop_out=False, violations=0
- trend_down: closes=0, tail_end=0.03, tail_reduction=0.0, reserve=0, max_dd=0%, min_margin=9999%, stop_out=False, violations=0
- flat: closes=0, tail_end=0.03, tail_reduction=0.0, reserve=0, max_dd=0%, min_margin=9999%, stop_out=False, violations=0
- whipsaw: closes=0, tail_end=0.03, tail_reduction=0.0, reserve=0, max_dd=0%, min_margin=9999%, stop_out=False, violations=0
- spike: closes=0, tail_end=0.03, tail_reduction=0.0, reserve=0, max_dd=0%, min_margin=9999%, stop_out=False, violations=0
- gap: closes=0, tail_end=0.03, tail_reduction=0.0, reserve=0, max_dd=0%, min_margin=9999%, stop_out=False, violations=0
- spike: closes=0, tail_end=0.03, tail_reduction=0.0, reserve=0, max_dd=0%, min_margin=9999%, stop_out=False, violations=0
- spike: closes=0, tail_end=0.03, tail_reduction=0.0, reserve=0, max_dd=0%, min_margin=9999%, stop_out=False, violations=0
- gap: closes=0, tail_end=0.03, tail_reduction=0.0, reserve=0, max_dd=0%, min_margin=9999%, stop_out=False, violations=0
- spike: closes=0, tail_end=0.03, tail_reduction=0.0, reserve=0, max_dd=0%, min_margin=9999%, stop_out=False, violations=0

## 1,000 Monte-Carlo runs (2,000 steps each)
- closes avg=0.00
- tail_end min/max/avg=0.0300/0.0300/0.0300
- reserve min/max/avg=0.00/0.00/0.00
- max_dd avg=0.00%
- min_margin avg=9999.00%
- stop_out runs=0
- violation runs=0

## Verdict
SET-1 accepted for PAPER TEST ONLY if stop_out stays False and violations=0 in monitored scenarios.