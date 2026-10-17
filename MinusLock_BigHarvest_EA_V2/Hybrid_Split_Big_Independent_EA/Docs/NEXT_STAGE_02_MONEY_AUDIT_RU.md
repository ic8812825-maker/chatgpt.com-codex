# Этап 2 — независимый аудит денежной модели HSBI

## 1. Паспорт аудита и ограничения

- Проверенная ветка: `work`.
- Исходный HEAD и родитель будущего аудиторского коммита: `de84a8afccd29231c4c6bead3b5873fabd74ce7a`.
- Время начальной проверки remote HEAD: **2026-10-17 08:33:33 UTC**. Повторная проверка непосредственно перед записью: **2026-10-17 08:34:47 UTC**.
- `EXECUTION_MODE=GITHUB_API`
- `LOCAL_WORKTREE_STATUS=NOT_APPLICABLE`
- `REMOTE_BASELINE_VERIFIED=YES`
- Recursive Git tree: `truncated=false`; отчёт этапа 1 присутствует.
- Локальная компиляция, запуск Python/MQL5 тестов и брокерские вызовы в рамках этой сессии **не выполнялись**. Успехи из сохранённых evidence не считаются свежими тестами.
- Production-файлы, нормативные спецификации, тесты и исторические evidence не изменялись. Изменение на этапе 2 — только этот отчёт.

Обязательные флаги остаются:
```
FULL_ECONOMIC_CORRECTNESS=NOT_PROVEN
MODEL_CHANGES_ALLOWED=NO
TRADING_LOGIC_START_ALLOWED=NO
TRADE_REQUESTS_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
```

## 2. Итог аудита

**Решение: переход к этапу 3 пока не разрешать. Общий PASS не присваивается.**

Статический разбор обнаружил критические пробелы в доказательстве происхождения Reserve/Far money и в связке consumption key с allocation source. Часть денежных полей имеет семантику, не закреплённую однозначно между нормативными документами. Брокерский wrapper в целом fail-closed на ошибке OrderCalcProfit/OrderCalcMargin, однако это не доказывает корректность сумм выше по цепочке, их происхождение или актуальность actual ledger.

### Сводка по статусам

| ID | Статус | Вывод |
|---|---|---|
| M-01 | `CONFIRMED_DEFECT` | Catch-Up не связывает `consumptionKey.sourceDealKey/sourceAllocationKey` с соответствующим `reserveAllocationSource`; чужой источник может пройти проверку ключа |
| M-02 | `CONFIRMED_DEFECT` | В вызывающем коде expected Reserve/Far identity строится копированием identity из того же proof, а source IDs не сверяются с независимым actual-deal/event snapshot |
| M-03 | `POTENTIAL_DEFECT` | Allocation validator допускает неполное распределение; это конфликтует с требованием равенства в документе 08, но документ 32 формулирует только верхнюю границу |
| M-04 | `POTENTIAL_DEFECT` | `basketNetMoney/recoveryMoney` — сумма projected net четырёх ног; имя `recoveryMoney` может ошибочно восприниматься как доступный Recovery Fund |
| M-05 | `POTENTIAL_DEFECT` | `reserveGainMoney` корзины включает Small, хотя нормативный Reserve proof допускает только BigCore/BigTrend; поле не используется как доказательство Catch-Up в основном solver path, но вводит опасную семантику |
| M-06 | `OPEN_QUESTION` | `farLossIncreaseMoney` рассчитывается как абсолютный отрицательный projected net Far, а не явно как приращение относительно базового снимка |
| M-07 | `OPEN_QUESTION` | `transitionLoss` строится из projected basket net, тогда как документ 08 определяет нормативный TransitionLoss через actual closing DealNet |
| M-08 | `OPEN_QUESTION` | Safety buffer вычитается в каждом projected leg и затем отдельно в Catch-Up; нужно подтвердить нормативно, является ли это двумя независимыми резервами риска или двойным вычитанием |
| M-09 | `NOT_VERIFIED` | Нельзя подтвердить согласованность всей денежной цепочки с независимым broker/oracle расчётом без исполнения в MetaTrader 5 |
| T-01 | `NOT_VERIFIED` | Никакие автоматические тесты в текущем запуске не выполнялись |

## 3. Нормативные источники и изученные компоненты

