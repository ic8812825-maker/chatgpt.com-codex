def get_big_move_points(level, start=100, step=50):
    if level <= 0:
        return 0
    return start + (level - 1) * step


assert get_big_move_points(0) == 0
assert get_big_move_points(1) == 100
assert get_big_move_points(2) == 150
assert get_big_move_points(3) == 200
assert get_big_move_points(4) == 250
assert get_big_move_points(5) == 300
assert get_big_move_points(6) == 350
assert get_big_move_points(7) == 400

print("BIG_MOVE_LEVELS_CHECK PASS")
