# 02B-R0E-C1 — дополнение к предлагаемым контрактам

BASE_SHA=074165b38f1b6d6253a9629c7d2def988e8e286a

PROPOSED / AWAITING_ADMIN_APPROVAL. Audit/test-only; production/trading/dispatch запрещены.

## Нормативный статус и границы

D-01–D-08, CR-09, NUM/SNAP, FUNDING-GLOBAL-ATTRIBUTION, MQL-DOMAIN и BALANCE-SCHEMA-MAPPING не утверждены. Исторические READY/COMPLETE не переписаны. Новое дозакрытие исправляет тестовую реализацию и доказательность пакета, а не production-экономику. Reference PASS не превращает PROPOSED в APPROVED.

Scope и доверенные inputs каждого API определены до реализации в NEXT_STAGE_02B_R0E_C1_API_SCOPE_AND_COMPOSITION_RU.md. Independent authority — fixture provider boundary, не broker authentication. Экономическая история и current context независимы от presented proof; source origin Plan1 и current Plan10 допустимы. В публичном составном apply нет параметра «готовое разрешение», он всегда заново авторизует запрос.

| ClarificationID | Изменение / текущий proposed контракт | Характер / административный выбор / R1.1 |
|---|---|---|
| C1-JOURNAL / D02,D07 | AvailableReserve только после complete independent core journal + commit receipts и reconstruction. Unknown не known0. Private арифметический helper не public proof | Исправление scope/реализации; не новый экономический выбор. Влияет на будущий caller контракт |
| C1-BATCH / D05,D08 | Independent expected broker/server/account, batch/order/position/cycle/symbol/currency/digits/volume/required source set. Существование fill не равно membership | Усиление provenance и scope. Порядок netting/cap требует утверждения D05; broker partial execution NOT_RUN |
| C1-COST / D06 | Полный independently supplied applicable-cost set. REQUIRED покрыт ровно один раз; UNKNOWN/unknown overlap UNAVAILABLE; KNOWN_ZERO и NOT_APPLICABLE отдельные dispositions | Уточнение полноты, не выбор размера buffer. Применимость/суммы задаёт provider, не request |
| C1-EVENT / D08,D07 | EconomicEventID, AllocationEventID, ConsumptionEventID раздельны; expected из history/allocation/context. _bind_allocation связывает immutable vector с ledger | Уточнение identity и обязанностей callers; field/schema migration требует утверждения прежних решений |
| C1-REPLAY / D07 | Сначала typed namespace/request + history + complete journals + immutable economic source; changed valid source CONFLICT. Затем exact known receipt NO_OP, changed payload CONFLICT, новые current gates только для нового event | Явный PROPOSED fixture priority. Администратор должен выбрать приоритет source conflict / receipt replay / unavailable authority; не implemented durable exactly-once |
| C1-HISTORICAL / D07,D08 | Receipt хранит независимо validated evaluationContext as-at-commit. Recovery связывает source, allocation digest/event и planned operation с reconstructed ledger, а не копирует presented identity в expected | Исправление прототипа C1. Historical context — fixture journal fact, authenticity/durable persistence UNPROVEN |
| C1-EVIDENCE | Required catalog из versioned executable spec, не из результатов. Уникальные status fields; provenance всех финальных evidence roles; dynamic subject call trace | Техническое исправление verification, не экономическое решение |

## Точные деньги и accounting

G=C+Reserved+Free; Gross=Reserved+Free. Компоненты Profit/Swap/Commission/Fee сохраняют знак. Raw sum и posted grid проверяются отдельно; source=(Broker,Server,Account,Deal). Валюта/digits не выводятся из суммы и не конвертируются неявно. Точная арифметика и codec R0D неизменны. MQL5 int64 domain не расширяется до Python Fraction domain.

C1 публичная composed операция ограничена CONSUME_FREE. PrincipalAmount задаётся independent planned-operation context и сверяется с request. AdditionalRisk — safety headroom deduction, не реальный расход. RequiredBalance=PrincipalAmount+AdditionalRisk, RequiredBalance<=Free; DebitAmount=PrincipalAmount; C'=C+Debit, Free'=Free-Debit. Buffer не становится Consumed. Пример: G50, principal10, risk0.5 →required10.5, consumed10, free40. Principal50/risk0.5 отклоняется; principal50/risk0 может полностью израсходовать50. Полный Catch-Up lot/Far/margin proof этим не реализован.

REQUIRED signed actual cost, ещё не включённый в reconciled net, даёт UNAVAILABLE: модель не создаёт локальный broker posting и не угадывает conversion. Полный registry CostSet содержит и dispositions KNOWN_ZERO/NOT_APPLICABLE; клиент не может удалить строку, скрыв отсутствие применения. Independently complete empty CostSet допускает empty claims.

## Partial-fill profile

Только явно названный PROPOSED_SIGNED_BATCH_NET_V1: unique принадлежавшие target batch fills, exact summed volume и signed net; loss=max(0,-net). Cap проверяется и при неполном prefix. CONFIRMED требует полного RequiredDeals и expectedVolume. Foreign account/lineage/currency блокируются до netting. Неизвестная policy/history UNAVAILABLE. Этот профиль не утверждает универсальное netting, sticky OVER_CAP или peak path-loss; такие варианты остаются административным выбором D05.

## Replay и authority

Exact replay означает только воспроизведение подтверждённого in-memory fixture receipt с zero deltas. Он не подтверждает новые current provider facts. Historical allocation/identity проверяется по independent journal/core reconstruction и stored evaluationContext, current Plan/Revision/Snapshot могут измениться без нового расхода. Current allocation provider не заменяет historical core allocation при replay; конфликт economic source в выбранном C1 profile приоритетнее NO_OP. Иная политика приоритетов требует явного выбора D07.

Input shape до lookup проверяет namespace/event ranges, required top-level fields и тип identity container; полная identity value verification относится к новому событию. Изменённый known payload (включая неполную identity dict) не может стать NO_OP; его статус CONFLICT. Синтаксически недопустимые top-level DTO/ID/amount отклоняются раньше. Unexpected programming exceptions не маскируются REJECT.

## План применения

Сначала независимое review C1 и административный выбор прежних D/NUM/SNAP contracts, затем отдельный verified-baseline R1.1. Namespace/immutable Economic Ledger equality остаётся первой узкой production фазой; funding/durable/identity/Catch-Up/FutureSmall/NewFar идут по прежнему dependency graph. Никакой реализации R1.1 сейчас. Global economic debit attribution, broker authenticity/precision/margin, durable CAS/crash recovery и full NewFar integration остаются UNPROVEN.
