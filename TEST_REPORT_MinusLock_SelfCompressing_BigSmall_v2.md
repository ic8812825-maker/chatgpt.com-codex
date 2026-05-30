# TEST REPORT: MinusLock_SelfCompressing_BigSmall_v2.xlsx

Дата проверки: 2026-05-30
Файл: `MinusLock_SelfCompressing_BigSmall_v2.xlsx`
Приоритет спецификации: раздел мануала `27. Уточнения v2: недвусмысленные правила исполнения`.

## 1. Область проверки

Проверялись:

- структура Excel-файла;
- лист `Settings` и редактируемые параметры;
- формулы Big и Small;
- направления `Trend_UP` и `Trend_DOWN`;
- BIG_SIDE: закрытие Big/Small, `NetProfit`, денежный бюджет хвоста, резерв;
- SMALL_SIDE: закрытие Small, 22% Big, 78% RemainBig, новый хвост;
- защита от `#DIV/0!`, отрицательных лотов и отрицательного бюджета;
- `DUAL_TAIL`, блокировка нового полноценного уровня, `WARNING`/`DANGER`;
- маржа, баланс, резерв;
- листы `Risk_Analysis`, `Tests`, `Manual`, `Examples`;
- отсутствие накопления Small.

## 2. Исправления, выполненные по результатам проверки

1. Исправлена формула `Costs` на листах `Calculator`, `Trend_UP`, `Trend_DOWN`: теперь она соответствует v2-мануалу и считается как `Commission + SpreadCost + SlippageCost`, а не как умножение затрат на суммарный лот.
2. Усилен расчёт `Status`: добавлены проверки `LossPerLotToClose <= 0`, `ActualBigRatio > MaxBigRatio`, `ActualSmallRatio > MaxSmallRatio`.
3. Лист `Tests` заменён на подробную таблицу с колонками `Test ID`, `Test Name`, `Input`, `Expected`, `Actual`, `Formula Checked`, `Status`, `Comment` и 29 проверками.
4. Добавлен отдельный pytest-набор `tests/excel/test_minuslock_bigsmall_v2.py`, который проверяет workbook-структуру, v2-формулы и независимые числовые сценарии.

## 3. Подробные результаты тестов

