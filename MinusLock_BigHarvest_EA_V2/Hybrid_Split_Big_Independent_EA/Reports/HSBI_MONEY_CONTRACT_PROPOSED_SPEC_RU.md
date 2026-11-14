# MONEY CONTRACT — предлагаемый нормативный текст

Статус каждого MUST ниже: **PROPOSED**. Не APPROVED. База `398da88424f3fb7b30e5315fbc3bf89219dd9ad2`, ветка `work`. Рекомендации и альтернативы — в OWNER_DECISIONS; production implementation не начата.

## 1. ECONOMIC-SOURCE-IDENTITY

**ESI-01.** Source identity и attribution разделены. Независимый broker/history provider подтверждает BrokerIdentity, ServerIdentity, AccountLogin и DealTicket как namespace одной физической операции. Symbol, Magic, CycleId, Role, ActionId и EventId описывают attribution и не создают новую прибыль при изменении. OrderTicket и PositionIdentifier сохраняются отдельно; source не равен position или order, у которых может быть несколько deals.

**ESI-02.** Immutable body содержит BrokerIdentity, ServerIdentity, AccountLogin, Symbol, Magic, CycleId, DealTicket, OrderTicket, PositionIdentifier, ActionId, EventId, Role, EntryType, Direction, Volume, Price, Profit, Swap, Commission, Fee, DealNet, Timestamp с единицей и authority, currency и monetary precision. SchemaVersion и numeric/codec profile обязательны. Все поля валидируются до сравнения. Неизвестные enum, nonfinite, отсутствующая identity или unsupported schema → REJECT/UNAVAILABLE без state delta.

**ESI-03.** DealNet=Profit+Swap+Commission+Fee с сохранением signed компонентов broker statement. Изменение любого компонента при том же net меняет body. Same SourceKey + identical canonical body → NO_OP только после проверки integrity; same SourceKey + changed body → CONFLICT, zero delta и reconciliation. Разные SourceKey ещё не дают funding: проверить глобальное соответствие physical deal и отсутствие другого alias того же источника.

**ESI-04.** SourceKey format здесь не выбран. Кандидат A: typed length-prefixed namespace tuple, миграция требует external namespace mapping. B: versioned canonical escaped textual tuple с однозначными длинами и UTF8/нормализацией, сложнее parser/roundtrip. C: legacy key только read-only alias, не funding authority. Namespace рекомендация D-08 не утверждает wire representation. Окончательный формат и byte goldens — owner D-08/D-12/D-15.

**ESI-05.** Canonical encoding обязан задавать type tags, field order, byte order, UTF8 policy, length limits, zero equivalence, absence encoding, schema/profile IDs и отказ на trailing/duplicate/unknown fields. Serializing rounded eight-digit diagnostics не равно canonical economic identity. Digest связывает body, но не удостоверяет источник. Authenticated provider receipt связывает независимо полученные history facts, account/server, observation window, completeness, revision и content digest. Предъявленный bool actual/runtimeConfirmed или receipt, вычисленный из того же altered DTO, не независимая authority.

**ESI-06.** Closing OUT/OUT_BY entry может стать Eligible только после reconciliation и policy; opening IN не создаёт harvest. INOUT, balance/credit/reversal и separate commission postings требуют явного provider mapping, иначе UNAVAILABLE. Negative economic deals учитываются в CyclePnL и не становятся positive grant. Source status: Captured, Reconciled, Eligible, Allocated, Exhausted, Quarantined; статус не часть immutable экономического факта и не способ повторной активации. Corrections/reversals — append-only events с causation, а не перепись истории.

Текущая причина: EconomicLedgerTypes:6–12 отсутствуют broker/account/schema/direction, full equality и key rebuild. ERR-001/002/003/013; IMP-001/002. C++ P0-01/ROLE/POSITION/SOURCE-KEY-REBUILD воспроизводят локальный дефект; broker provider не исполнен.

## 2. ALLOCATION-CONSERVATION

**AC-01.** Для подтверждённого eligible positive grant G в minor units, единой валюте/scale и committed immutable allocation:

`G = FinalReserve + PartialFar + Transition + Carry + Residual`.

Каждый компонент неотрицателен. Residual — явно удержанный нецелевой остаток, а не разрешение потратить деньги в любой роли. Pending draft может удовлетворять sum assigned≤G только с отдельным явным Unassigned=G−sum assigned. Draft/Unassigned не доступны для consumption. Commit обязан либо перенести Unassigned в Residual, либо отклонить; ни исчезнувшей суммы, ни скрытого свободного grant нет. Negative source даёт G=0; economic loss отражается отдельно, без negative buckets.

