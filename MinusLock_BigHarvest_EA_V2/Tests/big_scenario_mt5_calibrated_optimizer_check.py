import csv
from pathlib import Path
root = Path(__file__).resolve().parents[1]
script = root / 'Tools' / 'optimize_big_scenario_min_levels.py'
calibrator = root / 'Tools' / 'calibrate_big_scenario_model_from_mt5_report.py'
diff = root / 'Reports' / 'Python_vs_MT5_BigScenario_Diff.md'
cal_csv = root / 'Reports' / 'BigScenario_MT5_Calibrated_Parameter_Search.csv'
cal_recs = root / 'Reports' / 'BigScenario_MT5_Calibrated_Recommendations.md'
limits = root / 'Reports' / 'BigScenario_Model_Limitations.md'
sets = [root / 'Sets' / f'MT5_Candidate_BigScenario_{i}.set' for i in range(1, 4)]
for path in [script, calibrator, diff, cal_csv, cal_recs, limits, *sets]:
    assert path.exists(), path
script_text = script.read_text(encoding='utf-8')
assert 'POINT_VALUE_PER_LOT = 0.54322486' in script_text
assert 'POINT_VALUE_PER_LOT = 1.0' not in script_text
for token in ['END_OF_TEST', 'ONTESTER_MINUS_1', 'RemainingFarLot', 'BIG_L9+', 'MT5_CANDIDATE_NOT_CONFIRMED']:
    assert token in script_text or token in cal_recs.read_text(encoding='utf-8') or token in limits.read_text(encoding='utf-8'), token
with cal_csv.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
assert len(rows) >= 300, len(rows)
for row in rows:
    assert float(row['StartLot']) == 1.0, row['TestID']
invalid = [r for r in rows if r['RunGroup'] == 'MT5_INVALIDATED_PROFILE']
assert invalid, 'missing invalidated profile'
invalid = invalid[0]
assert invalid['FullCycleCompleted'] == 'NO', invalid
assert invalid['FinalState'] == 'END_OF_TEST', invalid
assert 'BIG_L11' in invalid['StopReason'] and 'ONTESTER_MINUS_1' in invalid['StopReason'], invalid
assert int(invalid['LevelsUsed']) >= 11, invalid
assert float(invalid['RemainingFarLot']) > 0.0, invalid
ranked = sorted(rows, key=lambda r: int(r['Rank']))
assert int(invalid['Rank']) > 10, invalid
assert all('MT5_CANDIDATE_NOT_CONFIRMED' in cal_recs.read_text(encoding='utf-8') for _ in [0])
diff_text = diff.read_text(encoding='utf-8')
assert 'OLD_OFFLINE_MODEL_INVALID_FOR_FINAL_SELECTION' in diff_text
assert 'first divergence is level 1 `BigScenarioNet`' in diff_text
for path in sets:
    assert 'StartLot=1.00' in path.read_text(encoding='utf-8'), path
print('BIG_SCENARIO_MT5_CALIBRATED_OPTIMIZER_CHECK PASS')
