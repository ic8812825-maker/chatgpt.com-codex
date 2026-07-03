import csv
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
config = root / 'Include' / 'Config.mqh'
report = root / 'Reports' / 'Full_Parameter_Optimization_Report.md'
summary = root / 'Reports' / 'Parameter_Optimization_Summary.csv'
candidates = root / 'Reports' / 'Full_Parameter_Optimization_Candidates.csv'
sensitivity = root / 'Reports' / 'Parameter_Sensitivity.csv'
dependency = root / 'Reports' / 'Parameter_Dependency_Data.csv'
preset_dir = root / 'Sets' / 'Optimization_Presets'
script = root / 'Tools' / 'run_full_parameter_optimization_study.py'

for path in [report, summary, candidates, sensitivity, dependency, script]:
    assert path.exists(), path

inputs = []
for line in config.read_text().splitlines():
    m = re.match(r'^input\s+.+?\s+(\w+)\s*=', line.strip())
    if m:
        inputs.append(m.group(1))
with summary.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
summary_params = {row['Parameter'] for row in rows}
missing = set(inputs) - summary_params
assert not missing, sorted(missing)
for row in rows:
    assert row['RecommendedValue'] != '', row
    assert row['WorkingRange'] != '', row
    assert row['Influence'] != '', row

text = report.read_text(encoding='utf-8')
for token in ['Search methodology', 'Top candidates', 'Recommended configuration', 'Sensitivity summary', 'Mathematical dependency data', 'Required preset set files', 'Maximum Big Level', 'Minimum_Big_Levels.set', 'Recommended.set']:
    assert token in text, token
with candidates.open(newline='', encoding='utf-8') as f:
    candidate_rows = list(csv.DictReader(f))
with dependency.open(newline='', encoding='utf-8') as f:
    dependency_rows = list(csv.DictReader(f))
assert {'BigRatio', 'SmallRatio', 'CloseFarShare', 'ReserveShare', 'ATRPeriod', 'FarDistancePoints'}.issubset({row['Parameter'] for row in dependency_rows})
assert len(candidate_rows) >= 400
methods = {row['Method'] for row in candidate_rows}
for method in ['Full Grid', 'Random Search', 'Latin Hypercube', 'Bayesian Candidate', 'Local Refinement', 'Preset']:
    assert method in methods, method
print('FULL_PARAMETER_OPTIMIZATION_STUDY_CHECK PASS')
