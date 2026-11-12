"""DG01 decision preparation. No modifications to any historical or production file."""
import sys,re,json,subprocess,hashlib
import HSBI_DG01_common as a
R=a.ROOT
NATIVE={
'FSA-001':['E1-EXACT','E1-PROFIT','E1-SWAP','E1-COMMISSION','E1-FEE','E1-SAME-NET','E1-MAGIC-NOT-NEW-SOURCE','E1-FOREIGN-AUTHORITY','E1-UNKNOWN-PROVENANCE','E1-CANONICAL-ZERO','E1-NONFINITE'],
'FSA-002':['E2-VECTOR-EXACT','E2-SAME-TOTAL'],
'FSA-003':['E2-BOUND-SOURCE','E2-FOREIGN-ALLOCATION','E2-UNKNOWN-AUTHORITY'],
'FSA-004':['E2-ALREADY-CONSUMED','E2-DUPLICATE-CONSUMPTION'],
'FSA-005':['E3-RISK-VALID','E3-NAN-MARGIN','E3-NEGATIVE-MARGIN'],
'FSA-006':['E3-TX-VALID','E3-NAN-FILL','E3-PARTIAL','E3-OWNERSHIP','E3-MISSING-CONFIRMATION'],
'FSA-007':['E2-NEGATIVE-BUCKET','E2-OVERALLOCATION'],
'FSA-008':['E3-INFINITY-MONEY'],
'FSA-009':['E4-ONE-FAR','E4-DISTINCT-FAR-SLOTS','E4-ALIAS-OBSERVATION'],
'FSA-010':['E4-INDEPENDENT-EXPECTED','E4-COPIED-EXPECTED','E4-MISSING-PROVIDER','E4-UNKNOWN-SOURCE']}
PLANS=[
('FSA-001','Добавить versioned source-key/full-payload API; старую struct/signatures сохранить. Это local API, не полное remediation.','D-02,D-08,NUM-CODEC,MQL-DOMAIN','Расширение новой economic record; independent provider; callers','Include/Money/HSBI_EconomicLedgerTypes.mqh','ONE_FILE_LOCAL_API_FEASIBLE','Старые записи без Broker/Server/Account/EA-origin не конвертировать автоматически; quarantine.','Старый classifier остаётся unsafe, пока не ограничен diagnostic policy и не мигрированы все financial consumers.'),
('FSA-002','Сравнивать полный immutable bucket vector и allocation identity, а не общую сумму; mutable consumed отделить.','D-01,D-08','Локальный comparator + schema/caller contracts','Include/Money/HSBI_AllocationLedgerTypes.mqh','LOCAL_AFTER_CONTRACT_APPROVAL','Старый total не восстанавливает утраченное назначение buckets.','Global source allocation sum требует separate source registry; local vector equality этого не доказывает.'),
('FSA-003','Сверять consumption sourceDealKey/sourceAllocationKey с authoritative source и его неизменным event/policy.','D-07,D-08,FUNDING-GLOBAL-ATTRIBUTION','Локальная binding проверка + mandatory caller/provider','Include/Money/HSBI_ReserveCatchUpEvaluator.mqh; Include/Money/HSBI_ReserveAllocationTypes.mqh','LOCAL_GUARD_ONLY_GLOBAL_DEPENDENCY','Legacy keys без namespace нельзя считать подтверждёнными allocation.','Даже согласованные строки caller не доказывают независимую authority; journal/global state обязательны.'),
('FSA-004','В обеих ветках использовать reconciled remaining eligible source; exhausted source не даёт нового grant.','D-01,D-02,D-07,FUNDING-GLOBAL-ATTRIBUTION','Global ledger + persistence/CAS + вызывающий модуль','Include/Money/HSBI_ReserveCatchUpEvaluator.mqh; future global source funding provider (not authorized)','MULTICOMPONENT_REQUIRED','Пересчитать только из complete history и immutable funding journal, не из текущей projected прибыли.','Локальный alreadyConsumed check устраняет пример, но не duplicate across allocations/restart/concurrency.'),
('FSA-005','Проверять finite/domain всех используемых risk inputs и limits до сравнения. Unlimited/no-margin моделировать явно, не NaN/Infinity.','MQL-DOMAIN','Локальный DTO guard + согласование producers','Include/Risk/HSBI_RiskGateResult.mqh; Include/Risk/HSBI_NewFarGateTypes.mqh','LOCAL_AFTER_DOMAIN_APPROVAL','Не нормализовать неизвестный risk в0; текущие snapshots переоценивать независимо.','Некорректная risk formula или stale provider не исправляются конечностью чисел.'),
('FSA-006','Finite положительный expectedVolume, finite accumulatedVolume, actual deal/position confirmation; partial не COMPLETE.','D-08,MQL-DOMAIN','Локальный barrier + event producer/reconciliation','Include/Execution/HSBI_TransactionTypes.mqh; Include/Execution/HSBI_ExternalOutcome.mqh','LOCAL_GUARD_PLUS_CALLERS','Старые COMPLETED без actual deals требуют reconciliation, не автоматического повторения.','Out-of-order/partial fills и transaction costs требуют complete history и event engine.'),
('FSA-007','Nonnegative finite buckets; отдельные PREPARED/COMMITTED инварианты, source<=0 не распределяется как harvest.','D-01,D-02','Локальный validator + phase schema + callers','Include/Money/HSBI_AllocationLedgerTypes.mqh','LOCAL_AFTER_PHASE_CONTRACT','Legacy Remaining/available не считать Free без Reserved/Consumed/owner mapping.','Локальный sum equality не доказывает global uniqueness/actual source.'),
('FSA-008','Finite денежные компоненты; explicit valid/revision contract для spending. RealizedCycleNet может быть отрицательным; inactive init не spendable.','BALANCE-SCHEMA-MAPPING,MQL-DOMAIN','Локальный shape guard + spender mandatory caller','Include/Money/HSBI_MoneyState.mqh','LOCAL_AFTER_SCOPE_CLARIFICATION','Инициализационный revision0 не превращать в funded state; unknown state UNAVAILABLE.','valid/revision semantics остаются отдельным contract question; Infinity defect подтверждён независимо.'),
('FSA-009','Контроль role-slot и уникальных actual FAR identifiers во всех слотах; отличать alias reference от двух различных позиций.','D-08,active-role/slot policy','Context schema + invariants + диагностические/торговые callers','Include/Core/HSBI_Context.mqh; Include/Core/HSBI_Invariants.mqh; Include/Core/HSBI_Roles.mqh; Include/Diagnostics/HSBI_Diagnostics.mqh','MULTICALLER_REQUIRED','Не угадывать owner/slot по comment. Aliases допустимы только после явного slot contract; не считать candidate реальным Far без fills.','Одна исправленная count-функция не закрывает другие count/slot callpaths.'),
('FSA-010','Сохранить local equality, убрать self-confirmed expected из решения о происхождении; supplied expected должен приходить из independent provider.','D-02,D-08,NUM-CODEC','Independent provider + reconciliation + caller integration','Include/Planning/HSBI_NewFarSolver.mqh; future independent provider boundary (not authorized)','BLOCKED_BY_PROVIDER','Старый proof без source receipt не подлежит автоматическому подтверждению.','UNIMPLEMENTED authority boundary; полный NewFar bypass не доказан. Helper acceptance copied expected — наблюдение, не authentication.')]
DECISION_NOTES={
'D-01':('READY_FOR_ADMIN_DECISION','G=C+R+F; RemainingGross=R+F; Available=F только после complete reconciliation/journal.','G50,C10,R15,F25: RemainingGross40,Free25. Подмена Free на40 завышает spending на15.',['FSA-002','FSA-004','FSA-007','FSA-008']),
'D-02':('READY_FOR_ADMIN_DECISION','Шесть денежных типов не взаимозаменяемы; каждый переход требует independent source/posted/policy/journal boundary.','Projected100, фактических deals нет → AvailableReserve не100; при неизвестной history UNAVAILABLE, не0.',['FSA-001','FSA-004','FSA-010']),
'D-03':('READY_FOR_ADMIN_DECISION','Small-only positive → ResidualHeld; transfer только отдельным approved policy/event.','Core0,Trend0,Small10 → BigReserve0,ResidualHeld10.',['FSA-004','FSA-019']),
'D-04':('READY_FOR_ADMIN_DECISION','AbsoluteFarLoss рабочий кандидат; Incremental только отдельная диагностика с независимым basis.','Absolute50,baseline40,reserve30: incremental10 покрыт, absolute margin=-20.',['FSA-015']),
'D-05':('CONTRACT_CONFLICT','Владелец выбирает current signed loss, sticky breach либо peak historical loss; выбор здесь не сделан.','Fills-15,+100,cap12: A loss15→0; B breach true→true; C peak15→15.',['FSA-006','FSA-015']),
'D-06':('INSUFFICIENT_EVIDENCE','Каждый обязательный cost покрывается ровно один раз по independent basis/window; unknown overlap не безопасный0.','Ask101→Bid110 уже даёт9; вычет того же spread1 даёт8 только при доказанном совпадении cost basis.',['FSA-019']),
'D-07':('READY_FOR_ADMIN_DECISION','Global source funding journal + immutable replay + atomic durable commit/CAS; локальная idempotency не exactly-once backend.','Две allocations используют source50 по30: local budgets проходят, общий debit60>50.',['FSA-003','FSA-004','FSA-013','FSA-027']),
'D-08':('READY_FOR_ADMIN_DECISION','SourceKey=(Broker,Server,Account,Deal), full immutable body; NEW identity не funding; unknown facts UNAVAILABLE.','Profit50/Commission0 и Profit60/Commission-10 при одном source → CONFLICT, несмотря на Net50.',['FSA-001','FSA-002','FSA-003','FSA-009','FSA-010']),
'CR-09':('BLOCKED_BY_DEPENDENCY','Явно выбрать ALL_LEVEL либо SINGLE_LEVEL scope; all-level требует minMargin>0 по каждому required level.','T1=10,margin1=9;T2=5,margin2=-11: worst-transition не worst-catchup.',['FSA-015']),
'NUM-EXACT-1':('READY_FOR_ADMIN_DECISION','Exact settled money representation; projected risk не округляется до безопасного0.','Reserve1e28,два расхода.01 требуют точный decrement.02; arbitrary Decimal context не доказательство.',['FSA-005','FSA-006','FSA-007','FSA-008']),
'NUM-DOMAIN-1':('INSUFFICIENT_EVIDENCE','Явный supported currency/precision/range и отказ за domain; unlimited Fraction не MQL domain.','INT64_MAX+1 выходит за signed64; float IDs после2^53 теряют различие.',['FSA-005','FSA-006','FSA-022']),
'NUM-CODEC':('INSUFFICIENT_EVIDENCE','F64Z рекомендуется как candidate raw captured codec; T17Z — альтернатива; native compatibility не подтверждена.','+0/-0 должны иметь явную Z policy; ulong9007199254740993 не проводить черезdouble.',['FSA-001','FSA-010','FSA-026']),
'SNAP-FIXTURE-1':('READY_FOR_ADMIN_DECISION','Versioned strict schema+typed content+независимый receipt; fixture receipt не broker authenticity.','string1 и numeric1 не эквивалентны без явного schema codec; copied receipt не независим.',['FSA-010','FSA-021']),
'FUNDING-GLOBAL-ATTRIBUTION':('BLOCKED_BY_DEPENDENCY','Единый source-level inventory across allocations, roles и restarts; transfer/reversal отдельными событиями.','Перестановка Magic/Cycle не создаёт новый broker deal и новую прибыль.',['FSA-001','FSA-003','FSA-004','FSA-013']),
'MQL-DOMAIN':('INSUFFICIENT_EVIDENCE','Native long/ulong/double/UTF8, overflow, finite-only и codec goldens обязательны до acceptance.','NaN делает оба ordered comparisons ложными; revision ULONG_MAX+1 требует stop.',['FSA-005','FSA-006','FSA-008','FSA-022','FSA-026']),
'BALANCE-SCHEMA-MAPPING':('BLOCKED_BY_DEPENDENCY','Legacy Remaining мигрирует только при известном gross/free/consumed/reserved/owner/currency mapping.','Remaining40,Reserved15 означает Free25, а не40; при неизвестном owner migration UNAVAILABLE.',['FSA-007','FSA-008','FSA-013'])}

