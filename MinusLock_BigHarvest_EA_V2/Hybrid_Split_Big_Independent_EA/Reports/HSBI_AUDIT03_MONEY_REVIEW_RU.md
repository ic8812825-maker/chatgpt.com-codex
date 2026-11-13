# AUDIT03 — денежная модель и границы доказательства

Это ручной документальный анализ. Числовые выражения ниже выведены в тексте, не исполнены. [Каталог формул](HSBI_AUDIT03_FORMULA_CATALOG_RU.md), [ошибки](HSBI_AUDIT03_ALL_ERRORS_RU.md), [предложения](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md) — единственные источники ID.

## Денежные типы

| Величина | Основание | Не доказывает |
|---|---|---|
| ProjectedBasketNet | Quotes, proposed legs, charge model | Сделку, eligibility или available funds |
| ProjectedCloseNowNet | Close Bid/Ask и current volume/basis | Будущий fill по этой цене |
| ActualRealizedDealNet | Signed Profit+Swap+Commission+Fee | Полноту history, принадлежность циклу, право grant |
| ReconciledEconomicNet | Independent broker history и EA-origin journal | Что один source не распределён уже в другом месте |
| EligibleSourceGrant | Approved role/policy + reconciled posted amount | Свободный остаток после reservations/consumption |
| AvailableReserve | Полный source/allocation/owner journal и reconciliation | Durable или concurrent atomicity без backend |
| OriginalGrant | Immutable allocation amount | Новый доход сверх самого source |
| RemainingGross | Reserved+Free | Доступность Reserved другому owner |
| Free / RemainingFree | Неизрасходованная незарезервированная часть | Допустимость любого назначения вне bucket policy |

Источники: `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:6-24`, `Docs/31_MONEY_PROOF_IDENTITY_RU.md:3-7`, `Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md:3-7`. Proposed mappings R0D/R0F не становятся approved по наличию reference PASS. Unknown history→UNAVAILABLE. Known complete empty history доказывает отсутствие источников и может дать known zero; это разные случаи (ERR-033/F060/IMP-004).

## Сохранение одного допустимого grant

Кандидат D-01: `G=Consumed+Reserved+Free`, `RemainingGross=Reserved+Free`, все компоненты>=0 и в одной currency/grid. Доказательство операций F053–F056 — сокращение одинаковых +d/-d. Отрицательные grants и несогласованные units недопустимы.

Ручная трасса G50: сначала C0,R0,Free50. Reserve ownerA15 → C0,R15,Free35. Consume unreserved10 → C10,R15,Free25. Release ownerA5 → C10,R10,Free30. Consume ownerA reservation10 → C20,R0,Free30. Полный законный consume30 → C50,R0,Free0. В каждой строке сумма50. Exact replay любого уже подтверждённого event оставляет строку прежней; changed payload того же event конфликтует, без delta.

OwnerB не получает права потратить ownerA reserved15 лишь из общего remaining50. Два потребителя, каждый видящий Free30, не могут оба расходовать20: независимые stale проверки не дают сериализуемости. Unknown journal не known Free30. Это математическая спецификация, **не запущенная reference-модель** и не доказательство production backend.

Source-level conservation требует `ΣOriginalGrants<=PostedEligibleSource` по полному реестру; полное COMMITTED распределение требует равенства. Локальные два grant50 одного источника50 не доказывают сумму<=50. PREPARED с Unallocated40 при grants10/source50 не spendable. ResidualHeld сохраняет сумму, но не автоматически превращается в available Reserve (ERR-004–008/017/033; F012–019; IMP-003/004/009).

## Immutable identity и replay

`HSBI_EconomicLedgerTypes.mqh:7-11`: key пропускает AccountLogin; equality пропускает signed components; serializer печатает только subset с8 digits. SameNet50 при P50,C0 и P60,C-10 не означает одинаковый факт (ERR-001/002/003). Source identity candidate Broker/Server/Account/Deal требует approval и независимого источника каждого поля; Magic/Cycle изменяют attribution, а не создают новый source.

`HSBI_AllocationLedgerTypes.mqh:8`: FinalReserve50/PF0 и FinalReserve0/PF50 не один immutable payload. Exact journal replay также требует проверки body: `HSBI_ExecutionJournal.mqh:27` возвращает NO_OP по прежнему заявленному digest раньше пересчёта body (ERR-030). NO_OP без delta не является новым списанием; однако неверно классифицированный replay нельзя называть полной проверкой immutable истории.

## Реальная экономика Initial Lock

Под предпосылками F050: equal L, constant K, BUY openAsk A0 и SELL openBid B0, liquidation Bid Bt/Ask At. Сумма `LK[(Bt-A0)+(B0-At)]=-LK(spread0+spread_t)`. Средняя цена сокращается. При LK1,spread0=spread_t=1 итог-2 до fees. Закрытие прибыльной ноги меняет распределение Balance/Floating, не создаёт этот недостающий2.

`Docs/09:20` исключает InitialProfit из RealizedCycleNet. Такая strategy metric может быть намеренно консервативной. Но экономический PnL всего Initial→Final цикла должен учитывать все realized и opening costs. “Не harvest eligible” не означает “не экономический расход”. ERR-036; F010/034/035/050; IMP-020.

## Harvest, Small attribution и costs

Signed source deal net вычисляется F007. Положительные reconciled разрешённые источники распределяются по policy; отрицательный deal не создаёт grant, но уменьшает экономический результат. Сумма положительных grants может превышать net всего basket при отрицательных других legs — это не создание денег, если отрицательные flows не скрыты в общей экономике и global funding не дублируется.

