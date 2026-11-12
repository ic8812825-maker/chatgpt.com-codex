# HSBI FULL SYSTEM AUDIT 02 — итоговый независимый вердикт

**SYSTEM_CRITICAL_CONTRADICTIONS_FOUND. AUDIT_COMPLETENESS=PARTIAL.** Восстановление workspace успешно; это не означает полноту доказательства всей системы. Production и historical evidence не исправлялись, никакого исполнения нет.

## Recovery и воспроизведение

Найдены12 незакоммиченных файлов первой попытки и ignored Python bytecode; оригинальные bytes сохранены base64 в RECOVERY_ARCHIVE, inventory с size/hash/mtime в RECOVERY_INVENTORY. Синтаксическая целостность не означает завершённость. Первичная попытка архивирования пыталась читать .pyc как UTF8 и завершилась UnicodeDecodeError; архив после этого создан бинарно безопасным способом, все recovered bytes проверяются по hashes. Файлы первой попытки не удалялись. Перед дальнейшей правкой recovered runner сохранён в archive; новый extension вынесен отдельно.

Независимая проверка Git tree:1416 исходных файлов,74 production sources. SHA/blob/mode, а не счётчик, являются основанием preservation. Исторические файлы остаются frozen.

First-attempt30 исходных проверок воспроизведены:17 PASS/13 FAIL. Новый дополнительный набор расширяет их до38:19 PASS/19 FAIL (6 новых несовпадений и2 положительных). Это не68 различных сценариев. 13 исходных FAIL разобраны индивидуально:10 source-contract mismatches,2 policy conflicts,1 valid-flag contract UNVERIFIED; несколько относятся к одному FSA. Отдельный Money Infinity является source-дефектом даже при неопределённости valid flag.

23 новых literal rational vectors PASS;22 перехода независимого integer-minor-unit ledger fixture PASS;6 различных мутаций реальных comparator/ownership/domain операций обнаружены. Эти mutations проверяют сохранённые guards, не доказывают полноту missing guards. Базовый ошибочный source не стал безопасным. Все compiler/process exits/stdout/stderr в evidence; исключения не считаются kill.

C++ LP64 adapter glue и dependency ordering взяты из frozen AUDIT01, **не являются вторым независимым MQL implementation**. Новые fixtures/ожидания написаны отдельно. Для P0 примеров не вызываются broker-money/margin stubs; сравнения finite/NaN зависят от стандартной C++/IEEE семантики, native MQL остаётся границей. Полный NewFar solver не запускался.

## Результат по вопросам задания

### 1–2. P0
9 независимо подтверждённых локальных source defects; FSA-010 классифицирован UNIMPLEMENTED independent authority, не доказан полный solver bypass. P0_UNVERIFIED=0 означает нет неклассифицированных строк, а не native доказательство всех10.

### 3–4. Достижимость
Все дефектные торговые контрпримеры не достигаются текущими OnInit/OnTick/OnTimer. OnTick вызывает запретительный stub. Диагностический FAR count достижим, но main не создаёт второй FAR. При будущей интеграции ошибки equality/funding/domain/role могут нарушить permission и учёт.

### 5–6. Формулы
23 условных real/rational утверждения разобраны алгебраически, 11 code/norm/proposal конфликтов,15 UNVERIFIED. F42 понижен относительно AUDIT01. Это не23 production proofs.

### 7–8. Деньги и funding
NO: exact specification подтверждает локальные partition-инварианты, production global registry/durable journal отсутствуют; exhaustion branch воспроизводит reserveGain40 из уже consumed50.

### 9–10. Harvest/FinalClose
NO: полного actual Harvest/FinalClose orchestration нет; positive Harvest не гарантирует positive cycle; fresh costs/positions/deals и threshold недостаточны без исполнения.

### 11–13. Far/recovery/loss
Только conditional N<F и q-теорема. Нет гарантии executable transitions/terminal close/верхней границы убытка при unrestricted unhedged Far. Broker min lot не zero residual.

