#!/usr/bin/env python3
"""C3 audit reports and traceability from actual results; no contract approvals."""
import ast,json,re
from pathlib import Path
import check_hsbi_02b_r0e_c3_common as a
from hsbi_02b_r0e_c3_decision_proposals import decisions
R=a.ROOT;H='BASE_SHA='+a.BASE+'\n\nAUDIT / PROPOSED / AWAITING_ADMIN_APPROVAL. Production, trading и dispatch запрещены.\n\n'
def load(n):
 f=R/('Tests/Evidence/NEXT_STAGE_02B_R0E_C3_'+n+'.json');return json.loads(f.read_text()) if f.exists() else {}
def write(path,body):(R/path).write_text('\n'.join(line.rstrip() for line in body.rstrip().splitlines())+'\n')
def source_line(path,pattern):
 for i,line in enumerate((R/path).read_text().splitlines(),1):
  if pattern in line:return i
 return None

def matrix():
 cat=json.loads((R/'Tests/Contracts/NEXT_STAGE_02B_R0E_C2_REQUIRED_CATALOG.json').read_text());survivors=load('SURVIVORS');ind=load('INDEPENDENT_TESTS');oldguards=[]
 for g in cat['Guards']:
  mutation=next(m for m in cat['Mutations'] if m['MutationID']==g['MutationID']);review=next((r for r in survivors.get('Rows',[]) if r['MutationID']==g['MutationID']),None)
  oldguards.append(dict(GuardID='C3-AUDIT-'+g['GuardID'],ClauseID=g['ClauseID'],ContractID=g['ContractID'],ObservedSourceFunction=g['SubjectFunction'],SourceFile=mutation['TargetFile'],SourceConditionObserved=[e['old'] for e in mutation['ExactEdit']],ConditionStatus='OBSERVED_IMPLEMENTATION_NOT_INDEPENDENT_ORACLE',PositiveFixture=g['PositiveTestID'],NegativeFixture=g['NegativeTestID'],MutationFixture=g['MutationID'],IndependentExpected='See C3 public-path rows/literal tests for independently tested properties; frozen C2 expected remains a separately identified historical oracle',FrozenEvidence='Tests/Evidence/NEXT_STAGE_02B_R0E_C3_C2_MUTATIONS.json#'+g['MutationID'],C3SurvivorClassification=review['Classification'] if review else 'NOT_A_SURVIVOR',Coverage='INDEPENDENT_PUBLIC_PATH_AUDIT' if review else 'FROZEN_CATALOG_REPRODUCED_NOT_EXHAUSTIVE_INDEPENDENT_CLAUSE_PROOF'))
 # Normative public API obligations with independently written literal tests.
 obligations=[
 ('DTO','Malformed ID/container cannot authorize debit',['authorize','apply_for_test'],'C3-PUBLIC-apply_for_test','C3-GATE-event-bool','C2-MUT-bool-id','REJECT; zero delta'),
 ('SOURCE','Independent source namespace/role must match proof',['verify_allocation_identity','authorize','apply_for_test'],'C3-PUBLIC-verify_allocation_identity','C3-FOREIGN-Magic','C2-C1-MUT-identity-Magic','REJECT; zero delta'),
 ('JOURNAL','Unavailable independent journal cannot produce known resource',['available','authorize','apply_for_test','recover_store'],'C3-PUBLIC-available','C3-GATE-journal-missing','C2-C1-MUT-available-journal-layer','UNAVAILABLE; zero delta'),
 ('PLANNED','Purpose and intent must match independent plan',['authorize','apply_for_test'],'C3-PUBLIC-authorize','C3-GATE-purpose','C2-MUT-planned-purpose','REJECT; zero delta'),
 ('BATCH','Foreign batch/order cannot be netted into target operation',['assess_batch','authorize','apply_for_test'],'C3-PUBLIC-assess_batch','C3-GATE-batch-foreign','C2-C1-MUT-batch-lineage','CONFLICT in pure batch / REJECT in apply; zero delta'),
 ('COST','Unknown basis is not zero; malformed fact returns typed conflict',['cost_coverage','authorize','apply_for_test'],'C3-PUBLIC-cost_coverage','C3-COST-UNKNOWN','C2-MUT-cost-shape-caller','UNKNOWN→UNAVAILABLE; malformed OverlapKnown1→CONFLICT'),
 ('REPLAY','Exact immutable event changes nothing; changed payload conflicts',['authorize','apply_for_test','recover_store'],'C3-EXACT-REPLAY','C3-ALTERED-REPLAY','C2-C1-MUT-composed-replay','NO_OP/CONFLICT; zero delta'),
 ('RECOVERY','Reconstruction is not full current/historical authorization',['recover_store','authorize','apply_for_test'],'C3-PUBLIC-recover_store','C3-GATE-journal-incomplete','C2-C1-MUT-receipt-source','Limited scope; unavailable journal cannot certify funds')]
 required=[]
 for gid,condition,callers,pos,neg,mut,expected in obligations:
  required.append(dict(GuardID='C3-PUBLIC-'+gid,ClauseID=gid,FormalCondition=condition,PublicCallers=callers,PositiveTestID=pos,NegativeTestID=neg,MutationID=mut,IndependentExpected=expected,StateDelta='Checked in C3 invoke/ExecutionTraces for refusal and replay; pure calls do not mutate inputs',MutationProof='Fresh C2 catalog evidence plus C3 survivor probes; not claimed full independent mutation coverage'))
 publication={p:dict(PositiveTestID='C3-PUBLIC-'+p,PositiveTrace=next((r.get('ExecutionTraces',[]) for r in ind.get('Rows',[]) if r['TestID']=='C3-PUBLIC-'+p),[]),MandatoryCondition='Full new-event gates on eligibility/commit, not all gates on every early rejection/replay',Coverage='DECLARED_SCOPE_ONLY') for p in ('authorize','apply_for_test','available','assess_batch','cost_coverage','verify_allocation_identity','recover_store')}
 data=dict(BaseSHA=a.BASE,CatalogVersion='HSBI-C3-AUDIT-1',IndependentTestIDs=[r['TestID'] for r in ind.get('Rows',[])],FrozenGuardRows=oldguards,PublicObligations=required,PublicAPIMatrix=publication,AdministrativeDecisionIDs=[r['DecisionID'] for r in decisions()],CoverageVerdict='PARTIAL: source-level observed clauses and finite probes do not establish universal guard completeness; one C2 redundancy claim disproved')
 write('Tests/Contracts/NEXT_STAGE_02B_R0E_C3_GUARD_MATRIX.json',json.dumps(data,ensure_ascii=False,indent=2));write('Tests/Contracts/NEXT_STAGE_02B_R0E_C3_ADMIN_MATRIX.json',json.dumps(dict(BaseSHA=a.BASE,Rows=decisions()),ensure_ascii=False,indent=2));return data

