# HSBI — NEXT STAGE 02A
## Полный независимый аудит денежной целостности, нормативных контрактов и доказательств

## 1. Паспорт проверки

| Поле | Значение |
|---|---|
| Проект | Hybrid Split Big Independent EA |
| Этап | HSBI_NEXT_STAGE_02A |
| Режим | локальный Git checkout; remote проверен read-only через GitHub HTTPS proxy |
| UTC начала | 2026-11-01T00:15:25Z |
| Ветка | work |
| Baseline | `6bb6a2f75f8fb0d5d51b1259476ddc47477eaaa3` |
| Remote baseline | совпадает |
| Рабочее дерево до аудита | чистое |
| Файлов в разрешённом каталоге | 1015 |
| Tree-list SHA-256 | `6b879ede76e6728b678d9c61797c467ba42fe6a5ea6d5679fae60740168b6a5b` |
| Python | 3.12.14 |
| MetaEditor / MT5 / Wine | недоступны |
| Production changes | запрещены и не выполнялись |

История и два предыдущих отчёта проверены. HEAD совпал с ожидаемым SHA, поэтому audit-only записи разрешены ТЗ. Автоматические reset/rebase/merge не выполнялись.

## 2. Исходный Git SHA

Baseline `6bb6a2f…` содержит Stage 02 money audit. Родитель `de84a8a…` содержит baseline inventory, ранее `9309e0b…` опубликован R12A fix. Исторические PASS-блоки не считаются свежим разрешением.

## 3. Проверенные документы

Нормативное ядро изучено по `Docs/00–32`: charter, glossary, identity, full manual, math, geometry, FSM, execution, ledger, Initial Lock, Big Harvest, Partial Far, Final Close, Small Transition, New Far, risk, persistence, reconciliation, architecture, traceability, testing, readiness, decisions, broker money/grid/control prices, Future Small, candidate objective, proof identity и reserve allocation/consumption. Дополнительно сверены HSB.2C/2D/2E contracts, current README/BUILD/PROJECT_MAP, Stage 01 и Stage 02 audits, R12A contracts/vectors/reports.

Иерархия:

1. Явные текущие normative decisions и contracts с более поздней ревизией.
2. `Docs/00–32`, если не superseded и нет конфликта.
3. Implementation handoff и test contracts как проверяемая спецификация, но не источник разрешения торговли.
4. Reports/Evidence/README status blocks — исторические доказательства; не норматив сами по себе.

При неоднозначности применён `CONFLICT/DECISION_REQUIRED`, а не выбран удобный вариант.

## 4. Проверенные исходники

Проверены 74 production-файла: main `.mq5` и 73 include. Основные цепочки: broker money/margin/cost, basket/candidate/level evaluators, money identity, economic/allocation ledgers, Reserve Catch-Up, Future Small, New Far, execution intent/preflight, journal/snapshot/restart validators, runtime barrier и no-trade guard.

Главный EA остаётся non-trading skeleton. `OnTick` вызывает только `HSBI_SubmitActionStub`; production scan дал ноль вызовов `OrderSend`, `CTrade`, `PositionOpen/Close`, `TRADE_ACTION_`, `OnTradeTransaction`.

## 5. Нормативная матрица

