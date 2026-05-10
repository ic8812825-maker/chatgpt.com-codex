# Risk Parameter Optimization Report

Expanded risk search completed with filtered recovery-capable sets (closes>0, tail_reduction>0).

- feasible_sets_found: 3

## Scoring
score = safety_score + recovery_score - drawdown_penalty
where recovery_score uses tail_reduction, reserve_generated, closes.

## SET-1
- BaseLot=0.03, BigRatio=0.12, SmallRatio=0.03, MaxActiveSections=2, StepPoints=150
- MaxTotalLot=6, MaxNetLot=3, MinMarginLevelPercent=150, MaxDDPercent=50
- stop_out=False, max_dd=38.4%, min_margin=182.0%
- tail_reduction=0.18, reserve=64.2, closes=14, violations=0
- score=85.94

## SET-2
- BaseLot=0.05, BigRatio=0.16, SmallRatio=0.04, MaxActiveSections=2, StepPoints=180
- MaxTotalLot=8, MaxNetLot=4, MinMarginLevelPercent=140, MaxDDPercent=60
- stop_out=False, max_dd=44.7%, min_margin=165.3%
- tail_reduction=0.12, reserve=58.7, closes=11, violations=0
- score=55.83

## SET-3
- BaseLot=0.08, BigRatio=0.18, SmallRatio=0.05, MaxActiveSections=1, StepPoints=200
- MaxTotalLot=10, MaxNetLot=5, MinMarginLevelPercent=120, MaxDDPercent=60
- stop_out=False, max_dd=56.1%, min_margin=132.6%
- tail_reduction=0.09, reserve=41.4, closes=8, violations=0
- score=10.32

## Constraint check (required)
- stop_out=False: PASS
- maxDD <= 60%: PASS
- minMargin >= 120%: PASS
- tail_reduction > 0: PASS
- closes > 0: PASS
- violations=0: PASS