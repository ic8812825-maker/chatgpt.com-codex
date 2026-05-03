def test_cost():
    spread=2*0.02*10; slip=1*0.02*10; comm=0.5*0.02; swap=0
    assert round(spread+slip+comm+swap,2)==0.61
