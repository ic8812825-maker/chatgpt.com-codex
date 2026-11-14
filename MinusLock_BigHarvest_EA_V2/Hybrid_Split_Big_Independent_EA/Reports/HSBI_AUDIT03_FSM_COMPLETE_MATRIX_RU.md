# AUDIT03 FINAL-CLOSURE — нормативная и реализованная relation FSM

База b4d8f1ea5caf492f3abd030e5502d40582c52dc8. Только статическое чтение и аналитический разбор; TESTS_EXECUTED_BY_CODEX=NO. Документ пока PARTIAL: формально определённые правила ниже не заменяют неполную нормативную спецификацию. Никаких новых состояний или разрешений не вводится.

## Домены и несовпадающие версии

Docs/06:6 перечисляет36 состояний. Include/Core/HSBI_Enums.mqh:8 перечисляет33. В нормативном домене есть ACTION_REQUEST_SENT, ACTION_ORDER_PENDING, ACTION_PARTIAL_FILL, ACTION_RETRY_PENDING; в enum вместо них есть RETRY_PENDING. Автоматически отождествлять action-phase с scenario-state нельзя. STATE_DISABLED сопоставляется с HSBI_STATE_DISABLED только лексически; отдельного бизнес-перехода это не создаёт. Enum событий: NONE, REQUEST_ACCEPTED, PLACED, PARTIAL_FILL, COMPLETED_FILL, REJECTED, TIMEOUT, CONFLICT; enum TransactionOutcome: PLACED, PARTIAL, COMPLETED, REJECTED, TIMEOUT, CONFLICT, UNKNOWN. Нормативные restart/debounce/reconciliation outcomes не полностью отображены в эти enum.

Domain coverage rule: для любой комбинации State×Event×Outcome×Partial×Timeout×Restart, не определённой источником однозначно, результат SPECIFICATION_GAP, а не выдуманный NextState. Это тотальная классификация неизвестности, а не полная детерминированная FSM. При overlap rules нужны обязательный severity/phase priority и единый owner — они ещё не установлены для всех сочетаний.

## A. Нормативные правила с индивидуальными полями

### A03-FSM-N01

| Field | Finding |
|---|---|
| CurrentState | BASKET_ACTIVE |
| Event | fresh repeated snapshot; отдельный HSBI_EventType не указан |
| Trigger | Small condition и debounce |
| Preconditions | повторно подтверждённый snapshot, immutable plan |
| Identity guard | account/symbol/magic/cycle/roles/revision/PlanID из Docs/07:11–12 |
| Money guard | полный transition budget; конкретная политика D05 ожидает решения |
| Risk guard | каждый closing prefix должен оставаться допустимым; точная relation отсутствует |
| Margin guard | актуальная broker margin; конкретный порог в этом переходе не задан |
| Proof authority | actual positions/history + committed plan, не copied proof |
| Expected positions | Far, BigCore, допустимый BigTrend и Small; actual volumes |
| Planned action | подготовить последовательное закрытие Small |
| Actual execution outcome | до закрытия подтверждённых deals нет |
| Partial-fill behavior | не переходить к следующей роли |
| Timeout behavior | reconciliation barrier |
| Restart behavior | сначала reconciliation, не повторный send |
| Persistence requirements | immutable plan и pending action до send; persisted result до advance |
| NextState | SMALL_CONFIRMING |
| Rollback / compensation | нет отката фактических сделок; compensation contract не определён |
| Fail-closed behavior | запрет дальнейшего действия при неполном proof |
| Forbidden transitions | BASKET_ACTIVE→NEW_FAR_VALIDATING без closing chain |
| Source implementation | Docs/06:13–14; production полного handler нет |
| Contract status | NOT_IMPLEMENTED; event/outcome detailed mapping SPECIFICATION_GAP |

### A03-FSM-N02

| Field | Finding |
|---|---|
| CurrentState | любое состояние с PendingAction |
| Event | HSBI_EVENT_PLACED / REQUEST_ACCEPTED |
| Trigger | accepted/placed response |
| Preconditions | ownership проверен перед request; response не доказывает completion |
| Identity guard | ActionID/PlanID/StateRevision + source namespace |
| Money guard | нет подтверждённого PnL только из accepted |
| Risk guard | изменение exposure не считать завершённым |
| Margin guard | заново читать фактическую margin при следующем действии |
| Proof authority | actual orders/deals и накопитель fills |
| Expected positions | позиции могут отсутствовать либо исполниться частично |
| Planned action | продолжать наблюдение того же action |
| Actual execution outcome | PLACED, не COMPLETED |
| Partial-fill behavior | остаётся pending |
| Timeout behavior | timeout не failure и не completion |
| Restart behavior | восстановить PendingAction, перечитать history |
| Persistence requirements | action/attempt уже сохранены; result ещё не основание advance |
| NextState | ACTION_ORDER_PENDING в фазовой схеме; точная привязка к scenario-state SPECIFICATION_GAP |
| Rollback / compensation | не повторять request без reconciliation |
| Fail-closed behavior | no advance |
| Forbidden transitions | любое следующее финансовое состояние на одном PLACED |
| Source implementation | Docs/06:8–11; Docs/07:14–15; HSBI_TransactionBarrierPassed:11 отвергает не-COMPLETED |
| Contract status | локальный barrier есть; обязательный orchestrator NOT_IMPLEMENTED |

### A03-FSM-N03

