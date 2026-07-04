from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / 'Include' / 'StateMachine.mqh').read_text()
for token in ['StateKey("CycleATRRaw")', 'StateKey("CycleATRPoints")', 'StateKey("GeometrySource")', 'StateKey("GeometryFallback")', 'StateKey("GeometryFallbackReasonCode")', 'StateKey("GeometryCleared")', 'StateKey("GeometryClearReasonCode")', 'StateKey("GeometryReady")', 'StateKey("TradingAllowedByFallback")', 'StateKey("WorkInitialTriggerPoints")', 'StateKey("WorkBigMoveStartPoints")', 'StateKey("WorkBigMoveStepPoints")', 'StateKey("WorkFarDistancePoints")', 'StateKey("GeometryModeUsed")', 'StateKey("GeometryCalculatedTime")']:
    assert token in state, token
for token in ['GetStateDouble("GeometryCleared"', 'GetStateDouble("GeometryClearReasonCode"', 'GetStateDouble("GeometryReady"', 'GetStateDouble("TradingAllowedByFallback"']:
    assert token in state, token
print('ADAPTIVE_GEOMETRY_GV_PERSISTENCE_CHECK PASS')
