# HSBI-03D — Бюллетень утверждения владельца

Версия предлагаемого текста **HSBI-03D-REMOTE-R1**. Scope: денежная policy/specification; не implementation/trading permission.
Ни одного owner approval нет. Точная версия и blob SHA принятого текста должны быть записаны отдельным явным решением владельца после публикации. Пустое поле/молчание не approval. Исторические proposals не получили приоритет действующей нормы автоматически.

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

## Порядок голосования

Для каждой карточки владелец отдельно фиксирует CanonicalDecisionId, выбранный именованный вариант, версию текста/commit+blob, scope, дату, identity владельца и решение APPROVE/REJECT/DEFER. Изменённый текст требует новой версии и consistency review. D06 требует A/B; D11/D12 остаются evidence-blocked; D13 требует profile clarification. Numeric concrete freeze — только совместный D10/D11/D12/D15 manifest с native evidence. READY не разрешает реализацию.

## D-01 — D-01: Grant, Consumed, Reserved, Free

Статус READY_FOR_OWNER_APPROVAL; OwnerDecision=AWAITING.
Варианты: A: immutable original grants + отдельный lifecycle; B: remaining-only, но только с отдельно утверждённой схемой/adapter; C: сохранить неоднозначность — недопустимо.
Рекомендация: A: сохраняет исходное распределение и позволяет доказать частичные reservation/consumption без двойного учёта.

### Полный предлагаемый нормативный текст

> Для одного подтверждённого источника исходный allocatable grant G распределяется единственным committed manifest по пяти bucket grants: G=C+P+T+K+R. Слагаемые — исходные grants соответствующих buckets, не потребление. Для каждого b: Grant_b=Consumed_b+Reserved_b+Free_b; все величины неотрицательны, в одном currency/profile. Draft допускает Unassigned≥0 при Σdraft+Unassigned=G и не предоставляет spendable balance. Commit требует Unassigned=0 и атомарной регистрации всего manifest. Consumed и Reserved не прибавляются повторно к исходному пятикомпонентному grant.

Текст применяется вместе с G1–G8 и указанными предпосылками; он не заявляет наличие ещё не созданного provider/journal.

**Математика/контрпример:** Две независимые identities: ΣG_b=G; G_b=C_b+R_b+F_b. Reserve/release/consume имеют сумму приращений 0. См. отдельное доказательство lifecycle и corrections.
**Обязательные тесты:** T01+: G100, grants20×5, первый bucket C7/R3/F10 → valid. T01−: committed сумма90 → reject; −1/101 buckets → reject; равный total и иной vector → conflict. TEST_SPECIFIED_NOT_RUN.
**R1.1 и совместимость:** Exact ledger schema, phase-aware guards, registry transaction; зависит D10/D14/D16. S02:5–10 и S03:4–5 не реализуют новый contract; remaining-only adapter допустим только по D16.
**Оставшиеся предположения:** Durable registry и доказанное mapping старых balances не квалифицированы.
**Пред-/постусловия, domain, error/source requirements:** полная карточка D-01 в [independent review](HSBI_03D_INDEPENDENT_CONTRACT_REVIEW_RU.md).

OwnerDecision=AWAITING; ApprovedVersion=NONE; ImplementationPermission=NO.

## D-02 — D-02: Projected и подтверждённые состояния

Статус READY_FOR_OWNER_APPROVAL; OwnerDecision=AWAITING.
Варианты: A: типизированные состояния и независимая authority; B: caller flags; C: scalar/digest. Только A достаточен.
Рекомендация: A: отделяет математический preview от происхождения и расходуемости денег.

### Полный предлагаемый нормативный текст

> ProjectedReserve — расчёт при заданных предпосылках, не средства. ConfirmedReserve — подтверждённый eligible economic amount, ещё не обязательно allocated. AllocatedReserve — committed grant; ReservedReserve — часть, закреплённая за незавершённой операцией; ConsumedReserve — подтверждённо использованная часть; FreeReserve — остаток D01. SpendableReserve существует только при valid source, полном registry, допустимом lifecycle и актуальной authority. Projected→Confirmed требует независимого actual evidence и association receipt; положительное число, digest и runtimeConfirmed этот переход не выполняют.

Текст применяется вместе с G1–G8 и указанными предпосылками; он не заявляет наличие ещё не созданного provider/journal.

