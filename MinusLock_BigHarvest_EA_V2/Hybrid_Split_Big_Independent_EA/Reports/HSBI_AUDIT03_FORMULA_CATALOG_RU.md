# AUDIT03 — каталог формул и зависимостей

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

## HSBI-A03-F-002 — Trend floor(F*Rt), Rt>=0

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:9`. **Production операция/строки:** `Include/Money/HSBI_BasketMoneyEvaluator.mqh:15-16`; mapping **MISMATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** CONTRADICTORY.

**Переменные, размерности и область:** lot; Rt=0 included; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** При Rt0 математически T0. Документ требует каждый lot>=min, geometry допускает zero, money-leg требует positive. Нужна active-leg конвенция.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-015; HSBI-A03-IMP-007. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-003 — Small ceil(F*Rs)

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:9`. **Production операция/строки:** `Include/Planning/HSBI_BrokerGrid.mqh:27`; mapping **PARTIALLY_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** lot; F,Rs>0,step>0; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Из ceil: S-step<F*Rs<=S. Округление вверх увеличивает hedge/расходы, поэтому max/margin перепроверяются. Tolerance и overflow отдельно.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-040; HSBI-A03-IMP-002, HSBI-A03-IMP-007. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-004 — All active legs min<=V<=max and grid

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:9`. **Production операция/строки:** `Include/Planning/HSBI_GeometrySolver.mqh:32-33`; mapping **MISMATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** lot; active role,min>0,max>=min; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Membership в broker admissible set необходимо для исполнения. Core0 не active допустимый lot; положительный raw не доказывает post-round validity.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-014, HSBI-A03-ERR-015; HSBI-A03-IMP-007. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-005 — Bnet=C+T-S; D=Bnet-F

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:12`. **Production операция/строки:** `Include/Planning/HSBI_GeometrySolver.mqh:6-10`; mapping **MATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** lot; common symbol,linear same K; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Сложение signed volumes даёт Net для FarSELL. В favorable coordinate derivative=K*D, не безусловный рост денег во времени. См.F51.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-046, HSBI-A03-ERR-037; HSBI-A03-IMP-007, HSBI-A03-IMP-021. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-006 — ReserveShare*Bnet>F

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:15`. **Production операция/строки:** `Include/Money/HSBI_CatchUpModel.mqh:12`; mapping **MATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** lot; share dimensionless[0,1],same K; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Сравнение slopes reserve и Far применимо при одинаковой линейной базе, расстояниях и eligible policy. Не покрывает разные entry prices, costs или availability.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-043, HSBI-A03-ERR-033; HSBI-A03-IMP-010, HSBI-A03-IMP-004. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-007 — ActualDealNet=P+Swap+Commission+Fee

**Источник правила:** `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:6`. **Production операция/строки:** `Include/Money/HSBI_CostModel.mqh:13`; mapping **MATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** signed account currency; common deal/window; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Компоненты signed:60-2-7-1=50. Комиссия уже отрицательна и не меняет знак повторно. Подлинность и полнота history не следуют из суммы.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-022, HSBI-A03-ERR-033; HSBI-A03-IMP-014, HSBI-A03-IMP-004. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-008 — ProjectedNet=gross+swap+comm+fee-spread-slip-buffer

**Источник правила:** `Docs/24_BROKER_MONEY_MODEL_RU.md:7`. **Production операция/строки:** `Include/Money/HSBI_CostModel.mqh:18`; mapping **PARTIALLY_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money; signed actual components,nonnegative extra allowances; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Алгебра верна только при disjoint costs: сумма исходной выплаты и ещё не включённых signed charges/extra allowances. Actual settled result не равен forecast автоматически.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-022; HSBI-A03-IMP-014. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-009 — Every applicable CostID covered exactly once

**Источник правила:** `Docs/24_BROKER_MONEY_MODEL_RU.md:7`. **Production операция/строки:** `Include/Money/HSBI_CostModel.mqh:4-18`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** UNDEFINED.

**Переменные, размерности и область:** CostID,basis,window,currency,authority; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** В текущем scalar snapshot нет полного независимого набора обязательных расходов и overlap mapping. Bid/Ask profit уже может содержать spread. Список компонентов без basis не завершает proof.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-022; HSBI-A03-IMP-014. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-010 — RecoveryPL=RealizedCycleNet+sum OpenCloseNowNet

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:18`. **Production операция/строки:** `Include/Money/HSBI_MoneyTypes.mqh:9`; mapping **PARTIALLY_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money; disjoint realised/open sets,same cycle/currency; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Partition экономических cash flows даёт равенство. Allocation — подмножества realised, повторное прибавление Reserve удвоит прибыль. Граница InitialProfit отдельно F35.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-036, HSBI-A03-ERR-044; HSBI-A03-IMP-020. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-011 — Threshold=minProfit+execBuffer+moneyTolerance

