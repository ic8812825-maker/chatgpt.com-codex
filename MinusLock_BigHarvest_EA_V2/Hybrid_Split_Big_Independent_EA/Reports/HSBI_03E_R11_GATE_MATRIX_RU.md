# HSBI-03E-F — R1.1 gate matrix

Версия: **HSBI-03E-R1**. SOURCE_COMMIT_SHA=`b5ca9d377d454dfbec63ece76dd1c759abc3656d`.
Репозиторий `ic8812825-maker/chatgpt.com-codex`, ветка `work`, все относительные source paths внутри `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/`.
Статус: **PROPOSED / AWAITING_OWNER_DECISION**. Ни один текст не APPROVED. Нормативный выбор, architecture/provider и implementation evidence — разные gates.
STATIC_REVIEWED означает чтение исходного текста; MATH_DERIVED — вывод при указанных предпосылках; COUNTEREXAMPLE_CONFIRMED — опровержение утверждения, не runtime PASS; HISTORICAL_TEST_RESULT — старый artifact; все новые vectors TEST_SPECIFIED_NOT_RUN; NATIVE_NOT_RUN. Новых compile/runtime/mutation/native tests не выполнялось.
UNAVAILABLE — обязательное evidence отсутствует; CONFLICT — доказательства противоречат; REJECT — доказанное нарушение домена/предусловия. Все три запрещают новый effect; финансовая delta=0. NO_OP возможен только по валидному полному старому receipt.
Публикация отчёта не утверждает контракт, не закрывает P0 и не разрешает production/R1.1/dispatch/trading.

GateManifestId=HSBI_R11_GATE_MANIFEST_V1;Revision=HSBI-03E-R1.
R11_IMPLEMENTATION_ALLOWED=NO. Статус каждого отсутствующего approval/provider/journal/native gate BLOCKED,не READY из-за публикации отчётов.

## Источники и scope

Reports/HSBI_R11_P0_DEPENDENCY_PLAN_RU.md:20–223 (A/B/C/D/E allowlists,acceptance,stopconditions);Reports/HSBI_03D_R11_READINESS_GATES_RU.md:8–62;HSBI_03D_P0_REMEDIATION_CROSSWALK_RU.md:1–39.
Production:RiskGateResult:6;MoneyState:4–5;EconomicLedgerTypes:6–12;AllocationLedgerTypes:5–10;ReserveCatchUpEvaluator:24–76;ReserveAllocationTypes:15–30;NewFarSolver:60–151;NewFarCandidate:26–40;ControlPrices:11–24;TransactionTypes:9–22;ExecutionJournal:18–43;PersistenceInterface:5–7;Context:19–53. Полные Include paths в [source inventory](HSBI_03E_FINAL_VERDICT_RU.md).
Никакие existing allowlists не расширяются этим report. Ни backend implementation,ни full strategy execution не разрешаются. Если gate требует backend вне минимального R1.1,это внешний blocker,не разрешение добавить его вscope.

## Gates: точные predicates

| Gate | PASS predicate | Текущий факт |
|---|---|---|
| G0-OWNER | owner receipt каждого requiredCanonicalID+variant+exacttextblob+scope | BLOCKED:0 approvals |
| G1-PROFILE | numeric manifest concrete fields noUNBOUND;independent currency/posting/grid/cost receipts;selected codec/mapping | BLOCKED:profiles/evidence not bound |
| G2-NATIVE | source/build-pinned positive/negative boundary+golden+hostiledecode logs;requirednative domain qualified | BLOCKED:NATIVE_NOT_RUN |
| G3-SOURCE | independent broker namespace/history,EA association,fullbody,key binding;completeness for NEW | BLOCKED:provider not qualified |
| G4-SNAPSHOT | allowlisted producer/verifier,trustbinding,clock/age intervals,content receipt,consistentcut,reconciliationepoch | BLOCKED:contract proposed,instance missing |
| G5-REGISTRY | serializable source capacity + exact lifecycle + uniqueness + expectedrev + receipt single transaction;concurrency logs | BLOCKED:global durable authority not demonstrated |
| G6-JOURNAL | full body beforeNOOP;state/receipts atomic;crash recovery/pending/unknown;D05 reset/sticky persist | BLOCKED:productionstub/durability NOT_RUN |
| G7-LEGACY | known mappings preserve K/consumed/appliedset/sticky;unknown quarantine;no changed old bytes/expected | BLOCKED:corpus mapping evidence missing |
| G8-COSTPOLICY | D06 A/B+Initialmembership+CostBasisManifest;H_in/H_gate disjoint/explicitheadroom;no duplicate expenses | BLOCKED:owner policy/basis unset |
| G9-ALLLEVEL | every required level+prefix proof,absoluteFar+minmargin,errorbounds,objectivechoice,requiredtail status | BLOCKED:objective choice/provider/tail proof missing |
| G10-PATH | scoped future diff,all mandatory caller paths,type/enum/domain tests,source mutation causal pairs,no dispatch change | BLOCKED:no future implementation authorised |
| G11-ACCEPT | all applicable gates pass,exactallowlist approved,native regression+crash/provider evidence,status no pending blockers | BLOCKED |
| G12-RISKBOUND | ERR038 explicit admissible market/execution/costmodel and independently reviewed theorem | BLOCKED:ERR038OPEN;activation/deployment blocker |

