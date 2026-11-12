"""Build Russian audit02 reports from fresh evidence and explicit independent review rows.
No trading, no historical writes. Publication is a separate manual gate.
"""
import sys,json,re,hashlib,subprocess
from pathlib import Path
import HSBI_FULL_SYSTEM_AUDIT_02_verify as a
R=a.ROOT;T=a.TAG

def md(name,text,folder='Reports'):(R/folder/(T+name+'_RU.md')).write_text(text.rstrip()+'\n')
def evidence(n):return a.strict(R/'Tests/Evidence'/(T+n+'.json'))
def source_ref(path,func):
 p=R/path;s=p.read_text();at=s.find(func);return dict(File=path,SHA256=a.sha(p),Function=func,Line=s[:at].count('\n')+1 if at>=0 else None,FullSourceReadBoundary='STATIC_SOURCE_NOT_NATIVE_RUNTIME')
# No outcomes below are inferred from historical PASS counts.
REVIEW=[
('001','CONFIRMED_SOURCE_DEFECT','HSBI_SameEconomicRecord','FSA001_COMPONENTS','Сравнение не включает Profit/Swap/Commission/Fee и другие immutable поля.','P50/C0 против P70/C-20, Net50. Компоненты различны при неизменном ключе.','Сопоставлять полный утверждённый immutable payload.','D-08, NUM-CODEC, MQL-DOMAIN'),
('002','CONFIRMED_SOURCE_DEFECT','HSBI_ClassifyAllocationDuplicate','FSA002_VECTOR','Равенство суммы ошибочно заменяет равенство вектора.','Reserve50/PF0 против Reserve0/PF50.','Тот же allocation event, изменённый bucket vector → CONFLICT.','D-01, D-08'),
('003','CONFIRMED_SOURCE_DEFECT','HSBI_EvaluateReserveCatchUp','FSA003_FOREIGN_ALLOCATION','Consumption key проверен по форме/plan/revision, но не по sourceAllocationKey/sourceDealKey authority.','Источник TEST-D101/ALLOC-A, consumption OTHER-ACCOUNT/OTHER-ALLOC.','Сверять оба namespace с независимой allocation.','D-07, D-08'),
('004','CONFIRMED_SOURCE_DEFECT','HSBI_EvaluateReserveCatchUp','FSA004_EXHAUSTED','В ветке not alreadyAllocated отсутствует вычитание/запрет alreadyConsumed.','Allocatable50, consumed50, reserveAllocated0, eligible50, share.8 → gain40.','Исчерпанный source не создаёт новый grant; global uniqueness требует реестра.','FUNDING-GLOBAL-ATTRIBUTION'),
('005','CONFIRMED_SOURCE_DEFECT','HSBI_ValidateRiskInput','FSA005_NAN','Сравнения с NaN ложны; нет finite/domain validation.','projectedMargin=NaN либо -1 при согласованных остальных gates.','Malformed/nonfinite не даёт passed. Отрицательная projected margin требует явного domain.','MQL-DOMAIN'),
('006','CONFIRMED_SOURCE_DEFECT','HSBI_TransactionBarrierPassed','FSA006_NAN','abs(NaN-expected)>epsilon ложно, completion может пройти.','expected1, accumulatedNaN, COMPLETED, ownership=true.','Конечный положительный объём и подтверждённые факты до completion.','D-08, MQL-DOMAIN'),
('007','CONFIRMED_SOURCE_DEFECT','HSBI_ValidateAllocationConservation','FSA007_NEGATIVE_BUCKET','Неотрицательность отдельных bucket не проверяется.','Reserve-50/PF100 при source50; сумма50.','Каждая grant component >=0. Полное COMMITTED равенство отдельно pending D-01.','D-01'),
('008','CONFIRMED_SOURCE_DEFECT','HSBI_ValidateMoneyState','MONEY_INF','Infinity >=0 принимается; valid и revision игнорируются.','finalReserve=+Infinity. Дополнительно valid=false/revision0.','Finite domain обязателен; правила valid/revision отдельно сформулировать.','BALANCE-SCHEMA-MAPPING, MQL-DOMAIN'),
('009','CONFIRMED_SOURCE_DEFECT','HSBI_ValidateContext','FSA009_INITIAL_SLOT','FAR-count и проверка role-slot пропускают initialBuy/initialSell/newFarCandidate.','farID100 и initialBuyID101 оба FAR, одинаковый owner.','Считать реальные активные FAR во всех слотах; отличать alias от двух позиций.','D-08, active-role schema'),
('010','UNIMPLEMENTED','HSBI_SolveNewFar','FSA010_INDEPENDENT_EXPECTED','Caller переписывает proof identity, затем копирует её в expected. Независимый экономический provider отсутствует.','Helper отвергает чужой proof при независимом expected, принимает при copied expected.','Helper equality локально корректен; весь NewFar independent provenance не доказан.','D-02, D-08, provider reconciliation'),
('011','CONFIRMED_SOURCE_DEFECT','HSBI_SolveBigGeometry','FSA011_ZERO_CORE','coreGrid разрешает Core=0 и не требует Core>=volumeMin.','Far.1 Rc.01 Rt3 Rs.1: rawCore.001→0.','Обязательный Core положителен и на broker grid/min/max.','Active-leg schema'),
('012','UNIMPLEMENTED','HSBI_IsTransitionAllowed','FSA012_CORE_TO_TREND','Таблица нормального пути обрывается после открытия Core; event orchestrator отсутствует.','CoreOpening→TrendOpening отсутствует; reconcile-путь не имеет admin resume аргумента.','Полный event FSM и запрет auto-resume требуют orchestration/authority.','Lifecycle approval'),
('013','UNIMPLEMENTED','HSBI_PersistSnapshotStub',None,'Stub возвращает success=false; production SHA256=false.','Restart без journal backend не восстанавливает подтверждённый funding.','Durable commit/lock/CAS нельзя доказать stub.','D-07'),
('014','UNIMPLEMENTED','OnTick',None,'EA вызывает только SubmitActionStub; OnTradeTransaction отсутствует.','Tick не запускает Harvest/PartialFar/NewFar.','Полный lifecycle не реализован. Это не дефект работающего dispatch.','Separate production task'),
('015','CONFIRMED_CONTRACT_CONFLICT','HSBI_AggregateFutureSmallProof','FSA015_MIN_MARGIN_LEVEL','WORST_CASE выбирает worstTransitionLossLevel вместо minimum CatchUpMargin.','T1=10,M1=9; T2=5,M2=-11. Выбран1.','ALL_LEVEL требует min margin>0; SINGLE_LEVEL должен иметь отдельный scope.','CR-09'),
('016','CONFIRMED_CONTRACT_CONFLICT','',None,'Разные документы требуют minimum-safe-volume и risk-first ordering.','Безопасный N.1 risk9 и N.2 risk1 дают разные optimum.','Владелец выбирает lexicographic objective; тест не утверждает экономическую цель.','NewFar objective policy'),
('017','CONFIRMED_SOURCE_DEFECT','HSBI_EvaluateFutureSmallLevel',None,'netBigVolume сравнивается с priorBigGross, затем priorBig тоже хранит net.','Old gross4/net2; new gross8/net0 проходит одну net-проверку. Не весь solver.','Сравнивать одинаковые gross величины; прочие gates независимы.','Gross schema'),
('018','CONFIRMED_CONTRACT_CONFLICT','HSBI_ValidateConservativeBound',None,'Функция endpoint-bound не доказывает единый закон будущих переходов.','F=1,.8,.64 затем .64; первые два шага не задают третий.','Нужна предпосылка Fnext<=qF на каждом переходе; helper не ошибочен внутри scope.','Tail/terminal contract'),
('019','UNVERIFIED','HSBI_TryProjectedNetMoney',None,'Нет независимого basis/window/coverage для spread/buffer.','BUY Ask101→Bid110 уже даёт9; вычет того же spread1 даёт8 только при доказанном overlap.','Нельзя объявить любой spread двойным: provider basis неизвестен.','D-06'),
('020','UNVERIFIED','',None,'Режим hedging/netting не закреплён независимым account admission.','BUY1+SELL1: hedging две позиции; netting net0.','Нужен hedging contract либо виртуальный netting ledger; broker evidence отсутствует.','Account mode'),
('021','CONFIRMED_CONTRACT_CONFLICT','HSBI_IsSnapshotFresh','FSA021_FUTURE_TIME_ZERO_SKEW','Нет нижней границы age; future timestamp принят.','now100,ts1000,maxAge10.','Для zero-skew fixture reject; универсальный clock skew требует выбора.','Clock-domain policy'),
('022','CONFIRMED_SOURCE_DEFECT','HSBI_ProposeStateTransition','FSA022_OVERFLOW','Revision+1 не проверяет ULONG_MAX.','IDLE/revision 2^64-1→InitialPlanReady. C++ unsigned wrap; native NOT_RUN.','Остановить переход до overflow; не обнулять revision.','MQL-DOMAIN'),
('023','CONFIRMED_SOURCE_DEFECT','HSBI_FutureSmallTemplateDigest',None,'Digest индексирует maximumDepth до downstream проверки <=128.','maximumDepth129 при ранних валидных полях; static potential OOB, не исполнялся.','Проверять shape/domain до digest. Нужен native checked test.','DTO/domain'),
('024','CONFIRMED_CONTRACT_CONFLICT','run',None,'Исторический scope запрещает MQL-файлы даже в разрешённых test harness.','Три R0H .mq5/.mqh в Tests; свежие findings сохранены.','Разделить test-only MQL и production; frozen checker не менять.','Test scope'),
('025','CONFIRMED_CONTRACT_CONFLICT','',None,'Исторические closure/readiness statements не означают текущего source approval.','OPEN_P0=0 прежнего этапа и новые source defects существуют одновременно.','Readiness версионировать по SHA/scope; исторические статусы не переписывать.','Normative hierarchy'),
('026','UNVERIFIED','OnStart',None,'Native harness есть, выполнения MetaEditor/MT5 в этой среде нет.','Python/C++ успешен без подтверждённых MQL compiler diagnostics.','NOT_RUN; отсутствие evidence не является runtime bug.','Native toolchain'),
('027','CONFIRMED_SOURCE_DEFECT','HSBI_ClassifyJournalAppend','FSA027_ALTERED_BODY','Duplicate lookup предшествует проверке digest/body candidate.','payload A→ALTERED, currentEntryDigest оставлен старым → NO_OP.','Проверять immutable body binding до exact replay; durable backend отсутствует.','D-07, D-08'),
('028','CONFIRMED_CONTRACT_CONFLICT','HSBI_SolveFutureSmall',None,'finiteSequence при Far<=volumeMin не означает full close; terminalRouteAllowed не используется.','Far=.01>0, разрешение terminal route не проверено.','Отдельный терминальный маршрут, стоимость и фактическое закрытие.','Terminal policy'),
('029','CONFIRMED_SOURCE_DEFECT','HSBI_EvaluateBasketMoney',None,'Geometry разрешает Trend0, money/margin вызываются для четырёх положительных leg.','Core=.3,Trend0,Small.01,Far.1; geometry valid, projected leg Trend0 invalid.','Явный optional-leg contract; Core нельзя пропускать.','Active-leg schema')]
PROOFS={
'F01':'При step>0 и x>=0 floor(x/step)*step<=x, разница<step. Это арифметика вещественных, не доказательство binary64/grid-origin.',
'F03':'ceil(x/step)*step>=x и <x+step при step>0; broker min/max проверяются отдельно.',
'F05':'Для одинакового линейного unit-value, фиксированных объёмов производная по движению против Far: C+T-S-F. При иной контрактной стоимости нужна broker модель.',
'F06':'В линейной симметричной модели рост Reserve r*B и FarLoss F даёт положительную разность slope при rB>F; начальный deficit/costs этим не покрыты.',
'F07':'Net определяется сложением signed денежных компонентов; знак каждого сохраняется. 60-2-7-1=50. Authenticy не следует из равенства.',
'F08':'При независимых непересекающихся deductions projectedNet=gross+signedSwap+signedCommission+signedFee-spread-slip-buffer по определению учёта. Overlap не доказан.',
'F10':'При едином boundary cycle realized уже включает все проведённые входные/выходные costs; closeNow открытых позиций учитывается один раз. Reserve — метка realised, а не дополнительный доход.',
'F11':'Порог minProfit+executionBuffer+tolerance — сумма в одной валюте. Сам размер и применимость порога требуют owner policy.',
'F13':'При grants без внешних transfer сохранение G=C+R+F задаёт точный partition. Переход consume d: C+=d,F-=d сохраняет сумму; 0<d<=F необходимо.',
'F14':'RemainingGross=G-C=R+F алгебраически следует из G=C+R+F. Legacy Remaining нельзя считать Free без доказанной схемы.',
'F20':'Loss=max(0,-net) равен0 при net>=0 и -net при net<0; только в указанном absolute close-now basis.',
'F22':'При известных independent Reserve,L,B coverage со строгим запасом эквивалентно R-L-B>0. Никаких гарантий fill/margin.',
'F24':'Loss=max(0,-sum signed fills) определяет текущую signed-loss политику. Это не peak/sticky. Fills обязаны принадлежать одному batch.',
'F26':'Если каждый из четырёх finite caps верхняя граница одной loss, одновременное выполнение loss<=каждый cap эквивалентно loss<=min(caps). Разные risk basis недопустимы.',
'F27':'При F>0,N>=0 compressionLots=F-N, compressionRatio=(F-N)/F. Строгое уменьшение требует N<F.',
'F28':'При r in(0,1), F>0 условие N<=rF даёт F-N>0; цена/lot rounding могут нарушить реализуемость.',
'F30':'Gross=sum abs(signed lots); Net=sum signed lots; triangle inequality abs(Net)<=Gross. Уменьшение absNet не влечёт уменьшения Gross.',
'F34':'Equity=Balance+floating net при фиксированном broker accounting boundary. Реальные free margin/stopout formulas здесь не выводятся.',
'F35':'CyclePnL=realized net+closeNow net открытых legs включая их exit costs. Все части учитываются по одному разу; Reserve второй раз не прибавляется.',
'F37':'Если Fk<=q^k F0 при каждом переходе, F0>=Vmin>0,0<q<1, то k>=log(Vmin/F0)/log(q) достаточно для Fk<=Vmin. Ceil — первый целый bound; Fk<=Vmin не равно Fk=0.',
'F44':'В точной арифметике tick*round(price/tick) лежит на origin0 grid и имеет error<=tick/2 при заданном tie rule. Binary64 и иные origin требуют отдельной проверки.',
'F45':'При явно заданных start/step в points и point в price/point, reference±(start+(k-1)step)*point имеет размерность price. Не подтверждает факт исполнения уровня.',
'F46':'Market BUY ликвидируется продажей по Bid, SELL покупкой по Ask при данной модели quotes; slippage, fees и availability дополнительные факты.'}

