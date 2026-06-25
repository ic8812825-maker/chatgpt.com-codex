from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / "Include" / "StateMachine.mqh").read_text()
assert "bool VerifyFullClose(ulong ticket, string operationName)" in state
for token in ["GetActualPositionVolume(ticket)", "ExpectedVolume=0.00", "ActualVolume", "Difference", "FULL_CLOSE_INCOMPLETE"]:
    assert token in state
for operation in ["FINAL_CLOSE_PROFIT", "MAX_LEVELS_FINAL_CLOSE", "STOP_MAX_LEVELS_CLOSE_FAR", "PENDING_FULL_FAR_CLOSE"]:
    assert f'VerifyFullClose(Ctx.farTicket, "{operation}"' in state
print("VERIFY_FULL_CLOSE_CHECK PASS")
