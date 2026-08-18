# Traceability R2

| Requirement | Implementation | Positive proof | Mutation | Check | Evidence | Status |
|---|---|---|---|---|---|---|
| HSBI-2D-V1-R2-BASELINE | fresh clone | Git parity | — | Git | reopening | PASS |
| HSBI-2D-V1-R2-SCOPE | Git diff prefix | clean audit | — | S048 | clean | PASS |
| HSBI-2D-V1-R2-LEXER | hsb_mql5_lexer.py | L001–L010 | meta fixtures | SLEX10 | clean | PASS |
| HSBI-2D-V1-R2-COMMENTS | ACTIVE_CODE | token proof | M056,M057,M060–M062,M065 | S027/S028/S038/S024 | mutation JSON | PASS |
| HSBI-2D-V1-R2-STRINGS | literals excluded | lexer tests | M058,M063 | S028/S039D | mutation JSON | PASS |
| HSBI-2D-V1-R2-PREPROCESSOR | conditional stack | lexer tests | M059,M064 | S028/S025 | mutation JSON | PASS |
| HSBI-2D-V1-R2-REVISION | active mismatch return | S028/S028B | M001–M005,M056–M060 | S028 | mutation JSON | PASS |
| HSBI-2D-V1-R2-OWNERSHIP | active ownership | S027 | M006–M010,M061 | S027 | mutation JSON | PASS |
| HSBI-2D-V1-R2-PERSISTENCE | active gates | S038/S038R | M011–M015,M062 | target | mutation JSON | PASS |
| HSBI-2D-V1-R2-DIGEST | active digest | S039/S039D | M016–M020,M063 | target | mutation JSON | PASS |
| HSBI-2D-V1-R2-RESTART | active restart guards | S024 | M027–M032,M065 | S024 | mutation JSON | PASS |
| HSBI-2D-V1-R2-BARRIER | active barrier | S025 | M021–M026,M064 | S025 | mutation JSON | PASS |
| HSBI-2D-V1-R2-STATUS-7 | canonical parser | S040A–S044E | M066–M100 | target | mutation JSON | PASS |
| HSBI-2D-V1-R2-EVIDENCE | SHA seal | S046E | M101–M103 | S046E | seal | PASS |
| HSBI-2D-V1-R2-NO-TRADE | source scan | S016–S022 | M033–M038 | target | mutation JSON | PASS |
| HSBI-2D-V1-R2-MUTATIONS | runner | 103 catalog | M001–M103 | expected | evidence | PASS |
| HSBI-2D-V1-R2-PUBLICATION | fast-forward | SHA parity | — | Git | publication | PENDING |
