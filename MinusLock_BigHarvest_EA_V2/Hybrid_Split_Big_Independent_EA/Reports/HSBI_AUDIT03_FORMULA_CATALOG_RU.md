# AUDIT03 — каталог формул и зависимостей

## Текущий срез FINAL-CLOSURE

На базе b4d8f1ea5caf492f3abd030e5502d40582c52dc8 все66 семейств получили индивидуальные таблицы по15 полей. Текстовая структурная сверка нашла66 последовательностей полей1–15 и66 строк двухосных статусов. Это проверка структуры отчёта, не исполнение формул/тестов. Текущая math ось: VALID_UNDER_ASSUMPTIONS47, FALSE3, CONTRADICTORY2, UNVERIFIED6, UNDEFINED8. Implementation ось: IMPLEMENTED_MATCH6, IMPLEMENTED_MISMATCH9, PARTIALLY_IMPLEMENTED17, NOT_IMPLEMENTED24, CALLER_NOT_VERIFIED10. Эти оси не складываются. Старые сводки/таблицы ниже сохранены как исторические и не являются текущим счётом. Полный document/guard/caller audit ещё PARTIAL.

F039: универсальное P+tick для обоих mirrors переоценено как FALSE математически, тогда как ERR046 остаётся нормативным CONTRADICTION. F041: неопределённый утверждённый settled domain — UNDEFINED по математической оси и NOT_IMPLEMENTED по implementation, а не математический статус NOT_IMPLEMENTED. Ни один ID не переиспользован.


**Текущий каталог: 66 семейств.** Исходные60 сохранены ниже; F061–066 и актуальный непересекающийся счёт — в дополнении COVERAGE-COMPLETION. Каталог пока не объявляется исчерпывающим по всем482 документам.

60 семантических семейств. F01–F49 — независимая переоценка исторического индекса, без наследования PASS; F50–F60 — дополнительные явные выводы. Исторические ID относятся к `Tests/Contracts/HSBI_FULL_SYSTEM_AUDIT_01_FORMULA_MATRIX.json`, прочитанному как индекс, не как oracle. Краткие IDs Fnn ниже означают HSBI-A03-F-nnn. Проверка исключительно ручная, без исполнения примеров.

## Общий словарь и границы

F=объём Far; C/T/S=Core/Trend/Small; N=кандидат или actual residual с обязательным scope. Все объёмы в lot одного symbol. P,Ask,Bid,Point,TickSize — price; ratio/шара — безразмерные. K — money/(lot·price), допустим как общий constant только в явно линейной локальной модели с неизменной конверсией. Profit/Swap/Commission/Fee — signed account currency; Cost/Buffer/LossMagnitude неотрицательные. G=OriginalGrant, C_consumed/Consumed не путать с Core, R_reserved/Reserved не путать с ReserveShare, Free — settled source balance. В карточках consume буква C означает Consumed, в geometry — Core. Counterexamples работают на уровне этой явно указанной алгебры, не являются synthetic broker evidence.

Для каждой карточки поля ниже задают source, предназначение, переменные/размерности/domain, ручной вывод или его отсутствие, production mapping и зависимости на ошибки/предложения. Статус VERIFIED_UNDER_ASSUMPTIONS означает только условное математическое утверждение, не утверждённый экономический норматив и не production PASS. INVALID F38 относится к неверной импликации prefix⇒forall, а не к корректной условной геометрической теореме F58. NOT_IMPLEMENTED относится к реализации, UNDEFINED — к незавершённому нормативному выбору.

| FormulaID | Исторический индекс | Выражение/назначение | Статус формулы | Production mapping |
|---|---|---|---|---|
| HSBI-A03-F-001 | F01 | Core floor(F*Rc) | VERIFIED_UNDER_ASSUMPTIONS | PARTIALLY_IMPLEMENTED |
| HSBI-A03-F-002 | F02 | Trend floor(F*Rt), Rt>=0 | CONTRADICTORY | MISMATCH |
| HSBI-A03-F-003 | F03 | Small ceil(F*Rs) | VERIFIED_UNDER_ASSUMPTIONS | PARTIALLY_IMPLEMENTED |
| HSBI-A03-F-004 | F04 | All active legs min<=V<=max and grid | VERIFIED_UNDER_ASSUMPTIONS | MISMATCH |
| HSBI-A03-F-005 | F05 | Bnet=C+T-S; D=Bnet-F | VERIFIED_UNDER_ASSUMPTIONS | MATCH |
| HSBI-A03-F-006 | F06 | ReserveShare*Bnet>F | VERIFIED_UNDER_ASSUMPTIONS | MATCH |
| HSBI-A03-F-007 | F07 | ActualDealNet=P+Swap+Commission+Fee | VERIFIED_UNDER_ASSUMPTIONS | MATCH |
| HSBI-A03-F-008 | F08 | ProjectedNet=gross+swap+comm+fee-spread-slip-buffer | VERIFIED_UNDER_ASSUMPTIONS | PARTIALLY_IMPLEMENTED |
| HSBI-A03-F-009 | F09 | Every applicable CostID covered exactly once | UNDEFINED | NOT_IMPLEMENTED |
| HSBI-A03-F-010 | F10 | RecoveryPL=RealizedCycleNet+sum OpenCloseNowNet | VERIFIED_UNDER_ASSUMPTIONS | PARTIALLY_IMPLEMENTED |
| HSBI-A03-F-011 | F11 | Threshold=minProfit+execBuffer+moneyTolerance | VERIFIED_UNDER_ASSUMPTIONS | PARTIALLY_IMPLEMENTED |
| HSBI-A03-F-012 | F12 | Committed sumGrants=EligibleNet | UNDEFINED | AMBIGUOUS |
| HSBI-A03-F-013 | F13 | OriginalGrant=Consumed+Reserved+Free | VERIFIED_UNDER_ASSUMPTIONS | NOT_IMPLEMENTED |
| HSBI-A03-F-014 | F14 | RemainingGross=Reserved+Free | VERIFIED_UNDER_ASSUMPTIONS | NOT_IMPLEMENTED |
| HSBI-A03-F-015 | F15 | Consume d: 0<d<=Free; C+=d,Free-=d | VERIFIED_UNDER_ASSUMPTIONS | NOT_IMPLEMENTED |
| HSBI-A03-F-016 | F16 | Equal allocation total != equal vector | VERIFIED_UNDER_ASSUMPTIONS | MISMATCH |
| HSBI-A03-F-017 | F17 | Equal DealNet != equal immutable economic components | VERIFIED_UNDER_ASSUMPTIONS | MISMATCH |
| HSBI-A03-F-018 | F18 | sum funding per source<=EligibleSourceNet | UNVERIFIED | NOT_IMPLEMENTED |
| HSBI-A03-F-019 | F19 | Consumption bound to authoritative remaining allocation | UNVERIFIED | MISMATCH |
| HSBI-A03-F-020 | F20 | AbsoluteFarLoss=max(0,-ProjectedCloseNowFarNet) | VERIFIED_UNDER_ASSUMPTIONS | MATCH |
| HSBI-A03-F-021 | F21 | IncrementalLoss=AbsoluteLoss-BaselineLoss | UNDEFINED | AMBIGUOUS |
| HSBI-A03-F-022 | F22 | CatchUpMargin=EligibleReserve-Loss-Buffer>0 | VERIFIED_UNDER_ASSUMPTIONS | PARTIALLY_IMPLEMENTED |
| HSBI-A03-F-023 | F23 | min_i CatchUpMargin_i>0 vs argmax TransitionLoss | UNDEFINED | AMBIGUOUS |
| HSBI-A03-F-024 | F24 | CurrentTransitionLoss=max(0,-sum signed actual fills) | VERIFIED_UNDER_ASSUMPTIONS | NOT_IMPLEMENTED |
| HSBI-A03-F-025 | F25 | Sticky breach / Peak loss policies | UNDEFINED | NOT_IMPLEMENTED |
| HSBI-A03-F-026 | F26 | AllowedLoss=min(absolute,equity,oldrisk,cumulative caps) | VERIFIED_UNDER_ASSUMPTIONS | PARTIALLY_IMPLEMENTED |
| HSBI-A03-F-027 | F27 | CompressionLots=F-N; ratio=(F-N)/F | VERIFIED_UNDER_ASSUMPTIONS | MATCH |
| HSBI-A03-F-028 | F28 | N<=MaximumNewFarRatio*F | VERIFIED_UNDER_ASSUMPTIONS | MATCH |
| HSBI-A03-F-029 | F29 | NextBigGross<OldBigGross | VERIFIED_UNDER_ASSUMPTIONS | MISMATCH |
| HSBI-A03-F-030 | F30 | Gross=sum abs volumes; Net=sum signed volumes | VERIFIED_UNDER_ASSUMPTIONS | MATCH |
| HSBI-A03-F-031 | F31 | RiskNext<RiskOld-Tolerance | UNVERIFIED | NOT_VERIFIED |
| HSBI-A03-F-032 | F32 | TotalAccountMargin=sum standalone leg margins | UNVERIFIED | PARTIALLY_IMPLEMENTED |
| HSBI-A03-F-033 | F33 | MarginLevel=100*Equity/Margin | VERIFIED_UNDER_ASSUMPTIONS | NOT_IMPLEMENTED |
| HSBI-A03-F-034 | F34 | Equity=Balance+FloatingNet | VERIFIED_UNDER_ASSUMPTIONS | NOT_IMPLEMENTED |
| HSBI-A03-F-035 | F35 | EconomicCyclePnL=AllRealized+OpenLiquidationNet | VERIFIED_UNDER_ASSUMPTIONS | AMBIGUOUS |
| HSBI-A03-F-036 | F36 | Nonfinite/unknown cannot pass money/risk/outcome gate | VERIFIED_UNDER_ASSUMPTIONS | MISMATCH |
| HSBI-A03-F-037 | F37 | K>=ceil(log(Vmin/F0)/log(q)) | VERIFIED_UNDER_ASSUMPTIONS | PARTIALLY_IMPLEMENTED |
| HSBI-A03-F-038 | F38 | Finite prefix implies uniform geometric future bound | INVALID | MISMATCH |
| HSBI-A03-F-039 | F39 | RecoveryMoney(P+tick)>RecoveryMoney(P) both mirrors | CONTRADICTORY | AMBIGUOUS |
| HSBI-A03-F-040 | F40 | PartialClose=floor_grid(Budget/LossPerLot) | VERIFIED_UNDER_ASSUMPTIONS | NOT_IMPLEMENTED |
| HSBI-A03-F-041 | F41 | Checked signed int64 settled arithmetic | NOT_IMPLEMENTED | NOT_IMPLEMENTED |
| HSBI-A03-F-042 | F42 | F64Z/T17Z canonical numeric identity | UNVERIFIED | NOT_IMPLEMENTED |
| HSBI-A03-F-043 | F43 | Small decrements remain exact near 10^28 | VERIFIED_UNDER_ASSUMPTIONS | NOT_IMPLEMENTED |
| HSBI-A03-F-044 | F44 | NormalizePrice=round(price/tickSize)*tickSize | VERIFIED_UNDER_ASSUMPTIONS | PARTIALLY_IMPLEMENTED |
| HSBI-A03-F-045 | F45 | Level=Reference+s*(Start+(k-1)*Step)*Point | VERIFIED_UNDER_ASSUMPTIONS | NOT_VERIFIED |
| HSBI-A03-F-046 | F46 | BUY closes Bid; SELL closes Ask | VERIFIED_UNDER_ASSUMPTIONS | PARTIALLY_IMPLEMENTED |
| HSBI-A03-F-047 | F47 | Minimum-safe N vs global risk-first objective | CONTRADICTORY | AMBIGUOUS |
| HSBI-A03-F-048 | F48 | Grid n*step vs Vmin+n*step | UNDEFINED | AMBIGUOUS |
| HSBI-A03-F-049 | F49 | round(sum components) vs sum(round components) | VERIFIED_UNDER_ASSUMPTIONS | AMBIGUOUS |
| HSBI-A03-F-050 | Дополнительный вывод | Equal-volume Initial Lock PnL=-L*K*(spread0+spread_t) | VERIFIED_UNDER_ASSUMPTIONS | NOT_IMPLEMENTED |
| HSBI-A03-F-051 | Дополнительный вывод | Favorable coordinate u=s(P-P0); dPi/du=K*(C+T-S-F) | VERIFIED_UNDER_ASSUMPTIONS | PARTIALLY_IMPLEMENTED |
| HSBI-A03-F-052 | Дополнительный вывод | Transition prefix Net: D→C+T-F→C+T→C→N | VERIFIED_UNDER_ASSUMPTIONS | NOT_IMPLEMENTED |
| HSBI-A03-F-053 | Дополнительный вывод | Reserve d:(R,Free)→(R+d,Free-d) | VERIFIED_UNDER_ASSUMPTIONS | NOT_IMPLEMENTED |
| HSBI-A03-F-054 | Дополнительный вывод | Release owner d:(R,Free)→(R-d,Free+d) | VERIFIED_UNDER_ASSUMPTIONS | NOT_IMPLEMENTED |
| HSBI-A03-F-055 | Дополнительный вывод | Unreserved consume d:(C,Free)→(C+d,Free-d) | VERIFIED_UNDER_ASSUMPTIONS | NOT_IMPLEMENTED |
| HSBI-A03-F-056 | Дополнительный вывод | Reserved owner consume d:(C,R)→(C+d,R-d) | VERIFIED_UNDER_ASSUMPTIONS | NOT_IMPLEMENTED |
| HSBI-A03-F-057 | Дополнительный вывод | Exact replay delta0; changed replay CONFLICT | VERIFIED_UNDER_ASSUMPTIONS | MISMATCH |
| HSBI-A03-F-058 | Дополнительный вывод | Uniform contraction implies F_k<=q^k*F_0 | VERIFIED_UNDER_ASSUMPTIONS | PARTIALLY_IMPLEMENTED |
| HSBI-A03-F-059 | Дополнительный вывод | Unhedged SELL adverse loss=F*K*(P-Popen) | VERIFIED_UNDER_ASSUMPTIONS | NOT_IMPLEMENTED |
| HSBI-A03-F-060 | Дополнительный вывод | Projected→Actual→Reconciled→Eligible→Available are distinct transformations | UNVERIFIED | NOT_IMPLEMENTED |

## HSBI-A03-F-001 — Core floor(F*Rc)

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:9`. **Production операция/строки:** `Include/Planning/HSBI_BrokerGrid.mqh:26`; mapping **PARTIALLY_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** lot; F,Rc,step finite,step>0; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** По определению floor: C<=F*Rc<C+step. Это точная вещественная модель без добавленного tolerance; после floor обязателен Core>=min.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-014, HSBI-A03-ERR-040; HSBI-A03-IMP-007, HSBI-A03-IMP-002. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-001 |
| 2 Exact normative source | Docs/04_MATHEMATICAL_MODEL_RU.md:9 |
| 3 Expression | Core floor(F*Rc) |
| 4 Variables | F — Far lot; Rc — Core/F ratio; h — volume step lot; C — нормализованный Core lot |
| 5 Dimensions | lot |
| 6 Domain | lot; F,Rc,step finite,step>0. |
| 7 Required assumptions | lot; F,Rc,step finite,step>0. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | По определению floor: C<=F*Rc<C+step. Это точная вещественная модель без добавленного tolerance; после floor обязателен Core>=min. |
| 9 Far BUY / Far SELL | Far SELL→Core BUY;Far BUY→Core SELL; объём одинаков по модулю. |
| 10 Broker grid / rounding | Floor zero-origin: C≤FRc<C+h; проверять Core≥Vmin после округления; tolerance не exact floor. |
| 11 Bid / Ask / costs | NOT_APPLICABLE к lot normalization; Bid/Ask и costs нужны для последующего money/risk gate. |
| 12 Partial fills / actual data | FRc — planned volume; actual fills повторно сверяются, partial не полный Core. |
| 13 Production mapping | Include/Planning/HSBI_BrokerGrid.mqh:26 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-014, HSBI-A03-ERR-040; HSBI-A03-IMP-007, HSBI-A03-IMP-002. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=PARTIALLY_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-002 — Trend floor(F*Rt), Rt>=0

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:9`. **Production операция/строки:** `Include/Money/HSBI_BasketMoneyEvaluator.mqh:15-16`; mapping **MISMATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** CONTRADICTORY.

