# Comment-aware audit R2

| Check | Функция | Active guard | Comment mutation | String mutation | Preprocessor mutation | Результат |
|---|---|---|---|---|---|---|
| S023 | DecisionValidator | immutable/policy | suite | lexer | lexer | PASS |
| S024 | RestartValidator | history/source/payload | M065 | lexer | lexer | PASS |
| S025 | TransactionBarrier | event/action/proofs | suite | lexer | M064 | PASS |
| S026–S027 | DecisionValidator | identity/ownership | M061 | lexer | lexer | PASS |
| S028 | DecisionValidator | revision mismatch reject | M056,M057,M060 | M058 | M059 | PASS |
| S029–S036 | DecisionValidator | event/schema/fresh/recon/residual/allocation | suite | lexer | lexer | PASS |
| S037–S038R | Decision/Restart | duplicate/persistence/snapshot | M062 | lexer | lexer | PASS |
| S039–S039D | Types/Decision | digest bindings/reject | suite | M063 | lexer | PASS |