**Математика/контрпример:** G_b=C_b+R_b+F_b относится к allocated grant. Не существует арифметического правила positive(projected)⇒confirmed/spendable.
**Обязательные тесты:** T02+: actual50,grant40,C10,R5 → book-free25 при authority. T02−: projected50/runtimeConfirmed=true без actual receipt → spendable0/UNAVAILABLE. TEST_SPECIFIED_NOT_RUN.
**R1.1 и совместимость:** Разделить preview/funds DTO и public gates; D08/D13/D14 interfaces. S04:24–33,44–75 принимает projected proofs и flags; S07:119–127 не заменяет независимую authority.
**Оставшиеся предположения:** Actual-source provider и полнота inventory не доказаны.
**Пред-/постусловия, domain, error/source requirements:** полная карточка D-02 в [independent review](HSBI_03D_INDEPENDENT_CONTRACT_REVIEW_RU.md).

OwnerDecision=AWAITING; ApprovedVersion=NONE; ImplementationPermission=NO.

## D-03 — D-03: Small отдельно от BigReserve

Статус READY_FOR_OWNER_APPROVAL; OwnerDecision=AWAITING.
Варианты: A: BigReserve только допустимые Big sources; B: включить Small; C: отдельный утверждённый transfer Small с attribution. Рекомендуется A; C требует отдельного разрешения.
Рекомендация: Экономический итог корзины не определяет eligibility каждого денежного источника.

### Полный предлагаемый нормативный текст

> Small contribution учитывается в соответствующем экономическом результате корзины, но не входит в BigReserve eligibility. BigReserve рассчитывается только из independently attributed допустимых Big sources. Нельзя получить BigReserve через max(0,BigCore+BigTrend+Small). Перевод Small в иной bucket допускается лишь отдельным разрешённым атомарным transfer с сохранением source attribution и не создаёт новую прибыль.

Текст применяется вместе с G1–G8 и указанными предпосылками; он не заявляет наличие ещё не созданного provider/journal.

**Математика/контрпример:** EconomicBasketNet и EligibleBigBasis различны; max(0,−10+0+100)=90 не доказывает Big grant.
**Обязательные тесты:** T03+: Core40,Trend10,Small100 → eligible Big basis50. T03−: Core−10,Trend0,Small100 → Big0, economic90. TEST_SPECIFIED_NOT_RUN.
**R1.1 и совместимость:** Eligibility aggregation + D02/D14; historical mixed grants через D16. Исправлять в будущем нужно HSBI_EvaluateBasketMoney, S15:11–19; не приписывать суммирование S16.
**Оставшиеся предположения:** Независимая role attribution, legacy mapping, отдельная transfer policy при выборе C.
**Пред-/постусловия, domain, error/source requirements:** полная карточка D-03 в [independent review](HSBI_03D_INDEPENDENT_CONTRACT_REVIEW_RU.md).

OwnerDecision=AWAITING; ApprovedVersion=NONE; ImplementationPermission=NO.

## D-04 — D-04: Absolute Far Loss

Статус READY_FOR_OWNER_APPROVAL; OwnerDecision=AWAITING.
Варианты: A: absolute loss; B: incremental-only funding; C: оба показателя, absolute для coverage. Рекомендуется C; B недопустим для покрытия.
Рекомендация: Диагностический прирост не должен скрывать уже существующее обязательство.

### Полный предлагаемый нормативный текст

> Для данного Far obligation и basis AbsoluteFarLoss=max(0,−FarCloseNet). IncrementalLoss=max(0,AbsoluteFarLoss−BaselineLoss) допускается как диагностика и не заменяет AbsoluteFarLoss в funding gate. Scalar amount, identity, volume, close side, snapshot, currency и cost basis связаны с одним proof. Projected loss применяется только к preview; actual settlement требует отдельного receipt.

Текст применяется вместе с G1–G8 и указанными предпосылками; он не заявляет наличие ещё не созданного provider/journal.

**Математика/контрпример:** Baseline40,current50 дают incremental10, но обязательство50. Margin=eligibleGain−absoluteLoss−buffer.
**Обязательные тесты:** T04+: gain40,loss20,buffer1 → preview margin19. T04−: baseline40,absolute50,reserve30 → reject несмотря на delta10. TEST_SPECIFIED_NOT_RUN.
**R1.1 и совместимость:** D02/D06/CR09; explicit amount/basis guards и provider. S04:30–33,73–75 не доказывает binding всех scalars. S07:121–122 выводит scalars из proofs: дефект public evaluator не объявляется автоматически solver exploit.
**Оставшиеся предположения:** Actual close costs и broker evidence; глобальная loss bound отдельно ERR038.
**Пред-/постусловия, domain, error/source requirements:** полная карточка D-04 в [independent review](HSBI_03D_INDEPENDENT_CONTRACT_REVIEW_RU.md).

OwnerDecision=AWAITING; ApprovedVersion=NONE; ImplementationPermission=NO.

## D-05 — D-05: Current accounting и sticky safety breach