**Переменные, размерности и область:** lot; Rt=0 included; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** При Rt0 математически T0. Документ требует каждый lot>=min, geometry допускает zero, money-leg требует positive. Нужна active-leg конвенция.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-015; HSBI-A03-IMP-007. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-002 |
| 2 Exact normative source | Docs/04_MATHEMATICAL_MODEL_RU.md:9 |
| 3 Expression | Trend floor(F*Rt), Rt>=0 |
| 4 Variables | F — Far lot; Rt≥0 — Trend ratio; h — step; T — Trend lot; activeTrend — явно выбранная активность |
| 5 Dimensions | lot |
| 6 Domain | lot; Rt=0 included. |
| 7 Required assumptions | lot; Rt=0 included. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | При Rt0 математически T0. Документ требует каждый lot>=min, geometry допускает zero, money-leg требует positive. Нужна active-leg конвенция. |
| 9 Far BUY / Far SELL | Trend противоположен Far в обоих направлениях; Rt=0 требует явной inactive-leg policy. |
| 10 Broker grid / rounding | T=0 не активный допустимый min lot; каждый положительный T проверяется после floor. |
| 11 Bid / Ask / costs | Отсутствующий Trend не обязан иметь positive-volume money evaluation; costs только реально активных ног. |
| 12 Partial fills / actual data | Неоткрытая/частично открытая Trend не объявляется completed отсутствующей без policy. |
| 13 Production mapping | Include/Money/HSBI_BasketMoneyEvaluator.mqh:15-16 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-015; HSBI-A03-IMP-007. |
| 15 Final statuses | MATH=CONTRADICTORY; IMPLEMENTATION=IMPLEMENTED_MISMATCH; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-003 — Small ceil(F*Rs)

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:9`. **Production операция/строки:** `Include/Planning/HSBI_BrokerGrid.mqh:27`; mapping **PARTIALLY_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** lot; F,Rs>0,step>0; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Из ceil: S-step<F*Rs<=S. Округление вверх увеличивает hedge/расходы, поэтому max/margin перепроверяются. Tolerance и overflow отдельно.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-040; HSBI-A03-IMP-002, HSBI-A03-IMP-007. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-003 |
| 2 Exact normative source | Docs/04_MATHEMATICAL_MODEL_RU.md:9 |
| 3 Expression | Small ceil(F*Rs) |
| 4 Variables | F — Far lot; Rs>0 — Small ratio; h — step; S — Small lot |
| 5 Dimensions | lot |
| 6 Domain | lot; F,Rs>0,step>0. |
| 7 Required assumptions | lot; F,Rs>0,step>0. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | Из ceil: S-step<F*Rs<=S. Округление вверх увеличивает hedge/расходы, поэтому max/margin перепроверяются. Tolerance и overflow отдельно. |
| 9 Far BUY / Far SELL | Small сонаправлен Far SELL/BUY соответственно. |
| 10 Broker grid / rounding | Ceil raw/h даёт увеличение; после него min/max/grid и все gates заново. |
| 11 Bid / Ask / costs | Увеличение Small меняет spread/fees/risk; money side определяется фактическим BUY/SELL. |
| 12 Partial fills / actual data | Округлённый план не подтверждает actual Small или complete fill. |
| 13 Production mapping | Include/Planning/HSBI_BrokerGrid.mqh:27 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-040; HSBI-A03-IMP-002, HSBI-A03-IMP-007. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=PARTIALLY_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-004 — All active legs min<=V<=max and grid

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:9`. **Production операция/строки:** `Include/Planning/HSBI_GeometrySolver.mqh:32-33`; mapping **MISMATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** lot; active role,min>0,max>=min; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Membership в broker admissible set необходимо для исполнения. Core0 не active допустимый lot; положительный raw не доказывает post-round validity.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-014, HSBI-A03-ERR-015; HSBI-A03-IMP-007. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-004 |
| 2 Exact normative source | Docs/04_MATHEMATICAL_MODEL_RU.md:9 |
| 3 Expression | All active legs min<=V<=max and grid |
| 4 Variables | V — actual/projected объём активной ноги; Vmin,Vmax,h — broker bounds/step; o — volume origin |
| 5 Dimensions | lot |
| 6 Domain | lot; active role,min>0,max>=min. |
| 7 Required assumptions | lot; active role,min>0,max>=min. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | Membership в broker admissible set необходимо для исполнения. Core0 не active допустимый lot; положительный raw не доказывает post-round validity. |
| 9 Far BUY / Far SELL | Одинаковый admissible lot set для BUY/SELL только при соответствующих broker permissions. |
| 10 Broker grid / rounding | Origin,min,max,step независимы; активная нога требует V≥Vmin; unknown origin не угадывается. |
| 11 Bid / Ask / costs | Lot admission не money/fill guarantee; valuation и costs отдельно. |
| 12 Partial fills / actual data | Каждый actual residual проверяется; trade fill step не автоматически same-as-request minimum. |
| 13 Production mapping | Include/Planning/HSBI_GeometrySolver.mqh:32-33 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-014, HSBI-A03-ERR-015; HSBI-A03-IMP-007. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=IMPLEMENTED_MISMATCH; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-005 — Bnet=C+T-S; D=Bnet-F

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:12`. **Production операция/строки:** `Include/Planning/HSBI_GeometrySolver.mqh:6-10`; mapping **MATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** lot; common symbol,linear same K; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Сложение signed volumes даёт Net для FarSELL. В favorable coordinate derivative=K*D, не безусловный рост денег во времени. См.F51.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-046, HSBI-A03-ERR-037; HSBI-A03-IMP-007, HSBI-A03-IMP-021. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-005 |
| 2 Exact normative source | Docs/04_MATHEMATICAL_MODEL_RU.md:12 |
| 3 Expression | Bnet=C+T-S; D=Bnet-F |
| 4 Variables | C,T,S,F — объёмы Core,Trend,Small,Far; Bnet=C+T−S; D=Bnet−F |
| 5 Dimensions | lot |
| 6 Domain | lot; common symbol,linear same K. |
| 7 Required assumptions | lot; common symbol,linear same K. Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | Сложение signed volumes даёт Net для FarSELL. В favorable coordinate derivative=K*D, не безусловный рост денег во времени. См.F51. |
| 9 Far BUY / Far SELL | Far SELL Net=D, Far BUY Net=−D; в благоприятной координате slope KD. |
| 10 Broker grid / rounding | C/T/S/F после брокерского округления; raw positive D не post-round proof. |
| 11 Bid / Ask / costs | K постоянный общий; при asymmetric ticks/FX/variable costs денежная производная иная. |
| 12 Partial fills / actual data | Использовать фактические volumes для actual slope; planned slope только preview. |
| 13 Production mapping | Include/Planning/HSBI_GeometrySolver.mqh:6-10 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-046, HSBI-A03-ERR-037; HSBI-A03-IMP-007, HSBI-A03-IMP-021. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=IMPLEMENTED_MATCH; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-006 — ReserveShare*Bnet>F

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:15`. **Production операция/строки:** `Include/Money/HSBI_CatchUpModel.mqh:12`; mapping **MATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** lot; share dimensionless[0,1],same K; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Сравнение slopes reserve и Far применимо при одинаковой линейной базе, расстояниях и eligible policy. Не покрывает разные entry prices, costs или availability.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-043, HSBI-A03-ERR-033; HSBI-A03-IMP-010, HSBI-A03-IMP-004. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-006 |
| 2 Exact normative source | Docs/04_MATHEMATICAL_MODEL_RU.md:15 |
| 3 Expression | ReserveShare*Bnet>F |
| 4 Variables | r — reserve share; Bnet — net Big lot; F — Far lot; K — общий money/(lot·price) |
| 5 Dimensions | lot |
| 6 Domain | lot; share dimensionless[0,1],same K. |
| 7 Required assumptions | lot; share dimensionless[0,1],same K. Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | Сравнение slopes reserve и Far применимо при одинаковой линейной базе, расстояниях и eligible policy. Не покрывает разные entry prices, costs или availability. |
| 9 Far BUY / Far SELL | Для обоих зеркал favorable movement задаётся разным знаком цены. |
| 10 Broker grid / rounding | Использовать нормализованные Bnet/F; ratio r не lot. |
| 11 Bid / Ask / costs | rBnet>F — slope filter при общем K, не доказательство текущего покрытия начального loss/cost deficit. |
| 12 Partial fills / actual data | Actual eligible source определяется после confirmed closes; projected slope не reserve funding. |
| 13 Production mapping | Include/Money/HSBI_CatchUpModel.mqh:12 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-043, HSBI-A03-ERR-033; HSBI-A03-IMP-010, HSBI-A03-IMP-004. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=IMPLEMENTED_MATCH; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-007 — ActualDealNet=P+Swap+Commission+Fee

**Источник правила:** `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:6`. **Production операция/строки:** `Include/Money/HSBI_CostModel.mqh:13`; mapping **MATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** signed account currency; common deal/window; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Компоненты signed:60-2-7-1=50. Комиссия уже отрицательна и не меняет знак повторно. Подлинность и полнота history не следуют из суммы.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-022, HSBI-A03-ERR-033; HSBI-A03-IMP-014, HSBI-A03-IMP-004. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-007 |
| 2 Exact normative source | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:6 |
| 3 Expression | ActualDealNet=P+Swap+Commission+Fee |
| 4 Variables | P — signed DEAL_PROFIT, W — DEAL_SWAP, C_fee — DEAL_COMMISSION, E — DEAL_FEE; N — DealNet |
| 5 Dimensions | signed account currency |
| 6 Domain | signed account currency; common deal/window. |
| 7 Required assumptions | signed account currency; common deal/window. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | Компоненты signed:60-2-7-1=50. Комиссия уже отрицательна и не меняет знак повторно. Подлинность и полнота history не следуют из суммы. |
| 9 Far BUY / Far SELL | Signed broker components складываются одинаково для BUY/SELL; gross profit уже отражает сторону. |
| 10 Broker grid / rounding | Сначала определить broker posting policy; raw sum и posted net не всегда одна grid. |
| 11 Bid / Ask / costs | Profit+Swap+Commission+Fee сохраняют полученные знаки; нельзя второй раз вычитать commission. |
| 12 Partial fills / actual data | Каждый confirmed deal отдельно; полная история/ownership не следуют из арифметического net. |
| 13 Production mapping | Include/Money/HSBI_CostModel.mqh:13 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-022, HSBI-A03-ERR-033; HSBI-A03-IMP-014, HSBI-A03-IMP-004. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=IMPLEMENTED_MATCH; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-008 — ProjectedNet=gross+swap+comm+fee-spread-slip-buffer

**Источник правила:** `Docs/24_BROKER_MONEY_MODEL_RU.md:7`. **Production операция/строки:** `Include/Money/HSBI_CostModel.mqh:18`; mapping **PARTIALLY_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money; signed actual components,nonnegative extra allowances; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Алгебра верна только при disjoint costs: сумма исходной выплаты и ещё не включённых signed charges/extra allowances. Actual settled result не равен forecast автоматически.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-022; HSBI-A03-IMP-014. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-008 |
| 2 Exact normative source | Docs/24_BROKER_MONEY_MODEL_RU.md:7 |
| 3 Expression | ProjectedNet=gross+swap+comm+fee-spread-slip-buffer |
| 4 Variables | G — projected gross profit; W,C_fee,E — signed costs; Sp,Sl,B — nonnegative extra deductions |
| 5 Dimensions | money |
| 6 Domain | money; signed actual components,nonnegative extra allowances. |
| 7 Required assumptions | money; signed actual components,nonnegative extra allowances. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | Алгебра верна только при disjoint costs: сумма исходной выплаты и ещё не включённых signed charges/extra allowances. Actual settled result не равен forecast автоматически. |
| 9 Far BUY / Far SELL | Gross берётся на правильной close side для каждой BUY/SELL ноги. |
| 10 Broker grid / rounding | Не округлять adverse deductions до безопасного0; scale/basis должен быть известен. |
| 11 Bid / Ask / costs | Sp/Sl/B вычитаются только если ещё не включены; signed charges сохраняют знак. |
| 12 Partial fills / actual data | Forecast до fills; actual reconcile заменяет прогноз, а не добавляется к нему повторно. |
| 13 Production mapping | Include/Money/HSBI_CostModel.mqh:18 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-022; HSBI-A03-IMP-014. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=PARTIALLY_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-009 — Every applicable CostID covered exactly once

**Источник правила:** `Docs/24_BROKER_MONEY_MODEL_RU.md:7`. **Production операция/строки:** `Include/Money/HSBI_CostModel.mqh:4-18`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** UNDEFINED.

**Переменные, размерности и область:** CostID,basis,window,currency,authority; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** В текущем scalar snapshot нет полного независимого набора обязательных расходов и overlap mapping. Bid/Ask profit уже может содержать spread. Список компонентов без basis не завершает proof.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-022; HSBI-A03-IMP-014. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-009 |
| 2 Exact normative source | Docs/24_BROKER_MONEY_MODEL_RU.md:7 |
| 3 Expression | Every applicable CostID covered exactly once |
| 4 Variables | CostID — независимый тип расхода; A — обязательный applicable inventory; basis/window/currency — область однократного учёта |
| 5 Dimensions | CostID,basis,window,currency,authority. |
| 6 Domain | CostID,basis,window,currency,authority. |
| 7 Required assumptions | CostID,basis,window,currency,authority. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | В текущем scalar snapshot нет полного независимого набора обязательных расходов и overlap mapping. Bid/Ask profit уже может содержать spread. Список компонентов без basis не завершает proof. |
| 9 Far BUY / Far SELL | Cost applicability определяется отдельно для BUY/SELL/операции/окна. |
| 10 Broker grid / rounding | Currency posting grid не доказывает inventory completeness или отсутствие overlap. |
| 11 Bid / Ask / costs | Каждый обязательный CostID учтён ровно один раз; UNKNOWN не KNOWN_ZERO. |
| 12 Partial fills / actual data | Partial fills могут изменить fees/slippage/window; complete set переоценивается по actual. |
| 13 Production mapping | Include/Money/HSBI_CostModel.mqh:4-18 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-022; HSBI-A03-IMP-014. |
| 15 Final statuses | MATH=UNDEFINED; IMPLEMENTATION=NOT_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-010 — RecoveryPL=RealizedCycleNet+sum OpenCloseNowNet

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:18`. **Production операция/строки:** `Include/Money/HSBI_MoneyTypes.mqh:9`; mapping **PARTIALLY_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money; disjoint realised/open sets,same cycle/currency; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Partition экономических cash flows даёт равенство. Allocation — подмножества realised, повторное прибавление Reserve удвоит прибыль. Граница InitialProfit отдельно F35.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-036, HSBI-A03-ERR-044; HSBI-A03-IMP-020. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-010 |
| 2 Exact normative source | Docs/04_MATHEMATICAL_MODEL_RU.md:18 |
| 3 Expression | RecoveryPL=RealizedCycleNet+sum OpenCloseNowNet |
| 4 Variables | R — RealizedCycleNet в выбранной границе; Ui — CloseNow net каждой ещё открытой позиции; PL — recovery result |
| 5 Dimensions | money |
| 6 Domain | money; disjoint realised/open sets,same cycle/currency. |
| 7 Required assumptions | money; disjoint realised/open sets,same cycle/currency. Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | Partition экономических cash flows даёт равенство. Allocation — подмножества realised, повторное прибавление Reserve удвоит прибыль. Граница InitialProfit отдельно F35. |
| 9 Far BUY / Far SELL | Каждая открытая BUY закрывается Bid, SELL Ask; realized signed уже фиксирован. |
| 10 Broker grid / rounding | Согласованный monetary scale; lot grid влияет на состав/остатки позиций. |
| 11 Bid / Ask / costs | OpenCloseNow должен включать ещё применимые exit costs без второго Reserve дохода. |
| 12 Partial fills / actual data | Разделить realised deals и оставшиеся open quantities после каждого partial fill. |
| 13 Production mapping | Include/Money/HSBI_MoneyTypes.mqh:9 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-036, HSBI-A03-ERR-044; HSBI-A03-IMP-020. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=PARTIALLY_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-011 — Threshold=minProfit+execBuffer+moneyTolerance

**Источник правила:** `Docs/12_FINAL_CLOSE_SPECIFICATION_RU.md:7`. **Production операция/строки:** `Include/Money/HSBI_MoneyTypes.mqh:7-9`; mapping **PARTIALLY_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money; finite nonnegative terms; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Сумма однородна по размерности; PL>=threshold — planned gate. Passed unvalidated threshold и возможное повторное inclusion buffer требуют отдельного constructor/cost contract.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-044, HSBI-A03-ERR-022; HSBI-A03-IMP-020, HSBI-A03-IMP-014. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-011 |
| 2 Exact normative source | Docs/12_FINAL_CLOSE_SPECIFICATION_RU.md:7 |
| 3 Expression | Threshold=minProfit+execBuffer+moneyTolerance |
| 4 Variables | m — minimumProfit; b — executionBuffer; t — moneyTolerance; H=m+b+t — threshold |
| 5 Dimensions | money |
| 6 Domain | money; finite nonnegative terms. |
| 7 Required assumptions | money; finite nonnegative terms. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | Сумма однородна по размерности; PL>=threshold — planned gate. Passed unvalidated threshold и возможное повторное inclusion buffer требуют отдельного constructor/cost contract. |
| 9 Far BUY / Far SELL | Порог в money одинаков по смыслу для обоих направлений; PL side-specific. |
| 10 Broker grid / rounding | Money tolerance не заменяет lot/price admission и не обнуляет убыток. |
| 11 Bid / Ask / costs | ExecutionBuffer должен иметь independent coverage, не повтор уже включённого расхода. |
| 12 Partial fills / actual data | Positive preview threshold не гарантия последующего profitable complete settlement. |
| 13 Production mapping | Include/Money/HSBI_MoneyTypes.mqh:7-9 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-044, HSBI-A03-ERR-022; HSBI-A03-IMP-020, HSBI-A03-IMP-014. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=PARTIALLY_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-012 — Committed sumGrants=EligibleNet

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:30`. **Production операция/строки:** `Include/Money/HSBI_AllocationLedgerTypes.mqh:7`; mapping **AMBIGUOUS**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** UNDEFINED.

**Переменные, размерности и область:** settled money; positive posted source,phase explicit; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Полное распределение требует равенства; partial preparation требует остатка. 10<=50 не доказывает полного распределения50. В старом типе нет достаточного phase mapping.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-006; HSBI-A03-IMP-003. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-012 |
| 2 Exact normative source | Docs/04_MATHEMATICAL_MODEL_RU.md:30 |
| 3 Expression | Committed sumGrants=EligibleNet |
| 4 Variables | Gj — grants/buckets по источнику; N — eligible posted source; U — unallocated; phase — PREPARED/COMMITTED |
| 5 Dimensions | settled money |
| 6 Domain | settled money; positive posted source,phase explicit. |
| 7 Required assumptions | settled money; positive posted source,phase explicit. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | Полное распределение требует равенства; partial preparation требует остатка. 10<=50 не доказывает полного распределения50. В старом типе нет достаточного phase mapping. |
| 9 Far BUY / Far SELL | NOT_APPLICABLE напрямую: per-source денежное распределение, direction уже подтверждён source. |
| 10 Broker grid / rounding | Exact posted units + explicit residual; PREPARED unallocated не spendable. |
| 11 Bid / Ask / costs | Расходы до eligible source; negative deals экономически учитываются, grant не создают. |
| 12 Partial fills / actual data | Распределять только reconciled source; partial basket не complete source/history. |
| 13 Production mapping | Include/Money/HSBI_AllocationLedgerTypes.mqh:7 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-006; HSBI-A03-IMP-003. |
| 15 Final statuses | MATH=UNDEFINED; IMPLEMENTATION=CALLER_NOT_VERIFIED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-013 — OriginalGrant=Consumed+Reserved+Free

**Источник правила:** `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:12,24`. **Production операция/строки:** `Include/Money/HSBI_AllocationLedgerTypes.mqh:5-7`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** settled money,each component>=0; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Это partition одного grant при disjoint state categories. Инвариант сохраняется операциями F53–F56, но не устанавливает независимую подлинность самого grant.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-005, HSBI-A03-ERR-006, HSBI-A03-ERR-033; HSBI-A03-IMP-003, HSBI-A03-IMP-004. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-013 |
| 2 Exact normative source | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:12,24 |
| 3 Expression | OriginalGrant=Consumed+Reserved+Free |
| 4 Variables | G — immutable OriginalGrant; Cc — Consumed; Rr — Reserved; Ff — Free |
| 5 Dimensions | settled money,each component>=0. |
| 6 Domain | settled money,each component>=0. |
| 7 Required assumptions | settled money,each component>=0. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | Это partition одного grant при disjoint state categories. Инвариант сохраняется операциями F53–F56, но не устанавливает независимую подлинность самого grant. |
| 9 Far BUY / Far SELL | NOT_APPLICABLE к partition: signed trades уже отражены в исходном settled grant. |
| 10 Broker grid / rounding | G/Cc/Rr/Ff одной currency/posting lattice, точная сумма, все категории disjoint. |
| 11 Bid / Ask / costs | Расходы не вычитаются ещё раз из grants; additional spend требует отдельного event. |
| 12 Partial fills / actual data | Partial debit меняет одну категорию один раз; unknown journal не known Free. |
| 13 Production mapping | Include/Money/HSBI_AllocationLedgerTypes.mqh:5-7 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-005, HSBI-A03-ERR-006, HSBI-A03-ERR-033; HSBI-A03-IMP-003, HSBI-A03-IMP-004. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=NOT_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-014 — RemainingGross=Reserved+Free

