import importlib.util
import sys
from pathlib import Path
root = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('simulate_big_scenario_trace', root / 'Tools' / 'simulate_big_scenario_trace.py')
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)
rows = mod.simulate(
    scenario='90_10',
    start_lot=1.0,
    big_ratio=1.15,
    small_ratio=0.25,
    close_far_share=0.90,
    reserve_share=0.10,
    close_big_on_small=0.40,
    remain_big_on_small=0.60,
    lot_step=0.01,
    point_value_per_lot=1.0,
    far_distance_points=200.0,
    big_move_points=100.0,
    max_levels=25,
)
previous_reserve = 0.0
for row in rows:
    assert abs(row.BigScenarioNet - (row.ClosedBigNet + row.ClosedSmallNet)) < 1e-7
    assert abs(row.CloseFarBudget - row.BigScenarioNet * 0.90) < 1e-7
    assert abs(row.ReserveAdd - row.BigScenarioNet * 0.10) < 1e-7
    assert row.CloseFarActualCost <= row.CloseFarBudget + 1e-7
    assert row.ReserveAfter >= previous_reserve - 1e-7
    previous_reserve = row.ReserveAfter
summary = mod.summarize(rows)
assert summary['TotalClosedFarLot'] > 0.0
assert rows[0].CloseFarBudget > rows[0].ReserveAdd
print('BIG_SCENARIO_90_10_SPLIT_CHECK PASS')
