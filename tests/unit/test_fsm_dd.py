from adaptive_lock_ev.calculator import _state

def test_fsm_dd():
    assert _state(0.06)=='FLOW'
    assert _state(0.07)=='FLOW'
    assert _state(0.071)=='STRESS'
    assert _state(0.15)=='STRESS'
    assert _state(0.151)=='ESCAPE'