**Источник правила:** `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:24`. **Production операция/строки:** `Include/Money/HSBI_MoneyState.mqh:4-5`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money; candidate mapping,not approved migration; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Из F13 RemainingGross=G-Consumed. При G50,C10,R15,Free25 remaining40; тратить можно25, а не40. Старое Remaining без owner/precision не мигрирует безопасно.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-006; HSBI-A03-IMP-003. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-014 |
| 2 Exact normative source | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:24 |
| 3 Expression | RemainingGross=Reserved+Free |
| 4 Variables | RG — RemainingGross; Rr — Reserved; Ff — Free; G — OriginalGrant; Cc — Consumed |
| 5 Dimensions | money |
| 6 Domain | money; candidate mapping,not approved migration. |
| 7 Required assumptions | money; candidate mapping,not approved migration. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | Из F13 RemainingGross=G-Consumed. При G50,C10,R15,Free25 remaining40; тратить можно25, а не40. Старое Remaining без owner/precision не мигрирует безопасно. |
| 9 Far BUY / Far SELL | NOT_APPLICABLE: RemainingGross — денежная view, не направление позиции. |
| 10 Broker grid / rounding | RG=G−Cc=Rr+Ff в тех же minor units; legacy Remaining не переименовывать без schema. |
| 11 Bid / Ask / costs | Reserve не новый PnL; owner-held Rr нельзя считать доступным другому consumer. |
| 12 Partial fills / actual data | Actual consume/release обновляет RG/Free по различным операциям; restart требует их различать. |
| 13 Production mapping | Include/Money/HSBI_MoneyState.mqh:4-5 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-006; HSBI-A03-IMP-003. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=NOT_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-015 — Consume d: 0<d<=Free; C+=d,Free-=d

**Источник правила:** `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:24`. **Production операция/строки:** `Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:47,63-70`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money; atomic source/allocation/owner/event authority; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Сумма C+Free сохраняется, Free неотрицательно. Проверка одного stale остатка недостаточна двум потребителям: нужны serialisation/CAS и replay receipt.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-007, HSBI-A03-ERR-008, HSBI-A03-ERR-017; HSBI-A03-IMP-004, HSBI-A03-IMP-009. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-015 |
| 2 Exact normative source | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:24 |
| 3 Expression | Consume d: 0<d<=Free; C+=d,Free-=d |
| 4 Variables | d — debit; Ff — незарезервированный Free; Cc — накопленный Consumed |
| 5 Dimensions | money |
| 6 Domain | money; atomic source/allocation/owner/event authority. |
| 7 Required assumptions | money; atomic source/allocation/owner/event authority. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | Сумма C+Free сохраняется, Free неотрицательно. Проверка одного stale остатка недостаточна двум потребителям: нужны serialisation/CAS и replay receipt. |
| 9 Far BUY / Far SELL | NOT_APPLICABLE к сохранению Cc+Ff; цель debit определяется bucket policy. |
| 10 Broker grid / rounding | 0<d≤authoritative Free в той же currency/precision, checked exact updates. |
| 11 Bid / Ask / costs | Debit включает actual permissible charge, а risk buffer не обязательно actual списание. |
| 12 Partial fills / actual data | Commit атомарен с immutable receipt; altered replay conflict, exact replay zero delta. |
| 13 Production mapping | Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:47,63-70 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-007, HSBI-A03-ERR-008, HSBI-A03-ERR-017; HSBI-A03-IMP-004, HSBI-A03-IMP-009. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=NOT_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-016 — Equal allocation total != equal vector

**Источник правила:** `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:15`. **Production операция/строки:** `Include/Money/HSBI_AllocationLedgerTypes.mqh:8`; mapping **MISMATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** ordered money vector with purpose labels; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Векторы (50,0) и (0,50) имеют одинаковую сумму, но не равны покомпонентно. Payload event должен включать каждый bucket и policy.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-004; HSBI-A03-IMP-003. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-016 |
| 2 Exact normative source | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:15 |
| 3 Expression | Equal allocation total != equal vector |
| 4 Variables | A,B — ordered vectors FinalReserve/PartialFar/Transition/Carry/Residual с policy/event identity |
| 5 Dimensions | ordered money vector with purpose labels. |
| 6 Domain | ordered money vector with purpose labels. |
| 7 Required assumptions | ordered money vector with purpose labels. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | Векторы (50,0) и (0,50) имеют одинаковую сумму, но не равны покомпонентно. Payload event должен включать каждый bucket и policy. |
| 9 Far BUY / Far SELL | NOT_APPLICABLE: equality ordered allocation vector, роли направлений уже source facts. |
| 10 Broker grid / rounding | Точное equality каждого posted bucket, без epsilon скрывающего изменённый payload. |
| 11 Bid / Ask / costs | Costs до eligible source, policy identity не заменяется равенством общей суммы. |
| 12 Partial fills / actual data | Partial grants/reservations не меняют immutable original vector; changes отдельными events. |
| 13 Production mapping | Include/Money/HSBI_AllocationLedgerTypes.mqh:8 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-004; HSBI-A03-IMP-003. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=IMPLEMENTED_MISMATCH; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-017 — Equal DealNet != equal immutable economic components

**Источник правила:** `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:6,15`. **Production операция/строки:** `Include/Money/HSBI_EconomicLedgerTypes.mqh:9`; mapping **MISMATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money/IDs; same source key; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Линейная сумма неинъективна: (P50,C0) и(P60,C-10) дают50. Полное equality необходимо независимо от итогового Net.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-001, HSBI-A03-ERR-002; HSBI-A03-IMP-001. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-017 |
| 2 Exact normative source | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:6,15 |
| 3 Expression | Equal DealNet != equal immutable economic components |
| 4 Variables | a,b — экономические records одного logical source; Net — сумма signed Profit/Swap/Commission/Fee |
| 5 Dimensions | money/IDs |
| 6 Domain | money/IDs; same source key. |
| 7 Required assumptions | money/IDs; same source key. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | Линейная сумма неинъективна: (P50,C0) и(P60,C-10) дают50. Полное equality необходимо независимо от итогового Net. |
| 9 Far BUY / Far SELL | Один и тот же logical source не меняется от Magic/Cycle/role; BUY/SELL immutable facts отдельно. |
| 10 Broker grid / rounding | Captured raw и posted money policy explicit; одинаковый Net не full component equality. |
| 11 Bid / Ask / costs | P50/C0 и P60/C−10 имеют один Net,но different immutable economic body. |
| 12 Partial fills / actual data | Разные partial deals имеют разные source identities; changed payload того же deal — conflict. |
| 13 Production mapping | Include/Money/HSBI_EconomicLedgerTypes.mqh:9 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-001, HSBI-A03-ERR-002; HSBI-A03-IMP-001. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=IMPLEMENTED_MISMATCH; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-018 — sum funding per source<=EligibleSourceNet

**Источник правила:** `Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md:3`. **Production операция/строки:** `Include/Money/HSBI_ReserveAllocationTypes.mqh:23`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** UNVERIFIED.

**Переменные, размерности и область:** settled money; global namespace,all allocations complete; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Две allocations50 одного source50 локально допустимы по отдельности, глобально100>50. Нужны complete registry и immutable source receipts, не только сумма одного DTO.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-033, HSBI-A03-ERR-017; HSBI-A03-IMP-004, HSBI-A03-IMP-009. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-018 |
| 2 Exact normative source | Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md:3 |
| 3 Expression | sum funding per source<=EligibleSourceNet |
| 4 Variables | s — logical source; Gj(s) — все grants источника; N(s) — eligible settled amount |
| 5 Dimensions | settled money |
| 6 Domain | settled money; global namespace,all allocations complete. |
| 7 Required assumptions | settled money; global namespace,all allocations complete. Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | Две allocations50 одного source50 локально допустимы по отдельности, глобально100>50. Нужны complete registry и immutable source receipts, не только сумма одного DTO. |
| 9 Far BUY / Far SELL | NOT_APPLICABLE напрямую: сумма funding одного logical source across roles/cycles. |
| 10 Broker grid / rounding | Все grants и eligible source amount в одном settled domain, global complete inventory. |
| 11 Bid / Ask / costs | Неучтённый account debit/negative other deal не исчезает из глобального капитала. |
| 12 Partial fills / actual data | Каждое allocation/funding event unique and atomic; restart не делает source новым. |
| 13 Production mapping | Include/Money/HSBI_ReserveAllocationTypes.mqh:23 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-033, HSBI-A03-ERR-017; HSBI-A03-IMP-004, HSBI-A03-IMP-009. |
| 15 Final statuses | MATH=UNVERIFIED; IMPLEMENTATION=NOT_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-019 — Consumption bound to authoritative remaining allocation

**Источник правила:** `Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md:5-7`. **Production операция/строки:** `Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:44-47,63-70`; mapping **MISMATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** UNVERIFIED.

**Переменные, размерности и область:** source/allocation/event/policy/revision,money; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Nonempty foreign key не связан с actual allocation. Source50 consumed50 больше не может дать reserve40. Текущее preview разрешение не является фактическим ledger debit.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-007, HSBI-A03-ERR-008; HSBI-A03-IMP-004. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-019 |
| 2 Exact normative source | Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md:5-7 |
| 3 Expression | Consumption bound to authoritative remaining allocation |
| 4 Variables | grant/source/allocation/owner/event/revision — независимые ключи; d — debit; Ff — authoritative Free |
| 5 Dimensions | source/allocation/event/policy/revision,money. |
| 6 Domain | source/allocation/event/policy/revision,money. |
| 7 Required assumptions | source/allocation/event/policy/revision,money. Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | Nonempty foreign key не связан с actual allocation. Source50 consumed50 больше не может дать reserve40. Текущее preview разрешение не является фактическим ledger debit. |
| 9 Far BUY / Far SELL | NOT_APPLICABLE к ledger binding; use-purpose/role independently validated. |
| 10 Broker grid / rounding | Authoritative remaining Free/owner reservation по source/allocation/policy/revision в точных money units. |
| 11 Bid / Ask / costs | Actual source income не равен amount permitted конкретному consumer; costs не создают resource. |
| 12 Partial fills / actual data | Любой partial consume пишет receipt/deltas; flags/new event не возвращают exhausted grant. |
| 13 Production mapping | Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:44-47,63-70 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-007, HSBI-A03-ERR-008; HSBI-A03-IMP-004. |
| 15 Final statuses | MATH=UNVERIFIED; IMPLEMENTATION=IMPLEMENTED_MISMATCH; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-020 — AbsoluteFarLoss=max(0,-ProjectedCloseNowFarNet)

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:15`. **Production операция/строки:** `Include/Money/HSBI_BasketMoneyEvaluator.mqh:17`; mapping **MATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money; full position,close side,current volume; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Для net-50 magnitude50, для+10 magnitude0. Это current liquidation estimate, не гарантированный будущий execution loss; название increase не меняет absolute смысл.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-043; HSBI-A03-IMP-010. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-020 |
| 2 Exact normative source | Docs/04_MATHEMATICAL_MODEL_RU.md:15 |
| 3 Expression | AbsoluteFarLoss=max(0,-ProjectedCloseNowFarNet) |
| 4 Variables | Nfar — projected close-now net полного Far; L=max(0,−Nfar) — absolute loss magnitude |
| 5 Dimensions | money |
| 6 Domain | money; full position,close side,current volume. |
| 7 Required assumptions | money; full position,close side,current volume. Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | Для net-50 magnitude50, для+10 magnitude0. Это current liquidation estimate, не гарантированный будущий execution loss; название increase не меняет absolute смысл. |
| 9 Far BUY / Far SELL | BUY Far loss рассчитывается по Bid, SELL по Ask. |
| 10 Broker grid / rounding | Actual Far lot и currency precision заданы; unknown rounding/basis не нулевой loss. |
| 11 Bid / Ask / costs | CloseNow включает применимые exit costs ровно один раз; absolute не incremental. |
| 12 Partial fills / actual data | Partial close меняет actual остаток и базис; прежний full loss не переносится без recalculation. |
| 13 Production mapping | Include/Money/HSBI_BasketMoneyEvaluator.mqh:17 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-043; HSBI-A03-IMP-010. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=IMPLEMENTED_MATCH; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-021 — IncrementalLoss=AbsoluteLoss-BaselineLoss

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:15`. **Production операция/строки:** `Include/Money/HSBI_BasketMoneyEvaluator.mqh:17`; mapping **AMBIGUOUS**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** UNDEFINED.

**Переменные, размерности и область:** money; same source,volume,basis,time contract; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** 50-40=10,но Reserve30 покрывает10,не50. Без stable baseline/volume change/restart contract incremental не взаимозаменяем с absolute. Loss magnitude и signed delta разные типы.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-043; HSBI-A03-IMP-010. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-021 |
| 2 Exact normative source | Docs/04_MATHEMATICAL_MODEL_RU.md:15 |
| 3 Expression | IncrementalLoss=AbsoluteLoss-BaselineLoss |
| 4 Variables | La — current absolute loss; L0 — independently defined baseline loss; ΔL=La−L0 — signed diagnostic delta |
| 5 Dimensions | money |
| 6 Domain | money; same source,volume,basis,time contract. |
| 7 Required assumptions | money; same source,volume,basis,time contract. Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | 50-40=10,но Reserve30 покрывает10,не50. Без stable baseline/volume change/restart contract incremental не взаимозаменяем с absolute. Loss magnitude и signed delta разные типы. |
| 9 Far BUY / Far SELL | Baseline/Current сравнивают одну сторону/источник/остаток в обоих зеркалах. |
| 10 Broker grid / rounding | Volume change и posting scale должны входить baseline contract. |
| 11 Bid / Ask / costs | Разность signed loss diagnostic не заменяет absolute coverage; buffers на одном basis. |
| 12 Partial fills / actual data | Partial execution/restart без сохранённого baseline→UNAVAILABLE, не guessed delta. |
| 13 Production mapping | Include/Money/HSBI_BasketMoneyEvaluator.mqh:17 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-043; HSBI-A03-IMP-010. |
| 15 Final statuses | MATH=UNDEFINED; IMPLEMENTATION=CALLER_NOT_VERIFIED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-022 — CatchUpMargin=EligibleReserve-Loss-Buffer>0

**Источник правила:** `Docs/24_BROKER_MONEY_MODEL_RU.md:9`. **Production операция/строки:** `Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:74-75`; mapping **PARTIALLY_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money; finite R,L,B>=0 and reconciled funds; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** 50-20-1=29; equality margin0 недостаточно при strict>. Если R projected, вывод только preview. Не доказывает finance/actual closing capacity.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-033, HSBI-A03-ERR-043; HSBI-A03-IMP-004, HSBI-A03-IMP-010. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-022 |
| 2 Exact normative source | Docs/24_BROKER_MONEY_MODEL_RU.md:9 |
| 3 Expression | CatchUpMargin=EligibleReserve-Loss-Buffer>0 |
| 4 Variables | Ri — eligible reserve, Li — loss на согласованном basis, Bi — additional buffer; Mi=Ri−Li−Bi |
| 5 Dimensions | money |
| 6 Domain | money; finite R,L,B>=0 and reconciled funds. |
| 7 Required assumptions | money; finite R,L,B>=0 and reconciled funds. Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | 50-20-1=29; equality margin0 недостаточно при strict>. Если R projected, вывод только preview. Не доказывает finance/actual closing capacity. |
| 9 Far BUY / Far SELL | Расчёт Mi использует соответствующий BUY/Bid/SELL/Ask Far loss. |
| 10 Broker grid / rounding | Amount proof и scalar должны совпадать на одной monetary grid. |
| 11 Bid / Ask / costs | Buffer disjoint с уже учтёнными costs; Ri confirmed/eligible или явно projected preview. |
| 12 Partial fills / actual data | После debit/partial fill обновить Ri/Li; два альтернативных preview не два consumption. |
| 13 Production mapping | Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:74-75 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-033, HSBI-A03-ERR-043; HSBI-A03-IMP-004, HSBI-A03-IMP-010. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=PARTIALLY_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-023 — min_i CatchUpMargin_i>0 vs argmax TransitionLoss

**Источник правила:** `Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md:5`. **Production операция/строки:** `Include/Planning/HSBI_FutureSmallProofAggregator.mqh:44,50`; mapping **AMBIGUOUS**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** UNDEFINED.

**Переменные, размерности и область:** money indexed by mandatory alternative levels; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Формальная all-level конъюнкция эквивалентна положительному минимуму конечного непустого набора, но выбор этого scope pending CR09. Trans10/M9 vsTrans5/M-11 опровергает замену минимума argmax другой функции.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-018; HSBI-A03-IMP-010. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-023 |
| 2 Exact normative source | Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md:5 |
| 3 Expression | min_i CatchUpMargin_i>0 vs argmax TransitionLoss |
| 4 Variables | I — непустой required level set; Mi — CatchUpMargin; Ti — TransitionLoss; j=argmax Ti |
| 5 Dimensions | money indexed by mandatory alternative levels. |
| 6 Domain | money indexed by mandatory alternative levels. |
| 7 Required assumptions | money indexed by mandatory alternative levels. Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | Формальная all-level конъюнкция эквивалентна положительному минимуму конечного непустого набора, но выбор этого scope pending CR09. Trans10/M9 vsTrans5/M-11 опровергает замену минимума argmax другой функции. |
| 9 Far BUY / Far SELL | Каждый обязательный уровень проверяется с корректной зеркальной close side. |
| 10 Broker grid / rounding | Все required levels и grid-normalized lots заданы независимо. |
| 11 Bid / Ask / costs | Уровень max TransitionLoss не обязан давать min Reserve−Loss−Buffer. |
| 12 Partial fills / actual data | Future levels — альтернативные прогнозы; actual последовательные расходы обновляют один ledger. |
| 13 Production mapping | Include/Planning/HSBI_FutureSmallProofAggregator.mqh:44,50 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-018; HSBI-A03-IMP-010. |
| 15 Final statuses | MATH=UNDEFINED; IMPLEMENTATION=CALLER_NOT_VERIFIED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-024 — CurrentTransitionLoss=max(0,-sum signed actual fills)

