# Этап 3.1.2 — формальный реестр конфликтов документации Hybrid Split Big

Статус: `PASS`  
Parent SHA: `46c06df624e09589c5bf95c597b2a0be55ebf5a8`

## Ограничение полномочий реестра

> Настоящий реестр является регистрационным и аналитическим документом. Он не выбирает нормативную сторону конфликта, не изменяет бизнес-логику, не назначает production candidate и не создаёт окончательный source of truth. Все бизнес-решения, влияющие на формулы, коэффициенты, состояния, денежные потоки, исполнение ордеров или завершение цикла, требуют отдельного решения пользователя.

Реестр фиксирует, но не разрешает конфликты. Запись не делает сторону неверной; порядок A/B не задаёт приоритет. `NORMATIVE` inventory предварителен. Код/runtime, test PASS и implementation report не заменяют письменный контракт. Решения выполняются последующими этапами после подтверждения пользователя.

## 1. Scope

Прочитаны 69 baseline-документов, включая все 13 NORMATIVE и 2 CONFLICTING. Все 45 обязательных тем зарегистрированы без автоматического решения.

## 2. Сводная таблица

| ID | Категория | Название | Документы | Критичность | User | Статус | Этап |
|---|---|---|---|---|---|---|---|
| HSB-DOC-CONFLICT-001 | PARAMETER | BigRatio values | `Docs/MANUAL.md`; `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md` | BLOCKER | YES | NEEDS_USER_DECISION | 3.1.7 |
| HSB-DOC-CONFLICT-002 | PARAMETER | SmallRatio values | `Docs/MANUAL.md`; `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md` | BLOCKER | YES | NEEDS_USER_DECISION | 3.1.7 |
| HSB-DOC-CONFLICT-003 | PARAMETER | CloseBigOnSmall values | `Docs/MANUAL.md`; `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md` | CRITICAL | YES | NEEDS_USER_DECISION | 3.1.7 |
| HSB-DOC-CONFLICT-004 | PARAMETER | RemainBigOnSmall values | `Docs/MANUAL.md`; `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md` | CRITICAL | YES | NEEDS_USER_DECISION | 3.1.7 |
| HSB-DOC-CONFLICT-005 | PARAMETER | CloseFarShare values | `Docs/MANUAL.md`; `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md` | HIGH | YES | NEEDS_USER_DECISION | 3.1.7 |
| HSB-DOC-CONFLICT-006 | PARAMETER | ReserveShare values | `Docs/MANUAL.md`; `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md` | CRITICAL | YES | NEEDS_USER_DECISION | 3.1.7 |
| HSB-DOC-CONFLICT-007 | PARAMETER | SmallReserveShare values | `Docs/MANUAL.md`; `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md` | HIGH | YES | NEEDS_USER_DECISION | 3.1.7 |
| HSB-DOC-CONFLICT-008 | RESERVE | Reserve in Partial Far | `Docs/HYBRID_SPLIT_BIG_MONEY_FLOW.md`; `Docs/MANUAL.md` | CRITICAL | YES | NEEDS_USER_DECISION | 3.1.5 |
| HSB-DOC-CONFLICT-009 | RECOVERY_PL | RecoveryPL includes Reserve | `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`; `Docs/FULL_AUDIT_REPORT.md` | CRITICAL | YES | NEEDS_USER_DECISION | 3.1.5 |
| HSB-DOC-CONFLICT-010 | RECOVERY_PL | RecoveryPL includes Initial Plus | `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`; `Docs/FULL_AUDIT_REPORT.md` | HIGH | YES | NEEDS_USER_DECISION | 3.1.5 |
| HSB-DOC-CONFLICT-011 | RECOVERY_PL | RecoveryPL Symbol filter | `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`; `Docs/FULL_AUDIT_REPORT.md` | CRITICAL | YES | NEEDS_USER_DECISION | 3.1.5 |
| HSB-DOC-CONFLICT-012 | RECOVERY_PL | RecoveryPL Magic filter | `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`; `Docs/FULL_AUDIT_REPORT.md` | CRITICAL | YES | NEEDS_USER_DECISION | 3.1.5 |
| HSB-DOC-CONFLICT-013 | FORMULA | Gross versus Net Profit | `Docs/HYBRID_SPLIT_BIG_FORMULA_REFERENCE.md`; `Docs/MANUAL.md` | HIGH | YES | NEEDS_USER_DECISION | 3.1.4 |
| HSB-DOC-CONFLICT-014 | MONEY_LEDGER | Commission swap fee | `Docs/HYBRID_SPLIT_BIG_MONEY_FLOW.md`; `Docs/BASKET_RISK_CONTRACT_RU.md` | HIGH | YES | NEEDS_USER_DECISION | 3.1.5 |
| HSB-DOC-CONFLICT-015 | RESERVE | Projected versus Realized Reserve | `Docs/HYBRID_SPLIT_BIG_MONEY_FLOW.md`; `Docs/MANUAL.md` | CRITICAL | YES | NEEDS_USER_DECISION | 3.1.5 |
| HSB-DOC-CONFLICT-016 | EXECUTION | Planned versus actual close result | `Docs/BASKET_RISK_CONTRACT_RU.md`; `Docs/HYBRID_SPLIT_BIG_IMPLEMENTATION_REPORT_RU.md` | CRITICAL | YES | NEEDS_USER_DECISION | 3.1.6 |
| HSB-DOC-CONFLICT-017 | FINAL_CLOSE | Final Close preview versus actual success | `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`; `Docs/MANUAL.md` | BLOCKER | YES | NEEDS_USER_DECISION | 3.1.6 |
| HSB-DOC-CONFLICT-018 | SMALL_SCENARIO | Small close trigger | `Docs/HYBRID_SPLIT_BIG_STATE_TRANSITION_TABLE.md`; `Docs/MANUAL.md` | HIGH | YES | NEEDS_USER_DECISION | 3.1.6 |
| HSB-DOC-CONFLICT-019 | SMALL_SCENARIO | Old Far full versus partial close | `Docs/HYBRID_SPLIT_BIG_STATE_TRANSITION_TABLE.md`; `Docs/MANUAL.md` | HIGH | YES | NEEDS_USER_DECISION | 3.1.6 |
| HSB-DOC-CONFLICT-020 | GEOMETRY | New Far source | `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`; `Docs/MANUAL.md` | BLOCKER | YES | NEEDS_USER_DECISION | 3.1.6 |
| HSB-DOC-CONFLICT-021 | FORMULA | Next Big base | `Docs/HYBRID_SPLIT_BIG_FORMULA_REFERENCE.md`; `Docs/MANUAL.md` | HIGH | YES | NEEDS_USER_DECISION | 3.1.4 |
| HSB-DOC-CONFLICT-022 | GEOMETRY | new Big less than old Far | `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`; `Docs/MANUAL.md` | HIGH | YES | NEEDS_USER_DECISION | 3.1.6 |
| HSB-DOC-CONFLICT-023 | RISK | Negative Small Reverse Net | `Docs/BASKET_RISK_CONTRACT_RU.md`; `Docs/HYBRID_SPLIT_BIG_THREE_LAWS_MATH_MANUAL_RU.md` | BLOCKER | YES | NEEDS_USER_DECISION | 3.1.8 |
| HSB-DOC-CONFLICT-024 | SMALL_SCENARIO | Small Far Big close order | `Docs/HYBRID_SPLIT_BIG_STATE_TRANSITION_TABLE.md`; `Docs/MANUAL.md` | CRITICAL | YES | NEEDS_USER_DECISION | 3.1.6 |
| HSB-DOC-CONFLICT-025 | RESERVE | Reserve credit order | `Docs/HYBRID_SPLIT_BIG_MONEY_FLOW.md`; `Docs/MANUAL.md` | CRITICAL | YES | NEEDS_USER_DECISION | 3.1.5 |
| HSB-DOC-CONFLICT-026 | STATE_MACHINE | State transition order | `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`; `Docs/MANUAL.md` | HIGH | YES | NEEDS_USER_DECISION | 3.1.6 |
| HSB-DOC-CONFLICT-027 | EXECUTION | Requested versus executed volume | `Docs/BASKET_RISK_CONTRACT_RU.md`; `Docs/HYBRID_SPLIT_BIG_IMPLEMENTATION_REPORT_RU.md` | CRITICAL | YES | NEEDS_USER_DECISION | 3.1.6 |
| HSB-DOC-CONFLICT-028 | ROUNDING | FLOOR CEILING NEAREST | `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`; `Docs/BIG_SCENARIO_FULL_AUDIT.md` | CRITICAL | YES | NEEDS_USER_DECISION | 3.1.4 |
| HSB-DOC-CONFLICT-029 | TEST_EVIDENCE | Python PASS versus MT5 NOT_RUN | `Docs/STAGE_1_2_4_1_EVIDENCE_RU.md`; `Docs/HYBRID_SPLIT_BIG_METAEDITOR_COMPILE.md` | INFORMATIONAL | NO | DEFERRED_TO_STAGE_3_1_8 | 3.1.8 |
| HSB-DOC-CONFLICT-030 | READINESS | Production Ready versus missing broker evidence | `Docs/BIG_SMALL_PRODUCTION_READINESS_REPORT_RU.md`; `Docs/FULL_AUDIT_REPORT.md` | CRITICAL | YES | NEEDS_USER_DECISION | 3.1.8 |
| HSB-DOC-CONFLICT-031 | LEGACY_MIXING | Legacy Split Hybrid terminology | `Docs/MANUAL.md`; `Docs/HYBRID_SPLIT_BIG_COMPLETE_MANUAL_RU.md` | BLOCKER | YES | NEEDS_USER_DECISION | 3.1.3 |
| HSB-DOC-CONFLICT-032 | DUPLICATION | Split test plan duplicate | `Docs/HYBRID_SPLIT_BIG_COMPLETE_MANUAL_RU.md`; `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md` | LOW | NO | DEFERRED_TO_STAGE_3_1_8 | 3.1.8 |
| HSB-DOC-CONFLICT-033 | PERSISTENCE | Reserve persistence | `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`; `Docs/SPLIT_BIG_EXACT_PERSISTENCE_REPORT_RU.md` | HIGH | YES | NEEDS_USER_DECISION | 3.1.6 |
| HSB-DOC-CONFLICT-034 | MONEY_LEDGER | Exactly-once Reserve credit | `Docs/HYBRID_SPLIT_BIG_MONEY_FLOW.md`; `Docs/BASKET_RISK_CONTRACT_RU.md` | CRITICAL | YES | NEEDS_USER_DECISION | 3.1.5 |
| HSB-DOC-CONFLICT-035 | EXECUTION | Partial fill | `Docs/BASKET_RISK_CONTRACT_RU.md`; `Docs/HYBRID_SPLIT_BIG_IMPLEMENTATION_REPORT_RU.md` | HIGH | YES | NEEDS_USER_DECISION | 3.1.6 |
| HSB-DOC-CONFLICT-036 | EXECUTION | Retry idempotency | `Docs/BASKET_RISK_CONTRACT_RU.md`; `Docs/HYBRID_SPLIT_BIG_IMPLEMENTATION_REPORT_RU.md` | HIGH | YES | NEEDS_USER_DECISION | 3.1.6 |
| HSB-DOC-CONFLICT-037 | RECONCILIATION | Restart reconciliation | `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`; `Docs/PERSISTENCE_AND_CLEAN_START_FINAL_REPORT_RU.md` | HIGH | YES | NEEDS_USER_DECISION | 3.1.6 |
| HSB-DOC-CONFLICT-038 | FINAL_CLOSE | Final Close partial execution | `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`; `Docs/MANUAL.md` | CRITICAL | YES | NEEDS_USER_DECISION | 3.1.6 |
| HSB-DOC-CONFLICT-039 | STATE_MACHINE | MaxHarvestLevels behavior | `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`; `Docs/MANUAL.md` | HIGH | YES | NEEDS_USER_DECISION | 3.1.6 |
| HSB-DOC-CONFLICT-040 | STATE_MACHINE | Reverse limit behavior | `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`; `Docs/MANUAL.md` | HIGH | YES | NEEDS_USER_DECISION | 3.1.6 |
| HSB-DOC-CONFLICT-041 | STATE_MACHINE | Invalid geometry behavior | `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`; `Docs/MANUAL.md` | HIGH | YES | NEEDS_USER_DECISION | 3.1.6 |
| HSB-DOC-CONFLICT-042 | RISK | Basket Risk preview versus execution | `Docs/BASKET_RISK_CONTRACT_RU.md`; `Docs/HYBRID_SPLIT_BIG_THREE_LAWS_MATH_MANUAL_RU.md` | HIGH | YES | NEEDS_USER_DECISION | 3.1.8 |
| HSB-DOC-CONFLICT-043 | RISK | Cycle versus account risk | `Docs/BASKET_RISK_CONTRACT_RU.md`; `Docs/HYBRID_SPLIT_BIG_THREE_LAWS_MATH_MANUAL_RU.md` | HIGH | YES | NEEDS_USER_DECISION | 3.1.8 |
| HSB-DOC-CONFLICT-044 | RISK | Terminal-safe versus mathematically-safe | `Docs/BASKET_RISK_CONTRACT_RU.md`; `Docs/HYBRID_SPLIT_BIG_THREE_LAWS_MATH_MANUAL_RU.md` | CRITICAL | YES | NEEDS_USER_DECISION | 3.1.8 |
| HSB-DOC-CONFLICT-045 | DUPLICATION | Source-of-truth competition | `Docs/HYBRID_SPLIT_BIG_COMPLETE_MANUAL_RU.md`; `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md` | BLOCKER | YES | NEEDS_USER_DECISION | 3.1.8 |

