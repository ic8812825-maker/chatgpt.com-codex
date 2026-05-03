def m(cost,s,q,p): return (cost*s)/(q*p) if q>0 else None
def test_min_move():
    assert round(m(1.2,1.2,0.02,10),1)==7.2
    assert m(2.4,1.2,0.02,10) > m(1.2,1.2,0.02,10)
    assert m(1.2,1.2,0.04,10) < m(1.2,1.2,0.02,10)
    assert m(1.2,1.2,0.02,20) < m(1.2,1.2,0.02,10)
    assert m(1.2,1.2,0,10) is None
