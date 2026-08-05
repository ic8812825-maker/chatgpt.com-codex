# Этап 3.1.6.3.17 — независимая приёмка полного аудита MQL5 mapping

## 1. Граница

- Репозиторий: `ic8812825-maker/chatgpt.com-codex`.
- Ветка: `work`.
- Каталог: `MinusLock_BigHarvest_EA_V2`.
- Production `.mq5/.mqh` не изменялись.
- Python не изменялся и не использовался как production-oracle.
- Реальная торговля не включалась.

## 2. Git-цепочка

| Пункт | SHA |
|---|---|
| baseline 3.1.6.2 | `9fb78470baf494d6d4fa7649d5b052d05a71e28a` |
| 3.1.6.3.1 | `281010741341339fefaf5398c9a22d67cadb5f33` |
| 3.1.6.3.2 | `b099a46162bc2f581a3e3612dd72cbb78c719063` |
| 3.1.6.3.3 | `8e86151a8cc5805eeba4d108c475eb1f9bed3196` |
| 3.1.6.3.4 | `812a3d7da84efebcc31046b74efc5ee97e4cdfa4` |
| 3.1.6.3.5 | `53b771c9b8aed859233ed3a0cf1f1bb428536118` |
| 3.1.6.3.6 | `323359ba83effe3469fd4cd61d1a1a9107c650fc` |
| 3.1.6.3.7 | `90ae6d086f3c6a02759376c57bb51f5863026517` |
| 3.1.6.3.8 | `d3b51d4b422598a5f0504d6e93be6bcdb89f33de` |
| 3.1.6.3.9 | `7edb2cd3da7bbbab9f6b4535f3218544797f3154` |
| 3.1.6.3.10 | `a3670efcbdeafe138e442a7d9a04209f449c817c` |
| 3.1.6.3.11 | `e7f35197872f5b1e2f1c68ac97a4627add83110d` |
| 3.1.6.3.12 | `1ad5f47eb14b4e177e06187decf9417d0c48dbe5` |
| 3.1.6.3.13 | `623dc23f020c71c6dcc7fd3c1d2bc4f8accb3b63` |
| 3.1.6.3.14 | `fa5fe96ba9f2fccaa16beb53202af08866d61f0a` |
| 3.1.6.3.15 | `d18588a0ba36a4bdd482d14f4a3c4b5c2fb112da` |
| 3.1.6.3.16 | `8b538c7e0acbc39fe1659d4c208373ea4eff128c` |

Все сообщения коммитов имеют русский формат `Этап 3.1.6.3.N: ...`.

## 3. Проверенные production-файлы

Учтены `MinusLock_BigHarvest_EA.mq5` и все 25 файлов `Include/*.mqh`. Физический include graph зафиксирован полностью. Основной runtime path прослежен через `OnInit`, `OnTick`, `RunStateMachine`, TradeEngine, Split/Hybrid open/close states, persistence и reconciliation.

## 4. Фактическая архитектура

```text
OnInit
→ config/validation/FSM integrity/geometry/environment
→ RecoverState
→ orphan/state/integrity/reconciliation

OnTick
→ risk snapshot
→ periodic reconciliation
→ direct Initial Lock path или RunStateMachine

RunStateMachine
→ Legacy path либо Split path
→ Hybrid только как modifier Split path
→ TradeEngine synchronous requests
→ polling/history/pending/reconciliation
```

`OnTradeTransaction` в production-коде отсутствует.

## 5. Что реально работает

- Legacy Initial Lock и создание Far.
- Legacy default mode.
- Split role topology BigCore/BigTrend/SmallBase.
- Hybrid geometry solver и несколько Hybrid gates при opt-in флаге.
- Hybrid Small order SmallBase→OldFar→BigTrend→BigCore partial.
- Получение actual remaining BigCore и promotion его ticket/identifier в единственный NewFar.
- GlobalVariables persistence, pending fields, role context, Reserve transaction persistence.
- Position/history-based reconciliation и topology checks.

## 6. Что существует частично или только как preview

- Immutable Hybrid CandidatePlan.
- Finite Catch-Up, Worst Case, Margin, Future Small.
- Hybrid Final Close preview.
- Broker-money risk.
- Economic/Allocation ledger 3.1.5 в production MQL5.
- Exactly-once deal lifecycle.

## 7. Что отсутствует

1. `OnTradeTransaction`.
2. Единый request→order→deal→allocation→persist EventKey lifecycle.
3. Обязательный `NO_STATE_ADVANCE_BEFORE_ACTUAL_DEAL` barrier.
4. Атомарная проверка `Symbol+Magic+CycleID+identifier+role` непосредственно в TradeEngine перед каждым action.
5. Единый autonomous runtime enum Hybrid/Legacy/Split.
6. Единый Final Close gate с нормативным RecoveryPLCloseNow на всех routes.
7. Atomic versioned persistence snapshot всего cycle.

## 8. Главные P0

- `RISK-001/MIX-014`: TradeEngine close wrapper атомарно проверяет Symbol+Magic, но не CycleID+identifier+role. При повреждённом caller context существует риск действия над неправильной managed-позицией с тем же Symbol/Magic.

## 9. Главные P1

- Отсутствует OnTradeTransaction.
- FSM advance возможен до actual deal confirmation.
- `PLACED` и `DONE_PARTIAL` могут считаться успехом wrapper.
- Hybrid является modifier Split, а не отдельной основной системой.
- CandidatePlan не полностью immutable/persisted и использует fixed TargetNewFarRatio.
- Risk preview содержит упрощённую формулу.
- Final Close semantics конкурируют.
- Persistence не атомарна.
- Reconciliation не связан с parent transaction events.
- Small Transition money gate не унифицирован с нормативным TransitionBudget contract.

## 10. Вердикт по Hybrid Split Big

Hybrid Split Big **не является полностью активной основной production-системой**. Он существует частично:

- как solver и projected gates;
- как Hybrid branches внутри Split StateMachine;
- как корректный источник actual NewFar из остатка BigCore.

При этом Legacy остаётся default mode, Split остаётся фактическим execution skeleton, а shared StateMachine/TradeEngine смешивают поколения.

## 11. Почему код не исправлялся

Подэтап 3.1.6.3 являлся только аудитом. Массовое исправление StateMachine, TradeEngine, ledger, persistence и transaction flow прямо запрещено. Изменялась только документация.

## 12. MetaEditor и Strategy Tester

```text
METAEDITOR_COMPILE=NOT_PROVEN
MT5_STRATEGY_TESTER=NOT_PROVEN
PRODUCTION_MQL5_READY=NO
REAL_TRADING_ALLOWED=NO
```

## 13. Финальный статус

```text
SUBSTAGE_3_1_6_3_STATUS=PASS
STAGE_3_1_6_STATUS=IN_PROGRESS
NEXT_ALLOWED_SUBSTAGE=3.1.6.4
SUBSTAGE_3_1_6_4_STARTED=NO
AWAITING_USER_APPROVAL=YES
PRODUCTION_MQL5_MAPPING=AUDITED
PRODUCTION_MQL5_CHANGED=NO
PRODUCTION_MQL5_READY=NO
REAL_TRADING_ALLOWED=NO
METAEDITOR_COMPILE=NOT_PROVEN
MT5_STRATEGY_TESTER=NOT_PROVEN
```

`PASS` относится только к завершению аудита и не означает готовность MQL5 или разрешение реальной торговли.

## 14. Остановка

Подэтап 3.1.6.4 самостоятельно не начинается. Требуется отдельное подтверждение Администратора.