| RequirementID | SourceDocument / Section | Formula / правило | Preconditions / invariants | ProductionFunction | TestCoverage / Evidence | Status | DecisionRequired |
|---|---|---|---|---|---|---|---|
| MONEY-01 | 24 Broker Money | `ProjectedNet=OrderCalcProfit-Costs-Buffer` | fresh broker properties, valid grid, typed price | `HSBI_CalculateProjectedProfit` | static read; R8 price/economic oracle | PASS в static scope | нет |
| MONEY-02 | 24, 27 Control Prices | BUY close Bid; SELL close Ask | fresh Bid/Ask, symbol binding | basket leg input | R8 price authority | PASS в reference/static scope | нет |
| MONEY-03 | 08 Ledger | `DealNet=Profit+Swap+Commission+Fee` | confirmed actual deal, broker signs | economic ledger DTO/cost helpers | broker execution NOT_RUN | UNPROVEN | нет |
| MONEY-04 | 31 Proof Identity | proof связан с actual source | independent deal/event/snapshot | proof identity validators | self-copy counterexample | FAIL | да, provenance owner |
| ALLOC-01 | 08 vs 32 | full equality или upper bound | confirmed allocatable actual DealNet | allocation validator | static counterexample | CONFLICT | да |
| ALLOC-02 | 32 | buckets nonnegative, finite, no over-allocation | reconciled source | `HSBI_ValidateReserveAllocationSource` | static | PASS в локальном scope | нет |
| RESERVE-01 | 31 | Reserve source role BigCore/BigTrend | positive projected proof; actual availability separately proven | `HSBI_ValidateReserveSourceProof` | static | PASS только role gate | нет |
| RESERVE-02 | 31/32 | Small не становится Reserve source | role-authoritative allocation | basket aggregate | vector `0,0,10` | FAIL | да, Small bucket |
| CONSUME-01 | 32 | consumption bound to allocation source | identical source keys and IDs | allocation/catch-up validators | M01-B/C | FAIL | нет для факта; да для exact contract |
| CONSUME-02 | 16/32 | no double spend after restart | durable registry restored | one prior key + restart DTO | M01-D/F | UNPROVEN | да, replay outcome |
| CATCHUP-01 | 30/31/32 | `ReserveGain-FarLossIncrease-Buffer>0` | volume gate, authoritative proofs | Reserve Catch-Up evaluator | local numeric/static | PASS локальной арифметики | нет |
| CATCHUP-02 | 30 | positive margin implies finite recovery | persistent actual Reserve and feasible future steps | none end-to-end | no broker/runtime proof | UNPROVEN | нет |
| RECOVERY-01 | 04/08/31 | projected and actual funds separated | confirmed closing deals before allocation | basket and money state | M04 | UNPROVEN | да, naming/type |
| FARLOSS-01 | 30 | absolute or incremental Far loss | baseline definition | basket/Catch-Up | M06 table | CONFLICT | да |
| TRANSITION-01 | 08 vs projected solver | actual closing DealNet vs projected risk loss | distinct lifecycle phases | basket/Future Small | M07 | CONFLICT | да |
| BUFFER-01 | 24/30 | per-leg and Catch-Up buffers | independent risk purposes | leg money + Catch-Up | M08 | CONFLICT | да |
| FS-01 | 27 Future Small | `0<F(n+1)<=qF(n)` | q<1, grid, finite levels | Future Small solver | R8/reference | PASS geometric bound scope | нет |
| FS-02 | 27/30 | actual finite executable recovery | money, risk, margin, broker and every next candidate | Future Small/New Far | MT5 NOT_RUN | UNPROVEN | нет |
| NF-01 | 28/29 | unique safe candidate + deterministic tie-break | actual residual, proofs, fresh snapshots | New Far solver | static/reference | PASS algorithmic scope | нет |
| NF-02 | 31/32 | selected candidate uses authoritative money provenance | independent ledger/allocation | New Far→Catch-Up | M01/M02 | FAIL | нет для defect |
| PERSIST-01 | 16/HSB.2D | snapshots/journal before state mutation | durable implementation and digest | persistence interface | stub inspection | FAIL/UNPROVEN | да, storage design |
| RESTART-01 | 16/HSB.2D | exactly-once after restart | complete durable history | restart validator | reference tests only | UNPROVEN | нет |
| TRADE-01 | runtime policy | dispatch prohibited | all modes | runtime policy/no-trade stub | production scan | PASS | нет |

## 6. Полная карта денежной модели

```text
Broker symbol + Bid/Ask + properties
  → OrderCalcProfit / OrderCalcMargin wrappers
  → projected per-leg money (Far/Core/Trend/Small)
  → projected basket / risk / margin
  → Future Small level proofs
  → candidate aggregate

Broker confirmed deal
  → actual economic ledger record
  → allocatable DealNet
  → allocation buckets (Reserve/PartialFar/Transition/Carry/Residual)
  → consumption registry
  → Catch-Up authorization
  → New Far decision
```

Первая цепочка частично реализована как pure calculation. Вторая существует главным образом как DTO/validators; durable broker-to-ledger-to-consumption pipeline отсутствует. Поэтому projected proof не может заменять actual availability.

## 7. M-01 — Reserve Consumption Binding

Дефект подтверждён. Allocation source и consumption key валидируются независимо. Нет обязательных сравнений sourceDealKey/sourceAllocationKey, account/symbol/magic/cycle и allocation event с authoritative record.

Сценарии:

- A: согласованный источник — локально возможен PASS, end-to-end UNPROVEN.
- B: чужой sourceDealKey — ошибочно может пройти, FAIL.
- C: чужой sourceAllocationKey — ошибочно может пройти, FAIL.
- D: exact prior key — блокируется как duplicate, но outcome semantics требует решения.
- E: изменённый повтор с тем же allocation/event — conflict, PASS локального guard.
- F: restart — UNPROVEN; production persistence stub, а `hasPriorConsumption=false` отключает знание прошлого.

Влияние: ложный Catch-Up может сделать небезопасный New Far кандидатом. Исправление требует cross-object binding и durable registry, а не только дополнительного boolean.

