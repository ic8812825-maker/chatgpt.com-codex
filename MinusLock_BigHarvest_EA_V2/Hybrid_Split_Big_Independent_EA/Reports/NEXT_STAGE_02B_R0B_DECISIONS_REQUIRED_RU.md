# 02B-R0B — решения, требующие администратора

База `9b43c38afdb89c6b3b514b654c7fb9a936f9bf2b`. Только audit/test-only. Все D-01–D-08/CR-09 ожидают администратора. Новые документы не заменяют старые нормативы автоматически.

Точные выбранные варианты должны быть подписаны отдельно. Рекомендуемые варианты не считаются автоматически действующими; явно небезопасные/неполные альтернативы возвращаются на переработку, а не запускаются в production.

## D-01

**Проблема:** Docs/04,08 требуют equality; Docs/32 допускает <= и складывает consumed с неуточнёнными grants. Дополнительные R0B gaps и пределы доказательств перечислены в Findings.

**Альтернативы:** Allocation F: full COMMITTED equality, partial only PREPARED (recommended); Permanent partial COMMITTED: not supported without separate exact schema decision; A: broker-posted amounts/posted components with independent source receipt; B: versioned local precision policy after broker validation; C: UNAVAILABLE without sufficient data

**Рекомендация:** Broker-posted первично; approved local policy only after verification, otherwise UNAVAILABLE. Полные immutable grants; отдельные balances; промежуточный Unallocated недоступен.

**Математическое обоснование:** При debit x: Remaining-=x, Consumed+=x, поэтому их сумма сохраняется. Reservation отдельно уменьшает Available, не Grant. Equality по каждому source не доказывает общесчётную solvency.

**Пример:** Grant50, remaining40, consumed10; reserved5 => available35. Нераспределённые10 допустимы PREPARED, не COMMITTED.

**Миграция:** Новая schema: OriginalGrant/Consumed/Reserved/Remaining различаются. Старое reserveAllocated нельзя автоматически объявить original/remaining. Legacy с неизвестной полнотой => reconciliation, без spend.

**Не доказано:** Broker authenticity/precision, durable IO/CAS, mandatory full caller chain, MQL5 runtime; никакой PASS из fixtures не закрывает эти зависимости.

**Approval:** AWAITING.

## D-02

**Проблема:** Общее recoveryMoney может смешивать прогноз и доступный ресурс. Дополнительные R0B gaps и пределы доказательств перечислены в Findings.

**Альтернативы:** Один double с флагами; Раздельные DTO и явные conversion gates

**Рекомендация:** Раздельные DTO, без неявного projected→actual/available.

**Математическое обоснование:** Нет разрешённого перехода Projected→Grant: обязательное actual event/reconciliation отсутствует. Поэтому projected100 и actual0 не дают Available100.

**Пример:** ProjectedBasketNet100, confirmed sources0 => allocated0/available0.

**Миграция:** Legacy projected без source receipt остаётся projected или UNAVAILABLE; никакой миграции через actual=true.

**Не доказано:** Broker authenticity/precision, durable IO/CAS, mandatory full caller chain, MQL5 runtime; никакой PASS из fixtures не закрывает эти зависимости.

**Approval:** AWAITING.

## D-03

**Проблема:** Aggregate Core+Trend+Small ошибочно выглядит разрешённым Big Reserve. Дополнительные R0B gaps и пределы доказательств перечислены в Findings.

**Альтернативы:** Small участвует в BigReserve по новому разрешению; Small отдельно в ResidualHeld; Small в отдельном утверждённом spending bucket

**Рекомендация:** Small positive net — ResidualHeld, не BigReserve; Core/Trend только confirmed eligible источники.

**Математическое обоснование:** Small10 сохраняется как EconomicNet10 и ResidualHeld10; FinalReserve0. Повторно прибавить buckets к actual net нельзя.

**Пример:** Core0 Trend0 Small10 => aggregate10, permitted BigReserve0.

