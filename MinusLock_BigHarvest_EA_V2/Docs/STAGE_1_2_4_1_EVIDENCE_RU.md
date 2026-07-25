# Stage 1.2.4.1 — доказательства исходного кода

Репозиторий:
https://github.com/ic8812825-maker/chatgpt.com-codex

Ветка:
`work`

Проект:
`MinusLock_BigHarvest_EA_V2`

Способ интеграции:
`DIRECT_COMMIT_AND_PUSH_TO_WORK`

## Provenance восстановления

```text
EXPECTED_LOCAL_COMMIT=79df903ab76a572c59be038f538f708cc48a228f
EXPECTED_LOCAL_COMMIT_STATUS=NOT_FOUND
ACTUAL_LOCAL_HEAD=c5dd3fbb4e0dc968e9847b7e754360744e51db81
ACTUAL_LOCAL_HEAD_STATUS=AUTHORIZED_FOR_RECOVERY
SOURCE_BASE=4413a05bd785cbef398fc418ad12b008fa090a00
SOURCE_COMMIT=11ae620f717cf011436db52cf4b3b76d0015c606
```

`SOURCE_COMMIT` содержит исправление Partial-lot dimension contract. `CI_COMMIT` обозначает линейный commit ветки `work`, содержащий CI/evidence-инфраструктуру. Эти SHA намеренно могут отличаться.

## PRIMARY_IMPLEMENTATION_RUN

```text
VALIDATED_SOURCE_COMMIT_A=8eb8fe8616a4966ddcc44e2285d5cc7bec6566b3
WORKFLOW_NAME=Stage 1.2.4.1 Source Validation
WORKFLOW_RUN_ID=30170647795
WORKFLOW_RUN_URL=https://github.com/ic8812825-maker/chatgpt.com-codex/actions/runs/30170647795
WORKFLOW_RUN_ATTEMPT=1
WORKFLOW_STATUS=completed
WORKFLOW_CONCLUSION=success
WORKFLOW_HEAD_BRANCH=work
WORKFLOW_HEAD_SHA=8eb8fe8616a4966ddcc44e2285d5cc7bec6566b3
CI_COMMIT=8eb8fe8616a4966ddcc44e2285d5cc7bec6566b3
JOB_ID=89711077231
ARTIFACT_NAME=stage-1.2.4.2.1-source-validation-8eb8fe8616a4966ddcc44e2285d5cc7bec6566b3
ARTIFACT_ID=8622818843
ARTIFACT_SIZE=4005
ARTIFACT_DIGEST=sha256:70eafa2742df42f72a0b906ea0d639f3a53617c44dc5f239b217ecfcc539a8df
ARTIFACT_EXPIRED=false
ARTIFACT_CREATED_AT=2026-07-25T18:57:30Z
ARTIFACT_EXPIRES_AT=2026-08-24T18:57:29Z
SHA256SUMS_FILE_SHA256=ec0886f08c662d54e151d29939e58ae7ee915c0a20cc27cc280db8400b9b0617
```

Artifact скачан через GitHub API. В нём присутствуют ровно 11 обязательных evidence-файлов, а `sha256sum -c SHA256SUMS.txt` завершён с `ALL OK`.

Фактические результаты из artifact:

```text
dimension-contract tests=17 passed in 0.08s
HybridSplitBig tests=186 passed in 0.49s
all project tests=391 passed in 0.86s
big_move_levels_check=PASS
validate_v2_static=PASS
forbidden-files guard=FORBIDDEN_FILES_EMPTY
guard self-tests=Passed=5,Failed=0
validation exit status=0
```

## FINAL_EVIDENCE_CONFIRMATION_RUN

`EVIDENCE_DOCUMENT_COMMIT_B` содержит эти фактические данные Primary run. Финальный status check выполняется на Commit B; его ID приводится в итоговом отчёте, чтобы обновление документа не создавало бесконечный цикл commit/run.

## Граница доказательства

GitHub Actions подтверждает только Python/static source validation. CI не подтверждает MetaEditor compilation, MQL5 runner execution, Strategy Tester, broker-specific calculations, торговое исполнение или production readiness.

Статус MQL5 остаётся:

```text
ADMIN_MT5_VALIDATION_REQUIRED
```

## Checklist Администратора MQL5

- [ ] `HybridCatchUpDimensionContractTests.mq5` скомпилирован
- [ ] Compiler errors = 0
- [ ] Compiler warnings проверены
- [ ] Runner запущен
- [ ] `CATCHUP_DIMENSION_TEST|SUMMARY|Failed=0`
- [ ] Outcome = `CONTINUE` или `FINITE_PASS`
- [ ] `continuationStateValid = true`
- [ ] Journal, symbol и broker build зафиксированы
