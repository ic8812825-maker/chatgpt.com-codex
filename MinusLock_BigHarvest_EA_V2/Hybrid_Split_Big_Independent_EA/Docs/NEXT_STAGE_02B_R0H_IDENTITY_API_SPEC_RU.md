BASE_SHA=7afad885a8ef8ff2c8189ca72760e06a1baaa50a

PROPOSED / AWAITING_ADMIN_APPROVAL. R0H TEST-ONLY. No production remediation, broker/account IO, funding, allocation or persistence.

Исходники: `Include/Money/HSBI_EconomicLedgerTypes.mqh:6` record, `:7` key, `:8` validate, `:9` equality, `:10` classifier, `:11` serializer, `:12` harvest helper. Production включает Core/Enums/Identifiers/ReasonCodes. R0G MINIMAL_IDENTITY_CONTRACT/MQL5_API_SPEC и F64Z/T17Z alternatives сохранены. Новая Python `hsbi_02b_r0h_identity_codec.py:source_key/equal_body/bits/unbits/encode/decode/classify`; MQL `hsbi_02b_r0h_native_codec.mqh:R0H_Validate/R0H_Key/R0H_Equal/R0H_Classify/R0H_Encode/R0H_Decode`, entry `hsbi_02b_r0h_native_harness.mq5:OnStart`. Новые goldens generated только independent fixture struct.pack/literal, не subject encoder.

# R0H-ID/STATUS: source observations vs funding

SourceKey=(Broker,Server,AccountLogin,DealTicket). Altered Magic/Cycle/Symbol/Role/components при прежнем source не новый source. Все29 fields R0G retained, exact comparison (Z zero equivalence), no epsilon/Net-only. Schema/type validation mandatory before key/index. SameNet50 Profit50/Commission0 vsProfit60/Commission-10 =>CONFLICT, even coherent presented+authority mutation blocked against unchanged independent registry.

Broker namespace требует stable independently configured binding, не company display name; Server/Account from independently verified account context/history-provider envelope; deal existence/ownership проверяются не по nonzero ticket. Broker DEAL_* не даёт HSBI Cycle/Action/Event/Role/SourcePlan/Policy, требуется independent EA-origin journal. Ни Python, ни MQL fixture не создают такого provider.

NEW_SOURCE_OBSERVATION = подтверждённый body + complete reconciled registry absence; не ELIGIBLE_FUNDING_SOURCE. Funding needs actual posted reconciliation/role/policy/conservation/globaluniqueledger/durableCAS, none implemented. Same supported exact body known source=>NO_OP; immutable mismatch=>CONFLICT; malformed=>REJECT; unknown facts/schema/history/codec/legacy=>UNAVAILABLE. No UNAVAILABLE→NEW or CONFLICT→NO_OP. Unknown namespace facts represented providerComplete=false =>UNAVAILABLE; malformed missing fields/type/emptyknown string are REJECT, не тот же случай.

Priority in classify: shape incoming -> codec -> authority/registry DTO/completeness -> shape authority -> independent source key -> body conflict -> all registry rows/uniqueness -> NEW/NO_OP/CONFLICT. Direct equal_body/key are local helpers with mandatory classify validation; helpers do not return eligibility. Replay is comparison only, not durable journal exactly-once. Errors have no input mutations (deep-copy before/after reference tests); native output preservation assertions prepared, NOT_RUN.

Legacy facade returns UNAVAILABLE for diagnostic string, never converts 0 to NEW. Old production functions unchanged and remain unsafe as funding authority; label diagnostic-only is proposal, not enforced remediation. Native test API supports fixed typed29 body + explicit completeness, uses schema/codec statuses; cannot encode unknown record as fabricated knownzero. Native test functions have no state, no allocate/consume/persist, no broker lookups. All five status semantics require separate admin decision and native acceptance.
