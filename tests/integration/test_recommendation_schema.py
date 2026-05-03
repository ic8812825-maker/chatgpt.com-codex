from adaptive_lock_ev.calculator import get_recommendation
from tests.utils import base_args

def test_recommendation_schema():
    r=get_recommendation(**base_args(current_price=1.1040,ema=1.1000,atr_short=0.0020,last_10_cycles_pnl=10))
    for rec in [r['scenario_up'][0], r['scenario_down'][0]]:
        for k in ['action','comment']:
            assert k in rec
