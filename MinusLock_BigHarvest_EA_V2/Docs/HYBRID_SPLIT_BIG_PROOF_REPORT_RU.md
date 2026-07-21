# Повторный инженерно-математический отчёт Hybrid Split Big

## 1. Репозиторий и область

Репозиторий: `ic8812825-maker/chatgpt.com-codex`; ветка: `work`; путь:
`MinusLock_BigHarvest_EA_V2`. Исходный SHA, SHA генерации доказательств и
итоговые метаданные записываются автоматическим runner в
`Reports/HYBRID_FINAL_LAW_STATUS.csv`. Исследование ограничено анализом
исходного кода, математическими условиями и Python-проверками.

## 2. Формулы и соответствие

MQL5 `HybridGeometrySolver.mqh` рассчитывает округлённые BigCore, BigTrend,
SmallBase, TargetNewFar, projected Reserve Catch-Up и
`ValidateHybridRecoveryMonotonicity`. `HybridTransitionPlanner.mqh` строит
план до закрытия OldFar и выбирает минимальный broker-safe остаток. Python
`hybrid_geometry_model.py` повторяет: `C=cF`, `T=tF`, `S=sF`,
`NetRecoveryExposure=C+T-S-F`, `BigGross=C+T`, Catch-Up
`ReserveShare*(C+T-S)/F`, а `NextBigGross` исключает SmallBase. Модель не
импортирует EA и используется как независимый вычислительный экран.

## 3. Закон №1

Projected slope проверяется на каждом point, а `hybrid_big_sequence_model.py`
передаёт фактические Far, Reserve и PartialFarCarry по L1–L7. Пока
`CoverageDeficit` положителен, требуется строгое уменьшение; при нулевом
дефиците допускается его сохранение. Отчёты содержат отдельные операции
Reserve и Partial Far, поэтому одна сумма не кредитуется дважды. Статусы
`LAW_1_PROJECTED_SLOPE`, `LAW_1_POINT_MODEL`, `LAW_1_BIG_SEQUENCE`,
`LAW_1_COVERAGE_DEFICIT` и `LAW_1_MONEY_CONSERVATION` вычисляет runner, а не
этот документ.

## 4. Закон №2

`HYBRID_RECOVERY_POINT_SWEEP.csv` содержит 0..700 point для FAR_BUY и
FAR_SELL, значения каждой leg, RecoveryPL, предыдущее значение и дельту.
Runner сам проверяет строковое неравенство, не доверяя полю PointSweep.
Закрытия Big/Partial Far учитываются как дискретные ledger-события, не как
ложная производная непрерывного движения. Cost stress входит в сценарии.

## 5. Закон №3

`hybrid_small_state_machine.py` исполняет реальные переходы плана, удаляет
OldFar, BigTrend и SmallBase из состояния и запрещает неверный порядок.
Финал допускается только как `VALID_SMALLER_NEXT_CYCLE` или
`CYCLE_FULLY_CLOSED`. Следующий риск включает Far, Core, Trend и SmallBase,
worst-case loss и маржу, а не один NewFar.

## 6. Деньги, stress и контрпримеры

Big ledger отдельно хранит net каждой закрытой leg, расходы, Reserve, budget,
фактически использованный Partial Far и carry. Small ledger хранит net
закрытий, TransitionBudget, расходы и подтверждает, что Final Reserve не
использован для transition. Имеется 120 stress строк, расширенная матрица
устойчивости и двадцать целевых контрпримеров, включая независимый
`TRANSITION_LOSS`. В каждом контрпримере сравниваются ExpectedRejectReason и
ActualRejectReason.

## 7. Единые финальные статусы

Единственный авторитет итогового PASS — `run_hybrid_full_proof.py`: он
запускает pytest и py_compile, запускает harness, читает CSV, валидирует
последовательности и создаёт final CSV. Harness не принимает pytest/compile
статусы и не создаёт final status. Поэтому для одного запуска отсутствует
смешение `NOT_PROVED`, `CONDITIONAL_PASS` и `PASS`: итог берётся только из
автоматически созданного CSV. Manual разрешён лишь при полном PASS и проверке
его существования и размера.
