# DG01 — native MQL5 verification plan

MQL5_COMPILE=NOT_RUN
MQL5_NATIVE_TESTS=NOT_RUN
NATIVE_VERIFIED=NO

## Подготовленный пакет

`Tests/Native/HSBI_DG01_harness.mq5`, codec cases/goldens и test-only identity candidate. E1 проверяет replay, все29 immutable fields, отдельные signed components, одинаковый Net, source changes, unknown facts/provider/registry, zero и nonfinite. E2 проверяет allocation vector, negative/over-allocation, exhausted/foreign source, duplicate и unknown authority. E3 — NaN/negative margin/Infinity/fill volume, partial, foreign owner, missing actual confirmation. E4 — один FAR, разные FAR в слотах, physical alias observation, independent/copied expected, отсутствующий provider/unknown source. E5 — independent F64Z scalar/record bytes, UTF8, ulong>2^53, canonical zero, min normal/subnormal/max finite, malformed/trailing/unknown wire, roundtrip; T17 — только compatibility probes.

Группы помечены scope: CURRENT_SOURCE_EXPECTED_DEFECT, PROPOSED_V2, LOCAL_EQUALITY, OBSERVATION_NOT_PROVIDER_PROOF и codec test subject. Native FAIL старого дефектного source не исправляется изменением expected. Copied expected observation ожидаемо допускается helper и не является доказательством полного NewFar bypass. Alias probe доказывает одинаковый physical identifier, но **не** автоматически разрешает роль FAR в initialBuy: slot policy ещё требует решения.

Goldens получены отдельным `HSBI_DG01_goldens.py` через literal field order, integer framing и struct.pack; нативный encoder их не вычисляет. Скалярные битовые ожидаемые значения заданы буквально. Decode/malformed probes получают independent golden wire, а не байты собственного encoder; encoder и decoder проверяются раздельно. Генераторы NaN/Infinity должны быть подтверждены как nonfinite; их сбой — INFRASTRUCTURE_ERROR, не kill. Source/value shape и masked unknown отличаются от произвольной самосогласованной authority.

## PowerShell compile launcher

`Tests/Native/HSBI_DG01_compile_isolated.ps1` требует явные MetaEditorPath, TerminalPath, DataPath. Проверяет существование/имена выбранных exe, наличие MQL5, запрещает reparse paths и существующий OutputRoot, создаёт новую изолированную копию только Include/test dependencies. Исходники хешируются до/после. DataPath не копируется, account/config/token files не читаются; terminal64.exe никогда не запускается. Только MetaEditor compile, полный compiler log/версия/hash/process exit/EX5 hash и машинный JSON. Отсутствующий или нераспознанный log не считается успехом; timeout — infrastructure error. Warnings сохраняются и требуют review.

Пример на отдельной офлайн Windows-машине, без реальных счетов:

```powershell
powershell.exe -NoProfile -File .\Tests\Native\HSBI_DG01_compile_isolated.ps1 -MetaEditorPath 'C:\MT5-Test\MetaEditor64.exe' -TerminalPath 'C:\MT5-Test\terminal64.exe' -DataPath 'C:\MT5-Test-Data'
```

Не использовать ExecutionPolicy bypass. Launcher не запускался в текущей Linux-среде: pwsh и MetaEditor не найдены в PATH/searched directories. Его синтаксическая/native совместимость должна быть проверена на Windows, не объявляется PASS по static review.

## Отдельный ручной runtime

После успешной компиляции владелец на чистой isolated/offline MT5 installation без реальных accounts/других EA переносит только Stage project в MQL5/Scripts и запускает именно Script. Автоторговля выключена. Не запускать production EA, не подключать history/provider и не импортировать account/config из выбранного DataPath. Если терминал не способен безопасно выполнить скрипт offline — оставить NOT_RUN и подготовить отдельную sandbox-среду, а не подключать реальный счёт.

Сохранить версию MT5, UTC, все source hashes из compile report и полные строки `DG01|TestID|PASS/FAIL|Scope`, generator infrastructure markers и `[HSBI_DG01_NATIVE_RESULT]`. Отсутствие маркера, crash или skipped conditional cases — не полный результат. Script Print не управляет OS exit code: нужны compiler/process exits **и** per-test outputs. COMPILED_ONLY не преобразуется в NATIVE_VERIFIED.

Нативная приёмка полного EA и выбранного production codec остаётся отдельным обязательным шагом после approval; тестовый R0H codec не становится production implementation.
