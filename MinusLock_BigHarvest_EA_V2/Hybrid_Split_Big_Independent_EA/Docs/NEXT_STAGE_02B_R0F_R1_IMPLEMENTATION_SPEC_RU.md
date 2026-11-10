# R0F — будущий R1.1: два точных scope

BASE_SHA=ad5ce78d74c53b34358cd7508982aa888976057a

PROPOSED / AWAITING_ADMIN_APPROVAL. CONTRACT-DECISION-PREPARATION / TEST-ONLY. Не разрешение production или торговли.


R1_1_START_ALLOWED=NO. В R0F production code/helpers не создаются. Единственный действующий allowlist сейчас — новые Docs/Reports/Tests.

Baseline inventory production references: HSBI_EconomicLedgerRecord/BuildSourceDealKey/SameEconomicRecord/ClassifyEconomicDuplicate/SerializeEconomicRecord найдены в Include только в самом EconomicLedgerTypes.mqh. Это статический scope argument, не MetaEditor/ABI/runtime доказательство.

## Minimal R1.1

Variant: Minimal R1.1
ProductionAllowlist: ["Include/Money/HSBI_EconomicLedgerTypes.mqh"]
DiffScope: Only inline schema/namespace helpers, immutable full-field equality/duplicate validation in existing header; no authoritative new persistence codec/backend. Legacy serializer remains explicitly diagnostic and cannot serve as new identity payload.
SingleFileFeasibility: STATICALLY_POSSIBLE_FOR_LOCAL_HEADER_ONLY; no active external production callsites found by textual inventory; native compile/integration not proved.
APICompatibility: New required fields break semantic compatibility of legacy records. Bool equality returns false for invalid input; new typed V2 validation/classification must expose REJECT/UNAVAILABLE. Preserve old facade only with explicit lossy-status/deprecation policy; no mapping unavailable→NEW/NO_OP. Administrator must approve facade policy.
NegativeTests: ["same Net changed Profit/Swap/Commission/Fee", "foreign namespace", "same deal changed Magic/Cycle not NEW funding", "unknown schema/currency/precision/origin", "malformed/nonfinite raw values", "exact replay zero delta", "legacy diagnostics cannot become proof"]
Acceptance: Fresh scoped native tests + per-field source mutations; one-file scope; no IO/provider lookup/credits/dispatch. Minimal does NOT claim stable restart serialization or full economic reconciliation.
ProductionImplementationAllowed: False
RequiredApprovals: ["D-08", "NUM-CODEC (scope-dependent)", "MQL-DOMAIN", "D-02 provider boundary", "new explicit baseline/allowlist task"]
Rollback: Separate reviewed revert of own future phase commit; preserve old/new bytes/schema; no reset/rebase/force, no compensating trades.
CompilePlan: Real MetaEditor main + new scoped MQL5 assertion harness; capture compiler version/log/exit. g++/Python not a substitute. NOT_RUN now.
Migration: No actual storage migration. Legacy without complete namespace/units/origin remains UNAVAILABLE; preserve original bytes/hash. No current ACCOUNT_LOGIN fallback.

## Extended R1.1

Variant: Extended R1.1
ProductionAllowlist: ["Include/Money/HSBI_EconomicLedgerTypes.mqh", "Include/Money/HSBI_EconomicSourceNamespace.mqh", "Include/Money/HSBI_EconomicCanonicalCodec.mqh", "Include/Money/HSBI_EconomicLegacyAdapter.mqh"]
DiffScope: Additional headers only after separate explicit approval. Namespace helper separates validation; codec helper raw serialization only; legacy adapter read-only typed mapping/quarantine only, no persistent migration.
SingleFileFeasibility: Extra headers are modularization/testability choices, not logically required; all could be inline but complexity/compile review grows. No new production headers created in R0F.
APICompatibility: Versioned V2 status/schema and codec envelope; no silent reinterpretation of four-field legacy string. Real provider caller integration requires a separate expanded allowlist if production callsites appear.
NegativeTests: ["all Minimal tests", "both codec golden vectors", "unknown profile/schema/type tags", "duplicate/trailing/oversized bytes", "utf8 length and delimiter collision", "source digest corruption", "legacy source missing account never auto-enriched"]
Acceptance: Selected approved codec + native UTF8/long/ulong/double/roundtrip golden tests; no money-domain substitution; no migration writes, backend or trading.
ProductionImplementationAllowed: False
RequiredApprovals: ["D-08", "NUM-CODEC (scope-dependent)", "MQL-DOMAIN", "D-02 provider boundary", "new explicit baseline/allowlist task"]
Rollback: Separate reviewed revert of own future phase commit; preserve old/new bytes/schema; no reset/rebase/force, no compensating trades.
CompilePlan: Real MetaEditor main + new scoped MQL5 assertion harness; capture compiler version/log/exit. g++/Python not a substitute. NOT_RUN now.
Migration: No actual storage migration. Legacy without complete namespace/units/origin remains UNAVAILABLE; preserve original bytes/hash. No current ACCOUNT_LOGIN fallback.

Minimal technically possible for local typed identity APIs in one existing header. It does not solve authoritative serialization, provider ingestion, account-wide funding, replay backend or actual migration. Existing int0/1/2 classifier cannot silently expose unavailable as NEW/NO_OP; typed V2 facade and legacy policy must be approved, otherwise scope remains blocked. Full source payload fields may make old callers/fixtures unavailable; no terminal defaults.

Extended headers are NOT mathematically required for one-file equality; each is optional modularization: namespace isolates broker/account validation; codec isolates raw wire format and golden vectors; legacy adapter performs read-only mapping/quarantine. Every additional production path needs explicit allowlist approval. Any future real provider caller modification needs its own scope expansion; no hidden include changes.

Forbidden both variants: other money/solver/geometry/runtime headers, main mq5, dispatch, OnTick/OnTradeTransaction trading, persistence backend, balance credits/consumption, automatic migration/corrections. Old HSB tests/evidence stay frozen; intentional schema incompatibility requires new scoped harness and classification, never editing old expectations to green.

Stop criteria: unapproved schema/API/codec/equivalence, missing namespace/units/origin, file outside allowlist, remote/baseline dirty mismatch, unexplained mutations/runtime errors, native compile unavailable for acceptance. Rollback only separate reviewed revert, preserve records/schema, no reset/rebase/force or compensating trades. Concrete future criteria in R1_ACCEPTANCE_MATRIX.json.
