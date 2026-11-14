# HSBI — GitHub delivery recovery / PR preflight

UTC 2026-11-14T16:15:12.956196+00:00. Только диагностика. Никаких push/merge/веток/PR/новых commits/тестов/компиляции. Этот новый отчёт не входит в закреплённые14 файлов commit10d4 и не должен незаметно попасть в будущий PR этого commit. Исходный commit не изменён.

## 1. Git и целостность

Repository `ic8812825-maker/chatgpt.com-codex`; origin fetch/push `https://github.com/ic8812825-maker/chatgpt.com-codex.git`; branch work. До отчёта git status --porcelain пуст, exit0. git fetch origin refs/heads/work:refs/remotes/origin/work exit0; git ls-remote origin refs/heads/work exit0, SHA `b4d8f1ea5caf492f3abd030e5502d40582c52dc8`. Local HEAD `10d4c376d9a71d9b0fbd5e2c9dd4894480136558`, parent `b4d8f1ea5caf492f3abd030e5502d40582c52dc8`. `git cat-file -t` exit0=`commit`; `git cat-file -p` exit0, полный объект ниже. git merge-base origin/work HEAD exit0=`b4d8f1ea5caf492f3abd030e5502d40582c52dc8`; git rev-list --left-right --count origin/work...HEAD exit0=`0 1`. База сейчас не устарела, ancestry допускает fast-forward на один commit. Это свойство Git DAG, не разрешение protected-branch push.

```text
tree e386ac0af5e4eee737ceabf146c990bbecce2290
parent b4d8f1ea5caf492f3abd030e5502d40582c52dc8
author Игорь Чернов <ic8812825@gmail.com> 1794668835 +0000
committer Игорь Чернов <ic8812825@gmail.com> 1794668835 +0000

docs(hsbi): publish AUDIT03 R5-R7 audit progress

Exact snapshot transfer of the 14 AUDIT03 files changed by the source audit commit; no audit-branch history merged. Production, historical evidence, Docs, Tests and workflows are unchanged. Audit research remains partial; this commit does not authorize trading or production remediation.

Source-Audit-Commit: f70b5da703c56e60438f0fab44443bcb5d4a34bf
Source-Audit-Parent: 5ef8983f1e91e3f4cb3b659de2e2e3c0b9268ae2
Target-Work-Base: b4d8f1ea5caf492f3abd030e5502d40582c52dc8

```

`git fsck --full --no-reflogs` exit0:25 dangling blobs, ошибок missing/corrupt/hash mismatch нет. Dangling blobs не являются повреждением и не удалялись. Полный вывод:

```text
dangling blob 508051c548fc31df2f5520662127e4afa8f457e3
dangling blob f708aa8b5614700162e080ac22793abd5f5282c2
dangling blob 9d0b56e86c86398aafbde8eb3f877fb103a2c00f
dangling blob f40d7a66370e81c1ba546e2287e9c394fd022b72
dangling blob b014992a7a0d9d22d45f8941514bf86417730abb
dangling blob ff96aa7f4dd1d6f89571b3d0c0053b18aacaf68c
dangling blob 1897a77d7d8696eea65d65b87fd3dcff200cdc41
dangling blob 4d988686ff623043042c0f4055ef791d1f196505
dangling blob ac181459ce2c707d828059190d90114a4e9400df
dangling blob 8e9d71ae0c0457d52c49a4bac19da8c58ac23bc5
dangling blob 77a4742d53909e16d693be270db19323002e93a5
dangling blob 44ac1cacd17e5afa832559ba1412c14acaec01e5
dangling blob 74b6240c145c72d3c137a7e5790880fab479f825
dangling blob 823da6102d45eacf0c7c896aa64a057158fb7bcd
dangling blob b5cfd8149a354760900bcbb39040064fb5aa0392
dangling blob ced056842dc956bd056eaf9dba68cd25864481e8
dangling blob 18572bd3599eb97ae59cc9928a54e12972556b48
dangling blob cdd808e8904cd47a05285e8be18d55f241e49a36
dangling blob 235caa7bd2f4ac1f2020d0a65770555e36ec0ae3
dangling blob 6a5c32ae600a5bedd40eee15f0cab16af885b1f3
dangling blob a85d346b6811a1567bead75a6348dd92655a2663
dangling blob af63f6a3b6f9c5456be5232b1b8ee6cacf3ce308
dangling blob f06590539e7442a7c18291350ed07e208ef1282d
dangling blob 5f6d88abcbb94ace41a1e9c9ea0e095ca2a06bdf
dangling blob 0d704db901071d7f8b95b55341bc6cdc879a8f05

```

Полная история родителей сохранена в приложении,1348 строк; SHA256 точного вывода `git rev-list --parents --reverse 10d4c376d9a71d9b0fbd5e2c9dd4894480136558`: `0eb5453da0292607cd61ac083a636e0c259c33264d76986c227e9b4f0fb8ba25`. git diff base local --check exit0. Ни один Git diagnostic не является торговым/математическим тестом.

## 2. Полные14 файлов

Каждая строка получена из git diff --numstat и git diff --name-status; SHA256 относится к blob локального10d4. Whole-repository tree comparison доказал: только эти14 путей различаются. Production74, Tests/Docs/historical evidence/workflows и файлы других проектов не изменены. Часть разрешённых AUDIT03 Markdown исторических разделов обновлена намеренно.

| Path | Status | Additions | Deletions | Bytes | SHA256 |
|---|---|---:|---:|---:|---|
| `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_ALL_ERRORS_RU.md` | M | 202 | 1 | 178662 | `f4886389895afd600f08aee4203e5d7a3064bef7a187c566e9b7381b47aeb0f4` |
| `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md` | M | 36 | 0 | 89980 | `f494a3e49bb825267ce3f89b0e23b312951c7570ab2850d4f626aa5afa978613` |
| `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_BASELINE_AND_PRESERVATION_RU.md` | M | 1580 | 0 | 873169 | `f9aa763cc1d9b8ff537051cb914d1c82dde1a9c4806b959d7bd50a60cbcbe459` |
| `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_COMPLETENESS_MATRIX_RU.md` | M | 308 | 0 | 43709 | `a73ef614e1f1daf6b9de3e59cb53098ba8807b6228ed7871280b30813122e73e` |
| `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_DOCUMENT_COVERAGE_RU.md` | M | 620 | 3 | 677988 | `8c67f995d850b38758412a36dfcd01df1517dfce168eca7bd0a8313e61b06fb9` |
| `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_FINAL_CLOSURE_READING_LOG_RU.md` | A | 1740 | 0 | 219262 | `6c081341be77744dd6a7bf553463527c98a7fc8ab16d48d018bff3b131eddd5d` |
| `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_FINAL_VERDICT_RU.md` | M | 456 | 0 | 68137 | `9970949313c3530a4dbc4d7baff8516662bc444c05366887cb1282866207b475` |
| `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_FORMULA_CATALOG_RU.md` | M | 1424 | 2 | 252431 | `a26b56436d5f44b1ebb681d678a1993e3273aadc243cd0dd61e12ab787042085` |
| `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_FSM_COMPLETE_MATRIX_RU.md` | A | 400 | 0 | 47801 | `12454cdd66e3b72f0f2b2f3af21a2f99203fb3954237af13f3bac430e09e4556` |
| `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_GUARD_CALLER_CROSSWALK_RU.md` | A | 2130 | 0 | 286286 | `076638849713555acaf7d31eec7e6b8d68604f9f3b42161bc49b9f4d00a010cc` |
| `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_R2_WORK_IN_PROGRESS_RU.md` | A | 957 | 0 | 79688 | `44ab61b18077a9fddd7ee5d6b23114e94be6a901eeb3e4e03d266c0afcee1e87` |
| `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_R4_GITHUB_PUBLICATION_RU.md` | A | 326 | 0 | 40804 | `602d89828e9ba384de5e5f04a4b311f12939ae140758f57eeedf70734df29e0d` |
| `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_R7_GIT_PUSH_DIAGNOSTICS_RU.md` | A | 227 | 0 | 23373 | `82816859ae4d9c071665265ea51a2f89e34961a4cad259d3cb36c10626a9d932` |
| `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_R7_RECOVERY_PATCH_RU.md` | A | 2629 | 0 | 655515 | `acb47ba09b5f38cacda204efb55a1c9d1bcaeeed90d42b25dfd0c0a5f64c1659` |

Итого additions13035/deletions6. Файлы совпадают с14 snapshot versions из исходногоf70b5da; provenance записан в commit body. Никакие дополнительные audit-branch commits не стали родителями10d4.

## 3. Актуальные правила и предел сведений

Официальная страница https://github.com/ic8812825-maker/chatgpt.com-codex/rules/12711484 повторно прочитана HTTP200. ChatGPT1 id12711484 enabled, target branch; ref conditions include [`~DEFAULT_BRANCH`,`~ALL`], exclude[]. Действующие правила:

- deletion и non_fast_forward запрещены;
- pull_request id82037334; allowed merge methods merge/squash/rebase; required_approving_review_count=0, но require_code_owner_review=true, require_last_push_approval=true, dismiss_stale_reviews_on_push=true, required_review_thread_resolution=true, require_extra_approval_for_unattributed_changes=true;
- code_scanning id82037335: CodeQL, alerts_threshold=errors, security_alerts_threshold=high_or_higher;
- code_quality id82037336: severity=all;
- required_deployments id82045783: environments=[], конкретной среды не задано.

bypassActors=null в public HTML означает недоступность полного списка, не подтверждённое отсутствие actors. Их использование запрещено. `gh api repos/ic8812825-maker/chatgpt.com-codex/rulesets/12711484` exit1: `Get "https://api.github.com/repos/ic8812825-maker/chatgpt.com-codex/rulesets/12711484": Forbidden`. Это ограничивает authenticated metadata/permissions, но само по себе не доказывает невозможность Git push. Мы не пробовали push и не диагностируем server rejection.

PR approval count0 не отменяет Code Owners/last-push требования. Нужны подходящие reviewers и разрешение threads; фактические reviewers/permissions не установлены. Содержание файлов GitHub config/CODEOWNERS вне проекта не менялось. Полная готовность CodeQL/Quality для нового14-file commit не подтверждена: он ещё не опубликован, checks на нём отсутствуют. Нельзя заранее обещать green CI без изменения запрещённых workflows.

## 4. Существующий PR #4

https://github.com/ic8812825-maker/chatgpt.com-codex/pull/4 повторно HTTP200: DRAFT, closedTime=null, base work@b4d8f1ea5caf492f3abd030e5502d40582c52dc8, head audit/hsbi-audit03-github-closure-r4@5ef8983f1e91e3f4cb3b659de2e2e3c0b9268ae2,2commits. Draft сам блокирует merge до ready-for-review. Reviews/CodeQL/Quality/threads должны быть удовлетворены; полного mergeable/reviewDecision ответа не получено. Наличие refs/pull/4/merge (`3070a926762b794a9fe9042cef6b8a9d8c89a4d1`) не подтверждает merge permission или завершённые checks.

Публичная /pull/4/files HTTP200 содержит ровно16 AUDIT03 путей; список совпадает с git diff base..PRhead. /pull/4.diff перенаправился на недоступный proxy endpoint и дал Tunnel connection failed:403 Forbidden (диагностический Python exit1); этот способ не принят за проверенный. Безопасный fallback — обычная официальная HTML files page, без tunnel workaround.

PR4 files:16; local files:14; intersection:12, все12 конечных blobs различаются. Это **различие scope/content**, а не доказанный textual merge conflict. Реальная конфликтность future merge не проверялась операцией merge.

### Четыре PR4-only файла (исключены из10d4)

| Path | Delivery risk |
|---|---|
| `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_FSM_REVIEW_RU.md` | Не входит в14-file diff; не добавлять без отдельного решения |
| `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_GLOBAL_PROPERTIES_RU.md` | Не входит в14-file diff; не добавлять без отдельного решения |
| `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_R3_STATIC_READING_METHOD_RU.md` | Не входит в14-file diff; не добавлять без отдельного решения |
| `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_SOURCE_FUNCTION_MAP_RU.md` | Не входит в14-file diff; не добавлять без отдельного решения |

Local-only relative to PR4: `HSBI_AUDIT03_R7_GIT_PUSH_DIAGNOSTICS_RU.md`, `HSBI_AUDIT03_R7_RECOVERY_PATCH_RU.md`. Полный список16 PR4 путей:

```text
MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_ALL_ERRORS_RU.md
MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md
MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_BASELINE_AND_PRESERVATION_RU.md
MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_COMPLETENESS_MATRIX_RU.md
MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_DOCUMENT_COVERAGE_RU.md
MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_FINAL_CLOSURE_READING_LOG_RU.md
MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_FINAL_VERDICT_RU.md
MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_FORMULA_CATALOG_RU.md
MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_FSM_COMPLETE_MATRIX_RU.md
MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_FSM_REVIEW_RU.md
MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_GLOBAL_PROPERTIES_RU.md
MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_GUARD_CALLER_CROSSWALK_RU.md
MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_R2_WORK_IN_PROGRESS_RU.md
MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_R3_STATIC_READING_METHOD_RU.md
MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_R4_GITHUB_PUBLICATION_RU.md
MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_SOURCE_FUNCTION_MAP_RU.md
```

### Подтверждённая содержательная зависимость

`HSBI_AUDIT03_SOURCE_FUNCTION_MAP_RU.md` содержит0 индивидуальных `| Function ID |` cards в published work и в10d4, но199 в PR4 head. Поэтому утверждение текущих14-file отчётов о сохранении199 карт относится к прежней audit-ветке, не к самодостаточному work tree. Есть declared thematic map, но он не заменяет199 individual cards. Публикация ровно14 файлов сохраняет их bytes, однако не доставляет все supporting R4 artefacts. Также PR4-only R3_STATIC_READING_METHOD отсутствует в14-file transfer. Не расширять diff автоматически. Это отдельный content readiness вопрос, а не Git corruption или основание включать весь PR4.

## 5. Варианты доставки — только план

**A. Рекомендуемый для точного14-file diff:** после отдельного разрешения на временный PR ref, создание/публикация ref, указывающего **точно10d4**, в этом же repo; отдельный PR→work с проверкой base/head и ровно14 путей. Не использовать audit-branch историю PR4. Текущее задание НЕ разрешает создание ref или PR; прежний запрет других веток остаётся не снятым. Возможность создания ref без обхода~ALL не проверена записью и не обещана. После публикации обязательны checks, reviewers, threads; исходныйSHA сохраняется у head. Merge-commit сохраняет10d4 как ancestor, final work tip получает новыйSHA. Squash/rebase создают новыйSHA доставленного commit; provenance надо записать явно. Никакой merge этим планом не разрешается.

До A владелец должен решить supporting-artifact gap: принять ровно14-file snapshot как частичную доставку с явным external dependency либо отдельно разрешить новый минимальный commit с выбранными supporting reports. Второй вариант изменяет scope/SHA и требует новой проверки. В этой диагностике файлы не добавлялись в10d4.

**B. Использовать существующий PR4:** сейчас он даёт16-file old snapshot, не требуемый14-file результат. Доставка через его head потребовала бы новых изменений и отдельного разрешения на старую audit-ветку;10d4 не является потомком её опубликованногоhead. Прямое перемещение head на10d4 было бы non-fast-forward и запрещено. Новый descendant correction мог бы дать другойSHA и потребовал бы точного удаления лишнего diff/совмещения12 overlapping files и полного review. Не рекомендуем без отдельного scope/branch разрешения. PR4 не закрывать и не merge автоматически.

**C. Оставить immutable10d4 локально и предоставить patch владельцу:** сохраняет исходный commit и14 SHA256, не публикует. Внешний maintainer применяет через свой разрешённый PR workflow; новыйSHA после применения должен быть сверён по tree/blobs и source provenance. Это fallback, не PUBLICATION_COMPLETE.

**Недопустимо:** прямой push вопреки PR, использование bypass actor, merge PR4 ради обхода, force/reset/rebase/cherry-pick при этой диагностике, изменение workflows/защиты, создание repo/fork. Если origin/work изменится до разрешённой доставки, не переписывать10d4: повторить preflight и согласовать отдельный новый commit/merge-процесс с сохранением sourceSHA.

## 6. Проверка опубликованного audit state

Восемь файлов verdict/registry/catalog/source-map/matrices повторно получены с raw.githubusercontent.com на полном base SHA HTTP200 и побайтно сверены с Git blobs. Ниже статусы документов, а не новое исполнение исторических tests или автоматическое подтверждение production.

| Пакет | Опубликованный вывод / фактическое различие | Граница |
|---|---|---|
| FULL_SYSTEM_AUDIT_02 | PARTIAL;9 P0 source defects+1unimplemented; P1:8source/contract+3unverified+3unimplemented;49formula=23conditional+11conflict+15unverified | Native NOT_RUN; нет global funding/fullFSM/trading/loss/profit proof |
| DG01 | contract preparation READY_FOR_ADMIN_DECISION; PARTIAL_NATIVE_PENDING;16decisions not approved | Reference62cases и6mutations исторические; не native/CAS/broker proof |
| AUDIT03 published work verdict | Старый блок47ERR/22IMP/60F остаётся в FINAL_VERDICT | Не согласован с actual published50ERR/22IMP/66F; не считать этот блок текущим complete summary |
| AUDIT03 prepared10d4 |51ERR/23IMP/66F; current R7 explicitlyPARTIAL |73GRD не полный нормативныйcensus;199individualfunctioncards не находятся в14-file tree |

### Все P0/P1 AUDIT02: сохранённая опубликованная классификация

Source SHA256 всех29 строк DEFECT_MATRIX сверены с актуальными published blobs; mismatches0. Это проверка актуальности source pins, не новое доказательство всех классификаций и не native PASS.

| ID | Severity | Published classification | Source |
|---|---|---|---|
| FSA-001 | P0 | CONFIRMED_SOURCE_DEFECT | `Include/Money/HSBI_EconomicLedgerTypes.mqh:9` |
| FSA-002 | P0 | CONFIRMED_SOURCE_DEFECT | `Include/Money/HSBI_AllocationLedgerTypes.mqh:8` |
| FSA-003 | P0 | CONFIRMED_SOURCE_DEFECT | `Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:35` |
| FSA-004 | P0 | CONFIRMED_SOURCE_DEFECT | `Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:35` |
| FSA-005 | P0 | CONFIRMED_SOURCE_DEFECT | `Include/Risk/HSBI_RiskGateResult.mqh:6` |
| FSA-006 | P0 | CONFIRMED_SOURCE_DEFECT | `Include/Execution/HSBI_TransactionTypes.mqh:9` |
| FSA-007 | P0 | CONFIRMED_SOURCE_DEFECT | `Include/Money/HSBI_AllocationLedgerTypes.mqh:7` |
| FSA-008 | P0 | CONFIRMED_SOURCE_DEFECT | `Include/Money/HSBI_MoneyState.mqh:5` |
| FSA-009 | P0 | CONFIRMED_SOURCE_DEFECT | `Include/Core/HSBI_Context.mqh:33` |
| FSA-010 | P0 | UNIMPLEMENTED | `Include/Planning/HSBI_NewFarSolver.mqh:94` |
| FSA-011 | P1 | CONFIRMED_SOURCE_DEFECT | `Include/Planning/HSBI_GeometrySolver.mqh:21` |
| FSA-012 | P1 | UNIMPLEMENTED | `Include/Core/HSBI_StateMachine.mqh:5` |
| FSA-013 | P1 | UNIMPLEMENTED | `Include/Persistence/HSBI_PersistenceInterface.mqh:7` |
| FSA-014 | P1 | UNIMPLEMENTED | `Hybrid_Split_Big_Independent_EA.mq5:35` |
| FSA-015 | P1 | CONFIRMED_CONTRACT_CONFLICT | `Include/Planning/HSBI_FutureSmallProofAggregator.mqh:23` |
| FSA-016 | P1 | CONFIRMED_CONTRACT_CONFLICT | `Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:22` |
| FSA-017 | P1 | CONFIRMED_SOURCE_DEFECT | `Include/Planning/HSBI_FutureSmallSolver.mqh:57` |
| FSA-018 | P1 | CONFIRMED_CONTRACT_CONFLICT | `Include/Planning/HSBI_FutureSmallSolver.mqh:12` |
| FSA-019 | P1 | UNVERIFIED | `Include/Money/HSBI_CostModel.mqh:15` |
| FSA-020 | P1 | UNVERIFIED | `Docs/03_FULL_SYSTEM_MANUAL_RU.md:9` |
| FSA-026 | P1 | UNVERIFIED | `Tests/Reference/hsbi_02b_r0h_native_harness.mq5:21` |
| FSA-027 | P1 | CONFIRMED_SOURCE_DEFECT | `Include/Persistence/HSBI_ExecutionJournal.mqh:25` |
| FSA-028 | P1 | CONFIRMED_CONTRACT_CONFLICT | `Include/Planning/HSBI_FutureSmallSolver.mqh:113` |
| FSA-029 | P1 | CONFIRMED_SOURCE_DEFECT | `Include/Money/HSBI_BasketMoneyEvaluator.mqh:11` |

### Все опубликованные P0/P1 AUDIT03 — issue inventory, не новое исполнение

Ниже сохранены classifications из опубликованного реестра; карточки048–050 добавлены из его актуального конца. Все OPEN. Не считать строки независимыми действующими EA exploits; часть root causes пересекается с FSA.

| ID | Severity | Scope | Published classification | Source |
|---|---|---|---|---|
| HSBI-A03-ERR-001 | P0 | Economic source / replay | SOURCE_DEFECT | Include/Money/HSBI_EconomicLedgerTypes.mqh:9 |
| HSBI-A03-ERR-002 | P0 | Source discovery | SOURCE_DEFECT | Include/Money/HSBI_EconomicLedgerTypes.mqh:6-7 |
| HSBI-A03-ERR-003 | P1 | Serialization | POTENTIAL_RISK | Include/Money/HSBI_EconomicLedgerTypes.mqh:11 |
| HSBI-A03-ERR-004 | P0 | Allocation replay | SOURCE_DEFECT | Include/Money/HSBI_AllocationLedgerTypes.mqh:8 |
| HSBI-A03-ERR-005 | P0 | Allocation | SOURCE_DEFECT | Include/Money/HSBI_AllocationLedgerTypes.mqh:7 |
| HSBI-A03-ERR-006 | P1 | Allocation phases | AMBIGUOUS_SPECIFICATION | Docs/04_MATHEMATICAL_MODEL_RU.md:30 |
| HSBI-A03-ERR-007 | P0 | Reserve eligibility | SOURCE_DEFECT | Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:44-47 |
| HSBI-A03-ERR-008 | P0 | Reserve preview | SOURCE_DEFECT | Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:63-70 |
| HSBI-A03-ERR-009 | P0 | Risk preflight | SOURCE_DEFECT | Include/Risk/HSBI_RiskGateResult.mqh:6 |
| HSBI-A03-ERR-010 | P0 | Fill confirmation | SOURCE_DEFECT | Include/Execution/HSBI_TransactionTypes.mqh:15 |
| HSBI-A03-ERR-011 | P0 | Money state | SOURCE_DEFECT | Include/Money/HSBI_MoneyState.mqh:5 |
| HSBI-A03-ERR-012 | P0 | Position discovery | SOURCE_DEFECT | Include/Core/HSBI_Context.mqh:19-24,48-53 |
| HSBI-A03-ERR-013 | P0 | NewFar provenance | MISSING_CONTRACT | Include/Planning/HSBI_NewFarSolver.mqh:119-124 |
| HSBI-A03-ERR-014 | P1 | Basket opening | SOURCE_DEFECT | Include/Planning/HSBI_GeometrySolver.mqh:28-35 |
| HSBI-A03-ERR-015 | P1 | Basket planning | CONTRADICTION | Docs/04_MATHEMATICAL_MODEL_RU.md:9 |
| HSBI-A03-ERR-016 | P1 | Full cycle | UNPROVEN_CLAIM | Hybrid_Split_Big_Independent_EA.mq5:19-44 |
| HSBI-A03-ERR-017 | P1 | Restart | UNPROVEN_CLAIM | Include/Persistence/HSBI_PersistenceInterface.mqh:5-7 |
| HSBI-A03-ERR-018 | P1 | Future Catch-Up | AMBIGUOUS_SPECIFICATION | Include/Planning/HSBI_FutureSmallProofAggregator.mqh:44,50-52 |
| HSBI-A03-ERR-019 | P1 | NewFar selection | CONTRADICTION | Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:22-23 |
| HSBI-A03-ERR-020 | P1 | Future geometry | SOURCE_DEFECT | Include/Planning/HSBI_FutureSmallSolver.mqh:89-90,143 |
| HSBI-A03-ERR-021 | P1 | Future Small | UNPROVEN_CLAIM | Include/Planning/HSBI_FutureSmallSolver.mqh:12-16,142-147 |
| HSBI-A03-ERR-022 | P1 | Valuation / Harvest | MISSING_CONTRACT | Include/Money/HSBI_CostModel.mqh:13-18 |
| HSBI-A03-ERR-023 | P1 | Initial Lock | MISSING_CONTRACT | Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md:6-12 |
| HSBI-A03-ERR-025 | P1 | All commits | SOURCE_DEFECT | Include/Core/HSBI_StateMachine.mqh:6 |
| HSBI-A03-ERR-026 | P1 | Plan digest | SOURCE_DEFECT | Include/Planning/HSBI_NewFarSolver.mqh:35-45,106 |
| HSBI-A03-ERR-030 | P1 | Journal replay | SOURCE_DEFECT | Include/Persistence/HSBI_ExecutionJournal.mqh:21-29 |
| HSBI-A03-ERR-031 | P1 | Terminal residual | SOURCE_DEFECT | Include/Planning/HSBI_FutureSmallSolver.mqh:144-149 |
| HSBI-A03-ERR-032 | P1 | Full recovery | UNPROVEN_CLAIM | Docs/04_MATHEMATICAL_MODEL_RU.md:33-36 |
| HSBI-A03-ERR-033 | P0 | Funding / allocation | MISSING_CONTRACT | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:6-24 |
| HSBI-A03-ERR-034 | P1 | All opens/closes | MISSING_CONTRACT | Include/Money/HSBI_BasketMoneyEvaluator.mqh:17 |
| HSBI-A03-ERR-035 | P1 | Small Transition | AMBIGUOUS_SPECIFICATION | Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md:9,20 |
| HSBI-A03-ERR-036 | P1 | Initial / FinalClose | AMBIGUOUS_SPECIFICATION | Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md:20 |
| HSBI-A03-ERR-037 | P1 | Price proof | UNPROVEN_CLAIM | Docs/05_GEOMETRY_MODEL_RU.md:22 |
| HSBI-A03-ERR-038 | P0 | Open residual risk | UNPROVEN_CLAIM | Docs/04_MATHEMATICAL_MODEL_RU.md:33-36 |
| HSBI-A03-ERR-040 | P1 | Numeric boundaries | AMBIGUOUS_SPECIFICATION | Include/Planning/HSBI_BrokerGrid.mqh:26-27 |
| HSBI-A03-ERR-041 | P1 | Small Transition | MISSING_CONTRACT | Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md:12-14 |
| HSBI-A03-ERR-042 | P1 | Full strategy | UNPROVEN_CLAIM | Docs/03_FULL_SYSTEM_MANUAL_RU.md:12-18 |
| HSBI-A03-ERR-043 | P1 | Catch-Up basis | MISSING_CONTRACT | Include/Money/HSBI_CatchUpModel.mqh:10-15 |
| HSBI-A03-ERR-044 | P1 | Final Close | MISSING_CONTRACT | Include/Money/HSBI_MoneyTypes.mqh:7-9 |
| HSBI-A03-ERR-045 | P1 | NewFar commit boundary | AMBIGUOUS_SPECIFICATION | Include/Planning/HSBI_NewFarSolver.mqh:108-113,149-151 |
| HSBI-A03-ERR-046 | P1 | Both directions | CONTRADICTION | Docs/03_FULL_SYSTEM_MANUAL_RU.md:12 |
| HSBI-A03-ERR-047 | P1 | Big/Small attribution | AMBIGUOUS_SPECIFICATION | Include/Money/HSBI_BasketMoneyEvaluator.mqh:17 |
| HSBI-A03-ERR-048 | P0 | Proof/amount binding | SOURCE_DEFECT | Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:24–74 |
| HSBI-A03-ERR-049 | P1 | Closed enum domain | SOURCE_DEFECT | Include/Execution/HSBI_ExecutionIntent.mqh:28–40 |
| HSBI-A03-ERR-050 | P1 | Snapshot count/body | AMBIGUOUS_SPECIFICATION | Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:27–40 |

