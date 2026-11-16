# HSBI-03F-R2 — Независимый source-level аудит ERR-018

Version=**HSBI-03F-R2-V1**. SourceCommitSHA=`ae367ff2925da4d845a413326c840fe468ff451b`.
Repository=`ic8812825-maker/chatgpt.com-codex`; Branch=`work`.
Все относительные пути относятся к `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/`.

D-06 A и companion NewFar A выбраны владельцем в беседе. FormalApprovalReceipt=NOT_REGISTERED. Остальные 15 денежных решений остаются AWAITING/BLOCKED; CR09_FULL_APPROVAL=AWAITING.
EvidenceClass: CONFIRMED_STATIC/STATIC_CONFIRMED — чтение исходного кода; MATH_DERIVED — математический вывод при указанных предпосылках; TEST_SPECIFIED_NOT_RUN — заданный, но не выполненный тест; HISTORICAL_TEST_RESULT — прежний artifact.
Native, compile, runtime, mutation, crash и concurrency испытания на этом этапе не запускались.

EXECUTION_MODE=GITHUB_MCP_REMOTE_ONLY; LOCAL_FILE_OPERATIONS=0; NATIVE_MQL5_TESTS=NOT_RUN.
PRODUCTION_CHANGED=NO; IMPLEMENTATION_ALLOWED=NO; R11_IMPLEMENTATION_ALLOWED=NO; BROKER_DISPATCH_ALLOWED=NO; REAL_TRADING_ALLOWED=NO.
Новый contract с пометкой PROPOSED не считается утверждённым или реализованным. UNAVAILABLE означает отсутствие обязательного evidence, CONFLICT — противоречие, REJECT — известное нарушение. Все три результата запрещают новый финансовый эффект. NO_OP требует проверки полного прежнего body/receipt.

Критические SourceBlobSHA:
- `Include/Planning/HSBI_NewFarSolver.mqh`: `3d19eccd6cd318b9b4591e2bc0ccaa95f661930d`.
- `Include/Planning/HSBI_FutureSmallProofAggregator.mqh`: `4678ae152960e98b9f398b4497786061d7e8a524`.
- `Include/Money/HSBI_ReserveCatchUpEvaluator.mqh`: `87a8b7e97727ce6e47c2a2f0abc3e237f6203204`.


Status=CONFIRMED_CONTRACT_GAP.
ERR018_SOURCE_AUDIT=CONFIRMED_CONTRACT_GAP.
ImplementationAspect=CONFIRMED_IMPLEMENTATION_GAP относительно all-required target.
RuntimeReachabilityAspect=BLOCKED_BY_MISSING_EVIDENCE.

## 1. Нормативная граница

Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md:3–7 требует полные level proofs, но допускает WORST_CASE/FINAL_LEVEL/explicit control. Он не устанавливает теорему «argmax TransitionLoss = argmin CatchUpMargin».
Reports/HSBI_AUDIT03_ALL_ERRORS_RU.md:265–276, SourceBlobSHA=a36d0fb1c37da7dcab02e54e9738e01befc16084, прямо сохраняет all-level minimum как предложенный CR-09.
Reports/HSBI_03E_NEWFAR_OBJECTIVE_RESOLUTION_RU.md:24–42 задаёт all-required feasibility и minimum для objective A. Этот objective выбран владельцем, но полный CR-09 и его required-set/funding/provider параметры остаются AWAITING.

Вывод разделяется на два аспекта: текущий контракт не завершает однозначное согласование selective/all-required scope; текущий код фактически выполняет single-control проверку. Это несовместимо с требованием передать в выбранный objective настоящий m(c), но не позволяет объявлять весь CR-09 уже утверждённым.

Рабочая формула:
Margin_l=G_l−A_l−B_l.
G_l — eligible projected allocation для preview либо independently confirmed allocated Free для funding; A_l — absolute Far close-net loss этого уровня; B_l — подтверждённый disjoint buffer.
Уже allocated amount не умножается на share повторно. Basket net, Initial result и TransitionLoss не заменяют eligible reserve. Неизвестный source/cost overlap означает UNAVAILABLE.

## 2. Сколько уровней проверяет producer

Include/Planning/HSBI_FutureSmallSolver.mqh, SourceBlobSHA=be55c93f051f57ddffd189b9d2e8eee4c3ddaf9d:
- HSBI_ValidateFutureSmallInput:45–55 принимает maximumDepth2…128 и требует достаточные counts market/cost/projection snapshots.
- HSBI_SolveFutureSmall:120–144 последовательно оценивает уровни; останавливается при первом invalid level либо terminal Far≤volumeMin+tolerance.
- Строка147 требует provenDepth≥2 и terminal либо conservative bound. ProvenDepth не обязан равняться configuredDepth.
- HSBI_EvaluateFutureSmallLevel:87–91 проверяет рост basket recovery, margin, exposure, уменьшение netBig и TransitionLoss cap. ReserveCatchUpEvaluator здесь не вызывается.
- Строки131–140 сохраняют volumes, recovery, money/margin/risk/transition statuses, market/cost IDs, Core reserveSourceProof и Far loss proof.
- projectedReserve:134 — копия x.expectedReserve. Это не независимый allocation receipt; NewFar:121 использует вместо него Core proof net.

