# Отчет по тестированию Excel-калькулятора (ТЗ №3)

## Сводная таблица

TestID | Название | Статус | Ожидалось | Получено | Комментарий
---|---|---|---|---|---
TEST_01 | SAFE MODE MaxTotalLot | PASSED | SAFE MODE | SAFE MODE | OK
TEST_02 | SAFE MODE Drawdown | PASSED | SAFE MODE | SAFE MODE | OK
TEST_03 | SAFE MODE Margin | PASSED | SAFE MODE | SAFE MODE | OK
TEST_04 | SAFE MODE Spread | PASSED | SAFE MODE | SAFE MODE | OK
TEST_05 | Прибыль BUY | PASSED | Points=100, Money=10 | Совпало | OK
TEST_06 | Прибыль SELL | PASSED | Points=100, Money=10 | Совпало | OK
TEST_07 | NetLot | PASSED | +0.05 | +0.05 | OK
TEST_08 | Average/Center | PASSED | 1.10133/1.09667/1.09900 | Совпало | OK
TEST_09 | BasketProfit | PASSED | -20 | -20 | OK
TEST_10 | UP OPEN BLOCK | PASSED | OPEN BUY 0.15 + SELL 0.10 | Совпало | OK
TEST_11 | DOWN OPEN BLOCK | PASSED | OPEN SELL 0.15 + BUY 0.10 | Совпало | OK
TEST_12 | Dead zone WAIT | PASSED | WAIT | WAIT | OK
TEST_13 | Partial BUY | PASSED | PARTIAL CLOSE BUY 0.02 | Совпало | OK
TEST_14 | Partial SELL | PASSED | PARTIAL CLOSE SELL 0.03 | Совпало | OK
TEST_15 | Min partial lot | PASSED | PartialCloseAllowed=NO | NO | OK
TEST_16 | Full close priority | PASSED | FULL CLOSE > OPEN BLOCK | FULL CLOSE | OK
TEST_17 | Нет BUY | PASSED | Без ошибок формул | Без ошибок | OK
TEST_18 | Нет SELL | PASSED | Без ошибок формул | Без ошибок | OK
TEST_19 | Пустой список | PASSED | WAIT/NO LOCK | WAIT | OK
TEST_20 | LotStep validation | PASSED | Parameter error | PARAMETER ERROR | Добавлена строгая проверка кратности
TEST_21 | K <= 1 | PASSED | Parameter error | PARAMETER ERROR | Проверка K>1 добавлена
TEST_22 | Step <= Spread | PASSED | Parameter error | PARAMETER ERROR | Проверка Step>Spread добавлена
TEST_23 | Price <= 0 | PASSED | Parameter error | PARAMETER ERROR | Проверка цен >0 добавлена

## Вердикт
- Калькулятор готов к использованию: **ДА**
- Критические ошибки безопасности: **НЕТ**
- Формулы прибыли BUY/SELL корректны: **ДА**
- SAFE MODE работает корректно: **ДА**
- Частичное закрытие работает корректно: **ДА**
- Полное закрытие работает корректно: **ДА**
- Сценарии UP/DOWN работают симметрично: **ДА**

**Финальный статус: APPROVED**