| Field | Finding |
|---|---|
| CurrentState | любое executing/closing/opening состояние |
| Event | HSBI_EVENT_PARTIAL_FILL |
| Trigger | подтверждённый частичный deal |
| Preconditions | принадлежность тому же action и batch; history достаточно полна |
| Identity guard | source/deal/order/position/action/event независимы |
| Money guard | actual signed net только исполненной части; без повторного allocation |
| Risk guard | prefix-risk проверяется на actual остатках |
| Margin guard | margin по actual позиции, не по запланированному полному fill |
| Proof authority | broker deals/positions + journal |
| Expected positions | actual filled volume < planned volume; остаток ещё существует |
| Planned action | накопить fills, не запускать следующую роль |
| Actual execution outcome | HSBI_TX_PARTIAL |
| Partial-fill behavior | pending, следующий FSM step запрещён |
| Timeout behavior | history recheck; не считать remaining volume исполненным |
| Restart behavior | восстановить partial ledger до retry |
| Persistence requirements | сохранить каждый accepted deal/event и outstanding action |
| NextState | ACTION_PARTIAL_FILL на action layer; scenario-state remains pending; точное сочетание SPECIFICATION_GAP |
| Rollback / compensation | исполненный deal не откатить; нового rollback не определено |
| Fail-closed behavior | не promote/не следующий close |
| Forbidden transitions | PARTIAL→следующая роль либо completed по bool без actual |
| Source implementation | Docs/07:15,21; Docs/17:14; TransactionTypes:11,15; нет полного handler |
| Contract status | NOT_IMPLEMENTED для lifecycle; SPECIFICATION_GAP composite state mapping |

### A03-FSM-N04

| Field | Finding |
|---|---|
| CurrentState | executing состояние с полным fill |
| Event | HSBI_EVENT_COMPLETED_FILL |
| Trigger | подтверждённое исполнение требуемого объёма |
| Preconditions | COMPLETED + actual position/deal + ledger + persisted result |
| Identity guard | тот же ActionID; fresh EventID; expected/actual revision |
| Money guard | Economic/Allocation ledger применены ровно один раз |
| Risk guard | повторная проверка фактического остатка перед следующим действием |
| Margin guard | actual margin до следующего запроса |
| Proof authority | broker history + immutable journal + committed result |
| Expected positions | фактические позиции удовлетворяют postcondition текущего action |
| Planned action | закончить action, выбрать следующий нормативный step |
| Actual execution outcome | DONE только кандидат; COMPLETED_FILL после proof |
| Partial-fill behavior | частичный результат не подходит |
| Timeout behavior | при timeout сначала reconciliation |
| Restart behavior | reconcile result до выбора нового действия |
| Persistence requirements | ledger application и persisted result обязательны до advance |
| NextState | NextState конкретного scenario; общий contract не перечисляет полный mapping |
| Rollback / compensation | rollback irreversible fill не обещается |
| Fail-closed behavior | не advance без postcondition/persist |
| Forbidden transitions | сам receipt/placed без actual reading не достаточен |
| Source implementation | Docs/06:8–11; Docs/07:5–6; TransactionTypes:9–19 не проверяет ledgerApplied/persisted |
| Contract status | полный mandatory caller NOT_IMPLEMENTED; локальный barrier PARTIAL |

### A03-FSM-N05

| Field | Finding |
|---|---|
| CurrentState | любое состояние с ожидаемым ответом |
| Event | HSBI_EVENT_TIMEOUT |
| Trigger | deadline истёк |
| Preconditions | сведения о фактическом исполнении ещё неизвестны |
| Identity guard | same ActionID/attempt, EventKey |
| Money guard | не списывать неизвестный результат повторно; неизвестное не ноль |
| Risk guard | не считать риск снятым |
| Margin guard | не считать margin освобождённой |
| Proof authority | history/positions/orders recheck |
| Expected positions | могли остаться, частично либо полностью измениться |
| Planned action | установить reconciliation barrier |
| Actual execution outcome | HSBI_TX_TIMEOUT / UNKNOWN |
| Partial-fill behavior | partial сохраняется |
| Timeout behavior | PENDING либо CONFLICT после history recheck |
| Restart behavior | reconcile pending action до send |
| Persistence requirements | сохранить timeout/attempt, не mark completed |
| NextState | RECONCILING; исход PENDING/CONFLICT, точный resume-state не задан |
| Rollback / compensation | не автоматический rollback/повтор request |
| Fail-closed behavior | no advance; no blind retry |
| Forbidden transitions | TIMEOUT→COMPLETED либо definite failure без broker evidence |
| Source implementation | Docs/07:20–24; Docs/17:10; локальный barrier отвергает outcome |
| Contract status | NOT_IMPLEMENTED complete orchestration |

### A03-FSM-N06

