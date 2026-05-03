from adaptive_lock_ev.calculator import get_recommendation
from tests.utils import base_args

def test_fsm_states():
    assert get_recommendation(**base_args(broker_dd=0.06))['state'] == 'FLOW'
    assert get_recommendation(**base_args(broker_dd=0.08))['state'] == 'STRESS'
    assert get_recommendation(**base_args(broker_dd=0.16))['state'] == 'ESCAPE'
