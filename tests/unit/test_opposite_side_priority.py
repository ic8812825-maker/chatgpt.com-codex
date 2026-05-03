from adaptive_lock_ev.calculator import select_positions_for_closing

def test_opposite_side_priority():
    ps=[{'id':1,'type':'BUY','lot':0.1,'open_price':1.0900},{'id':2,'type':'SELL','lot':0.1,'open_price':1.1100}]
    assert select_positions_for_closing(ps,'SELL',1.1000,0.0001,10)[0]['type']=='BUY'
    assert select_positions_for_closing(ps,'BUY',1.1000,0.0001,10)[0]['type']=='SELL'
