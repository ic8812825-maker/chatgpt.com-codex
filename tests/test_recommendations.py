from adaptive_lock_ev.calculator import get_recommendation
from tests.utils import base_args

def test_signal_recommendations():
    assert get_recommendation(**base_args(current_price=1.1040, ema=1.1000, atr_short=0.0020))['scenario_up'][0]['action'] == 'OPEN'
    assert get_recommendation(**base_args(current_price=1.0960, ema=1.1000, atr_short=0.0020))['scenario_down'][0]['action'] == 'OPEN'
    assert get_recommendation(**base_args(current_price=1.1010, ema=1.1000, atr_short=0.0020))['scenario_up'][0]['action'] == 'NO_ACTION'
