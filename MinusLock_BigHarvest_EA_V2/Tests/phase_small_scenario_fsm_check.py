from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
scenario_body = text.split("void ProcessSmallScenario()", 1)[1].split("void ProcessFinalClose()", 1)[0]
touch_body = text.split("void ProcessSmallAtFarTouch()", 1)[1].split("void ProcessSmallScenario()", 1)[0]
assert "SetState(STATE_SMALL_CLOSE_SMALL" in scenario_body
assert "SetState(STATE_SMALL_CLOSE_SMALL" in touch_body
for forbidden in ["ClosePositionByTicket", "SMALL_RESERVE_ADD", "SMALL_AT_FAR_NEW_FAR_CHECK"]:
    assert forbidden not in scenario_body
    assert forbidden not in touch_body
for handler in ["ProcessSmallCloseSmall", "ProcessSmallCloseOldFar", "ProcessSmallCloseBigPart", "ProcessSmallBuildNewFar", "ProcessSmallCheckReserve"]:
    assert handler in text
print("PHASE_SMALL_SCENARIO_FSM_CHECK PASS")
