# 02B-R0 — решения администратора D-01–D-08

Базовый SHA: `4e7d911002824a4a92e49b54f0f964afcf8cf703`. Статус всех предложений: `AWAITING_ADMIN_APPROVAL`.
Ни одно предложение не утверждено. Исторические статусы проекта и R12A static qualification не разрешают production-remediation или торговлю. Номера CR относятся к `Docs/NEXT_STAGE_02B_R0_CONTRACT_FREEZE_PROPOSAL_RU.md`; точные production-ссылки приведены там и в Findings. Численные примеры — критерии выбора, не изменение действующей модели.

## D-01. Полнота committed allocation

1. **Текущая нормативная формулировка:** Docs/08 требует Reserve+Partial+Transition+Carry+Residual=AllocatableDealNet; Docs/32 и локальные validators допускают верхнюю границу.

2. **Обнаруженное противоречие:** Остаток без Residual может молча исчезнуть; уже consumed может считаться и grant, и отдельной суммой.

3. **Возможные варианты:** (А) полное распределение; (Б) partial с явным Unallocated/phase.

4. **Рекомендуемый безопасный вариант:** Для committed — полное immutable grant; partial только промежуточно с запретом расхода Unallocated. Балансы отдельно: Remaining+Consumed=OriginalGrant.

5. **Численный контрпример:** Net=100, grant Reserve=60, прочие=0: 40 должны попасть в Residual либо Unallocated intermediate. Для grant=100, remaining=70, consumed=30 нельзя требовать grant+consumed=100.

6. **Последствия для Big:** Harvest выделяет только подтверждённый Net; не повышает funds на 40.

7. **Последствия для Small:** Small transition не получает скрытый остаток.

8. **Последствия для Catch-Up:** Берёт только available нужного bucket, без повторного ReserveShare.

9. **Последствия для New Far:** Кандидат без полного committed allocation не авторизуется.

10. **Последствия для persistence:** Сохранять grant/balances/phase/consumption с разными schema versions; legacy incomplete → reconciliation.

11. **Production-функции последующего исправления:** HSBI_ValidateAllocationConservation; HSBI_ValidateReserveAllocationSource; HSBI_ClassifyAllocationDuplicate; HSBI_EvaluateReserveCatchUp.

12. **Необходимые тесты:** E-allocation-unassigned, O-conservation-*, L02-bucket-permutation; exact/partial/negative/restart.

13. **Утверждение администратора:** статус НЕ УТВЕРЖДЕНО; выбранный вариант ______; версия контракта ______; исключения/границы ______; ФИО/ID ______; дата ______; подпись/ID решения ______.

## D-02. Типы projected/actual/allocated/available

1. **Текущая нормативная формулировка:** Docs/24 запрещает projected как actual; Docs/04 RecoveryPL=realized+open close-now, без buckets; Basket.recoveryMoney является projected basket.

2. **Обнаруженное противоречие:** Имя recoveryMoney допускает использование прогноза как settled fund.

3. **Возможные варианты:** (А) оставить общее double с тегами; (Б) отдельные DTO/типы и явные conversion gates.

4. **Рекомендуемый безопасный вариант:** Отдельные ProjectedBasketNet, ActualRealizedNet, AllocationGrant, AvailableBalance; conversion только confirmed/reconciled event.

5. **Численный контрпример:** Projected basket=100, closing deals=0, allocated=0, available=0: Catch-Up не получает 100.

6. **Последствия для Big:** Core/Trend прогноз используется для планирования, не для ledger credit.

7. **Последствия для Small:** Small forecast не становится reserve до confirmed close и D-03.

8. **Последствия для Catch-Up:** Оценка Catch-Up и разрешение расхода — разные результаты.

9. **Последствия для New Far:** Expected identity/availability из authority, не из projected candidate proof.

10. **Последствия для persistence:** Сохранять тип, phase, source и schema; запрещена миграция projected в available без history.

11. **Production-функции последующего исправления:** HSBI_EvaluateBasketMoney; HSBI_EvaluateFutureSmallLevel; HSBI_EvaluateReserveCatchUp; HSBI_SolveNewFar assembly.

12. **Необходимые тесты:** M02-control/foreign/digest, O-history-unavailable; новая R1 projected→actual mutation; broker runtime NOT_RUN.

