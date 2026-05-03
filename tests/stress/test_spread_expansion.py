from adaptive_lock_ev.calculator import get_recommendation
from tests.utils import base_args

def test_spread_expansion():
    a1=base_args(current_price=1.1040,ema=1.1000,atr_short=0.0020,last_10_cycles_pnl=10)
    a2=base_args(current_price=1.1040,ema=1.1000,atr_short=0.0020,last_10_cycles_pnl=10)
    a2['broker_params']['spread_points']=a1['broker_params']['spread_points']*5
    r1,r2=get_recommendation(**a1),get_recommendation(**a2)
    assert r2['min_move_points']>r1['min_move_points']
