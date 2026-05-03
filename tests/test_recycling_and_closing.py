from adaptive_lock_ev.calculator import get_recommendation, select_positions_for_closing
from tests.utils import base_args

def test_select_positions_for_closing_priority():
    positions=[{"id":1,"type":"BUY","lot":0.1,"open_price":1.0900},{"id":2,"type":"BUY","lot":0.1,"open_price":1.0990}]
    ranked = select_positions_for_closing(positions,'SELL',1.1000,0.0001,10)
    assert ranked[0]['id'] == 1

def test_pnl_recycling_partial_close_present():
    positions=[{"id":1,"type":"BUY","lot":0.1,"open_price":1.0900},{"id":2,"type":"SELL","lot":0.1,"open_price":1.1020}]
    r = get_recommendation(**base_args(current_price=1.1040, ema=1.1000, atr_short=0.0020, positions=positions))
    assert any(x['action'] == 'PARTIAL_CLOSE' for x in r['scenario_up'])
