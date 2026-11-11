BASE_SHA=7afad885a8ef8ff2c8189ca72760e06a1baaa50a

PROPOSED / AWAITING_ADMIN_APPROVAL. R0H TEST-ONLY. No production remediation, broker/account IO, funding, allocation or persistence.

Исходники: `Include/Money/HSBI_EconomicLedgerTypes.mqh:6` record, `:7` key, `:8` validate, `:9` equality, `:10` classifier, `:11` serializer, `:12` harvest helper. Production включает Core/Enums/Identifiers/ReasonCodes. R0G MINIMAL_IDENTITY_CONTRACT/MQL5_API_SPEC и F64Z/T17Z alternatives сохранены. Новая Python `hsbi_02b_r0h_identity_codec.py:source_key/equal_body/bits/unbits/encode/decode/classify`; MQL `hsbi_02b_r0h_native_codec.mqh:R0H_Validate/R0H_Key/R0H_Equal/R0H_Classify/R0H_Encode/R0H_Decode`, entry `hsbi_02b_r0h_native_harness.mq5:OnStart`. Новые goldens generated только independent fixture struct.pack/literal, не subject encoder.

# Native domain — proposed, NOT_RUN

R0H-DOMAIN: AccountLogin и TimestampMsc positive signed long1..2^63-1; Magic signed long[-2^63,2^63-1], nonzero только EA-attributed BUY/SELL profile; Cycle/Deal/Order/Position/Action/Event/SourcePlan/Policy positive ulong1..2^64-1, bool не integer-ID. SourcePlan/Policy N/A только explicit applicability false. Schema1 supported, positive future schema UNAVAILABLE, malformed0/bool REJECT. Money precision fixture0..8 не Symbol price digits и не все валюты мира.

Raw double finite binary64 наблюдение, Volume/Price>0; Profit/Swap/Commission/Fee signed и Net distinct immutable. NaN/Infinity invalid. +/-0 эквивалентны Z policy; wire negative-zero noncanonical reject. Никаких raw->posted округлений или balance arithmetic. LONG_MIN/MAX,ULONG_MAX,9007199254740993 проверяются bytes без промежуточного double для ID. Floating coefficient<=2^53 в decoder относится только double payload, не ticket. EndianBE, unsigned shifts и native signed casts требуют MetaEditor/MT5 evidence.

UTF8 exact/no NUL/no normalization; uint32 length — число bytes. Нативный proposed cap4096 bytes/string и65536/record, oversized UNAVAILABLE. Unicode roundtrip и surrogate policy должны пройти native assertion; Python strict UTF8 не доказывает MQL StringToCharArray/CharArrayToString. New typed DTO содержит tagged values с полной формой29полей; bool tag может быть wrong-type case даже при сильных native types. Registry/authority completeness fixture flags не provider authenticity.

MQL assertions planned: exact boundaries, unicode Б, 2^53+1 ID, normal/subnormal/maxfinite, +/-zero, bool kind rejection, byte arrays, key/equality/status. Полный native-domain closure/array-allocation failure behavior NOT_RUN. Native code is test-only candidate; compiler errors/warnings нельзя считать PASS статическим чтением.