Evidence gate — независимый проверенный факт,а не название поля. Для PASS недостаточно bool profileVerified или строкаdigest. При reject/conflict/noop balance delta0;new event stale revisionreject;oldreceipt replay no new funds.

## Required matrix

| R1.1 | Необходимые решения | Доказательства/точные gates | Можно реализовать? |
|---|---|---|---|
| C — Numeric guards | D10/D11/D12/D15;closed enums/profile;existingplan C includes10/11/15,03E acceptance adds codec bundle where serialized domain used | G0,G1,G2,G10;all inputs/limits/intermediates finite,overflowbeforeop,unknownenum,min/max/origingrid;fixed vectors N/C/G | NO,BLOCKED:approval/profile/native absent;even reversibleguard needs separate scope permission |
| A — Source identity | D02/D08/D12/D13/D16 + numeric bundle | G0–G4,G7,G10;full29field compare,namespace/sourceauth,changedbody conflict,unknown authority unavailable,exactreplay0delta | NO,BLOCKED |
| B — Allocation | D01/D07/D10/D14 plusD02/D03/D11/D16 existing dependency | G0–G7,G10;immutablegrantvector,phase exactness,G=C+R+F,globalcap acrossIDs,ownedreserve,CAS+durable receipt | NO,BLOCKED:registry/journal/provider/native missing |
| D — Reserve binding | D02/D04/D06/D13/D14 plusD03/CR09/D07/D08/numeric | G0–G10 applicable;publicscalar proof binding,absoluteFar,BigOnly,all-levelmin>0,no projectedfunds,no self-originproof | NO,BLOCKED |
| E — Integration | all dependent16 plusobjective/cost/reset/provider manifests | G0–G11;actualfills/reconciliation,noUNKNOWNretry,fullcontextslots,resetepochs,crash/restart/native;G12 for activation | NO,BLOCKED |

C can be architecturally designed before full integration,но это не фактическое implementation permission. Registry/backend absent означает fundingunavailable;не вводить stub PASS для acceptance. Native tests не запускаются в этом remote-only задании.

## ERR scope и приёмка

Сохранены14 P0: ERR001,002,004,005,007,008,009,010,011,012,013,033,038,048. Closed0.
C local finiteguards не закрывают provider ERR013/globalfunding ERR033;D publicequality не доказывает fullsource;E journaldigest не durability. ERR038 не исправляется одним пакетом/денежным контрактом.
Исторические7PASS/16FAIL C++ не rerun;два contractdependentcases отдельно. Новые acceptance vectors TEST_SPECIFIED_NOT_RUN.
Scope/approval change требует нового owner review,не самовольное расширение новыхReports.
Unresolved:allmissinggates выше. Связи:[numeric](HSBI_03E_NUMERIC_CONTRACT_MANIFEST_V1_RU.md),[snapshot](HSBI_03E_SNAPSHOT_AUTHORITY_CONTRACT_RU.md),[bundles](HSBI_03E_CONTRACT_DEPENDENCY_RECONCILIATION_RU.md),[ERR038](HSBI_03E_ERR038_PROOF_REQUIREMENTS_RU.md),[ballot](HSBI_03E_OWNER_FINAL_DECISION_BALLOT_RU.md).