**Миграция:** Исторические Small allocations не переклассифицировать без подтверждённого source/consumption history; отдельная policyVersion.

**Не доказано:** Broker authenticity/precision, durable IO/CAS, mandatory full caller chain, MQL5 runtime; никакой PASS из fixtures не закрывает эти зависимости.

**Approval:** AWAITING.

## D-04

**Проблема:** Название increase не определяет baseline и может ослаблять gate. Дополнительные R0B gaps и пределы доказательств перечислены в Findings.

**Альтернативы:** AbsoluteFarLoss для gate; IncrementalFarLoss с независимым baseline; Оба значения раздельно, metric в immutable policy

**Рекомендация:** Хранить оба, для рекомендуемого рабочего gate выбрать ABSOLUTE; incremental — diagnostic до отдельного разрешения.

**Математическое обоснование:** При loss50/baseline40/buffer5 margins R20: -35/+5; R60: +5/+45. Различие делает выбор метрики нормативным.

**Пример:** Baseline40/current50/Reserve20/buffer5: absolute rejects, incremental passes.

**Миграция:** Сохранять lossMetric/version, baseline origin и lineage. Старый baseline не угадывать; current absolute semantics до реализации остаётся прежней.

**Не доказано:** Broker authenticity/precision, durable IO/CAS, mandatory full caller chain, MQL5 runtime; никакой PASS из fixtures не закрывает эти зависимости.

**Approval:** AWAITING.

## D-05

**Проблема:** Одна семантическая область для плановой оценки и фактического accounting. Дополнительные R0B gaps и пределы доказательств перечислены в Findings.

**Альтернативы:** Общий DTO с тегом; Раздельные projected/actual records

**Рекомендация:** Раздельные типы и обязательная post-fill reconciliation.

**Математическое обоснование:** Observed net -15 даёт loss15 независимо от plan10; partial status не уменьшает известное превышение cap12.

**Пример:** Projected10/actual15/cap12: SAFE_BLOCKED; actual не переписывается на10.

**Миграция:** Хранить planned и actual separately, уникальные fills, remaining volume и over-cap reason; legacy с неизвестной completeness => UNAVAILABLE.

**Не доказано:** Broker authenticity/precision, durable IO/CAS, mandatory full caller chain, MQL5 runtime; никакой PASS из fixtures не закрывает эти зависимости.

**Approval:** AWAITING.

## D-06

**Проблема:** Не определено пересечение per-leg и Catch-Up deductions. Дополнительные R0B gaps и пределы доказательств перечислены в Findings.

**Альтернативы:** Единый общий budget с распределением; Независимые бюджеты с непересекающимися risk basis

**Рекомендация:** Charge-once по документированным riskBasis/window, отдельные независимые risk budgets; unresolved overlap блокирует proof.

**Математическое обоснование:** Сумма5 корректна лишь для пяти независимых покрытий. При одном RiskBasis/Window два charge являются double deduction; удаление одного без evidence может недоучесть риск.

**Пример:** Four leg1 + Catch-Up1: 5 при независимых risks; CONFLICT при повторе leg0 coverage.

**Миграция:** Новая cost coverage schema; старые combined buffers без basis требуют независимого rebuild projected proof, не изменения actual history.

**Не доказано:** Broker authenticity/precision, durable IO/CAS, mandatory full caller chain, MQL5 runtime; никакой PASS из fixtures не закрывает эти зависимости.

**Approval:** AWAITING.

## D-07

**Проблема:** Bool prior и key без amount не доказывают exactly-once. Дополнительные R0B gaps и пределы доказательств перечислены в Findings.

**Альтернативы:** Typed NO_OP; REJECT с доказанным NOOP reason

**Рекомендация:** Typed outcomes; eligibility отдельно от commit, durable registry как prerequisite.

**Математическое обоснование:** После E1=10 из50 Remaining40; exact E1 не меняет state/revision. Changed payload не эквивалентен первому событию и даёт CONFLICT.

