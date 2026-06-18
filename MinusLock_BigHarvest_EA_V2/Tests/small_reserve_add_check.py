def small_reserve_add(real_net, share=0.05):
    if real_net <= 0:
        return 0.0
    return real_net * share

assert small_reserve_add(100.0) == 5.0
assert small_reserve_add(0.0) == 0.0
assert small_reserve_add(-10.0) == 0.0
reserve = 90.0
new_far_loss = 87.5
assert reserve >= new_far_loss
reserve = 50.0
assert reserve < new_far_loss
print("SMALL_RESERVE_ADD_CHECK PASS")
