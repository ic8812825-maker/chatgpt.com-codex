# 23. Полный нормативный реестр решений Hybrid Split Big

Версия HSB.0R-C.24
STATUS=CLOSED_FOR_HSB1_ARCHITECTURE
OPEN_P0=0
OPEN_P1=0
OPEN_P2=0

Owner-документы являются нормативным source of truth; этот реестр обеспечивает трассировку.

| Decision | До | Owner | Requirement IDs | Принятое решение | Configuration/range | Validation/fail-closed | MQL5 owner | Unit/Integration/Tester | Статус |
|---|---|---|---|---|---|---|---|---|---|
| HSBI-DEC-001 | P1 | 04 | HSBI-MATH-001..006 | C/T floor, S ceil; три закона после rounding | Rc>0,Rt≥0,Rs>0 | invalid grid/law/money reject | Planning/GeometrySolver | rounding/basket/coarse | RESOLVED_FOR_ARCHITECTURE |
| 002 | P1 | 08 | HSBI-MONEY-001..020 | per-source conserved buckets | shares [0,1] | over-allocation/foreign source conflict | Money/AllocationLedger | conservation/replay/costs | RESOLVED_FOR_ARCHITECTURE |
| 003 | P1 | 05 | HSBI-GEO-010..018 | typed fresh control prices, Bid/Ask | MaxAge>0 | stale/wrong-side/off-grid reject | Planning/MarketSnapshot | sides/gates/spread | RESOLVED |
| 004 | P1 | 14 | HSBI-NF-010..018 | exact recursion + conservative bound | depth>0,0<q<1 | unproven future reject | Planning/FutureSmall | recursion/reversals | RESOLVED |
| 005 | P1 | 14 | HSBI-NF-001..009 | deterministic minimum-safe N | broker grid | no safe candidate reject | Planning/NewFarSolver | grid/transition/min lot | RESOLVED |
| 006 | P1 | 15 | HSBI-RISK-020..030 | Emergency separate from recovery | typed triggers | no recovery PASS/no auto-resume | Risk/EmergencyPolicy | triggers/stress | RESOLVED |
| 007 | P1 | 13 | HSBI-SMALL-020..026 | TransitionLoss limited by four caps | caps≥0 | exceeded/unknown cap reject | SmallTransition+Money | caps/reversals | RESOLVED_FOR_ARCHITECTURE |
| 008 | P1 | 12 | HSBI-FC-001..012 | RecoveryPL≥minimum+buffer+tolerance | money values≥0 | insufficient PL/coverage reject | Money/FinalCloseCalculator | accept/reject/costs | RESOLVED_FOR_ARCHITECTURE |
| 009 | P1 | 15 | HSBI-RISK-001..019 | typed margin/drawdown gate order | documented safe ranges | unknown/out-of-range fail-closed | Risk/* | ranges/low margin/gap | RESOLVED_FOR_ARCHITECTURE |
| 010 | P1 | 02/18 | HSBI-ID-001..015 | Account+Symbol+Magic+CycleID+identifier+role; one cycle/symbol | one generation-1 cycle | mismatch reconciliation | Core/Identity | foreign/multi-symbol | RESOLVED |
| 011 | P1 | 16 | HSBI-PERSIST-001..018 | crash-consistent versioned files+SHA256+journal | retention configured | corruption terminal-safe | Persistence/* | crash/restart | RESOLVED |
| 012 | P1 | 21 | HSBI-PROD-010..020 | REAL_LIMITED only explicit approval+all gates+demo | whitelist/loss limits | any missing gate denied | Core/RuntimeMode+Risk | readiness/demo | RESOLVED |
| 013 | P2 | 05 | HSBI-GEO-019..025 | repeated fresh snapshot+hold/retrace+debounce | hold/retrace≥0 | stale/duplicate reject | Geometry+SmallTransition | false touch/debounce | RESOLVED |
| 014 | P2 | 07 | HSBI-TX-020..032 | same ActionID retry; timeout→reconciliation | bounded retry/timeout | completed/unknown history blocks retry | Execution/TransactionEngine | delayed/partial/retry | RESOLVED |

Рассмотренные альтернативы fixed production profiles, depth1, weighted nondeterministic objective, mixed emergency/final close, comments-only identity, globals-only persistence и touch-only Small отвергнуты из-за неоднозначности или небезопасности. Evidence: HSB_0R_CORRECTED_MATH_ACCEPTANCE_RU.md и HSB_0R_SOURCE_OF_TRUTH_AUDIT_RU.md. Commit SHA фиксируется Git-историей соответствующего подэтапа.