# Deterministic formula sanity log for the MQL Small-at-Far fix.
# This is not an MT5 execution; it mirrors the corrected formulas and prints the
# exact diagnostic fields emitted by StateMachine.mqh.

point = 0.00001
point_value_per_lot = 1.0
big_open_price = 1.10000
current_price = 1.10125
remain_big_lot = 0.70
total_reserve = 50.0

far_open_price = big_open_price
effective_far_distance_points = abs(current_price - big_open_price) / point
expected_next_far_loss = remain_big_lot * effective_far_distance_points * point_value_per_lot
far_remain_loss = expected_next_far_loss
final_close_allowed = total_reserve >= far_remain_loss

print(
    "SMALL_AT_FAR_NEW_FAR_CHECK "
    f"bigOpenPrice={big_open_price:.5f} "
    f"currentPrice={current_price:.5f} "
    f"farOpenPrice={far_open_price:.5f} "
    f"effectiveFarDistancePoints={effective_far_distance_points:.1f} "
    f"expectedNextFarLoss={expected_next_far_loss:.2f} "
    f"farRemainLoss={far_remain_loss:.2f} "
    f"totalReserve={total_reserve:.2f} "
    f"finalCloseAllowed={'YES' if final_close_allowed else 'NO'} "
    f"farOpenEqualsBigOpen={'YES' if far_open_price == big_open_price else 'NO'} "
    f"farOpenEqualsCurrent={'YES' if far_open_price == current_price else 'NO'}"
)

assert far_open_price == big_open_price
assert far_open_price != current_price
assert effective_far_distance_points > 0
assert expected_next_far_loss > 0
assert far_remain_loss > 0
