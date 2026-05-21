# MANUAL_RU — Полный мануал по работе с MinusLock_Simple_Skew_Compression_Calculator.xlsx

## 1. Назначение калькулятора
`MinusLock_Simple_Skew_Compression_Calculator.xlsx` — это практический Excel-калькулятор для расчёта и проверки системы skew-компрессии минусового замка.

Калькулятор помогает:
- построить сетку уровней Big/Small/Close;
- проверить баланс Main/Opposite;
- контролировать SAFE CLOSE;
- учесть округление лотов по шагу брокера;
- получить понятный человеко-читаемый сценарий по уровням.

---

## 2. Быстрый старт
1. Откройте лист `Calculator`.
2. В блоке `PARAMETERS` задайте `StartLot`, `LotStep`, `Direction`.
3. Проверьте таблицу `LEVEL GRID`.
4. Проверьте блок `DOWN CALCULATION` или `UP CALCULATION` (в зависимости от `Direction`).
5. Проверьте `SUMMARY`.
6. Проверьте `HUMAN-READABLE LEVEL SUMMARY` и лист `HumanSummary`.
7. Убедитесь, что `Status = OK`, `Final System Status = OK`.

---

## 3. Описание листов Excel
- **Calculator** — основной рабочий лист: параметры, уровни, расчёты DOWN/UP, summary, human-block.
- **HumanSummary** — подробная человеко-понятная таблица уровней + итоги.
- **Tests** — встроенные тесты PASS/FAIL.
- **Manual** — краткая инструкция в файле.
- **README** — краткое описание.

---

## 4. Блок PARAMETERS
| Parameter | Назначение |
|---|---|
| StartLot | стартовый лот; все Big/Small/Close считаются от него |
| StepPoints | шаг сетки в пунктах; информационный параметр |
| MaxLevels | количество уровней расчёта |
| LotStep | минимальный шаг лота брокера |
| Direction | DOWN или UP |
| UseRounding | включить округление лотов |
| BigRoundMode | Big округляется вниз |
| SmallRoundMode | Small округляется вверх |
| CloseRoundMode | SAFE-режим закрытия |
| PointValue | стоимость пункта |
| Spread | спред |
| Commission | комиссия |

---

## 5. Блок LEVEL GRID
Стандартная сетка:
- Level 1: Big 90%, Small 30%, TargetSkew 0%, Close 60%
- Level 2: Big 30%, Small 15%, TargetSkew 15%, Close 30%
- Level 3: Big 20%, Small 15%, TargetSkew 10%, Close 0%
- Level 4: Big 10%, Small 10%, TargetSkew 10%, Close 0%
- Level 5: Big 5%, Small 5%, TargetSkew 10%, Close 0%

Смысл:
- **Big** — основной rescue-ордер.
- **Small** — защитный встречный ордер.
- **TargetSkew** — целевой защитный перекос.
- **ManualClose** — ручное переопределение частичного закрытия.

---

## 6. DOWN CALCULATION
Для `Direction = DOWN`:
- Big = BUY
- Small = SELL
- Close = Close Start BUY
- Main = BUY
- Opposite = SELL
- Условие: `Total BUY <= Total SELL`

Пример L1 (`StartLot=1`):
- Open Big BUY 0.90
- Open Small SELL 0.30
- Close Start BUY 0.60
- Start remains 0.40
- Total BUY = 130%
- Total SELL = 130%
- Status = OK

---

## 7. UP CALCULATION
Для `Direction = UP`:
- Big = SELL
- Small = BUY
- Close = Close Start SELL
- Main = SELL
- Opposite = BUY
- Условие: `Total SELL <= Total BUY`

---

## 8. SAFE CLOSE
Формула:

`AutoClose% = MIN(StartBefore%, MAX(0, TotalMainBefore% - TotalOppAfter% + TargetSkew%))`

Просто: калькулятор считает, сколько закрыть стартовой позиции, чтобы Main не стал больше Opposite.

---