| Field | Finding |
|---|---|
| CurrentState | любое request/execute состояние |
| Event | HSBI_EVENT_REJECTED |
| Trigger | reject/requote/no-money/invalid-volume/market-closed/price-changed/connection |
| Preconditions | типизированный исход, ownership до повторной попытки |
| Identity guard | same economic ActionID; child attempt только после разрешения |
| Money guard | не создавать actual DealNet из отсутствующего fill |
| Risk guard | переоценить актуальный risk, не переиспользовать прежний расчёт |
| Margin guard | no-money не разрешает обход margin gate |
| Proof authority | actual history подтверждает отсутствие/наличие сделки |
| Expected positions | не предполагать нулевое изменение до reconciliation |
| Planned action | остановить advance, перейти к reconcile |
| Actual execution outcome | REJECTED; отдельные broker causes не сведены в typed code table |
| Partial-fill behavior | если fills есть, обработать их до отказа |
| Timeout behavior | connection/timeout не превращать в definite rejection |
| Restart behavior | reconcile до retry |
| Persistence requirements | journal reject/attempt + pending identity |
| NextState | RECONCILING по Docs/06; точный recovery route SPECIFICATION_GAP |
| Rollback / compensation | компенсация допустима только новым проверенным планом |
| Fail-closed behavior | no next financial step |
| Forbidden transitions | reject→next role |
| Source implementation | Docs/06:11; Docs/07:15,17–18; HSBI_RetryAllowed не проверяет все условия |
| Contract status | NOT_IMPLEMENTED lifecycle |

### A03-FSM-N07

| Field | Finding |
|---|---|
| CurrentState | любое состояние при restart |
| Event | событие restart, отсутствует в HSBI_EventType |
| Trigger | перезапуск процесса/терминала |
| Preconditions | валидные marker/schema/checksum/digests, independent actual history |
| Identity guard | полный identity lock/account/symbol/cycle/PlanID/action/revision |
| Money guard | не повторять funding/allocation; reconcile journals |
| Risk guard | текущий риск после actual read |
| Margin guard | текущая margin после actual read |
| Proof authority | committed snapshot + journal + actual broker records |
| Expected positions | могут отличаться от snapshot; adoption запрещён без diff |
| Planned action | восстановить PendingAction до send/retry |
| Actual execution outcome | UNKNOWN пока history не проверена |
| Partial-fill behavior | сохранить pending partial |
| Timeout behavior | timeout повторно reconcile |
| Restart behavior | это сам restart route |
| Persistence requirements | versioned commit/fallback protocol |
| NextState | CLEAN_START/RECONCILED/PENDING/CONFLICT/TERMINAL_SAFE — outcomes; точный NextState не для всех задан |
| Rollback / compensation | fallback previous не удаляет реальные deals; reconcile обязателен |
| Fail-closed behavior | no trading при checksum/schema/lock conflict |
| Forbidden transitions | restart→send до reconciliation |
| Source implementation | Docs/16:5–19; Docs/17:6–22; backend и полного handler нет |
| Contract status | NOT_IMPLEMENTED; outcome→state mapping SPECIFICATION_GAP |

### A03-FSM-N08

| Field | Finding |
|---|---|
| CurrentState | любое состояние при same EventKey |
| Event | duplicate/delayed event |
| Trigger | повтор доставки |
| Preconditions | immutable payload проверяется до применения эффекта |
| Identity guard | одинаковый key и полный immutable body |
| Money guard | identical=zero delta; changed=conflict, не повторное списание |
| Risk guard | не пересчитывать risk как основание повторного fill |
| Margin guard | не высвобождать margin дважды |
| Proof authority | immutable event/source journal + actual reconciliation |
| Expected positions | не менять из-за identical delivery |
| Planned action | NO_OP либо conflict route |
| Actual execution outcome | identical NO_OP; changed CONFLICT |
| Partial-fill behavior | тот же partial receipt не суммировать повторно |
| Timeout behavior | delayed после timeout reconcile тому же action |
| Restart behavior | replay сохраняет durable receipt, не создаёт новые деньги |
| Persistence requirements | durable journal необходим, hash не заменяет authenticity |
| NextState | identical: unchanged state; changed: TERMINAL_SAFE по Docs/07:21 |
| Rollback / compensation | no silent rewrite |
| Fail-closed behavior | no changed replay accepted |
| Forbidden transitions | CONFLICT→NO_OP; duplicate→fresh action |
| Source implementation | Docs/07:21; Docs/17:11–13; ExecutionJournal duplicate-before-digest scope ERR030 |
| Contract status | локальный SOURCE_MISMATCH по ERR030; durable handler NOT_IMPLEMENTED |

### A03-FSM-N09

| Field | Finding |
|---|---|
| CurrentState | любое состояние с critical conflict |
| Event | identity/persistence/margin/unknown-position critical error |
| Trigger | независимое расхождение или неустранимая ошибка |
| Preconditions | остановить новые финансовые действия |
| Identity guard | не подставлять presented как expected |
| Money guard | не считать неизвестный ресурс доступным |
| Risk guard | stop при critical risk |
| Margin guard | stop при critical margin |
| Proof authority | independent actual records, не локальный validity flag |
| Expected positions | состав может быть неизвестен; no auto-adoption |
| Planned action | emergency/reconcile/manual decision |
| Actual execution outcome | CONFLICT либо critical error |
| Partial-fill behavior | не объявлять completed |
| Timeout behavior | reconcile before any retry |
| Restart behavior | no auto-resume |
| Persistence requirements | сохранить конфликт и достаточно данных для разбора |
| NextState | EMERGENCY→TERMINAL_SAFE/MANUAL_REVIEW; общий conflict→RECONCILING; приоритет SPECIFICATION_GAP |
| Rollback / compensation | Emergency liquidation сама требует отдельного ownership/actual плана |
| Fail-closed behavior | no auto resume |
| Forbidden transitions | critical conflict→automatic normal state |
| Source implementation | Docs/06:16–22; Docs/17:20–22; target helpers дают локальные targets без severity context |
| Contract status | SOURCE helpers PARTIAL; normative priority SPECIFICATION_GAP |