Обязательно прочитаны:
- `Docs/24_BROKER_MONEY_MODEL_RU.md`
- `Docs/31_MONEY_PROOF_IDENTITY_RU.md`
- `Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md`

Дополнительно:
- `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md`
- `Docs/HSB_2E_NEW_FAR_CATCH_UP_IMPLEMENTATION_CONTRACT_RU.md`
- `Docs/HSB_2E_PARTIAL_FAR_RESERVE_IMPLEMENTATION_CONTRACT_RU.md`

Production/source:
- `Include/Money/HSBI_BasketMoneyEvaluator.mqh`
- `HSBI_MoneyProofIdentity.mqh`, `HSBI_ReserveCatchUpEvaluator.mqh`, `HSBI_ReserveAllocationTypes.mqh`
- `HSBI_LevelMoneyEvaluator.mqh`, `HSBI_BrokerMoneyModel.mqh`, `HSBI_CandidateMoneyEvaluator.mqh`
- `HSBI_CostModel.mqh`, `HSBI_BrokerMoneyTypes.mqh`, `HSBI_BrokerMarginModel.mqh`, `HSBI_LevelMarginEvaluator.mqh`
- `HSBI_AllocationPolicyTypes.mqh`, `HSBI_AllocationLedgerTypes.mqh`, `HSBI_EconomicLedgerTypes.mqh`, `HSBI_MoneyTypes.mqh`, `HSBI_MoneyState.mqh`
- `HSBI_CatchUpModel.mqh`, `HSBI_CatchUpTypes.mqh`
- `Include/Planning/HSBI_FutureSmallTypes.mqh`, `HSBI_FutureSmallSolver.mqh`, `HSBI_FutureSmallProofAggregator.mqh`, `HSBI_NewFarSolver.mqh`
- `Include/Runtime/HSBI_RuntimeDecisionValidator.mqh`
- `Tests/MQL5/HSBI_Skeleton_Tests.mq5`
- `Tests/Static/verify_hsb_2e_r4_r9_r4a_r12a_normative_contract.py`
- `Tests/Static/audit_hsb_2e_r4_r9_r4a_r12a_actual_coverage.py`, `audit_hsb_2e_r4_r9_r4a_r12a_contract_conflict.py`, `check_hsb_2e_r4_r9_r4a_r12a_fix_01.py`
- Contract/vector/reference/static/evidence directories were inventoried. The repository has 46 contract files, 32 vector files, 62 reference files, 197 entries in Static, 2 MQL5 entries, and 338 evidence entries at the audited HEAD. Counts include non-source assets and are inventory counts, not test totals.

## 4. Происхождение денежных величин

| Поле | Фактическое происхождение | Единицы / тип | Аудиторский вывод |
|---|---|---|---|
| `grossProfit` | `OrderCalcProfit` по symbol, direction, volume, open/close price | Деньги счёта; projected | API error → UNAVAILABLE, non-finite → ERROR. Реальная брокерская проверка не запускалась |
| `commission/swap/fee` | Входной `HSBI_CostSnapshot`, не извлекается внутри wrapper из actual deals | Деньги со знаком snapshot | Snapshot проверяется на valid, actual/projected, timestamp, ID и finite. Связь с фактической сделкой — обязанность вызывающего кода |
| `spreadCost/slippageBuffer` | Проектный cost snapshot | Деньги | Вычитаются в projected net; актуальность должна быть обеспечена источником снимка |
| `netMoney` ноги | `gross + swap + commission + fee - spread - slippage - executionSafetyBuffer` | Деньги; projected | Формула совпадает с документом 24 на уровне wrapper |
| `actual DealNet` | `profit + swap + commission + fee` из actual closing deal | Деньги; actual | `HSBI_TryActualDealNet` требует actual cost snapshot; production-происхождение записи отдельно не доказано этим helper |
| `basketNetMoney` | Сумма projected net Far + Core + Trend + Small | Деньги; projected basket | Не actual P/L и не allocation ledger balance |
| `recoveryMoney` | Прямое присваивание `basketNetMoney` | Деньги; projected | Равенство техническое; нормативная эквивалентность доступному Recovery Fund не доказана |
| `reserveGainMoney` корзины | `max(0, Core.net + Trend.net + Small.net)` | Деньги; projected | Small входит в показатель; это не независимый Reserve proof |
| `farLossIncreaseMoney` корзины | `max(0, -Far.netMoney)` | Деньги; projected | Абсолютный прогнозный убыток ноги; сравнение с базовым снимком не выполняется в этой функции |
| `transitionLoss` корзины | `max(0, -basketNetMoney)` | Деньги; projected | Не равно нормативному actual TransitionLoss без отдельного контракта преобразования |
| `totalMargin` | Сумма четырёх `OrderCalcMargin` | Маржа в валюте счёта | API unavailable отклоняет корзину; сумма маржи ног может быть консервативной оценкой, но broker-specific netting/hedging effects не проверены |
| `grossExposure` | Сумма объёмов четырёх ног | Лоты | Это сумма лотов, не денежная экспозиция; имя должно трактоваться именно так |
| `safetyBuffer` корзины | `executionSafetyBuffer * 4` | Деньги, предполагаемо | Не входит в basket digest; отдельно от буфера, уже вычитаемого в каждой ноге |
| `reserveEligibleMoney` Catch-Up | В основном NewFar path — `max(0, control.reserveSourceProof.netMoney)` | Деньги; projected | В этом конкретном caller-path связано с Core proof; evaluator напрямую не проверяет равенство |
| `reserveGainMoney` Catch-Up | Если allocated — `reserveAllocated`; иначе `reserveEligibleMoney * reserveShare` | Деньги | Уже распределённый резерв не умножается повторно; источник и consumption binding имеют пробелы ниже |
| `catchUpMargin` | `reserveGainMoney - farLossIncreaseMoney - executionSafetyBuffer` | Деньги | PASS при строгом `> 0`; volume gate отдельно проверяет `reserveShare * netBigVolume > farVolume` |