Статус READY_FOR_OWNER_APPROVAL; OwnerDecision=AWAITING.
Варианты: A: current-only; B: current+sticky с явным reset; C: peak вместо current. Рекомендуется B; peak хранится отдельно.
Рекомендация: Current нужен для текущего accounting, sticky сохраняет факт прежнего safety cap breach.

### Полный предлагаемый нормативный текст

> Для OperationID и immutable CapEpoch используется полный упорядоченный actual fill net: S_n=Σnet_i, CurrentLoss_n=max(0,−S_n), Peak_n=max(Peak_(n−1),CurrentLoss_n), Sticky_n=Sticky_(n−1) OR (CurrentLoss_n>H) при фиксированном cap H. Равенство H не breach. Поздний положительный net sticky не очищает. Автоматический reset запрещён. Reset разрешён только authenticated owner principal отдельного administrative control plane после независимой проверки полной history, отсутствия pending/unknown outcomes, CurrentLoss≤H, отдельного safety review и expected revision. Reset receipt содержит principal,reason,OperationID,CapEpoch,history root,старую revision,новый MonitoringEpoch. Без настроенного principal/evidence reset недоступен. Reset очищает только latch в новом MonitoringEpoch; не изменяет fills,net,consumed,replay receipts и архивный peak, не вызывает autoresume. Restart восстанавливает committed sticky/receipts и выполняет independent fill association/reconciliation. Неполная, повреждённая или неоднозначно упорядоченная history → UNAVAILABLE и запрет обычного продолжения. Sticky блокирует NewFar, новые рисковые действия, обычное продолжение transition и routine FinalClose authorization. Safety-reducing exit допускается лишь отдельной SAFE/emergency authority, не считается successful recovery и sticky не снимает.

Текст применяется вместе с G1–G8 и указанными предпосылками; он не заявляет наличие ещё не созданного provider/journal.

**Математика/контрпример:** Fills −15,+100; H12 → net85,current0,peak15,stickytrue. Обратный порядок +100,−15 → net85,current0,peak0,stickyfalse. Final net не определяет ordered breach.
**Обязательные тесты:** T05±: две последовательности выше; −12/H12 → stickyfalse; restart на каждом prefix; corrupt history; unauthorized/stale/duplicate reset; no autoresume. TEST_SPECIFIED_NOT_RUN.
**R1.1 и совместимость:** Новые persisted epoch/sticky/peak/receipt fields и reset authority interface; реализация не ready до owner approval reset policy. S19:8 и S07 cap/transition paths не реализуют этот stateful contract; точная интеграция отдельно.
**Оставшиеся предположения:** Ordered-history provider и durable state ещё не квалифицированы; owner должен явно принять предложенную reset policy.
**Пред-/постусловия, domain, error/source requirements:** полная карточка D-05 в [independent review](HSBI_03D_INDEPENDENT_CONTRACT_REVIEW_RU.md).

OwnerDecision=AWAITING; ApprovedVersion=NONE; ImplementationPermission=NO.

## D-06 — D-06: Расходы, EconomicCyclePnL и RecoveryResult

Статус CONFLICTING; OwnerDecision=AWAITING.
Варианты: A: сохранить Initial exclusion в RecoveryResult, отдельно полный EconomicCyclePnL; B: явно изменить Docs/09:20 и включить Initial; C: один неуточнённый CyclePnL — недопустимо.
Рекомендация: A до отдельного owner policy change; статус CONFLICTING сохраняется до выбора A/B.

### Полный предлагаемый нормативный текст

> Вариант A: EconomicCyclePnL включает все подтверждённые economic facts цикла. NormativeRecoveryResult сохраняет исключения действующей Initial Lock policy. Для каждого показателя фиксируются membership, временная граница и cost basis. Result=RealizedNet+UnrealizedNet−RemainingCosts допустим лишь если RemainingCosts содержит только ещё не включённые расходы. Уже отражённые commission,swap,fee,spread,slippage повторно не вычитаются. Если UnrealizedNet уже close-now net с ожидаемыми расходами закрытия, они не входят повторно в RemainingCosts. Buffers имеют отдельное назначение и не записываются как совершившиеся расходы. Positive BigHarvest, positive EconomicCyclePnL, FinalClose authorization и actual CLOSED — разные предикаты. CLOSED требует actual fills, нулевых остаточных positions, отсутствия unknown outcomes, применённого ledger и persisted результата.

Текст применяется вместе с G1–G8 и указанными предпосылками; он не заявляет наличие ещё не созданного provider/journal.

