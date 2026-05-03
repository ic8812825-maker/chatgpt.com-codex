from adaptive_lock_ev.calculator import _regime

def test_regime_boundaries():
    assert _regime(1.19)=="MEAN_REVERT"
    assert _regime(1.20)=="NEUTRAL"
    assert _regime(1.50)=="NEUTRAL"
    assert _regime(1.51)=="VOLATILE"
