# BigScenario Model Limitations

`OLD_OFFLINE_MODEL_INVALID_FOR_FINAL_SELECTION`: the previous ideal Big-only model used `POINT_VALUE_PER_LOT=1.0`, fixed Far loss, and exact target prices. It produced a false one-level `STATE_CLOSED_PROFIT` for a profile that MT5 carried to `BIG_L11` and `END_OF_TEST`.

The new calibrated model is still not MT5 confirmation. It includes dynamic point-value calibration, Far-loss calibration, spread/slippage proxy, `END_OF_TEST` failure penalties, `OnTester=-1` penalties, `RemainingFarLot` penalties, `MaxHarvestLevels`, and `BIG_L9+` penalties.

Final acceptance still requires MT5 Strategy Tester: candidates must be treated as `MT5_CANDIDATE_NOT_CONFIRMED`.