from pathlib import Path
root = Path(__file__).resolve().parents[1]
geom = (root / 'Include' / 'GeometryEngine.mqh').read_text()
assert 'if(Ctx.geometryCleared > 0 && Ctx.geometryClearReasonCode == clearReasonCode)' in geom
assert 'return;' in geom.split('void ClearCycleGeometry',1)[1].split('if(!CanClearCycleGeometry',1)[0]
print('ADAPTIVE_GEOMETRY_CLEAR_SPAM_CHECK PASS')