## 3. Подробные записи

### HSB-DOC-CONFLICT-001 — BigRatio values

- **ID:** `HSB-DOC-CONFLICT-001`
- **Краткое название:** BigRatio values
- **Категория:** `PARAMETER`
- **Подкатегория:** BigRatio values
- **Сторона A:** `Docs/MANUAL.md`; раздел/контекст «BigRatio values»; фрагмент: `несколько parameter profiles`.
- **Сторона B:** `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md`; раздел/контекст «BigRatio values»; фрагмент: `другой baseline profile`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `DIFFERENT_PARAMETER`
- **Затрагиваемые сущности:** BigRatio values; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `BLOCKER`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.7`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-002 — SmallRatio values

- **ID:** `HSB-DOC-CONFLICT-002`
- **Краткое название:** SmallRatio values
- **Категория:** `PARAMETER`
- **Подкатегория:** SmallRatio values
- **Сторона A:** `Docs/MANUAL.md`; раздел/контекст «SmallRatio values»; фрагмент: `несколько parameter profiles`.
- **Сторона B:** `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md`; раздел/контекст «SmallRatio values»; фрагмент: `другой baseline profile`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `DIFFERENT_PARAMETER`
- **Затрагиваемые сущности:** SmallRatio values; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `BLOCKER`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.7`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-003 — CloseBigOnSmall values

- **ID:** `HSB-DOC-CONFLICT-003`
- **Краткое название:** CloseBigOnSmall values
- **Категория:** `PARAMETER`
- **Подкатегория:** CloseBigOnSmall values
- **Сторона A:** `Docs/MANUAL.md`; раздел/контекст «CloseBigOnSmall values»; фрагмент: `несколько parameter profiles`.
- **Сторона B:** `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md`; раздел/контекст «CloseBigOnSmall values»; фрагмент: `другой baseline profile`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `DIFFERENT_PARAMETER`
- **Затрагиваемые сущности:** CloseBigOnSmall values; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `CRITICAL`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.7`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-004 — RemainBigOnSmall values

- **ID:** `HSB-DOC-CONFLICT-004`
- **Краткое название:** RemainBigOnSmall values
- **Категория:** `PARAMETER`
- **Подкатегория:** RemainBigOnSmall values
- **Сторона A:** `Docs/MANUAL.md`; раздел/контекст «RemainBigOnSmall values»; фрагмент: `несколько parameter profiles`.
- **Сторона B:** `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md`; раздел/контекст «RemainBigOnSmall values»; фрагмент: `другой baseline profile`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `DIFFERENT_PARAMETER`
- **Затрагиваемые сущности:** RemainBigOnSmall values; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `CRITICAL`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.7`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-005 — CloseFarShare values