**AC-02.** Allocation vector неизменяем по SourceKey+AllocationEventId+PolicyVersion. Exact replay сверяет source, event и каждую корзину, валюту, scale, policy и initial grant. Total equality недостаточна. Новый AllocationEventId не допускает повторного funding того же source. Источник разбивается один раз в source-level registry; revisions/transfer/reversal отдельно дебетуют старое и кредитуют новое назначение в одной транзакции. Transfer не увеличивает G.

**AC-03.** Rounding proposal: posting signed components по подтверждённой broker precision; для shares сначала exact rational multiply и floor неотрицательных grants, Residual=G−sum остальных четырёх. Sum shares≤1, finite и каждая share∈[0,1]. Round-to-nearest-all-buckets может превысить G; такой алгоритм не принят. Tie/monetary posting policy требует D-10/D-11; HALF_EVEN в модели — только кандидат, не объявление broker правила.

**AC-04.** В каждой корзине b действует другая, независимая ось `Grant_b=Consumed_b+Reserved_b+Free_b`. Available_b=Free_b после reconciliation. Reserve transfer Free→Reserved; release Reserved→Free только тому же reservation owner; consume Free→Consumed или owned Reserved→Consumed. Все amounts положительны, precision exact; FinalReserve не тратится PartialFar. Source cap и bucket cap проверяются вместе. Каждый commit требует expected revision и атомарно меняет balances+receipt+revision. Exhausted source или role/status reset не восстанавливает Free.

**AC-05.** Immutable event receipt включает EventId, ActionId, source/allocation/bucket, owner, exact amount, expected revision, operation, causation, schema. Same event+same receipt → NO_OP после полной integrity проверки, даже если source уже Exhausted; altered event → CONFLICT; new event+insufficient free → REJECT. Stale new event revision → REJECT/CONFLICT с zero delta. Revision не выводится из сортировки EventId; broker события могут приходить не по порядку. Commit order задаёт journal, uniqueness — namespace IDs.

Причина: AllocationLedgerTypes:7–10 допускает отрицательные компоненты, сравнивает totals и не имеет полного source registry. ERR-004/005/006/033; IMP-003/004/009. Reference P0-02/03/13 и SECOND-ALLOCATION-EVENT; реальный CAS/durable backend не проверен.

## 3. RESERVE / CATCH-UP

**RC-01.** ProjectedReserve — результат valuation будущего закрытия, не asset. ConfirmedReserve — settled source после independent history reconciliation. AllocatedReserve — подтверждённая доля immutable vector. ConsumedReserve — фактически использованная доля. ReservedReserve — обязательства других in-flight действий. AvailableReserve=AllocatedReserve−ConsumedReserve−ReservedReserve, только с согласованной revision/ownership/history; неизвестная completeness даёт UNAVAILABLE, не0.

**RC-02.** Preview Catch-Up может использовать projected source и projected Far loss, с явным `previewOnly=true`, но не создаёт reservation, funding или dispatch authority. Spendable result требует confirmed source, exact allocation binding, free balance, provider receipt и commit capability. Same scalar value не связывает provenance. Bound fields: namespace, SourceKey, sourceDealId, sourceEventId, allocationKey/event/policy, account/currency/scale, planId, stateRevision, snapshot content, owner и permitted consumer. Публичная граница не доверяет отдельным moneyAvailable/fresh bool.

**RC-03.** При recommended absolute basis `FarLoss=max(0,−FarCloseNowNet)`; `ReserveGain=eligible confirmed allocation free amount` для actual funding, либо явно projected eligible×share для preview. Scalar eligible обязан совпадать с proof value в заданной basis; FarLoss scalar — с Far proof. Нельзя применять share повторно к уже выделенному reserve. `CatchUpMargin=ReserveGain−FarLoss−DisjointRemainingBuffer>0`; все intermediate outputs finite. Buffer не вычитается дважды, если уже включён в proof net.

**RC-04.** All-level funding требует проверки всех required level margins, источников и prefix margin/risk. Выбор maximum TransitionLoss level не заменяет minimum CatchUpMargin. NewFar candidate selection не является permission promotion. Actual остаток должен принадлежать original BigCore по независимому positions/history provider, а не по переписанным identity flags. Projected residual нельзя объявлять фактическим. Retry/restart проверяет остаток с прежними receipts; partial fills не создают право использовать ещё не подтверждённую прибыль.

