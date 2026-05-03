from adaptive_lock_ev.calculator import get_recommendation
from tests.utils import base_args

def test_mean_reversion_success():
    ps=[{'id':1,'type':'BUY','lot':0.1,'open_price':1.0900},{'id':2,'type':'SELL','lot':0.1,'open_price':1.1020}]
    r1=get_recommendation(**base_args(current_price=1.0960,ema=1.1000,atr_short=0.0020,positions=ps,last_10_cycles_pnl=10))
    r2=get_recommendation(**base_args(current_price=1.1005,ema=1.1000,atr_short=0.0020,positions=ps,last_10_cycles_pnl=10))
    assert r1['scenario_down'][0]['action']=='OPEN'
    assert r2['q']<=0.02
