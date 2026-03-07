from pathlib import Path


def test_fsm_states_exist():
    file = Path("Experts/VirtualPanel/right/ALEStateMachine.mqh")
    text = file.read_text(encoding="utf-8")

    states = ["IDLE", "BASE", "EXPANSION", "HARVEST", "RESET", "SAFE"]

    for state in states:
        assert state in text, f"Missing FSM state {state}"