### Формулы и брокерские проверки

- BUY закрывается по Bid, SELL — по Ask. Wrapper проверяет это сравнением `closePrice` с ожидаемой ценой.
- Проверяются finite значения, цена на TickSize grid, объём через volume min/max/step, направление, валидность и свежесть брокерских свойств, совпадение symbol/snapshot ID и валидность cost snapshot.
- `OrderCalcProfit=false` → `HSBI_CALC_UNAVAILABLE`; `OrderCalcMargin=false` → `HSBI_CALC_UNAVAILABLE`. Ошибка API не преобразуется в успешный ноль.
- Нулевой объём отклоняется через volume grid, если он ниже VolumeMin. Ноги корзины не имеют отдельного признака «отсутствует»: все четыре объёма передаются как обязательные и каждая нога оценивается. Это может намеренно запрещать неполную корзину, но поведение должно быть явным в контракте.
- `HSBI_BasketMoneyProofDigest` не включает `reserveGainMoney`, `farLossIncreaseMoney`, `safetyBuffer`, identity ног и cost snapshot details. Изменение этих полей не меняет digest корзины, если не меняет другие включённые поля. Это ограничивает доказательную силу digest; требуется включить все поля, влияющие на решения, либо документировать отдельные digests.
- Ручной независимый расчёт с фактическим broker contract не подтверждён: отсутствуют текущий запуск MetaTrader 5 и брокерский runtime.

## 5. Подтверждённые дефекты и контрпримеры

### M-01 — consumption key не привязан к allocation source

**Статус: `CONFIRMED_DEFECT`.**

Файлы: `Include/Money/HSBI_ReserveCatchUpEvaluator.mqh`, `HSBI_ReserveAllocationTypes.mqh`.

