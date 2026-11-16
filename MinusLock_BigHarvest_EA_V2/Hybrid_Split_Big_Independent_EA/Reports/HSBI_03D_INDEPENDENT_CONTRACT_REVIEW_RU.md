# HSBI-03D — Независимая экспертиза 16 денежных контрактов

Пакет публикации ранее выполненной экспертизы HSBI-03D / HSBI-03D-REMOTE-R1.
Исходный полный отчёт доступен в предыдущем ответе Codex этой беседы; текст перенесён по предметным разделам, без восстановления отсутствующего внешнего материала. Это audit/test-evidence only, не повторный полный аудит проекта.
Base SHA: 6543bc2c0d125f5f7e02f78a092b0412a2e34626. Историческая read-only проверка закончена 2026-11-16 15:16:59 UTC; publication baseline повторно проверен 2026-11-16 15:48:57 UTC и совпал.
16 reviewed,12 ready,1 conflicting,2 blocked,1 requires clarification;0 approved;14 P0 reviewed,0 closed;ERR038 OPEN.
Полный новый анализ74 modules/199 definitions не выполнен. Source coverage inventory не равно содержательной квалификации всех строк. Native/compile/mutation/new runtime tests NOT_RUN.

## Статус, приоритет и общие правила

Версия предлагаемого текста: **HSBI-03D-REMOTE-R1**. Все новые контракты PROPOSED; OwnerApproval=AWAITING. READY_FOR_OWNER_APPROVAL означает готовность нормативного предложения к голосованию, а не готовность реализации.

Приоритет: (1) явное решение владельца с версией и scope; (2) непротиворечивые действующие нормы; (3) утверждённые конкретные уточнения; (4) неутверждённые proposals; (5) код как факт поведения; (6) тесты как evidence конкретного объекта. Новизна файла, его название и PASS не утверждают норму. Конфликт равноправных норм разрешается отдельно владельцем.

Обязательные общие правила G1–G8 применяются к каждой карточке:
1. Неизвестное обязательное поле не заменяется 0/false/текущим account/server.
2. UNAVAILABLE означает отсутствие нужного evidence; CONFLICT — противоречие; оба запрещают зависимое новое расходование.
3. Reject не меняет balances, revision и committed receipts/journal.
4. NOOP требует проверки полного прежнего receipt и тела; он не создаёт grant и не повторяет consumption.
5. Новый effect требует expected revision; revision overflow запрещён.
6. Digest не является доказательством broker origin, completeness history или funding authority.
7. Settled money имеет currency/profile и exact units; preview не становится settled только из-за округления.
8. Trading/dispatch и production implementation этим пакетом не разрешаются.

Evidence: STATIC_REVIEWED — исходный текст; MATH_DERIVED — вывод при явных предпосылках; COUNTEREXAMPLE_CONFIRMED — проверяемое опровержение утверждения, не runtime PASS; HISTORICAL_TEST_RESULT — сохранённый старый результат; TEST_SPECIFIED_NOT_RUN — новый тест без исполнения; NATIVE_NOT_RUN — нет MQL5 запуска; UNVERIFIED — нет нужного факта. Все новые vectors — TEST_SPECIFIED_NOT_RUN; native tests NOT_RUN.

Общие типы: Logical SourceKey — tuple D08; IDs tickets/cycle/plan/action/event/revisions — ulong при применимости, без преобразования через double; accountLogin — positive signed long; magic — signed nonzero long; closed enums проверяются по membership. Timestamp содержит clock domain/unit, а не только число. Неотрицательные balances — checked exact minor units после утверждения numeric bundle. Уникальные ограничения каждого решения указаны в его карточке.


| № | Canonical DecisionId | Статус |
|---|---|---|
| D-01 | D-01 | READY_FOR_OWNER_APPROVAL |
| D-02 | D-02 | READY_FOR_OWNER_APPROVAL |
| D-03 | D-03 | READY_FOR_OWNER_APPROVAL |
| D-04 | D-04 | READY_FOR_OWNER_APPROVAL |
| D-05 | D-05 | READY_FOR_OWNER_APPROVAL |
| D-06 | D-06 | CONFLICTING |
| D-07 | D-07 | READY_FOR_OWNER_APPROVAL |
| D-08 | D-08 | READY_FOR_OWNER_APPROVAL |
| D-09 | CR-09 | READY_FOR_OWNER_APPROVAL |
| D-10 | NUM-EXACT-1 | READY_FOR_OWNER_APPROVAL |
| D-11 | NUM-DOMAIN-1 | BLOCKED_BY_EVIDENCE |
| D-12 | NUM-CODEC | BLOCKED_BY_EVIDENCE |
| D-13 | SNAP-FIXTURE-1 | REQUIRES_CLARIFICATION |
| D-14 | FUNDING-GLOBAL-ATTRIBUTION | READY_FOR_OWNER_APPROVAL |
| D-15 | MQL-DOMAIN | READY_FOR_OWNER_APPROVAL |
| D-16 | BALANCE-SCHEMA-MAPPING | READY_FOR_OWNER_APPROVAL |

## Зафиксированные источники

Все пути в этом пакете относительны `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/`. Все указанные строки относятся к commit `6543bc2c0d125f5f7e02f78a092b0412a2e34626`. Коды S01–S20 ниже используются как точные ссылки на production; это результаты предшествующей read-only экспертизы, не новый запуск тестов.

