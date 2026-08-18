# Архитектура verifier HSB.2D-V1-R1

Канонический entry point принимает `--root`, `--baseline-sha`, `--output-json`, `--output-text`, `--fixture-mode`. Wrapper старого имени только передаёт управление единственной реализации. Fixture mode отключает исключительно Git publication check и явно печатает `NOT_APPLICABLE_FIXTURE_MODE`; include, IDs, no-trade, status, manifest и structural guards остаются активны.

S023–S039 используют консервативные exact branch proofs и forbidden neutralizers. Неоднозначная/изменённая структура даёт `unable_to_prove` и FAIL. S028 проверяет operands, mismatch operator, conflict status/reason, отсутствие `false &&`, `true ||`, инверсии и early valid return.

Mutation runner для каждого catalog item создаёт отдельный `TemporaryDirectory`, меняет реальный файл, rehash только target для semantic mutations, запускает тот же verifier subprocess, сверяет expected Check ID, S045 PASS, changed file set, exit и crash state. Stdout/stderr хэшируются; production hashes сравниваются до/после.
