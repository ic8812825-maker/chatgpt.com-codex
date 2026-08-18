# Traceability HSB.2D-V1-R1

| Requirement | Production contract | Verifier check | Positive evidence | Mutations | Expected failure | Status |
|---|---|---|---|---|---|---|
| R1-REVISION | mismatch blocked | S028 | exact branch/status/reason | M001–M005 | S028 | PROVED_BY_E2E_MUTATION |
| R1-OWNERSHIP | actual owner/position | S027 | matcher + gate | M006–M010 | S027 | PROVED_BY_E2E_MUTATION |
| R1-PERSIST | prepared/snapshot/pending | S038/S038R | three guards | M011–M015,M026,M032 | S038/S038R | PROVED_BY_E2E_MUTATION |
| R1-DIGEST | empty/mismatch/bindings | S039/S039D | digest branch and fields | M016–M020 | S039/S039D | PROVED_BY_E2E_MUTATION |
| R1-BARRIER | event/action/proofs | S025 | exact guards | M021–M026 | S025 | PROVED_BY_E2E_MUTATION |
| R1-RESTART | history/residual | S024 | exact persisted comparison | M027–M032 | S024 | PROVED_BY_E2E_MUTATION |
| R1-NO-TRADE | disabled stub/no calls | S016/S017 | source scan | M033–M038 | S016/S017 | PROVED_BY_E2E_MUTATION |
| R1-STATUS | honest canonical state | S040/S044 | 7 status docs | M039–M044 | S040/S044 | PROVED_BY_E2E_MUTATION |
| R1-STRUCTURE | tests/includes/guards | S005–S013 | parsed graph/IDs | M045–M050 | target check | PROVED_BY_E2E_MUTATION |
| R1-MANIFEST | bidirectional complete/hash | S045 | independent expected set | M051–M055 | S045 | PROVED_BY_E2E_MUTATION |
