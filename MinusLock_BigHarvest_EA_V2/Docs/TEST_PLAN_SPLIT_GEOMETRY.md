# Split Geometry Test Plan

## Unit/static tests

Run all Python checks in `Tests/`, including:

```text
test_split_geometry_validation.py
test_big_net_exposure.py
test_reserve_growth_ratio.py
test_new_far_compression.py
test_dynamic_reverse_small_money.py
test_dynamic_reverse_small_direction.py
test_bigtrend_never_becomes_far.py
test_split_big_full_harvest.py
test_small_transition.py
test_restart_after_bigtrend_close.py
test_restart_after_reverse_small_open.py
test_symbol_magic_cycle_isolation.py
```

## MT5 scenarios for later stages

A. No-pullback Big: Far=1.00, BigCore=1.60, BigTrend=0.25, SmallBase=0.60; target moves 280/300/320.

B. One Small reverse: move +120, retrace -50; BigTrend closed, ReverseSmall calculated, Far touched; expected NewFar ≈ 0.96 OldFar.

C. Saw-tooth reverse stress: 8-10 reverses; expected Far compression and Reserve growth in ideal model.

D. Gap back to Far while BigTrend is open; expected BigTrend emergency close and actual BigTrend net in DynamicReverseSmall.