Prepared-only ERR051 remains P1 CONDITIONAL_STATIC_RISK, not published inwork. Native hang не воспроизводился и здесь не заявлен.

### Тематическая независимая граница текущего preflight

| Область | Проверенный source / published evidence | Вывод без ложного PASS |
|---|---|---|
| Money invariants/source allocation | AUDIT02 matrix pins; Docs08/32, Economic/Allocation ledger findings | Полное immutable payload/vector и authoritative grant/balance registry не доказаны; local equalities не global conservation |
| Proof/amount binding | ReserveCatchUpEvaluator:24–74; NewFarSolver:119–127 прочитаны заново | Public evaluator finite-checks scalar amounts, но не связывает их с proof.netMoney; NewFar121/122 выводит amounts из proofs, поэтому этот caller не объявлен доказанным amount-injection bypass |
| Reserve/Catch-Up | Evaluator:63–70, allocation alreadyConsumed branches | Projected reserve admission не превращает forecast в realised resource; source availability/global debit authority не подтверждены |
| FutureSmall/NewFar | Existing source pins, solver109–153; publishedFSA015–018/ERR020–021/031/045 | Finite prefix не universal tail proof; Gross не Net; selected N не independent actual residual. Copied expected identity119–124 не независимая authority. Floating-point iterator nonprogress остаётся conditional risk, не native finding |
| FSM / execution | main19–44; StateMachine5–10; AUDIT02FSA012/014 | OnInit DISABLED; OnTick no-trade stub; no OnTradeTransaction. Pure topology/revision mutation не financial settlement lifecycle |
| Crash/restart/idempotency | PersistenceInterface5–7; publishedFSA013/027, DG01bounds | PersistSnapshotStub returns success=false, SHA256 implemented=false. Local replay/DTO/journal checks не crash-consistent durable commit/CAS/backend proof |
| Profit / loss bound | Published audits02/DG01/A03 | All global guarantees NOT_PROVEN; positive Balance/Harvest и shrinking lots не recovery/profit/finite-time guarantee |

Данный delivery preflight не является повторным полным математическим аудитом всех domain/callpath assertions. Он сверил inventories, source pins, published status и ключевые executable boundaries. Ни одна проблема не закрыта как fixed/PASS только по документу или старому test count. Новых административных решений нет.

## 7. Итоговый machine-readable статус

```ini
REPOSITORY=ic8812825-maker/chatgpt.com-codex
TARGET_BRANCH=work
REMOTE_SHA_BEFORE=b4d8f1ea5caf492f3abd030e5502d40582c52dc8
LOCAL_COMMIT_SHA=10d4c376d9a71d9b0fbd5e2c9dd4894480136558
LOCAL_COMMIT_PARENT=b4d8f1ea5caf492f3abd030e5502d40582c52dc8
LOCAL_COMMIT_VALID=YES_GIT_OBJECT_INTEGRITY_AND_SCOPE
FILES_CHANGED=14_IN_PINNED_COMMIT
PRODUCTION_UNCHANGED=YES
OUTSIDE_PROJECT_CHANGES=0
RULESET_NAME=ChatGPT1
RULESET_ENFORCEMENT=enabled
PR_REQUIRED=YES
EXISTING_PR_4_CONFLICT=CONTENT_SCOPE_MISMATCH_16_VS_14_NOT_TEXTUAL_CONFLICT_PROVEN
FAST_FORWARD_POSSIBLE=YES_ANCESTRY_ONLY
SAFE_PR_DELIVERY_POSSIBLE=CONDITIONAL_TEMP_REF_APPROVAL_CHECKS_AND_CONTENT_DEPENDENCY_DECISION
TEMP_BRANCH_PERMISSION_REQUIRED=YES
CODEQL_REQUIREMENTS=CodeQL_ERRORS_HIGH_OR_HIGHER_SECURITY
CODE_QUALITY_REQUIREMENTS=ALL
APPROVAL_REQUIREMENTS=CODE_OWNER_LAST_PUSH_THREADS_EXTRA_UNATTRIBUTED
AUDIT_COMPLETENESS=PARTIAL
TRADING_LOGIC_START_ALLOWED=NO
BROKER_DISPATCH_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
PUSH_ATTEMPTED=NO
MERGE_ATTEMPTED=NO
PUBLICATION_CONFIRMED=NO
PREFLIGHT_DIAGNOSTIC_COMPLETE=YES_WITH_EXPLICIT_UNKNOWN_PERMISSIONS_AND_CHECKS
```

## Заключение

Commit10d4 исправен, основан на актуальномwork и содержит ровно14 разрешённых отчётов; потери исходных результатов нет. При нынешнем запрете других веток и любых публикационных действий доставку не выполнять. После отдельного разрешения потенциально корректен новый PR-ref на точном10d4 без историиPR4, но получение/соблюдение всех server-side gates ещё надо подтвердить штатным workflow. До выбора exact14 vs supporting-R4 scope нельзя выдавать пакет за самодостаточное завершениеAUDIT03. PR4 со старым16-file diff не заменяет этот выбор. Следующий этап только по отдельному разрешению владельца; обхода правил и положительного verdict по торговле нет.

## Приложение: полная Git parent history

Команда `git rev-list --parents --reverse 10d4c376d9a71d9b0fbd5e2c9dd4894480136558`, exit0. Исторические ancestry commits других частей того же repository приведены только как Git proof, не как область изменения/анализа проекта.