**Источник правила:** `Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md:9`. **Production операция/строки:** `Include/Money/HSBI_BasketMoneyEvaluator.mqh:17`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money; ordered confirmed same-batch fills; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** После -15,+100 signed sum85,currentloss0. Projected basket net не является authoritative actual transition batch. Membership/account/fees должны быть подтверждены отдельно.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-035, HSBI-A03-ERR-033; HSBI-A03-IMP-019, HSBI-A03-IMP-004. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-024 |
| 2 Exact normative source | Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md:9 |
| 3 Expression | CurrentTransitionLoss=max(0,-sum signed actual fills) |
| 4 Variables | nj — signed confirmed closing net fill j; Lt=max(0,−Σj≤t nj) |
| 5 Dimensions | money |
| 6 Domain | money; ordered confirmed same-batch fills. |
| 7 Required assumptions | money; ordered confirmed same-batch fills. Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | После -15,+100 signed sum85,currentloss0. Projected basket net не является authoritative actual transition batch. Membership/account/fees должны быть подтверждены отдельно. |
| 9 Far BUY / Far SELL | Signed net каждой BUY/SELL closing deal отражает фактический результат. |
| 10 Broker grid / rounding | Actual fill volume/posted net по объявленному broker domain. |
| 11 Bid / Ask / costs | Profit/Swap/Commission/Fee по одному разу, source membership independently verified. |
| 12 Partial fills / actual data | Current loss считается на каждом подтверждённом prefix; последний положительный fill не стирает прошлый breach. |
| 13 Production mapping | Include/Money/HSBI_BasketMoneyEvaluator.mqh:17 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-035, HSBI-A03-ERR-033; HSBI-A03-IMP-019, HSBI-A03-IMP-004. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=NOT_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-025 — Sticky breach / Peak loss policies

**Источник правила:** `Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md:20`. **Production операция/строки:** `LINE_NOT_VERIFIED`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** UNDEFINED.

**Переменные, размерности и область:** money,time/batch,reset policy; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Current loss15→0; peak15→15; breach cap12 true→true. Это разные функции истории. Не выбирать одну без владельца; отсутствие полной history означает UNAVAILABLE.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-035; HSBI-A03-IMP-019. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-025 |
| 2 Exact normative source | Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md:20 |
| 3 Expression | Sticky breach / Peak loss policies |
| 4 Variables | nj — ordered fills; Lt — current loss; Ht=maxs≤t Ls; Bt — historical breach flag; cap/reset policy |
| 5 Dimensions | money,time/batch,reset policy. |
| 6 Domain | money,time/batch,reset policy. |
| 7 Required assumptions | money,time/batch,reset policy. Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | Current loss15→0; peak15→15; breach cap12 true→true. Это разные функции истории. Не выбирать одну без владельца; отсутствие полной history означает UNAVAILABLE. |
| 9 Far BUY / Far SELL | В обоих зеркалах политика зависит от signed экономической истории, не от названия роли. |
| 10 Broker grid / rounding | Exact confirmed ordered fills, history/reset identity; grid сам историю не восстанавливает. |
| 11 Bid / Ask / costs | Costs включены в каждый actual net; UNKNOWN expense/history не текущий0. |
| 12 Partial fills / actual data | [-15,+100] даёт current15→0,peak15→15,stickytrue→true; reset требует решения. |
| 13 Production mapping | NOT_FOUND complete production operation; old locator retained above for history |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-035; HSBI-A03-IMP-019. |
| 15 Final statuses | MATH=UNDEFINED; IMPLEMENTATION=NOT_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-026 — AllowedLoss=min(absolute,equity,oldrisk,cumulative caps)

**Источник правила:** `Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:15`. **Production операция/строки:** `Include/Planning/HSBI_NewFarSolver.mqh:74`; mapping **PARTIALLY_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money; all finite known same horizon; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Условие L<=каждого cap равносильно L<=min caps. Equity percent сначала переводится в money. NaN/unknown cap не безопасный ноль и не допустимый минимум.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-009, HSBI-A03-ERR-035; HSBI-A03-IMP-005, HSBI-A03-IMP-019. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-026 |
| 2 Exact normative source | Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:15 |
| 3 Expression | AllowedLoss=min(absolute,equity,oldrisk,cumulative caps) |
| 4 Variables | L — assessed transition loss; A,E,O,C — absolute/equity-money/old-risk-money/cumulative-money caps |
| 5 Dimensions | money |
| 6 Domain | money; all finite known same horizon. |
| 7 Required assumptions | money; all finite known same horizon. Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | Условие L<=каждого cap равносильно L<=min caps. Equity percent сначала переводится в money. NaN/unknown cap не безопасный ноль и не допустимый минимум. |
| 9 Far BUY / Far SELL | Капы одной money-loss модели для BUY/SELL с соответствующим adverse side. |
| 10 Broker grid / rounding | Percent сначала /100 и умножить на equity/risk money; signed64/intermediate checks отдельно. |
| 11 Bid / Ask / costs | Все четыре cap finite,nonnegative,same horizon; unknown cap не minimum safe0. |
| 12 Partial fills / actual data | Cap проверять по выбранной current/peak/sticky policy и каждому применимому prefix. |
| 13 Production mapping | Include/Planning/HSBI_NewFarSolver.mqh:74 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-009, HSBI-A03-ERR-035; HSBI-A03-IMP-005, HSBI-A03-IMP-019. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=PARTIALLY_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-027 — CompressionLots=F-N; ratio=(F-N)/F

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:21`. **Production операция/строки:** `Include/Planning/HSBI_NewFarSolver.mqh:111`; mapping **MATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** lot and dimensionless; F>0,0<N<F; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** F1,N.6 дают.4lot и.4ratio. Формула определена только при положительном F и actual/planned scope не смешивается.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-045; HSBI-A03-IMP-011. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-027 |
| 2 Exact normative source | Docs/04_MATHEMATICAL_MODEL_RU.md:21 |
| 3 Expression | CompressionLots=F-N; ratio=(F-N)/F |
| 4 Variables | F>0 — old Far lot; N — candidate/actual residual lot; ΔV=F−N; c=ΔV/F |
| 5 Dimensions | lot and dimensionless |
| 6 Domain | lot and dimensionless; F>0,0<N<F. |
| 7 Required assumptions | lot and dimensionless; F>0,0<N<F. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | F1,N.6 дают.4lot и.4ratio. Формула определена только при положительном F и actual/planned scope не смешивается. |
| 9 Far BUY / Far SELL | Сторона NewFar противоположна старому Far как actual original Core residual. |
| 10 Broker grid / rounding | F,N — post-round lots; F−N lot, отношение безразмерно; F>0. |
| 11 Bid / Ask / costs | Compression не денежная прибыль; execution costs и risk могут ухудшиться. |
| 12 Partial fills / actual data | Selected N не actual residual; actual reduction/fills должны быть reconciled. |
| 13 Production mapping | Include/Planning/HSBI_NewFarSolver.mqh:111 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-045; HSBI-A03-IMP-011. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=IMPLEMENTED_MATCH; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-028 — N<=MaximumNewFarRatio*F

**Источник правила:** `Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:13`. **Production операция/строки:** `Include/Planning/HSBI_NewFarSolver.mqh:112`; mapping **MATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** lot; ratio in(0,1),post-round values; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Умножение не меняет размерность. Это отдельное ограничение не доказывает цену/стоимость/feasible next basket. Кандидат выше actual Core residual не promotion.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-045, HSBI-A03-ERR-032; HSBI-A03-IMP-011, HSBI-A03-IMP-013. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-028 |
| 2 Exact normative source | Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:13 |
| 3 Expression | N<=MaximumNewFarRatio*F |
| 4 Variables | F — old Far; N — next Far; qmax∈(0,1) — maximum ratio |
| 5 Dimensions | lot |
| 6 Domain | lot; ratio in(0,1),post-round values. |
| 7 Required assumptions | lot; ratio in(0,1),post-round values. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | Умножение не меняет размерность. Это отдельное ограничение не доказывает цену/стоимость/feasible next basket. Кандидат выше actual Core residual не promotion. |
| 9 Far BUY / Far SELL | Volume ratio одинаков по модулю в обоих направлениях. |
| 10 Broker grid / rounding | N≤qmaxF после normalization; округление/min lot может сделать множество пустым. |
| 11 Bid / Ask / costs | Ratio cap не доказывает account margin/price/cost feasibility. |
| 12 Partial fills / actual data | Фактический residual должен удовлетворять этому же bound, не только planned candidate. |
| 13 Production mapping | Include/Planning/HSBI_NewFarSolver.mqh:112 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-045, HSBI-A03-ERR-032; HSBI-A03-IMP-011, HSBI-A03-IMP-013. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=IMPLEMENTED_MATCH; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-029 — NextBigGross<OldBigGross

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:21`. **Production операция/строки:** `Include/Planning/HSBI_FutureSmallSolver.mqh:90,143`; mapping **MISMATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** lot; same Big-leg set; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Next C.7,T.5,S1 givesBigGross1.2,Net.2; oldGross1. Net comparison проходит, требуемый gross нет. Один тип lot не делает величины экономически тождественными.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-020; HSBI-A03-IMP-012. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-029 |
| 2 Exact normative source | Docs/04_MATHEMATICAL_MODEL_RU.md:21 |
| 3 Expression | NextBigGross<OldBigGross |
| 4 Variables | Cnext,Tnext — next Big legs; Gold — old C+T; Gnext=Cnext+Tnext; Snext не вычитается из Gross |
| 5 Dimensions | lot |
| 6 Domain | lot; same Big-leg set. |
| 7 Required assumptions | lot; same Big-leg set. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | Next C.7,T.5,S1 givesBigGross1.2,Net.2; oldGross1. Net comparison проходит, требуемый gross нет. Один тип lot не делает величины экономически тождественными. |
| 9 Far BUY / Far SELL | BigGross=C+T одинаков по модулю при зеркале; Net меняет знак. |
| 10 Broker grid / rounding | Сравнивать одинаковые Big-role sets после округления. |
| 11 Bid / Ask / costs | Снижение gross lot не гарантирует снижение money risk/cost при другом basis. |
| 12 Partial fills / actual data | Actual next legs отдельно подтверждаются; planned gross не учёт исполненных позиций. |
| 13 Production mapping | Include/Planning/HSBI_FutureSmallSolver.mqh:90,143 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-020; HSBI-A03-IMP-012. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=IMPLEMENTED_MISMATCH; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-030 — Gross=sum abs volumes; Net=sum signed volumes

**Источник правила:** `Docs/01_GLOSSARY_AND_DIMENSIONS_RU.md:1-56`. **Production операция/строки:** `Include/Money/HSBI_BasketMoneyEvaluator.mqh:17`; mapping **MATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** lot; actual same-symbol direction; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** BUY2.2,SELL1.5 даютGross3.7,Net+.7. При зеркале Gross тот же,Net-.7. Margin и risk не определяются одним Net.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-020, HSBI-A03-ERR-041; HSBI-A03-IMP-012, HSBI-A03-IMP-022. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-030 |
| 2 Exact normative source | Docs/01_GLOSSARY_AND_DIMENSIONS_RU.md:1-56 |
| 3 Expression | Gross=sum abs volumes; Net=sum signed volumes |
| 4 Variables | vj — nonnegative position lot; sj∈{−1,+1} — direction; Gross=Σvj; Net=Σsjvj |
| 5 Dimensions | lot |
| 6 Domain | lot; actual same-symbol direction. |
| 7 Required assumptions | lot; actual same-symbol direction. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | BUY2.2,SELL1.5 даютGross3.7,Net+.7. При зеркале Gross тот же,Net-.7. Margin и risk не определяются одним Net. |
| 9 Far BUY / Far SELL | BUY signs+1,SELL−1; зеркало меняет Net на−Net, Gross неизменен. |
| 10 Broker grid / rounding | Суммируются actual или явно planned lots одного symbol/domain, не смешивать профили. |
| 11 Bid / Ask / costs | Lots не money/margin; отсутствие hedge может увеличить денежный prefix risk. |
| 12 Partial fills / actual data | Каждый partial close вычитает фактическую signed volume закрытой ноги. |
| 13 Production mapping | Include/Money/HSBI_BasketMoneyEvaluator.mqh:17 (Gross); Include/Planning/HSBI_GeometrySolver.mqh:10,34 (signed Net) |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-020, HSBI-A03-ERR-041; HSBI-A03-IMP-012, HSBI-A03-IMP-022. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=PARTIALLY_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-031 — RiskNext<RiskOld-Tolerance

**Источник правила:** `Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:12`. **Production операция/строки:** `Include/Risk/HSBI_FutureSmallRiskEvaluator.mqh:29-50`; mapping **NOT_VERIFIED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** UNVERIFIED.

**Переменные, размерности и область:** money/risk unit; same adverse basis and horizon; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Неравенство осмысленно лишь для одинаковой модели. Уменьшение lot не доказывает уменьшение loss при новом basis/volatility/entry. Нужна независимая risk authority, не copied snapshot flag.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-037, HSBI-A03-ERR-038; HSBI-A03-IMP-021. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-031 |
| 2 Exact normative source | Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:12 |
| 3 Expression | RiskNext<RiskOld-Tolerance |
| 4 Variables | Ro,Rn — losses under same adverse control price/basis; τ≥0 — risk tolerance |
| 5 Dimensions | money/risk unit |
| 6 Domain | money/risk unit; same adverse basis and horizon. |
| 7 Required assumptions | money/risk unit; same adverse basis and horizon. Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | Неравенство осмысленно лишь для одинаковой модели. Уменьшение lot не доказывает уменьшение loss при новом basis/volatility/entry. Нужна независимая risk authority, не copied snapshot flag. |
| 9 Far BUY / Far SELL | Одна adverse control basis, соответствующая BUY/SELL и asymmetric ticks. |
| 10 Broker grid / rounding | Actual/planned lots нормализованы; tolerance money, не lot. |
| 11 Bid / Ask / costs | Все applicable costs/FX/horizon независимы и согласованы; иначе risk incomparable. |
| 12 Partial fills / actual data | После partial каждого irreversible шага risk заново; endpoint comparison недостаточно. |
| 13 Production mapping | Include/Risk/HSBI_FutureSmallRiskEvaluator.mqh:29-50 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-037, HSBI-A03-ERR-038; HSBI-A03-IMP-021. |
| 15 Final statuses | MATH=UNVERIFIED; IMPLEMENTATION=CALLER_NOT_VERIFIED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-032 — TotalAccountMargin=sum standalone leg margins

**Источник правила:** `Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:9`. **Production операция/строки:** `Include/Money/HSBI_BasketMoneyEvaluator.mqh:17`; mapping **PARTIALLY_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** UNVERIFIED.

**Переменные, размерности и область:** account money; hedging/tiers/other positions; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Равенство не теорема для любого broker. Сумма независимых OrderCalcMargin может быть estimator; required margin whole-account и max prefix должны иметь иной доказанный контракт.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-034; HSBI-A03-IMP-015. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-032 |
| 2 Exact normative source | Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:9 |
| 3 Expression | TotalAccountMargin=sum standalone leg margins |
| 4 Variables | mj — standalone OrderCalcMargin leg; Maccount — portfolio/account required margin |
| 5 Dimensions | account money |
| 6 Domain | account money; hedging/tiers/other positions. |
| 7 Required assumptions | account money; hedging/tiers/other positions. Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | Равенство не теорема для любого broker. Сумма независимых OrderCalcMargin может быть estimator; required margin whole-account и max prefix должны иметь иной доказанный контракт. |
| 9 Far BUY / Far SELL | BUY/SELL hedging/netting может менять margin policy; не универсальная аддитивность. |
| 10 Broker grid / rounding | Lot tiers,grid,account mode влияют на account margin; same unit money не same meaning. |
| 11 Bid / Ask / costs | Standalone OrderCalcMargin sums не учитывают автоматически whole-account offsets/tiers. |
| 12 Partial fills / actual data | Prefix/partial exposure может требовать больше margin, чем конечный portfolio. |
| 13 Production mapping | Include/Money/HSBI_BasketMoneyEvaluator.mqh:17 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-034; HSBI-A03-IMP-015. |
| 15 Final statuses | MATH=UNVERIFIED; IMPLEMENTATION=PARTIALLY_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-033 — MarginLevel=100*Equity/Margin

**Источник правила:** `Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:6`. **Production операция/строки:** `LINE_NOT_VERIFIED`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** percent; Margin>0,same currency; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Отношение однородных money безразмерно, множитель100 даёт%. При Margin0 формула не определена: нужна broker/account convention. Stopout/negative equity не игнорируются.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-034; HSBI-A03-IMP-015. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-033 |
| 2 Exact normative source | Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:6 |
| 3 Expression | MarginLevel=100*Equity/Margin |
| 4 Variables | E — account equity; M>0 — used margin; ML — margin level percent |
| 5 Dimensions | percent |
| 6 Domain | percent; Margin>0,same currency. |
| 7 Required assumptions | percent; Margin>0,same currency. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | Отношение однородных money безразмерно, множитель100 даёт%. При Margin0 формула не определена: нужна broker/account convention. Stopout/negative equity не игнорируются. |
| 9 Far BUY / Far SELL | NOT_APPLICABLE: account-level money ratio, не направление одной позиции. |
| 10 Broker grid / rounding | M>0; M=0 требует отдельной broker convention, division не определена. |
| 11 Bid / Ask / costs | Equity и used margin берутся на одном account snapshot/currency, charges не добавлять дважды. |
| 12 Partial fills / actual data | Partial fills меняют E/M; старый ML не permission следующего action. |
| 13 Production mapping | NOT_FOUND complete production operation; old locator retained above for history |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-034; HSBI-A03-IMP-015. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=NOT_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-034 — Equity=Balance+FloatingNet

**Источник правила:** `Docs/01_GLOSSARY_AND_DIMENSIONS_RU.md:1-56`. **Production операция/строки:** `LINE_NOT_VERIFIED`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money; broker-consistent accrued charge basis; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Реализация прибыли переводит floating в balance, не создавая equity. Balance1000,realized+10,floating-20 даёт equity990, несмотря на рост Balance до1010. Credit/charges требуют account mapping.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-036; HSBI-A03-IMP-020. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-034 |
| 2 Exact normative source | Docs/01_GLOSSARY_AND_DIMENSIONS_RU.md:1-56 |
| 3 Expression | Equity=Balance+FloatingNet |
| 4 Variables | B — account balance; U — broker-consistent floating/accrued net; E — account equity |
| 5 Dimensions | money |
| 6 Domain | money; broker-consistent accrued charge basis. |
| 7 Required assumptions | money; broker-consistent accrued charge basis. Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | Реализация прибыли переводит floating в balance, не создавая equity. Balance1000,realized+10,floating-20 даёт equity990, несмотря на рост Balance до1010. Credit/charges требуют account mapping. |
| 9 Far BUY / Far SELL | Все BUY/SELL floating учитываются с правильным знаком и broker quote basis. |
| 10 Broker grid / rounding | Currency/account basis едины; monetary precision и credit mapping explicit. |
| 11 Bid / Ask / costs | Аккумулированные charges/credit входят согласно broker accounting boundary. |
| 12 Partial fills / actual data | Realize переносит сумму floating→balance; само по себе не увеличивает Equity. |
| 13 Production mapping | NOT_FOUND complete production operation; old locator retained above for history |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-036; HSBI-A03-IMP-020. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=NOT_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-035 — EconomicCyclePnL=AllRealized+OpenLiquidationNet

