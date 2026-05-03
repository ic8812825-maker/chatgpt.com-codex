def st(b,s): return 'OK' if abs(b-s)<=0.05 else 'BLOCK'
def test_exposure_limit():
    assert st(0.10,0.10)=='OK'
    assert st(0.14,0.10)=='OK'
    assert st(0.15,0.10)=='OK'
    assert st(0.16,0.10)=='BLOCK'
