from adaptive_lock_ev.calculator import get_recommendation
from tests.utils import base_args

def test_commission_shock_blocks_when_ev_negative():
    a=base_args(current_price=1.1040,ema=1.1000,atr_short=0.0020,last_10_cycles_pnl=10)
    a['broker_params']['commission_per_lot']=120
    r=get_recommendation(**a)
    assert r['scenario_up'][0]['action']=='NO_ACTION'
