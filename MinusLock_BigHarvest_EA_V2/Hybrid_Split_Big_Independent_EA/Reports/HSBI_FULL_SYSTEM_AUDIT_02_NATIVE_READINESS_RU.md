# AUDIT 02 — native readiness и инструкция Windows

Свежий поиск PATH и каталогов `/opt`, `/workspace`, `/usr/local/bin` сохранён в `Tests/Evidence/HSBI_FULL_SYSTEM_AUDIT_02_NATIVE_ENVIRONMENT_FRESH.json`. Ни MetaEditor, ни MT5, ни Wine не найдены в этой ограниченной области. Это не поиск всех файлов машины.

MQL5_COMPILE=NOT_RUN
MQL5_NATIVE_TESTS=NOT_RUN

Минимальный неторговый Script: `Tests/Reference/HSBI_FULL_SYSTEM_AUDIT_02_native.mq5`. Он подключает реальные headers; проверки equality/vector/domain. Нет OrderSend/CTrade/History/AccountInfo/WebRequest/persistence. Пакет не содержит полного native покрытия 10 P0: нужны ещё Reserve/NewFar/context/nonfinite vectors. Непроверенная компилируемость и неполнота native пакета — открытые работы, не PASS.

На отдельной Windows-среде владельца:

1. Сверить SHA baseline и хеши source/harness, сохранить версию MetaEditor. Использовать изолированную копию всего HSBI с относительными include.
2. Запустить фактически установленный `MetaEditor64.exe /compile:"<HSBI>\Tests\Reference\HSBI_FULL_SYSTEM_AUDIT_02_native.mq5" /log:"<audit-output>\HSBI_FULL_SYSTEM_AUDIT_02_compile.log"`. Сохранить process exit, compiler diagnostics/warnings и SHA каждого входа. Exit0 сам по себе не заменяет compiler log.
3. Только после успешной компиляции запустить этот неторговый Script в изолированном терминале без связи с реальным счётом, без автоторговли и без подключённых других EA. Не запускать production EA для проверки исполнения.
4. Сохранить все строки `AUDIT02|TestID|PASS/FAIL`, итог FAILURES, версию терминала, UTC, source hashes. FAIL неизменённого source ожидаем; не исправлять expected для получения PASS. В MQL Script Print FAIL не гарантирует ненулевой terminal process exit — нужны оба вида результата.
5. До production-приёмки добавить native NaN/Infinity/domain/ulong overflow, SourceKey/29-field equality/codec fixtures, full main compile и реальный MQL version-specific результат.

Python Fraction и LP64 C++ extraction не подменяют эту процедуру. Нет доказательства native ABI, double canonicalization, terminal string/UTF8 или broker calculations. Не предпринимать сетевые/account operations для аудита.
