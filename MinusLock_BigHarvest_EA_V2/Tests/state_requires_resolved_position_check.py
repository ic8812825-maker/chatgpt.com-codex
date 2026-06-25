from pathlib import Path
engine = (Path(__file__).resolve().parents[1] / "Include" / "StateIntegrityEngine.mqh").read_text()
open_big = engine[engine.index("case STATE_OPEN_NEW_BIG_PENDING:"):engine.index("case STATE_OPEN_NEW_SMALL_PENDING:")]
open_small = engine[engine.index("case STATE_OPEN_NEW_SMALL_PENDING:"):engine.index("case STATE_CLOSE_BIG_PENDING:")]
required_check = engine[engine.index("if(required && (ticket == 0 || identifier == 0))"):engine.index("if(required && ticket != 0)")]
assert "requireFar = true" in open_big and "forbidBig = true" in open_big and "forbidSmall = true" in open_big
assert "requireFar = true" in open_small and "requireBig = true" in open_small and "forbidSmall = true" in open_small
assert "ticket == 0 || identifier == 0" in required_check
print("PASS state_requires_resolved_position_check")
