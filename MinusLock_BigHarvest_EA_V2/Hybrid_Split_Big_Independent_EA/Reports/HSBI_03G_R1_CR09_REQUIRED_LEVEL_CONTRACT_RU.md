# HSBI-03G-R1 — обязательный набор уровней CR-09

DocumentVersion=HSBI-03G-R1-V1
SourceCommitSHA=e68e73e1b252d20e15588645004f9066c6ae88f0
Scope=HSBI_CR09_ALL_REQUIRED_V1 / level scope
EvidenceClass=STATIC_REVIEWED; MATH_DERIVED; TEST_SPECIFIED_NOT_RUN
NormativeStatus=PROPOSED_AWAITING_OWNER_APPROVAL
Dependencies=CR-09; D-02/04/05/06/07/08/10/11/12/13/14/15/16

Репозиторий: `ic8812825-maker/chatgpt.com-codex`, ветка `work`. Все пути ниже находятся внутри `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/`. Новый текст является проектом контракта, а не утверждением реализации. Выбор D-06 A и companion NewFar A сохраняется; полный CR-09 не утверждён. Формальных approval receipts нет.

PRODUCTION_CHANGED=NO; IMPLEMENTATION_ALLOWED=NO; R11_IMPLEMENTATION_ALLOWED=NO; BROKER_DISPATCH_ALLOWED=NO; REAL_TRADING_ALLOWED=NO; NATIVE_MQL5_TESTS=NOT_RUN.

UNAVAILABLE означает отсутствие обязательного доказательства; CONFLICT — противоречие данных; REJECT — доказанное нарушение. Каждый результат запрещает новый финансовый эффект, delta=0. NO_OP допустим только после проверки подлинного полного прежнего event body и receipt. Числа математических примеров не являются брокерскими константами.

## Независимый вывод по source

