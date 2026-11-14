# AUDIT03 R7 — независимая диагностика Git push и GitHub API

Проверка 2026-11-14 (UTC); репозиторий `ic8812825-maker/chatgpt.com-codex`. Реального push, commit, merge, изменения ruleset, production или старых R5/R6/R7 отчётов не выполнялось. Этот документ уточняет и заменяет прежний категоричный технический вывод о невозможности Git push вследствие недоступности API; содержательные результаты аудита не переклассифицированы.

## Исправление прежнего вывода

API и Git HTTPS — разные endpoints и протоколы. Git использует github.com/...git/info/refs и git-receive-pack; gh REST/GraphQL — api.github.com. Их маршрутизация через proxy, аутентификация и разрешения могут отличаться. Успешный Git push одновременно с Forbidden API технически возможен. Недоступность API мешает проверять authenticated permissions/bypass actors и управлять PR через gh, но не доказывает отказ Git push. Прежний вывод PUBLISH_BLOCKED=BRANCH_PROTECTION_AND_NO_VERIFIED_WRITE_WORKFLOW являлся ограничением безопасно подтверждённого процесса, а не установленным серверным отказом обновления R7.

Сейчас реальный push не выполнялся: PUSH_REJECTED не установлен. Dry-run завершился успешно, но HEAD уже совпадает с remote. Незакоммиченные R7 файлы в dry-run не участвовали. No-op dry-run не проверяет приём новых объектов/ref update, ruleset evaluation нового commit, pre-receive hooks или наличие разрешённого bypass-free пути публикации.

## Git remote / local state

Remote `https://github.com/ic8812825-maker/chatgpt.com-codex.git`; branch `audit/hsbi-audit03-github-closure-r4`; local HEAD и remote audit/PR4 head `5ef8983f1e91e3f4cb3b659de2e2e3c0b9268ae2`; work `b4d8f1ea5caf492f3abd030e5502d40582c52dc8`. `git rev-list --left-right --count 5ef8983f1e91e3f4cb3b659de2e2e3c0b9268ae2...HEAD` exit0, output `0\t0`; `git log 5ef8983f1e91e3f4cb3b659de2e2e3c0b9268ae2..HEAD --format='%H %s'` exit0, пусто. Неопубликованных commits нет; есть12 изменённых tracked отчётов и1 untracked recovery-container.

`git var GIT_AUTHOR_IDENT` и `git var GIT_COMMITTER_IDENT` exit0: `Игорь Чернов <ic8812825@gmail.com>`, timestamp1794666805 +0000 в контрольном вызове. Это commit metadata, не доказательство GitHub login/token scope. В существующем HEAD author/committer совпадают с этими именем/email.

## Полный git ls-remote

Команда: `git ls-remote origin`

Exit code: 0

```text
b4d8f1ea5caf492f3abd030e5502d40582c52dc8	HEAD
91e19139bb52256c2efd0bb7274a0ad74d5008c3	refs/heads/ALE_DisplayOnly.zip
c2c9095ca7a8617c81d55f71b09d8497f7091bc3	refs/heads/ale
9089400908000e730342790ec7d99761e8756af1	refs/heads/ale_separate_brains
5ef8983f1e91e3f4cb3b659de2e2e3c0b9268ae2	refs/heads/audit/hsbi-audit03-github-closure-r4
3b0bb20faa4d305868f1a957c685c92fa23d5e8f	refs/heads/audit/stage-1.2.4.2-evidence
1c4ed1c9f0f15da9b8c4a9f37fef7c438bd904cb	refs/heads/ic8812825-maker-patch-1
7d5f83803c17e14339af5d9b5c7167e526e63568	refs/heads/ic8812825-maker-patch-2
6512bc2c6acfe3879a139b980cd71b3c4e037f51	refs/heads/ic8812825-maker-patch-3
428d331dcdd5b3041bf940ed52af4c4dc0840e26	refs/heads/ic8812825-maker-patch-4
9e7371e6f5d6851ff2199901c46063f6e86400f8	refs/heads/main
b4d8f1ea5caf492f3abd030e5502d40582c52dc8	refs/heads/work
7d5f83803c17e14339af5d9b5c7167e526e63568	refs/pull/1/head
1ca79251ad84579b77e8d3e4146ca8735a79b198	refs/pull/1/merge
428d331dcdd5b3041bf940ed52af4c4dc0840e26	refs/pull/2/head
3a4da62402685b108810f5f55a6720c8f04f376d	refs/pull/2/merge
3b0bb20faa4d305868f1a957c685c92fa23d5e8f	refs/pull/3/head
d7cac720a371ac59ccf017506221504776dbf842	refs/pull/3/merge
5ef8983f1e91e3f4cb3b659de2e2e3c0b9268ae2	refs/pull/4/head
3070a926762b794a9fe9042cef6b8a9d8c89a4d1	refs/pull/4/merge
```

