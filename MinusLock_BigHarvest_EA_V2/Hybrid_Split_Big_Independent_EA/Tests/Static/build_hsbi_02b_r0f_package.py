#!/usr/bin/env python3
"""Generate R0F proposals, not approvals. All artifacts new; no production helper creation."""
import json,re,hashlib
from pathlib import Path
import check_hsbi_02b_r0f_common as a
import hsbi_02b_r0f_decisions as decisions
import hsbi_02b_r0f_contract_candidate as model
import hsbi_02b_r0f_independent_fixtures as fixtures
R=a.ROOT;HEAD='BASE_SHA='+a.BASE+'\n\nPROPOSED / AWAITING_ADMIN_APPROVAL. CONTRACT-DECISION-PREPARATION / TEST-ONLY. Не разрешение production или торговли.\n\n'
PROD='Include/Money/HSBI_EconomicLedgerTypes.mqh'
def read(name):
 f=R/('Tests/Evidence/NEXT_STAGE_02B_R0F_'+name+'.json');return json.loads(f.read_text()) if f.exists() else {}
def write(path,text):(R/path).write_text('\n'.join(line.rstrip() for line in text.rstrip().splitlines())+'\n')

def fields():
 result=[]
 for name in model.FIELDS:
  key=name in ('Broker','Server','AccountLogin','DealTicket')
  raw=name in model.RAW
  if raw:typ='finite binary64 raw observation; no money rounding; Volume/Price>0'
  elif name in ('SourcePlanApplicable','SourcePolicyApplicable'):typ='exact bool from independent origin association; not user assertion'
  elif name in ('SourcePlan','SourcePolicyVersion'):typ='ulong1..2^64-1 when applicable; None only independently NOT_APPLICABLE; unknown applicable =>UNAVAILABLE'
  elif name in ('AccountLogin','TimestampMsc'):typ='long positive1..2^63-1'
  elif name=='Magic':typ='long signed[-2^63,2^63-1], nonzero for this EA-attributed profile; external/manual deals remain economic facts outside this eligible profile'
  elif name=='Precision':typ='known money digits; fixture0..8; production currency policy separately approved; not SYMBOL_DIGITS'
  elif name=='SchemaVersion':typ='ulong, supported proposed version1; unknown version UNAVAILABLE'
  elif name in ('Broker','Server','Symbol','Currency','Role','EntryType','DealType'):typ='exact nonempty UTF8/no NUL; closed enum where applicable; no NFC/casefold guessing'
  else:typ='ulong1..2^64-1'
  authority='Independent broker/account context' if name in ('Broker','Server','AccountLogin','Currency','Precision') else 'Independent EA-origin journal association, never current consumption context/comment' if name in ('CycleID','ActionID','EventID','Role','SourcePlanApplicable','SourcePlan','SourcePolicyApplicable','SourcePolicyVersion') else 'Approved economic schema registry' if name=='SchemaVersion' else 'Independent broker history observation/receipt'
  migration='Preserve captured legacy value only if provenance/type/precision complete; never invent missing fields. Unknown required facts=>UNAVAILABLE/quarantine.'
  if name in ('Broker','Server','AccountLogin'):migration='Legacy key lacks account namespace; independent storage/history ownership receipt required; do not substitute current terminal account/server.'
  if name=='TimestampMsc':migration='Legacy seconds timestamp does not prove missing milliseconds; no automatic *1000 inference as exact original timestamp.'
  result.append(dict(Field=name,ExactType=typ,SourceKey=key,ImmutableEquality=True,Required=True,MayChangeDuringReconciliation=False,ReconciliationRule='Corrections are separate versioned linked events; never overwrite original payload or call changed record NO_OP',Authority=authority,Serialization='A typed length-prefix UTF8/T17Z or B typed binary/F64Z in fixed field order; profile not selected',Migration=migration,Units='lots' if name=='Volume' else 'quote price' if name=='Price' else 'account currency raw observation' if name in ('Profit','Swap','Commission','Fee','DealNet') else 'milliseconds' if name=='TimestampMsc' else 'schema-defined/identifier'))
 return result

def variants():
 common=dict(ProductionImplementationAllowed=False,RequiredApprovals=['D-08','NUM-CODEC (scope-dependent)','MQL-DOMAIN','D-02 provider boundary','new explicit baseline/allowlist task'],Rollback='Separate reviewed revert of own future phase commit; preserve old/new bytes/schema; no reset/rebase/force, no compensating trades.',CompilePlan='Real MetaEditor main + new scoped MQL5 assertion harness; capture compiler version/log/exit. g++/Python not a substitute. NOT_RUN now.',Migration='No actual storage migration. Legacy without complete namespace/units/origin remains UNAVAILABLE; preserve original bytes/hash. No current ACCOUNT_LOGIN fallback.')
 return [dict(Variant='Minimal R1.1',ProductionAllowlist=[PROD],DiffScope='Only inline schema/namespace helpers, immutable full-field equality/duplicate validation in existing header; no authoritative new persistence codec/backend. Legacy serializer remains explicitly diagnostic and cannot serve as new identity payload.',SingleFileFeasibility='STATICALLY_POSSIBLE_FOR_LOCAL_HEADER_ONLY; no active external production callsites found by textual inventory; native compile/integration not proved.',APICompatibility='New required fields break semantic compatibility of legacy records. Bool equality returns false for invalid input; new typed V2 validation/classification must expose REJECT/UNAVAILABLE. Preserve old facade only with explicit lossy-status/deprecation policy; no mapping unavailable→NEW/NO_OP. Administrator must approve facade policy.',NegativeTests=['same Net changed Profit/Swap/Commission/Fee','foreign namespace','same deal changed Magic/Cycle not NEW funding','unknown schema/currency/precision/origin','malformed/nonfinite raw values','exact replay zero delta','legacy diagnostics cannot become proof'],Acceptance='Fresh scoped native tests + per-field source mutations; one-file scope; no IO/provider lookup/credits/dispatch. Minimal does NOT claim stable restart serialization or full economic reconciliation.',**common),dict(Variant='Extended R1.1',ProductionAllowlist=[PROD,'Include/Money/HSBI_EconomicSourceNamespace.mqh','Include/Money/HSBI_EconomicCanonicalCodec.mqh','Include/Money/HSBI_EconomicLegacyAdapter.mqh'],DiffScope='Additional headers only after separate explicit approval. Namespace helper separates validation; codec helper raw serialization only; legacy adapter read-only typed mapping/quarantine only, no persistent migration.',SingleFileFeasibility='Extra headers are modularization/testability choices, not logically required; all could be inline but complexity/compile review grows. No new production headers created in R0F.',APICompatibility='Versioned V2 status/schema and codec envelope; no silent reinterpretation of four-field legacy string. Real provider caller integration requires a separate expanded allowlist if production callsites appear.',NegativeTests=['all Minimal tests','both codec golden vectors','unknown profile/schema/type tags','duplicate/trailing/oversized bytes','utf8 length and delimiter collision','source digest corruption','legacy source missing account never auto-enriched'],Acceptance='Selected approved codec + native UTF8/long/ulong/double/roundtrip golden tests; no money-domain substitution; no migration writes, backend or trading.',**common)]