`HSBI_ValidateReserveConsumption` проверяет только непустые `sourceDealKey/sourceAllocationKey`, `consumptionEventId`, consumer и совпадение PlanID/StateRevision с аргументами. В `HSBI_EvaluateReserveCatchUp` нет проверки:
- `consumptionKey.sourceDealKey == reserveAllocationSource.sourceDealKey`;
- `consumptionKey.sourceAllocationKey == reserveAllocationSource.sourceAllocationKey);
- связи `consumptionEventId` с ожидаемым событием аллокации/реальным журналом потребления.

**Контрпример по логическому пути:** allocation source валиден, reconciled и confirmed с ключами `D9/A9`, sourceDealId=9, policyVersion=1; consumption key содержит `OTHER_DEAL/OTHER_ALLOC`, event=11, consumer=`NEW_FAR`, тот же PlanID/StateRevision, prior consumption отсутствует. `HSBI_ValidateReserveConsumption` возвращает true, поскольку ключи лишь непустые. Остальные проверки могут пройти, а evaluator не связывает ключ потребления с `D9/A9`. Поэтому результат способен стать PASS для consumption key, не относящегося к allocation source.

Норматив: документ 32 требует ConsumptionKey, связанный с deal/allocation/action/source, запрещает foreign source consumption и требует NO-OP/conflict для повторов. Предусловия не исключают пример, поскольку равенство ключей нигде не проверяется.

Минимальный различающий тест: сформировать иначе корректный Catch-Up input; заменить только оба ключа consumption на чужие непустые значения. Ожидается REJECT/CONFLICT, фактический статический путь допускает прохождение проверки ключа.

### M-02 — identity не является независимым доказательством происхождения

**Статус: `CONFIRMED_DEFECT` для независимой проверки source binding; действительность конкретной сделки в live account не проверялась.**

Файлы: `Include/Planning/HSBI_NewFarSolver.mqh`, `Include/Money/HSBI_MoneyProofIdentity.mqh`, `HSBI_ReserveCatchUpEvaluator.mqh`.

В NewFar solver вызывающий код задаёт identity через `HSBI_NewFarProofIdentity(..., x.reserveSourceDealId, x.reserveSourceEventId, ...)` и затем передаёт **копию той же identity** как `expectedReserveIdentity`; аналогично для Far. Catch-Up сравнивает proof identity с expected identity, но это сравнение не независимо от источника формирования proof.

`HSBI_ValidateNewFarSource` проверяет, что `actualClosingDeals.sourceDealId/sourceEventId` ненулевые и fill подтверждён, но не связывает их равенством с `reserveSourceDealId/reserveSourceEventId` и не читает actual economic ledger для подтверждения суммы источника. Ненулевой ID сам по себе не доказывает существование или корректность сделки.

**Контрпример:** old Far, original BigCore и actual residual имеют согласованные account/symbol/magic/cycle/identifier/ticket; actual closing deal snapshot содержит подтверждённые `deal=700,event=701`; поля Reserve proof получают `deal=900,event=901`; ожидаемая Reserve identity строится из `900/901` и копируется из неё. Проверки формата и equality identity не обнаруживают отсутствие доказанной связи между этими ID и actual closing event. Возможность прохождения остальных ворот зависит от конкретных snapshots, но именно независимая source binding отсутствует.

Норматив: документы 08 и 31 требуют реальный source deal/event и независимые Reserve/Far proofs; комментарий или identity, созданная из тех же входных данных, не является внешним подтверждением.

Минимальный тест: при валидных позициях и снимках изменить только reserve source deal/event на IDs, отсутствующие в authoritative ledger; solver должен отклонить источник до Catch-Up. Для доказательства нужен независимый ledger lookup / immutable source proof, а не копирование expected identity.

### M-03 — неполная allocation допускается валидатором

**Статус: `POTENTIAL_DEFECT` — нормативный конфликт.**

`HSBI_ValidateReserveAllocationSource` требует сумму Reserve + PartialFar + Transition + Carry + Residual + alreadyConsumed не выше allocatableNet, но не требует равенства. Пример: allocatableNet=100, все buckets=0, alreadyConsumed=0 — validator пропускает арифметическую conservation проверку.

Документ 08 говорит после округления `Reserve+Partial+Transition+Carry+Residual=AllocatableDealNet`; документ 32 говорит, что сумма этих частей и already-consumed «не превышает» allocatable net. До разрешения расхождения владельцем классификация остаётся потенциальной. Минимальный тест: нераспределённый остаток без residual должен FAIL, если действует контракт равенства.

### M-04 — RecoveryMoney и BasketNetMoney не являются доступным фондом

**Статус: `POTENTIAL_DEFECT` / семантическая граница.**

`HSBI_EvaluateBasketMoney` присваивает `recoveryMoney=basketNetMoney`, а BasketNetMoney — сумма четырёх projected legs. Это не actual closing DealNet и не сумма доступных allocation buckets. Документ 31 прямо запрещает заменять отдельные Reserve/Far proofs basket recovery, gross profit или transition loss. В текущем NewFar path Catch-Up получает отдельные Core/Far proofs, что является защитой; однако FutureSmall использует `basket.recoveryMoney` при сравнении с `moneyState.recoveryMoney`. Нужен явный контракт: является ли это лишь критерием улучшения прогноза или денежным фондом, доступным для расходования. До этого поле нельзя трактовать как свободный Recovery Fund.

### M-05 — reserveGainMoney корзины включает Small

**Статус: `POTENTIAL_DEFECT`.**

В `HSBI_BasketMoneyEvaluator.mqh`:
`reserveGainMoney = max(0, core.netMoney + trend.netMoney + small.netMoney)`.

Нормативный документ 31 допускает Reserve source proof только с ролью BigCore/BigTrend. Простой контрпример для арифметики: Core=0, Trend=0, Small=+10 → поле reserveGainMoney=10, хотя ни одна допустимая Reserve source leg не имеет положительной суммы. В основном Catch-Up solver используется отдельный Core proof, поэтому по просмотренному пути это поле не доказано как источник фактического расхода; но его имя и формула несовместимы с нормативной ролью Reserve и требуют исправления либо переименования после решения владельца.

### M-06 — смысл FarLossIncreaseMoney

**Статус: `OPEN_QUESTION`.**

Поле рассчитывается как `max(0, -far.netMoney)`. Нормативное название «increase» может означать абсолютный убыток текущего Far или приращение относительно baseline loss. В evaluator нет отдельного baseline loss, поэтому вторую трактовку он реализовать не может. Не менять формулу без решения владельца; требуется зафиксировать определение и тест с исходным убытком Far.

### M-07 — projected TransitionLoss и actual TransitionLoss

**Статус: `OPEN_QUESTION`.**

Корзина вычисляет `max(0,-basketNetMoney)` на projected позициях и передаёт значение в FutureSmall/aggregate. Документ 08 определяет нормативный TransitionLoss как `max(0,-ΣActualClosingDealNet)`. Это могут быть разные метрики (прогнозный risk gate против фактического accounting), но они используют одно имя. Нужны раздельные названия и спецификация моста между projected и actual, если он нужен. Пока не доказано, что projected величина используется как settled loss, дефект не повышается до confirmed.

### M-08 — safety buffer

**Статус: `OPEN_QUESTION`.**

Projected net каждой из четырёх ног уже вычитает `executionSafetyBuffer`. Catch-Up затем ещё вычитает `executionSafetyBuffer` из `catchUpMargin`; Basket также выставляет `safetyBuffer=4*executionSafetyBuffer`. Например при buffer=1 каждый leg net уменьшен на 1, basket net — на 4, а Catch-Up margin дополнительно уменьшается на 1. Это корректно только если Catch-Up buffer — отдельный независимый резерв поверх projected leg buffers. Документ 24 подтверждает оба упоминания, но не определяет достаточно ясно их независимость. Нужен явный тест по бюджету buffer, не менять формулу на этом этапе.

## 6. Proof identity: проверенные свойства и границы

Подтверждено статическим чтением:
- `HSBI_ValidateMoneyProofIdentity` требует положительные account/cycle/position/deal/event/snapshot/plan/revision, непустой symbol, ненулевой magic, role и direction.
- `HSBI_IsSameMoneyProofIdentity` сравнивает все перечисленные поля, включая source deal/event, snapshot, PlanID и StateRevision.
- Reserve proof требует valid PASS, projected=true, actual=false, runtimeConfirmed=true, finite positive net и роль BigCore/BigTrend.
- Far proof требует valid PASS, projected=true, actual=false, runtimeConfirmed=true, finite net и роль FAR.
- Catch-Up отклоняет stale/unavailable, testOnly source, identity mismatch, policy mismatch, duplicate key, conflict, отрицательные суммы/buffer и нарушенный lot/money gate.

Границы:
- Синтаксическая валидность и equality identity не доказывают, что указанный deal/event существует в actual ledger.
- Snapshot ID проверяется на ненулевое значение и свежесть флагом входа; независимая сверка snapshot с текущим брокерским/ledger state здесь не выполняется.
- Проверка equality не гарантирует независимость двух proofs, если оба созданы из общего источника или скопированной identity.
- `sourceDealId` в allocation source сравнивается с Reserve proof deal ID, но `allocationEventId` не связывается в этом evaluator с proof sourceEventId; связь ключей allocation/consumption тоже отсутствует.
- В `HSBI_ReserveCatchUpEvaluator` сравнивается только один переданный prior key. Устойчивость после рестарта зависит от корректного восстановления всех consumed records внешним владельцем; локальная функция не хранит ledger.

## 7. Reserve allocation и последовательные вызовы

### Conservation / already allocated
`HSBI_ValidateReserveAllocationSource` проверяет valid, confirmed, reconciled, source keys/IDs/version, finite и неотрицательные buckets, а также верхнюю границу суммы. `reserveEligibleMoneyAlreadyAllocated=true` берёт `reserveAllocated` напрямую, не умножая его повторно на ReserveShare; дополнительно rejects если reserveAllocated≤0, выше allocatableNet или alreadyConsumed>0. Это согласуется с запретом повторного умножения, но требует реальной подтверждённой allocation source и строгой привязки consumption.

### Минимальный сценарий вызовов
1. **Первый вызов:** нет prior consumption; валидный source и ключ K. При положительном `catchUpMargin` и пройденном volume gate evaluator может вернуть PASS.
2. **Точный повтор с prior key K:** `HSBI_IsDuplicateReserveConsumption` возвращает true; evaluator возвращает REJECT с `DUPLICATE_CONSUMPTION_NOOP`, поэтому повторный valid Catch-Up блокируется, хотя нормативный термин NO-OP может требовать отдельный outcome-код, а не только REJECT.
3. **Повтор с тем же allocation key, но изменённым event/consumer:** `HSBI_ReserveConsumptionConflict` возвращает true; evaluator REJECT `CONSUMPTION_CONFLICT`.

Важная граница: если при перезапуске вызывающий код не восстановил prior consumption и передал `hasPriorConsumption=false`, evaluator не имеет внутреннего журнала и не может распознать ранее потреблённый key. Это **`NOT_VERIFIED`** на уровне полной системы persistence, а не доказательство, что внешний persistence отсутствует во всём проекте. Кроме того, M-01 позволяет ключу consumption ссылаться на другой source даже при валидной allocation source.

## 8. Catch-Up: проверка размерностей и численный пример

Объёмное условие имеет размерность лотов с обеих сторон: `reserveShare` безразмерен, `netBigVolume` и `farVolume` — лоты. Денежное условие также размерностно согласовано, если все суммы выражены в одной валюте счёта:
`catchUpMargin = reserveGainMoney - farLossIncreaseMoney - executionSafetyBuffer`, PASS только если результат строго больше нуля.

Численный пример положительного запаса из структуры теста:
- ReserveShare=0.60; netBigVolume=2.00 lot; FarVolume=1.00 lot;
- reserveGainMoney=20; farLossIncreaseMoney=10; buffer=2;
- volume: 0.60×2.00=1.20 > 1.00, проходит;
- money: 20−10−2=8 > 0, проходит.

Границы:
- Margin ровно 0 → REJECT (проверка `<=0`).
- Margin отрицательный → REJECT.
- `moneyAvailable=false` или stale → UNAVAILABLE до денежного PASS.
- `reserveGainMoney=11`, Far loss=10, buffer=2 → margin=−1, REJECT.
- Недопустимая identity, duplicate consumption, conflict или неверная allocation policy → REJECT.
- Уже распределённый резерв берётся из `reserveAllocated`; повторное умножение на ReserveShare не выполняется.

Но отдельные суммы `farLossIncreaseMoney` и `reserveEligibleMoney` не сверяются внутри evaluator арифметически с соответствующими proof.netMoney. В текущем NewFar caller они назначаются из `control.farLossProof.netMoney` и `control.reserveSourceProof.netMoney`; это локальная гарантия caller, не универсальный инвариант evaluator. Для независимой проверки нужны прямые тесты evaluator с несовпадающими входными суммами и source proofs, а также тесты, подтверждающие что production caller всегда связывает их именно так.

## 9. Тесты и verifier

| Объект | Статус | Что реально подтверждено |
|---|---|---|
| `HSBI_Skeleton_Tests.mq5` | `NOT_RUN` | Исходник содержит множество прямых вызовов production helpers; видны проверки Bid/Ask, grids, unavailable, actual/projected separation, duplicate/conflict и identity. MetaEditor/MT5 запуск не выполнялся |
| `Tests/Static/verify_hsb_2e_r4_r9_r4a_r12a_normative_contract.py` | `CONFIRMED_DEFECT` как verifier полного аудита; запуск `NOT_RUN` | Прямой `__main__` вызывает только `print(root([]))). `root` канонизирует список переданных записей и проверяет дубликаты deal/event IDs; скрипт не импортирует production-код, не читает production money formulas, не запускает тестовые векторы и не делает mutation testing |
| `audit_hsb_2e_r4_r9_r4a_r12a_actual_coverage.py` | `NOT_RUN` | По коду это AST-аудит Python evaluator относительно ownership matrix; он не доказывает корректность MQL5 money formula |
| `audit_hsb_2e_r4_r9_r4a_r12a_contract_conflict.py` | `NOT_RUN` | Статически рассчитывает альтернативный hash для fixture и печатает контрактный конфликт; не вызывает broker-money production helpers |
| `check_hsb_2e_r4_r9_r4a_r12a_fix_01.py` | `NOT_RUN` | Содержит causal checks Python evaluator для batch/ledger cases, прямо указывает `SECOND_BLOCK_SOURCE_MUTATIONS=NOT_STARTED`; не является запуском MQL5 денежных формул |
| `Tests/Contracts/`, `Tests/Vectors/`, `Tests/Reference/` | `NOT_RUN` | Векторы/контракты/модели присутствуют; само наличие JSON и Python reference models не доказывает, что конкретные production функции вызываются и согласованы с независимым oracle |
| `Tests/Evidence/` | `NOT_RUN` в этой сессии | Сохранённые PASS/evidence исторические; не объявляются свежим запуском |