| Код | Путь, функция, строки |
|---|---|
| S01 | Include/Money/HSBI_EconomicLedgerTypes.mqh: DTO 6; HSBI_BuildSourceDealKey 7; HSBI_ValidateEconomicRecord 8; HSBI_SameEconomicRecord 9; HSBI_ClassifyEconomicDuplicate 10; HSBI_SerializeEconomicRecord 11; HSBI_IsHarvestSourceEntry 12 |
| S02 | Include/Money/HSBI_AllocationLedgerTypes.mqh: DTO 5; HSBI_AllocatedTotal 6; HSBI_ValidateAllocationConservation 7; HSBI_ClassifyAllocationDuplicate 8; HSBI_CanConsumeBucket/HSBI_CanConsumeAmount 9–10 |
| S03 | Include/Money/HSBI_MoneyState.mqh: DTO 4; HSBI_ValidateMoneyState 5 |
| S04 | Include/Money/HSBI_ReserveCatchUpEvaluator.mqh: HSBI_ValidateReserveSourceProof 24–28; HSBI_ValidateFarLossProof 30–33; HSBI_EvaluateReserveCatchUp 35–76, особенно 44–50,63–75 |
| S05 | Include/Money/HSBI_ReserveAllocationTypes.mqh: HSBI_ValidateReserveAllocationSource 15–23; HSBI_ValidateReserveConsumption/HSBI_IsDuplicateReserveConsumption/HSBI_ReserveConsumptionConflict 25–30 |
| S06 | Include/Money/HSBI_MoneyProofIdentity.mqh: HSBI_ValidateMoneyProofIdentity 10–14; HSBI_IsSameMoneyProofIdentity 16–21; HSBI_MoneyProofIdentityDigest 23–28 |
| S07 | Include/Planning/HSBI_NewFarSolver.mqh: source validation 60–72; cap 74; proof identity construction 80–82; HSBI_SolveNewFar 94–154, особенно 119–127 |
| S08 | Include/Planning/HSBI_FutureSmallProofAggregator.mqh: HSBI_AggregateFutureSmallProof 23–58; control selection 50–52 |
| S09 | Include/Risk/HSBI_RiskGateResult.mqh: HSBI_ValidateRiskInput 6; поля Include/Risk/HSBI_RiskTypes.mqh 3–4 |
| S10 | Include/Execution/HSBI_TransactionTypes.mqh: HSBI_TransactionBarrierPassed 9–18; HSBI_RetryAllowed 20–22 |
| S11 | Include/Core/HSBI_Context.mqh: HSBI_ContextRolesConflict 19–25; HSBI_ValidateContext 33–53; FAR count 48–53 |
| S12 | Include/Persistence/HSBI_ExecutionJournal.mqh: HSBI_ExecutionJournalEntryDigest 12–17; HSBI_ValidateJournalEntry 18–20; HSBI_IsDuplicateJournalEntry 21–22; HSBI_ClassifyJournalAppend 25–29; HSBI_ValidateJournalChain 31–43 |
| S13 | Include/Persistence/HSBI_PersistenceInterface.mqh: production digest stub 5; HSBI_PersistSnapshotStub 7 |
| S14 | Include/Money/HSBI_CostModel.mqh: HSBI_ValidateCostSnapshot 5–9; HSBI_TryActualDealNet 11–13; HSBI_TryProjectedNetMoney 15–18 |
| S15 | Include/Money/HSBI_BasketMoneyEvaluator.mqh: HSBI_BasketLegInput 7–9; HSBI_EvaluateBasketMoney 11–19 |
| S16 | Include/Money/HSBI_LevelMoneyEvaluator.mqh: HSBI_EvaluateProjectedLegMoney 7–14 |
| S17 | Include/Planning/HSBI_ControlPrices.mqh: HSBI_IsSnapshotFresh 11; HSBI_ValidateTypedControlPrice 16–24 |
| S18 | Include/Planning/HSBI_BrokerGrid.mqh: price grid 8–20; volume grid/rounding/limits 21–36 |
| S19 | Include/Money/HSBI_MoneyTypes.mqh: TransitionLoss DTO 8; HSBI_BuildRecoveryPL 9 |
| S20 | Include/Core/HSBI_StateMachine.mqh: HSBI_ProposeStateTransition/HSBI_ApplyPureStateTransition 6–7; Include/Core/HSBI_Invariants.mqh: HSBI_ExactlyOneFarOrZero/HSBI_NoDualTail 5–6, HSBI_StateRevisionMonotonic 9 |

### Нормативные точки

- Docs/00_PROJECT_CHARTER_RU.md: 11–18 — Hybrid-only, MQL5, ограничения разрешения торговли.
- Docs/01_GLOSSARY_AND_DIMENSIONS_RU.md: 13–27 — типы и единицы; 31–34,49–52 — projected/actual, buckets.
- Docs/02_SYSTEM_ROLES_AND_IDENTITY_RU.md: 20 — managed position identity; 23–28,36 — ownership/restart.
- Docs/04_MATHEMATICAL_MODEL_RU.md: 18 RecoveryPL; 24 TransitionLoss; 27 FinalClose; 30 conservation; 33–36 contraction; 42 nonfinite.
- Docs/06_STATE_MACHINE_SPECIFICATION_RU.md: 9–21 — actual/ledger/persist и restart.
- Docs/07_TRANSACTION_EXECUTION_CONTRACT_RU.md: 6–24 — pipeline, identity, retry, unknown, restart.
- Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md: 6 net; 9 source fields; 12 conservation; 15 replay; 18 bucket restrictions; 21 result; 24 lifecycle.
- Docs/09_INITIAL_LOCK_SPECIFICATION_RU.md: 20 — Initial Profit исключён из RealizedCycleNet и бюджетов.
- Docs/12_FINAL_CLOSE_SPECIFICATION_RU.md: 7 threshold; 9 coverage; 11 guards; 15 фактическое завершение.
- Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md: 9 caps; 12 порядок; 14 partial/unknown; 17 actual residual.
- Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md: 9 grid; 22–23 minimum-safe-first; 25 actual data.
- Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md: 6 limits; 9 gate order; 18 emergency; 21 permission.
- Docs/16_PERSISTENCE_AND_RESTART_RU.md: 6–12 crash consistency; 15 reconciliation; 18 unknown schema.
- Docs/24_BROKER_MONEY_MODEL_RU.md: 5–11 — calculation-only, costs, catch-up, finite domain.
- Docs/25_BROKER_GRID_AND_ROUNDING_RU.md: 3–7 — tick grid и volume rounding.
- Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md: 3 risk-first; 35 full proof.
- Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md: 3–7 complete finite depth.
- Docs/31_MONEY_PROOF_IDENTITY_RU.md: 3–5 identity/projection.
- Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md: 3 allocation+consumed; 5 reuse; 7 replay.
- Docs/HSB.2C_Journal_Persistence_Reconciliation.md: 3–7 full payload и actual outcomes.
- Docs/HSB_2E_PERSISTENCE_SCHEMA_RU.md: 8–10 более сильные недоказанные file/flush/rename заявления; 15–16 migration.

### Исходные предложения и исторические отчёты

Reports/HSBI_MONEY_CONTRACT_OWNER_DECISIONS_RU.md; HSBI_MONEY_CONTRACT_PROPOSED_SPEC_RU.md; HSBI_R11_P0_DEPENDENCY_PLAN_RU.md; HSBI_R11_P0_TEST_MATRIX_RU.md; HSBI_R11_P0_UNAPPLIED_PATCH_PLAN_RU.md; HSBI_AUDIT03_CLOSE_FINAL_VERDICT_RU.md; HSBI_AUDIT03_CLOSE_FINDINGS_RECONCILIATION_RU.md; HSBI_AUDIT03_CLOSE_FORMULA_PROOFS_RU.md; HSBI_AUDIT03_CLOSE_SOURCE_CROSSWALK_RU.md; HSBI_AUDIT03_CLOSE_DOCUMENT_COVERAGE_RU.md.

