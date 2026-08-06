# HSBI-DEC-004 — Future Small depth

Статус: `RESOLVED`.

Используется exact recursive preview до первого из условий: terminal lot, ConfiguredMaxFutureDepth либо доказанный analytical bound. Depth 1 не является доказательством конечности.

Состояние рекурсии содержит F, broker-rounded C/T/S/N, reserve, allocation balances, realized money, margin, risk, transition loss, state revision и visited fingerprint. На каждом уровне выполняются три закона, NewFar solver, transition limit и margin/risk gates. Cycle/fingerprint repetition, отсутствие допустимого N, рост F/risk/gross или исчерпание computational budget без conservative bound дают REJECT.

После exact части разрешён только conservative bound `F(k+j)<=q^j F(k)`, `0<q<1`, подтверждённый после rounding и с верхними оценками costs/losses. Owner: `Planning/FutureSmall`. Tests: terminal stop, cycle detection, coarse step, depth exhaustion, BUY/SELL symmetry.