**Источник правила:** `Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md:20; Docs/04_MATHEMATICAL_MODEL_RU.md:18`. **Production операция/строки:** `Include/Money/HSBI_MoneyTypes.mqh:9`; mapping **AMBIGUOUS**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money; common cycle start,disjoint costs; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Partition по закрытым/открытым cash flows: Harvest10 и remaining net-20 даютCycle-10. InitialProfit exclusion меняет метрику, не полную экономику. Reserve не третий доход.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-036, HSBI-A03-ERR-022; HSBI-A03-IMP-020, HSBI-A03-IMP-014. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-035 |
| 2 Exact normative source | Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md:20; Docs/04_MATHEMATICAL_MODEL_RU.md:18 |
| 3 Expression | EconomicCyclePnL=AllRealized+OpenLiquidationNet |
| 4 Variables | Rall — все realized flows после economic cycle start; Ui — remaining liquidation net; Π — full cycle PnL |
| 5 Dimensions | money |
| 6 Domain | money; common cycle start,disjoint costs. |
| 7 Required assumptions | money; common cycle start,disjoint costs. Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | Partition по закрытым/открытым cash flows: Harvest10 и remaining net-20 даютCycle-10. InitialProfit exclusion меняет метрику, не полную экономику. Reserve не третий доход. |
| 9 Far BUY / Far SELL | Все actual realised и remaining BUY/Bid/SELL/Ask включены за один cycle boundary. |
| 10 Broker grid / rounding | Остатки по actual volume, единый scale; InitialProfit exclusion меняет metric. |
| 11 Bid / Ask / costs | Harvest/Reserve не дополнительный доход; все opening/closing/holding costs однократно. |
| 12 Partial fills / actual data | После partial partition закрытых/открытых cash flows обновляется, неизвестные facts блокируют proof. |
| 13 Production mapping | Include/Money/HSBI_MoneyTypes.mqh:9 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-036, HSBI-A03-ERR-022; HSBI-A03-IMP-020, HSBI-A03-IMP-014. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=CALLER_NOT_VERIFIED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-036 — Nonfinite/unknown cannot pass money/risk/outcome gate

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:42`. **Production операция/строки:** `Include/Risk/HSBI_RiskGateResult.mqh:6; Include/Execution/HSBI_TransactionTypes.mqh:15`; mapping **MISMATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** finite typed DTO domain; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Ordered comparison с NaN не является доказательством диапазона. Предварительный finite/domain guard необходим до суммы, разности и выбора min/max.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-009, HSBI-A03-ERR-010, HSBI-A03-ERR-011; HSBI-A03-IMP-005. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-036 |
| 2 Exact normative source | Docs/04_MATHEMATICAL_MODEL_RU.md:42 |
| 3 Expression | Nonfinite/unknown cannot pass money/risk/outcome gate |
| 4 Variables | x — внешнее числовое поле; Domain(x) — точный тип/finite/range/unit; unavailable — отсутствие authority |
| 5 Dimensions | finite typed DTO domain. |
| 6 Domain | finite typed DTO domain. |
| 7 Required assumptions | finite typed DTO domain. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | Ordered comparison с NaN не является доказательством диапазона. Предварительный finite/domain guard необходим до суммы, разности и выбора min/max. |
| 9 Far BUY / Far SELL | Domain validation независимо от направления; BUY/SELL затем проверяется closed enum. |
| 10 Broker grid / rounding | Finite до суммы/division/grid; у каждого типа свой range, bool не integer. |
| 11 Bid / Ask / costs | Неизвестный expense/NaN не safe0; signed commissions остаются допустимы. |
| 12 Partial fills / actual data | Не finite actual fill не подтверждается; ошибка не должна менять balances/journal. |
| 13 Production mapping | Include/Risk/HSBI_RiskGateResult.mqh:6; Include/Execution/HSBI_TransactionTypes.mqh:15 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-009, HSBI-A03-ERR-010, HSBI-A03-ERR-011; HSBI-A03-IMP-005. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=IMPLEMENTED_MISMATCH; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-037 — K>=ceil(log(Vmin/F0)/log(q))

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:36`. **Production операция/строки:** `Include/Planning/HSBI_FutureSmallSolver.mqh:5-10`; mapping **PARTIALLY_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** steps; F0>=Vmin>0,0<q<1; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Из q^K*F0<=Vmin, после деления на logq<0 знак меняется: K>=log(Vmin/F0)/logq. Ceil даёт sufficient integer bound при uniform rounded contraction. step должен входить в discrete feasibility, не только в input shape.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-032, HSBI-A03-ERR-031; HSBI-A03-IMP-013. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-037 |
| 2 Exact normative source | Docs/04_MATHEMATICAL_MODEL_RU.md:36 |
| 3 Expression | K>=ceil(log(Vmin/F0)/log(q)) |
| 4 Variables | F0≥Vmin>0 — initial/min lot; q∈(0,1) — uniform contraction; k — число successful reductions |
| 5 Dimensions | steps |
| 6 Domain | steps; F0>=Vmin>0,0<q<1. |
| 7 Required assumptions | steps; F0>=Vmin>0,0<q<1. Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | Из q^K*F0<=Vmin, после деления на logq<0 знак меняется: K>=log(Vmin/F0)/logq. Ceil даёт sufficient integer bound при uniform rounded contraction. step должен входить в discrete feasibility, не только в input shape. |
| 9 Far BUY / Far SELL | NOT_APPLICABLE к доказательству числа reductions; каждый фактический цикл всё равно зеркально валиден. |
| 10 Broker grid / rounding | Uniform contraction обязана сохраняться после grid; Vmin>0 остаётся открытым lot. |
| 11 Bid / Ask / costs | K не time/cost/margin guarantee; ожидание и carry не ограничены этой формулой. |
| 12 Partial fills / actual data | Теорема о successful completed steps, не о число requests/partial/timeout. |
| 13 Production mapping | Include/Planning/HSBI_FutureSmallSolver.mqh:5-10 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-032, HSBI-A03-ERR-031; HSBI-A03-IMP-013. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=PARTIALLY_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-038 — Finite prefix implies uniform geometric future bound

**Источник правила:** `Docs/27_FUTURE_SMALL_SOLVER_RU.md:5`. **Production операция/строки:** `Include/Planning/HSBI_FutureSmallSolver.mqh:12-16,146-147`; mapping **MISMATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** INVALID.

**Переменные, размерности и область:** quantifier over all future reachable levels; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Импликация без invariant assumptions ложна:1,.8,.64 согласованы сq.8,но следующий.64>.512. Требование uniform assumptions в документе корректно; invalid именно попытка вывести forall из конечного наблюдения.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-021; HSBI-A03-IMP-013. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-038 |
| 2 Exact normative source | Docs/27_FUTURE_SMALL_SOLVER_RU.md:5 |
| 3 Expression | Finite prefix implies uniform geometric future bound |
| 4 Variables | F0…Fn — конечный observed prefix; q — proposed bound; universal tail — все последующие Fj |
| 5 Dimensions | quantifier over all future reachable levels. |
| 6 Domain | quantifier over all future reachable levels. |
| 7 Required assumptions | quantifier over all future reachable levels. Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | Импликация без invariant assumptions ложна:1,.8,.64 согласованы сq.8,но следующий.64>.512. Требование uniform assumptions в документе корректно; invalid именно попытка вывести forall из конечного наблюдения. |
| 9 Far BUY / Far SELL | Контрпример prefix→tail не зависит от BUY/SELL направления. |
| 10 Broker grid / rounding | Grid допускает plateau; finitely many observations не universally invariant domain. |
| 11 Bid / Ask / costs | Finite cost/margin/risk flags не доказывают все будущие значения. |
| 12 Partial fills / actual data | Наблюдённые completed transitions не доказывают существование/исполнение следующего. |
| 13 Production mapping | Include/Planning/HSBI_FutureSmallSolver.mqh:12-16,146-147 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-021; HSBI-A03-IMP-013. |
| 15 Final statuses | MATH=FALSE; IMPLEMENTATION=IMPLEMENTED_MISMATCH; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-039 — RecoveryMoney(P+tick)>RecoveryMoney(P) both mirrors

**Источник правила:** `Docs/03_FULL_SYSTEM_MANUAL_RU.md:12; Docs/26_GEOMETRY_ENGINE_SPECIFICATION_RU.md:7`. **Production операция/строки:** `Include/Planning/HSBI_GeometrySolver.mqh:12-19`; mapping **AMBIGUOUS**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** CONTRADICTORY.

**Переменные, размерности и область:** money; finite price on tick grid; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** FarBUY зеркало требует P-tick. Положительный D не меняет эту направленность. Одна пара цен не доказывает весь диапазон и все stress paths.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-046, HSBI-A03-ERR-037; HSBI-A03-IMP-007, HSBI-A03-IMP-021. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-039 |
| 2 Exact normative source | Docs/03_FULL_SYSTEM_MANUAL_RU.md:12; Docs/26_GEOMETRY_ENGINE_SPECIFICATION_RU.md:7 |
| 3 Expression | RecoveryMoney(P+tick)>RecoveryMoney(P) both mirrors |
| 4 Variables | Π(P) — recovery money at price P; tick>0 — price increment; Far direction — BUY/SELL |
| 5 Dimensions | money |
| 6 Domain | money; finite price on tick grid. |
| 7 Required assumptions | money; finite price on tick grid. Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | FarBUY зеркало требует P-tick. Положительный D не меняет эту направленность. Одна пара цен не доказывает весь диапазон и все stress paths. |
| 9 Far BUY / Far SELL | При Far BUY правильный next favorable price=P−tick, при SELL=P+tick. |
| 10 Broker grid / rounding | Две on-tick цены не range-wide proof; grid direction нужно задавать явно. |
| 11 Bid / Ask / costs | Money derivative требует fixed/asymmetric valuation и costs; lot slope недостаточен. |
| 12 Partial fills / actual data | Helper сравнивает supplied money, сам не доказывает actual fill/market movement. |
| 13 Production mapping | Include/Planning/HSBI_GeometrySolver.mqh:12-19 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-046, HSBI-A03-ERR-037; HSBI-A03-IMP-007, HSBI-A03-IMP-021. |
| 15 Final statuses | MATH=FALSE; IMPLEMENTATION=CALLER_NOT_VERIFIED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-040 — PartialClose=floor_grid(Budget/LossPerLot)

**Источник правила:** `Docs/11_PARTIAL_FAR_SPECIFICATION_RU.md:7`. **Production операция/строки:** `Include/Scenarios/HSBI_PartialFarTypes.mqh:4`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** lot; money/(money/lot),L>0,disjoint fixed costs; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** При constant per-lot loss и без fixed fees rounding down даётcost<=budget. Ограничить volume<=Far и остаток0 либо>=min. Actual costs после fill сверяются; fee/slippage нарушают простую пропорцию.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-022, HSBI-A03-ERR-032; HSBI-A03-IMP-014, HSBI-A03-IMP-013. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-040 |
| 2 Exact normative source | Docs/11_PARTIAL_FAR_SPECIFICATION_RU.md:7 |
| 3 Expression | PartialClose=floor_grid(Budget/LossPerLot) |
| 4 Variables | B — PartialFar budget money; ℓ>0 — complete constant loss money/lot; h — lot step; v — close lot |
| 5 Dimensions | lot |
| 6 Domain | lot; money/(money/lot),L>0,disjoint fixed costs. |
| 7 Required assumptions | lot; money/(money/lot),L>0,disjoint fixed costs. Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | При constant per-lot loss и без fixed fees rounding down даётcost<=budget. Ограничить volume<=Far и остаток0 либо>=min. Actual costs после fill сверяются; fee/slippage нарушают простую пропорцию. |
| 9 Far BUY / Far SELL | BUY закрыть Bid, SELL Ask для loss-per-lot basis. |
| 10 Broker grid / rounding | Floor бюджетного raw lot; bound≤Far и residual0 либо≥Vmin; grid origin задан. |
| 11 Bid / Ask / costs | Пропорциональность только без неизвестного fixed fee/slippage; весь cost budget включает charges. |
| 12 Partial fills / actual data | ActualConsumed по подтверждённым fills; reserved unused release тому же owner, не новый grant. |
| 13 Production mapping | Include/Scenarios/HSBI_PartialFarTypes.mqh:4 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-022, HSBI-A03-ERR-032; HSBI-A03-IMP-014, HSBI-A03-IMP-013. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=NOT_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-041 — Checked signed int64 settled arithmetic

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:42`. **Production операция/строки:** `Include/Money/HSBI_MoneyState.mqh:4-5`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** NOT_IMPLEMENTED.

**Переменные, размерности и область:** minor units, -2^63..2^63-1; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** При x=MAX,d=1 сумма вне signed domain; при проверке x<=MAX-d переполнение самого промежуточного выражения также исключается. Reference unlimited integers не дают это свойство production double.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-040; HSBI-A03-IMP-002. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-041 |
| 2 Exact normative source | Docs/04_MATHEMATICAL_MODEL_RU.md:42 |
| 3 Expression | Checked signed int64 settled arithmetic |
| 4 Variables | x,y — signed minor-unit integers; MIN=−2^63; MAX=2^63−1; scale/currency — approved money profile |
| 5 Dimensions | minor units, -2^63..2^63-1. |
| 6 Domain | minor units, -2^63..2^63-1. |
| 7 Required assumptions | minor units, -2^63..2^63-1. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | При x=MAX,d=1 сумма вне signed domain; при проверке x<=MAX-d переполнение самого промежуточного выражения также исключается. Reference unlimited integers не дают это свойство production double. |
| 9 Far BUY / Far SELL | NOT_APPLICABLE: signed integer money арифметика, стороны учтены до posting. |
| 10 Broker grid / rounding | Scale/currency bounded; MAX+1 и −MIN вне signed64, checked intermediates обязательны. |
| 11 Bid / Ask / costs | Raw double observations и settled minor units раздельны; rounding policy не выбрана из тестовых чисел. |
| 12 Partial fills / actual data | Частичные debit суммируются exact, replay atomicity отдельно от точности. |
| 13 Production mapping | Include/Money/HSBI_MoneyState.mqh:4-5 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-040; HSBI-A03-IMP-002. |
| 15 Final statuses | MATH=UNDEFINED; IMPLEMENTATION=NOT_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-042 — F64Z/T17Z canonical numeric identity

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:42; NUM-CODEC proposal`. **Production операция/строки:** `Include/Money/HSBI_EconomicLedgerTypes.mqh:11`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** UNVERIFIED.

**Переменные, размерности и область:** bytes,schema,currency,finite numeric fields; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Нужны fixed field order,type tags,lengths,endian/zero/NaN policy и независимый decoder. Восьмизначная диагностика не canonical full record. Native goldens этим этапом не выполнялись.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-003, HSBI-A03-ERR-029; HSBI-A03-IMP-002, HSBI-A03-IMP-018. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-042 |
| 2 Exact normative source | Docs/04_MATHEMATICAL_MODEL_RU.md:42; NUM-CODEC proposal |
| 3 Expression | F64Z/T17Z canonical numeric identity |
| 4 Variables | body — typed immutable raw fields; codec/schema versions; Encode/Decode; zero/finite policies |
| 5 Dimensions | bytes,schema,currency,finite numeric fields. |
| 6 Domain | bytes,schema,currency,finite numeric fields. |
| 7 Required assumptions | bytes,schema,currency,finite numeric fields. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | Нужны fixed field order,type tags,lengths,endian/zero/NaN policy и независимый decoder. Восьмизначная диагностика не canonical full record. Native goldens этим этапом не выполнялись. |
| 9 Far BUY / Far SELL | NOT_APPLICABLE к bytes codec; direction field serializes as typed immutable enum. |
| 10 Broker grid / rounding | Finite raw binary64, canonical±0,known endian/version/lengths; не settled rounding. |
| 11 Bid / Ask / costs | Codec сохраняет captured signed components, не доказывает cost coverage/authenticity. |
| 12 Partial fills / actual data | Partial facts сериализуются отдельно; content digest не durable commit/independent receipt. |
| 13 Production mapping | Include/Money/HSBI_EconomicLedgerTypes.mqh:11 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-003, HSBI-A03-ERR-029; HSBI-A03-IMP-002, HSBI-A03-IMP-018. |
| 15 Final statuses | MATH=UNVERIFIED; IMPLEMENTATION=NOT_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-043 — Small decrements remain exact near 10^28

**Источник правила:** `NUM-EXACT-1 proposal; Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:24`. **Production операция/строки:** `Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:74`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** exact rational/decimal money,admitted finite domain; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** В рациональных числах 10^28-.01 отличается от10^28. В bounded binary64 spacing на таком масштабе намного больше. Это не допускает автоматического принятия10^28 как MQL settled domain.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-040; HSBI-A03-IMP-002. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-043 |
| 2 Exact normative source | NUM-EXACT-1 proposal; Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:24 |
| 3 Expression | Small decrements remain exact near 10^28 |
| 4 Variables | M=10^28 — abstract exact money magnitude; d>0 — малый debit; Q — exact rational/decimal domain |
| 5 Dimensions | exact rational/decimal money,admitted finite domain. |
| 6 Domain | exact rational/decimal money,admitted finite domain. |
| 7 Required assumptions | exact rational/decimal money,admitted finite domain. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | В рациональных числах 10^28-.01 отличается от10^28. В bounded binary64 spacing на таком масштабе намного больше. Это не допускает автоматического принятия10^28 как MQL settled domain. |
| 9 Far BUY / Far SELL | NOT_APPLICABLE к точной разности чисел; actual debit любого направления нуждается в authority. |
| 10 Broker grid / rounding | Exact rational/decimal domain ≠ MQL int64 range; binary64 spacing на10^28 не cent. |
| 11 Bid / Ask / costs | Raw codec не исправляет loss of arithmetic precision; posting scale independently fixed. |
| 12 Partial fills / actual data | Последовательные малые debit должны реально менять exact balance; историческое replay отдельно. |
| 13 Production mapping | Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:74 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-040; HSBI-A03-IMP-002. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=NOT_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-044 — NormalizePrice=round(price/tickSize)*tickSize

