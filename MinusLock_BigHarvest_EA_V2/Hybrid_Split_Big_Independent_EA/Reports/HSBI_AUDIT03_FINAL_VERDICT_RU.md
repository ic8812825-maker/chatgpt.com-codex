# AUDIT03 — независимый итоговый вердикт

**Полная корректность HSBI, сохранение денег во всей production-системе, завершение recovery, ограниченность убытка и прибыльность не доказаны. `AUDIT_COMPLETENESS=PARTIAL`.** Подготовленные отчёты не означают разрешение R1.1 или торговли.

База `6231bfbe94d39fbbb469b90a93e01426a83756bb`, ветка work. UTC фиксации текста: 2026-11-13T09:38:36.331321+00:00. Главный мануал прочитан1–51 полностью; все34 основные нумерованные Docs прочитаны, всего51 из136 потенциально нормативных/исторических/proposed Docs прочитаны полностью.85 дополнительных/частичных документов и часть source headers требуют продолжения, с точной картой в DOCUMENT_COVERAGE. Нельзя объявлять полный каталог всех возможных нормативных формул по нынешним60 семействам.

## Основные находки

- Три противоречия нормативного описания: зеркальный price step, optional Trend и порядок выбора N. Они не являются автоматически доказанными broker/runtime ошибками.
- 16 статических source defects описаны с выражениями/строками и ручными причинными примерами. Current OnTick не подключает полный финансовый lifecycle. Полный NewFar bypass не доказан.
- 47 записей в едином реестре: P0=13,P1=29,P2=5,P3=0. Из них SOURCE_DEFECT16,CONTRADICTION3,AMBIGUOUS_SPECIFICATION9,MISSING_CONTRACT9,UNPROVEN_CLAIM8,POTENTIAL_RISK2. Все29 исторических FSA-ID сопоставлены.11 записей без прямого FSA соответствия — не заявление о первом открытии в истории D/NUM.
- 60 семейств:43 условно математически проверены,3 противоречивы,1 неверная импликация,13 остаются UNVERIFIED/UNDEFINED/NOT_IMPLEMENTED. Математический статус и production mapping раздельны.
- 22 предложения:20 high,2 medium,0 low; все PROPOSAL_ONLY. Ни один экономический контракт не утверждён.

## Доказательная база и ограничения

Только read-only source, ручная алгебра и новые Reports. Никаких тестов, regression runners, native compile, harness, симуляторов, backtests или production patches не запускалось и не создавалось. Исторические PASS/FAIL не переоценивались исполнением. Примеры в тексте — аналитические контрпримеры, не broker receipts. Отсутствие native evidence не означает, что компилятор обнаружил ошибку.

Все1515 исходных файлов, включая74 production sources, сопоставлены побайтно с Git blobs, modes и SHA256 перечислены в BASELINE_AND_PRESERVATION. Последующая публикационная проверка сравнивает тот же Git tree. Production и historical evidence не изменялись. Нет внешних торговых запросов, funding или persistence write. Новые файлы ограничены Reports/HSBI_AUDIT03_*.md.

## Ответы на20 вопросов

### 1. Корректна ли базовая идея?

Как условная перенастройка signed exposure и учёт источников — имеет корректные локальные тождества. Как универсальная прибыльная/восстанавливающая система не доказана.

