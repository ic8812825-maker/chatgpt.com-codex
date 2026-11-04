# 02B-R0B — денежная точность и posted amounts

База `9b43c38afdb89c6b3b514b654c7fb9a936f9bf2b`, ветка `work`; исходная проверка UTC `2026-11-04T01:56:44Z`. Только новые audit/test-only файлы. Production и исторические evidence неизменны. Все экономические формулировки — PROPOSED; утверждение администратора отсутствует.

## Величины и источники

`ActualDealNetRaw=Profit+Swap+Commission+Fee` сохраняет signed source components. Raw — наблюдённые значения/их representation, а не новый расходуемый ресурс. Broker-posted components уже могли быть округлены брокером до суммирования: их нельзя заменить гипотетическими unrounded estimates. `PostedActualDealNet` должен иметь независимый source/account/currency receipt либо проверенную source-specific posting policy. AccountCurrencyDigits сам по себе не доказывает порядок округления.

`AllocatableActualDealNet=max(0,PostedActualDealNet)` применим только к подтверждённому eligible source; negative/zero source сохраняется в economic result без positive grant. `RoundingAdjustment=posted-raw` — diagnostic, не дополнительный bucket. Не суммировать его как прибыль.

## Варианты для утверждения

| Вариант | Правило | Последствия |
|---|---|---|
| A — рекомендуется | Использовать independently confirmed broker-posted amount либо сумму подтверждённых posted components; binding по account/deal/currency/precision | Не навязывает локальный rounding. Без broker receipt данных недостаточно; external authenticity NOT_RUN |
| B | Versioned local policy (например HALF_EVEN один раз после raw суммы) только после сверки с broker posting на нужном account/mode/source | Нужны policy version, rounding stage, precision и compatibility evidence. При mismatch UNAVAILABLE, а не замена actual числа локальным |
| C | UNAVAILABLE, если ни A, ни проверенного B нет | Никаких расходуемых grants из одного raw/projection/positive DTO |

Текущий R0A helper reconciled_net() по умолчанию берёт USD/2 и HALF_EVEN без posted аргумента. На synthetic raw1.005 он даёт1.00, когда independently specified posted fixture=1.01. Это предел test-only API, не наблюдение конкретного брокера. Новый oracle в A сохраняет1.01, в B с HALF_EVEN и тем же posted даёт UNAVAILABLE. Старый helper не менялся.

## Численные проверки

| Случай | Результат Decimal |
|---|---|
| HALF_EVEN 1.005 / 1.015, digits2 | 1.00 / 1.02 |
| HALF_EVEN -1.005 / -1.015 | -1.00 / -1.02 |
| .335+.335+.335: округлить один раз | 1.00 |
| Округлить каждый .335 до .34 и сложить | 1.02; это другое правило и другая стадия |
| 1.2451: напрямую до2 / сначала до3, затем до2 | 1.25 / 1.24: повторное округление не идемпотентно относительно целевой precision |
| JPY fixture digits0: 1.5 / 2.5 | 2 / 2 |
| KWD fixture digits3: 1.0005 / 1.0015 | 1.000 / 1.002 |
| Source .01, shares .5/.5 | base buckets0, ResidualHeld .01; сумма .01 сохраняется |
| Unknown digits/receipt, currency mismatch, posted1.005 при digits2 | UNAVAILABLE, без молчаливого округления |
| NaN/Infinity | REJECT numeric input, не available money |

Currency labels JPY/KWD/USD в tests — independently specified fixtures, не подтверждение конкретного broker setting. Никакой автоматической currency conversion. Различающиеся currency/precision запроса, source и balance отвергаются. Модель использует Decimal для oracle и отдельные raw64 golden vectors для source identity; raw binary64 не участвует в вычислении posted ресурса.

## Conservation

Для COMMITTED `ΣGrant=N`, Unallocated0. Для PREPARED `ΣGrant+Unallocated=N`, расход запрещён. Для каждого bucket `R+C=G`, `0<=V<=R`, `A=R-V>=0`. Consumed не прибавляется к источнику. При unreserved x<=A: R'=R-x,C'=C+x,V'=V, сумма R'+C'=G. Для собственного reservation с owner receipt: R'=R-x,C'=C+x,V'=V-x; без такого receipt нельзя расходовать чужой lock. Release меняет V, не G/C, и тоже требует exactly-once event. Runtime/persistence этой ветви UNPROVEN.

Source shares округляются вниз в known minor units; весь остаток учтён ResidualHeld. Неизвестная precision блокирует money proof; нельзя выбирать policy, которая даёт удобный PASS. Предложенный source codec raw64 сохраняет наблюдённые bits и не определяет broker posting policy.

Источники: Docs/08, Docs/24, R0A D-01/D-06; tests `PREC-*`, `ALLOC-*`, `BALANCE-*`, `GUARD-currency`, `GUARD-precision-metadata` в новом evidence. Broker evidence по-прежнему NOT_RUN.
