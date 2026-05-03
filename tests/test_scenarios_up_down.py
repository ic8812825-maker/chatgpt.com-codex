from adaptive_lock_ev.calculator import get_recommendation
from tests.utils import base_args

def test_trigger_directions():
    r = get_recommendation(**base_args(current_price=1.1000))
    assert r['scenario_up'][0].get('price', 99) >= 1.1000 or r['scenario_up'][0]['action']=='NO_ACTION'
    assert r['scenario_down'][0].get('price', 0) <= 1.1000 or r['scenario_down'][0]['action']=='NO_ACTION'