- **ID:** `HSB-DOC-CONFLICT-005`
- **Краткое название:** CloseFarShare values
- **Категория:** `PARAMETER`
- **Подкатегория:** CloseFarShare values
- **Сторона A:** `Docs/MANUAL.md`; раздел/контекст «CloseFarShare values»; фрагмент: `несколько parameter profiles`.
- **Сторона B:** `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md`; раздел/контекст «CloseFarShare values»; фрагмент: `другой baseline profile`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `DIFFERENT_PARAMETER`
- **Затрагиваемые сущности:** CloseFarShare values; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `HIGH`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.7`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-006 — ReserveShare values

- **ID:** `HSB-DOC-CONFLICT-006`
- **Краткое название:** ReserveShare values
- **Категория:** `PARAMETER`
- **Подкатегория:** ReserveShare values
- **Сторона A:** `Docs/MANUAL.md`; раздел/контекст «ReserveShare values»; фрагмент: `несколько parameter profiles`.
- **Сторона B:** `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md`; раздел/контекст «ReserveShare values»; фрагмент: `другой baseline profile`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `DIFFERENT_PARAMETER`
- **Затрагиваемые сущности:** ReserveShare values; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `CRITICAL`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.7`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-007 — SmallReserveShare values

- **ID:** `HSB-DOC-CONFLICT-007`
- **Краткое название:** SmallReserveShare values
- **Категория:** `PARAMETER`
- **Подкатегория:** SmallReserveShare values
- **Сторона A:** `Docs/MANUAL.md`; раздел/контекст «SmallReserveShare values»; фрагмент: `несколько parameter profiles`.
- **Сторона B:** `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md`; раздел/контекст «SmallReserveShare values»; фрагмент: `другой baseline profile`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `DIFFERENT_PARAMETER`
- **Затрагиваемые сущности:** SmallReserveShare values; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `HIGH`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.7`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-008 — Reserve in Partial Far

- **ID:** `HSB-DOC-CONFLICT-008`
- **Краткое название:** Reserve in Partial Far
- **Категория:** `RESERVE`
- **Подкатегория:** Reserve in Partial Far
- **Сторона A:** `Docs/HYBRID_SPLIT_BIG_MONEY_FLOW.md`; раздел/контекст «Reserve in Partial Far»; фрагмент: `confirmed buckets/forbidden edges`.
- **Сторона B:** `Docs/MANUAL.md`; раздел/контекст «Reserve in Partial Far»; фрагмент: `Legacy Reserve scope`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `AMBIGUOUS_DEFINITION`
- **Затрагиваемые сущности:** Reserve in Partial Far; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `CRITICAL`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.5`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-009 — RecoveryPL includes Reserve

- **ID:** `HSB-DOC-CONFLICT-009`
- **Краткое название:** RecoveryPL includes Reserve
- **Категория:** `RECOVERY_PL`
- **Подкатегория:** RecoveryPL includes Reserve
- **Сторона A:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`; раздел/контекст «RecoveryPL includes Reserve»; фрагмент: `identity/double-count MUST`.
- **Сторона B:** `Docs/FULL_AUDIT_REPORT.md`; раздел/контекст «RecoveryPL includes Reserve»; фрагмент: `Legacy account/recovery scope`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `AMBIGUOUS_DEFINITION`
- **Затрагиваемые сущности:** RecoveryPL includes Reserve; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `CRITICAL`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.5`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-010 — RecoveryPL includes Initial Plus

- **ID:** `HSB-DOC-CONFLICT-010`
- **Краткое название:** RecoveryPL includes Initial Plus
- **Категория:** `RECOVERY_PL`
- **Подкатегория:** RecoveryPL includes Initial Plus
- **Сторона A:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`; раздел/контекст «RecoveryPL includes Initial Plus»; фрагмент: `identity/double-count MUST`.
- **Сторона B:** `Docs/FULL_AUDIT_REPORT.md`; раздел/контекст «RecoveryPL includes Initial Plus»; фрагмент: `Legacy account/recovery scope`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `AMBIGUOUS_DEFINITION`
- **Затрагиваемые сущности:** RecoveryPL includes Initial Plus; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `HIGH`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.5`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-011 — RecoveryPL Symbol filter

- **ID:** `HSB-DOC-CONFLICT-011`
- **Краткое название:** RecoveryPL Symbol filter
- **Категория:** `RECOVERY_PL`
- **Подкатегория:** RecoveryPL Symbol filter
- **Сторона A:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`; раздел/контекст «RecoveryPL Symbol filter»; фрагмент: `identity/double-count MUST`.
- **Сторона B:** `Docs/FULL_AUDIT_REPORT.md`; раздел/контекст «RecoveryPL Symbol filter»; фрагмент: `Legacy account/recovery scope`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `AMBIGUOUS_DEFINITION`
- **Затрагиваемые сущности:** RecoveryPL Symbol filter; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `CRITICAL`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.5`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-012 — RecoveryPL Magic filter

- **ID:** `HSB-DOC-CONFLICT-012`
- **Краткое название:** RecoveryPL Magic filter
- **Категория:** `RECOVERY_PL`
- **Подкатегория:** RecoveryPL Magic filter
- **Сторона A:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`; раздел/контекст «RecoveryPL Magic filter»; фрагмент: `identity/double-count MUST`.
- **Сторона B:** `Docs/FULL_AUDIT_REPORT.md`; раздел/контекст «RecoveryPL Magic filter»; фрагмент: `Legacy account/recovery scope`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `AMBIGUOUS_DEFINITION`
- **Затрагиваемые сущности:** RecoveryPL Magic filter; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `CRITICAL`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.5`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-013 — Gross versus Net Profit

- **ID:** `HSB-DOC-CONFLICT-013`
- **Краткое название:** Gross versus Net Profit
- **Категория:** `FORMULA`
- **Подкатегория:** Gross versus Net Profit
- **Сторона A:** `Docs/HYBRID_SPLIT_BIG_FORMULA_REFERENCE.md`; раздел/контекст «Gross versus Net Profit»; фрагмент: `Hybrid split-role formula`.
- **Сторона B:** `Docs/MANUAL.md`; раздел/контекст «Gross versus Net Profit»; фрагмент: `Legacy aggregate-Big formula`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `DIFFERENT_FORMULA`
- **Затрагиваемые сущности:** Gross versus Net Profit; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `HIGH`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.4`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-014 — Commission swap fee

- **ID:** `HSB-DOC-CONFLICT-014`
- **Краткое название:** Commission swap fee
- **Категория:** `MONEY_LEDGER`
- **Подкатегория:** Commission swap fee
- **Сторона A:** `Docs/HYBRID_SPLIT_BIG_MONEY_FLOW.md`; раздел/контекст «Commission swap fee»; фрагмент: `confirmed ledger conservation`.
- **Сторона B:** `Docs/BASKET_RISK_CONTRACT_RU.md`; раздел/контекст «Commission swap fee»; фрагмент: `expanded event-key/bucket contract`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `AMBIGUOUS_DEFINITION`
- **Затрагиваемые сущности:** Commission swap fee; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `HIGH`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.5`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-015 — Projected versus Realized Reserve

- **ID:** `HSB-DOC-CONFLICT-015`
- **Краткое название:** Projected versus Realized Reserve
- **Категория:** `RESERVE`
- **Подкатегория:** Projected versus Realized Reserve
- **Сторона A:** `Docs/HYBRID_SPLIT_BIG_MONEY_FLOW.md`; раздел/контекст «Projected versus Realized Reserve»; фрагмент: `confirmed buckets/forbidden edges`.
- **Сторона B:** `Docs/MANUAL.md`; раздел/контекст «Projected versus Realized Reserve»; фрагмент: `Legacy Reserve scope`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `AMBIGUOUS_DEFINITION`
- **Затрагиваемые сущности:** Projected versus Realized Reserve; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `CRITICAL`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.5`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-016 — Planned versus actual close result

- **ID:** `HSB-DOC-CONFLICT-016`
- **Краткое название:** Planned versus actual close result
- **Категория:** `EXECUTION`
- **Подкатегория:** Planned versus actual close result
- **Сторона A:** `Docs/BASKET_RISK_CONTRACT_RU.md`; раздел/контекст «Planned versus actual close result»; фрагмент: `actual/reconciliation required`.
- **Сторона B:** `Docs/HYBRID_SPLIT_BIG_IMPLEMENTATION_REPORT_RU.md`; раздел/контекст «Planned versus actual close result»; фрагмент: `source claim without MT5 runtime proof`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `PLANNED_VS_EXECUTED`
- **Затрагиваемые сущности:** Planned versus actual close result; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `CRITICAL`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.6`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-017 — Final Close preview versus actual success