**Источник правила:** `Docs/12_FINAL_CLOSE_SPECIFICATION_RU.md:7`. **Production операция/строки:** `Include/Money/HSBI_MoneyTypes.mqh:7-9`; mapping **PARTIALLY_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money; finite nonnegative terms; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Сумма однородна по размерности; PL>=threshold — planned gate. Passed unvalidated threshold и возможное повторное inclusion buffer требуют отдельного constructor/cost contract.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-044, HSBI-A03-ERR-022; HSBI-A03-IMP-020, HSBI-A03-IMP-014. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-012 — Committed sumGrants=EligibleNet

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:30`. **Production операция/строки:** `Include/Money/HSBI_AllocationLedgerTypes.mqh:7`; mapping **AMBIGUOUS**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** UNDEFINED.

**Переменные, размерности и область:** settled money; positive posted source,phase explicit; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Полное распределение требует равенства; partial preparation требует остатка. 10<=50 не доказывает полного распределения50. В старом типе нет достаточного phase mapping.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-006; HSBI-A03-IMP-003. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-013 — OriginalGrant=Consumed+Reserved+Free

**Источник правила:** `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:12,24`. **Production операция/строки:** `Include/Money/HSBI_AllocationLedgerTypes.mqh:5-7`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** settled money,each component>=0; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Это partition одного grant при disjoint state categories. Инвариант сохраняется операциями F53–F56, но не устанавливает независимую подлинность самого grant.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-005, HSBI-A03-ERR-006, HSBI-A03-ERR-033; HSBI-A03-IMP-003, HSBI-A03-IMP-004. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-014 — RemainingGross=Reserved+Free

**Источник правила:** `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:24`. **Production операция/строки:** `Include/Money/HSBI_MoneyState.mqh:4-5`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money; candidate mapping,not approved migration; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Из F13 RemainingGross=G-Consumed. При G50,C10,R15,Free25 remaining40; тратить можно25, а не40. Старое Remaining без owner/precision не мигрирует безопасно.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-006; HSBI-A03-IMP-003. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-015 — Consume d: 0<d<=Free; C+=d,Free-=d

**Источник правила:** `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:24`. **Production операция/строки:** `Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:47,63-70`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money; atomic source/allocation/owner/event authority; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Сумма C+Free сохраняется, Free неотрицательно. Проверка одного stale остатка недостаточна двум потребителям: нужны serialisation/CAS и replay receipt.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-007, HSBI-A03-ERR-008, HSBI-A03-ERR-017; HSBI-A03-IMP-004, HSBI-A03-IMP-009. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-016 — Equal allocation total != equal vector

**Источник правила:** `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:15`. **Production операция/строки:** `Include/Money/HSBI_AllocationLedgerTypes.mqh:8`; mapping **MISMATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** ordered money vector with purpose labels; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Векторы (50,0) и (0,50) имеют одинаковую сумму, но не равны покомпонентно. Payload event должен включать каждый bucket и policy.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-004; HSBI-A03-IMP-003. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-017 — Equal DealNet != equal immutable economic components

**Источник правила:** `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:6,15`. **Production операция/строки:** `Include/Money/HSBI_EconomicLedgerTypes.mqh:9`; mapping **MISMATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money/IDs; same source key; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Линейная сумма неинъективна: (P50,C0) и(P60,C-10) дают50. Полное equality необходимо независимо от итогового Net.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-001, HSBI-A03-ERR-002; HSBI-A03-IMP-001. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-018 — sum funding per source<=EligibleSourceNet

**Источник правила:** `Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md:3`. **Production операция/строки:** `Include/Money/HSBI_ReserveAllocationTypes.mqh:23`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** UNVERIFIED.

**Переменные, размерности и область:** settled money; global namespace,all allocations complete; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Две allocations50 одного source50 локально допустимы по отдельности, глобально100>50. Нужны complete registry и immutable source receipts, не только сумма одного DTO.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-033, HSBI-A03-ERR-017; HSBI-A03-IMP-004, HSBI-A03-IMP-009. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-019 — Consumption bound to authoritative remaining allocation

**Источник правила:** `Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md:5-7`. **Production операция/строки:** `Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:44-47,63-70`; mapping **MISMATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** UNVERIFIED.

**Переменные, размерности и область:** source/allocation/event/policy/revision,money; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Nonempty foreign key не связан с actual allocation. Source50 consumed50 больше не может дать reserve40. Текущее preview разрешение не является фактическим ledger debit.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-007, HSBI-A03-ERR-008; HSBI-A03-IMP-004. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-020 — AbsoluteFarLoss=max(0,-ProjectedCloseNowFarNet)

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:15`. **Production операция/строки:** `Include/Money/HSBI_BasketMoneyEvaluator.mqh:17`; mapping **MATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money; full position,close side,current volume; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Для net-50 magnitude50, для+10 magnitude0. Это current liquidation estimate, не гарантированный будущий execution loss; название increase не меняет absolute смысл.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-043; HSBI-A03-IMP-010. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-021 — IncrementalLoss=AbsoluteLoss-BaselineLoss

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:15`. **Production операция/строки:** `Include/Money/HSBI_BasketMoneyEvaluator.mqh:17`; mapping **AMBIGUOUS**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** UNDEFINED.

**Переменные, размерности и область:** money; same source,volume,basis,time contract; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** 50-40=10,но Reserve30 покрывает10,не50. Без stable baseline/volume change/restart contract incremental не взаимозаменяем с absolute. Loss magnitude и signed delta разные типы.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-043; HSBI-A03-IMP-010. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-022 — CatchUpMargin=EligibleReserve-Loss-Buffer>0

**Источник правила:** `Docs/24_BROKER_MONEY_MODEL_RU.md:9`. **Production операция/строки:** `Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:74-75`; mapping **PARTIALLY_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money; finite R,L,B>=0 and reconciled funds; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** 50-20-1=29; equality margin0 недостаточно при strict>. Если R projected, вывод только preview. Не доказывает finance/actual closing capacity.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-033, HSBI-A03-ERR-043; HSBI-A03-IMP-004, HSBI-A03-IMP-010. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-023 — min_i CatchUpMargin_i>0 vs argmax TransitionLoss

**Источник правила:** `Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md:5`. **Production операция/строки:** `Include/Planning/HSBI_FutureSmallProofAggregator.mqh:44,50`; mapping **AMBIGUOUS**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** UNDEFINED.

**Переменные, размерности и область:** money indexed by mandatory alternative levels; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Формальная all-level конъюнкция эквивалентна положительному минимуму конечного непустого набора, но выбор этого scope pending CR09. Trans10/M9 vsTrans5/M-11 опровергает замену минимума argmax другой функции.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-018; HSBI-A03-IMP-010. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-024 — CurrentTransitionLoss=max(0,-sum signed actual fills)

**Источник правила:** `Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md:9`. **Production операция/строки:** `Include/Money/HSBI_BasketMoneyEvaluator.mqh:17`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money; ordered confirmed same-batch fills; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** После -15,+100 signed sum85,currentloss0. Projected basket net не является authoritative actual transition batch. Membership/account/fees должны быть подтверждены отдельно.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-035, HSBI-A03-ERR-033; HSBI-A03-IMP-019, HSBI-A03-IMP-004. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-025 — Sticky breach / Peak loss policies

**Источник правила:** `Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md:20`. **Production операция/строки:** `LINE_NOT_VERIFIED`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** UNDEFINED.

**Переменные, размерности и область:** money,time/batch,reset policy; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Current loss15→0; peak15→15; breach cap12 true→true. Это разные функции истории. Не выбирать одну без владельца; отсутствие полной history означает UNAVAILABLE.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-035; HSBI-A03-IMP-019. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-026 — AllowedLoss=min(absolute,equity,oldrisk,cumulative caps)

**Источник правила:** `Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:15`. **Production операция/строки:** `Include/Planning/HSBI_NewFarSolver.mqh:74`; mapping **PARTIALLY_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money; all finite known same horizon; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Условие L<=каждого cap равносильно L<=min caps. Equity percent сначала переводится в money. NaN/unknown cap не безопасный ноль и не допустимый минимум.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-009, HSBI-A03-ERR-035; HSBI-A03-IMP-005, HSBI-A03-IMP-019. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-027 — CompressionLots=F-N; ratio=(F-N)/F

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:21`. **Production операция/строки:** `Include/Planning/HSBI_NewFarSolver.mqh:111`; mapping **MATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** lot and dimensionless; F>0,0<N<F; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** F1,N.6 дают.4lot и.4ratio. Формула определена только при положительном F и actual/planned scope не смешивается.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-045; HSBI-A03-IMP-011. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-028 — N<=MaximumNewFarRatio*F