def topo(edges):
 nodes={n for edge in edges for n in edge};left=set(nodes);order=[]
 while left:
  ready=sorted(n for n in left if not any(v==n and u in left for u,v in edges))
  if not ready:raise ValueError('dependency cycle')
  order+=ready;left-=set(ready)
 return order

def build_contracts():
 tests=read('TEST_RESULTS');rows=decisions.rows();field_rows=fields();v=variants();approval_edges=[(d,r['DecisionID']) for r in rows for d in r['Dependencies']]
 mapping={f'R0F-{i:02}':[] for i in range(1,13)}
 for test in tests.get('Rows',[]):
  for req in test['RequirementID'].split('/'):
   if req in mapping:mapping[req].append(test['TestID'])
 money_types=[dict(Name=n,Projected=n.startswith('Projected'),Unit='account currency + explicit precision/basis',ImplicitConversionsAllowed=False,RequiredEvidence=('independent current price/cost/risk snapshot, planning only' if n.startswith('Projected') else 'confirmed independent closing history/raw components' if n=='ActualRealizedDealNet' else 'independent posted receipt + currency/precision/component reconciliation' if n=='ReconciledEconomicNet' else 'reconciled eligible role + policy/allocation receipt' if n=='EligibleSourceGrant' else 'committed allocation + complete reconciled journal + global attribution + available ownership'),Spendability='NEVER_DIRECT' if n!='AvailableReserve' else 'ONLY_AFTER_ALL_INDEPENDENT_AUTHORITY_GATES') for n in ('ProjectedBasketNet','ProjectedCloseNowNet','ActualRealizedDealNet','ReconciledEconomicNet','EligibleSourceGrant','AvailableReserve')]
 matrix=dict(MoneyTypes=money_types,BaseSHA=a.BASE,ContractVersion='HSBI-R0F-PROPOSED-1',ApprovalStatus='AWAITING_ADMIN_APPROVAL',Evidence='Tests/Evidence/NEXT_STAGE_02B_R0F_TEST_RESULTS.json',Requirements=[dict(RequirementID=k,TestIDs=ids,ProofBoundary='Candidate fixture/math/encoding only; documents/admin tests cover decision preparation, not production runtime') for k,ids in mapping.items()],EconomicFields=field_rows,AllocationImmutableFields=['SourceLogicalKey','AllocationID','AllocationEventID','AllocationPolicyVersion','Currency','Precision','EligibleSourceReceiptRef','OriginalBucketGrants','Phase','Unallocated'],AllocationMutableState=['Consumed','Reserved','Free','ReservationOwners','StateRevision','JournalReferences'],CodecProfiles=['HSBI-T17Z-1','HSBI-F64Z-1'],CodecSelected=None,TransitionPolicySelected=None,RuntimeEvidenceEdges=[list(e) for e in decisions.EVIDENCE_EDGES],RuntimeTopologicalOrder=topo(decisions.EVIDENCE_EDGES),ApprovalDefinitionEdges=[list(e) for e in approval_edges],ApprovalTopologicalOrder=topo(approval_edges),Statement='A/B/C are mutually exclusive execution policies; all are tested alternatives, none becomes approved automatically.')
 a.save('ADMIN_DECISIONS',dict(BaseSHA=a.BASE,Source='Reports/NEXT_STAGE_02B_R0E_C3_ADMIN_DECISION_MATRIX_RU.md + exact R0F proposal rows',Rows=rows,DecisionsTotal=16,Approved=0),folder='Tests/Contracts');a.save('CONTRACT_MATRIX',matrix,folder='Tests/Contracts')
 acceptance=[]
 for variant in v:
  for id,description in [('SCOPE','Only approved files, no production helpers outside chosen allowlist'),('NAMESPACE','Broker/server/account/deal logical namespace, never terminal-account guess'),('IMMUTABLE','Exact all-component source equality, same-key changed payload conflict'),('API','Explicit V2 reject/conflict/unavailable/new/noop dispositions; legacy wrapper policy approved'),('UNITS','Currency/precision receipt or unavailable; no local raw→posted conversion'),('MIGRATION','Legacy ambiguous ownership/units quarantine, no writes'),('MUTATIONS','Every immutable field has a causal source mutation; runtime exceptions not kills'),('COMPILE','Real MetaEditor main+harness, compiler/exit/log; currently NOT_RUN'),('ROLLBACK','Reviewed phase revert only, preserve raw evidence, no trades'),('NO-TRADE','No OrderSend/CTrade dispatch/runtime-policy changes')]:
   acceptance.append(dict(CriterionID='R1-'+('MIN' if variant['Variant'].startswith('Minimal') else 'EXT')+'-'+id,Variant=variant['Variant'],Condition=description,CurrentStatus='SPECIFIED_NOT_IMPLEMENTED',RequiredEvidence='Future scoped native test/source diff after approval',R0FTestEvidence='Tests/Evidence/NEXT_STAGE_02B_R0F_TEST_RESULTS.json; identity/codec candidate only',ProductionSource=PROD))
 matrix['Requirements'][10]['PreparationEvidence']='Tests/Evidence/NEXT_STAGE_02B_R0F_CONSISTENCY.json#ADMIN-16'
 matrix['Requirements'][11]['PreparationEvidence']='Tests/Evidence/NEXT_STAGE_02B_R0F_CONSISTENCY.json#R1-SCOPE'
 a.save('CONTRACT_MATRIX',matrix,folder='Tests/Contracts')
 a.save('R1_ACCEPTANCE_MATRIX',dict(BaseSHA=a.BASE,Variants=v,Criteria=acceptance,R1_1_START_ALLOWED=False,SourceCallsiteInventory='Include/Money/HSBI_EconomicLedgerTypes.mqh:6–12; no other production references found in baseline scan'),folder='Tests/Contracts');return matrix,rows,v