| # | Название | Что проверялось | Входные данные | Ожидание | Факт / Excel-ячейка | Статус | Комментарий |
|---:|---|---|---|---|---|---|---|
| 1 | Структура листов | Строгий состав и порядок листов | Workbook sheets | `Settings`, `Calculator`, `Trend_UP`, `Trend_DOWN`, `Risk_Analysis`, `Tests`, `Manual`, `Examples` | `wb.sheetnames` совпадает | PASS | Проверено через `openpyxl`. |
| 2 | Settings | Наличие всех параметров и v2 defaults | `Settings!A2:B17` | Все 16 параметров есть; `BigRatio=1.15`, `SmallRatio=0.38`, `CloseFarShare=0.20`, `ReserveShare=0.80`, `CloseBigOnSmall=0.22`, `RemainBigOnSmall=0.78`, `MaxBigRatio=1.20`, `MaxSmallRatio=0.45` | Значения совпадают | PASS | Ячейки `B2:B17` числовые и редактируемые. |
| 3 | Пересчёт зависимых формул Settings | Формулы ссылаются на Settings | Изменяемые параметры `Settings!B3:B17` | Зависимые формулы используют ссылки на Settings | `Calculator!G2`, `J2`, `T2`, `X2`, `AL2`, `AQ2` содержат ссылки `Settings!$B$...` | PASS | Формулы видны и не заменены статическими числами. |
| 4 | Big для FarStart 1.00 | `BigLotRaw = FarStartLot × 1.15` | `FarStartLot=1.00`, `BigRatio=1.15` | `BigLotRaw=1.15`, `BigLot=1.15` | Модель и формула `Calculator!F2/G2` дают 1.15 | PASS | Округление при `LotStep=0.01` не меняет результат. |
| 5 | Big для FarStart 0.80 | `BigLotRaw = 0.80 × 1.15` | `FarStartLot=0.80` | `BigLotRaw=0.92`, `BigLot=0.92` | Независимая модель даёт 0.92 | PASS | Проверен второй обязательный пример. |
| 6 | Small formula | `SmallLotRaw = BigLot × 0.38` | `BigLot=1.15`, `SmallRatio=0.38`, `LotStep=0.01` | `SmallLotRaw=0.437`, `SmallLot=0.44` | Модель и формулы `Calculator!I2/J2` дают 0.44 | PASS | `SmallLot / BigLot = 0.3826 <= 0.45`. |
| 7 | Trend_UP directions | Направления на 10 уровнях | `FarDirection=SELL` | `BigDirection=BUY`, `SmallDirection=SELL` | `Trend_UP!E2:E11` используют `IF(C="SELL","BUY","SELL")`, `H=C` | PASS | Формулы сохраняют правило для всех уровней. |
| 8 | Trend_DOWN directions | Направления на 10 уровнях | `FarDirection=BUY` | `BigDirection=SELL`, `SmallDirection=BUY` | `Trend_DOWN!E2:E11` используют `IF(C="SELL","BUY","SELL")`, `H=C` | PASS | Формулы сохраняют правило для всех уровней. |
| 9 | BIG_SIDE close Big/Small | Обязательное закрытие уровня | BIG_SIDE rows | `Close Big=100%`, `Close Small=100%` | `Calculator!AN=1`, `Calculator!AO=1` для BIG_SIDE | PASS | Big/Small текущего уровня не остаются открытыми. |
| 10 | Отсутствие накопления Small | Small не переносится между уровнями | BIG_SIDE и SMALL_SIDE | `SmallClosedPercent=1`, нет `SmallRemain` | `Calculator!AO2:AO11 = 1`; `OpenLotsAfter` не содержит Small | PASS | Накопления Small не обнаружено. |
| 11 | BIG_SIDE NetProfit с затратами | v2 formula | `ProfitBig=200`, `LossSmall=60`, `Commission=5`, `Spread=3`, `Slippage=2` | `NetProfit=130` | Модель: `200-60-5-3-2=130`; Excel pattern `S=N-P-R`, `R=B13+B14+B15` | PASS | Ошибка per-lot costs исправлена. |
| 12 | Денежный бюджет хвоста | `CloseFarBudget = NetProfit × 0.20` | `NetProfit=130` | `CloseFarBudget=26` | Модель и `Calculator!T` дают 26 | PASS | 20% трактуется как денежный бюджет. |
| 13 | Резерв BIG_SIDE | `ReserveAdd = NetProfit × 0.80` | `NetProfit=130` | `ReserveAdd=104` | Модель и `Calculator!X` дают 104 | PASS | Резерв не прибавляется к балансу второй раз. |
| 14 | CloseFarLot | Денежное закрытие хвоста | `FarStart=1.00`, `Budget=26`, `LossPerLot=100` | `CloseFarLot=0.26`, `FarRemain=0.74` | Модель и формула `Calculator!V/W` совпадают | PASS | Не закрывается автоматически 20% лота; закрывается 0.26 лота по бюджету. |
| 15 | Защита от деления на ноль | `LossPerLotToClose = 0` | `LossPerLot=0` | Нет `#DIV/0!`, `CloseFarLot=0`, `Status=WARNING` | `Calculator!V` содержит `IFERROR`; `AQ` предупреждает при `U<=0` | PASS | Деление на ноль заблокировано. |
| 16 | Отрицательный NetProfit | Защита от отрицательных бюджетов | `ProfitBig=100`, `LossSmall=120`, `Costs=10` | `NetProfit=-30`, `CloseFarBudget=0`, `ReserveAdd=0`, `CloseFarLot=0`, `Status=WARNING/DANGER` | Модель и формулы `T/X/V/AQ` соответствуют | PASS | Отрицательные лоты и бюджеты не появляются. |
| 17 | SMALL_SIDE close rules | `Close Small=100%`, `Close Big=22%`, `Remain Big=78%` | `BigLot=1.15` | `CloseBig=0.253`, `RemainBig=0.897` | `Calculator!AL=G×0.22`, `AM=G-AL`, `AO=1` | PASS | Small закрывается полностью. |
| 18 | NewFar after SMALL_SIDE | Остаток Big становится хвостом | `RemainBig=0.897` | `NewFarStart=0.897`, `NewFarDirection=BigDirection` | `Calculator!AG=AM`, `AF=E` | PASS | Направление нового хвоста соответствует Big. |
| 19 | Самосжатие SMALL_SIDE | `F_next = F × 1.15 × 0.78` | `F=1.00`, `F=0.897` | `0.897`, `0.804609` до округления | Независимая модель подтверждает уменьшение хвоста | PASS | При лотовом округлении фактические значения могут немного отличаться, но хвост уменьшается. |
| 20 | DUAL_TAIL | Старый и новый хвост одновременно | `OldFarRemainLot>0`, `NewFarStartLot>0` | `Status=DUAL_TAIL` | `Calculator!AK=AND(AJ>0,AG>0)`, `AQ=DUAL_TAIL` | PASS | Двуххвостовая структура обнаруживается. |
| 21 | STOP / block next level | Блокировка нового уровня | `Status=DUAL_TAIL` или `DANGER` | `NewFullLevelAllowed=NO` | `Calculator!AP` возвращает `NO` | PASS | Новый полноценный уровень запрещается. |
| 22 | Маржа | `OpenLotsBefore` и `MarginBefore` | `Far=1.00`, `Big=1.15`, `Small=0.44`, `MarginPerLot=1000` | `OpenLotsBefore=2.59`, `MarginBefore=2590` | Формулы `AB=D+G+J`, `AD=AB×MarginPerLot` | PASS | После BIG_SIDE `MarginAfter = FarRemain × MarginPerLot`. |
| 23 | Баланс | Нет двойного учёта резерва | `BalanceBefore=0`, `NetProfit=130`, `Reserve=104` | `BalanceAfter=130`, не 234 | `Calculator!AA=Z+S` | PASS | Резерв — аналитическая часть прибыли, а не дополнительная прибыль. |
| 24 | Резерв | BIG_SIDE и SMALL_SIDE reserve rules | Positive/negative `NetProfit` | BIG_SIDE 80%; SMALL_SIDE positive 50%; negative 0 | `Calculator!X/Y` соответствуют | PASS | Резерв не используется в формулах Big/Small. |
| 25 | Лимиты Big/Small ratios | `ActualBigRatio` и `ActualSmallRatio` | Ratio breach | `Status=DANGER` при превышении лимитов | `Calculator!AQ` проверяет `G/D > MaxBigRatio` и `J/G > MaxSmallRatio` | PASS | Проверки лимитов добавлены. |
| 26 | LotStep rounding | Округление лотов | `LotStep=0.01`, `0.10`, `0.001` | Лоты кратны `LotStep`; отрицательных лотов нет | Формулы `G/J = ROUND(raw/LotStep)*LotStep` + `MAX(0, ...)` | PASS | Проверено независимой моделью. |
| 27 | Trend_UP 10 уровней | Полный сценарий вверх | `Trend_UP!2:11` | 10 уровней, направления корректны, Small не копится, маржа/резерв/статус считаются | Формулы листа совпадают с `Calculator` | PASS | Уровни содержат BIG_SIDE и SMALL_SIDE сценарии. |
| 28 | Trend_DOWN 10 уровней | Полный сценарий вниз | `Trend_DOWN!2:11` | 10 уровней, направления корректны, Small не копится, маржа/резерв/статус считаются | Формулы листа совпадают с `Calculator` | PASS | Уровни содержат BIG_SIDE и SMALL_SIDE сценарии. |
| 29 | Examples | Обязательные примеры | `Examples!A:D` | BIG_SIDE пример и SMALL_SIDE пример присутствуют | Найдены `Пример 1. Тренд вверх` и `Пример 2. Разворот вниз` | PASS | Описаны закрытие Big/Small и новый BUY-хвост. |
| 30 | Risk_Analysis | Итоговые показатели | `Risk_Analysis!A:C` | Все 12 метрик присутствуют и ссылаются на `Calculator` | `SUM`, `LOOKUP`, `MAX`, `COUNTIF` formulas | PASS | Сводка риска связана с расчётным листом. |
| 31 | Manual sheet | v2 anchors | `Manual!A:A` | `Close Big = 100%`, `Close Small = 100%`, `денежный`, `DUAL_TAIL`, `STOP` и др. | Все required texts найдены | PASS | Приоритетный v2-раздел встроен в Excel. |
| 32 | Tests sheet | Подробная таблица Tests | `Tests!A:H` | Колонки `Test ID..Comment`, минимум 25 тестов | 29 тестов, все `PASS` | PASS | Лист Tests соответствует требованию. |