DTO: Include/Planning/HSBI_FutureSmallTypes.mqh:48–62, SourceBlobSHA=ee962ed40a99b0d0a1fdd22f2ee071cc3fb6cbcc.
Per-level CatchUpMargin и его отдельного proof здесь нет. Внешний RequiredLevelCount/ID manifest отсутствует: aggregate.levelCount=p.provenDepth на строке25. Полнота предъявленного prefix не доказывает полноту внешнего required set или tail.

## 3. Что проверяет aggregator

HSBI_AggregateFutureSmallProof:28–39 проверяет каждый proven level: индекс, valid/status, money/margin/risk/transition flags, snapshots, projection и runtime flags.
Строки40–46 собирают max margin/risk/exposure/TransitionLoss и min recovery/compression.

| Policy | Фактический control |
|---|---|
| WORST_CASE | worstTransitionLossLevel, строка50; earliest maximum при tie из strict comparison44 |
| FINAL_LEVEL | provenDepth, строка51 |
| EXPLICIT_CONTROL_LEVEL | explicitControlLevel, строка52; range check53 |

aggregate.valid:55–56 не содержит per-level CatchUp predicate. Нет поля MinimumCatchUpMargin, нет цикла его вычисления и нет вызова ReserveCatchUp.
allMoneyProofsValid означает money calculation PASS, а не положительную CatchUpMargin каждого уровня.

## 4. Один CatchUp call на candidate

Include/Planning/HSBI_NewFarSolver.mqh:
1. 114–117 — получает FutureSmall proof и aggregate.
2. 118 — выбирает один control level.
3. 119–124 — создаёт identity/expected из caller context.
4. 121 — eligible=max(0,control Core net).
5. 122 — Far loss=max(0,−control Far net), buffer берётся из template.
6. 123 — NetBigVolume берётся из control, но FarVolume остаётся исходным candidate.
7. 125–126 — один outer consumption/prior pair, source/event/plan/revision; snapshot от control.
8. 127 — один HSBI_EvaluateReserveCatchUp(ci); 128 исключает кандидата при отказе.
9. 131–134 — проверяет aggregate TransitionLoss cap.
10. 138 — catchUpProofValid=catchResult.valid.
11. 140 — safetyBuffer=catchResult.catchUpMargin одного control level.
12. 146 — complete-candidate flags;149 — selection.

Итого: 0 или 1 CatchUp вызов на каждый рассматриваемый candidate, а не один на весь поиск и не один на каждый required level. Ни producer, ни aggregator дополнительных CatchUp calls не выполняют.
HSBI_IsCompleteCandidateProof, Include/Planning/HSBI_NewFarCandidate.mqh:26–31, проверяет flags/digests, но не пересчитывает all-level minimum.
Поэтому catchUpProofValid=true на этом маршруте подтверждает только control check. Это STATIC_CONFIRMED.

## 5. Согласованный контрпример

[Математический отчёт](HSBI_03F_R2_TRANSITION_CATCHUP_MATH_PROOFS_RU.md) задаёт четыре legs, единые open prices, broker grid, signed costs, уменьшающиеся Far volumes и strict recovery growth:

| L | BasketNet | TransitionLoss | CatchUpMargin |
|---|---:|---:|---:|
| L1 |−12|12|9|
| L2 |−7|7|−4|
| L3 |−3|3|2|

Worst Transition находится наL1, minimum CatchUp наL2. WORST_CASE выбираетL1 и не проверяет отрицательный marginL2. Числа согласованы с текущими денежными формулами, а не назначены произвольной таблицей.
Модель использует синтетический инструмент и не выдаёт его за реально доступный OrderCalcProfit/provider. Полный успешный native solver call не продемонстрирован.

Даже при constant confirmed reserve14.5 альтернативные checkpoint margins составляют0.3/−0.7/5.3. Это отдельно опровергает зависимость extrema, но не даёт право последовательно потратить один reserve несколько раз.

## 6. Ограничения достижимости, обнаруженные заново

### Recovery monotonicity