**Источник правила:** `Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:13`. **Production операция/строки:** `Include/Planning/HSBI_NewFarSolver.mqh:112`; mapping **MATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** lot; ratio in(0,1),post-round values; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Умножение не меняет размерность. Это отдельное ограничение не доказывает цену/стоимость/feasible next basket. Кандидат выше actual Core residual не promotion.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-045, HSBI-A03-ERR-032; HSBI-A03-IMP-011, HSBI-A03-IMP-013. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-029 — NextBigGross<OldBigGross

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:21`. **Production операция/строки:** `Include/Planning/HSBI_FutureSmallSolver.mqh:90,143`; mapping **MISMATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** lot; same Big-leg set; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Next C.7,T.5,S1 givesBigGross1.2,Net.2; oldGross1. Net comparison проходит, требуемый gross нет. Один тип lot не делает величины экономически тождественными.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-020; HSBI-A03-IMP-012. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-030 — Gross=sum abs volumes; Net=sum signed volumes

**Источник правила:** `Docs/01_GLOSSARY_AND_DIMENSIONS_RU.md:1-56`. **Production операция/строки:** `Include/Money/HSBI_BasketMoneyEvaluator.mqh:17`; mapping **MATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** lot; actual same-symbol direction; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** BUY2.2,SELL1.5 даютGross3.7,Net+.7. При зеркале Gross тот же,Net-.7. Margin и risk не определяются одним Net.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-020, HSBI-A03-ERR-041; HSBI-A03-IMP-012, HSBI-A03-IMP-022. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-031 — RiskNext<RiskOld-Tolerance

**Источник правила:** `Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:12`. **Production операция/строки:** `Include/Risk/HSBI_FutureSmallRiskEvaluator.mqh:29-50`; mapping **NOT_VERIFIED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** UNVERIFIED.

**Переменные, размерности и область:** money/risk unit; same adverse basis and horizon; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Неравенство осмысленно лишь для одинаковой модели. Уменьшение lot не доказывает уменьшение loss при новом basis/volatility/entry. Нужна независимая risk authority, не copied snapshot flag.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-037, HSBI-A03-ERR-038; HSBI-A03-IMP-021. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-032 — TotalAccountMargin=sum standalone leg margins

**Источник правила:** `Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:9`. **Production операция/строки:** `Include/Money/HSBI_BasketMoneyEvaluator.mqh:17`; mapping **PARTIALLY_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** UNVERIFIED.

**Переменные, размерности и область:** account money; hedging/tiers/other positions; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Равенство не теорема для любого broker. Сумма независимых OrderCalcMargin может быть estimator; required margin whole-account и max prefix должны иметь иной доказанный контракт.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-034; HSBI-A03-IMP-015. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-033 — MarginLevel=100*Equity/Margin

**Источник правила:** `Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:6`. **Production операция/строки:** `LINE_NOT_VERIFIED`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** percent; Margin>0,same currency; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Отношение однородных money безразмерно, множитель100 даёт%. При Margin0 формула не определена: нужна broker/account convention. Stopout/negative equity не игнорируются.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-034; HSBI-A03-IMP-015. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-034 — Equity=Balance+FloatingNet

**Источник правила:** `Docs/01_GLOSSARY_AND_DIMENSIONS_RU.md:1-56`. **Production операция/строки:** `LINE_NOT_VERIFIED`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money; broker-consistent accrued charge basis; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Реализация прибыли переводит floating в balance, не создавая equity. Balance1000,realized+10,floating-20 даёт equity990, несмотря на рост Balance до1010. Credit/charges требуют account mapping.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-036; HSBI-A03-IMP-020. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-035 — EconomicCyclePnL=AllRealized+OpenLiquidationNet

**Источник правила:** `Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md:20; Docs/04_MATHEMATICAL_MODEL_RU.md:18`. **Production операция/строки:** `Include/Money/HSBI_MoneyTypes.mqh:9`; mapping **AMBIGUOUS**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money; common cycle start,disjoint costs; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Partition по закрытым/открытым cash flows: Harvest10 и remaining net-20 даютCycle-10. InitialProfit exclusion меняет метрику, не полную экономику. Reserve не третий доход.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-036, HSBI-A03-ERR-022; HSBI-A03-IMP-020, HSBI-A03-IMP-014. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-036 — Nonfinite/unknown cannot pass money/risk/outcome gate

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:42`. **Production операция/строки:** `Include/Risk/HSBI_RiskGateResult.mqh:6; Include/Execution/HSBI_TransactionTypes.mqh:15`; mapping **MISMATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** finite typed DTO domain; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Ordered comparison с NaN не является доказательством диапазона. Предварительный finite/domain guard необходим до суммы, разности и выбора min/max.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-009, HSBI-A03-ERR-010, HSBI-A03-ERR-011; HSBI-A03-IMP-005. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-037 — K>=ceil(log(Vmin/F0)/log(q))

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:36`. **Production операция/строки:** `Include/Planning/HSBI_FutureSmallSolver.mqh:5-10`; mapping **PARTIALLY_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** steps; F0>=Vmin>0,0<q<1; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Из q^K*F0<=Vmin, после деления на logq<0 знак меняется: K>=log(Vmin/F0)/logq. Ceil даёт sufficient integer bound при uniform rounded contraction. step должен входить в discrete feasibility, не только в input shape.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-032, HSBI-A03-ERR-031; HSBI-A03-IMP-013. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-038 — Finite prefix implies uniform geometric future bound

**Источник правила:** `Docs/27_FUTURE_SMALL_SOLVER_RU.md:5`. **Production операция/строки:** `Include/Planning/HSBI_FutureSmallSolver.mqh:12-16,146-147`; mapping **MISMATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** INVALID.

**Переменные, размерности и область:** quantifier over all future reachable levels; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Импликация без invariant assumptions ложна:1,.8,.64 согласованы сq.8,но следующий.64>.512. Требование uniform assumptions в документе корректно; invalid именно попытка вывести forall из конечного наблюдения.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-021; HSBI-A03-IMP-013. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-039 — RecoveryMoney(P+tick)>RecoveryMoney(P) both mirrors

**Источник правила:** `Docs/03_FULL_SYSTEM_MANUAL_RU.md:12; Docs/26_GEOMETRY_ENGINE_SPECIFICATION_RU.md:7`. **Production операция/строки:** `Include/Planning/HSBI_GeometrySolver.mqh:12-19`; mapping **AMBIGUOUS**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** CONTRADICTORY.

**Переменные, размерности и область:** money; finite price on tick grid; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** FarBUY зеркало требует P-tick. Положительный D не меняет эту направленность. Одна пара цен не доказывает весь диапазон и все stress paths.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-046, HSBI-A03-ERR-037; HSBI-A03-IMP-007, HSBI-A03-IMP-021. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-040 — PartialClose=floor_grid(Budget/LossPerLot)

**Источник правила:** `Docs/11_PARTIAL_FAR_SPECIFICATION_RU.md:7`. **Production операция/строки:** `Include/Scenarios/HSBI_PartialFarTypes.mqh:4`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** lot; money/(money/lot),L>0,disjoint fixed costs; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** При constant per-lot loss и без fixed fees rounding down даётcost<=budget. Ограничить volume<=Far и остаток0 либо>=min. Actual costs после fill сверяются; fee/slippage нарушают простую пропорцию.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-022, HSBI-A03-ERR-032; HSBI-A03-IMP-014, HSBI-A03-IMP-013. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-041 — Checked signed int64 settled arithmetic

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:42`. **Production операция/строки:** `Include/Money/HSBI_MoneyState.mqh:4-5`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** NOT_IMPLEMENTED.

