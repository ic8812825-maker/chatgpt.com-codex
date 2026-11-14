# AUDIT03 CLOSE — preservation

BASE_SHA=398da88424f3fb7b30e5315fbc3bf89219dd9ad2. Snapshot UTC=2026-11-14T18:46:14.531075+00:00. `1529` исходных файлов проверены SHA256 + Git blob + mode; production sources=74. AllBaselineBytesModesBlobsUnchanged=True; issues=[].

Все существовавшие Reports/Docs/Tests, frozen fixtures и baseline результаты сохранены побайтно. Следовательно исторические ERR/IMP IDs, FAIL и expected в них не удалены и не подменены. Новые результаты находятся только в Reports/HSBI_AUDIT03_CLOSE_*, Reports/HSBI_MONEY_CONTRACT_*, Reports/HSBI_R11_P0_* и Tests/Close/. Новые metadata reading статусы не переписывают старый reading ledger.

`baseline.json` создан до новых production/test изменений; `inventory.csv` фиксирует все1529 paths, hashes, size/lines, роли и coverage. `verify_preservation.py` сравнивает каждый baseline файл, проверяет Git diff/untracked paths и отклоняет чужие изменения. `preservation_results.json` — машинное evidence. Повторная проверка выполняется после подготовки полного index и после commit; фактический publication outcome сообщается отдельно в финальном ответе, чтобы не подменять prepublication snapshot.

Не изменены production, historical evidence, old fixtures/expectations, normative sources или торговая логика. Никакие patches не применялись, broker команды не отправлялись. Нет force push/reset/merge. Создаются только новые audit/test-only files. Git clone/fetch и objects/index metadata не являются изменением файлов проекта.