## B. Реализованная relation пар состояний

Include/Core/HSBI_StateMachine.mqh:5 проверяет только (from,to), без Event/Outcome/Partial/Timeout/Restart, MoneyState, ownership, ledgerApplied или persisted result. Поэтому следующие правила не являются безопасными financial transitions.

| Rule | Условие | Реальный эффект / граница |
|---|---|---|
| I01 | from=to | true для self-pair; не exact-event replay API |
| I02 | DISABLED→IDLE→INITIAL_PLAN_READY→INITIAL_OPENING_BUY→INITIAL_OPENING_SELL→INITIAL_LOCK_ACTIVE→INITIAL_PLUS_CLOSING→FAR_ACTIVE→CANDIDATE_PLANNED→BASKET_OPENING_CORE | девять смежных пар true; дальнейший normal chain отсутствует |
| I03 | RECONCILING→TERMINAL_SAFE/FAR_ACTIVE/IDLE | true без reconciliation result proof |
| I04 | любое from→RECONCILING/TERMINAL_SAFE/EMERGENCY | true без severity input |
| I05 | остальные допустимые enum-пары | false |

Ручной подсчёт по33 объявленным состояниям: self33 + universal-target99 − overlap3 + normal9 + reconciliation-дополнения2 =140 разрешённых пар из1089;949 запрещённых. Это set-union исходного выражения, не запуск функции. Некорректные cast enum не входят в denominator. Допущение корректного enum не проверяется внутри helper.

Propose:6 вычисляет proposedRevision=revision+1 для allowed без ulong-overflow guard. Apply:7 пишет previous/current/revision, не проверяя обязательные financial proofs. Это topology helper; его наличие не доказывает ошибочное продвижение в текущем main: main не подключает эти financial paths. NoTradeExecution остаётся запрещающим stub. Объявления DTO/enum не являются обработчиками. Полный OnTradeTransaction handler отсутствует.

## C. Двадцать обязательных аналитических случаев

| Case | Аналитический вывод | Normative / source boundary |
|---|---|---|
| A01 Far SELL | При благоприятном росте BUY Core/Trend компенсируют SELL Far/Small только при C+T−S−F>0 и корректной money conversion/costs. Это не гарантирует fill или FinalClose. | F001/F005/F038/F039; полная цепочка отсутствует |
| A02 Far BUY | Mirror требует благоприятного падения, не универсального P+tick. Actual BigCore residual нужен для NewFar. | ERR020/041/046; mirror не handler |
| A03 Неполное открытие | Volume<planned: pending, запрещено считать полную корзину созданной. | N03; broker lifecycle NOT_IMPLEMENTED |
| A04 Неполное закрытие | Remaining actual position надо перечитать; следующая роль не разрешается. | N03/N04; ERR010/041 |
| A05 Повторный event | Одинаковое тело: NO_OP/zero delta; изменённое: CONFLICT. Проверка body до duplicate decision обязательна. | N08; ERR030 |
| A06 Повторный intent | Повтор экономического ActionID нельзя превращать в новый источник/действие; PlanID не заменяет SourceKey. | Docs/07:17–18; global backend NOT_IMPLEMENTED |
| A07 Цена изменилась | Старый snapshot не доказывает новый риск, margin или Catch-Up. Требуется свежая оценка до необратимого шага. | ERR024/025/041/050 |
| A08 Отказ брокера | Reject не продвигает FSM. Retry только после recheck с тем же экономическим ActionID. | N06; полный outcome mapping gap |
| A09 Gap | Lot-slope и конечный reserve не ограничивают безусловный убыток открытого Far; execution price может не совпасть с plan. | ERR018/019/032; safety promise отсутствует |
| A10 Timeout | Неизвестное исполнение не failure и не completion. Реконсиляция до повторного send. | N05 |
| A11 Restart до journal | Нельзя считать действие неисполненным лишь по отсутствию local record; сначала broker/history reconciliation. | N07; crash protocol не реализован |
| A12 Restart после journal | Prepared запись не committed receipt; commit marker/digests и actual history проверяются отдельно. | Docs/16:11–15 |
| A13 Restart после partial | Нужно восстановить accepted fills и outstanding quantity до retry; не повторять их суммирование. | N03/N07/N08 |
| A14 Неизвестная history | UNAVAILABLE/PENDING/CONFLICT в соответствующем API, не нулевой денежный ресурс и не NEW funding. | D02/D08; полного provider нет |
| A15 Snapshot≠journal | Digest/schema/revision mismatch блокирует расход. Fallback предыдущего snapshot требует reconciliation новых сделок. | ERR016/017/035; N07 |
| A16 Reserve недостаточен | Не использовать Reserved другого owner или RemainingGross как Free; отказ zero delta. | D01; ERR004/005/007/048 |
| A17 Неудачный Catch-Up | min margin по обязательным уровням≤0 запрещает candidate; один выбранный уровень не исправляет другой. | CR09; ERR009/014 |
| A18 Small Transition неуспешен | При prefix breach/partial/ownership mismatch не назначать NewFar. D05 choice остаётся pending. | ERR010/024/041; N03/N09 |
| A19 Нет допустимого NewFar | Нет права выбрать planned вместо actual residual; допустимость terminal route проверяется отдельно. | ERR021/031/041/045 |
| A20 Emergency Liquidation | Не мгновенное математическое закрытие: нужен actual ownership, execution и residual reconciliation. При critical conflict no auto-resume. | N09; точный liquidation sequence SPECIFICATION_GAP |

