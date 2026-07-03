import csv
import importlib.util
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
module_path = root / 'Tools' / 'simulate_big_scenario_trace.py'
spec = importlib.util.spec_from_file_location('simulate_big_scenario_trace', module_path)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)

rows_by_scenario = mod.default_runs(type('Args', (), {
    'start_lot': 1.0,
    'big_ratio': 1.15,
    'small_ratio': 0.25,
    'close_big_on_small': 0.40,
    'remain_big_on_small': 0.60,
    'lot_step': 0.01,
    'point_value_per_lot': 1.0,
    'far_distance_points': 200.0,
    'big_move_points': 100.0,
    'max_levels': 25,
})())
all_rows = [row for rows in rows_by_scenario.values() for row in rows]
assert all_rows
assert all(row.InvariantStatus == 'PASS' for row in all_rows)
mod.write_csv(all_rows)
mod.write_report(rows_by_scenario)
assert mod.CSV_PATH.exists(), mod.CSV_PATH
assert mod.MD_PATH.exists(), mod.MD_PATH
with mod.CSV_PATH.open(newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    required = {'Scenario', 'Level', 'ClosedBigNet', 'ClosedSmallNet', 'BigScenarioNet', 'CloseFarBudget', 'ReserveAdd', 'CloseFarActualCost', 'FarLotAfter', 'ReserveAfter', 'InvariantStatus'}
    assert required.issubset(reader.fieldnames), reader.fieldnames
    csv_rows = list(reader)
assert csv_rows and all(row['InvariantStatus'] == 'PASS' for row in csv_rows)
report = mod.MD_PATH.read_text(encoding='utf-8')
assert 'BigScenarioNet = ClosedBigNet + ClosedSmallNet' in report
assert '90/10 vs 20/80 comparison' in report
print('BIG_SCENARIO_TRACE_SIMULATION_CHECK PASS')