Docs/HSBI_DG01_CONTRACT_RESOLUTION_RU.md: D01 5–19; D02 21–35; D03 37–51; D04 53–67; D05 69–83; D06 85–99; D07 101–115; D08 117–131; CR09 133–147; NUM-EXACT 149–163; NUM-DOMAIN 165–179; NUM-CODEC 181–195; SNAP 197–211; FUNDING 213–227; MQL 229–243; BALANCE 245–259. Это предложения, не автоматически действующая authority.

Дополнительные прочитанные proposal sources: Docs/NEXT_STAGE_02B_R0F_MONEY_CONTRACT_CANDIDATE_RU.md 13–53; NEXT_STAGE_02B_R0F_ECONOMIC_IDENTITY_SPEC_RU.md 10–52; NEXT_STAGE_02B_R0G_MINIMAL_IDENTITY_CONTRACT_RU.md 11–55; NEXT_STAGE_02B_R0D_NUMERIC_CONTRACT_RU.md 7–47; NEXT_STAGE_02B_R0F_NUMERIC_CODEC_OPTIONS_RU.md 17–35; NEXT_STAGE_02B_R0G_CODEC_DECISION_RU.md 9–34; NEXT_STAGE_02B_R0D_SNAPSHOT_IDENTITY_CONTRACT_RU.md 3–24.


## Независимые заключения

Полные предлагаемые нормативные тексты и owner ballot: [HSBI_03D_OWNER_APPROVAL_BALLOT_RU.md](HSBI_03D_OWNER_APPROVAL_BALLOT_RU.md).
Карточки ниже вместе с полным текстом ballot и G1–G8 составляют единый contract review; ни один статус не равен APPROVED.

### D-01 — D-01: Grant, Consumed, Reserved, Free

**Статус:** READY_FOR_OWNER_APPROVAL. **OwnerApproval:** AWAITING.

**Предыдущая норма/источник противоречия:** Docs/08:12 требует полную пятикомпонентную conservation; Docs/32:3 добавляет alreadyConsumed, не уточняя original grants против remaining amounts. S02 смешивает представления.

**Допустимые варианты:** A: immutable original grants + отдельный lifecycle; B: remaining-only, но только с отдельно утверждённой схемой/adapter; C: сохранить неоднозначность — недопустимо.

**Независимая рекомендация и причина:** A: сохраняет исходное распределение и позволяет доказать частичные reservation/consumption без двойного учёта.

**Инварианты/математическое обоснование:** Две независимые identities: ΣG_b=G; G_b=C_b+R_b+F_b. Reserve/release/consume имеют сумму приращений 0. См. отдельное доказательство lifecycle и corrections.

**Предусловия:** Authenticated source, полный registry, утверждённый numeric profile, expected revision, разрешённая allocation policy.

**Постусловия:** Обе identities точны; source зарегистрирован единожды; reject/noop следуют G1–G8.

**Численный домен, типы и точность:** Неотрицательные exact minor units; Draft/Committed — явные фазы. Один статус consumed недостаточен для частичного C/R/F.

**Недопустимые состояния:** Negative/nonfinite component; committed underallocation; changed vector при прежнем total; повторный source grant.

**Ошибка/fail-closed:** REJECT до mutation; неоднозначный legacy representation → quarantine.

**SourceKey/revisions/journal:** SourceKey, ManifestID, BucketID, OperationID, PolicyVersion, Revision. Immutable grants отделены от mutable lifecycle; transaction receipt обязателен.

**Положительные/отрицательные тесты и контрпримеры:** T01+: G100, grants20×5, первый bucket C7/R3/F10 → valid. T01−: committed сумма90 → reject; −1/101 buckets → reject; равный total и иной vector → conflict. Все новые сценарии TEST_SPECIFIED_NOT_RUN.

**Последствия для старого кода/совместимости:** S02:5–10 и S03:4–5 не реализуют новый contract; remaining-only adapter допустим только по D16.

**Последствия для R1.1:** Exact ledger schema, phase-aware guards, registry transaction; зависит D10/D14/D16.

**Оставшиеся предположения/внешние зависимости:** Durable registry и доказанное mapping старых balances не квалифицированы.

### D-02 — D-02: Projected и подтверждённые состояния

**Статус:** READY_FOR_OWNER_APPROVAL. **OwnerApproval:** AWAITING.

**Предыдущая норма/источник противоречия:** Docs/31:5 различает projected proof и actual funds. S16:12 runtimeConfirmed означает успешный расчёт, не broker settlement.

**Допустимые варианты:** A: типизированные состояния и независимая authority; B: caller flags; C: scalar/digest. Только A достаточен.

**Независимая рекомендация и причина:** A: отделяет математический preview от происхождения и расходуемости денег.

**Инварианты/математическое обоснование:** G_b=C_b+R_b+F_b относится к allocated grant. Не существует арифметического правила positive(projected)⇒confirmed/spendable.

**Предусловия:** Тип, source, currency/profile, basis, snapshot и revision установлены до принятия scalar.

**Постусловия:** Preview не создаёт balance; actual/allocated effect только через registry receipt.

**Численный домен, типы и точность:** Шесть money states имеют разные значения, даже если число совпало. Общие типы G1–G8.

**Недопустимые состояния:** Projected используется как funds; proof/scalar mismatch; unknown actual origin.

**Ошибка/fail-closed:** Mismatch → CONFLICT; missing independent evidence → UNAVAILABLE; mutation запрещена.

**SourceKey/revisions/journal:** SourceKey + proof identity + provider receipt + allocation/revision binding; self-copy identity не authentication.

**Положительные/отрицательные тесты и контрпримеры:** T02+: actual50,grant40,C10,R5 → book-free25 при authority. T02−: projected50/runtimeConfirmed=true без actual receipt → spendable0/UNAVAILABLE. Все новые сценарии TEST_SPECIFIED_NOT_RUN.

**Последствия для старого кода/совместимости:** S04:24–33,44–75 принимает projected proofs и flags; S07:119–127 не заменяет независимую authority.

**Последствия для R1.1:** Разделить preview/funds DTO и public gates; D08/D13/D14 interfaces.

