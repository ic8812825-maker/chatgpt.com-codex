# Риск, margin, drawdown и брокерская исполнимость

BASE_SHA=4185b84f7a6a8847f6a9c5796f07113907be447d

Режим READ-ONLY ANALYSIS + AUDIT/TEST-ONLY. Источники не изменены. **AUDIT_COMPLETENESS=PARTIAL.** Native MQL5/MT5/broker/durable execution NOT_RUN. Proposed R0A–R0H не становятся нормативом из-за тестовых PASS. Все административные разрешения остаются NO.

## Что есть в коде

RiskInput/limits получают projected margin, margin level, free margin, cycle/account drawdown, gross exposure, managed count, worst-case/transition loss, spread и snapshotFresh. `HSBI_ValidateRiskInput` сравнивает их с limits, но не проверяет finite/domain. NaN projectedMargin проходит. `HSBI_EvaluateNewFarGates` проверяет некоторые next/cap values, но не все baseline/allowed inputs; allowedMargin=NaN проходит. Transaction volume/price NaN также может дать completed в extracted source. Исправления нужны до присоединения любой из этих библиотек к trading entry.

`OrderCalcMargin` wrappers fail UNAVAILABLE при API failure и проверяют finite/nonnegative returned margin. Это правильная локальная защита; фактическая маржа портфеля/hedging/account tier/leverage/free margin/stop-out не следует из суммы standalone margin четырёх ног. Risk runtime proof — externally supplied numeric value+sourceflags, не реализованный независимый adverse-control calculation/provider.

Неизвестная оценка !=0. При missing broker history/unsupported calculation mode/unknown currency/precision нельзя выдавать spendable source или riskPASS. Current actual-provider/CAS/settled-ledger отсутствуют, поэтому общесистемный риск UNVERIFIED даже при flags fresh/runtimeConfirmed.

## Диапазоны и account model

Нормативные проценты0..100, tolerance>=0, finite money и positioncount>0 требуют централизованного валидированного config. Main вообще не имеет input trading parameters/configloader. Нет gate ACCOUNT_MARGIN_MODE: same-symbol independent long/short legs требуют hedging или иной virtual-ledger architecture, не реализованной для netting. Начальный BUY1/SELL1 в netting не оставляет два независимых positions. Broker-specific tickValueProfit/Loss, currency conversion, asymmetric tick values, StopsLevel/FreezeLevel/order modes/SLTP constraints необходимо определить до execution. Сейчас dispatch отсутствует: эти пути не тестировались, нельзя объявить их корректными или все одинаково applicable.

## Нереальные гарантии

Stop-loss/emergency budget/Transition cap на projected values не гарантируют исполнение в пределах cap после gap/timeout/slippage. В fixture planned liquidation+2.56 переходит в−15.94 при adverse5 на всех fills. Source imperative emergency liquidation отсутствует: enum/terminal-safe metadata не закрывают позиции. Пользоваться этим skeleton как защитным EA для уже открытого счёта нельзя — он не читает/не ведёт/не ликвидирует позиции.

Нет математического risk bound без ограничений рыночного пути, исполнения, кредитного плеча, broker forced-liquidation/negativebalance policy и validated capital budget. Нет статистических trading-strategy доказательств. Partial prefix −15 при cap12 уже breach, даже если позже+100; A/B/C/reset/sticky semantics ждут администратора. Margin call/stop-out response и partial-fill actual loss reconciliation остаются UNIMPLEMENTED/NOT_RUN.

Сценарий LOW_MARGIN и более неблагоприятные quote paths проверяют accounting arithmetic, не broker margin/order acceptance. Все bridge/proxy flags — тестовые допущения. Safety current verified static: runtime disabled, brokerDispatch false, no sending paths; functional trading safety НЕ доказана.