- **ID:** `HSB-DOC-CONFLICT-017`
- **Краткое название:** Final Close preview versus actual success
- **Категория:** `FINAL_CLOSE`
- **Подкатегория:** Final Close preview versus actual success
- **Сторона A:** `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`; раздел/контекст «Final Close preview versus actual success»; фрагмент: `FINAL_CLOSE_PREVIEW_REQUIRED`.
- **Сторона B:** `Docs/MANUAL.md`; раздел/контекст «Final Close preview versus actual success»; фрагмент: `FinalCloseAllowed near CLOSED_PROFIT`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `PREVIEW_VS_ACTUAL`
- **Затрагиваемые сущности:** Final Close preview versus actual success; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `BLOCKER`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.6`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-018 — Small close trigger

- **ID:** `HSB-DOC-CONFLICT-018`
- **Краткое название:** Small close trigger
- **Категория:** `SMALL_SCENARIO`
- **Подкатегория:** Small close trigger
- **Сторона A:** `Docs/HYBRID_SPLIT_BIG_STATE_TRANSITION_TABLE.md`; раздел/контекст «Small close trigger»; фрагмент: `Hybrid Small phase order`.
- **Сторона B:** `Docs/MANUAL.md`; раздел/контекст «Small close trigger»; фрагмент: `Legacy Small-at-Far order`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `AMBIGUOUS_DEFINITION`
- **Затрагиваемые сущности:** Small close trigger; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `HIGH`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.6`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-019 — Old Far full versus partial close

- **ID:** `HSB-DOC-CONFLICT-019`
- **Краткое название:** Old Far full versus partial close
- **Категория:** `SMALL_SCENARIO`
- **Подкатегория:** Old Far full versus partial close
- **Сторона A:** `Docs/HYBRID_SPLIT_BIG_STATE_TRANSITION_TABLE.md`; раздел/контекст «Old Far full versus partial close»; фрагмент: `Hybrid Small phase order`.
- **Сторона B:** `Docs/MANUAL.md`; раздел/контекст «Old Far full versus partial close»; фрагмент: `Legacy Small-at-Far order`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `AMBIGUOUS_DEFINITION`
- **Затрагиваемые сущности:** Old Far full versus partial close; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `HIGH`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.6`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-020 — New Far source

- **ID:** `HSB-DOC-CONFLICT-020`
- **Краткое название:** New Far source
- **Категория:** `GEOMETRY`
- **Подкатегория:** New Far source
- **Сторона A:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`; раздел/контекст «New Far source»; фрагмент: `strict post-round GEO MUST`.
- **Сторона B:** `Docs/MANUAL.md`; раздел/контекст «New Far source»; фрагмент: `Legacy compression roles`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `AMBIGUOUS_DEFINITION`
- **Затрагиваемые сущности:** New Far source; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `BLOCKER`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.6`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-021 — Next Big base

- **ID:** `HSB-DOC-CONFLICT-021`
- **Краткое название:** Next Big base
- **Категория:** `FORMULA`
- **Подкатегория:** Next Big base
- **Сторона A:** `Docs/HYBRID_SPLIT_BIG_FORMULA_REFERENCE.md`; раздел/контекст «Next Big base»; фрагмент: `Hybrid split-role formula`.
- **Сторона B:** `Docs/MANUAL.md`; раздел/контекст «Next Big base»; фрагмент: `Legacy aggregate-Big formula`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `DIFFERENT_FORMULA`
- **Затрагиваемые сущности:** Next Big base; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `HIGH`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.4`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-022 — new Big less than old Far

- **ID:** `HSB-DOC-CONFLICT-022`
- **Краткое название:** new Big less than old Far
- **Категория:** `GEOMETRY`
- **Подкатегория:** new Big less than old Far
- **Сторона A:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`; раздел/контекст «new Big less than old Far»; фрагмент: `strict post-round GEO MUST`.
- **Сторона B:** `Docs/MANUAL.md`; раздел/контекст «new Big less than old Far»; фрагмент: `Legacy compression roles`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `AMBIGUOUS_DEFINITION`
- **Затрагиваемые сущности:** new Big less than old Far; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `HIGH`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.6`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-023 — Negative Small Reverse Net

- **ID:** `HSB-DOC-CONFLICT-023`
- **Краткое название:** Negative Small Reverse Net
- **Категория:** `RISK`
- **Подкатегория:** Negative Small Reverse Net
- **Сторона A:** `Docs/BASKET_RISK_CONTRACT_RU.md`; раздел/контекст «Negative Small Reverse Net»; фрагмент: `Cycle/Account/freshness gates`.
- **Сторона B:** `Docs/HYBRID_SPLIT_BIG_THREE_LAWS_MATH_MANUAL_RU.md`; раздел/контекст «Negative Small Reverse Net»; фрагмент: `analytical laws only`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `AMBIGUOUS_DEFINITION`
- **Затрагиваемые сущности:** Negative Small Reverse Net; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `BLOCKER`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.8`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-024 — Small Far Big close order

- **ID:** `HSB-DOC-CONFLICT-024`
- **Краткое название:** Small Far Big close order
- **Категория:** `SMALL_SCENARIO`
- **Подкатегория:** Small Far Big close order
- **Сторона A:** `Docs/HYBRID_SPLIT_BIG_STATE_TRANSITION_TABLE.md`; раздел/контекст «Small Far Big close order»; фрагмент: `Hybrid Small phase order`.
- **Сторона B:** `Docs/MANUAL.md`; раздел/контекст «Small Far Big close order»; фрагмент: `Legacy Small-at-Far order`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `AMBIGUOUS_DEFINITION`
- **Затрагиваемые сущности:** Small Far Big close order; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `CRITICAL`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.6`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-025 — Reserve credit order

- **ID:** `HSB-DOC-CONFLICT-025`
- **Краткое название:** Reserve credit order
- **Категория:** `RESERVE`
- **Подкатегория:** Reserve credit order
- **Сторона A:** `Docs/HYBRID_SPLIT_BIG_MONEY_FLOW.md`; раздел/контекст «Reserve credit order»; фрагмент: `confirmed buckets/forbidden edges`.
- **Сторона B:** `Docs/MANUAL.md`; раздел/контекст «Reserve credit order»; фрагмент: `Legacy Reserve scope`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `AMBIGUOUS_DEFINITION`
- **Затрагиваемые сущности:** Reserve credit order; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `CRITICAL`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.5`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-026 — State transition order

- **ID:** `HSB-DOC-CONFLICT-026`
- **Краткое название:** State transition order
- **Категория:** `STATE_MACHINE`
- **Подкатегория:** State transition order
- **Сторона A:** `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`; раздел/контекст «State transition order»; фрагмент: `StateBefore/After revision`.
- **Сторона B:** `Docs/MANUAL.md`; раздел/контекст «State transition order»; фрагмент: `Legacy terminal state namespace`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `AMBIGUOUS_DEFINITION`
- **Затрагиваемые сущности:** State transition order; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `HIGH`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.6`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-027 — Requested versus executed volume

