# AUDIT03 COVERAGE-COMPLETION — пять глобальных свойств

База4761c66edc3343f353ca774df835eedb1787b818. Ручная математика и статическое чтение. Никаких вычислительных экспериментов. Обозначения и ID сохраняются в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), [реестре ошибок](HSBI_AUDIT03_ALL_ERRORS_RU.md).

## A — Ограниченность объёма

Различать sup_t Gross(t), объём последовательности Far Fk и общий оборот Σ|executedVolume|. При максимум четырёх уникальных active positions одного symbol и bound Vmax на каждую sup Gross≤4Vmax (F061). При каждом успешном F(k+1)≤qFk и0<q<1 сумма Far величин по успешным шагам≤F0/(1−q) (геометрическая сумма), но это не сумма всех открытий/закрытий между этими шагами. Требуется uniform ratio также для объёмов C/T/S, ограниченное число повторов/failed requests с actual fills и отсутствие скрытых ролей.

Grid/Vmin/Vmax дают ограниченное множество объёмов только при известном origin и фиксированных symbol properties. Max одновременно открытых positions не ограничивает повторный оборот. Необходимое условие bounded cumulative turnover — отсутствие бесконечного числа операций с положительным минимальным actual volume; достаточный пример — ограниченное число таких операций и верхняя граница каждого объёма. Это условие о числах, не доказательство существующего lifecycle. Runtime проверка требует registry всех actual positions/fills, pending exposure и count window. Сейчас Context не проверяет все slots (ERR-012). **Итог: условная локальная bound, глобальная turnover bound UNVERIFIED.**

## B — Верхняя граница денежного убытка

Формулировка: существует конечный B, одинаковый для всех допустимых market/execution paths, такой что cumulative economic loss≤B. Для открытого SELL F>0, фиксированного K>0 и неограниченной adverse цены убыток FK(P−Popen) превышает любой B при достаточно большом P (F059). Ограничение Gross этого не меняет. При BUY и неотрицательной цене одна фиксированная нога имеет иной bound, но это не universal theorem о повторных leveraged циклах, conversion/carry и всех ролях.

Достаточные **условные** предпосылки: bounded price/conversion/charges за bounded holding time, bounded turnover/exposure и гарантированное ликвидационное исполнение с bounded adverse cost. Тогда каждый поток имеет конечную оценку и конечная сумма ограничена. Необходимо исключить все неограниченные contributing factors либо ограничить ответственность отдельным доказанным broker contract. Stop-loss trigger, cap или намерение emergency не дают guaranteed fill bound при gap. Production может отслеживать budget и fail closed, но не обеспечить рынок. **GLOBAL_LOSS_BOUND_PROVEN=NO; безусловная гарантия при указанных свободных путях опровергнута.** ERR-038/042; IMP-021.

## C — Гарантированный прибыльный FinalClose

Формулировка: для всякой admissible траектории существует конечное время actual полного закрытия с положительным full economic cycle PnL. Уже flat quotes без favorable trigger и с положительными costs дают контрпример отсутствию положительного выхода из equal lock. Если strategy допускает ждать бесконечно — нарушается конечность; если закрывается в убыток — нарушается прибыльность. При неблагоприятном gap положительный preview не guaranteed execution PnL.

Для условной гарантии пришлось бы задать достижение прибыльного состояния, достаточную маржу до него, bounded costs и guaranteed fills/complete accounting. Эти предпосылки содержат существенное рыночное утверждение; их нельзя доказать unit-тестом планировщика. Runtime может требовать текущий PL threshold, но это только необходимый pre-dispatch фильтр. **PROFITABILITY_GUARANTEED=NO.** ERR-036/042/044; F010/F011/F035/F050/F059.

## D — Конечность полного цикла

Uniform contraction доказывает Fk≤q^kF0 и достижение заданной малой шкалы за ограниченное число **успешных** reductions, если каждый существует (F037/F058). Не доказывает время до action, существование следующего кандидата, partial completion или ликвидацию минимального положительного остатка. При F=Vmin на одной сетке нет N с0<N<F. Утверждение конечного префикса о бесконечном tail неверно (F038).

Достаточная условная operational схема потребовала бы хорошо основанную дискретную меру, её строгое уменьшение на каждом полном шаге, конечное время каждого шага, отсутствие бесконечных retry/wait без уменьшения и исполнимый terminal close. Полное отсутствие следующего safe candidate должно вести в явно определённую остановку/manual policy, а не завершение со всё ещё открытым риском. Нет такого полного доказательства для текущей системы. **CYCLE_TERMINATION_PROVEN=NO**, конечность successful abstract reductions — условно верна. ERR-021/031/032; IMP-013.

## E — Отсутствие двойного использования ресурса

