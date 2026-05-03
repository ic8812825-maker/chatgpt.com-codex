from adaptive_lock_ev.calculator import get_recommendation
from tests.utils import base_args

def test_trigger_down():
    cp=1.1000
    r=get_recommendation(**base_args(current_price=cp,ema=1.1030,atr_short=0.0020,last_10_cycles_pnl=10))
    if r['scenario_down'][0]['action']=='OPEN':
        assert r['scenario_down'][0]['price']<=cp
