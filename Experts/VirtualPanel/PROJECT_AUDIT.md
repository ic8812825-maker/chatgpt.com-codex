# Аудит проекта `Experts/VirtualPanel`

## 1) Назначение проекта
`VirtualPanel.mq5` — это Expert Advisor для MetaTrader 5 в формате **display-only панели** (без прямого выставления реальных ордеров), который даёт оператору единый интерфейс для:
- ведения виртуальных позиций в Terminal-вкладке,
- просмотра состояния счёта в Broker-вкладке,
- просмотра характеристик инструмента в Symbol-вкладке,
- интеграции с архитектурой ALE (Adaptive Lock Expansion) в правой части проекта.

## 2) Архитектура верхнего уровня
Проект разбит на 2 крупные зоны:
- `left/` — пользовательская панель и вкладки (Terminal/Broker/Symbol),
- `right/ale/` — движок ALE (core/geometry/risk/exposure/math/optimization/interfaces),
- `right/tests/` — модульные проверки логики ALE.

Основной вход: `VirtualPanel.mq5`.

## 3) Левая часть (UI/операторский слой)
### 3.1 Управление вкладками
В `VirtualPanel.mq5` реализовано:
- enum вкладок (`Terminal`, `Broker`, `Symbol`),
- единые координаты панели,
- переключение видимости через `SetActiveLeftTab`,
- обработка кликов по таб-кнопкам в `OnChartEvent`,
- обновление только активной вкладки в `OnTimer`.

### 3.2 Terminal-вкладка (`CVPanel`)
Класс `CVPanel` — самый насыщенный по логике блок. Ключевые возможности:
- хранение массива виртуальных позиций `positions[MAX_POSITIONS]`,
- двухпоточная модель ввода (BUY-flow и SELL-flow),
- FSM-состояние панели (`IDLE/BUY_ACTIVE/SELL_ACTIVE/DUAL_ACTIVE/RISK_ALERT`),
- smart-обновление UI по флагам `ui_dirty/update_in_progress/deferred_ui_dirty`,
- режим выбора цены с графика (pick mode),
- авто-пересчёт метрик виртуальной позиции,
- валидация полей (цена, лот, минимум `MIN_LOT`),
- создание/редактирование/удаление строк таблицы.

### 3.3 Broker-вкладка (`CBrokerTab`)
Выводит сведения по счёту:
- Balance, Equity, Margin, FreeMargin,
- MarginLevel, Leverage, Currency,
- Trading status, StopOut.

Есть кэш полей и перерисовка layout при изменениях.

### 3.4 Symbol-вкладка (`CSymbolTab`)
Выводит рыночные параметры символа:
- Bid/Ask/Open/High/Low/Close,
- Point, Tick Value, Tick Size,
- Contract Size,
- Min/Max/Step lot,
- session metrics,
- валюты base/profit,
- торговая доступность символа.

## 4) Правая часть (ALE engine)
### 4.1 Core
- `CALEngine` агрегирует два потока: BUY (`CBuyEngine`) и SELL (`CSellEngine`).
- На каждом `OnPriceUpdate(price)`:
  - обновляет оба потока,
  - синхронизирует контекст,
  - проверяет глобальный SAFE-режим,
  - форсирует SAFE при превышении aggregate risk,
  - эмитит события состояния (`CALEvent`).

### 4.2 Модель состояния
`CALStateMachine` поддерживает переходы между `IDLE/BASE/EXPANSION/HARVEST/RESET/SAFE`, а также переходы по сигналам:
- `PRICE_MOVE`,
- `DRAWDOWN_EXCEEDED`,
- `HARVEST_REACHED`,
- `SAFE_TRIGGERED`,
- `RESET_REQUESTED`.

### 4.3 Контекст и метрики
`CALContext` хранит stream-контексты `buy` и `sell`:
- `net_delta`, `pnl`, `exposure`,
- `worst_dd`, `margin`, `gamma`, `convexity`,
- `safe_active`,
и агрегаты:
- `NetDeltaTotal()`,
- `NetExposureTotal()`,
- `TotalPnL()`.

### 4.4 Интерфейсы
`interfaces/` задают контракты ALE-системы:
- `IALEngine`,
- `IGeometryEngine`,
- `IMarketAdapter`,
- а также FSM/геометрия/риск-ориентированные интерфейсы.

## 5) Тесты
В `right/tests` есть самостоятельные unit-style проверки:
- `TestALE.mqh` — интеграционный сценарий dual-flow, проверка finite-метрик и переходов FSM,
- `TestGeometry.mqh` — симметрия BUY/SELL grid и свойства лог-геометрии,
- `TestRisk.mqh` — формулы риска, margin, worst drawdown и отчёт risk-engine.