Формулировка по каждому logical source s: Σ grants(s)≤eligible settled net(s); по каждому grant g: OriginalGrant=Consumed+Reserved+Free, компоненты≥0; каждое событие с тем же immutable payload имеет delta0, изменённое — conflict. Между reservations должны сохраняться owner/bucket rights. Это сумма settled money одной currency/precision, не forecast.

При serializable atomic transitions, complete independent source journal и immutable replay можно индукцией сохранить эти инварианты (F013–019/F053–057/F065). База — подтверждённый нераспределённый источник; шаг — одна допустимая операция, сохраняющая partition. Без единого source registry два allocation50 на source50 локально выглядят корректно. Без atomic commit два stale authorizations30 на Free50 не доказывают допустимость60. Snapshot checksum не broker authenticity, receipt reconstruction не новая authorization.

Нужны независимая broker history, EA-origin mapping, durable ledger, crash recovery и конкурентное ordering evidence. Они не заменяются скопированной expected identity. Current source содержит неполные equality/namespace/consumption paths (ERR-001–008/017/030/033/048). **GLOBAL_MONEY_CONSERVATION_PROVEN=NO.** Условная индукция верна; production/global/broker scope не доказан.

## Разделение вывода

A не влечёт B/C/D. E не влечёт прибыльность: можно идеально учитывать каждый понесённый убыток. Обнаружение математического countermodel не означает воспроизведённый broker incident. Нативное и брокерское исполнение этим заданием запрещено, поэтому native status NOT_RUN, а не FAIL или PASS. Все решения администратора остаются неутверждёнными.

## FINAL-CLOSURE — пять индивидуальных карточек по10 полей

Новая база b4d8f1ea5caf492f3abd030e5502d40582c52dc8. Это ручные доказательства/контрмодели; код/тесты не исполнялись. Предыдущие абзацы сохранены.

### A — volume

| Поле | Индивидуальный вывод |
|---|---|
| Точная формулировка | Отдельно sup_t Gross(t)≤B и cumulative turnover Σ abs(actual fill volume)≤T; ни одно не подменяет другое. |
| Необходимые предположения | Для bound открытого Gross нужен bound числа уникальных actual позиций и их объёма; для turnover исключить бесконечные положительные fills. |
| Достаточные предположения | Не более4 уникальных активных позиций, объём каждой≤Vmax дают B=4Vmax; не болееK executed fills, каждый≤Vmax дают T=K·Vmax. |
| Доказательство / контрпример | Σabs(volume)≤4Vmax при4 позициях по слагаемым; бесконечное повторение open/close Vmin имеет bounded instantaneous Gross, но unbounded turnover. |
| BUY / SELL | Знак направления не меняет absolute lots; зеркальные цены не нужны для этой алгебры. |
| Broker grid / partial fills | Grid ограничивает допустимый отдельный volume, но не число повторов. Partial quantities входят в executed turnover по одному разу. |
| Production проверяемость | Registry всех slots/pending fills нужен для actual bound; Context сейчас не охватывает все slots. |
| Рынок / брокер / внешняя authority | Broker Vmax/grid и полнота position history независимы; локальные DTO не подтверждают их. |
| Связи с формулами / ERR / IMP / решениями | F030/F037/F058/F061; ERR012/021/032; IMP007/013/021; MQL-DOMAIN. |
| Статус / proof boundary | VALID_UNDER_ASSUMPTIONS для указанного bound; global turnover UNVERIFIED, не full lifecycle proof. |

### B — loss

| Поле | Индивидуальный вывод |
|---|---|
| Точная формулировка | Существует единый конечный B для cumulative economic loss по всем admissible market/execution paths. |
| Необходимые предположения | Каждый contributing factor должен быть ограничен либо его вклад компенсирован доказанным hedge/liability contract; bounded volume недостаточен. |
| Достаточные предположения | Bounded prices/conversion/costs/holding-time плюс bounded exposure/turnover и guaranteed bounded-cost exit дают конечную сумму потоков. |
| Доказательство / контрпример | Открытый SELL F>0 с линейным K>0: loss=FK(P−Popen), при P→∞ конечного универсального B нет. |
| BUY / SELL | Одна BUY при цене≥0 имеет другой ценовой bound, но повторные циклы/fees/conversion не ограничены этим односторонним примером. |
| Broker grid / partial fills | Grid/Vmax не ограничивают adverse price; gap/partial fills могут оставить открытый риск. |
| Production проверяемость | Local cap способен блокировать новый action; не гарантирует fill/market response при уже открытом Far. |
| Рынок / брокер / внешняя authority | Нужны explicit market bounds/liquidity/guaranteed exit или broker liability; stopout/stop trigger недостаточен. |
| Связи с формулами / ERR / IMP / решениями | F030/F059/F061; ERR018/019/038/042; IMP021; risk/emergency policies pending. |
| Статус / proof boundary | Безусловная гарантия FALSE в указанном свободном domain; GLOBAL_LOSS_BOUND_PROVEN=NO. |

