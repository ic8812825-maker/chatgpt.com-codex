from adaptive_lock_ev.calculator import select_positions_for_closing

def test_position_ranking():
    ps=[{'id':1,'type':'BUY','lot':0.1,'open_price':1.0995},{'id':2,'type':'BUY','lot':0.1,'open_price':1.0985},{'id':3,'type':'BUY','lot':0.1,'open_price':1.0992}]
    assert select_positions_for_closing(ps,'SELL',1.1000,0.0001,10)[0]['id']==2