## Полный ответ dry-run

Команда: `git push --dry-run --porcelain origin HEAD:refs/heads/audit/hsbi-audit03-github-closure-r4`

Exit code: 0

```text
To https://github.com/ic8812825-maker/chatgpt.com-codex.git
=	HEAD:refs/heads/audit/hsbi-audit03-github-closure-r4	[up to date]
Done
```

## gh authentication status

Команда: `gh auth status`

Exit code: 0

```text
github.com
  X Failed to log in to github.com using token (GH_TOKEN)
  - Active account: true
  - The token in GH_TOKEN is invalid.
```

## GitHub repository API

Команда: `gh api repos/ic8812825-maker/chatgpt.com-codex --jq '{full_name,permissions}'`

Exit code: 1

```text
Get "https://api.github.com/repos/ic8812825-maker/chatgpt.com-codex": Forbidden
```

## Authenticated ruleset API

Команда: `gh api repos/ic8812825-maker/chatgpt.com-codex/rulesets/12711484`

Exit code: 1

```text
Get "https://api.github.com/repos/ic8812825-maker/chatgpt.com-codex/rulesets/12711484": Forbidden
```

## HTTPS authentication: доказательная граница

`GIT_TERMINAL_PROMPT=0 git credential fill` с stdin `protocol=https`, `host=github.com`, `path=ic8812825-maker/chatgpt.com-codex.git`: exit128, stderr:

```text
fatal: could not read Username for 'https://github.com': terminal prompts disabled
```

Значения credentials не выводились. Конфигурационных ключей credential.*, http.*extraheader и core.askpass в проверенном Git config не найдено (`git config --get-regexp` при отсутствии совпадений возвращает1). Это доказывает отсутствие возвращённых стандартным credential helper credentials в этом вызове, но не отсутствие управляемой аутентификации вне Git config. Ни владелец фактической Git HTTPS сессии, ни scope её credentials независимо не установлены.

Повторный dry-run с `GIT_TRACE_CURL=1 GIT_TRACE_CURL_NO_DATA=1 GIT_TERMINAL_PROMPT=0` exit0; trace разбирался только в памяти. Безопасно сохранены HTTP status lines; остальные headers/credentials исключены:

```text
git_dry_run_trace_exit=0
To https://github.com/ic8812825-maker/chatgpt.com-codex.git
=	HEAD:refs/heads/audit/hsbi-audit03-github-closure-r4	[up to date]
Done
14:32:29.592650 http.c:890              == Info: CONNECT tunnel: HTTP/1.1 negotiated
14:32:29.607842 http.c:849              <= Recv header: HTTP/1.1 200 OK
14:32:29.607885 http.c:890              == Info: CONNECT phase completed
14:32:29.607890 http.c:890              == Info: CONNECT tunnel established, response 200
14:32:30.024986 http.c:849              <= Recv header: HTTP/2 200
Other trace headers and authentication values deliberately omitted.
credential_fill_exit=128
fatal: could not read Username for '<URL_REDACTED> terminal prompts disabled
```

HTTP CONNECT200 и origin HTTP200 означают доступность использованного Git endpoint. Они не подтверждают конкретный GitHub account или permission обновления refs. Auth-header в клиентском trace не наблюдался; возможная upstream/proxy identity не установлена.

## API network versus authentication

Два независимых запроса к публичному API **без Authorization**, через `urllib.request.urlopen` (системный proxy, без отключения/обхода), дали:

```text
UNAUTHENTICATED_PUBLIC_API https://api.github.com
URLError <urlopen error Tunnel connection failed: 403 Forbidden>
UNAUTHENTICATED_PUBLIC_API https://api.github.com/repos/ic8812825-maker/chatgpt.com-codex
URLError <urlopen error Tunnel connection failed: 403 Forbidden>
```

Диагностический Python process exit0, потому что исключения намеренно пойманы и напечатаны; сами HTTP-запросы неуспешны. Это CONNECT403 до установления туннеля к api.github.com. Следовательно, HTTP401 от GitHub, настоящий repository permission403 и валидность GH_TOKEN этими вызовами не установлены. `gh auth status` вывел invalid token при exit0, но этот вывод нельзя независимо подтвердить, пока API tunnel блокируется. Нельзя приравнивать его к доказанному отказу Git HTTPS authentication.

