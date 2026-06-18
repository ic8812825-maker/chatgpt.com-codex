from pathlib import Path
text = (Path(__file__).resolve().parents[1] / "Include" / "StateMachine.mqh").read_text()
main = (Path(__file__).resolve().parents[1] / "MinusLock_BigHarvest_EA.mq5").read_text()
assert "ValidateFSMIntegrity" in text
assert "ValidateFSMIntegrity()" in main
for token in ["unreachable states", "dead states", "states without handlers", "states without transitions", "states without retry"]:
    assert token in text
print("FSM_INTEGRITY_CHECK PASS")
