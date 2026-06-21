from pathlib import Path
import re
root = Path(__file__).resolve().parents[1]
types = (root / "Include" / "Types.mqh").read_text()
engine = (root / "Include" / "StateIntegrityEngine.mqh").read_text()
body = re.search(r"enum EAState\s*\{(.*?)\};", types, re.S).group(1)
states = re.findall(r"\b(STATE_[A-Z0-9_]+)\b", body)
missing = [state for state in states if f"case {state}:" not in engine]
assert not missing, missing
for phase in ["STATE_BIG_HARVEST_CLOSE_BIG", "STATE_BIG_HARVEST_CLOSE_SMALL", "STATE_SMALL_CLOSE_OLD_FAR", "STATE_SMALL_BUILD_NEW_FAR", "STATE_FINAL_CLOSE"]:
    assert f"case {phase}:" in engine
assert "STATE_INTEGRITY_MATRIX" in engine
print("PASS phase_state_matrix_check")
