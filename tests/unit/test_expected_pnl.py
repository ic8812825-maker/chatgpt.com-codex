def test_expected_pnl():
    q=0.02; mm=7.2; pip=10; cost=1.2
    assert q*mm*pip-cost>0
