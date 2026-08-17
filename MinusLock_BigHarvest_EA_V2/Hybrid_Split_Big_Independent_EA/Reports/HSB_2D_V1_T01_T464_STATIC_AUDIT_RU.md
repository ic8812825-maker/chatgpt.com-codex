# Независимый статический аудит T01–T464

## Результат инвентаризации

```text
DECLARED_TESTS=464
UNIQUE_TEST_IDS=464
MIN_TEST_ID=T01
MAX_TEST_ID=T464
MISSING_TEST_IDS=0
DUPLICATE_TEST_IDS=0
MQL5_TESTS_T01_T464=NOT_EXECUTED_MT5_UNAVAILABLE
```

Каждый вызов `Check(id, requirement, expected, actual, reason)` содержит пять аргументов: Test ID, Requirement ID, ожидаемое bool, actual expression и ReasonCode. `Check()` увеличивает `g_pass` только при `expected==actual`, иначе увеличивает `g_fail`. Summary использует `g_pass+g_fail` и печатает `TOTAL`, `PASS`, `FAIL`. Присваивания `g_pass=464`, подавления `g_fail`, unconditional PASS и раннего выхода из `OnStart()` нет.

T431–T454 вызывают runtime decision validator и transaction barrier; T455–T464 вызывают restart validator. Negative cases до вызова изменяют identity, revision, freshness, residual, proof, allocation, digest, persistence, event/action, payload либо persisted state. Expected и actual соответствуют контракту.

T425–T430 проверяют только формат и исторические строковые отношения; они не обращаются к Git/GitHub и не доказывают публикацию:

```text
T425-T430=DOCUMENTARY_STATIC_CHECKS
GITHUB_PUBLICATION_PROOF=SEPARATE_GIT_VERIFICATION_REQUIRED
```

`TEST_IDS_T01_T464=PASS`; исполнение остаётся пользовательской проверкой HSB.2D-V2.
