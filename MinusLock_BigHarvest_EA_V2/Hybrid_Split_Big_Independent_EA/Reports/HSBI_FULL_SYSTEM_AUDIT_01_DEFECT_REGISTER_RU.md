# Реестр проблем и рисков

BASE_SHA=4185b84f7a6a8847f6a9c5796f07113907be447d

Режим READ-ONLY ANALYSIS + AUDIT/TEST-ONLY. Источники не изменены. **AUDIT_COMPLETENESS=PARTIAL.** Native MQL5/MT5/broker/durable execution NOT_RUN. Proposed R0A–R0H не становятся нормативом из-за тестовых PASS. Все административные разрешения остаются NO.

**29 entries**: P0=10, P1=14, P2=5, P3=0. P0 — latent blockers при использовании соответствующих библиотек, не наблюдавшиеся реальные сделки/списания; текущий EA disabled. Severity не отменяет proofscope. Category различает confirmed local/source defects, normative conflicts, proof obligations, unimplemented components и native blockers.

| ID | Severity | Category | Source | Status |
|---|---|---|---|---|
| FSA-001 | P0 | CONFIRMED_DEFECT | Include/Money/HSBI_EconomicLedgerTypes.mqh:9 | OPEN |
| FSA-002 | P0 | CONFIRMED_DEFECT | Include/Money/HSBI_AllocationLedgerTypes.mqh:8 | OPEN |
| FSA-003 | P0 | CONFIRMED_DEFECT | Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:44 | OPEN |
| FSA-004 | P0 | CONFIRMED_DEFECT | Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:63 | OPEN |
| FSA-005 | P0 | CONFIRMED_DEFECT | Include/Risk/HSBI_RiskGateResult.mqh:6 | OPEN |
| FSA-006 | P0 | CONFIRMED_DEFECT | Include/Execution/HSBI_TransactionTypes.mqh:15 | OPEN |
| FSA-007 | P0 | CONFIRMED_DEFECT | Include/Money/HSBI_AllocationLedgerTypes.mqh:7 | OPEN |
| FSA-008 | P0 | CONFIRMED_DEFECT | Include/Money/HSBI_MoneyState.mqh:5 | OPEN |
| FSA-009 | P0 | CONFIRMED_DEFECT | Include/Core/HSBI_Context.mqh:48 | OPEN |
| FSA-010 | P0 | CONFIRMED_DEFECT | Include/Planning/HSBI_NewFarSolver.mqh:119 | OPEN |
| FSA-011 | P1 | CONFIRMED_DEFECT | Include/Planning/HSBI_GeometrySolver.mqh:32 | OPEN |
| FSA-012 | P1 | UNIMPLEMENTED_ORCHESTRATION | Include/Core/HSBI_StateMachine.mqh:5 | OPEN |
| FSA-013 | P1 | UNIMPLEMENTED_COMPONENT | Include/Persistence/HSBI_PersistenceInterface.mqh:5 | BLOCKED |
| FSA-014 | P1 | UNIMPLEMENTED_COMPONENT | Hybrid_Split_Big_Independent_EA.mq5:35 | OPEN |
| FSA-015 | P1 | NORMATIVE_CONFLICT | Include/Planning/HSBI_FutureSmallProofAggregator.mqh:50 | BLOCKED |
| FSA-016 | P1 | NORMATIVE_CONFLICT | Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:22 | BLOCKED |
| FSA-017 | P1 | CONFIRMED_DEFECT | Include/Planning/HSBI_FutureSmallSolver.mqh:89 | OPEN |
| FSA-018 | P1 | UNPROVEN_PROOF_OBLIGATION | Include/Planning/HSBI_FutureSmallSolver.mqh:12 | BLOCKED |
| FSA-019 | P1 | NORMATIVE_UNCERTAINTY | Include/Money/HSBI_CostModel.mqh:18 | BLOCKED |
| FSA-020 | P1 | UNSPECIFIED_DOMAIN | Docs/03_FULL_SYSTEM_MANUAL_RU.md:9 | BLOCKED |
| FSA-021 | P2 | CONFIRMED_DEFECT | Include/Planning/HSBI_ControlPrices.mqh:11 | OPEN |
| FSA-022 | P2 | CONFIRMED_DEFECT | Include/Core/HSBI_StateMachine.mqh:6 | OPEN |
| FSA-023 | P2 | CONFIRMED_DEFECT | Include/Planning/HSBI_NewFarSolver.mqh:39 | OPEN |
| FSA-024 | P2 | HISTORICAL_CONTRACT_CONFLICT | Tests/Static/accept_hsb_2e_r4_r9_r4a_r8.py:1 | OPEN |
| FSA-025 | P2 | STALE_DOCUMENT_STATUS | Docs/03_FULL_SYSTEM_MANUAL_RU.md:50 | OPEN |
| FSA-026 | P1 | MISSING_ACCEPTANCE_EVIDENCE | Tests/Reference/hsbi_02b_r0h_native_harness.mq5:1 | BLOCKED |
| FSA-027 | P1 | CONFIRMED_DEFECT | Include/Persistence/HSBI_ExecutionJournal.mqh:27 | OPEN |
| FSA-028 | P1 | UNIMPLEMENTED_TERMINAL_PROOF | Include/Planning/HSBI_FutureSmallSolver.mqh:144 | OPEN |
| FSA-029 | P1 | CONFIRMED_DEFECT | Include/Money/HSBI_BasketMoneyEvaluator.mqh:15 | OPEN |

