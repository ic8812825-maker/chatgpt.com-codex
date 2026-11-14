# PROPOSED — воспроизведение MQL5 на Windows

MQL5_COMPILE=NOT_RUN; MQL5_NATIVE_TESTS=NOT_RUN; NATIVE_VERIFIED=NO.
В Linux `command -v wine` и `command -v metaeditor64` не нашли исполняемых файлов; g++ доступен.

1. Использовать отдельную установку MT5 без торгового подключения. Не включать Algo Trading. Сохранить полный проект с BASE_SHA из baseline.json в MQL5/Scripts/HSBI_Close_Project, сохранив относительные Include.
2. PowerShell, подставив фактические пути:

```powershell
$mtEditor = 'C:\Program Files\MetaTrader 5\metaeditor64.exe'
$harness = 'C:\MT5-Offline\MQL5\Scripts\HSBI_Close_Project\Tests\Close\native_close.mq5'
$compileLog = 'C:\MT5-Offline\hsbi-close-compile.log'
Start-Process -FilePath $mtEditor -ArgumentList @('/compile:"' + $harness + '"', '/log:"' + $compileLog + '"') -Wait
Get-Content -LiteralPath $compileLog
Get-FileHash -Algorithm SHA256 -LiteralPath $harness
```

3. Проверить compiler log: strict compile, errors=0; exit code запуска редактора не заменяет лог компилятора. Не запускать EA. В Navigator → Scripts запустить только native_close на offline chart; harness вызывает чистые предикаты и Print. Сохранить реальные строки `HSBI_CLOSE` из MQL5/Logs, compiler build, terminal build, хэши headers, времена и BASE_SHA в новом evidence каталоге.
4. Нынешние отрицательные тесты ожидают обнаружение известных дефектов (FAIL); не менять expected ради PASS. Три native checks не покрывают весь acceptance. Для R1.1 отдельно перенести все 14 P0 и дополнительные векторы из матрицы, provider и crash/concurrency проверки.

Нативный harness подготовлен, но не скомпилирован и не исполнен здесь. Он не проверяет broker/history authenticity или durable restart.
