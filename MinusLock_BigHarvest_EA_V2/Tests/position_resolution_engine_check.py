from pathlib import Path
root = Path(__file__).resolve().parents[1]
engine = (root / "Include" / "PositionResolutionEngine.mqh").read_text()
ea = (root / "MinusLock_BigHarvest_EA.mq5").read_text()
types = (root / "Include" / "Types.mqh").read_text()
for token in ["PositionResolutionResult", "ResolveOpenedPosition", "ResolveOpenedPositionAfterOpen", "POSITION_RESOLUTION_START", "POSITION_RESOLUTION_PASS", "POSITION_RESOLUTION_FAIL", "POSITION_RESOLUTION_BY_COMMENT", "POSITION_RESOLUTION_BY_MAGIC", "POSITION_RESOLUTION_BY_IDENTIFIER", "POSITION_RESOLUTION_BY_TIME"]:
    assert token in engine or token in types
assert "STATE_POSITION_RESOLUTION_ERROR" in types
assert 'Include/PositionResolutionEngine.mqh' in ea
print("PASS position_resolution_engine_check")
