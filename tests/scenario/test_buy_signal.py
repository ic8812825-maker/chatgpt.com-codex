from adaptive_lock_ev.calculator import get_recommendation
from tests.utils import base_args

def test_buy_signal():
    r=get_recommendation(**base_args(current_price=1.0960,ema=1.1000,atr_short=0.0020,last_10_cycles_pnl=10))
    assert r['scenario_down'][0]['action']=='OPEN'
