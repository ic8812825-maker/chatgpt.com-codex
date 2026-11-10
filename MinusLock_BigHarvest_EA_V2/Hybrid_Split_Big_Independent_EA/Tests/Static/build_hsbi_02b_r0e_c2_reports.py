#!/usr/bin/env python3
"""Generate only new C2 Russian reports from actual evidence, no administrative approval."""
import json,re
from pathlib import Path
import check_hsbi_02b_r0e_c2_contracts as t
R=t.ROOT
HEADER='BASE_SHA='+t.BASE+'\n\nPROPOSED / AWAITING_ADMIN_APPROVAL. Только audit/test-only; production и trading запрещены.\n\n'
def load(name):
 p=R/('Tests/Evidence/NEXT_STAGE_02B_R0E_C2_'+name+'.json');return t.subject.evidence.loads(p.read_text()) if p.exists() else {}
def write(path,text):(R/path).write_text(text)
def main():
 tests,mu,repro,reg,pkg=[load(n) for n in ('TEST_RESULTS','MUTATION_RESULTS','REPRODUCTION','REGRESSIONS','PACKAGE_RESULTS')]
 ready=tests.get('ExitCode')==mu.get('ExitCode')==repro.get('ExitCode')==reg.get('ExitCode')==pkg.get('ExitCode')==0 and pkg.get('Positive')=='PASS' and pkg.get('NegativeFailed')==0
 write('Docs/NEXT_STAGE_02B_R0E_C2_GUARD_COVERAGE_AND_RECOVERY_SCOPE_RU.md','# C2 — clauses, композиция и scope recovery\n\n'+HEADER+'''Матрица: Tests/Contracts/NEXT_STAGE_02B_R0E_C2_VERIFICATION_MATRIX.json. GuardID/ClauseID связывает exact source edit с positive/negative TestID; фактические вызовы сохраняются в SubjectCalls. Семантически независимые receipt clauses (nonnegative risk, principal binding, required sum, core debit), purpose/intent и immutable allocation event/policy проверены отдельно. Денежные ожидания literal/independent integer coefficient-scale encoder R0D; subject evaluator не вычисляет expected.

Обязательные public callers: apply_for_test→authorize→_authorize→schema Request/Store/Authority→economic_record→_reconcile_store→_bind_allocation→verify_allocation_identity→assess_batch/cost_coverage→available→checked delta. available/recover_store вызывают _reconcile_store самостоятельно. Pure assess_batch/cost_coverage/identity проверяют свои DTO напрямую. Private helpers не являются authorization API и Python privacy не security sandbox.

| Property | VerifiedByRecovery | RequiredAuthority | UnverifiedDependency | ReturnedScope | PermittedDownstreamUse |
|---|---|---|---|---|---|
| Accounting reconstruction | Да, exact journal replay/balance | Independent coreJournal/history | Durable bytes authenticity | RECONCILED_MODEL_ONLY | Accounting fixture result |
| Immutable receipt bindings | Да, digest/source/allocation/event/context/equations | Independent receipt journal | Authenticity historical provider | RECONCILED_MODEL_ONLY | Binding comparison |
| Historical source reconciliation | Да, immutable economic digest | Independent economic history | Broker authenticity/completeness | RECONCILED_MODEL_ONLY | Fixture reconciliation |
| Historical batch membership | Полностью не повторяется | Historical batch provider record | Сохранённый digest не доказывает provider fact | UNPROVEN | Не historical full proof |
| Historical cost coverage | Полностью не повторяется | Historical cost policy/provider | Trusted receipt boundary | UNPROVEN | Не historical full proof |
| Historical available headroom | Полностью не повторяется | As-at-commit eligibility facts | Полный historical authorization | UNPROVEN | Не разрешение нового расхода |
| Durable authenticity | Нет | Durable backend/receipts | Backend отсутствует | UNPROVEN | Нельзя заявлять durable commit |
| Concurrent ordering | Нет | CAS/locks/transaction ordering | Concurrent backend отсутствует | UNPROVEN | Нельзя заявлять concurrent exactly-once |

Пример C2-recovery-scope: reconstructed debit50 может соответствовать receipt required50.5 при исходных50. Recovery лишь RECONCILED_MODEL_ONLY; новая authorization50+.5 отклоняется. Это не доказательство double spend. Новый расход всегда повторяет текущую полную authorize; recovered store не eligibility token.

AdditionalRisk остаётся headroom, не actual debit:50/10/.5→required10.5/free40/consumed10. G=C+Reserved+Free; семантика RemainingGross/RemainingFree и R0D numeric domain не меняются. Нет глобального account-economic funding proof. Fixture completeness не broker evidence.

Redundant guards сохраняются как survivors: отдельный CostSet schema caller дублируется обязательным CostClaim validator на причинном bool-input; dual-caller mutation отдельно обнаруживается. Прежние outer post-state/format/self-repair clauses также могут быть защищены ранним C2 schema/reconstruction. Доказательство caller и whole-domain regression хранится в MUTATION_RESULTS; исключение не считается kill.
''')
 write('Reports/NEXT_STAGE_02B_R0E_C2_REPRODUCTION_RU.md','# C2 — независимое воспроизведение C1\n\n'+HEADER+f'''Штатный C1: {repro.get('StockReference',{}).get('Pass','NOT_RUN')} PASS; mutation kills {repro.get('StockMutations',{}).get('Killed','NOT_RUN')}, redundant {repro.get('StockMutations',{}).get('RedundantSurvivors','NOT_RUN')}; package negative {repro.get('StockPackage',{}).get('NegativePassed','NOT_RUN')}.

C2-01: bool PolicyVersion в fact+claim при root1 разрешает in-memory debit10 из50 в C1. Это ошибка типов, не создание денег/real trade. C2-02: nested batch None/empty/bool, empty history record и snapshot без payload дают TypeError/KeyError в C1. C2 typed DTO устраняет expected-input exceptions. C2-03: все шесть отдельных mutations сохраняют840 PASS старого suite; отдельные negative fixtures отличают оригинал от мутанта. Оригинальные guards работают; это coverage gaps.

C2-04: last-key-wins C1 принимает скрытый FAIL/exit1 при последнем PASS/0; обратный порядок фиксируется отдельно и может корректно отвергаться. Опубликованные evidence не обвиняются в дубликатах. C2-05: recovery ограничен reconstruction/bindings, не полным historical reauthorization; см. scope table.

Полные входы, source edits/hashes, original/mutant outcomes: Tests/Evidence/NEXT_STAGE_02B_R0E_C2_REPRODUCTION.json. Старый strict package запускается на точном Git archive C1. Adapter меняет только archive root/path-relative bookkeeping в отдельном module; исходный checker и исторические evidence не изменяются. Actual adapter source hash — hash C2 reproduction runner.
''')
 # Complete finding contract fields in the report; actual outcomes remain linked to immutable execution rows.
 f=R/'Reports/NEXT_STAGE_02B_R0E_C2_REPRODUCTION_RU.md'
 with f.open('a') as out:
  out.write("\n## Поля воспроизведения по FindingID\n\n")
  details=[
   ('C2-01','cost_coverage / authorize / apply_for_test','normal50/10/.5; C1 StockReference APPLY-positive passed','fact+claim PolicyVersion=True, root1','typed refusal, no debit','Findings[C2-01]','free50→40, consumed0→10, revision2→3','CONFIRMED','test-only malformed identifier, no real trade'),
   ('C2-02','_authorize / economic_record / recover_store','normal apply/recover controls in stock840','nested expected None/empty/bool; extra empty record; missing snapshot payload','typed outcome, no unexpected exception','Findings[C2-02-*] + SnapshotMissingPayload','InputsUnchanged recorded for apply probes; snapshot state delta not separately measured in old run','CONFIRMED','expected-input exceptions reproduced; C2 zero deltas tested separately'),
   ('C2-03','_reconcile_store / _authorize / _bind_allocation','original+mutant full C1 suite840 PASS for each edit','six exact source edits in SixAdditionalMutations','original rejects; mutant violates literal binding requirement','SixAdditionalMutations','explicit state summaries/zeroDelta in causal apply; receipt checks pure','CONFIRMED','coverage gap, not original bypass'),
   ('C2-04','check_hsbi_02b_r0e_c1_package.load / verify','untampered exact C1 archive PASS','duplicate Result/ExitCode, both orders; disposable hashes refreshed','reject ambiguous duplicate-key JSON','DuplicateJSON','disposable bytes only; real history unchanged','CONFIRMED','last-wins ambiguity; reverse order may correctly reject'),
   ('C2-05','recover_store / authorize','normal stock recovery control passed','historical50 versus receipt required50.5','limited reconstruction only; new authorize REJECT','RecoveryScope','inputsUnchanged=True','UNPROVEN','historical full eligibility outside declared recovery scope; not claimed double spend')]
  for finding,fn,pos,edit,exp,actual,delta,classification,boundary in details:
   out.write('### '+finding+'\n\n'+ '\n'.join(k+': '+v for k,v in [('FindingID',finding),('SourceFunction',fn),('PositiveControl',pos),('ExactInputOrSourceChange',edit),('IndependentExpected',exp),('ActualOutcome','Tests/Evidence/NEXT_STAGE_02B_R0E_C2_REPRODUCTION.json#'+actual),('StateDelta',delta),('ProofBoundary',boundary),('Classification',classification)])+'\n\n')
 write('Reports/NEXT_STAGE_02B_R0E_C2_TEST_AND_MUTATION_RESULTS_RU.md','# C2 — результаты проверок\n\n'+HEADER+f'''Различные reference scenarios={tests.get('Scenarios','NOT_RUN')}; contexts={len(tests.get('ContextConfigurations',[]))}; executions={tests.get('Executions','NOT_RUN')}; reference PASS={tests.get('Pass','NOT_RUN')}. Отдельные schema probes={tests.get('SchemaProbes','NOT_RUN')}, каждый один раз вне context cross-product; comparisons={tests.get('Comparisons','NOT_RUN')} (2 на execution +3 на schema probe). Эти величины не суммируются в число независимых сценариев.

Mutation catalog={mu.get('CatalogSize','NOT_RUN')}; killed={mu.get('Killed','NOT_RUN')}; redundant survivors={mu.get('RedundantSurvivors','NOT_RUN')}; unexplained={mu.get('UnexplainedSurvivors','NOT_RUN')}; infrastructure errors={mu.get('InfrastructureErrors','NOT_RUN')}. Каждый redundant survivor имеет mandatory caller proof и whole reference-domain regression. UNSAFE_ACCEPTANCE_KILL и STATUS_CONTRACT_KILL различаются в строках. Начальные два survivors сохранены в DEVELOPMENT.json; выявлено дублирование fact/claim guards, добавлены dual-caller и direct-schema причинные probes, без искусственных exceptions.

Package positive={pkg.get('Positive','NOT_RUN')}; negative passed={pkg.get('NegativePassed','NOT_RUN')}; negative failed={pkg.get('NegativeFailed','NOT_RUN')}. Старые46 классов остаются отдельно помеченной группой, strict JSON/schema/clause probes добавлены отдельно. Parser/import/runtime error не semantic kill. JSON всех новых artifacts проходит общий strict loader.

Regression status={reg.get('RegressionStatus','NOT_RUN')}; baseline match={reg.get('BaselineMatch','NOT_RUN')}; runs={len(reg.get('Runs',[]))}. R7/R0 сохраняют исходные exit1 и57/5,35/46. Нет выдуманного standalone02A; повторяется доступный no-trade scan. Commands, timestamps, source/runner hashes, stdout/stderr: REGRESSIONS.json. Adapted C2 runner — новый реальный файл со своим source hash, не подмена C1 runner.

DEVELOPMENT.json сохраняет initial8FAIL/8INFRA (nullable batch dereference и status expectation) и начальный archive adapter failure. Ни одна ошибка не удалена из evidence. Дополнительно сохранены initial regression copy-race, неверный путь mandatory package probe и перезапись inventory edit при reseal. Две bool-counter probes первоначально получили FAIL из-за ожидаемого кода позднего слоя: strict JSON уже корректно отклонял их как PACKAGE_SCHEMA; изменён диагностический expected code, защита не ослаблена. DEVELOPMENT.log/MUTATION.log/REPRODUCTION.log/REGRESSIONS.log сохраняют последовательность запусков. Expected malformed DTO не скрывается blanket except Exception; неожиданные implementation errors видимы как INFRASTRUCTURE_ERROR.

Команды: check_hsbi_02b_r0e_c2_reproduction.py; check_hsbi_02b_r0e_c2_contracts.py; check_hsbi_02b_r0e_c2_mutations.py; run_hsbi_02b_r0e_c2_regressions.py; build_hsbi_02b_r0e_c2_catalog.py; check_hsbi_02b_r0e_c2_package.py --seal --self-test. build_hsbi_02b_r0e_c2_reports.py генерирует только новые документы из evidence. Default package run read-only.

MQL5_COMPILE=NOT_RUN; MQL5_TESTS=NOT_RUN; STRATEGY_TESTER=NOT_RUN. Production не исправлялся. Broker/global funding/durable/concurrency/NewFar — UNPROVEN.
''')
 old=(R/'Reports/NEXT_STAGE_02B_R0E_C1_ADMIN_DECISIONS_RU.md').read_text();body=old[old.index('## Contract:'):];write('Reports/NEXT_STAGE_02B_R0E_C2_ADMIN_ADDENDUM_RU.md','# C2 — административное дополнение\n\n'+HEADER+'''Прежние16 решений остаются AWAITING_ADMIN_APPROVAL. Strict ID/nested shape/JSON исправляют implementation ранее предложенного контракта; отдельный экономический размер/источник средств не выбирается. Полная shape до replay и REJECT malformed authority token — уточнения API scope. Ограниченный recovery не расширяется до historical authorization. Новый validation inventory/strict evidence grammar — технические proposed contracts, требуют review, не самостоятельные16 новых экономических решений. Влияние на R1.1: использовать approved immutable namespace/equality и typed boundary; реализацию не начинать.

''' +body)
 status={'ADMIN_APPROVAL_COMPLETE':'NO','PRODUCTION_REMEDIATION_ALLOWED':'NO','TRADING_LOGIC_START_ALLOWED':'NO','BROKER_DISPATCH_ALLOWED':'NO','REAL_TRADING_ALLOWED':'NO','STAGE_02B_R0E_C2_COMPLETE':'YES' if ready else 'NO','CONTRACT_FREEZE_CANDIDATE_READY':'YES' if ready else 'NO'}
 write('Reports/NEXT_STAGE_02B_R0E_C2_FINAL_VERDICT_RU.md','# C2 — итоговый verdict\n\n'+HEADER+'''C1 исторический COMPLETE/READY не переписан. Независимые пробы показали собственные input-contract defects и недостаточность покрытия, поэтому прежняя готовность не подтверждается как полное дозакрытие обязательного C1-контракта. Его штатные840/54+1/46 остаются истинными.

C2 READY означает только готовность ограниченного test-only пакета к следующему независимому review и административному рассмотрению. Не доказана универсальная корректность модели или readiness советника. Ни одно административное решение автоматически не утверждено. После C2 остановиться; отдельное задание R1.1 только после явного утверждения.

[C2_FINAL_STATUS]
'''+'\n'.join(k+'='+v for k,v in status.items())+'\n[/C2_FINAL_STATUS]\n')
 print('reports READY',ready)
if __name__=='__main__':main()
