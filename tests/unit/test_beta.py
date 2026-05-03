def b(conf,dd=0): return 0.8 if dd>0.1 else 0.7-0.4*conf
def test_beta():
    assert round(b(0),2)==0.7
    assert round(b(0.5),2)==0.5
    assert round(b(1),2)==0.3
    assert b(0.2,0.11)==0.8