### Почему verifier нельзя считать независимым proof production money
Скрипт `verify_hsb_2e_r4_r9_r4a_r12a_normative_contract.py` не принимает production source как вход. Прямой запуск выводит SHA-256 для пустого набора ledger entries. Поэтому он может успешно завершиться даже при произвольной ошибке в `HSBI_BasketMoneyEvaluator.mqh` или `HSBI_ReserveCatchUpEvaluator.mqh`. Он полезен как функция канонизации ledger root, но не как полный нормативный verifier денежной модели. Поскольку запуск не выполнялся, статус исполнения — NOT_RUN; вывод о его ограниченной области основан на прочитанном исходнике.

## 10. Отсутствующие доказательства

1. Свежая компиляция MetaEditor для точного SHA.
2. Запуск MQL5 skeleton tests на MT5 с сохранением полного вывода и кода возврата.
3. Broker-specific подтверждение `OrderCalcProfit/OrderCalcMargin` на выбранном символе, типе счёта, режиме netting/hedging и реальных свойствах symbol.
4. Независимый oracle, который рассчитывает projected net и margin отдельно от production helpers и сравнивает все четыре ноги.
5. Actual deal/ledger fixtures, доказывающие sourceDealKey/sourceAllocationKey/sourceEventId и связь position identifier → deal → allocation → consumption.
6. Restart/replay test, где consumption history восстановлена из устойчивого ledger, затем выполнены первый вызов, exact replay и altered payload.
7. Mutation tests для конкретных M-01/M-02 денежных условий, с доказательством, что ошибочный production source приводит к FAIL.
8. Решение владельца по конфликту allocation conservation и определениям `FarLossIncrease`, projected/actual `TransitionLoss`, safety buffer.