Основание: F005/F050/F058–059 в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md); ERR-032/038/042 в [реестре](HSBI_AUDIT03_ALL_ERRORS_RU.md); IMP-013/020/021 в [предложениях](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Первичные источники: `Docs/03_FULL_SYSTEM_MANUAL_RU.md:6-18; Docs/04_MATHEMATICAL_MODEL_RU.md:12,33-43`. Краткие F/ERR/IMP означают полный префикс HSBI-A03.

### 2. Корректна ли геометрия?

Модель favorable slope корректна при constant K; полная геометрия не подтверждена из-за mirrored price rule, Gross/Net mismatch и prefix exposure.

Основание: F005/F029/F039/F051–052 в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md); ERR-020/041/046 в [реестре](HSBI_AUDIT03_ALL_ERRORS_RU.md); IMP-007/012/022 в [предложениях](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Первичные источники: `Docs/04_MATHEMATICAL_MODEL_RU.md:12,21,39; Docs/26_GEOMETRY_ENGINE_SPECIFICATION_RU.md:7`. Краткие F/ERR/IMP означают полный префикс HSBI-A03.

### 3. Согласованы ли все лоты?

Нет: Core может стать0, optional Trend не согласован с четырьмя money legs, два grid origins требуют admission. Нельзя поднимать lot до min без пересчёта risk.

Основание: F001–004/F048 в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md); ERR-014/015/039/040 в [реестре](HSBI_AUDIT03_ALL_ERRORS_RU.md); IMP-002/007 в [предложениях](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Первичные источники: `Docs/04_MATHEMATICAL_MODEL_RU.md:9; Include/Planning/HSBI_GeometrySolver.mqh:28-35`. Краткие F/ERR/IMP означают полный префикс HSBI-A03.

### 4. Корректна ли денежная модель?

Signed суммы и partition identities корректны при явных assumptions. Сквозные cost coverage, cycle boundary, authority и available resource не завершены.

Основание: F007–014/F035/F060 в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md); ERR-022/033/036/047 в [реестре](HSBI_AUDIT03_ALL_ERRORS_RU.md); IMP-003/004/014/020 в [предложениях](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Первичные источники: `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:6-24; Include/Money/HSBI_BasketMoneyEvaluator.mqh:17`. Краткие F/ERR/IMP означают полный префикс HSBI-A03.

### 5. Сохраняются ли денежные ресурсы?

Абстрактные reserve/release/consume сохраняют G по ручному выводу. В production отрицательные buckets и неразделённые allocation phases мешают доказать сквозное сохранение.

Основание: F012–019/F053–056 в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md); ERR-005/006/007/033 в [реестре](HSBI_AUDIT03_ALL_ERRORS_RU.md); IMP-003/004 в [предложениях](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Первичные источники: `Docs/04_MATHEMATICAL_MODEL_RU.md:30; Include/Money/HSBI_AllocationLedgerTypes.mqh:7`. Краткие F/ERR/IMP означают полный префикс HSBI-A03.

### 6. Исключено ли двойное использование?

Не доказано: source-level registry/durable/CAS отсутствуют, локальные immutable/replay predicates неполны. Preview flaw не объявляется actual double spend.

Основание: F015–019/F057 в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md); ERR-001/004/008/017/030/033 в [реестре](HSBI_AUDIT03_ALL_ERRORS_RU.md); IMP-001/003/004/009 в [предложениях](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Первичные источники: `Docs/32_RESERVE_ALLOCATION_CONSUMPTION_RU.md:3-7; Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:63-70`. Краткие F/ERR/IMP означают полный префикс HSBI-A03.

### 7. Корректен ли Harvest?

Нормативный actual-close→reconciliation→allocation маршрут осмыслен, полный handler не реализован. Positive Harvest совместим с отрицательным CyclePnL. Small attribution и расходы требуют явной policy.

Основание: F007/F012/F035/F060 в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md); ERR-016/022/033/047 в [реестре](HSBI_AUDIT03_ALL_ERRORS_RU.md); IMP-004/008/014/020 в [предложениях](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Первичные источники: `Docs/10_BIG_HARVEST_SPECIFICATION_RU.md:6-17; Include/Money/HSBI_BasketMoneyEvaluator.mqh:17`. Краткие F/ERR/IMP означают полный префикс HSBI-A03.

### 8. Корректен ли Reserve?

Не как полный available resource: foreign consumption shape и spent-source eligible branch не устанавливают authoritative remaining owner balance.

Основание: F013–019/F060 в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md); ERR-007/008/033 в [реестре](HSBI_AUDIT03_ALL_ERRORS_RU.md); IMP-003/004 в [предложениях](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Первичные источники: `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:18-24; Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:44-70`. Краткие F/ERR/IMP означают полный префикс HSBI-A03.

### 9. Корректен ли Catch-Up?

R-L-B>0 корректно для заданной базы; absolute/incremental и all-level/single-level scope не согласованы полностью. Projected proof не actual funds.

Основание: F006/F020–023 в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md); ERR-018/033/043 в [реестре](HSBI_AUDIT03_ALL_ERRORS_RU.md); IMP-004/010 в [предложениях](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Первичные источники: `Docs/24_BROKER_MONEY_MODEL_RU.md:9; Include/Planning/HSBI_FutureSmallProofAggregator.mqh:50`. Краткие F/ERR/IMP означают полный префикс HSBI-A03.

### 10. Корректен ли FutureSmall?

Finite prefix не доказывает uniform tail; terminal min lot не actual close; сравнение BigGross подменено Net. Полное свойство не подтверждено.

Основание: F029/F037–038/F058 в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md); ERR-020/021/031/032 в [реестре](HSBI_AUDIT03_ALL_ERRORS_RU.md); IMP-012/013 в [предложениях](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Первичные источники: `Docs/27_FUTURE_SMALL_SOLVER_RU.md:5; Include/Planning/HSBI_FutureSmallSolver.mqh:89-90,142-149`. Краткие F/ERR/IMP означают полный префикс HSBI-A03.

### 11. Корректен ли NewFar?

Actual original Core requirement правильно сформулирован, но independent expected/provider, objective precedence и planned/actual residual boundary не дают полного proof. Полный bypass не заявлен.

Основание: F027–029/F047/F060 в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md); ERR-013/019/045 в [реестре](HSBI_AUDIT03_ALL_ERRORS_RU.md); IMP-001/011 в [предложениях](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Первичные источники: `Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:22-27; Include/Planning/HSBI_NewFarSolver.mqh:119-124,149-151`. Краткие F/ERR/IMP означают полный префикс HSBI-A03.

### 12. Согласованы ли состояния FSM?

Нет полного implemented event FSM.33 enum states и generic topology не создают handlers, financial guards, retry/restart и manual resume protocol.

Основание: F024–026/F052/F057 в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md); ERR-016/017/025/030/041 в [реестре](HSBI_AUDIT03_ALL_ERRORS_RU.md); IMP-008/009/022 в [предложениях](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Первичные источники: `Docs/06_STATE_MACHINE_SPECIFICATION_RU.md:6-21; Include/Core/HSBI_StateMachine.mqh:5-7`. Краткие F/ERR/IMP означают полный префикс HSBI-A03.

### 13. Есть ли математические противоречия?

Да: единый P+tick против BUY mirror, optional Trend, minimum-safe N против global risk-first. Prefix⇒uniform tail без invariant hypotheses — отдельная неверная импликация, не опровержение условной индукции.

Основание: F002/F038–039/F047/F051 в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md); ERR-015/019/021/046 в [реестре](HSBI_AUDIT03_ALL_ERRORS_RU.md); IMP-007/011/013 в [предложениях](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Первичные источники: `Docs/03_FULL_SYSTEM_MANUAL_RU.md:12,21; Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md:3`. Краткие F/ERR/IMP означают полный префикс HSBI-A03.

### 14. Доказана ли устойчивость?

Нет: favorable derivative и уменьшение lot недостаточны для invariant account-risk set, executable transitions или expected profit. Понятие устойчивости и market assumptions надо определить.

Основание: F031/F037–039/F051/F058–059 в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md); ERR-021/032/037/038/042 в [реестре](HSBI_AUDIT03_ALL_ERRORS_RU.md); IMP-013/015/021 в [предложениях](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Первичные источники: `Docs/04_MATHEMATICAL_MODEL_RU.md:12,33-42; Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:9-18`. Краткие F/ERR/IMP означают полный префикс HSBI-A03.

### 15. Доказана ли ограниченность убытка?

Безусловная — нет. Для unhedged short с неограниченной adverse ценой есть аналитический контрпример любому finite bound. Условный bound возможен только при дополнительных проверяемых допущениях.

Основание: F026/F031/F059 в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md); ERR-034/038/042 в [реестре](HSBI_AUDIT03_ALL_ERRORS_RU.md); IMP-015/021 в [предложениях](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Первичные источники: `Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:6-18; Docs/04_MATHEMATICAL_MODEL_RU.md:36`. Краткие F/ERR/IMP означают полный префикс HSBI-A03.

### 16. Доказано ли завершение цикла?

Нет: bound успешных сокращений и terminal lot не гарантируют время, нужную цену, следующий safe candidate или actual zero residual.

Основание: F037–038/F058 в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md); ERR-021/031/032 в [реестре](HSBI_AUDIT03_ALL_ERRORS_RU.md); IMP-013 в [предложениях](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Первичные источники: `Docs/04_MATHEMATICAL_MODEL_RU.md:33-36; Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:19-27`. Краткие F/ERR/IMP означают полный префикс HSBI-A03.

### 17. Соответствует ли production мануалу?

Полный lifecycle не реализован, что мануал явно признаёт. В отдельных библиотеках есть статические несовпадения equality, allocation, finite guards, geometry и gross. Current main не торгует; это не работающий полный EA.

Основание: F016–019/F029/F036/F057 в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md); ERR-001–012/014/016/020 в [реестре](HSBI_AUDIT03_ALL_ERRORS_RU.md); IMP-001/003/004/005/007/008/012 в [предложениях](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Первичные источники: `Docs/03_FULL_SYSTEM_MANUAL_RU.md:51; Hybrid_Split_Big_Independent_EA.mq5:19-44`. Краткие F/ERR/IMP означают полный префикс HSBI-A03.

### 18. Что наиболее критично?

13 P0 — блокирующие требования будущего подключения, не13 действующих exploits: identity/source/allocation/buckets/reserve binding/spent-source, nonfinite risk/fills/money, all-slot Far, independent expected, funding bridge и отсутствие безусловного loss bound.

Основание: F016–019/F036/F059–060 в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md); ERR-001/002/004/005/007–013/033/038 в [реестре](HSBI_AUDIT03_ALL_ERRORS_RU.md); IMP-001/003/004/005/006/009/021 в [предложениях](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Первичные источники: `Include/Money/HSBI_EconomicLedgerTypes.mqh:7-10; Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:44-70`. Краткие F/ERR/IMP означают полный префикс HSBI-A03.

### 19. Что делать первым?

Утвердить точный source/status/numeric/domain/active-leg scope и закрыть противоречия; затем отдельное identity/finite remediation, далее provider/global funding/journal, затем path risk/FSM/terminal proof. Не начинать интеграцию с NewFar.

Основание: F012–019/F041–043/F047/F060 в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md); ERR-001/002/013/017/019/033/040 в [реестре](HSBI_AUDIT03_ALL_ERRORS_RU.md); IMP-001/002/003/005/007/008/009/011 в [предложениях](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Первичные источники: `Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md:6-24; Docs/16_PERSISTENCE_AND_RESTART_RU.md:12-15`. Краткие F/ERR/IMP означают полный префикс HSBI-A03.

### 20. Можно ли переходить к исправлениям?

В этом задании нет. Материалы позволяют сформулировать ограниченный следующий scope, но coverage PARTIAL, approval отсутствует. One-file additive identity API не равен полному исправлению source authority/callers и не допускает funding/trading.

Основание: F017–019/F041–043/F060 в [каталоге](HSBI_AUDIT03_FORMULA_CATALOG_RU.md); ERR-001/002/013/017/029/033/040 в [реестре](HSBI_AUDIT03_ALL_ERRORS_RU.md); IMP-001/002/004/018 в [предложениях](HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md). Первичные источники: `Docs/HSBI_DG01_MINIMAL_R1_1_DIFF_PLAN_RU.md:3-5,17-33; Include/Money/HSBI_EconomicLedgerTypes.mqh:6-12`. Краткие F/ERR/IMP означают полный префикс HSBI-A03.

## Раздельная оценка готовности

| Ось | Вердикт | Основание |
|---|---|---|
| Локальные математические тождества | VERIFIED_UNDER_ASSUMPTIONS |43 семейств, ограничения в каждой карточке |
| Нормативная согласованность | NOT_ESTABLISHED |3 прямых противоречия, другие ambiguous/missing contracts |
| Фактическая библиотечная реализация | DEFECTS_OPEN |16 статических source defects; current main не торгует |
| Полный торговый цикл | NOT_IMPLEMENTED / NOT_VERIFIED |Нет lifecycle handlers/backend/actual execution proof |
| Продолжение документальной работы | ALLOWED_IN_CURRENT_AUDIT_SCOPE |Остаток перечислен в DOCUMENT_COVERAGE |
| Production remediation / R1.1 | NOT_AUTHORISED |Нужно отдельное явное задание и approval |
| Реальная торговля | NOT_ALLOWED |Runtime disabled, dispatch false; safety/profitability не доказаны |

## Что осталось до полного аудита

Прочитать85 оставшихся/частичных Docs; установить нормативную приоритетность предложений/исторических corrections; завершить review непрочитанных headers/callers; расширить формульный каталог обнаруженными там правилами; формализовать все event-level FSM combinations; закрыть конкретные uniform-market/cost/domain/terminal proof gaps. Это фактическая незавершённость, а не замена FULL COVERAGE количеством строк отчёта. Известных пробелов достаточно, чтобы запретить положительный полный вердикт даже при корректности многих локальных тождеств.

Следующий разрешаемый шаг должен отдельно определить: продолжение documentary coverage, административный ballot либо узкий remediation. Настоящий отчёт не выбирает за владельца и не начинает ни один production шаг.

## Публикационные метаданные

Файл фиксируется до создания содержащего его commit. Его собственный итоговый SHA нельзя записать внутрь того же immutable commit без самоссылки. Поэтому ниже публикационные поля имеют явное значение POST_PUBLICATION_CHECK_REQUIRED, а фактические полный SHA/parity/clean tree сообщаются после push во внешнем ответе. BASE_SHA, результаты анализа и запреты уже определены. Это не утверждение об уже выполненном push.

```text
[HSBI_AUDIT03_FINAL_STATUS]
BASE_SHA=6231bfbe94d39fbbb469b90a93e01426a83756bb
FINAL_SHA=POST_PUBLICATION_CHECK_REQUIRED
REMOTE_SHA_PARITY=POST_PUBLICATION_CHECK_REQUIRED
WORKTREE_CLEAN=POST_PUBLICATION_CHECK_REQUIRED

FULL_MANUAL_READ=YES
NORMATIVE_DOCUMENTS_TOTAL=136
NORMATIVE_DOCUMENTS_FULLY_READ=51
FORMULAS_TOTAL=60
FORMULAS_VERIFIED=43
FORMULAS_CONTRADICTORY=3
FORMULAS_INVALID=1
FORMULAS_UNVERIFIED=13

ERRORS_TOTAL=47
ERRORS_P0=13
ERRORS_P1=29
ERRORS_P2=5
ERRORS_P3=0
ERRORS_PROVEN=16
ERRORS_CONTRADICTIONS=3
ERRORS_UNPROVEN=8
ERRORS_NEW=11
ERRORS_HISTORICAL_MAPPED=29

IMPROVEMENTS_TOTAL=22
IMPROVEMENTS_HIGH_PRIORITY=20
IMPROVEMENTS_MEDIUM_PRIORITY=2
IMPROVEMENTS_LOW_PRIORITY=0

GEOMETRY_VERIFIED=NO
MONEY_MODEL_VERIFIED=NO
MONEY_CONSERVATION_PROVEN=NO
GLOBAL_FUNDING_PROVEN=NO
CATCH_UP_VERIFIED=NO
NEW_FAR_VERIFIED=NO
FUTURE_SMALL_VERIFIED=NO
FSM_SPECIFICATION_VERIFIED=NO
FULL_TRADING_CYCLE_VERIFIED=NO
STABILITY_PROVEN=NO
LOSS_BOUND_PROVEN=NO
PROFITABILITY_PROVEN=NO

TESTS_EXECUTED=NO
MQL5_COMPILE=NOT_RUN
MQL5_NATIVE_TESTS=NOT_RUN
PRODUCTION_FILES_CHANGED=NO
TRADING_LOGIC_CHANGED=NO

ERROR_REGISTER=Reports/HSBI_AUDIT03_ALL_ERRORS_RU.md
IMPROVEMENT_REGISTER=Reports/HSBI_AUDIT03_ALL_IMPROVEMENTS_RU.md
FINAL_VERDICT=Reports/HSBI_AUDIT03_FINAL_VERDICT_RU.md

AUDIT_COMPLETENESS=PARTIAL
ADMIN_APPROVAL_COMPLETE=NO
PRODUCTION_REMEDIATION_ALLOWED=NO
TRADING_LOGIC_START_ALLOWED=NO
BROKER_DISPATCH_ALLOWED=NO
REAL_TRADING_ALLOWED=NO

AUDIT03_COMMIT_CREATED=POST_PUBLICATION_CHECK_REQUIRED
AUDIT03_PUBLISHED=POST_PUBLICATION_CHECK_REQUIRED
[/HSBI_AUDIT03_FINAL_STATUS]
```