**Математика/контрпример:** Initial50,otherRealized−10,open−5 → Economic35,Recovery−15 при A. Gross100+commission−2+swap−1+fee−1=96, не92.
**Обязательные тесты:** T06+: net96 из компонентов. T06−: Initial example выше; open-close-now уже включает cost3 — повторное −3 запрещено. TEST_SPECIFIED_NOT_RUN.
**R1.1 и совместимость:** Owner A/B first; D02/D11/D13; отдельные result names и FinalClose gates Docs/12:7–15. S14:11–18, S15:7–19, S19:9 требуют общего basis; одинаковый execution buffer для legs также нуждается в явном scope.
**Оставшиеся предположения:** Broker posting/cost conventions и Initial policy decision отсутствуют; конфликт не разрешён публикацией.
**Пред-/постусловия, domain, error/source requirements:** полная карточка D-06 в [independent review](HSBI_03D_INDEPENDENT_CONTRACT_REVIEW_RU.md).

OwnerDecision=AWAITING; ApprovedVersion=NONE; ImplementationPermission=NO.

## D-07 — D-07: Execution, durable journal, restart

Статус READY_FOR_OWNER_APPROVAL; OwnerDecision=AWAITING.
Варианты: A: durable effect+receipt transaction; B: только in-memory idempotence; C: blind retry. Только A достаточен.
Рекомендация: Exactly-once effect требует durable evidence и reconciliation, а не только matching IDs.

### Полный предлагаемый нормативный текст

> До NOOP валидируются полное body,schema,identity и прежний committed receipt. Новый event применяется лишь при expected revision. Economic effect, balances,receipt,revision фиксируются одной crash-consistent transaction. ActionID,EconomicEventID,ObservationID,JournalCommitSequence имеют разные назначения; возрастающий commit sequence не требует сортировки внешних EventID по величине. UNKNOWN/timeout не разрешает resend/release: сначала independent reconciliation доказывает actual outcome и отсутствие прежнего effect. Restart восстанавливает полный committed state+receipts с broker reconciliation либо blocked. Старый точно совпадающий receipt проверяется как replay до требования новой revision; новый event со старой revision не допускается.

Текст применяется вместе с G1–G8 и указанными предпосылками; он не заявляет наличие ещё не созданного provider/journal.

**Математика/контрпример:** Повтор effect должен иметь Δbalance=0; atomic commit исключает state без receipt и receipt без state.
**Обязательные тесты:** T07+: exact restart replay → NOOP. T07−: changed body/old digest; crash между balance/receipt; UNKNOWN resend; новый ObservationID старого fill. TEST_SPECIFIED_NOT_RUN.
**R1.1 и совместимость:** A/B/E interface; crash matrix; Docs/16 crash-consistency не доказывает более сильные flush/rename обещания Docs/HSB_2E:8–10. S12 full body before duplicate, S10 retry/barrier и S13 backend требуют будущих изменений.
**Оставшиеся предположения:** Durable implementation и platform crash evidence отсутствуют.
**Пред-/постусловия, domain, error/source requirements:** полная карточка D-07 в [independent review](HSBI_03D_INDEPENDENT_CONTRACT_REVIEW_RU.md).

OwnerDecision=AWAITING; ApprovedVersion=NONE; ImplementationPermission=NO.

## D-08 — D-08: Broker/server/account/source identity

Статус READY_FOR_OWNER_APPROVAL; OwnerDecision=AWAITING.
Варианты: A: codec-independent logical key+full attributed body; B: hash wire bytes как source; C: caller EventID как source. Рекомендуется A.
Рекомендация: Одна физическая сделка не становится новыми деньгами при переимпорте/codec change.

### Полный предлагаемый нормативный текст

> Logical SourceKey физического deal=(StableBrokerNamespace,StableServerNamespace,AccountLogin,DealTicket). SchemaVersion,codec,import attempt,ObservationID и DTO format не создают новый source. Namespace подтверждается independent association, не произвольным company string. Два представления одного immutable attributed economic fact эквивалентны iff совпадают authenticated logical key и все обязательные semantic fields полного envelope в утверждённом numeric domain, а association не противоречит source evidence. Неизвестное обязательное поле не доказывает равенства. Same key/changed immutable body → CONFLICT. Correction/reversal — отдельный связанный факт, исходный receipt не переписывается. Разные observations deal не создают grants. Completeness global registry необходима для NEW/spendable классификации; локальное сравнение уже authenticated facts само по себе полноту не доказывает.

Текст применяется вместе с G1–G8 и указанными предпосылками; он не заявляет наличие ещё не созданного provider/journal.

**Математика/контрпример:** Равный net не равен равному body. Тот же ticket при иных account/server — другой source. Новый observation старого K — не новый economic capacity.
**Обязательные тесты:** T08+: тот же K/body новый ObservationID → один source. T08−: equal net/changed components, role/position/price/volume → conflict; ticket разные accounts → distinct sources. TEST_SPECIFIED_NOT_RUN.
**R1.1 и совместимость:** Full schema, source/body validator, actual association, codec/migration interfaces. S01/S06/S07 caller-origin identities не независимая authority.
**Оставшиеся предположения:** Broker history не даёт EA cycle/action/role/plan/policy; нужен независимый association provider.
**Пред-/постусловия, domain, error/source requirements:** полная карточка D-08 в [independent review](HSBI_03D_INDEPENDENT_CONTRACT_REVIEW_RU.md).