**Источник правила:** `Docs/25_BROKER_GRID_AND_ROUNDING_RU.md:5`. **Production операция/строки:** `Include/Planning/HSBI_ControlPrices.mqh:12`; mapping **PARTIALLY_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** price; tick>0,defined tie policy; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** При точных reals ошибка ближайшей сетки<=tick/2. Округление execution trigger может требовать directional floor/ceil, не ближайший tick; преобразование Point и TickSize не тождественно.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-039, HSBI-A03-ERR-040; HSBI-A03-IMP-007, HSBI-A03-IMP-002. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-044 |
| 2 Exact normative source | Docs/25_BROKER_GRID_AND_ROUNDING_RU.md:5 |
| 3 Expression | NormalizePrice=round(price/tickSize)*tickSize |
| 4 Variables | P — price; t>0 — tick size; n — integer rounding result; normalized=n t |
| 5 Dimensions | price |
| 6 Domain | price; tick>0,defined tie policy. |
| 7 Required assumptions | price; tick>0,defined tie policy. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | При точных reals ошибка ближайшей сетки<=tick/2. Округление execution trigger может требовать directional floor/ceil, не ближайший tick; преобразование Point и TickSize не тождественно. |
| 9 Far BUY / Far SELL | Trigger floor/ceil может зависеть от BUY/SELL/назначения; nearest само по себе не side policy. |
| 10 Broker grid / rounding | t>0,known tie rule; error≤t/2 только для exact nearest и допустимого результата. |
| 11 Bid / Ask / costs | Price rounding меняет liquidation net и costs; Point≠TickSize. |
| 12 Partial fills / actual data | Price normalization не actual fill price guarantee; slippage после partial требует reconcile. |
| 13 Production mapping | Include/Planning/HSBI_ControlPrices.mqh:12 (nearest overload); Include/Planning/HSBI_BrokerGrid.mqh:13–18 (typed rounding) |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-039, HSBI-A03-ERR-040; HSBI-A03-IMP-007, HSBI-A03-IMP-002. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=PARTIALLY_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-045 — Level=Reference+s*(Start+(k-1)*Step)*Point

**Источник правила:** `Docs/05_GEOMETRY_MODEL_RU.md:19`. **Production операция/строки:** `Include/Planning/HSBI_ControlPrices.mqh:LINE_NOT_VERIFIED`; mapping **NOT_VERIFIED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** price; Start,Step in points,k>=1; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Скобка в points, умножение на Point даёт price; s задаёт сторону. После tick normalization уровни могут совпасть; gap через несколько уровней не означает несколько actual fills.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-037, HSBI-A03-ERR-039; HSBI-A03-IMP-021, HSBI-A03-IMP-007. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-045 |
| 2 Exact normative source | Docs/05_GEOMETRY_MODEL_RU.md:19 |
| 3 Expression | Level=Reference+s*(Start+(k-1)*Step)*Point |
| 4 Variables | Pref — Far reference price; a,b — Start/Step in points; k≥1 — level; pt — price per point; s∈{±1} |
| 5 Dimensions | price |
| 6 Domain | price; Start,Step in points,k>=1. |
| 7 Required assumptions | price; Start,Step in points,k>=1. Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | Скобка в points, умножение на Point даёт price; s задаёт сторону. После tick normalization уровни могут совпасть; gap через несколько уровней не означает несколько actual fills. |
| 9 Far BUY / Far SELL | s задаёт правильную сторону relative Far; BUY/SELL favorable координаты противоположны. |
| 10 Broker grid / rounding | Start/Step points×Point→price; tick normalization может объединить разные levels. |
| 11 Bid / Ask / costs | Forecast level не обнуляет spread/charges; close side выбирается отдельно. |
| 12 Partial fills / actual data | Gap через несколько levels не несколько исполненных Harvest/events. |
| 13 Production mapping | NOT_IMPLEMENTED full level construction; Include/Planning/HSBI_ControlPrices.mqh:7–10 contains DTOs only |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-037, HSBI-A03-ERR-039; HSBI-A03-IMP-021, HSBI-A03-IMP-007. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=NOT_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-046 — BUY closes Bid; SELL closes Ask

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:39`. **Production операция/строки:** `Include/Money/HSBI_BasketMoneyEvaluator.mqh:14`; mapping **PARTIALLY_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** price; bid<=ask,finite fresh quotes; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** BUY liquidation продаёт поBid,SELL выкупается поAsk. Entry BUY поAsk,SELL поBid. Broker commissions/FX/costs отдельны, side alone не обещает executable fill.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-022, HSBI-A03-ERR-037; HSBI-A03-IMP-014, HSBI-A03-IMP-021. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-046 |
| 2 Exact normative source | Docs/04_MATHEMATICAL_MODEL_RU.md:39 |
| 3 Expression | BUY closes Bid; SELL closes Ask |
| 4 Variables | Bid≤Ask — contemporaneous quote; d — BUY/SELL position; close side — executable side |
| 5 Dimensions | price |
| 6 Domain | price; bid<=ask,finite fresh quotes. |
| 7 Required assumptions | price; bid<=ask,finite fresh quotes. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | BUY liquidation продаёт поBid,SELL выкупается поAsk. Entry BUY поAsk,SELL поBid. Broker commissions/FX/costs отдельны, side alone не обещает executable fill. |
| 9 Far BUY / Far SELL | BUY liquidation sells Bid;SELL liquidation buys Ask; entry sides противоположны. |
| 10 Broker grid / rounding | Bid/Ask finite,fresh,on admitted tick grid; level normalization отдельно. |
| 11 Bid / Ask / costs | Spread уже проявляется в prices; не вычитать повторно тот же spread cost. |
| 12 Partial fills / actual data | Actual fills по broker receipt могут отличаться от quote; projected side не settlement. |
| 13 Production mapping | Include/Money/HSBI_BasketMoneyEvaluator.mqh:14 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-022, HSBI-A03-ERR-037; HSBI-A03-IMP-014, HSBI-A03-IMP-021. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=PARTIALLY_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-047 — Minimum-safe N vs global risk-first objective

**Источник правила:** `Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:22-23; Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md:3`. **Production операция/строки:** `Include/Planning/HSBI_NewFarCandidate.mqh:33-40`; mapping **AMBIGUOUS**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** CONTRADICTORY.

**Переменные, размерности и область:** lot/risk/margin lexicographic tuple; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Candidate(.1,risk10) и(.2,risk5) выбираются по-разному. Нельзя называть глобальный risk-first tie-break равных minimum-safe N. Требуется approval precedence.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-019; HSBI-A03-IMP-011. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-047 |
| 2 Exact normative source | Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:22-23; Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md:3 |
| 3 Expression | Minimum-safe N vs global risk-first objective |
| 4 Variables | N — NewFar lot; r,m — risk/margin; objective tuple priority и tie-break |
| 5 Dimensions | lot/risk/margin lexicographic tuple. |
| 6 Domain | lot/risk/margin lexicographic tuple. |
| 7 Required assumptions | lot/risk/margin lexicographic tuple. Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | Candidate(.1,risk10) и(.2,risk5) выбираются по-разному. Нельзя называть глобальный risk-first tie-break равных minimum-safe N. Требуется approval precedence. |
| 9 Far BUY / Far SELL | Одна и та же утверждённая objective для обоих зеркал, не bias по направлению. |
| 10 Broker grid / rounding | Сравнение только admitted grid candidates; min N и min risk выбирают разные элементы. |
| 11 Bid / Ask / costs | Risk/margin tuple requires common money basis and fees; выбор приоритета административный. |
| 12 Partial fills / actual data | Selector returns plan candidate, не actual residual promotion. |
| 13 Production mapping | Include/Planning/HSBI_NewFarCandidate.mqh:33-40 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-019; HSBI-A03-IMP-011. |
| 15 Final statuses | MATH=CONTRADICTORY; IMPLEMENTATION=CALLER_NOT_VERIFIED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-048 — Grid n*step vs Vmin+n*step

**Источник правила:** `Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:9; Docs/25_BROKER_GRID_AND_ROUNDING_RU.md:5`. **Production операция/строки:** `Include/Planning/HSBI_BrokerGrid.mqh:36`; mapping **AMBIGUOUS**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** UNDEFINED.

**Переменные, размерности и область:** lot; origin,min,max,step>0; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Эквивалентность требует Vmin/step integer. Для.03/.02 origins расходятся. Брокер может запретить такую конфигурацию, но это отдельный admission contract.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-039; HSBI-A03-IMP-007. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-048 |
| 2 Exact normative source | Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:9; Docs/25_BROKER_GRID_AND_ROUNDING_RU.md:5 |
| 3 Expression | Grid n*step vs Vmin+n*step |
| 4 Variables | Vmin,h — lot minimum/step; Z0={nh}; Zmin={Vmin+nh}; n — admissible nonnegative integer |
| 5 Dimensions | lot |
| 6 Domain | lot; origin,min,max,step>0. |
| 7 Required assumptions | lot; origin,min,max,step>0. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | Эквивалентность требует Vmin/step integer. Для.03/.02 origins расходятся. Брокер может запретить такую конфигурацию, но это отдельный admission contract. |
| 9 Far BUY / Far SELL | Grid origin не определяется BUY/SELL знаком. |
| 10 Broker grid / rounding | Z0=Zmin при Vmin/h integer; .03/.02 — различающиеся lattice sets. |
| 11 Bid / Ask / costs | Broker admission/fees/margin не следуют из арифметики сетки. |
| 12 Partial fills / actual data | Для actual residual grid/source повторно сверяются; неверный origin не guessed correction. |
| 13 Production mapping | Include/Planning/HSBI_BrokerGrid.mqh:36 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-039; HSBI-A03-IMP-007. |
| 15 Final statuses | MATH=UNDEFINED; IMPLEMENTATION=CALLER_NOT_VERIFIED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-049 — round(sum components) vs sum(round components)

**Источник правила:** `Docs/HSB_2E_FORMULA_CONTRACTS_R2_RU.md:7-34`. **Production операция/строки:** `Include/Money/HSBI_CostModel.mqh:13`; mapping **AMBIGUOUS**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money,declared scale/rounding policy; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** При digits2,nearest half-up два компонента.004+.004 дают aggregate.008→.01; индивидуально0+0=0. Операции не коммутируют. Документ предписывает aggregation-before-rounding, но broker component posting domain и settlement grid ещё должны быть утверждены.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-040, HSBI-A03-ERR-022; HSBI-A03-IMP-002, HSBI-A03-IMP-014. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-049 |
| 2 Exact normative source | Docs/HSB_2E_FORMULA_CONTRACTS_R2_RU.md:7-34 |
| 3 Expression | round(sum components) vs sum(round components) |
| 4 Variables | xi — signed economic components; round_d — declared currency posting/rounding operator |
| 5 Dimensions | money,declared scale/rounding policy. |
| 6 Domain | money,declared scale/rounding policy. |
| 7 Required assumptions | money,declared scale/rounding policy. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | При digits2,nearest half-up два компонента.004+.004 дают aggregate.008→.01; индивидуально0+0=0. Операции не коммутируют. Документ предписывает aggregation-before-rounding, но broker component posting domain и settlement grid ещё должны быть утверждены. |
| 9 Far BUY / Far SELL | Signed components/rounding применяются одинаково по policy, а не по направлению роли. |
| 10 Broker grid / rounding | Aggregate-before-round versus component posting must be fixed; example .004+.004 at digits2. |
| 11 Bid / Ask / costs | Charges included once; независимый posted broker rule, не locally assumed half-up. |
| 12 Partial fills / actual data | Partial deals могут иметь отдельный posting rule; не склеивать произвольно rounded receipts. |
| 13 Production mapping | Include/Money/HSBI_CostModel.mqh:13 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-040, HSBI-A03-ERR-022; HSBI-A03-IMP-002, HSBI-A03-IMP-014. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=CALLER_NOT_VERIFIED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-050 — Equal-volume Initial Lock PnL=-L*K*(spread0+spread_t)

**Источник правила:** `Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md:6-20`. **Production операция/строки:** `Hybrid_Split_Big_Independent_EA.mq5:35-39`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money; constant K,simultaneous equal legs,fees separate; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** BUY=L(Bid_t-Ask_0)K,SELL=L(Bid_0-Ask_t)K. Сумма после группировки минус двух spreads. Mid movement сокращается, costs ухудшают результат. При spread1,LK1 итог-2 без дополнительных fees.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-036, HSBI-A03-ERR-042; HSBI-A03-IMP-020, HSBI-A03-IMP-021. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-050 |
| 2 Exact normative source | Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md:6-20 |
| 3 Expression | Equal-volume Initial Lock PnL=-L*K*(spread0+spread_t) |
| 4 Variables | L — равный BUY/SELL lot; K — constant payout; A0,B0,At,Bt — opening/current Ask/Bid |
| 5 Dimensions | money |
| 6 Domain | money; constant K,simultaneous equal legs,fees separate. |
| 7 Required assumptions | money; constant K,simultaneous equal legs,fees separate. Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | BUY=L(Bid_t-Ask_0)K,SELL=L(Bid_0-Ask_t)K. Сумма после группировки минус двух spreads. Mid movement сокращается, costs ухудшают результат. При spread1,LK1 итог-2 без дополнительных fees. |
| 9 Far BUY / Far SELL | Equal BUY/SELL legs; перестановка имени Far не меняет суммарный lock PnL. |
| 10 Broker grid / rounding | Одинаковый admitted L; K fixed; actual equal volumes,не только requests. |
| 11 Bid / Ask / costs | Сумма=−LK(spread0+spreadt), дополнительные fees/carry отдельно signed. |
| 12 Partial fills / actual data | Partial/unbalanced fills ломают equal-volume lock premise и оставляют exposure. |
| 13 Production mapping | Hybrid_Split_Big_Independent_EA.mq5:35-39 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-036, HSBI-A03-ERR-042; HSBI-A03-IMP-020, HSBI-A03-IMP-021. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=NOT_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-051 — Favorable coordinate u=s(P-P0); dPi/du=K*(C+T-S-F)

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:12,39; Docs/26_GEOMETRY_ENGINE_SPECIFICATION_RU.md:7`. **Production операция/строки:** `Include/Planning/HSBI_GeometrySolver.mqh:10`; mapping **PARTIALLY_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money/price; K>0 common constant,spread/cost fixed; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** FarSELL s+1 signed netD;FarBUY s-1 signed net-D. Умножение dP/du=s даётKD для обоих. При K(P) и changing costs производная иная; lot slope остаётся фильтром.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-046, HSBI-A03-ERR-037; HSBI-A03-IMP-007, HSBI-A03-IMP-021. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-051 |
| 2 Exact normative source | Docs/04_MATHEMATICAL_MODEL_RU.md:12,39; Docs/26_GEOMETRY_ENGINE_SPECIFICATION_RU.md:7 |
| 3 Expression | Favorable coordinate u=s(P-P0); dPi/du=K*(C+T-S-F) |
| 4 Variables | s=+1 Far SELL,−1 Far BUY; u=s(P−P0); K>0 — payout coefficient; D=C+T−S−F |
| 5 Dimensions | money/price |
| 6 Domain | money/price; K>0 common constant,spread/cost fixed. |
| 7 Required assumptions | money/price; K>0 common constant,spread/cost fixed. Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | FarSELL s+1 signed netD;FarBUY s-1 signed net-D. Умножение dP/du=s даётKD для обоих. При K(P) и changing costs производная иная; lot slope остаётся фильтром. |
| 9 Far BUY / Far SELL | s=+1 SELL,−1 BUY; dP/du=s, поэтому обе favorable slopes=KD. |
| 10 Broker grid / rounding | C/T/S/F фиксированы и post-grid; local tick derivative не full price-range proof. |
| 11 Bid / Ask / costs | Общий постоянный K, fixed spread/cost; K(P) или changing costs добавляют terms. |
| 12 Partial fills / actual data | После partial volumes/D меняются; прежняя slope не сохраняется автоматически. |
| 13 Production mapping | Include/Planning/HSBI_GeometrySolver.mqh:10 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-046, HSBI-A03-ERR-037; HSBI-A03-IMP-007, HSBI-A03-IMP-021. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=PARTIALLY_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-052 — Transition prefix Net: D→C+T-F→C+T→C→N

**Источник правила:** `Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md:12-14`. **Production операция/строки:** `LINE_NOT_VERIFIED`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** lot; full closes in fixed order; FarSELL mirror negates Net; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Прямое вычитание закрытой signed leg: SmallSELL close добавляет S кNet;FarSELL close добавляетF. C1.2,T1,S.5,F1,N.6 дают.7,1.2,2.2,1.2,.6. Gross монотонно падает,Net временно растёт.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-041; HSBI-A03-IMP-022. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-052 |
| 2 Exact normative source | Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md:12-14 |
| 3 Expression | Transition prefix Net: D→C+T-F→C+T→C→N |
| 4 Variables | F,C,T,S,N — Far/Core/Trend/Small/residual lots; Dj — signed Net на каждом close prefix |
| 5 Dimensions | lot |
| 6 Domain | lot; full closes in fixed order; FarSELL mirror negates Net. |
| 7 Required assumptions | lot; full closes in fixed order; FarSELL mirror negates Net. Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | Прямое вычитание закрытой signed leg: SmallSELL close добавляет S кNet;FarSELL close добавляетF. C1.2,T1,S.5,F1,N.6 дают.7,1.2,2.2,1.2,.6. Gross монотонно падает,Net временно растёт. |
| 9 Far BUY / Far SELL | Far SELL prefix Net=D,C+T−F,C+T,C,N; зеркало меняет все знаки. |
| 10 Broker grid / rounding | Full closes таблицы на actual lots; partial даёт иные промежуточные значения. |
| 11 Bid / Ask / costs | Prefix risk/margin/cap оценивается по каждому состоянию,не только endpoint. |
| 12 Partial fills / actual data | Actual remaining Core и порядок confirmed fills обязательны; запрет следующего шага не отменяет прошлые closes. |
| 13 Production mapping | NOT_FOUND complete production operation; old locator retained above for history |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-041; HSBI-A03-IMP-022. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=NOT_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-053 — Reserve d:(R,Free)→(R+d,Free-d)

**Источник правила:** `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:24`. **Production операция/строки:** `LINE_NOT_VERIFIED`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** settled money;0<d<=Free,owner/event explicit; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Сумма R+Free неизменна,неотрицательность из предусловия. Owner reservation не равна consumed; повторная чужая reservation не использует тот же free.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-007, HSBI-A03-ERR-033; HSBI-A03-IMP-004. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-053 |
| 2 Exact normative source | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:24 |
| 3 Expression | Reserve d:(R,Free)→(R+d,Free-d) |
| 4 Variables | d — reservation money; Rr,Ff — Reserved/Free; owner/event — reservation identities |
| 5 Dimensions | settled money |
| 6 Domain | settled money;0<d<=Free,owner/event explicit. |
| 7 Required assumptions | settled money;0<d<=Free,owner/event explicit. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | Сумма R+Free неизменна,неотрицательность из предусловия. Owner reservation не равна consumed; повторная чужая reservation не использует тот же free. |
| 9 Far BUY / Far SELL | NOT_APPLICABLE: reservation меняет money categories, не positions. |
| 10 Broker grid / rounding | 0<d≤Free в той же monetary grid; Rr+d и Free−d checked. |
| 11 Bid / Ask / costs | Reservation не realised expense и не доход; цель/cost allowance фиксируются отдельно. |
| 12 Partial fills / actual data | Atomic reserve+receipt owner/event; exact repeat не повторное уменьшение Free. |
| 13 Production mapping | NOT_FOUND complete production operation; old locator retained above for history |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-007, HSBI-A03-ERR-033; HSBI-A03-IMP-004. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=NOT_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-054 — Release owner d:(R,Free)→(R-d,Free+d)

