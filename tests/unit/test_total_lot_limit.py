def st(v): return 'OK' if v<=0.30 else 'BLOCK'
def test_total_lot_limit():
    assert st(0.29)=='OK' and st(0.30)=='OK' and st(0.31)=='BLOCK'
