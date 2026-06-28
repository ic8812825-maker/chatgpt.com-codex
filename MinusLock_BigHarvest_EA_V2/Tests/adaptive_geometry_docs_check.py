from pathlib import Path
root = Path(__file__).resolve().parents[1]
manual = (root / 'Docs' / 'MANUAL.md').read_text()
plan = (root / 'Docs' / 'TEST_PLAN.md').read_text()
for token in ['Adaptive ATR Geometry', 'GEOMETRY_MANUAL', 'GEOMETRY_ATR_SAFE', 'GEOMETRY_ATR_BALANCED', 'GEOMETRY_ATR_PROFIT', 'GEOMETRY_ATR_CUSTOM', 'ATRTimeframe', 'ATRPeriod', 'Round-step', 'FreezeGeometryPerCycle', 'fallback']:
    assert token in manual, token
for token in ['Manual compatibility', 'ATR SAFE', 'ATR BALANCED', 'ATR PROFIT', 'ATR fallback', 'Freeze per cycle', 'ClearCycleGeometry', '190 / 190 / 75 / 250', '190 / 220 / 75 / 300', '200 / 230 / 85 / 300']:
    assert token in plan, token
print('ADAPTIVE_GEOMETRY_DOCS_CHECK PASS')
