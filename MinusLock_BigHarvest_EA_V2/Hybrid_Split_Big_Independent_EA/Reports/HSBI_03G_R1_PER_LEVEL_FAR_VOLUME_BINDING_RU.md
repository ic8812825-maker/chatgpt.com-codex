# HSBI-03G-R1 — привязка Far volume к каждому уровню

DocumentVersion=HSBI-03G-R1-V1
SourceCommitSHA=e68e73e1b252d20e15588645004f9066c6ae88f0
Scope=QuantityBindingManifest / CR09-SUB-04
EvidenceClass=STATIC_REVIEWED; MATH_DERIVED; TEST_SPECIFIED_NOT_RUN
NormativeStatus=PROPOSED_AWAITING_OWNER_APPROVAL
Dependencies=CR-09; D-04/08/11/13; Docs13 promotion semantics

Репозиторий: `ic8812825-maker/chatgpt.com-codex`, ветка `work`. Все пути ниже находятся внутри `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/`. Новый текст является проектом контракта, а не утверждением реализации. Выбор D-06 A и companion NewFar A сохраняется; полный CR-09 не утверждён. Формальных approval receipts нет.

PRODUCTION_CHANGED=NO; IMPLEMENTATION_ALLOWED=NO; R11_IMPLEMENTATION_ALLOWED=NO; BROKER_DISPATCH_ALLOWED=NO; REAL_TRADING_ALLOWED=NO; NATIVE_MQL5_TESTS=NOT_RUN.

UNAVAILABLE означает отсутствие обязательного доказательства; CONFLICT — противоречие данных; REJECT — доказанное нарушение. Каждый результат запрещает новый финансовый эффект, delta=0. NO_OP допустим только после проверки подлинного полного прежнего event body и receipt. Числа математических примеров не являются брокерскими константами.

## Фактический data flow

