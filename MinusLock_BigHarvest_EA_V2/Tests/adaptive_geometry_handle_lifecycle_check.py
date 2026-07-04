from pathlib import Path
root = Path(__file__).resolve().parents[1]
geom = (root / 'Include' / 'GeometryEngine.mqh').read_text()
main = (root / 'MinusLock_BigHarvest_EA.mq5').read_text()
for token in ['g_atrHandle', 'EnsureATRHandle()', 'ATR_HANDLE_CREATE_START', 'ATR_HANDLE_CREATE_OK', 'ATR_HANDLE_CREATE_FAIL', 'ReleaseATRHandle()', 'IndicatorRelease(g_atrHandle)']:
    assert token in geom, token
assert 'iATR(_Symbol, ATRTimeframe, ATRPeriod)' in geom
assert 'ReleaseATRHandle();' in main
assert 'CopyBuffer(g_atrHandle, 0, 1, 1, atrBuffer)' in geom
print('ADAPTIVE_GEOMETRY_HANDLE_LIFECYCLE_CHECK PASS')
