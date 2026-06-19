from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
for token in ["TerminalStatesNeverOpen=YES", "SmallBuildUsesSavedSmallDirection=YES", "OldFarCleanup=YES",
              "terminal states must not route to RetryOpenNewBig/RetryOpenNewSmall/OpenBigSmall/OpenInitialLock",
              "pending open states are handled separately", "SmallBuildNewFar uses savedSmallDirection", "OldFar close clears Ctx.far*"]:
    assert token in text, token
print("FSM_INTEGRITY_STRICT_CHECK PASS")
