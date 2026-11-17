# HSBI-03H-R1 — Вердикт о семантике уровней FutureSmall

DocumentVersion=HSBI-03H-R1-V1
SourceCommitSHA=70cc4c861b391a7916403106ff07f25729e602da
EvidenceClass=STATIC_REVIEWED; MATH_DERIVED; TEST_SPECIFIED_NOT_RUN
NormativeStatus=AUDIT_SPEC_ONLY_PROPOSED_AWAITING_OWNER_APPROVAL

Репозиторий: ic8812825-maker/chatgpt.com-codex; ветка work. Все пути относительно MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/. Режим GITHUB_MCP_REMOTE_ONLY, локальных файловых операций нет. SourceCommitSHA — исследованная база, не будущий commit отчётов.
D-06=A и NewFar=A/MINIMUM_SAFE_V1 сохраняются. Новых owner selections и approval receipts этот документ не создаёт. Все числовые торговые примеры синтетические; подтверждённых брокерских сделок в них нет.
PRODUCTION_CHANGED=NO; R11_IMPLEMENTATION_ALLOWED=NO; BROKER_DISPATCH_ALLOWED=NO; REAL_TRADING_ALLOWED=NO; NATIVE_MQL5_TESTS=NOT_RUN.
UNAVAILABLE — отсутствует доказательство, CONFLICT — противоречие, REJECT — доказанное нарушение. Ни один из этих результатов не разрешает новый финансовый эффект. Математическое ожидание не является фактическим PASS.

Scope=проверка A ALTERNATIVE_SCENARIOS, B SEQUENTIAL_TRANSITIONS, C BRANCHING_SCENARIO_TREE
Dependencies=physical ledger этого пакета; Docs04/13/14/30; FutureSmallSolver/Types/Aggregator; NewFarSolver; CR09-SUB-02/03/04/07
OpenQuestions=owner scope уровней и tail; action membership; provider receipts; физический state propagation
AcceptanceCriteria=вывод отдельно по Docs/source/lineage/money/funding; ни одна модель не признана реализованной без своих доказательств

## Вердикт

