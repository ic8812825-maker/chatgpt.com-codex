from pathlib import Path
root = Path(__file__).resolve().parents[1]
geom = (root / 'Include' / 'GeometryEngine.mqh').read_text()
state = (root / 'Include' / 'StateMachine.mqh').read_text()
recovery = (root / 'Include' / 'RecoveryMath.mqh').read_text()
logger = (root / 'Include' / 'Logger.mqh').read_text()
doc = (root / 'Docs' / 'ADAPTIVE_GEOMETRY_LIFECYCLE_AUDIT.md').read_text()

for token in [
    'ResetCycleGeometryFields("OpenInitialLock new cycle")',
    'bool EnsureCycleGeometry(string reason)',
    'ADAPTIVE_GEOMETRY_MISSING',
    'ADAPTIVE_GEOMETRY_FREEZE_KEEP',
    'EnsureCycleGeometry("RecoverState restored active or pending context without saved Work geometry")',
]:
    assert token in geom + state, token

for accessor in ['WorkInitialTriggerPoints', 'WorkBigMoveStartPoints', 'WorkBigMoveStepPoints', 'WorkFarDistancePoints']:
    block = geom.split(f'int {accessor}()', 1)[1].split('\n}\n', 1)[0]
    assert 'EnsureCycleGeometry(' in block, accessor

for bad in [
    'Ctx.cycleATRRaw = 0.0; Ctx.cycleATRPoints = 0.0; Ctx.workInitialTriggerPoints = 0',
]:
    assert bad not in state, bad

assert 'CopyBuffer(g_atrHandle, 0, 1, 1, atrBuffer)' in geom
assert 'IndicatorRelease(g_atrHandle)' in geom
assert 'WorkBigMoveStartPoints() + (level - 1) * WorkBigMoveStepPoints()' in recovery
assert 'WorkFarDistancePoints()' in recovery
for csv_token in ['"ConfiguredGeometryMode"', '"ATRRaw"', '"ATRPoints"', '"GeometrySource"', '"FallbackReason"', '"WorkInitialTriggerPoints"']:
    assert csv_token in logger, csv_token
for doc_token in ['Call map', 'ATR lifecycle', 'Work field lifecycle', 'Geometry read table', 'Freeze per cycle', 'Clear policy']:
    assert doc_token in doc, doc_token
print('ADAPTIVE_GEOMETRY_LIFECYCLE_AUDIT_CHECK PASS')