`gh api graphql` в этой проверке отдельно не запускался: приведённый владельцем прежний GraphQL Forbidden не выдаётся за новый запуск. Для текущего вывода достаточно отдельно подтверждённого proxy запрета к общему api.github.com и успешного Git dry-run.

## Правила и bypass actors

Официальные страницы `https://github.com/ic8812825-maker/chatgpt.com-codex/rules`, `/rules/12711484`, `/pull/4` HTTP200 (Python diagnostic process exit0). Полный существенный embedded JSON и извлечённые поля:

```text
URL https://github.com/ic8812825-maker/chatgpt.com-codex/rules
HTTP 200
ACCESS_FIELD currentUserCanPush false
RULESET {"id": 12711484, "target": "branch", "name": "ChatGPT1", "source": {"id": 1148625262, "type": "Repository", "name": "chatgpt.com-codex", "url": "http://github.com/ic8812825-maker/chatgpt.com-codex/settings/rules"}, "enforcement": "enabled", "rules": [{"id": 82037332, "ruleType": "deletion", "parameters": {}}, {"id": 82037333, "ruleType": "non_fast_forward", "parameters": {}}, {"id": 82037334, "ruleType": "pull_request", "parameters": {"required_reviewers": [], "allowed_merge_methods": ["merge", "squash", "rebase"], "require_code_owner_review": true, "require_last_push_approval": true, "dismiss_stale_reviews_on_push": true, "required_approving_review_count": 0, "authorized_dismissal_actors_only": false, "required_review_thread_resolution": true, "ignore_approvals_from_contributors": false, "dismissal_restriction": {"enabled": false, "allowed_actors": []}, "require_extra_approval_for_unattributed_changes": true}}, {"id": 82037335, "ruleType": "code_scanning", "parameters": {"code_scanning_tools": [{"tool": "CodeQL", "alerts_threshold": "errors", "security_alerts_threshold": "high_or_higher"}]}}, {"id": 82037336, "ruleType": "code_quality", "parameters": {"severity": "all"}}, {"id": 82045783, "ruleType": "required_deployments", "parameters": {"required_deployment_environments": []}}], "conditions": [{"id": 24149807, "target": "ref_name", "parameters": {"exclude": [], "include": ["~DEFAULT_BRANCH", "~ALL"]}}], "missingConditionTargets": [], "bypassActors": null}
ACCESS_FIELD bypassActors null
ACCESS_FIELD supportsBypass true
ACCESS_FIELD supportsBypass true
URL https://github.com/ic8812825-maker/chatgpt.com-codex/rules/12711484
HTTP 200
ACCESS_FIELD currentUserCanPush false
RULESET {"id": 12711484, "target": "branch", "name": "ChatGPT1", "source": {"id": 1148625262, "type": "Repository", "name": "chatgpt.com-codex", "url": "http://github.com/ic8812825-maker/chatgpt.com-codex/settings/rules"}, "enforcement": "enabled", "rules": [{"id": 82037332, "ruleType": "deletion", "parameters": {}}, {"id": 82037333, "ruleType": "non_fast_forward", "parameters": {}}, {"id": 82037334, "ruleType": "pull_request", "parameters": {"required_reviewers": [], "allowed_merge_methods": ["merge", "squash", "rebase"], "require_code_owner_review": true, "require_last_push_approval": true, "dismiss_stale_reviews_on_push": true, "required_approving_review_count": 0, "authorized_dismissal_actors_only": false, "required_review_thread_resolution": true, "ignore_approvals_from_contributors": false, "dismissal_restriction": {"enabled": false, "allowed_actors": []}, "require_extra_approval_for_unattributed_changes": true}}, {"id": 82037335, "ruleType": "code_scanning", "parameters": {"code_scanning_tools": [{"tool": "CodeQL", "alerts_threshold": "errors", "security_alerts_threshold": "high_or_higher"}]}}, {"id": 82037336, "ruleType": "code_quality", "parameters": {"severity": "all"}}, {"id": 82045783, "ruleType": "required_deployments", "parameters": {"required_deployment_environments": []}}], "conditions": [{"id": 24149807, "target": "ref_name", "parameters": {"exclude": [], "include": ["~DEFAULT_BRANCH", "~ALL"]}}], "missingConditionTargets": [], "bypassActors": null}
ACCESS_FIELD bypassActors null
ACCESS_FIELD supportsBypass true
ACCESS_FIELD supportsBypass true
URL https://github.com/ic8812825-maker/chatgpt.com-codex/pull/4
HTTP 200
PR {"state": "DRAFT", "baseBranch": "work", "headBranch": "audit/hsbi-audit03-github-closure-r4", "headSha": "5ef8983f1e91e3f4cb3b659de2e2e3c0b9268ae2", "baseSha": "b4d8f1ea5caf492f3abd030e5502d40582c52dc8", "closedTime": null}
```