## 9. Rounded Lots
- Big Rounded — Big Lot с учётом `LotStep`
- Small Rounded — Small Lot с учётом `LotStep`
- Close Rounded — Close Lot с учётом `LotStep`
- Rounded Main / Opp / Skew — контроль после округления

Ключевое правило: **Rounded Main <= Rounded Opposite**.

---

## 10. SUMMARY
Поля:
- Final Total Main %
- Final Total Opposite %
- Final Skew %
- Final Start Remaining %
- Final Rounded Main Lot
- Final Rounded Opp Lot
- Final Rounded Skew Lot
- Final Rounded Status
- Final System Status

Интерпретация:
- `OK` — расчёт математически безопасен.
- `WARNING` — нужно проверить skew/округление.
- `ERROR` — использовать нельзя.

---

## 11. HUMAN-READABLE LEVEL SUMMARY
Колонки:
- Level, Direction
- Action Big / Big % / Big Lot
- Action Small / Small % / Small Lot
- Close Action / Close % / Close Lot
- Start Remaining % / Start Remaining Lot
- Total Main % / Total Opposite % / Skew %
- Rounded Main / Opp / Skew
- Status
- Human Comment

Это главный «человеческий» блок: показывает по каждому уровню действия и итоговый баланс.

---

## 12. Как читать Status
Логика:
- `ERROR` — нарушены правила безопасности (параметры, баланс, rounding constraints).
- `WARNING` — целевой skew не достигнут (с учётом tolerance).
- `OK` — уровень корректен.

---

## 13. Как читать Human Comment
`Human Comment` — текстовое резюме уровня:
- направление (DOWN/UP),
- что открыть (Big/Small),
- что закрыть,
- остаток стартовой позиции,
- итоговый Main/Opp/Skew,
- статус.

---

## 14. Пример для StartLot = 1
- Sum Big = 1.55
- Sum Small = 0.75
- Sum Close = 0.90
- Final Rounded Main = 1.65
- Final Rounded Opp = 1.75
- Final Skew = 0.10
- Status = OK

## 15. Пример для StartLot = 2
- Sum Big = 3.10
- Sum Small = 1.50
- Sum Close = 1.80
- Final Rounded Main = 3.30
- Final Rounded Opp = 3.50
- Final Skew = 0.20
- Status = OK

## 16. Пример для StartLot = 5
- Sum Big = 7.75
- Sum Small = 3.75
- Sum Close = 4.50
- Final Rounded Main = 8.25
- Final Rounded Opp = 8.75
- Final Skew = 0.50
- Status = OK

---

## 17. Как проверять правильность
Признаки правильного расчёта:
1. DOWN уровни 1–5 = OK
2. UP уровни 1–5 = OK
3. Final System Status = OK
4. Human Summary не содержит нулей вместо лотов
5. Human Comment показывает нормальный текст
6. Rounded Main <= Rounded Opposite
7. Total Main <= Total Opposite

---

## 18. Частые ошибки
- `StartLot <= 0`
- слишком крупный `LotStep`
- Big меньше Small
- ManualClose больше остатка Start-позиции
- Rounded Main > Rounded Opposite
- Final Status = ERROR

---

## 19. Что нельзя делать
- Нельзя использовать расчёт при `Status = ERROR`.
- Нельзя игнорировать `WARNING`.
- Нельзя менять Big/Small без проверки `Summary`.
- Нельзя считать первый плюс частью разруливания.
- Нельзя использовать файл, если Human Summary показывает ошибки.

---

## 20. Финальный чеклист пользователя
- [ ] Параметры заполнены корректно
- [ ] Direction выбран правильно
- [ ] DOWN/UP таблица без ошибок
- [ ] Summary показывает адекватные итоги
- [ ] HumanSummary показывает реальные лоты и действия
- [ ] Tests = PASS
- [ ] Final System Status = OK

## ПАРАМЕТРЫ
## СЕТКА УРОВНЕЙ
## DOWN
## UP
## SUMMARY
## HUMAN SUMMARY

### StartLot = 1
### StartLot = 2
### StartLot = 5