**Оставшиеся предположения/внешние зависимости:** Actual-source provider и полнота inventory не доказаны.

### D-03 — D-03: Small отдельно от BigReserve

**Статус:** READY_FOR_OWNER_APPROVAL. **OwnerApproval:** AWAITING.

**Предыдущая норма/источник противоречия:** Docs/08:18 bucket restrictions и Docs/31:5 reserve source roles. Прежняя ссылка на LevelMoney для суммы Small ошибочна: фактическая сумма в S15:17.

**Допустимые варианты:** A: BigReserve только допустимые Big sources; B: включить Small; C: отдельный утверждённый transfer Small с attribution. Рекомендуется A; C требует отдельного разрешения.

**Независимая рекомендация и причина:** Экономический итог корзины не определяет eligibility каждого денежного источника.

**Инварианты/математическое обоснование:** EconomicBasketNet и EligibleBigBasis различны; max(0,−10+0+100)=90 не доказывает Big grant.

**Предусловия:** Полная role/source association и утверждённая eligibility policy.

**Постусловия:** Small не повышает Big capacity; общий экономический ledger не теряет Small fact.

**Численный домен, типы и точность:** Money в одном profile; Role — closed enum, не произвольный integer.

**Недопустимые состояния:** Unknown role; агрегатный net используется вместо per-source eligibility.

**Ошибка/fail-closed:** Неизвестная/несогласованная role → reject/unavailable без funding.

**SourceKey/revisions/journal:** SourceKey/role association immutable; transfer имеет отдельный receipt и revisions обеих сторон.

**Положительные/отрицательные тесты и контрпримеры:** T03+: Core40,Trend10,Small100 → eligible Big basis50. T03−: Core−10,Trend0,Small100 → Big0, economic90. Все новые сценарии TEST_SPECIFIED_NOT_RUN.

**Последствия для старого кода/совместимости:** Исправлять в будущем нужно HSBI_EvaluateBasketMoney, S15:11–19; не приписывать суммирование S16.

**Последствия для R1.1:** Eligibility aggregation + D02/D14; historical mixed grants через D16.

**Оставшиеся предположения/внешние зависимости:** Независимая role attribution, legacy mapping, отдельная transfer policy при выборе C.

### D-04 — D-04: Absolute Far Loss

**Статус:** READY_FOR_OWNER_APPROVAL. **OwnerApproval:** AWAITING.

**Предыдущая норма/источник противоречия:** Docs/04:15,24 и Docs/12:9 требуют фактического покрытия; baseline delta не равна полному обязательству.

**Допустимые варианты:** A: absolute loss; B: incremental-only funding; C: оба показателя, absolute для coverage. Рекомендуется C; B недопустим для покрытия.

**Независимая рекомендация и причина:** Диагностический прирост не должен скрывать уже существующее обязательство.

**Инварианты/математическое обоснование:** Baseline40,current50 дают incremental10, но обязательство50. Margin=eligibleGain−absoluteLoss−buffer.

**Предусловия:** Far proof с определённым close-now/cost basis; согласованные единицы и source receipt.

**Постусловия:** Gate не принимает delta за полный loss; mismatch блокирует расчёт.

**Численный домен, типы и точность:** Неотрицательный loss; signed Far net; preview не обязательно в minor units.

**Недопустимые состояния:** Negative/nonfinite amount; loss иной позиции/объёма; scalar != proof-derived amount.

**Ошибка/fail-closed:** CONFLICT при binding mismatch; UNAVAILABLE при missing cost/source evidence.

**SourceKey/revisions/journal:** Far position/source tuple, plan/snapshot/revision, cost profile и registry references.

**Положительные/отрицательные тесты и контрпримеры:** T04+: gain40,loss20,buffer1 → preview margin19. T04−: baseline40,absolute50,reserve30 → reject несмотря на delta10. Все новые сценарии TEST_SPECIFIED_NOT_RUN.

**Последствия для старого кода/совместимости:** S04:30–33,73–75 не доказывает binding всех scalars. S07:121–122 выводит scalars из proofs: дефект public evaluator не объявляется автоматически solver exploit.

**Последствия для R1.1:** D02/D06/CR09; explicit amount/basis guards и provider.

**Оставшиеся предположения/внешние зависимости:** Actual close costs и broker evidence; глобальная loss bound отдельно ERR038.

### D-05 — D-05: Current accounting и sticky safety breach

**Статус:** READY_FOR_OWNER_APPROVAL. **OwnerApproval:** AWAITING.

**Предыдущая норма/источник противоречия:** Docs/04:24, Docs/13:9 задают current loss. S19:8 не содержит полной sticky/reset/history policy. Это новый policy choice.

**Допустимые варианты:** A: current-only; B: current+sticky с явным reset; C: peak вместо current. Рекомендуется B; peak хранится отдельно.

**Независимая рекомендация и причина:** Current нужен для текущего accounting, sticky сохраняет факт прежнего safety cap breach.

**Инварианты/математическое обоснование:** Fills −15,+100; H12 → net85,current0,peak15,stickytrue. Обратный порядок +100,−15 → net85,current0,peak0,stickyfalse. Final net не определяет ordered breach.

**Предусловия:** Frozen membership/cap, независимо подтверждённые actual fills, установленный порядок, полный журнал.

**Постусловия:** Breach монотонен внутри MonitoringEpoch; reset явно receipt-authorised; history остаётся неизменной.

**Численный домен, типы и точность:** Signed net и nonnegative loss/cap в согласованном денежном профиле; CapEpoch/MonitoringEpoch не переиспользуются.

**Недопустимые состояния:** Reset по net>0; cap задним числом; restart без восстановления sticky; guessed chronology.

**Ошибка/fail-closed:** Unknown/corrupt history → UNAVAILABLE/manual-safe. Unauthorized/stale reset → reject. SAFE exit не включает автоматический dispatch.

**SourceKey/revisions/journal:** Broker chronology отличается от observation order. EventID не доказывает порядок; broker evidence+association+durable observation journal обязательны.

**Положительные/отрицательные тесты и контрпримеры:** T05±: две последовательности выше; −12/H12 → stickyfalse; restart на каждом prefix; corrupt history; unauthorized/stale/duplicate reset; no autoresume. Все новые сценарии TEST_SPECIFIED_NOT_RUN.

**Последствия для старого кода/совместимости:** S19:8 и S07 cap/transition paths не реализуют этот stateful contract; точная интеграция отдельно.

**Последствия для R1.1:** Новые persisted epoch/sticky/peak/receipt fields и reset authority interface; реализация не ready до owner approval reset policy.