## 8. M-02 — независимость Money Proof Identity

Дефект подтверждён. New Far формирует identities с caller-supplied deal/event IDs, записывает их в proof и затем копирует те же identities в expected fields. Equality остаётся тавтологичной относительно provenance.

Требуемая цепочка: terminal deal history → reconciled immutable ledger record → allocation source → proof reference/digest → consumption record → Catch-Up. На каждом переходе проверяются account, symbol, magic, cycle, position, deal, event, plan, revision, snapshot, amount и uniqueness.

Негативная матрица M02-01–14 записана в `Tests/Contracts/NEXT_STAGE_02A_TEST_MATRIX.json`. Часть identity field mismatches локально отклоняется, но nonexistent IDs, stale authoritative source, wrong DealNet, missing/consumed allocation и restart replay остаются UNPROVEN.

## 9. M-03–M-08

### M-03 Allocation Conservation

Текущий код реализует верхнюю границу. Вариант полного учёта требует equality и residual bucket. Вариант частичного учёта требует `Unallocated`, transaction phase и обязательной reconciliation. Решение D-01.

### M-04 RecoveryMoney

Basket `recoveryMoney` равен projected basket net четырёх ног. Это допустимая оценочная метрика, но не settled fund. Требуются разные типы/имена, решение D-02.

### M-05 ReserveGainMoney

Формула включает Small. При Core=0, Trend=0, Small=10 возвращает 10, несмотря на role gate BigCore/BigTrend для authoritative Reserve proof. Дефект aggregate semantics подтверждён; прямой double spend через это поле не доказан, поскольку основной Catch-Up использует отдельный Core proof.

### M-06 FarLossIncrease

Для baseline loss 40 и current loss 50 absolute=50, incremental=10. При ReserveGain=60 и buffer=5 Catch-Up margin будет 5 либо 45. Выбор меняет решение, поэтому требуется D-04.

### M-07 TransitionLoss

Projected loss нужен risk gate; actual realized loss нужен ledger/accounting. Они не должны иметь взаимозаменяемый тип. Требуется D-05.

### M-08 SafetyBuffer

При per-leg buffer=1 четыре legs вычитают 4, Catch-Up дополнительно 1. Итого 5. Корректность зависит от независимости покрываемых рисков; требуется D-06.

## 10. Broker money

Код корректно выбирает Bid для закрытия BUY и Ask для SELL, различает point/tickSize, проверяет volume min/max/step и fail-closed обрабатывает недоступный `OrderCalcProfit/OrderCalcMargin`. Однако currency conversion, calculation mode, hedging/netting и реальные broker properties на текущем symbol/account не проверены: MetaTrader отсутствует. Статус broker-specific proof — NOT_RUN.

## 11. Projected/actual separation

DTO различают projected/actual и source identities. Нарушение находится на системной границе: projected basket получает слишком общее имя `recoveryMoney`, а authoritative actual pipeline не реализован. Запрещено переносить projected сумму в Reserve/settled bucket без confirmed deal, allocation и replay check.

## 12. Reserve allocation

Положительно: finite/nonnegative checks, source keys/IDs, policy version, confirmed/reconciled flags, over-allocation guard. Недостаточно: не определён unallocated remainder; caller flags не доказывают durable source; allocation registry отсутствует.

## 13. Reserve consumption

Положительно: duplicate и altered conflict helpers. Недостаточно: M-01, один prior key, нет полного history lookup, нет durable exactly-once. Exact replay semantics DECISION_REQUIRED.

## 14. Catch-Up

Локальные размерности согласованы: `reserveShare*netBigVolume > farVolume`, денежный margin строго больше нуля. Но один положительный margin не доказывает конечное восстановление. Нужны actual Reserve accumulation, price-path stability, existence каждого следующего candidate, broker execution, margin/risk feasibility и restart safety.

## 15. Зависимости Big

Big зависит от projected Core/Trend profits, Far loss, actual Harvest DealNet, allocation, Reserve, Partial Far и Catch-Up. Геометрия не менялась. Глобальная монотонность RecoveryPL не доказана; допустима только локальная формулировка при фиксированных snapshots/cost policy и существующем feasible next step.

## 16. Зависимости Small

Small требует compression, reduced risk/exposure, money/margin gates, broker grid, unique Far, actual residual BigCore и допустимый transition loss. Геометрический bound с q<1 не доказывает существование денежно и брокерски исполнимого шага на каждом уровне.

## 17. Зависимости New Far