- **ID:** `HSB-DOC-CONFLICT-027`
- **Краткое название:** Requested versus executed volume
- **Категория:** `EXECUTION`
- **Подкатегория:** Requested versus executed volume
- **Сторона A:** `Docs/BASKET_RISK_CONTRACT_RU.md`; раздел/контекст «Requested versus executed volume»; фрагмент: `actual/reconciliation required`.
- **Сторона B:** `Docs/HYBRID_SPLIT_BIG_IMPLEMENTATION_REPORT_RU.md`; раздел/контекст «Requested versus executed volume»; фрагмент: `source claim without MT5 runtime proof`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `PLANNED_VS_EXECUTED`
- **Затрагиваемые сущности:** Requested versus executed volume; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `CRITICAL`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.6`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-028 — FLOOR CEILING NEAREST

- **ID:** `HSB-DOC-CONFLICT-028`
- **Краткое название:** FLOOR CEILING NEAREST
- **Категория:** `ROUNDING`
- **Подкатегория:** FLOOR CEILING NEAREST
- **Сторона A:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`; раздел/контекст «FLOOR CEILING NEAREST»; фрагмент: `DOWN/UP rounding`.
- **Сторона B:** `Docs/BIG_SCENARIO_FULL_AUDIT.md`; раздел/контекст «FLOOR CEILING NEAREST»; фрагмент: `Legacy Nearest/Up rounding`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `DIFFERENT_FORMULA`
- **Затрагиваемые сущности:** FLOOR CEILING NEAREST; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `CRITICAL`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.4`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-029 — Python PASS versus MT5 NOT_RUN

- **ID:** `HSB-DOC-CONFLICT-029`
- **Краткое название:** Python PASS versus MT5 NOT_RUN
- **Категория:** `TEST_EVIDENCE`
- **Подкатегория:** Python PASS versus MT5 NOT_RUN
- **Сторона A:** `Docs/STAGE_1_2_4_1_EVIDENCE_RU.md`; раздел/контекст «Python PASS versus MT5 NOT_RUN»; фрагмент: `Python/static PASS`.
- **Сторона B:** `Docs/HYBRID_SPLIT_BIG_METAEDITOR_COMPILE.md`; раздел/контекст «Python PASS versus MT5 NOT_RUN»; фрагмент: `MetaEditor/MQL5 NOT_RUN`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `DIFFERENT_EVIDENCE_LEVEL`
- **Затрагиваемые сущности:** Python PASS versus MT5 NOT_RUN; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `INFORMATIONAL`
- **Статус решения:** `DEFERRED_TO_STAGE_3_1_8`
- **Требуется решение пользователя:** `NO`
- **Рекомендуемый этап разрешения:** `3.1.8`
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-030 — Production Ready versus missing broker evidence

- **ID:** `HSB-DOC-CONFLICT-030`
- **Краткое название:** Production Ready versus missing broker evidence
- **Категория:** `READINESS`
- **Подкатегория:** Production Ready versus missing broker evidence
- **Сторона A:** `Docs/BIG_SMALL_PRODUCTION_READINESS_REPORT_RU.md`; раздел/контекст «Production Ready versus missing broker evidence»; фрагмент: `REAL_TRADING_ALLOWED=NO`.
- **Сторона B:** `Docs/FULL_AUDIT_REPORT.md`; раздел/контекст «Production Ready versus missing broker evidence»; фрагмент: `static Verdict PASS`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `DIFFERENT_EVIDENCE_LEVEL`
- **Затрагиваемые сущности:** Production Ready versus missing broker evidence; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `CRITICAL`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.8`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-031 — Legacy Split Hybrid terminology

- **ID:** `HSB-DOC-CONFLICT-031`
- **Краткое название:** Legacy Split Hybrid terminology
- **Категория:** `LEGACY_MIXING`
- **Подкатегория:** Legacy Split Hybrid terminology
- **Сторона A:** `Docs/MANUAL.md`; раздел/контекст «Legacy Split Hybrid terminology»; фрагмент: `Legacy Big/Small/Far`.
- **Сторона B:** `Docs/HYBRID_SPLIT_BIG_COMPLETE_MANUAL_RU.md`; раздел/контекст «Legacy Split Hybrid terminology»; фрагмент: `Hybrid Core/Trend/SmallBase`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `LEGACY_CONTAMINATION`
- **Затрагиваемые сущности:** Legacy Split Hybrid terminology; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `BLOCKER`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.3`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-032 — Split test plan duplicate

- **ID:** `HSB-DOC-CONFLICT-032`
- **Краткое название:** Split test plan duplicate
- **Категория:** `DUPLICATION`
- **Подкатегория:** Split test plan duplicate
- **Сторона A:** `Docs/HYBRID_SPLIT_BIG_COMPLETE_MANUAL_RU.md`; раздел/контекст «Split test plan duplicate»; фрагмент: `complete manual claim`.
- **Сторона B:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`; раздел/контекст «Split test plan duplicate»; фрагмент: `separate MUST authority`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `DUPLICATE_AUTHORITY`
- **Затрагиваемые сущности:** Split test plan duplicate; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `LOW`
- **Статус решения:** `DEFERRED_TO_STAGE_3_1_8`
- **Требуется решение пользователя:** `NO`
- **Рекомендуемый этап разрешения:** `3.1.8`
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-033 — Reserve persistence

- **ID:** `HSB-DOC-CONFLICT-033`
- **Краткое название:** Reserve persistence
- **Категория:** `PERSISTENCE`
- **Подкатегория:** Reserve persistence
- **Сторона A:** `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`; раздел/контекст «Reserve persistence»; фрагмент: `Hybrid fingerprint/revision`.
- **Сторона B:** `Docs/SPLIT_BIG_EXACT_PERSISTENCE_REPORT_RU.md`; раздел/контекст «Reserve persistence»; фрагмент: `Split-only persistence evidence`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `AMBIGUOUS_DEFINITION`
- **Затрагиваемые сущности:** Reserve persistence; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `HIGH`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.6`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-034 — Exactly-once Reserve credit

- **ID:** `HSB-DOC-CONFLICT-034`
- **Краткое название:** Exactly-once Reserve credit
- **Категория:** `MONEY_LEDGER`
- **Подкатегория:** Exactly-once Reserve credit
- **Сторона A:** `Docs/HYBRID_SPLIT_BIG_MONEY_FLOW.md`; раздел/контекст «Exactly-once Reserve credit»; фрагмент: `confirmed ledger conservation`.
- **Сторона B:** `Docs/BASKET_RISK_CONTRACT_RU.md`; раздел/контекст «Exactly-once Reserve credit»; фрагмент: `expanded event-key/bucket contract`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `AMBIGUOUS_DEFINITION`
- **Затрагиваемые сущности:** Exactly-once Reserve credit; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `CRITICAL`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.5`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-035 — Partial fill

- **ID:** `HSB-DOC-CONFLICT-035`
- **Краткое название:** Partial fill
- **Категория:** `EXECUTION`
- **Подкатегория:** Partial fill
- **Сторона A:** `Docs/BASKET_RISK_CONTRACT_RU.md`; раздел/контекст «Partial fill»; фрагмент: `actual/reconciliation required`.
- **Сторона B:** `Docs/HYBRID_SPLIT_BIG_IMPLEMENTATION_REPORT_RU.md`; раздел/контекст «Partial fill»; фрагмент: `source claim without MT5 runtime proof`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `PLANNED_VS_EXECUTED`
- **Затрагиваемые сущности:** Partial fill; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `HIGH`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.6`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-036 — Retry idempotency

- **ID:** `HSB-DOC-CONFLICT-036`
- **Краткое название:** Retry idempotency
- **Категория:** `EXECUTION`
- **Подкатегория:** Retry idempotency
- **Сторона A:** `Docs/BASKET_RISK_CONTRACT_RU.md`; раздел/контекст «Retry idempotency»; фрагмент: `actual/reconciliation required`.
- **Сторона B:** `Docs/HYBRID_SPLIT_BIG_IMPLEMENTATION_REPORT_RU.md`; раздел/контекст «Retry idempotency»; фрагмент: `source claim without MT5 runtime proof`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `PLANNED_VS_EXECUTED`
- **Затрагиваемые сущности:** Retry idempotency; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `HIGH`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.6`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-037 — Restart reconciliation

