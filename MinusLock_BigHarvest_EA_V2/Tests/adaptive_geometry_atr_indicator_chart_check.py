from pathlib import Path
root = Path(__file__).resolve().parents[1]
config = (root / 'Include' / 'Config.mqh').read_text()
geom = (root / 'Include' / 'GeometryEngine.mqh').read_text()
main = (root / 'MinusLock_BigHarvest_EA.mq5').read_text()
assert 'input bool ShowATRIndicatorOnChart = true;' in config
for token in ['ChartIndicatorAdd', 'ATR_INDICATOR_ADD_OK', 'ATR_INDICATOR_ADD_FAIL', 'EnsureATRIndicatorOnChart']:
    assert token in geom, token
assert 'EnsureATRIndicatorOnChart();' in main
print('ADAPTIVE_GEOMETRY_ATR_INDICATOR_CHART_CHECK PASS')
