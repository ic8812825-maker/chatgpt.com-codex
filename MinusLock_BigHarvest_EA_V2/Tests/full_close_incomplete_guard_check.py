from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / "Include" / "StateMachine.mqh").read_text()
for token in ["FULL_CLOSE_INCOMPLETE", "GetActualPositionVolume(Ctx.farTicket)", "PENDING_CLOSE_FAR_FULL", "PENDING_MAX_LEVELS_FINAL_CLOSE", "PENDING_STOP_MAX_LEVELS_CLOSE"]:
    assert token in state
assert "VerifyFullClose" in state
assert "ClearFarContext(\"full Far close confirmed by VerifyFullClose\")" in state
print("FULL_CLOSE_INCOMPLETE_GUARD_CHECK PASS")
