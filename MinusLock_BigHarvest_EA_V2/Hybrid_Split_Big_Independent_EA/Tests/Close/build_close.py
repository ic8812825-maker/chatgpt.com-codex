"""Build new audit artifacts; never rewrites baseline files. Coverage is evidence-limited."""
import csv,json,re,hashlib,subprocess,itertools,difflib
from pathlib import Path
HERE=Path(__file__).resolve().parent
P=HERE.parent.parent
R=P/'Reports'
B=json.loads((HERE/'baseline.json').read_text());BASE=B['BASE_SHA']
def write(name,text):
 f=R/name
 if name in {x['Path'].removeprefix('Reports/') for x in B['Files'] if x['Path'].startswith('Reports/')}:raise RuntimeError('baseline overwrite forbidden')
 f.write_text(text.rstrip()+'\n')
def link(path,line=1):return f'https://github.com/ic8812825-maker/chatgpt.com-codex/blob/{BASE}/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/{path}#L{line}'
header=f'База `{BASE}`; ветка `work`. Все новые изменения контрактов — **PROPOSED**. Owner approval отсутствует.\n\n'
full_docs={f'Docs/{x}' for x in ['04_MATHEMATICAL_MODEL_RU.md','06_STATE_MACHINE_SPECIFICATION_RU.md','08_MONEY_LEDGER_SPECIFICATION_RU.md','12_FINAL_CLOSE_SPECIFICATION_RU.md','13_SMALL_TRANSITION_SPECIFICATION_RU.md']}
partial_docs={'Reports/HSBI_AUDIT03_ALL_ERRORS_RU.md','Reports/HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md','Reports/HSBI_AUDIT03_DOCUMENT_COVERAGE_RU.md','Reports/HSBI_AUDIT03_SOURCE_FUNCTION_MAP_RU.md','Reports/HSBI_AUDIT03_FORMULA_CATALOG_RU.md','Reports/HSBI_AUDIT03_COMPLETENESS_MATRIX_RU.md','Docs/HSBI_DG01_CONTRACT_RESOLUTION_RU.md','Reports/HSBI_DG01_ADMIN_DECISION_BALLOT_RU.md','Reports/HSBI_DG01_R1_1_APPROVAL_GATE_RU.md'}
source_read={'Include/Money/'+x for x in ['HSBI_EconomicLedgerTypes.mqh','HSBI_AllocationLedgerTypes.mqh','HSBI_ReserveCatchUpEvaluator.mqh','HSBI_ReserveAllocationTypes.mqh','HSBI_MoneyState.mqh','HSBI_MoneyTypes.mqh','HSBI_CostModel.mqh']}
source_read|={'Include/'+x for x in ['Core/HSBI_Context.mqh','Core/HSBI_StateMachine.mqh','Core/HSBI_Enums.mqh','Core/HSBI_Identifiers.mqh','Core/HSBI_ReasonCodes.mqh','Execution/HSBI_EventTypes.mqh','Execution/HSBI_TransactionTypes.mqh','Persistence/HSBI_ExecutionJournal.mqh','Risk/HSBI_RiskTypes.mqh','Risk/HSBI_RiskGateResult.mqh','Planning/HSBI_NewFarSolver.mqh','Planning/HSBI_FutureSmallProofAggregator.mqh']}
source_read.add('Hybrid_Split_Big_Independent_EA.mq5')
# Only a targeted clause audit, not a claim of complete twenty-field module review.
rootdocs={'BUILD_INFO.md','README_RU.md','PROJECT_MAP_RU.md','CHANGELOG_RU.md'}
def isdoc(s):return s.startswith(('Docs/','Reports/','Tests/Contracts/')) or s in rootdocs
previous={}
for line in (R/'HSBI_AUDIT03_DOCUMENT_COVERAGE_RU.md').read_text().splitlines():
 if line.startswith('| `'):
  cells=[v.strip() for v in line.split('|')[1:-1]]
  if len(cells)>5 and cells[5] in ('FULL','PARTIAL','NOT_REVIEWED'):previous[cells[0].strip('`')]=cells[5]
