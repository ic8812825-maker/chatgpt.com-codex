# Hybrid Split Big — implementation gaps

Этот список **не изменяет** торговый код. Он отделяет математическую норму от текущей реализации и является backlog для отдельного задания программисту.

| ID | Математическое требование | Текущее состояние кода | Файл/строка | Риск | Требуемое будущее изменение |
|---|---|---|---|---|---|
| GAP-01 | отдельные projected/actual Final Close names | есть `realCyclePL`, но нормативный split не является единым объектом | `StateMachine.mqh` | смешение precheck и факт | ввести явные `ProjectedFinalRecoveryPL`/`ActualFinalRecoveryPL` |
| GAP-02 | α/β/γ allocation + residual | существуют reserve/carry механизмы, но нет нормативного трёхдольного API | `Types.mqh` | неявный источник partial money | add explicit allocation transaction and residual carry |
| GAP-03 | TransitionBudget available/consumed | есть projected/actual net, нет отдельного ledger bucket | `Types.mqh` | скрытое финансирование | separate persisted transition ledger |
| GAP-04 | cumulative transition loss limit | отсутствует dedicated cumulative field/gate | `Types.mqh` | серия допустимых losses | add per/cumulative/percent gates |
| GAP-05 | FutureSmallDepth policy | plan scans current transition; recursive policy absent | `HybridTransitionPlanner.mqh` | future feasibility is partial | configurable depth and explicit result |
| GAP-06 | conservative hedging margin upper bound | individual margin utilities exist; full conservative basket contract not normative | `BrokerMoneyModel.mqh` | margin underestimation | add upper-bound adapter and tester parity |
| GAP-07 | complete terminal safe protocol | multiple terminal/error states, no single normative terminal contract | `StateMachine.mqh` | unsafe recovery actions | persist terminal reason, allowed action filter |
| GAP-08 | optional T/S component policy | current hybrid solver rejects nonpositive T/S | `HybridGeometrySolver.mqh` | conflict if optional profile selected | retain strict mode or add explicit mode gates |
| GAP-09 | actual final mismatch audit | close result tracking exists, but dedicated mismatch code/report required | `MinusLock_BigHarvest_EA.mq5` | optimistic tester approval | add tolerance comparison after all deals |
| GAP-10 | reference-model parity | no MQL5 parity suite against supplied oracle | `Tests/MQL5` | semantic drift | feed shared vectors into tester |

The concrete code locations above must be re-audited by the programmer against the target commit before implementation.

## Stage 2 MQL5 pre-open gaps

| ID | Математическое требование | Текущее состояние кода | Файл/строка | Риск | Требуемое будущее изменение |
| -- | ------------------------- | ---------------------- | ----------- | ---- | --------------------------- |
| MQL5-STAGE2-01 | Подтверждённая MetaEditor компиляция `0/0` | В контейнере MetaEditor отсутствует | `Docs/HYBRID_SPLIT_BIG_METAEDITOR_COMPILE.md` | Нельзя объявить READY | Запустить compile в MT5 окружении |
| MQL5-STAGE2-02 | ADM-MQL5-05 должен быть решён | Текущая конфигурация честно rejected Law 1 | `Docs/HYBRID_SPLIT_BIG_ADMIN_DECISIONS_REQUIRED.md` | Hybrid candidate не будет разрешён | Администратор выбирает A/B/C/D |
| MQL5-STAGE2-03 | Полная рекурсия Future Small | Реализован только depth-1 preview этапа 2 | `Include/HybridFutureSmallSolver.mqh` | Future-depth >1 не доказан | Следующий этап: recursive solver |
| MQL5-STAGE0-04 | ADM-MQL5-05 | Утверждены `.10/.90/.00`; `K_R=1.125` | `Config.mqh`, normative algorithms | математический конфликт закрыт | RESOLVED |
| MQL5-STAGE0-05 | Полный алгоритмический контракт | State/Harvest/Risk/NewFar/Future/Final/Ledger/State Machine описаны нормативно | normative algorithms | реализация этапов 1–8 ещё отсутствует | staged implementation |
