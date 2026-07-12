loss=120.0; small_profit=80.0; bigtrend_net=10.0; safety=3.0; profit_per_lot=50.0
deficit=max(0.0, loss-small_profit-bigtrend_net+safety)
lot_money=deficit/profit_per_lot
assert abs(deficit-33.0)<1e-9
assert abs(lot_money-0.66)<1e-9
print("PASS dynamic reverse small money lot")
