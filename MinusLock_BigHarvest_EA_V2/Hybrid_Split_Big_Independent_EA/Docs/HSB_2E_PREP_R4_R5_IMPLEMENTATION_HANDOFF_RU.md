# HSB.2E PREP-R4-R5 — provenance-backed implementation handoff

Это только offline-спецификация. `TRADING_LOGIC_START_ALLOWED=NO`; production `.mq5/.mqh` не изменяются.

## Усиления существующих контрактов

| CHANGE_ID | OLD_BEHAVIOR | NEW_BEHAVIOR | WHY_REQUIRED | EQUIVALENCE_OR_STRENGTHENING_PROOF | REGRESSION_VECTOR_IDS | INVARIANT_IDS | MUTATION_IDS |
|---|---|---|---|---|---|---|---|
| R5-C01 | aggregate cache мог быть source of truth | cache пересчитывается из sealed deal records | исключить forged volume/money | все R4 primitive/identity predicates сохранены, provenance только усиливает admission | все R4-R2/R3/R4 vectors | PERSISTED_VOLUME_PROVENANCE; PERSISTED_MONEY_PROVENANCE | R5M004-R5M007 |
| R5-C02 | bare price Boolean | immutable bound-and-identity proof | связать actual deal с snapshot policy | exact historical side остаётся частным случаем structured proof | price/direction vectors | EXECUTION_PRICE_PROOF | R5M001-R5M003 |
| R5-C03 | committed Boolean | sealed commit certificate | доказать settlement и revision | idempotent replay сохранён после проверки certificate | restart vectors | COMMIT_CERTIFICATE; STATE_REVISION | R5M008-R5M010 |
| R5-C04 | apply during validation | VALIDATE_ALL_THEN_APPLY | atomic mixed batch | single valid batch semantics эквивалентна R4 | batch/lifecycle vectors | BATCH_ATOMICITY | R5M011-R5M012 |
| R5-C05 | Initial/Final допускали unsafe gates | InitialNet>0; Final FULL_CLOSE only | торговая безопасность | только сужение множества ранее небезопасных PASS | Initial/Final vectors | INITIAL_NET_PROFIT; FINAL_FULL_CLOSE | R5M013-R5M015 |

## Future owners

R5 reference contracts соответствуют будущим IMPL-01…IMPL-17, но не создают production owners. Broker contour выдаёт только sealed proposal; economic contour не принимает raw deals. Следующий этап требует отдельного административного решения.