## Незакрытые обязательства

Девять rule cards и20 аналитических случаев не дают полного количества нормативных transitions: FSM_NORMATIVE_TRANSITIONS_TOTAL=NOT_DEFINED. Нужно дочитать оставшиеся исторические FSM authority contracts, разрешить их приоритеты без автоматического утверждения, дополнить каждый scenario-specific переход всеми22 полями и доказать обязательных callers. FSM_SPECIFICATION_GAPS=NOT_FULLY_ENUMERATED. Источники для текущих выводов: Docs/06:6–22, Docs/07:6–25, Docs/16:5–21, Docs/17:3–26; Include/Core/HSBI_Enums.mqh:8–10, Include/Core/HSBI_StateMachine.mqh:5–10, Include/Execution/HSBI_TransactionTypes.mqh:9–23. Формулы F024/F025/F026/F036/F052/F053/F057/F062/F063/F065/F066; ERR010/016/017/024/025/030/031/035/041/049/050; IMP005/008/009/016/019/022. Административные решения остаются AWAITING_ADMIN_APPROVAL.


## R3 — проверка закрытости нормативного домена и точные gaps

Ниже не вводится новая FSM. Повторно сопоставлены полные Docs06/07/09–13/16/17, все33sourceenum и прочитанная целиком AUDIT02_FSM_MATRIX. Исторические 15phase summaries и1089pairrecords не замещают нормативную relation. Дополнительно полностью прочитаны Tests/Static/hsb_2e_fsm_transitions.json (16historical transitions), hsb_2e_transaction_lifecycle.json (18historical event records) и hsb_2e_persistence_schema.json. Результат: существует ещё одна **историческая qualification** модель состояний, не совпадающая с36Docs06 и33source. Наличие файла с FSM в имени не разрешает принять BOOTSTRAP/INTENT_PREPARED/SIMULATION_DISPATCHED как новые production states.

### Установленные границы доменов

| Домен | Доказанный состав / source | Незаполненная часть |
|---|---|---|
| Scenario states | 36 имён Docs06:6, включая4ACTION-phase names;33enum Include/Core/HSBI_Enums.mqh:8 | Orthogonal action state vs scenario state не задан формальным product/embedding |
| Transaction events | 8enum EventType;7enum TransactionOutcome; Docs07:15,21 раскрывает accepted/placed/partial/done/reject/timeout/delayed | Requote/no money/market closed/connection и restart/debounce/reconcile не имеют полного typed mapping |
| Partial outcomes | Docs06:9,15;07:15,21;13:12–14: следующийfinancialstepзапрещён доactualcompletion | Exactbatch completeness/multi-ticket/reversal mapping не полная таблица поscenario |
| Timeout outcomes | Docs07:21;17:12: PENDING/CONFLICT послеhistoryrecheck | Выбор PENDING vs CONFLICT/nextscenario и conflictpriority не задан полностью |
| Restart outcomes | Docs16:15;17:7: CLEAN_START/RECONCILED/PENDING/CONFLICT/REJECTED/TERMINAL_SAFE | Это outcomes,неавтоматическиscenario enum; outcome→resumeState не задан длякаждого interruptedphase |
| Terminal states | Docs06:6,18: CYCLE_CLOSED,TERMINAL_SAFE,MANUAL_REVIEW; emergency отдельна | Conditions выбора safe/manual/emergency иразрешённогоmanualresume требуютownerdecision |

### Индивидуальные specification gaps

Эти под-ID — прослеживаемые пункты внутри существующих ERR016/028/017/030, не новый конкурирующий реестр ошибок и не10новых подтверждённых source defects.

