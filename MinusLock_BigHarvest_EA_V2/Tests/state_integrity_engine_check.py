from pathlib import Path
root = Path(__file__).resolve().parents[1]
engine = (root / "Include" / "StateIntegrityEngine.mqh").read_text()
ea = (root / "MinusLock_BigHarvest_EA.mq5").read_text()
types = (root / "Include" / "Types.mqh").read_text()
state = (root / "Include" / "StateMachine.mqh").read_text()
assert "ValidateCurrentStateIntegrity" in engine
assert "STATE_INTEGRITY_ERROR" in types
assert 'Include/StateIntegrityEngine.mqh' in ea
assert "STATE_INTEGRITY_PASS" in engine and "STATE_INTEGRITY_FAIL" in engine
assert "ValidateCurrentStateIntegrity();" in state
print("PASS state_integrity_engine_check")