**Переменные, размерности и область:** minor units, -2^63..2^63-1; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** При x=MAX,d=1 сумма вне signed domain; при проверке x<=MAX-d переполнение самого промежуточного выражения также исключается. Reference unlimited integers не дают это свойство production double.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-040; HSBI-A03-IMP-002. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-042 — F64Z/T17Z canonical numeric identity

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:42; NUM-CODEC proposal`. **Production операция/строки:** `Include/Money/HSBI_EconomicLedgerTypes.mqh:11`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** UNVERIFIED.

**Переменные, размерности и область:** bytes,schema,currency,finite numeric fields; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Нужны fixed field order,type tags,lengths,endian/zero/NaN policy и независимый decoder. Восьмизначная диагностика не canonical full record. Native goldens этим этапом не выполнялись.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-003, HSBI-A03-ERR-029; HSBI-A03-IMP-002, HSBI-A03-IMP-018. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-043 — Small decrements remain exact near 10^28

**Источник правила:** `NUM-EXACT-1 proposal; Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:24`. **Production операция/строки:** `Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:74`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** exact rational/decimal money,admitted finite domain; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** В рациональных числах 10^28-.01 отличается от10^28. В bounded binary64 spacing на таком масштабе намного больше. Это не допускает автоматического принятия10^28 как MQL settled domain.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-040; HSBI-A03-IMP-002. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-044 — NormalizePrice=round(price/tickSize)*tickSize

**Источник правила:** `Docs/25_BROKER_GRID_AND_ROUNDING_RU.md:5`. **Production операция/строки:** `Include/Planning/HSBI_ControlPrices.mqh:12`; mapping **PARTIALLY_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** price; tick>0,defined tie policy; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** При точных reals ошибка ближайшей сетки<=tick/2. Округление execution trigger может требовать directional floor/ceil, не ближайший tick; преобразование Point и TickSize не тождественно.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-039, HSBI-A03-ERR-040; HSBI-A03-IMP-007, HSBI-A03-IMP-002. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-045 — Level=Reference+s*(Start+(k-1)*Step)*Point

**Источник правила:** `Docs/05_GEOMETRY_MODEL_RU.md:19`. **Production операция/строки:** `Include/Planning/HSBI_ControlPrices.mqh:LINE_NOT_VERIFIED`; mapping **NOT_VERIFIED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** price; Start,Step in points,k>=1; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Скобка в points, умножение на Point даёт price; s задаёт сторону. После tick normalization уровни могут совпасть; gap через несколько уровней не означает несколько actual fills.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-037, HSBI-A03-ERR-039; HSBI-A03-IMP-021, HSBI-A03-IMP-007. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-046 — BUY closes Bid; SELL closes Ask

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:39`. **Production операция/строки:** `Include/Money/HSBI_BasketMoneyEvaluator.mqh:14`; mapping **PARTIALLY_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** price; bid<=ask,finite fresh quotes; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** BUY liquidation продаёт поBid,SELL выкупается поAsk. Entry BUY поAsk,SELL поBid. Broker commissions/FX/costs отдельны, side alone не обещает executable fill.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-022, HSBI-A03-ERR-037; HSBI-A03-IMP-014, HSBI-A03-IMP-021. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-047 — Minimum-safe N vs global risk-first objective

