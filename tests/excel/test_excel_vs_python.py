from adaptive_lock_ev.calculator import get_recommendation
from tests.utils import base_args

def test_excel_python_parity_10_cases():
    cases=[
      base_args(current_price=1.0960,ema=1.1000,atr_short=0.0020,last_10_cycles_pnl=10),
      base_args(current_price=1.1040,ema=1.1000,atr_short=0.0020,last_10_cycles_pnl=10),
      base_args(current_price=1.1010,ema=1.1000,atr_short=0.0020,last_10_cycles_pnl=10),
      base_args(current_price=1.1040,ema=1.1000,atr_short=0.0040,atr_long=0.0020,last_10_cycles_pnl=10),
      base_args(current_price=1.1040,ema=1.1000,atr_short=0.0024,atr_long=0.0020,last_10_cycles_pnl=10),
      base_args(current_price=1.1040,ema=1.1000,atr_short=0.0020,last_10_cycles_pnl=10),
      base_args(current_price=1.1040,ema=1.1000,atr_short=0.0020,broker_dd=0.08,last_10_cycles_pnl=10),
      base_args(current_price=1.1040,ema=1.1000,atr_short=0.0020,broker_dd=0.16,last_10_cycles_pnl=10),
      base_args(current_price=1.1040,ema=1.1000,atr_short=0.0020,positions=[{'id':1,'type':'BUY','lot':0.2,'open_price':1.09},{'id':2,'type':'SELL','lot':0.2,'open_price':1.11}],last_10_cycles_pnl=10),
      base_args(current_price=1.1040,ema=1.1000,atr_short=0.0020,positions=[{'id':1,'type':'BUY','lot':0.16,'open_price':1.09},{'id':2,'type':'SELL','lot':0.10,'open_price':1.11}],last_10_cycles_pnl=10)
    ]
    for a in cases:
      r=get_recommendation(**a)
      z=(a['current_price']-a['ema'])/a['atr_short']; v=a['atr_short']/a['atr_long']
      assert abs(r['z']-z)<1e-6
      assert abs(r['v']-v)<1e-6