- [Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:9–25](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md#L9-L25). SourceBlobSHA=`f779a1a87ab2d0163c17d6c855c206047d970cec`; EvidenceClass=STATIC_REVIEWED.
- [Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md:3–7](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md#L3-L7). SourceBlobSHA=`0c4b5f9ea4aab1618a280a5c4510f89b76fb9646`; EvidenceClass=STATIC_REVIEWED.
- [Include/Planning/HSBI_FutureSmallSolver.mqh:113–149](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_FutureSmallSolver.mqh#L113-L149) — HSBI_SolveFutureSmall. SourceBlobSHA=`be55c93f051f57ddffd189b9d2e8eee4c3ddaf9d`; EvidenceClass=STATIC_REVIEWED.
- [Include/Planning/HSBI_FutureSmallTypes.mqh:48–76](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_FutureSmallTypes.mqh#L48-L76) — per-level / result DTO. SourceBlobSHA=`ee962ed40a99b0d0a1fdd22f2ee071cc3fb6cbcc`; EvidenceClass=STATIC_REVIEWED.
- [Include/Planning/HSBI_FutureSmallProofAggregator.mqh:23–58](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_FutureSmallProofAggregator.mqh#L23-L58) — HSBI_AggregateFutureSmallProof. SourceBlobSHA=`4678ae152960e98b9f398b4497786061d7e8a524`; EvidenceClass=STATIC_REVIEWED.

Производитель перебирает k<maximumDepth, прекращает расчёт при invalid level либо terminal Far. ProvenDepth увеличивается после успешного уровня. Result valid требует не менее двух уровней и terminal или conservative bound. Aggregator задаёт levelCount=provenDepth; это количество предъявленных доказательств, а не независимая норма полноты. WORST_CASE выбирает уровень максимального TransitionLoss; FINAL_LEVEL — последний доказанный; EXPLICIT — переданный индекс. Ни одна политика не вычисляет minimum CatchUp по всем required IDs.

## Проект versioned manifest

```text
ContractVersion=HSBI_CR09_ALL_REQUIRED_V1
ManifestVersion=CR09-LEVEL-MANIFEST-1
CanonicalDecisionId=CR-09
OwnerSelection=AWAITING
LevelSemantics=AWAITING_OWNER_SELECTION
RequiredLevelIDs=<frozen unique ordered IDs before evaluation>
ScenarioGraph=<root, nodes, edges, mutually-exclusive branch groups>
RequiredExecutionPrefixIDs=<ordered actions/checkpoints per path>
TerminalPolicyVersion=<owner-selected guard>
TailPolicyVersion=<explicit scope and theorem obligations>
InputReceipt/CostBasisVersion/NumericProfileVersion/ObjectiveVersion=<bound>
OriginalReceiptBinding=<authority, full content, account/symbol/cycle/plan/revision>
```

ID имеет logical scope (PlanVersion, ScenarioPathID, TransitionOrdinal, CheckpointKind); ordinal не является брокерским DealTicket. Конкретный wire encoding зависит от D-12 и не утверждается здесь. Нельзя переименовать уровни после расчёта, отфильтровать неудачные IDs или присвоить RequiredLevelCount=ProvenLevelCount. Required set и порядок фиксируются до candidate evaluation, входят в original receipt и plan binding. Разные candidates могут иметь разные заранее определённые terminal guards; результат guard должен быть доказан, а не угадан по длине массива.

REQUIRED_LEVEL_SET — frozen обязательства. PROVEN_LEVEL_SET — IDs с полным валидным proof соответствующего scope. CONTROL_LEVEL — диагностический/legacy checkpoint, не замена required set. TERMINAL_LEVEL — уровень с доказанным guard завершения. UNPROVEN_TAIL — область, для которой обязательства ещё не доказаны.

Пусть R — required IDs, P — подтверждённые IDs. Требуется R⊆P, совпадение manifest membership, уникальность ID и корректный order/edges. Публикуемый qualified result содержит именно required projection P|R; extras явно маркируются supplemental и не меняют extrema. Duplicate одного ID с разным body — CONFLICT. Один и тот же body с повторным authentic receipt — идемпотентный импорт, не дополнительный уровень.

## Два разных смысла уровней — выбор владельца открыт

| Свойство | ALTERNATIVE_SCENARIOS | SEQUENTIAL_TRANSITIONS |
|---|---|---|
| Экономический смысл | Независимые counterfactual исходы одного начального состояния | Последовательная цепь переходов состояний |
| Snapshot | У каждой ветви свой согласованный conditional market/cost scope | StateAfter(l)=StateBefore(l+1), с доказанной lineage |
| Reserve | Повторная оценка одного inventory допустима без debit | Каждый debit уменьшает доступный остаток следующего prefix |
| Требование денег | Для взаимоисключающих ветвей достаточно покрытия каждой ветви и доказанной эксклюзивности | Для каждого execution prefix нужен cumulative funding proof |
| Recovery monotonicity | Не следует из простого порядка scenarios | Только на утверждённом сопоставимом basis; нельзя смешать realized и open состояния |
| Контрпример | Сумма расходов взаимоисключающих вариантов 9+9 не означает совместный debit18 | Два реальных расхода9 из Free14.5 не допустимы, хотя каждый9<14.5 |
| Tail | Неизученные сценарии остаются вне гарантии | Последующие переходы требуют guard/theorem и funding lineage |

Текущий FutureSmall рекурсивно меняет far/priorBig/priorExposure/recovery, что похоже на последовательный расчёт. Это не доказывает физическую последовательность: farDirection и template open prices переиспользуются на всех уровнях (строки122–123), тогда как Docs13:12 требует promotion другого original BIG_CORE residual. Поэтому нельзя автоматически выбрать SEQUENTIAL_TRANSITIONS или назвать нынешний набор независимыми альтернативами. Владелец выбирает scope, затем архитектура должна предоставить доказательства выбранной модели. Возможен гибридный scenario tree, но только с явными paths/exclusivity и отдельным funding по каждому path.

## Полнота, terminal и tail

| Статус | Точный смысл и действие |
|---|---|
| COMPLETE | Все обязательства frozen manifest доказаны; все required IDs/префиксы проверены; обязательный tail покрыт разрешённым доказательством |
| INCOMPLETE | Известен недостающий required ID/доказательство; candidate не feasible |
| CONFLICT | Один ID/receipt/revision противоречит другому; новый эффект запрещён |
| UNSUPPORTED | Неизвестная schema/model/profile/теорема; не интерпретировать legacy молча |
| UNAVAILABLE | Нельзя определить полноту из-за отсутствующей authority/history; блокировать |

Invalid level — отказ по обязательному узлу, а не terminal. Terminal допускает остановку только по заранее утверждённому guard и доказанному состоянию; пропуск условно последующих узлов разрешает сам frozen graph, не producer задним числом. Минимальный брокерский лот не означает экономически завершённый цикл или profit.

Геометрическое F_after≤qF_before, 0<q<1 даёт bound объёма. Оно не даёт автоматически нижнюю границу CatchUpMargin, cost, liquidity или доступность reserve. Conservative bound может покрывать обязательный tail только при отдельной теореме, которая доказывает ВСЕ required safety predicates, в том числе cost/error/source/funding assumptions. Иначе prefix отмечается доказанным, tail — UNPROVEN; глобальная feasible гарантия отсутствует.

## Приёмка

Позитивный пример: R={L1,L2,L3}, P={L1,L2,L3}, все scopes и receipts согласованы, terminal guard подтверждён → completeness COMPLETE; feasibility ещё зависит от денег и других gates. Отрицательный: R={L1,L2,L3,L4}, P={L1,L2,L3}, volume bound известен, money L4 неизвестны → INCOMPLETE/UNAVAILABLE, не COMPLETE.

OpenQuestions: CR09-SUB-02/03 и связанный far lineage; какая область tail обязательна; кто подтверждает manifest и terminal evidence.
AcceptanceCriteria: frozen IDs/order/guards; точное set coverage; негативные cases LEVEL-01…06 из [qualification](HSBI_03G_R1_QUALIFICATION_TEST_SPEC_RU.md); ни один omitted ID не превращается в ноль.

Связи: [quantity](HSBI_03G_R1_PER_LEVEL_FAR_VOLUME_BINDING_RU.md), [feasibility](HSBI_03G_R1_ALL_LEVEL_FEASIBILITY_PROOF_RU.md), [ballot](HSBI_03G_R1_OWNER_CR09_DECISION_BALLOT_RU.md).
