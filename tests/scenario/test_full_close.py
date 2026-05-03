from adaptive_lock_ev.calculator import get_recommendation
from tests.utils import base_args

def test_full_close_like_case():
    ps=[{'id':1,'type':'BUY','lot':0.01,'open_price':1.0500},{'id':2,'type':'SELL','lot':0.1,'open_price':1.1020}]
    r=get_recommendation(**base_args(current_price=1.1040,ema=1.1000,atr_short=0.0020,positions=ps,last_10_cycles_pnl=10))
    assert r['scenario_up'][0]['action'] in ['OPEN','NO_ACTION']