**Источник правила:** `Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:22-23; Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md:3`. **Production операция/строки:** `Include/Planning/HSBI_NewFarCandidate.mqh:33-40`; mapping **AMBIGUOUS**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** CONTRADICTORY.

**Переменные, размерности и область:** lot/risk/margin lexicographic tuple; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Candidate(.1,risk10) и(.2,risk5) выбираются по-разному. Нельзя называть глобальный risk-first tie-break равных minimum-safe N. Требуется approval precedence.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-019; HSBI-A03-IMP-011. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-048 — Grid n*step vs Vmin+n*step

**Источник правила:** `Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:9; Docs/25_BROKER_GRID_AND_ROUNDING_RU.md:5`. **Production операция/строки:** `Include/Planning/HSBI_BrokerGrid.mqh:36`; mapping **AMBIGUOUS**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** UNDEFINED.

**Переменные, размерности и область:** lot; origin,min,max,step>0; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Эквивалентность требует Vmin/step integer. Для.03/.02 origins расходятся. Брокер может запретить такую конфигурацию, но это отдельный admission contract.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-039; HSBI-A03-IMP-007. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-049 — round(sum components) vs sum(round components)

**Источник правила:** `Docs/HSB_2E_FORMULA_CONTRACTS_R2_RU.md:7-34`. **Production операция/строки:** `Include/Money/HSBI_CostModel.mqh:13`; mapping **AMBIGUOUS**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money,declared scale/rounding policy; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** При digits2,nearest half-up два компонента.004+.004 дают aggregate.008→.01; индивидуально0+0=0. Операции не коммутируют. Документ предписывает aggregation-before-rounding, но broker component posting domain и settlement grid ещё должны быть утверждены.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-040, HSBI-A03-ERR-022; HSBI-A03-IMP-002, HSBI-A03-IMP-014. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-050 — Equal-volume Initial Lock PnL=-L*K*(spread0+spread_t)

