from adaptive_lock_ev.calculator import _round_lot

def test_lot_rounding():
    assert _round_lot(0.017,0.01,0)==0.01
    assert _round_lot(0.029,0.01,0)==0.02
    assert _round_lot(0.004,0.01,0)==0
