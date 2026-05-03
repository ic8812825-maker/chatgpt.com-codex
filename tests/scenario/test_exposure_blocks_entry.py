from adaptive_lock_ev.calculator import get_recommendation
from tests.utils import base_args

def test_exposure_blocks_entry():
    ps=[{'id':1,'type':'BUY','lot':0.16,'open_price':1.09},{'id':2,'type':'SELL','lot':0.10,'open_price':1.11}]
    r=get_recommendation(**base_args(current_price=1.1040,ema=1.1000,atr_short=0.0020,positions=ps))
    assert r['scenario_up'][0]['action']=='NO_ACTION'