ChatGPT1 enabled; include~ALL/exclude[] охватывает audit и work. Требуются PR, CodeQL, Code Quality, Code Owners/last-push approval и разрешение review threads; non-fast-forward/deletion запрещены. required_approving_review_count=0 не отменяет специальные approval clauses. Empty required_deployment_environments не добавляет конкретного deployment gate.

`bypassActors=null` публичного представления означает, что список actors не получен; это не пустой подтверждённый список. `currentUserCanPush=false` относится к неаутентифицированному HTML viewer, а не к Git HTTPS identity. Полные bypass actors и применимость исключений к фактическому transport actor не установлены: authenticated ruleset API возвращает Forbidden. Попыток изменить правила или воспользоваться bypass нет.

Предыдущий server-reported bypass для опубликованного5ef сохраняется как исторический факт:

```text
remote: Bypassed rule violations for refs/heads/audit/hsbi-audit03-github-closure-r4:
remote: - Changes must be made through a pull request.
remote: - Waiting for Code Scanning results. Code Scanning may not be configured for the target branch.
```

В текущем no-op dry-run этого сообщения нет. Это не опровергает предыдущий incident и не доказывает, что следующий update принят без bypass. Прямой новый push не выполняется без установленного разрешённого процесса.

## Неопубликованные материалы и контрольная сумма

Ниже снимок до создания данного диагностического документа; полный вывод локальной проверки с exit codes, numstat и SHA256 всех13 прежних файлов:

```text
credential_fill_exit 128
fatal: could not read Username for 'https://github.com': terminal prompts disabled
COMMAND ["git", "rev-list", "--left-right", "--count", "5ef8983f1e91e3f4cb3b659de2e2e3c0b9268ae2...HEAD"] EXIT 0
0	0
COMMAND ["git", "log", "5ef8983f1e91e3f4cb3b659de2e2e3c0b9268ae2..HEAD", "--format=%H %s"] EXIT 0
COMMAND ["git", "var", "GIT_AUTHOR_IDENT"] EXIT 0
Игорь Чернов <ic8812825@gmail.com> 1794666805 +0000
COMMAND ["git", "var", "GIT_COMMITTER_IDENT"] EXIT 0
Игорь Чернов <ic8812825@gmail.com> 1794666805 +0000
COMMAND ["git", "diff", "--numstat"] EXIT 0
20	0	MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_ALL_ERRORS_RU.md
4	0	MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md
32	0	MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_BASELINE_AND_PRESERVATION_RU.md
37	0	MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_COMPLETENESS_MATRIX_RU.md
175	109	MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_DOCUMENT_COVERAGE_RU.md
103	0	MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_FINAL_CLOSURE_READING_LOG_RU.md
271	0	MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_FINAL_VERDICT_RU.md
8	0	MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_FORMULA_CATALOG_RU.md
59	0	MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_FSM_COMPLETE_MATRIX_RU.md
101	0	MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_GUARD_CALLER_CROSSWALK_RU.md
142	0	MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_R2_WORK_IN_PROGRESS_RU.md
90	0	MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_R4_GITHUB_PUBLICATION_RU.md
COMMAND ["git", "diff", "--check"] EXIT 0
LOCAL_CHANGE_MANIFEST [{"path": "MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_ALL_ERRORS_RU.md", "bytes": 178662, "sha256": "f4886389895afd600f08aee4203e5d7a3064bef7a187c566e9b7381b47aeb0f4"}, {"path": "MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md", "bytes": 89980, "sha256": "f494a3e49bb825267ce3f89b0e23b312951c7570ab2850d4f626aa5afa978613"}, {"path": "MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_BASELINE_AND_PRESERVATION_RU.md", "bytes": 873169, "sha256": "f9aa763cc1d9b8ff537051cb914d1c82dde1a9c4806b959d7bd50a60cbcbe459"}, {"path": "MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_COMPLETENESS_MATRIX_RU.md", "bytes": 43709, "sha256": "a73ef614e1f1daf6b9de3e59cb53098ba8807b6228ed7871280b30813122e73e"}, {"path": "MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_DOCUMENT_COVERAGE_RU.md", "bytes": 677988, "sha256": "8c67f995d850b38758412a36dfcd01df1517dfce168eca7bd0a8313e61b06fb9"}, {"path": "MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_FINAL_CLOSURE_READING_LOG_RU.md", "bytes": 219262, "sha256": "6c081341be77744dd6a7bf553463527c98a7fc8ab16d48d018bff3b131eddd5d"}, {"path": "MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_FINAL_VERDICT_RU.md", "bytes": 68137, "sha256": "9970949313c3530a4dbc4d7baff8516662bc444c05366887cb1282866207b475"}, {"path": "MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_FORMULA_CATALOG_RU.md", "bytes": 252431, "sha256": "a26b56436d5f44b1ebb681d678a1993e3273aadc243cd0dd61e12ab787042085"}, {"path": "MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_FSM_COMPLETE_MATRIX_RU.md", "bytes": 47801, "sha256": "12454cdd66e3b72f0f2b2f3af21a2f99203fb3954237af13f3bac430e09e4556"}, {"path": "MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_GUARD_CALLER_CROSSWALK_RU.md", "bytes": 286286, "sha256": "076638849713555acaf7d31eec7e6b8d68604f9f3b42161bc49b9f4d00a010cc"}, {"path": "MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_R2_WORK_IN_PROGRESS_RU.md", "bytes": 79688, "sha256": "44ab61b18077a9fddd7ee5d6b23114e94be6a901eeb3e4e03d266c0afcee1e87"}, {"path": "MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_R4_GITHUB_PUBLICATION_RU.md", "bytes": 40804, "sha256": "602d89828e9ba384de5e5f04a4b311f12939ae140758f57eeedf70734df29e0d"}, {"path": "MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Reports/HSBI_AUDIT03_R7_RECOVERY_PATCH_RU.md", "bytes": 654498, "sha256": "04868750292bbc4b44040360ac80b1a33a66affadae245c299a68f2016902797"}]
```

