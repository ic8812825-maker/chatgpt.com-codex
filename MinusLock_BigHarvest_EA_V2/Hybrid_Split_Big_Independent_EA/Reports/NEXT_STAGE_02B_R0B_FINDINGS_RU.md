# 02B-R0B — выявленные факты и границы

База `9b43c38afdb89c6b3b514b654c7fb9a936f9bf2b`, ветка work. Audit/test-only. Production-код не изменён, исторические records/evidence не переписаны. Все решения ждут администратора.

## Подтверждённое

1. Исходная база совпала local/remote, clean; R0A commit имеет ровно 15 новых файлов, production additions/changes отсутствуют. Старые hashes сохранены.
2. Unchanged R0/R0A suites воспроизведены: R0 native81/reference58/probes13/mismatches46/exit1; R0A128 PASS/exit0. Это не native MQL5 acceptance.
3. Frozen128 пропускали восемь специально ослабленных guard вариантов: account namespace, allocation identity, bucket vector, precision, sum grants, confirmed source, snapshot freshness, role. После новых причинных tests все восемь пойманы без изменения старых tests/model.
4. R0A authorize/apply boundary не представляет/проверяет Symbol/Magic/Deal/Order/Position/Snapshot. Unknown extra field может игнорироваться и дать COMMITTED_IN_MEMORY. Это не доказательство обхода полного verify_proof pipeline: обязательность coupling и реальный provider остаются UNPROVEN.
5. R0 legacy oracle отдельно принимает Plan999/Revision999; R0A и новый oracle отвергают их. Старый oracle не изменён.
6. R0A reconciled_net default USD2/HALF_EVEN не знает broker-posted amount. Синтетическое raw1.005 →1.00 при отдельно заданном posted1.01 демонстрирует предел API. Нельзя переносить это как универсальный broker law.
7. Snapshot/role negatives исходного R0A были маскированы другим guard: изменялся digest либо оставалась чужая identity. Новый coherent negative действительно изолирует нужный запрет.
8. Zero Core ниже Vmin, max-volume и slope — разные ограничения. Core>=Vmin не достаточен; неизвестный min/step grid требует UNPROVEN, а не молчаливой нормализации.
9. CR-09 A/B неэквивалентны; sequential source50 нельзя потратить30+30. Missing trajectory data →UNPROVEN.

## Сохраняющиеся production defects

M-01 foreign consumption/source binding и incomplete history; M-02 self-copy expected identity; L-01 неполный immutable record comparator; L-02 total-only allocation duplicate; Account namespace отсутствует; M-05 reserve metric включает Small; zero-Core locally accepted. Ничто из этого здесь не исправлено. CR-09 остаётся нормативным выбором, а не автоматически принятой сменой policy.

## Математика и неподтверждённые зависимости

Per-source G=R+C и A=R-V непротиворечивы; positive/zero/negative source, partial/committed grants, residual, full/partial consumption и replay проверены. При source debit grant не создаётся; Consumed никогда не используется как новый ресурс. Но aggregate money после неатрибутированных losses, own-reservation settlement и account solvency требуют отдельной reconciliation. Нельзя получить их из 141 passing fixtures.

Внешняя broker authenticity/precision/margin, durable journal/CAS/restart/concurrency, реальные partial fills, обязательность complete caller chain, полный NewFar и экономическая конечность recovery — NOT_RUN/UNPROVEN. Source DTO validity/positive P&L/ненулевые IDs не заменяют эти доказательства.

## Ответственность слоёв

allocate/valid_balance — mathematical primitives, поэтому отсутствие history/currency в локальном API не объявлено само по себе production дефектом. Исправляется доказательство обязательной authority границы, а не произвольное добавление flags. New oracle проверяет proposed coupled boundary на independently assembled fixtures; он не является trusted broker provider.

Точные SourceFile/Function/Line и все 19 измерений evidence: [verification matrix](../Tests/Contracts/NEXT_STAGE_02B_R0B_VERIFICATION_MATRIX.json). CurrentStatus не повышает NOT_RUN/UNPROVEN до PASS. PASS source formula/no-trade относится только к указанному локальному scope.
