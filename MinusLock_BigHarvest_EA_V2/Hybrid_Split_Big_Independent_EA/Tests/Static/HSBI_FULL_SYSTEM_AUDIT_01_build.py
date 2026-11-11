"""Build new Russian audit reports/matrices from explicit judgments + real evidence.
Reports never approve policies or convert NOT_RUN/UNVERIFIED into PASS.
"""
import re,json,collections
from pathlib import Path
from fractions import Fraction
from decimal import Decimal,localcontext
import HSBI_FULL_SYSTEM_AUDIT_01_common as a
import HSBI_FULL_SYSTEM_AUDIT_01_knowledge as k

def esc(s):return str(s).replace('|','\\|').replace('\n','<br>')
def table(headers,rows):return '| '+' | '.join(headers)+' |\n|'+'|'.join('---' for _ in headers)+'|\n'+'\n'.join('| '+' | '.join(esc(x) for x in row)+' |' for row in rows)+'\n'
def write(name,body):(a.ROOT/'Reports'/(a.TAG+name+'_RU.md')).write_text('\n'.join(line.rstrip() for line in re.sub(r'\bFSA(\d{3})\b',r'FSA-\1',body).rstrip().splitlines())+'\n')
def fmt(value):
 try:
  v=Fraction(value)
  with localcontext() as c:c.prec=32;return str(Decimal(v.numerator)/Decimal(v.denominator))
 except (ValueError,TypeError):return str(value)
def owner(file):
 if file.startswith('Include/Core/'):return 'Docs/02_SYSTEM_ROLES_AND_IDENTITY_RU.md; Docs/06_STATE_MACHINE_SPECIFICATION_RU.md; Docs/18_MQL5_ARCHITECTURE_SPECIFICATION_RU.md'
 if file.startswith('Include/Planning/'):return 'Docs/04_MATHEMATICAL_MODEL_RU.md; Docs/05_GEOMETRY_MODEL_RU.md; Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md; Docs/27_FUTURE_SMALL_SOLVER_RU.md'
 if file.startswith('Include/Money/'):return 'Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md; Docs/24_BROKER_MONEY_MODEL_RU.md; Docs/31_MONEY_PROOF_IDENTITY_RU.md; Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md'
 if file.startswith('Include/Risk/'):return 'Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md'
 if file.startswith('Include/Execution/'):return 'Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md'
 if file.startswith('Include/Persistence/'):return 'Docs/16_PERSISTENCE_AND_RESTART_RU.md; Docs/17_RECONCILIATION_AND_TERMINAL_SAFE_RU.md'
 if file.startswith('Include/Runtime/'):return 'Docs/HSB_2D_RUNTIME_INTEGRATION_RU.md; Docs/HSB_2D_TRANSACTION_BARRIER_RU.md'
 if file.startswith('Include/Scenarios/'):return 'Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md through Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md'
 return 'Docs/18_MQL5_ARCHITECTURE_SPECIFICATION_RU.md; Docs/21_PRODUCTION_READINESS_CRITERIA_RU.md'

