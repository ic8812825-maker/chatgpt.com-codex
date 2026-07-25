# План самостоятельных Strategy Tester прогонов Hybrid Split Big

**Исполнитель:** Администратор. **Программист:** не заявляет прохождение этих прогонов. Запуск разрешён только после этапа 8, MetaEditor 0/0 и статуса `READY_FOR_ADMIN_STRATEGY_TESTER`.

## Общий профиль

Hedging account; `Every tick based on real ticks`; фиксированный Symbol/Magic/CycleID; депозит и символ выбираются так, чтобы `OrderCalcMargin` оставлял диагностический запас (рекомендуемый старт $10,000, ликвидный FX symbol, M15, не менее трёх месяцев). Hybrid `.10/.90/.00`, q policy `.50`, Small UP. Сохранить `.set`, HTML report, Journal и Experts log. Во всех тестах искать `HYBRID_DECISION|`, `FinalCode=`, `RejectCode=`, `ErrorCode=`, CycleID и fingerprint.

| ID | Параметры / рыночная модель | Ожидаемые состояния и коды | PASS | FAIL |
|---|---|---|---|---|
| ST-01 постоянный Big | базовый spread/commission; последовательные Big triggers | pre-open → harvest levels → Final preview/actual | конечный profitable close; monotonic recovery trace | Small transition, ledger mismatch, незакрытые positions |
| ST-02 постоянный Small | Small trigger повторяется; depth/max nodes включены | Small transition → compressed cycles → min-lot/final | Far строго уменьшается; Reserve не debit | q>=1, Reserve transition debit, loop без terminal |
| ST-03 Big/Small alternating | чередовать triggers | harvest/transition попеременно | каждый plan fingerprint reconciled | gate bypass или stale plan |
| ST-04 Far BUY | инициировать BUY Far | Big SELL, Small BUY; BUY close uses Bid | ожидаемая BUY/SELL геометрия | direction/price-side mismatch |
| ST-05 Far SELL | зеркало ST-04 | Big BUY, Small SELL; SELL close uses Ask | денежная симметрия в tolerance | асимметрия сверх costs |
| ST-06 spread expansion | ступени normal→2x→3x spread | Worst gate re-evaluated | reject/terminal до unsafe open | action после Worst fail |
| ST-07 slippage | заданные deviation/slippage events | projected vs actual reconciliation | mismatch logged, no continuation | silently accepted fill |
| ST-08 commission | non-zero both-side commission | finite level/risk include commission once | no double count | level matches zero-cost baseline |
| ST-09 swap | multi-day horizon | Worst Risk/Final include confirmed swap | swap trace and conservative result | swap ignored/doubled |
| ST-10 order reject | reject Core/Trend/Small individually | pending open → reconcile/terminal | basket never activated partially | partial basket treated active |
| ST-11 partial fill | force partial volume | pending deal mismatch | no promotion/continuation | requested lot used as actual |
| ST-12 restart | restart at every pending stage | recovery → reconciliation | no new order before match | duplicate event/credit |
| ST-13 min lot | Far near VolumeMin | terminal min lot | no new Far, close-only policy | below-min order |
| ST-14 no valid NewFar | tighten risk/margin/transition limits | `REJECT_NO_VALID_NEW_FAR`/terminal | all candidate rejects traced | fixed q selected anyway |
| ST-15 terminal safe | inject unreconciled state | Terminal Safe/Manual Hold | only proven risk-reducing closes | new position/reserve transfer |
| ST-16 Final actual mismatch | projected pass; adverse actual deals | preview pass → actual mismatch | `ERROR_FINAL_RESULT_MISMATCH`, no success reset | `CYCLE_CLOSED_PROFIT` despite threshold/positions |

## Параметры каждого прогона

В карточке результата обязательно записать: build/EX5 SHA, `.set` SHA, initial deposit, symbol, timeframe, from/to, tick model, spread mode, commission/swap assumptions, expected and actual state sequence, decision codes, final balance/equity, relevant Journal excerpts. PASS/FAIL определяется таблицей, а не положительной прибылью самой по себе.

## Артефакты

Для каждого `ST-nn`: `ST-nn.set`, tester HTML, Journal, Experts log, screenshot equity/state, SHA сборки. Неполные артефакты дают `NOT_EXECUTED/INCONCLUSIVE`, не PASS.