### 14–15. FSM/native
Полный FSM не реализован. Нативные MetaEditor/MT5 проверки NOT_RUN; C++ и Python не подмена.

### 16–17. Minimal R1.1/owner
Начинать NO. Все16 решений остаются AWAITING_ADMIN_APPROVAL; непосредственно нужны D-02/D-08/NUM-CODEC/MQL-DOMAIN/schema и compatibility ballot, отдельное задание и native acceptance.

### 18. Полная торговая логика
После отдельного утверждения contracts, исправлений dependency chain economic→reconciliation→allocation→global source funding→durable/CAS→availability→risk/margin→full FSM и native/integration/broker validation. Срок и прибыльность из этих тестов не выводятся.

## Исторические регрессии

R7 exit1:57 PASS/5 FAIL; R0 exit1:35 PASS/46 normative mismatches. R8 exit1 при48 выполненных cases и R10 exit1 при67: по одному SCOPE finding, перечисляющему3 R0H test-only MQL файла. Это scope-policy conflict, не новая functional regression. Frozen expectations не изменены. C1 840/840 executions, C2 1264/1264 и2462 schema probes; R0F116 actual Run calls, R0G128, R0H148 reference cases PASS. Полные реальные outputs/hashes сохранены. Это не fresh full replay каждого исторического mutation/package catalog.

## Оставшиеся работы — основание PARTIAL

1. Нет native MQL исполнения и all-domain адаптерной эквивалентности. Минимальный Windows harness не покрывает все10 P0; инструкции и limits раскрыты.
2. Полная normative event/precondition/action FSM всех timeout/retry/partial/out-of-order/restart combinations не формализована. Есть33×33 pure topology и phase-level manual map; это нельзя назвать full FSM verification.
3. P1/P2 static reclassification не заменяет нативные counterexample executions. FSA019/020/026 остаются UNVERIFIED; FSA023 OOB исследован статически, опасный вызов не исполнялся. Часть семантических связей требует решения владельца.
4. Нет полного proof→actual-deal→source-funding→allocation→durable-consumption composition и global/CAS/concurrent/broker evidence. Exact fixture не заменяет этот путь.
5. Source mutation каталог узкий:6 причинных проверок, не exhaustive mutation coverage всех29 issues/49 formulas. Условные теоремы не доказываются тестовыми совпадениями.

Пакет может быть опубликован как проверяемый частичный аудит после integrity/preservation проверки; завершённость полного системного аудита и готовность production не заявляются. Следующий шаг — независимое рассмотрение и owner decisions, без автоматического R1.1.

AUDIT_COMPLETENESS=PARTIAL
P0_CONFIRMED=9_SOURCE_DEFECTS
P0_UNVERIFIED=0_UNCLASSIFIED
P0_UNIMPLEMENTED=1
P1_CONFIRMED=8_SOURCE_OR_CONTRACT
P1_UNVERIFIED=3
P1_UNIMPLEMENTED=3
P2_CONFIRMED=5_SOURCE_OR_CONTRACT
FORMULA_VERIFIED=23_CONDITIONAL_MATHEMATICS
FORMULA_CONTRADICTORY=11
FORMULA_UNVERIFIED=15
MONEY_CONSERVATION_PROVEN=NO_PRODUCTION_PROOF
GLOBAL_FUNDING_PROVEN=NO
FULL_FSM_VERIFIED=NO
FULL_TRADING_CYCLE_VERIFIED=NO
PROFITABILITY_PROVEN=NO
LOSS_BOUND_PROVEN=NO
MQL5_COMPILE=NOT_RUN
MQL5_NATIVE_TESTS=NOT_RUN
ADMIN_APPROVAL_COMPLETE=NO
R1_1_START_ALLOWED=NO
PRODUCTION_REMEDIATION_ALLOWED=NO
TRADING_LOGIC_START_ALLOWED=NO
BROKER_DISPATCH_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
FINAL_SYSTEM_VERDICT=SYSTEM_CRITICAL_CONTRADICTIONS_FOUND
