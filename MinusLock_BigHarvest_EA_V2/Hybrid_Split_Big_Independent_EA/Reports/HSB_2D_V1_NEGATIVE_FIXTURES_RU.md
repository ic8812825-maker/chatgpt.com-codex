# Чувствительность offline verifier HSB.2D-V1

Verifier создаёт изолированные временные копии только в системном temporary directory, не подменяет production-файлы и удаляет fixtures автоматически. До и после suite сравниваются SHA-256 всех `.mq5`/`.mqh`.

| Mutation | Expected | Actual | Result |
|---|---|---|---|
| пропуск Test ID | DETECTED | DETECTED | PASS |
| duplicate Test ID | DETECTED | DETECTED | PASS |
| `OrderSend` | DETECTED | DETECTED | PASS |
| `CTrade` | DETECTED | DETECTED | PASS |
| include за root | DETECTED | DETECTED | PASS |
| отсутствующий include | DETECTED | DETECTED | PASS |
| include cycle | DETECTED | DETECTED | PASS |
| duplicate guard | DETECTED | DETECTED | PASS |
| удалён StateRevision gate | DETECTED | DETECTED | PASS |
| удалён ownership gate | DETECTED | DETECTED | PASS |
| удалён persistence gate | DETECTED | DETECTED | PASS |
| ложный MetaEditor PASS | DETECTED | DETECTED | PASS |
| ложный MQL5 runtime PASS | DETECTED | DETECTED | PASS |
| real trading YES | DETECTED | DETECTED | PASS |
| путь вне scope | DETECTED | DETECTED | PASS |

`NEGATIVE_FIXTURES_TOTAL=15`; `NEGATIVE_FIXTURES_CAUGHT=15`; `RESULT=PASS`.
