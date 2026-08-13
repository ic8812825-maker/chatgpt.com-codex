# HSB.2C-R1-P1: traceability

- Runtime matrix → `HSBI_BuildRuntimePolicy`.
- Injected source → `HSBI_IsInjectedProofAllowed`, FutureSmall/NewFar guards.
- Static preflight → `HSBI_IsProductionPreflightAllowed`.
- Completion source → `HSBI_IsCompletionSourceAllowed` + complete reconciliation.
- Dispatch → `HSBI_IsBrokerDispatchAllowed` always false.
- Tests → T381–T400; complete declared range T01–T400.
- Publication → отдельный append-only correction record.
- MetaEditor/MT5 → `USER_VERIFICATION_REQUIRED`.
