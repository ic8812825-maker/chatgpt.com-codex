# ALE + ALC Stability Verification & Lock Algorithm Specification

## 1) Objective

Ревизия вводит детальный алгоритм **Greedy Delta Matching + Geometry Rebuild** и интегрирует ALC в pipeline без разрушения ALE логики.

## 2) Pipeline Integration

Новый pipeline:

`geometry -> positions -> ALC compression -> exposure -> risk -> optimization -> FSM`

ALC расположен между `positions` и `exposure`.

## 3) Effective Delta


\[
\Delta = \sum_i sign_i \cdot lot_i,\quad sign_i=\begin{cases}+1, & BUY\\-1,& SELL\end{cases}
\]

В коде effective delta вычисляется через `CALPositionBook::EffectiveDelta()` и используется в compression/risk.

## 4) Greedy Delta Matching (Formal Pseudocode)

```text
Input:
  BUY[]  - lots of buy positions
  SELL[] - lots of sell positions

1) Sort BUY descending by lot
2) Sort SELL descending by lot
3) i = 0, j = 0
4) while i < len(BUY) and j < len(SELL):
      L = min(BUY[i].lot, SELL[j].lot)
      create lock_pair(BUY[i], SELL[j], L)
      BUY[i].lot  -= L
      SELL[j].lot -= L
      if BUY[i].lot  == 0: i++
      if SELL[j].lot == 0: j++
5) Δ_before = sum(BUY_in) - sum(SELL_in)
6) Δ_after  = sum(BUY_residual) - sum(SELL_residual)

Invariant:
  |Δ_after| <= |Δ_before|
```

## 5) Compression Trigger

ALC trigger:

- `n > 8`
- `margin_level < 200%`, где
  \[
  margin\_level = \frac{Equity}{Margin}\cdot 100
  \]
- `n >= max_levels`
- SAFE rescue path

## 6) Geometry Rebuild

Чтобы не разрушать ALE геометрию после компрессии, выполняется rebuild:

\[
L_i = L_0 \cdot k^i
\]

где `L0` вычисляется из сохранения суммарного объёма:

\[
\sum_{i=0}^{n-1}L_i = V_{total}
\]

если `k!=1`:

\[
L_0 = \frac{V_{total}}{\frac{k^n-1}{k-1}}
\]

если `k=1`:

\[
L_0 = V_{total}/n
\]

Геометрический инвариант:

\[
|L_i - L_0 k^i| < \varepsilon
\]

## 7) Compression Policy

- `alpha = 0.5`
- `effective_exposure_new = effective_exposure_old * alpha`
- `margin_new = margin_old * alpha`

PnL externally не фиксируется forced-close логикой; структура ребалансируется и затем пересчитывается на новой геометрии.

## 8) Stability & Risk Formulas

Без ALC:

\[
Risk \sim k^n
\]

С ALC:

\[
Risk \sim \alpha^m k^n
\]

Условие depth/margin устойчивости:

\[
Margin(n) = \sum_i \frac{lot_i\cdot contract\_size}{leverage}
\]

\[
DD = \sum_i lot_i \cdot price\_distance_i
\]

margin collapse:

\[
Equity < Margin + DD
\]

оценка collapse probability:

\[
P_{collapse} \approx 1/n_{max}
\]

## 9) Safe Deposit

Сценарная оценка:

\[
Deposit_{safe}(trend)=Margin_{req}+DD_{trend}+buffer
\]

buffer задаётся консервативным коэффициентом в тестовом анализе.

## 10) New Verification Suite

Добавлены unit targets:

- `TestLockCompression`
- `TestDeltaCalculation`
- `TestGeometryPreservation`
- `TestCompressionTrigger`
- `TestCompressionMargin`
- `TestALCStability`
- `TestSafeDeposit`

Каждый тест пишет отчёт в `tests/reports/*_report.md`.

## 11) Final Report

Генерируется `ALE_ALC_STABILITY_REPORT.md` с:

- `n_max`
- `P_collapse`
- таблицей `Trend -> Required Deposit`
- итоговым заключением.
