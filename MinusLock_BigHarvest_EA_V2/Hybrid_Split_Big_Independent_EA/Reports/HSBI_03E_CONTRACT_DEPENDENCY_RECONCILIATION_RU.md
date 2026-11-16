# HSBI-03E-E — Согласование 16 контрактов и approval bundles

Версия: **HSBI-03E-R1**. SOURCE_COMMIT_SHA=`b5ca9d377d454dfbec63ece76dd1c759abc3656d`.
Репозиторий `ic8812825-maker/chatgpt.com-codex`, ветка `work`, все относительные source paths внутри `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/`.
Статус: **PROPOSED / AWAITING_OWNER_DECISION**. Ни один текст не APPROVED. Нормативный выбор, architecture/provider и implementation evidence — разные gates.
STATIC_REVIEWED означает чтение исходного текста; MATH_DERIVED — вывод при указанных предпосылках; COUNTEREXAMPLE_CONFIRMED — опровержение утверждения, не runtime PASS; HISTORICAL_TEST_RESULT — старый artifact; все новые vectors TEST_SPECIFIED_NOT_RUN; NATIVE_NOT_RUN. Новых compile/runtime/mutation/native tests не выполнялось.
UNAVAILABLE — обязательное evidence отсутствует; CONFLICT — доказательства противоречат; REJECT — доказанное нарушение домена/предусловия. Все три запрещают новый effect; финансовая delta=0. NO_OP возможен только по валидному полному старому receipt.
Публикация отчёта не утверждает контракт, не закрывает P0 и не разрешает production/R1.1/dispatch/trading.

ReconciliationManifestId=HSBI_CONTRACT_DEPENDENCY_MANIFEST_V1;Revision=HSBI-03E-R1.
Источники: Reports/HSBI_03D_CONTRACT_CONSISTENCY_MATRIX_RU.md:1–71; HSBI_03D_OWNER_APPROVAL_BALLOT_RU.md:50–369; HSBI_03D_INDEPENDENT_CONTRACT_REVIEW_RU.md:114–625; HSBI_R11_P0_DEPENDENCY_PLAN_RU.md:20–223.
Production corroboration: EconomicLedgerTypes:6–12;AllocationLedgerTypes:5–10;ReserveAllocationTypes:15–30;ReserveCatchUpEvaluator:24–76;NewFarCandidate:26–40;NewFarSolver:119–151;ExecutionJournal:18–43;PersistenceInterface:5–7;ControlPrices:11–24. Все пути Include/Money,Include/Planning,Include/Persistence согласно source catalog HSBI03D; это STATIC_REVIEWED,не реализация нового контракта.

## Preserved dependency graph

N normative;A architectural;E evidence. Exact baseline edges HSBI03D сохранены:
| ID | Requires | Integration order |
|---|---|---|
| D01 | D10 N,D14 A,D16 N | exact grant/lifecycle + registry + mapping jointly specified |
| D02 | D08 N,D13 E,D14 A | source authority/freshness before spendable |
| D03 | D02 N,D14 A | role eligibility before source credit |
| D04 | D02 N,D06 N,CR09 N | same absolute loss/cost basis for every required level |
| D05 | D06 N,D07 A,D13 E | ordered actual net,sticky/reset persisted before continuation |
| D06 | D02 N,D13 E;D11 N posting clarification | Initial policy/cost scope before result authority |
| D07 | D08 N,D10 N,D13 E,D14 A | same transaction state+receipt+source |
| D08 | D02 N,D12 A,D13 E,D16 N | logical source independent wire;unknown history quarantine |
| CR09 | D04 N,D06 N,D13 E,D14 A | all-level feasibility before objective |
| D10 | D11 N,D12 A,D15 E | numeric manifest freeze joint |
| D11 | D10 N,D13 E,D15 E | currency/grid/posting evidence before conversion |
| D12 | D08 N,D10 N,D11 N,D15 E | codec/native/identity compatibility |
| D13 | D08 N,D12 A,D15 E | provider receipt,canonical profile,native clock/domain |
| D14 | D01 N,D02 N,D07 A,D08 N | global atomic registry contract |
| D15 | D10 E,D11 E,D12 E | concrete manifest→native evidence→qualified binding |
| D16 | D01 N,D07 A,D08 N,D10 N | original/remaining mapping+full applied events |