Basket evaluator `HSBI_BasketMoneyEvaluator.mqh:17` использует `max(0,Core+Trend+Small)` в поле reserveGainMoney. Proposed D-03 оставляет Small отдельно. Small-only+10 даёт в preview10, но отдельный ReserveCatchUp требует roleCore/Trend; полный funding обход отсюда не доказан (ERR-047; IMP-004). Необходимо выбрать/назвать policy, не выдавать весь forecast surplus за spendable BigReserve.

Costs имеют разные окна: accrued swap, opening/closing commission, deal fee, bid/ask spread в gross, дополнительный future slippage и buffers. F008 верна лишь при disjoint coverage. Дополнительное вычитание уже включённого spread меняет9 на8 без новой стоимости; пропущенный closing fee, наоборот, завышает net. `HSBI_CostModel.mqh:13-18` не содержит независимого полного CostID/basis/window coverage. Ни неизвестный расход, ни overlap не равны безопасному0 (ERR-022; IMP-014). Amount buffers аудитор не утверждает.

## Catch-Up

Для выбранного базиса: `Margin_i=EligibleReserve_i-AbsoluteFarLoss_i-Buffer_i`. Strict margin0 не PASS. AbsoluteLoss50,baseline40,Reserve30: incremental10 покрыт, но абсолютный50 нет (ERR-043). All-level min-margin является кандидатом CR09: ARGMAX TransitionLoss не ARGMIN Margin (A Trans10/M9, B Trans5/M-11; ERR-018).

Два значения одного Reserve в **альтернативных** price-state previews не являются двойным расходом; два последовательных фактических debit одного исходного Free — являются нарушением. Нужны раздельные сценарные индексы и обновление состояния после каждого реального шага. Projected CatchUp positive может быть preview, но не permission to debit actual Reserve (ERR-033).

## Partial Far и Final Close

PartialFar использует только PartialFarBudget, не FinalReserve (`Docs/11:5-13`). Budget/LossPerLot имеет lot dimension, floor ограничивает стоимость только при доказанной линейной потере и полном cost model. Fixed fee, adverse fill и недопустимый min residual требуют отказа/нового плана. ActualConsumed=max(0,-signed actual close net), затем release unused, а не полный budget расход по факту request.

FinalClose `Docs/12:7-15`: Economic/RecoveryPL gate, отдельный coverage, ownership/revision, no pending/unknown, fingerprint unchanged, actual zero и once-consumption. `HSBI_BuildRecoveryPL:9` — арифметический helper, не эта authority. Passed t.threshold без validated constructor — ERR-044. Sequential closes могут изменить quote/cost/risk между действиями, поэтому positive current liquidation estimate не гарантирует profit после завершения. Emergency не successful recovery.

## Domain и точность

Рационалы сохраняют малые increments на фоне10^28; это свойство exact чисел, не допустимый production money bound. Signed int64 max+1 вне domain; пересечение money scale/currency/volume types явно проверяется. Округление компонентов до суммы не коммутирует с округлением суммы: .004+.004 при digits2 half-up даёт.01 вместо0. Broker raw, posted и local rounding policy различаются. NUM/SNAP остаются proposed; кодек не создаёт authority.

MONEY_MODEL_VERIFIED=NO. Абстрактные partition-invariants выведены условно; MONEY_CONSERVATION_PROVEN=NO для сквозной production-системы; GLOBAL_FUNDING_PROVEN=NO. Durable/concurrent enforcement, подлинность history и фактический trading cycle остаются NOT_ESTABLISHED. Новых тестов или fresh regression-результатов нет.


## COVERAGE-COMPLETION — независимые суммы, authority и версия

Новый ERR-048 отделяет full-value binding от проверки shape identity: корректный sourceProof10 и scalar eligible100 не один денежный факт. В текущем NewFar caller scalars выводятся из proofs, поэтому вывод ограничен публичным evaluator, а не всем solver. D-02/D-04 обязаны определить базис, после чего guard связывает сумму, currency, precision, window и source. При allocated branch нельзя требовать повторного умножения allocation на reserveShare; это уже иная денежная стадия.

SourceKey ранних R0A/R0B включает schemaVersion и NFC-нормализацию; поздние R0F/R0G отделяют logical source от representation и не допускают guessed normalization. Нельзя молча объединять opaque broker names, равно как нельзя повторно funding того же источника при смене schema. Требуется approved versioned reconciliation/migration boundary, unknown legacy quarantined. Все16 решений остаются AWAITING_ADMIN_APPROVAL.

Для int64 minor units M=9223372036854775807: M−1=9223372036854775806, следующий debit1 даёт9223372036854775805 при точной арифметике и допустимых preconditions. M+1 и −(−9223372036854775808) вне signed64 domain. Это ручные равенства, не выполненный arithmetic test. Near10^28 одна cent не разрешается binary64; raw codec точного захваченного double не делает settled balance точным. Рounding расходов и переводы валют нужны до определения grant, неизвестная политика не безопасный zero.

Сохранность одного источника не доказывает account-wide free capital: source50 плюс неучтённый debit30 не даёт доступных50. Local sequential conservation, source registry conservation, global portfolio solvency и broker actuality — четыре отдельных proof scopes. GLOBAL_MONEY_CONSERVATION_PROVEN=NO.