13. **Утверждение администратора:** статус НЕ УТВЕРЖДЕНО; выбранный вариант ______; версия контракта ______; исключения/границы ______; ФИО/ID ______; дата ______; подпись/ID решения ______.

## D-03. Роли источников Reserve

1. **Текущая нормативная формулировка:** Docs/31 разрешает BigCore/BigTrend в Reserve proof; Docs/08 actual closing DealNet — источник harvest allocation.

2. **Обнаруженное противоречие:** Basket reserveGainMoney включает Small; projected source proof не доказывает actual available Reserve.

3. **Возможные варианты:** (А) разрешить Small отдельным решением; (Б) Small вести отдельно; (В) переименовать aggregate metric без authority.

4. **Рекомендуемый безопасный вариант:** Reserve только из подтверждённых положительных Net разрешённых Core/Trend. Small учитывать отдельно до решения bucket назначения; aggregate не является authority.

5. **Численный контрпример:** Core=0, Trend=0, Small=10: текущая RHS=10; разрешённый Core/Trend reserve contribution=0. Контроль Core=10 → 10.

6. **Последствия для Big:** Сохраняет Core/Trend provenance; отрицательные costs уменьшают Net.

7. **Последствия для Small:** Small=10 не теряется из economic ledger, но не повышает Reserve автоматически.

8. **Последствия для Catch-Up:** Small-only прогноз не разрешает Catch-Up.

9. **Последствия для New Far:** NewFar не должен использовать общий basket metric как Reserve proof.

10. **Последствия для persistence:** Role и исходные signed components обязательны; перераспределение старых Small записей требует утверждённой миграции.

11. **Production-функции последующего исправления:** HSBI_EvaluateBasketMoney; HSBI_ValidateReserveSourceProof; HSBI_EvaluateReserveCatchUp; HSBI_SolveNewFar assembly.

12. **Необходимые тесты:** M05-small-only/core-control; forbidden Small proof; allocation carry/residual fixture после решения.

13. **Утверждение администратора:** статус НЕ УТВЕРЖДЕНО; выбранный вариант ______; версия контракта ______; исключения/границы ______; ФИО/ID ______; дата ______; подпись/ID решения ______.

## D-04. Absolute и incremental Far loss

1. **Текущая нормативная формулировка:** Docs/24 Catch-Up называет FarLossIncrease; текущие Basket/NewFar используют max(0,-FarNetCurrent).

2. **Обнаруженное противоречие:** Название increase не определяет baseline; absolute и incremental меняют gate.

3. **Возможные варианты:** (А) absolute current loss; (Б) incremental от зафиксированного baseline; (В) хранить оба, явно выбрать gate.

4. **Рекомендуемый безопасный вариант:** Хранить оба раздельно. До выбора администратора не менять рабочую absolute метрику. Без baseline incremental=UNAVAILABLE; более слабый gate не выбирать автоматически.

5. **Численный контрпример:** Baseline loss=40, current=50, Reserve=20, buffer=5: absolute margin=-35 (reject), incremental=5 (allow). При Reserve=60: 5 против 45.

6. **Последствия для Big:** Изменяется момент выполнения recovery catch-up, не геометрия Big.

7. **Последствия для Small:** Меняется допустимость следующего transition.

8. **Последствия для Catch-Up:** Нужен утверждённый gateMetric и immutable baseline.

9. **Последствия для New Far:** Все candidates используют одну утверждённую метрику/версию, а не удобную для PASS.

10. **Последствия для persistence:** Baseline id/time/BidAsk/cost schema и chosen metric сохраняются; после рестарта нельзя переустанавливать baseline ради PASS.

11. **Production-функции последующего исправления:** HSBI_EvaluateBasketMoney; HSBI_EvaluateReserveCatchUp; HSBI_SolveNewFar assembly; HSBI_ReserveCatchUpDigest.

12. **Необходимые тесты:** Численные обе метрики, missing/stale baseline, BUY/SELL; новые R1 vectors; CR-09 extrema.

13. **Утверждение администратора:** статус НЕ УТВЕРЖДЕНО; выбранный вариант ______; версия контракта ______; исключения/границы ______; ФИО/ID ______; дата ______; подпись/ID решения ______.

## D-05. Projected и actual TransitionLoss

1. **Текущая нормативная формулировка:** Docs/04/08: actual TransitionLoss=max(0,-ΣActualClosingDealNet); Docs/27 прогнозирует transition risk.

