# C2 — clauses, композиция и scope recovery

BASE_SHA=fae7dfc18ca2d61af2f3446826ef3031825bbfd8

PROPOSED / AWAITING_ADMIN_APPROVAL. Только audit/test-only; production и trading запрещены.

Матрица: Tests/Contracts/NEXT_STAGE_02B_R0E_C2_VERIFICATION_MATRIX.json. GuardID/ClauseID связывает exact source edit с positive/negative TestID; фактические вызовы сохраняются в SubjectCalls. Семантически независимые receipt clauses (nonnegative risk, principal binding, required sum, core debit), purpose/intent и immutable allocation event/policy проверены отдельно. Денежные ожидания literal/independent integer coefficient-scale encoder R0D; subject evaluator не вычисляет expected.

Обязательные public callers: apply_for_test→authorize→_authorize→schema Request/Store/Authority→economic_record→_reconcile_store→_bind_allocation→verify_allocation_identity→assess_batch/cost_coverage→available→checked delta. available/recover_store вызывают _reconcile_store самостоятельно. Pure assess_batch/cost_coverage/identity проверяют свои DTO напрямую. Private helpers не являются authorization API и Python privacy не security sandbox.

| Property | VerifiedByRecovery | RequiredAuthority | UnverifiedDependency | ReturnedScope | PermittedDownstreamUse |
|---|---|---|---|---|---|
| Accounting reconstruction | Да, exact journal replay/balance | Independent coreJournal/history | Durable bytes authenticity | RECONCILED_MODEL_ONLY | Accounting fixture result |
| Immutable receipt bindings | Да, digest/source/allocation/event/context/equations | Independent receipt journal | Authenticity historical provider | RECONCILED_MODEL_ONLY | Binding comparison |
| Historical source reconciliation | Да, immutable economic digest | Independent economic history | Broker authenticity/completeness | RECONCILED_MODEL_ONLY | Fixture reconciliation |
| Historical batch membership | Полностью не повторяется | Historical batch provider record | Сохранённый digest не доказывает provider fact | UNPROVEN | Не historical full proof |
| Historical cost coverage | Полностью не повторяется | Historical cost policy/provider | Trusted receipt boundary | UNPROVEN | Не historical full proof |
| Historical available headroom | Полностью не повторяется | As-at-commit eligibility facts | Полный historical authorization | UNPROVEN | Не разрешение нового расхода |
| Durable authenticity | Нет | Durable backend/receipts | Backend отсутствует | UNPROVEN | Нельзя заявлять durable commit |
| Concurrent ordering | Нет | CAS/locks/transaction ordering | Concurrent backend отсутствует | UNPROVEN | Нельзя заявлять concurrent exactly-once |

Пример C2-recovery-scope: reconstructed debit50 может соответствовать receipt required50.5 при исходных50. Recovery лишь RECONCILED_MODEL_ONLY; новая authorization50+.5 отклоняется. Это не доказательство double spend. Новый расход всегда повторяет текущую полную authorize; recovered store не eligibility token.

AdditionalRisk остаётся headroom, не actual debit:50/10/.5→required10.5/free40/consumed10. G=C+Reserved+Free; семантика RemainingGross/RemainingFree и R0D numeric domain не меняются. Нет глобального account-economic funding proof. Fixture completeness не broker evidence.

Redundant guards сохраняются как survivors: отдельный CostSet schema caller дублируется обязательным CostClaim validator на причинном bool-input; dual-caller mutation отдельно обнаруживается. Прежние outer post-state/format/self-repair clauses также могут быть защищены ранним C2 schema/reconstruction. Доказательство caller и whole-domain regression хранится в MUTATION_RESULTS; исключение не считается kill.
