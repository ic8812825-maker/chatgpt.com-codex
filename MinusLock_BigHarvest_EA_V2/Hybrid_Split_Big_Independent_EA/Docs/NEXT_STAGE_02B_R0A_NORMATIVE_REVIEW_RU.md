# 02B-R0A — адресный нормативный review

Проверенная база: `cb5e55cb38aa4f2eb5b58e5218462c6738f3097a`, ветка `work`, UTC проверки `2026-11-04T01:18:36Z`. Режим `NORMATIVE_FREEZE_PREPARATION / AUDIT_AND_TEST_ONLY`. Все новые экономические формулировки — **PROPOSED**, не утверждённый production-норматив. `STAGE_02B_R1_IMPLEMENTATION_ALLOWED=NO`.

## Проверка базы

Исходная ветка work; local/remote HEAD совпали с ожидаемым cb5e55c…; дерево чистое. `git merge-base --is-ancestor cb5e55c HEAD` успешен. Полный список файлов commit получен через git diff предыдущего audit SHA→cb5e55c. Все записи A, .mq5/.mqh production не изменены. MetaEditor/MT5/Wine в настроенной среде недоступны; Python3.12.14 и g++ присутствуют. Условия baseline выполнены до новых записей. Reset/rebase/checkout не выполнялись.

## Прочитанные материалы и нормативный статус

- Полностью рассмотрены R0 Findings, Decisions, Test Results, Contract Freeze Proposal и R1 Implementation Task; matrix/results/source manifest/guard check JSON прочитаны программно по всем записям; runner и MQL5 template прочитаны целиком.
- Применены Docs/04,08,16,24,27,30,31,32 и адресные выводы Stage02A. Документы со статусом source of truth не отменяются более новой датой отчёта.
- R10 replay binding прямо ограничивает доказательство внутренней integrity/ownership предъявленных источников. R12A Ledger/Batch/Fill normative decisions относятся к static qualification и не меняют production accounting или historical R10/R11/R12 roots.
- R0/данный R0A — предложения; поля утверждения пусты. Исторические README acceptance blocks не разрешают изменения кода/торговлю.

## Матрица нормативных противоречий

| ID | Точная действующая область / формулировка | Неоднозначность и последствия | Предложение / решение |
|---|---|---|---|
| D-01 | Docs/04/08: sum buckets=allocatable; Docs/32: buckets+consumed<=allocatable | OriginalGrant и remaining не разделены; consumed может считаться повторно, остаток теряется | equality для committed, balances отдельно; PROPOSED |
| D-02 | Docs/24: projected!=actual; Basket.recoveryMoney — projected basket | Имя не доказывает availability | разные DTO/conversion receipts; PROPOSED |
| D-03 | Docs/31 Reserve roles Core/Trend; aggregate содержит Small | Small10 выглядит Reserve10, но direct actual spend не доказан | Small в ResidualHeld, no BigReserve; PROPOSED |
| D-04 | FarLossIncrease название против max(0,-FarNetCurrent) | при20 Reserve результат -35 или+5 | ABSOLUTE как recommended gate, incremental diagnostic; PROPOSED |
| D-05 | Docs/04/08 actual closing net против projected transition loss | projected10 не отменяет actual15>cap12 | разные типы и post-fill SAFE_BLOCKED; PROPOSED |
| D-06 | per-leg safety и Catch-Up safety без risk-basis карты | 4+1 может быть5 либо duplicate | charge once либо block overlap; PROPOSED |
| D-07 | identical NO_OP; evaluator возвращает REJECT+NOOP reason | enum outcome и факт mutation не одно и то же | typed NO_OP, eligibility!=commit; PROPOSED |
| D-08 | actual source/history против caller flags/self-copy | source existence не доказана, account namespace отсутствует | independent authority/reconciliation; PROPOSED |
| CR-09 | Docs/30 не определяет worst Catch-Up как max TransitionLoss | +29 выбран вместо другого -16 | all-level min margin A либо ограниченный B; DECISION_REQUIRED |
| ZERO-CORE | Docs/04 каждому required lot нужен Vmin/grid | slope .19 позволяет Core0 | reject candidate; отдельный geometry этап |
| Residual | Docs/08: Residual остаётся нераспределённым | Residual bucket и intermediate Unallocated — разные понятия | явно учтённый non-spendable ResidualHeld; только после D-01/D-03 approval |

