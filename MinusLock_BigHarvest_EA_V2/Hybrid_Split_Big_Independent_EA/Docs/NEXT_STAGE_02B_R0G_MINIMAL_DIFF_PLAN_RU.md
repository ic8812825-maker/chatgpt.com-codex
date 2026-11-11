# R0G — one-file diff и native acceptance plan

BASE_SHA=bcaa766568b9fe7eec0781a8c6efbb288cf16dae

PROPOSED / AWAITING_ADMIN_APPROVAL. Только подготовка Minimal R1.1; ни одного production изменения или утверждения.

Источники: `Include/Money/HSBI_EconomicLedgerTypes.mqh:6` struct, `:7` BuildSourceDealKey, `:8` ValidateEconomicRecord, `:9` SameEconomicRecord, `:10` ClassifyEconomicDuplicate, `:11` SerializeEconomicRecord, `:12` IsHarvestSourceEntry. R0F ECONOMIC_IDENTITY_SPEC/NUMERIC_CODEC_OPTIONS/R1_IMPLEMENTATION_SPEC; frozen `hsbi_02b_r0f_contract_candidate.py:record_shape/encode_record`; новые TestID в TEST_RESULTS.json.

Единственный future production path: `Include/Money/HSBI_EconomicLedgerTypes.mqh`. Текущий R0G не создаёт production structures/helpers. Статическая возможность one-file есть: все новые structs/enums/functions могут объявляться inline в этом header; нет production external calls найденных rg. Header-only plan не доказательство MetaEditor compatibility.

| Existing / new | Future diff |
|---|---|
| HSBI_EconomicLedgerRecord :6 | Сохранить старую struct/layout. Add separate HSBI_EconomicLedgerRecordV2 с29fields, не дописывать молча old serialized records |
| old Build/Validate/Same/Classify/Serialize :7–11 | Сохранить сигнатуры и диагностическую legacy семантику; пометка diagnostic-only в comments, no new proof callers |
| old IsHarvestSourceEntry :12 | Не менять source-role economics; diagnostic helper не funding gate |
| New namespace/validate/key/compare/classifier | V2 strict contracts/statuses; no epsilon, no implicit identity copies |
| New encode/decode helpers | Approved candidate F64Z inline; bounded lengths, finite double, unsigned/signed checks, buffers temp→output only on success |
| New view/envelope types | Independent authority/registry completeness and explicit unknown; no provider IO/backend/CAS |
| Legacy adapter if needed | Read-only explicit unavailable for missing fields, no invented enrichment; keep raw record bytes outside financial proof |

Добавляются SchemaVersion,Broker,Server,AccountLogin,DealType,TimestampMsc,Currency,Precision,SourcePlanApplicable/SourcePlan/SourcePolicyApplicable/SourcePolicyVersion в отдельный V2, исходные IDs/роль/volume/price/components/net переносятся только при independent validation. `valid=true`/sourceDealKey не authority. EA Role enum↔wire closed string mapping versioned explicit; unsupported role=>UNAVAILABLE or known invalid=>REJECT, no numeric guessing. Timestamp old datetime seconds не равен доказанным millis.

Минимальный patch не реализует двойной funding protection. Он исключает ложный NEW из codec/key/legacy classification в заявленном V2 gate. Существование глобального logical-source unique registry, CAS и funding integration остаётся UNPROVEN; не обещать их исправление одним header. Direct equality API не выдаёт NEW; future funding caller обязан вызывать registry-aware classifier + economic reconciliation + actual durable allocation authorization. В R1.1 никакие balance grants не создаются.

## NATIVE-ACCEPTANCE-1 (будущий отдельный этап)

1. Зафиксировать MetaEditor build, OS, command и compiler logs; production main mq5 compile в copied output workspace, source hashes неизменны кроме allowlisted header. Exit0+0errors обязательны; warnings описать. Не считать g++ equivalent.
2. Новый test-only MQL5 assertion script (после отдельного разрешения Tests path; без OnTick/dispatch): include EconomicLedgerTypes, initialize all explicit facts/views, no broker History/OrderSend.
3. long boundaries ±2^63/Magicnonzero; positive Account/Timestamp; ulong1..2^64-1 и overflow conversion отказ; bool не parse ID. Native DTO typed fields не позволяют некоторые Python bool-integer cases, но wire parser обязан отвергать wrong tags.
4. Все CODEC-GOLDEN vectors, +0/-0/subnormal/maxfinite, NaN/Infinityrejection, exact exponent/UTF8 byte lengths. Native endian, shifts, locale, NUL and Unicode surrogate handling. Unknown schema/codec=>UNAVAILABLE.
5. Source namespace variation, all29 per-field exact/altered comparisons; components50/0 vs60/-10 sameNet=>CONFLICT. Same key changed Magic/Cycle неNEW.
6. NEW только independent confirmed+complete registry absence; missing/legacy/source mismatch=>UNAVAILABLE, malformedREJECT. Empty or duplicate registry semantics verified.
7. Native encoder/decoder positive roundtrip плюс corrupted/truncated/duplicate/trailing/wrong tags/oversize tests (reference fixture decode сейчас не это доказательство). Output refs unchanged on errors.
8. Old struct/function signatures compile compatibility diagnostic-only; adapter never returns NEW for unknown legacy. Existing frozen test failures классифицировать, не переписывать.
9. Assertions pass counts and actual exit/platform/tester logs capture. Нативные assertion failures должны иметь machine-detectable failure status; terminal script stop сам по себе не PASS.
10. Diff onlyone production path; no new include headers/main/runtime edits. Hash/static scan no OrderSend/CTrade/OnTick trading/persistence. No real broker/tests on live account.

MetaEditor/MT5 не найдены в PATH и searched /opt,/workspace,/usr/local/bin; только historical Windows compile script вне scope. Native compile/tests/StrategyTester=NOT_RUN. Native tests — обязательный blocker будущей production приёмки; до отдельного задания не запускать платформу/сделки.

Stop: missing admin decision/baseline drift, malformed authority, required data missing, unknown codec, native mismatch/errors, need other production file, unexplained test failure, security rule bypass requirement. Не расширять allowlist скрыто. Rollback будущего phase commit отдельным reviewed revert; preserve old/new payload/schema. Не reset/rebase/force и не денежные compensation trades. Никаких actual storage migrations в Minimal.
