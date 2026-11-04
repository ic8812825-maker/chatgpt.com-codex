# 02B-R0D — PROPOSED численный контракт до реализации модели

База `ec7ae40fe22e1d6e5bed035450750502a1162ab5`. Test-only; D-01–D-08/CR-09/R0C/R0D не утверждены. Никакого production, dispatch или R1.1.

## NUM-EXACT-1: выбор архитектуры

Subject использует Fraction (целые numerator/denominator произвольной точности). Входной finite decimal преобразуется через integer coefficient/exponent либо Decimal.as_integer_ratio, **без Decimal arithmetic**, изменения context, округления или float. Settled money принадлежит сетке currency/digits: amount*10^digits — integer. Expected критических тестов строится другим способом: integer coefficient/scale и literal vectors, без вызова subject.number, Fraction arithmetic или повторного evaluator с другой precision.

Integer minor units оптимальны для posted/grants/consumption, но не должны уничтожать sub-unit projected loss/buffer. Поэтому единое точное рациональное representation + строгий grid gate на settled границах. Decimal с ограниченным context отвергнут как общий механизм: копирование одной precision не фиксирует traps/Emax/Emin и оставляет прямые helper calls незащищёнными.

## NUM-DOMAIN-1

Входные численные величины — int (не bool), finite Decimal, decimal text или finite-decimal Fraction. Значение кратно10^-64 и abs(value)<10^65. Decimal text lexeme: до256 mantissa digits, exponent token до4 символов включая знак, итоговый parsed exponent по модулю<=256 перед проверкой value-domain. Эти lexical limits — часть fixture API. Float, bool, NaN/Infinity, malformed text и неподдерживаемые типы — Malformed. Well-formed number вне профиля — Unsupported. Это PROPOSED bounded fixture domain, не брокерский/account limit.

DTO money принимает Decimal/Fraction/int; текст допускают только арифметические helper API. IDs имеют отдельные signed-long/ulong ranges и не являются money. Digits — известный int0..8 в fixture profile; явный None означает unknown precision и Unsupported/UNAVAILABLE, а bool/неверный тип — Malformed; currency — nonempty opaque string. Currency conversion не реализуется.

Все промежуточные суммы/произведения/деления вычисляются Fraction точно; precision bound для intermediate не нужен. Для двух finite decimal inputs denominator произведения делит10^128; division может быть repeating rational, но integer numerator/denominator остаются точными. Приведение к floor/ceil и HALF_EVEN выполняется integer divmod. Сложение4 raw components и margin subtraction не теряют знак при cancellation.

Returned monetary quantities проверяются на input-domain membership; outside-domain => Unsupported/UNAVAILABLE, а не положительный proof. Успешное spending замкнуто: 0<x<=R-V, R+C=G, 0<=V<=R; R'=R-x>=V>=0, C'=C+x<=G, R'+C'=G. Все settled values кратны одному unit, поэтому R'/C' тоже на grid и <=G<10^65; denominator не выходит за grid. Каждый следующий шаг обязан пройти direct balance и shape validation. Grant conservation/prepared расход проверяются отдельно.

## Контракты публичных функций

| API / ContractID | Назначение, входы/единицы | Rounding | Outcome/граница и композиция |
|---|---|---|---|
| number / NUM-PARSE | Exact finite decimal scalar в NUM-DOMAIN-1, raw/money/lot/ratio смысл задаёт caller | Нет | Fraction; Malformed/Unsupported явно; не доказывает source |
| candidate_round / NUM-ROUND | Decimal raw + known digits; только candidate local policy | Integer HALF_EVEN один раз на выбранной стадии | Не broker-posted факт; negative ties симметричны |
| posted / NUM-POSTED | raw/currency/digits + independent receipt | Broker amount не округляется; local mode только verified и совпадающий с receipt | POSTED/value, REJECT или UNAVAILABLE; posted grid обязателен |
| allocate / NUM-GRANT | Posted net on grid, четыре shares0..1, sum<=1, approved role fixture | Первые4 grants floor в minor units, весь остаток ResidualHeld | ΣGrant=max(0,net); Small positive отдельно в ResidualHeld; неизвестная роль Unsupported |
| balance / NUM-BALANCE | Full state DTO одной currency/digits | Нет | Boolean на точных equalities/nonnegativity; malformed/domain =>False; programmer error видим |
| authorize / NUM-AUTH | Request/state/journal + independent history/allocation/context/snapshot receipt | Нет | Typed eligibility/NO_OP/CONFLICT/REJECT/UNAVAILABLE, без spending |
| apply_for_test / NUM-APPLY | Только authorized unreserved debit | Нет | Copies, exact R-=x/C+=x, revision+1; post-state shape/balance/domain gate до journal commit; не durable CAS |
| worst / NUM-WORST | Complete required levels, currency/digits, settled Available on grid, projected loss/buffer точные | Projected loss/buffer не округляются до unit | A ALL_LEVEL_POSITIVE iff exact min>0; B SINGLE_LEVEL_POSITIVE; bad/missing proof REJECT/UNPROVEN/UNAVAILABLE |
| sequential / NUM-SEQUENTIAL | Settled reserve/positive consumptions одной currency/digits | Нет | Явный prefix trace, appliedCount/rejectedIndex/remaining; conservation каждого шага и prefix; no reuse |
| geometry / NUM-GEOMETRY | Lots/ratios, Vmin/Vmax/step и zero-origin fixture grid | Только integer floor Core/Trend, ceil Small | GEOMETRY_ONLY/REJECT/UNPROVEN/UNAVAILABLE; никаких money/margin/trading guarantees |
| canonical / NUM-CODEC | Versioned typed JSON tokens для поддерживаемого DTO | Numeric values нормализуются exact rational, -0=+0 | str/int/bool/number/list/tuple различаются; Decimal/Fraction одного numeric value эквивалентны; finite typed trees depth<=64, UTF-8 без surrogate; не universal MQL5 source codec |

## Ambient context

Все11 API должны работать независимо от precision/rounding/flags/traps/Emax/Emin. Subject не выполняет Decimal операции. Восемь явно сохранённых context configurations включают низкую precision, все traps, sticky flags и узкий exponent range. Context до/после вызовов идентичен; прогон охватывает direct и composed calls.

## AUTH и границы

История/posted receipts/allocations/snapshot registry/journal — independently assembled fixtures. SourcePlan/OriginRevision не приравниваются к current consumption context. Exact known event после shape/namespace/completeness lookup даёт zero-delta NO_OP до current gates. New event требует всех current/source/available gates. Current revision ULONG_MAX =>UNAVAILABLE.

Global source funding across allocations, durable restart/CAS/concurrency, broker authenticity/precision/margin, own-reservation settlement, real fills и NewFar integration остаются UNPROVEN/NOT_RUN. Компоненты Profit/Swap/Commission/Fee сохраняют знаки. Никакая арифметика не создаёт actual authority из projection.

Источники: Docs/08 DealNet/Allocation/Isolation; Docs/24 Broker Money; R0C Oracle Contract; численный контрпример R0D-01/02. Точные функции/строки и тесты будут привязаны в R0D verification matrix.
