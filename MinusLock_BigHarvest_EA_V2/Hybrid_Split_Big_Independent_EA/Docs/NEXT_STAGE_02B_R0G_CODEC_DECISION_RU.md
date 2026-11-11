# R0G — codec ballot alternatives

BASE_SHA=bcaa766568b9fe7eec0781a8c6efbb288cf16dae

PROPOSED / AWAITING_ADMIN_APPROVAL. Только подготовка Minimal R1.1; ни одного production изменения или утверждения.

Источники: `Include/Money/HSBI_EconomicLedgerTypes.mqh:6` struct, `:7` BuildSourceDealKey, `:8` ValidateEconomicRecord, `:9` SameEconomicRecord, `:10` ClassifyEconomicDuplicate, `:11` SerializeEconomicRecord, `:12` IsHarvestSourceEntry. R0F ECONOMIC_IDENTITY_SPEC/NUMERIC_CODEC_OPTIONS/R1_IMPLEMENTATION_SPEC; frozen `hsbi_02b_r0f_contract_candidate.py:record_shape/encode_record`; новые TestID в TEST_RESULTS.json.

Рекомендация-кандидат: HSBI-F64Z-1, альтернатива HSBI-T17Z-1. CODEC_ADMIN_APPROVED=NO. Оба профиля frozen R0F: порядок29 полей FIELDS/fixture.ORDER, имена typed, exact UTF8 bytes/no NUL, не NFC/casefold. Рекомендация не является выбором администратора.

| Property | F64Z | T17Z |
|---|---|---|
| Header | HSBI-F64Z-1 + NUL | HSBI-T17Z-1 + LF |
| String | s + uint32BE byteLength + UTF8 | s + decimal byteLength + : + UTF8 |
| Integer | u+uint64BE positive/nonnegative; i+signed64BE negative | i+canonical decimal length+:+integer; no leading zeros |
| Float | d+8-byte binary64BE | d+length+:+scientific17:1 digit,16 decimals,e±DDD |
| bool / absent applicable | b0/b1 / n | b0/b1 / n0: |
| +/-0 | normalized +0 (Z) | normalized +0 (Z) |
| Finite/subnormal | exact bits from normalization |17 significant digit roundtrip; canonical formatter must match exactly |
| Unknown schema/codec | UNAVAILABLE, no new source | UNAVAILABLE, no new source |
| Nonfinite/type invalid | REJECT | REJECT |
| UTF8/integer/roundtrip | Python literal + independent struct fixture | Python literal whole fixture + scientific vectors |
| Native implementation | Inline byte helpers possible; checked ulong shifts, no union assumption | Inline possible but exact decimal-digit generation/formatter difficult |
| MetaEditor acceptance | NOT_RUN, required blocker for production acceptance | NOT_RUN, required blocker for production acceptance |

Wire integer bounds не задают field domain: AccountLogin/TimestampMsc positive signed64; Magic signed nonzero EA profile; tickets positive ulong; flags bool; Precision fixture0..8 only. SchemaVersion1 supported; future positive version UNAVAILABLE, bool/0 malformed. Logical key excludes codec, comparison cross-known profiles decode to identical validated schema, unknown mapping UNAVAILABLE. Python status gate receives typed objects, НЕ декодирует недоверенные wire bytes. Fixture roundtrip decoders проверяют только known valid vectors.

F64 candidate основан на bounded exponent [-1074,1023],53significant bits. Native *2,/2 normalization и underflow/subnormal behavior требуется проверить, в том числе ulong>=2^63 и смену endian. Нет предположения, что MQL разрешает C union/pointer punning. T17: произвольная roundtrip строка не canonical; DoubleToString формат не считать доказанным до goldens. При несоответствии formatter минимальный scope надо вернуть на доработку, не добавлять header.

Предложенный native resource cap для обоих кандидатов: <=4096 UTF8 bytes на string, <=65536 bytes на record, prechecked total/length/allocations. Это технический proposed MQL domain для ballot, не broker универсальный limit; wire32 допускает больше, но oversized native input=>UNAVAILABLE без allocation. Проверять UTF16 surrogate→UTF8 mapping/terminating NUL exclusion. Строгий decoder проверяет truncation, exact fields/order/tags, duplicate/unknown/trailing bytes, length caps, canonical exponent/int. В R0G hostile decoder/native cap enforcement NOT_RUN (не реализованы в Python wrapper).

Golden source: R0F independent fixture.GOLDENS (8scalar vectors), literal Text17Expected/BitsExpected в R0F CODEC_GOLDENS.json, новые CODEC-* tests/UTF8/account bounds. Raw negative zero original sign не сохраняется Z; если требуется bit-exact raw packet, ни один Z профиль не подходит без другого решения.

Блокер: без MetaEditor нельзя доказать production compatibility. Это не препятствие подготовить ballot, но запрещает native PASS/приёмку будущего R1.1. Decimal/broker posting/settled integer conversion не часть source codec.
