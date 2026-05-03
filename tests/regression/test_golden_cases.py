from adaptive_lock_ev.calculator import get_recommendation
from tests.utils import base_args

def test_golden_cases_min20():
    cases=[base_args(current_price=1.1000+i*0.0005,ema=1.1000,atr_short=0.0020,last_10_cycles_pnl=10) for i in range(-10,10)]
    assert len(cases)==20
    for c in cases:
        r=get_recommendation(**c)
        assert r['state'] in ['FLOW','STRESS','ESCAPE']
        assert r['regime'] in ['MEAN_REVERT','NEUTRAL','VOLATILE']
