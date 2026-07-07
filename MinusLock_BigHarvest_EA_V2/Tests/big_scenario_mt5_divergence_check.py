import csv
from pathlib import Path
root = Path(__file__).resolve().parents[1]
script = root / 'Tools' / 'analyze_mt5_big_scenario_divergence.py'
report = root / 'Reports' / 'BigScenario_MT5_Divergence_Report.md'
csv_path = root / 'Reports' / 'BigScenario_MT5_Divergence.csv'
recs = root / 'Reports' / 'BigScenario_Parameter_Recommendations.md'
audit = root / 'Docs' / 'BIG_SCENARIO_FULL_AUDIT.md'
for path in [script, report, csv_path, recs, audit]:
    assert path.exists(), path
script_text = script.read_text(encoding='utf-8')
for token in ['MT5_LEVEL_REACHED = 11', 'MT5_ON_TESTER = -1', 'MT5_CLOSED_BIG_NET = 147.73', 'MT5_FAR_PARTIAL_REAL_LOSS = 78.27']:
    assert token in script_text, token
report_text = report.read_text(encoding='utf-8')
for token in ['invalidates the previous offline optimizer claim', 'first material divergence', 'BigScenarioNet=106.83', 'FarDistanceMode=REAL_PRICE_DISTANCE', 'optimizer must **not** be used']:
    assert token in report_text, token
recs_text = recs.read_text(encoding='utf-8')
assert 'MT5 invalidation notice' in recs_text
assert 'not be used as working-parameter recommendations' in recs_text
audit_text = audit.read_text(encoding='utf-8')
assert 'MT5 Strategy Tester invalidation addendum' in audit_text
assert 'current Python optimizer is invalid for selecting working MT5 parameters' in audit_text
with csv_path.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
assert any(row['Metric'] == 'BigScenarioNet L1' and row['MT5Tester'] == '106.83' for row in rows)
assert any(row['Metric'] == 'Next action after L1' and 'Open MinusLock_BIG_L2' in row['MT5Tester'] for row in rows)
print('BIG_SCENARIO_MT5_DIVERGENCE_CHECK PASS')