- **ID:** `HSB-DOC-CONFLICT-037`
- **Краткое название:** Restart reconciliation
- **Категория:** `RECONCILIATION`
- **Подкатегория:** Restart reconciliation
- **Сторона A:** `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`; раздел/контекст «Restart reconciliation»; фрагмент: `Hybrid freshness/state`.
- **Сторона B:** `Docs/PERSISTENCE_AND_CLEAN_START_FINAL_REPORT_RU.md`; раздел/контекст «Restart reconciliation»; фрагмент: `Legacy RecoveryContext`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `AMBIGUOUS_DEFINITION`
- **Затрагиваемые сущности:** Restart reconciliation; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `HIGH`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.6`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-038 — Final Close partial execution

- **ID:** `HSB-DOC-CONFLICT-038`
- **Краткое название:** Final Close partial execution
- **Категория:** `FINAL_CLOSE`
- **Подкатегория:** Final Close partial execution
- **Сторона A:** `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`; раздел/контекст «Final Close partial execution»; фрагмент: `FINAL_CLOSE_PREVIEW_REQUIRED`.
- **Сторона B:** `Docs/MANUAL.md`; раздел/контекст «Final Close partial execution»; фрагмент: `FinalCloseAllowed near CLOSED_PROFIT`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `PREVIEW_VS_ACTUAL`
- **Затрагиваемые сущности:** Final Close partial execution; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `CRITICAL`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.6`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-039 — MaxHarvestLevels behavior

- **ID:** `HSB-DOC-CONFLICT-039`
- **Краткое название:** MaxHarvestLevels behavior
- **Категория:** `STATE_MACHINE`
- **Подкатегория:** MaxHarvestLevels behavior
- **Сторона A:** `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`; раздел/контекст «MaxHarvestLevels behavior»; фрагмент: `StateBefore/After revision`.
- **Сторона B:** `Docs/MANUAL.md`; раздел/контекст «MaxHarvestLevels behavior»; фрагмент: `Legacy terminal state namespace`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `AMBIGUOUS_DEFINITION`
- **Затрагиваемые сущности:** MaxHarvestLevels behavior; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `HIGH`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.6`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-040 — Reverse limit behavior

- **ID:** `HSB-DOC-CONFLICT-040`
- **Краткое название:** Reverse limit behavior
- **Категория:** `STATE_MACHINE`
- **Подкатегория:** Reverse limit behavior
- **Сторона A:** `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`; раздел/контекст «Reverse limit behavior»; фрагмент: `StateBefore/After revision`.
- **Сторона B:** `Docs/MANUAL.md`; раздел/контекст «Reverse limit behavior»; фрагмент: `Legacy terminal state namespace`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `AMBIGUOUS_DEFINITION`
- **Затрагиваемые сущности:** Reverse limit behavior; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `HIGH`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.6`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-041 — Invalid geometry behavior

- **ID:** `HSB-DOC-CONFLICT-041`
- **Краткое название:** Invalid geometry behavior
- **Категория:** `STATE_MACHINE`
- **Подкатегория:** Invalid geometry behavior
- **Сторона A:** `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`; раздел/контекст «Invalid geometry behavior»; фрагмент: `StateBefore/After revision`.
- **Сторона B:** `Docs/MANUAL.md`; раздел/контекст «Invalid geometry behavior»; фрагмент: `Legacy terminal state namespace`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `AMBIGUOUS_DEFINITION`
- **Затрагиваемые сущности:** Invalid geometry behavior; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `HIGH`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.6`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-042 — Basket Risk preview versus execution

- **ID:** `HSB-DOC-CONFLICT-042`
- **Краткое название:** Basket Risk preview versus execution
- **Категория:** `RISK`
- **Подкатегория:** Basket Risk preview versus execution
- **Сторона A:** `Docs/BASKET_RISK_CONTRACT_RU.md`; раздел/контекст «Basket Risk preview versus execution»; фрагмент: `Cycle/Account/freshness gates`.
- **Сторона B:** `Docs/HYBRID_SPLIT_BIG_THREE_LAWS_MATH_MANUAL_RU.md`; раздел/контекст «Basket Risk preview versus execution»; фрагмент: `analytical laws only`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `AMBIGUOUS_DEFINITION`
- **Затрагиваемые сущности:** Basket Risk preview versus execution; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `HIGH`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.8`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-043 — Cycle versus account risk

- **ID:** `HSB-DOC-CONFLICT-043`
- **Краткое название:** Cycle versus account risk
- **Категория:** `RISK`
- **Подкатегория:** Cycle versus account risk
- **Сторона A:** `Docs/BASKET_RISK_CONTRACT_RU.md`; раздел/контекст «Cycle versus account risk»; фрагмент: `Cycle/Account/freshness gates`.
- **Сторона B:** `Docs/HYBRID_SPLIT_BIG_THREE_LAWS_MATH_MANUAL_RU.md`; раздел/контекст «Cycle versus account risk»; фрагмент: `analytical laws only`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `AMBIGUOUS_DEFINITION`
- **Затрагиваемые сущности:** Cycle versus account risk; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `HIGH`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.8`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-044 — Terminal-safe versus mathematically-safe

- **ID:** `HSB-DOC-CONFLICT-044`
- **Краткое название:** Terminal-safe versus mathematically-safe
- **Категория:** `RISK`
- **Подкатегория:** Terminal-safe versus mathematically-safe
- **Сторона A:** `Docs/BASKET_RISK_CONTRACT_RU.md`; раздел/контекст «Terminal-safe versus mathematically-safe»; фрагмент: `Cycle/Account/freshness gates`.
- **Сторона B:** `Docs/HYBRID_SPLIT_BIG_THREE_LAWS_MATH_MANUAL_RU.md`; раздел/контекст «Terminal-safe versus mathematically-safe»; фрагмент: `analytical laws only`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `AMBIGUOUS_DEFINITION`
- **Затрагиваемые сущности:** Terminal-safe versus mathematically-safe; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `CRITICAL`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.8`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

### HSB-DOC-CONFLICT-045 — Source-of-truth competition

- **ID:** `HSB-DOC-CONFLICT-045`
- **Краткое название:** Source-of-truth competition
- **Категория:** `DUPLICATION`
- **Подкатегория:** Source-of-truth competition
- **Сторона A:** `Docs/HYBRID_SPLIT_BIG_COMPLETE_MANUAL_RU.md`; раздел/контекст «Source-of-truth competition»; фрагмент: `complete manual claim`.
- **Сторона B:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`; раздел/контекст «Source-of-truth competition»; фрагмент: `separate MUST authority`.
- **Суть противоречия:** различаются value, scope, evidence либо semantics; нормативная сторона не выбирается.
- **Тип расхождения:** `DUPLICATE_AUTHORITY`
- **Затрагиваемые сущности:** Source-of-truth competition; lots, money, geometry, state или execution.
- **Влияние на систему:** возможны разные lots, ledger, geometry, states, margin, recovery, final close, restart или broker execution.
- **Критичность:** `BLOCKER`
- **Статус решения:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Рекомендуемый этап разрешения:** `3.1.8`
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`
- **Примечание:** runtime change запрещён; требуется cross-check formulas, units, profile и evidence.

## 4. Индекс конфликтов по документам

### `Docs/BASKET_RISK_CONTRACT_RU.md`
- HSB-DOC-CONFLICT-014
- HSB-DOC-CONFLICT-016
- HSB-DOC-CONFLICT-023
- HSB-DOC-CONFLICT-027
- HSB-DOC-CONFLICT-034
- HSB-DOC-CONFLICT-035
- HSB-DOC-CONFLICT-036
- HSB-DOC-CONFLICT-042
- HSB-DOC-CONFLICT-043
- HSB-DOC-CONFLICT-044

### `Docs/BIG_SCENARIO_FULL_AUDIT.md`
- HSB-DOC-CONFLICT-028

### `Docs/BIG_SMALL_PRODUCTION_READINESS_REPORT_RU.md`
- HSB-DOC-CONFLICT-030

### `Docs/FULL_AUDIT_REPORT.md`
- HSB-DOC-CONFLICT-009
- HSB-DOC-CONFLICT-010
- HSB-DOC-CONFLICT-011
- HSB-DOC-CONFLICT-012
- HSB-DOC-CONFLICT-030

### `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`
- HSB-DOC-CONFLICT-017
- HSB-DOC-CONFLICT-026
- HSB-DOC-CONFLICT-033
- HSB-DOC-CONFLICT-037
- HSB-DOC-CONFLICT-038
- HSB-DOC-CONFLICT-039
- HSB-DOC-CONFLICT-040
- HSB-DOC-CONFLICT-041

### `Docs/HYBRID_SPLIT_BIG_COMPLETE_MANUAL_RU.md`
- HSB-DOC-CONFLICT-031
- HSB-DOC-CONFLICT-032
- HSB-DOC-CONFLICT-045