**Источник правила:** `Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md:6-20`. **Production операция/строки:** `Hybrid_Split_Big_Independent_EA.mq5:35-39`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money; constant K,simultaneous equal legs,fees separate; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** BUY=L(Bid_t-Ask_0)K,SELL=L(Bid_0-Ask_t)K. Сумма после группировки минус двух spreads. Mid movement сокращается, costs ухудшают результат. При spread1,LK1 итог-2 без дополнительных fees.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-036, HSBI-A03-ERR-042; HSBI-A03-IMP-020, HSBI-A03-IMP-021. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-051 — Favorable coordinate u=s(P-P0); dPi/du=K*(C+T-S-F)

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:12,39; Docs/26_GEOMETRY_ENGINE_SPECIFICATION_RU.md:7`. **Production операция/строки:** `Include/Planning/HSBI_GeometrySolver.mqh:10`; mapping **PARTIALLY_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money/price; K>0 common constant,spread/cost fixed; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** FarSELL s+1 signed netD;FarBUY s-1 signed net-D. Умножение dP/du=s даётKD для обоих. При K(P) и changing costs производная иная; lot slope остаётся фильтром.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-046, HSBI-A03-ERR-037; HSBI-A03-IMP-007, HSBI-A03-IMP-021. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-052 — Transition prefix Net: D→C+T-F→C+T→C→N

**Источник правила:** `Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md:12-14`. **Production операция/строки:** `LINE_NOT_VERIFIED`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** lot; full closes in fixed order; FarSELL mirror negates Net; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Прямое вычитание закрытой signed leg: SmallSELL close добавляет S кNet;FarSELL close добавляетF. C1.2,T1,S.5,F1,N.6 дают.7,1.2,2.2,1.2,.6. Gross монотонно падает,Net временно растёт.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-041; HSBI-A03-IMP-022. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-053 — Reserve d:(R,Free)→(R+d,Free-d)

**Источник правила:** `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:24`. **Production операция/строки:** `LINE_NOT_VERIFIED`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** settled money;0<d<=Free,owner/event explicit; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Сумма R+Free неизменна,неотрицательность из предусловия. Owner reservation не равна consumed; повторная чужая reservation не использует тот же free.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-007, HSBI-A03-ERR-033; HSBI-A03-IMP-004. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-054 — Release owner d:(R,Free)→(R-d,Free+d)

**Источник правила:** `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:24`. **Production операция/строки:** `LINE_NOT_VERIFIED`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money;d<=that owner reserved balance; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Сумма сохранена. Общего R>=d недостаточно: средства могут принадлежать другому owner. Нужен receipt reservation identity и exact replay.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-007, HSBI-A03-ERR-017; HSBI-A03-IMP-004, HSBI-A03-IMP-009. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-055 — Unreserved consume d:(C,Free)→(C+d,Free-d)

**Источник правила:** `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:24`. **Production операция/строки:** `LINE_NOT_VERIFIED`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money;0<d<=Free,complete reconciled journal; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Плюс d и минус d сокращаются в G. Прогноз, Unallocated и ResidualHeld не подставляются вFree без отдельного eligibility policy.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-033, HSBI-A03-ERR-006; HSBI-A03-IMP-004, HSBI-A03-IMP-003. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-056 — Reserved owner consume d:(C,R)→(C+d,R-d)

**Источник правила:** `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:24`. **Production операция/строки:** `LINE_NOT_VERIFIED`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money;same owner/reservation,0<d<=owner R; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** G сохраняется,Free не меняется. Нельзя одновременно списать d из R и Free или оставить reservation доступным после расхода.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-007, HSBI-A03-ERR-017; HSBI-A03-IMP-004, HSBI-A03-IMP-009. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-057 — Exact replay delta0; changed replay CONFLICT

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:30; Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md:6-21`. **Production операция/строки:** `Include/Persistence/HSBI_ExecutionJournal.mqh:21-29`; mapping **MISMATCH**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** event key+full immutable payload+durable receipt; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Доказательство exact idempotency требует прежний полный payload, не только заявленный digest. Повтор изменённого компонента не NO_OP. Существование local equality не доказывает durable/concurrent once.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-001, HSBI-A03-ERR-004, HSBI-A03-ERR-030, HSBI-A03-ERR-017; HSBI-A03-IMP-001, HSBI-A03-IMP-003, HSBI-A03-IMP-009. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-058 — Uniform contraction implies F_k<=q^k*F_0

**Источник правила:** `Docs/04_MATHEMATICAL_MODEL_RU.md:33-36`. **Production операция/строки:** `Include/Planning/HSBI_FutureSmallSolver.mqh:142-147`; mapping **PARTIALLY_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** lot;forall reachable transitions,q in(0,1),rounded states; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** База k0 equality. Шаг: F(k+1)<=qF(k)<=q*q^kF0=q^(k+1)F0. Доказательство условно: не доказывает existence/execution следующего transition и terminal closure.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-021, HSBI-A03-ERR-032; HSBI-A03-IMP-013. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-059 — Unhedged SELL adverse loss=F*K*(P-Popen)

**Источник правила:** `Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:6-18`. **Production операция/строки:** `LINE_NOT_VERIFIED`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** VERIFIED_UNDER_ASSUMPTIONS.

**Переменные, размерности и область:** money;F,K>0 linear payout,P>=Popen; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Для любого boundB можно выбрать P>Popen+B/(FK), тогдаloss>B. Это опровержение безусловного bound при данных assumptions; ограниченный price/liability domain требует отдельного доказательства и не исключается.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-038; HSBI-A03-IMP-021. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## HSBI-A03-F-060 — Projected→Actual→Reconciled→Eligible→Available are distinct transformations

**Источник правила:** `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:6-24; Docs/31_MONEY_PROOF_IDENTITY_RU.md:5`. **Production операция/строки:** `Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:24-28`; mapping **NOT_IMPLEMENTED**. Если LINE_NOT_VERIFIED, точный executable counterpart не установлен и не выдумывается. **Статус:** UNVERIFIED.

**Переменные, размерности и область:** typed money with authority,currency,scope,owner; остальные обозначения в общем словаре. **Назначение:** проверить именно указанное выражение/преобразование в соответствующей стадии денежного/позиционного цикла.

**Ручной вывод, границы или контрпример:** Каждая стрелка добавляет независимые факты, а не просто копирует scalar100. Если нет deals, projected100 не grants100. Unknown history не известный ноль; full empty history может доказывать отсутствие funds.

