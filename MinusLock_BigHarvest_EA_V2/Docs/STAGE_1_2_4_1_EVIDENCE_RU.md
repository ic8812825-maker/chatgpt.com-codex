# Stage 1.2.4.1 — доказательства исходного кода

## Provenance

- Проверяемый source commit: `11ae620f717cf011436db52cf4b3b76d0015c606`.
- Source base: `4413a05bd785cbef398fc418ad12b008fa090a00`.
- Исторический способ интеграции: прямой обычный push в `origin/work`.
- Отдельный implementation PR Stage 1.2.4.1 не подтверждён номером и URL.
- Подготовленные title/body или payload означают `PR_PREPARED_ONLY`, но не `PR_CREATED`.

## Термины доказательств

- `LOCAL_TEST_REPORTED`: локальный запуск заявлен исполнителем, независимый CI artifact отсутствует.
- `CI_TEST_VERIFIED`: существует успешный GitHub Actions run с URL, run ID и logs.
- `CI_ARTIFACT_AVAILABLE`: существует artifact с именем, artifact ID и привязкой к commit SHA.
- `PR_CREATED`: GitHub подтверждает PR number, URL, state, base и head.
- `PR_PREPARED_ONLY`: подготовлены только title/body без подтверждённого GitHub PR.

## Что проверяет CI

Workflow `Stage 1.2.4.1 Source Validation` проверяет Python syntax, dimension tests Stage 1.2.4.1, полный `HybridSplitBig` suite, все Python-тесты проекта, legacy static checks, отсутствие изменений запрещённых execution-файлов и Partial-lot source contract. Скрипт сохраняет отдельные логи, manifest и `SHA256SUMS.txt`.

## Что CI не проверяет

GitHub CI подтверждает только Python/static source validation. Он не проверяет MetaEditor compilation, выполнение MQL5 runner, Strategy Tester, broker-specific money calculation, реальное прохождение MQL continuation fixture или торговое исполнение. MQL5 compilation и runtime validation выполняются Администратором проекта самостоятельно.

## Фактические GitHub-поля

До получения ответа GitHub поля нельзя заполнять предположениями.

| Поле | Значение |
|---|---|
| Workflow run ID | `NOT_YET_AVAILABLE` |
| Workflow run URL | `NOT_YET_AVAILABLE` |
| Workflow result | `NOT_YET_AVAILABLE` |
| Artifact name | `NOT_YET_AVAILABLE` |
| Artifact ID | `NOT_YET_AVAILABLE` |
| Artifact SHA256SUMS | `NOT_YET_AVAILABLE` |
| Evidence branch SHA | `NOT_YET_AVAILABLE` |
| Pull request number | `NOT_YET_AVAILABLE` |
| Pull request URL | `NOT_YET_AVAILABLE` |

## Checklist Администратора MQL5

- [ ] `HybridCatchUpDimensionContractTests.mq5` скомпилирован
- [ ] Compiler errors = 0
- [ ] Compiler warnings проверены
- [ ] Runner запущен
- [ ] `CATCHUP_DIMENSION_TEST|SUMMARY|Failed=0`
- [ ] `MQL-DIM-EVAL-FIXTURE-NOT-FOUND = PASS`
- [ ] Outcome = `CONTINUE` или `FINITE_PASS`
- [ ] `continuationStateValid = true`
- [ ] Journal сохранён
- [ ] Symbol и broker build зафиксированы