```text
Actual Deal [UNPROVEN runtime]
 → Money Ledger [contract only]
 → Allocation [local validation; conservation conflict]
 → Reserve [role gate; provenance FAIL]
 → Consumption [M-01 FAIL]
 → Catch-Up [local arithmetic PASS; source proof FAIL]
 → Future Small [reference/static PASS; runtime UNPROVEN]
 → New Far [algorithmic gates PASS; economic authorization BLOCKED]
```

Следующий независимый New Far audit должен проверить unique Far, compression, grid normalization, risk/margin/transition gates, objective/tie-break, residual provenance, stale/foreign source, restart/replay и fail-closed paths после закрытия M-01/M-02.

## 18. Persistence/restart

Необходимо сохранять cycle/plan/revision, confirmed deals, allocation/consumption registry, bucket balances, positions, pending outcomes и reconciliation state. Текущий persistence interface — stub. Поэтому restart после Harvest/allocation/consumption/partial fill/dispatch-before-outcome классифицирован UNPROVEN. Pure restart validators не заменяют durable IO.

## 19. Независимые тесты

Свежие результаты приведены в `Reports/NEXT_STAGE_02A_TEST_EXECUTION_RU.md`. Актуальные Python reference suites прошли, frozen R7 verifier дал 57/62 из-за устаревших manifest/status expectations. MetaEditor, MQL5, Strategy Tester и broker checks — NOT_RUN. Матрица независимых vectors и mutations создана, но production source mutations не исполнялись.

## 20. Подтверждённые дефекты

1. M-01 foreign consumption/allocation keys не связаны.
2. M-02 self-confirming expected proof identity.
3. M-05 aggregate reserveGain включает Small вопреки разрешённым Reserve roles.
4. Production persistence отсутствует; end-to-end restart guarantees недоступны.
5. R12A canonicalizer сам по себе не является production money verifier.

## 21. Неподтверждённые риски

Broker-specific money/margin, currency conversion, complete ledger conservation, final-close actual accounting, partial-fill recovery, durable replay, finite economic recovery и Strategy Tester behavior.

## 22. Нормативные конфликты

M-03 full/partial allocation; M-06 absolute/incremental Far loss; M-07 projected/actual TransitionLoss; M-08 buffer independence; replay outcome semantics. Все оформлены в decisions report.

## 23. Предложения исправлений

План Stage 02B: authoritative ledger, M-01 binding, M-02 independent lookup, typed money states, approved formula semantics, independent oracle/mutations и runtime verification. План не является разрешением.

## 24. Критерии допуска к следующему этапу

- решения D-01–D-08 утверждены;
- M-01/M-02 исправлены и убиваются mutations;
- actual/projected типизированы и не взаимозаменяемы;
- durable ledger/allocation/consumption/restart доказаны;
- independent oracle не импортирует production formulas;
- MetaEditor/MQL5/broker tests свежие и привязаны к SHA;
- no-trade guard сохранён.

## 25. Итоговый вердикт

`AUDIT_COMPLETE_WITH_BLOCKERS`.

Аудит выполнен, но денежная целостность production pipeline не доказана. M-01 и M-02 блокируют экономическую авторизацию New Far/Catch-Up; M-03/M-06/M-07/M-08 требуют решений администратора; persistence и broker runtime evidence отсутствуют. Реальная торговля остаётся запрещённой.

```text
PROJECT=Hybrid_Split_Big_Independent_EA
STAGE=HSBI_NEXT_STAGE_02A
BASE_SHA=6bb6a2f75f8fb0d5d51b1259476ddc47477eaaa3
FINAL_SHA=NOT_PUBLISHED_YET
AUDIT_STATUS=AUDIT_COMPLETE_WITH_BLOCKERS
NORMATIVE_CONTRACTS=CONFLICT_DECISION_REQUIRED
MONEY_INTEGRITY=UNPROVEN
RESERVE_PROVENANCE=FAIL
RESERVE_CONSUMPTION=FAIL
CATCH_UP=BLOCKED_BY_PROVENANCE
BIG_MONEY_DEPENDENCIES=UNPROVEN
SMALL_MONEY_DEPENDENCIES=UNPROVEN
NEW_FAR_MONEY_DEPENDENCIES=BLOCKED
PERSISTENCE_RESTART=UNPROVEN
METAEDITOR_COMPILE=NOT_RUN
MQL5_TESTS=NOT_RUN
PYTHON_TESTS=PASS_WITH_LIMITATIONS
STRATEGY_TESTER=NOT_RUN
FULL_ECONOMIC_CORRECTNESS=NOT_PROVEN
MODEL_CHANGES_ALLOWED=NO
TRADING_LOGIC_START_ALLOWED=NO
TRADE_REQUESTS_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
ADMIN_DECISION_REQUIRED=YES
```