**Зависимости и проверка согласованности:** HSBI-A03-ERR-033, HSBI-A03-ERR-013; HSBI-A03-IMP-004, HSBI-A03-IMP-001. Нельзя переносить вывод за указанные finite/grid/authority/cost/market assumptions. При их отсутствии scope становится UNVERIFIED/UNAVAILABLE, а не автоматически безопасным нулём. Проверка native/broker данным документом не выполнялась.

## Сводка статусов

CONTRADICTORY=3, INVALID=1, NOT_IMPLEMENTED=1, UNDEFINED=6, UNVERIFIED=6, VERIFIED_UNDER_ASSUMPTIONS=43.

UNVERIFIED в итоговом машинном блоке включает UNVERIFIED+UNDEFINED+NOT_IMPLEMENTED, чтобы сумма категорий равнялась FORMULAS_TOTAL. Production mapping — независимая ось: условно верная алгебра может иметь MISMATCH в исходнике. Наличие этих 60 семейств не доказывает, что все формулы всех исторических приложений обнаружены: документальное покрытие PARTIAL.


## COVERAGE-COMPLETION — новые отношения и уточнение классификации

Исходные F001–F060 и их исторические статусы сохранены выше. Современные имена статусов: VERIFIED_UNDER_ASSUMPTIONS → MATHEMATICALLY_VALID_UNDER_ASSUMPTIONS; CONTRADICTORY → NORMATIVE_CONTRADICTION; INVALID → MATHEMATICALLY_FALSE. SOURCE_CONTRADICTION — отдельная ось соответствия реализации, а не дополнительная формула в сумме. UNDEFINED означает отсутствующий выбор нормы, UNVERIFIED — отсутствующее доказательство сформулированного свойства. NOT_IMPLEMENTED не заменяется PASS корректной алгебры.

### HSBI-A03-F-061 — Мгновенный объём не равен обороту за время

**Источник:** Docs/02_SYSTEM_ROLES_AND_IDENTITY_RU.md:6–20; Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:6–24; Include/Core/HSBI_Context.mqh:19–24,48–53. **Статус:** MATHEMATICALLY_VALID_UNDER_ASSUMPTIONS. **Production mapping:** PARTIALLY_IMPLEMENTED / ERR-012.

Пусть в один момент существует не более четырёх уникальных собственных позиций, каждая объёмом не более Vmax. Тогда TotalGross(t)=Σ|Vj(t)|≤4Vmax. Это lot, не money. Необходимы один symbol/учёт виртуальных legs, отсутствие pending overfill, глобальный position inventory и применимость broker max к каждой позиции. Для обоих направлений модуль одинаков. Grid уменьшает множество допустимых объёмов, но сам не ограничивает число повторных открытий. При каждом из n повторов открыть и закрыть v>0 lot оборот уже 2nv; при n→∞ он неограничен, даже если мгновенный Gross≤4Vmax. Costs и частичные fills учитываются по actual обороту. Нельзя из ограничения мгновенного объёма вывести ограничение суммарных комиссий, убытка или времени. Связи F030/F052/F058/F059; ERR-032/038/042; IMP-013/021. Не доказано, что current source гарантирует все перечисленные предусловия.

### HSBI-A03-F-062 — Учёт fills и точное завершение

**Источник:** Tests/Contracts/HSB_2E_R4_R9_R4A_R12A_NORMATIVE_DECISIONS.md:27–31. **Статус:** MATHEMATICALLY_VALID_UNDER_ASSUMPTIONS. **Область:** исторический static qualification contract, не production settlement. **Production:** Include/Execution/HSBI_TransactionTypes.mqh:15 / неполная интеграция.

Для одного intent I: Filled(I)=Σ уникальных подтверждённых, принадлежащих I и ticket сделок; Remaining(I)=Requested(I)−Filled(I), 0≤Filled≤Requested. Объёмы lot, Requested>0 finite, каждый fill>0 на объявленной step-сетке, membership/history complete. BUY/SELL меняют денежный результат, не равенство объёмов. Zero remaining обязателен для полного исполнения, но не для PARTIAL. Deal ID uniqueness без полного immutable equality недостаточна; неизвестная history не даёт Remaining=0. Bid/Ask, комиссия и slippage требуют отдельной фактической денежной сверки, а не усреднения плановой цены. Связи F007/F024/F036/F057; ERR-010/017/030; IMP-005/008/009.

### HSBI-A03-F-063 — Равенство множеств intent IDs не доказывает полного fill

**Источник:** тот же R12A документ:19–31. **Статус:** MATHEMATICALLY_FALSE для импликации SetEquality⇒ExactSettlement. **Production mapping:** соответствующая полноценная связанная интеграция NOT_VERIFIED.

Пусть expected IDs={I1}, Requested(I1)=1 lot, observed deal D1 принадлежит I1, confirmed, volume=.4. Тогда observed IDs={I1}, множества равны, но Remaining=.6. Это ручной контрпример для BUY и SELL; step=.1, все объёмы on-grid. Расходы не устраняют недостающий объём. Строка31 прямо требует exact settlement; поэтому полный норматив читается как conjunction: set/batch/confirmation/uniqueness И ∀I Filled(I)=Requested(I). Нельзя объявить весь документ противоречивым только по изолированной строке25; нельзя также исполнить только её set equality. Связи F062/F057; ERR-010/016/028, IMP-008/017. Проверка всех исторических evaluator callers этого conjunction ещё не завершена; автоматический новый SOURCE_DEFECT не присвоен.

