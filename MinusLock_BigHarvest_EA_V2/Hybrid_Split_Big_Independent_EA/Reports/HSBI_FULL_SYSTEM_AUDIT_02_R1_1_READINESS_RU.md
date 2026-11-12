# AUDIT 02 — Minimal R1.1 readiness

R1_1_START_ALLOWED=NO
PRODUCTION_REMEDIATION_ALLOWED=NO

Единственный proposed production allowlist: `Include/Money/HSBI_EconomicLedgerTypes.mqh`. Все прочие Include/main/runtime/persistence/execution запрещены. Сейчас **нет** разрешения менять даже этот header.

Кандидат source namespace `(Broker,Server,AccountLogin,DealTicket)` не включает Magic/Cycle: их изменение при том же source key конфликт payload, а не новая прибыль. Broker — стабильная независимая namespace binding, не автоматически имя company. Broker history даёт Deal/Order/Position/Symbol/Magic/Entry/Type/Time/Volume/Price/Profit/Swap/Commission/Fee; HSBI Cycle/Action/Event/Role/Plan/Policy требует независимого EA-origin journal. DealNet derived; его equality не заменяет полные компоненты. Currency/precision — account/provider, не SYMBOL_DIGITS.

Предложенный 29-field envelope и точные acceptance rows: `Tests/Contracts/HSBI_FULL_SYSTEM_AUDIT_02_R1_1_ACCEPTANCE.json`. Это review R0G, не утверждение всех29 полей универсально минимальными. Required/unknown факты должны быть различимы и не получать fabricated default. Unknown legacy/history/source namespace → UNAVAILABLE, malformed → REJECT, same full source/payload → NO_OP, altered same key → CONFLICT, NEW лишь complete independently reconciled registry absence. NEW_IDENTITY не funding.

Canonical numeric boundary: captured finite binary64 immutable observations отдельно от posted integer-minor-unit amounts. Для F64Z-1 нужны fixed field order, version, exact UTF8 lengths, signed/unsigned encoding, zero normalization и finite-only goldens. F64Z пока PROPOSED. Не округлять raw observation в posted факт и не переносить Fraction в MQL. Native compatibility NOT_RUN.

One-file feasibility — условная: additive V2 structs/pure equality/status/codec helpers могут размещаться в одном header. Не доказана MetaEditor compile совместимость. Сохранение старого unsafe classifier как diagnostic-only не является исправлением старого financial caller. Перед разрешением нужен полный current callsite audit и явный выбор compatibility policy; external consumers не обнаруживаются одним rg. Реализация providers, reconciliation registry, durable funding и migration backend потребует отдельного расширенного scope — здесь не разрешена.

Положительные tests: full replay, independently confirmed new namespace, per-field equality. Negative: sameNet alteredcomponents, changed Magic/Cycle under same key, crossaccount source mismatch, unknown legacy/authority/currency/precision, nonfinite and boundaries, altered codec/schema, duplicate registry. На каждом отказе/no-op — zero delta. Native строгая компиляция основного EA и неторгового assertion harness обязательна до production acceptance.

Миграция: preserve old bytes/schema/digest; неизвестные records quarantine, не backfill текущим account. В Minimal не выполнять on-disk migration. Rollback: отдельный обратимый коммит, без persisted преобразований. Stop: недостающий approved contract, native failure/unavailable, необходимость второго production file, unexpected callsite или remote mismatch.

Семантические D-02/D-08/NUM-CODEC/MQL-DOMAIN/schema/compatibility прямо блокируют. D-01, D-03–D-07/CR-09/global funding не обязательно блокируют изолированную pure equality, но блокируют дальнейшее использование результата для funding/торговли. Даже готовый план и approved semantics не разрешают реализацию без отдельного задания.
