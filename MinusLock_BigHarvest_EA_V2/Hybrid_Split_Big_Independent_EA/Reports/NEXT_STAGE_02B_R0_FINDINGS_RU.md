# 02B-R0 — результаты предремедиационной проверки

Базовый SHA `4e7d911002824a4a92e49b54f0f964afcf8cf703`, ветка `work`. До записи локальный и remote SHA совпали, рабочее дерево было чистым. Статус этапа: `PRE_REMEDIATION_REVIEW_COMPLETE_WITH_BLOCKERS`. Это test-only аудит, не готовность советника к торговле. Предложения D-01–D-08 не утверждены.

## Как получены выводы

Не повторялся полный 02A audit. Проверены указанные документы и денежные функции, выполнены численные эксперименты на C++-совместимом подмножестве **извлечённых production MQL тел**, independent Python proposed oracle, актуальные regression suites. Shim заменяет базовые Math/string/ZeroMemory операции, не broker APIs. Aggregate digest в selector experiment заменён явным test-only shim: это не проверка digest integrity. Exact MQL5 семантика и полная NewFar selection — NOT_RUN.

Каждый native outcome сопоставлен с независимым CR expected. `ALLOW` — локальный bool/valid, не торговое разрешение. Duplicate int=1 нормализован в NO_OP, int=2 в CONFLICT; evaluator CALC_REJECT с DUPLICATE_CONSUMPTION_NOOP/CONSUMPTION_CONFLICT нормализован по reason. Это нормализация отчёта, production statuses не менялись.

## M-01 — воспроизводится на локальной границе

