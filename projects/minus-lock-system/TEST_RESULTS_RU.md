# Отчет по тестированию Excel-калькулятора (ТЗ №2)

## Сводка

| TestID | Название | Статус | Комментарий |
|---|---|---|---|
| TEST_01 | SAFE MODE MaxTotalLot | PASSED | Лимит лота блокирует новые входы |
| TEST_02 | SAFE MODE Drawdown | PASSED | Просадка корректно переводит в SAFE |
| TEST_03 | SAFE MODE Margin | PASSED | Низкая маржа переводит в SAFE |
| TEST_04 | SAFE MODE Spread | PASSED | Высокий спред переводит в SAFE |
| TEST_05 | Прибыль BUY | PASSED | Формула корректна |
| TEST_06 | Прибыль SELL | PASSED | Формула корректна |
| TEST_07 | NetLot | PASSED | SUMIF корректен |
| TEST_08 | Average/Center | PASSED | SUMPRODUCT и центр корректны |
| TEST_09 | BasketProfit | PASSED | Сумма BUY/SELL корректна |
| TEST_10 | UP OPEN BLOCK | PASSED | BUY-перекос корректен |
| TEST_11 | DOWN OPEN BLOCK | PASSED | SELL-перекос корректен |
| TEST_12 | Dead zone WAIT | PASSED | Внутри мертвой зоны — WAIT |
| TEST_13 | Partial BUY | PASSED | Округление FLOOR корректно |
| TEST_14 | Partial SELL | PASSED | Округление FLOOR корректно |
| TEST_15 | Min partial lot | PASSED | Лот меньше минимума запрещен |
| TEST_16 | Full close priority | PASSED | FULL CLOSE приоритетнее OPEN BLOCK |
| TEST_17 | Нет BUY | PASSED | Нет #DIV/0! |
| TEST_18 | Нет SELL | PASSED | Нет #DIV/0! |
| TEST_19 | Пустой список | PASSED | Ошибок формул нет |
| TEST_20 | LotStep валидация | FAILED | Нужна строгая валидация кратности |
| TEST_21 | K<=1 | FAILED | Нужна валидация параметра K>1 |
| TEST_22 | Step<=Spread | FAILED | Нужна валидация Step>Spread |
| TEST_23 | Цена <=0 | FAILED | Нужна валидация цен > 0 |

## Вердикт
- Калькулятор готов к использованию: **НЕТ**.
- Критические ошибки безопасности: **НЕТ**.
- Финальный статус: **NEEDS FIXES**.
