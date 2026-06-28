from pathlib import Path
root = Path(__file__).resolve().parents[1]
config = (root / 'Include' / 'Config.mqh').read_text()
geom = (root / 'Include' / 'GeometryEngine.mqh').read_text()
types = (root / 'Include' / 'Types.mqh').read_text()
state = (root / 'Include' / 'StateMachine.mqh').read_text()
main = (root / 'MinusLock_BigHarvest_EA.mq5').read_text()
logger = (root / 'Include' / 'Logger.mqh').read_text()
recovery = (root / 'Include' / 'RecoveryMath.mqh').read_text()
sets = (root / 'Tools' / 'generate_set_files.py').read_text()

for token in [
    'enum GeometryModeEnum', 'GEOMETRY_MANUAL', 'GEOMETRY_ATR_SAFE',
    'GEOMETRY_ATR_BALANCED', 'GEOMETRY_ATR_PROFIT', 'GEOMETRY_ATR_CUSTOM',
    'input GeometryModeEnum GeometryMode = GEOMETRY_MANUAL', 'input ENUM_TIMEFRAMES ATRTimeframe = PERIOD_M30',
    'input int ATRPeriod = 14', 'input bool FreezeGeometryPerCycle = true'
]:
    assert token in config, token

for token in [
    'double cycleATRPoints', 'int workInitialTriggerPoints', 'int workBigMoveStartPoints',
    'int workBigMoveStepPoints', 'int workFarDistancePoints', 'int geometryModeUsed',
    'datetime geometryCalculatedTime'
]:
    assert token in types, token

for token in [
    'int RoundToStep(double value, int step)', 'int ClampInt(int value, int minValue, int maxValue)',
    'bool CalculateAdaptiveGeometry()', 'bool InitializeCycleGeometry()', 'void ApplyGeometryPresetMultipliers',
    'void PrintGeometryDiagnostics()', 'CopyBuffer(atrHandle, 0, 1, 1, atrBuffer)',
    'UseManualGeometryFallback("ATR_NOT_AVAILABLE")', 'WARNING: Adaptive geometry failed. Manual geometry fallback used.',
    'ADAPTIVE_GEOMETRY_CALCULATED', 'GEOMETRY_MODE=MANUAL', 'UpdateGeometryPanel()'
]:
    assert token in geom, token

assert 'if(GeometryMode == GEOMETRY_MANUAL)' in geom
assert 'return InitialTriggerPoints;' in geom
assert 'WorkBigMoveStartPoints() + (level - 1) * WorkBigMoveStepPoints()' in recovery
assert 'WorkFarDistancePoints()' in recovery
for raw in ['buyProfitPoints >= WorkInitialTriggerPoints()', 'sellProfitPoints >= WorkInitialTriggerPoints()', 'InitializeCycleGeometry();']:
    assert raw in state, raw
for token in ['CycleATRPoints', 'WorkInitialTriggerPoints', 'WorkBigMoveStartPoints', 'WorkBigMoveStepPoints', 'WorkFarDistancePoints', 'GeometryModeUsed', 'GeometryCalculatedTime']:
    assert token in state, token
for token in ['GeometryMode', 'ATRTimeframe', 'ATRPeriod', 'ATRPoints', 'WorkInitialTriggerPoints', 'FreezeGeometryPerCycle']:
    assert token in logger, token
for token in ['"GeometryMode"', '"ATRTimeframe"', '"FreezeGeometryPerCycle"']:
    assert token in sets, token
assert '#include "Include/GeometryEngine.mqh"' in main
print('ADAPTIVE_GEOMETRY_STATIC_CHECK PASS')