FutureSmallSolver:89,143 требует B_(l+1)>B_l для конечных корректных producer values.
Отсюда T_(l+1)=max(0,−B_(l+1))≤T_l. В такой genuine chain worst Transition находится наL1 либо первом уровне tie.
Поэтому вариант T=(3,7,12),worstL3 не является допустимым producer witness. Public aggregator может получить такой caller DTO сvalid flags, поскольку не повторяет этот invariant; NewFar же генерирует proof внутри и отвергает injected proofs.
Основной TL03 использует T=(12,7,3) и explicit controlL2 вместо неподтверждённого worstL3.

### Far volume на будущем уровне

В модели share×NetBig=(0.96,0.48,0.24).
Сравнение с собственными FarBefore=(0.4,0.2,0.1) проходит на всех уровнях.
Текущий ci.FarVolume=candidate0.4 приводит к отказу L3 по0.24≤0.4, даже при положительной margin2. Следовательно FINAL_LEVEL нельзя объявить принимающим этот пример; explicitL2 отвергает margin−4, а WORST_CASEL1 условно проходит локальные numeric checks.
Простой цикл, копирующий прежний ci, не полный fix. Proposed contract связывает per-level volume/obligation с proof; окончательный смысл должен быть утверждён.

## 7. Независимость денег и metadata

| Поле | Текущая передача | Требование для all-level/funding |
|---|---|---|
| ReserveEligibleMoney | Core net одного control | approved eligibility/kind/currency/basis каждого уровня |
| ReserveGainMoney | reserveAllocated либо eligible×share | confirmed Free, reservation/consumption lifecycle; no reshare |
| FarLossMoney | absolute control Far net | тот же level/volume/position/cost basis |
| Buffer | один template scalar плюс embedded leg buffers | CostCoverageMap и disjoint headroom purposes |
| AllocationKey | один outer source/consumption tuple | полный source registry, exact key/policy/event binding |
| SourceDealId/EventId | outer IDs, копируются в proof identity | independent broker history и EA association |
| SnapshotId | control snapshot ID | original content receipt, clock/expiry/restart |
| PlanId/StateRevision | outer current values | independently bound proof; historical origin plan отдельно |
| Prior history | bool+один prior pair | complete durable event/source inventory |

ReserveAllocationTypes:15–30 проверяет shape/часть tuple; это не provider/CAS.
ReserveCatchUpEvaluator:24–33 явно требует projected&&!actual. runtimeConfirmed относится к calculation result, не превращает projection в settled funds.
Allocated branch:63–66 отвергает any consumed>0, а не реализует полную модель частичного Free. Unallocated branch67–70 не имеет эквивалентного запрета. Reservations/global Free не запрашиваются.
Чистые повторные preview calls одного source не расходуют деньги. Runtime double-spend здесь не доказан; опасность возникает при превращении таких preview в funding permissions или повторном consumption.

## 8. Digest не заменяет content receipt

FutureSmallLevelDigest:95–104 включает recovery/T и cost snapshot IDs, но не отдельные Far/Core nets или cost components.
NewFar TemplateDigest:35–45 также использует IDs.
Перераспределение Far/Small fees вL2 между M_MINUS/M_PLUS сохраняет basket−7, но меняет CatchUp. Если IDs оставлены прежними, trusted immutable content receipt должен дать CONFLICT. Нельзя признавать изменённый snapshot authentic только по caller flags/пересчитанному digest.
Это связанный D13/ERR013 binding gap, а не утверждение об обходе валидной криптографической authority.

## 9. Однозначное заключение

| Аспект | Статус |
|---|---|
| Selective/all-required нормативный scope | CONFIRMED_CONTRACT_GAP |
| Отсутствие all-level evaluation/minimum относительно выбранного objective и proposed target | CONFIRMED_IMPLEMENTATION_GAP |
| Max Transition обязательно совпадает с min CatchUp | Опровергнуто MATH_DERIVED |
| Полный unsafe native accepted candidate | BLOCKED_BY_MISSING_EVIDENCE |
| Новый P0 | Не установлен |
| Исторический ERR018 | OPEN, прежний P1 |

Общий статус ERR018_SOURCE_AUDIT=CONFIRMED_CONTRACT_GAP. Кодовая структура single-control доказана; полнота реального runtime exploit не заявляется.

## 10. Приёмка и оставшиеся обязательства

Нужны fullCR09/required-set approval, per-level quantity/source/cost/numeric/snapshot receipts, funding prefix, completeness manifest, typed result, mandatory caller integration и native TL/CU cases. Все14P0 остаются открытыми. Никакого production fix нет.
Связи: [future contract](HSBI_03F_R2_TRANSITION_CATCHUP_CONTRACT_V1_RU.md), [vectors](HSBI_03F_R2_TEST_VECTOR_SPECIFICATION_RU.md), [TL001](HSBI_03F_R2_TL001_REGISTERED_FINDING_RU.md), [readiness](HSBI_03F_R2_DEPENDENCY_AND_READINESS_MATRIX_RU.md).