**Оставшиеся предположения/внешние зависимости:** Ordered-history provider и durable state ещё не квалифицированы; owner должен явно принять предложенную reset policy.

### D-06 — D-06: Расходы, EconomicCyclePnL и RecoveryResult

**Статус:** CONFLICTING. **OwnerApproval:** AWAITING.

**Предыдущая норма/источник противоречия:** Docs/09:20 исключает Initial Profit из RealizedCycleNet/бюджетов. Формула «все realized deals» молча меняет эту норму. S14 задаёт arithmetic, но не полный membership/cost basis; S19 не вся FinalClose authority.

**Допустимые варианты:** A: сохранить Initial exclusion в RecoveryResult, отдельно полный EconomicCyclePnL; B: явно изменить Docs/09:20 и включить Initial; C: один неуточнённый CyclePnL — недопустимо.

**Независимая рекомендация и причина:** A до отдельного owner policy change; статус CONFLICTING сохраняется до выбора A/B.

**Инварианты/математическое обоснование:** Initial50,otherRealized−10,open−5 → Economic35,Recovery−15 при A. Gross100+commission−2+swap−1+fee−1=96, не92.

**Предусловия:** Явный выбор A/B; cost inventory с включённостью, горизонтом и независимыми receipts.

**Постусловия:** Каждый economic expense учитывается один раз в каждом определённом result; buckets не добавляются как прибыль.

**Численный домен, типы и точность:** Signed actual net и отдельно projected costs/buffers; currency/posting profile обязателен.

**Недопустимые состояния:** Initial молча включён вопреки норме; повтор cost deduction; profit buffer выдан за expense/fill.

**Ошибка/fail-closed:** Неопределённый membership/cost inclusion → UNAVAILABLE; conflicting receipts → CONFLICT.

**SourceKey/revisions/journal:** Cost fact/receipt связывает deal, interval, basis, profile; один physical expense не появляется дважды из разных DTO.

**Положительные/отрицательные тесты и контрпримеры:** T06+: net96 из компонентов. T06−: Initial example выше; open-close-now уже включает cost3 — повторное −3 запрещено. Все новые сценарии TEST_SPECIFIED_NOT_RUN.

**Последствия для старого кода/совместимости:** S14:11–18, S15:7–19, S19:9 требуют общего basis; одинаковый execution buffer для legs также нуждается в явном scope.

**Последствия для R1.1:** Owner A/B first; D02/D11/D13; отдельные result names и FinalClose gates Docs/12:7–15.

**Оставшиеся предположения/внешние зависимости:** Broker posting/cost conventions и Initial policy decision отсутствуют; конфликт не разрешён публикацией.

### D-07 — D-07: Execution, durable journal, restart

**Статус:** READY_FOR_OWNER_APPROVAL. **OwnerApproval:** AWAITING.

**Предыдущая норма/источник противоречия:** Docs/06:9–21, Docs/07:12–24, Docs/16:6–18. S12:25–29 duplicate раньше body validation; S10:20–22 UNKNOWN допускает локальный retry; S13 stub.

**Допустимые варианты:** A: durable effect+receipt transaction; B: только in-memory idempotence; C: blind retry. Только A достаточен.

**Независимая рекомендация и причина:** Exactly-once effect требует durable evidence и reconciliation, а не только matching IDs.

**Инварианты/математическое обоснование:** Повтор effect должен иметь Δbalance=0; atomic commit исключает state без receipt и receipt без state.

**Предусловия:** Полный валидный body, durable store, association/reconciliation provider, current revision для нового event.

**Постусловия:** Commit единожды либо no mutation; recovery не конструирует недоказанный результат.

**Численный домен, типы и точность:** IDs и CommitSequence раздельны; signed money exact; MAX revision не increment.

**Недопустимые состояния:** Duplicate по одному digest; UNKNOWN retry; journal order основан только на величине EventID.

**Ошибка/fail-closed:** Conflict/unknown → blocked; corrupted/torn state → fail-closed, не guess repair.

**SourceKey/revisions/journal:** Source/Action/Event/Observation/CommitSequence, old receipt и hash chain; durability отдельно от chain validity.

**Положительные/отрицательные тесты и контрпримеры:** T07+: exact restart replay → NOOP. T07−: changed body/old digest; crash между balance/receipt; UNKNOWN resend; новый ObservationID старого fill. Все новые сценарии TEST_SPECIFIED_NOT_RUN.

**Последствия для старого кода/совместимости:** S12 full body before duplicate, S10 retry/barrier и S13 backend требуют будущих изменений.

**Последствия для R1.1:** A/B/E interface; crash matrix; Docs/16 crash-consistency не доказывает более сильные flush/rename обещания Docs/HSB_2E:8–10.

**Оставшиеся предположения/внешние зависимости:** Durable implementation и platform crash evidence отсутствуют.

### D-08 — D-08: Broker/server/account/source identity

**Статус:** READY_FOR_OWNER_APPROVAL. **OwnerApproval:** AWAITING.

**Предыдущая норма/источник противоречия:** Docs/08:9,15; R0G minimal identity 11–55. S01:7 пропускает namespace, S01:9 неполное body compare.

**Допустимые варианты:** A: codec-independent logical key+full attributed body; B: hash wire bytes как source; C: caller EventID как source. Рекомендуется A.

**Независимая рекомендация и причина:** Одна физическая сделка не становится новыми деньгами при переимпорте/codec change.

**Инварианты/математическое обоснование:** Равный net не равен равному body. Тот же ticket при иных account/server — другой source. Новый observation старого K — не новый economic capacity.

**Предусловия:** Stable namespace, independent actual source и EA association для cycle/role/action/plan/policy.

**Постусловия:** Один source lifetime через imports/codecs; исправления append-only; no implicit funding.

**Численный домен, типы и точность:** Account positive signed64; deal/order/position IDs ulong; money/profile; finite volume/price; closed enums; timestamp unit/domain.

**Недопустимые состояния:** Guess missing namespace; changed role/position/price/volume; same net как единственный comparator.

**Ошибка/fail-closed:** Missing required field → UNAVAILABLE; same K/changed body → CONFLICT; unknown complete history → no new funding.

**SourceKey/revisions/journal:** Полный envelope 29 fields перечислен ниже; immutable EconomicEventID отделён от ObservationID.

**Положительные/отрицательные тесты и контрпримеры:** T08+: тот же K/body новый ObservationID → один source. T08−: equal net/changed components, role/position/price/volume → conflict; ticket разные accounts → distinct sources. Все новые сценарии TEST_SPECIFIED_NOT_RUN.