OwnerDecision=AWAITING; ApprovedVersion=NONE; ImplementationPermission=NO.

## D-09 — CR-09: All-level NewFar/FutureSmall

Статус READY_FOR_OWNER_APPROVAL; OwnerDecision=AWAITING.
Варианты: A: every required finite level; B: один controlling level; C: global infinite-tail guarantee без отдельной теоремы. Рекомендуется A; C только с дополнительным доказательством.
Рекомендация: Разные экстремумы достигаются на разных уровнях; objective не заменяет feasibility.

### Полный предлагаемый нормативный текст

> Для каждого уровня явного required set нужны согласованные money,cost,risk,margin,identity,freshness proofs. Feasibility требует прохождения каждого; aggregate хранит min CatchUpMargin и max соответствующих рисков независимо. Max TransitionLoss level не заменяет min margin. Проверенный finite prefix гарантирует только этот prefix при его предпосылках; unchecked tail маркируется UNPROVEN. Missing required level, invalid proof или отрицательная margin отвергает candidate. Objective/tiebreak применяется после полного feasibility proof.

Текст применяется вместе с G1–G8 и указанными предпосылками; он не заявляет наличие ещё не созданного provider/journal.

**Математика/контрпример:** Losses(10,5),margins(9,−11) → max loss level1, min margin level2; candidate reject.
**Обязательные тесты:** T09+: losses10,5/margins9,2 → feasible. T09−: margins9,−11 → reject независимо от max-loss level. TEST_SPECIFIED_NOT_RUN.
**R1.1 и совместимость:** D04/D06/D13/D14. Дополнительный нерешённый конфликт: Docs/14:22–23 minimum-safe-first против Docs/29:3 risk-first; S07:149 risk-first. S08:23–58 и S07:114–151 требуют согласованных all-level gates.
**Оставшиеся предположения:** Owner objective decision; tail/market assumptions; ERR038 отдельный proof.
**Пред-/постусловия, domain, error/source requirements:** полная карточка D-09 в [independent review](HSBI_03D_INDEPENDENT_CONTRACT_REVIEW_RU.md).

OwnerDecision=AWAITING; ApprovedVersion=NONE; ImplementationPermission=NO.

## D-10 — NUM-EXACT-1: Точный settled accounting

Статус READY_FOR_OWNER_APPROVAL; OwnerDecision=AWAITING.
Варианты: A: checked signed64 minor units; B: иной полностью qualified exact representation; C: double/epsilon для settled identities. Рекомендуется A при доказанном profile; B отдельная архитектурная альтернатива.
Рекомендация: Точные balances и overflow guards дают проверяемую conservation без скрытой epsilon capacity.

### Полный предлагаемый нормативный текст

> Settled grants,consumption,reservations,balances — exact integer minor units утверждённой currency/profile. Signed64 range −9223372036854775808…9223372036854775807; nonnegative balances≤MAX. Каждое сложение,вычитание,масштабирование и intermediate operation проверяется до исполнения; wraparound,float conversion и допустимость лишь конечного результата запрещены. Projected values до posting не округляются автоматически до settled precision: малый loss не становится доказанным нулём. Conversion требует D11 receipt. Ticket/revision ulong не преобразуется через signed long/double.

Текст применяется вместе с G1–G8 и указанными предпосылками; он не заявляет наличие ещё не созданного provider/journal.

**Математика/контрпример:** MAX+1,abs(MIN),MIN×−1 invalid. MAX+MAX−MAX−MAX mathematically0, но unsafe intermediates. G10000=C3000+R2000+F5000 точно.
**Обязательные тесты:** T10+: exact split10000. T10−: boundaries выше; positive projected0.004 не доказывает zero loss. TEST_SPECIFIED_NOT_RUN.
**R1.1 и совместимость:** D11/D12/D15 numeric bundle; principles можно голосовать, concrete implementation ещё не frozen. Numeric DTO/schema migration required; без автоматической замены старого representation.
**Оставшиеся предположения:** Currency profile/native evidence; другой exact representation требует отдельного доказательства.
**Пред-/постусловия, domain, error/source requirements:** полная карточка D-10 в [independent review](HSBI_03D_INDEPENDENT_CONTRACT_REVIEW_RU.md).

OwnerDecision=AWAITING; ApprovedVersion=NONE; ImplementationPermission=NO.