def main():
 ind,rep,reg,sur,native,executions=[load(n) for n in ('INDEPENDENT_TESTS','REPRODUCTION','REGRESSIONS','SURVIVORS','NATIVE_SUBSET','EXECUTIONS')];mat=matrix()
 write('Docs/NEXT_STAGE_02B_R0E_C3_CONTRACT_CLARIFICATIONS_RU.md','# C3 — уточнения для административного рассмотрения\n\n'+H+'''Нормативная иерархия: первичные Docs08/16/31/32 задают исторические требования; proposed R0E/C1/C2 не утверждаются тестами. Фактический MQL5 source — поведение, а не автоматическое нормативное разрешение. Административные поля прежних16 решений остаются пустыми. Никакой исторический статус не переписан.

## Имена баланса: существенное противоречие

В задании C3 Gross=Consumed+Reserved+Free. В R0E/C2 документах G означает OriginalGrant, а Gross-view означает Reserved+Free. Это две разные величины. Рекомендуется запретить bare Gross и использовать:

OriginalGrant=Consumed+Reserved+RemainingFree; RemainingGross=Reserved+RemainingFree; Available=RemainingFree только после обязательной authority/journal reconciliation. Числа50,10,15,25 дают RemainingGross40; 10+15+40=65 ошибочно. Если Gross в C3 понимается как исходный grant50, его равенство верно; если как RemainingGross40 — неверно. Это naming/schema decision D01/BALANCE-SCHEMA-MAPPING, не ошибка точной арифметики. Никакой новый смысл не вступает в силу автоматически.

## Scope и отсутствующие переходы

C2 публичная composed операция — CONSUME_FREE. Reserve/release/consume-reserved доступны как математические private registry transforms; JournalPayload C2 store допускает только FUND/CONSUME_FREE. C3 проверяет owner algebra отдельно, но не выдаёт это за публичный production reservation lifecycle. Source-local multi-allocation cap не доказывает global economic debit attribution.

C2 Snapshot ID/fresh берутся из independent fixture evaluation context. В Authority нет текущего snapshot-object/receipt registry. Поэтому current C2 proof подтверждает ID binding, не полный snapshot content proof. R0D отдельный snapshot-content тест не доказывает его интеграцию в C2/NewFar. Coherent ID999 в request/context может разрешить fixture debit; authenticity/content остаются UNPROVEN.

## D05 и costs

Префикс fills -15,+100 при cap12: signed loss15→0; current final CONFIRMED совместим с C2 profile, но sticky breach остаётся true, peak cumulative loss15. Выбор signed/peak/sticky — решение администратора. Подтверждённый deal не доказывает batch membership; повторный reference не увеличивает unique volume. Changed history payload между assessments не превращается автоматически в CONFLICT без immutable provider journal.

AdditionalRisk — headroom, не actual debit. Неизвестный cost или risk overlap не0. Малформированный OverlapKnown1 должен быть CONFLICT в pure cost API; C3 показывает, что один C2 survivor не эквивалентен по этому правилу. Денежное небезопасное списание этим не доказано.

## Геометрия и числа

Zero Core недопустим при обязательной BigCore-ноге даже при positive slope. Необходимы min<=Core<=max, допустимая сетка/step/origin, positive required legs, correct ratios/direction и recovery/risk/margin gates. Одно Core>=min недостаточно: min.03/step.02 при origin0 не на сетке, при origin.03 может быть допустимо. Broker volume origin нельзя угадывать; недостаток данных UNPROVEN/UNAVAILABLE.

R0D lattice10^-64, abs<10^65 не является MQL-domain. Settled integer minor units требуют checked overflow; projected subunit losses нельзя округлять до0. Unknown broker precision policy не заменяется HALF_EVEN. Критерии0 и отрицательного margin сохраняются точными.
''')
 write('Docs/NEXT_STAGE_02B_R0E_C3_VERIFICATION_BOUNDARIES_RU.md','# C3 — границы доказательств\n\n'+H+'''| Утверждение | Доказательство | Граница |
|---|---|---|
| C2 published counts | Fresh unchanged function suites and archived strict package | Reproduces historical oracle, not independent economic correctness |
| C3 monetary vectors | Literal integer minor units/coefficient-scale reference | Python fixture/math scope |
| Public acceptance composition | Actual calls/lines and independent negative fixtures | Finite public paths, not universal formal verification |
| Five redundant survivors | Mandatory early schemas/reconstruction + exact-delta algebra + multi-caller probes | Declared C2 API domain only |
| CostSet survivor | Direct pure cost OverlapKnown1 distinguishes original/mutant | Status contract coverage gap; no unsafe debit shown |
| L01/L02 | Actual production functions compiled in disposable C++ subset | Not MetaEditor/MQL5 runtime; g++ shims documented |
| Zero-Core / maxTransition control | Static source + numeric counterexamples | Native production geometry runtime NOT_RUN |
| R0D snapshot content | Frozen separate API with independent original receipt | Not composed C2/current NewFar integration |
| Durable/concurrent exactly-once | No backend | UNPROVEN |
| Broker amounts/fills/authenticity/margin | Fixtures only | UNPROVEN |
| Full global economic funding/NewFar | No production integration | UNPROVEN |

Unknown/unsupported/malformed/unavailable remain distinct according to declared API. Infrastructure exceptions are recorded as INFRASTRUCTURE_ERROR, never semantic mutation kills. Current/archived results, source hashes and actual process commands are separately labelled. Direct roles within one reproduction CLI have computed role outcomes, not invented subprocess exits. Outer EXECUTIONS captures real OS exit codes/stdout/stderr. g++ compile success does not change MQL5_COMPILE=NOT_RUN.

Reconstruction RECONCILED_MODEL_ONLY does not certify historical batch/cost/headroom or authorize a new operation. Immutable receipts and history providers are trusted fixture boundaries, not broker authentication. Reference PASS cannot approve any of16 administrative decisions.
''')
 write('Reports/NEXT_STAGE_02B_R0E_C3_REPRODUCTION_RU.md','# C3 — воспроизведение C2 и provenance\n\n'+H+f'''C2 reference: {rep.get('ReferenceCounts','NOT_RUN')}. Mutation: {rep.get('MutationCounts','NOT_RUN')}. Package: {rep.get('PackageCounts','NOT_RUN')}. Источник — новые C3_C2_REFERENCE/MUTATIONS/PACKAGE JSON, не копирование старых summary.

Сценарии158 — TestID inventory; contexts8 — повторные исполнения, а не независимые доказательства. Full Context0 call-argument duplicate groups: {rep.get('DuplicateContext0CallGroups','NOT_RUN')}. Отсутствие точных совпадений captured-call lists не доказывает независимость всех assertions: fixtures/source50 и часть predicates повторяются. 2462 schema probes — отдельные path edits, не2462 экономические модели. Comparisons9914=2*1264+3*2462 — bookkeeping, не полнота свойств.

Фактические CLI, UTC, OS exit/stdout/stderr — EXECUTIONS.json; commands и stdout/stderr legacy jobs — REGRESSIONS.json. Role execution внутри reproduction одного процесса явно помечен; source/fixture hashes — common pins и BASELINE. Native subset source и compiler stdout/stderr сохранены отдельно. Archived package adapter меняет только root/default/path-relative bookkeeping; его точный код — C3 reproduction runner. Historical bytes и modes не менялись.

Development failures: initial leading-dot integer parser и duplicated timestamp wrapper, затем исправление role Command metadata и C3 regression metadata adapter. Контролируемое прерывание адаптера, остаточная disposable копия R10 и временный R7 S009146/73 зафиксированы отдельно; удалён только session-created untracked каталог, затем выполнен чистый повтор без изменения frozen expectations. Native fixtures усилены фактическими production shape/conservation validators. Они сохранены в DEVELOPMENT.json и исходных log, не превращены в semantic PASS. Все actual final results проверяются package verifier C3.
''')
 lines=['# C3 — аудит шести survivors','',H,'Оригинальный C2 каталог64 killed/6 reported redundant воспроизведён отдельно. Новая классификация не переписывает C2 evidence.']
 for row in sur.get('Rows',[]):
  lines+=['','## '+row['MutationID'],'', 'SourceFunction: '+row['SourceFunction'], 'Classification: '+row['Classification'], 'MandatoryCaller: '+', '.join(row['MandatoryCaller']), 'ExactSourceChange: `'+json.dumps(row['ExactSourceChange'],ensure_ascii=False)+'`','CallerProof: '+row['CallerProof'],'','| Public API | Original negative | Mutant negative | Independent expected | Zero delta |','|---|---|---|---|---|']
  for p in row['IndependentCallerAudit']:lines.append('| '+p['PublicCaller']+' | '+p['OriginalOutcome']['Status']+' | '+p['MutantOutcome']['Status']+' | '+p['IndependentExpected']+' | '+str(p['StateDeltaZero'])+' |')
 lines+=['','Positive controls и actual calls/lines сохранены в SURVIVORS.json. Для outer post-state дополнительно используется алгебра: G=C+V+F, 0<x<=F => G=(C+x)+V+(F-x); lower delta проверяет before/after, остальные rows реконструируются и не меняются. Для schemas удаление нижней проверки не обходит публичный обязательный validation caller. Это объяснение domain-limited, не универсальная полнота mutation coverage.','', 'C2-MUT-cost-shape-caller: counterexample fact.OverlapKnown=1, normal valid claims. Original CONFLICT, mutant UNAVAILABLE; public apply/authorize оба REJECT. Старый causal bool-policy input не обнаруживал это различие. Поэтому глобальная избыточность этого mutant опровергнута на status contract; unsafe acceptance/double spend не доказаны.']
 write('Reports/NEXT_STAGE_02B_R0E_C3_MUTATION_AUDIT_RU.md','\n'.join(lines))
 write('Reports/NEXT_STAGE_02B_R0E_C3_MONEY_CONTRACT_AUDIT_RU.md','# C3 — денежные контракты и production\n\n'+H+f'''Независимые сценарии: {ind.get('Scenarios','NOT_RUN')}; PASS={ind.get('Pass','NOT_RUN')}; FAIL={ind.get('Fail','NOT_RUN')}; INFRA={ind.get('InfrastructureErrors','NOT_RUN')}. Их expected — literals и новый integer coefficient/scale oracle без imports subject evaluator. До/после и trace reserve/release/consume/owner rejection находятся в INDEPENDENT_TESTS.json; raw/posted/currency/grid не смешиваются.

D01 naming conflict описан в CONTRACT_CLARIFICATIONS; исходный grant50, consumed10, reserved15, free25. D02 projection не source; incomplete history unavailable. D03 Small10→ResidualHeld10 и Big0. D04 absolute50 против incremental10/Reserve30. D05 prefix/final/sticky/peak неодинаковы. D06 unknown cost/overlap блокируется. D07 in-memory exact replay0 delta; altered conflict; durable/concurrent unavailable. D08 foreign18 identity fields отвергаются, но trusted fixture provider не broker history. Все эти proposed semantic choices остаются неутверждёнными.

CR09: L1 margin79/transition50, L2 margin-6/transition1: A rejects L2, B positive L1. Cancellation1e28-.010-(1e28-.005)=-.005 точно отрицательна. Sequential reserve1e28 после двух.01 =1e28-.02. Signed64 max+1/min*(-1) недоступны, а не truncated. Лоты требуют min/max/step/origin и positive required legs.

| Production finding | Source/function | Доказательство / требуемое исправление |
|---|---|---|
| L01 / namespace | Include/Money/HSBI_EconomicLedgerTypes.mqh:6–11; HSBI_SameEconomicRecord/HSBI_ClassifyEconomicDuplicate/HSBI_BuildSourceDealKey | Native subset: components60/-10→70/-20 при net50 принимаются как duplicate1, нормативно conflict2. Account/Broker/Server в key отсутствуют. Full immutable payload + namespace после approval |
| L02 | Include/Money/HSBI_AllocationLedgerTypes.mqh:8; HSBI_ClassifyAllocationDuplicate | Native subset: FinalReserve50/Partial0 →0/50 total50, actual1 вместо conflict2 |
| M01 | Include/Money/HSBI_ReserveAllocationTypes.mqh:25–30; HSBI_ValidateReserveConsumptionKey | Local nonempty key/plan checks не связывают все поля с authoritative allocation; frozenR0 behavioral failures сохранены. Требуется allocation-bound durable consumption, не bool hasPrior |
| M02 | Include/Planning/HSBI_NewFarSolver.mqh:124; expectedReserveIdentity/expectedFarIdentity assignment | Expected копируется из проверяемого proof, независимость не доказана. Нужен provider→reconciled record→allocation→expected identity |
| M05 | Include/Money/HSBI_LevelMoneyEvaluator.mqh; reserveGainMoney | Small contribution остаётся source-role decision D03, формула production не изменена |
| Zero-Core | Include/Planning/HSBI_GeometrySolver.mqh:32–35; HSBI_SolveBigGeometry | coreGrid допускает0, slope только nonnegative core. Far.1 coreRatio.01 trendRatio3 smallRatio.1 даёт Core0/Trend.3/Small.01/slope.19; обязательная Core отсутствует |
| CR09 production | Include/Planning/HSBI_FutureSmallProofAggregator.mqh:50 | WORST_CASE выбирает worstTransitionLossLevel, не minCatchUpMargin |
| Persistence | Include/Persistence/HSBI_PersistenceInterface.mqh:7; HSBI_PersistSnapshotStub | success=false, PERSISTENCE_NOT_IMPLEMENTED; durable/CAS/restart UNPROVEN |
| Broker precision/fills/global funding | Provider/backend отсутствует | Fixtures не подтверждают actual broker posted values, partial executions, source-wide economic capital или concurrent settlement |

Native source normative result={native.get('NormativeResult','NOT_RUN')}; finding={native.get('Finding','NOT_RUN')}. Это воспроизведение дефекта, не production PASS. Production modifications=NO. Остальные статические finding не объявлены выполненным MQL5 runtime тестом.

Регрессии: {reg.get('RegressionStatus','NOT_RUN')}; BaselineMatch={reg.get('BaselineMatch','NOT_RUN')}. Исторические R7/R0 FAIL не исправлены. Матрица70 frozen guards и C3 public obligations явно различает reproduction и независимое покрытие; GUARD_COVERAGE=PARTIAL.
''')
 lines=['# C3 — независимая административная матрица','',H,'Все16 решений требуют явного утверждения; ни подписи, ни решения администратора нет. SEMANTIC_CHOICE_READY означает возможность рассмотреть логическое правило, не permission implementation. Данные брокера/размеры buffers/MQL domain/codec/backend требуют отдельных проверок.']
 for row in decisions():
  lines+=['','## '+row['DecisionID'],'']+[k+': '+str(v) for k,v in row.items()]
 write('Reports/NEXT_STAGE_02B_R0E_C3_ADMIN_DECISION_MATRIX_RU.md','\n'.join(lines))
 write('Reports/NEXT_STAGE_02B_R0E_C3_R1_READINESS_RU.md','# C3 — gate будущего R1.1 Economic Ledger Identity\n\n'+H+'''R1_1_START_ALLOWED=NO. Ни C3 COMPLETE, ни reference PASS не является административным approval.

| Gate | Текущее состояние | Требуется до отдельного R1.1 |
|---|---|---|
| Approval | Все16 AWAITING | Явные выбранные schema/namespace/codec/precision зависимости |
| Production allowlist | C3 предполагает только Include/Money/HSBI_EconomicLedgerTypes.mqh; старый R0B R1.1 spec разрешал также2 новых helper headers | Разрешить конфликт scope отдельным заданием; не добавлять helpers автоматически |
| Immutable schema | Production отсутствуют AccountLogin/Broker/Server/currency/precision/SourcePlan/direction/schema envelope | Утвердить полный immutable payload и отдельные mutable reconciliation flags |
| Source namespace | Текущий key symbol|magic|cycle|deal; account отсутствует | Versioned broker/server/account/deal namespace, типы/диапазоны и collision tests |
| Duplicate equality | L01 native confirmed; отдельные Profit/Swap/Commission/Fee игнорируются | Exact raw/component/identity equality; changed payload CONFLICT, exact NO_OP zero deltas |
| Raw vs posted / precision | R0B raw64/NFC proposal vs R0D fixture codec vs integer money architecture | Выбрать source codec и отдельные posted fields; неизвестные broker amounts не money authority |
| Provider boundary | DealID>0/valid flag только shape | Shape не existence; reconciliation provider отдельно, unavailable source нельзя credit |
| Migration | Legacy key без account, truncated serialization | Preserve bytes/schema/hash; append-only authenticated migration or quarantine; не текущий ACCOUNT_LOGIN |
| Rollback | Production phases не начаты | Separate reviewed revert своего будущего commit; no reverse money migration/trades |
| Tests | Новые независимые C3 vectors; точное количество в evidence; native equality defects | Per-field source mutations, account collision, unknown schemas, raw components cancellation, posted mismatch, zero deltas |
| Compile plan | MetaEditor/MT5 отсутствует | Реальный MetaEditor compile main+new MQL harness; g++ extraction не замена |

Предлагаемый будущий порядок: (1) административные решения schema/namespace/raw-vs-posted/codec/legacy unavailable; (2) новое задание с одним явным allowlist и свежим baseline; (3) immutable Economic DTO/source key/equality/serialization и scoped tests без money credits; (4) MetaEditor/native acceptance и review; (5) отдельно остальные ledger/funding/durable/identity/CatchUp/FutureSmall/NewFar этапы по dependency graph. Source identity должна предшествовать allocation provenance; оба — consumption/journal; durable backend и reconciliation — runtime authorization; NewFar не может безопасно обходить предпосылки.

Нельзя одновременно исправлять M01/M02/L02/geometry или реализовывать dispatch в R1.1. Даже при одобрении логической независимости источника broker integration остаётся отдельным приёмочным этапом. Этот документ не меняет production allowlist сейчас.
''')
 package=load('PACKAGE_RESULTS');package_ready=package.get('Positive')=='PASS' and package.get('ExitCode')==0 and package.get('RunnerSourceHash')==a.sha(R/'Tests/Static/check_hsbi_02b_r0e_c3_package.py')
 complete=package_ready and rep.get('ExitCode')==ind.get('ExitCode')==reg.get('ExitCode')==executions.get('ExitCode')==0 and len(sur.get('Rows',[]))==6
 status=dict(BASE_SHA=a.BASE,FINAL_SHA='NOT_EMBEDDED_SELF_REFERENTIAL_PUBLICATION_SHA',REMOTE_SHA_PARITY='PUBLICATION_CHECK_IN_FINAL_RESPONSE',WORKTREE_CLEAN='PUBLICATION_CHECK_IN_FINAL_RESPONSE',PRODUCTION_FILES_UNCHANGED='YES_BASELINE_VERIFIED',C2_REPRODUCTION='PASS' if rep.get('ExitCode')==0 else 'NOT_RUN',REFERENCE_TESTS='PASS_PYTHON_ONLY' if ind.get('ExitCode')==0 else 'NOT_RUN',MUTATION_AUDIT='STATUS_COVERAGE_GAP_CONFIRMED',GUARD_COVERAGE='PARTIAL',MONEY_CONTRACT_AUDIT='DECISION_REQUIRED',PACKAGE_INTEGRITY='PASS_C2_REPRODUCED_C3_VERIFIED' if package_ready else 'PENDING_FINAL_CHECK',REGRESSION_STATUS=reg.get('RegressionStatus','NOT_RUN'),REGRESSION_BASELINE_MATCH='YES' if reg.get('BaselineMatch') else 'NOT_RUN',ADMIN_DECISIONS_REVIEWED='16',ADMIN_APPROVAL_COMPLETE='NO',R1_1_START_ALLOWED='NO',PRODUCTION_REMEDIATION_ALLOWED='NO',TRADING_LOGIC_START_ALLOWED='NO',BROKER_DISPATCH_ALLOWED='NO',REAL_TRADING_ALLOWED='NO',STAGE_02B_R0E_C3_COMPLETE='YES' if complete else 'NO')
 write('Reports/NEXT_STAGE_02B_R0E_C3_FINAL_VERDICT_RU.md','# C3 — итог независимого аудита\n\n'+H+'''Опубликованные C2 числа воспроизводятся, но не доказывают полноту денежных контрактов или mutation coverage. Из6 survivors5 обоснованы в заявленном domain,1 не является глобально эквивалентным по status contract (OverlapKnown1). Unsafe debit этим не показан. L01/L02 production defects подтверждены extracted native subset; MQL5 runtime NOT_RUN. Snapshot-content integration, public reservation lifecycle, durable/concurrent/global funding/NewFar остаются UNPROVEN.

Нормативные блокеры: Gross naming ambiguity; D05 signed/sticky/peak cap choice; codec/numeric/MQL domains;16 неутверждённых решений; R1.1 one-file allowlist против старого расширенного spec. Решение: R1.1 не допускать автоматически. C3 COMPLETE означает завершённый аудит с явно зарегистрированными пробелами, а не готовность implementation/trading.

Git publication SHA/parity не встраиваются в собственный commit; фактические значения сообщаются после публикации. Ни один исторический verdict не изменён. MQL5_COMPILE=NOT_RUN; MQL5_TESTS=NOT_RUN; STRATEGY_TESTER=NOT_RUN.

[C3_FINAL_STATUS]
'''+'\n'.join(k+'='+v for k,v in status.items())+'\n[/C3_FINAL_STATUS]')
 print('C3 reports generated; preliminary complete',complete)
if __name__=='__main__':main()
