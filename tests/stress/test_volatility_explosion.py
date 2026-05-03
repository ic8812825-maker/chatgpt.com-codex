from adaptive_lock_ev.calculator import get_recommendation
from tests.utils import base_args

def test_volatility_explosion():
    r=get_recommendation(**base_args(current_price=1.1040,ema=1.1000,atr_short=0.0060,atr_long=0.0020,last_10_cycles_pnl=10))
    assert r['regime']=='VOLATILE'
    assert r['scenario_up'][0]['action']=='NO_ACTION'