2. **Обнаруженное противоречие:** Одно имя допускает перенос projected loss в actual accounting.

3. **Возможные варианты:** (А) один tagged DTO; (Б) разные ProjectedTransitionRisk и ActualTransitionLoss с отдельными gates.

4. **Рекомендуемый безопасный вариант:** Раздельные типы: projected для planning caps, actual для ledger/reconciliation после fills; фактическое превышение не превращается в успешный план.

5. **Численный контрпример:** Projected loss=10, actual closing Net=-15 → actual loss=15; cap=12: план мог пройти, фактическое исполнение требует reconciliation, не переписать actual на 10.

6. **Последствия для Big:** Harvest actual accounting не подменяется оценкой.

7. **Последствия для Small:** Small transition caps проверяются прогнозно и затем фактически.

8. **Последствия для Catch-Up:** Не использовать transition loss как Reserve source или Far proof.

9. **Последствия для New Far:** Кандидат проходит projected risk gate, но actual NewFar role требует confirmed fills и residual.

10. **Последствия для persistence:** Хранить projected snapshot отдельно от actual events, execution slippage delta и cap decision.

11. **Production-функции последующего исправления:** HSBI_EvaluateBasketMoney; HSBI_EvaluateFutureSmallLevel; HSBI_EvaluateNewFarGates; HSBI_SolveNewFar.

12. **Необходимые тесты:** No-fill projected-only; actual over-cap; partial fills; signed DealNet components; NOT_RUN terminal fills.

13. **Утверждение администратора:** статус НЕ УТВЕРЖДЕНО; выбранный вариант ______; версия контракта ______; исключения/границы ______; ФИО/ID ______; дата ______; подпись/ID решения ______.

## D-06. Назначение safety buffers

1. **Текущая нормативная формулировка:** Docs/24 включает projected leg costs; Docs/04 Catch-Up добавляет execution safety buffer.

2. **Обнаруженное противоречие:** Нет явной карты рисков: per-leg и Catch-Up могут покрывать одно и то же.

3. **Возможные варианты:** (А) независимые budgets с непересекающимися рисками; (Б) единый budget с формализованным распределением.

4. **Рекомендуемый безопасный вариант:** Явные компоненты/units/risk-purpose/version. Независимое сложение только после доказательства отсутствия overlap. Не убирать существующий buffer до решения.

5. **Численный контрпример:** 4 legs × 1 + Catch-Up 1 = 5. Если общий risk budget=4, пятая единица дублируется; если отдельный переходный риск=1, 5 корректно.

6. **Последствия для Big:** Costs Core/Trend должны оставаться в projected net.

7. **Последствия для Small:** Small cost и transition safety не смешиваются.

8. **Последствия для Catch-Up:** Строго >0 margin после утверждённых независимых buffers.

9. **Последствия для New Far:** Digest включает policy и каждый component; переименование не должно отменять gate.

10. **Последствия для persistence:** Сохранять buffer policy/version и snapshot; stale versions требуют recompute projected, не переписывать actual DealNet.

11. **Production-функции последующего исправления:** HSBI_CalculateProjectedProfit; HSBI_EvaluateProjectedLegMoney; HSBI_EvaluateBasketMoney; HSBI_EvaluateReserveCatchUp.

12. **Необходимые тесты:** Per-leg vs shared buffer scenarios; missing/nonfinite/negative; removal-buffer mutation запланирована R1, не заявлена выполненной R0.

13. **Утверждение администратора:** статус НЕ УТВЕРЖДЕНО; выбранный вариант ______; версия контракта ______; исключения/границы ______; ФИО/ID ______; дата ______; подпись/ID решения ______.

## D-07. NO_OP и изменённый replay

1. **Текущая нормативная формулировка:** Docs/08/32: identical replay NO_OP, changed payload CONFLICT; evaluator возвращает CALC_REJECT с reason DUPLICATE_CONSUMPTION_NOOP.

2. **Обнаруженное противоречие:** Typed outcome отсутствует; key не содержит amount/bucket; bool prior не доказывает полноту registry.

3. **Возможные варианты:** (А) отдельный outcome NO_OP; (Б) REJECT+typed no-op reason с формально нулевыми deltas.

4. **Рекомендуемый безопасный вариант:** Отдельный NO_OP, zero deltas/revision/actions, altered payload CONFLICT. Authority сначала проверяет committed replay, потом remaining для нового расхода.

