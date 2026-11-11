# R1_1_MINIMAL_APPROVAL_BALLOT

BASE_SHA=bcaa766568b9fe7eec0781a8c6efbb288cf16dae

PROPOSED / AWAITING_ADMIN_APPROVAL. Только подготовка Minimal R1.1; ни одного production изменения или утверждения.

ProductionBaseline: bcaa766568b9fe7eec0781a8c6efbb288cf16dae
ProductionAllowlist: Include/Money/HSBI_EconomicLedgerTypes.mqh
IdentitySchemaCandidate: HSBI-EA-ECON-1 (все29 fields, explicit origin applicability)
StatusApiCandidate: HSBI-ECON-CLASSIFY-2 (NEW/NO_OP/CONFLICT/REJECT/UNAVAILABLE)
CodecCandidate: HSBI-F64Z-1
AlternativeCodec: HSBI-T17Z-1
CompatibilityCandidate: additive V2; legacy diagnostic-only; no implicit adapters
NumericAssumptions: positive signed Account/Timestamp; signed nonzero Magic; ulong IDs; finite binary64/Z-zero; known currency/precision; UTF8 native caps4096/65536 bytes proposed
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:
AdministratorName:
DecisionTimestamp:

**Формулировка для администратора:** «Рассматриваю HSBI-EA-ECON-1, V2 status API, F64Z candidate и additive diagnostic legacy policy в пределах указанного одного header. Даже при выборе APPROVE_MINIMAL_R1_1 необходимы отдельное явное implementation задание, актуальный baseline gate и успешная native приёмка. Это не разрешение на funding, trading, runtime/persistence/provider integration». Администратор может выбрать альтернативный T17Z только явным изменением ballot candidate/версии и native acceptance требований, не молчаливой подстановкой.

Варианты ответа (ни один не выбран): APPROVE_MINIMAL_R1_1 / REJECT_MINIMAL_R1_1 / RETURN_FOR_REVISION.

KnownLimitations: broker/source-origin authenticity UNPROVEN; full semantic reconciliation/native codec implementation NOT_RUN; source-level/global funding/CAS/durable restart/NewFar not implemented. No flag becomes provider evidence. Full account nontrade/manual events вне EA-attributed profile.

DeferredDependencies: D01/03/04/05/06/07/CR09/funding/balance mapping не утверждаются этим ballot. Узкие NUM-EXACT/DOMAIN assertions нужны, не вся money architecture. Detailed reasons — approval matrix и blocker analysis.

NativeRequirements: main mq5 compile и scoped assertion harness, golden vectors/hostile decode/field mutations/backward compatibility/no trade (NATIVE-ACCEPTANCE-1).
Rollback: separate reviewed revert of own future R1.1 phase, preserve observations, no migration writes/reset/force/compensation trades.
StopConditions: unapproved schema/status/codec/compatibility; missing data; different baseline; native test unavailable for acceptance; out-of-allowlist change; conflicting evidence/security publication refusal.

ADMIN_APPROVAL_COMPLETE=NO
R1_1_START_ALLOWED=NO
PRODUCTION_REMEDIATION_ALLOWED=NO
TRADING_LOGIC_START_ALLOWED=NO
BROKER_DISPATCH_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