## 4. Уровневый отчёт Trend_UP

Лист `Trend_UP` содержит 10 уровней. Проверка выполнена по формулам листа и независимой модели:

| Level | Проверка | Результат |
|---:|---|---|
| 1 | `FarDirection=SELL`, `BigDirection=BUY`, `SmallDirection=SELL`, BIG_SIDE закрывает Big/Small 100% | PASS |
| 2 | Направления сохраняются, CloseFarBudget денежный, ReserveAdd считается | PASS |
| 3 | Направления сохраняются, CloseFarBudget денежный, ReserveAdd считается | PASS |
| 4 | SMALL_SIDE закрывает Small 100%, Big 22%, RemainBig 78%, проверяет старый хвост | PASS |
| 5 | Следующий уровень использует новый хвост или блокируется при опасном статусе | PASS |
| 6 | Big/Small считаются от текущего хвоста, Small не накапливается | PASS |
| 7 | Маржа считается от открытых лотов, резерв накапливается | PASS |
| 8 | SMALL_SIDE повторно проверяет DUAL_TAIL | PASS |
| 9 | BIG_SIDE завершает уровень полностью | PASS |
| 10 | Итоговые формулы статуса, маржи и резерва присутствуют | PASS |

## 5. Уровневый отчёт Trend_DOWN

