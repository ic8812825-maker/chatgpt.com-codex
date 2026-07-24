# Hybrid Split Big MQL5 pre-open fixtures

`HybridDecisionEngineTests.mq5` is a script-level MetaEditor/MT5 harness for stage 2. It does not trade and does not call `StateMachine`; it builds frozen `HybridCycleSnapshot` fixtures and calls only `EvaluateHybridCandidate()` plus rounding helpers.

Minimum expected checks:

* disabled Hybrid returns `applicable=false` / `HYBRID_DISABLED`;
* invalid symbol and cycle id reject identity;
* current approved `β=0.70` geometry rejects `HYBRID_REJECT_LAW1`;
* `SmallBase` uses UP rounding.

Run in MetaEditor/MT5 after compiling the EA headers. The container used by Codex does not include MetaEditor, so compile status is recorded separately in `Docs/HYBRID_SPLIT_BIG_METAEDITOR_COMPILE.md`.
