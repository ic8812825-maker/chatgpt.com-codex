# HSBI-03E-D — Snapshot authority contract

Версия: **HSBI-03E-R1**. SOURCE_COMMIT_SHA=`b5ca9d377d454dfbec63ece76dd1c759abc3656d`.
Репозиторий `ic8812825-maker/chatgpt.com-codex`, ветка `work`, все относительные source paths внутри `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/`.
Статус: **PROPOSED / AWAITING_OWNER_DECISION**. Ни один текст не APPROVED. Нормативный выбор, architecture/provider и implementation evidence — разные gates.
STATIC_REVIEWED означает чтение исходного текста; MATH_DERIVED — вывод при указанных предпосылках; COUNTEREXAMPLE_CONFIRMED — опровержение утверждения, не runtime PASS; HISTORICAL_TEST_RESULT — старый artifact; все новые vectors TEST_SPECIFIED_NOT_RUN; NATIVE_NOT_RUN. Новых compile/runtime/mutation/native tests не выполнялось.
UNAVAILABLE — обязательное evidence отсутствует; CONFLICT — доказательства противоречат; REJECT — доказанное нарушение домена/предусловия. Все три запрещают новый effect; финансовая delta=0. NO_OP возможен только по валидному полному старому receipt.
Публикация отчёта не утверждает контракт, не закрывает P0 и не разрешает production/R1.1/dispatch/trading.

ContractId=HSBI_SNAPSHOT_AUTHORITY_V1;Revision=HSBI-03E-R1.
SNAPSHOT_AUTHORITY_STATUS=PROPOSED_CONTRACT_READY_PROVIDER_BLOCKED. CanonicalDecisionId=SNAP-FIXTURE-1 (D13) сохраняется; fixture profile не выдаётся за production authority.

## Источники

Docs/31_MONEY_PROOF_IDENTITY_RU.md:3–7; Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md:12,18–24; Docs/12_FINAL_CLOSE_SPECIFICATION_RU.md:9–15; Docs/16_PERSISTENCE_AND_RESTART_RU.md:9–18.
Docs/NEXT_STAGE_02B_R0D_SNAPSHOT_IDENTITY_CONTRACT_RU.md:11–24 fixture ID/tick/receipt.
Reports/HSBI_03D_INDEPENDENT_CONTRACT_REVIEW_RU.md:498–529; HSBI_03D_OWNER_APPROVAL_BALLOT_RU.md:290–309.
Include/Planning/HSBI_ControlPrices.mqh:7–11 DTO/freshness,HSBI_IsSnapshotFresh;16–24 HSBI_ValidateTypedControlPrice.
Include/Money/HSBI_BrokerMoneyTypes.mqh:7–18 properties validation; Include/Planning/HSBI_NewFarSolver.mqh:100,119–127 caller freshness/identity.
Include/Persistence/HSBI_ExecutionJournal.mqh:18–43 validation/append/chain; HSBI_PersistenceInterface.mqh:5–7 stub.
Self-computed hash и fresh=true не независимая authority. Текущие helpers не реализуют этот contract.

## Роли и trust boundary

1. SnapshotProducer — allowlisted read-only terminal/broker adapter instance,не caller strategy DTO. Он непосредственно читает quotes,properties,positions,orders,deals в заданном scope и фиксирует capture window.
2. OriginAssociationProvider — независимо от предъявленного DTO связывает broker position/deal с EA cycle/role/action/event и historical source plan;deal magic не достаточен.
3. ReceiptAuthority — allowlisted verifier/store,получающий original capture непосредственно от producer через configured trust binding. Он проверяет capture provenance,completeness,sequence,scope,clock и consistent cut;issued receipt immutable.
4. Consumer — planning/money/risk,передающий expected scope/revision/purpose и получающий verifier result. Он не может легитимировать altered DTO самопересчитанным hash.
5. DurableReceiptStore/Reconciler — сохраняет high-water,consumption/replay receipts,producer/process epochs и restart state;reconciles independent actual history.

Independent здесь означает независимость канала получения/validation от caller-supplied body,не обещание защиты от компрометации всего terminal/OS. In-process flags не доказательство независимости. Provider instance allowlist,trust binding,credential/signature/MAC scheme если transport untrusted,clock calibration и durable implementation UNBOUND. Сам факт signature без trusted key/source binding не enough. Данный этап не создаёт provider,keys,network endpoints или backend.

## Обязательный envelope/content receipt

