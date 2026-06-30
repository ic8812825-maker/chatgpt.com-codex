from pathlib import Path
root = Path(__file__).resolve().parents[1]
geom = (root / 'Include' / 'GeometryEngine.mqh').read_text()
logger = (root / 'Include' / 'Logger.mqh').read_text()
types = (root / 'Include' / 'Types.mqh').read_text()
main = (root / 'MinusLock_BigHarvest_EA.mq5').read_text()
state = (root / 'Include' / 'StateMachine.mqh').read_text()

for token in ['SeriesInfoInteger(_Symbol, ATRTimeframe, SERIES_SYNCHRONIZED', 'Bars(_Symbol, ATRTimeframe)', 'iATR(_Symbol, ATRTimeframe, ATRPeriod)', 'INVALID_HANDLE', 'BarsCalculated(atrHandle)', 'CopyBuffer(atrHandle, 0, 1, 1, atrBuffer)', 'MathIsValidNumber', 'atrRaw / point']:
    assert token in geom, token
for reason in ['History not synchronized', 'Not enough bars', 'INVALID_HANDLE', 'BarsCalculated=0', 'CopyBuffer failed', 'ATR=NaN', 'ATR<=0', 'Point<=0']:
    assert reason in geom, reason
for token in ['ATR CALCULATION FAILED', 'fallback=MANUAL', '========== ADAPTIVE GEOMETRY ==========', 'Initial before round', 'BigStart before round', 'BigStep before round', 'Far before round', 'Geometry READY']:
    assert token in geom, token
for token in ['cycleATRRaw', 'geometrySource', 'geometryFallback', 'geometryFallbackReasonCode']:
    assert token in types, token
    assert token in state, token
for token in ['ATRRaw', 'GeometrySource', 'Fallback', 'FallbackReason']:
    assert token in logger, token
for token in ['ATRRaw=', 'GeometrySource=', 'Fallback=', 'Reason=']:
    assert token in geom, token
assert 'else\n      CalculateAdaptiveGeometry();' in main
print('ADAPTIVE_GEOMETRY_ATR_CHAIN_CHECK PASS')
