# End-to-end mutation audit HSB.2D-V1-R1

Каталог содержит обязательные M001–M055. Каждая запись содержит target, точное изменение, тип, expected checks и manifest strategy. Mutation считается `CAUGHT` только при применённом target, отсутствии unexpected changes, nonzero exit, отсутствии crash, expected failure и S045 PASS для semantic mutation. Manifest-only, wrong failure, survived и not-applied — FAIL.

Self-tests MR001–MR010 проверяют missing target/replacement, лишние файлы, crash/survival, manifest-only, wrong check, cleanup и полноту/уникальность catalog. Фактические результаты находятся в machine-readable evidence.
