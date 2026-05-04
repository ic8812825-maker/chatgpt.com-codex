# Excel-калькулятор следующего шага (Minus Lock)

Файл: `MinusLock_NextStep_Calculator.xlsx`

## Что делает
Калькулятор рассчитывает следующий шаг разруливания замка для двух сценариев:
- движение цены вверх;
- движение цены вниз.

Приоритет решений:
1. SAFE MODE
2. FULL CLOSE
3. PARTIAL CLOSE
4. OPEN BLOCK
5. WAIT

## Структура листов
- `01_INPUT` — входные параметры брокера, системы и рынка.
- `02_POSITIONS` — открытые позиции.
- `03_CORE_CALC` — ядро расчетов корзины.
- `04_SCENARIO_UP` — расчет сценария вверх.
- `05_SCENARIO_DOWN` — расчет сценария вниз.
- `06_ACTIONS` — таблица действий.
- `07_TESTS` — тестовые кейсы.
- `08_REPORT` — итоговый отчет.
- `09_USER_GUIDE` — пошаговая инструкция пользователя.
- `10_PRECHECK` — предторговый чек-лист GO/STOP.
- `11_DECISION_LOG` — журнал решений системы.
- `12_ACTION_LOG` — журнал действий пользователя.
- `13_ANALYTICS` — аналитика дисциплины и исполнения.

## Как использовать
1. Заполните `01_INPUT`.
2. Введите/обновите позиции в `02_POSITIONS`.
3. Проверьте `03_CORE_CALC` (SafeMode, BasketProfit, WorstSide).
4. Смотрите решения в `04_SCENARIO_UP` и `05_SCENARIO_DOWN` (`FinalDecision`).
5. Используйте `06_ACTIONS` и `08_REPORT` для итогового решения.

## Ограничения
- Калькулятор не отправляет ордера брокеру.
- Это расчетный инструмент, а не торговый робот.


## Предторговый контроль
Перед действием обязательно проверьте `10_PRECHECK!B17`:
- `GO` — работать можно.
- `STOP` — сначала исправить ошибки входных данных.


## Логирование и контроль действий
- Фиксируйте каждое решение на листе `11_DECISION_LOG` (кнопка/процедура: `ЗАПИСАТЬ РЕШЕНИЕ`, в текущей версии — manual copy, VBA можно добавить отдельно).
- Фиксируйте реальное действие на листе `12_ACTION_LOG`.
- На `13_ANALYTICS` контролируйте `DisciplineScore`, `LastMatch` и предупреждение `WARNING: DISCIPLINE LOW`.

## Автоматический подбор параметров (ТЗ №6)

Новые листы:
- `14_OPTIMIZER_INPUT`
- `15_OPTIMIZER_TABLE`
- `16_OPTIMIZER_RESULT`
- `17_OPTIMIZER_REPORT`

Как использовать:
1. На `14_OPTIMIZER_INPUT` выберите режим: `Conservative`, `Balanced`, `Aggressive`, `Custom`.
2. Проверьте рекомендуемые параметры на `16_OPTIMIZER_RESULT` (`Recommended BaseLot/K/Step`, `Risk LOW/MEDIUM/HIGH`).
3. Включите `01_INPUT!B40 = YES`, чтобы применить рекомендации (`Effective*` параметры).
4. Если `OptimizerStatus = NO VALID PARAMS`, использовать рекомендации нельзя: система даст `PARAMETER ERROR`.

Когда нельзя использовать рекомендации:
- если `ValidationStatus = ERROR`;
- если `OptimizerStatus = NO VALID PARAMS`;
- если `10_PRECHECK` показывает `STOP`.

## Стресс-тестирование серии шагов (ТЗ №7)

Новые листы:
- `18_STRESS_INPUT` — вход стресс-теста (режим, число шагов, правила остановки).
- `19_STRESS_PATH` — путь цены по шагам.
- `20_STRESS_SIMULATION` — последовательная симуляция (шаг N влияет на N+1).
- `21_STRESS_REPORT` — итог (`PASSED/WARNING/FAILED`).

Режимы StressMode:
- `UP` — каждый шаг вверх.
- `DOWN` — каждый шаг вниз.
- `SAW` — пила (вверх/вниз чередуются).
- `CUSTOM` — ручные направления.

Как читать отчет:
- `FinalStatus`, `FinalBasketProfit`, `SafeModeStep`, `FullCloseStep`, `Verdict`.
- `PASSED` — цель достигнута или корзина неотрицательна.
- `WARNING` — восстановление не завершено.
- `FAILED` — сработал SAFE MODE.