DOCS_INTENT=SEQUENTIAL_TRANSITIONS: сильнейшее прямое основание — [Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md:11](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/70cc4c861b391a7916403106ff07f25729e602da/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md#L11) (единственный порядок и original Core residual) вместе с [Docs/04_MATHEMATICAL_MODEL_RU.md:32](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/70cc4c861b391a7916403106ff07f25729e602da/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Docs/04_MATHEMATICAL_MODEL_RU.md#L32) (следующий cycle рекурсии). Это основание рекомендовать владельцу B для одной физической траектории. OWNER_SELECTION=AWAITING: рекомендация не записывает выбор.

SOURCE_BEHAVIOR=RECURSIVE_SCALAR_TEMPLATE, PHYSICAL_SEQUENTIAL_CHAIN=NOT_PROVEN. Это описательный термин аудита, не новая canonical policy. Source переносит некоторые scalars предыдущего уровня, поэтому назвать существующий массив независимыми оценками одного исходного inventory нельзя. Одновременно он не переносит необходимые direction/open/identity/realized/funding state для цепи Docs13. Ни A, ни B, ни C полностью не подтверждены текущим production.

C может быть разумной будущей оболочкой для нескольких ценовых путей B. Нормативного перечня ветвей/вероятностей/exclusivity и graph provider нет; выбирать C как уже существующую стратегию оснований недостаточно. Вероятностное усреднение safety обязательств не разрешено.

## Проверенная матрица

| Модель | DOCS_SUPPORT | SOURCE_SUPPORT | PHYSICAL_LINEAGE_SUPPORT | MONEY_SUPPORT | FUNDING_SUPPORT | CONTRADICTIONS | RECOMMENDATION |
|---|---|---|---|---|---|---|---|
| A ALTERNATIVE_SCENARIOS | Docs30 разрешает выбор control, но не определяет уровни как independent alternatives; слабое/непрямое | Нет: far/priorBig/priorExposure/recovery/risk обновляются | Для отдельных counterfactual snapshots возможна, если они имеют один root и отдельные state copies; current root equality не доказана | Каждый сценарий оценивается отдельно; нельзя считать current recurrence независимым reset | Один root Free можно проверить на каждом взаимоисключающем пути без debit; exclusivity обязательна | Разные F и strict recurrence не один неизменный starting inventory | Только отдельный явно ограниченный preview scope после owner выбора; не переименовывать текущие levels |
| B SEQUENTIAL_TRANSITIONS | Прямое: Docs13 original Core→Far; Docs04 next cycle; Docs14 actual residual revalidation | Частично: передаются F_after и числовые gates; нет полной physical state chain | НЕ доказана: направление не меняется, Core open не становится Far open, original per-level IDs/actions не связаны | Basket full Core, нет closing membership и accumulated realized; recovery сравнивает template basket scalars | expectedReserve копируется, нет prefix debit/free/grant chain | Scalar recursion не выполняет переход Docs13 | Рекомендовать как целевой принцип одной траектории, реализация/authority blocked |
| C BRANCHING_SCENARIO_TREE | Совместима как расширение B, но явного graph в исследованных Docs нет | Нет Node/Parent/PathID/exclusivity graph в DTO/loop | Потребуются root и полный StateAfter→StateBefore по каждой edge | Отдельные accumulated realized/costs/позиции на каждой ветви | Общие prefixes учитываются один раз на path, sibling outcomes взаимоисключающи; общий source registry нельзя клонировать как новые деньги | Массив уровней не дерево; index не path | До graph specification/evidence выбор конкретного дерева преждевременен |

## Что передаётся между уровнями

[Include/Planning/HSBI_FutureSmallSolver.mqh:119](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/70cc4c861b391a7916403106ff07f25729e602da/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_FutureSmallSolver.mqh#L119):
far=x.currentFar; priorBig=x.currentBigGross; priorExposure=x.currentGrossExposure; money/risk/margin копируются.
В loop120–144 nextFar=level.farAfter, priorBig=level.netBigVolume, exposure=level.grossExposure, money.recoveryMoney=level.recoveryMoney, risk=level.riskValue, margin=level.totalMargin.

Но строки122–123 каждый раз задают:
farDirection=x.farDirection;
farOpenPrice=x.farOpenPrice;
coreOpenPrice=x.coreOpenPrice;
trendOpenPrice=x.trendOpenPrice;
smallOpenPrice=x.smallOpenPrice.

Синтетический witness: old Far SELL1@100, C BUY3@120; после закрытия C2.6 остаток C BUY0.4@120 становится Far BUY0.4@120. Следующая Far SELL0.4@100 из неизменного template описывала бы другую позицию. Смена только объёма не сохраняет ни direction, ни money basis.

[Include/Planning/HSBI_FutureSmallTypes.mqh:32](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/70cc4c861b391a7916403106ff07f25729e602da/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_FutureSmallTypes.mqh#L32) хранит один общий farDirection и набор open prices. [Include/Planning/HSBI_FutureSmallSolver.mqh:32](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/70cc4c861b391a7916403106ff07f25729e602da/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_FutureSmallSolver.mqh#L32) валидирует projection flags/volume и ненулевые identifiers, но не доказывает полную old/core/action state relation каждого уровня. [Include/Planning/HSBI_NewFarSolver.mqh:79](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/70cc4c861b391a7916403106ff07f25729e602da/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_NewFarSolver.mqh#L79) меняет currentFar=candidate, plan/revision/policy; это также не доказательство направления/цен actual promoted residual.

## Денежные величины, которые нельзя смешивать

1. Full-basket close-now: оценить F,C,T,S как если ликвидированы все четыре legs.
2. SmallTransition closing group: оценить F,T,S и C−N. N остаётся open.
3. Cycle economic: предыдущие realized + current open net − только ещё не включённые costs.
4. D06 A recovery: economic минус excluded Initial и объявленный H_in.
5. Projected CatchUp: утверждённый eligible preview G минус loss конкретной Far obligation A и disjoint B.
6. Funding inventory: уже подтверждённый допустимый Free конкретного source/bucket на execution prefix.

Full-basket loss не обязан равняться loss actual закрываемой группы. Рост template recovery не доказывает рост economic/recovery результата физической цепи. На неизменной цене без новых fees только перевод части U в R не создаёт прибыль; документы сценариев демонстрируют точную conservation.

## Полное закрытие old Far и новая Far

A допустима для каждого отдельного counterfactual полного перехода, если старую Far в каждой независимой ветви закрывают полностью, а N задают как residual другого Core. Нельзя назвать A «повторными partial closes той же Far».

B требует на edge: OldFarID исчезает из open set, CoreID сохраняется, Role Core→Far, DirectionAfter=CoreDirectionBefore, OpenBasisAfter=CoreOpenBasisBefore, VolumeAfter=actual residual. На следующем устойчивом состоянии C/T создаются opposite NEW Far. Поэтому направления последовательных promoted Far чередуются. Ценовой путь при этом может включать развороты; односторонняя линейная таблица с фиксированными opens это не доказывает.

C требует те же свойства для каждой edge и явное разветвление. Состояние общего prefix нельзя получить суммированием несовместимых sibling outcomes. Общее фактическое source имущество одно; projection branch inventory — условная копия, не новый grant.

## Funding: prefix сильнее конечной суммы

Пусть общий grant14.5, два debit9. При B после первого Free5.5; второй недостаточен. При A две взаимоисключающие потребности9 каждая могут быть покрыты тем же root14.5 без физического двойного debit. При C этот вывод действует только на siblings; два последовательных debit вдоль одного path всё равно требуют18.

Другой физический пример из сценария S3: Small−1000, OldFar−3000, Trend+1000, закрытая Core+2600. Итог closing net−400. Но до будущих прибылей prefix уже требует4000. Из Free500 такой план не финансируется; обещанные будущие proceeds и full Core profit не settled cash. Это справедливо даже когда cap400 формально не превышен. Конкретный loss-consumption/offset contract не утверждён; здесь показана нижняя временная потребность при отсутствии новых confirmed credits и консервативная потребность без offset.

## All-level и terminal

[Include/Planning/HSBI_FutureSmallProofAggregator.mqh:28](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/70cc4c861b391a7916403106ff07f25729e602da/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_FutureSmallProofAggregator.mqh#L28) проверяет предъявленный proven prefix. WORST_CASE берёт argmax TransitionLoss, FINAL_LEVEL — provenDepth, EXPLICIT — переданный index. Producer/aggregator не вычисляют минимум CatchUp; [Include/Planning/HSBI_NewFarSolver.mqh:118](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/70cc4c861b391a7916403106ff07f25729e602da/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_NewFarSolver.mqh#L118) вызывает CatchUp максимум один раз на candidate.

Для выбранной NewFar A нужен min всех REQUIRED margins. Required set нельзя задать provenDepth постфактум. До расчёта нужны semantic scope, frozen node/action IDs, terminal guards, required paths/prefixes, costs/numeric/provider версии. q-bound на объём не доказывает money/funding tail. Если exact tail обязателен и отсутствует, статус UNAVAILABLE/INCOMPLETE, не PASS.

Docs30 selective controls и selected objective minAll требуют versioned согласования; не переписываем Docs в этом audit. Вопросы о concrete tree, eligible source и native runtime остаются открытыми.

## Проверяемая будущая state relation

Для edge e: StateBefore содержит account/server/symbol/cycle/plan/revision, открытые IDs/roles/directions/volumes/open bases/cost components, полный unique actual realized set, grants/reserved/free и pending action state.
Apply(action, confirmed facts) проверяет volume conservation, source membership и новые расходы один раз.
StateAfter(e)=StateBefore(next(e)) на ВСЕХ этих полях, не только F_after.
Projected relation отдельно помечена PROJECTED; actual relation требует независимых fills/history. Присвоить projected.confirmed=true недостаточно.

Принять модель можно лишь после проверки обоих направлений, двух successive promotions, nonzero-cost partial closes, actual≠requested residual, отказа по unknown fill и prefix funding. Arithmetic illustrations ниже не являются доказательством native successful route.
