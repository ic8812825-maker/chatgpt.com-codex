import importlib.util
import sys
from pathlib import Path
root = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('simulate_big_scenario_trace', root / 'Tools' / 'simulate_big_scenario_trace.py')
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)
common = dict(
    start_lot=1.0,
    big_ratio=1.15,
    small_ratio=0.25,
    close_big_on_small=0.40,
    remain_big_on_small=0.60,
    lot_step=0.01,
    point_value_per_lot=1.0,
    far_distance_points=200.0,
    big_move_points=100.0,
    max_levels=25,
)
rows90 = mod.simulate(scenario='90_10', close_far_share=0.90, reserve_share=0.10, **common)
rows20 = mod.simulate(scenario='20_80', close_far_share=0.20, reserve_share=0.80, **common)
s90 = mod.summarize(rows90)
s20 = mod.summarize(rows20)
assert s90['TotalClosedFarLot'] > s20['TotalClosedFarLot']
assert s90['RemainingFarLot'] < s20['RemainingFarLot']
assert s20['ReserveAfter'] > s90['ReserveAfter']
assert s90['LevelsToFinalClose'] != s20['LevelsToFinalClose']
assert rows90[0].CloseFarBudget > rows20[0].CloseFarBudget
assert rows20[0].ReserveAdd > rows90[0].ReserveAdd
print('BIG_SCENARIO_20_80_VS_90_10_CHECK PASS')
