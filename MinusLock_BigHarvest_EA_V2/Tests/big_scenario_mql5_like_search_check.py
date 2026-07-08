import csv
from pathlib import Path
root = Path(__file__).resolve().parents[1]
script = root / 'Tools' / 'mql5_like_big_scenario_parameter_search.py'
search = root / 'Reports' / 'BigScenario_MQL5_Search_Journal.csv'
verify = root / 'Reports' / 'BigScenario_MQL5_Level1_Verification.csv'
top50 = root / 'Reports' / 'BigScenario_MQL5_Top50.md'
top10 = root / 'Reports' / 'BigScenario_MQL5_Top10.md'
recs = root / 'Reports' / 'BigScenario_MQL5_Programmer_Recommendations.md'
audit = root / 'Reports' / 'BigScenario_MQL5_Model_Audit.md'
limit = root / 'Reports' / 'BigScenario_MQL5_Minimum_Level_Limit.md'
sets = [
    root / 'Sets' / 'MQL5_Top_1.set',
    root / 'Sets' / 'MQL5_Top_2.set',
    root / 'Sets' / 'MQL5_Top_3.set',
    root / 'Sets' / 'MQL5_Universal.set',
    root / 'Sets' / 'MQL5_Conservative.set',
    root / 'Sets' / 'MQL5_Aggressive_Recovery.set',
    root / 'Sets' / 'MQL5_Minimum_Big_Levels.set',
]
for path in [script, search, verify, top50, top10, recs, audit, limit, *sets]:
    assert path.exists(), path
script_text = script.read_text(encoding='utf-8')
for token in ['MT5_BIG_SCENARIO_NET_L1 = 106.83', 'verify_mt5_l1', 'ROUND1_GLOBAL_300', 'ROUND2_TOP20_150', 'ROUND3_TOP5_100']:
    assert token in script_text, token
with verify.open(newline='', encoding='utf-8') as f:
    verify_rows = list(csv.DictReader(f))
assert verify_rows and all(r['Status'] == 'PASS' for r in verify_rows), verify_rows
with search.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
assert len(rows) >= 550, len(rows)
assert sum(1 for r in rows if r['RunGroup'] == 'ROUND1_GLOBAL_300') >= 299
assert sum(1 for r in rows if r['RunGroup'] == 'ROUND2_TOP20_150') == 150
assert sum(1 for r in rows if r['RunGroup'] == 'ROUND3_TOP5_100') == 100
for row in rows:
    assert float(row['StartLot']) == 1.0, row['TestID']
    assert row['CandidateStatus'] == 'MT5_CANDIDATE_NOT_CONFIRMED', row['TestID']
invalid = [r for r in rows if r['RunGroup'] == 'MT5_L1_INVALIDATED_PROFILE'][0]
assert invalid['FinalState'] == 'END_OF_TEST', invalid
assert int(invalid['BigLevelsUsed']) >= 11, invalid
assert 'ONTESTER_MINUS_1' in invalid['EndReason'], invalid
best = min((r for r in rows if r['FullCycleCompleted'] == 'YES'), key=lambda r: int(r['Rank']))
assert int(best['BigLevelsUsed']) <= 8, best
assert 'MT5_CANDIDATE_NOT_CONFIRMED' in top10.read_text(encoding='utf-8')
assert 'No MQL5 trading logic was changed' in audit.read_text(encoding='utf-8')
assert 'Minimum observed level count' in limit.read_text(encoding='utf-8')
for path in sets:
    text = path.read_text(encoding='utf-8')
    assert 'StartLot=1.00' in text, path
    assert 'MT5_CANDIDATE_NOT_CONFIRMED' in text, path
print('BIG_SCENARIO_MQL5_LIKE_SEARCH_CHECK PASS')
