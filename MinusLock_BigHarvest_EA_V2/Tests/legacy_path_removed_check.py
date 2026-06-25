from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
big_body = text.split("void ProcessBigHarvest()", 1)[1].split("void ProcessBigHarvestCloseBig()", 1)[0]
small_body = text.split("void ProcessSmallAtFarTouch()", 1)[1].split("void ProcessSmallScenario()", 1)[0]
scenario_body = text.split("void ProcessSmallScenario()", 1)[1].split("void ProcessFinalClose()", 1)[0]
for body in [big_body, small_body, scenario_body]:
    assert "ClosePositionByTicket" not in body
    assert "Ctx.totalReserve +=" not in body
assert "case STATE_BIG_HARVEST_CLOSE_BIG:\n         ProcessBigHarvestCloseBig();" in text
print("LEGACY_PATH_REMOVED_CHECK PASS")
