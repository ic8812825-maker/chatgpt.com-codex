# 02B-R0E — errata provenance R0D

BASE_SHA=2d34c3378edc5f2df064282fa067bb4af2a1e3b0

Статус: PROPOSED / AWAITING_ADMIN_APPROVAL. Только audit/test-only; никаких production-изменений и торговли.

Исторические оригиналы не изменяются. Ошибка находится в Reports/NEXT_STAGE_02B_R0D_TEST_AND_MUTATION_RESULTS_RU.md:3 и Reports/NEXT_STAGE_02B_R0D_FINAL_VERDICT_RU.md:3.

WrongReportedR0DBase: ec7ae40fe22e1d6e5bed035450750502a1182ab5

CorrectHistoricalR0DBase: ec7ae40fe22e1d6e5bed035450750502a1162ab5

HistoricalR0DCommit: 2d34c3378edc5f2df064282fa067bb4af2a1e3b0

Этот commit является базой R0E; его parent — правильный HistoricalR0DBase. Проверено git rev-parse BASE^ и Git tree. R0D JSON evidence использует правильную базу; два Markdown поля ошибочны. Вывод о механизме ошибки (замена116→118 вместе со счётчиком сценариев) — вероятная причина, не восстановленный execution trace. Метаданные R0E и счётчики генерируются раздельно; blanket замена чисел не используется. Package probe report-baseline проверяет маркированное BASE_SHA, а не произвольное наличие любого исторического SHA в тексте.
