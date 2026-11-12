# AUDIT 02 — фактические запуски и границы

Исходный30-case набор:17 PASS/13 FAIL. Расширенный38-case набор:19 PASS/19 FAIL. Они перекрываются, не суммируются. Rational23/23, proposed ledger22/22;6 различных source mutations обнаружены. Package positive и8 negative probes PASS. Native MQL5 NOT_RUN.

| Набор | Exit | PASS | FAIL | Классификация |
|---|---:|---:|---:|---|
|R7|1|57|5|EXPECTED_HISTORICAL_FAILURE|
|R0|1|35|46|EXPECTED_HISTORICAL_FAILURE|
|R8|1|None|None|SCOPE_POLICY_FAILURE_REVIEW_DETAILS|
|R10|1|None|None|SCOPE_POLICY_FAILURE_REVIEW_DETAILS|
|C1|0|840|0|PASS|
|C2|0|1264|0|PASS|
|R0F|0|116|0|PASS|
|R0G|0|128|0|PASS|
|R0H|0|148|0|PASS|

Null/None означает отсутствие сопоставимого PASS/FAIL counter, не ноль. R8/R10 сами выводят RESULT=FAIL, EXPECTED=EXECUTED48/67 и FINDINGS=1; полный finding — scope3test MQL paths.

Команды/UTC/process exits/stdout/stderr: `SOURCE_TESTS_FRESH.json`, `SOURCE_TESTS_EXTENDED.json`, `REGRESSIONS.json`; у C1/C2 полные rows в отдельных new output files. Source/runner/fixture hashes сохранены в этих evidence и VERIFICATION. Rational vectors выполняются из указанного `verify.py --run`; ledger через `ledger_tests.py`. Синтаксис в recovery inventory не является compiler verification.

Source mutations: ECON_PRICE, ECON_VOLUME, ALLOC_EVENT, TX_OWNERSHIP, TX_ACTION, MONEY_NEGATIVE. Для каждой original positive/negative PASS, mutant positive PASS, mutant causal negative нарушает literal expected. Эти шесть не покрывают все отсутствующие guards P0; surviving mutations в этом небольшом каталоге0, infrastructure errors0.

Архивированные source results первой попытки не подменены итогами: исходные bytes находятся в RECOVERY_ARCHIVE, связи хешей проверяет package checker. Development failures архивирования/генератора раскрыты в DEVELOPMENT_FAILURES; ни один не посчитан kill.

Production74 sources и все1416 baseline-файлов сверяются по Git blob/mode и SHA256. Нет отправки ордеров, production migration или persistence backend. Broker fixture keys не являются данными реального счёта.

Воспроизведение (из project root):
```text
PYTHONDONTWRITEBYTECODE=1 python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_02_verify.py --run
PYTHONDONTWRITEBYTECODE=1 python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_02_verify.py --run --extended
PYTHONDONTWRITEBYTECODE=1 python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_02_ledger_tests.py
PYTHONDONTWRITEBYTECODE=1 python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_02_regressions.py
PYTHONDONTWRITEBYTECODE=1 python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_02_build.py
PYTHONDONTWRITEBYTECODE=1 python Tests/Static/HSBI_FULL_SYSTEM_AUDIT_02_package.py
```
Re-execution writing outputs допустимо только в disposable copy/new scope, не поверх опубликованного evidence. Последняя команда read-only. Для обновлённых результатов отдельно требуются `--seal`, `--probes`; они не подтверждают правильность системы. После публикации здесь ничего не перезаписывается.
