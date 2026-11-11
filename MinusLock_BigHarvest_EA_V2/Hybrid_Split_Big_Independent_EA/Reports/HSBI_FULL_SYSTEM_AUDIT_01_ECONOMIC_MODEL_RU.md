# Экономическая состоятельность и источники результата

BASE_SHA=4185b84f7a6a8847f6a9c5796f07113907be447d

Режим READ-ONLY ANALYSIS + AUDIT/TEST-ONLY. Источники не изменены. **AUDIT_COMPLETENESS=PARTIAL.** Native MQL5/MT5/broker/durable execution NOT_RUN. Proposed R0A–R0H не становятся нормативом из-за тестовых PASS. Все административные разрешения остаются NO.

## Исходные допущения аналитического примера

Синтетический hedging unit-value symbol (1money на1price×1lot), tick1, unit leverage100 только для иллюстрации margin, quoted Bid/Ask, opening и closing commission0.1/lot; swap/fee0. Starting capital1000. FarSELL1@100, CoreBUY1.2@101, TrendBUY1@101, SmallSELL.5@100; opening commissions.37 =>Balance999.63. При Bid100/Ask101 floating−3.7, Equity995.93. Это не реальные broker values и не калиброванный forex backtest. Native trading отсутствует; команды fills заданы тестом, не вырабатываются EA.

Сценарии содержат initial positions/balance/equity, quotes/path, requested analytical fills, each status, final volumes/net/gross, realized/unrealized, liquidation PnL и remaining obligations в REFERENCE.json. `Meaning` — интерпретация fixture, не копируемое expected decision кода HSBI. Например BROKER_REJECT означает заданное отсутствие fills, не выполненный retcode engine. Partial scenario — arithmetic fill.4 и остаток.6, не доказанный MQL fill accumulator. Все20 accounting vectors совпали с независимыми literal balances/equities.

| Scenario | Expected/actual balance | Equity | Gross / Net | Meaning |
|---|---|---|---|---|
| SCENARIO-UP | 999.63 | 1002.93 | 3.7 / 0.7 | NO_AUTOMATIC_EA_ACTION |
| SCENARIO-DOWN | 999.63 | 988.93 | 3.7 / 0.7 | NO_AUTOMATIC_EA_ACTION |
| SCENARIO-RANGE | 999.63 | 995.93 | 3.7 / 0.7 | NO_TERMINATION_PROOF |
| SCENARIO-WHIPSAW | 999.63 | 995.93 | 3.7 / 0.7 | NO_TERMINATION_PROOF |
| SCENARIO-GAP_UP | 999.63 | 1023.93 | 3.7 / 0.7 | GAP_RISK_NOT_BOUNDED |
| SCENARIO-GAP_DOWN | 999.63 | 967.93 | 3.7 / 0.7 | GAP_RISK_NOT_BOUNDED |
| SCENARIO-SPREAD_WIDENS | 999.63 | 982.43 | 3.7 / 0.7 | REVALIDATE_REQUIRED |
| SCENARIO-SLIPPAGE | 984.06 | 984.06 | 0 / 0 | PLANNED_PROFIT_NOT_GUARANTEED |
| SCENARIO-LOW_MARGIN | 4.63 | 0.93 | 3.7 / 0.7 | INSUFFICIENT_MARGIN |
| SCENARIO-PARTIAL_FILL | 995.19 | 1002.89 | 3.3 / 1.1 | PENDING_REMAINING_FAR_0.6 |
| SCENARIO-BROKER_REJECT | 999.63 | 1002.93 | 3.7 / 0.7 | REJECT_NO_FILL |
| SCENARIO-DUPLICATE_EVENT | 995.19 | 1002.89 | 3.3 / 1.1 | NO_OP_SECOND_EVENT |
| SCENARIO-RESTART | 995.19 | 1002.89 | 3.3 / 1.1 | UNAVAILABLE_NEW_ACTION_WITHOUT_HISTORY |
| SCENARIO-HISTORY_MISSING | 999.63 | 1002.93 | 3.7 / 0.7 | UNAVAILABLE |
| SCENARIO-ECONOMIC_CONFLICT | 995.19 | 1002.89 | 3.3 / 1.1 | CONFLICT_SECOND_EVENT |
| SCENARIO-BIG_PROFIT_SMALL_LOSS | 1003.46 | 998.46 | 1 / -1 | HARVEST_POSITIVE_CYCLE_NEGATIVE |
| SCENARIO-SMALL_PROFIT_BIG_LOSS | 1004.08 | 988.88 | 3.2 / 1.2 | SMALL_PROFIT_NOT_BIG_FUNDING |
| SCENARIO-INSUFFICIENT_CATCHUP | 999.63 | 1002.93 | 3.7 / 0.7 | MARGIN_MINUS_9_REJECT |
| SCENARIO-FULL_CLOSE | 1002.56 | 1002.56 | 0 / 0 | ZERO_POSITIONS_FIXTURE_ONLY |
| SCENARIO-NO_SAFE_EXIT | 999.63 | 967.93 | 3.7 / 0.7 | FINAL_CLOSE_PROFIT_GATE_REJECT |