```text
91e19139bb52256c2efd0bb7274a0ad74d5008c3
0724d662e07716d0b9f442b235a5fb296126c29e 91e19139bb52256c2efd0bb7274a0ad74d5008c3
cf3aefa7898825933c8960cbab05b72a5f59250a 0724d662e07716d0b9f442b235a5fb296126c29e
d86b624fb9a69adeda6b75162c8a7538225bc306 cf3aefa7898825933c8960cbab05b72a5f59250a
cc84afe5c99a8783acee896e3d3d313314c4e6f7 d86b624fb9a69adeda6b75162c8a7538225bc306
2e02248c40e73077543702b30287d65fc019b702 cc84afe5c99a8783acee896e3d3d313314c4e6f7
15677adb912f92b0503d2bbb59c8a9fa2a68259f 2e02248c40e73077543702b30287d65fc019b702
4459ce25508e99ac61468c1a9874caf754fcac91 15677adb912f92b0503d2bbb59c8a9fa2a68259f
a4a49de208da9eb9f5748175635915e6d4cb2cf0 4459ce25508e99ac61468c1a9874caf754fcac91
c0369c91c361f4b1411099ff9a4b1c323d4f31bf a4a49de208da9eb9f5748175635915e6d4cb2cf0
c2c9095ca7a8617c81d55f71b09d8497f7091bc3 c0369c91c361f4b1411099ff9a4b1c323d4f31bf
1edb9f89afd5553acae54d3cd014ea81a88cfb43 c2c9095ca7a8617c81d55f71b09d8497f7091bc3
f2a831388e3d8a377ce41692c82617c33d0179fd 1edb9f89afd5553acae54d3cd014ea81a88cfb43
f8720b3c71d9f789583b2e5e22913a395394f365 f2a831388e3d8a377ce41692c82617c33d0179fd
2bcd2a506d11146dc965c48ebf2c7bf1c515aa3c f8720b3c71d9f789583b2e5e22913a395394f365
a1bd8500e5e0a968187ba61bb59cf00a2a888e15 2bcd2a506d11146dc965c48ebf2c7bf1c515aa3c
7031b1d84e0c6ec479155a3aed66282b4a851f44 a1bd8500e5e0a968187ba61bb59cf00a2a888e15
f12b3fc3a36e711a666b4162b71e20dc556a33fe 7031b1d84e0c6ec479155a3aed66282b4a851f44
8c9017b552c06b650cc8f42ea532214e93a4598d f12b3fc3a36e711a666b4162b71e20dc556a33fe
1e6f3d5c275abb070741d2e3a051b74622ac48f2 8c9017b552c06b650cc8f42ea532214e93a4598d
adf56382ae0ffeeb9049dcef21638aba1bade9dc 1e6f3d5c275abb070741d2e3a051b74622ac48f2
88cdacf500326af7fe4e22a7a36decb11510f6fd adf56382ae0ffeeb9049dcef21638aba1bade9dc
d4fd38ab045ef2c4139976502c7f70dceac749f3 88cdacf500326af7fe4e22a7a36decb11510f6fd
321f30d1ce8fe9f2e3a383735857e1922e43b049 d4fd38ab045ef2c4139976502c7f70dceac749f3
c635e290f52e2d85335e22d9c866e5eb1d0610c1 321f30d1ce8fe9f2e3a383735857e1922e43b049
32b61b2dc2ac9985583b709d1a22ab3247af57b9 c635e290f52e2d85335e22d9c866e5eb1d0610c1
42ed7b351e9c10122bd2bc136d9ffb22eeb15fac 32b61b2dc2ac9985583b709d1a22ab3247af57b9
bb55672f820b01af966b74e80070bb58b3dfd7ad 42ed7b351e9c10122bd2bc136d9ffb22eeb15fac
4b4eda41f63cb535df1d1474729d6eefaa77c6c9 bb55672f820b01af966b74e80070bb58b3dfd7ad
f648522a5c3b531d772dcd032a6a314b10f8cd02 4b4eda41f63cb535df1d1474729d6eefaa77c6c9
379ecbc46bde650b1b834b60eff7b414ca26ba58 f648522a5c3b531d772dcd032a6a314b10f8cd02
2b6cbd57b3fc2be0a35820a32c495e13859b98b7 379ecbc46bde650b1b834b60eff7b414ca26ba58
6144ee339e173bcb3fcd6a83d64a6205d09cfe32 2b6cbd57b3fc2be0a35820a32c495e13859b98b7
b756f402bb88db1b15b17998b28c2aae97b9ecc4 6144ee339e173bcb3fcd6a83d64a6205d09cfe32
ca4dbb57dfe7c7ffeff0005568cd77f94f1aa903 b756f402bb88db1b15b17998b28c2aae97b9ecc4
2e86d1c42e40083842cd3c0ff8a422148fbb8b78 ca4dbb57dfe7c7ffeff0005568cd77f94f1aa903
85150c6fb42383830d8477d8a85a6029ab0ccd54 2e86d1c42e40083842cd3c0ff8a422148fbb8b78
d7b421b64446da5a40b6d52d3481aeef7eca76e0 85150c6fb42383830d8477d8a85a6029ab0ccd54
d56b1ee06438d53a481efba37ea59fdf8915d22c d7b421b64446da5a40b6d52d3481aeef7eca76e0
22e8608fe8a6f9027724fd055d7152ba01512545 d56b1ee06438d53a481efba37ea59fdf8915d22c
17a825446e218fc678d50e8c0605149ecd7b1c5c 22e8608fe8a6f9027724fd055d7152ba01512545
b8ed8b42137c93981a4903060bbb3528a9f7e974 17a825446e218fc678d50e8c0605149ecd7b1c5c
8406299cad66025ff756f5ed44e8513630eea7b0 b8ed8b42137c93981a4903060bbb3528a9f7e974
b5e0575ac9203763f01341f4908c9faddaf45f27 8406299cad66025ff756f5ed44e8513630eea7b0
6f4fa627546fdcc719a76b68fc142c8cbdd8445d b5e0575ac9203763f01341f4908c9faddaf45f27
be52ab47cb3435df961f48e49b1e97ef9340d263 6f4fa627546fdcc719a76b68fc142c8cbdd8445d
8cc673916317b655be3a20736f6c7d54470cfcf0 be52ab47cb3435df961f48e49b1e97ef9340d263
1a8da9d1c91345002d70fb0804fe695272f06be6 8cc673916317b655be3a20736f6c7d54470cfcf0
fb2d9b813efc2e43a027ed57e2b49fbd9a0fed77 1a8da9d1c91345002d70fb0804fe695272f06be6
80155ba32d413a89a2e2cb7220e438f78da5db0b fb2d9b813efc2e43a027ed57e2b49fbd9a0fed77
cf432d1ae5d2867cba61a7af1c3347cd64af553e 80155ba32d413a89a2e2cb7220e438f78da5db0b
ebfa0e2362d54b6b93f4c2515d77ebcb20867fae cf432d1ae5d2867cba61a7af1c3347cd64af553e
c6ecd9e2f2f243ab4299b3c7b749649b51b13ef6 ebfa0e2362d54b6b93f4c2515d77ebcb20867fae
bd03f7506dace1699685dd62cba227b4b0c17644 c6ecd9e2f2f243ab4299b3c7b749649b51b13ef6
f6f0ecdfd4d361b496a25bbba30c4716fa73677e bd03f7506dace1699685dd62cba227b4b0c17644
473ffacc525d8b4631e56d4d57ae269f1edd4d76 f6f0ecdfd4d361b496a25bbba30c4716fa73677e
d193b3feebdb811ab4d3cc1a333acd1403932e02 473ffacc525d8b4631e56d4d57ae269f1edd4d76
5eeb4c3d23608fdb23fc1559ad7f353e9d9368d7 d193b3feebdb811ab4d3cc1a333acd1403932e02
25b1e91eb0256b1be0de133475338528fb283018 5eeb4c3d23608fdb23fc1559ad7f353e9d9368d7
92b409204300631a16ae510922b9930b806488ca 25b1e91eb0256b1be0de133475338528fb283018
4193d23c29c4e5aa1ac3f06de975f609f09dcf5f 92b409204300631a16ae510922b9930b806488ca
4ecc9bf29956f1ee125217901438bb3f20acc3d2 4193d23c29c4e5aa1ac3f06de975f609f09dcf5f
215fe8a01d357a952f0c2995930d162ca56a22d0 4ecc9bf29956f1ee125217901438bb3f20acc3d2
104c6f9cef701570bfebcc069e0fd6387b5282da 215fe8a01d357a952f0c2995930d162ca56a22d0
38a159a7c45c1905bb8d6575a1db17aca470973b 104c6f9cef701570bfebcc069e0fd6387b5282da
c4b50cc952aa739224be2e33985e6eec8f95e034 38a159a7c45c1905bb8d6575a1db17aca470973b
2bf7513d6aa8d7691c458cf666c06204a61d24d8 c4b50cc952aa739224be2e33985e6eec8f95e034
f8223b40d3c8233e0eeaab4a1f83294e53fae869 2bf7513d6aa8d7691c458cf666c06204a61d24d8
5b88df1b44878146069e33537ef912bb633fabc5 f8223b40d3c8233e0eeaab4a1f83294e53fae869
7078a4c5b760a69cb705658cbfd7610b4b03f84f 5b88df1b44878146069e33537ef912bb633fabc5
3ca30fdae66c5368d17d1d8e31b5f4a44ab6614f 7078a4c5b760a69cb705658cbfd7610b4b03f84f
00a531f5e235945c5bd5936c23b03e914f177bc6 3ca30fdae66c5368d17d1d8e31b5f4a44ab6614f
e072fbb0e0a1ba8895fa6a15669178b8483e63da 00a531f5e235945c5bd5936c23b03e914f177bc6
2fa062409d8058e5e73ad96add60bdbeaee29c19 e072fbb0e0a1ba8895fa6a15669178b8483e63da
fed982be69d8934858280254e7e8baefe705f377 2fa062409d8058e5e73ad96add60bdbeaee29c19
9ab4a50fb5c0fd214fed40950b68f33f7e049409 fed982be69d8934858280254e7e8baefe705f377
1308071b7bcf5e8756c228d1c28bb9ef35cd019f 9ab4a50fb5c0fd214fed40950b68f33f7e049409
50174f73a88a9e00897802a1f9bb876417dc742b 1308071b7bcf5e8756c228d1c28bb9ef35cd019f
6734a22551f05df9992aaa9531f2c4435ce3de79 50174f73a88a9e00897802a1f9bb876417dc742b
5fa221170a4e7125b1642efc9fedc57304f240d9 6734a22551f05df9992aaa9531f2c4435ce3de79
955eb42b8f887f231cc40e6b7be6b92d664cf4d3 5fa221170a4e7125b1642efc9fedc57304f240d9
eefa41074076ebeda744dc54f02cc0a4a993edd9 955eb42b8f887f231cc40e6b7be6b92d664cf4d3
fc21fa1cc21c83680b301a6a1251eef82a151a68 eefa41074076ebeda744dc54f02cc0a4a993edd9
dcdd51190d44f1f2c8a867cbc9b55d6e28c913c8 fc21fa1cc21c83680b301a6a1251eef82a151a68
3f2ea7ed6ac0f7e6f6543467efa454e17213c8bf dcdd51190d44f1f2c8a867cbc9b55d6e28c913c8
745161f73dc4d32db58d188efe8e65dd4ba72e38 3f2ea7ed6ac0f7e6f6543467efa454e17213c8bf
51e2c655fe69cc9a5cb9080011bd6cc0465d341f 745161f73dc4d32db58d188efe8e65dd4ba72e38
764bc8a63dbe77f809da764f1d54e437e8016bef 51e2c655fe69cc9a5cb9080011bd6cc0465d341f
e5af21759053e7bc70d73cf417186fc9230ee77f 764bc8a63dbe77f809da764f1d54e437e8016bef
f7743fd4fc4f47b5bc4b413c39f8d73d8670d069 e5af21759053e7bc70d73cf417186fc9230ee77f
81cc832fffa818165858f6596a94b5cad6c3c0c2 f7743fd4fc4f47b5bc4b413c39f8d73d8670d069
fddbe0be40e6ad6d6e0537cc26ad2fed953866ed 81cc832fffa818165858f6596a94b5cad6c3c0c2
da77ac614e88f1adcf3c7fdfef66aaa9b6dc6680 fddbe0be40e6ad6d6e0537cc26ad2fed953866ed
dab26bee811425618ff36b3827caec940fa9e93e da77ac614e88f1adcf3c7fdfef66aaa9b6dc6680
80ffa82616a05c9291288b7851b2991e7c94705f dab26bee811425618ff36b3827caec940fa9e93e
bd1bb0237f68bf42bf266e2c428f784eab58a4de 80ffa82616a05c9291288b7851b2991e7c94705f
dd76f1de6475e4ea88266ff1fcdc2f6c3a541ca0 bd1bb0237f68bf42bf266e2c428f784eab58a4de
9427f9cc62f8d3438fc949b89a659c74d6d1e414 dd76f1de6475e4ea88266ff1fcdc2f6c3a541ca0
308d1d36b57a01994b42638c24dd7864dac0d426 9427f9cc62f8d3438fc949b89a659c74d6d1e414
7fbfabcc2ff50af7e27e7ce015bbb673da7c6142 308d1d36b57a01994b42638c24dd7864dac0d426
986d54d5ec58c81e30ab01b809e88226090280af 7fbfabcc2ff50af7e27e7ce015bbb673da7c6142
c41abb1fcce320bd9d7f44eba90e8db7e9bcb01c 986d54d5ec58c81e30ab01b809e88226090280af
03ab7d973a68a2b76eec8c601a9ce63992781a79 c41abb1fcce320bd9d7f44eba90e8db7e9bcb01c
8403e1f7dbc6dfaecf83e7b3cae70476ee036d04 03ab7d973a68a2b76eec8c601a9ce63992781a79
8ff1984f6c962ad7d1c1aa0c4ae2e3e5ce623b9b 8403e1f7dbc6dfaecf83e7b3cae70476ee036d04
9efc5397a62729a69a20468fbfdfaff3fa18f62a 8ff1984f6c962ad7d1c1aa0c4ae2e3e5ce623b9b
1a8484b87928fd3274b8c89f8e70f568fe7d7874 9efc5397a62729a69a20468fbfdfaff3fa18f62a
e63527801956d567181c4386ebd9701d6efba82d 1a8484b87928fd3274b8c89f8e70f568fe7d7874
58295d01ce0612129b0d5a59fa63debafa55d430 e63527801956d567181c4386ebd9701d6efba82d
c7d824150978fdf2a470fceb4dd3bcda8cf5c8a1 58295d01ce0612129b0d5a59fa63debafa55d430
892eb165dfa7a46867b741c2837f53738dc76c8e c7d824150978fdf2a470fceb4dd3bcda8cf5c8a1
604fbff4ea82f32e038449f3bd263daa4b4fed27 892eb165dfa7a46867b741c2837f53738dc76c8e
6736a9c4c98b07c04c9e689005e1fa30d7f51007 604fbff4ea82f32e038449f3bd263daa4b4fed27
0413df66c41d8b040eb472ab81d5955c57460942 6736a9c4c98b07c04c9e689005e1fa30d7f51007
c907e1e07a72c5ce1009cd1997b0e75c56246f58 0413df66c41d8b040eb472ab81d5955c57460942
767576a9325e0f44210531c86313b5f004cb2f04 c907e1e07a72c5ce1009cd1997b0e75c56246f58
9dbc98a3f383287600f0af535a6638d2b490ca14 767576a9325e0f44210531c86313b5f004cb2f04
581afdd0accf2e47e97ecd00b5dd0080f0ea0757 9dbc98a3f383287600f0af535a6638d2b490ca14
e0f222f1ac668bb0a7a7e29b7aaae082cf9a1040 581afdd0accf2e47e97ecd00b5dd0080f0ea0757
f2b327403540320fba931d4093474e2ef38c8ed1 e0f222f1ac668bb0a7a7e29b7aaae082cf9a1040
7fb980df16d80c4bbb293186fbb86ecb49d22b7d f2b327403540320fba931d4093474e2ef38c8ed1
8922b63d595864fc3490f7056752bb6453176b6f 7fb980df16d80c4bbb293186fbb86ecb49d22b7d
0f7aaed15d247aeb4f9d400106aaf0d865f6cf1e 8922b63d595864fc3490f7056752bb6453176b6f
9eb658beeed9412875f865ba1fbfe4639d5c1612 0f7aaed15d247aeb4f9d400106aaf0d865f6cf1e
3d94e2d67389d6d38e26305db0ad1f2601ccad5b 9eb658beeed9412875f865ba1fbfe4639d5c1612
cce7f4dd8226899dcce8100290b9baef58ee887a 3d94e2d67389d6d38e26305db0ad1f2601ccad5b
4a0d114296f19fd57b2c2787596f8ab984bcdc42 cce7f4dd8226899dcce8100290b9baef58ee887a
b911a85266c30d61a8cb508005735a13ad6615d4 4a0d114296f19fd57b2c2787596f8ab984bcdc42
f926512893c94a3b02f6d8455f1a9ec82ce7f701 b911a85266c30d61a8cb508005735a13ad6615d4
552de050fd3389d4571889905261fe83b6503fa5 f926512893c94a3b02f6d8455f1a9ec82ce7f701
80574b8d127f0f842f7cf16f2892da8b1d6871f0 552de050fd3389d4571889905261fe83b6503fa5
833fccac504b6411d23b9ef8521c6130edfbf2b5 80574b8d127f0f842f7cf16f2892da8b1d6871f0
bf3a84b37e7b720e90fc4395ae4100f8694067d3 833fccac504b6411d23b9ef8521c6130edfbf2b5
a5763ce48281cc4c97e4ef939b15c4ef3998f6e4 bf3a84b37e7b720e90fc4395ae4100f8694067d3
0ac1df08add3cefc983e29a36ee49a48fae68579 a5763ce48281cc4c97e4ef939b15c4ef3998f6e4
7fd28fd481ffc00fb3a6b47a473c6fdcf46d6da6 0ac1df08add3cefc983e29a36ee49a48fae68579
954a4bc025cc51193c432dd0658c796bcfcd471c 7fd28fd481ffc00fb3a6b47a473c6fdcf46d6da6
522af23fedf82c85f2306f77ccc28756b0d4dd88 954a4bc025cc51193c432dd0658c796bcfcd471c
76bf78e1dcddb2a53291b42c1f7a95e3376f78ae 522af23fedf82c85f2306f77ccc28756b0d4dd88
5d4a684110259e4b8d8650fc816a510218c87556 76bf78e1dcddb2a53291b42c1f7a95e3376f78ae
e4cc6360ba9d56ed0394ee08ede6f69604399b32 5d4a684110259e4b8d8650fc816a510218c87556
b90e85bb822f1c33855c1c8f6512c374acd1973b e4cc6360ba9d56ed0394ee08ede6f69604399b32
2a398eb56ebcbae9d8ef8992dd2409d4f14d42db b90e85bb822f1c33855c1c8f6512c374acd1973b
7f33db068b00fa84762ad3574a84ffecd611e9ea 2a398eb56ebcbae9d8ef8992dd2409d4f14d42db
96019ba98885a483733250747e0fe02f42699d3f 7f33db068b00fa84762ad3574a84ffecd611e9ea
a8f93831d12edd2cacf56c753b044cbd959eb39c 96019ba98885a483733250747e0fe02f42699d3f
cf2bb143da6d15a83acc476ac16ab13575673d1a a8f93831d12edd2cacf56c753b044cbd959eb39c
703f2416eb5d017790b67d54209743c53cba641e cf2bb143da6d15a83acc476ac16ab13575673d1a
233e69b2c7b94e45825052c197bb5551274eb375 703f2416eb5d017790b67d54209743c53cba641e
7c613d1e910a1739053852b8da66a162cbba35a0 233e69b2c7b94e45825052c197bb5551274eb375
3de83c70426dc677c68cee5811fdbb398bcd25cf 7c613d1e910a1739053852b8da66a162cbba35a0
951258809eb78af418ca88d855380c84d05ced87 3de83c70426dc677c68cee5811fdbb398bcd25cf
abf3c40a1105222c89bef2e31541432bcacece4c 951258809eb78af418ca88d855380c84d05ced87
26bdd9b5cc9a378c964659d50635a21514633ddf abf3c40a1105222c89bef2e31541432bcacece4c
64d033e36033d8d0a9c2659e3e6dd79b7a9daaae 26bdd9b5cc9a378c964659d50635a21514633ddf
46e570b25355b765a08104212258f8790b9bd477 64d033e36033d8d0a9c2659e3e6dd79b7a9daaae
946342c8282d41be4dc8845c28e39da242eec962 46e570b25355b765a08104212258f8790b9bd477
37420cb5029de11cc295e01edc622980a2de1e4c 946342c8282d41be4dc8845c28e39da242eec962
8633c0d1f079ea02d46521cc36434e1cff9bc807 37420cb5029de11cc295e01edc622980a2de1e4c
99e1f665573c720241368a88a229bb4c36d4e37d 8633c0d1f079ea02d46521cc36434e1cff9bc807
105cd700b40f67257750265ebd12ebe2a0962d17 99e1f665573c720241368a88a229bb4c36d4e37d
76226e24a2aa9176badf829fa97479217ac30dcc 105cd700b40f67257750265ebd12ebe2a0962d17
2b9d23c335a19828c825a923f2e2c22028c33ef2 76226e24a2aa9176badf829fa97479217ac30dcc
7569aa47b6961c21d48d5c9394a25322f3fed08e 2b9d23c335a19828c825a923f2e2c22028c33ef2
a700899c4e9aaf91fdbb21b924d2af243b0790d8 7569aa47b6961c21d48d5c9394a25322f3fed08e
fa2945d7ccef48170b75d94f0918a844bf1dee1f a700899c4e9aaf91fdbb21b924d2af243b0790d8
e60646fc5336de91cff20fbbef73de1cee86779f fa2945d7ccef48170b75d94f0918a844bf1dee1f
f6f8e4ed43f874ff43cc4e6721e484c0cf342b7e e60646fc5336de91cff20fbbef73de1cee86779f
6a9adb5c77dce9783237259dda7f7ae85f89fb38 f6f8e4ed43f874ff43cc4e6721e484c0cf342b7e
2ef40a12d49f75acf453a65a7336fd5b14fde570 6a9adb5c77dce9783237259dda7f7ae85f89fb38
f8e6f750c853b4864c8b317d2fa123001c18e471 2ef40a12d49f75acf453a65a7336fd5b14fde570
1ea8299994194b7c5d2c1d23c05b1ceb627b7102 f8e6f750c853b4864c8b317d2fa123001c18e471
85525bba6ed59012ade1e467061fe1d86938ab73 1ea8299994194b7c5d2c1d23c05b1ceb627b7102
0df1b2ed592da8e10a8ed4e2aeaffd9d31df84ab 85525bba6ed59012ade1e467061fe1d86938ab73
0632485f750e85e0740de7be86fcac1fc428162a 0df1b2ed592da8e10a8ed4e2aeaffd9d31df84ab
a7e37e6dee760d4b97e991a591e0c9a187017443 0632485f750e85e0740de7be86fcac1fc428162a
a79d3d1d0ca623af6ac67a5a6a912004f9067e75 a7e37e6dee760d4b97e991a591e0c9a187017443
b296626662232a88942931ef565d9d1957d29040 a79d3d1d0ca623af6ac67a5a6a912004f9067e75
bba4adf4e2df1689e83e94d4d8f15b4262445ef4 b296626662232a88942931ef565d9d1957d29040
31b3a87dbdf4db3d4a88145c01fd8ddead936933 bba4adf4e2df1689e83e94d4d8f15b4262445ef4
c768d6347c4893b89d330fa2050f8182d390237b 31b3a87dbdf4db3d4a88145c01fd8ddead936933
25dbe19ac8379093beb0a105b42116fb4ae6324a c768d6347c4893b89d330fa2050f8182d390237b
2f621cd1790fcbeec6eb6ac18d3bda11787fc65b 25dbe19ac8379093beb0a105b42116fb4ae6324a
c5ad0f389773253fdd066793ac15a94ac07484b0 2f621cd1790fcbeec6eb6ac18d3bda11787fc65b
cca45df42b829ca8b5520965aff757dbc2adf90d c5ad0f389773253fdd066793ac15a94ac07484b0
af6844729c3f5e81fec5b91aa33c2a761d4b02d7 cca45df42b829ca8b5520965aff757dbc2adf90d
a3ffe3363914a70113f77b714989781b2f85b9df af6844729c3f5e81fec5b91aa33c2a761d4b02d7
fab8419ad91457a566e269374ee8b9d062f35f8f a3ffe3363914a70113f77b714989781b2f85b9df
15bb47f9e61c2458da687c03e35296e395e3a52b fab8419ad91457a566e269374ee8b9d062f35f8f
83c9ff69d73d85ae99faa5c5a14c3a92e96e46a5 15bb47f9e61c2458da687c03e35296e395e3a52b
5c78e6d26ad6d13d79aea6932e38963b17a81ce6 83c9ff69d73d85ae99faa5c5a14c3a92e96e46a5
88eaed2f6ad7ac469aa4699df1a269e1f62897a7 5c78e6d26ad6d13d79aea6932e38963b17a81ce6
f311e66c0df08ca6b76f2dac3f681a762cfdc07a 88eaed2f6ad7ac469aa4699df1a269e1f62897a7
34cf91893737d55f551c39ffe148fe961b22f533 f311e66c0df08ca6b76f2dac3f681a762cfdc07a
4e805bfab9f6cff8e2c1efabe05660a7228b95a3 34cf91893737d55f551c39ffe148fe961b22f533
b6604faedc72771d558fa2f9a33c95e1957a07f6 4e805bfab9f6cff8e2c1efabe05660a7228b95a3
575bbf150e4567d29b83b49f5f17f83df06b78b6 b6604faedc72771d558fa2f9a33c95e1957a07f6
37dcb1f7d3923cc7b8cc77baa83e86dc3e4a529c 575bbf150e4567d29b83b49f5f17f83df06b78b6
85a601bd45084838d8c21892bd05240c0cf3d19e 37dcb1f7d3923cc7b8cc77baa83e86dc3e4a529c
05176c899ea90d407eb65ffaebd805c626c98b32 85a601bd45084838d8c21892bd05240c0cf3d19e
01a63d05948c9f64253edebe3de559b2e365b082 05176c899ea90d407eb65ffaebd805c626c98b32
50e6470f0c3140266ba89d329524d6cd34cda3a8 01a63d05948c9f64253edebe3de559b2e365b082
e7be8556ba6b186a09c779b0ba14953a5e5603c5 50e6470f0c3140266ba89d329524d6cd34cda3a8
07efb88ee0adcc667eba08ba98a62ba0fa0a77ca e7be8556ba6b186a09c779b0ba14953a5e5603c5
647240f1bd986075d62545db53609350b1c62a75 07efb88ee0adcc667eba08ba98a62ba0fa0a77ca
d27d7a8ff81fdf0688859269c380fb6545927738 647240f1bd986075d62545db53609350b1c62a75
38e65e210d6af919e8cc4b4cb66afa72dc255060 d27d7a8ff81fdf0688859269c380fb6545927738
99cf58df692c4403c07a32342ff61454e7d14d8e 38e65e210d6af919e8cc4b4cb66afa72dc255060
59ed1b0db1a0d2a7884a45e9ceca4e44b42c6a61 99cf58df692c4403c07a32342ff61454e7d14d8e
65cc83a92484f93b1d4387ada4788d2495017767 59ed1b0db1a0d2a7884a45e9ceca4e44b42c6a61
e0923aebb33f761f3af073df0ca88079cdf24ee8 65cc83a92484f93b1d4387ada4788d2495017767
68f444182cb488413dbf61c1609e751b737c855f e0923aebb33f761f3af073df0ca88079cdf24ee8
16df178e5a0092369221e5e4fcedb1be20a37a41 68f444182cb488413dbf61c1609e751b737c855f
9e3578f16fff478b96e6fe021d77350bfe4e5a76 16df178e5a0092369221e5e4fcedb1be20a37a41
6adc7f09b139275f9a5f15c55e273e4a6b2fda39 9e3578f16fff478b96e6fe021d77350bfe4e5a76
39a04a5f9e47d515abc92ef44492c81bf0c17d30 6adc7f09b139275f9a5f15c55e273e4a6b2fda39
9bb1b15b769d83cbef74d7f2959a91f75a80788e 39a04a5f9e47d515abc92ef44492c81bf0c17d30
17ce79ede2cd2bcd63210fcbbabe6c4e98ba6441 9bb1b15b769d83cbef74d7f2959a91f75a80788e
075e3f464048634590a8c50ce48edcb3a96c919f 17ce79ede2cd2bcd63210fcbbabe6c4e98ba6441
b4889030ea189511fdbfb9a09f812f419fb9eff0 075e3f464048634590a8c50ce48edcb3a96c919f
f15abe407396c076246af00494e86f06995ffd4f b4889030ea189511fdbfb9a09f812f419fb9eff0
db7a32852d02de2f1a631193c87c2fc2ad42b152 f15abe407396c076246af00494e86f06995ffd4f
72c3b8bace3092ebe58f3cde6050e5cbdc40fdcc db7a32852d02de2f1a631193c87c2fc2ad42b152
34810ebffc1792c7e2cdeddff5b1027829da8210 72c3b8bace3092ebe58f3cde6050e5cbdc40fdcc
92a8fa667141ca1e21ae5b4f5547393a88c28ba2 99cf58df692c4403c07a32342ff61454e7d14d8e
3d51e77c901bf1e22dde82ddd2da18407f84943a 92a8fa667141ca1e21ae5b4f5547393a88c28ba2 34810ebffc1792c7e2cdeddff5b1027829da8210
7aec6f6c01a78fee7c9c05eb984902b082bc5199 3d51e77c901bf1e22dde82ddd2da18407f84943a
c3c8ae8526cc31c01b87eff29d149c0712f9ade1 7aec6f6c01a78fee7c9c05eb984902b082bc5199
8b21baad50cae655a2a7777d5fcf773142f7129a c3c8ae8526cc31c01b87eff29d149c0712f9ade1
ca939e342e1b864a114ee08358e14ce1fbecd592 8b21baad50cae655a2a7777d5fcf773142f7129a
0cf25a6762946e8dbf07b413baca83a346c6d3f3 ca939e342e1b864a114ee08358e14ce1fbecd592
b0505fb7202f0c7935292173aa2b907dcbba6487 0cf25a6762946e8dbf07b413baca83a346c6d3f3
14c29e3d41201953c395a68c6196eeff05f749c0 b0505fb7202f0c7935292173aa2b907dcbba6487
0de702048799914b3921a3421df4f348977e1ce1 14c29e3d41201953c395a68c6196eeff05f749c0
da621569b900959e82b8c69cca2a05f3a2573d2b 0de702048799914b3921a3421df4f348977e1ce1
3f51bea1acbf7203d0510c80e122dcc8ce38eb42 da621569b900959e82b8c69cca2a05f3a2573d2b
efc50dfc534c06f78f37190070c85ee6d82980b4 3f51bea1acbf7203d0510c80e122dcc8ce38eb42
750a709b51d1103ecf3039799b0c7859bd04698c efc50dfc534c06f78f37190070c85ee6d82980b4
82b02b46b666bcb0ddb7972e6ce2accb38e0680b 750a709b51d1103ecf3039799b0c7859bd04698c
c35692b61466f7759f99243303a6f6969fa1b51c 82b02b46b666bcb0ddb7972e6ce2accb38e0680b
e87527f8b3e4677e6cbe3d401b26f0ada81272af c35692b61466f7759f99243303a6f6969fa1b51c
8c6ce0279f32b417ec3b38e40b1eb903660dddd0 e87527f8b3e4677e6cbe3d401b26f0ada81272af
ccc1d17f9bf6b2b34813a5f5b3c7e85b126b3e93 8c6ce0279f32b417ec3b38e40b1eb903660dddd0
7b5cdcc52cf7a2f32e0fe954bcc907724132b5da ccc1d17f9bf6b2b34813a5f5b3c7e85b126b3e93
67898ed51e652eb8b5de32bbcb957e2ace77b364 7b5cdcc52cf7a2f32e0fe954bcc907724132b5da
059e1e22b7b823c6eaa4fa3bc8e67829dc726f2c 67898ed51e652eb8b5de32bbcb957e2ace77b364
5e22abceb33154bd6dc9004f8f9ec087b8ac0f30 059e1e22b7b823c6eaa4fa3bc8e67829dc726f2c
316686b47d6f6efd8a6cdae5bdd3ebe53d4b5136 5e22abceb33154bd6dc9004f8f9ec087b8ac0f30
9769c5a0e65f4c148bd1dcfb166f159af1c885e1 316686b47d6f6efd8a6cdae5bdd3ebe53d4b5136
983d4b27ede5a47e9f36310feee2f2565f639726 9769c5a0e65f4c148bd1dcfb166f159af1c885e1
391226da0ae16ea93c61eb192c796da1a82649ec 983d4b27ede5a47e9f36310feee2f2565f639726
b41169c66150e4800f693d047bd535339cf74ee6 391226da0ae16ea93c61eb192c796da1a82649ec
bc11115b056fc87aeb5cd732bd97e8d596cde817 b41169c66150e4800f693d047bd535339cf74ee6
aed4df7991b9d84b2e1d1456b3faf0d93a8a4ccb bc11115b056fc87aeb5cd732bd97e8d596cde817
848fc0a16c53629a27a0297cb7c52c47168f5b9e aed4df7991b9d84b2e1d1456b3faf0d93a8a4ccb
9d13a4c59aec43cf3e94bcb2ed206d5cea6f1524 848fc0a16c53629a27a0297cb7c52c47168f5b9e
811d42deb64a0831176159330ca43b2f34d25d6d 9d13a4c59aec43cf3e94bcb2ed206d5cea6f1524
1b9cbb5587a75c14ac4ca6ace7286de1134a1de0 811d42deb64a0831176159330ca43b2f34d25d6d
137fa8a12cde843b0d8d3c96bcf6cd28cc5cc4e8 1b9cbb5587a75c14ac4ca6ace7286de1134a1de0
028e3c514ebf4b93280e7ce993c50c460df61078 137fa8a12cde843b0d8d3c96bcf6cd28cc5cc4e8
177062bac1ab5cfb4aa41de09912e1d3ac0f914a 028e3c514ebf4b93280e7ce993c50c460df61078
becdfca08a9cb478c55b92592ad8ef4b5e860342 177062bac1ab5cfb4aa41de09912e1d3ac0f914a
fe0310b9c983d11acde137b36a2f4166e7529df9 becdfca08a9cb478c55b92592ad8ef4b5e860342
36ae80d782b2ff8265bc6579961ec02fb18ecff2 fe0310b9c983d11acde137b36a2f4166e7529df9
096457f1c6447f208fa52e77bbd15c624888e6c5 36ae80d782b2ff8265bc6579961ec02fb18ecff2
4c92bee312d78c26189101c74db3057b7a2733e8 096457f1c6447f208fa52e77bbd15c624888e6c5
6485ac375cafb5a1fb67be519d520fff15f25ee6 4c92bee312d78c26189101c74db3057b7a2733e8
a4c7c74740d90f389152c0c6223f56cde9786abe 6485ac375cafb5a1fb67be519d520fff15f25ee6
798619fd0cb7e5b0ec143ebb0108001063fabfa8 a4c7c74740d90f389152c0c6223f56cde9786abe
e2827a4db62f58ec31daab26c68629f9ff3f345e 798619fd0cb7e5b0ec143ebb0108001063fabfa8
40aa6dfc496211bdad48a2b271365be4a7f6f0a1 e2827a4db62f58ec31daab26c68629f9ff3f345e
20263af15951cbcc5e86238aa8afc0e275b80239 40aa6dfc496211bdad48a2b271365be4a7f6f0a1
f46addc226c465b817b6ebb5afb71a75f29b59b5 20263af15951cbcc5e86238aa8afc0e275b80239
6090cc54508d16849bea3b745f920c8be3b883f6 f46addc226c465b817b6ebb5afb71a75f29b59b5
b2c55452abaeeb68ae03dded3b3ea35096f306d6 6090cc54508d16849bea3b745f920c8be3b883f6
67aaaa050d6e90388fff20042f18eba6be662d10 b2c55452abaeeb68ae03dded3b3ea35096f306d6
a6b396de926c47fe27a6bca40c783861d533b3cc 67aaaa050d6e90388fff20042f18eba6be662d10
b40faf3cf3855cf1e748d1e636d958fe3f5f2b04 a6b396de926c47fe27a6bca40c783861d533b3cc
1fa91d5123031707bfb9db2f60c023d4196262f5 b40faf3cf3855cf1e748d1e636d958fe3f5f2b04
d8fcd2bd90d5a28e0e05f44b32cffa3102ada598 1fa91d5123031707bfb9db2f60c023d4196262f5
22359292d4a1cce7033b3f28df8a620a13de6452 d8fcd2bd90d5a28e0e05f44b32cffa3102ada598
5247c71e70ec42fe58ea73117f2239fe68d744c0 22359292d4a1cce7033b3f28df8a620a13de6452
2e3c0bf995a399f43347556ad1c1255b102a7184 5247c71e70ec42fe58ea73117f2239fe68d744c0
f8d1d35f2a8366b9f4ebd8e6c324e9cfb10b965e 2e3c0bf995a399f43347556ad1c1255b102a7184
671c023dc22b5476a2a71319ede424901f28e0f0 f8d1d35f2a8366b9f4ebd8e6c324e9cfb10b965e
11c39d5161d5615f6fcfeebc7fc47888816dc321 671c023dc22b5476a2a71319ede424901f28e0f0
757c9a2a1da39d87e7e9bb97d8260b1bab09c2eb 11c39d5161d5615f6fcfeebc7fc47888816dc321
e5b352eaf1f29a33d2b077292e2046b95f8ede4b 757c9a2a1da39d87e7e9bb97d8260b1bab09c2eb
fcb2ba17808d70436215af4f99a3bc7dca57c79f e5b352eaf1f29a33d2b077292e2046b95f8ede4b
e91b3e75f078bf7c68e5a41bdebc3e70becfc015 fcb2ba17808d70436215af4f99a3bc7dca57c79f
89bd0948b938f2d0157ea25695e97543bba98f0c e91b3e75f078bf7c68e5a41bdebc3e70becfc015
08a3fad58b99e64d2eb9b19d589ea80795de5592 89bd0948b938f2d0157ea25695e97543bba98f0c
27d413baa9f68233c5797ab3f1f09b02ff387fc2 08a3fad58b99e64d2eb9b19d589ea80795de5592
c586f344f73763af0b1e648738f1ebd5fc0e9dca 27d413baa9f68233c5797ab3f1f09b02ff387fc2
094c8a857fe3a4d15ecec3e1a60affde1d9fa8d9 c586f344f73763af0b1e648738f1ebd5fc0e9dca
3ce2bb70501b4ddc6132a0cc87a09faa9ac91242 094c8a857fe3a4d15ecec3e1a60affde1d9fa8d9
f45e5e7b0173ca5b3c018951798c0aaad77e8c99 3ce2bb70501b4ddc6132a0cc87a09faa9ac91242
9065258cb36d396d150a65409da30d8d5008d2eb f45e5e7b0173ca5b3c018951798c0aaad77e8c99
4aa4eb9063908ea85f87237244eae5b754e4a987 9065258cb36d396d150a65409da30d8d5008d2eb
6e6cfb5465dd5a45d5642ba78b2430bb19022561 4aa4eb9063908ea85f87237244eae5b754e4a987
3d94ee162a4c707385aec7ad5657da4b726c3cd8 6e6cfb5465dd5a45d5642ba78b2430bb19022561
abd460b3c8b085ca9c42e75bb92980dcf381697e 3d94ee162a4c707385aec7ad5657da4b726c3cd8
e96f300f71a1a25be59e5d71201ed0ca68e738ff abd460b3c8b085ca9c42e75bb92980dcf381697e
bbf5d532eb01ed87aa6079b94df42e08d1ec982b e96f300f71a1a25be59e5d71201ed0ca68e738ff
a571e9be14545d4ebed688b314bc5f72cf6d1632 bbf5d532eb01ed87aa6079b94df42e08d1ec982b
7e24c34d08fb1cd35e810ac208eb9d181c3b84a4 a571e9be14545d4ebed688b314bc5f72cf6d1632
50eb1fa6825f15b79709225aa7a6df934ac5eca1 7e24c34d08fb1cd35e810ac208eb9d181c3b84a4
923223407eeafaeed9e11e1c0d9129ef21b2c363 50eb1fa6825f15b79709225aa7a6df934ac5eca1
87edbdd858b9f0762ce61f43aa4d46384f5bf93c 923223407eeafaeed9e11e1c0d9129ef21b2c363
b16f1a5475ff2e1939c768730a95d0060f95be88 87edbdd858b9f0762ce61f43aa4d46384f5bf93c
084d17166f0e9e48eacb9b27ef47fc8bc5e6348e b16f1a5475ff2e1939c768730a95d0060f95be88
212845f1e8d8eb1c6ad83d1e241fd8fddcff7058 084d17166f0e9e48eacb9b27ef47fc8bc5e6348e
bb9396c2e9fc7595702ff254f22a75cfb33df7d9 212845f1e8d8eb1c6ad83d1e241fd8fddcff7058
a693850c26947e7ba1164d00bac66933141c8661 bb9396c2e9fc7595702ff254f22a75cfb33df7d9
04b5922df91659fe925470fc4ce2560aa411399a a693850c26947e7ba1164d00bac66933141c8661
d6980b1a1d8955ad47571c95fa18782118c237dc 04b5922df91659fe925470fc4ce2560aa411399a
29abcaa9208fae6c068a28f8d4e4e79c59347160 d6980b1a1d8955ad47571c95fa18782118c237dc
a2e07ef37c7d671a4ae6232245e0a9a95f75f9d6 29abcaa9208fae6c068a28f8d4e4e79c59347160
ec7ac386edeb38b5e79bae44afcb45013f7235dc a2e07ef37c7d671a4ae6232245e0a9a95f75f9d6
1f1cd49bbd703942f6393fee5b3a96659e172cfe ec7ac386edeb38b5e79bae44afcb45013f7235dc
7c9032a741467cb390425887d6dc39bfa2272e27 1f1cd49bbd703942f6393fee5b3a96659e172cfe
82aa3be039f5c8cead49c6d996cfeeeeb3866262 7c9032a741467cb390425887d6dc39bfa2272e27
5cb1591f063154847b04433c9c31499d4a1c56ef 82aa3be039f5c8cead49c6d996cfeeeeb3866262
40e3807632c6335d4d7531e31a940b2f16fe8e8d 5cb1591f063154847b04433c9c31499d4a1c56ef
74cd40a53460308ae0750ca0a0ac92ce0f968232 40e3807632c6335d4d7531e31a940b2f16fe8e8d
9dd44ec039a917d78fee34d2a060a77dc23e8226 74cd40a53460308ae0750ca0a0ac92ce0f968232
d03007ef573da2f22200fa74903c4c16b44c1646 9dd44ec039a917d78fee34d2a060a77dc23e8226
401dd95d42d2411eb2a72731cd678dbdffca07b9 d03007ef573da2f22200fa74903c4c16b44c1646
508917a441a8ddd62f2491fb36b341d292aed781 401dd95d42d2411eb2a72731cd678dbdffca07b9
b57b92c8312dceca7e947a34a3d9c000ce1eeb91 508917a441a8ddd62f2491fb36b341d292aed781
6316b1ba8b414459a744b299b2fea66a8c9ac99f b57b92c8312dceca7e947a34a3d9c000ce1eeb91
d44881d59a28ca4cd3e1eade5fa223c5d1426b5b 6316b1ba8b414459a744b299b2fea66a8c9ac99f
cba183b00116959552a645deefe9bf3e50edd484 d44881d59a28ca4cd3e1eade5fa223c5d1426b5b
7a2310569890144f84d6ad44340d746e81184146 cba183b00116959552a645deefe9bf3e50edd484
1b6fe6f3654a0d098054a51086069258c41179e8 7a2310569890144f84d6ad44340d746e81184146
52f313accba4d22e10175a13699247a12b366120 1b6fe6f3654a0d098054a51086069258c41179e8
4b3ebed3860925844e92f464b0ac686649e76f52 52f313accba4d22e10175a13699247a12b366120
fe59582a9b54df93b95d5bf19eabde024ca1fa58 4b3ebed3860925844e92f464b0ac686649e76f52
c3d940a4e66fb826c8ffb706206581cfcb727fc0 fe59582a9b54df93b95d5bf19eabde024ca1fa58
cd9d51f7001cb266457a6d6a079c897973b0f66b c3d940a4e66fb826c8ffb706206581cfcb727fc0
5fc693fcdb33476a3e423a411c989568471c00df cd9d51f7001cb266457a6d6a079c897973b0f66b
0e89aa4fe7a3b5527d345c382f150c0f4eb9c2b6 5fc693fcdb33476a3e423a411c989568471c00df
18163b4dde18be20332fc2ab3d56d388aa306b22 0e89aa4fe7a3b5527d345c382f150c0f4eb9c2b6
99243a757c8cfd1bc095350f0183d8d3e68d3d86 18163b4dde18be20332fc2ab3d56d388aa306b22
c5ad69f01dd2e0ab0c07cc6e804844e09b626c62 99243a757c8cfd1bc095350f0183d8d3e68d3d86
ee96128bb8aae087d6b3974a80b3f62672d23890 c5ad69f01dd2e0ab0c07cc6e804844e09b626c62
ef2d427bfd8783fa454ffbc3e5b8ec3d06441b7e ee96128bb8aae087d6b3974a80b3f62672d23890
ebf0a68498740cb92dbb78f78eacfb6ffaf78e07 ef2d427bfd8783fa454ffbc3e5b8ec3d06441b7e
f97fce18b8bfed3007979f58add812b10d0df4b9 ebf0a68498740cb92dbb78f78eacfb6ffaf78e07
31d782fa3c9ef658be7a45ce45b15b8b4b4e5a67 f97fce18b8bfed3007979f58add812b10d0df4b9
1532ce9f318cddc9039e38933e9c1a73c340dca7 31d782fa3c9ef658be7a45ce45b15b8b4b4e5a67
8cd0b7e684e9e5dbb51833239e550cb34b318667 1532ce9f318cddc9039e38933e9c1a73c340dca7
e5b2786d8e76cb582866bb07f21261dd7e797573 8cd0b7e684e9e5dbb51833239e550cb34b318667
a589f684da612bb0c02e89c67d73666ae2cf06cf e5b2786d8e76cb582866bb07f21261dd7e797573
a2dcfe965bd8da94f662ab651da6ac62b7d1d45b a589f684da612bb0c02e89c67d73666ae2cf06cf
0e5ea03ad9bd59c806f0ea25b0d348e6117c47c6 a2dcfe965bd8da94f662ab651da6ac62b7d1d45b
07b05714161e9d4979e2da42967ed62841c3ff13 0e5ea03ad9bd59c806f0ea25b0d348e6117c47c6
86061f6e2cca10b55c85179de010f7bb0c352710 07b05714161e9d4979e2da42967ed62841c3ff13
bef2c96e91ad74da7ba693ba1569b2b6484c9772 86061f6e2cca10b55c85179de010f7bb0c352710
91eec06b7e9d61889a737d8c4fb92f20dc0bd0e2 bef2c96e91ad74da7ba693ba1569b2b6484c9772
f6270a1fb5ca61f58152bbfb0f874b5c00c27d73 91eec06b7e9d61889a737d8c4fb92f20dc0bd0e2
df3c37df393f04635d4f1add75cb35497a3cc6e6 f6270a1fb5ca61f58152bbfb0f874b5c00c27d73
263313149d562babd3e83402a4ea59d18118bc3f df3c37df393f04635d4f1add75cb35497a3cc6e6
a635e855f749cdd0537daffa8e601032da7645df 263313149d562babd3e83402a4ea59d18118bc3f
2539672153ae9d3b59d66b3b9f56c84a8dd1341b a635e855f749cdd0537daffa8e601032da7645df
268386b1008793a881c66dc602a821ccb4237c4e 2539672153ae9d3b59d66b3b9f56c84a8dd1341b
c21f12ddfd7e67b90d44250b3a652e8a80bc219a 268386b1008793a881c66dc602a821ccb4237c4e
efc820dd8181e6e848aa71ccb452b6b407a3d0f4 c21f12ddfd7e67b90d44250b3a652e8a80bc219a
1ad00b774cc79fe0199a086ece848d505428f83c efc820dd8181e6e848aa71ccb452b6b407a3d0f4
d731c9f0e3940d02006c29b7ec867f0d323e1f88 1ad00b774cc79fe0199a086ece848d505428f83c
b974d66241f9c660b31f3e7d716636b6c6e35ef7 d731c9f0e3940d02006c29b7ec867f0d323e1f88
39cb83a1efc3da2dc5de4daa8ab83942d8b1fbe5 b974d66241f9c660b31f3e7d716636b6c6e35ef7
59b2594e5faf11dade1f8eb86939f4b6c9cd7f53 39cb83a1efc3da2dc5de4daa8ab83942d8b1fbe5
7fad7bc7f20aea29fd9c179f87aca17e955781ac 59b2594e5faf11dade1f8eb86939f4b6c9cd7f53
723e5a6712968ac6cc7188e3367baaa40facf22b 7fad7bc7f20aea29fd9c179f87aca17e955781ac
abc55cc9cda697b21d6b289b8ca597dbe7229edb 723e5a6712968ac6cc7188e3367baaa40facf22b
e4b6ee23ebbba27738c6ba06af18198b01a57a14 abc55cc9cda697b21d6b289b8ca597dbe7229edb
554e8ef9df61d009635e34a96aa7ad9ba0f08bd0 e4b6ee23ebbba27738c6ba06af18198b01a57a14
35d92ea0dc54687cbef2a66c1f6dc5889eac61f9 554e8ef9df61d009635e34a96aa7ad9ba0f08bd0
a461e8f7f80dba82a57760693eef40b4bfd3b744 35d92ea0dc54687cbef2a66c1f6dc5889eac61f9
20a0ea590ebd7105c8cfde83d42a0d2e5582503d a461e8f7f80dba82a57760693eef40b4bfd3b744
5df68d126590701c8aa9aaac0e7cd283cd0ebb52 20a0ea590ebd7105c8cfde83d42a0d2e5582503d
921f74211ea5e035c5cd45c2311929a9663b2ab0 5df68d126590701c8aa9aaac0e7cd283cd0ebb52
fdd982549e335fb96a0885df85f909c094fb6230 921f74211ea5e035c5cd45c2311929a9663b2ab0
955b73789bd8795c939bd2d1a6eab1e7c5bdce87 fdd982549e335fb96a0885df85f909c094fb6230
f87e0d9fbff9ed5c7b53d1532d3a47b187fa48df 955b73789bd8795c939bd2d1a6eab1e7c5bdce87
e277c407ce4dab4d3f271bea51f30ff426120efe f87e0d9fbff9ed5c7b53d1532d3a47b187fa48df
ae21ed942e8e5570084fd92859368d044b9644e0 e277c407ce4dab4d3f271bea51f30ff426120efe
6b93c47cfd844a2c1ee4a186829e1f6bc40c2204 ae21ed942e8e5570084fd92859368d044b9644e0
8ab61afbffd38983b0000a8a1d5b6df06f43ea59 6b93c47cfd844a2c1ee4a186829e1f6bc40c2204
358dc3f094f6ce8df20ca98934c52fc9d648feb4 8ab61afbffd38983b0000a8a1d5b6df06f43ea59
aaf3dd9f5ca63f0a6b9522035128041d54d0c0f7 358dc3f094f6ce8df20ca98934c52fc9d648feb4
c72a2b5d6ce5aab348176ad45cd5f78d0266430c aaf3dd9f5ca63f0a6b9522035128041d54d0c0f7
dcb594742310aeda51e7f66093697441a0112e1d c72a2b5d6ce5aab348176ad45cd5f78d0266430c
9e19c1b8adeaca4bd4324cd2c5395f07563289b6 dcb594742310aeda51e7f66093697441a0112e1d
cc55248e83402c27e4a575452b0b206fca245edf 9e19c1b8adeaca4bd4324cd2c5395f07563289b6
5f8bd2459a3e75875da8850fa8223ade8406b405 cc55248e83402c27e4a575452b0b206fca245edf
05754ec3160ec33528637394b7872f0840acf3f7 5f8bd2459a3e75875da8850fa8223ade8406b405
0c7fb05b2962cefe8ce939897c9a151f5ce1f8c5 05754ec3160ec33528637394b7872f0840acf3f7
6f67297641b3ff80b8fca36552526717aabcd0fd 0c7fb05b2962cefe8ce939897c9a151f5ce1f8c5
566577f357f5270a2c8e25649c41a64f4d6e6b03 6f67297641b3ff80b8fca36552526717aabcd0fd
06cc5a9567220fd5470f4a57890f99dd1c6fa77d 566577f357f5270a2c8e25649c41a64f4d6e6b03
23bc269062e05f6cd3c635340fb83b5ae71cee6d 06cc5a9567220fd5470f4a57890f99dd1c6fa77d
3d47ac1b7e231518eac37c07f5ebfa984733df6e 23bc269062e05f6cd3c635340fb83b5ae71cee6d
38e57272e185c4c8f0ad35f25222df0d8c3b159d 3d47ac1b7e231518eac37c07f5ebfa984733df6e
e717a537a77d4db3c804cbdf2580768bb9f740c4 38e57272e185c4c8f0ad35f25222df0d8c3b159d
999625967be4e8281d808f466dc76d48251541d0 e717a537a77d4db3c804cbdf2580768bb9f740c4
9543deb0c2ce37cd8d41526b63cab65cf5f225e5 999625967be4e8281d808f466dc76d48251541d0
d85684e4b5be1108c013c7b7fba5426a64600fce 9543deb0c2ce37cd8d41526b63cab65cf5f225e5
0d0a8d195cb704859fa541257dd25bdc980c64b1 d85684e4b5be1108c013c7b7fba5426a64600fce
a6e318617893a06a3827285232638b555a757b0f 0d0a8d195cb704859fa541257dd25bdc980c64b1
f205f22ed804fbca2a46b81c3910b380e57226c2 a6e318617893a06a3827285232638b555a757b0f
dd36b4bdbc510a0e113d27a3671e499a7feeb7b0 f205f22ed804fbca2a46b81c3910b380e57226c2
4a56b1d45ba925d7ea235eeae7c0273a67473317 dd36b4bdbc510a0e113d27a3671e499a7feeb7b0
1d5c8396a37bf278cd234ebb0dcd38332368a531 4a56b1d45ba925d7ea235eeae7c0273a67473317
38d5002245a8407d9cea393a950360fa1fa1ead6 1d5c8396a37bf278cd234ebb0dcd38332368a531
4dce4eb251b745605a62e26b65fb47dedd402275 38d5002245a8407d9cea393a950360fa1fa1ead6
adead099f0f8a606405ecdcb107dbf79ff267ced 4dce4eb251b745605a62e26b65fb47dedd402275
d9fa796e604068b522359da8b8187a0c798403d3 adead099f0f8a606405ecdcb107dbf79ff267ced
42b474501af5e9a307a80b75c2495102adb67f3a d9fa796e604068b522359da8b8187a0c798403d3
dbfa77e835c02434004738f550c653178fc07522 42b474501af5e9a307a80b75c2495102adb67f3a
4beb807c8133b22f2207c981622e6aef6486cf9f dbfa77e835c02434004738f550c653178fc07522
92e37a1488fed70a478dac25e6f5e95cc2a06897 4beb807c8133b22f2207c981622e6aef6486cf9f
6e79bc14acc10c6f7f867fccfea7871260d671c5 92e37a1488fed70a478dac25e6f5e95cc2a06897
7cf6911136409180b56763ab6abe4baed47e083c 6e79bc14acc10c6f7f867fccfea7871260d671c5
7483634b7d7fcc9d58c21c6a8d639a81b2b1566a 7cf6911136409180b56763ab6abe4baed47e083c
7c7725e50bc7c3debc0f56964e862d906054955b 7483634b7d7fcc9d58c21c6a8d639a81b2b1566a
4413a05bd785cbef398fc418ad12b008fa090a00 7c7725e50bc7c3debc0f56964e862d906054955b
11ae620f717cf011436db52cf4b3b76d0015c606 4413a05bd785cbef398fc418ad12b008fa090a00
886e13f6ad7178d64b63f7a5cb54637064683816 11ae620f717cf011436db52cf4b3b76d0015c606
8eb8fe8616a4966ddcc44e2285d5cc7bec6566b3 886e13f6ad7178d64b63f7a5cb54637064683816
258d2488c56684e97cbd2f8e9e665264f6063b7c 8eb8fe8616a4966ddcc44e2285d5cc7bec6566b3
cac3faa83c89a2cf7f5b8aadafcb830e55c9b6ce 258d2488c56684e97cbd2f8e9e665264f6063b7c
1603b8b7576b3317fd80367188e900fd955ae5bb cac3faa83c89a2cf7f5b8aadafcb830e55c9b6ce
343307cf4090ee74a5a81dc69db2fc83a18c7b4e 1603b8b7576b3317fd80367188e900fd955ae5bb
2530cfabb139564d2c55df68cac4ebde1c9b9722 343307cf4090ee74a5a81dc69db2fc83a18c7b4e
403ce689543adf561554f47890152f967323944b 2530cfabb139564d2c55df68cac4ebde1c9b9722
7e69ba38e8ed11fcab9a2a7adb78caf8c3c5d6d6 403ce689543adf561554f47890152f967323944b
fb5bda05c9c153cd27a2142decb1ac76b8985c92 7e69ba38e8ed11fcab9a2a7adb78caf8c3c5d6d6
bbea55da2758e46f4df42316730b525ba4c771c7 fb5bda05c9c153cd27a2142decb1ac76b8985c92
1dac9008f219636f18a80c9d5451c72481225182 bbea55da2758e46f4df42316730b525ba4c771c7
83e56b142f5ea55be6f22b71a1d1cf1f54d5ae96 1dac9008f219636f18a80c9d5451c72481225182
6ffd808a99550d2c18741a83baac469b2f0fec4b 83e56b142f5ea55be6f22b71a1d1cf1f54d5ae96
3cb817fb6b50ec5b963bb2d0a04678ba22e164e4 6ffd808a99550d2c18741a83baac469b2f0fec4b
24682fcad56ab0123571ba4e9a9565869263206c 3cb817fb6b50ec5b963bb2d0a04678ba22e164e4
94d8b4b3ec4c3034302e035c0ecb3e6e0cb711c0 24682fcad56ab0123571ba4e9a9565869263206c
864fa199b96a65b9e06f9e0f4db2c1d5bc1b0233 94d8b4b3ec4c3034302e035c0ecb3e6e0cb711c0
d19f008fc88d6011174c4aaf030938dc409d911f 864fa199b96a65b9e06f9e0f4db2c1d5bc1b0233
eeb73278fdad3851c5352132eff3a361c527a606 d19f008fc88d6011174c4aaf030938dc409d911f
c693a7ba82749bf5227d2ca7886dc4528a640b1a eeb73278fdad3851c5352132eff3a361c527a606
47174bec23a1af308a9dc8814f912f2f0bcea3eb c693a7ba82749bf5227d2ca7886dc4528a640b1a
46c06df624e09589c5bf95c597b2a0be55ebf5a8 47174bec23a1af308a9dc8814f912f2f0bcea3eb
79676a58afaf8e926f42aeed22e4d99806b10acc 46c06df624e09589c5bf95c597b2a0be55ebf5a8
54fd26c9a68fa022801d90f61414200174bc0685 79676a58afaf8e926f42aeed22e4d99806b10acc
20d50cecfe1fcc4444c2bf536ad32fe43d4ec44f 54fd26c9a68fa022801d90f61414200174bc0685
65752df780a3ee524d44da5114943ed6cc91a39b 20d50cecfe1fcc4444c2bf536ad32fe43d4ec44f
065f579d64e4d970521543e7bfd29b682ad4fe73 65752df780a3ee524d44da5114943ed6cc91a39b
3d64370bd35486a11ab5a2eae4e0b319e4849587 065f579d64e4d970521543e7bfd29b682ad4fe73
6026b44d4e6d83f509b91a254b7313124dc2aad3 3d64370bd35486a11ab5a2eae4e0b319e4849587
3a5fa3eff826343a7a465cbb6039aa10a5233fcc 6026b44d4e6d83f509b91a254b7313124dc2aad3
a2a6b6ba5c727e5ae56fa0f6741561837cf007c2 3a5fa3eff826343a7a465cbb6039aa10a5233fcc
08237a5c0cce989265967133fea04ad7955ca9e9 a2a6b6ba5c727e5ae56fa0f6741561837cf007c2
96d6def222517fb836da9f37885a23038ce26343 08237a5c0cce989265967133fea04ad7955ca9e9
b601bd791f10428acd72e4c8b59a2d44eb22b0cf 96d6def222517fb836da9f37885a23038ce26343
b08f433ab5b38e92e2dfdebaf87806fcb9cae8c9 b601bd791f10428acd72e4c8b59a2d44eb22b0cf
a136a4ded9c38438207ce20aa9a72d76d0f0b1cd b08f433ab5b38e92e2dfdebaf87806fcb9cae8c9
acc692f7edb9cf41dbd3a3a99ef272484575d42f a136a4ded9c38438207ce20aa9a72d76d0f0b1cd
3b94a2c1e59899e1e86534db7209af2ac4a8d25e acc692f7edb9cf41dbd3a3a99ef272484575d42f
fbf0e0e297f572b80c9fb0cbfc22fa6f3dc7fa2c b08f433ab5b38e92e2dfdebaf87806fcb9cae8c9
15c54ab15944da5728759f2a1c8a4fb4cf0da164 fbf0e0e297f572b80c9fb0cbfc22fa6f3dc7fa2c 3b94a2c1e59899e1e86534db7209af2ac4a8d25e
682325bee7bd3a196828651cc9869d394eb1ac79 15c54ab15944da5728759f2a1c8a4fb4cf0da164
c2ccea5c6b7d4b89e72de7a8fdfe3db5fd175695 682325bee7bd3a196828651cc9869d394eb1ac79
d66eb845750899faeb31a903948991e5bc512947 c2ccea5c6b7d4b89e72de7a8fdfe3db5fd175695
b7298407ae22ed21a02ffb10c1463f1a287f159b d66eb845750899faeb31a903948991e5bc512947
f2b5786c22107cbdcdf1d869424ffdf856cc56b3 b7298407ae22ed21a02ffb10c1463f1a287f159b
f6999f4aae2463b130e966d6c937c1c9aae525ac f2b5786c22107cbdcdf1d869424ffdf856cc56b3
e728974850a1856593e3971c74a22c22ca255d77 f6999f4aae2463b130e966d6c937c1c9aae525ac
a761f135ae7810f192269802a8b64f9b290e8c07 e728974850a1856593e3971c74a22c22ca255d77
6b88cb5aa8f621a42f05ea13c4c43d4e10728719 b08f433ab5b38e92e2dfdebaf87806fcb9cae8c9
750ca04c127c48b03f20a24b20422b21d73ca8cf 6b88cb5aa8f621a42f05ea13c4c43d4e10728719 a761f135ae7810f192269802a8b64f9b290e8c07
5c6df983ddf89e303736d55824711a994e67d123 750ca04c127c48b03f20a24b20422b21d73ca8cf
ae20bf45eb005eae5838b9e4d5c4fc42323b23de 5c6df983ddf89e303736d55824711a994e67d123
88054d803278dd95674354febb7ebad82f33bf4f ae20bf45eb005eae5838b9e4d5c4fc42323b23de
c22ddb363dd7139a286b460cb5a8e60657fd4b7f 88054d803278dd95674354febb7ebad82f33bf4f
087066f2b985160fc6b1e8a290b91703974019ad c22ddb363dd7139a286b460cb5a8e60657fd4b7f
412cf6a3b0ae7299b7f185c8253368bc5233557d 087066f2b985160fc6b1e8a290b91703974019ad
913d2da82456c9dac7933124c596fa3410157ac8 412cf6a3b0ae7299b7f185c8253368bc5233557d
a0c75f77900d2e35e61fadba5c826c05981e9beb 913d2da82456c9dac7933124c596fa3410157ac8
6ea05edde0ae825d278241700f2b882ade2b9cf2 a0c75f77900d2e35e61fadba5c826c05981e9beb
cee1bce7c8100c7b432315bcdb4f8b1e6e4159b2 6ea05edde0ae825d278241700f2b882ade2b9cf2
53b37e04f075679053bbfc592e60eddefc9fb1c7 cee1bce7c8100c7b432315bcdb4f8b1e6e4159b2
c9eda945dc9d9d04865c158326288e3287a6d10f 53b37e04f075679053bbfc592e60eddefc9fb1c7
1c1cf7be319010e9a15e8ccd084fef0da22fc22c c9eda945dc9d9d04865c158326288e3287a6d10f
28459f3da2267c477cc54e597df735e0ba4843d2 1c1cf7be319010e9a15e8ccd084fef0da22fc22c
64fff75d755bdb1878b52b6c5f26d8bcfc5a090e 28459f3da2267c477cc54e597df735e0ba4843d2
10a7042d1a2692ad5a25e7afc2b996529a674928 64fff75d755bdb1878b52b6c5f26d8bcfc5a090e
c261318f9c3e0f5ec90586fc791c4e69f0e68cbd 10a7042d1a2692ad5a25e7afc2b996529a674928
16a851884156399a7b4d782ee0e9d8f0c565a55e c261318f9c3e0f5ec90586fc791c4e69f0e68cbd
cc8090f8c95adb7455b73846dc883aeeb4805ae0 16a851884156399a7b4d782ee0e9d8f0c565a55e
5e1f9c68f5d36fd0d2d71ce9a56f3107c88392ce cc8090f8c95adb7455b73846dc883aeeb4805ae0
52d9f17bc89421fe9b3417e61909f74ceb359dd2 5e1f9c68f5d36fd0d2d71ce9a56f3107c88392ce
018d25e3722d7830dd85d1e04e19583660e55f28 52d9f17bc89421fe9b3417e61909f74ceb359dd2
65eccf69aed67ddd57ad742da8aa9c2a8f30eeed 018d25e3722d7830dd85d1e04e19583660e55f28
66557ea0839bf84c72f8979a849f0786619ce864 10a7042d1a2692ad5a25e7afc2b996529a674928
c0b2588d96d8e2db6fd009af2cfd7f993dca8383 66557ea0839bf84c72f8979a849f0786619ce864 65eccf69aed67ddd57ad742da8aa9c2a8f30eeed
b663114f5604dfc2b5693d8f016a471e8f832e81 c0b2588d96d8e2db6fd009af2cfd7f993dca8383
4a309351dff3f0b3731d7b51b8f4b0c07c19bad4 b663114f5604dfc2b5693d8f016a471e8f832e81
83ee791b9cf01bc0e507e3907bb1be06124c902a 4a309351dff3f0b3731d7b51b8f4b0c07c19bad4
44b8fb31aa98881c4f8b4051154ab690bd5f2add 83ee791b9cf01bc0e507e3907bb1be06124c902a
0924b0dbba0cd3def491254707b495b6dca6a311 44b8fb31aa98881c4f8b4051154ab690bd5f2add
c17cc182fe100993c717fed12a6c975404b0d13d 0924b0dbba0cd3def491254707b495b6dca6a311
11ebbb45a2717e1c8e81356ffd4c7c1ba9cb498b c17cc182fe100993c717fed12a6c975404b0d13d
0572879790a4cb19c81bd7a5c2d7f12142354a31 11ebbb45a2717e1c8e81356ffd4c7c1ba9cb498b
1b5fc762a281c2927b54994e2cdf7683e076e649 0572879790a4cb19c81bd7a5c2d7f12142354a31
176de2b91eb4f988a6b0e3f1faa9a0045a139d36 1b5fc762a281c2927b54994e2cdf7683e076e649
fdabe6b2deefa22d2d4d2afdd06acf934abe4ff2 176de2b91eb4f988a6b0e3f1faa9a0045a139d36
8b4f6e8e4725b69981cc28cefefd70d3cf1b9acd fdabe6b2deefa22d2d4d2afdd06acf934abe4ff2
64e08f84685d9bddeef1d1d5d491c51e212dd365 8b4f6e8e4725b69981cc28cefefd70d3cf1b9acd
98b95123eb9b7f9d8f8f9fe667bde86cd296b9d7 64e08f84685d9bddeef1d1d5d491c51e212dd365
f410240af857a74615f7b437c6972bb4738b108f 98b95123eb9b7f9d8f8f9fe667bde86cd296b9d7
dd02dd1c04998e39844a05180da58e97f250b62f f410240af857a74615f7b437c6972bb4738b108f
14c4bb18de895fafe0c883a8a7fd9f737b66a1ea dd02dd1c04998e39844a05180da58e97f250b62f
183adfb63ec746be8796efb47a71ab844843fb70 14c4bb18de895fafe0c883a8a7fd9f737b66a1ea
3908fc1f7daaf07e4f9836e40806b63ede9338c2 183adfb63ec746be8796efb47a71ab844843fb70
77b4824f326202be099ae5c87bb9598ffbccefa0 3908fc1f7daaf07e4f9836e40806b63ede9338c2
03f239d0bb7ce8d41ab03674069c3e73bd22b1fe 77b4824f326202be099ae5c87bb9598ffbccefa0
b89c8e0c071c31eb7ce4fb961ac88b6d9e091dd8 03f239d0bb7ce8d41ab03674069c3e73bd22b1fe
733a3a5918e465216efe6dabffba679c443dd96f b89c8e0c071c31eb7ce4fb961ac88b6d9e091dd8
fbb631fb6c8724bfb2a274eca6edf8a29db8347c 733a3a5918e465216efe6dabffba679c443dd96f
a941902c8eaca368b2d6d667b392575565be4360 fbb631fb6c8724bfb2a274eca6edf8a29db8347c
ac2a43e294464498ed27acc3aadc14471b4ba927 a941902c8eaca368b2d6d667b392575565be4360
f31e5bfb7cf74db0e4786203b62dedd9037853b3 ac2a43e294464498ed27acc3aadc14471b4ba927
c5174c1db5258c286a82bdd741a4749a7ca805c0 f31e5bfb7cf74db0e4786203b62dedd9037853b3
a5d3b14d65c24c5cb1c67a90ab0465a2a267454a c5174c1db5258c286a82bdd741a4749a7ca805c0
2770d2b9e7cefbd22b80d18424ba41dd2959330d 10a7042d1a2692ad5a25e7afc2b996529a674928
d10ebe3fad63edc5325933a5daf0bb21db18c28f 2770d2b9e7cefbd22b80d18424ba41dd2959330d a5d3b14d65c24c5cb1c67a90ab0465a2a267454a
a8645ed4e4e52a7d4ad63c7368d1941e54e8b1c4 d10ebe3fad63edc5325933a5daf0bb21db18c28f
8e7dd3d90f17a49d815528f78dd005f594b68016 a8645ed4e4e52a7d4ad63c7368d1941e54e8b1c4
d3bb6cc991124b5d7ca7af1569156f5f02e6ca6b 8e7dd3d90f17a49d815528f78dd005f594b68016
8af80e5d2f0a985e156a4ca40c6a5f0f2988c335 d3bb6cc991124b5d7ca7af1569156f5f02e6ca6b
a7e9a2156e694076427bc36cace0a5347a98d04b 8af80e5d2f0a985e156a4ca40c6a5f0f2988c335
eb86d0abd905a2dd078dda0cc2335f79b64d9fd4 a7e9a2156e694076427bc36cace0a5347a98d04b
596bcd0e4b8791546081f482d1a1204a57b6f095 eb86d0abd905a2dd078dda0cc2335f79b64d9fd4
d7f92e498552356c548089f7ab7aa0d50f2e166a 596bcd0e4b8791546081f482d1a1204a57b6f095
6817d83bbbcd16545cf28d17f7a82d42ea769c69 d7f92e498552356c548089f7ab7aa0d50f2e166a
73e865fb219aca7ea4533d4ee1900b7bfd7abe03 6817d83bbbcd16545cf28d17f7a82d42ea769c69
920e8cba39895732587475f93b9eafb917f8904b 73e865fb219aca7ea4533d4ee1900b7bfd7abe03
ea4e40f5c0fb7a3b457dec39d7d68426e762346e 920e8cba39895732587475f93b9eafb917f8904b
47efda749fcfad840a51eb5c6ae9fc512fdd70ad ea4e40f5c0fb7a3b457dec39d7d68426e762346e
28fb3c323f107a0536d573368a37b4f43894e0c1 47efda749fcfad840a51eb5c6ae9fc512fdd70ad
be4d73ab3d9b880e23813657c614f5ca2b221ec6 28fb3c323f107a0536d573368a37b4f43894e0c1
b88324aa42627e2e5eced4ea34853e08fb0463ee be4d73ab3d9b880e23813657c614f5ca2b221ec6
786f3e216af43c0dfc1ac8f9fc7a45a3be571e08 b88324aa42627e2e5eced4ea34853e08fb0463ee
55bd8d032e2eebb9a187b0cbd1201b3a154888f9 786f3e216af43c0dfc1ac8f9fc7a45a3be571e08
bade1ce545e777ab9ba2c787e566652286bddf8e 55bd8d032e2eebb9a187b0cbd1201b3a154888f9
1ac2343d8ead08ad846dea25aae1eff34642683d bade1ce545e777ab9ba2c787e566652286bddf8e
682e25b88fa894be2eef15a4bd4974998e64f42f 1ac2343d8ead08ad846dea25aae1eff34642683d
b5cc68175fb46203be9eaea41163e6292ef9e35a 682e25b88fa894be2eef15a4bd4974998e64f42f
78fdcbc1bdbc982cde0898e65420cae1f759aa40 b5cc68175fb46203be9eaea41163e6292ef9e35a
e709b4e60bd0b8c44d21f8cef3d46dec03cc14bc 78fdcbc1bdbc982cde0898e65420cae1f759aa40
57ac7d0c0c586f06c1d5e0151aa3afc203217080 e709b4e60bd0b8c44d21f8cef3d46dec03cc14bc
e023395bfd4836a0ecc17343c677e08b09e28b2e 57ac7d0c0c586f06c1d5e0151aa3afc203217080
11989a45fd29bfad252308c88943313f73b790ea e023395bfd4836a0ecc17343c677e08b09e28b2e
fee3de5a2b8587634688bc0fbff487a9e3478f7a 11989a45fd29bfad252308c88943313f73b790ea
c3545319d93c10a98c568b5868c5d711788bf719 fee3de5a2b8587634688bc0fbff487a9e3478f7a
130cb06a8d1cfccbfe72664f45b423d66c497cea c3545319d93c10a98c568b5868c5d711788bf719
845688f357b4d497a47bec561f2d583770dd9522 130cb06a8d1cfccbfe72664f45b423d66c497cea
b1d4329ce423abf4ec6639b459940fa6ccf01939 845688f357b4d497a47bec561f2d583770dd9522
66f5ef9932917e4ba7106f0fa9471589de3c9740 b1d4329ce423abf4ec6639b459940fa6ccf01939
146715c5badcdc06dc48d8e43d08bed7881d1d63 66f5ef9932917e4ba7106f0fa9471589de3c9740
20fd2f8af0a0772b2229674aa831dec0dcf3876e 146715c5badcdc06dc48d8e43d08bed7881d1d63
e129c83ba431ab2f2fc95d12d49fe82fd23a73c4 20fd2f8af0a0772b2229674aa831dec0dcf3876e
fd66a974e4a3b85164506659ab379b2682937a92 e129c83ba431ab2f2fc95d12d49fe82fd23a73c4
3ba237f7fafbcbf8719de8ca6deca207400c87b1 fd66a974e4a3b85164506659ab379b2682937a92
a3704637fbc6dcc5fc88a1efe1cf39a17bccd6c7 3ba237f7fafbcbf8719de8ca6deca207400c87b1
8fd069f2592d08f62172ad592bc97d7c35be39db a3704637fbc6dcc5fc88a1efe1cf39a17bccd6c7
380788cefb8cbebff3b45b317e0b3fddfb78ba57 8fd069f2592d08f62172ad592bc97d7c35be39db
66ace3317df41157b4077848ab30e7f94f0ea3e7 380788cefb8cbebff3b45b317e0b3fddfb78ba57
a02ea8b3a5eafe2a80958035dda9d94fdf3083fa 66ace3317df41157b4077848ab30e7f94f0ea3e7
a3dd81c7fac8e9ae7e9860abba21c011a0230040 a02ea8b3a5eafe2a80958035dda9d94fdf3083fa
e4ae60c0b9fcb5538568a2e224525827a0720297 a3dd81c7fac8e9ae7e9860abba21c011a0230040
16a6c9e5c62bfe9c088f893d007e796e7d71e2aa e4ae60c0b9fcb5538568a2e224525827a0720297
c02cd479b812b75a3c4d977863847010ab2056ff 16a6c9e5c62bfe9c088f893d007e796e7d71e2aa
31230f94864c65e3bd7fa867ea3a3918bec59fbf c02cd479b812b75a3c4d977863847010ab2056ff
4a8c9615ac4ee805de77c6c7aea8dccca56c9ca2 31230f94864c65e3bd7fa867ea3a3918bec59fbf
21f8fb84333df4d9af89ca5582f4ba3669c3baec 4a8c9615ac4ee805de77c6c7aea8dccca56c9ca2
b71b78c7e78a51628cdbf8cc11e42ac6e17a4956 21f8fb84333df4d9af89ca5582f4ba3669c3baec
35d4f70aa347b39dc5920319ebbbe06a3de393fa b71b78c7e78a51628cdbf8cc11e42ac6e17a4956
0391ebe3ec097add91cb818b836a06c7a6700d05 35d4f70aa347b39dc5920319ebbbe06a3de393fa
22e20a684a128a8448b7ea7998d23f7cfc90d852 0391ebe3ec097add91cb818b836a06c7a6700d05
0f4c03e23559d1512a9be6ba2ed05511d2eadd39 22e20a684a128a8448b7ea7998d23f7cfc90d852
93db0f4dd2fbd57b4610e2f40077695cd01fe253 0f4c03e23559d1512a9be6ba2ed05511d2eadd39
935a4f97125bd68cf754c0d4febaa55e01b0a09c 93db0f4dd2fbd57b4610e2f40077695cd01fe253
35cca6a1747d0358f73ae02fee0a554c594f2856 935a4f97125bd68cf754c0d4febaa55e01b0a09c
b78d01dd4e9514ad79d4b9a7b1641db4d19eda1d 35cca6a1747d0358f73ae02fee0a554c594f2856
91f9983456b2d59cbda6b042144ef7b6884fd0a7 b78d01dd4e9514ad79d4b9a7b1641db4d19eda1d
9eb26398c01d3cab6c1f9b31c1f474eca1817e7c 91f9983456b2d59cbda6b042144ef7b6884fd0a7
568f4e3d7f08f43d9560fb165e8e3ea70f0b447a 9eb26398c01d3cab6c1f9b31c1f474eca1817e7c
4acc659d1a812eeb862f99ac7d8e98843ab9f84f 568f4e3d7f08f43d9560fb165e8e3ea70f0b447a
e2cc1ddb2171215d12c06b15ee7417d8ca622e02 4acc659d1a812eeb862f99ac7d8e98843ab9f84f
f1595828de964ee673e2794791b84b54206b832f e2cc1ddb2171215d12c06b15ee7417d8ca622e02
3adcce7368c1c07e483d1d71eea87881d51fc60f f1595828de964ee673e2794791b84b54206b832f
6c9a6daaf0cc514b1bba3c599850c2985be7aaf8 3adcce7368c1c07e483d1d71eea87881d51fc60f
c90b6048f4e0570cb8f3ca1e04d8f9707b60e82a 6c9a6daaf0cc514b1bba3c599850c2985be7aaf8
4a4f290a81e3b022b2738fb504e815b7b5489001 c90b6048f4e0570cb8f3ca1e04d8f9707b60e82a
507e94f0973fb85fa1e9748987804d532d20b75c 4a4f290a81e3b022b2738fb504e815b7b5489001
9c78a7b2490b03ac17740582d2716fc9042f766c 507e94f0973fb85fa1e9748987804d532d20b75c
04878eb5402a4d7b0906d399a6d24ec12641882b 9c78a7b2490b03ac17740582d2716fc9042f766c
8bfe19f35d71f5edbf7da10703bded35492b3325 04878eb5402a4d7b0906d399a6d24ec12641882b
17f59f72fdefc4fbc3fd70e6ce266bd05173256c 8bfe19f35d71f5edbf7da10703bded35492b3325
2b43fc2428c2f262d80df31b086fc3a753825611 17f59f72fdefc4fbc3fd70e6ce266bd05173256c
a398ca511c225a522631d0c925c46c69374a9594 2b43fc2428c2f262d80df31b086fc3a753825611
e0188aa8f2f79803c2378fb442322fb798190e13 a398ca511c225a522631d0c925c46c69374a9594
8c59285b023018df8e4e30aae94bdd3769c86325 e0188aa8f2f79803c2378fb442322fb798190e13
acbff863630cff119f503bef850d73c5f893cbd1 8c59285b023018df8e4e30aae94bdd3769c86325
f0185c5c8ffd1dd94110d320e68ce372592c259f acbff863630cff119f503bef850d73c5f893cbd1
1f73fd5b183be27f4db9b2bd31be297cfb6e634c f0185c5c8ffd1dd94110d320e68ce372592c259f
719f07640943226c5158117ebf828bf36f238f53 1f73fd5b183be27f4db9b2bd31be297cfb6e634c
dd008dbc2da27a7437c640ecd49b30c250da96a2 719f07640943226c5158117ebf828bf36f238f53
4b4b67acbafd90aad439d3530625827b2640ef7d dd008dbc2da27a7437c640ecd49b30c250da96a2
4800cfd941ff03e0db69105ab41b4a09f71833a1 4b4b67acbafd90aad439d3530625827b2640ef7d
911705a1b8126b8e1e22a1dbbbb670a59fcabfd5 4800cfd941ff03e0db69105ab41b4a09f71833a1
7c66240d621ca7ce70080a4d12e9e229a4721916 911705a1b8126b8e1e22a1dbbbb670a59fcabfd5
30c2f80b3700ceffdddbd6b4a11f35cef7f459cf 7c66240d621ca7ce70080a4d12e9e229a4721916
5aef5d4803880e5b70bd68868ca558c181d8bb9f 30c2f80b3700ceffdddbd6b4a11f35cef7f459cf
14ef8afdd32000e12113313683882957e8b54681 5aef5d4803880e5b70bd68868ca558c181d8bb9f
bbd89c1ffc59744dddd2742c24ff98f22a4ef71a 14ef8afdd32000e12113313683882957e8b54681
120f1cd3a2ddfdc12b44775cfdd054291e45b387 bbd89c1ffc59744dddd2742c24ff98f22a4ef71a
4ef1873b5f42dce48caad67bfa78fb7239627443 120f1cd3a2ddfdc12b44775cfdd054291e45b387
d244a3f673ee3b72c8a9e90a68ed915ad561edf7 4ef1873b5f42dce48caad67bfa78fb7239627443
e6253459fa9051268fc0fca1a1448233aaf364c1 d244a3f673ee3b72c8a9e90a68ed915ad561edf7
b6fd427a2b13f854a3c73d5bf13d3df6b77926b6 e6253459fa9051268fc0fca1a1448233aaf364c1
efec38242f1837bb122736f9720335dd0e37828f b6fd427a2b13f854a3c73d5bf13d3df6b77926b6
bd4b1cf0b72289635704572c09ef943690bed300 efec38242f1837bb122736f9720335dd0e37828f
51be4032625f3b86f329b51e4e41433e4d00f1b5 bd4b1cf0b72289635704572c09ef943690bed300
e3511b411370a536c5783b783e183cd2acaf984a 51be4032625f3b86f329b51e4e41433e4d00f1b5
78a4e9e6330ecfdb624a9022e168336698cd712b e3511b411370a536c5783b783e183cd2acaf984a
986cf00550df3b6c82284dfee16b2b7d6462b93c 78a4e9e6330ecfdb624a9022e168336698cd712b
a2dc6a9444c81cb11bde16eda61a750009b0a81f 986cf00550df3b6c82284dfee16b2b7d6462b93c
7eee7964e445d9f4c038c08470d8dad3060c91bf a2dc6a9444c81cb11bde16eda61a750009b0a81f
f440c7a4cf62384e60ab377cdc4841acdd0f0ef2 7eee7964e445d9f4c038c08470d8dad3060c91bf
7441d77175a0f8332df3b723f3f6facdaf8762c1 f440c7a4cf62384e60ab377cdc4841acdd0f0ef2
db3cabbf3f5134d01f3f8ad28278314138b40b56 7441d77175a0f8332df3b723f3f6facdaf8762c1
be1371b4d24b0c3a82c174b9abc2e4c0f71585a6 db3cabbf3f5134d01f3f8ad28278314138b40b56
bfe8816fe808a8c3b929bbc2f6adc1bad2cee166 be1371b4d24b0c3a82c174b9abc2e4c0f71585a6
871c7a7f7ee4610a50f6518ac4f49ca9f54bc3b9 bfe8816fe808a8c3b929bbc2f6adc1bad2cee166
e1074701a428721fed698cc581ffe7f05da463f4 871c7a7f7ee4610a50f6518ac4f49ca9f54bc3b9
44e98336aee792221eaba9d4363a1b4f483aedbe e1074701a428721fed698cc581ffe7f05da463f4
072bce2bde7bccfb8058af069050d65dd66d7eff 44e98336aee792221eaba9d4363a1b4f483aedbe
2dc1cabd6dd8b4e37af1a2acb709d8127058ef99 072bce2bde7bccfb8058af069050d65dd66d7eff
df2af810aba286e0cb3f692e63d169916409c86d 2dc1cabd6dd8b4e37af1a2acb709d8127058ef99
5a9251693557ba195d85c4983b1620d378e39c03 df2af810aba286e0cb3f692e63d169916409c86d
0f848a57a5e98a5d85bc8a887fab2cdf0c22e3fe 5a9251693557ba195d85c4983b1620d378e39c03
8000b959e58186b0089f16cf06cbae83ad6eddba 0f848a57a5e98a5d85bc8a887fab2cdf0c22e3fe
b707def3efe2545e0d1b42d008530b7c821834ef 8000b959e58186b0089f16cf06cbae83ad6eddba
5b5378066822354b4756ccccbe5337787e5a4489 b707def3efe2545e0d1b42d008530b7c821834ef
ddfaea12430d44c11ecf1ea76925d81765c116bd 5b5378066822354b4756ccccbe5337787e5a4489
0376abfb0c616f93b536f9c8358e9dff1315e854 ddfaea12430d44c11ecf1ea76925d81765c116bd
d9b5b85571f2fa6346ce78adebee17cfe8b778bd 0376abfb0c616f93b536f9c8358e9dff1315e854
908c23a0b65163d048f6cff962fb037691eda839 d9b5b85571f2fa6346ce78adebee17cfe8b778bd
9da24f50700ff5d2a5704624476ccc643a777615 908c23a0b65163d048f6cff962fb037691eda839
4cc944cbf1d6cc1b35835368fcd4dc9369f91c62 9da24f50700ff5d2a5704624476ccc643a777615
5b43f3ea27f89941c64704266fc5dba18a0dbe44 4cc944cbf1d6cc1b35835368fcd4dc9369f91c62
42ec764cf5d379906b025af458b2311cafbd2a0d 5b43f3ea27f89941c64704266fc5dba18a0dbe44
87c0a428987d09ec280a645ae84a507327bd52b8 42ec764cf5d379906b025af458b2311cafbd2a0d
7b80a3e8de15aeb39823b8a4d72b42361447419b 87c0a428987d09ec280a645ae84a507327bd52b8
f5a5038f381f3f5680b24c6e10d04e760cb93d22 7b80a3e8de15aeb39823b8a4d72b42361447419b
844e69bc471b8ea1ba15c18a473b5096dd0c9185 f5a5038f381f3f5680b24c6e10d04e760cb93d22
4b77d172638b1c3fe4b056a62d53e70cc7c36c5c 844e69bc471b8ea1ba15c18a473b5096dd0c9185
04d31b0f340aba58aa8d2e2366c0ddee8a17441c 4b77d172638b1c3fe4b056a62d53e70cc7c36c5c
fb2d4b80c5737f0cbb9887f7a748d397509e5276 04d31b0f340aba58aa8d2e2366c0ddee8a17441c
63638a4900e7bc57c9eccd54d00c71e634a5d0e9 fb2d4b80c5737f0cbb9887f7a748d397509e5276
6b26294f8421193207922386450876aa2627ca02 63638a4900e7bc57c9eccd54d00c71e634a5d0e9
e017a21acfea688a2134d087f75ccc3769986f0b 6b26294f8421193207922386450876aa2627ca02
4faeede6d1e13fb9f614d19f85353c2867892205 e017a21acfea688a2134d087f75ccc3769986f0b
30ecf2dbcbf485e11c3b135066cfd624e9cacacf 4faeede6d1e13fb9f614d19f85353c2867892205
ace4b167920ba0f39adaa07e64fc7d052f1fbe69 30ecf2dbcbf485e11c3b135066cfd624e9cacacf
a8baa0665538f0c52a9a619081722e8caf55e9f5 ace4b167920ba0f39adaa07e64fc7d052f1fbe69
d987ccc8a15ff78906d1f7ef322a46a7c96d9f7f a8baa0665538f0c52a9a619081722e8caf55e9f5
14f0a284b21c77cf2596a20446eb52804f54fb0a d987ccc8a15ff78906d1f7ef322a46a7c96d9f7f
c9b52d7375b6a3ec57c1226d6a94848fba0e4b1f 14f0a284b21c77cf2596a20446eb52804f54fb0a
e0d84aeb1b517526fafd296ad233e31deb83c223 c9b52d7375b6a3ec57c1226d6a94848fba0e4b1f
92d4e986cea2620904780f68245b2a4c115150d6 e0d84aeb1b517526fafd296ad233e31deb83c223
70c8557bafb49e0b119fbb612c2d1215982deb57 92d4e986cea2620904780f68245b2a4c115150d6
d97a1b8f9299a4b994c4eb0ddc869145c3a1d3b8 70c8557bafb49e0b119fbb612c2d1215982deb57
5a5a4a681e935ddb74c1bb5f0f91f7da6282ced0 d97a1b8f9299a4b994c4eb0ddc869145c3a1d3b8
587bc796009021c987fa81f28a63e154b6a62647 5a5a4a681e935ddb74c1bb5f0f91f7da6282ced0
e578894458175725f8c77f567dde7af711028404 587bc796009021c987fa81f28a63e154b6a62647
9f7eeaeeea73e80484fd7be3602c2184e4dbc686 e578894458175725f8c77f567dde7af711028404
1935d06cc500c38052aeed746e409fb1554a1255 9f7eeaeeea73e80484fd7be3602c2184e4dbc686
39dfdc429d46db15faeaa63d259b533370d47336 1935d06cc500c38052aeed746e409fb1554a1255
c4396dfe230b0164a50d8cac85b974d403e612e4 39dfdc429d46db15faeaa63d259b533370d47336
37a266276fcac106230374f86091e52d44b45f8b c4396dfe230b0164a50d8cac85b974d403e612e4
3b8bfa37665e288c107789514a5c46a2677602fd 37a266276fcac106230374f86091e52d44b45f8b
d8ea0cf55618e59c25b7b7b61d223ae06ef7a2e7 3b8bfa37665e288c107789514a5c46a2677602fd
ffb523cae07614a826278f3c0b3b0dc646ebcfa6 d8ea0cf55618e59c25b7b7b61d223ae06ef7a2e7
559f9838c051ba459811aa6b00cdd1cd26db790d ffb523cae07614a826278f3c0b3b0dc646ebcfa6
4912c141348242e3e970ec9ce6b2ebc656deed91 559f9838c051ba459811aa6b00cdd1cd26db790d
c13ab5e2f47795a8baad2ab4ec38c7b86e232c23 4912c141348242e3e970ec9ce6b2ebc656deed91
c8f4e6aaf18a2d0efa1a9c28e5d7619cfd1035d0 c13ab5e2f47795a8baad2ab4ec38c7b86e232c23
890dcd2f8fc4dddc9b9753f3feee8f19c7393fc9 c8f4e6aaf18a2d0efa1a9c28e5d7619cfd1035d0
6f79be085c50b415e3fff3f6af43fdbd16339005 890dcd2f8fc4dddc9b9753f3feee8f19c7393fc9
767951688e455a69d84e987ba268057fa38a803e 6f79be085c50b415e3fff3f6af43fdbd16339005
facf7d3bb2748d2fa09ef2be7d83f126135d025c 767951688e455a69d84e987ba268057fa38a803e
0dd77ec6ead2a27fcf51565f8971dbabb44e30cc facf7d3bb2748d2fa09ef2be7d83f126135d025c
9b458e8e9373abcb8875d357d2f6d3c2ce05bf1a 0dd77ec6ead2a27fcf51565f8971dbabb44e30cc
c9e1efa1717ed5afe812739b6aae5fa0a65298c0 9b458e8e9373abcb8875d357d2f6d3c2ce05bf1a
2d636038bdfa13ee7a29548448aa8647b0f1dab7 c9e1efa1717ed5afe812739b6aae5fa0a65298c0
23f88a53cef6980776f4cbd1e41473cdce4f5dd2 2d636038bdfa13ee7a29548448aa8647b0f1dab7
2c0d5fef0206d829a3d57c319c91c9d5b58239f3 23f88a53cef6980776f4cbd1e41473cdce4f5dd2
204edfab3f20c1f9e2d980d4b5b5a454587dceba 2c0d5fef0206d829a3d57c319c91c9d5b58239f3
be2e8862525d6a599dcabca0971ff7150f21dd78 204edfab3f20c1f9e2d980d4b5b5a454587dceba
e60fada5dee6797d57acadce5809c1085861b5b7 be2e8862525d6a599dcabca0971ff7150f21dd78
f4a18b70bffe805745b8831d2288c804f4a3e4c2 e60fada5dee6797d57acadce5809c1085861b5b7
27b1fa77e0cfb5d174fa68b2580b2e6fbd58cf24 f4a18b70bffe805745b8831d2288c804f4a3e4c2
ae83a5f2b4e9fb705119ccebe7530fadd83fde1c 27b1fa77e0cfb5d174fa68b2580b2e6fbd58cf24
8fdbcb5f3ec8be2551fa4e18ccc2be7e8620b7b9 ae83a5f2b4e9fb705119ccebe7530fadd83fde1c
36a2984c420dc9382fe6fe57dc8fd070841070ac 8fdbcb5f3ec8be2551fa4e18ccc2be7e8620b7b9
a6485240b5e54a24eddb1eb0aa90c72e56c504cd 36a2984c420dc9382fe6fe57dc8fd070841070ac
e03fac61978590059aa90f61091bb3849fa7f6c7 a6485240b5e54a24eddb1eb0aa90c72e56c504cd
4a427441c0a27f58e0f31b09a3dd5f9ac11cc6d8 e03fac61978590059aa90f61091bb3849fa7f6c7
77a28982a51851389aa828538574be152cc190b1 4a427441c0a27f58e0f31b09a3dd5f9ac11cc6d8
88e3bf706a0e6e6663d4258d57e549db3cd6f0f5 77a28982a51851389aa828538574be152cc190b1
77478b9170488ca0c4ef92da33e9e7fb6c70d748 88e3bf706a0e6e6663d4258d57e549db3cd6f0f5
e15eeb60ac4cb65c7c7e20e569a2a88bc94a0047 77478b9170488ca0c4ef92da33e9e7fb6c70d748
9fb78470baf494d6d4fa7649d5b052d05a71e28a e15eeb60ac4cb65c7c7e20e569a2a88bc94a0047
281010741341339fefaf5398c9a22d67cadb5f33 9fb78470baf494d6d4fa7649d5b052d05a71e28a
b099a46162bc2f581a3e3612dd72cbb78c719063 281010741341339fefaf5398c9a22d67cadb5f33
8e86151a8cc5805eeba4d108c475eb1f9bed3196 b099a46162bc2f581a3e3612dd72cbb78c719063
812a3d7da84efebcc31046b74efc5ee97e4cdfa4 8e86151a8cc5805eeba4d108c475eb1f9bed3196
53b771c9b8aed859233ed3a0cf1f1bb428536118 812a3d7da84efebcc31046b74efc5ee97e4cdfa4
323359ba83effe3469fd4cd61d1a1a9107c650fc 53b771c9b8aed859233ed3a0cf1f1bb428536118
90ae6d086f3c6a02759376c57bb51f5863026517 323359ba83effe3469fd4cd61d1a1a9107c650fc
d3b51d4b422598a5f0504d6e93be6bcdb89f33de 90ae6d086f3c6a02759376c57bb51f5863026517
7edb2cd3da7bbbab9f6b4535f3218544797f3154 d3b51d4b422598a5f0504d6e93be6bcdb89f33de
a3670efcbdeafe138e442a7d9a04209f449c817c 7edb2cd3da7bbbab9f6b4535f3218544797f3154
e7f35197872f5b1e2f1c68ac97a4627add83110d a3670efcbdeafe138e442a7d9a04209f449c817c
1ad5f47eb14b4e177e06187decf9417d0c48dbe5 e7f35197872f5b1e2f1c68ac97a4627add83110d
623dc23f020c71c6dcc7fd3c1d2bc4f8accb3b63 1ad5f47eb14b4e177e06187decf9417d0c48dbe5
fa5fe96ba9f2fccaa16beb53202af08866d61f0a 623dc23f020c71c6dcc7fd3c1d2bc4f8accb3b63
d18588a0ba36a4bdd482d14f4a3c4b5c2fb112da fa5fe96ba9f2fccaa16beb53202af08866d61f0a
8b538c7e0acbc39fe1659d4c208373ea4eff128c d18588a0ba36a4bdd482d14f4a3c4b5c2fb112da
00a29e350e777fa6dd6aa708a744c4fc8ec4abac 8b538c7e0acbc39fe1659d4c208373ea4eff128c
a93b92e03288c14b40813373754ceda1f66631b0 00a29e350e777fa6dd6aa708a744c4fc8ec4abac
bdbedb304232b7375ac2e0c94245f2bb62bfd7aa a93b92e03288c14b40813373754ceda1f66631b0
e297cd9c162ad935df78872acd5909778e598d16 bdbedb304232b7375ac2e0c94245f2bb62bfd7aa
b766d56517a6a8abf9e85a1849b4a08e62c87ebe e297cd9c162ad935df78872acd5909778e598d16
478066b2c5d03b5159beffa4fc26376bc420b00d b766d56517a6a8abf9e85a1849b4a08e62c87ebe
ca32fb86c21f5e083f71fc49c693379800ec72c2 478066b2c5d03b5159beffa4fc26376bc420b00d
6ff8f2706d384b3aa0a57e78c897eb9428f3fc94 ca32fb86c21f5e083f71fc49c693379800ec72c2
951bb00fbdd6a89011931fd883cc868f3212b3b2 6ff8f2706d384b3aa0a57e78c897eb9428f3fc94
d7de0bd6872810df78e0162553922ad93ad7fc8e 951bb00fbdd6a89011931fd883cc868f3212b3b2
abf145930e51236fc4505af2b8ea8a7c471a27e4 d7de0bd6872810df78e0162553922ad93ad7fc8e
ec0735ad4039ef233adbd6c14166905509a363a7 abf145930e51236fc4505af2b8ea8a7c471a27e4
b71a294e8b6f00b9ca008c0ac94023f52f773469 ec0735ad4039ef233adbd6c14166905509a363a7
d821abdbb01d9ad13c9ddfe728026fbe9b8efc4a b71a294e8b6f00b9ca008c0ac94023f52f773469
07ce5bbb9994077a7e7e6a49f35194dd86dc375c d821abdbb01d9ad13c9ddfe728026fbe9b8efc4a
9bf0afac97a87f2108d79f438edd8a5b0f819a51 07ce5bbb9994077a7e7e6a49f35194dd86dc375c
9e057123197cc1cb46f682745704679664c66102 9bf0afac97a87f2108d79f438edd8a5b0f819a51
e81858032989ef3ab9327ed29790e224d0877168 9e057123197cc1cb46f682745704679664c66102
e9adb749e642abb7efaab1d42849273aaa293271 e81858032989ef3ab9327ed29790e224d0877168
985a7f27dc51a2bad897127d8b5f4924e9648b2d e9adb749e642abb7efaab1d42849273aaa293271
c4425a8a25154c1157145879d7acbc778aadd595 985a7f27dc51a2bad897127d8b5f4924e9648b2d
e48f34a875ee661a8330b43c0a6ff5b707c29181 c4425a8a25154c1157145879d7acbc778aadd595
bc0be43671c7ccc0cdece8ded3a7df289b3fcfab e48f34a875ee661a8330b43c0a6ff5b707c29181
cb333a39cf86a6ce5b5183a78d75fc1296011222 bc0be43671c7ccc0cdece8ded3a7df289b3fcfab
7a3d3c8ea3fd7039a8df8c144582ed0f5e985d4f cb333a39cf86a6ce5b5183a78d75fc1296011222
c12867a09e998366f1a44ea25002e86d898d7783 7a3d3c8ea3fd7039a8df8c144582ed0f5e985d4f
5e9668a6bccfd5913c656ba0d08e97de74d507fb c12867a09e998366f1a44ea25002e86d898d7783
34bfe26063c984a773aa55dc55fbc44f4cc3853a 5e9668a6bccfd5913c656ba0d08e97de74d507fb
0fb3355898327ced11681ef85ecf6de742e75670 34bfe26063c984a773aa55dc55fbc44f4cc3853a
f83e873fe6ce0c76bcd7eefda92367fbd8f3e56a 0fb3355898327ced11681ef85ecf6de742e75670
902575c34688eb08f12a7b5b83cf4e19b1341fe6 f83e873fe6ce0c76bcd7eefda92367fbd8f3e56a
d1d41ed0a692f5334a80487434f634d9fc60a854 902575c34688eb08f12a7b5b83cf4e19b1341fe6
86ecb046e0ce2f0d8067601fa2ac23632f759432 d1d41ed0a692f5334a80487434f634d9fc60a854
ce8417b860d9bc2602f5e42eea337effc275d08e 86ecb046e0ce2f0d8067601fa2ac23632f759432
e3b063f6fc704e5d8210412a9053a5e477cb09f1 ce8417b860d9bc2602f5e42eea337effc275d08e
0ef9daf605c11b1b9d98464735077772f5030500 e3b063f6fc704e5d8210412a9053a5e477cb09f1
7cc6457f2cef2c5c6758e10abeb8a89d2013b945 0ef9daf605c11b1b9d98464735077772f5030500
0dab82b590c18000902f9e37678002ddd2f6832b 7cc6457f2cef2c5c6758e10abeb8a89d2013b945
07713cdb48f285f1295fa4dbfd97612cd47eff1f 0dab82b590c18000902f9e37678002ddd2f6832b
18c39da388312de0bf86537f08b4f62c2e2131f6 07713cdb48f285f1295fa4dbfd97612cd47eff1f
43735b2dcfb5acd32199edfabe82df0f7e35e643 18c39da388312de0bf86537f08b4f62c2e2131f6
d80f8e2a057093a8aa0ecd2d806b96d7a4ebb159 43735b2dcfb5acd32199edfabe82df0f7e35e643
0209627e60b08ac7279be4bee0eeb76e8e678acc d80f8e2a057093a8aa0ecd2d806b96d7a4ebb159
bcdcf3c20e1c098f8ab9940be1bdadea25930010 0209627e60b08ac7279be4bee0eeb76e8e678acc
6cd242b88cd4b79231cbe7d2b6b40a8c130bf3ba bcdcf3c20e1c098f8ab9940be1bdadea25930010
1b8ffe9ea0c618af03976a778023469f339d9892 6cd242b88cd4b79231cbe7d2b6b40a8c130bf3ba
0489a2144d90a1367887cd4630016af954b87ebb 1b8ffe9ea0c618af03976a778023469f339d9892
528b5560697079390e1e56b7582fc11dcb32b778 0489a2144d90a1367887cd4630016af954b87ebb
753fd5bf168ec28987c41e0162ee20c65666ee59 528b5560697079390e1e56b7582fc11dcb32b778
840aabf34d8d542ac3012f28c45f3b7e475f9a98 753fd5bf168ec28987c41e0162ee20c65666ee59
50b72c30b2cbbf13efad87683f0dff1e468deb3e 840aabf34d8d542ac3012f28c45f3b7e475f9a98
3395ae9fae103e24c1b70653e1d504b22fa2c25f 50b72c30b2cbbf13efad87683f0dff1e468deb3e
56122a41a56cfa4ec99f87e1ed595688e6040f9a 3395ae9fae103e24c1b70653e1d504b22fa2c25f
3311c6ade36053165a57ddcea243709973551e88 56122a41a56cfa4ec99f87e1ed595688e6040f9a
69d5c227ca0e0ad16aa402ff392e4e14e7b11f15 3311c6ade36053165a57ddcea243709973551e88
6d414c0e8698afcb05d9cae1632c3800da07ee24 69d5c227ca0e0ad16aa402ff392e4e14e7b11f15
d242bcbce4f46fbf08d468880c9e29252e35ae53 6d414c0e8698afcb05d9cae1632c3800da07ee24
f84ef430f500e6c185b123d9c68668c890a7eb2c d242bcbce4f46fbf08d468880c9e29252e35ae53
dc4608efe6988f902b954f7ce5eb9a8a23883b12 f84ef430f500e6c185b123d9c68668c890a7eb2c
5ea143b23a5e9080e0005c6b76359d60da00e365 dc4608efe6988f902b954f7ce5eb9a8a23883b12
54a28a870b629432713af0fcddc4fe0e6c784f94 5ea143b23a5e9080e0005c6b76359d60da00e365
4eda05bf50d5d8264609185ec6ed3c5551705763 54a28a870b629432713af0fcddc4fe0e6c784f94
1e4a7fbfec0ff364e4e50b7887289e4b9dba6edb 4eda05bf50d5d8264609185ec6ed3c5551705763
e5a1ac80841485a9aa186c0e6a95b8d430a25b1b 1e4a7fbfec0ff364e4e50b7887289e4b9dba6edb
2e4ce0859e1eef54768acb6238faf09ae6ac1fe0 e5a1ac80841485a9aa186c0e6a95b8d430a25b1b
7e129c14a9d24f4b06ee9b04d00dee53ee999d9f 2e4ce0859e1eef54768acb6238faf09ae6ac1fe0
a06559d1e51b86546168cc4218d1a15cf937668b 7e129c14a9d24f4b06ee9b04d00dee53ee999d9f
a108f0d8b3fd7cafe9e553377ab563833d55ecd4 a06559d1e51b86546168cc4218d1a15cf937668b
7e9eee1bfc82c74c12b2f5a6d5604fb6b573ff5c a108f0d8b3fd7cafe9e553377ab563833d55ecd4
b0cf6bba4d9a498342c245b7b8a18362bc97703e 7e9eee1bfc82c74c12b2f5a6d5604fb6b573ff5c
a8ea43af6d2d69b031c9e66eb5a8fb225819744d b0cf6bba4d9a498342c245b7b8a18362bc97703e
13c53599c31d0fbb82c1339f0b1a240bb01f127f a8ea43af6d2d69b031c9e66eb5a8fb225819744d
fa27b99cf11e3483cbcf00f373b2b8691a8944fa 13c53599c31d0fbb82c1339f0b1a240bb01f127f
cca4e759c83f46f730237cdf17ed671ba2d3c5d3 fa27b99cf11e3483cbcf00f373b2b8691a8944fa
cb752bd2e9bd1da92bff0a49ece4880e5d9cbf41 cca4e759c83f46f730237cdf17ed671ba2d3c5d3
b2ea50551259a4b510e8876463ace13125839267 cb752bd2e9bd1da92bff0a49ece4880e5d9cbf41
20c9a0f91e34753c88d25647271a5b93973395d2 b2ea50551259a4b510e8876463ace13125839267
d8bd2d5812e90279095755d5e9b47e603e5106e8 20c9a0f91e34753c88d25647271a5b93973395d2
4614c70fcdff34962d6f2875aa8bc48a34cd8b5c d8bd2d5812e90279095755d5e9b47e603e5106e8
5f0477d69806e76729e9fc8526fbfaf59f1717ed 4614c70fcdff34962d6f2875aa8bc48a34cd8b5c
af9da9f7ffd0d8f74adc33571b91b861724db9f1 5f0477d69806e76729e9fc8526fbfaf59f1717ed
84b66327c607356847b4678cf05414b652211346 af9da9f7ffd0d8f74adc33571b91b861724db9f1
1bd521b43fd27b997b5f4290f7a2f8ee0eb7081c 84b66327c607356847b4678cf05414b652211346
baf931cd99bc459caefe85567433fc5a9f979bd3 1bd521b43fd27b997b5f4290f7a2f8ee0eb7081c
74a9a75b50725fdf9d645e0ba479a7fa29c05ca2 baf931cd99bc459caefe85567433fc5a9f979bd3
8950a2d838bea12d1bbd45fa8541e1aa61c69dbf 74a9a75b50725fdf9d645e0ba479a7fa29c05ca2
8ddcd5dcabdb1f4873317d40009a0f6b6a0422fd 8950a2d838bea12d1bbd45fa8541e1aa61c69dbf
2986c6455d37a421600c9693ec205bb2fdec6463 8ddcd5dcabdb1f4873317d40009a0f6b6a0422fd
26a0fdc05f32ff2df77c47ba3c9a40c26950db4b 2986c6455d37a421600c9693ec205bb2fdec6463
753265a5755df80acca0807c07e389f550407b45 26a0fdc05f32ff2df77c47ba3c9a40c26950db4b
91ed71f0afbe7ccf13e9ea7cdfe515e414df7592 753265a5755df80acca0807c07e389f550407b45
dae49b31fecf0e63fbf6219431b6993a08dc8553 91ed71f0afbe7ccf13e9ea7cdfe515e414df7592
9d5526e0c971521fa4fc54432f68236ddef3cb74 dae49b31fecf0e63fbf6219431b6993a08dc8553
531de2ccda49cf7c5dd308707563e0f705b0c527 9d5526e0c971521fa4fc54432f68236ddef3cb74
6298a11288cac7d87d35bcdd3f067e9de21266ee 531de2ccda49cf7c5dd308707563e0f705b0c527
bc77665f2ccb22b3dabfbac0349bce0a822fc796 6298a11288cac7d87d35bcdd3f067e9de21266ee
ee4903374059f5c6bf961cc70c7ea0361a3e3864 bc77665f2ccb22b3dabfbac0349bce0a822fc796
7de54dc9cd43de2bd585159fd39fa1817c99697a ee4903374059f5c6bf961cc70c7ea0361a3e3864
b26bdb17be34543a302a1017cf80cc490eef3434 7de54dc9cd43de2bd585159fd39fa1817c99697a
4e153261e6a3f5efe97e4995e39fae4b92d6087d b26bdb17be34543a302a1017cf80cc490eef3434
0ddaa99c67d3790ee66ef27f642ba3eec8aa68e9 4e153261e6a3f5efe97e4995e39fae4b92d6087d
024714913216d0f15cdd95510f6f0b34827d44e3 0ddaa99c67d3790ee66ef27f642ba3eec8aa68e9
12256702c81d7ac77b0ac51822bb42a42e032dfa 024714913216d0f15cdd95510f6f0b34827d44e3
d9d99c284ef80d7ce2704f577352e221b57c5aea 12256702c81d7ac77b0ac51822bb42a42e032dfa
3564c914a17b4e317be46fc86c7334e325c7ebd3 d9d99c284ef80d7ce2704f577352e221b57c5aea
96c90350d9bc8589e16d539b30fbbf26faa00a09 3564c914a17b4e317be46fc86c7334e325c7ebd3
56b73f1e95c6dfae09bb0c50ce68a9b6e99574ee 96c90350d9bc8589e16d539b30fbbf26faa00a09
6939d3f4ad1bced7fda382911a42c74ab873826d 56b73f1e95c6dfae09bb0c50ce68a9b6e99574ee
14ce68c88b79605ae15a0511699b6e4349b31df5 6939d3f4ad1bced7fda382911a42c74ab873826d
6ef9545902e4446174f294eaf8d0b174d7984440 14ce68c88b79605ae15a0511699b6e4349b31df5
82664748abff0dec450edc68fb9ceb9c640f98b1 6ef9545902e4446174f294eaf8d0b174d7984440
9928793a19216e5a51c0699afc74ccdff4bbd300 82664748abff0dec450edc68fb9ceb9c640f98b1
85f2aa75c7b0c2593b3f54c59246486c04b4184a 9928793a19216e5a51c0699afc74ccdff4bbd300
744b37db7013d6eadf8452abf7491bdc49c9fb44 85f2aa75c7b0c2593b3f54c59246486c04b4184a
cf694489e089af81f8c84b867a305168e3793d85 744b37db7013d6eadf8452abf7491bdc49c9fb44
4e6f17c8b9051be5b108f403aaba8c8d8893f73c cf694489e089af81f8c84b867a305168e3793d85
1a6358868f944a75fc360da865222afaf9157666 4e6f17c8b9051be5b108f403aaba8c8d8893f73c
dbae2baba1a346fd6686773f59a8d0f0d0ad0480 1a6358868f944a75fc360da865222afaf9157666
7964d31dc78f20c47c597356702024e20e7e1f1b dbae2baba1a346fd6686773f59a8d0f0d0ad0480
09a95d2af516e3219e2a7c3f314f32db657cf73e 7964d31dc78f20c47c597356702024e20e7e1f1b
9dc7761c0172b169166a2b739901322f87da9877 09a95d2af516e3219e2a7c3f314f32db657cf73e
f481717606fd6d6534a8cd020c8ce8e4e68d13c8 9dc7761c0172b169166a2b739901322f87da9877
b4ea255688026a2d87cfa2176f42186f72aaa07a f481717606fd6d6534a8cd020c8ce8e4e68d13c8
5782d4f66d9b582e84153c1133e824fd7f4b10d9 b4ea255688026a2d87cfa2176f42186f72aaa07a
be8c22d259f15edadf9bd23e9f0719b726b9a6b4 5782d4f66d9b582e84153c1133e824fd7f4b10d9
67eeae7c5f7980f15b8fa17ce0e11bdabe05e0e1 82664748abff0dec450edc68fb9ceb9c640f98b1
84275803ec19a7d697b5d36d421e1d0cb3ec5fdb 67eeae7c5f7980f15b8fa17ce0e11bdabe05e0e1 be8c22d259f15edadf9bd23e9f0719b726b9a6b4
5cf7692c95879bcb978c4d6cd6a8307240539cc3 84275803ec19a7d697b5d36d421e1d0cb3ec5fdb
e625f8dfe943d78c407dcf74926d58a024e8e5da 5cf7692c95879bcb978c4d6cd6a8307240539cc3
f3a0c2c66a1b7438665662bb31a77de874e2cb75 e625f8dfe943d78c407dcf74926d58a024e8e5da
f7b0181d52f103bc71c4a6d25cf27f9ec1109bce f3a0c2c66a1b7438665662bb31a77de874e2cb75
3a54d3c7213e2ea21f54b0a650fb7c90cd23be27 f7b0181d52f103bc71c4a6d25cf27f9ec1109bce
06daf89ea91c2f7f0d5dc6f7a21156aa720863e8 3a54d3c7213e2ea21f54b0a650fb7c90cd23be27
83543bcf769dd5141df40a98ca76480530e62d19 06daf89ea91c2f7f0d5dc6f7a21156aa720863e8
2a7ca1ac5f2c627c1ba97aa9c5aeffb382d612b8 83543bcf769dd5141df40a98ca76480530e62d19
1c5659b2054eefabd18011570ac5c9ae574019ef 2a7ca1ac5f2c627c1ba97aa9c5aeffb382d612b8
24358ae2ca7bd3cb24f4927c73e8be7c6ca2e63f 1c5659b2054eefabd18011570ac5c9ae574019ef
854d19ea2d57e622826b1768c632e38040f165bd 24358ae2ca7bd3cb24f4927c73e8be7c6ca2e63f
203271c67e2766d4b2e16a56bf2ab1f173b860bc 854d19ea2d57e622826b1768c632e38040f165bd
9d6eab7c426b76a1063903e400ed1b5fdcf9b708 203271c67e2766d4b2e16a56bf2ab1f173b860bc
117b55192b3d2112972baad210d9a7657d6c979a 9d6eab7c426b76a1063903e400ed1b5fdcf9b708
5e26e4cb3544743b9fe2adab65624583a8969964 117b55192b3d2112972baad210d9a7657d6c979a
8a746e0c1db0ad06f0177412fd8574fad87de59e 5e26e4cb3544743b9fe2adab65624583a8969964
f760f360909bfd6fc25811ca2e1fbf17c73fb9fb 8a746e0c1db0ad06f0177412fd8574fad87de59e
4f00c63ee7313e2e738111e0fb3e0eb212f3cab9 f760f360909bfd6fc25811ca2e1fbf17c73fb9fb
3e1bbd4ee7ef58c73d17c2fa460ac837cb77ea8f 4f00c63ee7313e2e738111e0fb3e0eb212f3cab9
d84b98e238a84e6f3117d7d4e7b17967710e2168 3e1bbd4ee7ef58c73d17c2fa460ac837cb77ea8f
c2c2bd223b6daa2551a9d7665396d0f88e484af4 82664748abff0dec450edc68fb9ceb9c640f98b1
0614d065db81e9fd2a0c977e92f9a485e4e64bd1 c2c2bd223b6daa2551a9d7665396d0f88e484af4 d84b98e238a84e6f3117d7d4e7b17967710e2168
7f21ac8b46e2d9edcf32deaa2da559980d67fb18 0614d065db81e9fd2a0c977e92f9a485e4e64bd1
0cbf8a740e81a82bb25f72572da6bcb8b6678f8a 7f21ac8b46e2d9edcf32deaa2da559980d67fb18
42d10dd5def7943006cee59fac37100dc7d7b0b4 0cbf8a740e81a82bb25f72572da6bcb8b6678f8a
6b1dc0755602ec3dc2a77ccf7e0f5eab511b48d7 42d10dd5def7943006cee59fac37100dc7d7b0b4
78a55c2b5958347bd7897e94a8f630a7e3318ff8 6b1dc0755602ec3dc2a77ccf7e0f5eab511b48d7
3930218238bd71ac123a621f085c2a2c2c68238a 78a55c2b5958347bd7897e94a8f630a7e3318ff8
cf895ef2f45d47bc6dfbac6a76ce02af6e9eac39 3930218238bd71ac123a621f085c2a2c2c68238a
97cea6a672825965bbd8db960253af9f8d7a3544 cf895ef2f45d47bc6dfbac6a76ce02af6e9eac39
c2a5cff79ef27484c9df9108ccafd8873f73a364 97cea6a672825965bbd8db960253af9f8d7a3544
cf1dd26c167a3cd54780b947d0aa6b1d7cd690b4 c2a5cff79ef27484c9df9108ccafd8873f73a364
82918db0d6db2747690d9f08d2b3bf46deca5149 cf1dd26c167a3cd54780b947d0aa6b1d7cd690b4
80efd3fdb7de33dabee52292b7fc4bdb8fb6a0bf 82918db0d6db2747690d9f08d2b3bf46deca5149
7f4837512c6f039bdf536a0d6a62eb79d992782b 80efd3fdb7de33dabee52292b7fc4bdb8fb6a0bf
b2ba00f6585419d44427ea0720146c35faf36678 7f4837512c6f039bdf536a0d6a62eb79d992782b
83ad29895aacce57372377c869292f57d5c4f78d b2ba00f6585419d44427ea0720146c35faf36678
a0a456ab1db9847eb5df8bb9bc1c62f2887d8eb8 83ad29895aacce57372377c869292f57d5c4f78d
62f81cd41fcbd2cb800bc0506a48f9fc641fdf4c a0a456ab1db9847eb5df8bb9bc1c62f2887d8eb8
7692ce1b1c5f6384d0154e67dcc6752d164f3471 62f81cd41fcbd2cb800bc0506a48f9fc641fdf4c
976aa9b089b610ef738cc89c411febbd8322fdd6 7692ce1b1c5f6384d0154e67dcc6752d164f3471
73f32c2dd94d81bf06730ec53387c3860933f149 82664748abff0dec450edc68fb9ceb9c640f98b1
cc80ab6967ac0a387487ce51a03ae29f5a5d2cdd 73f32c2dd94d81bf06730ec53387c3860933f149 976aa9b089b610ef738cc89c411febbd8322fdd6
f8fd6337298c1d691b09387e490ff520f68e8959 cc80ab6967ac0a387487ce51a03ae29f5a5d2cdd
86d244f3cb6e388748463bfee18f311ab1af1488 f8fd6337298c1d691b09387e490ff520f68e8959
d21c2b59c0efdbb6c132a104649b45e703e7c34a 86d244f3cb6e388748463bfee18f311ab1af1488
7a7cd04d6df69503df0f963fec189b51bb84ad23 d21c2b59c0efdbb6c132a104649b45e703e7c34a
b197e3ac6294cb8439c333407275a5e17bc76951 7a7cd04d6df69503df0f963fec189b51bb84ad23
24d66a31c6a3f70f1f6c8a6bf8b512c6d616fa71 b197e3ac6294cb8439c333407275a5e17bc76951
fe3444c3fd749c30351e01662c3087540489281e 24d66a31c6a3f70f1f6c8a6bf8b512c6d616fa71
751857a80ed9e9770a33aeb13e860911d18597e8 fe3444c3fd749c30351e01662c3087540489281e
af6cc0b9037d5152b330e9213f4b007781dd2ee6 751857a80ed9e9770a33aeb13e860911d18597e8
ec3605f025c3aa3a72290dd9220c9a38434a0c6b af6cc0b9037d5152b330e9213f4b007781dd2ee6
6cf9b941980e35a77b6645c00370ba12a4cc35ff ec3605f025c3aa3a72290dd9220c9a38434a0c6b
3011a14858bfde67364730ff5dfbad3744d313da 6cf9b941980e35a77b6645c00370ba12a4cc35ff
c82e915e2b837baa985e76aac3bc8914c5e4990d 3011a14858bfde67364730ff5dfbad3744d313da
38aa37413713b788ef732e1ea25b5c2cc1f22e56 c82e915e2b837baa985e76aac3bc8914c5e4990d
1536134233888083af29cf00a2066e12179a87fa 38aa37413713b788ef732e1ea25b5c2cc1f22e56
13d4e510cdd88c71a7f0fdb421b10e9eb5a3b3ce 1536134233888083af29cf00a2066e12179a87fa
eb747633c20bb1088bb7bf1bcdcd1b5a1a13d8c4 13d4e510cdd88c71a7f0fdb421b10e9eb5a3b3ce
fdfbc94971c9751c2d40f4e438529df0719ca67c eb747633c20bb1088bb7bf1bcdcd1b5a1a13d8c4
5a650d30c65aeda18b33ead07e501a501636b603 fdfbc94971c9751c2d40f4e438529df0719ca67c
28ab6cd94d7d5b8fd4a2edb0132ae0c9e11619ba 5a650d30c65aeda18b33ead07e501a501636b603
35130d3c1e1ccaaf1bb3a9dc419a526349d29286 82664748abff0dec450edc68fb9ceb9c640f98b1
867c8c75caafe70ff198181135127657e26ea46e 35130d3c1e1ccaaf1bb3a9dc419a526349d29286 28ab6cd94d7d5b8fd4a2edb0132ae0c9e11619ba
b7bc59121b58ed8d7835798631ba4f140f506c9d 867c8c75caafe70ff198181135127657e26ea46e
1f6779c5258b3e48f0f4e3ea1e916d1697c7db34 b7bc59121b58ed8d7835798631ba4f140f506c9d
b8e0505c2e09b219e2154147a17d1da0c3f631de 1f6779c5258b3e48f0f4e3ea1e916d1697c7db34
db501e69ea0ae5716ae93806ce53d24c4295b40f b8e0505c2e09b219e2154147a17d1da0c3f631de
a988bf21523c7b547025a29ca530acf60ba3c2f9 db501e69ea0ae5716ae93806ce53d24c4295b40f
fc9e7345a716f6f6ed83780d111c190fd0d276cd a988bf21523c7b547025a29ca530acf60ba3c2f9
fb2864f88078cb662513da26724c60b1a62f188f fc9e7345a716f6f6ed83780d111c190fd0d276cd
ae2806c585aa26b2b12ab293e988de0caafb7407 fb2864f88078cb662513da26724c60b1a62f188f
6c7cd0a42729eca2abedb5ca50b881cf5b512a43 ae2806c585aa26b2b12ab293e988de0caafb7407
aa7022fbc525731aebf949ba97d6a712df67efbf 6c7cd0a42729eca2abedb5ca50b881cf5b512a43
ba9a89f21dfee60b31fd9ab1b8a753d909b0da02 aa7022fbc525731aebf949ba97d6a712df67efbf
846589ff03afea8abec9a30e7b6fca3b5578df18 ba9a89f21dfee60b31fd9ab1b8a753d909b0da02
a4d9a408065ba8058d37e0d0b9f72bc1d802c8bd 846589ff03afea8abec9a30e7b6fca3b5578df18
63ded8c029b67486a11d87874f0c9c4927661c98 a4d9a408065ba8058d37e0d0b9f72bc1d802c8bd
5b030298b6d9dba7b34cff5f3c468a8609e10943 63ded8c029b67486a11d87874f0c9c4927661c98
4623102dc4e4a17beab5c23762413b1307aba762 5b030298b6d9dba7b34cff5f3c468a8609e10943
0475e11088d4e01b57669eb3dac7ef1cab7ca5d7 4623102dc4e4a17beab5c23762413b1307aba762
11ecaab92fd91ecc05e886d29b2bf4ee0dc4b84e 82664748abff0dec450edc68fb9ceb9c640f98b1
034a1199c0f0c2739da51fcf2dcf073cf2de41e4 11ecaab92fd91ecc05e886d29b2bf4ee0dc4b84e 0475e11088d4e01b57669eb3dac7ef1cab7ca5d7
fe81b0ff2dfc4c2160ae9395fd8c2a32cb616231 034a1199c0f0c2739da51fcf2dcf073cf2de41e4
2338884d475326f922f06c9d95c242a233eb01e6 fe81b0ff2dfc4c2160ae9395fd8c2a32cb616231
cc3d7e8ef2fd9d74105ee5b51dd7d0362fd3267f 2338884d475326f922f06c9d95c242a233eb01e6
20bd2478485790333f390a2af6102bf038e7dba1 cc3d7e8ef2fd9d74105ee5b51dd7d0362fd3267f
fafbe02eb333799348c2c9a64e169f7f0e495e49 20bd2478485790333f390a2af6102bf038e7dba1
fe8b7e333aba9aaa37cc39a42e016b06ba0df1b3 fafbe02eb333799348c2c9a64e169f7f0e495e49
77036e799c508350e72619904d3feb90152b30aa fe8b7e333aba9aaa37cc39a42e016b06ba0df1b3
5eacc0ef0b5441616521b9bc46d3e9c53c6887a4 77036e799c508350e72619904d3feb90152b30aa
256ef564a273732527ae9b90b25f102df305c8df 5eacc0ef0b5441616521b9bc46d3e9c53c6887a4
21ff9d0bbc4c0d844665a956d7a0cb5e9177d2d0 256ef564a273732527ae9b90b25f102df305c8df
821f5cebf32b07924eea3ccbc84ffc1e7a13c879 21ff9d0bbc4c0d844665a956d7a0cb5e9177d2d0
a37ccb639c0431059bf3076bd2516e16685f67a0 821f5cebf32b07924eea3ccbc84ffc1e7a13c879
ea8a44d0c5c1d67b9e1157e905dc9f387c1b4387 a37ccb639c0431059bf3076bd2516e16685f67a0
fdaae7ba99321a5ce489fd15dca2e52efac2c31f ea8a44d0c5c1d67b9e1157e905dc9f387c1b4387
6b4d6dd9736adc9e84bd12b4b222bb6a1905cf2d 82664748abff0dec450edc68fb9ceb9c640f98b1
33ea2b0e957ff59f9638b0ec1eee0c3725ee34d1 6b4d6dd9736adc9e84bd12b4b222bb6a1905cf2d fdaae7ba99321a5ce489fd15dca2e52efac2c31f
d5b3639a8cf875bfc899469214739dd0323fc857 33ea2b0e957ff59f9638b0ec1eee0c3725ee34d1
bcf0b85e2501d4f4e8012bd711876d8360531cab d5b3639a8cf875bfc899469214739dd0323fc857
0ae7239680fa33be112c8f688c1a27cd1ed01382 bcf0b85e2501d4f4e8012bd711876d8360531cab
a14c4e8f524e7885c67bd1dcbbe143c9772944d0 0ae7239680fa33be112c8f688c1a27cd1ed01382
88e75653c9ca42502726f7edf681925cf3b82fa2 a14c4e8f524e7885c67bd1dcbbe143c9772944d0
18bbeb28e2c2281d7d276e5f5346e246618f28a8 88e75653c9ca42502726f7edf681925cf3b82fa2
e6d79b94bd82ad035deedeab33258d29609605ad 18bbeb28e2c2281d7d276e5f5346e246618f28a8
35a5073071f1ee87a92906685f38d077800da287 e6d79b94bd82ad035deedeab33258d29609605ad
918975b15b2e56e4370a926b3aad3281a7fc9059 35a5073071f1ee87a92906685f38d077800da287
30bd307659fa0ee0bd7f0c6c3bafa848e1c25d40 918975b15b2e56e4370a926b3aad3281a7fc9059
f26cdc1d3ea9c1922c145aa9e1e1cd07da11cb29 30bd307659fa0ee0bd7f0c6c3bafa848e1c25d40
277c4049486ba050e356d8a58ad00097bcc3ec10 82664748abff0dec450edc68fb9ceb9c640f98b1
279559ba73981f1bcc24681890e322af54f0164e 277c4049486ba050e356d8a58ad00097bcc3ec10 f26cdc1d3ea9c1922c145aa9e1e1cd07da11cb29
4a6e8115d16140b74b777169e739e1e5df2fc960 279559ba73981f1bcc24681890e322af54f0164e
12eafe9a0459241c4bedfe921f41d422206b76be 4a6e8115d16140b74b777169e739e1e5df2fc960
8a42fe26e282cdd5ca3ab58aee2a4a29d3b7ff7b 12eafe9a0459241c4bedfe921f41d422206b76be
78c5b2d6f87c5cfcff8ebaaea8537e1f09a341a0 8a42fe26e282cdd5ca3ab58aee2a4a29d3b7ff7b
d37317052f9153576ba9497067c3ffa165babd00 78c5b2d6f87c5cfcff8ebaaea8537e1f09a341a0
d5e6ca81471fd4d986146ef65137eb64547542fe d37317052f9153576ba9497067c3ffa165babd00
fa74711c60a64f3c166966556024dedabbee3868 d5e6ca81471fd4d986146ef65137eb64547542fe
35f8ac4430e70b5ea027e228c063d224b7e75dc6 fa74711c60a64f3c166966556024dedabbee3868
29928aa0695eea0a25db79df36fe13ca60baada6 35f8ac4430e70b5ea027e228c063d224b7e75dc6
50cdb3b4b2499c4f6819aab87374ced7f3f534b1 29928aa0695eea0a25db79df36fe13ca60baada6
acd92da0820ab5dbd43b289f4b92fe5601656511 50cdb3b4b2499c4f6819aab87374ced7f3f534b1
fee2721edb8b430068a9d0aea796d3668a538cf1 acd92da0820ab5dbd43b289f4b92fe5601656511
d5c38247542b854cd2e970800e2463424233b588 fee2721edb8b430068a9d0aea796d3668a538cf1
dcafb222081dfef6686275fb32d8c7ffa0c60d59 d5c38247542b854cd2e970800e2463424233b588
81f954871cc39967f239f3296c7471235487a6cd dcafb222081dfef6686275fb32d8c7ffa0c60d59
42c4d418bdd9cb56785cffee4b5abc0221c2974b 81f954871cc39967f239f3296c7471235487a6cd
7963bbc4ac90fcd31cdaee9f1efeb80e441cd5df 82664748abff0dec450edc68fb9ceb9c640f98b1
657fcfbabf9123161f4ca3f5a84ebc6b44ea3d3e 7963bbc4ac90fcd31cdaee9f1efeb80e441cd5df 42c4d418bdd9cb56785cffee4b5abc0221c2974b
a6c4f1e615f883e9c096edf2cd3d4b85d5e972d4 657fcfbabf9123161f4ca3f5a84ebc6b44ea3d3e
f1298dbc3d6b275630135cd4a43e4f0429ece562 a6c4f1e615f883e9c096edf2cd3d4b85d5e972d4
29580a694912a4f870a3b50540c6d4505c55438c f1298dbc3d6b275630135cd4a43e4f0429ece562
fc4773b657b22d9d3f3ba382c42a5108c3ed6bcf 29580a694912a4f870a3b50540c6d4505c55438c
98a7a332776830341fb156269457a21c54e63c9b fc4773b657b22d9d3f3ba382c42a5108c3ed6bcf
2bba76b410573ae943e1e5d2b74c4252ba76cee5 98a7a332776830341fb156269457a21c54e63c9b
c9a1fdd8589335f4684bb4c247fa2097ad5cc025 2bba76b410573ae943e1e5d2b74c4252ba76cee5
447f82710e97e548dabe13985bdcc31d77d765da c9a1fdd8589335f4684bb4c247fa2097ad5cc025
8a02010448c338afc7f3b59e999ad4cc9dae1a3b 447f82710e97e548dabe13985bdcc31d77d765da
49ecfb37443f34d03271811db334669ff683c2cc 82664748abff0dec450edc68fb9ceb9c640f98b1
37dd61e7999d1810e8b211de384d0a205a3132df 49ecfb37443f34d03271811db334669ff683c2cc 8a02010448c338afc7f3b59e999ad4cc9dae1a3b
423fb90c17cb914767692f55df40b6c238fd56bb 37dd61e7999d1810e8b211de384d0a205a3132df
b7bb6c5f01a5d687afbff95931138f4d8dd9769c 423fb90c17cb914767692f55df40b6c238fd56bb
627203c0d4613f1506e8a6f391e94fb260df8e55 b7bb6c5f01a5d687afbff95931138f4d8dd9769c
aee95a66145381395a8570b9d7835f9bd62cc22e 627203c0d4613f1506e8a6f391e94fb260df8e55
2b42d46ab3053cd81610dfda9167b56fa444cefa aee95a66145381395a8570b9d7835f9bd62cc22e
3b3a46af17b2175f2b387cb47868bd9d703903da 2b42d46ab3053cd81610dfda9167b56fa444cefa
bd02322d9f41eae05a73548186c27cabf8194be3 3b3a46af17b2175f2b387cb47868bd9d703903da
32b1ec8683aad4a6ac4e1487a92d484f4ee3465c bd02322d9f41eae05a73548186c27cabf8194be3
bbcb92724a911326b7d9ec91b04e098f178fc186 32b1ec8683aad4a6ac4e1487a92d484f4ee3465c
c5797cc7cdb75594d866807694983aee17da6295 bbcb92724a911326b7d9ec91b04e098f178fc186
46b48f4348142b3e75a84b2f790f34a86b53c2d4 c5797cc7cdb75594d866807694983aee17da6295
9669eec43107ec7bef1a5b48d5e4f057d44c6794 46b48f4348142b3e75a84b2f790f34a86b53c2d4
90186313a010fbb58e8ff87ce436d44cfa8ad559 9669eec43107ec7bef1a5b48d5e4f057d44c6794
0b971192d8377c05a9800954c5b3eeff3e2d0223 90186313a010fbb58e8ff87ce436d44cfa8ad559
71b8ce88b5e5471d9856d32d791f7ac2508a10ed 0b971192d8377c05a9800954c5b3eeff3e2d0223
db15fdc982db43f30d738bc88e6cd990d40bd358 71b8ce88b5e5471d9856d32d791f7ac2508a10ed
558933769f134abbacaae32376db7acbd4952ff5 db15fdc982db43f30d738bc88e6cd990d40bd358
647b65bf2afcbcd7d9413e8e4e5522831cff2b76 558933769f134abbacaae32376db7acbd4952ff5
a5e2a3339a93cfd836dc63e777df300a4456eff4 647b65bf2afcbcd7d9413e8e4e5522831cff2b76
88392888caff0765afdca655c00134bc471c9543 a5e2a3339a93cfd836dc63e777df300a4456eff4
78633a5cc2161e8247554e5c81440a25d0a38737 88392888caff0765afdca655c00134bc471c9543
f27c83ebb1f9d9bdd8d6e71843de9e5354542669 78633a5cc2161e8247554e5c81440a25d0a38737
1f1d495b50a94352e0b0b13d833d1a58aa19f3b3 f27c83ebb1f9d9bdd8d6e71843de9e5354542669
9253e14a08d7f8a23be76b773cfeae1cc387e276 1f1d495b50a94352e0b0b13d833d1a58aa19f3b3
92628233a7b7c37d2ad77c528976e5d5c4d23351 9253e14a08d7f8a23be76b773cfeae1cc387e276
ce061e49b1bd661acebee80e050c136189c41cbd 92628233a7b7c37d2ad77c528976e5d5c4d23351
d681179efa80d0aa8cd28b59bffee10071aa8060 ce061e49b1bd661acebee80e050c136189c41cbd
cba447a51420814874955ff528c69306cf545bb3 d681179efa80d0aa8cd28b59bffee10071aa8060
6508ad09acc1b420050b0c7b50221c52c42b92d9 cba447a51420814874955ff528c69306cf545bb3
3993ff34be43995be564dfa7da925480535f676d 6508ad09acc1b420050b0c7b50221c52c42b92d9
ee1a767cc414daaac8aac5ccff4861f797245d30 3993ff34be43995be564dfa7da925480535f676d
4213d112ff524988bc666000ef1f4f716b5a9269 ee1a767cc414daaac8aac5ccff4861f797245d30
1883c8a15aabfc81d07ace071a3284fbf2531d81 4213d112ff524988bc666000ef1f4f716b5a9269
974792307c0cd2a736fca8edfa1befa8d347c556 1883c8a15aabfc81d07ace071a3284fbf2531d81
1d5760067fa1ba734420b7c0cc5dff0e22b7f881 974792307c0cd2a736fca8edfa1befa8d347c556
f4cd8c42d60f825c5c95beb41dd115d979dd5889 1d5760067fa1ba734420b7c0cc5dff0e22b7f881
b063f0db3828c39408253b59d0134b29b23508f4 f4cd8c42d60f825c5c95beb41dd115d979dd5889
08fec0268c6aa2503f92de6e498ddcee5ff89aa6 b063f0db3828c39408253b59d0134b29b23508f4
5a8018214448829d60f4a26a9ff57ac10ba9de3d 08fec0268c6aa2503f92de6e498ddcee5ff89aa6
45cbbe043526faf669d10f8bbce1c5ed18c5c872 5a8018214448829d60f4a26a9ff57ac10ba9de3d
9e2b374e71533f96917b05e6ed6ef6123e06bad1 45cbbe043526faf669d10f8bbce1c5ed18c5c872
840e47017d6d85398068bb7228eae21992cf35c0 9e2b374e71533f96917b05e6ed6ef6123e06bad1
3184b1288ca648c4be379860aeeb3563b9890542 840e47017d6d85398068bb7228eae21992cf35c0
dc37c376e36aa634ff45f8199e6f573a62b06bfe 3184b1288ca648c4be379860aeeb3563b9890542
d7143bf31ea1f2051647a9f5387b44fa32140a14 dc37c376e36aa634ff45f8199e6f573a62b06bfe
5587cf766ac08e66d301549d35ecc8d03b86477a d7143bf31ea1f2051647a9f5387b44fa32140a14
270cda530bed453a7004cb2c412f89e26f105b8e 5587cf766ac08e66d301549d35ecc8d03b86477a
c93be199efe6e2a1f558687e2fc38fe4d85fdf35 270cda530bed453a7004cb2c412f89e26f105b8e
f7d6b5206e81b9b52428c49349ed214f942ec916 c93be199efe6e2a1f558687e2fc38fe4d85fdf35
3104e2a1ac21af020d9a05fad450680c03df7139 f7d6b5206e81b9b52428c49349ed214f942ec916
824ad49448c9366c33ef19182cdd96342a1ced78 3104e2a1ac21af020d9a05fad450680c03df7139
4303bca22c38ef4fc9fac62a181144c0acbed452 824ad49448c9366c33ef19182cdd96342a1ced78
5a86a830fa2d8ccabe963756d7356436acaa95d6 4303bca22c38ef4fc9fac62a181144c0acbed452
7d15393a138f8ca98bb3ac37b56a9136bb4be9bf 5a86a830fa2d8ccabe963756d7356436acaa95d6
93127723ee94087a4e365d62220050231a772f3e 7d15393a138f8ca98bb3ac37b56a9136bb4be9bf
fec7620664cdafd819024fb7ed8a66ad1b9d4b1c 93127723ee94087a4e365d62220050231a772f3e
49b4419a488f7ab1e73aeec75e00285f9793dda1 fec7620664cdafd819024fb7ed8a66ad1b9d4b1c
af72efe3e204dd2102346f1a4945766b462319c6 49b4419a488f7ab1e73aeec75e00285f9793dda1
ffce2b1a2efc665486f709919683309f7c84ba3e af72efe3e204dd2102346f1a4945766b462319c6
94c801ac15ad7c4058b1beba5eff2b52657bc534 ffce2b1a2efc665486f709919683309f7c84ba3e
fb254c1832e885f64d337b7e676c3e3ddbf2b597 94c801ac15ad7c4058b1beba5eff2b52657bc534
a13f75041c8f0cd93028ac590ca07d0b2e224195 fb254c1832e885f64d337b7e676c3e3ddbf2b597
744e036dc365ee1733d136fc813259875a944e20 a13f75041c8f0cd93028ac590ca07d0b2e224195
ee15ae441cd546d020a328e62a338e4355200afb 744e036dc365ee1733d136fc813259875a944e20
ea4047752e5c214a4201eb23fa6ddc62043d1167 ee15ae441cd546d020a328e62a338e4355200afb
4f89df3b97b8b95c28071086ada8bb6a098e7d3e ea4047752e5c214a4201eb23fa6ddc62043d1167
2366b55f1091cebac4695425a355dab5b1a19008 4f89df3b97b8b95c28071086ada8bb6a098e7d3e
934466fdcba67691dd4459a32bb0d84d8115535c 2366b55f1091cebac4695425a355dab5b1a19008
e86b98ac790492be3b71958a024cb73303ae832f 934466fdcba67691dd4459a32bb0d84d8115535c
83ecbd3d4084d00ccb5a0c650b1815c8855b8b61 e86b98ac790492be3b71958a024cb73303ae832f
e94a61dd0b71e8f87e60ac298d9bfb301cdc1147 83ecbd3d4084d00ccb5a0c650b1815c8855b8b61
fdfda2674d64d532485633df3ac3b8cefd1101a0 e94a61dd0b71e8f87e60ac298d9bfb301cdc1147
9a518cd5d35671e6fdc60794c0a6826d80d4e5ac fdfda2674d64d532485633df3ac3b8cefd1101a0
8460600e1f44bef8f6a094bc14f46b730bfe47c8 9a518cd5d35671e6fdc60794c0a6826d80d4e5ac
e7101209ae2c58a577ca75ddf2c91ae2c0504f61 8460600e1f44bef8f6a094bc14f46b730bfe47c8
ee31041eb00a1925ea11fd68b78afe239d54edfc e7101209ae2c58a577ca75ddf2c91ae2c0504f61
35b09def738bc434627f444304344432dcda4c3c ee31041eb00a1925ea11fd68b78afe239d54edfc
c50e353080716c4f3243034111c188b639d3821f 35b09def738bc434627f444304344432dcda4c3c
f0fbd42c8e6c6515d3d3fa83538c89b8175aaa5b c50e353080716c4f3243034111c188b639d3821f
fa56d25defb428e404aff89818b704d676ed8b76 f0fbd42c8e6c6515d3d3fa83538c89b8175aaa5b
78bfa099e2937fbf1a060f53bb4c9889ff5cee10 fa56d25defb428e404aff89818b704d676ed8b76
3e6c8132be41bc24a361f177a3eb225e226942c7 78bfa099e2937fbf1a060f53bb4c9889ff5cee10
a07c115cb672f280a40a2e35d56b78fd52743101 3e6c8132be41bc24a361f177a3eb225e226942c7
752ce84a6f34851d995c8fa7bac69f90cb2317c2 a07c115cb672f280a40a2e35d56b78fd52743101
d9de57bed2e6149938a1eb5cd9365a8a250d40f1 752ce84a6f34851d995c8fa7bac69f90cb2317c2
f3efee2719f8c16561c63a2acaa0be6c5753633e d9de57bed2e6149938a1eb5cd9365a8a250d40f1
202b36e454bbee592bfae9a20226f67d0d4fbbae f3efee2719f8c16561c63a2acaa0be6c5753633e
9af8f1d59feafdd7f51762f43775000f1272fa33 202b36e454bbee592bfae9a20226f67d0d4fbbae
0ae6246d1a070297022e751aa2a06c4c933d082e 9af8f1d59feafdd7f51762f43775000f1272fa33
11d22bde8738171fc41cdb9c253cf203e968be2c 0ae6246d1a070297022e751aa2a06c4c933d082e
2f3312496849e8a218a159fc3be18ed3b3deebc7 11d22bde8738171fc41cdb9c253cf203e968be2c
9d963f59e52ac8c925cb38ba7a09fa978221a1e8 2f3312496849e8a218a159fc3be18ed3b3deebc7
a016496a3514193b94ba4b3ffc9c25b59417c944 9d963f59e52ac8c925cb38ba7a09fa978221a1e8
c526b495f1bd362037d2eb229430e690972ec2eb a016496a3514193b94ba4b3ffc9c25b59417c944
6e66f8ba379dfbb86787cdbc84c377fef1de3066 c526b495f1bd362037d2eb229430e690972ec2eb
ece5dd000f541d96fffeb55d71b030d0657ab8d9 6e66f8ba379dfbb86787cdbc84c377fef1de3066
596edd29d7634d1e19534df56b6cc9a51fe1804e ece5dd000f541d96fffeb55d71b030d0657ab8d9
17198f6c6e1f38d78736e71986469a00e32b1137 596edd29d7634d1e19534df56b6cc9a51fe1804e
915467e84d1229140efaa8617bcd11cea238b5e7 17198f6c6e1f38d78736e71986469a00e32b1137
d90b16eecc9c54c8bf387e315af79b589cbf02ee 915467e84d1229140efaa8617bcd11cea238b5e7
45fa599bb0c446a8cc24bcdf79ec5f8999ef050e d90b16eecc9c54c8bf387e315af79b589cbf02ee
1ae92548fad552810cc857ad76d65c7aaba7d461 45fa599bb0c446a8cc24bcdf79ec5f8999ef050e
c05d12a0a10e6ced3792295d6ee141dbc9e4d320 1ae92548fad552810cc857ad76d65c7aaba7d461
4d253b523a0d2f0f8c3f7a6032c19ee9b578e251 c05d12a0a10e6ced3792295d6ee141dbc9e4d320
4ff066783f24882e9efc3bc1f95201206176f070 4d253b523a0d2f0f8c3f7a6032c19ee9b578e251
a8a8dacfd5ba7dff655ffd1f54eefce1afe99efc 4ff066783f24882e9efc3bc1f95201206176f070
df306557e4b228731b13280ab89ebfa140fed965 a8a8dacfd5ba7dff655ffd1f54eefce1afe99efc
a5f55a0ff44f398836ce66015aab67e214200835 df306557e4b228731b13280ab89ebfa140fed965
4df72dda6f672eb440eac994365f902606442d58 a5f55a0ff44f398836ce66015aab67e214200835
e3095e78e393208ad71b75be9c5d8ea1067b8db8 4df72dda6f672eb440eac994365f902606442d58
634f06a977d8d0379d2fb915765c20c287fbf166 e3095e78e393208ad71b75be9c5d8ea1067b8db8
254172c25055496f3c3217629f2a073317efe47b 634f06a977d8d0379d2fb915765c20c287fbf166
d6c3e80a6eecb3288b5846d1824bd7e86711ef82 254172c25055496f3c3217629f2a073317efe47b
d6e5d1540727c206d614b1bf1fbf5ee423aa3b29 d6c3e80a6eecb3288b5846d1824bd7e86711ef82
63427287d46d3603c3f055ce5387432c65e0956f d6e5d1540727c206d614b1bf1fbf5ee423aa3b29
3ca75e3b96d3c9783075f0ab5453fbe6e190e89a 63427287d46d3603c3f055ce5387432c65e0956f
fbbee74004a8f98f0d1000e515649e1aa7b136d7 3ca75e3b96d3c9783075f0ab5453fbe6e190e89a
4db1b1286761e2865fe0da4d2177627ed28b7b3b fbbee74004a8f98f0d1000e515649e1aa7b136d7
4db59bc230c6e51ed0f789c3e31d66b2177a8e89 4db1b1286761e2865fe0da4d2177627ed28b7b3b
e467a468d4c9a98cacfa7c34dc903468e233d543 4db59bc230c6e51ed0f789c3e31d66b2177a8e89
8effdabe9468017276b79208643c9222c1254500 e467a468d4c9a98cacfa7c34dc903468e233d543
08c8fdc2b59dde9fd4594218b45986ef2407131b 8effdabe9468017276b79208643c9222c1254500
79d00a8b1f8c36968b330539bd172bd8cf0fca22 08c8fdc2b59dde9fd4594218b45986ef2407131b
620b575e5b15754d127a2974db5f98d1f05df0ec 79d00a8b1f8c36968b330539bd172bd8cf0fca22
a8987f37900045e68af46e5aa24f8c359b849435 620b575e5b15754d127a2974db5f98d1f05df0ec
090cdefc7a0cd61080b866fe065a5a9e1c03079e a8987f37900045e68af46e5aa24f8c359b849435
9664f3dcde6c862673feea1cbe7346d9907f0bd9 090cdefc7a0cd61080b866fe065a5a9e1c03079e
42a265d1d7a4fc54dc51b778472fef9fb88c4da8 9664f3dcde6c862673feea1cbe7346d9907f0bd9
c3f0b094db40a0f36bb97daac7e97500a2a4f1ac 42a265d1d7a4fc54dc51b778472fef9fb88c4da8
dfdf80d5a7194aa1003516dd529f6d677898d7e8 c3f0b094db40a0f36bb97daac7e97500a2a4f1ac
98e06da317c8ac9388360e870ea08c403d9e85fe dfdf80d5a7194aa1003516dd529f6d677898d7e8
f125ce3c06bd58444aecae907cc3ec0dbbe9fcb7 98e06da317c8ac9388360e870ea08c403d9e85fe
fe10bf3f72185592296fb87ece7fd0ff9fdded62 f125ce3c06bd58444aecae907cc3ec0dbbe9fcb7
b21646a8ab8839c4d7e32ccd3d3287aed68114f1 fe10bf3f72185592296fb87ece7fd0ff9fdded62
4b0be6c622ab8502f35ae3b3dcdbbacf6d458e32 b21646a8ab8839c4d7e32ccd3d3287aed68114f1
763e3b698a69c05e1cc9474555971fd55305cb76 4b0be6c622ab8502f35ae3b3dcdbbacf6d458e32
3435de038e2c5c107609fe2ebcc56f9e7aa797fd 763e3b698a69c05e1cc9474555971fd55305cb76
c37cb942283371bbc95483244ff47607707f7a37 3435de038e2c5c107609fe2ebcc56f9e7aa797fd
105da9a86ac15138dbd8239654951179b032c238 c37cb942283371bbc95483244ff47607707f7a37
2b4766ddee24d919a8772957a30936316b244769 105da9a86ac15138dbd8239654951179b032c238
184ca43d71a94151dad786f3e13f1998ac7a6e18 2b4766ddee24d919a8772957a30936316b244769
61a4110ab69c953ee0f037d530f3d81374b85060 184ca43d71a94151dad786f3e13f1998ac7a6e18
5679b34f66c4f75cc1f6ee9e7882630d1453f9cc 61a4110ab69c953ee0f037d530f3d81374b85060
e04d086e423c22f73fdc1574589ccb2478788ce8 5679b34f66c4f75cc1f6ee9e7882630d1453f9cc
1e2d9465f5b9b8be97ecb6ecbed3aaf731d1479d e04d086e423c22f73fdc1574589ccb2478788ce8
c22acca23f6242d89ec31ee701878b1450fc0a84 1e2d9465f5b9b8be97ecb6ecbed3aaf731d1479d
d0398932264cd5449d1c6e36196154516b715056 c22acca23f6242d89ec31ee701878b1450fc0a84
b65b4925a7b378d29c1bec5476876e29692dfeec d0398932264cd5449d1c6e36196154516b715056
24a5a9bc203f08446de01e6e108a6e5bcf348d13 b65b4925a7b378d29c1bec5476876e29692dfeec
b7e9243be7a5a68e9be328e09760a0f535e2eeef 24a5a9bc203f08446de01e6e108a6e5bcf348d13
ab4f49b2668c68719988b50105160fcb3e23f71b b7e9243be7a5a68e9be328e09760a0f535e2eeef
4a0604973f9e9aeda0a29f3e64ac1d8d6acf9ae6 ab4f49b2668c68719988b50105160fcb3e23f71b
e4a29e087c5b3f006b7d1d21fa0871abdd6792e5 4a0604973f9e9aeda0a29f3e64ac1d8d6acf9ae6
d428189cedf05a71877a7907318e5f08b9a25e16 e4a29e087c5b3f006b7d1d21fa0871abdd6792e5
7a6bdfb9f68e6c74af126ce7003930b6822b0403 d428189cedf05a71877a7907318e5f08b9a25e16
681d27416e80cbf176b1cded4f41a4ab270943f9 7a6bdfb9f68e6c74af126ce7003930b6822b0403
1baaedf116b037e8c88922e970f365a194368ecc 681d27416e80cbf176b1cded4f41a4ab270943f9
efb988d0e5bc5a7a384d64f36446aa04db39974b 1baaedf116b037e8c88922e970f365a194368ecc
6c5093a53a8d1701ebcdfa351de1b7c5d534f52a efb988d0e5bc5a7a384d64f36446aa04db39974b
078c66b32d189c88c275a61a4553fbaa6b0c3672 6c5093a53a8d1701ebcdfa351de1b7c5d534f52a
ebe6dff814cd385b03f574df45d4ad901972c770 078c66b32d189c88c275a61a4553fbaa6b0c3672
d6cfcca5fa37b302324fd01b7899ba4efbcd7416 ebe6dff814cd385b03f574df45d4ad901972c770
f7b57cb38acfe967eb334f39fda8a87337d2a372 d6cfcca5fa37b302324fd01b7899ba4efbcd7416
0f1c830ecee31ad9b75d0fd5623cfcf22ebf3a55 f7b57cb38acfe967eb334f39fda8a87337d2a372
56a34891755e57a3397df0fab320efc8ef0bc847 0f1c830ecee31ad9b75d0fd5623cfcf22ebf3a55
b8c55a456ae251fbe5e896be395e05125c8935dd 56a34891755e57a3397df0fab320efc8ef0bc847
0aefb410de834bdcd49de7ba9453d67125c7c629 b8c55a456ae251fbe5e896be395e05125c8935dd
dfd4087ce1453ca8f7768fe31e8dc87a9cfa2faf 0aefb410de834bdcd49de7ba9453d67125c7c629
b299b938122104efe47fffdbd19d0653d4fb1467 dfd4087ce1453ca8f7768fe31e8dc87a9cfa2faf
ec14339188ab234b5657c483755a66c9b768642e b299b938122104efe47fffdbd19d0653d4fb1467
c651343afa72d2831370ccf3dc31ff8f3688d23a ec14339188ab234b5657c483755a66c9b768642e
c79a793a21b5d65006f72d64148cc429e61b2b3d c651343afa72d2831370ccf3dc31ff8f3688d23a
35ec1ca3826712e168a040d107159a60665f7de1 c79a793a21b5d65006f72d64148cc429e61b2b3d
fd96742eb3362cd56099c673b93072da2e741235 35ec1ca3826712e168a040d107159a60665f7de1
72dda795672b7f5ae531f7d844941519d8d0b7b1 fd96742eb3362cd56099c673b93072da2e741235
4e0b78dcef4e58578d1ce47aa73d7eec7653343d 72dda795672b7f5ae531f7d844941519d8d0b7b1
2dec520715de3b000d01039cda20c0f46d683005 4e0b78dcef4e58578d1ce47aa73d7eec7653343d
78520488d53f3f19eebc254a9cc5a7338714ceb4 2dec520715de3b000d01039cda20c0f46d683005
93d6c856c8bc5acd2d1a51099f0e864c77910f56 78520488d53f3f19eebc254a9cc5a7338714ceb4
b05370709fe57b3b5bfeeab58504bd3a6b958c42 93d6c856c8bc5acd2d1a51099f0e864c77910f56
418d4b587001eae57c92cd04ec55dff6fb6a1593 b05370709fe57b3b5bfeeab58504bd3a6b958c42
7411eceb91dfdda4ca7ea36ea59230b27e17ce57 418d4b587001eae57c92cd04ec55dff6fb6a1593
b555415c9c031ab396885073ea3d554b08712b6f 7411eceb91dfdda4ca7ea36ea59230b27e17ce57
edfab420f2e08c9137c31875d593a3a22b311e94 b555415c9c031ab396885073ea3d554b08712b6f
822c6ceac8df9f88b04bd19ea712da5cf80270c2 edfab420f2e08c9137c31875d593a3a22b311e94
e5719c6e259ff617aa3c56822eafee460fdad921 822c6ceac8df9f88b04bd19ea712da5cf80270c2
0e499e2f82e6c1cf31e079e887d89063ce4adf36 e5719c6e259ff617aa3c56822eafee460fdad921
d1dd933e714b258c8ab51a2a5d2b27a5fa213142 0e499e2f82e6c1cf31e079e887d89063ce4adf36
d7292b94ff42370128c778d439117f2b29f2410c d1dd933e714b258c8ab51a2a5d2b27a5fa213142
c25b9db022c36d36a9f8d1346b13640bfc1b20f6 d7292b94ff42370128c778d439117f2b29f2410c
9006671fb7a2f7cd5c55bb4cc7fd1996443c79f3 c25b9db022c36d36a9f8d1346b13640bfc1b20f6
39bb192cc4a3cefeb27f703484fb8ade451ff037 9006671fb7a2f7cd5c55bb4cc7fd1996443c79f3
b983d0e2b6cdbb82d54c157ba87873a764c055c2 39bb192cc4a3cefeb27f703484fb8ade451ff037
a9af83f6cf45b664f175539180b5ee1724695515 b983d0e2b6cdbb82d54c157ba87873a764c055c2
e971c50cf6118bc41b2dcd879cd0f3b17501b089 a9af83f6cf45b664f175539180b5ee1724695515
441a780704bf9322c0c6c561faf66754bb880974 e971c50cf6118bc41b2dcd879cd0f3b17501b089
6cd2cab6036176043df72e86b4d1be4ed9e0cb48 441a780704bf9322c0c6c561faf66754bb880974
36b6070c7932b440d3715531f7691b1176b1b040 6cd2cab6036176043df72e86b4d1be4ed9e0cb48
fb4e98a34dcec2a455e51883b4c4b68c64539bac 36b6070c7932b440d3715531f7691b1176b1b040
7fec25e6f90f4576dad6bbc6158be4a68ecfa312 fb4e98a34dcec2a455e51883b4c4b68c64539bac
29ec63ba14d84b8cc45caf2e251fe3a3347c100d 7fec25e6f90f4576dad6bbc6158be4a68ecfa312
cacb7b7be6e43144ac92ca09fb7146ffc143c5cf 29ec63ba14d84b8cc45caf2e251fe3a3347c100d
b999da4f2be2a6952c929a8d52fb1034a79c361c cacb7b7be6e43144ac92ca09fb7146ffc143c5cf
1e54d20282c1f128ccbc09fcdff70e4ad3164c82 b999da4f2be2a6952c929a8d52fb1034a79c361c
1da7f78e45b01045cb1ec30eaa6dadd91f36ed8e 1e54d20282c1f128ccbc09fcdff70e4ad3164c82
d587a21f45feed5884435373ba9612fea9627719 1da7f78e45b01045cb1ec30eaa6dadd91f36ed8e
232adf4ddedcded5690921c06970f77c1cd97c09 d587a21f45feed5884435373ba9612fea9627719
fb156a3de1b7f494553aa39d872ce20884bc9612 232adf4ddedcded5690921c06970f77c1cd97c09
fe5eff52211f47147eaf91a7508750a8859b4537 fb156a3de1b7f494553aa39d872ce20884bc9612
c1f985ba66dfcdd6ebc932ae2ad5ccb87752c52b fe5eff52211f47147eaf91a7508750a8859b4537
5be284ac2938b2d47d8cb4b14de4f5b351045eed c1f985ba66dfcdd6ebc932ae2ad5ccb87752c52b
75fdb3c8cc77c084f95bfcfac78f253f54607786 5be284ac2938b2d47d8cb4b14de4f5b351045eed
9165274619e229d2d010fde1e7561793d2fe2ff1 75fdb3c8cc77c084f95bfcfac78f253f54607786
5b34a19747a50a710f0b7b8689b9737926f73a5b 9165274619e229d2d010fde1e7561793d2fe2ff1
d3af79ca9233c4808ad9d8b9005a182e56234dbb 5b34a19747a50a710f0b7b8689b9737926f73a5b
b5ce89140a62c9160e07df6594607a705ebc8b81 d3af79ca9233c4808ad9d8b9005a182e56234dbb
1b0353b0a79f0de3a21c8be37dab16526a5a15c8 b5ce89140a62c9160e07df6594607a705ebc8b81
ed3000ecc97580edd3fb65c3f6d3cac3cf56f991 1b0353b0a79f0de3a21c8be37dab16526a5a15c8
f8708d4a9fa49a6ac2109051e648ad0d771b1042 ed3000ecc97580edd3fb65c3f6d3cac3cf56f991
4d903d78bafa164395c5d7f99478a00c39bb1bbd f8708d4a9fa49a6ac2109051e648ad0d771b1042
0f1c854f76aa159e87f44988e713fbfae1f459cf 4d903d78bafa164395c5d7f99478a00c39bb1bbd
e710ae7ea280774892a005ead1d75e54c33cf23c 0f1c854f76aa159e87f44988e713fbfae1f459cf
8a2c610452ce62b8522feec323404088af1267d1 e710ae7ea280774892a005ead1d75e54c33cf23c
3f8f910f16d3cc9e7022b2fe0b1365007b906783 8a2c610452ce62b8522feec323404088af1267d1
b687702ab39efe4a2f526ebe399860105acaad2c 3f8f910f16d3cc9e7022b2fe0b1365007b906783
b7b8874739c6dad25083a893a00ff10ee8dcaaeb b687702ab39efe4a2f526ebe399860105acaad2c
e40b66c2f0ea98d398b3b296dfa816c37f171215 b7b8874739c6dad25083a893a00ff10ee8dcaaeb
4efa372b2b7ebc1e340875d3464d5abdba3c4a94 e40b66c2f0ea98d398b3b296dfa816c37f171215
e4ca5dbc0cdcccab8eb40e4edcacf146df8054a3 4efa372b2b7ebc1e340875d3464d5abdba3c4a94
f159e5f66d9127d84097b9ed583071817b8752b5 e4ca5dbc0cdcccab8eb40e4edcacf146df8054a3
85effb0864de2448bb73f87224f4b1528147653a f159e5f66d9127d84097b9ed583071817b8752b5
0be3d3c3f20f4f7877f23367433056f91f5f3808 85effb0864de2448bb73f87224f4b1528147653a
b111e2b8d7d3f803b378f675926ecd9f7181fc0a 0be3d3c3f20f4f7877f23367433056f91f5f3808
cb07dfc3538598ebd2de49f55d380f5d6380f102 b111e2b8d7d3f803b378f675926ecd9f7181fc0a
5879357e86c7e701c94b74c6bea13941a7da8f40 cb07dfc3538598ebd2de49f55d380f5d6380f102
e319dcafb95150f33ea75631ac3ea858e32e45fd 5879357e86c7e701c94b74c6bea13941a7da8f40
07930fd3690163f30bd9cb161d228e009e19f255 e319dcafb95150f33ea75631ac3ea858e32e45fd
f44b7e5cae314fced0f8d519e1e5d70f3c49c35d 07930fd3690163f30bd9cb161d228e009e19f255
98b957f7e4d7aaf96cc33fe04399278357f3ab9f f44b7e5cae314fced0f8d519e1e5d70f3c49c35d
6ddaa952bf0c5b92cef701701005f5e14398f266 98b957f7e4d7aaf96cc33fe04399278357f3ab9f
da6bb22fc7afd4f5cf7df37cfc3dc3b6957c6f17 6ddaa952bf0c5b92cef701701005f5e14398f266
034f95c35721cd1146b88ad2c70b94d2e0069952 da6bb22fc7afd4f5cf7df37cfc3dc3b6957c6f17
f89746d1236a42046c7b0fed0c0dd19dc37839c9 034f95c35721cd1146b88ad2c70b94d2e0069952
d930576e7c8723c4c408af048ba25edf9e5df623 f89746d1236a42046c7b0fed0c0dd19dc37839c9
6e171dad7f2b5d19f656b8e7799d6bed1a0d4805 d930576e7c8723c4c408af048ba25edf9e5df623
9143a170903b9bcffed509d98c714bfde2d1f03f 6e171dad7f2b5d19f656b8e7799d6bed1a0d4805
ffdfc9a96c1427eaf727116df582544bd035b1e0 9143a170903b9bcffed509d98c714bfde2d1f03f
28f24de216a87e615fcffdee7bcb9bc4fec494de ffdfc9a96c1427eaf727116df582544bd035b1e0
2331a837a08f0b9d0ee8bae2bc0d662ae12360bd 28f24de216a87e615fcffdee7bcb9bc4fec494de
77743d39fc572eefcceaa65b129d9d6cfcb8b098 2331a837a08f0b9d0ee8bae2bc0d662ae12360bd
913c095db657bbecb950802920c28e876ac7c897 77743d39fc572eefcceaa65b129d9d6cfcb8b098
634f250beac05baed4d9ee42f851d2d13dd63208 913c095db657bbecb950802920c28e876ac7c897
20d1981a79c4a18fc0d924ed7c70d5848730b2d3 634f250beac05baed4d9ee42f851d2d13dd63208
240b13189c05dabce42d4d84b0dec60cd712d972 20d1981a79c4a18fc0d924ed7c70d5848730b2d3
bbfae493f218d730ff0c080f529183b099f19cab 240b13189c05dabce42d4d84b0dec60cd712d972
2430c881f6ee180ffbf657a4df1134474baf8ebc bbfae493f218d730ff0c080f529183b099f19cab
20988f6104ab853ffd3f9f5811ab7af681b87b22 2430c881f6ee180ffbf657a4df1134474baf8ebc
046ebfba15fc29dde339b2709209bfbd0af0c3e7 20988f6104ab853ffd3f9f5811ab7af681b87b22
f27cc2cb2010d54aaeefdf5aa12d2088a85b6800 046ebfba15fc29dde339b2709209bfbd0af0c3e7
8b847240d027020a18017367ca53d68294324ddf f27cc2cb2010d54aaeefdf5aa12d2088a85b6800
bae7ed52fbad7b3f8f557767b4956016e414e0f1 8b847240d027020a18017367ca53d68294324ddf
c118d2e3d810d0708c3960f0ab78fbd891964eed bae7ed52fbad7b3f8f557767b4956016e414e0f1
e87ba8f995f15482cb43d440d29785f1aa277a99 c118d2e3d810d0708c3960f0ab78fbd891964eed
0926ba98f4426e6ab29304b2c106a8388428a1dd e87ba8f995f15482cb43d440d29785f1aa277a99
bbcc516cb0e93968fa7f75644129d40569ed75f5 0926ba98f4426e6ab29304b2c106a8388428a1dd
f31264f9b78cbb5f96161e7dd1e3c0fd9af0de07 bbcc516cb0e93968fa7f75644129d40569ed75f5
28cccf056162b6518a566c63d6ecedf0c8af2c2f f31264f9b78cbb5f96161e7dd1e3c0fd9af0de07
c4f1aa5746ec24b35e6eecc7f448427b9fa7bf6d 28cccf056162b6518a566c63d6ecedf0c8af2c2f
fac3d8559b8b52c7d09d55ca4fc39f6a35b09076 c4f1aa5746ec24b35e6eecc7f448427b9fa7bf6d
a355a56c6e87b85b42e13d99a34d9a2e9e373e20 fac3d8559b8b52c7d09d55ca4fc39f6a35b09076
9c788d33120fe709c51fa70aa724bd16edf030b1 a355a56c6e87b85b42e13d99a34d9a2e9e373e20
e75dc59aca52bb2ae0672cf5dcab1148ca0a0230 9c788d33120fe709c51fa70aa724bd16edf030b1
f46af8e2dbfc80d1ba9581bf6c76ead71bb7d152 e75dc59aca52bb2ae0672cf5dcab1148ca0a0230
6fe86c54354d918aed2da2a171b66d599d605464 f46af8e2dbfc80d1ba9581bf6c76ead71bb7d152
e6fd02b8e8b70032849824cdd52135e4e5014fa2 6fe86c54354d918aed2da2a171b66d599d605464
822e2598bcf5957b712eafe9d7b3524990798759 e6fd02b8e8b70032849824cdd52135e4e5014fa2
67e13292a7f9a6763cf376409d56c6f9c743c9c8 822e2598bcf5957b712eafe9d7b3524990798759
4a4bd1fd4d41d0b8394e48d34dfb28316351c04d 67e13292a7f9a6763cf376409d56c6f9c743c9c8
8fa52ac5ee1cd989255993f346f4b471cb27e7bf 4a4bd1fd4d41d0b8394e48d34dfb28316351c04d
eb409682d44c96b39770b4fe98167973d1830a71 8fa52ac5ee1cd989255993f346f4b471cb27e7bf
0d74249f6fb11d13a65da5f19b267f58f04f04b3 eb409682d44c96b39770b4fe98167973d1830a71
b16999acc46f859c583811b698c68dda2b7fe0a8 0d74249f6fb11d13a65da5f19b267f58f04f04b3
db47f2c091ac900323b14452b321e8e7581a30cc b16999acc46f859c583811b698c68dda2b7fe0a8
92b0b57b04d0603ffe13ec197dc090bf9e7951dd db47f2c091ac900323b14452b321e8e7581a30cc
057ac946a3e92c91198bdb6ce0a4ae44881f96d7 92b0b57b04d0603ffe13ec197dc090bf9e7951dd
77302afe83138dd90a7c8773b9bb28a0f0cab714 057ac946a3e92c91198bdb6ce0a4ae44881f96d7
0111c600e142a71a1deb76a77d0afd3d1bc5bd49 77302afe83138dd90a7c8773b9bb28a0f0cab714
5a3c411799e8fec03e14651ffa4cf86117450768 0111c600e142a71a1deb76a77d0afd3d1bc5bd49
81aa2a8cf303d6b0bfbbc2e7f5292fad5ae68145 5a3c411799e8fec03e14651ffa4cf86117450768
b27da1e9997287aade21180400fd14c7778232b9 81aa2a8cf303d6b0bfbbc2e7f5292fad5ae68145
d5fd47b0f4d367e0301688e6995f93920d78f590 b27da1e9997287aade21180400fd14c7778232b9
8237e52bbbd3c7a4822c5189ee72969a43a4df5a d5fd47b0f4d367e0301688e6995f93920d78f590
30beb7f320e0121b2ad1831b08c95fe9aee1ec1d 8237e52bbbd3c7a4822c5189ee72969a43a4df5a
9ada828877262598c7c9d69ec7717f7dc537bb18 30beb7f320e0121b2ad1831b08c95fe9aee1ec1d
1731c113a663f82201bc947e868a4e77f7c61172 9ada828877262598c7c9d69ec7717f7dc537bb18
7b9ceb0d39bcf446de5cbbdbc13a16e58009ee87 1731c113a663f82201bc947e868a4e77f7c61172
4181fad1dfbad975a962bd04e90bfe45fadf4ecb 7b9ceb0d39bcf446de5cbbdbc13a16e58009ee87
2141806cf32c5c9155f2fd7d7e3600b6bc234681 4181fad1dfbad975a962bd04e90bfe45fadf4ecb
62f146b782786f39faee4ad2319ed254e6d34a4f 2141806cf32c5c9155f2fd7d7e3600b6bc234681
f4df7703846818563596db80c97dca6be12b651d 62f146b782786f39faee4ad2319ed254e6d34a4f
0fed83e867612b605014aaecdb1da97220e64c1c f4df7703846818563596db80c97dca6be12b651d
82aeec18790e97da3c2acc098709411288aacf3d 0fed83e867612b605014aaecdb1da97220e64c1c
a0fe1d0dc40da0155de5101b345f21fc500a5c01 82aeec18790e97da3c2acc098709411288aacf3d
8f0ee27c675e25bc26ff0827ac5351fb3438803f a0fe1d0dc40da0155de5101b345f21fc500a5c01
0c3e8637d26dab538222e5a15510ee92d1b26760 8f0ee27c675e25bc26ff0827ac5351fb3438803f
b39ae6edaebd51c4d519cfae5f139afd2ecbdd9e 0c3e8637d26dab538222e5a15510ee92d1b26760
487a67f7e1121a4dbd4f075602bc7eaa0ca9e108 b39ae6edaebd51c4d519cfae5f139afd2ecbdd9e
0013f09d87454c66d3ce1800b402b75a286a03da 487a67f7e1121a4dbd4f075602bc7eaa0ca9e108
d85e13b39d462ae9de43ed2884eba5ae056e37de 0013f09d87454c66d3ce1800b402b75a286a03da
cc51b8b5ecf2e8edfb163c86a52a267ff220d876 d85e13b39d462ae9de43ed2884eba5ae056e37de
dee67cf3f65f983c9a30424e5fe39b39c76539cd cc51b8b5ecf2e8edfb163c86a52a267ff220d876
0b2a645578c7591afb7c16982251b40e0152df1f dee67cf3f65f983c9a30424e5fe39b39c76539cd
3e26d45ea342ea3c6d0909dc7e46c94fb465ae32 0b2a645578c7591afb7c16982251b40e0152df1f
88ccaa2f65547b3525b00936a20e55af63f562b4 3e26d45ea342ea3c6d0909dc7e46c94fb465ae32
b58d4bf3a789039a056f378f0fad003c514a214c 88ccaa2f65547b3525b00936a20e55af63f562b4
9309e0b11745d4499f875ecd5744a68c1f7d2ea7 b58d4bf3a789039a056f378f0fad003c514a214c
de84a8afccd29231c4c6bead3b5873fabd74ce7a 9309e0b11745d4499f875ecd5744a68c1f7d2ea7
6bb6a2f75f8fb0d5d51b1259476ddc47477eaaa3 de84a8afccd29231c4c6bead3b5873fabd74ce7a
4e7d911002824a4a92e49b54f0f964afcf8cf703 6bb6a2f75f8fb0d5d51b1259476ddc47477eaaa3
cb5e55cb38aa4f2eb5b58e5218462c6738f3097a 4e7d911002824a4a92e49b54f0f964afcf8cf703
9b43c38afdb89c6b3b514b654c7fb9a936f9bf2b cb5e55cb38aa4f2eb5b58e5218462c6738f3097a
8903f7ba5d376dc642024ac8ab4400b884466c55 9b43c38afdb89c6b3b514b654c7fb9a936f9bf2b
ec7ae40fe22e1d6e5bed035450750502a1162ab5 8903f7ba5d376dc642024ac8ab4400b884466c55
2d34c3378edc5f2df064282fa067bb4af2a1e3b0 ec7ae40fe22e1d6e5bed035450750502a1162ab5
074165b38f1b6d6253a9629c7d2def988e8e286a 2d34c3378edc5f2df064282fa067bb4af2a1e3b0
fae7dfc18ca2d61af2f3446826ef3031825bbfd8 074165b38f1b6d6253a9629c7d2def988e8e286a
3737116bff6e2275d674b3dd7b816de93715f27c fae7dfc18ca2d61af2f3446826ef3031825bbfd8
ad5ce78d74c53b34358cd7508982aa888976057a 3737116bff6e2275d674b3dd7b816de93715f27c
bcaa766568b9fe7eec0781a8c6efbb288cf16dae ad5ce78d74c53b34358cd7508982aa888976057a
7afad885a8ef8ff2c8189ca72760e06a1baaa50a bcaa766568b9fe7eec0781a8c6efbb288cf16dae
4185b84f7a6a8847f6a9c5796f07113907be447d 7afad885a8ef8ff2c8189ca72760e06a1baaa50a
707f51d82217b13613c5d56d9d51d10bac5a2412 4185b84f7a6a8847f6a9c5796f07113907be447d
92a55371299439f2ff33494497cde2aa78013d77 707f51d82217b13613c5d56d9d51d10bac5a2412
6231bfbe94d39fbbb469b90a93e01426a83756bb 92a55371299439f2ff33494497cde2aa78013d77
4761c66edc3343f353ca774df835eedb1787b818 6231bfbe94d39fbbb469b90a93e01426a83756bb
b4d8f1ea5caf492f3abd030e5502d40582c52dc8 4761c66edc3343f353ca774df835eedb1787b818
10d4c376d9a71d9b0fbd5e2c9dd4894480136558 b4d8f1ea5caf492f3abd030e5502d40582c52dc8

```