def main():
 inv=a.load('INVENTORY');ref=a.load('REFERENCE');ex=a.load('EXTRACTED');math=a.load('MATH_TESTS');reg=a.load('REGRESSIONS');ds=k.defects();fs=k.formulas();counts=collections.Counter(r['Severity'] for r in ds);fcounts=collections.Counter(r['Status'] for r in fs)
 header='BASE_SHA='+a.BASE+'\n\nРежим READ-ONLY ANALYSIS + AUDIT/TEST-ONLY. Источники не изменены. **AUDIT_COMPLETENESS=PARTIAL.** Native MQL5/MT5/broker/durable execution NOT_RUN. Proposed R0A–R0H не становятся нормативом из-за тестовых PASS. Все административные разрешения остаются NO.\n\n'
 meta=a.meta(__file__);scopes='`STATICALLY_INSPECTED`, `REFERENCE_EXECUTED`, `EXTRACTED_CPP_SUBSET_EXECUTED_NOT_NATIVE`, `HISTORICAL_EVIDENCE_ONLY`, `NOT_RUN`, `UNVERIFIED` не взаимозаменяемы.\n\n'
 risks=[
 dict(RiskID='UR01',Title='Global economic funding',Source='Docs/08:12,24; R0F FUNDING',Reason='Нет глобального unique source/allocation/account registry с фактическими opening/closing/foreign debits. Один локальный валидатор не доказывает conservation across allocations.',Status='UNVERIFIED'),
 dict(RiskID='UR02',Title='Broker execution, posted precision, actual costs/margin',Source='Docs/24:5-11; Docs/15:9',Reason='OrderCalc wrappers не исполнялись в MT5; currency conversion, tiers, netting/hedging, margin calls, swap/fee timing и posted policy неизвестны.',Status='UNVERIFIED'),
 dict(RiskID='UR03',Title='Loss bound/profitability',Source='Docs/04:12,33-36; SCENARIO-BIG_PROFIT_SMALL_LOSS',Reason='Нет market/stochastic assumptions/backtest. Положительный Harvest не обеспечивает положительный full-cycle PnL; gaps/remaining short liability не ограничены моделью.',Status='UNVERIFIED'),
 dict(RiskID='UR04',Title='Cycle termination/liveness',Source='Docs/05:25; Docs/13:12; FutureSmallSolver:144',Reason='Сужение Far по успешным transitions не гарантирует приход нужных цен, доступность маржи, исполнения или закрытие terminalFar. Flat/adverse path может не завершить recovery.',Status='UNVERIFIED'),
 dict(RiskID='UR05',Title='Durable/concurrent exactly-once',Source='Docs/16; PersistenceInterface:5-7',Reason='Нет реального backend/CAS/locks/crash/restart provider. Boolean historyUnchanged не доказывает долговечность.',Status='UNVERIFIED'),
 dict(RiskID='UR06',Title='Native MQL5 compatibility',Source='Docs/20:HSBI-TEST-001..003; R0H harness',Reason='Нет MetaEditor/MT5, compile/runtime/byte/golden/out-of-memory evidence. C++ адаптер не замена.',Status='UNVERIFIED'),
 dict(RiskID='UR07',Title='Risk/margin/source snapshot identity across candidate levels',Source='FutureSmallSolver:83-90,127; NewFarSolver:77',Reason='RuntimeConfirmed/evaluatedRisk/snapshotId принимаются от вызывающего слоя. Independent provider/candidate-specific reconciliation отсутствуют; self-consistent flags не proof.',Status='UNVERIFIED'),
 dict(RiskID='UR08',Title='Coverage beyond reviewed owner contracts',Source='INVENTORY.json Docs/TestFiles; COVERAGE.json',Reason='Все133 документа проиндексированы, но не каждая историческая таблица/qualification oracle повторно семантически проверена;279 test scripts не все выполнены;137 expression sites не все выделены в атомарные формулы.',Status='UNVERIFIED'),
 dict(RiskID='UR09',Title='Actual reconciliation and authority authenticity',Source='Docs/07; Docs/17; MoneyProofIdentity:10',Reason='Нет actual position/order/deal reader и producer origin association journal; nonzero IDs/flags не подтверждают наличие/принадлежность сделки.',Status='UNVERIFIED')]
 a.save('DEFECTS',dict(meta,Rows=ds,SeverityCounts={s:counts[s] for s in ('P0','P1','P2','P3')},UnverifiedRisks=risks,CountMethod=str(len(ds))+' issue entries: confirmed source defects + explicit normative conflicts/unimplemented components/proof obligations; not that many live/native exploits. P0 latent behind disabled dispatch.'))
 primary=[d for d in inv['Docs'] if re.match(r'Docs/\d\d_',d)];fullowners=[p for p in primary if not p.startswith(('Docs/19_','Docs/21_','Docs/22_'))]
 manual_sections=[];doc03=(a.ROOT/'Docs/03_FULL_SYSTEM_MANUAL_RU.md').read_text().splitlines();status_by={'Полный цикл':'UNIMPLEMENTED','Роли и направления':'PARTIALLY_VERIFIED','Объёмы и три закона':'CONTRADICTORY','Typed control prices':'PARTIALLY_VERIFIED','CandidatePlan и Future Small':'CONTRADICTORY','NewFar':'CONTRADICTORY','Money и allocation':'CONTRADICTORY','Partial Far':'UNIMPLEMENTED','Transition Loss':'PARTIALLY_VERIFIED','Final Close':'UNIMPLEMENTED','Small confirmation':'UNIMPLEMENTED','Transaction, retry и timeout':'UNIMPLEMENTED','Risk, margin и emergency':'CONTRADICTORY','Scope, persistence и REAL_LIMITED':'UNIMPLEMENTED','Restart/error semantics':'UNIMPLEMENTED'}
 for i,line in enumerate(doc03,1):
  if line.startswith('## '):
   end=next((j for j in range(i,len(doc03)) if doc03[j].startswith('## ')),len(doc03));title=line[3:];manual_sections.append(dict(Section=title,SourceFile='Docs/03_FULL_SYSTEM_MANUAL_RU.md',Line=i,EndLine=end,Assertion=' '.join(s for s in doc03[i:end] if s.strip()),Verdict=status_by.get(title,'UNTESTED'),CodeOwner='See owner chapter/module matrix; not whole-cycle implementation',Evidence='EXTRACTED.json, REFERENCE.json, state/call matrices',Boundary='Owner specification vs actual source; PARTIAL/UNIMPLEMENTED are not native PASS'))
 reqrows=[]
 def state_for_doc(p):
  if p.startswith(('Docs/09_','Docs/10_','Docs/11_','Docs/12_','Docs/13_','Docs/16_','Docs/17_')):return 'UNIMPLEMENTED'
  if p.startswith(('Docs/08_','Docs/14_','Docs/15_','Docs/29_','Docs/30_','Docs/31_','Docs/32_')):return 'CONTRADICTORY'
  if p in fullowners:return 'PARTIALLY_VERIFIED'
  return 'UNTESTED'
 for p in primary:
  section=''
  for n,line in enumerate((a.ROOT/p).read_text().splitlines(),1):
   if line.startswith('#'):section=line.lstrip('# ');continue
   if not line.strip() or line.startswith(('Версия','> **Граница','|---','```')):continue
   reqrows.append(dict(RequirementID='DOC-'+Path(p).name.split('_')[0]+'-L'+str(n)+'-'+str(len(reqrows)+1),SourceFile=p,Line=n,Section=section,Text=line,CodeOwner=owner('Include/'+('Money/' if p.startswith(('Docs/08','Docs/24','Docs/31','Docs/32')) else 'Planning/' if p.startswith(('Docs/04','Docs/05','Docs/14','Docs/27','Docs/28','Docs/29','Docs/30')) else 'Core/')),Status=state_for_doc(p),Evidence='Scoped functions/formulas/cases, not all assertions in this row are proved',ReviewBoundary='Primary owner reading' if p in fullowners else 'INDEXED historical traceability/status table; not semantic acceptance of every row'))
 modules=[];code_rows=[];exfiles={r['File'] for r in ex['Sources']};reachable=set(inv['ConservativeReachable'])
 for p in inv['Production']:
  functions=inv['Functions'][p];effects=[];text=(a.ROOT/p).read_text()
  if 'Print(' in text:effects.append('diagnostic Print')
  if 'TimeCurrent(' in text:effects.append('read server timestamp for diagnostics')
  if 'EventSetTimer(' in text:effects.append('terminal timer registration')
  if 'OrderCalcProfit(' in text or 'OrderCalcMargin(' in text:effects.append('calculation-only broker API; not executed in MT5')
  if p.endswith('HSBI_StateMachine.mqh'):effects.append('explicit Context state/revision mutation in pure apply helper')
  reached=[f['Name'] for f in functions if p+':'+str(f['Line'])+':'+f['Name'] in reachable]
  mode='ENTRY_REACHABLE_FUNCTIONS' if reached else 'INCLUDED_NOT_ENTRY_CALLED' if p in inv['MainIncludeClosure'] else 'DORMANT_LIBRARY_NOT_INCLUDED_BY_EA'
  modules.append(dict(File=p,SHA256=inv['Existing'][p]['SHA256'],Lines=inv['Existing'][p]['Lines'],Purpose='types/enums/contracts only' if not functions else ' / '.join(f['Name'] for f in functions),Input='Declared source DTOs/parameters (exact signature/source in INVENTORY Functions)',Output='Declared return DTO/status/bool/digest; full source retained',OwnerDocument=owner(p),Functions=[dict(Name=f['Name'],Line=f['Line'],EndLine=f['EndLine']) for f in functions],Dependencies=inv['Includes'][p],SideEffects=effects,EntryUse=mode,EntryFunctions=reached,CppBodyIncluded=p in exfiles,AdapterLimitation='ValidateJournalChain omitted from C++ adaptation' if p.endswith('HSBI_ExecutionJournal.mqh') else 'No native verification',NativeEvidence='NOT_RUN',DefectIDs=[d['DefectID'] for d in ds if d['SourceFile']==p],ReviewStatus='STATICALLY_INSPECTED',NotClaimed='No file-level native correctness or complete function test coverage inferred from file existence/adapter compilation'))
  for f in functions:code_rows.append(dict(File=p,Function=f['Name'],Line=f['Line'],OwnerDocument=owner(p),ReachableFromEA=f['Name'] in reached,StaticCalls=f['Calls'],DefectIDs=[d['DefectID'] for d in ds if d['SourceFile']==p and f['Line']<=d['SourceLine']<=f['EndLine']],NativeStatus='NOT_RUN',FunctionalEvidence='Specific EXTRACTED cases only; compilation of helper definitions not execution of every function'))
 a.save('REQUIREMENT_MATRIX',dict(meta,ManualSections=manual_sections,Rows=reqrows,CodeToRequirement=code_rows,ModuleReview=modules,AllowedVerdicts=['VERIFIED','PARTIALLY_VERIFIED','CONTRADICTORY','UNIMPLEMENTED','UNTESTED','UNSPECIFIED','NOT_APPLICABLE'],AuditCompleteness='PARTIAL'),'Tests/Contracts')
 a.save('FORMULA_MATRIX',dict(meta,Rows=fs,StatusCounts=dict(fcounts),RawSourceExpressionSites=inv['FormulaSites'],Method='49 semantic formula/contract families;137 lexical arithmetic/comparison/string-expression sites. Not137 independent financial formulas, not exhaustive atomic-expression proof. Raw sites individually remain UNVERIFIED unless scoped evidence cited.',NativeVerifiedCount=0),'Tests/Contracts')
 kinds=[x for x in ref['Properties'] if x['Sample']==0];invstatus={'CONSERVATION':'CONTRADICTORY','DOUBLE_FUNDING':'UNVERIFIED','REPLAY_IDENTITY':'CONTRADICTORY','SOURCE_NAMESPACE':'CONTRADICTORY','NO_FALSE_NOOP':'CONTRADICTORY','UNAVAILABLE_NOT_NEW':'UNVERIFIED','ATTRIBUTION':'PARTIALLY_VERIFIED','COST_COVERAGE':'UNVERIFIED','LOT_LIMITS':'CONTRADICTORY','SIGNED_EXPOSURE':'PARTIALLY_VERIFIED','BALANCE_EQUITY':'UNVERIFIED','AFFORDABILITY':'CONTRADICTORY','FSM_COMPLETION':'CONTRADICTORY','NO_HIDDEN_RESERVE':'PARTIALLY_VERIFIED','SNAPSHOT_BINDING':'UNVERIFIED'}
 invrows=[dict(InvariantID=r['PropertyID'],MathematicalPositive=r['Positive'],MathematicalNegative=r['Negative'],LiteralExpected=[True,False],Seed=20261111,DistinctInputPairs=sum(x['PropertyID']==r['PropertyID'] for x in ref['Properties']),ModelStatus='REFERENCE_EXECUTED_PASS',MutationID='PROPERTY-MUT-'+r['PropertyID'],ProductionSystemStatus=invstatus[r['PropertyID']],Boundary='Abstract acceptance predicate/fixture; no actual backend/orchestration or broker proof',Evidence='REFERENCE.json#Properties[PropertyID='+r['PropertyID']+']') for r in kinds]
 a.save('INVARIANT_MATRIX',dict(meta,Rows=invrows,ModelNotProduction=True),'Tests/Contracts')
 et=(a.ROOT/'Include/Core/HSBI_Enums.mqh').read_text();names=[x.strip().split('=')[0] for x in re.search(r'enum HSBI_State\{([^}]+)\}',et)[1].split(',')];edges=ex['FSMEdges'];topology={0};changed=True
 while changed:
  new={e['To'] for e in edges if e['Allowed'] and e['From'] in topology};changed=not new<=topology;topology|=new
 cycle=[('INITIAL_PLAN_READY','INITIAL_OPENING_BUY'),('INITIAL_OPENING_BUY','INITIAL_OPENING_SELL'),('INITIAL_OPENING_SELL','INITIAL_LOCK_ACTIVE'),('INITIAL_LOCK_ACTIVE','INITIAL_PLUS_CLOSING'),('INITIAL_PLUS_CLOSING','FAR_ACTIVE'),('FAR_ACTIVE','CANDIDATE_PLANNED'),('CANDIDATE_PLANNED','BASKET_OPENING_CORE'),('BASKET_OPENING_CORE','BASKET_OPENING_TREND'),('BASKET_OPENING_TREND','BASKET_OPENING_SMALL'),('BASKET_OPENING_SMALL','BASKET_ACTIVE'),('BASKET_ACTIVE','BIG_HARVEST_PLANNED'),('BIG_HARVEST_PLANNED','BIG_HARVEST_EXECUTING'),('BIG_HARVEST_EXECUTING','ALLOCATION_PENDING'),('ALLOCATION_PENDING','FINAL_CLOSE_PLANNED'),('FINAL_CLOSE_PLANNED','FINAL_CLOSE_EXECUTING'),('FINAL_CLOSE_EXECUTING','CYCLE_CLOSED')];sequence=[]
 for src,dst in cycle:
  ii=names.index('HSBI_STATE_'+src);jj=names.index('HSBI_STATE_'+dst);allowed=next(e['Allowed'] for e in edges if e['From']==ii and e['To']==jj)
  sequence.append(dict(From=src,To=dst,LibraryTopologyAllowed=allowed,ActualEAExecution='UNIMPLEMENTED',InputRequirement='Independent market/history/ownership/plan, risk/money/broker proof, actual fill+durable settlement before transition',ExpectedMutation='Positions/ledger/state only after authoritative action completed; details owner docs',ReplayRequirement='Exact verified receipt NO_OP, altered CONFLICT',RestartRequirement='Persisted journal+broker reconciliation; NOT_IMPLEMENTED'))
 failure=[dict(Event=event,Required=required,Current=current,Status=status) for event,required,current,status in [
 ('ACCEPTED/PLACED','PENDING notcomplete','types+completed barrier only','PARTIALLY_VERIFIED'),('PARTIAL_FILL','block nextrole; accumulate actualdeals','barrier rejectsPARTIAL; accumulator absent','PARTIALLY_VERIFIED'),('REJECT/REQUOTE/PRICE_CHANGE/CANCEL','typed noadvance/reconcile','no real retcode mapper/request engine','UNIMPLEMENTED'),('TIMEOUT/UNKNOWN/DISCONNECT','neither failure norcomplete; history lookup','barrier requiresCompleted; lookup/retryengine absent','UNIMPLEMENTED'),('DUPLICATE_IDENTICAL','verified immutable NO_OP zero delta','ledger/journal duplicate helpers incomplete','CONTRADICTORY'),('ALTERED_REPLAY','CONFLICT','ledger/journal falseNOOP counterexamples','CONTRADICTORY'),('OUT_OF_ORDER','history idempotent reconciliation','eventId freshness blocksadvance; actualreconcile absent','UNIMPLEMENTED'),('RESTART/CORRUPTION','durable validate+history+safe fallback','PersistStub fails; DTO validators only','UNIMPLEMENTED'),('RISK/DUAL_FAR_CONFLICT','blockactions/manual/terminalsafe','sourcevalidators have NaN/cardinality gaps','CONTRADICTORY'),('EMERGENCY','liquidation separateauthority/noautoresume','generic enum/topology; no actual emergency engine','UNIMPLEMENTED')]]
 a.save('STATE_MATRIX',dict(meta,States=[dict(ID=i,Name=name,LibraryTopologyReachable=i in topology,ActualEAReachable=(i==0),PerStateRoleAndMoneyGuard='Only partial context/topology checks; not full documented contract') for i,name in enumerate(names)],Edges=edges,NormalSequence=sequence,FailureTransitions=failure,ActualEAStates=['HSBI_STATE_DISABLED'],Method='All33x33 direct source predicate outputs in C++ adapter, not native/run FSM; actual EA static callbacks never advance state'),'Tests/Contracts')
 coverage=dict(meta,AuditCompleteness='PARTIAL',MainManual='Docs/03_FULL_SYSTEM_MANUAL_RU.md',MainManualLines=51,MainManualReadFull=True,DocumentsIndexed=len(inv['Docs']),PrimaryOwnerDocuments=len(primary),PrimaryOwnerFullReadingScope=fullowners,HistoricalTablesNotFullySemanticallyReviewed=['Docs/19_REQUIREMENT_TRACEABILITY_MATRIX_RU.md','Docs/21_PRODUCTION_READINESS_CRITERIA_RU.md','Docs/22_OPEN_DECISIONS_REGISTER_RU.md','Other historical proposal/test-model appendices indexed, not all independently reaudited'],ProductionModulesIndexedAndStaticallyReviewed=74,ProductionDeclaredFunctions=len(code_rows),EntryIncludedModules=len(inv['MainIncludeClosure']),EntryReachableProjectFunctions=len(inv['ConservativeReachable']),ExtractedCppSourceHeaders=len(ex['Sources']),ExtractedCaseCount=len(ex['Rows']),ExtractedContractPass=ex['Pass'],ExtractedContractFail=ex['Fail'],FormulaFamilies=49,FormulaCounts=dict(fcounts),LexicalExpressionSites=len(inv['FormulaSites']),ExistingPythonTestScripts=len([p for p in inv['TestFiles'] if p.endswith('.py')]),FreshHistoricalRuns=len(reg['Runs']),ReferenceScenarios=20,DistinctPropertyInputPairs=ref['PropertySamplePairs'],PropertyFamilies=15,PropertyMutations=15,SpecMathVectors=len(math['Rows']),MQL5_COMPILE='NOT_RUN',MQL5_NATIVE_TESTS='NOT_RUN',BrokerExecution='NOT_RUN',DurableConcurrentRecovery='UNVERIFIED',ProofLimits=risks,NoOverallReadinessPercentage=True)
 a.save('COVERAGE',coverage)
 # PROJECT_INVENTORY / DOCUMENTATION_MAP
 write('PROJECT_INVENTORY','# Карта проекта HSBI\n\n'+header+f"Из Git tree baseline независимо получено **{len(inv['Existing'])} файлов**, production **74**, строки по splitlines **{inv['ProductionLineCount']}** (wc -l отличается для файлов без завершающего LF), определений функций **{len(code_rows)}**. Docs/root index **{len(inv['Docs'])}**, Reports **{len(inv['Reports'])}**, existing Python test scripts **{coverage['ExistingPythonTestScripts']}**. SHA256/blob/mode каждого baseline-file — INVENTORY/PRESERVATION.\n\n"+table(['Production module','Lines','Functions','EA use','Issues'],[(m['File'],m['Lines'],len(m['Functions']),m['EntryUse'],','.join(m['DefectIDs']) or 'No absence-of-defect claim') for m in modules])+'''\nОсновной вход Hybrid_Split_Big_Independent_EA.mq5:19/29/35/41. OnTradeTransaction отсутствует. Никаких input-параметров торгового профиля в main нет: конфигурация существует в DTO/документах, не в валидированном runtime loader. Functions/signatures/inputs/outputs/dependencies и line locators — REQUIREMENT_MATRIX.CodeToRequirement/ModuleReview и INVENTORY.Functions.

Все74 файла статически разобраны/рассмотрены; это не74 nativePASS и не покрытие всех веток. Только16 входят в main includeclosure,13 project functions консервативно достижимы из entry callbacks;58futureheaders не подключены главным EA. Included-but-uncalled отдельно от not-included; не предлагается автоматически удалить эти модули как deadcode. Подробная история и evidence индексируются отдельно HISTORICAL_INDEX, source/test inventory неизменны.
''')
 docs_table=[]
 for d in inv['DocumentIndex']:
  label='READ_FULL_OWNER_TEXT' if d['File'] in fullowners else 'INDEXED_HISTORICAL_STATUS_OR_PROPOSAL_NOT_FULLY_REAUDITED'
  docs_table.append((d['File'],d['Lines'],label,d['Headings'][0]['Text'] if d['Headings'] else 'noheading'))
 write('DOCUMENTATION_MAP','# Руководство и нормативная иерархия\n\n'+header+'''Найдено основное руководство `Docs/03_FULL_SYSTEM_MANUAL_RU.md`, все51 строки прочитаны. Это компактная схема, а не готовое operator handbook: подробности разнесены по00–32 owner-docs и historical/proposed amendments. Формальные источники владельцев не равны работающему implementation. Все133 документа проиндексированы с SHA256/headings/status locators;31 owner-текст прочитан целиком,19/21/22 и многие исторические appendices проиндексированы/выборочно сопоставлены, не повторно доказаны целиком.

Иерархия: явные пользовательские границы текущего задания > отдельные документированные административные решения в их scope > owner-contracts с явными amendments > historical acceptance только своего этапа > proposed R0A–R0H (AWAITING) > reference evidence/фактический code. Нельзя превратить code или PASS в экономический норматив. Docs23 CLOSED_FOR_HSB1_ARCHITECTURE не разрешает исправления/торговлю; OPEN_P0=0 относится к старому архитектурному срезу, не текущему source verdict.

Основные противоречия: minimum-safeN (03:21/14:22) против risk-first (29:3/code); allocation equality (08:12) и inequality/remaining+consumed (32:3) без typed phase/balance mapping; FarLossIncrease имя против absolute фактической величины; WORST_CASE maxTransitionLoss не предложенный minCatchUpMargin; thin3-field legacy equality против immutable economic identity; старые ManagedIdentity безAccount в02:20 против23:22/Core. Никакое изменение не утверждено этим аудитом. D01–D08/CR09/NUM/SNAP/funding остаются pending, complete/current authority package не доказан.

'''+table(['Document','Lines','Review boundary','Title'],docs_table)+'\n## Полный мануал: section traceability\n\n'+table(['Section / locator','Requirement / mechanism','Code & tests','Verdict'],[(s['Section']+' Docs/03:'+str(s['Line']),s['Assertion'],s['Evidence'],s['Verdict']) for s in manual_sections])+'''\nФормальная построчная карта owner-требований — REQUIREMENT_MATRIX.Rows. Статус PARTIALLY_VERIFIED не означает весь paragraphPASS. Именованные владельцы вроде TransactionEngine/FillAccumulator/FinalCloseCalculator/SnapshotStore во многих случаях существуют только в руководстве; source содержит DTO/stubs. Полнота operational parameters, account support, rounding/transition/buffer policies, emergency/recovery и proof providers не подтверждена.
''')
 # ARCHITECTURE
 write('ARCHITECTURE','# Архитектура и реальные пути выполнения\n\n'+header+scopes+'''## Два разных объекта аудита

Фактический EA — non-trading skeleton. Будущая HSBI — описанная в owner-документах система из planning/money/risk/execution/scenarios/persistence. Нельзя присвоить skeleton свойства всей проектируемой стратегии.

```mermaid
flowchart TD
 Init[OnInit: disabled policy] --> Ctx[InitializeContext: DISABLED]
 Tick[OnTick] --> Stub[SubmitActionStub: success=false]
 Stub --> Reason[lastReason only]
 Timer[OnTimer] --> Diag[Read context / Print diagnostics]
 Deinit[OnDeinit] --> Kill[Kill timer]
```

OnInit:21–26 проверяет policy и запрещённый dispatch, но не загружает positions/history или broker properties. Context после initialize имеет zero identity и не является production-ready context; это допустимо только для disabled skeleton. OnTick:37–38 не вызывает solver/risk/ledger/FSM. OnTimer:43 диагностирует; не подтверждает executions. OnTradeTransaction отсутствует. Поэтому реальная текущая FSM по этим callbacks остаётся DISABLED; manual cycle не исполняется.

## Объявленные библиотеки

Существуют real source bodies для broker-grid/cost/money/margin calculation, geometry, FutureSmall, NewFar, proof/ownership/runtime validators; economic/allocation records и сравнения; action/outcome/journal/snapshot DTO. Но producer actual MT5 history/account/EA-origin evidence, complete risk calculation и durable backend отсутствуют. `runtimeConfirmed=true` после OrderCalcProfit подтверждает лишь успешный расчёт, не Deal existence/actual profit/eligible funds.

```mermaid
flowchart LR
 Provider[Independent account/history/origin providers: absent] --> Econ[Economic immutable identity]
 Econ --> Reconcile[Reconciled actual posted economics]
 Reconcile --> Alloc[Authoritative allocation/consumption]
 Alloc --> Journal[Durable atomic journal/CAS: absent]
 Journal --> Available[Verified available reserve]
 Market[Typed market/cost/grid snapshots] --> Plan[Geometry / FutureSmall / NewFar]
 Available --> Plan
 Plan --> Risk[Runtime risk/margin proof]
 Risk --> Intent[Execution intent / preflight]
 Intent --> Engine[Transaction engine: absent]
 Engine --> Persist[Actual reconciliation + durable commit: absent]
 Persist --> FSM[Full guarded FSM: absent]
 FSM --> Scenario[Harvest / Partial / Final / Small scenarios: DTO only]
```

Это требуемая зависимость, не реализованный call graph. Fact include graph и function graph сохранены в INVENTORY; code-to-requirement matrix содержит199 definitions с path/line/calls. Лексический граф — overapproximation, не formal control-flow dominance proof. Для слоя Money есть зависимости на Planning/BrokerGrid и CandidateMoney→FutureSmall→Money, что усиливает coupling; header graph не равен доказанному бизнес-циклу и не утверждается compile cycle. Чистые DTO/common math логично выделять при отдельной архитектурной фазе, не расширяя MinimalR1.1 сейчас.

Execution/persistence validators принимают externally populated booleans/digests. Их проверка формы не создаёт независимую authority. Часть вспомогательных validators локально корректна при preconditions; обязательность caller и достоверность producer часто ещё не реализованы. Function presence, body compilation в adapter и root README acceptance не доказывают интеграцию.

Core Context cardinality охватывает лишь четыре слота: FSA009 показывает пропущенный secondFar в initialBuy. Pure FSM допускает arbitrary reconciliation escape, но нет orchestration/admin resume enforcement. Нужно различать library predicate и реальное применение после completed+persisted event.
''')
 # MATH
 write('MATHEMATICS','# Математические формулы, единицы и ограничения\n\n'+header+f"Выделено49 semantic families: **{fcounts['VERIFIED']} VERIFIED при указанных предпосылках**, **{fcounts['CONTRADICTORY']} CONTRADICTORY**, **{fcounts['UNVERIFIED']} UNVERIFIED**. Отдельно137 lexical source-expression sites (включают string/time/ID arithmetic), не137 независимых финансовых формул. Полная атомарная декомпозиция каждого site не завершена — одно из оснований PARTIAL. Native verified=0.\n\n"+table(['FormulaID / expression','Units/domain','Normative / code locator','Status / vector','Evidence / limit'],[(f['FormulaID']+' '+f['Expression'],f['UnitsAndDomain'],f['NormativeSource']+'; '+f['Source'],f['Status']+'; '+f['IndependentVector'],f['TestID']+'; '+f['ProofBoundary']) for f in fs])+'''
## Что алгебра действительно доказывает

При неизменных lots и общем линейном money-per-price коэффициенте: dRecovery/dP = C+T−S−F для FarSELL и зеркального favorable движения. Строго положительная slope — локальный directional filter. Она не доказывает favourable movement, достаточность equity/margin, отсутствие gaps, независимость costs, фактическую сделку или прибыль завершённого цикла. В source slope.19 проходит даже при Core0 (FSA011), то есть одного закона недостаточно для обязательной leg.

G=Cspent+Rreserved+Ffree, все>=0. Consuming a<=F даёт C'=C+a,F'=F-a,R'=R =>sum неизменна. Reserving r<=F даёт R'=R+r,F'=F-r; release делает обратное для того же owner. Это корректный abstract accounting invariant (15 seeded predicate families), но production имеет другую неполную MoneyState/Allocation форму и не реализует этот полный lifecycle. Cannot infer production money conservation from a correct equation.

Если для всех j существует доказанное F(j+1)<=qF(j),0<q<1, то F(k)<=q^k F0; K>=ceil(log(Vmin/F0)/logq) даёт достижение minimum-scale bound. Это условная теорема о successful transitions, не о времени, broker executions или закрытии позиции. Два первых значения .8,.64 не доказывают F3<=.512: допустимое без нового доказательства продолжение .64 нарушает bound. Source проверяет finite prefix/flags и terminal minlot, не общий tail-law/terminal-close affordability (FSA018/028).

Если выбрать worst level по argmax TransitionLoss, это не равно argmin(Reserve−Loss−Buffer). Два допустимых уровня: (Trans10,Reserve100,Loss90,Buffer1)->margin9; (Trans5,Reserve10,Loss20,Buffer1)->margin−11. Старый control выбирает1, all-level contract должен отклонить. Варианты политики требуют административного решения CR09/D04, не самовольной смены.

`SignedNet[-15,+100]=85`, current loss0; peak cumulative loss15; cap12 был нарушен на префиксе. Sticky/peak/current final отличаются. Prefix protection не позволяет задним числом отменить actual loss; reset/order/partial-fill policy не выбраны автоматически.

Raw signed DealNet sum в CostModel корректен на finite inputs. Allocation conservation/immutable equality не вытекают из равенства Net или суммы buckets: P50/C0 иP60/C−10 одинаковы по net, но разные immutable facts; Reserve50/PF0 иReserve0/PF50 одинаковы по total, но разные цели денег. Existing source возвращает identical для обоих (FSA001/002).

## Численная точность

Независимые spec vectors используют Fraction/integer и Decimal localcontext для маленького explicitly bounded .005+.005 примера. ROUND_HALF_EVEN здесь лишь один proposed profile: round aggregate=.01 vs sum rounded components=0.00. Это не политика реального брокера. Raw binary64 codec наблюдения не settled money; cents на1e28 неразрешимы в binary64. Python arbitrary integers/Fraction не native long MQL. Overflow/subnormal/locale/UTF8/codec ещё NOT_RUN в MetaEditor.

EXTRACTED uses actual selected source bodies with C++ adapters:54 checks,27 PASS,27 normative/integration expectation FAIL. Эти27 не27 уникальных live-exploits и не MQL runtime verdicts; scope каждого failure указан в defect register. Synthetic OrderCalcProfit линейный и margin=notional/100, не broker proof. Все20 independent spec vectors PASS; это проверка примеров/алгебры, не кода каждой production-формулы. Для14 UNVERIFIED families полного независимого runtime oracle нет; они не преобразованы в PASS.
''')
 # ECONOMIC
 scenariotable=table(['Scenario','Expected/actual balance','Equity','Gross / Net','Meaning'],[(r['TestID'],fmt(r['Actual']['Balance']),fmt(r['Actual']['Equity']),fmt(r['Actual']['GrossLot'])+' / '+fmt(r['Actual']['NetLot']),r['Meaning']) for r in ref['Scenarios']])
 write('ECONOMIC_MODEL','# Экономическая состоятельность и источники результата\n\n'+header+'''## Исходные допущения аналитического примера

Синтетический hedging unit-value symbol (1money на1price×1lot), tick1, unit leverage100 только для иллюстрации margin, quoted Bid/Ask, opening и closing commission0.1/lot; swap/fee0. Starting capital1000. FarSELL1@100, CoreBUY1.2@101, TrendBUY1@101, SmallSELL.5@100; opening commissions.37 =>Balance999.63. При Bid100/Ask101 floating−3.7, Equity995.93. Это не реальные broker values и не калиброванный forex backtest. Native trading отсутствует; команды fills заданы тестом, не вырабатываются EA.

Сценарии содержат initial positions/balance/equity, quotes/path, requested analytical fills, each status, final volumes/net/gross, realized/unrealized, liquidation PnL и remaining obligations в REFERENCE.json. `Meaning` — интерпретация fixture, не копируемое expected decision кода HSBI. Например BROKER_REJECT означает заданное отсутствие fills, не выполненный retcode engine. Partial scenario — arithmetic fill.4 и остаток.6, не доказанный MQL fill accumulator. Все20 accounting vectors совпали с независимыми literal balances/equities.

'''+scenariotable+'''
## Положительный Harvest при отрицательном цикле возможен

Bid104/Ask105. Core profit3.6 и Trend3, closing commission.22 =>BigNet6.38. Small close loss2.5 +commission.05 =>−2.55. После закрытия ВСЕХ C/T/S, как требует role contract, HarvestNet=3.83>0. Balance=999.63+3.83=1003.46. Remaining Far SELL1 has floating−5 =>Equity998.46. Ещё.10 закрытия Far =>full liquidation cycle PnL−1.64. Положительный realized Harvest и выросший balance не означают выросшую equity или прибыль полного цикла. Это не доказывает, что полный HSBI gate обязан разрешить такой Harvest/FinalClose; оно доказывает недопустимость использовать Harvest-only statistic как доказательство прибыльности. Корректный FinalClose threshold/coverage должен здесь отклонить recovery close.

При Bid90/Ask91 Small close приносит4.45, баланс1004.08, но оставшиеся Big losses дают equity988.88. Small-only income не становится автоматически BigReserve. В реальном source `reserveGainMoney=max(0,CoreNet+TrendNet+SmallNet)` — projected field: при Core−1/Trend−1/Small10 он равен8. Это НЕ доказанный actual grant; текущий отдельный ReserveSourceProof дополнительно требует Core/Trend role. Нужно устранить неоднозначность projected/actual/allocated/available и утверждать attribution, не объявлять любой projected field прямым funding.

## Перенос остаточного риска и отсутствие гарантии bounded loss

После Harvest остаётся ненулевая Far liability. Для оставшейся SELL-volume Q при росте price P прибыль остатка = Q*(open−Ask), то есть при P→∞ без исполнения нового хеджа/ликвидации loss не ограничен этой моделью. Initial fixed lots + bounded price interval дают лишь условный bound; ни допустимый диапазон рыночных gaps, ни guaranteed fills/negative-balance protection/stop-out price тут не доказаны. Реальный брокер может принудительно закрыть позиции раньше, но такой loss/price outcome не моделирован. Отсутствие гарантий не означает доказанную неизбежную убыточность на каждой траектории; означает LOSS_BOUND_NOT_PROVEN.

При favorable trend в fixture полное закрытие на110/111 даёт+2.56. Adverse slippage5 на каждой leg превращает тот же расчёт в−15.94 полного цикла (Balance984.06). При flat path trigger/exit может не прийти, а отрицательный carry при его наличии накапливается. Возможность нескольких последовательных recovery cycles не доказывает, что общая задолженность уменьшается после costs, капитал достаточен и cycle завершится.

Positive slope, compression, локальные rebates/закрытые profits не создают expected economic edge. Нет independent market dataset, sample protocol, out-of-sample/backtest, slippage model validation, реального inventory accounting или native lifecycle. Полный account PnL должен учитывать также excluded InitialProfit/opening costs/прочие account debits; recovery metric, который намеренно исключает InitialProfit, не полный strategy/account return.

Ответы на главные вопросы: positive Harvest с negative CyclePnL — да; positive Small/Big может скрывать loss других legs при partial metrics — да; Far liability может расти после закрытия прибыльных ног — условно да; риск бесконечного ожидания/капитальной недостаточности не исключён; положительный full-cycle return после всех costs и ограниченный убыток НЕ ДОКАЗАНЫ. `PROFITABILITY_NOT_PROVEN`, `LOSS_BOUND_NOT_PROVEN`. No empirical profitability estimate is fabricated.
''')
 # TRADING_CYCLE
 write('TRADING_CYCLE','# Торговый цикл, фактическая FSM и failure routes\n\n'+header+'''Реальные enum states — Core/Enums:8, не предложенная пользователем гипотезаINITIAL_STATE→LOSS_EVALUATION и т.п. STATES=33; extracted direct topology evaluated33×33=1089 pairs, это наблюдения predicate, не1089 независимых PASS. Фактический EA callback cycle остаётся DISABLED. Plan→Action→Persist→Request→OnTradeTransaction→actualledger→persist→FSM указан Docs03/07, но не реализован.

## Номинальная последовательность из owner-docs

'''+table(['From','To','Library topology','Actual orchestrator'],[(r['From'],r['To'],r['LibraryTopologyAllowed'],r['ActualEAExecution']) for r in sequence])+'''
После initial BUY partial/delayed исполнений нужен rollback при незавершённом SELL. Только actual closed INITIAL_PLUS создаёт Far с исходным identifier и exclusion; эти операции представлены контрактами, не runtime. Candidate C/T/S staged open, BigHarvest actual reconciliation, allocation, FinalClose before PartialFar затем newplan — отсутствующие scenario controllers. У Small: confirmation+debounce→immutable transition→closeSmall→oldFar→Trend→partCore→actual originalCore residual→revalidate/promote→newcycle; каждый шаг требует immutable origin/actual fills/durable receipt, не только requested volumes. Scenarios/*.mqh содержат структуры, не исполнение этих шагов.

## Failure matrix

'''+table(['Event','Normative route','Current scope','Verdict'],[(r['Event'],r['Required'],r['Current'],r['Status']) for r in failure])+'''
Pure FSM допускает self-loop, global Reconciling/TerminalSafe/Emergency targets и несколько early normal edges. CoreOpening→TrendOpening отсутствует. Reconciling→FarActive без admin parameter не доказывает no-auto-resume; будущий обязательный orchestrator должен это ограничивать. НаulongMAX proposedRevision unchecked. CurrentEA этот helper не вызывает, поэтому это latent library/implementation gap, не текущий авто-resume на реальном счёте.

Liveness: нет доказательства eventual trigger/fill/reconciliation/terminal affordability. Endless waiting возможно в спецификации при flat/stale/disconnect, однако текущий skeleton просто никогда не запускает цикл. Basket growth ограничивается лишь proposed limits/conditional proof; полная реальная bounded transition sequence не реализована. Duplicate/partial/unknown события типизированы, но engine/history accumulation отсутствуют; no missingdeal may be assumed completed. Full STATE_TRANSITION_MATRIX/FULL_CYCLE_SEQUENCE/FAILURE_TRANSITION_MATRIX — STATE_MATRIX.json.
''')
 # RISK
 write('RISK_ANALYSIS','# Риск, margin, drawdown и брокерская исполнимость\n\n'+header+'''## Что есть в коде

RiskInput/limits получают projected margin, margin level, free margin, cycle/account drawdown, gross exposure, managed count, worst-case/transition loss, spread и snapshotFresh. `HSBI_ValidateRiskInput` сравнивает их с limits, но не проверяет finite/domain. NaN projectedMargin проходит. `HSBI_EvaluateNewFarGates` проверяет некоторые next/cap values, но не все baseline/allowed inputs; allowedMargin=NaN проходит. Transaction volume/price NaN также может дать completed в extracted source. Исправления нужны до присоединения любой из этих библиотек к trading entry.

`OrderCalcMargin` wrappers fail UNAVAILABLE при API failure и проверяют finite/nonnegative returned margin. Это правильная локальная защита; фактическая маржа портфеля/hedging/account tier/leverage/free margin/stop-out не следует из суммы standalone margin четырёх ног. Risk runtime proof — externally supplied numeric value+sourceflags, не реализованный независимый adverse-control calculation/provider.

Неизвестная оценка !=0. При missing broker history/unsupported calculation mode/unknown currency/precision нельзя выдавать spendable source или riskPASS. Current actual-provider/CAS/settled-ledger отсутствуют, поэтому общесистемный риск UNVERIFIED даже при flags fresh/runtimeConfirmed.

## Диапазоны и account model

Нормативные проценты0..100, tolerance>=0, finite money и positioncount>0 требуют централизованного валидированного config. Main вообще не имеет input trading parameters/configloader. Нет gate ACCOUNT_MARGIN_MODE: same-symbol independent long/short legs требуют hedging или иной virtual-ledger architecture, не реализованной для netting. Начальный BUY1/SELL1 в netting не оставляет два независимых positions. Broker-specific tickValueProfit/Loss, currency conversion, asymmetric tick values, StopsLevel/FreezeLevel/order modes/SLTP constraints необходимо определить до execution. Сейчас dispatch отсутствует: эти пути не тестировались, нельзя объявить их корректными или все одинаково applicable.

## Нереальные гарантии

Stop-loss/emergency budget/Transition cap на projected values не гарантируют исполнение в пределах cap после gap/timeout/slippage. В fixture planned liquidation+2.56 переходит в−15.94 при adverse5 на всех fills. Source imperative emergency liquidation отсутствует: enum/terminal-safe metadata не закрывают позиции. Пользоваться этим skeleton как защитным EA для уже открытого счёта нельзя — он не читает/не ведёт/не ликвидирует позиции.

Нет математического risk bound без ограничений рыночного пути, исполнения, кредитного плеча, broker forced-liquidation/negativebalance policy и validated capital budget. Нет статистических trading-strategy доказательств. Partial prefix −15 при cap12 уже breach, даже если позже+100; A/B/C/reset/sticky semantics ждут администратора. Margin call/stop-out response и partial-fill actual loss reconciliation остаются UNIMPLEMENTED/NOT_RUN.

Сценарий LOW_MARGIN и более неблагоприятные quote paths проверяют accounting arithmetic, не broker margin/order acceptance. Все bridge/proxy flags — тестовые допущения. Safety current verified static: runtime disabled, brokerDispatch false, no sending paths; functional trading safety НЕ доказана.
''')
 # CODE_REVIEW
 write('CODE_REVIEW','# Production code review по всем74 модулям\n\n'+header+scopes+'''Метод: full source indexing, чтение/рассмотрение source contracts и entry/caller wiring, conservative include/call graphs; выбранные реальные bodies в C++adapter. Это не MetaEditor compilation всех headers и не proof every branch. Source inventory/тексты всех199 definitions с line locators доступны в INVENTORY.Functions; code-to-requirement bindings в REQUIREMENT_MATRIX.CodeToRequirement. Компиляция неиспользованного helper в adapter не означает его фактический вызов.

'''+table(['File','Purpose / functions','Dependencies','Side effects','Evidence / issues'],[(m['File'],m['Purpose'],'; '.join(m['Dependencies']),'; '.join(m['SideEffects']) or 'pure data/local calculation; no declared account writes',('CPP bodies included, not all called; ' if m['CppBodyIncluded'] else 'static only; ')+','.join(m['DefectIDs'])+'; nativeNOT_RUN') for m in modules])+'''
## Существенные межслойные проблемы

1. Ledger equality/source key не immutable economic identity. Allocation equality по total не preserving bucket intent. ValidateAllocation допускает negative buckets/partial sum; MoneyState ignoresvalid/revision/infinity.
2. Reserve consumption key не связан с allocation keys. Unallocated branch может повторно задействовать known spentsource. Это calculator permission, не executedconsumption; самой apply/backend реализации нет.
3. NewFar proof identity создаётся из input/descriptors и expected копируется из проверяемого объекта. Helper совпадения корректно сравнивает выданный expected, но этот caller не доказывает его независимость; nonzeroDeal не existence. No actual broker origin/economic reconciliation reader.
4. FutureSmall compares net Big against prior gross; optionalTrend0 crosses geometry but fails money layer; Corezero may pass geometry then fail other mandatory money wrappers. Не объявлять это существующим successful whole-solver обходом.
5. Runtime validators и restart принимают provenance/completeness/confirmedflags от ещё отсутствующего producer. Data/digest shape≠independentauthority. Durable chain/atomicity не реализованы.
6. Journal duplicate classifier возвращает NO_OP по IDs+presented currentDigest до проверки связи с changed payloadDigest. Native source scopes в FSA027: zero ledger write не оправдывает false identical classification.
7. Main callbacks не используют эти финансовые modules. Только16mainincludes/13projectfunctions reachable. Поэтому current no-trade safety объясняется отключённым skeleton, а не завершённой системой risk/ledger controls.

Дополнительно: input bounds должны проверяться до digest loops, maximumDepth129 может выйти за128 arrays в NewFarTemplateDigest до downstream validation. Native memory failure/OOB test NOT_RUN; это статическая validation-order находка. Price freshness допускает futuretimestamp; native uint revision overflow guards отсутствуют. Policy choice и broker clockskew требуют explicit contract, не arbitrary imposed production defaults.
''')
 # HISTORICAL_DEFECTS
 hist=[('L01','FSA001','OPEN','full-component equality unchanged; direct source counterexample'),('L02','FSA002','OPEN','bucket permutation still identical'),('M01','FSA003/FSA004','OPEN','foreign keys and exhausted source permission'),('M02','FSA010','OPEN','caller copies/reconstructs expected identity, no independent reconciliation record'),('M05 Small contribution','D03/projection scope; BasketMoney:17','OPEN','ReserveSourceProof role filter exists; projected Basket field includesSmall. Not actualgrantproof; attribution/globalfunding unresolved'),('ZeroCore/minlot','FSA011/FSA029','OPEN','geometry acceptsCore0/belowmin; Trend0 integration false-reject'),('CR09','FSA015','BLOCKED','maxTransition !=minCatchUp; adminpolicy needed'),('snapshot/provenance','FSA013 +UR05/09','BLOCKED','DTO/flags/stringdigest not durable/authentic provider'),('durable/concurrent recovery','FSA013','BLOCKED','productionstub, noCAS/crash tests'),('codec/MQL5 compatibility','FSA026','BLOCKED','R0H Python148PASS, noMetaEditor'),('legacy caller compatibility','FSA001/010','BLOCKED','V2 API proposed; legacy financial callers not safely migrated'),('historical R7/R0','FSA024/025','OPEN','rawFAIL preserved; no frozen repair')]
 write('HISTORICAL_DEFECTS','# История, текущие статусы и неподтверждённые закрытия\n\n'+header+table(['Historical finding','Current issue','Status','Current evidence'],hist)+'''
Источники R0A–R0H/C1/C2/C3 Reports, contracts, exact hashes и status locators индексируются HISTORICAL_INDEX.json; это не повторная полная проверка всех прошлых oracle. No old acceptance/status file changed. New reference fixes/status packages не изменили production: L01/L02/M01/M02/zeroCore нельзя считать resolved по PASS новогоPython. Текущий audit independently extracts source cases instead of доверия прежнемуобщемуPASS.

Свежие R0A128/R0B141/R0C221/R0D944/R0E728/C1840/C21264 executions сохраняют свои scope; repeated Decimal contexts — не новые сценарии. C2 schema rows отдельно2462. R0G128 иR0H148 снова выполнялись через API без old save(). Начальный R0F_API лишь перечислил116 cases (stdout116); это не test execution. Отдельный FOLLOWUP действительно вызвал все116 Run и сохранил R0F_FRESH, не подменяя metadata первого запуска.

R7=57PASS/5FAIL: S040B/S040C/S044A/S044B связаны со старыми canonical-status markers/keys, S045 — historical manifest. Это не доказательство ledger correctness и не разрешение отредактировать frozen artifacts. R0=35/46 contract cases остаются FAIL. R8/R10 теперь exit1: толькоSCOPE на трёх test-only R0H .mqh/.mq5; это конфликт устаревшего blanketnoMQL checker с разрешённым R0H harness, не изменение production тела. R12 иR12A сохранилиexit0, но их выводы ограничены qualification predicates, не full EA.

Новое: NaN risk/completion, hidden secondFar in initialslot, spent-source catchup, journal altered-body falseNOOP, gross/net metric mismatch, inactiveTrend mismatch, terminal route/proof gaps. Detailed categories/scopes — DEFECTS.json. Native broker execution всех перечисленных случаев NOT_RUN.
''')
 # TEST_COVERAGE
 write('TEST_COVERAGE','# Доказательства и реальные границы покрытия\n\n'+header+scopes+f'''## Текущие независимые проверки

- Main manual51/51lines read;31 ownerdocuments fullread;133 docsindexed. Historical appendices не все заново семантически проверены.
- 74/74 production files статически рассмотрены;199 declarations;16 mainincludeclosure;13 conservative entry-reachable functions. Никакой «процентготовности» не вычисляется.
- C++extracted **{len(ex['Rows'])} scopedchecks: {ex['Pass']}PASS/{ex['Fail']}FAIL** against normative/caller expectations. Real source bodies, but LP64/math/string adapters and explicit synthetic calculation-only brokerstubs. Not MetaEditor/nativeMT5. Нельзя считать codefile-leveladapter compilation выполнением всех functions.
- **20 analytical accounting scenarios PASS**, initial/final balances/quotes/positions/traces сохранены. No signals/scenario controllers executed.
- **15 abstract invariant families**, **{ref['PropertySamplePairs']} exact-distinct generated positive/negative input pairs PASS**, seed20261111. Из360 rawpairs удалены115 exactduplicates. Numeric variants не245 независимых mathematical proofs.
- **15 analytical guard mutations killed**; no parser/runtime exception counted kill. Первоначальный14/15 survivor иточные initialsourcebytes сохранены в DEVELOPMENT/INITIAL_REFERENCE_SOURCE; причина — неправильный positivecontrol для attribution, исправлен тестfixture, не production.
- **20 exact spec-arithmetic vectors PASS**. Это отдельный oracle/literal checklist, не полный native coverage всех49families/137sourcesites.

## Свежие historical commands

'''+table(['Run','Actual exit','Pass/Fail counts','Count scope'],[(r['ID'],r['ExitCode'],str(r.get('PassCount'))+'/'+str(r.get('FailCount')),r['CountScope']) for r in reg['Runs']])+'''
Полные commands,UTC,start/end,subject/runner hashes,actual stdout/stderr и outputpaths в REGRESSIONS/EXECUTIONS. PassCount=None означает runner не выдал сопоставимый counter; не заменён0 или выдуманнымPASS. R8/R10 SCOPE failures раскрыты в AcceptanceDetail, R0F enumeration отдельно от fresh116 execution. Overall historical regressions=FAIL. Отличие от C3 только scopeR8/R10 не автоматически «functional regression», source bytes preserved и exactfindingsquoted. Full279Python scripts и все прежниеmutations/packagechecks не выполнялись.

## Не выполнено / не доказано

MQL5main/harness compile, native MQL5 execution, brokerOrderCalcProfit/OrderCalcMargin, actual history/partialfill/requote/timeout/retcode processing, durable restart/crash/CAS/concurrency, full account globalfunding, operational finalclose/smalltransition/NewFar promotion, backtest/demo/statistical profitability — NOT_RUN/UNVERIFIED/UNIMPLEMENTED согласно контексту. Эти статусы неconvertedPASS. Old accepted UNIT/static/model evidence cannot substitute. Package verification proves artifact integrity/consistency only, not the truth of all mathematical/systemclaims.

## Повторение новых проверок

`python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_common.py`
`python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_extracted.py`
`python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_reference.py`
`python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_math.py`
`python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_regressions.py`
`python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_followup.py`
`python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_build.py`

Sourceextraction success exit0 means reproduction infrastructure succeeded, не normative sourcechecks allPASS. Actual EXTRACTED.json.Fail оставлен{ex['Fail']}. Начальные development failures nothidden. Финальный VERIFY orchestrator captures fresh subprocess exits without rewriting frozenfiles; default packageverification read-only.
'''.replace("{ex['Fail']}",str(ex['Fail'])))
 # DEFECT_REGISTER
 body='# Реестр проблем и рисков\n\n'+header+f"**{len(ds)} entries**: "+', '.join(level+'='+str(counts[level]) for level in ('P0','P1','P2','P3'))+'. P0 — latent blockers при использовании соответствующих библиотек, не наблюдавшиеся реальные сделки/списания; текущий EA disabled. Severity не отменяет proofscope. Category различает confirmed local/source defects, normative conflicts, proof obligations, unimplemented components и native blockers.\n\n'
 body+=table(['ID','Severity','Category','Source','Status'],[(d['DefectID'],d['Severity'],d['Category'],d['SourceFile']+':'+str(d['SourceLine']),d['Status']) for d in ds])
 for d in ds:
  body+='\n## '+d['DefectID']+' '+d['Severity']+'\n\n'+'\n\n'.join('**'+field+'**: '+(json.dumps(d[field],ensure_ascii=False) if type(d[field]) is list else str(d[field])) for field in ('SourceFile','SourceLine','Requirement','Category','Cause','Counterexample','Expected','Actual','PotentialConsequence','TestIDs','Reproduction','ProposedFix','Dependencies','ProofBoundary','Status'))+'\n'
 body+='\n## Отдельные непроверенные риски\n\n'+table(['RiskID','Topic','Source','Unknown/impact'],[(r['RiskID'],r['Title'],r['Source'],r['Reason']) for r in risks])
 write('DEFECT_REGISTER',body)
 # ROADMAP
 phases=[
 ('GATE-0','Admin contract reconciliation + native environment','Docs/Reports/new Tests only','D02/D08, schema/equality/status/codec/legacy compat; disputedD01,D04,D05,D06,CR09 as relevant','Independent records/negative/mutation/goldens; real MetaEditor readiness','Exact baseline, no approval inferred, explicit one-fileR1.1 task','Any unresolved mandatory schema/compatibility/native evidence ->stop'),
 ('R1.1','Minimal Economic Ledger Identity','Include/Money/HSBI_EconomicLedgerTypes.mqh only','Approved key/account/sourcebody/codec/status and nativeacceptance','Every immutablefield, sameNetcomponents, unknownlegacy/source, exact/alteredreplay; per-fieldmutants; main+harnessnative compile','No outside-header changes; no funding/dispatch; legacydiagnostic cannot become authority','Need provider/caller/helpers elsewhere ->request separate expanded scope, do not silently change'),
 ('R1.2A','Finite data / complete role cardinality / checked revision','RiskGateResult,NewFarGateTypes;TransactionTypes,ExternalOutcome;Core Context/Invariants/StateMachine (exact separate allowlist)','Known finite inputs/limits/outcomes, allslots/actualidentifier set; explicitresume policy','NaN/Inf/negative domain,bounds,secondFar in every slot; actualtransaction zero deltas; mutation eachguard','Native assertions+existingcontracts preserved/classified','Any newfalsePASS or out-of-scope edits'),
 ('R1.2B','Allocation identity/conservation/authoritative consumption','Money AllocationLedgerTypes,ReserveAllocationTypes,ReserveCatchUpEvaluator,MoneyState (separate approvedscope)','D01/phase,immutablegrants vs remaining,owner/bucket/source/cycle,postedcurrency/precision','per-source/globalclone,permutation,exhaustedsource,nohiddenrebudget,replay/conflict','Exact conservation and no new funding from booleanbranch; native differentialtests','Unknown history/units/authority=>unavailable notmintedmoney'),
 ('R1.3','Independent history/economic/risk/market providers','New provider files require new named allowlist, not created here','BrokerAccountMode/symbol/FX/posted amounts/EA-originjournal/candidateproof context','Real isolated read-only brokerhistory/provider tests and deterministic replays, no realaccounttrades','Expectedidentity independent, actual/projected/source eligibility distinct','Unavailable data cannot be fabricated byflags'),
 ('R1.4','Durable journal/restart/CAS and globally unique funding','Persistence backend/ExecutionJournal/Snapshot/RuntimeRestart namedseparately','Approved native codec/schema/source attribution and crashconsistent protocol','Crash everycommitpoint,corruption,fallback,concurrentdoublecommit,receipt alteration,lockfailure','Global funding/accountdebit conservation+exact replay proven on real backend','Any durable ambiguity/conflict stopsopens; no silentmigration'),
 ('R1.5','Geometry/solver/terminal proof correctness','Planning Geometry/FutureSmall/Aggregator/NewFar+Money Basket (separate task)','Activelegs/brokergridorigin,BigGross vsNet,independentRisk,terminalclosebudget,objective/CR09 approved','Zero/min/max/nonstandardstep,allrequiredlevels,worst margins,tailproof/plateau,minimumNvsobjective','Native solver+broker calculation proof, no promotion/dispatch','Unknown nextlevel/terminalaffordability remainsUNPROVEN'),
 ('SIM-1','Full scenario/FSM/event-engine simulation without brokerdispatch','Scenarios/Execution/Runtime/Main changes only after full named authorization','All monetary/provenance/persistence prerequisites; completedactualevents beforeadvance','Initialrollback,C/T/Sopen,Harvestallocation,Partial/Final/Small/NewFar; allfailure/restart/orderings','Deterministic full lifecycle and invariant evidence, no liveorders','Any earlyadvance/dualFar/doubleconsumption ->block'),
 ('NATIVE-TESTER','Limited MT5 trading-logic test permission (future)','Explicit separately approved simulator/test-only/runtime boundary','Native compile allheaders and fullE2E simulatedproofs; adminapproval','RealMT5StrategyTester data/report/stress/accountmode/costs and holdout robustness','No realbrokerdispatch enabled; quantitative risk/strategy evidence reviewed','Current audit does NOT authorize this phase'),
 ('LIVE-GATE','Demo forward then explicit narrowlylimited real admission','Only future dedicated security/adminscope','All gates,kill switches,capital/risk budgets,broker safeguards,operatorrunbooks','Demo/forward/economicreconciliation + manualkill/restart/crash tests','Separate explicit admin decision; not implied by any pastPASS','No permission in this audit')]
 write('REMEDIATION_ROADMAP','# Порядок будущих исправлений и разрешений\n\n'+header+'''Критический путь к первой remediation: ограничить supported domain и утвердить обязательные source/equality/status/codec/legacy contracts; получить native toolchain/test plan; затем отдельное MinimalR1.1 задание на одинheader. До funding/execution должны быть устранены все применимые P0, а не толькоL01. Независимые ветви risk/cardinality могут проверяться параллельно по зависимостям, но ни один bypass не считается безопасным из-за наличия другого неисполняемого validator.

'''+table(['Phase','Goal','Future scope','Dependencies/contracts','Required tests','Acceptance','Stop'],phases)+'''

```mermaid
flowchart TD
 Contracts[Approved source/schema/domain/status contracts] --> Native[Native toolchain and golden assertions]
 Native --> Identity[Minimal R1.1 identity]
 Identity --> Alloc[Immutable allocation + exact consumption]
 Safety[Finite risk/outcome + complete role/FSM guards] --> Providers[Independent provider reconciliation]
 Identity --> Providers
 Alloc --> Durable[Durable global funding/journal/CAS]
 Providers --> Durable
 Durable --> Solver[Full solver/terminal/Catch-Up policy proof]
 Solver --> Sim[Full event/scenario simulation]
 Safety --> Sim
 Sim --> Tester[Separate MT5 tester permission]
 Tester --> Forward[Demo and external evidence]
 Forward --> Admin[Separate live approval gate]
```

Это dependency plan, не разрешение новыхфайлов/торговли. Ни один production файл не изменяется этим аудитом. Administrative choice нельзя заменить implementation convenience. Existing source may be patched only in its future explicitly approved task; multiple helper headers не прячутся в single-filephase. Native compilation mandatory before productionacceptance, no g++ substitute. Rollback ownfuturecommit отдельным reviewedrevert, сохранять observations/schema/receipts; no reset/rebase/force/compensatingtrades. No automatic stage advancement.
''')
 # FINAL VERDICT -- explicit answers, evidence boundaries, no readiness percentage.
 critical=table(['ID / severity','Source locator','Problem','Evidence / category'],[(d['DefectID']+' '+d['Severity'],d['SourceFile']+':'+str(d['SourceLine']),d['Cause'],','.join(d['TestIDs'])+'; '+d['Category']) for d in ds if d['Severity'] in ('P0','P1')])
 final='''# Независимый вердикт по всей системе HSBI

'''+header+'''## 18.1. Общая характеристика

**FINAL_SYSTEM_VERDICT=SYSTEM_CRITICAL_CONTRADICTIONS_FOUND.** HSBI сейчас представляет собой неторгующий MQL5-каркас с библиотекой расчётных/проверочных прототипов, обширным нормативным дизайном и несколькими поколениями test-only моделей. Это не целостный реализованный recovery EA. Его главная идея: после Initial Lock оставить Far, открыть противоположные Core/Trend с Small на стороне Far, закрывать/распределять подтверждённые profits, частично уменьшать Far либо пройти SmallTransition и переназначить actual residual originalCore как новый Far.

Текущий production entry намеренно выключен: main:21 задаёт HSBI_RUNTIME_DISABLED, RuntimePolicy:25 всегда запрещает dispatch, OnTick:37 вызывает только неуспешный stub. Это подтверждает отсутствие текущего broker dispatch path в проверенных исходниках, но не математическую/экономическую безопасность будущей системы. В реальном счёте этот каркас не управляет уже открытыми позициями и не является защитным EA.

Аудит нельзя считать полным доказательством системы: **AUDIT_COMPLETENESS=PARTIAL**. Все74production modules статически рассмотрены, основной51-lineмануал прочитан целиком, но не вся историческая документация/279test scripts повторно проверена семантически,137expression sites не доказаны как отдельные атомарные формулы, native/broker/durable/full-cycle evidence отсутствуют. Это ограничивает полноту отрицательного/положительного вывода, но не отменяет воспроизведённые source-contract failures.

## 18.2. Полнота руководства

Основное руководство: `Docs/03_FULL_SYSTEM_MANUAL_RU.md:1–51`; owner-contracts00–32, в том числе два27. Найдены133 indexed Docs/root files.31owner-текст прочитан целиком;19/21/22 и многие historical/proposed appendices индексированы/выборочно сопоставлены. Полная карта headings/status locators и manual-section→code/evidence/verdict в DOCUMENTATION_MAP/REQUIREMENT_MATRIX.

Руководство описывает требуемую последовательность, но «self-contained/OPEN_P0=0» не current implementation acceptance. Нужно отдельно решить objective minN vs risk-first, FarLoss absolute/incremental, reserve/balance phase mapping, cost overlap/buffers, all-level Catch-Up, transition A/B/C, codec/native domain и legacy provider boundary. Отсутствуют доказанные production procedures для actual account model/retcodes/fills/journal/terminal affordability/restart. Формальные owners TransactionEngine/FillAccumulator/FinalCloseCalculator/SnapshotStore не реализованы как рабочие компоненты. Historical architecture closure остаётся историей, не разрешением на R1.1/торговлю.

## 18.3. Вердикт по математике

Базовая размерностная алгебра lot/price/money во многих формулах корректна при предпосылках. Signed DealNet сохраняет Profit+Swap+Commission+Fee; Bid/Ask close side и lot floor/ceil существуют в source. RecoveryPL=realized+open-net без повторного прибавления allocation buckets — правильное accounting identity, не стратегия заработка.

Но формальная связность системы не доказана. Из49semantic families24 проверены только в заявленном математическом/reference domain,11 имеют code/spec/предлагаемый-policy contradictions,14 остаются UNVERIFIED. Counts не проценты готовности и не49nativeформул. Существуют ложные локальные PASS и неразрешённые proof obligations.

**Геометрия.** Сlope=C+T−S−F>0 — лишь sensitivity filter. Actual source приF.1,Rc.01,Rt3,Rs.1 получает Core0,Trend.3,Small.01,slope.19 и geometryVALID, вопреки обязательному minimumCore. Core.01 приmin.05 тоже допускается. Напротив, Rt0 допускается геометрией/нормативом, но BasketMoney требует positive volume всех четырёх legs и отклоняет отсутствующий Trend. Такие локальные defects не объявляются working whole-solver обходом: другие money wrappers могут отклонить zeroCore.

**Gross/net.** FutureSmallSolver:90 сравнивает netBigVolume с priorBigGross. ПриC.6,T.6,S1,F.1 BigGross1.2>old1, net.2<1. Permitted UnitTestlevel с остальными synthetic gates проходит. Это неверный показатель для документированного NextBigGross<OldBigGross.

**Worst-case.** Source выбирает уровень argmax TransitionLoss, не минимум Catch-Up margin. (Trans10,Rsv100,FarLoss90,Buffer1)->+9 против (Trans5,Rsv10,FarLoss20,Buffer1)->−11. Положительный выбранный control не all-level proof. CR09 должен явно утвердить scope, не просто дать одинаковое POSITIVE двум политикам.

**Конечность.** Теорема F(k)<=q^kF0 условна при uniformq на каждом будущем успешном transition. Finite prefix.8,.64 и flags не доказывают tail: следующий.64 нарушаетq^3=.512. ДостижениеVmin не закрывает оставшуюся позицию; solver может вернуть valid/finite при terminalRouteAllowedfalse и remainingFar.01. Нет operational close affordability proof. Это пробел доказательства/реализации, а не опровержение правильной условной геометрической теоремы.

**Transition.** Signed batch[-15,+100] даёт currentloss0, peak15 и stickybreachcap12. Решение о A/B/C/reset/ordered partialfills не принято автоматически. Раннее нарушение cap не исчезает как исторический факт из-за последующей прибыли.

## 18.4. Вердикт по экономике

**PROFITABILITY_PROVEN=NO; LOSS_BOUND_PROVEN=NO.** Нет независимого empirical market protocol/backtest/demo/holdout или реализованного полного cycle. Успешная unit арифметика не доказывает positive expectancy.

Синтетический exact пример (не brokerdata): FarSELL1@100, CoreBUY1.2@101, TrendBUY1@101, SmallSELL.5@100, openingfees.37. На104/105 BigNet6.38, SmallNet−2.55; закрытие всех C/T/S даёт положительный Harvest3.83. Balance1003.46, remainingFar loss−5, Equity998.46. Стоимость окончательного Farclose.10 =>CyclePnL−1.64. Сценарий не утверждает разрешение actual HSBI gate; он математически доказывает, что positive Harvest/balance не означает прибыль всего цикла. FinalClose full recovery gate должен отклонить недостаточный результат.

Не закрытая Far liability может увеличиваться после закрытия выгодных ног. При оставшемся shortQ, без guaranteed hedge/exit, P→∞ даёт−Q(P−open), то есть модель не имеет unconditional lossbound. Реальные stop-out/negative-balance safeguards требуют отдельной broker account модели, не предполагаются. Flat/adverse path, отрицательный carry, отсутствие ликвидности/маржи/receipt или gap могут сорвать дальнейший recovery и потребовать капитал либо принятие убытка. Нет доказанной неизбежной убыточности каждой траектории; есть отсутствие доказательств заявляемых гарантий.

Allocation/source accounting критически неполон. Economic equality допускает изменённые компоненты при том жеNet, allocation equality перестановку buckets. Reserve key не связан с authoritative allocation, а exhausted source50 может получить новое projected Catch-Up permission45 через alreadyAllocatedfalse. Это не исполненное повторное списание: backendapply отсутствует. Но такой калькулятор нельзя сделать financial authority без исправления. Global economic funding/account debits across allocations не доказаны. Source-level positive receipt не автоматический discretionary accountsurplus после losses Small/Far/fees.

## 18.5. Вердикт по торговой логике

**Полный торговый цикл не реализован.** Source callback FSM фактически одно состояние DISABLED. Library topology имеет33enums и1089 observedpair results, но нормальные transitions заканчиваются openingCore; Core→Trend отсутствует. Нет engines initialrollback, stagedbasketopen, fillaccumulation, Harvestsettlement, PartialFar reservationconsumption, authoritative FinalClose, confirmation/debounce, stagedSmall/newFarcommit или cycle reset.

Pure topology допускает terminalSafe→reconciling→FarActive без admin argument. Это не текущий autoresume (main не вызываетhelper), но не готовое enforcement no-auto-resume. Реальный переход требует independent observed event+ownership+ledger+durable result; provided booleans не заменяют эти действия. Нет liveness/termination proof, полной error-state recovery, защиты от actual external intervention, account reconnect/retcodes/out-of-order fills. Статусы и outcome DTO не сами brokerexecution.

## 18.6. Вердикт по архитектуре

Безопасное полезное свойство текущего дизайна — явный no-trade runtime, изоляция расчётов от sends, typed roles/IDs, fail-unavailable broker calculation wrappers и часть pure validators. Но только16headers в mainincludeclosure и13projectfunctions консервативно entry-reachable. Большинство библиотек dormant. Концептуальный layered design не соответствует работающей end-to-end orchestration.

Independent providers/history/origin attribution отсутствуют. NewFar перезаписывает proof identity из входных descriptors/IDs, затем копирует expected=presented; helper equality корректно сравнит данные, но независимость expected не доказана caller. Без provider reconciliation nonzeroDeal/actualfillsConfirmed/runtimeConfirmed остаются предпосылками, не брокерскими фактами.

Durable backend/SHA256/lock/CAS/versioned commit/restart history loader не реализованы: PersistenceInterface:5–7 явноfalse/stub. Snapshot/journal DTO и prefix checks не durable exactly-once. Journal alteredpayload с сохранённымcurrentDigest получает NO_OP до validation (FSA027). Main не использует этивалидации для реального цикла. Money/Planning dependency coupling и отсутствие готового input config/account mode требуют отдельного designgate, не скрытого расширения MinimalR1.1.

## 18.7. Вердикт по исходному коду

Выбранные source bodies выполнены в isolated C++ LP64 adapter с documented math/string wrappers и synthetic OrderCalcProfit/OrderCalcMargin. Это НЕ nativeMQL5. **54scoped source checks:27PASS/27FAIL**; числоFAIL не числоуникальныхвзломов. M02 coherent expected acceptance и conservative-prefix acceptance записаны как корректные локальные наблюдения: они не доказывают независимую authority или universal tail. Отдельные caller/global proof gaps оцениваются статически/математически, не ложным helperFAIL. Каждыйissue имеет evidence scope/контрпример/локатор в DEFECT_REGISTER/DEFECTS.json.

Дополнительно подтверждены:

- Risk gate допускает NaN projectedMargin; NewFar gate допускает unknown allowedMargin. Не все ограничения/диапазоны проверяются.
- TransactionBarrier/ExternalOutcome допускают NaN volumes/prices как completed при прочих заданных flags/IDs.
- Context validator пропускает второйFAR в initialBuy, а NoDualTail считает лишь четыре слота.
- MoneyState ignoresvalid/revision и принимает+Infinity; Allocation validator допускает отрицательный bucket при сохранённой общей сумме.
- Futuretimestamp принимается какfresh; universalclock/skew contract отсутствует. StateRevision+1 не имеетoverflowguard.
- Digest-loop maximumDepth используется до downstream<=128 validation; опасный OOB runtime не запускался, staticgap сохранён кактаковой.

Нет доказательства, что эти dormantlibrary flaws уже привели к реальным сделкам/списаниям. Но включать их в financial orchestration без исправления нельзя. Вывод «real trading отсутствует» не превращает формулы/контракты в корректные.

## 18.8. Вердикт по безопасности

**Использовать как реальный торговый/защитный советник нельзя. Включать broker dispatch нельзя.** Currentstatic scan не нашёл sendingpaths, guards/versionflagsdisabled подтверждены hashes. Это означает no-current-dispatch, а не completed execution safety.

MetaEditor/MT5/Wine не обнаружены; MQL5compile/native tests/StrategyTester NOT_RUN. No native profit/codec/ABI/runtime guarantee. Подготовленные R0H harness/goldens могут быть основой следующего isolated native test задания после предоставления среды; это не разрешение торговых операций. Ограниченное tradinglogic StrategyTester testing требует сначала monetary/provenance/persistence/FSM gates и отдельного административного задания. Нынешний audit ничего из этого не разрешает.

## 18.9. Критические проблемы P0/P1

'''+critical+'''

Порог severity описывает потенциальный ущерб при использовании соответствующего пути, не активный доступ к счёту. Реестр включает confirmed local defects, normative conflicts, unimplemented components и proof/evidenceblockers; count не подменяет proofseverity. Все28/29 issue scopes в DEFECT_REGISTER, отдельные9 unverifiedrisks в COVERAGE/DEFECTS.

## 18.10. Что исправлять и проверять дальше

1. Утвердить точные source/body/status/codec/legacy/provenance boundaries для MinimalR1.1; resolve policy prerequisites без overexpanding всейстратегии. Native toolchain/acceptance обязателен; не autoapprove16decisions.
2. Отдельным заданием исправить economic identity; затем allocation immutable vector/phase/state/conservation и authoritative source/bucket/consumer/replay binding, включая spentsource. Не смешивать projections и actualavailable.
3. Устранить finite/domain/cardinality/outcome/revision gaps во всех обязательных public paths, доказать mandatory callers и отсутствие bypass. Не считать наличие необязательного guard защитой.
4. Реализовать независимые account/history/EA-origin/risk/margin/cost providers. Утвердить supported accountmode, currency/precision/rounding/costbasis и current policy assumptions.
5. Затем durable storage/journal/CAS/globalfunding/reconciliation; validatealteredreplay и crash/restart/concurrent events на реальном backend.
6. Исправить geometry/optionalleg/grossmetric/objective/CR09/tail/terminalclose proofs и проверить в nativeMQL5 с реальными calculation-only broker contexts.
7. Только потом отдельные fullscenario/FSM simulation/nativeeventintegration, затем явно разрешённые StrategyTester/demoevidence и отдельный liveapprovalgate.

Полная пофазная таблица fileallowlists/dependencies/tests/stop/rollback в REMEDIATION_ROADMAP. Ни один этап не запускается текущей публикацией.

## 18.11. Итоговое заключение

**SYSTEM_CRITICAL_CONTRADICTIONS_FOUND** — подтверждены фундаментальные source/accounting/guard несоответствия, а непротиворечивость и экономическая состоятельность всей торговой системы не установлены. Одновременно **SYSTEM_NOT_FULLY_VERIFIABLE** описывает предел полноты из-за отсутствующих execution/backend/native/provider components, но не отменяет отрицательные конкретные находки. Положительный full-system status не обоснован.

Ответы администратора:

1. Математика целиком правильной не признана: есть корректные условные identity и ошибочные/неполные проверки/definitions.
2. Все части фактически не взаимодействуют end-to-end; main не запускает cycle.
3. Ошибки в денежных validators/equality/binding, риск nonfinite и lot/gross/terminal consistency подтверждены в scoped source evidence.
4. Работать как в руководстве текущий EA не может: ключевые engines/providers отсутствуют.
5. Реализованы skeleton/DTO/pure calculators/validators, а не полноценное исполнение.
6. Scenarios/backend/fullreconciliation/funding/terminalclose/ActualMarginRisk integration остаются преимущественно спецификацией/моделями.
7. Adverse trend/gaps/costs/margin shortage/noevent/nohistory и partial/unknown execution могут сорвать/зависить recovery; гарантии completion/lossbound не установлены.
8. Исправления начинаются с identity/conservation/provenance/finiteguards, не с отправки ордеров.
9. Доказаны лишь перечисленные local algebra/fixture properties при предпосылках. Ни прибыльность, ни реальная whole-account conservation/exactly-once/native execution ими не доказаны.
10. Дальнейшее продвижение требует конкретного approvedscope, native environment, provider/backend и доказательного fullcycle тестирования.

## 18.12. Readiness и полнота доказательств

'''+table(['Readiness','Status','Reason / evidence'],[
 ('DOCUMENTATION_READY','PARTIAL','Mainmanual/ownertexts есть, но конфликты/current policy/provider/runbook gaps; DOCUMENTATION_MAP'),('MATHEMATICS_READY','NO_FULL_SYSTEM_PROOF','49families/137sites; zeroCore,gross,worstcase/tail problems; MATHEMATICS'),('ECONOMIC_MODEL_READY','NO','No profitability/lossbound/globalfunding; ECONOMIC_MODEL'),('PRODUCTION_READY','NO','No event/scenario/storage/provider lifecycle; CODE_REVIEW'),('NATIVE_TESTING_READY','HARNESSES_PREPARED_TOOLCHAIN_MISSING','MQL5compile/runtimeNOT_RUN; NATIVE_ENVIRONMENT'),('TRADING_LOGIC_READY','NO','Full FSM/scenarios unimplemented; TRADING_CYCLE'),('BROKER_DISPATCH_READY','NO','Intentionallydisabled; no execution/risk/provider acceptance'),('REAL_TRADING_READY','NO','All necessary gates/admin approval absent')])+'''

Coverage:74staticallyreviewed productionfiles,199definitions,51linesmanualfullread,31ownertextsread,133docsindexed. All historicalqualification appendices and279test scripts не fullyreverified;14families unverified; no fullnative/broker/durable execution. Therefore AUDIT_COMPLETENESS=PARTIAL, STAGE_COMPLETE=NO_PARTIAL_AUDIT. Это опубликованный частичный независимый отчёт с конкретным отрицательным вердиктом, не ложное заявление полного выполнения аудита. PublicationSHA/parity фиксируются после commit в окончательном ответе, не self-embedded в собственный commit.

ADMIN_APPROVAL_COMPLETE=NO
PRODUCTION_REMEDIATION_ALLOWED=NO
TRADING_LOGIC_START_ALLOWED=NO
BROKER_DISPATCH_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
'''
 final=final.replace('Все28/29 issue scopes','Все'+str(len(ds))+' issue scopes')
 write('FINAL_VERDICT',final)
 # Honest summary used by package checker/final machine block.
 summary=dict(meta,MainManualFound=True,DocumentationCompleteness='PARTIAL',ProductionModulesReviewed=74,FormulaFamilies=len(fs),FormulaCounts=dict(fcounts),StateMachineVerified=False,FullTradingCycleVerified=False,MoneyConservationProductionVerified=False,ProfitabilityProven=False,LossBoundProven=False,AuditCompleteness='PARTIAL',StageComplete=False,FinalSystemVerdict='SYSTEM_CRITICAL_CONTRADICTIONS_FOUND',FinalVerdictFile='Reports/HSBI_FULL_SYSTEM_AUDIT_01_FINAL_VERDICT_RU.md',DefectCounts={s:counts[s] for s in ('P0','P1','P2','P3')},UnverifiedRiskCount=len(risks),ReferenceScenarioPass=ref['ScenarioPass'],DistinctPropertyPairs=ref['PropertySamplePairs'],PropertyFamilyCount=15,PropertyMutationsKilled=ref['MutationsKilled'],SpecVectorPass=math['Pass'],ExtractedCppPass=ex['Pass'],ExtractedCppFail=ex['Fail'],MQL5_COMPILE='NOT_RUN',MQL5_NATIVE_TESTS='NOT_RUN',HistoricalRegressions='FAIL_R7_R0_R8_R10',AdminApprovalComplete=False,ProductionRemediationAllowed=False,TradingLogicStartAllowed=False,BrokerDispatchAllowed=False,RealTradingAllowed=False)
 a.save('TEST_RESULTS',summary)
 print('BUILD',len(ds),'issues',dict(counts),'formulas',dict(fcounts),'audit PARTIAL')
if __name__=='__main__':main()
