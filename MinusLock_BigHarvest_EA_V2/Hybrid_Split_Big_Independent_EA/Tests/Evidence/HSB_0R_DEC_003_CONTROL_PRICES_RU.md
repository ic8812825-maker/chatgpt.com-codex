# HSBI-DEC-003 — control prices и proof range

Статус: `RESOLVED`.

Утверждены типы: CurrentClosePrice, NextBigControlPrice, SmallTransitionControlPrice, AdverseRiskControlPrice, GapStressPrice, FinalClosePrice. Для BUY-close используется Bid, для SELL-close Ask. Каждый snapshot хранит Symbol, Bid, Ask, tick size, digits, timestamp и максимальный возраст.

RecoveryPL monotonicity проверяется на broker tick grid от текущей close-side цены до NextBigControlPrice включительно; пропуск точек запрещён, кроме доказанного piecewise-linear сегмента с обязательной проверкой границ, spread discontinuities и cashflow events. Reserve Catch-Up использует тот же Big control range; risk/margin используют adverse и gap prices; Final Close только свежую текущую close-side цену.

Reject: stale snapshot, invalid spread, ненормализованная цена, отсутствующий tick value/OrderCalcProfit result. Owner: `Planning/ControlPriceModel`, `Money/BrokerMoneyModel`. Tests: BUY/SELL side, freshness, tick normalization, endpoint inclusion.