Точные affected functions и source lines — в [кандидате](NEXT_STAGE_02B_R0A_CONTRACT_FREEZE_CANDIDATE_RU.md), сохранённые ссылки R0 и `NEXT_STAGE_02B_R0_SOURCE_MANIFEST.json`; функции и старые нормы не менялись.

## Адресная проверка доказательств

R0 runner не изменён. Повторный запуск дал 81 native subset, 58 reference, 13 mutation probes, 46 mismatches, exit1. Технический baseSha внутри runner остаётся историческим 4e7d911…; actual testedHead в новом RECHECK — cb5e55c… . Это различие версий объяснено, а не исправлено переписыванием старого runner/evidence.

Expected outcomes задаются proposed CR отдельно от production actual. В 13 probes есть шесть fault mutations, пять repair sensitivity и два diagnostic probes; «13 detected» не является mutation score исправленной production. Проверена запись sourceFile и изменение original/mutant hash. Шесть fault mutants дают нормативно неправильный outcome на соответствующем положительном/отрицательном контроле; repair probes лишь устраняют конкретное расхождение. WORST_CASE probe меняет selector на final level: это **не** реализация minimum margin policy.

Старый oracle независим от production helper imports, но неполон. Новый probe `LEGACY-ORACLE-plan-revision` получает ALLOW при PlanID/Revision999: `oracle_consumption` не проверяет эти поля. Новые тесты proposed authorization отклоняют их. Старый conservation helper использует float-compatible math/zip на test fixtures; он не является полным schema/precision validator. Самопроверки equality/digest показывают различия payload, но не подлинность реального broker source.

C++ source extraction использует ограниченный brace/regex extractor и убирает include directives; string/numeric/ZeroMemory shims и stub level digest не являются MetaEditor. Hash доказывает identity проверенной копии, не broker authenticity. MQL5 template не компилировался. Независимый Decimal oracle имеет точный test profile USD/2 digits и linear unit-price fixtures; он проверяет предложенную арифметику/границы, не currency conversion или broker modes. In-memory apply не доказывает durable crash/atomicity. Обязательность вызовов полной production цепочки остаётся UNPROVEN.

## Поправка к сводной отчётности: 29, не 3

Git содержит 29 новых файлов cb5e55c, а не три изменённых файла: Docs2, Reports3, Tests/Contracts1, Tests/Evidence21, Tests/MQL5 template1, Tests/Static runner1. Три ссылки на основные документы не составляют полного инвентаря. Исторический commit/evidence не переписываются; полный фактический список:

- `Docs/NEXT_STAGE_02B_R0_CONTRACT_FREEZE_PROPOSAL_RU.md`
- `Docs/NEXT_STAGE_02B_R1_IMPLEMENTATION_TASK_RU.md`
- `Reports/NEXT_STAGE_02B_R0_DECISIONS_REQUIRED_RU.md`
- `Reports/NEXT_STAGE_02B_R0_FINDINGS_RU.md`
- `Reports/NEXT_STAGE_02B_R0_TEST_RESULTS_RU.md`
- `Tests/Contracts/NEXT_STAGE_02B_R0_ADVERSARIAL_MATRIX.json`
- `Tests/Evidence/NEXT_STAGE_02B_R0_GUARD_CHECK.json`
- `Tests/Evidence/NEXT_STAGE_02B_R0_RESULTS.json`
- `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R10.log`
- `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R10_acceptance.log`
- `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R10_mutations.log`
- `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R10_properties.log`
- `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R10_regressions.log`
- `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R12A_causal.log`
- `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R12A_contract.log`
- `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R12A_coverage.log`
- `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R12_acceptance.log`
- `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R12_alignment.log`
- `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R7_frozen.log`
- `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R8.log`
- `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R8_acceptance.log`
- `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R8_current.log`
- `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R8_properties.log`
- `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/R8_sensitivity.log`
- `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/adversarial.log`
- `Tests/Evidence/NEXT_STAGE_02B_R0_RUNS/summary.json`
- `Tests/Evidence/NEXT_STAGE_02B_R0_SOURCE_MANIFEST.json`
- `Tests/MQL5/HSBI_02B_R0_MoneyContracts.mq5.in`
- `Tests/Static/check_hsbi_02b_r0_ledger_integrity.py`

Категории и полный machine inventory сохранены в `Tests/Evidence/NEXT_STAGE_02B_R0A_VERIFICATION_SUMMARY.json`. Ни список ссылок, ни краткое резюме не должны использоваться как file count.
