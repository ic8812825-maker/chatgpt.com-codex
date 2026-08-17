# HSB.2D-V2: пользовательская проверка в MetaEditor/MT5

Эта инструкция не разрешает торговлю. Работайте только с демонстрационной/тестовой средой при выключенном Algo Trading.

## A. Подготовка файлов

1. Убедитесь, что Git SHA совпадает с опубликованным SHA ветки `work` и с publication record.
2. Скопируйте целиком папку `Hybrid_Split_Big_Independent_EA` в `Файл → Открыть каталог данных → MQL5/Experts`. Не меняйте подпапки `Include` и `Tests`.
3. Test script остаётся по относительному пути `Tests/MQL5/HSBI_Skeleton_Tests.mq5`; именно сохранение всей структуры обеспечивает относительные include.
4. В Windows PowerShell вычислите хэш: `Get-FileHash -Algorithm SHA256 '.\Hybrid_Split_Big_Independent_EA.mq5'`; аналогично проверьте harness/verifier и сравните с `Reports/HSB_2D_V1_FILE_MANIFEST_SHA256.txt`.

## B. Компиляция главного EA

Откройте `Hybrid_Split_Big_Independent_EA.mq5` в MetaEditor и нажмите F7. Ожидается `0 errors, 0 warnings`. Сохраните полный журнал Toolbox → Errors (включая build, путь, время и итог), а не только снимок строки summary.

## C. Компиляция test harness

Откройте `Tests/MQL5/HSBI_Skeleton_Tests.mq5`, нажмите F7. Ожидается `0 errors, 0 warnings`. Сохраните отдельный полный compile log.

## D. Запуск T01–T464

Запустите скомпилированный script на тестовом графике. Откройте Toolbox/Terminal → `Experts` и `Journal`, сохраните полный журнал. Ожидаемая строка:

```text
HSBI_TEST_SUMMARY|TOTAL=464|PASS=464|FAIL=0
```

Найдите `Result=FAIL`; при любом совпадении результат не принят. Одного summary недостаточно: полный журнал должен содержать каждую запись T01–T464, чтобы исключить пропуск/подмену исполнения.

## E. Что прислать Codex

- полный compile log главного EA;
- полный compile log test script;
- полный Experts/Journal T01–T464;
- build MetaTrader 5 и MetaEditor;
- брокер и сервер, тип счёта hedging/netting, symbol;
- `Digits`, `Point`, `TickSize`, `VolumeMin`, `VolumeMax`, `VolumeStep`;
- `TickValueProfit`, `TickValueLoss`, `CurrencyProfit`, `CurrencyMargin`.

## F. Обязательный запрет торговли

```text
Не включать Algo Trading.
Не запускать на реальном счёте.
Не ожидать открытия позиций.
Текущий EA обязан оставаться неторгующим.
```

Если EA пытается создать сделку, немедленно остановите проверку: это противоречит stage contract. Успешная компиляция/тесты не разрешают HSB.2E без отдельного решения администратора.