**Последствия для старого кода/совместимости:** S01/S06/S07 caller-origin identities не независимая authority.

**Последствия для R1.1:** Full schema, source/body validator, actual association, codec/migration interfaces.

**Оставшиеся предположения/внешние зависимости:** Broker history не даёт EA cycle/action/role/plan/policy; нужен независимый association provider.

### D-09 — CR-09: All-level NewFar/FutureSmall

**Статус:** READY_FOR_OWNER_APPROVAL. **OwnerApproval:** AWAITING.

**Предыдущая норма/источник противоречия:** Docs/30:3–7 complete finite proof; S08:50 max TransitionLoss selection не доказывает min CatchUpMargin.

**Допустимые варианты:** A: every required finite level; B: один controlling level; C: global infinite-tail guarantee без отдельной теоремы. Рекомендуется A; C только с дополнительным доказательством.

**Независимая рекомендация и причина:** Разные экстремумы достигаются на разных уровнях; objective не заменяет feasibility.

**Инварианты/математическое обоснование:** Losses(10,5),margins(9,−11) → max loss level1, min margin level2; candidate reject.

**Предусловия:** Установленные required depth/set, policies, per-level proofs и basis.

**Постусловия:** Ни один required level не пропущен; tail не объявлен доказанным.

**Численный домен, типы и точность:** Finite indexed set, level ID и complete coverage; nonfinite aggregate отвергается.

**Недопустимые состояния:** Proxy-only proof; chosen level выдаётся за all-level; finite prefix выдаётся за infinity guarantee.

**Ошибка/fail-closed:** UNAVAILABLE для missing proof; REJECT для отрицательной margin; никакого funding по preview.

**SourceKey/revisions/journal:** Каждый level proof связан с plan/snapshot/source/profile/revision; aggregate receipt содержит полный набор.

**Положительные/отрицательные тесты и контрпримеры:** T09+: losses10,5/margins9,2 → feasible. T09−: margins9,−11 → reject независимо от max-loss level. Все новые сценарии TEST_SPECIFIED_NOT_RUN.

**Последствия для старого кода/совместимости:** S08:23–58 и S07:114–151 требуют согласованных all-level gates.

**Последствия для R1.1:** D04/D06/D13/D14. Дополнительный нерешённый конфликт: Docs/14:22–23 minimum-safe-first против Docs/29:3 risk-first; S07:149 risk-first.

**Оставшиеся предположения/внешние зависимости:** Owner objective decision; tail/market assumptions; ERR038 отдельный proof.

### D-10 — NUM-EXACT-1: Точный settled accounting

**Статус:** READY_FOR_OWNER_APPROVAL. **OwnerApproval:** AWAITING.

**Предыдущая норма/источник противоречия:** S01/S02/S03 используют double/epsilon; reference unlimited integers не являются MQL5 domain.

**Допустимые варианты:** A: checked signed64 minor units; B: иной полностью qualified exact representation; C: double/epsilon для settled identities. Рекомендуется A при доказанном profile; B отдельная архитектурная альтернатива.

**Независимая рекомендация и причина:** Точные balances и overflow guards дают проверяемую conservation без скрытой epsilon capacity.

**Инварианты/математическое обоснование:** MAX+1,abs(MIN),MIN×−1 invalid. MAX+MAX−MAX−MAX mathematically0, но unsafe intermediates. G10000=C3000+R2000+F5000 точно.

**Предусловия:** Numeric manifest, profile и checked arithmetic; validated conversion receipt.

**Постусловия:** Exact identities либо reject before overflow; previews сохраняют свой domain.

**Численный домен, типы и точность:** Signed64 money; ulong IDs раздельно. Для scale100 max main units=92233720368547758.07.

**Недопустимые состояния:** Out-of-range amount/intermediate; lossy double ID; early zeroing preview loss0.004.

**Ошибка/fail-closed:** Overflow/invalid conversion → REJECT/UNAVAILABLE без mutation.

**SourceKey/revisions/journal:** Profile/schema/version и original posting receipt обязательны; codec не меняет source.

**Положительные/отрицательные тесты и контрпримеры:** T10+: exact split10000. T10−: boundaries выше; positive projected0.004 не доказывает zero loss. Все новые сценарии TEST_SPECIFIED_NOT_RUN.

**Последствия для старого кода/совместимости:** Numeric DTO/schema migration required; без автоматической замены старого representation.

**Последствия для R1.1:** D11/D12/D15 numeric bundle; principles можно голосовать, concrete implementation ещё не frozen.

**Оставшиеся предположения/внешние зависимости:** Currency profile/native evidence; другой exact representation требует отдельного доказательства.

### D-11 — NUM-DOMAIN-1: Currency, precision, limits

**Статус:** BLOCKED_BY_EVIDENCE. **OwnerApproval:** AWAITING.

**Предыдущая норма/источник противоречия:** Fixture precision0…8 не broker evidence. BrokerProperties.digits — цена symbol, не monetary currency precision. S18 zero-origin против Docs/14:9 Vmin+nstep.

**Допустимые варианты:** A: evidenced currency/posting/grid profile; B: fixture default; C: universal HALF_EVEN. Только A достаточен.

**Независимая рекомендация и причина:** Rounding определяется фактическим posting stage; универсальное правило создаёт разные деньги.

**Инварианты/математическое обоснование:** HALF_EVEN cents: отдельно0.005+0.005→0; aggregate→0.01. Для −0.005−0.005:0 против−0.01. Scale100 signedMAX main=92233720368547758.07.

**Предусловия:** Broker/account currency evidence, posting policy и grid profile; native qualification.

**Постусловия:** Один воспроизводимый conversion path; unknown profile не создаёт money.

**Численный домен, типы и точность:** Известный scale; exact range; price/volume grid и minimum отдельно. Fixture0…8 не universal production promise.

**Недопустимые состояния:** Price digits как currency digits; component/aggregate mixing; fake adjustment; underflow changing gate.

**Ошибка/fail-closed:** No profile → UNAVAILABLE. No guessed defaults.

**SourceKey/revisions/journal:** CurrencyProfileID/PostingProfileID/GridProfileID versions + source receipt.

**Положительные/отрицательные тесты и контрпримеры:** T11+: aggregate HALF_EVEN0.005+0.005→1 minor. T11−: component result0 под aggregate receipt→conflict; min0.03/step0.02 distinguishes grid origins. Все новые сценарии TEST_SPECIFIED_NOT_RUN.

