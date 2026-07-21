# Hybrid Split Big — доказательный screening-отчёт

## Метод и границы применимости

Проведён детерминированный поиск 100 000 кандидатов двумя независимыми
методами: Latin Hypercube и uniform random (seed `20260720`). Модель проверяет
после брокерского округления положительную Big-экспозицию и монотонный наклон
RecoveryPL, Reserve catch-up, целевой NewFar, новый Big, margin и удвоенные
расходы. Проверено пять классов: `core_target`, `core_budget`,
`trend_funded`, `two_stage`, `dynamic`.

Из 100 000 кандидатов прошли жёсткие Gate 934; 99 066 сохранены оптимизатором
как отклонённые с причиной. Лучшие Pareto-кандидаты дали NewFar 0.20--0.28
OldFar, NewBig gross 0.61--0.84 OldFar, catch-up 2.64--3.00 и расчётную
верхнюю границу 4--5 reverse переходов для Far=1.00, шаг=0.01.

## Формальная область

Для округлённых лотов `C,T,S,F` требуются одновременно:

`C + T - S - F >= MinimumNetBigExposureLots`;
`ReserveShare * (C + T - S) / F >= MinimumReserveCatchUpRatio`;
`0 < TargetNewFar <= C < F*BigCoreRatio`;
`(C+T-S-F)/F * TargetNewFar < F`;
`(C+T+S)/F * TargetNewFar < MaximumNewBigToOldFarRatio*F`;
`TransitionNet >= 0`; `MarginPercent <= MaxMarginPercent`.

При reverse закрывается только избыточная выигрышная часть BigCore; BigTrend
никогда не становится Far. `TransitionBudget` и `ReserveCredit` разные
денежные корзины: Budget не кредитуется в Reserve, что исключает двойной учёт.

## Важное ограничение

Это независимый математический screening, а не доказательство исполнения у
брокера. Финальная активация `UseHybridGeometrySolver=true` запрещена до
успешной компиляции MetaEditor и Strategy Tester Every Tick/real ticks.