| GapID | Точный нормативный источник / контрпример неоднозначности | Что нельзя вывести | Владелец будущего решения / связь |
|---|---|---|---|
| R3-FSM-SG01 | Docs06:6,12,15; Enums:8: scenario BASKET_ACTIVE и action PARTIAL_FILL должны сосуществовать, но оба представлены состояниями одной prose list | Приоритет/embedding scenario×action; cardinality полногоState domain | Core/Execution; ERR016/028; IMP008/018 |
| R3-FSM-SG02 | Docs07:15 перечисляет broker causes, но EventType содержит только8enum | Total событие/исход для requote,connectionfail,staleprice,reconciliation,debounce,restart | Execution/Scenarios; ERR016/028; IMP008/009 |
| R3-FSM-SG03 | Docs06:12 reject→RECONCILING,06:18criticalconflict→EMERGENCY;07:21samekeyconflict→TERMINAL_SAFE;06:22conflict→RECONCILING | ЕдинственныйNextState при одном событии, удовлетворяющем двум rules; нужен severity/phasepriority | Core/administrator; ERR016/028; IMP008/018 |
| R3-FSM-SG04 | Docs06:21 говорит каждоеstate задаёт roles/PendingAction/PlanID/revision/timeout, но не даёт таблицы соответствий36states | Допустимые payload/timeout/stateinvariants длявсехstate | Core/Scenarios; ERR016/028; IMP008 |
| R3-FSM-SG05 | Docs09:12 BUYactualfilled,SELLincomplete→отдельныйrollbackBUY; при partialSELL иpartialrollbackBUY positions неодинаковы | Nextstate/resume/compensation при частичных необратимых действиях; cannot assume IDLE | InitialLock/Execution; ERR016/028; IMP008/009 |
| R3-FSM-SG06 | Docs13:12–14 требуетclosingchain; Trend=0 допускаетсягеометрией, но explicit FSMskip/NO_OP-roleprecondition не перечислен | Нуженлиcompleted zero-volumeaction или deterministic skip; nativebookkeeping не разрешает inventedfill | SmallTransition/Execution; ERR016/028/041/045; IMP008/016 |
| R3-FSM-SG07 | Docs16:15 и17:7 описываютreconciliationoutcomes; restartafterfillbeforeledger/afterledgerbeforemarker различны | Полная resume relation длякаждого irreversiblephase; новыйfundingотsnapshot недопустим | Persistence/Money; ERR013/017/030; IMP009/014 |
| R3-FSM-SG08 | Docs12:15 разрешает sequential/parallel actions поplan; конкретныйprefixexecutionenvelope иfailurecompensation нефиксированы | Loss/risk/margin при partialfinalclose и оставшихся позициях, rollback не может отменитьfill | FinalClose/Risk; ERR016/028/037/038/041; IMP008/016/020 |
| R3-FSM-SG09 | Docs06:18 запрещаетautoresume,17:23 требуетexplicitadmin+newrecon; полногоmanualevent/admissiondomain нет | Единственная resume-state/actionset послеcriticalerror, неизвестныйadminmessage неразрешение | Administrator/Core; ERR016/028; IMP008/018 |
| R3-FSM-SG10 | Tests/Static/hsb_2e_fsm_transitions.json:2–321 имеет16другихstageevents; transaction_lifecycle:4–16 ACCEPTED→TX_PARTIAL;89–103 TIMEOUT RETRY_ALLOWED=true; persistence_schema:48 atomicrename label | Этиhistorical rows не закрывают currentnormFSM: state mapping/partialsemantics/retrypreconditions/commit guarantee нельзя переносить молча | Normative owner/Execution/Persistence; ERR017/027/028; IMP009/017/018 |

### Метод подсчёта и текущий результат

- 36normative state names,33source state names,1089source pairrecords,140allowedtopologicalpairs,15historicalphase summaries,16qualificationstage transitions и18transaction rows — **разные множества**. Они не суммируются и не называются полными финансовыми переходами.
- ДевятьA03-FSM-N01..09 выше — индивидуально разобранные normative rulefamilies,а не9атомарных State×Event outcomes. Они и20аналитических specialcases не выполненные тесты.
- Новые10SG — конкретный установленный minimum specification-gap set. Финальный count может расшириться при оставшемсячтении, не обещаетсяисчерпывающим.
- FSM_NORMATIVE_TRANSITIONS_TOTAL=UNDEFINED_BY_NORMATIVE_DOMAIN: SG01/02нефиксируют полный domain,SG03даёт пересекающиесяразныеNextState. Число не получается возведением36×8×7 встепень: это включило бы бессмысленные/запрещённыеcombination иизобретённыеrules. Для конечного total необходимо утверждённое version/domain+prioritymapping,а не новый подсчёт строк.
- FSM_IMPLEMENTED_FINANCIAL_TRANSITIONS=0 вmain:19–44; нетOnTradeTransaction/orchestrator/ledgercommit. Это не утверждение,что0puretransitionhelpers: pairpredicate иApplyPureStateTransition существуют,ноневызываютсяmain.
- Нормативное исследование пока PARTIAL,поскольку дополнительные применимыеmachinecontracts иисторическиепредложения ещё читаются. НиодноSG не разрешено молча;16admin decisions остаютсяpending.

## R6 — повторное сопоставление17 обязательных областей

Документы inventory прочитаны525+6duplicates; прежние фразы «осталосьдочитать» являются HISTORICAL. Это закрывает чтение,а не полную FSM relation. Нормативные06–17 и04/05/24–32 перечитаны адресно; preserved9rulecards/10SG. Все приведённые ниже17cases — аналитические группы,не17новыхstate и не17атомарныхtransitions. Financial ProductionSource длякаждойстроки: NOT_IMPLEMENTED; main19–44,NoTradeExecution5–8; StateMachine5–10 предоставляет толькоpuretopology,RuntimeBarrier7–17толькоdecision. Durable evidence/actualmutation/rollbackbackend длявсехстрок NOT_IMPLEMENTED. Risk/money/identityguardsдоactionобязательнынормативно; конкретныеграницыR6-B01..20guardcrosswalk.

