# Hybrid Split Big reference model

Run from repository root:

```bash
python3 -m pytest -q MinusLock_BigHarvest_EA_V2/Tests/HybridSplitBig
```

The model is a deterministic mathematical oracle. It does **not** emulate MT5 or replace `OrderCalcProfit()`/broker hedging rules. A production adapter must inject broker-derived money and margin inputs. `test_vectors.json` provides reproducible scenario input fields and expected decision codes.
