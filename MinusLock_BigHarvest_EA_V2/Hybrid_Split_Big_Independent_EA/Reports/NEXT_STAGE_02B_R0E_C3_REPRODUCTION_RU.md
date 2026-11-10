# C3 — воспроизведение C2 и provenance

BASE_SHA=3737116bff6e2275d674b3dd7b816de93715f27c

AUDIT / PROPOSED / AWAITING_ADMIN_APPROVAL. Production, trading и dispatch запрещены.

C2 reference: {'Comparisons': 9914, 'Executions': 1264, 'Fail': 0, 'InfrastructureErrors': 0, 'Pass': 1264, 'Scenarios': 158, 'SchemaProbes': 2462}. Mutation: {'CatalogSize': 70, 'InfrastructureErrors': 0, 'Killed': 64, 'RedundantSurvivors': 6, 'UnexplainedSurvivors': 0}. Package: {'NegativeFailed': 0, 'NegativePassed': 58, 'Positive': 'PASS'}. Источник — новые C3_C2_REFERENCE/MUTATIONS/PACKAGE JSON, не копирование старых summary.

Сценарии158 — TestID inventory; contexts8 — повторные исполнения, а не независимые доказательства. Full Context0 call-argument duplicate groups: []. Отсутствие точных совпадений captured-call lists не доказывает независимость всех assertions: fixtures/source50 и часть predicates повторяются. 2462 schema probes — отдельные path edits, не2462 экономические модели. Comparisons9914=2*1264+3*2462 — bookkeeping, не полнота свойств.

Фактические CLI, UTC, OS exit/stdout/stderr — EXECUTIONS.json; commands и stdout/stderr legacy jobs — REGRESSIONS.json. Role execution внутри reproduction одного процесса явно помечен; source/fixture hashes — common pins и BASELINE. Native subset source и compiler stdout/stderr сохранены отдельно. Archived package adapter меняет только root/default/path-relative bookkeeping; его точный код — C3 reproduction runner. Historical bytes и modes не менялись.

Development failures: initial leading-dot integer parser и duplicated timestamp wrapper, затем исправление role Command metadata и C3 regression metadata adapter. Контролируемое прерывание адаптера, остаточная disposable копия R10 и временный R7 S009146/73 зафиксированы отдельно; удалён только session-created untracked каталог, затем выполнен чистый повтор без изменения frozen expectations. Native fixtures усилены фактическими production shape/conservation validators. Они сохранены в DEVELOPMENT.json и исходных log, не превращены в semantic PASS. Все actual final results проверяются package verifier C3.