**Пример:** E1=10 повторён с amount11 или policy2: CONFLICT, даже если текущая revision уже2.

**Миграция:** Старые events без amount/bucket/policy нельзя автоматически считать exact replay. Восстановить source payload или UNAVAILABLE/manual review.

**Не доказано:** Broker authenticity/precision, durable IO/CAS, mandatory full caller chain, MQL5 runtime; никакой PASS из fixtures не закрывает эти зависимости.

**Approval:** AWAITING.

## D-08

**Проблема:** Флаги и self-copy expected не подтверждают existence/provenance. Дополнительные R0B gaps и пределы доказательств перечислены в Findings.

**Альтернативы:** Доверенные caller flags; Broker history + durable journal + independent reconciliation; Test-only fixture provider без production authorization

**Рекомендация:** История брокера плюс durable журнал и независимая reconciliation; fixture только для тестов.

**Математическое обоснование:** Нет логического вывода existence из DealID>0 или proof==copiedExpected. Фиксированный independent history отсутствующий deal отвергает независимо от caller flags.

**Пример:** Order/Position/Snapshot неизвестны authorize R0A; добавленный чужой атрибут может быть проигнорирован. Это gap локальной API, не доказательство обхода полного verify_proof pipeline.

**Миграция:** Legacy source без account/server/полного payload нельзя восстановить по строке Symbol|Magic|Cycle|Deal. Нужна проверяемая миграция из history, иначе блокировка.

**Не доказано:** Broker authenticity/precision, durable IO/CAS, mandatory full caller chain, MQL5 runtime; никакой PASS из fixtures не закрывает эти зависимости.

**Approval:** AWAITING.

## CR-09

**Проблема:** Maximum TransitionLoss не обязан совпадать с minimum Catch-Up margin. Дополнительные R0B gaps и пределы доказательств перечислены в Findings.

**Альтернативы:** A: все обязательные уровни; B: один выбранный уровень без all-level guarantee

**Рекомендация:** A; B допустим только явно ограниченным альтернативным решением.

**Математическое обоснование:** T1=100>T2=10, но C1=29>C2=-16. Equivalence требует дополнительной antitone зависимости, например C=a-bT,b>0, с согласованными ties.

**Пример:** A выбирает L2=-16 и reject; B выбирает L1=+29, но только SINGLE_LEVEL_ONLY.

**Миграция:** Хранить selectionPolicy/scope/version, RequiredLevels и все source proof references. Старый max-loss proof не повышать автоматически до all-level.

**Не доказано:** Broker authenticity/precision, durable IO/CAS, mandatory full caller chain, MQL5 runtime; никакой PASS из fixtures не закрывает эти зависимости.

**Approval:** AWAITING.

## Дополнительные вопросы в рамках этих решений

- D-01/D-08: как атрибутируются negative actual debits и opening costs к funding sources; до reconciliation не делать общий available вывод из positive grants.
- D-07: ReservationOwner/Intent settlement и durable CAS — formal requirements, не реализованный backend.
- D-08: новый proposed raw64 codec не меняет broker precision law и не переинтерпретирует R10/R12A roots. Неизвестная schema/source namespace блокирует money authorization.
- Zero BigCore: reject mandatory Core ниже min; отдельная geometry фаза, автоматическая ceil-normalization не разрешена. Core>=min не закрывает grid/max/slope/money/risk/margin.
- R1.1 требует отдельного задания после утверждения. R1.2–R1.5 и dispatch не входят в него автоматически.

См. [лист утверждения](NEXT_STAGE_02B_R0B_ADMIN_APPROVAL_SHEET_RU.md), [precision review](../Docs/NEXT_STAGE_02B_R0B_PRECISION_POLICY_REVIEW_RU.md) и [R1.1 spec](../Docs/NEXT_STAGE_02B_R1_1_IMPLEMENTATION_SPEC_RU.md).
