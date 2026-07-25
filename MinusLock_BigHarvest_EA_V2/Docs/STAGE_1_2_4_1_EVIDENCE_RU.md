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
FINAL_CI_VALUES_PENDING
```

Фактические run, artifact и test-count значения вносятся только после успешного запуска Commit A и проверки скачанного artifact.

## FINAL_EVIDENCE_CONFIRMATION_RUN

Финальный status check выполняется на Evidence Commit B. Его ID приводится в итоговом отчёте, чтобы обновление документа не создавало бесконечный цикл commit/run.

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