rows=[];docs=[];sources=[]
for x in B['Files']:
 s=x['Path'];prod=s.endswith(('.mqh','.mq5')) and not s.startswith('Tests/')
 doc=isdoc(s);t=(P/s).read_text(errors='replace') if doc else ''
 role='IMPLEMENTATION_REFERENCE' if prod else 'TEST_FIXTURE' if s.startswith('Tests/') else 'HISTORICAL_EVIDENCE' if s.startswith('Reports/') or s in rootdocs else 'UNRESOLVED_AUTHORITY'
 if s.startswith('Docs/'):
  if 'Статус: нормативный source of truth' in t:role='NORMATIVE' # declared status, not owner approval of future policy
  elif re.search(r'PROPOSAL_ONLY|AWAITING_ADMIN_APPROVAL|Все16 выборов|предложени',t,re.I):role='PROPOSAL'
 coverage='FULL' if s in full_docs else 'PARTIAL' if s in partial_docs or s in source_read else 'NOT_REVIEWED'
 evidence='Текст и clauses сверены в текущем проходе' if coverage=='FULL' else 'Целевой фрагмент/предикат; полный semantic review не выполнен' if coverage=='PARTIAL' else 'Содержательная сверка в текущем проходе не выполнена; файл доступен, технического препятствия чтению нет'
 r=dict(x,HistoricalCoverage=previous.get(s,'NOT_IN_OLD_LEDGER'),Category='PRODUCTION' if prod else 'DOCUMENT' if doc else 'TEST_OR_ASSET',NormativeStatus=role,CoverageStatus=coverage,Findings='NOT_VERIFIED',Evidence=evidence)
 rows.append(r)
 if doc:docs.append(r)
 if prod:sources.append(r)