def main():
 matrix,rows,v=build_contracts();tests=read('TEST_RESULTS');verification=read('VERIFICATION');gap=read('STATUS_GAP');pkg=read('PACKAGE_RESULTS')
 write('Docs/NEXT_STAGE_02B_R0F_MONEY_CONTRACT_CANDIDATE_RU.md','# R0F — кандидат денежных контрактов\n\n'+HEAD+'''## Иерархия и статус

Первичные Docs04/08/16/24/31/32 — исторические нормативные источники. Их наличие/статус source-of-truth не заменяет явное административное решение о proposed изменениях. Production source — фактическое поведение, не разрешение изменить экономику. R0D/R0E/C1/C2/C3 — proposed/spec/test evidence; C3 предложения не стали APPROVED. Спорные версии перечислены в CONFLICT_RESOLUTION; выбранной production policy в R0F нет. Independent counterexamples опровергают свойства в указанном scope, не подтверждают broker execution.

## R0F-01: закрытая кандидатная схема баланса

OriginalGrant=Consumed+Reserved+Free; RemainingGross=Reserved+Free; все четыре части неотрицательны и имеют одну currency/precision/ownership. Bare Gross запрещён в новом API из-за конфликта с legacy RemainingGross. Grant — immutable исходный ресурс, Consumed никогда не возвращается в Free без отдельного подтверждённого экономического события. AvailableReserve не равен просто полю Free: нужен полный authority/journal/global-funding proof.

Reserve x: F'=F-x,R'=R+x; release своему owner: F'=F+x,R'=R-x; consume free: C'=C+x,F'=F-x; consume reserved своему owner: C'=C+x,R'=R-x. Везде x>0, checked bounds, новый event/revision. Чужой owner не тратит reserved. Grant50/C10/R15/F25 =>RemainingGross40; C+R+RemainingGross=65 неверно. Source total COMMITTED ΣOriginalGrants=EligibleNet, Unallocated0; PREPARED Σgrants+Unallocated=EligibleNet, spending forbidden. Zero/negative actual net сохраняется economic, eligible grant0 без отдельного loss-consumption contract.

Exact event payload с original revision даёт NO_OP/zero delta; changed payload same event — CONFLICT. Complete trusted fixture journal — предпосылка модели, не durable proof. Unknown history/currency/precision/owner →UNAVAILABLE. Legacy adapter только при доказанной старой семантике RemainingGross: F=RemainingGross-Reserved. Не создавать фиктивный account/owner и не выполнять persistent migration.

## R0F-02: money types и переходы

ProjectedBasketNet — плановая корзина; ProjectedCloseNowNet — оценка закрытия по текущему snapshot/спреду/расходам; ActualRealizedDealNet — наблюдённые подтверждённые закрытия с исходными знаками Profit/Swap/Commission/Fee; ReconciledEconomicNet — независимая сверка raw/posted components, currency, precision и source; EligibleSourceGrant — разрешённая policy доля подтверждённого допустимого источника; AvailableReserve — неистраченный/неудержанный ресурс после complete ledger/journal и global attribution.

Прогноз100 не создаёт actual grant. Неполная history не known0. Raw signed sum точна в объявленном representation; ObservedDealNet — отдельное raw поле. Даже .1+.2 binary observations не равны exact decimal.3: это не основание локально создать broker posting. Независимые posted components/net и verified policy сохраняются отдельно. ReconciliationReceipt привязан к immutable source digest, хранится отдельным append-only envelope; текущий receipt не переписывает raw identity. Kind/confirmed/PolicyVerified в Python — trusted fixture boundary, не аутентификация брокера. Формальный registry шести типов — CONTRACT_MATRIX.MoneyTypes; runtime nominal-type enforcement и полный AvailableReserve API не реализуются. operate/state — trusted integer-balance algebra, не способ подтвердить авторизацию по вручную созданному state. Извлечение числа из projection не создаёт independent receipt.

## R0F-03: Big/Small

Рекомендуемый A: Core0/Trend0/Small10 =>BigReserve0/ResidualHeld10. B: только отдельный утверждённый transfer event с debit+credit и source provenance. Role/policy не меняются в старом source payload. Opening costs остаются economic facts, но не harvest grant; INOUT требует независимого разделения закрытой/открытой частей. HSBI_LevelMoneyEvaluator reserveGainMoney и Reserve Allocation/Catch-Up не меняются до approval D03 и отдельной production-фазы.

## R0F-04: Far/Catch-Up

AbsoluteFarLoss=max(0,-ProjectedCloseNowFarNet), incremental=max(0,absolute-baselineAbsolute) только diagnostic с verified basis/volume/cycle/plan/revision/clock lineage. Absolute50 baseline40 reserve30: покрытие incremental10 не покрывает50. BUY close по Bid, SELL по Ask. Restart/partial close/basis change без подтверждённого baseline делает incremental UNAVAILABLE.

CatchUpMargin_i=EligibleReserve_i-AbsoluteFarLoss_i-SafetyBuffer_i; all-required forecast proof требует min_i margin_i>0 и полные required levels, money/risk/margin/exposure/transition/lot/snapshot gates. Margin0 не PASS. Это необходимо, но недостаточно для real execution: broker authenticity, актуальная ликвидность/цены/margin, actual fills, durable ownership и последовательное расходование не доказаны. SINGLE_LEVEL maxTransition имеет другой scope. Нельзя несколько последовательных шагов финансировать одним и тем же исходным Free; ReserveAfter_i=ReserveBefore_i-Consumed_i.

## R0F-05: три политики, без выбора по умолчанию

| Policy | После Fill1=-15, cap12 | После Fill2=+100 | Cap gate после2 |
|---|---|---|---|
| A current signed | net-15, loss15, breach | net85, loss0 | Численно проходит; не runtime permission |
| B sticky | breach=true | breach=true | Не проходит до approved reset |
| C peak | peak15 | peak15 | Не проходит при cap12 |

У A reset означает новую доказанную operation/window, не обнуление actual losses; у B нужен отдельный authorized reset event с причиной/политикой/history linkage; у C historical peak нельзя уменьшать произвольной сменой окна. Cap/policy фиксируются на operation: смена cap/version не может молча очистить breach. Complete independently ordered unique fills нужны B/C после restart; отсутствие префикса →UNAVAILABLE. A может оценить проверенный текущий net, но не доказывает отсутствие прошлых breaches. Порядок [+100,-15] даёт net85/peak0: нельзя переставлять broker events ради результата. Partial closes не обходят cap через новые локальные batch labels; operation/cycle membership independently confirmed. Стоимость A — cumulative net; B — плюс persistent breach/reset receipts; C — плюс peak/ordered history/checkpoints. Backend не реализуется.

Никакая A/B/C не выбрана. Все параметры tests — PROPOSED fixture policies; при policy=None model возвращает UNAVAILABLE. Реальное действие в R0F запрещено при любом cap gate.

## R0F-08: immutable allocation и mutable consumption

Immutable AllocationGrantRecord: logical source, AllocationID/EventID, allocation policy, currency/precision, eligible source receipt, OriginalGrant vector FinalReserve/PartialFar/Transition/Carry/Residual, phase/unallocated. Same source/event с FinalReserve50/Partial0→0/50 — CONFLICT, хотя total50. Mutable Consumed/Reserved/Free/owners/revision/journal — отдельный ConsumptionState: replay grant никогда не сбрасывает consumed. Same state revision с изменённым consumed/available — конфликт snapshot; легальный расход требует нового event/revision. PREPARED не расходуется. Подготовка — отдельный versioned draft/PreparationID, не изменяемый replay уже committed AllocationEventID. Final source allocation commit имеет полный immutable payload/manifest и Unallocated0. Если есть child allocations, source-level commit обязан атомарно покрыть их полный manifest; partial child не получает ресурс до полного group commit. Изменение draft не переписывает committed payload. Любая последующая transfer/rebalance policy требует нового события с conservation, а не повторного funding source. Нельзя выдавать residual/unallocated за permission to spend.

## R0F-09: ровно один раз и authority

In-memory idempotency — только память fixture. Immutable journal — payload/sequence/source binding; durability — проверяемый commit/recovery; CAS/concurrent authorization — отдельный backend atomicity; broker reconciliation и snapshot-content binding — независимые evidence. Ни одно не следует автоматически из другого. Expected строится из independently provided record/allocation/context, не presented proof. Исторический source plan не обязан равняться текущему consumption plan. Recovery reconstruction не новое spending permission.

Конкретные тесты: TEST_RESULTS.json TestIDs R0F-BALANCE-TRACE/MIGRATE-*/EXACT-REPLAY/ALTERED-REPLAY/PROJECTED-NOT-ACTUAL/SMALL-ONLY/ABSOLUTE-FAR/TRANSITION-A/B/C/BUCKET-PERMUTATION. Их scope — fixture algebra/encoders, не production money model.
''')
 lines=['# R0F — immutable Economic Ledger identity','',HEAD,'Source: Include/Money/HSBI_EconomicLedgerTypes.mqh:6–12; Docs08; C3 R1_READINESS.','', 'Logical source key=(Broker,Server,AccountLogin,DealTicket), independently sourced. Payload SchemaVersion не создаёт новый экономический источник; unknown schema UNAVAILABLE. Physical codec/key version не повод для двойного funding одного logical deal. Symbol/Magic/Cycle не часть key: их изменение при прежнем source должно конфликтовать, а не создавать новый grant.','', 'Профиль HSBI-EA-ECON-1 — attributed EA source. Manual/unknown magic0/cycle-less deals остаются economic observations для будущего полного account ledger, но не получают EA attribution по умолчанию. Этот узкий профиль не доказывает global account funding. Origin IDs/role/plan берутся из independent EA association journal, не comment/current terminal. Broker company display name сам по себе не является стабильным BrokerIdentity; provider binding требует evidence.','', 'Receipt/correction/provenance verification envelopes отдельно от immutable body: повторное чтение тех же фактов с новым observation receipt не переписывает body. Corrected broker facts →CONFLICT для старого source и отдельный linked correction contract; никаких silent replace/NEW credit. SourcePlanApplicable/SourcePolicyApplicable=false требует доказанного NOT_APPLICABLE, не маскирует unknown.','', '| Field | Type | Key | Immutable | Authority | Migration |','|---|---|---|---|---|---|']
 for r in matrix['EconomicFields']:lines.append('| '+r['Field']+' | '+r['ExactType']+' | '+str(r['SourceKey'])+' | yes | '+r['Authority']+' | '+r['Migration']+' |')
 lines+=['','Каждое поле обязательно в DTO; conditional origin ID может быть None только при verified NOT_APPLICABLE. Missing/invalid type REJECT; unknown required units/origin/schema UNAVAILABLE. Raw finite doubles сохраняются как наблюдённые значения с явно proposed Z-zero equivalence в двух codec-кандидатах; это не неизменённый broker network packet. Exact raw-byte packet, если нужен, хранится separately unchanged под independent receipt. No epsilon/DoubleToString8 для equality. Mutable valid/reconciliation flags не входят в immutable equality и не создают authority.','', 'Same logical key + exact approved semantic payload =>NO_OP/zero delta; changed Profit/Commission/Swap/Fee/volume/price/role/time/units/EA origin =>CONFLICT даже при Net50. Foreign logical namespace =>NEW_IDENTITY_ONLY, не grant authorization. Кодек неизвестен или нет approved cross-version mapping =>UNAVAILABLE. Current ActorCycle/Plan/Revision/Snapshot не подставляются в historical source.','', 'Serialization: fixed field order в CONTRACT_MATRIX и CODEC_GOLDENS; field type/length tags disjoint. Full native canonical decoder ещё NOT_RUN; Python fixture decoders только проверяют known golden payloads. R1.1 минимальный scope не вправе объявлять legacy serializer authoritative. Reconciliation независимых broker components/posted net — отдельный слой, не source-key validation.']
 write('Docs/NEXT_STAGE_02B_R0F_ECONOMIC_IDENTITY_SPEC_RU.md','\n'.join(lines))
 write('Docs/NEXT_STAGE_02B_R0F_NUMERIC_CODEC_OPTIONS_RU.md','# R0F — numeric architecture и два codec-кандидата\n\n'+HEAD+'''| Representation | Exactness / domain | Overflow / rounding | Broker/MQL compatibility | Complexity / migration / tests |
|---|---|---|---|---|
| double boundary | Точное наблюдаемое finite binary64 значение, не истинный decimal posting | Не использовать double balance aggregation/epsilon; native conversion verified отдельно | MQL double внешний API; broker internal decimal неизвестен | Raw capture/equality only; finite/subnormal/zero vectors |
| integer minor units | Exact settled sum на известной currency/grid | Signed64 checked до операции, currency scale отдельно | long естественный кандидат, предел не брокерский account limit | Низкая арифметическая сложность, migration требует posted receipts |
| fixed-point explicit scale | Exact при общем проверенном scale | Scale multiplication/intermediates могут overflow | MQL feasible с checked/wide code после approval | Выше сложность; explicit domain/refusal/native vectors |
| exact rational reference | Математически точные суммы/множители | Arbitrary integer coefficients; не MQL native domain | Только независимый oracle | Нельзя переносить Fraction как production architecture |
| immutable raw source codec | Сохраняет observed components/IDs, отдельно от posted money | Никакого financial rounding | Два кандидата ниже, native evidence NOT_RUN | Versioned keys/compatibility; legacy four-field string недостаточна |

## A: HSBI-T17Z-1

Header `HSBI-T17Z-1` + LF, фиксированный schema field order. Имена и значения tagged: s<byteLength>:<UTF8>, i<byteLength>:<canonical integer>, d<byteLength>:<canonical scientific17>, b0/b1, n0:. Raw float — ровно1 digit перед точкой,16 после, e±DDD; finite binary64 roundtrip, zero нормализуется к+0 (Z). UTF8 exact, без NFC/casefold, без NUL; length — bytes, не StringLen characters. Record names закрыты, отсутствие/trailing/unknown data при production decode запрещены.

Технический MQL путь: StringToCharArray(CP_UTF8), integer formatting, DoubleToString scientific + canonical exponent formatting ONLY после подтверждения полного golden профиля и roundtrip. Если встроенный formatter не даёт точно предписанный token, нужен проверенный decimal-digit adapter в Extended scope либо UNAVAILABLE; нельзя объявлять любую roundtrip строку canonical. Large/small/subnormal/ties требуют native acceptance. Полностью deterministic decimal digit routine технически реализуема, но в R0F не пишется в production.

## B: HSBI-F64Z-1

Header `HSBI-F64Z-1` + NUL; те же names/order. s + uint32 byte length + UTF8; u+uint64 для nonnegative integers, i+signed64 для negative; b0/b1; n; d+8-byte finite64 big-endian. DTO schema отдельно ограничивает AccountLogin/Magic/Timestamp long и tickets ulong. Raw float bits можно реконструировать арифметически без union/unsafe casting: нормализовать finite x точными *2,/2 в [1,2), получить52 fraction bits, exponent/sign; subnormal масштабируется в integer fraction. Лимиты1023/1074 и53 significant bits следуют из binary64, не тестовых денег. В MQL нужны checked ulong shifts и проверенный native IEEE/subnormal режим. Golden mismatch отключает codec как UNAVAILABLE. Reference implementation использует этот алгоритм, independent oracle — struct.pack и literal hex.

B рекомендуется рассмотреть для raw source, но NUMERIC_CODEC_SELECTED=NO. Две формы не совпадают bytewise; совместимость — approved decoded semantic identity в одинаковой schema/zero equivalence, а не сравнение произвольных wire hashes. Unknown codec/schema/cross-version mapping UNAVAILABLE. Digest не становится broker authority.

Z-профили оба считают -0 и+0 эквивалентными. Если требуется bit-exact negative-zero preservation, эти профили не подходят без отдельного утверждённого native raw-bit capture profile; не выдавать canonical observations за неизменённый network packet. NaN/Infinity/float overflow отвергаются. Native string resource cap/array length нужно утвердить отдельно; wire uint32 length не обещает поддержать4GB в MQL. Decode до allocation проверяет approved bounds, duplicate/unknown fields, exact lengths, no trailing bytes.

## Settled conversion и ограничения

Нет raw float→posted minor units без independent posted amounts и verified broker policy. ROUND_HALF_EVEN — вариант локальной policy после verification, не универсальный брокерский закон. .005+.005 при component-rounding digits2 может дать0, aggregate-rounding1cent; нельзя выбрать по удобству. Account money digits не Symbol price digits.

G<=INT64_MAX, C/R/F>=0, G=C+R+F: при0<x<=F операции C+x/R+x не превышаютG; release ограничен owner reservation. Поэтому trusted balance transitions замкнуты без overflow. Произвольный signed sum components требует wider accumulator либо проверки каждого intermediate: MAX+MAX-MAX-MAX имеет final0, но naive long addition уже overflow. Checked(sum) Python big ints не переносится как sum-then-check MQL. Source raw float/sub-unit projected loss не округляется ради положительного proof.

Golden vectors: CODEC_GOLDENS.json и literal `hsbi_02b_r0f_independent_fixtures.py:GOLDENS/TEXT_LITERAL`, TEST_RESULTS R0F-CODEC-*. MQL5_COMPILE/MQL5_TESTS=NOT_RUN; fixture encoders не являются принятым production codec и не доказывают untrusted byte decoder.
''')
 graph=['# R0F — граф зависимостей','',HEAD,'Approval definitions и runtime evidence — разные DAG. Schema можно проверить offline, но observed record требует independent facts. Статус каждого runtime узла — PROPOSED/UNPROVEN либо FINITE_REFERENCE_ONLY, не IMPLEMENTED.','', '```mermaid','flowchart TD']
 graph += ['  '+u+' --> '+v for u,v in decisions.EVIDENCE_EDGES];graph+=['```','', 'OriginAssociationEvidence — prior EA origin journal, отдельный от будущего MoneyConsumptionJournal. PriorCommittedFundingIndex_t — внешний доказанный input; MoneyConsumptionJournal формирует NextFundingIndex_t1. Нельзя рисовать одну и ту же mutable funding state входом и выходом одного атомарного proof и объявлять круг доказанным. Следующий шаг использует t+1 как новый prior state, не текущий self-authority.','', 'Основной путь: Broker Evidence→Raw/Attributed Economic Identity→Reconciliation→Allocation Identity→Conservation→Durable Money Journal→Available Reserve→Catch-Up/NewFar. Отдельные branches: approved schemas, currency/posted receipts, origin association, snapshots, broker risk/margin/geometry, global debit attribution. Projected FutureSmall proof не создаёт ActualAvailable и не используется для собственного funding.','', 'Матрица содержит отдельный topological order для16 approval definitions и runtime graph. D01 definition не зависит от legacy adapter; BALANCE-SCHEMA-MAPPING зависит от D01, поэтому нет ложного цикла. Native primitive-domain evidence не зависит от выбранного codec; совместная проверка происходит позже на acceptance gate. Все реальные broker/durable/concurrent/NewFar dependencies остаются UNPROVEN.']
 write('Docs/NEXT_STAGE_02B_R0F_DEPENDENCY_GRAPH_RU.md','\n'.join(graph))
 lines=['# R0F — будущий R1.1: два точных scope','',HEAD,'R1_1_START_ALLOWED=NO. В R0F production code/helpers не создаются. Единственный действующий allowlist сейчас — новые Docs/Reports/Tests.','', 'Baseline inventory production references: HSBI_EconomicLedgerRecord/BuildSourceDealKey/SameEconomicRecord/ClassifyEconomicDuplicate/SerializeEconomicRecord найдены в Include только в самом EconomicLedgerTypes.mqh. Это статический scope argument, не MetaEditor/ABI/runtime доказательство.']
 for variant in v:
  lines+=['','## '+variant['Variant'],'']+[k+': '+(json.dumps(value,ensure_ascii=False) if type(value) in (dict,list) else str(value)) for k,value in variant.items()]
 lines+=['','Minimal technically possible for local typed identity APIs in one existing header. It does not solve authoritative serialization, provider ingestion, account-wide funding, replay backend or actual migration. Existing int0/1/2 classifier cannot silently expose unavailable as NEW/NO_OP; typed V2 facade and legacy policy must be approved, otherwise scope remains blocked. Full source payload fields may make old callers/fixtures unavailable; no terminal defaults.','', 'Extended headers are NOT mathematically required for one-file equality; each is optional modularization: namespace isolates broker/account validation; codec isolates raw wire format and golden vectors; legacy adapter performs read-only mapping/quarantine. Every additional production path needs explicit allowlist approval. Any future real provider caller modification needs its own scope expansion; no hidden include changes.','', 'Forbidden both variants: other money/solver/geometry/runtime headers, main mq5, dispatch, OnTick/OnTradeTransaction trading, persistence backend, balance credits/consumption, automatic migration/corrections. Old HSB tests/evidence stay frozen; intentional schema incompatibility requires new scoped harness and classification, never editing old expectations to green.','', 'Stop criteria: unapproved schema/API/codec/equivalence, missing namespace/units/origin, file outside allowlist, remote/baseline dirty mismatch, unexplained mutations/runtime errors, native compile unavailable for acceptance. Rollback only separate reviewed revert, preserve records/schema, no reset/rebase/force or compensating trades. Concrete future criteria in R1_ACCEPTANCE_MATRIX.json.']
 write('Docs/NEXT_STAGE_02B_R0F_R1_IMPLEMENTATION_SPEC_RU.md','\n'.join(lines))
 lines=['# R0F — пакет16 административных решений','',HEAD,'Ни одна Recommendation не является AdministratorDecision. Утверждение возможно только отдельным явным решением администратора; пустое поле не согласие. ApprovalReadiness описывает готовность рассмотрения/внешние зависимости, не permission execution. D05 A/B/C и production codec не выбраны.','', 'Возможные решения администратора: утвердить конкретный выбранный текст/вариант с версией и границами; отклонить; вернуть на доработку. При изменении варианта требуется новая явная формулировка, не модификация frozen evidence.']
 for row in rows:
  lines+=['','## '+row['DecisionID'],'']+[k+': '+(json.dumps(v,ensure_ascii=False) if type(v) is list else str(v)) for k,v in row.items()]
 write('Reports/NEXT_STAGE_02B_R0F_ADMIN_APPROVAL_PACKAGE_RU.md','\n'.join(lines))
 write('Reports/NEXT_STAGE_02B_R0F_CONFLICT_RESOLUTION_RU.md','# R0F — реестр разрешения противоречий\n\n'+HEAD+'''| ConflictID | Старый источник/правило | Кандидат R0F | Что остаётся |
|---|---|---|---|
| BAL-GROSS | C3 request Gross=grant, R0E/C2 Gross-view=remaining | OriginalGrant и RemainingGross раздельно | D01/MAPPING approval; legacy ownership/units |
| MONEY-TYPE | Projected positive и actual деньги одной формой | Шесть disjoint money types/independent receipts | Provider/broker/runtime UNPROVEN |
| SMALL-ROLE | LevelMoney projected sum содержит Small | A Small residual; B explicit transfer | D03 не утверждён, production формула сохранена |
| FAR-METRIC | Incremental с baseline может быть меньшеabsolute | Absolute working forecast; incremental diagnostic | D04/baseline/native pricing proof |
| TRANSITION | C2 final signed loss не sticky/peak | Полные A/B/C, no default | Выбор D05 и reset/backend/ordered history |
| COST-STATUS | C2 survivor объявлен redundant на одном input | malformed pure fact CONFLICT vs unknown UNAVAILABLE | Новая fixture coverage; C2/C3 не меняются |
| CODEC | raw64/NFC старый proposal vs typed fixture | A/B explicit UTF8/no implicit normalization, Z equivalence | Native codec и zero policy approval |
| R1-SCOPE | Старый spec+2 helper headers vs C3 single file | Minimal inline vs explicitly Extended3 helpers | Admin scope/API choice; no headers created |
| ALLOCATION | Equal total игнорирует bucket vector | Immutable grant vector отдельно от consumed state | L02 production остаётся открытым |
| FUNDING | Source-local cap != account economic funding | Explicit scope; full account all roles/external debits required | Backend/global data UNPROVEN |

Структурные противоречия сформулированы непротиворечиво в candidate profile; это не означает их административного разрешения. CONTRACT_CONFLICTS_RESOLVED не YES: D05, codec, actual domain, scope и approvals остаются открыты. Никакой proposed профиль не переписал действующий historical норматив или acceptance status.
''')
 write('Reports/NEXT_STAGE_02B_R0F_MUTATION_STATUS_GAP_RU.md','# R0F — формальный status contract и C3 gap\n\n'+HEAD+'''Source: frozen C2 `cost_coverage` и `C2-MUT-cost-shape-caller`; новые фактические outcomes — STATUS_GAP.json. Минимальный input: independent fact OverlapKnown=1 (int), все claim поля нормальны. Positive control COVERED в original/mutant. Pure original CONFLICT, mutant UNAVAILABLE; authorize/apply оба REJECT, zero deltas и input unchanged. Это status coverage gap, не unsafe spend и не глобально избыточный guard.

| API / факт | Outcome | State |
|---|---|---|
| Pure cost malformed/противоречивый authoritative fact | CONFLICT | Pure/zero delta |
| Pure cost authority отсутствует или overlap неизвестен | UNAVAILABLE | Pure/zero delta; не known zero |
| Spending request malformed/неразрешён | REJECT | zero balances/journal/revision delta |
| Changed known event payload/source immutable conflict | CONFLICT | zero delta |
| Независимая history/provider недоступна | UNAVAILABLE | zero delta |
| Exact verified receipt/payload | NO_OP | zero delta, не новое eligibility |

Обязательные callers: direct cost_coverage; authorize->_authorize; apply_for_test->authorize. Public spending prevalidation предотвращает этот malformed fact до pure helper. Она не заменяет самостоятельный direct-helper status contract. R0F candidate cost_status сначала проверяет формы/точные bool types, затем различает malformed и unknown. Это новый test-only профиль, не исправление C2/C3.

Будущий план: в новом versioned test-only suite добавить independent OverlapKnown1 и complete/unknown controls; повторить exact source mutation; сохранить old C2/C3 rows и новую классификацию отдельно; не утверждать redundant по одному bool-policy input. Любое дальнейшее production изменение требует отдельного approved scope. Tests R0F-COST-malformed/unknown/known и STATUS_GAP.json не используют evaluator как expected.
''')
 write('Reports/NEXT_STAGE_02B_R0F_VERIFICATION_RU.md','# R0F — фактическая проверка\n\n'+HEAD+f'''Новые candidate scenarios={tests.get('Scenarios','NOT_RUN')}, PASS={tests.get('Pass','NOT_RUN')}, FAIL={tests.get('Fail','NOT_RUN')}, infrastructure={tests.get('InfrastructureErrors','NOT_RUN')}. Expected — literal vectors, independent struct packing/fixture decoders и signed integer units, не проверяемый evaluator. Raw codec scalar expectations включают17-digit text и IEEE hex, whole record A/B, zero/subnormal/maxfinite. Fixture decoders работают только на known goldens, не подтверждают hostile-stream/native parser.

C3 status={verification.get('C3EvidenceStatus','NOT_RUN')}; его обязательные archived artifacts/hashes проверены exact Git archive. Полный C3 reference/mutation suite повторно NOT_RUN; это не новый запуск76/70/58. Отдельно свежий original/mutant status gap воспроизведён по literals. Fresh frozen R7/02B-R0: {[(r['ID'],r['PassCount'],r['FailCount'],r['ExitCode']) for r in verification.get('Runs',[])]}; baseline match={verification.get('RegressionBaselineMatch','NOT_RUN')}. Исторический FAIL остаётся FAIL. Commands, timestamps, hashes, stdout/stderr и scopes — VERIFICATION.json. TEST_RESULTS содержит complete balance traces; CODEC_GOLDENS — независимые expected.

Consistency tests проверяют16 unique IDs, пустые admin decisions, allowed readiness statuses, no selected D05/codec,29 immutable fields, acyclic approval/runtime graphs, fixed one-file Minimal и отдельно Extended, no production helpers/runtime changes. Evidence package verifier проверяет baseline Git bytes/blob/modes и new hashes. MQL5_COMPILE/MQL5_TESTS/STRATEGY_TESTER=NOT_RUN, не заменены Python.

Ссылки: CONTRACT_MATRIX/R1_ACCEPTANCE_MATRIX/ADMIN_DECISIONS в Tests/Contracts; package results и preservation в Tests/Evidence. Все production sources и исторические evidence сохранены. Runtime disabled/broker dispatch false подтверждаются source hashes и static no-trade scan. Никто не исполнял OnTick/OnTradeTransaction/broker requests.
''')
 ready=read('CONSISTENCY').get('ExitCode')==tests.get('ExitCode')==verification.get('ExitCode')==pkg.get('ExitCode')==0 and pkg.get('Positive')=='PASS'
 statuses=dict(BASE_SHA=a.BASE,FINAL_SHA='PUBLICATION_SHA_IN_FINAL_RESPONSE',REMOTE_SHA_PARITY='PUBLICATION_CHECK_IN_FINAL_RESPONSE',WORKTREE_CLEAN='PUBLICATION_CHECK_IN_FINAL_RESPONSE',PRODUCTION_FILES_UNCHANGED='YES_BASELINE_VERIFIED',ADMIN_DECISIONS_TOTAL=16,ADMIN_DECISIONS_PREPARED=16,ADMIN_DECISIONS_APPROVED=0,CONTRACT_CONFLICTS_RESOLVED='NO_ADMIN_CHOICES_PENDING',NUMERIC_CODEC_SELECTED='NO',ECONOMIC_IDENTITY_SPEC_READY='FOR_ADMIN_REVIEW',ALLOCATION_IDENTITY_SPEC_READY='FOR_ADMIN_REVIEW',R1_MINIMAL_SCOPE_READY='SPEC_PREPARED_APPROVAL_PENDING',R1_EXTENDED_SCOPE_READY='SPEC_PREPARED_APPROVAL_PENDING',MUTATION_STATUS_GAP_REVIEWED='YES',REGRESSION_BASELINE_MATCH='YES' if verification.get('RegressionBaselineMatch') else 'NOT_RUN',MQL5_COMPILE='NOT_RUN',MQL5_TESTS='NOT_RUN',ADMIN_APPROVAL_COMPLETE='NO',R1_1_START_ALLOWED='NO',PRODUCTION_REMEDIATION_ALLOWED='NO',TRADING_LOGIC_START_ALLOWED='NO',BROKER_DISPATCH_ALLOWED='NO',REAL_TRADING_ALLOWED='NO',STAGE_02B_R0F_COMPLETE='YES' if ready else 'NO')
 write('Reports/NEXT_STAGE_02B_R0F_FINAL_VERDICT_RU.md','# R0F — итог подготовки решений\n\n'+HEAD+'''Подготовлены16 конкретных ballots с alternatives/proof/counterexample/impact/dependencies/readiness. Их логические определения и независимые examples проверены; ни одна policy не APPROVED. Mathematical balance candidate и source/allocation identity сформулированы явно, но D05/codec/native domain/scope остаются выборами администратора. Numeric codec selected=NO. R1.1 не разрешён.

R0F COMPLETE — завершение decision preparation, не production readiness. Broker authenticity, posted policy applicability, global economic funding, durable/CAS/concurrency, actual fills и NewFar integration остаются UNPROVEN. Source key, raw codec или local equality не создают authority/available money. Self-consistent fixture/provider flag не заменяет broker history.

Publication SHA не встраивается в собственный commit; фактические Git parity/clean будут сообщены после push. После R0F остановиться.

[R0F_FINAL_STATUS]
'''+'\n'.join(str(k)+'='+str(value) for k,value in statuses.items())+'\n[/R0F_FINAL_STATUS]')
 print('R0F package documents generated; preliminary complete',ready)
if __name__=='__main__':main()