Лист `Trend_DOWN` содержит 10 уровней. Проверка выполнена по формулам листа и независимой модели:

| Level | Проверка | Результат |
|---:|---|---|
| 1 | `FarDirection=BUY`, `BigDirection=SELL`, `SmallDirection=BUY`, BIG_SIDE закрывает Big/Small 100% | PASS |
| 2 | SMALL_SIDE закрывает Small 100%, Big 22%, RemainBig 78%, проверяет старый хвост | PASS |
| 3 | Следующий уровень пересчитывает Big/Small от текущего хвоста | PASS |
| 4 | Денежный режим закрытия хвоста сохраняется | PASS |
| 5 | Резерв считается отдельно от баланса | PASS |
| 6 | SMALL_SIDE повторно проверяет DUAL_TAIL | PASS |
| 7 | Small не переносится как открытая позиция | PASS |
| 8 | Маржа до/после считается от открытых лотов | PASS |
| 9 | Статус ловит WARNING/DANGER условия | PASS |
| 10 | Итоговые формулы статуса, маржи и резерва присутствуют | PASS |

## 6. Проверка обязательных команд

### 6.1. Workbook-specific pytest

Команда:

```bash
python -m pytest tests/excel/test_minuslock_bigsmall_v2.py -q
```

Результат:

```text
12 passed in 1.07s
```

Статус: PASS.

### 6.2. Openpyxl smoke-test из задания

Команда:

