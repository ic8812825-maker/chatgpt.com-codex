from adaptive_lock_ev.calculator import select_positions_for_closing

def test_only_profitable_present_first():
    ps=[{'id':1,'type':'BUY','lot':0.1,'open_price':1.1010},{'id':2,'type':'BUY','lot':0.1,'open_price':1.0990}]
    assert select_positions_for_closing(ps,'SELL',1.1000,0.0001,10)[0]['id']==2