## 11. Рекомендуемые действия перед следующим этапом

1. Сначала решить контрактные вопросы M-03, M-06, M-07 и M-08; не менять экономическую семантику по догадке.
2. На отдельном утверждённом этапе закрыть M-01: привязать consumption key к allocation source и подтверждённому журналу; определить точный NO-OP outcome.
3. Закрыть M-02 независимым подтверждением source deal/event и snapshot, не копированием expected identity из проверяемого proof.
4. Уточнить semantics/digest Basket money fields и исключить возможность трактовать projected basket sum как свободный фонд.
5. Добавить независимые численные oracle и негативные/mutation тесты, включая несовпадающие identity, foreign allocation key, старый snapshot, неправильную сумму source proof и restart replay.
6. Запустить тесты в подходящей среде, сохранить точный SHA, команды, exit codes, stdout и доказательства. Не использовать исторические evidence вместо свежего запуска.

**Разрешение:** этот отчёт не разрешает этап 3, изменения production-кода, изменение нормативной модели или запуск торговой логики. Требуется review владельца и отдельное решение. Реальная торговля остаётся запрещена.

## 12. Финальные флаги

```
FULL_ECONOMIC_CORRECTNESS=NOT_PROVEN
MODEL_CHANGES_ALLOWED=NO
TRADING_LOGIC_START_ALLOWED=NO
TRADE_REQUESTS_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
```
