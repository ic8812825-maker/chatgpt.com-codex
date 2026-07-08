# Minimum Big Level Limit Without Logic Changes

The tested MQL5-like Python model found no stable 1-level or 2-level candidate after applying the MT5 L1 gate, REAL_PRICE_DISTANCE proxy, dynamic point value, budget-only partial Far close and END_OF_TEST penalties.

Minimum observed level count in this Python search: `3`.

Mathematical reason: with StartLot fixed at 1.00 and Small opened against Big, L1 net must both fund partial Far close and reserve. The MT5-calibrated L1 showed that real Far loss per lot is much larger than the old ideal model assumed. Therefore a single level leaves too much Far or too little reserve unless trading logic changes.

Further reduction below 3 levels is not supported by this grid without changing the EA logic. MT5 Strategy Tester remains required to prove or reject the candidate lower bound.