Receipt body включает:
- ReceiptSchema/Version,ReceiptID,ProducerID/InstanceID,AuthorityID,TrustProfileVersion,raw evidence reference.
- BrokerNamespace,ServerNamespace,AccountLogin,exact Symbol,Magic,CycleID;Purpose,ExpectedPlanID,ActionID/EconomicEventID/ObservationID с explicit applicability.
- PositionSet с PositionIdentifier,Ticket,Role,Direction,actual Volume,Price/cost references;ordered canonical set;PositionSetCompleteness и independently associated ownership. Для FinalClose actual-zero purpose обязательный явно complete empty set,а не missing field.
- Deal/history coverage interval+watermarks,OrderSet/pending/unknown status,association receipt roots;source OriginPlan не обязан равняться current consumption Plan.
- StateRevision/RegistryRevision,PlanDigest,CostProfile/NumericManifest/InstrumentProfile versions,Candidate/RequiredLevelSet IDs при применимости.
- Market: bid/ask,quote event time/domain,point,tick size/asymmetric tick values,volume grid,all finite fields и availability markers.
- CaptureStart/End monotonic ticks,ClockDomain/TimeUnit,ClockEpoch/BootID,provider time,offset/skew bound,QuoteAgeBound,IssuedAt/ExpiresAt,ProducerSequence.
- OriginalContentDigest,canonical body/codec profile,PreviousReceipt/sequence linkage,ReconciliationEpoch/Receipt,authority attestation/trust binding и issuance status.

ContentDigest вычисляется по полному immutable original envelope и ordered positions/deals;authority attestation отдельно подтверждает original source/capture. Caller digest не заменяет attestation/store lookup. If canonical codec unqualified→no production receipt acceptance. Receipt ID namespaced by authority/producer epoch,not bare integer across restart.

## Независимая freshness и clock skew

Authoritative freshness clock — approved provider/local monotonic clock captured by verifier,not caller now/fresh flag. Broker quote/deal timestamp authoritative только как event timestamp;не доказывает независимый now и не заменяет clock calibration.
Для одного exact clock: age=trustedNow−captureTime;0≤age≤TTL. Capture window и quote event age проверяются отдельно: повторно прочитать старую котировку не делает её fresh.
Для translated clock: δ=localClock−providerClock;approved offset estimate δ0,error bound ε≥0.
a=trustedNowLocal−(ProviderTimestamp+δ0);true age∈[a−ε,a+ε].
Консервативно accept iff whole interval subset [0,TTL];capture/quote windows оба удовлетворяют profile. Если interval выходит за bounds→no freshness permission;future exact timestamp→REJECT,uncertain bound→UNAVAILABLE по typed reason. Никакого молчаливого «допустимfuture».
Все timestamp subtraction/translation checked;ClockDomain/TimeUnit должны совпадать/calibrated. FIXTURE_MONOTONIC/tick не UTC/ms. Неизвестные TTL/skew/clock mapping→UNAVAILABLE.

QuoteAgeBound проверяется против quote TTL даже если capture age fresh. Clock calibration receipt/revision/expiry bound independently verified. Example exact100−95=5≤10;future101 age−1 reject. Offset example a5,ε2,TTL10 →[3,7] fresh; a9,ε2→[7,11] unavailable.

## Consistent cut и неполные данные

Receipt не обещает атомарного broker snapshot,если API даёт последовательные reads. Producer фиксирует bracket/capture duration,positions/orders/history watermarks и journal revision;verifier доказывает достаточный consistent cut/rechecks. Если между reads изменился обязательный state или completeness unknown — UNAVAILABLE/reconcile. Нельзя выдавать смешанные quotes/positions разных revisions за single snapshot.
Missing field/type malformed→REJECT;known field explicit unknown required data→UNAVAILABLE. No authority→UNAVAILABLE,no financial delta. Account/symbol/cycle/position mismatch→CONFLICT and reconciliation. Если full position set подтверждает отсутствие expected position→REJECT(SOURCE_POSITION_MISSING),reconcile context,не подменять position. Для purpose FINAL_CLOSED_POSTCONDITION expected empty complete set допустим;ordinary NewFar expected residual не empty.

## Replay,старые snapshots и authority use