Все13 прежних файлов должны остаться побайтно неизменными после этой диагностики; заключительная проверка выполняется отдельно. Recovery-container остаётся историческим полным patch12 tracked отчётов; новый диагностический документ в старый patch не входит. Тестовые runners, MQL5 и торговля не запускались.

## Раздельные итоговые статусы

```text
GIT_REMOTE_READ_ACCESS=YES_EXIT_0
GIT_AUTHENTICATION=NOT_INDEPENDENTLY_ESTABLISHED_FOR_HTTPS_ACTOR
GITHUB_API_ACCESS=BLOCKED_PROXY_CONNECT_403
GITHUB_REPOSITORY_PUSH_PERMISSION=NOT_ESTABLISHED_BY_NO_OP_DRY_RUN
GIT_PUSH_DRY_RUN_RESULT=EXIT_0_UP_TO_DATE_NO_REF_UPDATE_PROPOSED
BRANCH_PROTECTION_STATUS=ACTIVE_CHATGPT1_ALL_BRANCHES_ACTOR_EXCEPTIONS_UNVERIFIED
ACTUAL_PUSH_ATTEMPTED=NO_THIS_DIAGNOSTIC
ACTUAL_PUSH_REJECTED=NOT_APPLICABLE_NO_ACTUAL_PUSH
BYPASS_REQUIRED=NOT_ESTABLISHED_FOR_A_NEW_R7_COMMIT
BYPASS_USED=NO_THIS_DIAGNOSTIC_PREVIOUS_SERVER_REPORTED_BYPASS_RETAINED
R7_LOCAL_CHANGES_PRESERVED=YES_13_PRIOR_FILES_BYTE_IDENTICAL
R7_PUBLICATION_STATUS=NOT_PUBLISHED_NO_R7_COMMIT_CREATED
```

Подтверждено ограничение API и наличие ruleset. **Не подтверждены** отсутствие repository push permission, отказ аутентификации Git HTTPS, фактический отказ обновления R7 и неизбежность bypass для любого штатного способа публикации. Безопасный следующий шаг — получить через официальный доступ данные actor/permissions/bypass exceptions и согласованный repository PR workflow; настройки защиты не отключать. No-op dry-run не заменяет эту проверку.

## Заключительная проверка сохранности

Статическая SHA256/size проверка после создания отчёта: все13 прежних R5/R6/R7 файлов побайтно совпали со снимком до диагностики. Единственный добавленный файл — этот Markdown-отчёт. Сравнение1515 защищённых файлов с b4d8f1e по Git blob и mode успешно, включая74 production; git diff --check exit0. HEAD остался5ef8983f. Изменения старых отчётов, commit, настоящий push, merge, тесты и компиляция не выполнялись.
