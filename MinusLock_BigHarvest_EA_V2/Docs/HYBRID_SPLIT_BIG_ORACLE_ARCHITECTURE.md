# Hybrid Split Big — Simulation Oracle architecture

The broker-agnostic oracle separates schema validation, money calculation, event-key buckets, discrete NewFar enumeration, bounded Future Small recursion, candidate margin, computed Worst Case and final decision aggregation. `target_new_far` is diagnostic only; enumeration begins at `VolumeMin` and selects the first fully valid broker-step candidate. Future simulation fingerprints normalized Far and has deterministic depth/node limits. MT5 parity remains a future adapter task because OrderCalcProfit and broker hedging margin are not simulated here.

Final decisions are separate from gate trace: `PASS_NEW_FAR` is a solver result, while a full candidate returns `PASS_ALL_LAWS`; reject/error reason and all intermediate gates remain in trace.