## 6) Константы и UI-хелперы
- `PanelConstants.mqh` определяет лимиты (`MAX_POSITIONS`, `MIN_LOT`, `VP_MAX_TOTAL_LOT`), размеры и spacing UI.
- `UIHelpers.mqh` даёт унифицированные функции `EnsureLabel/EnsureButton/EnsureEdit/DeleteByPrefix`.

## 7) Наблюдения по качеству
Сильные стороны:
1. Чёткое разделение UI-слоя и ALE-движка.
2. Явные контракты через interfaces.
3. Наличие тестовых модулей для ключевых подсистем.
4. Практичный подход smart UI redraw.

## 8) Предложенный список улучшений (приоритизированный)

### P0 (критично для надёжности)
1. **Единый runner для тестов ALE**
   - Добавить общий `RunAllTests.mqh`/`RunAllTests.mq5`, который последовательно вызывает `TestALE/TestGeometry/TestRisk`.
   - На выходе: единый pass/fail отчёт и коды возврата.
2. **Инварианты в runtime для `CVPanel`**
   - Явно проверять инварианты после операций add/edit/delete:
     - `count <= MAX_POSITIONS`,
     - `lot >= MIN_LOT`,
     - `dir in {DIR_BUY, DIR_SELL}`.
   - При нарушении: детальный `PrintFormat` + безопасный откат действия.
3. **SAFE-порог в конфиг**
   - Пороги из `CheckGlobalSAFE()` (margin / worst_dd) вынести в параметры.
   - Это позволит адаптировать стратегию без перекомпиляции.

### P1 (качество и поддерживаемость)
4. **Базовый абстрактный класс для табов**
   - Унифицировать `Init/Resize/SetVisible/Deinit` для `CBrokerTab` и `CSymbolTab`.
   - Убрать дублирование кода по скрытию/показу объектов.
5. **Единый стиль именования и префиксов объектов**
   - Зафиксировать соглашение (`vp_<tab>_<type>_<id>`) и применить ко всем объектам UI.
   - Снизит риск конфликтов имён и упростит отладку.
6. **Централизация валидации UI-ввода**
   - Вынести проверки price/lot/comment в отдельный валидатор.
   - Уменьшить копипасту между BUY-flow и SELL-flow.

### P2 (функциональное развитие)
7. **Мост между `left/` и `right/ale/`**
   - Добавить слой адаптера: действия пользователя в `CVPanel` должны генерировать события для ALE.
   - На панель вывести ключевые ALE-метрики: state, worst_dd, margin, safe_active.
8. **Снимки состояния и экспорт отчётов**
   - Добавить экспорт текущих виртуальных позиций и контекста ALE в CSV.
   - Упростит аудит, регрессию и сравнение сценариев.
9. **Сценарные тесты (price-path tests)**
   - Готовые сценарии: тренд, флэт, шок, V-shape.
   - Проверять устойчивость состояния и отсутствие NaN/inf в метриках.

### Быстрые победы (можно сделать сразу)
10. В `CBrokerTab::Update()` удалить неиспользуемую переменную `digits`.
11. Добавить короткий `README` именно в `Experts/VirtualPanel` с картой модулей.
12. Добавить макрос `VP_DEBUG` для включения/выключения диагностических логов.

## 9) Команды, которые можно выполнять с этим проектом
Ниже — практический набор команд, которые я могу делать в этом репозитории/проекте:

### Git и репозиторий
- `git status -sb`
- `git branch --show-current`
- `git remote -v`
- `git log --oneline --decorate -n 30`
- `git diff`
- `git add <files>`
- `git commit -m "..."`
- `git show --stat`

### Инспекция структуры/кода
- `rg --files Experts/VirtualPanel`
- `find Experts/VirtualPanel -maxdepth 4 -type d`
- `sed -n '1,220p' <file>`
- `nl -ba <file> | sed -n '1,220p'`

### Проверка/верификация
- `bash verify-all.sh`
- `bash verify-all.sh work`

### Локальная аналитика качества
- поиск потенциальных TODO:
  - `rg "TODO|FIXME|XXX" Experts/VirtualPanel`
- поиск точек входа/обработчиков:
  - `rg "OnInit|OnDeinit|OnTimer|OnChartEvent" Experts/VirtualPanel`
- поиск публичных методов классов:
  - `rg "^\s*(public:|virtual|void|bool|int|double|string)" Experts/VirtualPanel/right/ale`

### Что именно я могу сделать по вашему запросу дальше
- Полный code-review каждого файла ALE с рисками и приоритетами.
- Карта зависимостей между классами (кто кого вызывает).
- Разбор математических формул риска/геометрии с примерами.
- Подготовка плана рефакторинга по этапам.
- Формирование чек-листа для регресс-тестов перед релизом.
