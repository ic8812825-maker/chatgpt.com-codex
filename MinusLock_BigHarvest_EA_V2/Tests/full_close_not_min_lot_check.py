from pathlib import Path
root = Path(__file__).resolve().parents[1]
state = (root / "Include" / "StateMachine.mqh").read_text()
full_block = state.split("bool ApplyPendingCloseSuccessToContext()", 1)[1].split("void ClearPendingOperationContext()", 1)[0]
for forbidden in ["actualFarLot > minLot", "actualVolume > minLot", "> minLot +", "SYMBOL_VOLUME_MIN"]:
    assert forbidden not in full_block
assert "VerifyFullClose" in full_block
print("FULL_CLOSE_NOT_MIN_LOT_CHECK PASS")