## D-11 — NUM-DOMAIN-1: Currency, precision, limits

Статус BLOCKED_BY_EVIDENCE; OwnerDecision=AWAITING.
Варианты: A: evidenced currency/posting/grid profile; B: fixture default; C: universal HALF_EVEN. Только A достаточен.
Рекомендация: Rounding определяется фактическим posting stage; универсальное правило создаёт разные деньги.

### Полный предлагаемый нормативный текст

> Money profile содержит currency identifier,minor-unit scale,posting stage,rounding rule,limits,version,provenance. Currency precision не выводится из SYMBOL_DIGITS. Component rounding и aggregate-net rounding — разные profiles и не смешиваются. Settled arithmetic использует только independently confirmed profile и conversion receipt. Unknown currency/scale/posting stage,nonfinite input,decision-changing underflow или range violation → UNAVAILABLE/REJECT. Нельзя создавать balancing adjustment ради искусственного согласования independently posted net с отдельно округлёнными components. Price tick,volume step,money scale — разные domains. Grid origin задаётся явно; zero-origin и Vmin+nstep не предполагаются эквивалентными.

Текст применяется вместе с G1–G8 и указанными предпосылками; он не заявляет наличие ещё не созданного provider/journal.

**Математика/контрпример:** HALF_EVEN cents: отдельно0.005+0.005→0; aggregate→0.01. Для −0.005−0.005:0 против−0.01. Scale100 signedMAX main=92233720368547758.07.
**Обязательные тесты:** T11+: aggregate HALF_EVEN0.005+0.005→1 minor. T11−: component result0 под aggregate receipt→conflict; min0.03/step0.02 distinguishes grid origins. TEST_SPECIFIED_NOT_RUN.
**R1.1 и совместимость:** Joint numeric bundle D10/D12/D15 plus snapshot/provider evidence. S18 and monetary DTOs need explicit profile; no old precision reinterpretation.
**Оставшиеся предположения:** Production currency/posting profiles и grid convention не квалифицированы; BLOCKED_BY_EVIDENCE сохраняется.
**Пред-/постусловия, domain, error/source requirements:** полная карточка D-11 в [independent review](HSBI_03D_INDEPENDENT_CONTRACT_REVIEW_RU.md).

OwnerDecision=AWAITING; ApprovedVersion=NONE; ImplementationPermission=NO.

## D-12 — NUM-CODEC: Canonical wire encoding

Статус BLOCKED_BY_EVIDENCE; OwnerDecision=AWAITING.
Варианты: F64Z; T17Z; иной полностью specified/qualified codec. Голосовать по имени+версии, не букве.
Рекомендация: Logical identity отделить сейчас; final wire codec не freeze до native goldens/hostile decoder.

### Полный предлагаемый нормативный текст

> Logical SourceKey и semantic equality codec-independent. Wire имеет explicit schema/codec version,fixed field order/types,framing,byte order,UTF-8 policy,size limits,absence rules. Decoder отвергает unknown schema,duplicate/reordered mandatory fields,noncanonical numbers,trailing bytes,size excess. Codec change не создаёт income source; cross-version mapping требует semantic migration receipt. Z-profile делает −0/+0 семантически равными и canonical, не обещая raw-bit preservation. NaN/Infinity запрещены. NFC/case-folding identity strings запрещено без отдельной нормы. F64Z/T17Z остаются candidates до native approved golden и hostile decoder evidence; F64Z окончательно не утверждён.

Текст применяется вместе с G1–G8 и указанными предпосылками; он не заявляет наличие ещё не созданного provider/journal.

**Математика/контрпример:** Decode(Encode(x))=x в declared semantic domain, не обязательно raw packet. Crosscodec same fact → один K.
**Обязательные тесты:** T12+: один fact в двух qualified codecs→один source. T12−: truncated/unknown/trailing bytes reject; maxulong/subnormal/negativezero/UTF8 roundtrip. TEST_SPECIFIED_NOT_RUN.
**R1.1 и совместимость:** D08/D10/D11/D15 joint bundle; do not freeze F64Z on reference evidence. S01:11 and S06:23–28 rounded text не canonical economic wire proof.
**Оставшиеся предположения:** Native binary64/UTF-8/decoder evidence отсутствует; candidate caps также требуют hostile qualification.
**Пред-/постусловия, domain, error/source requirements:** полная карточка D-12 в [independent review](HSBI_03D_INDEPENDENT_CONTRACT_REVIEW_RU.md).

OwnerDecision=AWAITING; ApprovedVersion=NONE; ImplementationPermission=NO.

## D-13 — SNAP-FIXTURE-1: Snapshot freshness и content receipt

