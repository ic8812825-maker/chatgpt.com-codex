# Двусторонний manifest audit HSB.2D-V1-R1

Expected file set вычисляется независимо: главный EA, harness, все `.mqh`, оба verifier entry points, runner/catalog, include graph, 7 status docs, handoff и все R1 reports кроме publication self-reference. Evidence outputs и сам manifest явно исключены как изменяемые/self-referential результаты запуска.

S045 проверяет expected-minus-manifest, manifest-minus-expected, duplicate paths, missing/external targets, format и SHA-256. M051–M055 реально меняют manifest и должны дать только целевой S045 FAIL.
