# HSB.2D-V2: точная пользовательская процедура

1. Сверить `git rev-parse HEAD` с publication record и проверить SHA-256 R5 manifest/seal.
2. Скопировать всю папку проекта с сохранением структуры в чистый каталог MQL5.
3. Использовать только demo/test account; выключить Algo Trading и AutoTrading.
4. Сохранить MT5/MetaEditor build и broker properties: server, account mode, symbol, digits, point, tick size, volume min/max/step, tick values и currencies.
5. Скомпилировать главный `.mq5`, затем `Tests/MQL5/HSBI_Skeleton_Tests.mq5`; для каждого требуется `0 errors, 0 warnings`.
6. Запустить harness T01–T464. Сохранить полные Experts и Journal без фильтрации/обрезки.
7. Проверить ровно один PASS каждого T001–T464, summary 464/464/0 и отсутствие trade request markers.
8. При любой заявке немедленно остановить терминал, сохранить evidence и установить FAIL.
9. Запустить offline analyzer R5 с четырьмя логами и ожидаемым SHA. Не использовать реальный счёт.
