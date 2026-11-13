# AUDIT03 — геометрия, направления и объёмы

Метод: ручные преобразования; никакие числовые примеры не исполнялись. База и хеши — [preservation](HSBI_AUDIT03_BASELINE_AND_PRESERVATION_RU.md). Этот отчёт использует [единый реестр](HSBI_AUDIT03_ALL_ERRORS_RU.md), не создаёт второго перечня ошибок.

## Роли и зеркальная модель

Первичные источники: `Docs/02_SYSTEM_ROLES_AND_IDENTITY_RU.md:6-36`, `Docs/03_FULL_SYSTEM_MANUAL_RU.md:6-21`, `Docs/04_MATHEMATICAL_MODEL_RU.md:9-15,39`.

| Роль/момент | Far SELL | Far BUY | Объём и proof |
|---|---|---|---|
| Initial BUY/SELL | BUY и SELL | BUY и SELL | Равный lock — только явно заданная модель; обе actual positions необходимы |
| INITIAL_PLUS | Подтверждённая прибыльная стартовая нога | Зеркально | Закрывается actual, не по пожеланию плана |
| Far | SELL | BUY | F>0, единственный physical identifier |
| BigCore | BUY | SELL | C=floor_grid(F Rc), обязательная нога >=Vmin |
| BigTrend | BUY | SELL | T=floor_grid(F Rt), Rt=0 требует active-leg решения |
| Small Base | SELL | BUY | S=ceil_grid(F Rs), после округления полный min/max/grid |
| FutureSmall | Будущие projected комбинации | Зеркально | Не broker position и не actual NewFar |
| NewFar | Original Core BUY residual | Original Core SELL residual | Actual original identifier/ticket, не новая сделка из planned N |

До закрытия InitialPlus два lock positions; затем Far; с активной полной C/T/S корзиной четыре managed позиции, а при разрешённом отсутствии Trend — три. После SmallTransition по нормативу остаётся ровно original Core residual. Дескрипторы/aliases не являются дополнительными physical positions. Source `HSBI_Context.mqh:48-53` не проверяет все slots (ERR-012; IMP-006). На netting account это количество независимых positions не следует из встречных orders (ERR-023; IMP-015).

Открытие BUY по Ask, SELL по Bid; ликвидация BUY по Bid, SELL по Ask (F046). Относительная цена C/T/S зависит от actual fill каждого action. Нельзя присвоить всем legs предполагаемую общую цену при partial execution. Историческое имя Far не гарантирует конкретный знак текущего PnL.

## Вывод знака и размерности

Пусть одна и та же линейная выплата имеет K account-money/(lot·price), неизменную конверсию, spread и расходы. Для Far SELL signed объём равен `D=C+T-S-F`; поэтому `dΠ/dP=K D`. Для зеркального Far BUY `dΠ/dP=-K D`.

Введём `s=+1` для Far SELL и `s=-1` для Far BUY, `u=s(P-P0)`. Тогда `dΠ/du=K D`. Следовательно, нужная проверка — `Π(P+s tick)>Π(P)`, а не одинаковый P+tick обоим направлениям. При D=.7,K=1 прирост цены1 даёт +.7 первому и -.7 второму. Это ERR-046, F039/F051, IMP-007. В `HSBI_EvaluateRecoveryMoneyDirection:12-19` сравниваются уже поданные значения: caller обязан подать именно благоприятный next price; helper не строит его самостоятельно.

Если K или расходы зависят от цены/конверсии/времени, простая производная не универсальна: у произведения K(P)·signed payout появляются дополнительные члены. Асимметрия tick value, разные entry prices и различный horizon требуют broker valuation и admitted symbol domain. Положительный D — локальный аналитический фильтр, не actual margin и не прибыльность (ERR-037/042, IMP-021).

## Округление и broker grid

F001–F004 и F044–F049 дают раздельные размерности. `F Rc` в lot; floor/ceil только после деления на lot-step. Для exact floor `C<=raw<C+step`, для ceil `S-step<raw<=S`. Для point distance `DistancePoints*Point` в price; Point не обязан равняться TickSize. Сетка цены проверяется после преобразования.

`HSBI_GeometrySolver.mqh:32` допускает Core0 или on-grid Core без min. Пример ERR-014: F.1,Rc.01,Rt3,Rs.1,step.01 → Core0,Trend.3,Small.01,D.19. Это статический дефект обязательной ноги, несмотря на positive slope. Rt0 имеет самостоятельное противоречие (ERR-015), потому что money evaluator всё равно требует четыре valid legs.

`Docs/14:9` задаёт N=min+n step, но `HSBI_BrokerGrid.mqh:36` использует zero-origin multiples. Их эквивалентность требует min/step integer. Конфигурация min.03,step.02 разделяет два набора. Это ERR-039/F048; конкретный broker такой конфигурацией здесь не подтверждён. Floating tolerance `floor(x/step+1e-12)` имеет иной точный смысл, чем математический floor при значениях сколь угодно близких к границе (ERR-040).