Причина: ReserveCatchUpEvaluator:24–76, NewFarSolver:119–127, FutureSmallProofAggregator:44–52. ERR-007/008/013/018/033/043/048; IMP-001/004/010/011. Direct scalar mismatch — статический counterexample; текущий NewFar caller выводит scalar из proofs. Полная независимость provider не доказана.

## 4. CYCLE-PNL / FINAL-CLOSE

**CF-01.** `CyclePnL=RealizedNet+UnrealizedNet−RemainingCosts`. RealizedNet — signed sum подтверждённых actual closing deals и однозначно attributed component postings данного цикла. UnrealizedNet — current close-now valuation всех managed открытых остатков, в актуальной account currency. RemainingCosts содержит только ещё не включённые execution расходы из disjoint cost inventory. Spread, встроенный в Ask-open/Bid-close, отдельно не вычитается. Swap/commission/fee signed; rebates не принудительно превращаются в расходы. Unknown conversion/cost coverage → UNAVAILABLE.

**CF-02.** До расчёта каждая valuation объявляет IncludedCostIDs, basis, volume, currency, quote side, observation/expiry window и PositionIdentifier. Если в UnrealizedNet уже включены все remaining costs, RemainingCosts=0 лишь при подтверждённой completeness. SafetyBuffer — headroom, не автоматически actual debit. При использовании его в PnL нельзя вторично включать тот же buffer в threshold. Mapping текущего `RecoveryPLCloseNow` и нового CyclePnL выбирается как конкретная versioned basis, без молчаливой смены исторических expected.

**CF-03.** PositiveHarvest, positive account Balance, positive Equity, positive CyclePnL и executable FinalClose различны. Не добавлять FinalReserve/PartialFar/Carry к PnL повторно: это partitions уже учтённой прибыли. FinalClose preview разрешён при `CyclePnL≥MinimumProfit+DisjointExecutionBuffer+Tolerance`; actual authorization дополнительно требует confirmed allowed coverage sources, fresh reconciled positions, no pending/unknown deals, exact revision, cost/provider validity, spread limit, risk и margin gate на каждом intermediate шаге. Emergency liquidation — отдельная authority, не успешный recovery profit.

**CF-04.** CYCLE_CLOSED фиксируется только после confirmed fills, independent actual zero managed positions, exactly-once ledger application и durable persisted result. Partial close не full close, preview не future profit guarantee. PositiveHarvest50 при Unrealized−60 и remaining1 даёт CyclePnL−11: NO FINAL CLOSE.

Норма Docs/08:6–24, Docs/12:5–17; MoneyTypes:9 не обеспечивает весь conjunction. ERR-022/034/036/044; IMP-014/015/020. Reference P0-14, GAP, SPREAD-EXPANSION, MARGIN-SHORTAGE, SNAPSHOT-MISMATCH — модель, не фактическое исполнение.

## 5. NUMERIC-DOMAIN

**ND-01.** Все внешние financial values, limits, ratios, lot/price inputs, snapshots и вычисленные результаты finite-only. NaN/±Infinity/overflow → REJECT/ERROR/UNAVAILABLE до разрешения. Guard должен проверять limits и inputs, затем каждый intermediate/output; finite inputs не исключают intermediate overflow. Underflow, меняющий sign/magnitude proof, не трактуется как безопасный0. Denominators проверяются до деления. Revision/IDs — exact integer domain, без double и с отказом на increment overflow.

**ND-02.** Double допустим для captured broker values и bounded projected calculations при versioned domain/error bounds. Settled financial accounting proposal — checked signed64 minor units, с explicit currency/scale и отказом на overflow каждого intermediate. Python unlimited integers/Decimal не доказывают native domain. Wide accumulators допускаются только с explicit checked adapter; окончательный0 не оправдывает переполнение промежуточной суммы. Precision берётся из independent broker currency profile; неизвестная precision → UNAVAILABLE.

**ND-03.** Financial posting round mode отдельно от canonical raw serialization. Кандидат HALF_EVEN для signed posting требует owner/provider approval; allocation floor+residual — другой шаг. +0/−0 считаются равными финансово, raw evidence сохраняется отдельно до явно утверждённой Z-normalization. Нельзя epsilon-равенством объявлять изменённый immutable payload дубликатом. Exact minor units сравниваются точно; tolerance применяется только к конкретному valuation/grid predicate с задокументированной единицей и bound.