### HSBI-A03-F-064 — Целочисленное распределение с остатком

**Источник:** Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:12–24; Include/Money/HSBI_AllocationPolicyTypes.mqh:16–23; Include/Money/HSBI_AllocationLedgerTypes.mqh:6–10. **Статус:** MATHEMATICALLY_VALID_UNDER_ASSUMPTIONS. **Production mapping:** SOURCE_CONTRADICTION для negative buckets, не для policy transitionShare.

Пусть N≥0 — settled minor units, 0≤si≤1, Σsi≤1. Выдать bi=floor(Nsi), а residual=N−Σbi. Тогда каждый bi≥0, residual≥0, Σbi+residual=N. Направления/lot grid неприменимы непосредственно: деньги имеют собственную currency/scale lattice. Нужны точные произведения/checked intermediates; округление каждого bi вверх может нарушить бюджет: N=1, shares .5/.5, ceil даёт2. Signed broker components сначала сверяются по утверждённой posting policy; нельзя делить projected или отрицательный DealNet как положительный grant. На N=0 гранты0. Costs уже в N не вычитаются повторно; partial fills создают факты лишь после reconciliation. Связи F007/F012–016/F049, ERR-005/006/022, IMP-002/003. Policy validator уже проверяет transitionShare≥0; снятая гипотеза отмечена в реестре.

### HSBI-A03-F-065 — Проверка revision не является атомарным commit

**Источник:** Docs/16_PERSISTENCE_AND_RESTART_RU.md:6–21; Docs/HSB.2C_Journal_Persistence_Reconciliation.md:3–7; Include/Core/HSBI_StateMachine.mqh:6–7; Include/Persistence/HSBI_ExecutionJournal.mqh:21–29. **Статус:** MATHEMATICALLY_VALID_UNDER_ASSUMPTIONS для необходимости единой сериализации competing transitions; production durable/concurrent enforcement NOT_IMPLEMENTED.

Free=50, revision=r. A и B независимо читают эти же значения и запрашивают30. Оба локальных условия30≤50 истинны. Два разрешения не доказывают, что60≤50; требуется атомарное сравнение revision и запись balances+receipts либо эквивалентная сериализуемая транзакция. При CAS один commit делает Free20,r+1; второй получает conflict и zero delta. Даже корректная in-memory последовательная функция не доказывает crash durability или multi-process ordering. Денежные единицы едины; r безразмерный ограниченный ID с проверкой переполнения. BUY/SELL, grid и costs не заменяют backend ordering; actual debit определяется отдельно. Связи F013–019/F053–057; ERR-017/025/030/033; IMP-004/009. Это аналитическая интерливинг-схема, конкурентный тест не запускался.

### HSBI-A03-F-066 — Связь счётчика snapshot и наличия объекта

**Источник:** Include/Persistence/HSBI_ExecutionStateSnapshot.mqh:27–40; Docs/HSB.2C_Journal_Persistence_Reconciliation.md:5. **Статус:** UNDEFINED для нормативного смысла completedActionCount; SOURCE_CONTRADICTION условно, если count означает количество предъявленных completed actions.

При capacity1 этот смысл требует (count=1)⇔(completedIntent.intentId>0), а completed status/lastConfirmed IDs должны иметь независимые journal bindings. Existing activeIntentCount имеет аналогичный iff, completedActionCount — нет. Если count является иным историческим счётчиком, его связь и предел1 требуют отдельного объяснения; отсутствие iff нельзя скрыто исправить без schema contract. Безразмерные exact integers, domain0..1; направления/grid/costs неприменимы к этому логическому инварианту. Доказательство acceptance несогласованного DTO — ERR-050; успешное историческое расходование из него не следует. Связи F057/F060/F065, IMP-009/SNAP-FIXTURE-1.

## Обязательные общие уточнения к F001–F060

Для геометрических F001–006/F027–030/F037–039/F044–048/F050–052/F058 благоприятная координата u=s(P−P0), s=+1 для Far SELL и −1 для Far BUY. Денежная интерпретация требует конечного положительного K и единого symbol/currency basis; асимметричные tick values и расходы требуют broker valuation. Объём нормализуется по явно выбранному origin, затем min/max, активность каждой ноги и все gates повторяются. Lot slope не является суммой денег.

Для денежных F007–026/F034–036/F040–043/F049/F053–057/F060 signed components, posting grid, distinct cost basis и независимая история обязательны. Частичный fill — самостоятельная подтверждённая запись с принадлежностью batch; расчёт по planned volume не actual settlement. Утверждение local partition не расширяется до global funding или broker authenticity. Для F031–033 account-specific margin/risk domain обязателен; standalone margin sum не доказана фактической account margin. Для F037–038/F058–059 uniform quantifier, terminal feasibility и market/execution assumptions раздельны.

Эта групповая оговорка не выдаётся за завершённые 15 индивидуальных полей каждого семейства. Детальная field-by-field матрица и полный просмотр исторических machine contracts остаются в списке незавершённого охвата; AUDIT_COMPLETENESS сохраняет PARTIAL.

Текущий непересекающийся счёт: 66 семейств; 47 MATHEMATICALLY_VALID_UNDER_ASSUMPTIONS, 3 NORMATIVE_CONTRADICTION, 2 MATHEMATICALLY_FALSE, 6 UNVERIFIED, 7 UNDEFINED, 1 NOT_IMPLEMENTED. SOURCE_CONTRADICTION считается отдельно как production mapping. F066 не повышается до безусловного нормативного дефекта при неизвестной семантике count.