[Include/Money/HSBI_ReserveAllocationTypes.mqh:25](../Include/Money/HSBI_ReserveAllocationTypes.mqh#L25) — `HSBI_ValidateReserveConsumption`; [Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:35](../Include/Money/HSBI_ReserveCatchUpEvaluator.mqh#L35) — `HSBI_EvaluateReserveCatchUp`, строки 46–52.

Согласованный источник D1/A1, policy=1, deal=11, allocationEvent=31, net=100, Reserve=50, Residual=50; consumer CatchUp, plan/revision=1, event=41, lot gate 0.5×4>1, loss=10, buffer=1. Результат ALLOW, margin=39.

Чужие SourceDealKey, SourceAllocationKey, CycleID в строке ключа, allocationEvent=999 проходят тем же ALLOW, хотя независимый CR-01 ожидает REJECT. Отдельного CycleID/owner/allocationEvent в ConsumptionKey нет: тест изменяет предъявленный source key, а не несуществующее поле.

Exact prior key блокируется (нормализован NO_OP); изменённый consumer даёт CONFLICT. Повтор использованной **суммы** при том же key невозможно выразить в DTO: amount/bucket отсутствуют; Python oracle на E1=10→11 даёт CONFLICT. При unknown registry и hasPrior=false evaluator даёт ALLOW, oracle UNAVAILABLE. В alreadyAllocated ветке alreadyConsumed>0 отклоняется, но при reserveEligibleMoneyAlreadyAllocated=false те же spent evidence могут дать ALLOW. Это локальный контрпример, не доказанный реальный double spend: durable registry и dispatch отсутствуют.

Точный предлагаемый binding: CR-01/07/08. Нельзя чинить только сравнение двух строк и объявлять restart решённым.

## M-02 — self-copy воспроизводится, полная NewFar selection не заявляется

[Include/Money/HSBI_MoneyProofIdentity.mqh:16](../Include/Money/HSBI_MoneyProofIdentity.mqh#L16) — `HSBI_IsSameMoneyProofIdentity`; [Include/Planning/HSBI_NewFarSolver.mqh:82](../Include/Planning/HSBI_NewFarSolver.mqh#L82) (caller-derived identity), строки 119–125 (перезапись identities и копирование expected); [Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:35](../Include/Money/HSBI_ReserveCatchUpEvaluator.mqh#L35) — `HSBI_EvaluateReserveCatchUp`.

В adapter исполняются точные две assignment-строки expected из NewFar. Foreign account, magic, cycle, position, ненулевые отсутствующие deal/event=999, wrong plan/revision/snapshot после self-copy проходят локальный Catch-Up. С независимым expected те же nine mismatches отклоняются. Нулевые deal/event также отклоняются. Положительный согласованный контроль проходит.

Это доказывает тавтологию assembly/equality и недостаточность локального authorization; **не утверждается**, что любой чужой owner проходит все source guards полного NewFar solver. Там есть отдельные descriptor/plan checks. Они не предоставляют независимый confirmed economic record. Существование ненулевых IDs нигде в этой цепочке не проверяется по history.

Неверный digest, changed DealNet, missing event/history и allocation reuse проверены независимым Python oracle: REJECT; unavailable history: UNAVAILABLE. Их production end-to-end статус UNPROVEN: поля/lookup отсутствуют, нельзя выдать прохождение reference теста за проверку broker history.

## L-01 — ложный identical duplicate подтверждён

[Include/Money/HSBI_EconomicLedgerTypes.mqh:9](../Include/Money/HSBI_EconomicLedgerTypes.mqh#L9) — `HSBI_SameEconomicRecord`; [Include/Money/HSBI_EconomicLedgerTypes.mqh:10](../Include/Money/HSBI_EconomicLedgerTypes.mqh#L10) — `HSBI_ClassifyEconomicDuplicate`.

A: SourceDealKey=D1, volume=1, price=100, Profit=55, Commission=-5, Net=50. B: те же ключ/volume/price/net, Profit=60, Commission=-10. Production comparator выдаёт int=1 (NO_OP); immutable oracle — CONFLICT. Аналогично пропущены event, position, role, timestamp, Swap/Fee. Exact record положительно даёт NO_OP. Сериализация сохраняет только source/volume/price/net и потому тоже теряет эти различия.

AccountLogin отсутствует в record и source key; PlanID отсутствует в record. [Include/Money/HSBI_EconomicLedgerTypes.mqh:7](../Include/Money/HSBI_EconomicLedgerTypes.mqh#L7) — `HSBI_BuildSourceDealKey` строит Symbol|Magic|Cycle|DealTicket. Два account с одинаковыми EUR/7/1/11 получают один ключ; без namespace коллекции это collision. Изоляция ledger внешним account scope теоретически возможна, но обязательный authority caller/registry не доказан. CR-03 предлагает AccountLogin+broker/server и проверку всех связей; исторический R12A ledger qualification не добавляет этих полей в production DTO.

## L-02 — перестановка buckets подтверждена

[Include/Money/HSBI_AllocationLedgerTypes.mqh:8](../Include/Money/HSBI_AllocationLedgerTypes.mqh#L8) — `HSBI_ClassifyAllocationDuplicate`.

A: FinalReserve=50, PartialFar=0. B: FinalReserve=0, PartialFar=50. Один source, allocationEvent=31, сумма=50. Production: NO_OP; oracle: CONFLICT. Изменение consumed, available, residual с компенсирующим уменьшением Reserve, sourceNet/status и negative compensated buckets также может молча дать NO_OP. NaN не даёт identical replay в этом компараторе (CONFLICT) — не приписываем ему обратный результат.

PolicyVersion отсутствует в AllocationLedgerRecord, поэтому production duplicate policy test не выразим. ReserveAllocationSource содержит policyVersion и его validator проверяет nonzero/current policy в Catch-Up; это не исправляет недостаточность отдельного AllocationLedger comparator. Oracle policy change требует CONFLICT.

## E — локальные validators и граница обязательного caller

[Include/Money/HSBI_AllocationLedgerTypes.mqh:7](../Include/Money/HSBI_AllocationLedgerTypes.mqh#L7) — `HSBI_ValidateAllocationConservation`; [Include/Money/HSBI_MoneyState.mqh:5](../Include/Money/HSBI_MoneyState.mqh#L5) — `HSBI_ValidateMoneyState`; [Include/Money/HSBI_AllocationLedgerTypes.mqh:9](../Include/Money/HSBI_AllocationLedgerTypes.mqh#L9) — `HSBI_CanConsumeBucket`; [Include/Money/HSBI_AllocationLedgerTypes.mqh:10](../Include/Money/HSBI_AllocationLedgerTypes.mqh#L10) — `HSBI_CanConsumeAmount`.

Conservation пропускает отрицательные компенсирующие buckets, отрицательный consumed, status CONFLICT, foreign nonempty source и Infinity при Infinity sourceNet. NaN и превышение consumed/available в положительной ветке блокируются. Under-allocation рассматривается как D-01/DECISION_REQUIRED, а не уже утверждённая ошибка формулы. MoneyState игнорирует valid/revision/realizedCycleNet finite, допускает +Infinity, отклоняет отрицательный bucket. Bucket helper правильно запрещает FinalReserve для PartialFar, но пропускает неизвестный enum. Amount helper проверяет предел available, однако не valid/owner/source.

Поиск всех production callers дал только определения этих helpers. Поэтому нет доказательства обязательного внешнего слоя и невозможности обхода. Их форма сама по себе не доказывает торговую уязвимость: production pipeline отсутствует. Критический реальный вызов NewFar→CatchUp использует ReserveAllocation validator с finite/nonnegative guard, но не закрывает M-01/M-02. Точные границы ответственности — CR-05 и матрица с пометками proposal/context-required.

## F — M-05 и zero-Core

[Include/Money/HSBI_BasketMoneyEvaluator.mqh:11](../Include/Money/HSBI_BasketMoneyEvaluator.mqh#L11) — `HSBI_EvaluateBasketMoney`, строка 17: исполнена точная RHS, 0+0+10 даёт ReserveGain=10; Core=10 контроль даёт 10. Ограничение source roles относится к authoritative Reserve; aggregate поле его не соблюдает. Прямой Small→Reserve расход через NewFar не доказан, потому что тот берёт Core proof. D-03 обязателен до изменения формулы.

[Include/Planning/HSBI_GeometrySolver.mqh:21](../Include/Planning/HSBI_GeometrySolver.mqh#L21) — `HSBI_SolveBigGeometry`, строки 31–35: F=.10, ratios .01/3/.1, min=step=.01 → rawCore=.001, Core=0, Trend=.30, Small=.01, slope=.19, valid=true. Нарушение broker-min Core воспроизведено. Положительный ratios=2/1/.5 проходит. Geometry не изменена; передать отдельному regression fix после разрешения.

## G — WORST_CASE не соответствует минимуму Catch-Up margin

[Include/Planning/HSBI_FutureSmallProofAggregator.mqh:23](../Include/Planning/HSBI_FutureSmallProofAggregator.mqh#L23) — `HSBI_AggregateFutureSmallProof`, строка 50. L1 maximum TransitionLoss=100 и Catch-Up margin=29; L2 loss=10 и margin=-16. Все предъявленные completeness flags true; aggregator выбирает L1. FINAL_LEVEL контроль выбирает L2; incomplete proof отклоняется. Source sensitivity смены selector меняет выбранный уровень.

Это не broker-reachable path proof и не изменение политики. Docs/30 не определяет minimum Catch-Up margin как норматив WORST_CASE. Статус `DECISION_REQUIRED`, CR-09; до решения нельзя автоматически назвать L1 ошибочным относительно неутверждённого критерия либо объявить all-level Catch-Up достаточным.

## NewFar dependency safety

Confirmed history [NOT_RUN] → economic authority [L-01/account gap] → allocation authority [L-02/conservation decision] → consumption [M-01/restart gap] → expected identity [M-02] → Catch-Up [локальная арифметика проверена, authorization blocked] → Future Small [selector decision/runtime NOT_RUN] → NewFar [полная selection NOT_RUN]. Source/plan guards и fail-closed runtime policy сохраняются, но не заменяют эту цепочку. Positive margin не доказывает конечное исполнимое восстановление.

## Независимость и пределы mutation proof

6 fault mutations, 5 repair-sensitivity probes и 2 metric/selector sensitivity probes применяются к копиям исходных .mqh внутри temporary Tests tree; исходный Include не меняется. Собираются и исполняются извлечённые тела, сверяются source и mutant hashes, результат обязан измениться на целевом тесте. Ошибка компиляции или отсутствие anchor считается infrastructure failure, не пойманной mutation. Native adapter не превращает source-sensitive experiment в MQL5 runtime proof.

Тесты не всегда PASS: `--enforce-contract` возвращает 1 при известных contract mismatches. Отдельно отчёт evidenceExecution=PASS означает успешное выполнение экспериментов, не moneyIntegrity=PASS. Полная таблица actual/expected и runtime gaps — matrix/results.

## Решения и handoff

D-01–D-08 содержат все 13 требуемых полей, численные примеры и пустое поле утверждения: `Reports/NEXT_STAGE_02B_R0_DECISIONS_REQUIRED_RU.md`. Контракты CR-01–10: `Docs/NEXT_STAGE_02B_R0_CONTRACT_FREEZE_PROPOSAL_RU.md`. Ограниченное задание R1: `Docs/NEXT_STAGE_02B_R1_IMPLEMENTATION_TASK_RU.md`. R1 implementation, broker dispatch и real trading остаются запрещены.
