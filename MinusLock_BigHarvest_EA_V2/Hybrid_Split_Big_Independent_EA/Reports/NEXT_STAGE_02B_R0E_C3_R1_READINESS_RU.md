# C3 — gate будущего R1.1 Economic Ledger Identity

BASE_SHA=3737116bff6e2275d674b3dd7b816de93715f27c

AUDIT / PROPOSED / AWAITING_ADMIN_APPROVAL. Production, trading и dispatch запрещены.

R1_1_START_ALLOWED=NO. Ни C3 COMPLETE, ни reference PASS не является административным approval.

| Gate | Текущее состояние | Требуется до отдельного R1.1 |
|---|---|---|
| Approval | Все16 AWAITING | Явные выбранные schema/namespace/codec/precision зависимости |
| Production allowlist | C3 предполагает только Include/Money/HSBI_EconomicLedgerTypes.mqh; старый R0B R1.1 spec разрешал также2 новых helper headers | Разрешить конфликт scope отдельным заданием; не добавлять helpers автоматически |
| Immutable schema | Production отсутствуют AccountLogin/Broker/Server/currency/precision/SourcePlan/direction/schema envelope | Утвердить полный immutable payload и отдельные mutable reconciliation flags |
| Source namespace | Текущий key symbol|magic|cycle|deal; account отсутствует | Versioned broker/server/account/deal namespace, типы/диапазоны и collision tests |
| Duplicate equality | L01 native confirmed; отдельные Profit/Swap/Commission/Fee игнорируются | Exact raw/component/identity equality; changed payload CONFLICT, exact NO_OP zero deltas |
| Raw vs posted / precision | R0B raw64/NFC proposal vs R0D fixture codec vs integer money architecture | Выбрать source codec и отдельные posted fields; неизвестные broker amounts не money authority |
| Provider boundary | DealID>0/valid flag только shape | Shape не existence; reconciliation provider отдельно, unavailable source нельзя credit |
| Migration | Legacy key без account, truncated serialization | Preserve bytes/schema/hash; append-only authenticated migration or quarantine; не текущий ACCOUNT_LOGIN |
| Rollback | Production phases не начаты | Separate reviewed revert своего будущего commit; no reverse money migration/trades |
| Tests | Новые независимые C3 vectors; точное количество в evidence; native equality defects | Per-field source mutations, account collision, unknown schemas, raw components cancellation, posted mismatch, zero deltas |
| Compile plan | MetaEditor/MT5 отсутствует | Реальный MetaEditor compile main+new MQL harness; g++ extraction не замена |

Предлагаемый будущий порядок: (1) административные решения schema/namespace/raw-vs-posted/codec/legacy unavailable; (2) новое задание с одним явным allowlist и свежим baseline; (3) immutable Economic DTO/source key/equality/serialization и scoped tests без money credits; (4) MetaEditor/native acceptance и review; (5) отдельно остальные ledger/funding/durable/identity/CatchUp/FutureSmall/NewFar этапы по dependency graph. Source identity должна предшествовать allocation provenance; оба — consumption/journal; durable backend и reconciliation — runtime authorization; NewFar не может безопасно обходить предпосылки.

Нельзя одновременно исправлять M01/M02/L02/geometry или реализовывать dispatch в R1.1. Даже при одобрении логической независимости источника broker integration остаётся отдельным приёмочным этапом. Этот документ не меняет production allowlist сейчас.