- [Include/Planning/HSBI_NewFarSolver.mqh:118–127](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_NewFarSolver.mqh#L118-L127) — HSBI_SolveNewFar: ci.netBigVolume / ci.farVolume. SourceBlobSHA=`3d19eccd6cd318b9b4591e2bc0ccaa95f661930d`; EvidenceClass=STATIC_REVIEWED.
- [Include/Planning/HSBI_FutureSmallSolver.mqh:63–90](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_FutureSmallSolver.mqh#L63-L90) — HSBI_EvaluateFutureSmallLevel. SourceBlobSHA=`be55c93f051f57ddffd189b9d2e8eee4c3ddaf9d`; EvidenceClass=STATIC_REVIEWED.
- [Include/Planning/HSBI_FutureSmallSolver.mqh:120–144](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_FutureSmallSolver.mqh#L120-L144) — HSBI_SolveFutureSmall. SourceBlobSHA=`be55c93f051f57ddffd189b9d2e8eee4c3ddaf9d`; EvidenceClass=STATIC_REVIEWED.
- [Include/Planning/HSBI_GeometrySolver.mqh:21–35](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Planning/HSBI_GeometrySolver.mqh#L21-L35) — HSBI_SolveBigGeometry. SourceBlobSHA=`707cc1678ca4d98888b3acc2599838094fe13a78`; EvidenceClass=STATIC_REVIEWED.
- [Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:63–75](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Include/Money/HSBI_ReserveCatchUpEvaluator.mqh#L63-L75) — HSBI_EvaluateReserveCatchUp. SourceBlobSHA=`87a8b7e97727ce6e47c2a2f0abc3e237f6203204`; EvidenceClass=STATIC_REVIEWED.
- [Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md:9–20](https://github.com/ic8812825-maker/chatgpt.com-codex/blob/e68e73e1b252d20e15588645004f9066c6ae88f0/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md#L9-L20). SourceBlobSHA=`4ecebeb09c9dcfbbf9d3927b980e44fd81289cf6`; EvidenceClass=STATIC_REVIEWED.

ci.netBigVolume берётся из выбранного control level; ci.farVolume всегда равен исходному candidate N. На будущих уровнях FarBefore уже меняется. Evaluator проверяет share×NetBig>farVolume. Поэтому текущая проверка смешивает quantity scope. Это не доказывает, что замена на FarBefore является единственно правильной policy.

## Раздельные величины и обязательный binding

| Поле | Определение | Единицы/диапазон |
|---|---|---|
| FarBefore_l | Объём конкретной Far position непосредственно перед действием/оценкой l | lots, >0, на approved grid |
| FarAfter_l | Объём Far в результирующем состоянии, с собственной position lineage | lots, ≥0; zero только при разрешённом terminal |
| FarClosedVolume_l | Сумма фактически/планово закрываемых долей конкретной старой Far по Action membership | lots, 0…FarBefore при отсутствии новых opens/corrections |
| CompressionLots_l | FarBefore_l−FarAfter_l на сопоставимом strategy scope | lots; не автоматически closed volume |
| NetBigVolume_l | Core_l+Trend_l−Small_l после broker normalization | lots, >0 по этой geometry |
| ReserveShare_l | Доля eligibility policy для l, а не перевод money→lots | безразмерная, 0…1 |
| FarObligationVolume_l | Выбранная владельцем обязанность покрытия; kind обязателен | lots, на том же economic/position scope |

QuantityBinding включает LevelID, CandidateID, RoleBefore/After, PositionIdentifier/Ticket references, DirectionBefore/After, ActionIDs, PlanID, StateRevision, SnapshotReceipt, BrokerGridVersion, NumericProfileVersion и purpose. Projected position references не выдаются за actual DealTicket. Actual закрытие требует independently associated fills, не template flag.

### Почему closed volume не равно compression в общем случае

Docs13:12 закрывает OldFar полностью, затем делает NewFar из остатка другого original BIG_CORE. Если FarBefore=1.00 SELL, новый FarAfter=0.40 BUY от другого identifier, то CompressionLots=0.60, а закрытый OldFar=1.00. Равенство FarClosed=Before−After допустимо лишь в другом контракте: same position identifier/direction, partial reduction, отсутствие opens/corrections, подтверждённые fills и сохраняющийся residual. Нельзя использовать 0.60 для цены закрытия полного OldFar1.00.

При последовательной интерпретации новый Far после promotion должен наследовать direction/open basis original Core. Basket evaluator ставит Core opposite Far; FutureSmall loop повторяет исходный farDirection/open prices. Это дополнительное требование к lineage evidence, а не доказательство текущего physically executable chain. Синтетические таблицы денег ниже подтверждают расчётные равенства, но не исполненную последовательность promotion.

## Четыре допустимых проекта quantity policy

Общая форма предлагаемого предиката: share_l×NetBigVolume_l > FarObligationVolume_l. Он не заменяет денежный CatchUpMargin и не доказывает profit. Выбор правой части зависит от purpose:

| Вариант | Обязанность | Когда применим | Чего не доказывает |
|---|---|---|---|
| A | FarBefore_l | Полное закрытие old Far, loss proof оценён на том же объёме | Safety будущего нового Far |
| B | FarAfter_l | Покрытие остающейся/следующей экспозиции | Способность оплатить закрытие old Far |
| C | FarClosedVolume_l | Доказанный partial/full close конкретного Action | Право подменить physical closed объёмом compression |
| D | OriginalCandidateN | Сохраняющаяся обязанность initial candidate с явной lineage | Универсальную применимость на всех будущих уровнях |

Рекомендация условная: для full-close обязанности Docs13 использовать A, либо C с доказанным FarClosed=FarBefore. Для иной обязанности нужен её собственный money proof. B/D нельзя объявлять неверными независимо от смысла, но нельзя ими без доказательств покрывать A. OwnerSelection=AWAITING; EVIDENCE_REQUIRED_BEFORE_SELECTION для конкретного position/action binding.

## Численные контрпримеры

Fixture V1: share0.5, NetBig1.2 → lhs0.6; FarBefore1.0, FarAfter0.4, OriginalN0.8. В same-position partial model FarClosed0.6: A reject, B passes quantity only, C reject по строгому равенству, D reject. В promotion model FarClosed1.0: C reject уже по1.0, а не0.6. При lhs1.0 A и promotion-C отвергают equality, B/D проходят quantity; выводы money остаются отдельными.

Fixture V2: Fbefore=(0.4,0.2,0.1), NetBig=(1.2,0.6,0.3), share0.8 → lhs=(0.96,0.48,0.24). ConstantN0.4 отвергает L3; per-level FarBefore проходит все три. Это показывает несогласованность scopes, но само по себе не выбирает A и не доказывает физический сценарий. FutureSmall projections Fafter=(0.2,0.1,0.05) задают compression=(0.2,0.1,0.05); это не доказательство closed fills.

Для любой выбранной обязанности Far loss рассчитывается заново по её direction, volume, close side и cost membership. Нельзя взять A_l от full old Far, заменить lot denominator на маленький FarAfter и объявить полное coverage. Share×lots — лишь стратегия geometry; currency money остаётся G−A−B.

## Ошибки, миграция и проверка

Off-grid, nonfinite, отрицательные volumes, role/identifier mismatch → REJECT/CONFLICT. Неизвестные physical ownership/action membership/snapshot → UNAVAILABLE. Без утверждённого rounding/error profile нельзя допускать equality через произвольный epsilon. После actual fills повторно читается original Core residual; planned N не разрешает promotion.

Legacy FarVolume без ObligationKind/LevelID не переименовывается молча. Старый persisted plan сохраняется; требуется revalidation и новая schema/version/receipt, либо quarantine.

OpenQuestions: CR09-SUB-04; fixed template directions/open prices; actual close quantities; grid/profile authority.
AcceptanceCriteria: VOLUME-01…05, оба направления и promotion/partial distinctions; деньги и lots связаны одним LevelID/receipt; неизвестная lineage блокирует кандидата.

Связи: [metric schema](HSBI_03G_R1_TRANSITION_CATCHUP_METRIC_SCHEMA_RU.md), [owner ballot](HSBI_03G_R1_OWNER_CR09_DECISION_BALLOT_RU.md).