def doc(name,text,folder='Docs'):(R/folder/(a.TAG+name+'_RU.md')).write_text(text.rstrip()+'\n')
def build():
 old=a.strict(R/'Tests/Contracts/HSBI_FULL_SYSTEM_AUDIT_02_DEFECT_MATRIX.json')['Rows'];formula=a.strict(R/'Tests/Contracts/HSBI_FULL_SYSTEM_AUDIT_02_FORMULA_REVIEW.json');issues=[]
 for x in old:
  current=a.sha(R/x['Source']['File']);assert current==x['Source']['SHA256'],x['ID'];issues.append(dict(DefectID=x['ID'],Severity=x['Severity'],Classification=x['Classification'],Source=x['Source'],NormalizedDefinitionLines=next(z['DefinitionLines'] for z in a.load('SOURCE_REFERENCE_REVIEW')['Rows'] if z['DefectID']==x['ID']),HistoricalClassificationPreserved=True,ReviewBoundary='No new reclassification; original source/hash and formatted presentation checked'))
 assert len(issues)==29 and len(formula['Rows'])==49
 for f in formula['Rows']:
  if f['CurrentSourceSHA256']:
   path=f['Source'].rsplit(':',1)[0];assert a.sha(R/path)==f['CurrentSourceSHA256'],f['FormulaID']
 a.save('BASELINE_REVIEW',dict(UTC=a.now(),Defects=issues,FormulaCount=49,FormulaCounts=dict(ConditionalMathematics=23,Conflicts=11,Unverified=15),OldIntegrityRecheck=a.load('AUDIT02_INTEGRITY_RECHECK')['ExitCode'],OldScopeFailure=a.load('AUDIT02_PACKAGE_RECHECK')['ExitCode'],Note='Frozen CLI rejects new DG01 scope, exit1 retained. Unchanged checker API baseline=False validates archived graph only; independent current Git inventory covers all1464 files. No old classification changed.'))
 previous=a.strict(R/'Tests/Contracts/HSBI_FULL_SYSTEM_AUDIT_02_DECISION_MATRIX.json')['Rows'];decisions=[]
 for ordinal,p in enumerate(previous,1):
  did=p['DecisionID'];status,recommend,example,depends=DECISION_NOTES[did]
  decisions.append(dict(DecisionID=did,DisplayOrdinal='D-%02d'%ordinal,CanonicalIDPreserved=True,SourceContract=p['CurrentContract'],Conflict=p['Conflict'],PreferredSemantics=recommend,Alternatives=p['AlternativeChoice'] if did!='D-05' else ['A: current loss=max(0,-cumulative signed net)','B: sticky flag until separately authorized reset','C: peak=max historical prefix loss'],MathematicalJustification=p['MathematicalJustification'],Counterexample=example,DependentDefects=depends,ProductionModules=sorted({x['Source']['File'] for x in old if x['ID'] in depends}),RequiredTests=['Positive/negative literal vectors','Immutable source/identity changes','Zero deltas on reject/no-op','Per-guard causal mutation where implemented'],RequiredNativeEvidence='MetaEditor compile + isolated script actual logs; codec/native integers goldens for relevant contracts. Backend/broker/durable/concurrent evidence separate.',MigrationRisk=p['MigrationImpact'],StopConditions=['Unknown namespace/units/origin/legacy','Unapproved dependent policy','Native or independent provider evidence missing at implementation acceptance'],ApprovalRequired=True,ReadinessStatus=status,ApprovalStatus='AWAITING_ADMIN_APPROVAL',AdministratorDecision='',ShortBallot='Утвердить/отклонить/вернуть на доработку: '+recommend,ImplementationReadiness='NO_PRODUCTION_PERMISSION'))
 for row in decisions:
  if row['DecisionID']=='D-05':
   row['TransitionPolicyComparison']=[dict(Policy='A_CURRENT_SIGNED',AfterFill1Loss=15,AfterFill2Loss=0,NewAction='Current loss gate may re-evaluate after positive fill, but no automatic FSM resume',History='Complete signed batch fills and costs',Reset='Metric recomputed; safety stop policy separate'),dict(Policy='B_STICKY_BREACH',AfterFill1Breach=True,AfterFill2Breach=True,NewAction='Blocked until explicitly approved reset',History='Ordered prefixes plus durable breach/reset events',Reset='Owner-defined reset authority/scope'),dict(Policy='C_PEAK_LOSS',AfterFill1Loss=15,AfterFill2Loss=15,NewAction='Cap12 remains breached',History='Complete ordered prefixes',Reset='Explicit metric window/cycle reset policy')]
   row['MigrationRisk']='Final cumulative Net85 cannot reconstruct earlier breach15. Missing ordered history/reset journal => UNAVAILABLE for sticky/peak migration; do not infer no breach.'
   row['RequiredNativeEvidence']='Confirmed batch membership, ordered partial fills, component costs, restart preservation of selected metric and reset authority; no policy selected here.'
 a.save('DECISION_MATRIX',dict(BaseSHA=a.BASE,IDMapping='Historical canonical IDs retained; DisplayOrdinal D-01..D-16 is NOT a renaming. D-09=CR-09, D-10..D-16 named NUM/SNAP/FUNDING/MQL/BALANCE choices.',Rows=decisions),'Tests/Contracts')
 plans=[]
 for did,candidate,contracts,kind,scope,ready,migration,remaining in PLANS:
  d=next(x for x in old if x['ID']==did)
  plans.append(dict(DefectID=did,CurrentSource=d['Source'],ConfirmedFailure=d['Actual'],Classification=d['Classification'],RootCause=d['Actual'],RequiredContract=contracts.split(','),MinimalChangeCandidate=candidate,DependencyGraph=['Independent facts/contracts',kind,'Mandatory caller integration','Native/regression acceptance'],RequiredNativeTests=NATIVE[did],RequiredRegressionTests=['Frozen AUDIT02 source positives/negatives','R0/R7 failures retained','Local source/key/vector/shape altered input tests','Full caller integration after separate scope approval'],MigrationRisk=migration,RemainingRisk=remaining,ProductionScope=scope,ApprovalRequired=True,ReadinessStatus=ready,CurrentImplementationAllowed=False))
 a.save('P0_REMEDIATION_MATRIX',dict(Rows=plans,CompleteLocalFixNotImplied=True),'Tests/Contracts')
 nativepaths=[p for p in (R/'Tests/Native').glob('HSBI_DG01_*') if p.suffix in ('.mq5','.mqh')]
 text='\n'.join(p.read_text() for p in nativepaths);native_ids=[n for n in re.findall(r'DGCheck\("([^"\n]+)"',text) if n!='E1-FIELD-']
 for name in ['zero','negative-zero','one','negative-five','tenth','min-normal','min-subnormal','max-finite']:
  native_ids.extend('E5-'+name+suffix for suffix in ['-bits','-roundtrip','-T17-probe'])
 native_ids.extend('E1-FIELD-'+name for name in ['SchemaVersion','Broker','Server','AccountLogin','Symbol','Magic','CycleID','DealTicket','OrderTicket','PositionIdentifier','ActionID','EventID','Role','EntryType','DealType','TimestampMsc','Volume','Price','Profit','Swap','Commission','Fee','DealNet','Currency','Precision','SourcePlanApplicable','SourcePlan','SourcePolicyApplicable','SourcePolicyVersion'])
 assert len(native_ids)==len(set(native_ids))
 searches=[a.run(['which',n]) for n in ['metaeditor64','metaeditor','MetaEditor64.exe','terminal64','wine','pwsh']]
 searches.append(a.run(['rg','--files','/opt','/workspace','/usr/local/bin','-g','*[Mm]eta[Ee]ditor*','-g','*terminal64*']))
 sources={str(p.relative_to(R)):a.sha(p) for p in nativepaths+[R/'Tests/Reference/HSBI_DG01_identity_candidate.mqh',R/'Tests/Reference/hsbi_02b_r0h_native_codec.mqh']}
 native_rows=[dict(TestID=tid,SubjectSHA256=sources,RunnerSHA256=a.sha(R/'Tests/Native/HSBI_DG01_harness.mq5'),Input='Literal native fixture in harness/codec_cases; generated independent scalar/record goldens for E5',Expected=dict(AssertionTrue=True,Scope='Literal native predicate; current source defects/proposed API/codec probe separately labelled in source'),Actual=None,Status='NOT_RUN',ExitCode=None,Environment='No MetaEditor/MT5/Wine/pwsh found in PATH/searched directories',ExecutionTimeUTC=None,ProofBoundary='Prepared native cases; no compile or runtime result') for tid in sorted(native_ids)]
 a.save('NATIVE_RESULTS',dict(BaseSHA=a.BASE,UTC=a.now(),MQL5_COMPILE='NOT_RUN',MQL5_NATIVE_TESTS='NOT_RUN',NATIVE_VERIFIED=False,PowerShellLauncherExecution='NOT_RUN',Searches=searches,Rows=native_rows,CaseCount=len(native_rows),NativePass=0,NativeFail=0,Scope='Generators GEN-NAN/GEN-INF must be independently confirmed at runtime; fixture-generation failure is infrastructure error, not risk-gate kill.'))
 acceptance=dict(BaseSHA=a.BASE,Rows=issues,Decisions=16,P0Plans=10,NativeRequiredIDs=sorted(native_ids),OneFileLocalAPIFeasible=True,OneFileCompleteRemediationFeasible=False,ProductionAllowlistCandidate=['Include/Money/HSBI_EconomicLedgerTypes.mqh'],MandatoryBeforeR1=['Explicit owner contract and compatibility approval','Separate implementation task','Native compile + per-field/codec actual logs before production acceptance','No addition of provider/funding/dispatch/persistence in local identity step','Fresh baseline and preservation checks'],NativeStatus='NOT_RUN',Approved=False,ApprovalGate='READY_FOR_ADMIN_DECISION',RuntimeGate='PARTIAL_NATIVE_PENDING')
 a.save('ACCEPTANCE_MATRIX',acceptance,'Tests/Contracts')
 # Current callsite inventory, not a claim about external or future consumers.
 symbols=['HSBI_BuildSourceDealKey','HSBI_ValidateEconomicRecord','HSBI_SameEconomicRecord','HSBI_ClassifyEconomicDuplicate','HSBI_SerializeEconomicRecord','HSBI_IsHarvestSourceEntry'];callers=[]
 for x in a.inventory():
  if x['Production']:
   for line,s in enumerate((R/x['Path']).read_text().splitlines(),1):
    if any(n in s for n in symbols):callers.append(dict(File=x['Path'],Line=line,Text=s,SHA256=x['SHA256']))
 a.save('CALLSITE_REVIEW',dict(Rows=callers,Scope='Lexical scan of all74 current production sources; external programs excluded. Current symbols appear only in header; old algorithms remain unsafe if future financial caller uses them.'))
 # Written representations consume the same canonical rows, with actual newlines.
 doc('CONTRACT_RESOLUTION','# DG01 — разрешение контрактов (предложения)\n\nВсе16 выборов остаются AWAITING_ADMIN_APPROVAL. Status readiness не равен approval. Исторические canonical IDs сохранены; отображаемые D-09..D-16 не подменяют CR/NUM/SNAP/FUNDING/MQL/BALANCE IDs.\n\n'+ '\n\n'.join('## '+d['DecisionID']+' ('+d['DisplayOrdinal']+')\n'+'\n'.join('- **'+k+'**: '+str(d[k]) for k in ['SourceContract','Conflict','PreferredSemantics','Alternatives','MathematicalJustification','Counterexample','DependentDefects','ProductionModules','RequiredTests','RequiredNativeEvidence','MigrationRisk','StopConditions','ReadinessStatus','ApprovalStatus']) for d in decisions))
 doc('P0_REMEDIATION_MATRIX','# DG01 — P0 remediation: только планы\n\nFSA-010 остаётся UNIMPLEMENTED independent authority; full solver bypass не объявлен. Local equality может проверить соответствие supplied expected, но не его происхождение. Обязательный будущий end-to-end тест: independent provider frozen, request+proof согласованно изменены → UNAVAILABLE/CONFLICT без списания; полный caller не обходит provider. Provider отсутствует/неполон → UNAVAILABLE.\n\n'+ '\n\n'.join('## '+d['DefectID']+'\n'+'\n'.join('- **'+k+'**: '+str(v) for k,v in d.items() if k!='DefectID') for d in plans))
 doc('MINIMAL_R1_1_DIFF_PLAN', '''# DG01 — точный неприменённый проект Minimal R1.1

ONE_FILE_LOCAL_API_FEASIBLE=YES_STATIC_CONDITIONAL
ONE_FILE_COMPLETE_REMEDIATION_NOT_FEASIBLE=YES
R1_1_START_ALLOWED=NO

## Что именно подготовлено

`Tests/Reference/HSBI_DG01_MINIMAL_R1_1_CANDIDATE.patch` — точный unified diff к baseline `92a55371299439f2ff33494497cde2aa78013d77`, только `Include/Money/HSBI_EconomicLedgerTypes.mqh`. Выполнен лишь `git apply --check`, код не применён. Test-only `HSBI_DG01_identity_candidate.mqh` содержит тот же добавляемый body, но включает старый header из Tests; package checker сверяет body и diff. Проект не является production helper.

Не меняются старый struct, имена, сигнатуры, equality/classifier/serializer и фактическое legacy поведение. Добавляются отдельная V2 struct29 immutable fields, известность facts mask как envelope metadata, enum NEW/NO_OP/CONFLICT/REJECT/UNAVAILABLE, shape validator, logical source-key equality, full immutable payload equality и pure classifier с независимыми authority+complete registry входами. Это не legacy migration и не новый funding path.

## Контракт API кандидата

EconomicEventID, AllocationEventID и ConsumptionEventID — разные namespaces: первое принадлежит immutable origin, второе allocation vector, третье consumption journal. Произвольное равенство между ними не требуется.

SourceKey=(Broker,Server,AccountLogin,DealTicket). Magic/Cycle/Symbol/Role входят в immutable body, а не создают новый источник. При одном key изменённые Profit/Swap/Commission/Fee/Net и прочие поля — CONFLICT; одинаковый Net не заменяет components. NEW означает только independently confirmed identity observation и отсутствие key в complete registry, не доступные деньги.

Captured finite binary64 equality точная, без epsilon; +0/-0 эквивалентны только в proposed Z profile. В reference journal event IDs уникальны в своих namespaces, а порядок применения задаётся expected revision, не численным возрастанием EventID. Это отличается от fresh transaction event sequence и требует явного mapping, не подменяет OnTradeTransaction порядок. Integer IDs никогда не проходят через double; long/ulong типы не требуют суммирования для comparator. Malformed/nonfinite → REJECT, unknown facts/schema/provider/registry → UNAVAILABLE. Никакого UNAVAILABLE→NEW. Декодер обязан проверять wire types до приведения: после преобразования bool→long MQL struct уже не хранит исходный wire tag.

`knownFieldsMask` нужен для missing/unknown facts, чтобы false/0 в initialized struct не означали доказанный факт. sourcePlanApplicable=false требует sourcePlan0; аналогично policy. Currency/precision — независимый account/provider fact, не SYMBOL_DIGITS. Digits0..8 и positive price/volume — **proposed supported profile**, не универсальные broker limits. Все29 field-equality probes подготовлены в native harness. Typed role/entry fields V2 ещё не имеют утверждённого mapping в string wire fields F64Z; это отдельный schema/codec вопрос. Codec сериализация в этом локальном API **не реализована**: pure equality не объявляется полным NUM-CODEC или broker reconciliation. F64Z/T17Z проверяются отдельным test-only subject; выбор и native реализация потребуют owner решения.

Validate проверяет shape/captured domain, не выполняет арифметическую брокерскую reconciliation DealNet из компонентов. Её выполняет независимый provider с declared posted/raw policy. Входной bool independentSourceConfirmed и registryComplete сами по себе не удостоверяют receipt; это обязательная граница caller/provider, не новый доказанный источник истины.

## Почему полного исправления в одном файле нет

Старый classifier намеренно остаётся с прежней небезопасной семантикой. Additive V2 не устраняет FSA-001 во всех возможных путях. В74 текущих production sources lexical scan нашёл старые economic symbols только в исходном header; external/future consumers не проверены. Чтобы объявить полное remediation, надо утвердить diagnostic-only legacy policy, проверить всех consumers и подключить independent namespace/origin provider + registry reconciliation. Глобальные funding/restart/durable/CAS невозможно получить из equality header. Каждый дополнительный production-модуль требует отдельного расширенного allowlist, не разрешён здесь.

## Acceptance, stop и rollback

До первого production изменения: явный ballot по D-02/D-08/MQL-DOMAIN/schema+compatibility; NUM-CODEC для serialization части; отдельное задание с новым baseline/allowlist. До acceptance: MetaEditor strict compile полного EA и isolated harness, full-field changes, signed components, namespace, unknown legacy, nonfinite, zero policy, overflow/UTF8/codecs goldens, zero deltas и caller review. Одна successful compilation не означает native runtime PASS.

Legacy без Broker/Server/Account/origin/currency/precision — quarantine/UNAVAILABLE; нельзя достраивать текущими terminal facts или умножать timestamp до миллисекунд без источника. Minimal не пишет migration files. Rollback — отдельный обратимый remediation commit без on-disk преобразований; исходные bytes/schema сохраняются. Stop: unapproved contract, native incompatibility, новая зависимость/financial callsite вне allowlist, changed remote или необходимость dispatch/persistence.
''')
 doc('NATIVE_VERIFICATION_PLAN', '''# DG01 — native MQL5 verification plan

MQL5_COMPILE=NOT_RUN
MQL5_NATIVE_TESTS=NOT_RUN
NATIVE_VERIFIED=NO

## Подготовленный пакет

`Tests/Native/HSBI_DG01_harness.mq5`, codec cases/goldens и test-only identity candidate. E1 проверяет replay, все29 immutable fields, отдельные signed components, одинаковый Net, source changes, unknown facts/provider/registry, zero и nonfinite. E2 проверяет allocation vector, negative/over-allocation, exhausted/foreign source, duplicate и unknown authority. E3 — NaN/negative margin/Infinity/fill volume, partial, foreign owner, missing actual confirmation. E4 — один FAR, разные FAR в слотах, physical alias observation, independent/copied expected, отсутствующий provider/unknown source. E5 — independent F64Z scalar/record bytes, UTF8, ulong>2^53, canonical zero, min normal/subnormal/max finite, malformed/trailing/unknown wire, roundtrip; T17 — только compatibility probes.

Группы помечены scope: CURRENT_SOURCE_EXPECTED_DEFECT, PROPOSED_V2, LOCAL_EQUALITY, OBSERVATION_NOT_PROVIDER_PROOF и codec test subject. Native FAIL старого дефектного source не исправляется изменением expected. Copied expected observation ожидаемо допускается helper и не является доказательством полного NewFar bypass. Alias probe доказывает одинаковый physical identifier, но **не** автоматически разрешает роль FAR в initialBuy: slot policy ещё требует решения.

Goldens получены отдельным `HSBI_DG01_goldens.py` через literal field order, integer framing и struct.pack; нативный encoder их не вычисляет. Скалярные битовые ожидаемые значения заданы буквально. Decode/malformed probes получают independent golden wire, а не байты собственного encoder; encoder и decoder проверяются раздельно. Генераторы NaN/Infinity должны быть подтверждены как nonfinite; их сбой — INFRASTRUCTURE_ERROR, не kill. Source/value shape и masked unknown отличаются от произвольной самосогласованной authority.

## PowerShell compile launcher

`Tests/Native/HSBI_DG01_compile_isolated.ps1` требует явные MetaEditorPath, TerminalPath, DataPath. Проверяет существование/имена выбранных exe, наличие MQL5, запрещает reparse paths и существующий OutputRoot, создаёт новую изолированную копию только Include/test dependencies. Исходники хешируются до/после. DataPath не копируется, account/config/token files не читаются; terminal64.exe никогда не запускается. Только MetaEditor compile, полный compiler log/версия/hash/process exit/EX5 hash и машинный JSON. Отсутствующий или нераспознанный log не считается успехом; timeout — infrastructure error. Warnings сохраняются и требуют review.

Пример на отдельной офлайн Windows-машине, без реальных счетов:

```powershell
powershell.exe -NoProfile -File .\\Tests\\Native\\HSBI_DG01_compile_isolated.ps1 -MetaEditorPath 'C:\\MT5-Test\\MetaEditor64.exe' -TerminalPath 'C:\\MT5-Test\\terminal64.exe' -DataPath 'C:\\MT5-Test-Data'
```

Не использовать ExecutionPolicy bypass. Launcher не запускался в текущей Linux-среде: pwsh и MetaEditor не найдены в PATH/searched directories. Его синтаксическая/native совместимость должна быть проверена на Windows, не объявляется PASS по static review.

## Отдельный ручной runtime

После успешной компиляции владелец на чистой isolated/offline MT5 installation без реальных accounts/других EA переносит только Stage project в MQL5/Scripts и запускает именно Script. Автоторговля выключена. Не запускать production EA, не подключать history/provider и не импортировать account/config из выбранного DataPath. Если терминал не способен безопасно выполнить скрипт offline — оставить NOT_RUN и подготовить отдельную sandbox-среду, а не подключать реальный счёт.

Сохранить версию MT5, UTC, все source hashes из compile report и полные строки `DG01|TestID|PASS/FAIL|Scope`, generator infrastructure markers и `[HSBI_DG01_NATIVE_RESULT]`. Отсутствие маркера, crash или skipped conditional cases — не полный результат. Script Print не управляет OS exit code: нужны compiler/process exits **и** per-test outputs. COMPILED_ONLY не преобразуется в NATIVE_VERIFIED.

Нативная приёмка полного EA и выбранного production codec остаётся отдельным обязательным шагом после approval; тестовый R0H codec не становится production implementation.
''')
 doc('DEPENDENCY_GRAPH', '''# DG01 — зависимости и безопасная граница

```mermaid
flowchart TD
 A[Owner semantic choices] --> I[Local versioned economic identity API]
 A --> C[Captured codec and MQL domain approval]
 C --> N[Native compile and goldens]
 I --> N
 B[Independent broker namespace/history] --> P[Independent EA-origin provider]
 P --> R[Reconciled immutable economic registry]
 R --> L[Allocation vector identity]
 L --> G[Global source attribution and remaining grant]
 G --> D[Durable journal and atomic commit/CAS]
 D --> V[Journal-aware available funds]
 V --> K[Catch-Up/NewFar composed proof]
 Q[Risk/margin/quotes/costs independent providers] --> K
 K --> F[Full execution FSM and broker reconciliation]
```

Ветви можно проверять независимо. Native-tested local identity не зависит от выбора Transition Loss для чистого comparator, но не разрешает funding/торговлю. Independent provider и durable backend не создаются bool-флагами test fixture. D-01/D-03..D-07/CR-09 могут быть deferred для локального API, но не для дальнейшего финансового использования. Прямые prerequisites Minimal: D-02/D-08, выбранная schema/domain, compatibility policy; serialization требует NUM-CODEC. Нет автоматической цепочки approval→implementation.

Global funding требует source uniqueness по полному broker/account namespace across allocations, логического source lifetime, reversals/transfers policy и реального complete history. Exactly-once требует backend locking/CAS/crash-recovery ordering; serialized Python revision simulation — только specification. Rollback/migration неизвестных records не решаются временным присвоением текущего account.
''')
 doc('ADMIN_DECISION_BALLOT','# DG01 — ballot владельца\n\nВсе поля AdministratorDecision пусты. ReadinessStatus — оценка подготовленности вопроса, не решение. Возможные действия: утвердить конкретную формулировку, отклонить, вернуть на доработку. Ни один выбор не выполнен Codex.\n\n| Canonical ID | Display | Readiness | Approval |\n|---|---|---|---|\n'+ '\n'.join('|'+d['DecisionID']+'|'+d['DisplayOrdinal']+'|'+d['ReadinessStatus']+'|AWAITING_ADMIN_APPROVAL|' for d in decisions)+'\n\n'+ '\n\n'.join('## '+d['DecisionID']+'\n'+d['ShortBallot']+'\n\nAdministratorDecision: (не заполнено)\n\nRequired native/external evidence: '+d['RequiredNativeEvidence'] for d in decisions),'Reports')
 doc('R1_1_APPROVAL_GATE', '''# DG01 — gate Minimal R1.1

CONTRACT_PREPARATION=READY_FOR_ADMIN_DECISION
NATIVE_AXIS=PARTIAL_NATIVE_PENDING
ADMIN_APPROVAL_COMPLETE=NO
R1_1_START_ALLOWED=NO
PRODUCTION_REMEDIATION_ALLOWED=NO

## Четыре ответа

1. До первого локального identity изменения нужны explicit owner choices D-02/D-08, immutable schema/namespace, typed statuses, captured numeric domain и legacy compatibility. Codec approval нужен для production serialization. Остальные16 вопросов рассмотрены, но не все прямо блокируют pure equality. D-05 A/B/C не выбран.
2. FSA-002/005/006/007/008 допускают локальные guards после уточнения domain/phase и проверки callers. FSA-001 требует новой record schema. FSA-003 имеет local binding fix, но полная safety зависит от provider/journal. FSA-004 требует global source registry и durable/atomic enforcement. FSA-009 затрагивает context/invariants/roles/diagnostics. FSA-010 требует независимого provider и end-to-end caller, не только equality.
3. ONE_FILE_LOCAL_API_FEASIBLE — условно да: точный additive diff подготовлен. ONE_FILE_COMPLETE_REMEDIATION_NOT_FEASIBLE — также да: старый classifier и внешние authority/callers не исправлены. Нет утверждения о native compilability без MetaEditor.
4. Нужны MetaEditor strict compile, full29 immutable/namespace/status tests, native integer/double/UTF8/codec goldens, zero delta, actual source hashes и separate runtime logs. Сейчас NOT_RUN.

## Что считается допуском

Только отдельное явное owner approval конкретного baseline, allowlist, schema/status/domain/compatibility и отдельное implementation task. Готовый ballot или reference PASS не являются допуском. Готовый native harness не является работающим EA. Необходимо сохранить старые failures и current no-trade policy.
''','Reports')
 reference=a.load('TEST_RESULTS');mutations=a.load('MUTATION_RESULTS')
 conflicts=sum(d['ReadinessStatus']=='CONTRACT_CONFLICT' for d in decisions)
 doc('FINAL_VERDICT',f'''# HSBI-DG01 — итог подготовки решений

**READY_FOR_ADMIN_DECISION по оси подготовки контрактов; PARTIAL / NATIVE_PENDING по оси нативной проверки.** Ни один контракт не утверждён. Production/remediation/trading запрещены.

База: `{a.BASE}`, branch work. Все1464 существовавших файла, включая74 production sources, проверяются независимо по Git blobs/SHA256/file modes. Существующие AUDIT02 отчёты, источники и evidence не изменены.

## Что проверено и подготовлено

29 дефектов отражены с сохранением предыдущей классификации;49 математических семейств сохранены как23 условных математических утверждения/11 конфликтов/15 UNVERIFIED. Повторная проверка всех non-null source SHA256 выполнена. Найдена locator-ошибка FSA-024: исторический run line7 относится к тексту, определение функции находится в line37; новый SOURCE_REFERENCE_REVIEW и NormalizedDefinitionLines фиксируют это без изменения классификации или formatted-копии оригинала. Это не новое утверждение полной production корректности. Статусы первоначального аудита остаются PARTIAL.

Три formatted Markdown файла — точная обратимая замена буквальных backslash+n на LF. Новые переводы строк не меняют формулы, IDs или выводы; original bytes/hash и offsets преобразования сохранены. Старый AUDIT02 package CLI вернул exit1 из-за новых DG01 untracked files вне его frozen scope; результат не скрыт. Unchanged checker API baseline=False проверил архивный граф без scope, exit0; сохранность всей текущей базы проверена независимо. Исторические R7/R0 FAIL и R8/R10 scope FAIL не исправлены и не переобозначены PASS; свежий полный replay всех исторических suites в DG01 не заявлен.

Все16 административных вопросов рассмотрены; {conflicts} строка имеет ReadinessStatus=CONTRACT_CONFLICT (D-05: явный выбор A/B/C). Named IDs CR/NUM/SNAP/FUNDING/MQL/BALANCE сохранены; отображаемые D-09..D-16 не переименовывают исторические решения. Для каждого P0 подготовлен отдельный план с local/system dependencies. FSA-010: local helper equality не authentication; copied expected acceptance не доказательство полного solver bypass.

Подготовлен точный неприменённый one-file diff. Старые объявления и алгоритмы сохраняются; добавляется test-only V2 кандидат29 immutable facts с SourceKey broker/server/account/deal и unknown-facts envelope. `git apply --check` не является применением patch. Полное устранение FSA-001 во всех callpaths в таком scope не доказано и не заявлено. Production serializer/provider/global ledger не реализованы.

## Реальные результаты

Reference-ledger: {reference['Pass']} PASS / {reference['Fail']} FAIL / {reference['InfrastructureErrors']} infrastructure errors. Это {len(reference['Rows'])} конкретных сценариев, включая типовые negative variants; они не являются таким же числом независимых математических доказательств. Три formatting проверки считаются отдельно. Integer minor units сохраняют маленькие debit на границе INT64_MAX; source/allocation/event/owner/revision, replay, history/cost/precision, altered equal-net и immutable vector проверены literal expected values. Перезапуск — trusted snapshot simulation; конкурирующие consumers — serialized revision conflict, не реальный CAS/concurrency.

Source mutations нового reference: {mutations['Killed']} killed / {mutations['Survived']} survived / {mutations['InfrastructureErrors']} errors. UNSAFE_ACCEPTANCE_KILL и STATUS_CONTRACT_KILL разделены; это не mutation доказательство production. Первоначальный59-case прогон имел один status failure, а mutation suite — survivor после ужесточения default authority facts. Точные исходные bytes/hashes и rows сохранены в DEVELOPMENT_*: malformed allocation теперь проверяется до отсутствующей authority, mutation VECTOR использует новый event2 и explicit complete facts, чтобы не маскироваться другим replay guard. Expected outcomes не подгонялись под source.

Подготовлен расширенный MQL5 Script E1–E5 и compile-only PowerShell launcher. Нативных результатов нет: MetaEditor/MT5/Wine/pwsh не найдены в PATH и перечисленных поисковых каталогах. MQL5_COMPILE=NOT_RUN; MQL5_NATIVE_TESTS=NOT_RUN; NATIVE_VERIFIED=NO. Launcher также NOT_RUN, его Windows compatibility требует проверки. COMPILED_ONLY никогда не означает runtime PASS. F64Z/T17Z остаются candidates.

## Границы и следующий шаг

Broker authenticity, complete global economic attribution, durable restart, concurrent double-spend, full proof→consumption/NewFar и полный торговый цикл остаются UNPROVEN/UNIMPLEMENTED. Строгая форма DTO и bool flags не превращают fixtures в реальную историю. Reference-ledger — proposed DG01-LEDGER-1 профиль USD/digits2/positive reconciled closing OUT/OUT_BY BigCore/Trend source with explicit proposed policy1, не универсальная broker policy. Captured raw binary64 body и settled minor-unit money различаются. Положительный Balance не доказывает recovery Equity, прибыльность или loss bound.

Следующий шаг — независимое рассмотрение и owner ballot, затем отдельная native verification на изолированной Windows-среде. R1.1 требует отдельного разрешения и задания. Нет автоматического перехода к production.

CONTRACT_PREPARATION=READY_FOR_ADMIN_DECISION
NATIVE_AXIS=PARTIAL_NATIVE_PENDING
AUDIT_COMPLETENESS=PARTIAL_NATIVE_PENDING
ADMIN_APPROVAL_COMPLETE=NO
R1_1_START_ALLOWED=NO
PRODUCTION_REMEDIATION_ALLOWED=NO
TRADING_LOGIC_START_ALLOWED=NO
BROKER_DISPATCH_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
''','Reports')
 print('DG01 BUILD',len(issues),'defects',len(decisions),'decisions',len(plans),'plans','native prepared',len(native_rows))
if __name__=='__main__':build()
