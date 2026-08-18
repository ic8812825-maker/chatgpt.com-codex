# Runtime contract audit HSB.2D-V1-R1

| Contract | Guard | Return status | Reason code | Positive check | Mutations | Result |
|---|---|---|---|---|---|---|
| immutable | immutable + policy | REJECTED | CONTEXT_INVALID | S023 | M005 | PROVED |
| identity | account/symbol/magic/cycle/plan | REJECTED | IDENTITY_MISMATCH | S026 | M006–M010 | PROVED |
| revision | mismatch | CONFLICT | STATE_REVISION_MISMATCH | S028 | M001–M005 | PROVED |
| schema | schema constant | REJECTED | SCHEMA_VERSION_MISMATCH | S031 | structural proof | PROVED |
| money version | version constant | REJECTED | MONEY_STATE_VERSION_MISMATCH | S032 | structural proof | PROVED |
| freshness | market/cost/policy | STALE | STALE_SNAPSHOT | S033 | structural proof | PROVED |
| reconciliation | conflict/confirmed | CONFLICT/REQUIRED | RECON reasons | S034 | structural proof | PROVED |
| actual residual | actual + matcher | REJECTED | ACTUAL_RESIDUAL_REQUIRED | S035 | M009–M010 | PROVED |
| Future Small | complete runtime aggregate | UNAVAILABLE | FUTURE_SMALL_INCOMPLETE | S023 | catalog structural baseline | PROVED |
| New Far binding | identifier/ticket | REJECTED | NEW_FAR_INVALID | S027 | M009–M010 | PROVED |
| Catch-Up | runtime/source identities | UNAVAILABLE | CATCH_UP_INVALID | S023 | catalog structural baseline | PROVED |
| money/margin | runtime proof | UNAVAILABLE | MONEY_UNAVAILABLE | S025 | M024 | PROVED |
| risk | runtime proof identity | UNAVAILABLE | RISK_UNAVAILABLE | S023 | catalog structural baseline | PROVED |
| allocation | policy + source validator | CONFLICT | ALLOCATION_CONFLICT | S036 | structural proof | PROVED |
| consumption | key binding/conflict | CONFLICT | CONSUMPTION_CONFLICT | S037 | M027–M028 | PROVED |
| persistence | prepared/snapshot/pending | PERSISTENCE_REQUIRED | PERSISTENCE_REQUIRED | S038/S038R | M011–M015,M026,M032 | PROVED |
| digest | empty/mismatch + bound fields | CONFLICT | DIGEST_MISMATCH | S039/S039D | M016–M020 | PROVED |
| restart | history/residual | CONFLICT | DOUBLE_COUNT/POSITION | S024 | M027–M032 | PROVED |
| transaction barrier | event/action/proofs | reject/conflict/unavailable | specific reasons | S025 | M021–M026 | PROVED |
| duplicate/replay | completed ID/payload | NO_OP | OK | S025/S037 | M023,M027 | PROVED |
| conflict | differing payload/source | CONFLICT | PENDING/DOUBLE_COUNT | S024/S025 | M023,M028 | PROVED |
| NO_OP | identical completed payload | NO_OP | OK | S025 | M023 | PROVED |