**Последствия для старого кода/совместимости:** S18 and monetary DTOs need explicit profile; no old precision reinterpretation.

**Последствия для R1.1:** Joint numeric bundle D10/D12/D15 plus snapshot/provider evidence.

**Оставшиеся предположения/внешние зависимости:** Production currency/posting profiles и grid convention не квалифицированы; BLOCKED_BY_EVIDENCE сохраняется.

### D-12 — NUM-CODEC: Canonical wire encoding

**Статус:** BLOCKED_BY_EVIDENCE. **OwnerApproval:** AWAITING.

**Предыдущая норма/источник противоречия:** R0F codec options17–35 и R0G codec9–34: F64Z candidate, native unqualified. Буквы вариантов в старых proposals различаются.

**Допустимые варианты:** F64Z; T17Z; иной полностью specified/qualified codec. Голосовать по имени+версии, не букве.

**Независимая рекомендация и причина:** Logical identity отделить сейчас; final wire codec не freeze до native goldens/hostile decoder.

**Инварианты/математическое обоснование:** Decode(Encode(x))=x в declared semantic domain, не обязательно raw packet. Crosscodec same fact → один K.

**Предусловия:** Frozen schema/order/limits/zero policy и native build evidence.

**Постусловия:** Canonical unique bytes в profile либо reject; semantic source unchanged.

**Численный домен, типы и точность:** Finite binary64 candidate; exact u64/i64; typed UTF-8 lengths; explicit bool/absent; bounded record sizes.

**Недопустимые состояния:** Unknown schema,malformed framing,NUL ambiguity,oversize,nonfinite,lossy ID,implicit normalization.

**Ошибка/fail-closed:** Strict decoder REJECT; unqualified codec domain UNAVAILABLE.

**SourceKey/revisions/journal:** Schema/codec metadata не входит как новая economic identity; original full body и migration receipt сохраняются.

**Положительные/отрицательные тесты и контрпримеры:** T12+: один fact в двух qualified codecs→один source. T12−: truncated/unknown/trailing bytes reject; maxulong/subnormal/negativezero/UTF8 roundtrip. Все новые сценарии TEST_SPECIFIED_NOT_RUN.

**Последствия для старого кода/совместимости:** S01:11 and S06:23–28 rounded text не canonical economic wire proof.

**Последствия для R1.1:** D08/D10/D11/D15 joint bundle; do not freeze F64Z on reference evidence.

**Оставшиеся предположения/внешние зависимости:** Native binary64/UTF-8/decoder evidence отсутствует; candidate caps также требуют hostile qualification.

### D-13 — SNAP-FIXTURE-1: Snapshot freshness и content receipt

**Статус:** REQUIRES_CLARIFICATION. **OwnerApproval:** AWAITING.

**Предыдущая норма/источник противоречия:** Docs/31:3–5 и R0D snapshot contract отделяют fixture monotonic ticks от server UTC. S17:11 нет lower-bound future check.

**Допустимые варианты:** A: provider clock/receipt profile; B: caller fresh bool; C: digest без source receipt. Рекомендуется A.

**Независимая рекомендация и причина:** Freshness имеет смысл только в известном clock domain и не доказывает content origin.

**Инварианты/математическое обоснование:** Exact clock now100,ts95,TTL10 fresh; ts101 future invalid; ts89 stale.

**Предусловия:** Реальные providers, units, clock uncertainty и receipt authority должны быть выбраны.

**Постусловия:** Принятый snapshot имеет verified age и content binding; stale/future/substituted rejected.

**Численный домен, типы и точность:** Timestamp с domain/unit; TTL и uncertainty bounded; arithmetic overflow checked.

**Недопустимые состояния:** Future accepted из-за отрицательного age; fixture tick как UTC; unchanged ID changed price.

**Ошибка/fail-closed:** Unknown clock → UNAVAILABLE, mismatch→CONFLICT; no guessed tolerance.

**SourceKey/revisions/journal:** Provider+content receipt+snapshot revision; content hash не независимая authentication.

**Положительные/отрицательные тесты и контрпримеры:** T13± exact examples; changed price под old receipt conflict; TTL endpoints; cross-clock reject. Все новые сценарии TEST_SPECIFIED_NOT_RUN.

**Последствия для старого кода/совместимости:** S17:11,16–24; S06/S07 требуют независимого receipt, не только свежих flags.

**Последствия для R1.1:** Provider profile first; D08/D12/D15 и actual freshness integration.

**Оставшиеся предположения/внешние зависимости:** Нужно уточнить providers,domains,units,uncertainty. Статус REQUIRES_CLARIFICATION.

### D-14 — FUNDING-GLOBAL-ATTRIBUTION: Единый атомарный source registry

**Статус:** READY_FOR_OWNER_APPROVAL. **OwnerApproval:** AWAITING.

**Предыдущая норма/источник противоречия:** Docs/08:12–24; S04/S05 local checks не global authority; S13 durable implementation отсутствует.

**Допустимые варианты:** A: единый serializable inventory; B: independent local ledgers; C: новый EventID→новые деньги. Только A достаточен.

**Независимая рекомендация и причина:** Conservation должна сохраняться между consumers, roles, allocation IDs и restarts.

**Инварианты/математическое обоснование:** Free50; concurrent requests30+30 same revision → at most one commit, затем Free20; второй conflict.

**Предусловия:** Independent source inventory, serializable durable backend, defined authority scope.

**Постусловия:** No overspend/double grant; state+receipt atomic; restart same inventory.

**Численный домен, типы и точность:** Exact nonnegative balances, checked totals/revisions; account margin — отдельный risk domain.

**Недопустимые состояния:** Local replay set выдан за completeness; per-allocation source reuse; partial transfer.

**Ошибка/fail-closed:** Registry unavailable/ambiguous→no new spend; transaction conflict→no mutation.

**SourceKey/revisions/journal:** Global K, manifest,bucket,operation,policy,revision; balances+receipts and uniqueness atomic.

**Положительные/отрицательные тесты и контрпримеры:** T14+: first30 commit→Free20. T14−: second30 same revision rejected; crash/multi-source/restart tests обязательны. Все новые сценарии TEST_SPECIFIED_NOT_RUN.

**Последствия для старого кода/совместимости:** S04:44–70/S05 validate shapes только; реализация registry НЕ считается существующей.

**Последствия для R1.1:** B/D/E plus independent provider; funding registry не заменяет capital/free-margin gate.

