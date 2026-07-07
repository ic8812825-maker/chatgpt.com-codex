import csv
from pathlib import Path
root = Path(__file__).resolve().parents[1]
script = root / 'Tools' / 'optimize_big_scenario_min_levels.py'
csv_path = root / 'Reports' / 'BigScenario_Parameter_Search.csv'
recs = root / 'Reports' / 'BigScenario_Parameter_Recommendations.md'
best = root / 'Reports' / 'BigScenario_Best_Presets.md'
sets = [root / 'Sets' / f'BigScenario_Best_{i}.set' for i in range(1, 4)]
for path in [script, csv_path, recs, best, *sets]:
    assert path.exists(), path
text = script.read_text(encoding='utf-8')
assert 'START_LOT = 1.00' in text
assert 'BigRatio^2 * RemainBigOnSmall < 1' in text
assert 'FIRST_ROUND_50_PLUS' in text and 'LOCAL_ROUND_AROUND_TOP' in text
with csv_path.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
assert len(rows) >= 70, len(rows)
first = [r for r in rows if r['RunGroup'] in {'BASELINE', 'FIRST_ROUND_50_PLUS'}]
local = [r for r in rows if r['RunGroup'] == 'LOCAL_ROUND_AROUND_TOP']
assert len(first) >= 50, len(first)
assert 15 <= len(local) <= 60, len(local)
for r in rows:
    assert float(r['StartLot']) == 1.0, r['TestID']
    assert abs(float(r['CloseFarShare']) + float(r['ReserveShare']) - 1.0) < 1e-9, r['TestID']
    assert float(r['BigRatio']) ** 2 * float(r['RemainBigOnSmall']) < 1.0, r['TestID']
accepted = [r for r in rows if r['FullCycleCompleted'] == 'YES' and r['FinalState'] == 'STATE_CLOSED_PROFIT' and float(r['RecoveryPL']) > 0]
assert accepted, 'no accepted rows'
top = min(accepted, key=lambda r: int(r['Rank']))
assert int(top['LevelsUsed']) <= 8, top
assert int(top['Rank']) == 1, top
for path in sets:
    data = path.read_text(encoding='utf-8')
    assert 'StartLot=1.00' in data, path
print('BIG_SCENARIO_PARAMETER_SEARCH_CHECK PASS')