def build():
 old=a.load01('DEFECTS')['Rows'];initial=evidence('SOURCE_TESTS_FRESH');extended=evidence('SOURCE_TESTS_EXTENDED');math=evidence('MATH_TESTS_FRESH')
 bytest={x['TestID']:x for x in extended['Rows']};defects=[]
 for nr,status,fn,test,actual,example,expected,decision in REVIEW:
  prev=next(x for x in old if x['DefectID']=='FSA-'+nr);src=source_ref(prev['SourceFile'],fn) if fn else dict(File=prev['SourceFile'],SHA256=a.sha(R/prev['SourceFile']),Function=None,Line=prev['SourceLine'])
  defects.append(dict(ID='FSA-'+nr,Severity=prev['Severity'],Classification=status,Source=src,Contract=prev['Requirement'],Actual=actual,Expected=expected,Counterexample=example,FreshTest=bytest.get(test),TestID=test,Reachability='NOT_REACHED_FROM_CURRENT_EA_EVENTS; source library only' if nr!='014' else 'OnTick reachable: execution stub only',FutureConsequence='Подключение этого модуля без устранения предпосылок может дать неверное решение/учёт; это не доказанный реальный ордер.',Evidence=T+'SOURCE_TESTS_EXTENDED.json' if test else 'STATIC_SOURCE_AND_EXPLICIT_MATHEMATICAL_ARGUMENT; no fresh end-to-end execution',RequiredDecision=decision,RemediationScope='PLAN_ONLY; no production changes',Dependencies=['Separate admin approval','Native MQL acceptance','Independent provider/complete registry where applicable']))
 a.save('DEFECT_MATRIX',dict(BaseSHA=a.BASE,Rows=defects,Counts={s:sum(x['Classification']==s for x in defects) for s in sorted({x['Classification'] for x in defects})},Boundary='29 individually classified; not 29 exploitable runtime defects'), 'Tests/Contracts')
 # The thirteen original failures remain separate, including scope/policy uncertainty.
 links={'FSA001_COMPONENTS':'001','MAGIC_SAME_PHYSICAL_SOURCE':'001','FSA002_VECTOR':'002','FSA007_NEGATIVE_BUCKET':'007','FSA003_FOREIGN_ALLOCATION':'003','FSA004_EXHAUSTED':'004','FSA005_NAN':'005','RISK_NEGATIVE_MARGIN':'005','FSA006_NAN':'006','FSA008_INVALID_FLAG':'008','MONEY_INF':'008','FSA009_INITIAL_SLOT':'009','NO_DUAL_ALL_SLOTS':'009'}
 failrows=[]
 for i,x in enumerate((x for x in initial['Rows'] if x['Result']=='FAIL'),1):
  d=next(z for z in defects if z['ID']=='FSA-'+links[x['TestID']]);kind='CONTRACT_CONFLICT' if x['TestID'] in ('MAGIC_SAME_PHYSICAL_SOURCE','RISK_NEGATIVE_MARGIN') else 'UNVERIFIED' if x['TestID']=='FSA008_INVALID_FLAG' else 'CONFIRMED_SOURCE_DEFECT'
  failrows.append(dict(FailureID='A02-FAIL-%02d'%i,**x,FSA=d['ID'],Classification=kind,Source=d['Source'],Contract=d['Contract'],IndependentOracle=d['Expected'],MinimalCounterexample=d['Counterexample'],StateDelta='Result-only API: no durable ledger/debit executed. const-input/pure-source review; dynamic deep state snapshots only in independent ledger tests, not claimed for these source probes.',Reachability=d['Reachability'],FutureConsequence=d['FutureConsequence'],AdapterAnalysis='These vectors use field equality, comparisons and standard abs only; OrderCalcProfit/OrderCalcMargin not invoked. Shared language glue remains an unverified native-semantics boundary.',Note='valid=false semantics need explicit API contract' if kind=='UNVERIFIED' else 'Namespace/domain proposal requires owner choice' if kind=='CONTRACT_CONFLICT' else 'Local contract violation; no broker execution'))
 a.save('FAIL_CLASSIFICATION',dict(Rows=failrows,OriginalPass=17,OriginalFail=13,Reproduced=initial['Pass']==17 and initial['Fail']==13,Note='10 source-contract failures,2 policy conflicts,1 valid-flag requirement unverified. Several rows map to one defect.'))
 # 49 source/contract mappings: old entries are an index, never automatically proof.
 formulas=[]
 for q in a.load01('FORMULA_MATRIX','Tests/Contracts')['Rows']:
  fid=q['FormulaID'];st='VERIFIED_CONDITIONAL_MATHEMATICS' if fid in PROOFS else 'CONTRADICTORY_CONTRACT_OR_SOURCE' if fid in {'F02','F04','F12','F16','F17','F19','F21','F23','F29','F36','F47'} else 'UNVERIFIED'
  location=q['Source'].rsplit(':',1);file=location[0];loc=int(location[1]) if len(location)==2 and location[1].isdigit() else 1;exists=(R/file).is_file();lines=(R/file).read_text().splitlines() if exists else []
  formulas.append(dict(FormulaID=fid,Expression=q['Expression'],Contract=q['NormativeSource'],Source=q['Source'],CurrentSourceSHA256=a.sha(R/file) if exists else None,SourceExcerpt=lines[max(0,loc-2):loc+2],Status=st,Proof=PROOFS.get(fid,'См. индивидуальную проблему/границу ниже; численные совпадения не являются доказательством.'),HistoricalStatusNotInherited=q['Status'],ProofBoundary='Formal real/rational arithmetic under explicit assumptions; not all-domain MQL/broker proof',Outstanding=q['ProofBoundary']))
 a.save('FORMULA_REVIEW',dict(Rows=formulas,Verified=sum(x['Status']=='VERIFIED_CONDITIONAL_MATHEMATICS' for x in formulas),Contradictory=11,Unverified=sum(x['Status']=='UNVERIFIED' for x in formulas),DifferenceFromAudit01='F42 raw codec specification/native compatibility not independently proved in this pass; downgraded to UNVERIFIED. Other VERIFIED labels now explicitly conditional mathematical statements.'),'Tests/Contracts')
 # Current owner choices are retained verbatim as proposals, independently annotated.
 decisions=a.strict(R/'Tests/Contracts/NEXT_STAGE_02B_R0F_ADMIN_DECISIONS.json')['Rows']
 for x in decisions:
  x['ApprovalStatus']='AWAITING_ADMIN_APPROVAL';x['AdministratorDecision']='';x['Audit02Review']='Рекомендация не утверждена. Математический аргумент проверяется по формуле/контрпримеру; provider/native/durable evidence не следует из proposal.'
  x['CurrentEvidenceBoundary']='SOURCE_STATIC + scoped exact fixtures; MQL5 native/broker/durable NOT_RUN or UNPROVEN'
 assert len(decisions)==16
 a.save('DECISION_MATRIX',dict(Source='R0F proposal rows; content not silently promoted to normative',SourceSHA256=a.sha(R/'Tests/Contracts/NEXT_STAGE_02B_R0F_ADMIN_DECISIONS.json'),Rows=decisions),'Tests/Contracts')
 # Exact state names and all ordered pairs independently evaluated from the current pure source expression.
 s=(R/'Include/Core/HSBI_StateMachine.mqh').read_text();names=re.findall(r'HSBI_STATE_[A-Z_]+',(R/'Include/Core/HSBI_Enums.mqh').read_text().split('enum HSBI_State{')[1].split('};')[0]);expr=s[s.index('bool HSBI_IsTransitionAllowed'):s.index('HSBI_StateTransitionResult HSBI_Propose')]
 ordered=re.findall(r'if\(from==(HSBI_STATE_\w+)&&to==(HSBI_STATE_\w+)\)return true',expr)
 actual=[]
 for f in names:
  for t in names:
   allowed=f==t or (f,t) in ordered or f=='HSBI_STATE_RECONCILING' and t in ['HSBI_STATE_TERMINAL_SAFE','HSBI_STATE_FAR_ACTIVE','HSBI_STATE_IDLE'] or t in ['HSBI_STATE_RECONCILING','HSBI_STATE_TERMINAL_SAFE','HSBI_STATE_EMERGENCY']
   actual.append(dict(From=f,To=t,PureTopologyAllowed=allowed,EventHandlerImplemented=False,RuntimeReachable=False,Event='NOT_AN_EVENT_API',Preconditions='Topology only; no deals/ownership/timeouts/resume authority',StateEffect='Pure helper can change context/revision if called; main never calls it'))
 normative=[('IDLE','INITIAL_LOCK_ACTIVE','Initial Lock fills','Persisted plan, two actual fills, ownership and fresh history'),('INITIAL_LOCK_ACTIVE','FAR_ACTIVE','Close InitialPlus completed','Independent economic record + actual remaining position'),('FAR_ACTIVE','BASKET_ACTIVE','Open C/T/S completed','Immutable candidate, volume/min/step, account margin, no pending'),('BASKET_ACTIVE','ALLOCATION_PENDING','Big Harvest completed','Actual BigCore/Trend deals, source attribution, full components'),('ALLOCATION_PENDING','FINAL_CLOSE_EXECUTING','FinalClose eligible','Realized+closeNow net threshold, no unknown/pending, fresh costs'),('ALLOCATION_PENDING','PARTIAL_FAR_EXECUTING','PartialFar eligible','Only PartialFarBudget owner reservation + actual loss'),('BASKET_ACTIVE','SMALL_CONFIRMING','Touch then hold/retrace','Fresh second snapshot, persisted debounce, no active transition'),('SMALL_CONFIRMING','OLD_FAR_CLOSING','Small close completed','Plan + actual Small deal + partial-fill barrier'),('OLD_FAR_CLOSING','BIG_TREND_CLOSING','OldFar close completed','Actual closure and no second Far'),('BIG_TREND_CLOSING','BIG_CORE_REDUCING','Trend close completed','Actual deal and cap/batch reconciliation'),('BIG_CORE_REDUCING','NEW_FAR_VALIDATING','Core partial complete','Original Core residual owner/id/volume confirmed'),('NEW_FAR_VALIDATING','FAR_ACTIVE','Promotion confirmed','All-level or explicit scope proofs + single actual Far'),('FINAL_CLOSE_EXECUTING','CYCLE_CLOSED','All positions closed','Actual final deals, ledger reconciliation, zero managed residual'),('ANY_PENDING','RECONCILING','Timeout/partial/out-of-order','No FSM advance until actual history and ownership reconciled'),('ANY','TERMINAL_SAFE','Critical unresolved conflict','No openings; manual authority required for restart/resume')]
 a.save('FSM_MATRIX',dict(ActualStates=names,ActualPurePairs=actual,NormativeTransitions=[dict(From=f,To=t,Event=e,Preconditions=p,Actions='Desired transaction→actual history→ledger→persist→FSM; UNIMPLEMENTED event orchestration',Invariants='SingleFar, no double-funding, exact owner/replay, fresh independent facts',RuntimeStatus='UNIMPLEMENTED') for f,t,e,p in normative],MainState='DISABLED',Boundary='Complete 33x33 pure-topology map, normative manual phase-level map only. Full normative event/precondition/action matrix not formally complete; audit remains PARTIAL.'),'Tests/Contracts')
 r1=dict(Baseline=a.BASE,ProductionAllowlist=['Include/Money/HSBI_EconomicLedgerTypes.mqh'],Status='PROPOSED_AWAITING_ADMIN_APPROVAL',SourceKey=['Broker','Server','AccountLogin','DealTicket'],PayloadFields=['SchemaVersion','Broker','Server','AccountLogin','Symbol','Magic','CycleID','DealTicket','OrderTicket','PositionIdentifier','ActionID','EventID','Role','EntryType','DealType','TimestampMsc','Volume','Price','Profit','Swap','Commission','Fee','DealNet','Currency','Precision','SourcePlanApplicable','SourcePlan','SourcePolicyApplicable','SourcePolicyVersion'],Statuses=['NEW','NO_OP','CONFLICT','REJECT','UNAVAILABLE'],NativeAcceptance='MetaEditor strict compile complete EA and isolated no-trade harness; diagnostics, warnings and per-field goldens required. NOT_RUN now.',Acceptance=['Same key exact full immutable payload NO_OP with zero state delta','Same Net but changed signed components CONFLICT','Magic/Cycle/Symbol change under same broker account deal CONFLICT, never new profit','Unknown namespace/history/origin/registry completeness UNAVAILABLE, never NEW','Malformed nonfinite/range/schema rejected without mutation','Different independently confirmed source can be NEW_IDENTITY only, never spending permission','29-field equality roundtrip, UTF8/int64/uint64/binary64 goldens with exact zero policy','Unknown legacy quarantine, no fabricated current account or origin data','Legacy diagnostic-only semantics explicitly approved; caller static scan before integrating','One-file diff only; no new production helper, provider/backend/funding/dispatch','Full immutable source tests, checked double domain, exact allowed codec approved by owner'],Compatibility='Additive V2 surface may fit one header; this does not fix old financial equality by itself. Old names diagnostic-only only after explicit owner agreement and caller audit.',Rollback='Single remediation commit reversible; no on-disk migration writes in Minimal R1.1. Preserve original bytes and immutable schema; quarantine unknown legacy.',OneFileFeasibility='STATIC_CONDITIONAL; data structs/pure equality/status helpers fit one header. Provider authenticity, persistence/CAS and active callers cannot be remedied in this scope.',StopConditions=['Unapproved codec/schema/domain','New callsite or helper needed outside allowlist','MetaEditor compile/native fails or unavailable at acceptance','Any trading/persistence/provider operations introduced','Remote baseline changed'],StartAllowed=False)
 a.save('R1_1_ACCEPTANCE',r1,'Tests/Contracts')
 # Full 29-row written record includes exact individual decisions and scope, not a blanket exploit count.
 p0=['# AUDIT 02 — независимая перепроверка P0','База: `'+a.BASE+'`. Изменений production нет. 9 локальных source-дефектов; FSA-010 — UNIMPLEMENTED independent-provider boundary. Все 10 не являются достижимыми торговыми обходами текущего EA.','Новые first-attempt fixtures воспроизведены без изменения expected. FSA010 имеет positive independent reject и copied-expected observation; полный NewFar solver/broker не исполнялся.']
 pp=['# AUDIT 02 — P1/P2: повторная классификация','Ни одна строка не означает native runtime доказательство. Отдельно различены source, normative conflict, unimplemented и UNVERIFIED.']
 for d in defects:
  block='\\n## '+d['ID']+' — '+d['Severity']+' / '+d['Classification']+'\\n'+ '\\n'.join('- **'+k+'**: '+str(d[k]) for k in ['Source','Contract','Actual','Expected','Counterexample','TestID','Reachability','FutureConsequence','RequiredDecision','Dependencies','Evidence'])
  (p0 if d['Severity']=='P0' else pp).append(block)
 md('P0_REVERIFICATION','\\n'.join(p0));md('P1_P2_REVIEW','\\n'.join(pp))
 md('MATH_PROOF_GAPS','# AUDIT 02 — 49 семейств формул\\n\\n23 условных математических утверждения; 11 конфликтов code/contract/proposal; 15 UNVERIFIED. В первом аудите было24/11/14: F42 понижен, native codec не доказан. Ни одна условная теорема не подтверждает production по всему domain.\\n\\n'+ '\\n\\n'.join('## '+q['FormulaID']+' — '+q['Expression']+'\\nСтатус: '+q['Status']+'\\nИсточник: '+q['Source']+'; норматив: '+q['Contract']+'\\n'+q['Proof']+'\\nГраница/оставшаяся проверка: '+q['Outstanding'] for q in formulas)+ '\\n\\n### Catch-Up и конечность\\nОбязательные уровни exact proof представлены provenDepth (2..128), но CR-09 ALL_LEVEL vs SINGLE_LEVEL остаётся owner choice. Проверка all-level: min_i(R_i-L_i-B_i)>0 нужна для одновременного proof, но недостаточна для fills/margin/slippage. Это альтернативные сценарии: один reserve можно оценивать на каждом уровне отдельно; последовательные реальные расходы обязаны уменьшать его. Пример R50, два consumption30 оставляет -10 и должен отвергаться. При partial Far нужен новый actual residual и basis, а не механический старый loss.\\n\\nЛогарифмическая оценка шагов требует uniform q каждого будущего перехода, допустимого broker grid и выполнения всех действий. В ненулевом min lot остаётся экономическая позиция. Бесконечно растущая цена при незащищённом SELL не даёт безусловной конечной границы убытка. Нужны явные ограничения цены/gap, гарантии ликвидности/exit/slippage/маржи или полностью оценённый hedge; stopout сам по себе не математическая гарантия общей суммы.\\n\\nНе завершены: native численные домены/codecs, all-domain bounded rounding, broker margin/netting formulas, actual cost/window overlap, весь event-level FSM и full integration. Поэтому PARTIAL.')
 md('FSM_COMPARISON', '''# AUDIT 02 — нормативная и реализованная FSM

Нормативный источник: `Docs/03_FULL_SYSTEM_MANUAL_RU.md`, разделы «Полный цикл», «Transaction», «Restart/error». Реализация: `Include/Core/HSBI_StateMachine.mqh` и основной `.mq5`.

```mermaid
flowchart TD
 I[Initial Lock actual fills] --> P[Close InitialPlus actual deal]
 P --> F[One Far]
 F --> C[Immutable candidate and C/T/S actual fills]
 C --> H[Big Harvest actual deals]
 H --> A[Allocation]
 A --> FC[Final Close actual fills]
 A --> PF[Partial Far reservation and actual debit]
 PF --> F
 C --> S[Small confirmation and close]
 S --> OF[OldFar close]
 OF --> T[Trend close]
 T --> CR[Original Core actual reduction]
 CR --> NF[NewFar actual residual validation]
 NF --> F
 FC --> END[Reconciled zero residual]
```

```mermaid
flowchart TD
 INIT[OnInit] --> DIS[Initialize DISABLED]
 TICK[OnTick] --> STUB[SubmitActionStub: blocked]
 STUB --> REASON[Update lastReason only]
 TIMER[OnTimer] --> DIAG[Diagnostics, no state advance]
 PURE[Pure state helpers: not called by main] -.-> TABLE[Limited topology, not full event FSM]
```

Машиночитаемый полный 33×33 topology inventory: `Tests/Contracts/HSBI_FULL_SYSTEM_AUDIT_02_FSM_MATRIX.json`. Это **не** полная нормативная event-level таблица. В ней явно отсутствуют implemented handlers. Нормативная часть описывает фазы мануала; полный перечень event/preconditions/actions/retry/out-of-order/restart combinations ещё не формализован.

Pure table допускает self-loop, ранний путь до CoreOpening, generic переходы в RECONCILING/TERMINAL_SAFE/EMERGENCY и выходы RECONCILING в FarActive/Idle/TerminalSafe. CoreOpening→TrendOpening отсутствует. Generic разрешение topology не является authority для manual resume. Текущий EA эту таблицу не использует для торговли. Внешние fills и out-of-order события не поступают: OnTradeTransaction отсутствует.

Для каждого нормативного перехода нужны shape/owner/actual-fill/replay/partial/timeout/reject/restart guards, экономический ledger и persistence. Их отсутствие отмечено UNIMPLEMENTED, а не PASS. Диагностический far-count helper достижим по OnTimer, но дефектный fixture с двумя FAR не создаётся текущим main. Из fail-counterexamples нет доказанного пути к реальному исполнению.
''','Docs')
 md('ECONOMIC_CONSERVATION', '''# AUDIT 02 — денежные границы и сохранение

## Слои и authority

| Величина | Основание | Что не доказывает |
|---|---|---|
| ProjectedBasketNet | Quotes, proposed positions, cost model | Actual deal/funding |
| ProjectedCloseNowNet | Close-side Bid/Ask, costs, open positions | Реальный fill |
| ActualRealizedDealNet | Profit+Swap+Commission+Fee фактических deals | Полноту history/право harvest |
| ReconciledEconomicNet | Independent history + EA-origin mapping + component equality | Распределение/остаток источника |
| EligibleSourceGrant | Approved role/policy + positive posted reconciled source | Свободный Reserve |
| AvailableReserve | Grant reconciliation + consumed/reserved owners + complete journal | Durable/concurrent proof само по себе |

Отсутствие provider/history не ноль: UNAVAILABLE. Локальные production DTO-флаги projected/runtimeConfirmed/sourceReconciled не являются независимой broker authority. Whole-chain conversion и global ledger в production отсутствуют.

## Инварианты кандидата, не утверждение владельца

`G=C+R+F`, `RemainingGross=R+F`, `C,R,F>=0`. Reserve d: `(R,F)→(R+d,F-d)` при d<=F. Release owner d: `(R,F)→(R-d,F+d)`. Unreserved consume: `(C,F)→(C+d,F-d)`. Owner reserved consume: `(C,R)→(C+d,R-d)`. Все операции сохраняют G. Free не равно RemainingGross при R>0. `PREPARED sum grants+Unallocated=Eligible`; spending запрещён. `COMMITTED sum grants=Eligible,Unallocated=0` — pending D-01. ResidualHeld и Unallocated не расходуются без policy.

Проверки `HSBI_FULL_SYSTEM_AUDIT_02_ledger_tests.py` используют новый независимый integer-minor-unit fixture: 22 literal сценария funding/reserve/release/consume/replay/reconstruction; каждый отказ/NO_OP проверяет before==after. Это specification model одного source-level pool с immutable allocation vector, **не полная реализация отдельных spendable buckets**. Модель не импортирует production. Её PASS не доказывает production, broker, durable или concurrent свойства. Snapshot reconstruction подтверждает только accounting равенства по доверенному fixture, не историческую eligibility.

## Полная стоимость и контрпримеры

В точных rational fixtures учтено: positive Harvest +3.83 при CyclePnL -1.64; Balance1003.46 и Equity998.46 при стартовом1000; Small+10/Big-20; Big+20/Small-30; FarLoss50/Reserve30; Profit2 Commission-2 Swap-1; gap100→110 при step5 не доказывает два fill; текущий loss0 после -15,+100 не отменяет peak15>cap12. Opening commission .37 и future Far exit .10 не смешиваются с уже realised Harvest. Формула `CyclePnL=RealizedNet+UnrealizedCloseNowNet` верна лишь при согласованном учёте будущих costs. Reserve/allocation второй раз к PnL не добавляются.

Частичное закрытие Far с сохранением basket улучшает локальный slope, но дальнейшее закрытие Trend/Core может ухудшить exposure. Поэтому partial Far не гарантирует recovery geometry после всей последовательности. Например C1,T1,S.5,F1 slope.5; после Far.2 close и Trend1 close slope=-.3. Полный actual execution этого примера не выполнялся.

Local validator проверяет форму/суммы, но не global uniqueness одного broker deal в нескольких allocations, complete history, owner journal, restart/CAS. Production preservation не доказывает сохранение экономических средств. Global funding остаётся UNPROVEN.
''','Docs')
 md('NATIVE_READINESS', '''# AUDIT 02 — native readiness и инструкция Windows

Свежий поиск PATH и каталогов `/opt`, `/workspace`, `/usr/local/bin` сохранён в `Tests/Evidence/HSBI_FULL_SYSTEM_AUDIT_02_NATIVE_ENVIRONMENT_FRESH.json`. Ни MetaEditor, ни MT5, ни Wine не найдены в этой ограниченной области. Это не поиск всех файлов машины.

MQL5_COMPILE=NOT_RUN
MQL5_NATIVE_TESTS=NOT_RUN

Минимальный неторговый Script: `Tests/Reference/HSBI_FULL_SYSTEM_AUDIT_02_native.mq5`. Он подключает реальные headers; проверки equality/vector/domain. Нет OrderSend/CTrade/History/AccountInfo/WebRequest/persistence. Пакет не содержит полного native покрытия 10 P0: нужны ещё Reserve/NewFar/context/nonfinite vectors. Непроверенная компилируемость и неполнота native пакета — открытые работы, не PASS.

На отдельной Windows-среде владельца:

1. Сверить SHA baseline и хеши source/harness, сохранить версию MetaEditor. Использовать изолированную копию всего HSBI с относительными include.
2. Запустить фактически установленный `MetaEditor64.exe /compile:"<HSBI>\\Tests\\Reference\\HSBI_FULL_SYSTEM_AUDIT_02_native.mq5" /log:"<audit-output>\\HSBI_FULL_SYSTEM_AUDIT_02_compile.log"`. Сохранить process exit, compiler diagnostics/warnings и SHA каждого входа. Exit0 сам по себе не заменяет compiler log.
3. Только после успешной компиляции запустить этот неторговый Script в изолированном терминале без связи с реальным счётом, без автоторговли и без подключённых других EA. Не запускать production EA для проверки исполнения.
4. Сохранить все строки `AUDIT02|TestID|PASS/FAIL`, итог FAILURES, версию терминала, UTC, source hashes. FAIL неизменённого source ожидаем; не исправлять expected для получения PASS. В MQL Script Print FAIL не гарантирует ненулевой terminal process exit — нужны оба вида результата.
5. До production-приёмки добавить native NaN/Infinity/domain/ulong overflow, SourceKey/29-field equality/codec fixtures, full main compile и реальный MQL version-specific результат.

Python Fraction и LP64 C++ extraction не подменяют эту процедуру. Нет доказательства native ABI, double canonicalization, terminal string/UTF8 или broker calculations. Не предпринимать сетевые/account operations для аудита.
''')
 md('R1_1_READINESS', '''# AUDIT 02 — Minimal R1.1 readiness

R1_1_START_ALLOWED=NO
PRODUCTION_REMEDIATION_ALLOWED=NO

Единственный proposed production allowlist: `Include/Money/HSBI_EconomicLedgerTypes.mqh`. Все прочие Include/main/runtime/persistence/execution запрещены. Сейчас **нет** разрешения менять даже этот header.

Кандидат source namespace `(Broker,Server,AccountLogin,DealTicket)` не включает Magic/Cycle: их изменение при том же source key конфликт payload, а не новая прибыль. Broker — стабильная независимая namespace binding, не автоматически имя company. Broker history даёт Deal/Order/Position/Symbol/Magic/Entry/Type/Time/Volume/Price/Profit/Swap/Commission/Fee; HSBI Cycle/Action/Event/Role/Plan/Policy требует независимого EA-origin journal. DealNet derived; его equality не заменяет полные компоненты. Currency/precision — account/provider, не SYMBOL_DIGITS.

Предложенный 29-field envelope и точные acceptance rows: `Tests/Contracts/HSBI_FULL_SYSTEM_AUDIT_02_R1_1_ACCEPTANCE.json`. Это review R0G, не утверждение всех29 полей универсально минимальными. Required/unknown факты должны быть различимы и не получать fabricated default. Unknown legacy/history/source namespace → UNAVAILABLE, malformed → REJECT, same full source/payload → NO_OP, altered same key → CONFLICT, NEW лишь complete independently reconciled registry absence. NEW_IDENTITY не funding.

Canonical numeric boundary: captured finite binary64 immutable observations отдельно от posted integer-minor-unit amounts. Для F64Z-1 нужны fixed field order, version, exact UTF8 lengths, signed/unsigned encoding, zero normalization и finite-only goldens. F64Z пока PROPOSED. Не округлять raw observation в posted факт и не переносить Fraction в MQL. Native compatibility NOT_RUN.

One-file feasibility — условная: additive V2 structs/pure equality/status/codec helpers могут размещаться в одном header. Не доказана MetaEditor compile совместимость. Сохранение старого unsafe classifier как diagnostic-only не является исправлением старого financial caller. Перед разрешением нужен полный current callsite audit и явный выбор compatibility policy; external consumers не обнаруживаются одним rg. Реализация providers, reconciliation registry, durable funding и migration backend потребует отдельного расширенного scope — здесь не разрешена.

Положительные tests: full replay, independently confirmed new namespace, per-field equality. Negative: sameNet alteredcomponents, changed Magic/Cycle under same key, crossaccount source mismatch, unknown legacy/authority/currency/precision, nonfinite and boundaries, altered codec/schema, duplicate registry. На каждом отказе/no-op — zero delta. Native строгая компиляция основного EA и неторгового assertion harness обязательна до production acceptance.

Миграция: preserve old bytes/schema/digest; неизвестные records quarantine, не backfill текущим account. В Minimal не выполнять on-disk migration. Rollback: отдельный обратимый коммит, без persisted преобразований. Stop: недостающий approved contract, native failure/unavailable, необходимость второго production file, unexpected callsite или remote mismatch.

Семантические D-02/D-08/NUM-CODEC/MQL-DOMAIN/schema/compatibility прямо блокируют. D-01, D-03–D-07/CR-09/global funding не обязательно блокируют изолированную pure equality, но блокируют дальнейшее использование результата для funding/торговли. Даже готовый план и approved semantics не разрешают реализацию без отдельного задания.
''')
 # Each of16 proposals is explicitly visible to administrator with all original consequences.
 md('ADMIN_DECISIONS','# AUDIT 02 — 16 решений владельца (все AWAITING_ADMIN_APPROVAL)\n\nИсходные R0F строки являются proposed material, не действующей новой нормой. Указанные математические аргументы не заменяют runtime/broker evidence.\n\n'+ '\n\n'.join('## '+x['DecisionID']+'\n'+'\n'.join('- **'+k+'**: '+str(x.get(k,'')) for k in ['CurrentContract','Conflict','RecommendedChoice','AlternativeChoice','MathematicalJustification','Counterexample','ProductionImpact','MigrationImpact','RequiredEvidence','Dependencies','ShortApprovalStatement','ApprovalStatus'])+'\nAdministratorDecision: (не заполнено)' for x in decisions))
 # Frozen failure expectations left untouched; actual counts derived from stdout/evidence where available.
 regress=evidence('REGRESSIONS');regtable=[]
 for x in regress['Runs']:
  if x['ID']=='R7':
   passn=re.search(r'CLEAN_PASS=(\d+)',x['Stdout']);failn=re.search(r'CLEAN_FAIL=(\d+)',x['Stdout']);counts=(int(passn[1]) if passn else None,int(failn[1]) if failn else None)
  elif x['ID']=='R0':q=evidence('R0_REGRESSION');counts=(sum(bool(c['contractPass']) for c in q['nativeCases']),q['normativeMismatchCount'])
  elif x['ID'] in ['C1','C2']:q=evidence(x['ID']+'_REGRESSION');counts=(q['Pass'],q['Fail'])
  elif x['ID'] in ['R0F','R0G','R0H']:
   q=json.loads(x['Stdout']);counts=(sum(v[1] for v in q),sum(not v[1] for v in q)) if x['ID']=='R0F' else (sum(v['Result']=='PASS' for v in q),sum(v['Result']!='PASS' for v in q))
  else:counts=(None,None)
  regtable.append(dict(ID=x['ID'],ExitCode=x['ExitCode'],Pass=counts[0],Fail=counts[1],Classification=x['Classification'],Boundary='Runner own counts; reference contexts are executions, not independent scenarios'))
 a.save('REGRESSION_CLASSIFICATION',dict(Rows=regtable,R7FailIDs=[line.split('|')[0] for line in regress['Runs'][0]['Stdout'].splitlines() if '|FAIL|' in line],R8R10='Only SCOPE findings for3 R0H test MQL files; expected executed48/67, no missing cases. Existing audit02 untracked harness is not part of their tracked-history scope comparison.',Note='R7 includes stale status-key/marker/manifest checks; static acceptance FAIL is not independently a runtime defect. R0 extracted tests not native despite historical NATIVE label.'))
 a.save('TEST_RESULTS',dict(BaseSHA=a.BASE,FirstAttempt=dict(Pass=17,Fail=13),FreshOriginal=dict(Pass=initial['Pass'],Fail=initial['Fail'],Scenarios=len(initial['Rows'])),FreshExtended=dict(Pass=extended['Pass'],Fail=extended['Fail'],Scenarios=len(extended['Rows'])),Rational=dict(Pass=math['Pass'],Fail=math['Fail']),Ledger=evidence('LEDGER_TESTS'),SourceMutations=dict(Killed=sum(v['Verdict']=='MUTATION_KILLED' for v in initial['Mutations']),Survived=sum(v['Verdict']=='MUTATION_SURVIVED' for v in initial['Mutations']),InfrastructureErrors=sum(v['Verdict']=='INFRASTRUCTURE_ERROR' for v in initial['Mutations']),Cases=initial['Mutations']),Regressions=regtable,InfrastructureErrorsNotHidden=True,Scope='Fresh original and extended tests overlap30 vectors; DO NOT SUM as68 independent scenarios. 6 mutations repeated on each build, not12 distinct. No MQL5 native evidence.'))
 # User's18 questions answered separately, with no unqualified PASS conclusion.
 answer=[('1–2. P0','9 независимо подтверждённых локальных source defects; FSA-010 классифицирован UNIMPLEMENTED independent authority, не доказан полный solver bypass. P0_UNVERIFIED=0 означает нет неклассифицированных строк, а не native доказательство всех10.'),('3–4. Достижимость','Все дефектные торговые контрпримеры не достигаются текущими OnInit/OnTick/OnTimer. OnTick вызывает запретительный stub. Диагностический FAR count достижим, но main не создаёт второй FAR. При будущей интеграции ошибки equality/funding/domain/role могут нарушить permission и учёт.'),('5–6. Формулы','23 условных real/rational утверждения разобраны алгебраически, 11 code/norm/proposal конфликтов,15 UNVERIFIED. F42 понижен относительно AUDIT01. Это не23 production proofs.'),('7–8. Деньги и funding','NO: exact specification подтверждает локальные partition-инварианты, production global registry/durable journal отсутствуют; exhaustion branch воспроизводит reserveGain40 из уже consumed50.'),('9–10. Harvest/FinalClose','NO: полного actual Harvest/FinalClose orchestration нет; positive Harvest не гарантирует positive cycle; fresh costs/positions/deals и threshold недостаточны без исполнения.'),('11–13. Far/recovery/loss','Только conditional N<F и q-теорема. Нет гарантии executable transitions/terminal close/верхней границы убытка при unrestricted unhedged Far. Broker min lot не zero residual.'),('14–15. FSM/native','Полный FSM не реализован. Нативные MetaEditor/MT5 проверки NOT_RUN; C++ и Python не подмена.'),('16–17. Minimal R1.1/owner','Начинать NO. Все16 решений остаются AWAITING_ADMIN_APPROVAL; непосредственно нужны D-02/D-08/NUM-CODEC/MQL-DOMAIN/schema и compatibility ballot, отдельное задание и native acceptance.'),('18. Полная торговая логика','После отдельного утверждения contracts, исправлений dependency chain economic→reconciliation→allocation→global source funding→durable/CAS→availability→risk/margin→full FSM и native/integration/broker validation. Срок и прибыльность из этих тестов не выводятся.')]
 final='''# HSBI FULL SYSTEM AUDIT 02 — итоговый независимый вердикт

**SYSTEM_CRITICAL_CONTRADICTIONS_FOUND. AUDIT_COMPLETENESS=PARTIAL.** Восстановление workspace успешно; это не означает полноту доказательства всей системы. Production и historical evidence не исправлялись, никакого исполнения нет.

## Recovery и воспроизведение

Найдены12 незакоммиченных файлов первой попытки и ignored Python bytecode; оригинальные bytes сохранены base64 в RECOVERY_ARCHIVE, inventory с size/hash/mtime в RECOVERY_INVENTORY. Синтаксическая целостность не означает завершённость. Первичная попытка архивирования пыталась читать .pyc как UTF8 и завершилась UnicodeDecodeError; архив после этого создан бинарно безопасным способом, все recovered bytes проверяются по hashes. Файлы первой попытки не удалялись. Перед дальнейшей правкой recovered runner сохранён в archive; новый extension вынесен отдельно.

Независимая проверка Git tree:1416 исходных файлов,74 production sources. SHA/blob/mode, а не счётчик, являются основанием preservation. Исторические файлы остаются frozen.

First-attempt30 исходных проверок воспроизведены:17 PASS/13 FAIL. Новый дополнительный набор расширяет их до38:19 PASS/19 FAIL (6 новых несовпадений и2 положительных). Это не68 различных сценариев. 13 исходных FAIL разобраны индивидуально:10 source-contract mismatches,2 policy conflicts,1 valid-flag contract UNVERIFIED; несколько относятся к одному FSA. Отдельный Money Infinity является source-дефектом даже при неопределённости valid flag.

23 новых literal rational vectors PASS;22 перехода независимого integer-minor-unit ledger fixture PASS;6 различных мутаций реальных comparator/ownership/domain операций обнаружены. Эти mutations проверяют сохранённые guards, не доказывают полноту missing guards. Базовый ошибочный source не стал безопасным. Все compiler/process exits/stdout/stderr в evidence; исключения не считаются kill.

C++ LP64 adapter glue и dependency ordering взяты из frozen AUDIT01, **не являются вторым независимым MQL implementation**. Новые fixtures/ожидания написаны отдельно. Для P0 примеров не вызываются broker-money/margin stubs; сравнения finite/NaN зависят от стандартной C++/IEEE семантики, native MQL остаётся границей. Полный NewFar solver не запускался.

## Результат по вопросам задания

'''+ '\n\n'.join('### '+q+'\n'+v for q,v in answer)+'''

## Исторические регрессии

R7 exit1:57 PASS/5 FAIL; R0 exit1:35 PASS/46 normative mismatches. R8 exit1 при48 выполненных cases и R10 exit1 при67: по одному SCOPE finding, перечисляющему3 R0H test-only MQL файла. Это scope-policy conflict, не новая functional regression. Frozen expectations не изменены. C1 840/840 executions, C2 1264/1264 и2462 schema probes; R0F116 actual Run calls, R0G128, R0H148 reference cases PASS. Полные реальные outputs/hashes сохранены. Это не fresh full replay каждого исторического mutation/package catalog.

## Оставшиеся работы — основание PARTIAL

1. Нет native MQL исполнения и all-domain адаптерной эквивалентности. Минимальный Windows harness не покрывает все10 P0; инструкции и limits раскрыты.
2. Полная normative event/precondition/action FSM всех timeout/retry/partial/out-of-order/restart combinations не формализована. Есть33×33 pure topology и phase-level manual map; это нельзя назвать full FSM verification.
3. P1/P2 static reclassification не заменяет нативные counterexample executions. FSA019/020/026 остаются UNVERIFIED; FSA023 OOB исследован статически, опасный вызов не исполнялся. Часть семантических связей требует решения владельца.
4. Нет полного proof→actual-deal→source-funding→allocation→durable-consumption composition и global/CAS/concurrent/broker evidence. Exact fixture не заменяет этот путь.
5. Source mutation каталог узкий:6 причинных проверок, не exhaustive mutation coverage всех29 issues/49 formulas. Условные теоремы не доказываются тестовыми совпадениями.

Пакет может быть опубликован как проверяемый частичный аудит после integrity/preservation проверки; завершённость полного системного аудита и готовность production не заявляются. Следующий шаг — независимое рассмотрение и owner decisions, без автоматического R1.1.

AUDIT_COMPLETENESS=PARTIAL
P0_CONFIRMED=9_SOURCE_DEFECTS
P0_UNVERIFIED=0_UNCLASSIFIED
P0_UNIMPLEMENTED=1
P1_CONFIRMED=8_SOURCE_OR_CONTRACT
P1_UNVERIFIED=3
P1_UNIMPLEMENTED=3
P2_CONFIRMED=5_SOURCE_OR_CONTRACT
FORMULA_VERIFIED=23_CONDITIONAL_MATHEMATICS
FORMULA_CONTRADICTORY=11
FORMULA_UNVERIFIED=15
MONEY_CONSERVATION_PROVEN=NO_PRODUCTION_PROOF
GLOBAL_FUNDING_PROVEN=NO
FULL_FSM_VERIFIED=NO
FULL_TRADING_CYCLE_VERIFIED=NO
PROFITABILITY_PROVEN=NO
LOSS_BOUND_PROVEN=NO
MQL5_COMPILE=NOT_RUN
MQL5_NATIVE_TESTS=NOT_RUN
ADMIN_APPROVAL_COMPLETE=NO
R1_1_START_ALLOWED=NO
PRODUCTION_REMEDIATION_ALLOWED=NO
TRADING_LOGIC_START_ALLOWED=NO
BROKER_DISPATCH_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
FINAL_SYSTEM_VERDICT=SYSTEM_CRITICAL_CONTRADICTIONS_FOUND
'''
 md('FINAL_VERDICT',final)
 print('BUILD',len(defects),'defects',len(formulas),'formulas',len(decisions),'decisions')
if __name__=='__main__':build()