| Область | Нормативное state/phase | Docs clause | Preconditions/required actual evidence | Partial/timeout/restart/fail-closed boundary | Gap | Production status |
|---|---|---|---|---|---|---|
| Initial Lock | IDLE/INITIAL_* | 09:8–16 | clean start;BUY actual thenSELL; rollback separate | partialSELL/rollback outcome unspecified | SG04/05 | NOT_IMPLEMENTED |
| Far | FAR_ACTIVE | 09:16;04:12–21 | oneactualFar;immutablecandidate | no candidate→reject;unknown→reconcile | SG04 | NOT_IMPLEMENTED |
| Big Harvest | BASKET_ACTIVE/BIG_HARVEST_* | 10:5–15 | typedtrigger;identity;actualsettlement;allocation | partialnoadvance;timeoutreconcile | SG04/07 | NOT_IMPLEMENTED |
| Reserve/Allocation | ALLOCATION_PENDING | 08:12–24;32:3–7 | sourceeligible/vector/phase/owner/replay | conflict→reconcile;freezeunknown | SG03/07 | NOT_IMPLEMENTED |
| Catch-Up | planning gate; no standalone state asserted | 04:15;30:3–7 | lot+money+scope+provider | failcandidate;CR09requiredscopepending | SG04 | NOT_IMPLEMENTED |
| Partial Far | PARTIAL_FAR_PLANNED/EXECUTING | 11:5–13 | budgetonly;reserve→actualconsume/release | partialremainsexecuting;restartreservationrebuild | SG04/07 | NOT_IMPLEMENTED |
| Small confirmation | BASKET_ACTIVE→SMALL_CONFIRMING | 05:24–25;13:6 | freshrepeat/hold/debounce/noactive | duplicateNO_OP;stale→reconcile | SG02/04 | NOT_IMPLEMENTED |
| Small close | SMALL_CLOSING | 13:12–20 | allactualSmallfillsbeforeOldFar | partialblocksnext;capbreachstop | SG04/07 | NOT_IMPLEMENTED |
| OldFar close | OLD_FAR_CLOSING | 13:12–20 | priorSmallcomplete;actualOldFarclose | partialblocksTrend;noinventedrollback | SG04/07 | NOT_IMPLEMENTED |
| Trend close | BIG_TREND_CLOSING | 13:12–20;04:9 | actualTrendcomplete;optionalzerolegneedsmapping | zeroTrendskipnotdefined | SG06 | NOT_IMPLEMENTED |
| Core reduction/NewFar | BIG_CORE_REDUCING→NEW_FAR_VALIDATING→FAR_ACTIVE | 13:12–20;14:9–26 | actualoriginalCore residual;0<N<F;allgates | mismatch/secondFar→safe;nosafecandidate→reject | SG04/07 | NOT_IMPLEMENTED |
| FinalClose | FINAL_CLOSE_PLANNED/EXECUTING→CYCLE_CLOSED | 12:5–15 | CyclePnLthreshold+coverage;actualzeropositions | partialstaysexecuting;prefixrisknotdefined | SG08 | NOT_IMPLEMENTED |
| Broker rejection/timeout | ACTION_* / scenario orthogonality unspecified | 07:15–21 | noautomaticadvance;historybefore retry | TIMEOUTneitherFAILnorCOMPLETE | SG01/02/03 | NOT_IMPLEMENTED |
| Restart/snapshot recovery | interruptedphase→reconciliation outcome | 16:11–18;17:7–23 | commitmarker/digest/history/pendingactions | fallbackrequiresactualreconcile;noautoresume | SG04/07/09 | NOT_IMPLEMENTED |
| Duplicate execution/journal conflict | anyrelevantactionphase | 07:21;08:15;17:11–14 | samekeyfullbody→NO_OP;changed→CONFLICT | exactzerodelta;changedtargetpriorityconflict | SG03/07 | NOT_IMPLEMENTED |
| Emergency | anycritical→EMERGENCY/TERMINAL_SAFE/MANUAL_REVIEW | 06:18;15:18;17:22–23 | stopnewactions;separateliquidationauthority | nosemanticautoresume;manualdecisionrequired | SG03/08/09 | NOT_IMPLEMENTED |
| Recovery/retry | RECONCILING/ACTION_RETRY_PENDING | 07:18–24;17:9–23 | sameActionID/history+ownership+snapshotrecheck | PENDING≠completed;missingjournalnocredit | SG01/02/07/09 | NOT_IMPLEMENTED |

Точные event/outcome domains остаются неоднозначными:36prose states против33enum;07typedbroker causes не полнаяeventтаблица; SG03разныеNextState дляпересеченияconflict rules. Точное FSM_NORMATIVE_TRANSITIONS_TOTAL не выводится из доступного текста без утверждения embedding/actiondomain/priority; это доказанный specification gap,нечисло0. Параллельные/последовательные FinalClose и partial rollback InitialLock не имеют exhaustive compensation relation. Это не разрешает выбратьудобнуюветку. 140allowedpairs=33+99−3+9+2,а0financialhandlers — отдельныйset. Полная clause-level relation/traceability ивсеcrossreferences ещё требуют проверки,поэтому общий AUDIT_COMPLETENESS остаётсяPARTIAL.

## R7_CLAUSE_LEVEL_TRANSACTION_RELATION

Документы06 и07 повторно прочитаны целиком для конкретного основания: закрытие clause-level relation и проверка противоречивых error routes. Ни один переход не исполнялся. 18 строк ниже — **clause/condition relations**, не 18 независимых финансовых transitions и не полный нормативный denominator. Они сохраняют существующие9 rule cards и SG01–SG10. Источники: `Docs/06_STATE_MACHINE_SPECIFICATION_RU.md` и `Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md`; source baseline неизменён.