Receipt существует immutable в trusted store до caller acceptance. Same scoped SnapshotID/epoch,changed body →CONFLICT,даже с новым caller digest.
Exact old event receipt после полной integrity проверки может дать historical NO_OP;он не позволяет новую action по expired snapshot.
Новая authority требует current expected state/plan/registry revisions,purpose,producer epoch/sequence не rollback,clock age,receipt unused-for-this-action/operation semantics,live reconciliation.
Snapshot может использоваться несколькими разрешёнными read-only preview consumers в TTL;нельзя превращать его в unique spending permission. Каждое новое financial effect требует отдельного D07/D14 transaction receipt и current revalidation;reusing snapshot не повторяет source grant.
High-water producer sequence защищает от rollback;duplicate exact receipt допустим как read/replay только без нового authorization. Смена schema/epoch не очищает applied-event inventory.

## Restart

Начать BLOCKED. Проверить durable receipts/chain/revisions/source inventory,pending/unknown,read actual positions/orders/deals,reconcile,создать новый ReconciliationEpoch receipt. Старый monotonic BootID не сравнивать с новым;старый snapshot только historical evidence. Для нового authorization требуется новый capture/receipt в current epoch. Reconciliation receipt не auto-resume;D05 sticky/owner reset сохраняются. Incomplete/corrupt journal/history→UNAVAILABLE/TERMINAL_SAFE manual review. Existing persistence stub не удовлетворяет этому.

## Fixed cases и expected (TEST_SPECIFIED_NOT_RUN)

Fixture authority A1/producer P1,account1,symbolEURUSD,cycle7,position13,event31,plan9,rev4,epochE1;complete source/store/reconciliation предполагаются только для positive fixture. Exact clock now100,TTL10,capture95,quote95.

| ID | Изменение входа | Expected |
|---|---|---|
| S+ | Original receiptR1,all scope/body match | AUTHORIZED_PREVIEW_ONLY;не funds/dispatch |
| S01 | fresh=true,authority/store evidence absent | UNAVAILABLE(AUTHORITY_MISSING) |
| S02 | ID R1 unchanged,bid changed,caller hash recomputed | CONFLICT(CONTENT_MISMATCH),delta0 |
| S03 | timestamp101 exact clock | REJECT(FUTURE_TIMESTAMP) |
| S04 | receipt account2,expected account1 | CONFLICT(ACCOUNT_SCOPE),delta0 |
| S05 | expected position13,complete actual set omits13 | REJECT(SOURCE_POSITION_MISSING),reconcile |
| S06 | position set completeness unknown | UNAVAILABLE(INCOMPLETE_POSITION_SET) |
| S07 | restartE2,receiptE1,no reconciliation | UNAVAILABLE(RESTART_NOT_RECONCILED) |
| S08 | exact old event replay+valid full receipt at expired time | historical NO_OP only;new action REJECT(EXPIRED) |
| S09 | a5,ε2,TTL10 →[3,7] | fresh if other gates valid |
| S10 | a9,ε2 →[7,11] | UNAVAILABLE(AGE_BOUND_EXCEEDS_TTL) |
| S11 | capture95 but quote80,quoteTTL10 | REJECT(STALE_QUOTE) |
| S12 | no position expected for confirmed closure,complete empty set,current receipt | valid postcondition evidence;ledger/persist required before CLOSED |
| S13 | sequence rollback100→99 for new action | REJECT(SEQUENCE_ROLLBACK) |
| S14 | caller requested event32 but action receipt bound31 | CONFLICT(EVENT/PURPOSE_BINDING) |
| S15 | source historical OriginPlan1,valid association/current consumePlan9 | no false rejection merely from unequal origin/current plan;other binding required |
| S16 | clock unit tick vs expectedms without mapping | UNAVAILABLE(CLOCK_DOMAIN) |

## Acceptance и unresolved

Проверить all fixed cases,causal authority substitution,receipt-store tamper,position-set add/drop,duplicate/root mutation,capture race,clock reset/overflow,all restart stages. Нужны independent producer/verifier trust evidence,durable store,provider clock/calibration/live metadata,canonical encoding,native integration. Все отсутствующие instance facts UNBOUND; статус provider-blocked сохраняется.
Связи: [numeric manifest](HSBI_03E_NUMERIC_CONTRACT_MANIFEST_V1_RU.md),[bundles](HSBI_03E_CONTRACT_DEPENDENCY_RECONCILIATION_RU.md),[owner ballot](HSBI_03E_OWNER_FINAL_DECISION_BALLOT_RU.md),[R11 gates](HSBI_03E_R11_GATE_MATRIX_RU.md).