Статус REQUIRES_CLARIFICATION; OwnerDecision=AWAITING.
Варианты: A: provider clock/receipt profile; B: caller fresh bool; C: digest без source receipt. Рекомендуется A.
Рекомендация: Freshness имеет смысл только в известном clock domain и не доказывает content origin.

### Полный предлагаемый нормативный текст

> Snapshot содержит ProviderID,ClockDomain,TimeUnit,observation time,approved uncertainty/skew,TTL,revision,immutable content identity. Freshness оценивается внутри approved clock profile; fixture ticks не считаются server milliseconds. Exact-clock требует 0≤now−timestamp≤TTL; uncertainty profile использует отдельно утверждённые bounds. Content receipt связывает original provider content,identity,revision. Тот же ID с изменённым content → CONFLICT. Caller flags/self-computed digest не заменяют receipt. Unconfigured provider/clock profile → UNAVAILABLE.

Текст применяется вместе с G1–G8 и указанными предпосылками; он не заявляет наличие ещё не созданного provider/journal.

**Математика/контрпример:** Exact clock now100,ts95,TTL10 fresh; ts101 future invalid; ts89 stale.
**Обязательные тесты:** T13± exact examples; changed price под old receipt conflict; TTL endpoints; cross-clock reject. TEST_SPECIFIED_NOT_RUN.
**R1.1 и совместимость:** Provider profile first; D08/D12/D15 и actual freshness integration. S17:11,16–24; S06/S07 требуют независимого receipt, не только свежих flags.
**Оставшиеся предположения:** Нужно уточнить providers,domains,units,uncertainty. Статус REQUIRES_CLARIFICATION.
**Пред-/постусловия, domain, error/source requirements:** полная карточка D-13 в [independent review](HSBI_03D_INDEPENDENT_CONTRACT_REVIEW_RU.md).

OwnerDecision=AWAITING; ApprovedVersion=NONE; ImplementationPermission=NO.

## D-14 — FUNDING-GLOBAL-ATTRIBUTION: Единый атомарный source registry

Статус READY_FOR_OWNER_APPROVAL; OwnerDecision=AWAITING.
Варианты: A: единый serializable inventory; B: independent local ledgers; C: новый EventID→новые деньги. Только A достаточен.
Рекомендация: Conservation должна сохраняться между consumers, roles, allocation IDs и restarts.

### Полный предлагаемый нормативный текст

> Один logical economic source имеет единый global funding inventory в заданном scope. Allocation,reserve,consume,release,transfer,correction hold,replay receipts сериализуются против него. Expected revision,availability,uniqueness,balance mutation,receipt commit — одна atomic transaction. Registry сохраняет attribution source/manifest/bucket/operation/policy, переживает restart и исключает двойное расходование между roles,allocations,consumers. Multi-source transfer требует atomic debit/credit всех legs либо отдельно доказанного протокола без частично spendable результата. Новый allocation/event/codec key не создаёт source capacity. Registry доступен после доказательства completeness/reconciliation. DTO,bool,local dictionary не являются authority.

Текст применяется вместе с G1–G8 и указанными предпосылками; он не заявляет наличие ещё не созданного provider/journal.

**Математика/контрпример:** Free50; concurrent requests30+30 same revision → at most one commit, затем Free20; второй conflict.
**Обязательные тесты:** T14+: first30 commit→Free20. T14−: second30 same revision rejected; crash/multi-source/restart tests обязательны. TEST_SPECIFIED_NOT_RUN.
**R1.1 и совместимость:** B/D/E plus independent provider; funding registry не заменяет capital/free-margin gate. S04:44–70/S05 validate shapes только; реализация registry НЕ считается существующей.
**Оставшиеся предположения:** Durable provider, real concurrency/crash evidence отсутствуют; это архитектурное требование, не PASS.
**Пред-/постусловия, domain, error/source requirements:** полная карточка D-14 в [independent review](HSBI_03D_INDEPENDENT_CONTRACT_REVIEW_RU.md).

OwnerDecision=AWAITING; ApprovedVersion=NONE; ImplementationPermission=NO.

## D-15 — MQL-DOMAIN: Нативные границы MQL5

Статус READY_FOR_OWNER_APPROVAL; OwnerDecision=AWAITING.
Варианты: A: bounded evidence-qualified native domain; B: перенос reference PASS; C: декларация полного binary64 domain без tests. Рекомендуется A.
Рекомендация: Language/platform conversions и persistence могут отличаться от reference mathematics.

### Полный предлагаемый нормативный текст

> Production domain ограничен values/operations с native evidence соответствующего compiler/terminal build. Qualification включает signed/unsigned boundaries,checked arithmetic,binary64 conversion,subnormal/zero policy,UTF-8 framing,enum membership,price/volume grids,receipt roundtrip. Reference/C++ result не native qualification. Untested subdomain маркируется UNAVAILABLE, не PASS. Compile success или finite roundtrip sample не доказывает full economic correctness/durable funding.

