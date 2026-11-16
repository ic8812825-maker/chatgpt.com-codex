# HSBI-03D — Scope attestation и происхождение публикации

## Область

Repository ic8812825-maker/chatgpt.com-codex; branch work; project MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/.
Этот этап HSBI-03D-PUBLISH выполняется только подключённым GitHub MCP после отдельного явного разрешения владельца необходимых API reads/writes.
Никаких local checkout/clone/filesystem search/local file generation в этом этапе. Ruleset ChatGPT1 не исследуется/не меняется; PR,CodeQL,other branches,force/bypass запрещены.
Изменения разрешены только9 новым Reports files перечисленным ниже. Production,Docs,Contracts,Tests,исторические Reports/frozen evidence неизменны.

Не следует распространять эту stage-specific attestation на всю беседу: между audit и публикацией ранее был неуспешный обычный Git environment check в /workspace (not a git repository); он не создавал checkout/clone/files/commit и был остановлен. Новая публикация не использует тот путь.

## Источники и baseline

Полный предшествующий ответ HSBI-03D / HSBI-03D-REMOTE-R1 доступен в контексте и является источником этих9 документов. Это его предметное размещение, не утверждение о найденных локальных отчётах и не выдуманное восстановление. Подробные16 карточек,20 facets,полные normative texts,14 P0,counterexamples,cycles,tests preserved в связанном пакете.

Историческая audit remote verification: 2026-11-16 15:16:59 UTC.
Publication baseline recheck: 2026-11-16 15:48:57 UTC.
Expected/actual work HEAD: 6543bc2c0d125f5f7e02f78a092b0412a2e34626.
Commit metadata/root tree ca6f73ae24ae64da69acb33b6835904348e85e14.
Project scoped listing:
Docs7748742a222e6b4a2410ad56ccf9f13af1b80b14;
Include8ef77572c3c921e4e88a86a6b140e11a0613246a;
Reportse3ae3ab2ee826ae0fdc626ee2b1d18c47b666355;
Tests8b2b0770d6decb4383245dc9ff3f2e344fd555dc.
Reports279 entries; целевые9 отсутствуют, name conflict нет. HEAD совпадает historical baseline, поэтому новые incoming commits для reconcile отсутствуют.

Metadata repository/ref/commit/tree нужна для разрешённой публикации; содержимое других проектов/веток не читается. Root-tree SHA используется как base tree, не как разрешение читать другие project paths.

## Manifest новых файлов

- Reports/HSBI_03D_REMOTE_SCOPE_ATTESTATION_RU.md
- Reports/HSBI_03D_INDEPENDENT_CONTRACT_REVIEW_RU.md
- Reports/HSBI_03D_OWNER_APPROVAL_BALLOT_RU.md
- Reports/HSBI_03D_CONTRACT_CONSISTENCY_MATRIX_RU.md
- Reports/HSBI_03D_MONEY_INVARIANTS_AND_COUNTEREXAMPLES_RU.md
- Reports/HSBI_03D_P0_REMEDIATION_CROSSWALK_RU.md
- Reports/HSBI_03D_NUMERIC_NATIVE_QUALIFICATION_RU.md
- Reports/HSBI_03D_R11_READINESS_GATES_RU.md
- Reports/HSBI_03D_FINAL_VERDICT_RU.md

## Publication integrity procedure

Содержимое проверяется в памяти без local FS. Create9 blobs; tree на base root с ровно9 explicit project/Reports paths; один commit с единственным parent current work HEAD; ещё одна HEAD check перед записью; update_ref branch_name=work,force=false,expected_sha=baseline.
Никакой branch protection bypass,policy mutation,новой ветки или PR. Фактический server rejection следует сообщить дословно, а не предполагать.

После update требуются ref re-read, commit metadata/diff9 added files, full content reread at published SHA, comparison с подготовленным текстом и повторный work HEAD.
Эта attestation создаётся ДО ref update и не заявляет будущий SUCCESS. Фактические commit SHA/result/parity сообщаются в финальном publication receipt ответа; собственный commit SHA не встраивается в себя.

## Пределы сохранности/исследования

Не заявляется отдельный новый побайтовый rehash1529 baseline files, новый полный аудит74 modules/199 definitions или новое native/runtime/mutation исполнение. Сохранность обеспечивается base-tree construction и разрешённым diff, затем проверяется remote diff.
Source catalog и historical blob references в independent review; tests 7PASS/16FAIL только HISTORICAL_TEST_RESULT.
Отчёты не утверждают контракты и не разрешают R1.1/trading.