**ND-04.** Volume quantization: explicit broker grid origin, step>0, min≤active volume≤max и exact grid membership; нормализация не разрешает активный lot ниже min. Optional Trend0 означает inactive leg, другие обязательные ноги не могут исчезнуть. Price tick grid отдельно от Point и volume grid; BUY close=Bid, SELL close=Ask. Unknown/invalid enum отвергается exhaustive membership, не `!=NONE`. Broker grid origin выбор и profile version требуют owner; тестовая модель использует zero-origin явно.

**ND-05.** Canonical schema запрещает bool вместо integer, truncating conversion, float IDs>2^53, nonfinite, unknown scale и silent legacy coercion. Ограничить длины и numeric exponents до parse/allocate. Точный диапазон long/ulong/double/UTF8 и codec должен пройти native goldens. Никакой `NATIVE_VERIFIED` по C++ или Python.

ERR-003/009/010/011/014/025/026/040/049; IMP-002/005/007/018. P0-04/05, numeric/grid reference cases; native pending.

## 6. EXECUTION / JOURNAL / RESTART

**EJR-01.** Unique ActionId задаёт immutable intent, unique EventId — receipt экономического события в определённом namespace. Intent содержит expected revision, account/symbol/position/role/direction/volume/price policy, cost/risk basis, source reservations и schema. Изменение intent требует нового explicit plan и reconciliation прежнего outcome; тот же ActionId с новым body → CONFLICT.

**EJR-02.** До dispatch будущий backend обязан durable сохранить intent и reservations. Partial fill accumulation использует unique confirmed deals и actual volumes, без double counting. COMPLETED требует exact accumulated requested amount, independent deals/positions/ownership, no unknown remainder и persisted ledger result. PLACED/REQUEST_ACCEPTED/timeout не означают completion или rejection. UNKNOWN/TIMEOUT → BLOCK/RECONCILE; автоматический повтор отправки запрещён. Known rejection допускает retry same ActionId только после доказательства отсутствия исполнения/остатка и revalidation unchanged intent.

**EJR-03.** Receipt проверяет полный body+digest+chain+namespace до duplicate classification. Прежний digest, оставленный при изменённом body, не позволяет NO_OP. Equality journal entry IDs не proof integrity. Atomic commit охватывает source balance, bucket reservations/consumption, event uniqueness и state/journal revisions. Concurrent consumers используют single serializable owner/CAS; check-then-write отдельно не годится. Каждая REJECT/CONFLICT/NO_OP ветвь оставляет финансовое состояние неизменным.

**EJR-04.** Restart начинает blocked state. Прочитать проверенную journal chain/schema/checksums, immutable intent, source inventory и actual broker history/positions; reconcile partial/unknown/corrections, восстановить exact balances и applied events. Неполная history, повреждённый chain, расхождение revisions или namespace → quarantine/manual review, no auto-resume. Повтор события после restart применяет экономику не более одного раза. Trusted in-memory snapshot не доказывает durability.

**EJR-05.** Без broker/backend provider невозможно подтвердить authenticity/completeness history, exactly-once внешнюю отправку, account margin каждого prefix, атомарную запись при crash, fsync semantics, multi-process ordering и restart reconciliation. Корректный локальный oracle этих гарантий не даёт. Данный этап не подключает provider и не отправляет ордеров.

Нормы Docs/06:9–21, Docs/08:15/24, Docs/13:12–20. ExecutionJournal:21–29, TransactionTypes:8–22 и StateMachine:5–7 обеспечивают только части. ERR-010/016/017/025/030/033/050; IMP-005/008/009. P0-07/08/09/10/13; реальные crash/concurrency проверки NOT_RUN.

## 7. Утверждение и совместимость

Все шесть контрактов имеют тестовые obligations и связаны с 16 карточками. Проект не переводится в approved status этим текстом. Snapshot freshness, funding, NewFar, FinalClose, partial execution, restart, codec и Transition A/B/C вынесены в D-02/04/05/06/07/08/09/12/13/14/15/16. Unknown legacy facts блокируют migration, старые fixtures/expected не переписываются. Full AUDIT03 остаётся PARTIAL из-за открытых документальных/source/caller obligations.
