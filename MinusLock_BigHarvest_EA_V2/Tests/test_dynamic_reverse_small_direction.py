old_far=1.0; big_core=1.6; small_base=0.6; buffer_ratio=0.03
reverse_direction=big_core-old_far-small_base+old_far*buffer_ratio
assert abs(reverse_direction-0.03)<1e-9
print("PASS dynamic reverse small direction lot")
