# Hybrid Split Big — Decision Trace Specification

Каждый evaluator пишет одну deterministic record на gate и одну aggregate decision record. Поля не переименовываются между pre-open, transition, Future Small и restart.

## Gate record

```text
HYBRID_GATE |
Timestamp= | Symbol= | Magic= | CycleID= | Revision= | Fingerprint= |
PlanID= | Stage= | Gate= | Sequence= | Evaluated= | Passed= |
Inputs={...} | Outputs={...} | ReasonCode= | Reason= |
DurationMicros= | ModelVersion= | Profile=BASE|WORST
```

Обязательные поля: gate name/code, normalized inputs с units, computed outputs, reason/reject/error, decision, execution duration. `DurationMicros` диагностический и не влияет на решение.

## Harvest-level record

```text
HYBRID_CATCHUP_LEVEL |
CycleID= | PlanID= | Level= | Bid= | Ask= |
FarNet= | CoreNet= | TrendNet= | SmallNet= | HarvestNet= |
PartialAfter= | ReserveAfter= | CarryAfter= |
FarCloseCost= | CoverageDeficit= | RecoveryPL= |
MarginBase= | MarginWorst= | WorstNet= | Decision= | Reason=
```

## Aggregate decision

```text
HYBRID_DECISION |
Symbol= | Magic= | CycleID= | Revision= | PlanID= |
EvaluatedGateMask= | PassedGateMask= | FailedGate= |
FinalCode= | RejectCode= | ErrorCode= | TerminalCode= | Reason=
```

Money печатается с account-currency precision, lots с broker volume digits, prices с symbol digits. Secrets и unordered map serialization запрещены. Trace должен воспроизводиться из immutable snapshot/config/model version.

## Sequential `HYBRID_CATCHUP_LEVEL` fields

```text
StateBeforeFingerprint= | StateAfterFingerprint= |
FarLotBefore= | FarLotClosed= | FarLotAfter= | FarOpenPrice= |
CoreLot= | CoreOpenPrice= | CoreCloseNet= |
TrendLot= | TrendOpenPrice= | TrendCloseNet= |
SmallLot= | SmallOpenPrice= | SmallCloseNet= |
HarvestNet= |
PartialAdd= | PartialBudgetBefore= | PartialBudgetConsumed= | PartialBudgetAfter= | PartialFarNet= |
ReserveBefore= | ReserveAdd= | ReserveAfter= |
CarryBefore= | CarryAdd= | CarryAfter= |
RealizedPLBefore= | RealizedPLAfterHarvest= | RealizedPLAfterPartial= |
NextCoreLot= | NextTrendLot= | NextSmallLot= | NextOpenBid= | NextOpenAsk= |
RecoveryBefore= | RecoveryAfter= |
MarginBefore= | MarginReleased= | MarginAfter= | MarginPeak= |
CoverageBefore= | CoverageAfter= | Decision= | Reason=
```

Sequential records additionally require `Profile`, `TriggerBid/Ask`, `EligibleHarvest`, `RemainingFarNet/Cost`, `RecoveryAfterPartial/Reopen`, `OverlapUpper`, and every allocation/budget/temporal pass flag. Field omission is a trace-contract failure.

Temporal authority: `HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`.
