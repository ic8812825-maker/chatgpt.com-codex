# AUDIT 02 — нормативная и реализованная FSM

Нормативный источник: `Docs/03_FULL_SYSTEM_MANUAL_RU.md`, разделы «Полный цикл», «Transaction», «Restart/error». Реализация: `Include/Core/HSBI_StateMachine.mqh` и основной `.mq5`.

```mermaid
flowchart TD
 I[Initial Lock actual fills] --> P[Close InitialPlus actual deal]
 P --> F[One Far]
 F --> C[Immutable candidate and C/T/S actual fills]
 C --> H[Big Harvest actual deals]
 H --> A[Allocation]
 A --> FC[Final Close actual fills]
 A --> PF[Partial Far reservation and actual debit]
 PF --> F
 C --> S[Small confirmation and close]
 S --> OF[OldFar close]
 OF --> T[Trend close]
 T --> CR[Original Core actual reduction]
 CR --> NF[NewFar actual residual validation]
 NF --> F
 FC --> END[Reconciled zero residual]
```

```mermaid
flowchart TD
 INIT[OnInit] --> DIS[Initialize DISABLED]
 TICK[OnTick] --> STUB[SubmitActionStub: blocked]
 STUB --> REASON[Update lastReason only]
 TIMER[OnTimer] --> DIAG[Diagnostics, no state advance]
 PURE[Pure state helpers: not called by main] -.-> TABLE[Limited topology, not full event FSM]
```

Машиночитаемый полный 33×33 topology inventory: `Tests/Contracts/HSBI_FULL_SYSTEM_AUDIT_02_FSM_MATRIX.json`. Это **не** полная нормативная event-level таблица. В ней явно отсутствуют implemented handlers. Нормативная часть описывает фазы мануала; полный перечень event/preconditions/actions/retry/out-of-order/restart combinations ещё не формализован.

Pure table допускает self-loop, ранний путь до CoreOpening, generic переходы в RECONCILING/TERMINAL_SAFE/EMERGENCY и выходы RECONCILING в FarActive/Idle/TerminalSafe. CoreOpening→TrendOpening отсутствует. Generic разрешение topology не является authority для manual resume. Текущий EA эту таблицу не использует для торговли. Внешние fills и out-of-order события не поступают: OnTradeTransaction отсутствует.

Для каждого нормативного перехода нужны shape/owner/actual-fill/replay/partial/timeout/reject/restart guards, экономический ledger и persistence. Их отсутствие отмечено UNIMPLEMENTED, а не PASS. Диагностический far-count helper достижим по OnTimer, но дефектный fixture с двумя FAR не создаётся текущим main. Из fail-counterexamples нет доказанного пути к реальному исполнению.
