BASE_SHA=7afad885a8ef8ff2c8189ca72760e06a1baaa50a

PROPOSED / AWAITING_ADMIN_APPROVAL. R0H TEST-ONLY. No production remediation, broker/account IO, funding, allocation or persistence.

Исходники: `Include/Money/HSBI_EconomicLedgerTypes.mqh:6` record, `:7` key, `:8` validate, `:9` equality, `:10` classifier, `:11` serializer, `:12` harvest helper. Production включает Core/Enums/Identifiers/ReasonCodes. R0G MINIMAL_IDENTITY_CONTRACT/MQL5_API_SPEC и F64Z/T17Z alternatives сохранены. Новая Python `hsbi_02b_r0h_identity_codec.py:source_key/equal_body/bits/unbits/encode/decode/classify`; MQL `hsbi_02b_r0h_native_codec.mqh:R0H_Validate/R0H_Key/R0H_Equal/R0H_Classify/R0H_Encode/R0H_Decode`, entry `hsbi_02b_r0h_native_harness.mq5:OnStart`. Новые goldens generated только independent fixture struct.pack/literal, не subject encoder.

# Independent mutation scope

14 Python source mutations; isolated exec of exact edited source, hashes and edits stored, no existing source writes. Each mutation positive/original negative/mutant negative expected independent fixture/literal. Parser/import/runtime exceptions are INFRASTRUCTURE_ERROR, not kill. Changed input objects checked for pure classify. No monetary state exists to prove balances/funding/durable behavior.

Ignore Broker/Account/Deal key mutations produce conservative CONFLICT instead of expected NEW for independently confirmed different logical source. These are STATUS_CONTRACT_KILL, not unsafe funding acceptance. Float endian/UTF8/zero similarly codec contract kills. Component/Magic/Cycle omission and conflict/unavailable weakening are UNSAFE_ACCEPTANCE_KILL in identity classification only; not actual economic spending.

| Mutation | CausalTest | Outcome |
|---|---|---|
|OMIT-Profit|ID-COHERENT-Profit|UNSAFE_ACCEPTANCE_KILL|
|OMIT-Commission|ID-COHERENT-Commission|UNSAFE_ACCEPTANCE_KILL|
|OMIT-Swap|ID-COHERENT-Swap|UNSAFE_ACCEPTANCE_KILL|
|OMIT-Fee|ID-COHERENT-Fee|UNSAFE_ACCEPTANCE_KILL|
|OMIT-Magic|ID-COHERENT-Magic|UNSAFE_ACCEPTANCE_KILL|
|OMIT-CycleID|ID-COHERENT-CycleID|UNSAFE_ACCEPTANCE_KILL|
|IGNORE-Broker|ID-COHERENT-Broker|STATUS_CONTRACT_KILL|
|IGNORE-AccountLogin|ID-COHERENT-AccountLogin|STATUS_CONTRACT_KILL|
|IGNORE-DealTicket|ID-COHERENT-DealTicket|STATUS_CONTRACT_KILL|
|CONFLICT-TO-NOOP|ID-COHERENT-Profit|UNSAFE_ACCEPTANCE_KILL|
|UNAVAILABLE-TO-NEW|ID-UNKNOWN-HISTORY|UNSAFE_ACCEPTANCE_KILL|
|BYTE-ORDER|CODEC-B-FULL|STATUS_CONTRACT_KILL|
|UTF8-LENGTH|UTF8-cyrillic|STATUS_CONTRACT_KILL|
|ZERO-POLICY|BITS-negative-zero|STATUS_CONTRACT_KILL|

14 killed,0survived,0infrastructure in finalcatalog (counts in evidence); this is not full mutation coverage and not native mutation verification. Native mutants NOT_RUN. All initial runs observed successful; no hidden development failures claimed. Acceptance matrix links guard/test/mutation/scope. Future native suite must rerun samesemantic probes on compiled MQL code; Python source kill does not prove native caller integration.
