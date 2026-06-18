from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
body = text.split("void ProcessBigHarvest()", 1)[1].split("void ProcessBigHarvestCloseBig()", 1)[0]
assert "SetState(STATE_BIG_HARVEST_CLOSE_BIG" in body
assert "ClosePositionByTicket" not in body
assert "ProcessBigHarvestCloseBig" in text
assert "case STATE_BIG_HARVEST_CLOSE_BIG:" in text
assert "ProcessBigHarvestCloseBig();" in text
print("PHASE_BIG_HARVEST_FSM_CHECK PASS")