## FSA-001 P0

**SourceFile**: Include/Money/HSBI_EconomicLedgerTypes.mqh

**SourceLine**: 9

**Requirement**: Docs/08:6,9,15; D08; L01

**Category**: CONFIRMED_DEFECT

**Cause**: Equality ignores components/identity metadata and uses epsilon Net; legacy key partitions same deal by Magic/Cycle without account namespace

**Counterexample**: Profit50,C0 vsProfit60,C-10,Net50 samekey ->duplicate1; Magic change sameTicket changeskey

**Expected**: samekey altered payload CONFLICT; source namespace independently bound

**Actual**: identical1; changedMagic can be classifiednew0

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["L01_COMPONENT_CONFLICT", "KEY_MAGIC_PARTITION"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: Versioned immutable equality/source key/status API; quarantine unknown legacy. No automatic cross-account migration.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: LATENT_LIBRARY_DEFECT; EA dispatch disabled

**Status**: OPEN

## FSA-002 P0

**SourceFile**: Include/Money/HSBI_AllocationLedgerTypes.mqh

**SourceLine**: 8

**Requirement**: Docs/08:12,15; L02

**Category**: CONFIRMED_DEFECT

**Cause**: Duplicate checks total only, not bucket vector/policy/immutable payload

**Counterexample**: FinalReserve50/PF0 ->Reserve0/PF50, same deal/event,total50

**Expected**: CONFLICT

**Actual**: duplicate1

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["L02_VECTOR_CONFLICT"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: Compare complete immutable allocation vector/version/source; separate mutable consumption state.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: LATENT_LIBRARY_DEFECT; EA dispatch disabled

**Status**: OPEN

## FSA-003 P0

**SourceFile**: Include/Money/HSBI_ReserveCatchUpEvaluator.mqh

**SourceLine**: 44

**Requirement**: Docs/08:15; Docs/32:7; M01

**Category**: CONFIRMED_DEFECT

**Cause**: Consumption key only shape/plan/revision checked, not matching authoritative allocation keys

**Counterexample**: valid D1/A1 allocation, key FOREIGN/FOREIGN, no prior

**Expected**: REJECT/CONFLICT zero permission

**Actual**: valid Catch-Up

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["M01_FOREIGN_SOURCE_REJECT"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: Bind exact source/allocation/event/cycle/owner and independently complete journal.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: LATENT_LIBRARY_DEFECT; EA dispatch disabled

**Status**: OPEN

## FSA-004 P0

**SourceFile**: Include/Money/HSBI_ReserveCatchUpEvaluator.mqh

**SourceLine**: 63

**Requirement**: Docs/08:24; Docs/32:3-7; reserve consumption

**Category**: CONFIRMED_DEFECT

**Cause**: alreadyConsumed rejected only alreadyAllocated branch; eligible branch recreates gain from same exhausted source

**Counterexample**: allocatable50, reserve0,alreadyConsumed50,alreadyAllocatedfalse,eligible50,share.9

**Expected**: No new permission from spent source

**Actual**: gain45,catchUp24 =>valid

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["RESERVE_SPENT_SOURCE_REJECT"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: Authoritative remaining/grants and consumed checks before either branch; cannot trust allocation-state flag as new money proof.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: LATENT_LIBRARY_DEFECT; EA dispatch disabled

**Status**: OPEN

## FSA-005 P0

**SourceFile**: Include/Risk/HSBI_RiskGateResult.mqh

**SourceLine**: 6

**Requirement**: Docs/15:6,9; Docs/24:11

**Category**: CONFIRMED_DEFECT

**Cause**: NaN comparisons are false, most fields/limits have no finite/domain checks

**Counterexample**: valid limits and snapshot; projectedMargin=NaN

**Expected**: reject unknown/nonfinite

**Actual**: passed=true

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["RISK_NAN_REJECT", "NF_GATE_UNKNOWN_LIMIT_REJECT"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: Validate all quantities and both sides of every limit, before comparisons; include NewFarGateTypes:13-14.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: LATENT_LIBRARY_DEFECT; EA dispatch disabled

**Status**: OPEN

## FSA-006 P0

**SourceFile**: Include/Execution/HSBI_TransactionTypes.mqh

**SourceLine**: 15

**Requirement**: Docs/07:15,21; actual fill validation

**Category**: CONFIRMED_DEFECT

**Cause**: NaN accumulated volume or outcome price/volume bypass abs(diff)>tolerance

**Counterexample**: completed flags+matching IDs, actualVolume=NaN

**Expected**: no completion

**Actual**: barrier/completionAllowed=true

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["TX_NAN_VOLUME_REJECT", "OUTCOME_NAN_VOLUME_REJECT", "OUTCOME_NAN_PRICE_REJECT"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: Finite/nonnegative/domain validation for intent/outcome/tolerances; independent history-backed producer; review ExternalOutcome:25-30.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: LATENT_LIBRARY_DEFECT; EA dispatch disabled

**Status**: OPEN

## FSA-007 P0

**SourceFile**: Include/Money/HSBI_AllocationLedgerTypes.mqh

**SourceLine**: 7

**Requirement**: Docs/08:12,24; D01

**Category**: CONFIRMED_DEFECT

**Cause**: No nonnegative/finite bucket validation; committed full equality not distinguished from partial inequality

**Counterexample**: Rsv=-50,PF100,source50; alternatively committed only10/50

**Expected**: reject negative; committed full sum or explicit PREPARED

**Actual**: accepts both

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["ALLOC_NEGATIVE_BUCKET_REJECT", "ALLOC_COMMITTED_UNALLOCATED"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: Typed PREPARED/COMMITTED and exact posted-money domain; reconcile D01 vs Doc32 inequality before implementation.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: LATENT_LIBRARY_DEFECT; EA dispatch disabled

**Status**: OPEN

## FSA-008 P0

**SourceFile**: Include/Money/HSBI_MoneyState.mqh

**SourceLine**: 5

**Requirement**: Docs/08:12,24; fail-closed money state

**Category**: CONFIRMED_DEFECT

**Cause**: Only >=0 bucket tests, ignores valid/revision/finiteness

**Counterexample**: valid=false,rev0 nonnegative; or reserve=+Infinity

**Expected**: invalid/unavailable

**Actual**: true

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["MONEY_INVALID_FLAG_REV", "MONEY_INFINITY"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: Explicit validated state schema/revision/known units/finite bounds; mandatory caller proof before consumption.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: LATENT_LIBRARY_DEFECT; EA dispatch disabled

**Status**: OPEN

## FSA-009 P0

**SourceFile**: Include/Core/HSBI_Context.mqh

**SourceLine**: 48

**Requirement**: Docs/00:12; Docs/02:25; exactly-oneFar

**Category**: CONFIRMED_DEFECT

**Cause**: Far count and slot role validation cover only far/core/trend/small, omit initial and new candidate slots

**Counterexample**: FAR_ACTIVE farID1 + initialBuy roleFAR ID2 same scope

**Expected**: invalid context/dual-tail invariant

**Actual**: ValidateContext true; NoDualTail passes

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["CONTEXT_TWO_FAR_OTHER_SLOT_REJECT", "INVARIANT_DUAL_FAR_OTHER_SLOT_REJECT"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: Validate every role slot and distinct managed identifier from complete observed positions, count all active Far roles.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: LATENT_LIBRARY_DEFECT; EA dispatch disabled

**Status**: OPEN

## FSA-010 P0

**SourceFile**: Include/Planning/HSBI_NewFarSolver.mqh

**SourceLine**: 119

**Requirement**: Docs/31:3-7; D08; M02

**Category**: CONFIRMED_DEFECT

**Cause**: Proof identity overwritten from input; expected then copied from same proof; no independent deal-reconciliation record

**Counterexample**: mutate proof+expected account together; helper accepts; caller expected=actual at124

**Expected**: independent authority must establish expected identity before verify

**Actual**: local equality cannot detect coherent identity substitution

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["M02_COPIED_FOREIGN_EXPECTED"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: Independent ConfirmedDeal->ReconciledRecord->Allocation->expected identity. Do not demand authentication from helper whose caller supplies expected.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: STATIC_CALLER_CONTRACT_GAP + EXTRACTED_HELPER demonstration; not full NewFar exploit/provider authentication proof

**Status**: OPEN

## FSA-011 P1

**SourceFile**: Include/Planning/HSBI_GeometrySolver.mqh

**SourceLine**: 32

**Requirement**: Docs/04:9; Docs/25:5; zeroCore

**Category**: CONFIRMED_DEFECT

**Cause**: Core0 accepted and positive Core/Trend omit volumeMin

**Counterexample**: F.1,Rc.01,Rt3,Rs.1 ->Core0 Trend.3 S.01 slope.19; min.05 Core.01 also passes

**Expected**: requiredCore>=min, all active legs within grid/bounds

**Actual**: valid

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["ZERO_CORE_MINLOT", "BELOW_MIN_CORE"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: Active-leg policy and broker min/max/step/origin checks after rounding, preserve Trend optional semantics.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: LATENT_LIBRARY_DEFECT; EA dispatch disabled

**Status**: OPEN

## FSA-012 P1

**SourceFile**: Include/Core/HSBI_StateMachine.mqh

**SourceLine**: 5

**Requirement**: Docs/06 full transition lifecycle

**Category**: UNIMPLEMENTED_ORCHESTRATION

**Cause**: Normal topology stops at openingCore; generic reconcile route lacks explicit resume authority

**Counterexample**: Core->Trend false; TerminalSafe->Reconciling->FarActive allowed without admin input

**Expected**: complete guarded lifecycle/no auto-resume

**Actual**: missing transition; pure topology permits two-step resume

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["FSM_CORE_TO_TREND", "FSM_AUTO_RESUME_UNGUARDED"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: Specify full orchestrator/state+role guards, admin resume policy and mandatory transaction/persist barrier.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: PARTIAL_PURE_TOPOLOGY; not an executing trading FSM

**Status**: OPEN

## FSA-013 P1

**SourceFile**: Include/Persistence/HSBI_PersistenceInterface.mqh

**SourceLine**: 5

**Requirement**: Docs/16:6,12,15

**Category**: UNIMPLEMENTED_COMPONENT

**Cause**: Production SHA256/storage stub; no durable lock/commit/CAS/history load

**Counterexample**: PersistSnapshotStub always success=false; restart flags only DTO

**Expected**: crash-consistent committed history/recovery

**Actual**: no production backend

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["PROPERTY-SNAPSHOT_BINDING", "PROPERTY-REPLAY_IDENTITY"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: Separate approved persistence phase with crash injection/concurrency/provider reconciliation.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: STATICALLY_INSPECTED; crash/durable tests NOT_RUN

**Status**: BLOCKED

## FSA-014 P1

**SourceFile**: Hybrid_Split_Big_Independent_EA.mq5

**SourceLine**: 35

**Requirement**: Docs/03:6,39; Docs/18:29

**Category**: UNIMPLEMENTED_COMPONENT

**Cause**: OnTick only SubmitActionStub; no OnTradeTransaction/planning/scenario ingress

**Counterexample**: no market provider, action engine, actual ledger commit or cycle orchestration

**Expected**: full cycle only after separate production authorizations

**Actual**: nontrading skeleton, as documented boundary

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["STATIC-CALL-GRAPH"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: Money foundations/native tests first; separate provider/transaction/FSM/scenarios implementation.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: ACTUAL_ENTRY_SOURCE_INSPECTION; no trading runtime tests

**Status**: OPEN

## FSA-015 P1

**SourceFile**: Include/Planning/HSBI_FutureSmallProofAggregator.mqh

**SourceLine**: 50

**Requirement**: Docs/30:5 vs proposed CR09/D04

**Category**: NORMATIVE_CONFLICT

**Cause**: Max transition-loss level need not minimize Catch-Up margin

**Counterexample**: level1 Trans10 Margin+9;level2 Trans5 Margin-11

**Expected**: all-required-level min>0 for proposedA; selection scope explicit

**Actual**: WORST_CASE selectslevel1

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["AGGREGATE_POSITIVE_VALID", "CR09-EXTREMA"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: Administrator select all-level Catch-Up criterion and FarLoss metric; do not silently replace existing policy.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: EXTRACTED_SELECTION + INDEPENDENT_COUNTEREXAMPLE; proposed policy not automatically normative

**Status**: BLOCKED

## FSA-016 P1

**SourceFile**: Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md

**SourceLine**: 22

**Requirement**: Docs/03:21; Docs/14:22 vs Docs/29:3

**Category**: NORMATIVE_CONFLICT

**Cause**: minimum-safeN vs global risk/margin-first selection have different order

**Counterexample**: N.2 risk10 vsN.3 risk5

**Expected**: explicit single objective contract

**Actual**: CompareCandidateTieBreak risk-first :35-39

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["OBJECTIVE-NON_EQUIVALENCE"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: Resolve normative precedence/monotonic assumptions; independent objectives tests before solver changes.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: STATICALLY_INSPECTED + MATHEMATICAL_COUNTEREXAMPLE

**Status**: BLOCKED

## FSA-017 P1

**SourceFile**: Include/Planning/HSBI_FutureSmallSolver.mqh

**SourceLine**: 89

**Requirement**: Docs/04:21 NextBigGross<OldBigGross

**Category**: CONFIRMED_DEFECT

**Cause**: compares netBigVolume with priorBigGross

**Counterexample**: C.6 T.6 S1 F.1 ->BigGross1.2,net.2,priorBigGross1; other level gates synthetic valid

**Expected**: reject increased BigGross

**Actual**: exact level valid in permitted UNIT_TEST injected path

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["FS_BIG_GROSS_GROWTH_REJECT"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: Compare C+T gross with correct prior gross; keep net slope and total exposure separate.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: EXTRACTED_UNIT_TEST_LEVEL_WITH_EXPLICIT_INJECTED_BASKET; full production solver NOT executed

**Status**: OPEN

## FSA-018 P1

**SourceFile**: Include/Planning/HSBI_FutureSmallSolver.mqh

**SourceLine**: 12

**Requirement**: Docs/04:33,36; Docs/27:5

**Category**: UNPROVEN_PROOF_OBLIGATION

**Cause**: Finite prefix checks and boolean flags do not establish a uniform infinite-tail q law

**Counterexample**: F0=1,F1=.8,F2=.64 passesq.8; possibleF3=.64 violates .512

**Expected**: global bound must be an assumption/certificate with domain, or remainunproven

**Actual**: endpoint validator returns true

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["BOUND_FINITE_PREFIX_NOT_GLOBAL_PROOF", "PREFIX-NOT-TAIL"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: Define certified global recurrence/domain/rounding/terminal route; do not claim finite wall-clock exit from conditional contraction.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: LOGICAL_COUNTEREXAMPLE_TO_PROOF_COMPLETENESS; not incorrect algebra of q^n

**Status**: BLOCKED

## FSA-019 P1

**SourceFile**: Include/Money/HSBI_CostModel.mqh

**SourceLine**: 18

**Requirement**: D06; Docs/04:18; Docs/24:7

**Category**: NORMATIVE_UNCERTAINTY

**Cause**: No cost basis/window/coverage identity to establish spread/buffer nonoverlap

**Counterexample**: buy Ask101 closeBid110 ->brokerPL9; subtract same realizedspread1 again =>8

**Expected**: count same cost once or explicitly independent stressbuffer

**Actual**: formula permits repeatdeduction if supplied cost overlaps

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["COST-OVERLAP"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: Approve typed cost-coverage and buffers independently; values unknown notzero.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: CONDITIONAL_ACCOUNTING_COUNTEREXAMPLE; not all spreadCost necessarily duplicate

**Status**: BLOCKED

## FSA-020 P1

**SourceFile**: Docs/03_FULL_SYSTEM_MANUAL_RU.md

**SourceLine**: 9

**Requirement**: Supported account/broker model admission

**Category**: UNSPECIFIED_DOMAIN

**Cause**: Multiple simultaneous same-symbol opposite positions require hedging semantics or a virtual-position design

**Counterexample**: netting BUY1+SELL1 ->net0, cannot keep InitialBuy+InitialSell tickets

**Expected**: explicit supported account model/gate

**Actual**: no ACCOUNT_MARGIN_MODE admission in production

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["ACCOUNT-MODE-NETTING"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: Approve hedging-only supported scope or separately design/test netting virtual ledger; broker evidence required.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: ACCOUNT_MODE_LOGIC + STATIC_ABSENCE; actual broker account NOT_RUN

**Status**: BLOCKED

## FSA-021 P2

**SourceFile**: Include/Planning/HSBI_ControlPrices.mqh

**SourceLine**: 11

**Requirement**: Docs/05:6,13; freshness clock contract

**Category**: CONFIRMED_DEFECT

**Cause**: age only upper bounded; future time accepted

**Counterexample**: now100,timestamp1000,maxAge10

**Expected**: unknown/future outside approved skew must not provefresh

**Actual**: true

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["FUTURE_TIMESTAMP_REJECT"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: Define clock domain/units/skew; require bounded age according to explicit approved policy.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: EXTRACTED_ZERO_SKEW_FIXTURE; universal production skew not chosen

**Status**: OPEN

## FSA-022 P2

**SourceFile**: Include/Core/HSBI_StateMachine.mqh

**SourceLine**: 6

**Requirement**: Docs/01 StateRevision commit monotonicity

**Category**: CONFIRMED_DEFECT

**Cause**: Allowed revision +1 not guarded atulongMAX

**Counterexample**: before2^64-1, allowedtransition

**Expected**: reject unsupported nextrevision

**Actual**: C++ adapter proposedrevision wraps,allowed=true

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["FSM_REVISION_OVERFLOW_REJECT"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: Checked revision domain/CAS; native boundary test.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: EXTRACTED_CPP_UNSIGNED_DOMAIN; MQL native numeric behavior NOT_RUN

**Status**: OPEN

## FSA-023 P2

**SourceFile**: Include/Planning/HSBI_NewFarSolver.mqh

**SourceLine**: 39

**Requirement**: Array128/domain/proof digest

**Category**: CONFIRMED_DEFECT

**Cause**: maximumDepth used for array indexing in digest before SolveFutureSmall validates<=128

**Counterexample**: valid outer inputs, maximumDepth129

**Expected**: reject before digest loop

**Actual**: static potential OOB; not executed dangerousprobe

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["STATIC-BOUNDS-DIGEST"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: Validate domain at every public digest/entry before array access and prove mandatory caller.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: STATICALLY_INSPECTED_PATH; OOB/native exploit NOT_RUN

**Status**: OPEN

## FSA-024 P2

**SourceFile**: Tests/Static/accept_hsb_2e_r4_r9_r4a_r8.py

**SourceLine**: 1

**Requirement**: Historical frozen scope vs explicitly permitted R0H test harness

**Category**: HISTORICAL_CONTRACT_CONFLICT

**Cause**: Scope checker rejects any changed .mq5/.mqh even under test path

**Counterexample**: three R0H native test files cause only SCOPE finding

**Expected**: classify stale scope separately; retain rawFAIL

**Actual**: R8/R10 exit1; no missingcase/functional finding

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["REGRESSION-R8", "REGRESSION-R10"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: New acceptance wrapper/explicit exception contract, never edit frozen expectations/evidence.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: FRESH_HISTORICAL_CLI_FAIL + EXACT_FINDING_JSON

**Status**: OPEN

## FSA-025 P2

**SourceFile**: Docs/03_FULL_SYSTEM_MANUAL_RU.md

**SourceLine**: 50

**Requirement**: Current evidence cannot inherit oldOPEN_P0=0

**Category**: STALE_DOCUMENT_STATUS

**Cause**: Historical closure claim followed by implementation-boundary footer; later16pending decisions and open source defects

**Counterexample**: OPEN_P0=0 vs L01/L02/M01 stillpresent

**Expected**: current independent status separate from historicalacceptance

**Actual**: historicaldocs remainunchanged

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["STATIC-DOCUMENTATION-MAP"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: New current authoritative status/index, explicit historical scope/approval chain; no retroactive changes.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: DOCUMENTARY_CONFLICT

**Status**: OPEN

## FSA-026 P1

**SourceFile**: Tests/Reference/hsbi_02b_r0h_native_harness.mq5

**SourceLine**: 1

**Requirement**: Native acceptance R0G/R0H; MQL production readiness

**Category**: MISSING_ACCEPTANCE_EVIDENCE

**Cause**: No MetaEditor/MT5 native logs; Python/C++ not MQL proof

**Counterexample**: native harness prepared, not compiled/executed

**Expected**: native toolchain/target assertions/goldens before acceptance

**Actual**: NOT_RUN

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["NATIVE-DISCOVERY"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: Obtain isolated MetaEditor/MT5 environment and execute signed/native evidence.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: ENVIRONMENT_BLOCKER; not a claimed native compile defect

**Status**: BLOCKED

## FSA-027 P1

**SourceFile**: Include/Persistence/HSBI_ExecutionJournal.mqh

**SourceLine**: 27

**Requirement**: Docs/16:append-only immutablejournal; Docs/17:14

**Category**: CONFIRMED_DEFECT

**Cause**: Duplicate lookup occurs before validating candidate body/currentEntryDigest binding

**Counterexample**: sameIDs+oldcurrentDigest, changedpayloadDigest ALTERED

**Expected**: changed payload REJECT/CONFLICT, notNO_OP

**Actual**: JOURNAL_NO_OP

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["JOURNAL_ALTERED_BODY_NOT_NOOP"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: Validate immutable replay payload binding before trusting presented digest; preserve exact verified receipt replay across revisions.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: EXTRACTED_JOURNAL_CLASSIFIER; no durable append/spend executed

**Status**: OPEN

## FSA-028 P1

**SourceFile**: Include/Planning/HSBI_FutureSmallSolver.mqh

**SourceLine**: 144

**Requirement**: Docs/04:36 operationalterminalclose; Docs/27:5

**Category**: UNIMPLEMENTED_TERMINAL_PROOF

**Cause**: Terminal flag means Far<=Vmin, not actual closure/affordability; terminalRouteAllowed input is unused

**Counterexample**: two levels .03->.02->.01 with terminalRouteAllowedfalse can be valid/finite while remainingFar>0

**Expected**: missing terminal route proof must remain UNPROVEN

**Actual**: valid FutureSmall, positive terminalFar

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["FS_MISSING_TERMINAL_ROUTE_REJECT"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: Separate finite shrink sequence from operational FinalClose/terminal loss authority; require terminal route proof and economics.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: EXTRACTED_UNIT_TEST_INJECTED_FUTURE_SMALL; not full production solver/native execution

**Status**: OPEN

## FSA-029 P1

**SourceFile**: Include/Money/HSBI_BasketMoneyEvaluator.mqh

**SourceLine**: 15

**Requirement**: Docs/04:9 Rt>=0; optional Trend

**Category**: CONFIRMED_DEFECT

**Cause**: Geometry permits Trend0; basket always calls positive-volume money/margin wrapper for allfour legs

**Counterexample**: F.1,Rc3,Rt0,Rs.1 validgeometry; trendVolume0 basketinvalid

**Expected**: Skip explicitly inactive optional Trend with zero PnL/cost/margin, not broker request

**Actual**: money/evaluatedcandidate rejected

**PotentialConsequence**: Incorrect permission/state if these currently dormant library paths are later integrated; no real orders/funding observed

**TestIDs**: ["TREND_ZERO_GEOMETRY_ACCEPTED", "TREND_ZERO_BASKET_ACCEPTED"]

**Reproduction**: python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py; see EXTRACTED.json / reference scenario IDs

**ProposedFix**: Approve active-leg schema and typed zero-leg evaluation; do not allow zero mandatory Core/Small.

**Dependencies**: ["separate explicit admin task", "native MQL5 compile/runtime evidence", "source/provenance contracts"]

**ProofBoundary**: EXTRACTED_GEOMETRY/BASKET_CROSS_LAYER_INCONSISTENCY; synthetic OrderCalc stubs

**Status**: OPEN

## Отдельные непроверенные риски

| RiskID | Topic | Source | Unknown/impact |
|---|---|---|---|
| UR01 | Global economic funding | Docs/08:12,24; R0F FUNDING | Нет глобального unique source/allocation/account registry с фактическими opening/closing/foreign debits. Один локальный валидатор не доказывает conservation across allocations. |
| UR02 | Broker execution, posted precision, actual costs/margin | Docs/24:5-11; Docs/15:9 | OrderCalc wrappers не исполнялись в MT5; currency conversion, tiers, netting/hedging, margin calls, swap/fee timing и posted policy неизвестны. |
| UR03 | Loss bound/profitability | Docs/04:12,33-36; SCENARIO-BIG_PROFIT_SMALL_LOSS | Нет market/stochastic assumptions/backtest. Положительный Harvest не обеспечивает положительный full-cycle PnL; gaps/remaining short liability не ограничены моделью. |
| UR04 | Cycle termination/liveness | Docs/05:25; Docs/13:12; FutureSmallSolver:144 | Сужение Far по успешным transitions не гарантирует приход нужных цен, доступность маржи, исполнения или закрытие terminalFar. Flat/adverse path может не завершить recovery. |
| UR05 | Durable/concurrent exactly-once | Docs/16; PersistenceInterface:5-7 | Нет реального backend/CAS/locks/crash/restart provider. Boolean historyUnchanged не доказывает долговечность. |
| UR06 | Native MQL5 compatibility | Docs/20:HSBI-TEST-001..003; R0H harness | Нет MetaEditor/MT5, compile/runtime/byte/golden/out-of-memory evidence. C++ адаптер не замена. |
| UR07 | Risk/margin/source snapshot identity across candidate levels | FutureSmallSolver:83-90,127; NewFarSolver:77 | RuntimeConfirmed/evaluatedRisk/snapshotId принимаются от вызывающего слоя. Independent provider/candidate-specific reconciliation отсутствуют; self-consistent flags не proof. |
| UR08 | Coverage beyond reviewed owner contracts | INVENTORY.json Docs/TestFiles; COVERAGE.json | Все133 документа проиндексированы, но не каждая историческая таблица/qualification oracle повторно семантически проверена;279 test scripts не все выполнены;137 expression sites не все выделены в атомарные формулы. |
| UR09 | Actual reconciliation and authority authenticity | Docs/07; Docs/17; MoneyProofIdentity:10 | Нет actual position/order/deal reader и producer origin association journal; nonzero IDs/flags не подтверждают наличие/принадлежность сделки. |