Реальная большая strongly connected group baseline {D01,D02,D07,D08,D10,D11,D12,D13,D14,D15,D16}; cycle{D04,CR09}. D06 posting link сохранён. Уточнения shared interfaces могут добавить обратные обязанности (например D07 persist D05 reset state);они не удаляют cycles. Не заявляется global DAG или возможность независимого activation каждого bundle.

## Проверка обязательных пар

| Пара | Совместимый contract | Несовместимо/стоп | Проверяемый критерий |
|---|---|---|---|
| D01↔D14 | immutableG=Σgrants;G_b=C_b+R_b+F_b;single source inventory | новый allocation key повторно credit source;local map authority | concurrent30+30/Free50 →only one;atomic receipt/revision |
| D02↔D13 | projected receipt preview only;actual independent authority | fresh=true/hash→confirmed funds | authority missing→UNAVAILABLE;altered snapshot→CONFLICT |
| D05↔D07 | sticky/cap/monitor epochs+reset receipt in durable history | restart setsfalse;positive net reset;unknown resend | −15,+100 cap12 remainssticky afterrestart;authorized reset no autoresume |
| D06↔D04 | same physical cost basis;Initial affects recovery membership only | incremental loss covers absolute;exclude costs to improve result | E/H/I formulas;absolute50/reserve30 reject |
| D07↔D08 | same physical source dedup;ObservationID separateCommitSeq | new event/import resets source/applied events | exact replay0delta;changed body conflict beforeNOOP |
| D08↔D12 | semantic K/body validated across approved profiles | wire hash/version=newincome | same source across codecs;unknownmapping unavailable |
| D10↔D11↔D12↔D15 | exact settled/range+posted profile+canonical codec+native | float minor conversion withoutreceipt;referencePASS=native | every numeric vector on chosen build/profile;UNBOUND blocks |
| D16↔D07/D08 | migration receipt preserves K,applied set,consumed/sticky | missing namespace defaults;reset journal/revision | unknown legacy quarantine;exact migrationNOOP |
| CR09↔D04/D06 | min all-levelmargin>0 with absolute loss,disjointcosts | maxTransition selected level alone;same future funds reused | loss(10,5)/margin(9,−11) reject;prefix inventory |
| CR09↔objective | identicalF before A/B;requiredtail status explicit | unsafe better objective wins | NF1–NF3 x excluded;objective choice only feasible set |
| D03↔D14 | BigOnly eligibility;Small economic separate | totalbasketnet creditsBig | Core−10/Small100→Big0 |
| D06↔D01/D14 | Initial inclusion B only recoverymetric | B creates Initial grant/coverage | R_B maypass,Initialgrant0,coverage independent |

## Versioned approval manifests (embedded,не дополнительные файлы)

Каждый manifest имеет statusPROPOSED/OwnerApprovalAWAITING. Member IDs остаются самостоятельными. Значения choices/profile bindings должны быть заполнены owner receipt;placeholder не approval.

### HSBI_APPROVAL_NUMERIC_BUNDLE_V1 / HSBI-03E-R1

Members: NUM-EXACT-1(D10),NUM-DOMAIN-1(D11),NUM-CODEC(D12),MQL-DOMAIN(D15).
Texts: HSBI_NUMERIC_CONTRACT_MANIFEST_V1/HSBI-03E-R1;HSBI_03E_NUMERIC_VECTORS_V1/HSBI-03E-R1;inherited16texts exact03D blob ccc83eb70ccbe0daa9963d3ca12352eb6a59325d.
Bindings: Currency/Account/Posting/Grid/CostProfile IDs,chosen codec/version,role/native enum mappings,resource caps,zero/error bounds,legacy adapter.
Evidence: independent posted receipts;native compiler/terminal/log/vector set;hostile decoder;overflow/roundtrip;D08 association.
State now: principle choices ready;concrete profile UNBOUND;native NOT_RUN;activation BLOCKED.

### HSBI_APPROVAL_FUNDING_AUTHORITY_BUNDLE_V1 / HSBI-03E-R1

