from adaptive_lock_ev.calculator import get_recommendation
from tests.utils import base_args

def test_trend_without_reversion_protection():
    rs=[get_recommendation(**base_args(current_price=1.1040+i*0.001,ema=1.1000,atr_short=0.0020,last_10_cycles_pnl=10)) for i in range(5)]
    assert all(r['q']<=0.02 for r in rs)