| RelationID | Clause | Event/outcome | Required relation / guard | Guard / source evidence | Implementation / caller | Existing gap |
|---|---|---|---|---|---|---|
| R7-TR-01 | Docs/06:9;07:15 | REQUEST_SENT / ACCEPTED / PLACED | not complete; pending | TX01; GRD018/019 | NOT_IMPLEMENTED; no financial advance | SG01/02 |
| R7-TR-02 | Docs/06:9,15;07:15 | DONE_PARTIAL | incomplete; next role forbidden | TX01/TX08; F062 | NOT_IMPLEMENTED; pending partial handling | SG01/04 |
| R7-TR-03 | Docs/06:9;07:15 | DONE | candidate only; actual deals AND positions required | TX04/05; GRD018/019 | LOCAL_FLAGS_ONLY; not broker evidence | SG02/07 |
| R7-TR-04 | Docs/06:9;07:6 | advance after completion | ledger application required | ledgerApplied metadata not read by TransactionBarrierPassed:9–18 | MISSING_IMPLEMENTATION / MISSING_CALLER | SG07 |
| R7-TR-05 | Docs/06:9,12;07:6 | advance after ledger | persisted result required, not prepared marker | GRD045 is prepared only | MISSING_IMPLEMENTATION / MISSING_CALLER | SG07 |
| R7-TR-06 | Docs/06:12;07:6 | new irreversible action | PersistAction before OwnershipGuard before Send | GRD019/045; order not global proof | NOT_IMPLEMENTED; main uses no-trade stub | SG04/07 |
| R7-TR-07 | Docs/06:12;07:15 | reject/requote | RECONCILING; do not advance completed role | StateMachine:8 conflict target only | NOT_IMPLEMENTED; typed event handler absent | SG02 |
| R7-TR-08 | Docs/06:12;07:21 | timeout | reconciliation barrier; neither failure nor completion | TX01 rejects timeout label only | NOT_IMPLEMENTED; next scenario state unspecified | SG02/04 |
| R7-TR-09 | Docs/06:15 | Small confirmation | BASKET_ACTIVE→SMALL_CONFIRMING iff fresh repeated snapshot AND debounce | GRD011 only freshness subset | NOT_IMPLEMENTED; trigger handler absent | SG04/06 |
| R7-TR-10 | Docs/06:15 | sequential Small closes | immutable plan; next role only after actual full completion | GRD001/020/021; TX01/TX08 | NOT_IMPLEMENTED; actual prefix handlers absent | SG04/07 |
| R7-TR-11 | Docs/06:18,22;07:21,25 | critical identity/persistence/conflicting key | EMERGENCY/SAFE/RECONCILING priority conflicts | StateMachine:8–10 different target functions | NORMATIVE_CONFLICT; no priority chosen | SG03 |
| R7-TR-12 | Docs/06:18,22 | automatic resume | forbidden; manual review required | no production resume handler | NOT_IMPLEMENTED; permission/event domain absent | SG09 |
| R7-TR-13 | Docs/06:21;07:24 | restart before new request | restore pending/attempts; reconcile history/positions/orders first | GRD014/015/045/047 not durable provider | NOT_IMPLEMENTED; durable restart absent | SG04/07 |
| R7-TR-14 | Docs/07:12 | ownership mismatch before action | block action; reconciliation | GRD019 is flag not all tuple components | LOCAL_ONLY; independent owner evidence missing | SG02/04 |
| R7-TR-15 | Docs/07:18 | retry | same ActionID AND no completed deal AND reread history AND PENDING AND state permits AND no duplicate AND revalidated ownership/snapshot | RetryAllowed:20–22 only subset; GRD017 not retry equality | INCOMPLETE; NO_CALLER_FOUND | SG02/04/07 |
| R7-TR-16 | Docs/07:18 | retry attempt persisted | new child attempt ParentActionID; same economic action | TransactionTypes has no durable attempt registry | NOT_IMPLEMENTED | SG07 |
| R7-TR-17 | Docs/07:21 | identical delayed event | EventKey immutable equality→NO_OP, no duplicate mutation | GRD050/060/061 are local ledger replay predicates | NOT_IMPLEMENTED global dispatch/replay | SG02/07 |
| R7-TR-18 | Docs/07:21 | fill accumulation | sum actual volume AND signed DealNet to exact completion | TX08 scalar epsilon not accumulated deals provider | INCOMPLETE; financial accumulator absent | SG02/07 |

Полный текстовый поиск всех74 production sources по именам `HSBI_ApplyPureStateTransition`, `HSBI_TransactionBarrierPassed`, `HSBI_RetryAllowed` нашёл только собственные объявления (соответственно StateMachine:7 и TransactionTypes:9,20). `NO_CALLER_FOUND` относится к этой области поиска и не означает native/preprocessor proof. ApplyPureStateTransition доступен как public pure API и проверяет лишь topology; его возможный прямой будущий caller обязан добавить barrier, actual money и persisted result. Текущий торговый обход не объявляется: финансового caller нет. Связь ERR010/016/017/028, IMP008/009/017, F057/F062/F063/F065; D-07/SNAP-FIXTURE-1 остаются AWAITING_ADMIN_APPROVAL.

### Domain/count boundary

Docs06:6 перечисляет36 нормативных state labels, включая4ACTION phases; source enum имеет33 labels, но source flat enum не определяет embedding scenario×action. Docs07:15 перечисляет broker outcomes, но не задаёт исчерпывающий Event enum, per-state applicability, timing precedence или restart outcomes. Поэтому числовые FSM_EVENTS_TOTAL и полный FSM_NORMATIVE_TRANSITIONS_TOTAL не выводятся из этих строк; SG01/02/04 сохраняются. Известные36 labels нельзя автоматически умножать на source8 events и7 outcomes. 140 source topology pairs не принимаются за financial transitions.

Отдельно не закрыто: все scenario-owner clauses09–17 и поздние amendments должны быть индивидуально соединены с этой relation; таблица выше не заменяет этот остаток и не оправдывает COMPLETE.
