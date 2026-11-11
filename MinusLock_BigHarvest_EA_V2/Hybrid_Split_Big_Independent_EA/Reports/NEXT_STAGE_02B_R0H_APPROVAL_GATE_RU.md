BASE_SHA=7afad885a8ef8ff2c8189ca72760e06a1baaa50a

PROPOSED / AWAITING_ADMIN_APPROVAL. R0H TEST-ONLY. No production remediation, broker/account IO, funding, allocation or persistence.

Исходники: `Include/Money/HSBI_EconomicLedgerTypes.mqh:6` record, `:7` key, `:8` validate, `:9` equality, `:10` classifier, `:11` serializer, `:12` harvest helper. Production включает Core/Enums/Identifiers/ReasonCodes. R0G MINIMAL_IDENTITY_CONTRACT/MQL5_API_SPEC и F64Z/T17Z alternatives сохранены. Новая Python `hsbi_02b_r0h_identity_codec.py:source_key/equal_body/bits/unbits/encode/decode/classify`; MQL `hsbi_02b_r0h_native_codec.mqh:R0H_Validate/R0H_Key/R0H_Equal/R0H_Classify/R0H_Encode/R0H_Decode`, entry `hsbi_02b_r0h_native_harness.mq5:OnStart`. Новые goldens generated только independent fixture struct.pack/literal, не subject encoder.

# Approval Gate options

A NATIVE_VERIFIED / READY_FOR_ADMIN_DECISION — только после real MetaEditor/MT5 compile+assertions и independent bytes; сейчас НЕ достигнут.
B REFERENCE_ONLY / NATIVE_NOT_RUN — текущий фактический результат. Reference identity/status/strictcodec checks pass, native source prepared but uncompiled; no productionacceptance/start.
C BLOCKED / NATIVE_FAILED — при native compile/semantics/golden mismatch; нельзя присваивать сейчас без запуска. Будущие исправления только test scope до отдельного разрешения.

F64Z recommendation reference-only; no codec APPROVED. D02/D08, NUM-CODEC/MQL-DOMAIN, fullschema/compatibility и nativegate остаются AWAITING_ADMIN_APPROVAL. R0H не подписывает R0G ballot. Broker/EA origin authenticity, actual reconciliation/globalfunding/durableconcurrency/NewFar UNPROVEN. Semantic decision может быть рассмотрено администратором, но никакой A/B/C сам не разрешает R1.1.

ADMIN_APPROVAL_COMPLETE=NO
R1_1_START_ALLOWED=NO
PRODUCTION_REMEDIATION_ALLOWED=NO
TRADING_LOGIC_START_ALLOWED=NO
BROKER_DISPATCH_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