5. **Численный контрпример:** Reserve=50, event E1 amount=10 → remaining=40; exact E1 amount=10 → 40; E1 amount=11 → CONFLICT и 40; новый E2 amount=41 → REJECT.

6. **Последствия для Big:** Повтор Harvest не создаёт второй grant.

7. **Последствия для Small:** Повтор transition не закрывает повторно и не удваивает loss.

8. **Последствия для Catch-Up:** NO_OP не является новым valid Catch-Up authorization.

9. **Последствия для New Far:** Replay не создаёт новый selected action/state revision.

10. **Последствия для persistence:** Durable all-event registry, payload digests, commit marker; incomplete restart → UNAVAILABLE.

11. **Production-функции последующего исправления:** HSBI_IsDuplicateReserveConsumption; HSBI_ReserveConsumptionConflict; HSBI_ReserveConsumptionKeyDigest; HSBI_EvaluateReserveCatchUp; journal/restart validators после отдельного scope.

12. **Необходимые тесты:** M01-exact/altered/restart/spent; O-changed-amount-replay, O-consume-over-remaining; durable crash checks NOT_RUN.

13. **Утверждение администратора:** статус НЕ УТВЕРЖДЕНО; выбранный вариант ______; версия контракта ______; исключения/границы ______; ФИО/ID ______; дата ______; подпись/ID решения ______.

## D-08. Авторитетный provenance

1. **Текущая нормативная формулировка:** Docs/08 actual deals; Docs/16 durable journal/history reconciliation; Docs/31/32 source identity/evidence.

2. **Обнаруженное противоречие:** Caller flags и self-copy identity заменяют независимую сверку; production persistence stub.

3. **Возможные варианты:** (А) доверять флагам/ненулевым IDs; (Б) broker history + durable journal + независимая reconciliation; (В) ручной offline fixture только для tests.

4. **Рекомендуемый безопасный вариант:** Б для authorization; В допустим только test-only. Неполный источник даёт UNAVAILABLE; NONZERO_ID не даёт confirmed. AccountLogin дополняется broker/server namespace.

5. **Численный контрпример:** Deal=999/Event=888 отсутствуют в полном history: REJECT даже при valid/actual/confirmed=true. History недоступна: UNAVAILABLE. На двух accounts Deal=11 не означает одну сделку.

6. **Последствия для Big:** Фактический Harvest связан с конкретным closing deal и ролью.

7. **Последствия для Small:** Residual original BigCore подтверждается positions/fills, не projected Small.

8. **Последствия для Catch-Up:** Expected source и available из authority; нельзя доверять submitted digest как проверке самого себя.

9. **Последствия для New Far:** Цепочка CR-02 обязательна; непроверенный source исключает candidate до tie-break.

10. **Последствия для persistence:** Versioned durable records и completeness proof, сверка snapshot/journal/history и migration; криптографический checksum не доказывает broker authenticity сам по себе.

11. **Production-функции последующего исправления:** HSBI_BuildSourceDealKey; HSBI_NewFarProofIdentity; HSBI_SolveNewFar assembly; HSBI_ValidateReserveSourceProof/FarLossProof; HSBI_PersistSnapshotStub и новый read-only authority provider.

12. **Необходимые тесты:** M02 независимые ownership/deal/event/plan/revision/stale/digest/Net/reuse, O-proof-*; broker/restart fault injection NOT_RUN.

13. **Утверждение администратора:** статус НЕ УТВЕРЖДЕНО; выбранный вариант ______; версия контракта ______; исключения/границы ______; ФИО/ID ______; дата ______; подпись/ID решения ______.

## Дополнительное решение CR-09

WORST_CASE Catch-Up требует отдельного выбора: minimum Catch-Up margin по всем допустимым уровням либо maximum TransitionLoss с явно ограниченной гарантией. Контрпример L1: loss=100, margin=29; L2: loss=10, margin=-16. Предложение: минимум money margin с all-level identity/lot/availability gates и deterministic tie-break. Последствия затрагивают aggregate selection/digest, Catch-Up и NewFar; Big/Small geometry не меняются. Persistence сохраняет selection policy/version и все control proof references. До утверждения — DECISION_REQUIRED. Администратор ______; выбранный вариант ______; дата ______; ID решения ______.