### C — profitable exit

| Поле | Индивидуальный вывод |
|---|---|
| Точная формулировка | На всякой допустимой траектории за конечное время actual full close имеет positive full-cycle PnL. |
| Необходимые предположения | Нужно достижение прибыльного состояния, достаточная margin до него и исполнимое полное закрытие после всех costs. |
| Достаточные предположения | Достижение threshold с запасом на bounded adverse execution при guaranteed fills и complete cycle accounting было бы достаточным условным профилем. |
| Доказательство / контрпример | Flat quotes equal lock с положительными costs: ожидание не даёт обязательного positive exit; закрытие фиксирует cost. Это countermodel universal claim. |
| BUY / SELL | Одинаковый вывод для зеркального equal BUY/SELL lock; universal P+tick без direction не основание доказательства. |
| Broker grid / partial fills | Min/step допускают residual; partial close не full close. Preview threshold может исчезнуть между fills. |
| Production проверяемость | Текущий threshold calculator может дать необходимый local eligibility filter, не гарантировать outcome. |
| Рынок / брокер / внешняя authority | Достижение favorable state и guaranteed liquidity — внешние предпосылки, не следствие unit arithmetic. |
| Связи с формулами / ERR / IMP / решениями | F010/F011/F035/F038/F039/F050/F059; ERR036/042/044/046; IMP010/020/021; D02/D06. |
| Статус / proof boundary | PROFITABILITY_GUARANTEED=NO; universal guarantee опровергнута допустимым countermodel. |

### D — cycle termination

| Поле | Индивидуальный вывод |
|---|---|
| Точная формулировка | Для любого допустимого исполнения существует конечный момент CYCLE_CLOSED без открытого экономического остатка. |
| Необходимые предположения | Все нужные transitions должны существовать и завершаться за конечное время; terminal route исполним, не один finite proof prefix. |
| Достаточные предположения | Well-founded discrete measure строго падает на каждом completed step; каждый step конечен; bounded retries; terminal liquidation доказана. |
| Доказательство / контрпример | F_k≤q^k F0 достигает Vmin, но не нуля. При F=Vmin нет допустимого 0<N<F на той же grid. Поэтому contraction не full close theorem. |
| BUY / SELL | Объёмная рекурсия mirror-invariant, исполнимость/costs BUY/SELL отдельно зависят от quotes. |
| Broker grid / partial fills | Округление может дать plateau; partial/rejected fills не completed reduction. Уменьшение требуется после actual recheck. |
| Production проверяемость | terminalRouteAllowed не прочитан solver; terminal=true по достижению Vmin не проверяет route. Pure planner не обязан сам торговать. |
| Рынок / брокер / внешняя authority | Нет гарантии favorable price/finite wait/доступности безопасного следующего кандидата без внешних предпосылок. |
| Связи с формулами / ERR / IMP / решениями | F037/F038/F058; ERR021/031/032/041; IMP013/019/022; terminal policy pending. |
| Статус / proof boundary | CYCLE_TERMINATION_PROVEN=NO; bounded number successful ideal reductions условно доказан. |

### E — resource uniqueness

| Поле | Индивидуальный вывод |
|---|---|
| Точная формулировка | По source Σgrants≤eligible settled net; по grant G=C+R+F, C/R/F≥0; exact event replay delta0, altered replay conflict; owner/bucket rights. |
| Необходимые предположения | Полный source namespace и immutable equality, complete independent receipts, serializable transitions; локальной арифметики недостаточно. |
| Достаточные предположения | Изначально подтверждённый source, один атомарный переход на событие, complete durable journal и checked affordability сохраняют partition индукцией. |
| Доказательство / контрпример | Без общего registry два allocation50 на source50 проходят local bounds; два stale authorization30 на Free50 не легализуют60. |
| BUY / SELL | Money identity требует одной currency/precision, направления сохраняются в signed components; BUY/SELL не меняет partition. |
| Broker grid / partial fills | Накопление actual partial fills по source/deal/event ровно один раз; forecast/reserve labels не дополнительные деньги. |
| Production проверяемость | Current equality/namespace/available/amount-binding guards неполны; добавление local helper не global backend. |
| Рынок / брокер / внешняя authority | Broker history + EA-origin mapping + durable receipts + concurrent commit evidence обязательны для global/broker claim. |
| Связи с формулами / ERR / IMP / решениями | F007/F013–019/F034/F036/F053–057/F064/F065; ERR001–008/017/030/033/048; IMP001–005/009/014; D01/D02/D07/D08. |
| Статус / proof boundary | Условная abstract induction VALID_UNDER_ASSUMPTIONS; GLOBAL_MONEY_CONSERVATION_PROVEN=NO. |
