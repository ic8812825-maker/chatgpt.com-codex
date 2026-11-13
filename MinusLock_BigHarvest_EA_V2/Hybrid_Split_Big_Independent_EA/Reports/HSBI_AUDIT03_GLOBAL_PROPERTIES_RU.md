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