**Источник правила:** `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:24`. **Production операция/строки:** `LINE_NOT_VERIFIED`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money;d<=that owner reserved balance; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Сумма сохранена. Общего R>=d недостаточно: средства могут принадлежать другому owner. Нужен receipt reservation identity и exact replay.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-007, HSBI-A03-ERR-017; HSBI-A03-IMP-004, HSBI-A03-IMP-009. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-054 |
| 2 Exact normative source | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:24 |
| 3 Expression | Release owner d:(R,Free)→(R-d,Free+d) |
| 4 Variables | d — release money; Rowner — reserve этого owner; Rr,Ff — общий Reserved/Free |
| 5 Dimensions | money |
| 6 Domain | money;d<=that owner reserved balance. |
| 7 Required assumptions | money;d<=that owner reserved balance. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | Сумма сохранена. Общего R>=d недостаточно: средства могут принадлежать другому owner. Нужен receipt reservation identity и exact replay. |
| 9 Far BUY / Far SELL | NOT_APPLICABLE: release денежной reservation. |
| 10 Broker grid / rounding | 0<d≤Rowner, exact posting units; global Rr≥d без owner binding недостаточно. |
| 11 Bid / Ask / costs | Release не новая прибыль и не возврат уже фактически consumed суммы. |
| 12 Partial fills / actual data | Reconcile actual unused amount, затем release receipt; чужой owner не освобождает reservation. |
| 13 Production mapping | NOT_FOUND complete production operation; old locator retained above for history |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-007, HSBI-A03-ERR-017; HSBI-A03-IMP-004, HSBI-A03-IMP-009. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=NOT_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-055 — Unreserved consume d:(C,Free)→(C+d,Free-d)

**Источник правила:** `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:24`. **Production операция/строки:** `LINE_NOT_VERIFIED`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money;0<d<=Free,complete reconciled journal; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Плюс d и минус d сокращаются в G. Прогноз, Unallocated и ResidualHeld не подставляются вFree без отдельного eligibility policy.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-033, HSBI-A03-ERR-006; HSBI-A03-IMP-004, HSBI-A03-IMP-003. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-055 |
| 2 Exact normative source | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:24 |
| 3 Expression | Unreserved consume d:(C,Free)→(C+d,Free-d) |
| 4 Variables | d — free debit; Cc,Ff — Consumed/Free; event/source/bucket — обязательные identities |
| 5 Dimensions | money |
| 6 Domain | money;0<d<=Free,complete reconciled journal. |
| 7 Required assumptions | money;0<d<=Free,complete reconciled journal. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | Плюс d и минус d сокращаются в G. Прогноз, Unallocated и ResidualHeld не подставляются вFree без отдельного eligibility policy. |
| 9 Far BUY / Far SELL | NOT_APPLICABLE: unreserved money debit. |
| 10 Broker grid / rounding | 0<d≤Free, exact same-unit Cc+d/Free−d. |
| 11 Bid / Ask / costs | Не тратить held/forecast/unallocated как Free; actual debit и additional risk раздельны. |
| 12 Partial fills / actual data | One event commit, journal completeness и replay guard обязательны до изменения. |
| 13 Production mapping | NOT_FOUND complete production operation; old locator retained above for history |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-033, HSBI-A03-ERR-006; HSBI-A03-IMP-004, HSBI-A03-IMP-003. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=NOT_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-056 — Reserved owner consume d:(C,R)→(C+d,R-d)

**Источник правила:** `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:24`. **Production операция/строки:** `LINE_NOT_VERIFIED`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money;same owner/reservation,0<d<=owner R; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** G сохраняется,Free не меняется. Нельзя одновременно списать d из R и Free или оставить reservation доступным после расхода.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-007, HSBI-A03-ERR-017; HSBI-A03-IMP-004, HSBI-A03-IMP-009. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-056 |
| 2 Exact normative source | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:24 |
| 3 Expression | Reserved owner consume d:(C,R)→(C+d,R-d) |
| 4 Variables | d — reserved debit; Cc,Rowner — Consumed/owner reserve; Ff — Free неизменен |
| 5 Dimensions | money |
| 6 Domain | money;same owner/reservation,0<d<=owner R. |
| 7 Required assumptions | money;same owner/reservation,0<d<=owner R. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | G сохраняется,Free не меняется. Нельзя одновременно списать d из R и Free или оставить reservation доступным после расхода. |
| 9 Far BUY / Far SELL | NOT_APPLICABLE: owner reservation consumption. |
| 10 Broker grid / rounding | 0<d≤reservation этого owner, exact Cc+d/Rowner−d, Free неизменен. |
| 11 Bid / Ask / costs | Не списать одновременно изReserved иFree; expense не становится второй grant. |
| 12 Partial fills / actual data | Actual used portion confirmed,unused отдельно release,immutable consumption receipt. |
| 13 Production mapping | NOT_FOUND complete production operation; old locator retained above for history |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-007, HSBI-A03-ERR-017; HSBI-A03-IMP-004, HSBI-A03-IMP-009. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=NOT_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-057 — Exact replay delta0; changed replay CONFLICT

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:30; Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md:6-21`. **Production операция/строки:** `Include/Persistence/HSBI_ExecutionJournal.mqh:21-29`; mapping **MISMATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** event key+full immutable payload+durable receipt; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Доказательство exact idempotency требует прежний полный payload, не только заявленный digest. Повтор изменённого компонента не NO_OP. Существование local equality не доказывает durable/concurrent once.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-001, HSBI-A03-ERR-004, HSBI-A03-ERR-030, HSBI-A03-ERR-017; HSBI-A03-IMP-001, HSBI-A03-IMP-003, HSBI-A03-IMP-009. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-057 |
| 2 Exact normative source | Docs/04_MATHEMATICAL_MODEL_RU.md:30; Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md:6-21 |
| 3 Expression | Exact replay delta0; changed replay CONFLICT |
| 4 Variables | e — event key; p — immutable payload; receipt(e,p) — ранее committed result; Δstate — изменение |
| 5 Dimensions | event key+full immutable payload+durable receipt. |
| 6 Domain | event key+full immutable payload+durable receipt. |
| 7 Required assumptions | event key+full immutable payload+durable receipt. Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | Доказательство exact idempotency требует прежний полный payload, не только заявленный digest. Повтор изменённого компонента не NO_OP. Существование local equality не доказывает durable/concurrent once. |
| 9 Far BUY / Far SELL | NOT_APPLICABLE: replay key/payload equality независимо от market direction. |
| 10 Broker grid / rounding | Типизированные точные IDs/payload,полный digest/body binding; raw/posted policy неизменна. |
| 11 Bid / Ask / costs | Changed component при equalNet не NO_OP; costs входят в immutable economic receipt. |
| 12 Partial fills / actual data | Exact replay delta0/revision unchanged; durability/concurrency требуют backend,не только memory comparison. |
| 13 Production mapping | Include/Persistence/HSBI_ExecutionJournal.mqh:21-29 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-001, HSBI-A03-ERR-004, HSBI-A03-ERR-030, HSBI-A03-ERR-017; HSBI-A03-IMP-001, HSBI-A03-IMP-003, HSBI-A03-IMP-009. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=IMPLEMENTED_MISMATCH; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-058 — Uniform contraction implies F_k<=q^k*F_0

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:33-36`. **Production операция/строки:** `Include/Planning/HSBI_FutureSmallSolver.mqh:142-147`; mapping **PARTIALLY_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** lot;forall reachable transitions,q in(0,1),rounded states; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** База k0 equality. Шаг: F(k+1)<=qF(k)<=q*q^kF0=q^(k+1)F0. Доказательство условно: не доказывает existence/execution следующего transition и terminal closure.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-021, HSBI-A03-ERR-032; HSBI-A03-IMP-013. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-058 |
| 2 Exact normative source | Docs/04_MATHEMATICAL_MODEL_RU.md:33-36 |
| 3 Expression | Uniform contraction implies F_k<=q^k*F_0 |
| 4 Variables | Fk — nonnegative rounded Far lot; F0 — initial lot; q∈(0,1); k — успешные transitions |
| 5 Dimensions | lot |
| 6 Domain | lot;forall reachable transitions,q in(0,1),rounded states. |
| 7 Required assumptions | lot;forall reachable transitions,q in(0,1),rounded states. Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | База k0 equality. Шаг: F(k+1)<=qF(k)<=q*q^kF0=q^(k+1)F0. Доказательство условно: не доказывает existence/execution следующего transition и terminal closure. |
| 9 Far BUY / Far SELL | Contraction volume theorem одинакова по модулю для BUY/SELL; каждый следующий actual direction проверяется. |
| 10 Broker grid / rounding | Uniform q именно для normalized Fk; на минимальной сетке terminal close обязателен отдельно. |
| 11 Bid / Ask / costs | Costs/risk/margin must preserve invariant admitted set; q alone не economic solvency. |
| 12 Partial fills / actual data | Каждый complete successful step обязан существовать; partial/timeout не induction step. |
| 13 Production mapping | Include/Planning/HSBI_FutureSmallSolver.mqh:142-147 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-021, HSBI-A03-ERR-032; HSBI-A03-IMP-013. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=PARTIALLY_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-059 — Unhedged SELL adverse loss=F*K*(P-Popen)

**Источник правила:** `Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:6-18`. **Production операция/строки:** `LINE_NOT_VERIFIED`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money;F,K>0 linear payout,P>=Popen; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Для любого boundB можно выбрать P>Popen+B/(FK), тогдаloss>B. Это опровержение безусловного bound при данных assumptions; ограниченный price/liability domain требует отдельного доказательства и не исключается.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-038; HSBI-A03-IMP-021. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-059 |
| 2 Exact normative source | Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:6-18 |
| 3 Expression | Unhedged SELL adverse loss=F*K*(P-Popen) |
| 4 Variables | F>0 — открытый SELL lot; K>0 — payout; Popen — entry; P — adverse close price |
| 5 Dimensions | money |
| 6 Domain | money;F,K>0 linear payout,P>=Popen. |
| 7 Required assumptions | money;F,K>0 linear payout,P>=Popen. Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | Для любого boundB можно выбрать P>Popen+B/(FK), тогдаloss>B. Это опровержение безусловного bound при данных assumptions; ограниченный price/liability domain требует отдельного доказательства и не исключается. |
| 9 Far BUY / Far SELL | Контрпример unbounded adverse price относится к SELL; BUY при nonnegative P имеет другой local bound. |
| 10 Broker grid / rounding | F,K fixed positive; lot cap не cap price/liability. |
| 11 Bid / Ask / costs | Gap/fees/carry/conversion могут расширять риск; stop trigger не guaranteed fill bound. |
| 12 Partial fills / actual data | Незакрытый residual несёт риск до actual terminal fill; price path/исполнение не гарантированы. |
| 13 Production mapping | NOT_FOUND complete production operation; old locator retained above for history |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-038; HSBI-A03-IMP-021. |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=NOT_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

## HSBI-A03-F-060 — Projected→Actual→Reconciled→Eligible→Available are distinct transformations

**Источник правила:** `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:6-24; Docs/31_MONEY_PROOF_IDENTITY_RU.md:5`. **Production операция/строки:** `Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:24-28`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** UNVERIFIED.

**Переменные, размерности и область:** typed money with authority,currency,scope,owner; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Каждая стрелка добавляет независимые факты, а не просто копирует scalar100. Если нет deals, projected100 не grants100. Unknown history не известный ноль; full empty history может доказывать отсутствие funds.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-033, HSBI-A03-ERR-013; HSBI-A03-IMP-004, HSBI-A03-IMP-001. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-060 |
| 2 Exact normative source | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:6-24; Docs/31_MONEY_PROOF_IDENTITY_RU.md:5 |
| 3 Expression | Projected→Actual→Reconciled→Eligible→Available are distinct transformations |
| 4 Variables | Projected/Actual/Reconciled/Eligible/Available — разные денежные типы и фактические authority stages |
| 5 Dimensions | typed money with authority,currency,scope,owner. |
| 6 Domain | typed money with authority,currency,scope,owner. |
| 7 Required assumptions | typed money with authority,currency,scope,owner. Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | Каждая стрелка добавляет независимые факты, а не просто копирует scalar100. Если нет deals, projected100 не grants100. Unknown history не известный ноль; full empty history может доказывать отсутствие funds. |
| 9 Far BUY / Far SELL | Тип денежного факта не зависит от имени BUY/SELL; ownership и role проверяются independently. |
| 10 Broker grid / rounding | Currency/precision/window/source immutable facts обязательны между стадиями. |
| 11 Bid / Ask / costs | Actual signed components и costs подтверждаются, forecast/buffer не settled resource. |
| 12 Partial fills / actual data | Каждая стрелка требует новых независимых facts/history; scalar copy/flags не actual confirmation. |
| 13 Production mapping | Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:24-28 |
| 14 ERR / IMP / contracts | HSBI-A03-ERR-033, HSBI-A03-ERR-013; HSBI-A03-IMP-004, HSBI-A03-IMP-001. |
| 15 Final statuses | MATH=UNVERIFIED; IMPLEMENTATION=NOT_IMPLEMENTED; scope limited to this relation, native NOT_RUN |


## Сводка статусов

CONTRADICTORY=3, INVALID=1, NOT_IMPLEMENTED=1, UNDEFINED=6, UNVERIFIED=6, VERIFIED_UNDER_ASSUMPTIONS=43.

UNVERIFIED в итоговом машинном блоке включает UNVERIFIED+UNDEFINED+NOT_IMPLEMENTED, чтобы сумма категорий равнялась FORMULAS_TOTAL. Production mapping — независимая ось: условно верная алгебра может иметь MISMATCH в исходнике. Наличие этих 60 семейств не доказывает, что все формулы всех исторических приложений обнаружены: документальное покрытие PARTIAL.


## COVERAGE-COMPLETION — новые отношения и уточнение классификации

Исходные F001–F060 и их исторические статусы сохранены выше. Современные имена статусов: VERIFIED_UNDER_ASSUMPTIONS → MATHEMATICALLY_VALID_UNDER_ASSUMPTIONS; CONTRADICTORY → NORMATIVE_CONTRADICTION; INVALID → MATHEMATICALLY_FALSE. SOURCE_CONTRADICTION — отдельная ось соответствия реализации, а не дополнительная формула в сумме. UNDEFINED означает отсутствующий выбор нормы, UNVERIFIED — отсутствующее доказательство сформулированного свойства. NOT_IMPLEMENTED не заменяется PASS корректной алгебры.


### HSBI-A03-F-061 — Мгновенный объём не равен обороту за время

**Источник:** Docs/02_SYSTEM_ROLES_AND_IDENTITY_RU.md:6–20; Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:6–24; Include/Core/HSBI_Context.mqh:19–24,48–53. **Статус:** MATHEMATICALLY_VALID_UNDER_ASSUMPTIONS. **Production mapping:** PARTIALLY_IMPLEMENTED / ERR-012.

Пусть в один момент существует не более четырёх уникальных собственных позиций, каждая объёмом не более Vmax. Тогда TotalGross(t)=Σ|Vj(t)|≤4Vmax. Это lot, не money. Необходимы один symbol/учёт виртуальных legs, отсутствие pending overfill, глобальный position inventory и применимость broker max к каждой позиции. Для обоих направлений модуль одинаков. Grid уменьшает множество допустимых объёмов, но сам не ограничивает число повторных открытий. При каждом из n повторов открыть и закрыть v>0 lot оборот уже 2nv; при n→∞ он неограничен, даже если мгновенный Gross≤4Vmax. Costs и частичные fills учитываются по actual обороту. Нельзя из ограничения мгновенного объёма вывести ограничение суммарных комиссий, убытка или времени. Связи F030/F052/F058/F059; ERR-032/038/042; IMP-013/021. Не доказано, что current source гарантирует все перечисленные предусловия.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-061 |
| 2 Exact normative source | Docs/02_SYSTEM_ROLES_AND_IDENTITY_RU.md:6–20; Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:6–24 |
| 3 Expression | Gross(t)≤4Vmax; turnover not bounded by it |
| 4 Variables | n(t)≤4 — unique active positions; Vj≤Vmax; Gross(t)=ΣVj; turnover=Σ executed lot over time |
| 5 Dimensions | lot |
| 6 Domain | n(t)≤4,each actual Vj≤Vmax,unique positions,no pending overfill |
| 7 Required assumptions | n(t)≤4,each actual Vj≤Vmax,unique positions,no pending overfill Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | Σj≤4 Vj≤4Vmax. Reopen/close v repeatedly n times gives turnover2nv,unbounded as n grows. |
| 9 Far BUY / Far SELL | Gross uses absolute lots; зеркальное направление меняет Net, не bound4Vmax. |
| 10 Broker grid / rounding | Нужен bound числа unique positions и каждого volume; grid не bound числа повторов. |
| 11 Bid / Ask / costs | Bound holdings не bound turnover/fees/carry или money loss. |
| 12 Partial fills / actual data | Учитывать actual fills/pending exposure, aliases не отдельные позиции. |
| 13 Production mapping | Include/Core/HSBI_Context.mqh:19–24,48–53; count constraints incomplete |
| 14 ERR / IMP / contracts | ERR-012/032/038/042; IMP-006/013/021 |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=PARTIALLY_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

### HSBI-A03-F-062 — Учёт fills и точное завершение

**Источник:** Tests/Contracts/HSB_2E_R4_R9_R4A_R12A_NORMATIVE_DECISIONS.md:27–31. **Статус:** MATHEMATICALLY_VALID_UNDER_ASSUMPTIONS. **Область:** исторический static qualification contract, не production settlement. **Production:** Include/Execution/HSBI_TransactionTypes.mqh:15 / неполная интеграция.