Текст применяется вместе с G1–G8 и указанными предпосылками; он не заявляет наличие ещё не созданного provider/journal.

**Математика/контрпример:** Математическое равенство не доказывает отсутствие overflow/rounding implementation; oracle domain явно отделён.
**Обязательные тесты:** T15+: ulong18446744073709551615 exact roundtrip. T15−: nonfinite money,invalid enum,subminimum volume→reject; полный native matrix отдельно. TEST_SPECIFIED_NOT_RUN.
**R1.1 и совместимость:** D10/D11/D12 bundle; сейчас можно утвердить requirement, не concrete native PASS. S01–S20 остаются неквалифицированными одним reference result; source reading не compile.
**Оставшиеся предположения:** Native MQL5 environment/evidence отсутствуют; NATIVE_NOT_RUN.
**Пред-/постусловия, domain, error/source requirements:** полная карточка D-15 в [independent review](HSBI_03D_INDEPENDENT_CONTRACT_REVIEW_RU.md).

OwnerDecision=AWAITING; ApprovedVersion=NONE; ImplementationPermission=NO.

## D-16 — BALANCE-SCHEMA-MAPPING: Fail-closed legacy migration

Статус READY_FOR_OWNER_APPROVAL; OwnerDecision=AWAITING.
Варианты: A: proven versioned mapping; B: quarantine unknown records; C: fill defaults/current account. A+B совместимы и рекомендуются, C запрещён.
Рекомендация: Неизвестная история не должна превращаться в новые spendable funds.

### Полный предлагаемый нормативный текст

> Legacy record мигрируется только по versioned mapping, доказывающему source identity,money profile,semantic body,grant representation,applied-event set,lifecycle balances. Migration receipt связывает original record/schema,mapping version,source evidence,new record,registry revision. Missing broker/server/account,unknown consumed,ambiguous timestamps,rounding/posting policy или incomplete replay receipts не заполняются предположениями; запись quarantine,spendable0. Seconds не становятся доказанным точным millisecond timestamp. Migration не сбрасывает consumed,sticky,replay history и не импортирует source повторно под новой schema. Registry registration+receipt atomic; exact повтор NOOP,changed mapping/body conflict до отдельного разрешения.

Текст применяется вместе с G1–G8 и указанными предпосылками; он не заявляет наличие ещё не созданного provider/journal.

**Математика/контрпример:** Known G100,C20,R10,F70 сохраняет identity100=20+10+70; available100 без consumed не позволяет вывести исходный grant.
**Обязательные тесты:** T16+: complete known split100/20/10/70 migrated, replay NOOP. T16−: available100 без namespace/consumed→quarantine/spendable0. TEST_SPECIFIED_NOT_RUN.
**R1.1 и совместимость:** D01/D07/D08/D10 interfaces; отдельная квалификация реального legacy corpus. Нельзя автоматически интерпретировать смешанный DTO S02 как original или remaining.
**Оставшиеся предположения:** Фактическая completeness legacy sources и mapping evidence не доказаны.
**Пред-/постусловия, domain, error/source requirements:** полная карточка D-16 в [independent review](HSBI_03D_INDEPENDENT_CONTRACT_REVIEW_RU.md).

OwnerDecision=AWAITING; ApprovedVersion=NONE; ImplementationPermission=NO.

## Envelope D08: обязательные семантические поля

29 fields: SchemaVersion,Broker,Server,AccountLogin,Symbol,Magic,CycleID,DealTicket,OrderTicket,PositionIdentifier,ActionID,EventID,Role,EntryType,DealType,TimestampMsc,Volume,Price,Profit,Swap,Commission,Fee,DealNet,Currency,Precision,SourcePlanApplicable,SourcePlan,SourcePolicyApplicable,SourcePolicyVersion.
Applicability неизвестно не равно false; отсутствующее required поле не0. Immutable EconomicEventID отличается от import ObservationID. Поле schema описывает representation и не делает другой logical source.

## Рекомендация владельцу

Сейчас можно голосовать за 12 предложений как principles/policy: D01–D05,D07,D08,CR09,NUM-EXACT-1,FUNDING-GLOBAL-ATTRIBUTION,MQL-DOMAIN,BALANCE-SCHEMA-MAPPING.
D05 только с полной reset policy; D10/D15 не означают concrete native qualification. D06 сначала выбор Initial policy; D11 реальные currency/posting/grid profiles; D12 native codec evidence; D13 provider/clock/uncertainty clarification.
Даже после нормативного approval остаются независимые architecture/evidence/implementation gates. Approval всех16 автоматически не установлен.
