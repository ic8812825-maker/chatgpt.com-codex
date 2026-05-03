from adaptive_lock_ev.calculator import get_recommendation
from tests.utils import base_args

def test_real_scenario_lock_reduction_signal_flow():
    prices=[1.1000,1.1020,1.1040,1.1030,1.1010]
    positions=[{"id":1,"type":"BUY","lot":0.1,"open_price":1.0900},{"id":2,"type":"SELL","lot":0.1,"open_price":1.1020}]
    partials=0
    for p in prices:
        r=get_recommendation(**base_args(current_price=p, ema=1.1000, atr_short=0.0020, positions=positions))
        partials += sum(1 for a in r['scenario_up'] if a['action']=='PARTIAL_CLOSE')
    assert partials >= 1