with (HERE/'inventory.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys(),lineterminator='\n');w.writeheader();w.writerows(rows)
# Each baseline document remains individually addressable, with explicit current gaps.
notes={
 'Docs/04_MATHEMATICAL_MODEL_RU.md':'9: optional Trend zero конфликтует с min lot для каждой ноги; 18: buckets уже subsets; 30: equality + nonnegative; 33–36: uniform q условен, market profit не доказан.',
 'Docs/06_STATE_MACHINE_SPECIFICATION_RU.md':'9–12: only confirmed outcome + actual positions + ledger + persistence; 21: restart reconcile first. Pure FSM не реализует этот conjunction.',
 'Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md':'6: signed components; 9: AccountLogin нужен, но отсутствует economic DTO; 12/15: vector equality и conflict; 18: residual и isolation; 24: reserve/persist/consume lifecycle не готов.',
 'Docs/12_FINAL_CLOSE_SPECIFICATION_RU.md':'7–15: PnL gate и coverage gate независимы; no pending/unknown, actual zero нужны; positive harvest недостаточен.',
 'Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md':'9: current signed loss является declared norm; sticky/peak требуют отдельного owner change. 12–16: каждый intermediate close подтверждён; actual residual, не planned.'}
coverage='# AUDIT03 CLOSE — индивидуальный ledger документов\n\n'+header
coverage+=f'Baseline files={len(rows)}; documentary denominator={len(docs)} (Docs, Reports, Tests/Contracts и четыре корневых status-документа). Новые close artifacts не включены. FULL означает новый содержательный review документа, PARTIAL — только целевые разделы; чтение исторического вывода не повышает coverage его ссылок. HistoricalCoverage в CSV сохраняет прежний reading ledger отдельно от нового review scope; прежние FULL не объявляются ошибочными и не наследуются автоматически как текущий полный crosswalk. Полная metadata-инвентаризация всех файлов: `Tests/Close/inventory.csv`.\n\n'
coverage+='Автоматическая классификация роли помечает declared normative текст, но не устанавливает precedence конфликтующих редакций. Исторический PASS не норма. Для непросмотренных Docs статус authority требует отдельного review; строка классификатора не означает содержательное заключение. Поэтому AUDIT_COMPLETENESS=PARTIAL.\n\n| Path | Role | Coverage | Индивидуальное заключение / причина |\n|---|---|---|---|\n'
for x in docs:coverage+=f"| `{x['Path']}` | {x['NormativeStatus']} | {x['CoverageStatus']} | {notes.get(x['Path'],x['Evidence'])} |\n"
write('HSBI_AUDIT03_CLOSE_DOCUMENT_COVERAGE_RU.md',coverage)
# Lexical index with caller sites, never labeled enforcement proof.
def strip(t):return re.sub(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"',lambda m:'\n'*m.group().count('\n')+' '*(len(m.group())-m.group().count('\n')),t)
source_text={x['Path']:strip((P/x['Path']).read_text()) for x in sources}
functions=[]
for s,t in source_text.items():
 for m in re.finditer(r'(?:^|[;}])\s*(?:bool|void|string|int|double|ulong|HSBI_\w+)\s+(HSBI_\w+|OnInit|OnTick|OnTimer|OnDeinit)\s*\([^;{}]*\)\s*\{',t,re.M):
  name=m.group(1);line=t.count('\n',0,m.start(1))+1;callers=[]
  for cs,ct in source_text.items():
   for c in re.finditer(r'\b'+re.escape(name)+r'\s*\(',ct):
    cl=ct.count('\n',0,c.start())+1
    if cs==s and cl==line:continue
    callers.append(f'{cs}:{cl}')
  functions.append(dict(Function=name,Source=s,Line=line,Callers=callers,GuardEnforcement='NOT_VERIFIED',Crosswalk='PARTIAL_LEXICAL'))
(HERE/'function_index.json').write_text(json.dumps(functions,ensure_ascii=False,indent=2)+'\n')
cross='# AUDIT03 CLOSE — Source / Function / Caller / Guard\n\n'+header
cross+=f'{len(sources)} production modules; {len(functions)} лексических definitions. Caller sites извлечены после удаления comments/strings. Это навигация; нет type-resolution, call graph reachability и доказательства доминирования guards. Full twenty-field module review и FUNCTIONS_CROSSWALK_COMPLETE остаются NO.\n\n'
cross+='| Requirement | Formula | Function/source | Caller | Guard | Test | ERR |\n|---|---|---|---|---|---|---|\n'
focus=[('Docs/08:9,15','F017','HSBI_SameEconomicRecord','payload incompletely compared','P0-01','001/002'),('Docs/08:12,15','F016','HSBI_ClassifyAllocationDuplicate','total only','P0-02','004/005'),('Docs/04:42','F036','HSBI_ValidateRiskInput','finite missing','P0-04','009'),('Docs/04:42','F036','HSBI_ValidateMoneyState','finite missing','P0-05','011'),('Docs/06:9','F062','HSBI_TransactionBarrierPassed','finite fill missing','P0-07','010'),('Docs/06:12','F057','HSBI_RetryAllowed','UNKNOWN accepted locally','P0-10','010/017'),('Docs/08:24','F020/F060','HSBI_EvaluateReserveCatchUp','proof scalar equality absent','PLANNED binding','007/008/048'),('Docs/13:16','F060','HSBI_SolveNewFar','caller derives scalar but rewrites proof identity','PLANNED provider','013'),('Docs/06:9,21','F065','HSBI_ClassifyJournalAppend','duplicate before body validation','PLANNED replay','030')]
for req,formula,name,guard,test,err in focus:
 ff=next((x for x in functions if x['Function']==name),None)
 if ff:cross+=f"| {req} | {formula} | [{name}]({link(ff['Source'],ff['Line'])}) | {'; '.join(ff['Callers']) or 'NONE_FOUND_IN_PRODUCTION'} | {guard}; обязательность NOT_VERIFIED | {test} | ERR-{err} |\n"
cross+='\n## Индивидуальные модули\n\n| Module | Текстовый scope | Definitions | Preconditions/postconditions/callers/guards/tests |\n|---|---|---|---|\n'
for x in sources:
 fs=[f for f in functions if f['Source']==x['Path']]
 cross+=f"| `{x['Path']}` | {'TARGETED_READING' if x['Path'] in source_read else 'NOT_REVIEWED'} | {'; '.join(f['Function']+':'+str(f['Line']) for f in fs) or 'DTO / no lexical match'} | Полные 20 полей: NOT_VERIFIED. Dependencies доступны в include directives; точные callers в function_index.json. |\n"
cross+='\n## Все найденные функции\n\n| Function | Source:line | Production caller sites | Guard enforcement |\n|---|---|---|---|\n'
for f in functions:cross+=f"| {f['Function']} | `{f['Source']}:{f['Line']}` | {'; '.join(f['Callers']) or 'NONE_FOUND (не доказательство недостижимости)'} | NOT_VERIFIED |\n"
write('HSBI_AUDIT03_CLOSE_SOURCE_CROSSWALK_RU.md',cross)
# Full index of known formula families with explicit noninheritance.
old=(R/'HSBI_AUDIT03_FORMULA_CATALOG_RU.md').read_text();fam={}
for l in old.splitlines():
 m=re.match(r'\| HSBI-A03-F-(\d{3}) \|',l)
 if m:fam[int(m.group(1))]=l.split('|')[3].strip()
for i in range(61,67):
 m=re.search(r'### HSBI-A03-F-'+f'{i:03}'+r' — (.*)',old);fam[i]=m.group(1) if m else 'Историческая карточка'
proofs={7:('PROVEN_UNDER_ASSUMPTIONS','DealNet=P+Swap+Commission+Fee по signed actual компонентах одной валюты. 6000−100−200−50=5650 minor units; SIGNED-DEAL. Это accounting identity, не broker authenticity.'),13:('PROVEN_UNDER_ASSUMPTIONS','G=C+R+F, C/R/F disjoint nonnegative integer balances. consume d≤F: C′=C+d,F′=F−d; сумма сохраняется. G5000→C5000,F0. CONSUME/EXHAUSTED-VECTOR. Restart/durable scope не доказан.'),16:('PROVEN_UNDER_ASSUMPTIONS','Векторы (5000,0,0,0,0) и (0,5000,0,0,0) имеют сумму5000 и различаются; P0-02. Скалярная сумма не достаточна для replay equality.'),17:('PROVEN_UNDER_ASSUMPTIONS','P6000,C−1000 и P7000,C−2000 оба Net5000. Полное экономическое содержимое различно; P0-01. Равенство net не является equality payload.'),23:('CONTRADICTORY','Если WORST_CASE трактуется как all-level, выбор argmax transition недостаточен: level1 transition10/catchup9; level2 transition5/catchup−11. Worst transition выбирает1, minMargin=−11. Нужен CR-09; production policy semantics пока owner question.'),38:('INVALID','Finite prefix не влечёт uniform tail. Построить совпадающие первые n шагов и n+1 plateau F; прежние n не ограничивают следующий. Price/margin path и terminal close не следуют из q-prefix.'),58:('PROVEN_UNDER_ASSUMPTIONS','Если ∀k F(k+1)≤qF(k), 0<q<1, индукция F(k)≤q^kF0. Достижение ≤Vmin при k≥ceil(log(Vmin/F0)/log(q)). Для строгого < нужен следующий шаг при точном равенстве. Positive lot broker grid не гарантирует zero; operational close отдельное условие.'),63:('INVALID','Expected intent set={I}, Requested1, observed confirmed volume.4: IDs равны, missing.6. Поэтому conjunction требует exact fill volumes; P0-07 проверяет отдельный незавершённый fill, не весь исторический settlement.'),64:('PROVEN_UNDER_ASSUMPTIONS','N≥0 integer; si≥0,sum si≤1; bi=floor(Nsi). Тогда sum bi≤N, residual=N−sum bi≥0 и sum bi+residual=N. Round each ceil для N1,s=.5/.5 даёт2>N. Checked products и exact scale обязательны.'),65:('PROVEN_UNDER_ASSUMPTIONS','Два consumer читают Free50,r; каждый30≤50, вместе60>50. Требуется serializable CAS балансы+receipts. После A Free20,r+1 второй B отклоняется. COMPETING-B-STALE моделирует последовательную конкуренцию, не реальный concurrent backend.')}
form='# AUDIT03 CLOSE — формулы, доказательства и пределы\n\n'+header
form+='Все 66 исторических ID сохранены. Открытая инвентаризация новых формул по непрочитанным документам не завершена. Исторические 47 valid-under-assumptions не наследуются как новая проверка.\n\n| ID | Formula / family | Current proof | Доказательство / причина |\n|---|---|---|---|\n'
for i in range(1,67):
 st,note=proofs.get(i,('UNVERIFIED','Индивидуальная повторная сверка 15 полей (domain, dimensions, derivation, MQL mapping, boundaries, tests, limitations, ERR/IMP) не завершена; историческая карточка доступна по ID, статус не перенесён.'))
 form+=f"| F{i:03} | {fam.get(i,'NOT_INDEXED')} | {st} | {note} |\n"
form+='\n## Обязательные связи\n\nGeometry lot → денежный результат требует общего конечного положительного money/(lot·price) коэффициента и одинаковой valuation basis. В broker model BUY close=Bid, SELL close=Ask; tick asymmetry и costs разрушают простую зеркальную денежную теорему. Zero Trend требует явного inactive leg. Gross=C+T, Net=C+T−S; уменьшение Net не доказывает уменьшения Gross.\n\nCyclePnL и disjoint costs определены в PROPOSED_SPEC. Reserve amount binding и source ownership обязательны до разрешения consumption. q-tail не доказывает конечное время рынка, margin каждого prefix, turnover/loss bound или profitability. GLOBAL_FUNDING_PROVEN=NOT_VERIFIED; LOSS_BOUND_PROVEN=NOT_VERIFIED; PROFITABILITY_PROVEN=NO.\n'
write('HSBI_AUDIT03_CLOSE_FORMULA_PROOFS_RU.md',form)
# Cartesian obligations: execution expected outcomes, not verified production transitions.
enums=(P/'Include/Core/HSBI_Enums.mqh').read_text();states=re.search(r'enum HSBI_State\{([^}]+)',enums).group(1).split(',');events=re.search(r'enum HSBI_EventType\{([^}]+)',enums).group(1).split(',')
production_states=list(states)
for alias in ['HSBI_STATE_ACTION_REQUEST_SENT','HSBI_STATE_ACTION_ORDER_PENDING','HSBI_STATE_ACTION_PARTIAL_FILL','HSBI_STATE_ACTION_RETRY_PENDING']:
 if alias not in states:states.append(alias)
fsm=[]
for st,ev,partial,timeout,restart in itertools.product(states,events,['NONE','PARTIAL','COMPLETE'],['NONE','TIMEOUT','UNKNOWN'],['NO','YES']):
 if restart=='YES':result='BLOCK_RECONCILE';why='RESTART_RECONCILIATION_FIRST'
 elif timeout!='NONE' or ev in ('HSBI_EVENT_TIMEOUT','HSBI_EVENT_CONFLICT'):result='BLOCK_RECONCILE';why='UNKNOWN_OR_CONFLICT_NO_REDISPATCH'
 elif partial=='PARTIAL' or ev=='HSBI_EVENT_PARTIAL_FILL':result='BLOCK_NEXT_ROLE';why='NO_COMPLETED_FILL'
 elif ev=='HSBI_EVENT_COMPLETED_FILL' and partial=='COMPLETE':result='VERIFY_BEFORE_TRANSITION';why='ACTUAL_POSITIONS_DEALS_OWNERSHIP_LEDGER_DURABLE_REVISION_REQUIRED'
 else:result='NO_COMPLETION_AUTHORITY';why='EVENT_ALONE_NOT_SETTLEMENT'
 fsm.append(dict(State=st,Event=ev,Partial=partial,Timeout=timeout,Restart=restart,Expected=result,Reason=why,ProductionVerification='NOT_VERIFIED'))
with (HERE/'fsm_matrix.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fsm[0],lineterminator='\n');w.writeheader();w.writerows(fsm)
write('HSBI_AUDIT03_CLOSE_FSM_MATRIX_RU.md','# AUDIT03 CLOSE — Event × State × Partial × Timeout × Restart\n\n'+header+f'`Tests/Close/fsm_matrix.csv`: {len(states)} union states ({len(production_states)} production + documentary aliases) × {len(events)} events × 3 fill states × 3 outcome states × 2 restart states = {len(fsm)} obligation rows. Каждая строка содержит expected и причину; ProductionVerification=NOT_VERIFIED. Это полный Cartesian obligation grid для объявленных enum, а не проверенная full FSM.\n\nDocs/06:6 дополнительно называет ACTION_REQUEST_SENT, ACTION_ORDER_PENDING, ACTION_PARTIAL_FILL, ACTION_RETRY_PENDING; production enum вместо них содержит RETRY_PENDING. Эти четыре documentary aliases включены отдельными строками полного Cartesian grid; их mapping к production enum NOT_VERIFIED. Ни одна неприсутствующая роль не считается покрытой автоматически.\n\nStateMachine:5 разрешает часть графа и self-transition, :6 не проверяет event/actual settlement и increment overflow, :7 не сохраняет journal. Поэтому topology не является execution authorization. Main:19–44 остаётся DISABLED + stub.\n\nПри COMPLETE fill нужны независимые confirmed deals, exact volume, fresh positions, ownership, ledger, persisted result и expected revision. Partial/timeout/unknown не разрешают следующий шаг; restart блокирует resume до reconciliation. Terminal/manual/emergency safety conditions отдельно от recovery success.\n\nFULL_FSM_VERIFIED=NO. Full documentary state alias mapping и реализация обязательных callers остаются gap.\n')
# Historical ERR records: metadata parsed, classification does not imply semantic rereview.
errtext=(R/'HSBI_AUDIT03_ALL_ERRORS_RU.md').read_text();errors=[]
for l in errtext.splitlines():
 if re.match(r'\| HSBI-A03-ERR-\d{3} \| P[012] \|',l):
  f=[x.strip() for x in l.split('|')[1:-1]]
  if len(f)<8:continue
  errors.append(dict(ID=f[0],Priority=f[1],Category=f[2],Stage=f[3],File=f[4],Lines=f[5],HistoricalProof=f[6],IMP=f[7]))
errors=list({e['ID']:e for e in errors}.values())
errors += [dict(ID='HSBI-A03-ERR-048',Priority='P0',Category='RESERVE',Stage='Public amount binding',File='Include/Money/HSBI_ReserveCatchUpEvaluator.mqh',Lines='24–76',HistoricalProof='SOURCE_DEFECT',IMP='IMP-004/010'),dict(ID='HSBI-A03-ERR-049',Priority='P1',Category='IDENTITY',Stage='Closed enums',File='Include/Execution/HSBI_ExecutionIntent.mqh',Lines='28–40',HistoricalProof='SOURCE_DEFECT',IMP='IMP-005/007/008'),dict(ID='HSBI-A03-ERR-050',Priority='P1',Category='PERSISTENCE',Stage='Snapshot count',File='Include/Persistence/HSBI_ExecutionStateSnapshot.mqh',Lines='27–40',HistoricalProof='AMBIGUOUS_SPECIFICATION',IMP='IMP-009')]
confirmed={'001':'C++ P0-01: equal-net altered components → duplicate1 вместо conflict2','002':'Economic record:6–7 AccountLogin/Broker/Server отсутствуют; namespace не различает accounts','004':'C++ P0-02: разные векторы с равной суммой → duplicate1','005':'C++ NEGATIVE-BUCKET принят; −50+100=50','007':'Reserve evaluator:44–47 проверяет shape/sourceDealId, не exact source/allocation key binding','008':'Reserve evaluator:67–70 unallocated ветвь не отвергает alreadyConsumed>0; global availability не запрашивается','009':'C++ P0-04: NaN risk принят; NAN-LIMIT принят','010':'C++ P0-07-NAN-FILL и P0-10-UNKNOWN-RETRY приняты; обязательность caller не доказана','011':'C++ P0-05: +Infinity reserve принят','012':'Context:19–24,48–53 охватывает четыре слота, initialBuy/initialSell/newFarCandidate вне Far count; полный global registry не проверен','013':'NewFar:119–124 перезаписывает proof identity из caller DTO; provider authenticity не следует из equality','048':'Reserve:61–74 нет equalities eligible=proof.net и farLoss=max(0,−farProof.net); NewFar:121–122 их вычисляет, direct-public mismatch не solver exploit'}
recon='# AUDIT03 CLOSE — сверка ERR / IMP\n\n'+header
recon+='Исторический реестр содержит 50 IDs: P0=14, P1=31, P2=5. Это унаследованный register, а не 50 заново подтверждённых production defects. Новые ERR IDs не присвоены. Ни один OPEN не закрыт. ERR-050 остаётся AMBIGUOUS_SPECIFICATION. Снятая гипотеза о transitionShare не возвращена в дефекты.\n\n| ERR | Priority | Source | Текущая проверка | IMP |\n|---|---|---|---|---|\n'
for e in errors:
 short=e['ID'][-3:];note=confirmed.get(short,'NOT_VERIFIED: историческая запись сохранена; индивидуальная нормативная/кодовая переоценка не завершена')
 recon+=f"| {e['ID']} | {e['Priority']} | `{e['File']}:{e['Lines']}` | {note} | {e['IMP']} |\n"
recon+='\nERR-033 — global funding contract gap и ERR-038 — отсутствие unconditional loss bound остаются P0 blockers, но не объявляются здесь исправимыми одной equality-проверкой.\n\nC++ 16 FAIL включают два явно PROPOSED ожидания (committed equality и exhausted-source semantics): существующий DTO не определяет полный lifecycle, поэтому эти FAIL не превращены автоматически в новые безусловные source defects. Остальные локальные counterexamples также не доказывают работу торгового exploit в disabled main. Все исторические 22 IMP IDs сохраняются без переназначения.\n'
write('HSBI_AUDIT03_CLOSE_FINDINGS_RECONCILIATION_RU.md',recon)
(HERE/'counts.json').write_text(json.dumps(dict(BASE_SHA=BASE,TOTAL_FILES=len(rows),TOTAL_DOCUMENTS=len(docs),DOCUMENTS_FULLY_REVIEWED=sum(x['CoverageStatus']=='FULL' for x in docs),DOCUMENTS_PARTIALLY_REVIEWED=sum(x['CoverageStatus']=='PARTIAL' for x in docs),DOCUMENTS_NOT_REVIEWED=sum(x['CoverageStatus']=='NOT_REVIEWED' for x in docs),PRODUCTION_SOURCES_TOTAL=len(sources),PRODUCTION_SOURCES_FULLY_REVIEWED=0,FUNCTIONS_TOTAL=len(functions),ERRORS_TOTAL=len(errors),ERRORS_P0=sum(x['Priority']=='P0' for x in errors),ERRORS_P1=sum(x['Priority']=='P1' for x in errors),ERRORS_P2=sum(x['Priority']=='P2' for x in errors),FORMULA_FAMILIES_TOTAL=66,FORMULAS_PROVEN_UNDER_ASSUMPTIONS=sum(x[0]=='PROVEN_UNDER_ASSUMPTIONS' for x in proofs.values()),FORMULAS_CONTRADICTORY=sum(x[0]=='CONTRADICTORY' for x in proofs.values()),FORMULAS_INVALID=sum(x[0]=='INVALID' for x in proofs.values()),FORMULAS_UNVERIFIED=66-len(proofs)),indent=2)+'\n')
print('Generated inventory, source index, formula ledger, FSM and findings; semantic gaps preserved.')
