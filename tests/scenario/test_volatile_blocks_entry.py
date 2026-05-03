from adaptive_lock_ev.calculator import get_recommendation
from tests.utils import base_args

def test_volatile_blocks_entry():
    r=get_recommendation(**base_args(current_price=1.1040,ema=1.1000,atr_short=0.0040,atr_long=0.0020))
    assert r['scenario_up'][0]['action']=='NO_ACTION'
