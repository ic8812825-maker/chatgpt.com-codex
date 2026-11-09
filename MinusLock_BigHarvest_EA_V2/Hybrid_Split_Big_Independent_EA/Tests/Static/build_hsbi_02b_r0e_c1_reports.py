#!/usr/bin/env python3
"""Russian C1 reports from actual evidence. No historical writes; pending package stays NO."""
import ast,json
from pathlib import Path
import check_hsbi_02b_r0e_c1_contracts as t
import check_hsbi_02b_r0e_c1_package as p
ROOT=t.ROOT

def header(s):return '# '+s+'\n\nBASE_SHA='+t.BASE+'\n\nPROPOSED / AWAITING_ADMIN_APPROVAL. Audit/test-only; production/trading/dispatch запрещены.\n\n'
def write(path,text):(ROOT/path).write_text(text.rstrip()+'\n')
def main():
 tests=json.loads((ROOT/p.TEST).read_text());mut=json.loads((ROOT/p.MUT).read_text());repro=json.loads((ROOT/p.REPRO).read_text());reg=json.loads((ROOT/p.REG).read_text());package=json.loads((ROOT/p.RESULT).read_text()) if (ROOT/p.RESULT).exists() else {}
 mathematical=not tests['Fail'] and not tests['InfrastructureErrors'] and not mut['UnexplainedSurvivors'] and not mut['InfrastructureErrors'] and reg['BaselineMatch'] and repro['ExitCode']==0
 ready=mathematical and package.get('CatalogDigest')==p.catalog.canonical_digest(p.catalog.expected_catalog()) and all((ROOT/f).is_file() and p.sha(ROOT/f)==h for f,h in package.get('SourceHashes',{}).items()) and package.get('Positive')=='PASS' and package.get('NegativePassed')==len(p.PROBE_IDS) and package.get('NegativeFailed')==0
 addendum=header('02B-R0E-C1 — дополнение к предлагаемым контрактам')+'''## Нормативный статус и границы

D-01–D-08, CR-09, NUM/SNAP, FUNDING-GLOBAL-ATTRIBUTION, MQL-DOMAIN и BALANCE-SCHEMA-MAPPING не утверждены. Исторические READY/COMPLETE не переписаны. Новое дозакрытие исправляет тестовую реализацию и доказательность пакета, а не production-экономику. Reference PASS не превращает PROPOSED в APPROVED.

Scope и доверенные inputs каждого API определены до реализации в NEXT_STAGE_02B_R0E_C1_API_SCOPE_AND_COMPOSITION_RU.md. Independent authority — fixture provider boundary, не broker authentication. Экономическая история и current context независимы от presented proof; source origin Plan1 и current Plan10 допустимы. В публичном составном apply нет параметра «готовое разрешение», он всегда заново авторизует запрос.

| ClarificationID | Изменение / текущий proposed контракт | Характер / административный выбор / R1.1 |
|---|---|---|
| C1-JOURNAL / D02,D07 | AvailableReserve только после complete independent core journal + commit receipts и reconstruction. Unknown не known0. Private арифметический helper не public proof | Исправление scope/реализации; не новый экономический выбор. Влияет на будущий caller контракт |
| C1-BATCH / D05,D08 | Independent expected broker/server/account, batch/order/position/cycle/symbol/currency/digits/volume/required source set. Существование fill не равно membership | Усиление provenance и scope. Порядок netting/cap требует утверждения D05; broker partial execution NOT_RUN |
| C1-COST / D06 | Полный independently supplied applicable-cost set. REQUIRED покрыт ровно один раз; UNKNOWN/unknown overlap UNAVAILABLE; KNOWN_ZERO и NOT_APPLICABLE отдельные dispositions | Уточнение полноты, не выбор размера buffer. Применимость/суммы задаёт provider, не request |
| C1-EVENT / D08,D07 | EconomicEventID, AllocationEventID, ConsumptionEventID раздельны; expected из history/allocation/context. _bind_allocation связывает immutable vector с ledger | Уточнение identity и обязанностей callers; field/schema migration требует утверждения прежних решений |
| C1-REPLAY / D07 | Сначала typed namespace/request + history + complete journals + immutable economic source; changed valid source CONFLICT. Затем exact known receipt NO_OP, changed payload CONFLICT, новые current gates только для нового event | Явный PROPOSED fixture priority. Администратор должен выбрать приоритет source conflict / receipt replay / unavailable authority; не implemented durable exactly-once |
| C1-HISTORICAL / D07,D08 | Receipt хранит независимо validated evaluationContext as-at-commit. Recovery связывает source, allocation digest/event и planned operation с reconstructed ledger, а не копирует presented identity в expected | Исправление прототипа C1. Historical context — fixture journal fact, authenticity/durable persistence UNPROVEN |
| C1-EVIDENCE | Required catalog из versioned executable spec, не из результатов. Уникальные status fields; provenance всех финальных evidence roles; dynamic subject call trace | Техническое исправление verification, не экономическое решение |

## Точные деньги и accounting

G=C+Reserved+Free; Gross=Reserved+Free. Компоненты Profit/Swap/Commission/Fee сохраняют знак. Raw sum и posted grid проверяются отдельно; source=(Broker,Server,Account,Deal). Валюта/digits не выводятся из суммы и не конвертируются неявно. Точная арифметика и codec R0D неизменны. MQL5 int64 domain не расширяется до Python Fraction domain.

C1 публичная composed операция ограничена CONSUME_FREE. PrincipalAmount задаётся independent planned-operation context и сверяется с request. AdditionalRisk — safety headroom deduction, не реальный расход. RequiredBalance=PrincipalAmount+AdditionalRisk, RequiredBalance<=Free; DebitAmount=PrincipalAmount; C'=C+Debit, Free'=Free-Debit. Buffer не становится Consumed. Пример: G50, principal10, risk0.5 →required10.5, consumed10, free40. Principal50/risk0.5 отклоняется; principal50/risk0 может полностью израсходовать50. Полный Catch-Up lot/Far/margin proof этим не реализован.

REQUIRED signed actual cost, ещё не включённый в reconciled net, даёт UNAVAILABLE: модель не создаёт локальный broker posting и не угадывает conversion. Полный registry CostSet содержит и dispositions KNOWN_ZERO/NOT_APPLICABLE; клиент не может удалить строку, скрыв отсутствие применения. Independently complete empty CostSet допускает empty claims.

## Partial-fill profile

Только явно названный PROPOSED_SIGNED_BATCH_NET_V1: unique принадлежавшие target batch fills, exact summed volume и signed net; loss=max(0,-net). Cap проверяется и при неполном prefix. CONFIRMED требует полного RequiredDeals и expectedVolume. Foreign account/lineage/currency блокируются до netting. Неизвестная policy/history UNAVAILABLE. Этот профиль не утверждает универсальное netting, sticky OVER_CAP или peak path-loss; такие варианты остаются административным выбором D05.

## Replay и authority

Exact replay означает только воспроизведение подтверждённого in-memory fixture receipt с zero deltas. Он не подтверждает новые current provider facts. Historical allocation/identity проверяется по independent journal/core reconstruction и stored evaluationContext, current Plan/Revision/Snapshot могут измениться без нового расхода. Current allocation provider не заменяет historical core allocation при replay; конфликт economic source в выбранном C1 profile приоритетнее NO_OP. Иная политика приоритетов требует явного выбора D07.

Input shape до lookup проверяет namespace/event ranges, required top-level fields и тип identity container; полная identity value verification относится к новому событию. Изменённый known payload (включая неполную identity dict) не может стать NO_OP; его статус CONFLICT. Синтаксически недопустимые top-level DTO/ID/amount отклоняются раньше. Unexpected programming exceptions не маскируются REJECT.

## План применения

Сначала независимое review C1 и административный выбор прежних D/NUM/SNAP contracts, затем отдельный verified-baseline R1.1. Namespace/immutable Economic Ledger equality остаётся первой узкой production фазой; funding/durable/identity/Catch-Up/FutureSmall/NewFar идут по прежнему dependency graph. Никакой реализации R1.1 сейчас. Global economic debit attribution, broker authenticity/precision/margin, durable CAS/crash recovery и full NewFar integration остаются UNPROVEN.
'''
 write('Docs/NEXT_STAGE_02B_R0E_C1_CONTRACT_ADDENDUM_RU.md',addendum)
 # Preserve the preimplementation API document, append generated inventory once.
 api=ROOT/'Docs/NEXT_STAGE_02B_R0E_C1_API_SCOPE_AND_COMPOSITION_RU.md';content=api.read_text().split('## Финальный inventory публичных функций')[0].replace('`costs_status`, ','').replace('`reserve_available`, ','').replace('full fixture allocation binding','allocation-ID/event binding; money vector separately validated')
 content+='''\n## Финальный inventory публичных функций\n\nPrivate helpers с underscore не являются authorization entry points. Публичные математические helpers возвращают только локальные результаты; они не могут заменить composed store/authority schema. Импортированные number/canonical/digest — frozen R0D primitives. Полный scope identity helper: source/current/event/AllocationID binding; monetary vector/currency/ledger source проверяет обязательный _bind_allocation.\n\n'''
 for node in ast.parse((ROOT/p.mu.TARGET).read_text()).body:
  if isinstance(node,ast.FunctionDef) and not node.name.startswith('_'):
   kind='COMPOSED_OR_PROOF' if node.name in ('authorize','apply_for_test','available','recover_store','verify_allocation_identity','assess_batch','cost_coverage') else 'MATHEMATICAL_OR_SHAPE_ONLY'
   content+=f'- `{node.name}` — {kind}; SourceLine={node.lineno}. '+('Zero deltas кроме apply_for_test; preconditions и authority приведены в таблице.' if kind=='COMPOSED_OR_PROOF' else 'Не spending authorization; типы/диапазоны задаёт exact R0D и локальная schema; ошибки формы Malformed/Unsupported видимы. Caller для spending — authorize/apply_for_test.')+'\n'
 content+='\nnew_store создаёт пустой fixture store; snapshot_store только копирует/checksums store и не доказывает completeness; recover_store обязан независимо сверить оба journals. available возвращает account-scoped registry total одной валюты; authorize отдельно ограничивает debit allocation-local Free. assess_batch не отменяет реальные fills; будущий Economic Ledger обязан учитывать их независимо от cap. C1 store не является полным broker-economic ledger. Completeness относится к объявленному fixture domain, не доказывает полноту broker account history. Historical evaluationContext хранится как as-at-commit provider fact, не строится из предъявленной identity при восстановлении.\n'
 write(str(api.relative_to(ROOT)),content)
 reproduction=header('02B-R0E-C1 — независимое воспроизведение замечаний')+f"Штатный R0E: {repro['StockReference']['passed']} PASS; исходный каталог13: {sum(r['Killed'] for r in repro['StockMutations'])}/13; старые package probes23: {repro['StockPackage'].get('negativePassed')}/23. Это отдельные executions, не новый общий числитель. Команды/UTC/TestedSHA/SourceHashes в REPRODUCTION.json. Архив074165b получен git archive; /tmp предыдущего review не использовался.\n\n"
 for row in repro['PackageGaps']+repro['Findings']:
  reproduction+=f"## {row['FindingID']} — {row['Classification']}\n\nSource: {row['SourceFile']} / {row['SourceFunction']}.\n\nExpected: {row.get('IndependentExpected')}.\n\nActual: `{json.dumps(row.get('ActualOutcome'),ensure_ascii=False)}`.\n\nBoundary: {row.get('ProofBoundary')}. Полные positive controls, inputs и deltas — JSON.\n\n"
 reproduction+='## Три дополнительные mutations\n\n'
 for row in repro['AdditionalMutations']:reproduction+=f"- {row['MutationID']}: stock={row['Stock']['passed']} PASS, original={row['OriginalNegativeOutcome']}, mutant={row['MutantNegativeOutcome']}; {row['Classification']}.\n"
 reproduction+='\nGrid case — прямое принятие record, не доказанный spend. Journal case — false known available при реально блокируемом operate, не double spend. Partial fills/cost/allocation cases классифицированы как неполный scope, исправленный новыми mandatory callers C1. C1-09 исходные ссылки проверены против реально вызываемых операций; новая матрица также содержит observed SubjectCalls.\n'
 write('Reports/NEXT_STAGE_02B_R0E_C1_REPRODUCTION_RU.md',reproduction)
 results=header('02B-R0E-C1 — результаты tests/mutations/package/regressions')+f"Reference: {tests['Scenarios']} различных сценариев × {len(tests['ContextConfigurations'])} contexts = {tests['Executions']} executions; PASS={tests['Pass']}, FAIL={tests['Fail']}, INFRA={tests['InfrastructureErrors']}. Comparisons={tests['Comparisons']} — два top-level comparison на execution, не количество независимых сценариев. Context0 Input.Calls содержит фактические аргументы заявленного public operation; остальные contexts ссылаются на этот fixture. SubjectCalls захватывает реально вызванные операции.\n\nMutation catalog={mut['CatalogSize']}; killed={mut['Killed']}, redundant survivors={mut['RedundantSurvivors']}, unexplained={mut['UnexplainedSurvivors']}, infra={mut['InfrastructureErrors']}. Unsafe acceptance и status-only kills хранятся раздельно. Исходные R0E13 и три initial survivors сохранены в REPRODUCTION, не переименованы в новый каталог.\n\n"
 results+='''## Объяснённый survivor

C1-MUT-outer-poststate удаляет повторную внешнюю проверку balance. До delta обязательная _reconcile_store реконструирует все строки по independent journal; private delta проверяет выбранную строку до и после exact debit, все остальные строки неизменны. Public apply проверяет status private delta. Поэтому при допустимом входе условие повторной проверки не может стать false: G=C+V+F, x<=F ⇒G=(C+x)+V+(F-x). Мутация не меняет семантику в этом domain. Весь suite мутанта проходит; отрицательный тест allocation corruption по-прежнему отклоняется обязательным ранним слоем. Не создавалось искусственного обхода private validator ради kill. Это survivor, а не PASS/killed.

## Первоначальные ошибки раскрыты

DEVELOPMENT.json хранит initial contract run:4FAIL/12INFRA из-за ambient Decimal addition в независимом fixture receipt builder; заменено integer minor arithmetic. Malformed nested source record в prototype вызывал TypeError; malformed external journal ранее возвращал UNAVAILABLE; добавлены shape validation и causal semantic mutations без засчитывания runtime errors как kills. Прототип C1 также принимал historical receipt с Magic999 при history Magic7: добавлены historical source/allocation/evaluationContext bindings и три causal probes/mutations. Первый regression runner временно хранил baseline archives перед recursive R7 scan, получил S009 guards219/unique73 и56/6; archive materialization перенесена после recursive suites, frozen test не менялся. Draft source metadata не считается final execution evidence.

## Package

'''
 results+=f"Текущее сохранённое выполнение: Positive={package.get('Positive','NOT_RUN')}; negativePassed={package.get('NegativePassed','NOT_RUN')}; negativeFailed={package.get('NegativeFailed','NOT_RUN')}. Обязательный каталог содержит {len(p.PROBE_IDS)} package probes:23 прежних класса отдельно и {len(p.NEW_PROBES)} C1 extensions. Hashes disposable artifacts обновляются для semantic isolation; реальные historical bytes/modes не меняются. Required test/guard/mutation inventory вычисляется из executable specifications и их source pins, не из проверяемого evidence. Пустой mutation catalog, coherent deletion теста, дубликаты/unknown IDs, conflicting statuses, wrong section/case, regression hashes и неверные source mappings обязаны отклоняться.\n\n"
 results+='## Регрессии\n\n| Suite | Exit | PASS | FAIL | BaselineMatch | Classification |\n|---|---|---|---|---|---|\n'
 for r in reg['Runs']:results+='| '+' | '.join(str(r.get(k)) for k in ('ID','ExitCode','PassCount','FailCount','BaselineMatch','Classification'))+' |\n'
 results+='''
Исторические FAIL R7/R0 не скрыты. R7 S040B/S040C/S044A/S044B — старые status/markers; S045 — frozen manifest. Обязательными остаются действующие runtime/no-trade guards и baseline preservation, не возврат исторических status labels. C1 не изменяет production, поэтому подтверждённой новой функциональной регрессии при baseline match нет. 02A standalone suite отсутствует; executable report commands покрыты named runs. R0E_mutations — ссылка на реальное reproduction execution, не отдельный фиктивный CLI запуск, который мог бы перезаписать historical JSON.

Команды: check_hsbi_02b_r0e_c1_reproduction.py; check_hsbi_02b_r0e_c1_contracts.py; check_hsbi_02b_r0e_c1_mutations.py; run_hsbi_02b_r0e_c1_regressions.py; build_hsbi_02b_r0e_c1_catalog.py; check_hsbi_02b_r0e_c1_package.py --seal --self-test. Повторный default package run read-only. build_hsbi_02b_r0e_c1_reports.py генерирует только новые отчёты из фактических JSON. Unknown/outside-domain не преобразуется в PASS.

MQL5_COMPILE/MQL5_TESTS/STRATEGY_TESTER=NOT_RUN; MetaEditor/terminal64/Wine availability сохранена в preservation. C++ extraction не MQL5 runtime. Broker authenticity/precision/margin, real partial fills, global funding/debit attribution, durable/concurrent enforcement и full NewFar остаются UNPROVEN. Флаги complete/fresh — fixture provider assumptions, не broker receipts. Ни одна таблица не разрешает trading или implementation.
'''
 write('Reports/NEXT_STAGE_02B_R0E_C1_TEST_AND_MUTATION_RESULTS_RU.md',results)
 admin=header('02B-R0E-C1 — административные решения и уточнения')+'Сохраняются16 прежних решений. C1 усиливает их технические критерии, не создаёт отдельное экономическое решение для каждого теста. Реального утверждения нет. Replay priority и batch netting — явно предложенные исполнимые fixture profiles, требуют выбора в D07/D05 до production.\n\n'
 impacts={'D-02':'Journal-aware AvailableReserve, unknown не known0.','D-05':'Independent batch membership; предложенный signed-batch-net/cap-on-prefix; sticky historical breach/peak loss не решены.','D-06':'Полный applicable cost set; buffer gate, не actual Consumed; размеры из provider, не выбирались.','D-07':'Exact receipt versus immutable history conflict: C1 proposed conflict-first для economic source и unavailable при incomplete journals; current gates не повторяются для known receipt.','D-08':'Раздельные economic/allocation/consumption events, immutable vector binding, historical receipt context.'}
 for name in p.DECISIONS:
  admin+=f"## Contract: {name}\n\nRecommendation: Сохранить прежнее PROPOSED решение до явного утверждения; {impacts.get(name,'C1 не меняет экономическую семантику; прежний scope/approval неизменён.')}\nExactProposedContract: См. C1 CONTRACT_ADDENDUM и исходный R0E sheet.\nAlternatives: Для D05 net batch loss либо отдельно утверждённый peak/sticky cap; для D07 receipt-first либо conflict-first с явно заданной unavailable policy. Остальные альтернативы R0E сохранены.\nMigrationImpact: Не выполняется; C1 store/schema/receipts только fixtures, не совместимый production migration codec.\nUnprovenDependencies: broker authenticity, global funding/debit attribution, durable/CAS/recovery, MQL5 runtime и full NewFar integration.\nR1Impact: Новое отдельное задание только после approved dependencies; production сейчас запрещён.\nApprovalStatus: AWAITING_ADMIN_APPROVAL\nAdministratorDecision:\n\nApprovalDate:\n\nApprovalIdentifier:\n\n"
 write(p.SHEET,admin)
 verdict=header('02B-R0E-C1 — итоговый verdict')+f"Предыдущий R0E READY=YES переоценён: штатные728/13/23 воспроизводятся, но найденные пробелы не позволяют принимать его как полный проверенный package. Исторический документ не изменён. C1 предлагает отдельное техническое дозакрытие: {tests['Scenarios']} сценария, {tests['Executions']} executions, {mut['Killed']} обнаруженных mutations и {mut['RedundantSurvivors']} объяснённый redundant survivor. Итоговый COMPLETE разрешён только после фактических package probes и baseline preservation.\n\n"
 verdict+='C1 public apply ограничен registry CONSUME_FREE с полным заявленным fixture chain; reservation math отдельно, broker dispatch отсутствует. Не утверждаются live broker funding, durable receipt authenticity или полнота производственной цепочки NewFar. Это не исправление production M-01/M-02/L-01/L-02/M-05/Zero-Core/persistence.\n\n'
 verdict+='[C1_FINAL_STATUS]\n'
 for field,value in p.POLICY.items():
  if field in ('STAGE_02B_R0E_C1_COMPLETE','CONTRACT_FREEZE_CANDIDATE_READY'):value='YES' if ready else 'NO'
  verdict+=field+'='+value+'\n'
 verdict+='[/C1_FINAL_STATUS]\n\nREADY означает пригодность ограниченного C1 пакета к независимому review и административному рассмотрению, а не утверждение contracts. Пока package NOT_RUN/FAIL, COMPLETE/READY остаютсяNO. Final publication SHA/parity сообщаются после реального push; self-referential SHA внутрь commit не подставляется. После C1 остановиться.\n'
 write(p.VERDICT,verdict)
 print('REPORTS mathematical=',mathematical,'package=',package.get('Positive','NOT_RUN'),'ready=',ready)
if __name__=='__main__':main()
