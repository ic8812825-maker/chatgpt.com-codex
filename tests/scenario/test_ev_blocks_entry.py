from adaptive_lock_ev.calculator import get_recommendation
from tests.utils import base_args

def test_ev_blocks_entry():
    a=base_args(current_price=1.1040,ema=1.1000,atr_short=0.0020)
    a['broker_params']['spread_points']=20
    r=get_recommendation(**a)
    assert 'EV <= 0' in r['scenario_up'][0]['comment']