Для одного intent I: Filled(I)=Σ уникальных подтверждённых, принадлежащих I и ticket сделок; Remaining(I)=Requested(I)−Filled(I), 0≤Filled≤Requested. Объёмы lot, Requested>0 finite, каждый fill>0 на объявленной step-сетке, membership/history complete. BUY/SELL меняют денежный результат, не равенство объёмов. Zero remaining обязателен для полного исполнения, но не для PARTIAL. Deal ID uniqueness без полного immutable equality недостаточна; неизвестная history не даёт Remaining=0. Bid/Ask, комиссия и slippage требуют отдельной фактической денежной сверки, а не усреднения плановой цены. Связи F007/F024/F036/F057; ERR-010/017/030; IMP-005/008/009.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-062 |
| 2 Exact normative source | Tests/Contracts/HSB_2E_R4_R9_R4A_R12A_NORMATIVE_DECISIONS.md:27–31 |
| 3 Expression | Filled(I)=Σ unique bound volumes;Remaining=Requested−Filled |
| 4 Variables | I — intent; D(I) — unique valid bound deals; Requested,Filled,Remaining — lot; Filled=Σ volume |
| 5 Dimensions | lot |
| 6 Domain | Requested>0,positive admitted fill volumes,complete independent membership/history |
| 7 Required assumptions | Requested>0,positive admitted fill volumes,complete independent membership/history Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | By definition remaining difference;0≤Filled≤Requested iff remaining≥0. Full settlement additionally remaining0. |
| 9 Far BUY / Far SELL | BUY/SELL влияет на economic net, но не на amount Filled/Remaining lot. |
| 10 Broker grid / rounding | Все fill volumes positive и admitted step; requested/actual и ticket membership отдельно. |
| 11 Bid / Ask / costs | Actual fill prices/charges по deals; volume equality не cost/identity proof. |
| 12 Partial fills / actual data | Filled=sum unique valid bound deals; remaining=requested−filled; full только remaining0. |
| 13 Production mapping | Include/Execution/HSBI_TransactionTypes.mqh:15; full independent accumulator not implemented |
| 14 ERR / IMP / contracts | ERR-010/017/030; IMP-005/008/009 |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=PARTIALLY_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

### HSBI-A03-F-063 — Равенство множеств intent IDs не доказывает полного fill

**Источник:** тот же R12A документ:19–31. **Статус:** MATHEMATICALLY_FALSE для импликации SetEquality⇒ExactSettlement. **Production mapping:** соответствующая полноценная связанная интеграция NOT_VERIFIED.

Пусть expected IDs={I1}, Requested(I1)=1 lot, observed deal D1 принадлежит I1, confirmed, volume=.4. Тогда observed IDs={I1}, множества равны, но Remaining=.6. Это ручной контрпример для BUY и SELL; step=.1, все объёмы on-grid. Расходы не устраняют недостающий объём. Строка31 прямо требует exact settlement; поэтому полный норматив читается как conjunction: set/batch/confirmation/uniqueness И ∀I Filled(I)=Requested(I). Нельзя объявить весь документ противоречивым только по изолированной строке25; нельзя также исполнить только её set equality. Связи F062/F057; ERR-010/016/028, IMP-008/017. Проверка всех исторических evaluator callers этого conjunction ещё не завершена; автоматический новый SOURCE_DEFECT не присвоен.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-063 |
| 2 Exact normative source | Tests/Contracts/HSB_2E_R4_R9_R4A_R12A_NORMATIVE_DECISIONS.md:19–31 |
| 3 Expression | ExpectedIDs=ObservedIDs ⇒ every intent fully settled |
| 4 Variables | E — expected intent ID set; O — observed deal intent IDs; Requested/Filled — per-intent lot |
| 5 Dimensions | dimensionless logic/count plus declared lot/money facts |
| 6 Domain | Nonempty requested intents; confirmed unique but possibly partial fills |
| 7 Required assumptions | Nonempty requested intents; confirmed unique but possibly partial fills Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | Requested(I1)=1,one bound fill.4: sets equal{I1},yet remaining.6. Conjunction with F062 is needed. |
| 9 Far BUY / Far SELL | Контрпример .4 изrequested1 работает для BUY/SELL. |
| 10 Broker grid / rounding | Requested1/fill.4 при step.1 валидны; missing.6 не исчезает от grid. |
| 11 Bid / Ask / costs | Costs никак не доказывают недостающий volume; set equality не economic settlement. |
| 12 Partial fills / actual data | ExpectedIDs={I1}=ObservedIDs,но Filled.4≠1; full commit требует conjunction с F062. |
| 13 Production mapping | Historical batch evaluators callers NOT_VERIFIED; no complete production settlement provider |
| 14 ERR / IMP / contracts | ERR-010/016/028; IMP-008/017 |
| 15 Final statuses | MATH=FALSE; IMPLEMENTATION=CALLER_NOT_VERIFIED; scope limited to this relation, native NOT_RUN |

### HSBI-A03-F-064 — Целочисленное распределение с остатком

**Источник:** Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:12–24; Include/Money/HSBI_AllocationPolicyTypes.mqh:16–23; Include/Money/HSBI_AllocationLedgerTypes.mqh:6–10. **Статус:** MATHEMATICALLY_VALID_UNDER_ASSUMPTIONS. **Production mapping:** SOURCE_CONTRADICTION для negative buckets, не для policy transitionShare.

Пусть N≥0 — settled minor units, 0≤si≤1, Σsi≤1. Выдать bi=floor(Nsi), а residual=N−Σbi. Тогда каждый bi≥0, residual≥0, Σbi+residual=N. Направления/lot grid неприменимы непосредственно: деньги имеют собственную currency/scale lattice. Нужны точные произведения/checked intermediates; округление каждого bi вверх может нарушить бюджет: N=1, shares .5/.5, ceil даёт2. Signed broker components сначала сверяются по утверждённой posting policy; нельзя делить projected или отрицательный DealNet как положительный grant. На N=0 гранты0. Costs уже в N не вычитаются повторно; partial fills создают факты лишь после reconciliation. Связи F007/F012–016/F049, ERR-005/006/022, IMP-002/003. Policy validator уже проверяет transitionShare≥0; снятая гипотеза отмечена в реестре.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-064 |
| 2 Exact normative source | Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:12–24; R0F candidate monetary profile |
| 3 Expression | bi=floor(Nsi); residual=N−Σbi;Σbi+residual=N |
| 4 Variables | N≥0 — settled minor units; si≥0,Σsi≤1 — shares; bi=floor(Nsi); residual=N−Σbi |
| 5 Dimensions | integer account minor units |
| 6 Domain | N integer≥0,each share≥0,sum shares≤1,checked exact arithmetic |
| 7 Required assumptions | N integer≥0,each share≥0,sum shares≤1,checked exact arithmetic Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | 0≤Σfloor(Nsi)≤NΣsi≤N,so residual≥0 and exact partition follows. Ceil .5/.5 on N1 gives2,not allowed. |
| 9 Far BUY / Far SELL | NOT_APPLICABLE: settled source allocation, направления уже отражены signed source net. |
| 10 Broker grid / rounding | N integer minor units; floor shares и explicit residual сохраняют exact sum. |
| 11 Bid / Ask / costs | Делится eligible posted net после расходов; отрицательные deals не positive grants. |
| 12 Partial fills / actual data | Grant only после reconciliation; partial predicted net не может быть распределён actual. |
| 13 Production mapping | NOT_IMPLEMENTED exact integer allocator; adjacent Include/Money/HSBI_AllocationPolicyTypes.mqh:16–23 and Include/Money/HSBI_AllocationLedgerTypes.mqh:6–10 are validators |
| 14 ERR / IMP / contracts | ERR-005/006/022/040; IMP-002/003/014 |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=NOT_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

### HSBI-A03-F-065 — Проверка revision не является атомарным commit

**Источник:** Docs/16_PERSISTENCE_AND_RESTART_RU.md:6–21; Docs/HSB.2C_Journal_Persistence_Reconciliation.md:3–7; Include/Core/HSBI_StateMachine.mqh:6–7; Include/Persistence/HSBI_ExecutionJournal.mqh:21–29. **Статус:** MATHEMATICALLY_VALID_UNDER_ASSUMPTIONS для необходимости единой сериализации competing transitions; production durable/concurrent enforcement NOT_IMPLEMENTED.

Free=50, revision=r. A и B независимо читают эти же значения и запрашивают30. Оба локальных условия30≤50 истинны. Два разрешения не доказывают, что60≤50; требуется атомарное сравнение revision и запись balances+receipts либо эквивалентная сериализуемая транзакция. При CAS один commit делает Free20,r+1; второй получает conflict и zero delta. Даже корректная in-memory последовательная функция не доказывает crash durability или multi-process ordering. Денежные единицы едины; r безразмерный ограниченный ID с проверкой переполнения. BUY/SELL, grid и costs не заменяют backend ordering; actual debit определяется отдельно. Связи F013–019/F053–057; ERR-017/025/030/033; IMP-004/009. Это аналитическая интерливинг-схема, конкурентный тест не запускался.


### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-065 |
| 2 Exact normative source | Docs/16_PERSISTENCE_AND_RESTART_RU.md:6–21; Docs/HSB.2C_Journal_Persistence_Reconciliation.md:3–7 |
| 3 Expression | Local revision check ≠ atomic balance+receipt commit |
| 4 Variables | r — expected state revision; Free — settled money; debit A/B — competing transitions; CAS — atomic state update |
| 5 Dimensions | dimensionless logic/count plus declared lot/money facts |
| 6 Domain | Two consumers share source;stale reads permitted without serialization;exact state |
| 7 Required assumptions | Two consumers share source;stale reads permitted without serialization;exact state Не доказаны provider/market/execution предпосылки; условная математика не operational guarantee. |
| 8 Proof/counterexample | Both readFree50/r and request30;both local inequalities pass,but combined60>50. Serialized/CAS commit leaves20/r+1 and rejects second stale writer. |
| 9 Far BUY / Far SELL | NOT_APPLICABLE: concurrency accounting, не направление позиции. |
| 10 Broker grid / rounding | Exact balance и bounded revision; overflow/restart ordering отдельно от CAS. |
| 11 Bid / Ask / costs | Сериализация не создаёт economic credit; costs определяют сам debit отдельно. |
| 12 Partial fills / actual data | Два stale debit30 на Free50 нельзя разрешить одновременно; один commit, второй conflict. |
| 13 Production mapping | Include/Core/HSBI_StateMachine.mqh:6–7 and Include/Persistence/HSBI_ExecutionJournal.mqh:21–29; durable concurrent backend NOT_IMPLEMENTED |
| 14 ERR / IMP / contracts | ERR-017/025/030/033; IMP-004/009 |
| 15 Final statuses | MATH=VALID_UNDER_ASSUMPTIONS; IMPLEMENTATION=NOT_IMPLEMENTED; scope limited to this relation, native NOT_RUN |

### HSBI-A03-F-066 — Связь счётчика snapshot и наличия объекта

**Источник:** Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:27–40; Docs/HSB.2C_Journal_Persistence_Reconciliation.md:5. **Статус:** UNDEFINED для нормативного смысла completedActionCount; SOURCE_CONTRADICTION условно, если count означает количество предъявленных completed actions.

При capacity1 этот смысл требует (count=1)⇔(completedIntent.intentId>0), а completed status/lastConfirmed IDs должны иметь независимые journal bindings. Existing activeIntentCount имеет аналогичный iff, completedActionCount — нет. Если count является иным историческим счётчиком, его связь и предел1 требуют отдельного объяснения; отсутствие iff нельзя скрыто исправить без schema contract. Безразмерные exact integers, domain0..1; направления/grid/costs неприменимы к этому логическому инварианту. Доказательство acceptance несогласованного DTO — ERR-050; успешное историческое расходование из него не следует. Связи F057/F060/F065, IMP-009/SNAP-FIXTURE-1.

### FINAL-CLOSURE — индивидуальные15 полей

| Field | Analysis |
|---|---|
| 1 Formula ID | HSBI-A03-F-066 |
| 2 Exact normative source | Docs/HSB.2C_Journal_Persistence_Reconciliation.md:5; snapshot meaning ADMIN_DECISION_REQUIRED |
| 3 Expression | If count is cardinality:(count=1) iff completed object exists |
| 4 Variables | count∈{0,1}; exists=(completedIntent.intentId>0); status/lastConfirmed IDs/journal — snapshot facts |
| 5 Dimensions | dimensionless logic/count plus declared lot/money facts |
| 6 Domain | count exact0..1;cardinality meaning not established by normative text |
| 7 Required assumptions | count exact0..1;cardinality meaning not established by normative text Предполагаются точные операции в объявленной области; broker authority не выводится из равенства. |
| 8 Proof/counterexample | Predicate bounds count and completed status but lacks iff. This demonstrates shape inconsistency only under cardinality interpretation,not unconditional economic defect. |
| 9 Far BUY / Far SELL | NOT_APPLICABLE: snapshot logical counter/body relation. |
| 10 Broker grid / rounding | Count exact0..1; schema meaning должен быть выбран независимо. |
| 11 Bid / Ask / costs | NOT_APPLICABLE: инвариант count не рассчитывает money/cost. |
| 12 Partial fills / actual data | Recovery reconstruction не историческая eligibility и не permission нового consumption. |
| 13 Production mapping | Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:27–40 |
| 14 ERR / IMP / contracts | ERR-050; IMP-009; SNAP-FIXTURE-1 |
| 15 Final statuses | MATH=UNDEFINED; IMPLEMENTATION=PARTIALLY_IMPLEMENTED; scope limited to this relation, native NOT_RUN |



## Обязательные общие уточнения к F001–F060

Для геометрических F001–006/F027–030/F037–039/F044–048/F050–052/F058 благоприятная координата u=s(P−P0), s=+1 для Far SELL и −1 для Far BUY. Денежная интерпретация требует конечного положительного K и единого symbol/currency basis; асимметричные tick values и расходы требуют broker valuation. Объём нормализуется по явно выбранному origin, затем min/max, активность каждой ноги и все gates повторяются. Lot slope не является суммой денег.

Для денежных F007–026/F034–036/F040–043/F049/F053–057/F060 signed components, posting grid, distinct cost basis и независимая история обязательны. Частичный fill — самостоятельная подтверждённая запись с принадлежностью batch; расчёт по planned volume не actual settlement. Утверждение local partition не расширяется до global funding или broker authenticity. Для F031–033 account-specific margin/risk domain обязателен; standalone margin sum не доказана фактической account margin. Для F037–038/F058–059 uniform quantifier, terminal feasibility и market/execution assumptions раздельны.

Историческая оговорка COVERAGE-COMPLETION: тогда15 индивидуальных полей ещё не были завершены. В FINAL-CLOSURE таблицы добавлены для66 семейств; полный просмотр исторических machine contracts и обязательных callers остаётся незавершённым, AUDIT_COMPLETENESS=PARTIAL.

Исторический счёт COVERAGE-COMPLETION (заменён текущим двухосным срезом выше): 66 семейств; 47 MATHEMATICALLY_VALID_UNDER_ASSUMPTIONS, 3 NORMATIVE_CONTRADICTION, 2 MATHEMATICALLY_FALSE, 6 UNVERIFIED, 7 UNDEFINED, 1 NOT_IMPLEMENTED. SOURCE_CONTRADICTION считается отдельно как production mapping. F066 не повышается до безусловного нормативного дефекта при неизвестной семантике count.

## FINAL-CLOSURE — переоценка двух осей и итог карточек

Все66 ранее присвоенных IDs сохранены; каждой карточке добавлены собственные15 полей. Исторические исходные тексты/статусы выше сохранены. F039 CORRECTED: старое CONTRADICTORY описывало противоречие нормативов; универсальная формула P+tick для обоих зеркал математически FALSE. ERR-046 остаётся нормативной CONTRADICTION. F041 CORRECTED: прежнее NOT_IMPLEMENTED было implementation status, не math status; production settled domain пока UNDEFINED, implementation NOT_IMPLEMENTED. F030/F044/F045 source locators уточнены: Net находится в GeometrySolver, nearest overload и typed rounding различаются, полная level construction не найдена; DTO не считается реализацией.

FORMULAS_WITH_15_FIELDS=66. MATH counts: CONTRADICTORY=2, FALSE=3, UNDEFINED=8, UNVERIFIED=6, VALID_UNDER_ASSUMPTIONS=47. Это оформление и индивидуальный математический разбор, не доказательство полноты всех ещё непрочитанных контрактов и не native tests. AUDIT_COMPLETENESS остаётся PARTIAL до остальных обязательств.

## FORMULA_STATUS_RECONCILIATION — R2

Сравнение выполнено с неизменённым Git blob базового FORMULA_CATALOG (b4d8f1ea5caf492f3abd030e5502d40582c52dc8). Все66 IDs сопоставлены текстово, без исполнения формул. Старые VERIFIED_UNDER_ASSUMPTIONS и MATHEMATICALLY_VALID_UNDER_ASSUMPTIONS нормализованы в VALID_UNDER_ASSUMPTIONS; INVALID/MATHEMATICALLY_FALSE в FALSE; CONTRADICTORY/NORMATIVE_CONTRADICTION в CONTRADICTORY. NOT_IMPLEMENTED относится к implementation, не математической оси. После нормализации изменились только2ID; остальные64 сохранили математический смысл классификации.

| ID | Старый статус | Новый MATH / implementation | Причина и доказательство | Источник / ERR / IMP | Решение администратора |
|---|---|---|---|---|---|
| F039 | CONTRADICTORY / NORMATIVE_CONTRADICTION | FALSE / CALLER_NOT_VERIFIED | Утверждение о росте RecoveryMoney(P+tick) в обоих mirrors ложно уже в линейной модели: Far BUY F1, противоположные Core2/Trend1,Small1 дают slopeLots1 по благоприятному движению вниз. При K>0 и росте P на tick money меняется на −K·tick. Far SELL зеркально растёт. Противоречие документов остаётся отдельным фактом, а universal inequality имеет контрпример. | Docs/05_GEOMETRY_MODEL_RU.md:22; Docs/03_FULL_SYSTEM_MANUAL_RU.md:12; ERR046; IMP007/021 | Контрпример не требует approval; исправление нормативной координаты/production — отдельное решение. |
| F041 | NOT_IMPLEMENTED (смешанная ось) | UNDEFINED / NOT_IMPLEMENTED | Неопределён именно утверждённый settled numeric profile: units/scale/ranges/codec/conversion. Абстрактная checked int64 arithmetic при явных bounds математически определена; её не объявляем ложной. Отсутствие implementation не отдельный math bucket. | NUM-EXACT-1/NUM-DOMAIN-1/MQL-DOMAIN; Docs/NEXT_STAGE_02B_R0E_NUMERIC_ARCHITECTURE_RU.md; ERR040; IMP002/018 | Требуется выбор администратора и в будущем разрешённые native evidence; сейчас pending. |

Итого старая смешанная сводка47valid/2false/3contradictory/6unverified/7undefined/1notimplemented превращается в47valid/3false/2contradictory/6unverified/8undefined; количество66 неизменно. Никакой historical evidence не изменён и ни один ID не удалён. Реализация оценивается отдельно.

Структурно все66 таблиц имеют15 непустых полей. Новые тексты индивидуальны по variables/direction/grid/cost/actual scope; это не повышение unknown authority/implementation до PROVEN. Полный review всех связанных исторических contracts ещё не завершён; FORMULA_STATUS_RECONCILIATION_COMPLETE=YES относится только к согласованию таксономии и2изменений.