```bash
python - <<'PY'
from openpyxl import load_workbook
wb = load_workbook("MinusLock_SelfCompressing_BigSmall_v2.xlsx", data_only=False)
expected_sheets = ["Settings", "Calculator", "Trend_UP", "Trend_DOWN", "Risk_Analysis", "Tests", "Manual", "Examples"]
assert wb.sheetnames == expected_sheets
manual = "\n".join(str(wb["Manual"].cell(r, 1).value or "") for r in range(1, wb["Manual"].max_row + 1))
for text in ["Close Big = 100%", "Close Small = 100%", "Основной режим системы", "денежный", "20% — это денежный бюджет", "Close Big = 22%", "Remain Big = 78%", "DUAL_TAIL", "STOP"]:
    assert text in manual, f"Manual missing: {text}"
print("smoke validation ok")
PY
```

Результат:

```text
smoke validation ok
```

Статус: PASS.

### 6.3. Full repository pytest

Команда:

```bash
python -m pytest
```

Результат:

```text
66 passed, 1 failed
```

Статус: WARNING.
Комментарий: новый workbook-specific набор `tests/excel/test_minuslock_bigsmall_v2.py` прошёл полностью. Единственный FAIL находится в старом тесте `tests/excel/test_workbook_generation.py::test_workbook_generation_and_required_fields`, который ожидает лист `Excel_Audit` в другом workbook (`adaptive_lock_ev_calculator.xlsx`) и не относится к `MinusLock_SelfCompressing_BigSmall_v2.xlsx`.

## 7. Ручные проверки Excel: статус

Среда выполнения headless, поэтому открыть файл в GUI Excel/LibreOffice невозможно. Вместо этого выполнены программные эквиваленты через `openpyxl`:

| Проверка | Статус | Комментарий |
|---|---|---|
| Формулы видны | PASS | Workbook открыт с `data_only=False`, формулы сохранены как строки. |
| Нет статических чисел вместо формул в расчётных колонках | PASS | Проверены ключевые formula anchors. |
| Нет `#DIV/0!` в формуле CloseFarLot | PASS | Используется `IFERROR`, статус предупреждает при `LossPerLotToClose<=0`. |
| Нет отрицательных лотов | PASS | Формулы используют `MAX(0, ...)`. |
| Нет накопления Small | PASS | `SmallClosedPercent=1`, `OpenLotsAfter` не включает Small. |
| Цветовая подсветка | PASS | Условное форматирование и fills присутствуют. |
| Все листы читаемы | PASS | Все листы загружены через `openpyxl`. |
| Settings пересчитывает Calculator | PASS | Формулы ссылаются на `Settings!$B$...`; фактический пересчёт произойдёт при открытии Excel. |
| Risk_Analysis связан с Calculator | PASS | Метрики используют `SUM`, `LOOKUP`, `MAX`, `COUNTIF` по `Calculator`. |

## 8. Итоговый Summary

```text
Всего тестов в подробном отчёте: 32
PASS: 32
FAIL: 0 для MinusLock_SelfCompressing_BigSmall_v2.xlsx
WARNING: 1 внешний full-pytest warning по старому нерелевантному тесту другого workbook
Критические ошибки: 0 после исправлений
Исправленные ошибки: 3
  1. Costs приведён к v2-формуле Commission + SpreadCost + SlippageCost.
  2. Status теперь ловит LossPerLotToClose <= 0 и превышение лимитов Big/Small.
  3. Tests sheet расширен до подробного формата с 29 тестами.
Оставшиеся риски: GUI-проверка в Excel не выполнена из-за headless-среды; формулы проверены программно.
Готовность калькулятора: ГОТОВ к ревью по v2-логике; workbook-specific тесты PASS.
```

## 9. Итоговый вывод

Калькулятор `MinusLock_SelfCompressing_BigSmall_v2.xlsx` после исправлений соответствует v2-логике:

```text
BIG_SIDE:
    Big закрыт 100%
    Small закрыт 100%
    NetProfit посчитан с затратами
    20% NetProfit идёт как денежный бюджет на хвост
    80% NetProfit идёт в резерв

SMALL_SIDE:
    Small закрыт 100%
    Big закрыт 22%
    RemainBig 78% становится новым хвостом
    старый хвост проверяется
    DUAL_TAIL блокирует новый полноценный уровень
```
