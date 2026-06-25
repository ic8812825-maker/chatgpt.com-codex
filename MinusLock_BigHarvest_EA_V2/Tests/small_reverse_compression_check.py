def compression_ok(big_ratio=1.20, remain_big_on_small=0.65):
    return big_ratio * big_ratio * remain_big_on_small < 1.0

old_far = 100.0
big_ratio = 1.20
small_ratio = 0.35
close_big_on_small = 0.35
remain_big_on_small = 0.65
old_big = old_far * big_ratio
new_far = old_big * remain_big_on_small
new_big = new_far * big_ratio
new_small = new_big * small_ratio

assert abs((close_big_on_small + remain_big_on_small) - 1.0) <= 0.000001
assert compression_ok(big_ratio, remain_big_on_small)
assert new_far == old_big * remain_big_on_small
assert new_big == new_far * big_ratio
assert new_big < old_far
assert round(new_far, 2) == 78.00
assert round(new_big, 2) == 93.60
assert round(new_small, 2) == 32.76
print("SMALL_REVERSE_COMPRESSION_CHECK PASS")