Нельзя автоматически увеличивать Core/Trend до min, если это нарушит lot ratio, risk/margin или affordability. Безопасный proposed outcome — отказ и новый план, а не скрытая коррекция объёма. Выбор active-leg и origin требует владельца; реализации не выполнены.

## Gross и Net

`BigGross=C+T` по составу BigCore/BigTrend из Docs02:13-15 (Small — отдельная роль), `NetBig=C+T-S`, `TotalGross=F+C+T+S`; направление меняет знак Net, но не Gross. При C.7,T.5,S1 nextBigGross1.2,NetBig.2. Если oldBigGross1, проверка .2<1 не доказывает 1.2<1 (ERR-020/F029–030/IMP-012). Отдельные slope gates в полном примере могут отказать: это не превращает неверное сравнение в доказательство требуемого gross-инварианта.

При partial Far с неизменной C/T/S уменьшение F на d увеличивает благоприятный D на d. Однако последующее закрытие Trend уменьшает D на T; полный переход не наследует slope от одного partial шага. После promotion старый Core меняет роль и направление благоприятного движения следующего цикла: входы следующей geometry строятся заново, не переносится прежний favourable sign.

## Промежуточный риск фиксированного SmallTransition

Порядок `Docs/13:12-14`: закрыть Small, Far, Trend, часть Core, перечитать остаток. Для Far SELL:

| После шага | Gross | Net |
|---|---|---|
| Basket active | F+C+T+S | C+T-S-F |
| Close Small | F+C+T | C+T-F |
| Close Far | C+T | C+T |
| Close Trend | C | C |
| Core reduced | N | N |

При F1,C1.2,T1,S.5,N.6: Gross3.7→3.2→2.2→1.2→.6, но Net.7→1.2→2.2→1.2→.6. Зеркало имеет те же абсолютные нагрузки и отрицательный Net. Это F052/ERR-041/IMP-022. Endpoint contraction не ограничивает промежуточную потерю/маржу. При partial fill промежуточный объём лежит между соседними строками, но max monetary risk без модели цен и account margin этим не доказан. Отказ следующего action оставляет открытую направленность. Никакой новый порядок close или защитная торговля здесь не предлагаются как уже разрешённые действия.

## NewFar и завершение

0<N<F, ratio/compression inequalities (F027–028) проверяются по post-round values. Minimum-safe N и global risk-first дают разные выборы (ERR-019). Selected N<=actual residual — preview кандидата, но не доказательство фактического уменьшения до N (ERR-045). Promotion допускается только после перечитывания original Core и повторных all-gates; independent provider ещё не реализован (ERR-013).

При строго уменьшающемся объёме на дискретной сетке число успешных уменьшений ограничено числом доступных lot states. Это не bound времени и не доказательство существования следующего шага. Vmin>0 — ещё открытая позиция. F037/F038/F058 разделяют условную индукцию, неверное prefix⇒tail и operational terminal closure; ERR-021/031/032, IMP-013.

GEOMETRY_VERIFIED=NO для всей системы. Локальная алгебра signed slopes и зеркальности проверена условно; обязательные normative/API/admission/prefix/terminal gaps остаются OPEN.


## COVERAGE-COMPLETION — распространение ERR-020 и ERR-046

ERR-020 нужно искать не только по имени BigGross. Production `HSBI_FutureSmallSolver.mqh` сравнивает netBigVolume в relation к priorBigGross; источники Docs/04:21 и Docs/27_FUTURE_SMALL_SOLVER_RU.md требуют уменьшения BigGross. BigGross=C+T, а не C+T+S; последнее вместе с Far относится к другому total. Все списки candidate/previews обязаны сохранять название и состав одной и той же метрики. Report Audit01 F29 уже называл эту проблему; повтор в AUDIT03 не отдельная новая ошибка.

ERR-046: Docs/03_FULL_SYSTEM_MANUAL_RU.md:12, Docs/05_GEOMETRY_MODEL_RU.md:22 и Docs/26_GEOMETRY_ENGINE_SPECIFICATION_RU.md:7 необходимо читать с единой благоприятной координатой. `HSBI_EvaluateRecoveryMoneyDirection` сам цену не строит; поэтому нельзя приписать ему автоматический неверный BUY price step. Сводные формулы R0A–R0H и Docs/HSB_2E_FORMULA_CONTRACTS* не отменяют primary ambiguity без approval. Полное лексическое доказательство отсутствия иных повторов в каждом историческом Report/машинном oracle ещё не закончено; current coverage это явно учитывает.

Параметрический counterexample для min/Core: F=.1,Rc=.01,Rt=3,Rs=.1,step=.01,Vmin=.01 даёт C0,T.3,S.01,D.19; положительный D не восстанавливает отсутствующую Core. Для случая C=.01,Vmin=.05 потребуются иные допустимые broker inputs с корректным admitted origin; одного on-grid не достаточно. Для убывания Net без убывания BigGross: oldBigGross1, nextC.7,T.5,S1 ⇒ nextBigGross1.2>1, NetBig.2<1. Отдельный slope может отказать; это не доказательство соблюдения именно Gross-контракта.