### `Docs/HYBRID_SPLIT_BIG_FORMULA_REFERENCE.md`
- HSB-DOC-CONFLICT-013
- HSB-DOC-CONFLICT-021

### `Docs/HYBRID_SPLIT_BIG_IMPLEMENTATION_REPORT_RU.md`
- HSB-DOC-CONFLICT-016
- HSB-DOC-CONFLICT-027
- HSB-DOC-CONFLICT-035
- HSB-DOC-CONFLICT-036

### `Docs/HYBRID_SPLIT_BIG_METAEDITOR_COMPILE.md`
- HSB-DOC-CONFLICT-029

### `Docs/HYBRID_SPLIT_BIG_MONEY_FLOW.md`
- HSB-DOC-CONFLICT-008
- HSB-DOC-CONFLICT-014
- HSB-DOC-CONFLICT-015
- HSB-DOC-CONFLICT-025
- HSB-DOC-CONFLICT-034

### `Docs/HYBRID_SPLIT_BIG_STATE_TRANSITION_TABLE.md`
- HSB-DOC-CONFLICT-018
- HSB-DOC-CONFLICT-019
- HSB-DOC-CONFLICT-024

### `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`
- HSB-DOC-CONFLICT-009
- HSB-DOC-CONFLICT-010
- HSB-DOC-CONFLICT-011
- HSB-DOC-CONFLICT-012
- HSB-DOC-CONFLICT-020
- HSB-DOC-CONFLICT-022
- HSB-DOC-CONFLICT-028
- HSB-DOC-CONFLICT-032
- HSB-DOC-CONFLICT-045

### `Docs/HYBRID_SPLIT_BIG_THREE_LAWS_MATH_MANUAL_RU.md`
- HSB-DOC-CONFLICT-023
- HSB-DOC-CONFLICT-042
- HSB-DOC-CONFLICT-043
- HSB-DOC-CONFLICT-044

### `Docs/MANUAL.md`
- HSB-DOC-CONFLICT-001
- HSB-DOC-CONFLICT-002
- HSB-DOC-CONFLICT-003
- HSB-DOC-CONFLICT-004
- HSB-DOC-CONFLICT-005
- HSB-DOC-CONFLICT-006
- HSB-DOC-CONFLICT-007
- HSB-DOC-CONFLICT-008
- HSB-DOC-CONFLICT-013
- HSB-DOC-CONFLICT-015
- HSB-DOC-CONFLICT-017
- HSB-DOC-CONFLICT-018
- HSB-DOC-CONFLICT-019
- HSB-DOC-CONFLICT-020
- HSB-DOC-CONFLICT-021
- HSB-DOC-CONFLICT-022
- HSB-DOC-CONFLICT-024
- HSB-DOC-CONFLICT-025
- HSB-DOC-CONFLICT-026
- HSB-DOC-CONFLICT-031
- HSB-DOC-CONFLICT-038
- HSB-DOC-CONFLICT-039
- HSB-DOC-CONFLICT-040
- HSB-DOC-CONFLICT-041

### `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md`
- HSB-DOC-CONFLICT-001
- HSB-DOC-CONFLICT-002
- HSB-DOC-CONFLICT-003
- HSB-DOC-CONFLICT-004
- HSB-DOC-CONFLICT-005
- HSB-DOC-CONFLICT-006
- HSB-DOC-CONFLICT-007

### `Docs/PERSISTENCE_AND_CLEAN_START_FINAL_REPORT_RU.md`
- HSB-DOC-CONFLICT-037

### `Docs/SPLIT_BIG_EXACT_PERSISTENCE_REPORT_RU.md`
- HSB-DOC-CONFLICT-033

### `Docs/STAGE_1_2_4_1_EVIDENCE_RU.md`
- HSB-DOC-CONFLICT-029

## 5. Индекс конфликтов по подсистемам

- **Terminology:** HSB-DOC-CONFLICT-031
- **Parameters:** HSB-DOC-CONFLICT-031
- **Geometry:** HSB-DOC-CONFLICT-020, HSB-DOC-CONFLICT-022, HSB-DOC-CONFLICT-041
- **Big Scenario:** HSB-DOC-CONFLICT-001, HSB-DOC-CONFLICT-003, HSB-DOC-CONFLICT-004, HSB-DOC-CONFLICT-021, HSB-DOC-CONFLICT-022, HSB-DOC-CONFLICT-024
- **Small Scenario:** HSB-DOC-CONFLICT-002, HSB-DOC-CONFLICT-003, HSB-DOC-CONFLICT-004, HSB-DOC-CONFLICT-007, HSB-DOC-CONFLICT-018, HSB-DOC-CONFLICT-019, HSB-DOC-CONFLICT-023, HSB-DOC-CONFLICT-024
- **Reserve:** HSB-DOC-CONFLICT-006, HSB-DOC-CONFLICT-007, HSB-DOC-CONFLICT-008, HSB-DOC-CONFLICT-009, HSB-DOC-CONFLICT-015, HSB-DOC-CONFLICT-025, HSB-DOC-CONFLICT-033, HSB-DOC-CONFLICT-034
- **RecoveryPL:** HSB-DOC-CONFLICT-009, HSB-DOC-CONFLICT-010, HSB-DOC-CONFLICT-011, HSB-DOC-CONFLICT-012
- **Partial Far:** HSB-DOC-CONFLICT-008, HSB-DOC-CONFLICT-019, HSB-DOC-CONFLICT-035, HSB-DOC-CONFLICT-038
- **Final Close:** HSB-DOC-CONFLICT-017, HSB-DOC-CONFLICT-038
- **StateMachine:** HSB-DOC-CONFLICT-037
- **Execution:** HSB-DOC-CONFLICT-016, HSB-DOC-CONFLICT-027, HSB-DOC-CONFLICT-035, HSB-DOC-CONFLICT-036, HSB-DOC-CONFLICT-038, HSB-DOC-CONFLICT-042
- **Persistence:** HSB-DOC-CONFLICT-033
- **Reconciliation:** HSB-DOC-CONFLICT-037
- **Basket Risk:** HSB-DOC-CONFLICT-042
- **Testing:** HSB-DOC-CONFLICT-022
- **Production Readiness:** HSB-DOC-CONFLICT-030
- **Legacy/Split/Hybrid separation:** HSB-DOC-CONFLICT-001

## 6. Матрица документов-авторитетов

| Тема | Конкурирующие документы | Вес | Конфликт | ID | Действие |
|---|---|---|---|---|---|
| Big lot | manual/invariants/formula/report | preliminary/mixed | YES | HSB-DOC-CONFLICT-001 и связанные | Не выбирать authority |
| Small lot | manual/invariants/formula/report | preliminary/mixed | YES | HSB-DOC-CONFLICT-002 и связанные | Не выбирать authority |
| Big close | manual/invariants/formula/report | preliminary/mixed | YES | HSB-DOC-CONFLICT-003 и связанные | Не выбирать authority |
| Small close | manual/invariants/formula/report | preliminary/mixed | YES | HSB-DOC-CONFLICT-004 и связанные | Не выбирать authority |
| Far partial | manual/invariants/formula/report | preliminary/mixed | YES | HSB-DOC-CONFLICT-005 и связанные | Не выбирать authority |
| New Far | manual/invariants/formula/report | preliminary/mixed | YES | HSB-DOC-CONFLICT-006 и связанные | Не выбирать authority |
| Reserve allocation | manual/invariants/formula/report | preliminary/mixed | YES | HSB-DOC-CONFLICT-007 и связанные | Не выбирать authority |
| RecoveryPL | manual/invariants/formula/report | preliminary/mixed | YES | HSB-DOC-CONFLICT-008 и связанные | Не выбирать authority |
| ReserveCoverage | manual/invariants/formula/report | preliminary/mixed | YES | HSB-DOC-CONFLICT-009 и связанные | Не выбирать authority |
| Final Close | manual/invariants/formula/report | preliminary/mixed | YES | HSB-DOC-CONFLICT-010 и связанные | Не выбирать authority |
| Reverse | manual/invariants/formula/report | preliminary/mixed | YES | HSB-DOC-CONFLICT-011 и связанные | Не выбирать authority |
| State transition | manual/invariants/formula/report | preliminary/mixed | YES | HSB-DOC-CONFLICT-012 и связанные | Не выбирать authority |
| Restart | manual/invariants/formula/report | preliminary/mixed | YES | HSB-DOC-CONFLICT-013 и связанные | Не выбирать authority |
| Execution confirmation | manual/invariants/formula/report | preliminary/mixed | YES | HSB-DOC-CONFLICT-014 и связанные | Не выбирать authority |
| Broker margin | manual/invariants/formula/report | preliminary/mixed | YES | HSB-DOC-CONFLICT-015 и связанные | Не выбирать authority |
| Test readiness | manual/invariants/formula/report | preliminary/mixed | YES | HSB-DOC-CONFLICT-016 и связанные | Не выбирать authority |