**Оставшиеся предположения/внешние зависимости:** Durable provider, real concurrency/crash evidence отсутствуют; это архитектурное требование, не PASS.

### D-15 — MQL-DOMAIN: Нативные границы MQL5

**Статус:** READY_FOR_OWNER_APPROVAL. **OwnerApproval:** AWAITING.

**Предыдущая норма/источник противоречия:** Reference/C++ shim не квалифицируют native MQL5. Native tests не выполнены.

**Допустимые варианты:** A: bounded evidence-qualified native domain; B: перенос reference PASS; C: декларация полного binary64 domain без tests. Рекомендуется A.

**Независимая рекомендация и причина:** Language/platform conversions и persistence могут отличаться от reference mathematics.

**Инварианты/математическое обоснование:** Математическое равенство не доказывает отсутствие overflow/rounding implementation; oracle domain явно отделён.

**Предусловия:** Frozen numeric manifest, exact vectors, no dispatch, recorded build.

**Постусловия:** Каждый qualified subdomain имеет reproducible evidence; остальные remain unverified.

**Численный домен, типы и точность:** Native i64/u64/binary64/string/bytes/grid; detailed limits в qualification report.

**Недопустимые состояния:** Native_PASS без native run; cast через double больших IDs; invalid enum accepted.

**Ошибка/fail-closed:** Unsupported/untested domain→UNAVAILABLE; nonfinite/out-of-range→REJECT.

**SourceKey/revisions/journal:** Evidence связывает source SHA,compiler/terminal build,profile,test version,inputs/actual/log.

**Положительные/отрицательные тесты и контрпримеры:** T15+: ulong18446744073709551615 exact roundtrip. T15−: nonfinite money,invalid enum,subminimum volume→reject; полный native matrix отдельно. Все новые сценарии TEST_SPECIFIED_NOT_RUN.

**Последствия для старого кода/совместимости:** S01–S20 остаются неквалифицированными одним reference result; source reading не compile.

**Последствия для R1.1:** D10/D11/D12 bundle; сейчас можно утвердить requirement, не concrete native PASS.

**Оставшиеся предположения/внешние зависимости:** Native MQL5 environment/evidence отсутствуют; NATIVE_NOT_RUN.

### D-16 — BALANCE-SCHEMA-MAPPING: Fail-closed legacy migration

**Статус:** READY_FOR_OWNER_APPROVAL. **OwnerApproval:** AWAITING.

**Предыдущая норма/источник противоречия:** Docs/16:18 unknown schema rejects. Legacy S01/S02 не содержат весь новый identity/balance evidence.

**Допустимые варианты:** A: proven versioned mapping; B: quarantine unknown records; C: fill defaults/current account. A+B совместимы и рекомендуются, C запрещён.

**Независимая рекомендация и причина:** Неизвестная история не должна превращаться в новые spendable funds.

**Инварианты/математическое обоснование:** Known G100,C20,R10,F70 сохраняет identity100=20+10+70; available100 без consumed не позволяет вывести исходный grant.

**Предусловия:** Known schema/mapping, independent source facts, complete applied-event evidence.

**Постусловия:** No invented balance/identity; exact migration preserves history; unknown remains quarantined.

**Численный домен, типы и точность:** Versioned exact representation; timestamp precision не повышается без evidence.

**Недопустимые состояния:** Defaults account/server/consumed0; revision reset; duplicate source под new schema.

**Ошибка/fail-closed:** Unknown→quarantine/UNAVAILABLE; contradictory mapping→CONFLICT.

**SourceKey/revisions/journal:** Old record/schema reference + MappingVersion + K + migration receipt + expected registry revision.

**Положительные/отрицательные тесты и контрпримеры:** T16+: complete known split100/20/10/70 migrated, replay NOOP. T16−: available100 без namespace/consumed→quarantine/spendable0. Все новые сценарии TEST_SPECIFIED_NOT_RUN.

**Последствия для старого кода/совместимости:** Нельзя автоматически интерпретировать смешанный DTO S02 как original или remaining.

**Последствия для R1.1:** D01/D07/D08/D10 interfaces; отдельная квалификация реального legacy corpus.

**Оставшиеся предположения/внешние зависимости:** Фактическая completeness legacy sources и mapping evidence не доказаны.

## Существенные отличия от предыдущих рекомендаций

1. D03: источник суммы Small — Basket evaluator S15:17; не LevelMoney evaluator. Различие исправлено в этом новом отчёте, исторические файлы не переписаны.
2. D06: «all realized» не принимается автоматически: Docs/09:20 исключает Initial. EconomicCyclePnL и RecoveryResult разделены; A/B остаётся owner choice.
3. D05: готовая proposed reset policy содержит authority,conditions,receipt,epoch,restart,SAFE consequences. Это не реализованная функция и не owner approval.
4. D08/D12: logical K и wire codec отделены; новый ObservationID/codec не новый grant. Registry completeness и локальная equality — разные требования.
5. D10–D12/D15: unlimited reference arithmetic и F64Z proposal не объявлены native-qualified. Сохранён реальный approval cycle.
6. ERR048: public evaluator binding gap не автоматически доказанный solver exploit: S07:121–122 derives amounts.
7. Correction не «исправляет» conservation удалением consumed: immutable history + linked correction hold/deficit до отдельного settlement contract.
8. NewFar objective Docs/14 против Docs/29 остаётся отдельным нормативным конфликтом; money ballot не разрешает его.
9. ERR038 не закрывается bounded lots/денежным контрактом.

## Связанные доказательства и пределы

[Conservation/identity/sticky/cost/counterexamples](HSBI_03D_MONEY_INVARIANTS_AND_COUNTEREXAMPLES_RU.md);
[dependency cycles/несовместимости](HSBI_03D_CONTRACT_CONSISTENCY_MATRIX_RU.md);
[14 P0](HSBI_03D_P0_REMEDIATION_CROSSWALK_RU.md);
[native matrix и fixed vectors](HSBI_03D_NUMERIC_NATIVE_QUALIFICATION_RU.md);
[R1.1 gates](HSBI_03D_R11_READINESS_GATES_RU.md).
Исторические7 PASS/16 FAIL сохранены как HISTORICAL_TEST_RESULT, два contract-dependent случая отдельно. Исторические expected/frozen evidence не менялись. Наличие отчёта не делает описанный gap resolved.

AUDIT_STATUS=PARTIAL; R11_IMPLEMENTATION_ALLOWED=NO; BROKER_DISPATCH_ALLOWED=NO; REAL_TRADING_ALLOWED=NO.
