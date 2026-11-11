# R0G — предлагаемые MQL5 signatures, не production code

BASE_SHA=bcaa766568b9fe7eec0781a8c6efbb288cf16dae

PROPOSED / AWAITING_ADMIN_APPROVAL. Только подготовка Minimal R1.1; ни одного production изменения или утверждения.

Источники: `Include/Money/HSBI_EconomicLedgerTypes.mqh:6` struct, `:7` BuildSourceDealKey, `:8` ValidateEconomicRecord, `:9` SameEconomicRecord, `:10` ClassifyEconomicDuplicate, `:11` SerializeEconomicRecord, `:12` IsHarvestSourceEntry. R0F ECONOMIC_IDENTITY_SPEC/NUMERIC_CODEC_OPTIONS/R1_IMPLEMENTATION_SPEC; frozen `hsbi_02b_r0f_contract_candidate.py:record_shape/encode_record`; новые TestID в TEST_RESULTS.json.

## R0G-STATUS-2

Статусы versioned enum `HSBI_EconomicIdentityStatusV2`: NEW=0, NO_OP=1, CONFLICT=2, REJECT=3, UNAVAILABLE=4. Значения0/1/2 исторически совпадают, но V2 enum НЕ совместим семантически с legacy int без явного caller review.

| Status | Precise scope |
|---|---|
| NEW | Полный подтверждённый incoming source, complete reconciled logical registry, key отсутствует; только new identity, не funding |
| NO_OP | Supported exact same immutable body по independently confirmed logical key и existing registry; zero state delta |
| CONFLICT | Изменённый immutable payload при известном key, либо противоречивый/дублированный registry |
| REJECT | Malformed input/type/known invalid enum/nonfinite/out-of-range ID; zero delta |
| UNAVAILABLE | Unknown schema/codec/legacy/missing independent source/namespace/origin/currency/precision/absence proof; не NEW |

Приоритет: shape incoming -> codec support -> shape/completeness authority+registry -> independent source key -> body conflict -> registry validation/uniqueness -> NEW/NO_OP/CONFLICT. Все решения pure; authoritative source с другим logical key не доказывает incoming, даёт UNAVAILABLE. Authority DTO malformed=>REJECT; unknown provider facts=>UNAVAILABLE. Unknown ledger schema/entry blocks absence, unknown key migration не создаёт source. Duplicate registry rows требуют reconciliation даже при одинаковом payload.

## Точные предлагаемые сигнатуры

```cpp
enum HSBI_EconomicIdentityStatusV2 { HSBI_ECON_V2_NEW=0, HSBI_ECON_V2_NO_OP=1, HSBI_ECON_V2_CONFLICT=2, HSBI_ECON_V2_REJECT=3, HSBI_ECON_V2_UNAVAILABLE=4 };
HSBI_EconomicIdentityStatusV2 HSBI_ValidateEconomicRecordV2(const HSBI_EconomicLedgerRecordV2 &record, string &reason);
bool HSBI_SameEconomicSourceKeyV2(const HSBI_EconomicLedgerRecordV2 &a, const HSBI_EconomicLedgerRecordV2 &b);
HSBI_EconomicIdentityStatusV2 HSBI_CompareEconomicPayloadV2(const HSBI_EconomicLedgerRecordV2 &existing, const HSBI_EconomicLedgerRecordV2 &incoming, string &reason);
HSBI_EconomicIdentityStatusV2 HSBI_ClassifyEconomicIdentityV2(const HSBI_EconomicLedgerRecordV2 &incoming, const HSBI_EconomicAuthorityViewV2 &authority, const HSBI_EconomicRegistryViewV2 &registry, const string codecId, string &reason);
HSBI_EconomicIdentityStatusV2 HSBI_EncodeEconomicRecordV2(const HSBI_EconomicLedgerRecordV2 &record, const string codecId, uchar &bytes[], string &reason);
HSBI_EconomicIdentityStatusV2 HSBI_DecodeEconomicRecordV2(const uchar &bytes[], const string codecId, HSBI_EconomicLedgerRecordV2 &record, string &reason);
```

Validate/Encode/Decode successful result=NO_OP как `validated/no state operation`, не NEW credit; Compare same key exact=>NO_OP, altered=>CONFLICT, distinct key=>UNAVAILABLE (caller cannot infer registry absence). Key bool true только validated keys; false не NEW. Classify — единственный identity-level NEW. Все output refs при error остаются неизменными, reason может обновляться; Decode uses temporary validated body then assignment. No exceptions-as-success. Новые structs/views в том же header: V2body29fields, optional SourcePlan/Policy presence bool; RegistryView содержит complete flag+record array; AuthorityView содержит independentConfirmed/available flags+record, namespace receipt reference/provider version. Flags/reference не доказывают broker authenticity: только boundary contract; Classify проверяет shapes и body binding.

Для C-like MQL API нет Python None: unknown namespace/units/origin/legacy задаются explicit typed completeness/presence status в envelope; их нельзя default-initialize в known. Только producer независимого provider может ставить confirmed; в R1.1 provider не реализуется. SourceKey equality не использует sourceDealKey legacy cache. Все helpers inline в одном разрешённом header после отдельного задания.

## Legacy compatibility (R0G-COMPAT-1)

Старая struct и все7 имён/сигнатур сохраняются. BuildSourceDealKey/Validate/Same/Classify/Serialize/IsHarvestSourceEntry/record — diagnostic-only для старой схемы; старая Classify возвращает0/1/2 с прежней diagnostic семантикой. Не переопределять0 как безопасный NEW. Никаких implicit overload/adapters legacy→V2/UNAVAILABLE→NEW. Любой старый diagnostic int не разрешён как proof/funding decision. Только V2 используется новым harness/API. Для неизвестного legacy V2 conversion возвращает UNAVAILABLE, без current account fallback и fabricated milliseconds.

Это additive remediation proposal: устраняет L01 в новом typed approved surface, не делает старую unsafe equality безопасной. Пока есть возможный external consumer старого Classify как financial authority, Minimal approval недостаточно — caller integration/расширение allowlist отдельным заданием. Static rg по текущим Include/main нашёл legacy symbols только в самом header; это не гарантия внешних программ. Сохранение old diagnostic algorithm требует явного принятия compatibility policy администратором; при требовании исправить старый financial path без V2 нужен другой ballot.
