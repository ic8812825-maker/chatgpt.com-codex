from adaptive_lock_ev.calculator import get_recommendation
from tests.utils import base_args

def test_block_when_limits_exceeded():
    positions = [{"id":1,"type":"BUY","lot":0.3},{"id":2,"type":"SELL","lot":0.0}]
    r = get_recommendation(**base_args(positions=positions,current_price=1.1040, ema=1.1000, atr_short=0.0020))
    assert r['scenario_up'][0]['action'] == 'NO_ACTION'
