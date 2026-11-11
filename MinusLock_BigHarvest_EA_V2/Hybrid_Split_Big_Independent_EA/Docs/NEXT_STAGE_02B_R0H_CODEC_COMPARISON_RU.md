BASE_SHA=7afad885a8ef8ff2c8189ca72760e06a1baaa50a

PROPOSED / AWAITING_ADMIN_APPROVAL. R0H TEST-ONLY. No production remediation, broker/account IO, funding, allocation or persistence.

Исходники: `Include/Money/HSBI_EconomicLedgerTypes.mqh:6` record, `:7` key, `:8` validate, `:9` equality, `:10` classifier, `:11` serializer, `:12` harvest helper. Production включает Core/Enums/Identifiers/ReasonCodes. R0G MINIMAL_IDENTITY_CONTRACT/MQL5_API_SPEC и F64Z/T17Z alternatives сохранены. Новая Python `hsbi_02b_r0h_identity_codec.py:source_key/equal_body/bits/unbits/encode/decode/classify`; MQL `hsbi_02b_r0h_native_codec.mqh:R0H_Validate/R0H_Key/R0H_Equal/R0H_Classify/R0H_Encode/R0H_Decode`, entry `hsbi_02b_r0h_native_harness.mq5:OnStart`. Новые goldens generated только independent fixture struct.pack/literal, не subject encoder.

# F64Z и T17Z: сравнение и границы

| Criterion | F64Z | T17Z |
|---|---|---|
| Binary64 precision | Python arithmetic bits vs literal/struct.pack PASS | Python17digit literals/roundtrip PASS |
| MQL5 complexity | bounded normalization + shifts + strict binary parser | exact17digit formatter/exponent/locale + text parser |
| Determinism | reference PASS, native NOT_RUN | reference PASS, native formatter probe NOT_RUN |
| Canonical encoding | tagged fixed names/order, finite64BE, zero normalized | tagged lengths, scientific1+16digits/e±DDD; zero normalized |
| Malformed input | Python truncation/duplicate/trailing/tag/cap/UTF8/nonfinite tested | Python strict length/type/duplicate/trailing/schema tested |
| Native implementation | isolated full candidate encoder/decoder header | T17Probe only: DoubleToString(x,-16)+exponent normalization; no full native text decoder |
| Size | actual source bytes/lines in CODE_METRICS evidence; no runtime size claims | full production implementation not written; estimate additional exact formatter/text grammar code |
| Minimal one-file | statically inlineable, native acceptance remains blocker | conditional if nativeformatter matches all goldens; otherwise extra algorithm needed in sameheader/return forrevision |

Recommendation remains F64Z candidate, not ADMIN_APPROVED. Arithmetic bit extraction avoids assumed union/pointer casts; native normalization, cast signed/unsigned and subnormal behavior unknown. Negative zero normalized, so neither Z codec preserves network packet sign bit. Source identity excludes codecversion, new codec does not new income. Mismatched known payload->CONFLICT after semantic decode; unsupported codec/schema->UNAVAILABLE, no NEW.

Goldens: independent R0F fixture.GOLDENS and binary_record, literal17digit expectations, generated test mqh stores full fixed29field wire hex. Python expected for malformed tests constructed independently from fixture tokens; expected statuses literal. Runtime decoder actual NOT_RUN. Compiler literal minsubnormal may be unsupported; then native assertion/compile FAIL and recommendation must be reviewed. Exact DoubleToString result is a probe, not presumed canonical/native PASS. Hostile untrusted native decoder fuzzing/largeallocation failure tests not executed.
