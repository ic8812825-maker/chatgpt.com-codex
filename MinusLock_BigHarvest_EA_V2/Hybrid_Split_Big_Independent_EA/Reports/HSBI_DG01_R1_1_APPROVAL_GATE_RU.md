# DG01 — gate Minimal R1.1

CONTRACT_PREPARATION=READY_FOR_ADMIN_DECISION
NATIVE_AXIS=PARTIAL_NATIVE_PENDING
ADMIN_APPROVAL_COMPLETE=NO
R1_1_START_ALLOWED=NO
PRODUCTION_REMEDIATION_ALLOWED=NO

## Четыре ответа

1. До первого локального identity изменения нужны explicit owner choices D-02/D-08, immutable schema/namespace, typed statuses, captured numeric domain и legacy compatibility. Codec approval нужен для production serialization. Остальные16 вопросов рассмотрены, но не все прямо блокируют pure equality. D-05 A/B/C не выбран.
2. FSA-002/005/006/007/008 допускают локальные guards после уточнения domain/phase и проверки callers. FSA-001 требует новой record schema. FSA-003 имеет local binding fix, но полная safety зависит от provider/journal. FSA-004 требует global source registry и durable/atomic enforcement. FSA-009 затрагивает context/invariants/roles/diagnostics. FSA-010 требует независимого provider и end-to-end caller, не только equality.
3. ONE_FILE_LOCAL_API_FEASIBLE — условно да: точный additive diff подготовлен. ONE_FILE_COMPLETE_REMEDIATION_NOT_FEASIBLE — также да: старый classifier и внешние authority/callers не исправлены. Нет утверждения о native compilability без MetaEditor.
4. Нужны MetaEditor strict compile, full29 immutable/namespace/status tests, native integer/double/UTF8/codec goldens, zero delta, actual source hashes и separate runtime logs. Сейчас NOT_RUN.

## Что считается допуском

Только отдельное явное owner approval конкретного baseline, allowlist, schema/status/domain/compatibility и отдельное implementation task. Готовый ballot или reference PASS не являются допуском. Готовый native harness не является работающим EA. Необходимо сохранить старые failures и current no-trade policy.