## Положительный Harvest при отрицательном цикле возможен

Bid104/Ask105. Core profit3.6 и Trend3, closing commission.22 =>BigNet6.38. Small close loss2.5 +commission.05 =>−2.55. После закрытия ВСЕХ C/T/S, как требует role contract, HarvestNet=3.83>0. Balance=999.63+3.83=1003.46. Remaining Far SELL1 has floating−5 =>Equity998.46. Ещё.10 закрытия Far =>full liquidation cycle PnL−1.64. Положительный realized Harvest и выросший balance не означают выросшую equity или прибыль полного цикла. Это не доказывает, что полный HSBI gate обязан разрешить такой Harvest/FinalClose; оно доказывает недопустимость использовать Harvest-only statistic как доказательство прибыльности. Корректный FinalClose threshold/coverage должен здесь отклонить recovery close.

При Bid90/Ask91 Small close приносит4.45, баланс1004.08, но оставшиеся Big losses дают equity988.88. Small-only income не становится автоматически BigReserve. В реальном source `reserveGainMoney=max(0,CoreNet+TrendNet+SmallNet)` — projected field: при Core−1/Trend−1/Small10 он равен8. Это НЕ доказанный actual grant; текущий отдельный ReserveSourceProof дополнительно требует Core/Trend role. Нужно устранить неоднозначность projected/actual/allocated/available и утверждать attribution, не объявлять любой projected field прямым funding.

## Перенос остаточного риска и отсутствие гарантии bounded loss

После Harvest остаётся ненулевая Far liability. Для оставшейся SELL-volume Q при росте price P прибыль остатка = Q*(open−Ask), то есть при P→∞ без исполнения нового хеджа/ликвидации loss не ограничен этой моделью. Initial fixed lots + bounded price interval дают лишь условный bound; ни допустимый диапазон рыночных gaps, ни guaranteed fills/negative-balance protection/stop-out price тут не доказаны. Реальный брокер может принудительно закрыть позиции раньше, но такой loss/price outcome не моделирован. Отсутствие гарантий не означает доказанную неизбежную убыточность на каждой траектории; означает LOSS_BOUND_NOT_PROVEN.

При favorable trend в fixture полное закрытие на110/111 даёт+2.56. Adverse slippage5 на каждой leg превращает тот же расчёт в−15.94 полного цикла (Balance984.06). При flat path trigger/exit может не прийти, а отрицательный carry при его наличии накапливается. Возможность нескольких последовательных recovery cycles не доказывает, что общая задолженность уменьшается после costs, капитал достаточен и cycle завершится.

Positive slope, compression, локальные rebates/закрытые profits не создают expected economic edge. Нет independent market dataset, sample protocol, out-of-sample/backtest, slippage model validation, реального inventory accounting или native lifecycle. Полный account PnL должен учитывать также excluded InitialProfit/opening costs/прочие account debits; recovery metric, который намеренно исключает InitialProfit, не полный strategy/account return.

Ответы на главные вопросы: positive Harvest с negative CyclePnL — да; positive Small/Big может скрывать loss других legs при partial metrics — да; Far liability может расти после закрытия прибыльных ног — условно да; риск бесконечного ожидания/капитальной недостаточности не исключён; положительный full-cycle return после всех costs и ограниченный убыток НЕ ДОКАЗАНЫ. `PROFITABILITY_NOT_PROVEN`, `LOSS_BOUND_NOT_PROVEN`. No empirical profitability estimate is fabricated.
