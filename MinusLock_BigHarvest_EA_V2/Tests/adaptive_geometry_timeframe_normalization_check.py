from pathlib import Path
root = Path(__file__).resolve().parents[1]
geom = (root / 'Include' / 'GeometryEngine.mqh').read_text()
for token in ['EffectiveATRTimeframe()', 'if(tf == 60) return PERIOD_H1;', 'ATRTimeframeToString()', 'normalized_from_%d']:
    assert token in geom, token
assert 'iATR(_Symbol, EffectiveATRTimeframe(), ATRPeriod)' in geom
assert 'Bars(_Symbol, EffectiveATRTimeframe())' in geom
assert 'SeriesInfoInteger(_Symbol, EffectiveATRTimeframe(), SERIES_SYNCHRONIZED' in geom
print('ADAPTIVE_GEOMETRY_TIMEFRAME_NORMALIZATION_CHECK PASS')