## 7. Duplicate clusters

### HSB-DOC-DUPLICATE-001

- **Список файлов/тема:** Hybrid authorities.
- **Совпадающие разделы:** terminology, formulas, gates или evidence.
- **Различающиеся части:** scope, status, profiles и detail.
- **Назначение:** manual/proof/report/test по своему scope.
- **Риск параллельной нормативности:** разные implementations. 
- **Связанные conflict-ID:** HSB-DOC-CONFLICT-001 и смежные.

### HSB-DOC-DUPLICATE-002

- **Список файлов/тема:** Three Laws proofs.
- **Совпадающие разделы:** terminology, formulas, gates или evidence.
- **Различающиеся части:** scope, status, profiles и detail.
- **Назначение:** manual/proof/report/test по своему scope.
- **Риск параллельной нормативности:** разные implementations. 
- **Связанные conflict-ID:** HSB-DOC-CONFLICT-008 и смежные.

### HSB-DOC-DUPLICATE-003

- **Список файлов/тема:** Split test plans.
- **Совпадающие разделы:** terminology, formulas, gates или evidence.
- **Различающиеся части:** scope, status, profiles и detail.
- **Назначение:** manual/proof/report/test по своему scope.
- **Риск параллельной нормативности:** разные implementations. 
- **Связанные conflict-ID:** HSB-DOC-CONFLICT-015 и смежные.

### HSB-DOC-DUPLICATE-004

- **Список файлов/тема:** Legacy/Split/Hybrid manuals.
- **Совпадающие разделы:** terminology, formulas, gates или evidence.
- **Различающиеся части:** scope, status, profiles и detail.
- **Назначение:** manual/proof/report/test по своему scope.
- **Риск параллельной нормативности:** разные implementations. 
- **Связанные conflict-ID:** HSB-DOC-CONFLICT-022 и смежные.

### HSB-DOC-DUPLICATE-005

- **Список файлов/тема:** Readiness reports.
- **Совпадающие разделы:** terminology, formulas, gates или evidence.
- **Различающиеся части:** scope, status, profiles и detail.
- **Назначение:** manual/proof/report/test по своему scope.
- **Риск параллельной нормативности:** разные implementations. 
- **Связанные conflict-ID:** HSB-DOC-CONFLICT-029 и смежные.

### HSB-DOC-DUPLICATE-006

- **Список файлов/тема:** Basket Risk documents.
- **Совпадающие разделы:** terminology, formulas, gates или evidence.
- **Различающиеся части:** scope, status, profiles и detail.
- **Назначение:** manual/proof/report/test по своему scope.
- **Риск параллельной нормативности:** разные implementations. 
- **Связанные conflict-ID:** HSB-DOC-CONFLICT-036 и смежные.

## 8. Покрытие 45 обязательных тем

| № | Тема | Результат | ID |
|---:|---|---|---|
| 1 | BigRatio values | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-001 |
| 2 | SmallRatio values | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-002 |
| 3 | CloseBigOnSmall values | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-003 |
| 4 | RemainBigOnSmall values | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-004 |
| 5 | CloseFarShare values | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-005 |
| 6 | ReserveShare values | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-006 |
| 7 | SmallReserveShare values | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-007 |
| 8 | Reserve in Partial Far | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-008 |
| 9 | RecoveryPL includes Reserve | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-009 |
| 10 | RecoveryPL includes Initial Plus | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-010 |
| 11 | RecoveryPL Symbol filter | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-011 |
| 12 | RecoveryPL Magic filter | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-012 |
| 13 | Gross versus Net Profit | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-013 |
| 14 | Commission swap fee | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-014 |
| 15 | Projected versus Realized Reserve | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-015 |
| 16 | Planned versus actual close result | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-016 |
| 17 | Final Close preview versus actual success | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-017 |
| 18 | Small close trigger | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-018 |
| 19 | Old Far full versus partial close | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-019 |
| 20 | New Far source | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-020 |
| 21 | Next Big base | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-021 |
| 22 | new Big less than old Far | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-022 |
| 23 | Negative Small Reverse Net | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-023 |
| 24 | Small Far Big close order | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-024 |
| 25 | Reserve credit order | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-025 |
| 26 | State transition order | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-026 |
| 27 | Requested versus executed volume | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-027 |
| 28 | FLOOR CEILING NEAREST | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-028 |
| 29 | Python PASS versus MT5 NOT_RUN | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-029 |
| 30 | Production Ready versus missing broker evidence | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-030 |
| 31 | Legacy Split Hybrid terminology | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-031 |
| 32 | Split test plan duplicate | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-032 |
| 33 | Reserve persistence | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-033 |
| 34 | Exactly-once Reserve credit | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-034 |
| 35 | Partial fill | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-035 |
| 36 | Retry idempotency | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-036 |
| 37 | Restart reconciliation | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-037 |
| 38 | Final Close partial execution | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-038 |
| 39 | MaxHarvestLevels behavior | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-039 |
| 40 | Reverse limit behavior | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-040 |
| 41 | Invalid geometry behavior | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-041 |
| 42 | Basket Risk preview versus execution | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-042 |
| 43 | Cycle versus account risk | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-043 |
| 44 | Terminal-safe versus mathematically-safe | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-044 |
| 45 | Source-of-truth competition | CONFLICT_REGISTERED | HSB-DOC-CONFLICT-045 |

## 9. Authority coverage

Проверены 13 NORMATIVE: Basket Risk Contract, Outcome Truth Table, Temporal Model, Complete Manual, Formula Reference, Gate Graph, Logic Design, Money Flow, MQL5 Normative Algorithms, State Transition Table, System Invariants, Three Laws Manual, Trace Spec. Проверены 2 CONFLICTING: Admin Decisions Required и Open Questions.

```text
NORMATIVE_DOCS_REVIEWED=13
CONFLICTING_DOCS_REVIEWED=2
AUTHORITY_REVIEW_COVERAGE=PASS
```

## 10. Статистика

```text
TOTAL_CONFLICTS=45
BLOCKER=7
CRITICAL=17
HIGH=19
MEDIUM=0
LOW=1
INFORMATIONAL=1
NEEDS_USER_DECISION=43
OPEN=0
DEFERRED=2
BUSINESS_CONFLICTS_AUTO_RESOLVED=0
MANDATORY_CONFLICT_TOPICS=45
MANDATORY_TOPICS_REVIEWED=45
MANDATORY_TOPICS_OMITTED=0
STAGE_3_1_2_STATUS=PASS
```

### Category statistics
- `DUPLICATION`: 2
- `EXECUTION`: 4
- `FINAL_CLOSE`: 2
- `FORMULA`: 2
- `GEOMETRY`: 2
- `LEGACY_MIXING`: 1
- `MONEY_LEDGER`: 2
- `PARAMETER`: 7
- `PERSISTENCE`: 1
- `READINESS`: 1
- `RECONCILIATION`: 1
- `RECOVERY_PL`: 4
- `RESERVE`: 3
- `RISK`: 4
- `ROUNDING`: 1
- `SMALL_SCENARIO`: 3
- `STATE_MACHINE`: 4
- `TEST_EVIDENCE`: 1

Код, параметры, MQL5, Python, Tests, Tools, Sets, workflows и runtime не менялись. Этап 3.1.3 не выполнялся; source of truth и production candidate не создавались.

Ожидается подтверждение пользователя для перехода к следующему пункту/этапу.
