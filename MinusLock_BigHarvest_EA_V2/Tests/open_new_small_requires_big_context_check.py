from pathlib import Path
engine = (Path(__file__).resolve().parents[1] / "Include" / "StateIntegrityEngine.mqh").read_text()
open_small = engine[engine.index("case STATE_OPEN_NEW_SMALL_PENDING:"):engine.index("case STATE_CLOSE_BIG_PENDING:")]
assert "requireBig = true" in open_small
assert "forbidSmall = true" in open_small
assert "INVALID_STATE_SHAPE" in engine and "unresolved ticket/identifier" in engine
print("PASS open_new_small_requires_big_context_check")