Members: D01,D02,D03,D07,D08,SNAP-FIXTURE-1(D13),FUNDING-GLOBAL-ATTRIBUTION(D14),BALANCE-SCHEMA-MAPPING(D16).
Texts: exact03D member normative paragraphs plus full HSBI_SNAPSHOT_AUTHORITY_V1/HSBI-03E-R1 and numeric cross-reference.
Bindings: source namespace/association provider,receipt trust/clock/epoch,registry scope,transaction schema+linearization point,complete source manifest,appliedevent set,migration mappings.
Evidence: same source alias rejection,bookgrant partitions,correctroleeligibility,concurrent+crash/restart/provider mismatch.
D14 atomicity НЕ implemented. UNKNOWN/correction deficit quarantine cannot be cleared by newIDs/profile.
State now: proposed interfaces;providers/durability/native missing;activation BLOCKED.

### HSBI_APPROVAL_SAFETY_RESTART_BUNDLE_V1 / HSBI-03E-R1

Members: D05,D07,SNAP-FIXTURE-1(D13);crossrefs D06,D14,D16.
Text: exact03D D05 current/peak/sticky/reset paragraph + E snapshot restart contract.
Bindings: immutable OperationID/CapEpoch,H,owner principal/control-plane trust,HistoryOrderAuthority,MonitoringEpoch,ResetReceipt fields,SAFE scope,no autoresume.
Evidence: ordered prefixes,cap equality,corrupt/incomplete history,unauthorized/stale reset,crash before/after reset commit.
No default owner principal or ordered-history provider is invented. Reset не меняетconsumed,appliedsource,archivedpeak;funding registryunchanged.
State now: ready policy choice;backend evidence BLOCKED.

### HSBI_APPROVAL_RECOVERY_NEWFAR_BUNDLE_V1 / HSBI-03E-R1

Members: D04,D06,CR-09;companion NEWFAR-OBJECTIVE(A/B),crossrefs D02,D03,D05,D13,D14 andnumeric.
Texts: D06-A or D06-B/HSBI-03E-R1;MINIMUM_SAFE_V1 orRISK_FIRST_V1/HSBI-03E-R1;03D D04/CR09.
Bindings: chosenInitialPolicy,CostBasisManifest(I,H_in,H_gate),absoluteFarBasis,requiredLevelSet,tail theorem status,objective tuple,canonical tieID,source inventory perprefix.
Evidence: D06 pairedexamples,partial invariance conditional proof,NF1–NF3,all-level negative,membership/costnooverlap.
State now: options ready,owner choices AWAITING,tail theorem/provider/nativemissing;activation BLOCKED.

### HSBI_OWNER_DECISION_PACKAGE_V1 / HSBI-03E-R1

Member set exactly16 IDs from owner ballot;fourbundle manifests above version-pinned;no17th money ID.
Receipt schema:
PackageVersion,PublishedCommitSHA,FileBlobSHAs,CanonicalDecisionId,SelectedOption,TextVersion,Scope,OwnerIdentity,DecisionDate,Decision(APPROVE/REJECT/DEFER),DependencyManifestVersions,ExplicitSupersession,ImplementationPermission=NO.
All OwnerDecision fields currentlyAWAITING;PublishedCommitSHA assigned externally after publication,не self-referential SHA.
If one bundle changes,overlap interfaces must be reconciled;passingonebundle не unlock другой. Concurrency/journal completeness нельзя объявить achieved из architecture approval.

## Оставшиеся вопросы и acceptance

Owner D06 A/B;objective A/B;cost/headroom policy;currency/grid/codec binding;provider/trust/clock policy;authorized reset principal;fullhistory/migration;native qualification;tail theorem. Не меняем исходные нормы,пока owner не утвердил точнуюreplacement version.
Consistency accept iff all16IDs present exactlyonce,chosen options have no incompatible pairs,sharedprofile/source/revision/receipt schemas match,cycles declared,all UNBOUND/evidence gates explicit,production untouched.
Связи: [owner ballot](HSBI_03E_OWNER_FINAL_DECISION_BALLOT_RU.md),[gates](HSBI_03E_R11_GATE_MATRIX_RU.md),[D06](HSBI_03E_D06_POLICY_RESOLUTION_RU.md),[objective](HSBI_03E_NEWFAR_OBJECTIVE_RESOLUTION_RU.md),[numeric](HSBI_03E_NUMERIC_CONTRACT_MANIFEST_V1_RU.md),[snapshot](HSBI_03E_SNAPSHOT_AUTHORITY_CONTRACT_RU.md).
