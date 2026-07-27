# Исправление Этапа 3.1.2 — доказательный реестр конфликтов Hybrid Split Big

Статус: `PASS`
Parent SHA: `79676a58afaf8e926f42aeed22e4d99806b10acc`

## Ограничение полномочий реестра

> Настоящий реестр является регистрационным и аналитическим документом. Он не выбирает нормативную сторону конфликта, не изменяет бизнес-логику, не назначает production candidate и не создаёт окончательный source of truth. Все бизнес-решения, влияющие на формулы, коэффициенты, состояния, денежные потоки, исполнение ордеров или завершение цикла, требуют отдельного решения пользователя.

Каждая обязательная тема проверена по фактическим фрагментам. Если стороны описывают разные scope/этапы одной совместимой цепочки, запись получает `NO_DIRECT_CONFLICT_FOUND`, а не искусственный конфликт.

## 1. Сводная таблица

| ID | Тема | Результат проверки | Критичность | User decision | Этап |
|---|---|---|---|---|---|
| HSB-DOC-CONFLICT-001 | BigRatio values | PARAMETER_PROFILE_CONFLICT | BLOCKER | YES | 3.1.7 |
| HSB-DOC-CONFLICT-002 | SmallRatio values | PARAMETER_PROFILE_CONFLICT | BLOCKER | YES | 3.1.7 |
| HSB-DOC-CONFLICT-003 | CloseBigOnSmall values | PARAMETER_PROFILE_CONFLICT | BLOCKER | YES | 3.1.7 |
| HSB-DOC-CONFLICT-004 | RemainBigOnSmall values | PARAMETER_PROFILE_CONFLICT | BLOCKER | YES | 3.1.7 |
| HSB-DOC-CONFLICT-005 | CloseFarShare values | PARAMETER_PROFILE_CONFLICT | BLOCKER | YES | 3.1.7 |
| HSB-DOC-CONFLICT-006 | ReserveShare values | PARAMETER_PROFILE_CONFLICT | BLOCKER | YES | 3.1.7 |
| HSB-DOC-CONFLICT-007 | SmallReserveShare values | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO | не требуется; сохранить результат проверки |
| HSB-DOC-CONFLICT-008 | Reserve in Partial Far | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO | не требуется; сохранить результат проверки |
| HSB-DOC-CONFLICT-009 | RecoveryPL includes Reserve | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO | не требуется; сохранить результат проверки |
| HSB-DOC-CONFLICT-010 | RecoveryPL includes Initial Plus | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO | не требуется; сохранить результат проверки |
| HSB-DOC-CONFLICT-011 | RecoveryPL Symbol filter | MISSING_DEFINITION | HIGH | NO | 3.1.3–3.1.6 по теме |
| HSB-DOC-CONFLICT-012 | RecoveryPL Magic filter | MISSING_DEFINITION | HIGH | NO | 3.1.3–3.1.6 по теме |
| HSB-DOC-CONFLICT-013 | Gross versus Net Profit | FORMULA_CONFLICT | CRITICAL | YES | 3.1.4 |
| HSB-DOC-CONFLICT-014 | Commission swap fee | MISSING_DEFINITION | HIGH | NO | 3.1.3–3.1.6 по теме |
| HSB-DOC-CONFLICT-015 | Projected versus Realized Reserve | SCOPE_CONFLICT | MEDIUM | NO | 3.1.3–3.1.8 по теме |
| HSB-DOC-CONFLICT-016 | Planned versus actual close result | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO | не требуется; сохранить результат проверки |
| HSB-DOC-CONFLICT-017 | Final Close preview versus actual success | AMBIGUITY | HIGH | NO | 3.1.3–3.1.6 по теме |
| HSB-DOC-CONFLICT-018 | Small close trigger | SCOPE_CONFLICT | MEDIUM | NO | 3.1.3–3.1.8 по теме |
| HSB-DOC-CONFLICT-019 | Old Far full versus partial close | SCOPE_CONFLICT | MEDIUM | NO | 3.1.3–3.1.8 по теме |
| HSB-DOC-CONFLICT-020 | New Far source | AUTHORITY_CONFLICT | BLOCKER | YES | 3.1.8 |
| HSB-DOC-CONFLICT-021 | Next Big base | SCOPE_CONFLICT | MEDIUM | NO | 3.1.3–3.1.8 по теме |
| HSB-DOC-CONFLICT-022 | new Big less than old Far | MISSING_DEFINITION | HIGH | NO | 3.1.3–3.1.6 по теме |
| HSB-DOC-CONFLICT-023 | Negative Small Reverse Net | MISSING_DEFINITION | HIGH | NO | 3.1.3–3.1.6 по теме |
| HSB-DOC-CONFLICT-024 | Small Far Big close order | ORDERING_CONFLICT | CRITICAL | YES | 3.1.6 |
| HSB-DOC-CONFLICT-025 | Reserve credit order | AMBIGUITY | HIGH | NO | 3.1.3–3.1.6 по теме |
| HSB-DOC-CONFLICT-026 | State transition order | MISSING_DEFINITION | HIGH | NO | 3.1.3–3.1.6 по теме |
| HSB-DOC-CONFLICT-027 | Requested versus executed volume | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO | не требуется; сохранить результат проверки |
| HSB-DOC-CONFLICT-028 | FLOOR CEILING NEAREST | FORMULA_CONFLICT | CRITICAL | YES | 3.1.4 |
| HSB-DOC-CONFLICT-029 | Python PASS versus MT5 NOT_RUN | EVIDENCE_GAP | INFORMATIONAL | NO | последующие MetaEditor/MT5 проверки |
| HSB-DOC-CONFLICT-030 | Production readiness versus missing broker evidence | EVIDENCE_GAP | INFORMATIONAL | NO | последующие MT5/broker проверки |
| HSB-DOC-CONFLICT-031 | Legacy Split Hybrid terminology | AUTHORITY_CONFLICT | BLOCKER | YES | 3.1.8 |
| HSB-DOC-CONFLICT-032 | Split test plan duplicate | DUPLICATION_WITH_DIFFERENCES | LOW | NO | 3.1.8 |
| HSB-DOC-CONFLICT-033 | Reserve persistence | SCOPE_CONFLICT | MEDIUM | NO | 3.1.3–3.1.8 по теме |
| HSB-DOC-CONFLICT-034 | Exactly-once Reserve credit | AMBIGUITY | HIGH | NO | 3.1.3–3.1.6 по теме |
| HSB-DOC-CONFLICT-035 | Partial fill | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO | не требуется; требуется runtime validation |
| HSB-DOC-CONFLICT-036 | Retry idempotency | SCOPE_CONFLICT | MEDIUM | NO | 3.1.3–3.1.8 по теме |
| HSB-DOC-CONFLICT-037 | Restart reconciliation | SCOPE_CONFLICT | MEDIUM | NO | 3.1.3–3.1.8 по теме |
| HSB-DOC-CONFLICT-038 | Final Close partial execution | AMBIGUITY | HIGH | NO | 3.1.3–3.1.6 по теме |
| HSB-DOC-CONFLICT-039 | MaxHarvestLevels behavior | ORDERING_CONFLICT | CRITICAL | YES | 3.1.6 |
| HSB-DOC-CONFLICT-040 | Reverse limit behavior | MISSING_DEFINITION | HIGH | NO | 3.1.3–3.1.6 по теме |
| HSB-DOC-CONFLICT-041 | Invalid geometry behavior | MISSING_DEFINITION | HIGH | NO | 3.1.3–3.1.6 по теме |
| HSB-DOC-CONFLICT-042 | Basket Risk preview versus execution | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO | не требуется; сохранить результат проверки |
| HSB-DOC-CONFLICT-043 | Cycle versus account risk | MISSING_DEFINITION | HIGH | NO | 3.1.3–3.1.6 по теме |
| HSB-DOC-CONFLICT-044 | Terminal-safe versus mathematically-safe | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO | не требуется; сохранить результат проверки |
| HSB-DOC-CONFLICT-045 | Source-of-truth competition | AUTHORITY_CONFLICT | BLOCKER | YES | 3.1.8 |

## 2. Доказательные записи

### HSB-DOC-CONFLICT-001 — BigRatio values

- **Классификация результата:** `PARAMETER_PROFILE_CONFLICT`
- **Категория:** `PARAMETER`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «2. Параметры»
- **Подраздел:** строка 23 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `BigRatio = 1.30`
- **Конкретное утверждение:** BigRatio = 1.30.
- **Конкретное значение:** см. таблицу значений ниже
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md`
- **Раздел:** «Текущие входные параметры»
- **Подраздел:** строка 27 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `- базовые лоты/распределение: `StartLot=0.10`, `BigRatio=1.15`, `SmallRatio=0.25`, `CloseBigOnSmall=0.40`, `RemainBigOnSmall=0.60`, `CloseFarShare=0.10`, `ReserveShare=0.90`, `SmallReserveShare=0.05`;`
- **Конкретное утверждение:** - базовые лоты/распределение: `StartLot=0.10`, `BigRatio=1.15`, `SmallRatio=0.25`, `CloseBigOnSmall=0.40`, `RemainBigOnSmall=0.60`, `CloseFarShare=0.10`, `ReserveShare=0.90`, `SmallReserveShare=0.05`;.
- **Конкретное значение:** см. таблицу значений ниже
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Все найденные документированные значения

| Значение | Документ | Раздел | Профиль | Назначение | Preliminary authority |
|---:|---|---|---|---|---|
| 1.15 | BIG_SCENARIO_ENGINEERING_AUDIT.md | 6. Numeric scenario used by the trace | test/report | Документированное значение | предварительный |
| 1.11 | BIG_SCENARIO_FULL_AUDIT.md | 13. MT5 Strategy Tester invalidation addendum | test/report | Документированное значение | предварительный |
| 1.15 | BIG_SMALL_COMPLETION_BASELINE_RU.md | Defaults и режимы | baseline | Документированное значение | предварительный |
| 1.30 | MANUAL.md | 2. Параметры | manual/profile | Документированное значение | предварительный |
| 1.30 | MANUAL.md | Python Candidate 50/50 | manual/profile | Документированное значение | предварительный |
| 1.20 | MANUAL.md | Risk Compression Reverse | manual/profile | Документированное значение | предварительный |
| 1.20 | MANUAL.md | V2.4.1 RiskGate Architecture Fix | manual/profile | Документированное значение | предварительный |
| 1.15 | MONEY_MODEL_COMPLETION_BASELINE_RU.md | Текущие входные параметры | baseline | Документированное значение | предварительный |
| 1.14 | TEST_PLAN.md | ATR Geometry Runtime Validation | test/report | Документированное значение | предварительный |

#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/MANUAL.md` и `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md` без profile/scope discriminator даёт два разных правила для темы «BigRatio values»; единая production-норма не определена.
- **Статус:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Этап разрешения:** `3.1.7`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `BLOCKER` выбран потому, что тема «BigRatio values» блокирует следующий нормативный документ или способна изменить lot/money/state.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-002 — SmallRatio values

- **Классификация результата:** `PARAMETER_PROFILE_CONFLICT`
- **Категория:** `PARAMETER`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «2. Параметры»
- **Подраздел:** строка 24 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `SmallRatio = 0.37`
- **Конкретное утверждение:** SmallRatio = 0.37.
- **Конкретное значение:** см. таблицу значений ниже
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md`
- **Раздел:** «Текущие входные параметры»
- **Подраздел:** строка 27 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `- базовые лоты/распределение: `StartLot=0.10`, `BigRatio=1.15`, `SmallRatio=0.25`, `CloseBigOnSmall=0.40`, `RemainBigOnSmall=0.60`, `CloseFarShare=0.10`, `ReserveShare=0.90`, `SmallReserveShare=0.05`;`
- **Конкретное утверждение:** - базовые лоты/распределение: `StartLot=0.10`, `BigRatio=1.15`, `SmallRatio=0.25`, `CloseBigOnSmall=0.40`, `RemainBigOnSmall=0.60`, `CloseFarShare=0.10`, `ReserveShare=0.90`, `SmallReserveShare=0.05`;.
- **Конкретное значение:** см. таблицу значений ниже
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Все найденные документированные значения

| Значение | Документ | Раздел | Профиль | Назначение | Preliminary authority |
|---:|---|---|---|---|---|
| 0.25 | BIG_SCENARIO_ENGINEERING_AUDIT.md | 6. Numeric scenario used by the trace | test/report | Документированное значение | предварительный |
| 0.25 | BIG_SCENARIO_FULL_AUDIT.md | 13. MT5 Strategy Tester invalidation addendum | test/report | Документированное значение | предварительный |
| 0.25 | BIG_SMALL_COMPLETION_BASELINE_RU.md | Defaults и режимы | baseline | Документированное значение | предварительный |
| 0.37 | MANUAL.md | 2. Параметры | manual/profile | Документированное значение | предварительный |
| 0.36 | MANUAL.md | Python Candidate 50/50 | manual/profile | Документированное значение | предварительный |
| 0.35 | MANUAL.md | Risk Compression Reverse | manual/profile | Документированное значение | предварительный |
| 0.35 | MANUAL.md | V2.4.1 RiskGate Architecture Fix | manual/profile | Документированное значение | предварительный |
| 0.25 | MONEY_MODEL_COMPLETION_BASELINE_RU.md | Текущие входные параметры | baseline | Документированное значение | предварительный |
| 0.36 | TEST_PLAN.md | ATR Geometry Runtime Validation | test/report | Документированное значение | предварительный |

#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/MANUAL.md` и `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md` без profile/scope discriminator даёт два разных правила для темы «SmallRatio values»; единая production-норма не определена.
- **Статус:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Этап разрешения:** `3.1.7`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `BLOCKER` выбран потому, что тема «SmallRatio values» блокирует следующий нормативный документ или способна изменить lot/money/state.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-003 — CloseBigOnSmall values

- **Классификация результата:** `PARAMETER_PROFILE_CONFLICT`
- **Категория:** `PARAMETER`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «2. Параметры»
- **Подраздел:** строка 25 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `CloseBigOnSmall = 0.30`
- **Конкретное утверждение:** CloseBigOnSmall = 0.30.
- **Конкретное значение:** см. таблицу значений ниже
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md`
- **Раздел:** «Текущие входные параметры»
- **Подраздел:** строка 27 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `- базовые лоты/распределение: `StartLot=0.10`, `BigRatio=1.15`, `SmallRatio=0.25`, `CloseBigOnSmall=0.40`, `RemainBigOnSmall=0.60`, `CloseFarShare=0.10`, `ReserveShare=0.90`, `SmallReserveShare=0.05`;`
- **Конкретное утверждение:** - базовые лоты/распределение: `StartLot=0.10`, `BigRatio=1.15`, `SmallRatio=0.25`, `CloseBigOnSmall=0.40`, `RemainBigOnSmall=0.60`, `CloseFarShare=0.10`, `ReserveShare=0.90`, `SmallReserveShare=0.05`;.
- **Конкретное значение:** см. таблицу значений ниже
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Все найденные документированные значения

| Значение | Документ | Раздел | Профиль | Назначение | Preliminary authority |
|---:|---|---|---|---|---|
| 0.40 | BIG_SCENARIO_ENGINEERING_AUDIT.md | 6. Numeric scenario used by the trace | test/report | Документированное значение | предварительный |
| 0.30 | MANUAL.md | 2. Параметры | manual/profile | Документированное значение | предварительный |
| 0.35 | MANUAL.md | Python Candidate 50/50 | manual/profile | Документированное значение | предварительный |
| 0.35 | MANUAL.md | Risk Compression Reverse | manual/profile | Документированное значение | предварительный |
| 0.35 | MANUAL.md | V2.4.1 RiskGate Architecture Fix | manual/profile | Документированное значение | предварительный |
| 0.40 | MONEY_MODEL_COMPLETION_BASELINE_RU.md | Текущие входные параметры | baseline | Документированное значение | предварительный |

- **Проверка пары:** profiles должны проверять `CloseBigOnSmall + RemainBigOnSmall = 1`; документированные пары 0.30+0.70, 0.35+0.65 и 0.40+0.60 дают 1.00, но не являются одним production profile.

#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/MANUAL.md` и `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md` без profile/scope discriminator даёт два разных правила для темы «CloseBigOnSmall values»; единая production-норма не определена.
- **Статус:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Этап разрешения:** `3.1.7`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `BLOCKER` выбран потому, что тема «CloseBigOnSmall values» блокирует следующий нормативный документ или способна изменить lot/money/state.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-004 — RemainBigOnSmall values

- **Классификация результата:** `PARAMETER_PROFILE_CONFLICT`
- **Категория:** `PARAMETER`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «2. Параметры»
- **Подраздел:** строка 26 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `RemainBigOnSmall = 0.70`
- **Конкретное утверждение:** RemainBigOnSmall = 0.70.
- **Конкретное значение:** см. таблицу значений ниже
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md`
- **Раздел:** «Текущие входные параметры»
- **Подраздел:** строка 27 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `- базовые лоты/распределение: `StartLot=0.10`, `BigRatio=1.15`, `SmallRatio=0.25`, `CloseBigOnSmall=0.40`, `RemainBigOnSmall=0.60`, `CloseFarShare=0.10`, `ReserveShare=0.90`, `SmallReserveShare=0.05`;`
- **Конкретное утверждение:** - базовые лоты/распределение: `StartLot=0.10`, `BigRatio=1.15`, `SmallRatio=0.25`, `CloseBigOnSmall=0.40`, `RemainBigOnSmall=0.60`, `CloseFarShare=0.10`, `ReserveShare=0.90`, `SmallReserveShare=0.05`;.
- **Конкретное значение:** см. таблицу значений ниже
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Все найденные документированные значения

| Значение | Документ | Раздел | Профиль | Назначение | Preliminary authority |
|---:|---|---|---|---|---|
| 0.60 | BIG_SCENARIO_ENGINEERING_AUDIT.md | 6. Numeric scenario used by the trace | test/report | Документированное значение | предварительный |
| 0.70 | MANUAL.md | 2. Параметры | manual/profile | Документированное значение | предварительный |
| 0.65 | MANUAL.md | Python Candidate 50/50 | manual/profile | Документированное значение | предварительный |
| 0.65 | MANUAL.md | Risk Compression Reverse | manual/profile | Документированное значение | предварительный |
| 0.65 | MANUAL.md | V2.4.1 RiskGate Architecture Fix | manual/profile | Документированное значение | предварительный |
| 0.60 | MONEY_MODEL_COMPLETION_BASELINE_RU.md | Текущие входные параметры | baseline | Документированное значение | предварительный |
| 0.40 | TEST_PLAN.md | ATR Geometry Runtime Validation | test/report | Документированное значение | предварительный |

- **Проверка пары:** profiles должны проверять `CloseBigOnSmall + RemainBigOnSmall = 1`; документированные пары 0.30+0.70, 0.35+0.65 и 0.40+0.60 дают 1.00, но не являются одним production profile.

#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/MANUAL.md` и `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md` без profile/scope discriminator даёт два разных правила для темы «RemainBigOnSmall values»; единая production-норма не определена.
- **Статус:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Этап разрешения:** `3.1.7`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `BLOCKER` выбран потому, что тема «RemainBigOnSmall values» блокирует следующий нормативный документ или способна изменить lot/money/state.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-005 — CloseFarShare values

- **Классификация результата:** `PARAMETER_PROFILE_CONFLICT`
- **Категория:** `PARAMETER`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «2. Параметры»
- **Подраздел:** строка 27 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `CloseFarShare = 0.90`
- **Конкретное утверждение:** CloseFarShare = 0.90.
- **Конкретное значение:** см. таблицу значений ниже
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md`
- **Раздел:** «Текущие входные параметры»
- **Подраздел:** строка 27 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `- базовые лоты/распределение: `StartLot=0.10`, `BigRatio=1.15`, `SmallRatio=0.25`, `CloseBigOnSmall=0.40`, `RemainBigOnSmall=0.60`, `CloseFarShare=0.10`, `ReserveShare=0.90`, `SmallReserveShare=0.05`;`
- **Конкретное утверждение:** - базовые лоты/распределение: `StartLot=0.10`, `BigRatio=1.15`, `SmallRatio=0.25`, `CloseBigOnSmall=0.40`, `RemainBigOnSmall=0.60`, `CloseFarShare=0.10`, `ReserveShare=0.90`, `SmallReserveShare=0.05`;.
- **Конкретное значение:** см. таблицу значений ниже
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Все найденные документированные значения

| Значение | Документ | Раздел | Профиль | Назначение | Preliminary authority |
|---:|---|---|---|---|---|
| 0.90 | BIG_SCENARIO_ENGINEERING_AUDIT.md | 90/10 profile | test/report | Документированное значение | предварительный |
| 0.20 | BIG_SCENARIO_ENGINEERING_AUDIT.md | 20/80 profile | test/report | Документированное значение | предварительный |
| 0.70 | BIG_SCENARIO_FULL_AUDIT.md | 11. Risks | test/report | Документированное значение | предварительный |
| 0.75 | BIG_SCENARIO_FULL_AUDIT.md | 13. MT5 Strategy Tester invalidation addendum | test/report | Документированное значение | предварительный |
| 0.70 | FULL_AUDIT_REPORT.md | 3. Config Check | test/report | Документированное значение | предварительный |
| 0.90 | MANUAL.md | 2. Параметры | manual/profile | Документированное значение | предварительный |
| 0.50 | MANUAL.md | Python Candidate 50/50 | manual/profile | Документированное значение | предварительный |
| 0.40 | MANUAL.md | V2.4.1 RiskGate Architecture Fix | manual/profile | Документированное значение | предварительный |
| 0.10 | MONEY_MODEL_COMPLETION_BASELINE_RU.md | Текущие входные параметры | baseline | Документированное значение | предварительный |
| 0.10 | NEXT_STAGE_BASELINE_AUDIT_RU.md | Текущие defaults из `Include/Config.mqh` | test/report | Документированное значение | предварительный |
| 0.10 | SPLIT_BIG_IMPLEMENTATION_REPORT_RU.md | Изменённые файлы | test/report | Документированное значение | предварительный |
| 0.90 | TEST_PLAN.md | Cycle Math Internal Report Tests | test/report | Документированное значение | предварительный |
| 0.70 | TEST_PLAN.md | Cycle Math Internal Report Tests | test/report | Документированное значение | предварительный |
| 0.50 | TEST_PLAN.md | Cycle Math Internal Report Tests | test/report | Документированное значение | предварительный |
| 0.70 | TEST_PLAN.md | Real Recovery P/L Validation Tests | test/report | Документированное значение | предварительный |
| 0.40 | TEST_PLAN.md | V2.4.1 RiskGate Architecture Fix Tests | test/report | Документированное значение | предварительный |

- **Проверка пары:** profiles 0.90+0.10, 0.70+0.30, 0.50+0.50, 0.40+0.60 и 0.10+0.90 дают 1.00; назначение test/default/legacy/Hybrid различается.

#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/MANUAL.md` и `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md` без profile/scope discriminator даёт два разных правила для темы «CloseFarShare values»; единая production-норма не определена.
- **Статус:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Этап разрешения:** `3.1.7`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `BLOCKER` выбран потому, что тема «CloseFarShare values» блокирует следующий нормативный документ или способна изменить lot/money/state.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-006 — ReserveShare values

- **Классификация результата:** `PARAMETER_PROFILE_CONFLICT`
- **Категория:** `PARAMETER`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «2. Параметры»
- **Подраздел:** строка 28 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `ReserveShare = 0.10`
- **Конкретное утверждение:** ReserveShare = 0.10.
- **Конкретное значение:** см. таблицу значений ниже
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md`
- **Раздел:** «Текущие входные параметры»
- **Подраздел:** строка 27 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `- базовые лоты/распределение: `StartLot=0.10`, `BigRatio=1.15`, `SmallRatio=0.25`, `CloseBigOnSmall=0.40`, `RemainBigOnSmall=0.60`, `CloseFarShare=0.10`, `ReserveShare=0.90`, `SmallReserveShare=0.05`;`
- **Конкретное утверждение:** - базовые лоты/распределение: `StartLot=0.10`, `BigRatio=1.15`, `SmallRatio=0.25`, `CloseBigOnSmall=0.40`, `RemainBigOnSmall=0.60`, `CloseFarShare=0.10`, `ReserveShare=0.90`, `SmallReserveShare=0.05`;.
- **Конкретное значение:** см. таблицу значений ниже
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Все найденные документированные значения

| Значение | Документ | Раздел | Профиль | Назначение | Preliminary authority |
|---:|---|---|---|---|---|
| 0.10 | BIG_SCENARIO_ENGINEERING_AUDIT.md | 90/10 profile | test/report | Документированное значение | предварительный |
| 0.80 | BIG_SCENARIO_ENGINEERING_AUDIT.md | 20/80 profile | test/report | Документированное значение | предварительный |
| 0.25 | BIG_SCENARIO_FULL_AUDIT.md | 13. MT5 Strategy Tester invalidation addendum | test/report | Документированное значение | предварительный |
| 0.30 | FULL_AUDIT_REPORT.md | 3. Config Check | test/report | Документированное значение | предварительный |
| 0.10 | MANUAL.md | 2. Параметры | manual/profile | Документированное значение | предварительный |
| 0.50 | MANUAL.md | Python Candidate 50/50 | manual/profile | Документированное значение | предварительный |
| 0.60 | MANUAL.md | V2.4.1 RiskGate Architecture Fix | manual/profile | Документированное значение | предварительный |
| 1 | MANUAL.md | Split Big Geometry stage 1: BigCore + BigTrend + SmallBase | manual/profile | Документированное значение | предварительный |
| 0.90 | MONEY_MODEL_COMPLETION_BASELINE_RU.md | Текущие входные параметры | baseline | Документированное значение | предварительный |
| 0.90 | NEXT_STAGE_BASELINE_AUDIT_RU.md | Текущие defaults из `Include/Config.mqh` | test/report | Документированное значение | предварительный |
| 0.90 | SPLIT_BIG_IMPLEMENTATION_REPORT_RU.md | Изменённые файлы | test/report | Документированное значение | предварительный |
| 0.10 | TEST_PLAN.md | Cycle Math Internal Report Tests | test/report | Документированное значение | предварительный |
| 0.30 | TEST_PLAN.md | Cycle Math Internal Report Tests | test/report | Документированное значение | предварительный |
| 0.50 | TEST_PLAN.md | Cycle Math Internal Report Tests | test/report | Документированное значение | предварительный |
| 0.30 | TEST_PLAN.md | Real Recovery P/L Validation Tests | test/report | Документированное значение | предварительный |
| 0.60 | TEST_PLAN.md | V2.4.1 RiskGate Architecture Fix Tests | test/report | Документированное значение | предварительный |
| 0.75 | TEST_PLAN.md | ATR Geometry Runtime Validation | test/report | Документированное значение | предварительный |

- **Проверка пары:** profiles 0.90+0.10, 0.70+0.30, 0.50+0.50, 0.40+0.60 и 0.10+0.90 дают 1.00; назначение test/default/legacy/Hybrid различается.

#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/MANUAL.md` и `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md` без profile/scope discriminator даёт два разных правила для темы «ReserveShare values»; единая production-норма не определена.
- **Статус:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Этап разрешения:** `3.1.7`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `BLOCKER` выбран потому, что тема «ReserveShare values» блокирует следующий нормативный документ или способна изменить lot/money/state.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-007 — SmallReserveShare values

- **Классификация результата:** `NO_DIRECT_CONFLICT_FOUND`
- **Категория:** `PARAMETER`
- **Критичность:** `INFORMATIONAL`

#### Проверенные источники

| Значение | Документ | Раздел | Профиль | Назначение | Preliminary authority |
|---:|---|---|---|---|---|
| 0.05 | `Docs/MANUAL.md` | «Risk Compression Reverse», строка 481 | manual/profile | доля положительного `SmallScenarioRealNet`, направляемая в Small Reserve | предварительный |
| 0.05 | `Docs/MANUAL.md` | «V2.4.1 RiskGate Architecture Fix», строка 543 | runtime input profile | значение `SmallReserveShare` в наборе входов | предварительный |
| 0.05 | `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md` | «Текущие входные параметры», строка 27 | baseline | baseline-доля Small Reserve | предварительный |

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Risk Compression Reverse»
- **Подраздел:** «Small Reserve Logic»
- **Уникальный маркер или формула:** `SmallReserveAdd = SmallScenarioRealNet * SmallReserveShare`
- **Конкретное утверждение:** `SmallReserveShare = 0.05`; credit возникает только при положительном `SmallScenarioRealNet`.
- **Конкретное значение:** `0.05`
- **Единица измерения:** безразмерная доля (`ratio`).
- **Профиль или режим:** manual/runtime input profile.
- **Контекст применения:** распределение положительного realized net Small-at-Far.

#### Сторона B
- **Документ:** `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md`
- **Раздел:** «Текущие входные параметры»
- **Подраздел:** baseline лотов и распределения
- **Уникальный маркер или формула:** `SmallReserveShare=0.05`
- **Конкретное утверждение:** baseline фиксирует `SmallReserveShare` равным `0.05`.
- **Конкретное значение:** `0.05`
- **Единица измерения:** безразмерная доля (`ratio`).
- **Профиль или режим:** money-model baseline.
- **Контекст применения:** baseline-параметр распределения Small Reserve.

#### Вывод проверки
- **Логическая сопоставимость:** обе стороны определяют один параметр, в одной размерности и с одинаковым значением.
- **Результат:** Во всех обнаруженных профильных и baseline-документах найдено одинаковое значение SmallReserveShare=0.05. Прямого конфликта значений не обнаружено. Различие названий разделов не создаёт нормативного конфликта параметра.
- **Статус:** `NO_DIRECT_CONFLICT_FOUND`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** не требуется; повторить поиск при изменении документации.
- **Почему выбран именно этот уровень критичности:** `INFORMATIONAL`, поскольку проверка подтвердила согласованность значения и не выявила механизма изменения lot, money или state.
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`; запись не является выбором production profile.

### HSB-DOC-CONFLICT-008 — Reserve in Partial Far

- **Классификация результата:** `NO_DIRECT_CONFLICT_FOUND`
- **Категория:** `RESERVE`
- **Критичность:** `INFORMATIONAL`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_MONEY_FLOW.md`
- **Раздел:** «Forbidden edges»
- **Подраздел:** таблица запрещённых денежных рёбер, строки 27–34
- **Уникальный маркер или формула:** `FinalReserve -X-> Partial Far`
- **Конкретное утверждение:** FinalReserve не является источником или параметром Partial Far solver; Partial Far финансируется отдельным PartialBudget.
- **Конкретное значение:** запрещённое ребро `FinalReserve → Partial Far`; разрешённый bucket — `PartialBudget`.
- **Единица измерения:** money bucket / направление денежного потока.
- **Профиль или режим:** Hybrid Split Big money-flow contract.
- **Контекст применения:** allocation подтверждённого Harvest net и последующее финансирование Partial Far.

#### Сторона B
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Big-сценарий»
- **Подраздел:** расчёт `CloseFarBudget`, строки 83–93
- **Уникальный маркер или формула:** `CloseFarBudget = NetProfit × 0.90`; `ReserveAdd = NetProfit × 0.10`
- **Конкретное утверждение:** частичное закрытие Far вычисляется из `CloseFarBudget`; Reserve начисляется отдельно.
- **Конкретное значение:** два раздельных allocation результата — `CloseFarBudget` и `ReserveAdd`.
- **Единица измерения:** money.
- **Профиль или режим:** manual Big-harvest profile.
- **Контекст применения:** распределение NetProfit перед денежным partial close Far.

#### Сопоставление последовательностей
1. `HYBRID_SPLIT_BIG_MONEY_FLOW.md`: confirmed Harvest deals → Actual HarvestNet → Eligible Harvest → отдельные PartialBudget и FinalReserve → Partial Far расходует только PartialBudget.
2. `MANUAL.md`: NetProfit → отдельные `CloseFarBudget` и `ReserveAdd` → Far закрывается по `CloseFarBudget`.

#### Вывод проверки
- **Логическая сопоставимость:** обе стороны описывают отдельный бюджет Partial Far и отдельный Reserve bucket.
- **Результат:** прямого конфликта не найдено. Сторона A явно запрещает `FinalReserve → Partial Far`; сторона B не разрешает это ребро и использует `CloseFarBudget`. Отсутствие термина `FinalReserve` в указанном фрагменте Manual не является противоположным правилом.
- **Статус:** `NO_DIRECT_CONFLICT_FOUND`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** не требуется; определения bucket будут консолидированы позднее без изменения бизнес-логики.
- **Почему выбран именно этот уровень критичности:** `INFORMATIONAL`, поскольку проверенные последовательности совместимы и не создают доказанного двойного расходования Reserve.
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`.

### HSB-DOC-CONFLICT-009 — RecoveryPL includes Reserve

- **Классификация результата:** `NO_DIRECT_CONFLICT_FOUND`
- **Категория:** `RECOVERY_PL`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`
- **Раздел:** «Money»
- **Подраздел:** строка 24 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `/ MONEY-06 / Reserve уже входит в RealizedCyclePL и никогда не добавляется к RecoveryPL повторно. /`
- **Конкретное утверждение:** / MONEY-06 / Reserve уже входит в RealizedCyclePL и никогда не добавляется к RecoveryPL повторно. /.
- **Конкретное значение:** / MONEY-06 / Reserve уже входит в RealizedCyclePL и никогда не добавляется к RecoveryPL повторно. /
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/FULL_AUDIT_REPORT.md`
- **Раздел:** «9. RealRecoveryPL Check»
- **Подраздел:** строка 223 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `## 9. RealRecoveryPL Check`
- **Конкретное утверждение:** ## 9. RealRecoveryPL Check.
- **Конкретное значение:** ## 9. RealRecoveryPL Check
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Вывод проверки
- **Точная несовместимость:** Стороны описывают разные последовательные уровни или scope и могут сосуществовать; ни одно из приведённых утверждений явно не отрицает другое.
- **Статус:** `NO_DIRECT_CONFLICT_FOUND`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** `не требуется; сохранить результат проверки`
- **Результат:** Проверка темы завершена: прямого междокументного противоречия не найдено; запись не является основанием для пользовательского выбора.
- **Почему выбран именно этот уровень критичности:** `INFORMATIONAL` выбран потому, что тема «RecoveryPL includes Reserve» создаёт ограниченный scope/evidence gap без доказанного немедленного runtime ущерба.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-010 — RecoveryPL includes Initial Plus

- **Классификация результата:** `NO_DIRECT_CONFLICT_FOUND`
- **Категория:** `RECOVERY_PL`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`
- **Раздел:** «Hybrid Split Big — System Invariants»
- **Подраздел:** строка 3 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `Нарушение любого `MUST` запрещает необратимое действие и переводит результат в reject/error/reconciliation. Safe default не заменяет failed invariant.`
- **Конкретное утверждение:** Нарушение любого `MUST` запрещает необратимое действие и переводит результат в reject/error/reconciliation. Safe default не заменяет failed invariant..
- **Конкретное значение:** Нарушение любого `MUST` запрещает необратимое действие и переводит результат в reject/error/reconciliation. Safe default не заменяет failed invariant.
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/FULL_AUDIT_REPORT.md`
- **Раздел:** «3. Config Check»
- **Подраздел:** строка 60 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `InitialTriggerPoints, BigMoveStartPoints, BigMoveStepPoints, FarDistanceMode,`
- **Конкретное утверждение:** InitialTriggerPoints, BigMoveStartPoints, BigMoveStepPoints, FarDistanceMode,.
- **Конкретное значение:** InitialTriggerPoints, BigMoveStartPoints, BigMoveStepPoints, FarDistanceMode,
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Вывод проверки
- **Точная несовместимость:** Стороны описывают разные последовательные уровни или scope и могут сосуществовать; ни одно из приведённых утверждений явно не отрицает другое.
- **Статус:** `NO_DIRECT_CONFLICT_FOUND`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** `не требуется; сохранить результат проверки`
- **Результат:** Проверка темы завершена: прямого междокументного противоречия не найдено; запись не является основанием для пользовательского выбора.
- **Почему выбран именно этот уровень критичности:** `INFORMATIONAL` выбран потому, что тема «RecoveryPL includes Initial Plus» создаёт ограниченный scope/evidence gap без доказанного немедленного runtime ущерба.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-011 — RecoveryPL Symbol filter

- **Классификация результата:** `MISSING_DEFINITION`
- **Категория:** `RECOVERY_PL`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`
- **Раздел:** «Identity and logic»
- **Подраздел:** строка 34 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `/ LOGIC-04 / CycleID уникален; roles идентифицируются Symbol+Magic+CycleID+identifier. /`
- **Конкретное утверждение:** / LOGIC-04 / CycleID уникален; roles идентифицируются Symbol+Magic+CycleID+identifier. /.
- **Конкретное значение:** / LOGIC-04 / CycleID уникален; roles идентифицируются Symbol+Magic+CycleID+identifier. /
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/FULL_AUDIT_REPORT.md`
- **Раздел:** «V2.4 Safety Audit Addendum»
- **Подраздел:** строка 454 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `- Trade setup uses `SetExpertMagicNumber`, `SetDeviationInPoints(MaxSlippagePoints)`, and `SetTypeFillingBySymbol`.`
- **Конкретное утверждение:** - Trade setup uses `SetExpertMagicNumber`, `SetDeviationInPoints(MaxSlippagePoints)`, and `SetTypeFillingBySymbol`..
- **Конкретное значение:** - Trade setup uses `SetExpertMagicNumber`, `SetDeviationInPoints(MaxSlippagePoints)`, and `SetTypeFillingBySymbol`.
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md` и `Docs/FULL_AUDIT_REPORT.md` без profile/scope discriminator даёт два разных правила для темы «RecoveryPL Symbol filter»; единая production-норма не определена.
- **Статус:** `OPEN`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** `3.1.3–3.1.6 по теме`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `HIGH` выбран потому, что тема «RecoveryPL Symbol filter» создаёт ограниченный scope/evidence gap без доказанного немедленного runtime ущерба.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-012 — RecoveryPL Magic filter

- **Классификация результата:** `MISSING_DEFINITION`
- **Категория:** `RECOVERY_PL`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`
- **Раздел:** «Identity and logic»
- **Подраздел:** строка 34 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `/ LOGIC-04 / CycleID уникален; roles идентифицируются Symbol+Magic+CycleID+identifier. /`
- **Конкретное утверждение:** / LOGIC-04 / CycleID уникален; roles идентифицируются Symbol+Magic+CycleID+identifier. /.
- **Конкретное значение:** / LOGIC-04 / CycleID уникален; roles идентифицируются Symbol+Magic+CycleID+identifier. /
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/FULL_AUDIT_REPORT.md`
- **Раздел:** «3. Config Check»
- **Подраздел:** строка 65 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `MaxSpreadPoints, MaxMarginPercent, MagicNumber, AllowRealTrading,`
- **Конкретное утверждение:** MaxSpreadPoints, MaxMarginPercent, MagicNumber, AllowRealTrading,.
- **Конкретное значение:** MaxSpreadPoints, MaxMarginPercent, MagicNumber, AllowRealTrading,
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md` и `Docs/FULL_AUDIT_REPORT.md` без profile/scope discriminator даёт два разных правила для темы «RecoveryPL Magic filter»; единая production-норма не определена.
- **Статус:** `OPEN`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** `3.1.3–3.1.6 по теме`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `HIGH` выбран потому, что тема «RecoveryPL Magic filter» создаёт ограниченный scope/evidence gap без доказанного немедленного runtime ущерба.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-013 — Gross versus Net Profit

- **Классификация результата:** `FORMULA_CONFLICT`
- **Категория:** `FORMULA`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_FORMULA_REFERENCE.md`
- **Раздел:** «Формулы уровня B»
- **Подраздел:** строка 21 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `* `LegNet=OrderCalcProfit(direction,symbol,lot,open,directional Bid/Ask close)-not-yet-included costs`.`
- **Конкретное утверждение:** * `LegNet=OrderCalcProfit(direction,symbol,lot,open,directional Bid/Ask close)-not-yet-included costs`..
- **Конкретное значение:** * `LegNet=OrderCalcProfit(direction,symbol,lot,open,directional Bid/Ask close)-not-yet-included costs`.
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «5. Big-сценарий»
- **Подраздел:** строка 82 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `3. Считает `NetProfit = ProfitBig - LossSmall - Costs`.`
- **Конкретное утверждение:** 3. Считает `NetProfit = ProfitBig - LossSmall - Costs`..
- **Конкретное значение:** 3. Считает `NetProfit = ProfitBig - LossSmall - Costs`.
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/HYBRID_SPLIT_BIG_FORMULA_REFERENCE.md` и `Docs/MANUAL.md` без profile/scope discriminator даёт два разных правила для темы «Gross versus Net Profit»; единая production-норма не определена.
- **Статус:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Этап разрешения:** `3.1.4`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `CRITICAL` выбран потому, что тема «Gross versus Net Profit» блокирует следующий нормативный документ или способна изменить lot/money/state.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-014 — Commission swap fee

- **Классификация результата:** `MISSING_DEFINITION`
- **Категория:** `MONEY_LEDGER`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_MONEY_FLOW.md`
- **Раздел:** «Sequential Harvest refinement»
- **Подраздел:** строка 43 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `Open commission provenance: already-realized old-leg open costs are never debited again; projected reopen cost is recorded once in the new state; each projected close cost belongs to one disjoint close event.`
- **Конкретное утверждение:** Open commission provenance: already-realized old-leg open costs are never debited again; projected reopen cost is recorded once in the new state; each projected close cost belongs to one disjoint close event..
- **Конкретное значение:** Open commission provenance: already-realized old-leg open costs are never debited again; projected reopen cost is recorded once in the new state; each projected close cost belongs to one disjoint close event.
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/BASKET_RISK_CONTRACT_RU.md`
- **Раздел:** «18. Exactly-once contract»
- **Подраздел:** строка 490 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `Exactly once применяется к каждому `HarvestNet`, `PartialFarNet`, open commission leg и ledger event. Projected event не является commit. Один event имеет ровно один terminal commit outcome (`COMMITTED` или typed rejected/rolled-back status по существующему le`
- **Конкретное утверждение:** Exactly once применяется к каждому `HarvestNet`, `PartialFarNet`, open commission leg и ledger event. Projected event не является commit. Один event имеет ровно один terminal commit outcome (`COMMITTED` или typed rejected/rolled-back status по существующему le.
- **Конкретное значение:** Exactly once применяется к каждому `HarvestNet`, `PartialFarNet`, open commission leg и ledger event. Projected event не является commit. Один event имеет ровно один terminal commit outcome (`COMMITTED` или typed rejected/rolled-back status по существующему le
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Денежная последовательность
- Projected costs are estimates; actual net is deal profit+swap+commission+fee with broker signs.
- **Rollback/exactly-once:** projected amount не коммитится; confirmed event обязан иметь idempotent key и reconciliation.
- **Partial/Final связь:** buckets не взаимозаменяются без отдельного authority.

#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/HYBRID_SPLIT_BIG_MONEY_FLOW.md` и `Docs/BASKET_RISK_CONTRACT_RU.md` без profile/scope discriminator даёт два разных правила для темы «Commission swap fee»; единая production-норма не определена.
- **Статус:** `OPEN`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** `3.1.3–3.1.6 по теме`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `HIGH` выбран потому, что тема «Commission swap fee» создаёт ограниченный scope/evidence gap без доказанного немедленного runtime ущерба.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-015 — Projected versus Realized Reserve

- **Классификация результата:** `SCOPE_CONFLICT`
- **Категория:** `RESERVE`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_MONEY_FLOW.md`
- **Раздел:** «Forbidden edges»
- **Подраздел:** строка 34 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `Projected money -X-> persisted bucket`
- **Конкретное утверждение:** Projected money -X-> persisted bucket.
- **Конкретное значение:** Projected money -X-> persisted bucket
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Параметры защиты»
- **Подраздел:** строка 179 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `input double MinProjectedReserveCoverage = 1.00;`
- **Конкретное утверждение:** input double MinProjectedReserveCoverage = 1.00;.
- **Конкретное значение:** input double MinProjectedReserveCoverage = 1.00;
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Денежная последовательность
- ProjectedReserve is read-only forecast; confirmed Harvest deal creates realized bucket credit.
- **Rollback/exactly-once:** projected amount не коммитится; confirmed event обязан иметь idempotent key и reconciliation.
- **Partial/Final связь:** buckets не взаимозаменяются без отдельного authority.

#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/HYBRID_SPLIT_BIG_MONEY_FLOW.md` и `Docs/MANUAL.md` без profile/scope discriminator даёт два разных правила для темы «Projected versus Realized Reserve»; единая production-норма не определена.
- **Статус:** `OPEN`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** `3.1.3–3.1.8 по теме`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `MEDIUM` выбран потому, что тема «Projected versus Realized Reserve» создаёт ограниченный scope/evidence gap без доказанного немедленного runtime ущерба.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-016 — Planned versus actual close result

- **Классификация результата:** `NO_DIRECT_CONFLICT_FOUND`
- **Категория:** `EXECUTION`

#### Сторона A
- **Документ:** `Docs/BASKET_RISK_CONTRACT_RU.md`
- **Раздел:** «3. Термины и соответствие существующей системе»
- **Подраздел:** строка 45 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `/ Post-Execution Reconciliation / LOGIC-05/06 / Подтверждение actual result и новый snapshot /`
- **Конкретное утверждение:** / Post-Execution Reconciliation / LOGIC-05/06 / Подтверждение actual result и новый snapshot /.
- **Конкретное значение:** / Post-Execution Reconciliation / LOGIC-05/06 / Подтверждение actual result и новый snapshot /
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_IMPLEMENTATION_REPORT_RU.md`
- **Раздел:** «Static baseline»
- **Подраздел:** строка 21 / ближайший уникальный контекст
- **Уникальный маркер или формула:** ``BASELINE_STATIC_FAILURE_RESOLVED`: контракт `SimRecordClosedDeal` восстановлен как совместимый wrapper над единым `SimRecordDeal`, поэтому static test больше не должен падать на отсутствии имени функции.`
- **Конкретное утверждение:** `BASELINE_STATIC_FAILURE_RESOLVED`: контракт `SimRecordClosedDeal` восстановлен как совместимый wrapper над единым `SimRecordDeal`, поэтому static test больше не должен падать на отсутствии имени функции..
- **Конкретное значение:** `BASELINE_STATIC_FAILURE_RESOLVED`: контракт `SimRecordClosedDeal` восстановлен как совместимый wrapper над единым `SimRecordDeal`, поэтому static test больше не должен падать на отсутствии имени функции.
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Execution lifecycle
- **Фактическая цепь проверки:** request→retcode→deal history→actual net→ledger/reconciliation
- Accepted request не равен actual position/deal result; partial/retry/restart требуют нового verified snapshot.

#### Вывод проверки
- **Точная несовместимость:** Стороны описывают разные последовательные уровни или scope и могут сосуществовать; ни одно из приведённых утверждений явно не отрицает другое.
- **Статус:** `NO_DIRECT_CONFLICT_FOUND`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** `не требуется; сохранить результат проверки`
- **Результат:** Проверка темы завершена: прямого междокументного противоречия не найдено; запись не является основанием для пользовательского выбора.
- **Почему выбран именно этот уровень критичности:** `INFORMATIONAL` выбран потому, что тема «Planned versus actual close result» создаёт ограниченный scope/evidence gap без доказанного немедленного runtime ущерба.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-017 — Final Close preview versus actual success

- **Классификация результата:** `AMBIGUITY`
- **Категория:** `FINAL_CLOSE`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`
- **Раздел:** «14. Result, terminal and reason contract»
- **Подраздел:** строка 148 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `Full-Far affordability routes to `CATCHUP_REQUIRES_FINAL_CLOSE_PREVIEW`; invalid residual to `CATCHUP_REJECT_INVALID_FAR_REMAINDER`; component min-volume to `CATCHUP_TERMINAL_MIN_VOLUME`. Other exact failures: `CATCHUP_STATE_INVALID`, `CATCHUP_TRIGGER_INVALID``
- **Конкретное утверждение:** Full-Far affordability routes to `CATCHUP_REQUIRES_FINAL_CLOSE_PREVIEW`; invalid residual to `CATCHUP_REJECT_INVALID_FAR_REMAINDER`; component min-volume to `CATCHUP_TERMINAL_MIN_VOLUME`. Other exact failures: `CATCHUP_STATE_INVALID`, `CATCHUP_TRIGGER_INVALID`.
- **Конкретное значение:** Full-Far affordability routes to `CATCHUP_REQUIRES_FINAL_CLOSE_PREVIEW`; invalid residual to `CATCHUP_REJECT_INVALID_FAR_REMAINDER`; component min-volume to `CATCHUP_TERMINAL_MIN_VOLUME`. Other exact failures: `CATCHUP_STATE_INVALID`, `CATCHUP_TRIGGER_INVALID`
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Real Recovery P/L Validation»
- **Подраздел:** строка 443 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `LastSystemCloseComment = FINAL_CLOSE_PROFIT or CLOSED_PROFIT`
- **Конкретное утверждение:** LastSystemCloseComment = FINAL_CLOSE_PROFIT or CLOSED_PROFIT.
- **Конкретное значение:** LastSystemCloseComment = FINAL_CLOSE_PROFIT or CLOSED_PROFIT
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md` и `Docs/MANUAL.md` без profile/scope discriminator даёт два разных правила для темы «Final Close preview versus actual success»; единая production-норма не определена.
- **Статус:** `OPEN`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** `3.1.3–3.1.6 по теме`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `HIGH` выбран потому, что тема «Final Close preview versus actual success» создаёт ограниченный scope/evidence gap без доказанного немедленного runtime ущерба.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-018 — Small close trigger

- **Классификация результата:** `SCOPE_CONFLICT`
- **Категория:** `SMALL_SCENARIO`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_STATE_TRANSITION_TABLE.md`
- **Раздел:** «Hybrid Split Big — State Transition Truth Table»
- **Подраздел:** строка 8 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `/ OPEN_TREND_PENDING / Trend fill / exact identifier/lot / persist confirmation / OPEN_SMALL_PENDING / RECONCILIATION /`
- **Конкретное утверждение:** / OPEN_TREND_PENDING / Trend fill / exact identifier/lot / persist confirmation / OPEN_SMALL_PENDING / RECONCILIATION /.
- **Конкретное значение:** / OPEN_TREND_PENDING / Trend fill / exact identifier/lot / persist confirmation / OPEN_SMALL_PENDING / RECONCILIATION /
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «1. Назначение»
- **Подраздел:** строка 13 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `5. От `Far` строятся `Big` и `Small` по геометрии мануала.`
- **Конкретное утверждение:** 5. От `Far` строятся `Big` и `Small` по геометрии мануала..
- **Конкретное значение:** 5. От `Far` строятся `Big` и `Small` по геометрии мануала.
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Сравнение последовательностей
- **Последовательность A:** 1) движение к Small; 2) ожидание Far touch; 3) close Small; 4) close OldFar; 5) partial Big; 6) NewFar.
- **Последовательность B:** 1) Split trigger; 2) phase-state validation; 3) role-specific closes; 4) actual remainder verification.

#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/HYBRID_SPLIT_BIG_STATE_TRANSITION_TABLE.md` и `Docs/MANUAL.md` без profile/scope discriminator даёт два разных правила для темы «Small close trigger»; единая production-норма не определена.
- **Статус:** `OPEN`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** `3.1.3–3.1.8 по теме`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `MEDIUM` выбран потому, что тема «Small close trigger» создаёт ограниченный scope/evidence gap без доказанного немедленного runtime ущерба.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-019 — Old Far full versus partial close

- **Классификация результата:** `SCOPE_CONFLICT`
- **Категория:** `SMALL_SCENARIO`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_STATE_TRANSITION_TABLE.md`
- **Раздел:** «Hybrid Split Big — State Transition Truth Table»
- **Подраздел:** строка 17 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `/ FINAL_CLOSE_PENDING / all managed closes / positions=0 and actual threshold PASS / confirmed deals reconciled / CLOSED_PROFIT / TERMINAL_SAFE /`
- **Конкретное утверждение:** / FINAL_CLOSE_PENDING / all managed closes / positions=0 and actual threshold PASS / confirmed deals reconciled / CLOSED_PROFIT / TERMINAL_SAFE /.
- **Конкретное значение:** / FINAL_CLOSE_PENDING / all managed closes / positions=0 and actual threshold PASS / confirmed deals reconciled / CLOSED_PROFIT / TERMINAL_SAFE /
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Small-at-Far Scenario»
- **Подраздел:** строка 162 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `Small-сценарий больше не исполняется сразу при первом движении в сторону Small. Если Small достиг защитного движения, советник переводит цикл в `STATE_WAIT_SMALL_TO_FAR` и ждёт, пока текущая цена дойдёт до цены открытия старого `Far` с учётом `SmallFarTouchOff`
- **Конкретное утверждение:** Small-сценарий больше не исполняется сразу при первом движении в сторону Small. Если Small достиг защитного движения, советник переводит цикл в `STATE_WAIT_SMALL_TO_FAR` и ждёт, пока текущая цена дойдёт до цены открытия старого `Far` с учётом `SmallFarTouchOff.
- **Конкретное значение:** Small-сценарий больше не исполняется сразу при первом движении в сторону Small. Если Small достиг защитного движения, советник переводит цикл в `STATE_WAIT_SMALL_TO_FAR` и ждёт, пока текущая цена дойдёт до цены открытия старого `Far` с учётом `SmallFarTouchOff
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Сравнение последовательностей
- **Последовательность A:** 1) Small close; 2) OldFar full close; 3) Big partial close.
- **Последовательность B:** 1) budget gate; 2) Partial Far candidate; 3) residual Far re-evaluation.

#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/HYBRID_SPLIT_BIG_STATE_TRANSITION_TABLE.md` и `Docs/MANUAL.md` без profile/scope discriminator даёт два разных правила для темы «Old Far full versus partial close»; единая production-норма не определена.
- **Статус:** `OPEN`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** `3.1.3–3.1.8 по теме`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `MEDIUM` выбран потому, что тема «Old Far full versus partial close» создаёт ограниченный scope/evidence gap без доказанного немедленного runtime ущерба.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-020 — New Far source

- **Классификация результата:** `AUTHORITY_CONFLICT`
- **Категория:** `GEOMETRY`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`
- **Раздел:** «Geometry»
- **Подраздел:** строка 9 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `/ GEO-01 / `0 < NewFar < OldFar`. /`
- **Конкретное утверждение:** / GEO-01 / `0 < NewFar < OldFar`. /.
- **Конкретное значение:** / GEO-01 / `0 < NewFar < OldFar`. /
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Geometry Validator»
- **Подраздел:** строка 190 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `NewFarLot < OldFarLot`
- **Конкретное утверждение:** NewFarLot < OldFarLot.
- **Конкретное значение:** NewFarLot < OldFarLot
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Сравнение последовательностей
- **Последовательность A:** 1) close Big part; 2) read actual remaining Big; 3) promote NewFar.
- **Последовательность B:** 1) close SmallBase/OldFar/BigTrend; 2) verify BigCore remainder; 3) promote only BigCore.

#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md` и `Docs/MANUAL.md` без profile/scope discriminator даёт два разных правила для темы «New Far source»; единая production-норма не определена.
- **Статус:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Этап разрешения:** `3.1.8`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `BLOCKER` выбран потому, что тема «New Far source» блокирует следующий нормативный документ или способна изменить lot/money/state.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-021 — Next Big base

- **Классификация результата:** `SCOPE_CONFLICT`
- **Категория:** `FORMULA`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_FORMULA_REFERENCE.md`
- **Раздел:** «Margin and terminal rule»
- **Подраздел:** строка 55 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `**Oracle rounding profile:** `EA_CURRENT` means BigCore DOWN, BigTrend DOWN, SmallBase UP and NewFar DOWN; every gate is rerun on these rounded lots.`
- **Конкретное утверждение:** **Oracle rounding profile:** `EA_CURRENT` means BigCore DOWN, BigTrend DOWN, SmallBase UP and NewFar DOWN; every gate is rerun on these rounded lots..
- **Конкретное значение:** **Oracle rounding profile:** `EA_CURRENT` means BigCore DOWN, BigTrend DOWN, SmallBase UP and NewFar DOWN; every gate is rerun on these rounded lots.
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Geometry Validator»
- **Подраздел:** строка 191 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `NewBigLot > NewFarLot`
- **Конкретное утверждение:** NewBigLot > NewFarLot.
- **Конкретное значение:** NewBigLot > NewFarLot
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Сравнение последовательностей
- **Последовательность A:** 1) NewFar formed; 2) NewBig=NewFar*BigRatio.
- **Последовательность B:** 1) residual Far frozen; 2) NextCore/NextTrend normalized separately; 3) post-round gates.

#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/HYBRID_SPLIT_BIG_FORMULA_REFERENCE.md` и `Docs/MANUAL.md` без profile/scope discriminator даёт два разных правила для темы «Next Big base»; единая production-норма не определена.
- **Статус:** `OPEN`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** `3.1.3–3.1.8 по теме`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `MEDIUM` выбран потому, что тема «Next Big base» создаёт ограниченный scope/evidence gap без доказанного немедленного runtime ущерба.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-022 — new Big less than old Far

- **Классификация результата:** `MISSING_DEFINITION`
- **Категория:** `GEOMETRY`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`
- **Раздел:** «Geometry»
- **Подраздел:** строка 10 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `/ GEO-02 / `NextCore + NextTrend < OldFar * MaximumNewBigToOldFarRatio`. /`
- **Конкретное утверждение:** / GEO-02 / `NextCore + NextTrend < OldFar * MaximumNewBigToOldFarRatio`. /.
- **Конкретное значение:** / GEO-02 / `NextCore + NextTrend < OldFar * MaximumNewBigToOldFarRatio`. /
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Geometry Validator»
- **Подраздел:** строка 191 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `NewBigLot > NewFarLot`
- **Конкретное утверждение:** NewBigLot > NewFarLot.
- **Конкретное значение:** NewBigLot > NewFarLot
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Сравнение последовательностей
- **Последовательность A:** 1) compute Next Big; 2) require strict comparison with OldFar.
- **Последовательность B:** 1) legacy migration describes inputs; 2) strict ratio/tolerance is not defined there.

#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md` и `Docs/MANUAL.md` без profile/scope discriminator даёт два разных правила для темы «new Big less than old Far»; единая production-норма не определена.
- **Статус:** `OPEN`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** `3.1.3–3.1.6 по теме`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `HIGH` выбран потому, что тема «new Big less than old Far» создаёт ограниченный scope/evidence gap без доказанного немедленного runtime ущерба.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-023 — Negative Small Reverse Net

- **Классификация результата:** `MISSING_DEFINITION`
- **Категория:** `RISK`

#### Сторона A
- **Документ:** `Docs/BASKET_RISK_CONTRACT_RU.md`
- **Раздел:** «7.3. Conservation checks»
- **Подраздел:** строка 195 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `- Negative Harvest не создаёт credits.`
- **Конкретное утверждение:** - Negative Harvest не создаёт credits..
- **Конкретное значение:** - Negative Harvest не создаёт credits.
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_THREE_LAWS_MATH_MANUAL_RU.md`
- **Раздел:** «Глава 25. Инварианты»
- **Подраздел:** строка 131 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `Identity: Symbol, Magic, CycleID and identifier must match. Reserve: nonnegative, within eligible realized profit, never double-counted, nondecreasing in Small. Big: normalized monetary Catch-Up and slope PASS. Small: `0<N<F`, `NextBigGross<OldFar`, `RiskNext<`
- **Конкретное утверждение:** Identity: Symbol, Magic, CycleID and identifier must match. Reserve: nonnegative, within eligible realized profit, never double-counted, nondecreasing in Small. Big: normalized monetary Catch-Up and slope PASS. Small: `0<N<F`, `NextBigGross<OldFar`, `RiskNext<.
- **Конкретное значение:** Identity: Symbol, Magic, CycleID and identifier must match. Reserve: nonnegative, within eligible realized profit, never double-counted, nondecreasing in Small. Big: normalized monetary Catch-Up and slope PASS. Small: `0<N<F`, `NextBigGross<OldFar`, `RiskNext<
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Сравнение последовательностей
- **Последовательность A:** 1) compute Small Reverse net; 2) policy input may allow negative result.
- **Последовательность B:** 1) require transition budget/limit; 2) reject if policy not approved.

#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/BASKET_RISK_CONTRACT_RU.md` и `Docs/HYBRID_SPLIT_BIG_THREE_LAWS_MATH_MANUAL_RU.md` без profile/scope discriminator даёт два разных правила для темы «Negative Small Reverse Net»; единая production-норма не определена.
- **Статус:** `OPEN`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** `3.1.3–3.1.6 по теме`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `HIGH` выбран потому, что тема «Negative Small Reverse Net» создаёт ограниченный scope/evidence gap без доказанного немедленного runtime ущерба.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-024 — Small Far Big close order

- **Классификация результата:** `ORDERING_CONFLICT`
- **Категория:** `SMALL_SCENARIO`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_STATE_TRANSITION_TABLE.md`
- **Раздел:** «Hybrid Split Big — State Transition Truth Table»
- **Подраздел:** строка 3 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `/ Current / Event / Condition / Pending/actual requirement / Next / Failure /`
- **Конкретное утверждение:** / Current / Event / Condition / Pending/actual requirement / Next / Failure /.
- **Конкретное значение:** / Current / Event / Condition / Pending/actual requirement / Next / Failure /
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Split Big Geometry stage 1: BigCore + BigTrend + SmallBase»
- **Подраздел:** строка 991 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `## Split Big Geometry stage 1: BigCore + BigTrend + SmallBase`
- **Конкретное утверждение:** ## Split Big Geometry stage 1: BigCore + BigTrend + SmallBase.
- **Конкретное значение:** ## Split Big Geometry stage 1: BigCore + BigTrend + SmallBase
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Сравнение последовательностей
- **Последовательность A:** 1) close Small; 2) close OldFar; 3) partial Big; 4) promote remainder.
- **Последовательность B:** 1) close SmallBase; 2) OldFar; 3) BigTrend; 4) staged BigCore; 5) verify; 6) promote.

#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/HYBRID_SPLIT_BIG_STATE_TRANSITION_TABLE.md` и `Docs/MANUAL.md` без profile/scope discriminator даёт два разных правила для темы «Small Far Big close order»; единая production-норма не определена.
- **Статус:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Этап разрешения:** `3.1.6`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `CRITICAL` выбран потому, что тема «Small Far Big close order» блокирует следующий нормативный документ или способна изменить lot/money/state.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-025 — Reserve credit order

- **Классификация результата:** `AMBIGUITY`
- **Категория:** `RESERVE`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_MONEY_FLOW.md`
- **Раздел:** «Hybrid Split Big — Money Flow»
- **Подраздел:** строка 14 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `Partial FinalReserve Carry`
- **Конкретное утверждение:** Partial FinalReserve Carry.
- **Конкретное значение:** Partial FinalReserve Carry
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «1. Назначение»
- **Подраздел:** строка 11 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `3. Прибыль первого плюса не участвует в разруливании: `InitialProfitIgnored = true`, `Reserve = 0`.`
- **Конкретное утверждение:** 3. Прибыль первого плюса не участвует в разруливании: `InitialProfitIgnored = true`, `Reserve = 0`..
- **Конкретное значение:** 3. Прибыль первого плюса не участвует в разруливании: `InitialProfitIgnored = true`, `Reserve = 0`.
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Сравнение последовательностей
- **Последовательность A:** 1) compute ReserveAdd; 2) persist pending amount; 3) apply after deal path.
- **Последовательность B:** 1) confirm Harvest deals; 2) calculate EligibleHarvest; 3) allocate; 4) commit idempotent credit.

#### Денежная последовательность
- Credit must follow confirmed deals and allocation conservation; pre-confirmation amount is pending only.
- **Rollback/exactly-once:** projected amount не коммитится; confirmed event обязан иметь idempotent key и reconciliation.
- **Partial/Final связь:** buckets не взаимозаменяются без отдельного authority.

#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/HYBRID_SPLIT_BIG_MONEY_FLOW.md` и `Docs/MANUAL.md` без profile/scope discriminator даёт два разных правила для темы «Reserve credit order»; единая production-норма не определена.
- **Статус:** `OPEN`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** `3.1.3–3.1.6 по теме`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `HIGH` выбран потому, что тема «Reserve credit order» создаёт ограниченный scope/evidence gap без доказанного немедленного runtime ущерба.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-026 — State transition order

- **Классификация результата:** `MISSING_DEFINITION`
- **Категория:** `STATE_MACHINE`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`
- **Раздел:** «Hybrid Split Big — нормативная временная модель Catch-Up»
- **Подраздел:** строка 3 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `**Статус:** `NORMATIVE`. Единственный нормативный источник временной семантики Big Harvest. Модель строго последовательная, не alternative-price. Каждый level закрывает только существующие в его `StateBefore` рабочие позиции, после чего строит новый state.`
- **Конкретное утверждение:** **Статус:** `NORMATIVE`. Единственный нормативный источник временной семантики Big Harvest. Модель строго последовательная, не alternative-price. Каждый level закрывает только существующие в его `StateBefore` рабочие позиции, после чего строит новый state..
- **Конкретное значение:** **Статус:** `NORMATIVE`. Единственный нормативный источник временной семантики Big Harvest. Модель строго последовательная, не alternative-price. Каждый level закрывает только существующие в его `StateBefore` рабочие позиции, после чего строит новый state.
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «MinusLock BigHarvest EA — технический мануал»
- **Подраздел:** строка 3 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `Документ описывает MQL5-советник, реализованный строго на базе `manual/big_harvest_system_manual_ru.md`.`
- **Конкретное утверждение:** Документ описывает MQL5-советник, реализованный строго на базе `manual/big_harvest_system_manual_ru.md`..
- **Конкретное значение:** Документ описывает MQL5-советник, реализованный строго на базе `manual/big_harvest_system_manual_ru.md`.
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md` и `Docs/MANUAL.md` без profile/scope discriminator даёт два разных правила для темы «State transition order»; единая production-норма не определена.
- **Статус:** `OPEN`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** `3.1.3–3.1.6 по теме`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `HIGH` выбран потому, что тема «State transition order» создаёт ограниченный scope/evidence gap без доказанного немедленного runtime ущерба.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-027 — Requested versus executed volume

- **Классификация результата:** `NO_DIRECT_CONFLICT_FOUND`
- **Категория:** `EXECUTION`

#### Сторона A
- **Документ:** `Docs/BASKET_RISK_CONTRACT_RU.md`
- **Раздел:** «3. Термины и соответствие существующей системе»
- **Подраздел:** строка 45 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `/ Post-Execution Reconciliation / LOGIC-05/06 / Подтверждение actual result и новый snapshot /`
- **Конкретное утверждение:** / Post-Execution Reconciliation / LOGIC-05/06 / Подтверждение actual result и новый snapshot /.
- **Конкретное значение:** / Post-Execution Reconciliation / LOGIC-05/06 / Подтверждение actual result и новый snapshot /
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_IMPLEMENTATION_REPORT_RU.md`
- **Раздел:** «Статус»
- **Подраздел:** строка 5 / ближайший уникальный контекст
- **Уникальный маркер или формула:** ``HYBRID_PREOPEN_DECISION_ENGINE_NOT_READY` до подтверждённой компиляции MetaEditor `0 errors / 0 warnings`.`
- **Конкретное утверждение:** `HYBRID_PREOPEN_DECISION_ENGINE_NOT_READY` до подтверждённой компиляции MetaEditor `0 errors / 0 warnings`..
- **Конкретное значение:** `HYBRID_PREOPEN_DECISION_ENGINE_NOT_READY` до подтверждённой компиляции MetaEditor `0 errors / 0 warnings`.
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Execution lifecycle
- **Фактическая цепь проверки:** requested/normalized lot→request→actual filled lot→position snapshot→new revision
- Accepted request не равен actual position/deal result; partial/retry/restart требуют нового verified snapshot.

#### Вывод проверки
- **Точная несовместимость:** Стороны описывают разные последовательные уровни или scope и могут сосуществовать; ни одно из приведённых утверждений явно не отрицает другое.
- **Статус:** `NO_DIRECT_CONFLICT_FOUND`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** `не требуется; сохранить результат проверки`
- **Результат:** Проверка темы завершена: прямого междокументного противоречия не найдено; запись не является основанием для пользовательского выбора.
- **Почему выбран именно этот уровень критичности:** `INFORMATIONAL` выбран потому, что тема «Requested versus executed volume» создаёт ограниченный scope/evidence gap без доказанного немедленного runtime ущерба.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-028 — FLOOR CEILING NEAREST

- **Классификация результата:** `FORMULA_CONFLICT`
- **Категория:** `ROUNDING`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`
- **Раздел:** «Stage 1.2.4.1 money/Partial clarification»
- **Подраздел:** строка 131 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `- `HybridMoneyEqual(a,b)` проверяет ledger-normalized значения: `abs(Round2(a)-Round2(b)) <= MoneyCalculationTolerance`.`
- **Конкретное утверждение:** - `HybridMoneyEqual(a,b)` проверяет ledger-normalized значения: `abs(Round2(a)-Round2(b)) <= MoneyCalculationTolerance`..
- **Конкретное значение:** - `HybridMoneyEqual(a,b)` проверяет ledger-normalized значения: `abs(Round2(a)-Round2(b)) <= MoneyCalculationTolerance`.
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/BIG_SCENARIO_FULL_AUDIT.md`
- **Раздел:** «3. Function/file table»
- **Подраздел:** строка 77 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `/ Lot rounding / `Include/LotUtils.mqh` / `NormalizeLotDown`, `NormalizeLotUp`, `NormalizeLotNearest`, `NormalizeVolumeToStep` / Broker/user lot step alignment / No direct mutation /`
- **Конкретное утверждение:** / Lot rounding / `Include/LotUtils.mqh` / `NormalizeLotDown`, `NormalizeLotUp`, `NormalizeLotNearest`, `NormalizeVolumeToStep` / Broker/user lot step alignment / No direct mutation /.
- **Конкретное значение:** / Lot rounding / `Include/LotUtils.mqh` / `NormalizeLotDown`, `NormalizeLotUp`, `NormalizeLotNearest`, `NormalizeVolumeToStep` / Broker/user lot step alignment / No direct mutation /
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md` и `Docs/BIG_SCENARIO_FULL_AUDIT.md` без profile/scope discriminator даёт два разных правила для темы «FLOOR CEILING NEAREST»; единая production-норма не определена.
- **Статус:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Этап разрешения:** `3.1.4`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `CRITICAL` выбран потому, что тема «FLOOR CEILING NEAREST» блокирует следующий нормативный документ или способна изменить lot/money/state.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-029 — Python PASS versus MT5 NOT_RUN

- **Классификация результата:** `EVIDENCE_GAP`
- **Категория:** `TEST_EVIDENCE`
- **Критичность:** `INFORMATIONAL`

#### Сторона A
- **Документ:** `Docs/STAGE_1_2_4_1_EVIDENCE_RU.md`
- **Раздел:** «PRIMARY_IMPLEMENTATION_RUN»
- **Подраздел:** dimension-contract tests, строка 57
- **Уникальный маркер или формула:** `dimension-contract tests=17 passed in 0.08s`
- **Конкретное утверждение:** 17 Python/static dimension-contract tests завершились PASS.
- **Конкретное значение:** `17 passed`; Python/static evidence.
- **Единица измерения:** уровень test evidence.
- **Профиль или режим:** container Python/static validation.
- **Контекст применения:** проверка размерностного контракта, не MetaEditor и не MT5 runtime.

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_METAEDITOR_COMPILE.md`
- **Раздел:** «Hybrid Split Big — MetaEditor compile record»
- **Подраздел:** таблица compile evidence, строка 6
- **Уникальный маркер или формула:** `MetaTrader build | NOT_RUN_IN_CONTAINER`
- **Конкретное утверждение:** MetaEditor compile/MetaTrader build в контейнере не выполнялся.
- **Конкретное значение:** `NOT_RUN_IN_CONTAINER`.
- **Единица измерения:** уровень compile/runtime evidence.
- **Профиль или режим:** MetaEditor/MT5 validation.
- **Контекст применения:** доказательство компилируемости и терминального поведения MQL5.

#### Вывод проверки
- **Логическая сопоставимость:** стороны относятся к разным, дополняющим уровням evidence; PASS одного уровня не противоречит отсутствию запуска другого.
- **Результат:** Python/static evidence подтверждает только соответствующий уровень тестирования и не заменяет MetaEditor compile, MT5 Strategy Tester или broker runtime evidence.
- **Статус:** `EVIDENCE_GAP`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** последующие MetaEditor compile, MT5 Strategy Tester и broker-runtime проверки.
- **Почему выбран именно этот уровень критичности:** `INFORMATIONAL`, поскольку бизнес-правила не расходятся; отсутствует только необходимый следующий уровень доказательств.
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`; Python PASS не повышает MT5 readiness.

### HSB-DOC-CONFLICT-030 — Production readiness versus missing broker evidence

- **Классификация результата:** `EVIDENCE_GAP`
- **Категория:** `READINESS`
- **Критичность:** `INFORMATIONAL`

#### Сторона A
- **Документ:** `Docs/BIG_SMALL_PRODUCTION_READINESS_REPORT_RU.md`
- **Раздел:** «Результат»
- **Подраздел:** итоговый readiness status, строка 34
- **Уникальный маркер или формула:** `REAL_TRADING_ALLOWED=NO`
- **Конкретное утверждение:** реальная торговля не разрешена.
- **Конкретное значение:** `NO`.
- **Единица измерения:** readiness status.
- **Профиль или режим:** production-readiness report.
- **Контекст применения:** допуск проекта к реальной торговле.

#### Сторона B
- **Документ:** `Docs/FULL_AUDIT_REPORT.md`
- **Раздел:** «V2.4.20 Position Resolution + Small Scenario Promote Fix»
- **Подраздел:** заключение о внешних проверках, строка 564
- **Уникальный маркер или формула:** `MetaEditor compilation and Strategy Tester validation still require MT5 and broker history outside this Linux container.`
- **Конкретное утверждение:** MetaEditor compile и Strategy Tester validation остаются невыполненными в Linux-контейнере и требуют MT5/broker history.
- **Конкретное значение:** MT5 compile/tester/broker evidence отсутствует в данном audit scope.
- **Единица измерения:** readiness/evidence level.
- **Профиль или режим:** full source audit в Linux-контейнере.
- **Контекст применения:** ограничение доказательности audit относительно MT5 и broker runtime.

#### Вывод проверки
- **Логическая сопоставимость:** обе стороны указывают на отсутствие достаточного runtime/broker evidence и не содержат противоположных readiness-утверждений.
- **Результат:** `REAL_TRADING_ALLOWED=NO` согласуется с прямым указанием Full Audit, что MetaEditor, Strategy Tester и broker-history validation ещё требуются. Это evidence gap, а не конфликт production-правил.
- **Статус:** `EVIDENCE_GAP`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** последующие MT5/Strategy Tester/broker validation этапы.
- **Почему выбран именно этот уровень критичности:** `INFORMATIONAL`, поскольку audit не заявляет production readiness; дата audit исключена как нерелевантная сторона сравнения.
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`; реальная торговля остаётся запрещённой.

### HSB-DOC-CONFLICT-031 — Legacy Split Hybrid terminology

- **Классификация результата:** `AUTHORITY_CONFLICT`
- **Категория:** `LEGACY_MIXING`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Split Big Geometry stage 1: BigCore + BigTrend + SmallBase»
- **Подраздел:** строка 991 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `## Split Big Geometry stage 1: BigCore + BigTrend + SmallBase`
- **Конкретное утверждение:** ## Split Big Geometry stage 1: BigCore + BigTrend + SmallBase.
- **Конкретное значение:** ## Split Big Geometry stage 1: BigCore + BigTrend + SmallBase
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_COMPLETE_MANUAL_RU.md`
- **Раздел:** «Область и назначение»
- **Подраздел:** строка 6 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `Far является единственным хвостом. BigCore и BigTrend направлены против Far,`
- **Конкретное утверждение:** Far является единственным хвостом. BigCore и BigTrend направлены против Far,.
- **Конкретное значение:** Far является единственным хвостом. BigCore и BigTrend направлены против Far,
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/MANUAL.md` и `Docs/HYBRID_SPLIT_BIG_COMPLETE_MANUAL_RU.md` без profile/scope discriminator даёт два разных правила для темы «Legacy Split Hybrid terminology»; единая production-норма не определена.
- **Статус:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Этап разрешения:** `3.1.8`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `BLOCKER` выбран потому, что тема «Legacy Split Hybrid terminology» блокирует следующий нормативный документ или способна изменить lot/money/state.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-032 — Split test plan duplicate

- **Классификация результата:** `DUPLICATION_WITH_DIFFERENCES`
- **Категория:** `DUPLICATION`

#### Сторона A
- **Документ:** `Docs/SPLIT_GEOMETRY_TEST_PLAN.md`
- **Раздел:** «Split Geometry Test Plan»
- **Подраздел:** строка 1 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `# Split Geometry Test Plan`
- **Конкретное утверждение:** # Split Geometry Test Plan.
- **Конкретное значение:** # Split Geometry Test Plan
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/TEST_PLAN_SPLIT_GEOMETRY.md`
- **Раздел:** «Split Geometry Test Plan»
- **Подраздел:** строка 1 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `# Split Geometry Test Plan`
- **Конкретное утверждение:** # Split Geometry Test Plan.
- **Конкретное значение:** # Split Geometry Test Plan
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/SPLIT_GEOMETRY_TEST_PLAN.md` и `Docs/TEST_PLAN_SPLIT_GEOMETRY.md` без profile/scope discriminator даёт два разных правила для темы «Split test plan duplicate»; единая production-норма не определена.
- **Статус:** `OPEN`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** `3.1.8`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `LOW` выбран потому, что тема «Split test plan duplicate» создаёт ограниченный scope/evidence gap без доказанного немедленного runtime ущерба.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-033 — Reserve persistence

- **Классификация результата:** `SCOPE_CONFLICT`
- **Категория:** `PERSISTENCE`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`
- **Раздел:** «1. `HybridCatchUpState`»
- **Подраздел:** строка 16 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `double finalReserveReal; double carryAvailable;`
- **Конкретное утверждение:** double finalReserveReal; double carryAvailable;.
- **Конкретное значение:** double finalReserveReal; double carryAvailable;
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/SPLIT_BIG_EXACT_PERSISTENCE_REPORT_RU.md`
- **Раздел:** «SplitGeometry Big — отчёт Этапа 4: точное persistence-восстановление»
- **Подраздел:** строка 1 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `# SplitGeometry Big — отчёт Этапа 4: точное persistence-восстановление`
- **Конкретное утверждение:** # SplitGeometry Big — отчёт Этапа 4: точное persistence-восстановление.
- **Конкретное значение:** # SplitGeometry Big — отчёт Этапа 4: точное persistence-восстановление
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Execution lifecycle
- **Фактическая цепь проверки:** persist confirmed reserve event→restart→rebuild event set→compare balance
- Accepted request не равен actual position/deal result; partial/retry/restart требуют нового verified snapshot.

#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md` и `Docs/SPLIT_BIG_EXACT_PERSISTENCE_REPORT_RU.md` без profile/scope discriminator даёт два разных правила для темы «Reserve persistence»; единая production-норма не определена.
- **Статус:** `OPEN`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** `3.1.3–3.1.8 по теме`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `MEDIUM` выбран потому, что тема «Reserve persistence» создаёт ограниченный scope/evidence gap без доказанного немедленного runtime ущерба.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-034 — Exactly-once Reserve credit

- **Классификация результата:** `AMBIGUITY`
- **Категория:** `MONEY_LEDGER`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_MONEY_FLOW.md`
- **Раздел:** «Hybrid Split Big — Money Flow»
- **Подраздел:** строка 3 / ближайший уникальный контекст
- **Уникальный маркер или формула:** ````text`
- **Конкретное утверждение:** ```text.
- **Конкретное значение:** ```text
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/BASKET_RISK_CONTRACT_RU.md`
- **Раздел:** «17. Partial execution и reconciliation»
- **Подраздел:** строка 481 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `4. применить idempotent confirmed ledger events exactly once;`
- **Конкретное утверждение:** 4. применить idempotent confirmed ledger events exactly once;.
- **Конкретное значение:** 4. применить idempotent confirmed ledger events exactly once;
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Денежная последовательность
- Ledger event requires stable namespace/key and one commit outcome; replay after restart must be no-op.
- **Rollback/exactly-once:** projected amount не коммитится; confirmed event обязан иметь idempotent key и reconciliation.
- **Partial/Final связь:** buckets не взаимозаменяются без отдельного authority.

#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/HYBRID_SPLIT_BIG_MONEY_FLOW.md` и `Docs/BASKET_RISK_CONTRACT_RU.md` без profile/scope discriminator даёт два разных правила для темы «Exactly-once Reserve credit»; единая production-норма не определена.
- **Статус:** `OPEN`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** `3.1.3–3.1.6 по теме`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `HIGH` выбран потому, что тема «Exactly-once Reserve credit» создаёт ограниченный scope/evidence gap без доказанного немедленного runtime ущерба.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-035 — Partial fill

- **Классификация результата:** `NO_DIRECT_CONFLICT_FOUND`
- **Категория:** `EXECUTION`
- **Критичность:** `INFORMATIONAL`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`
- **Раздел:** «Logic»
- **Подраздел:** invariant `LOGIC-06`, строка 36
- **Уникальный маркер или формула:** `Любой partial fill/reject требует reconciliation до следующего open.`
- **Конкретное утверждение:** partial fill блокирует продолжение открытий до reconciliation.
- **Конкретное значение:** обязательный переход к reconciliation.
- **Единица измерения:** execution/state rule.
- **Профиль или режим:** Hybrid execution invariant.
- **Контекст применения:** фактически частично исполненная брокером операция.

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_TEST_VECTORS.md`
- **Раздел:** таблица test vectors
- **Подраздел:** `TV-13`, строка 22
- **Уникальный маркер или формула:** `partial fill | requested .70, filled .35; ERROR_PARTIAL_EXECUTION`
- **Конкретное утверждение:** несовпадение requested 0.70 и filled 0.35 ожидаемо даёт `ERROR_PARTIAL_EXECUTION`.
- **Конкретное значение:** requested `0.70 lot`, filled `0.35 lot`.
- **Единица измерения:** lot и execution result.
- **Профиль или режим:** negative execution test vector.
- **Контекст применения:** detection частичного исполнения до continuation.

#### Вывод проверки
- **Логическая сопоставимость:** test vector проверяет то же правило остановки/reconciliation, которое задано invariant.
- **Результат:** прямого конфликта не найдено: обе стороны запрещают считать partial fill полным успехом и продолжать plan без reconciliation.
- **Статус:** `NO_DIRECT_CONFLICT_FOUND`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** не требуется; требуется будущая runtime-валидация реализации.
- **Почему выбран именно этот уровень критичности:** `INFORMATIONAL`, поскольку письменные требования согласованы; наличие runtime evidence оценивается отдельно.
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`.

### HSB-DOC-CONFLICT-036 — Retry idempotency

- **Классификация результата:** `SCOPE_CONFLICT`
- **Категория:** `EXECUTION`

#### Сторона A
- **Документ:** `Docs/BASKET_RISK_CONTRACT_RU.md`
- **Раздел:** «17. Partial execution и reconciliation»
- **Подраздел:** строка 486 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `Risk-reducing retry может продолжить только заранее определённый close route с actual ticket/volume и duplicate guard; он не разрешает новый open. Если reconciliation невозможно, результат ERROR/TERMINAL/manual intervention согласно существующему lifecycle.`
- **Конкретное утверждение:** Risk-reducing retry может продолжить только заранее определённый close route с actual ticket/volume и duplicate guard; он не разрешает новый open. Если reconciliation невозможно, результат ERROR/TERMINAL/manual intervention согласно существующему lifecycle..
- **Конкретное значение:** Risk-reducing retry может продолжить только заранее определённый close route с actual ticket/volume и duplicate guard; он не разрешает новый open. Если reconciliation невозможно, результат ERROR/TERMINAL/manual intervention согласно существующему lifecycle.
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_IMPLEMENTATION_REPORT_RU.md`
- **Раздел:** «Статус»
- **Подраздел:** строка 5 / ближайший уникальный контекст
- **Уникальный маркер или формула:** ``HYBRID_PREOPEN_DECISION_ENGINE_NOT_READY` до подтверждённой компиляции MetaEditor `0 errors / 0 warnings`.`
- **Конкретное утверждение:** `HYBRID_PREOPEN_DECISION_ENGINE_NOT_READY` до подтверждённой компиляции MetaEditor `0 errors / 0 warnings`..
- **Конкретное значение:** `HYBRID_PREOPEN_DECISION_ENGINE_NOT_READY` до подтверждённой компиляции MetaEditor `0 errors / 0 warnings`.
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Execution lifecycle
- **Фактическая цепь проверки:** retry key→duplicate lookup→single action→confirmed result
- Accepted request не равен actual position/deal result; partial/retry/restart требуют нового verified snapshot.

#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/BASKET_RISK_CONTRACT_RU.md` и `Docs/HYBRID_SPLIT_BIG_IMPLEMENTATION_REPORT_RU.md` без profile/scope discriminator даёт два разных правила для темы «Retry idempotency»; единая production-норма не определена.
- **Статус:** `OPEN`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** `3.1.3–3.1.8 по теме`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `MEDIUM` выбран потому, что тема «Retry idempotency» создаёт ограниченный scope/evidence gap без доказанного немедленного runtime ущерба.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-037 — Restart reconciliation

- **Классификация результата:** `SCOPE_CONFLICT`
- **Категория:** `RECONCILIATION`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`
- **Раздел:** «1. `HybridCatchUpState`»
- **Подраздел:** строка 36 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `/ realizedCyclePL / account money, confirmed/projected deals / own / `+HarvestNet+PartialFarNet` / да / да / reconciliation /`
- **Конкретное утверждение:** / realizedCyclePL / account money, confirmed/projected deals / own / `+HarvestNet+PartialFarNet` / да / да / reconciliation /.
- **Конкретное значение:** / realizedCyclePL / account money, confirmed/projected deals / own / `+HarvestNet+PartialFarNet` / да / да / reconciliation /
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/PERSISTENCE_AND_CLEAN_START_FINAL_REPORT_RU.md`
- **Раздел:** «Итоговый отчёт безопасности persistence»
- **Подраздел:** строка 3 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `START_SHA=7e24c34d08fb1cd35e810ac208eb9d181c3b84a4`
- **Конкретное утверждение:** START_SHA=7e24c34d08fb1cd35e810ac208eb9d181c3b84a4.
- **Конкретное значение:** START_SHA=7e24c34d08fb1cd35e810ac208eb9d181c3b84a4
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Execution lifecycle
- **Фактическая цепь проверки:** persist state/revision→restart→resolve positions/deals→reconciliation outcome
- Accepted request не равен actual position/deal result; partial/retry/restart требуют нового verified snapshot.

#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md` и `Docs/PERSISTENCE_AND_CLEAN_START_FINAL_REPORT_RU.md` без profile/scope discriminator даёт два разных правила для темы «Restart reconciliation»; единая production-норма не определена.
- **Статус:** `OPEN`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** `3.1.3–3.1.8 по теме`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `MEDIUM` выбран потому, что тема «Restart reconciliation» создаёт ограниченный scope/evidence gap без доказанного немедленного runtime ущерба.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-038 — Final Close partial execution

- **Классификация результата:** `AMBIGUITY`
- **Категория:** `FINAL_CLOSE`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`
- **Раздел:** «Hybrid Split Big — нормативная временная модель Catch-Up»
- **Подраздел:** строка 3 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `**Статус:** `NORMATIVE`. Единственный нормативный источник временной семантики Big Harvest. Модель строго последовательная, не alternative-price. Каждый level закрывает только существующие в его `StateBefore` рабочие позиции, после чего строит новый state.`
- **Конкретное утверждение:** **Статус:** `NORMATIVE`. Единственный нормативный источник временной семантики Big Harvest. Модель строго последовательная, не alternative-price. Каждый level закрывает только существующие в его `StateBefore` рабочие позиции, после чего строит новый state..
- **Конкретное значение:** **Статус:** `NORMATIVE`. Единственный нормативный источник временной семантики Big Harvest. Модель строго последовательная, не alternative-price. Каждый level закрывает только существующие в его `StateBefore` рабочие позиции, после чего строит новый state.
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «V2.4.11 Actual Volume After Partial Close»
- **Подраздел:** строка 666 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `This rule now covers BigHarvest Far budget closes, Small Reverse Big partial closes, and retry paths. Full Far closes also verify that MT5 reports zero remaining volume before clearing context; otherwise the EA logs `FULL_CLOSE_INCOMPLETE` and retries instead `
- **Конкретное утверждение:** This rule now covers BigHarvest Far budget closes, Small Reverse Big partial closes, and retry paths. Full Far closes also verify that MT5 reports zero remaining volume before clearing context; otherwise the EA logs `FULL_CLOSE_INCOMPLETE` and retries instead .
- **Конкретное значение:** This rule now covers BigHarvest Far budget closes, Small Reverse Big partial closes, and retry paths. Full Far closes also verify that MT5 reports zero remaining volume before clearing context; otherwise the EA logs `FULL_CLOSE_INCOMPLETE` and retries instead
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Execution lifecycle
- **Фактическая цепь проверки:** final-close request→actual residual check→retry/reconcile→zero positions confirmation
- Accepted request не равен actual position/deal result; partial/retry/restart требуют нового verified snapshot.

#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md` и `Docs/MANUAL.md` без profile/scope discriminator даёт два разных правила для темы «Final Close partial execution»; единая production-норма не определена.
- **Статус:** `OPEN`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** `3.1.3–3.1.6 по теме`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `HIGH` выбран потому, что тема «Final Close partial execution» создаёт ограниченный scope/evidence gap без доказанного немедленного runtime ущерба.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-039 — MaxHarvestLevels behavior

- **Классификация результата:** `ORDERING_CONFLICT`
- **Категория:** `STATE_MACHINE`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`
- **Раздел:** «Hybrid Split Big — нормативная временная модель Catch-Up»
- **Подраздел:** строка 3 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `**Статус:** `NORMATIVE`. Единственный нормативный источник временной семантики Big Harvest. Модель строго последовательная, не alternative-price. Каждый level закрывает только существующие в его `StateBefore` рабочие позиции, после чего строит новый state.`
- **Конкретное утверждение:** **Статус:** `NORMATIVE`. Единственный нормативный источник временной семантики Big Harvest. Модель строго последовательная, не alternative-price. Каждый level закрывает только существующие в его `StateBefore` рабочие позиции, после чего строит новый state..
- **Конкретное значение:** **Статус:** `NORMATIVE`. Единственный нормативный источник временной семантики Big Harvest. Модель строго последовательная, не alternative-price. Каждый level закрывает только существующие в его `StateBefore` рабочие позиции, после чего строит новый state.
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «2. Параметры»
- **Подраздел:** строка 31 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `MaxHarvestLevels = 7`
- **Конкретное утверждение:** MaxHarvestLevels = 7.
- **Конкретное значение:** MaxHarvestLevels = 7
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md` и `Docs/MANUAL.md` без profile/scope discriminator даёт два разных правила для темы «MaxHarvestLevels behavior»; единая production-норма не определена.
- **Статус:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Этап разрешения:** `3.1.6`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `CRITICAL` выбран потому, что тема «MaxHarvestLevels behavior» блокирует следующий нормативный документ или способна изменить lot/money/state.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-040 — Reverse limit behavior

- **Классификация результата:** `MISSING_DEFINITION`
- **Категория:** `STATE_MACHINE`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`
- **Раздел:** «Hybrid Split Big — нормативная временная модель Catch-Up»
- **Подраздел:** строка 3 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `**Статус:** `NORMATIVE`. Единственный нормативный источник временной семантики Big Harvest. Модель строго последовательная, не alternative-price. Каждый level закрывает только существующие в его `StateBefore` рабочие позиции, после чего строит новый state.`
- **Конкретное утверждение:** **Статус:** `NORMATIVE`. Единственный нормативный источник временной семантики Big Harvest. Модель строго последовательная, не alternative-price. Каждый level закрывает только существующие в его `StateBefore` рабочие позиции, после чего строит новый state..
- **Конкретное значение:** **Статус:** `NORMATIVE`. Единственный нормативный источник временной семантики Big Harvest. Модель строго последовательная, не alternative-price. Каждый level закрывает только существующие в его `StateBefore` рабочие позиции, после чего строит новый state.
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Параметры защиты»
- **Подраздел:** строка 175 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `input int MaxReverseCycles = 3;`
- **Конкретное утверждение:** input int MaxReverseCycles = 3;.
- **Конкретное значение:** input int MaxReverseCycles = 3;
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md` и `Docs/MANUAL.md` без profile/scope discriminator даёт два разных правила для темы «Reverse limit behavior»; единая production-норма не определена.
- **Статус:** `OPEN`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** `3.1.3–3.1.6 по теме`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `HIGH` выбран потому, что тема «Reverse limit behavior» создаёт ограниченный scope/evidence gap без доказанного немедленного runtime ущерба.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-041 — Invalid geometry behavior

- **Классификация результата:** `MISSING_DEFINITION`
- **Категория:** `STATE_MACHINE`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`
- **Раздел:** «14. Result, terminal and reason contract»
- **Подраздел:** строка 148 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `Full-Far affordability routes to `CATCHUP_REQUIRES_FINAL_CLOSE_PREVIEW`; invalid residual to `CATCHUP_REJECT_INVALID_FAR_REMAINDER`; component min-volume to `CATCHUP_TERMINAL_MIN_VOLUME`. Other exact failures: `CATCHUP_STATE_INVALID`, `CATCHUP_TRIGGER_INVALID``
- **Конкретное утверждение:** Full-Far affordability routes to `CATCHUP_REQUIRES_FINAL_CLOSE_PREVIEW`; invalid residual to `CATCHUP_REJECT_INVALID_FAR_REMAINDER`; component min-volume to `CATCHUP_TERMINAL_MIN_VOLUME`. Other exact failures: `CATCHUP_STATE_INVALID`, `CATCHUP_TRIGGER_INVALID`.
- **Конкретное значение:** Full-Far affordability routes to `CATCHUP_REQUIRES_FINAL_CLOSE_PREVIEW`; invalid residual to `CATCHUP_REJECT_INVALID_FAR_REMAINDER`; component min-volume to `CATCHUP_TERMINAL_MIN_VOLUME`. Other exact failures: `CATCHUP_STATE_INVALID`, `CATCHUP_TRIGGER_INVALID`
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Параметры защиты»
- **Подраздел:** строка 180 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `input bool StopOnInvalidReverseGeometry = true;`
- **Конкретное утверждение:** input bool StopOnInvalidReverseGeometry = true;.
- **Конкретное значение:** input bool StopOnInvalidReverseGeometry = true;
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md` и `Docs/MANUAL.md` без profile/scope discriminator даёт два разных правила для темы «Invalid geometry behavior»; единая production-норма не определена.
- **Статус:** `OPEN`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** `3.1.3–3.1.6 по теме`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `HIGH` выбран потому, что тема «Invalid geometry behavior» создаёт ограниченный scope/evidence gap без доказанного немедленного runtime ущерба.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-042 — Basket Risk preview versus execution

- **Классификация результата:** `NO_DIRECT_CONFLICT_FOUND`
- **Категория:** `RISK`

#### Сторона A
- **Документ:** `Docs/BASKET_RISK_CONTRACT_RU.md`
- **Раздел:** «Basket Risk — нормативный контракт Этапа 2.0»
- **Подраздел:** строка 1 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `# Basket Risk — нормативный контракт Этапа 2.0`
- **Конкретное утверждение:** # Basket Risk — нормативный контракт Этапа 2.0.
- **Конкретное значение:** # Basket Risk — нормативный контракт Этапа 2.0
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_THREE_LAWS_MATH_MANUAL_RU.md`
- **Раздел:** «Глава 4. Абсолютный и относительный P/L — уровень A»
- **Подраздел:** строка 43 / ближайший уникальный контекст
- **Уникальный маркер или формула:** ``PLbasket(x)=PLbasket0+(C+T-S-F)Vx`, где `PLbasket0=PLF0+PLC0+PLT0+PLS0`.`
- **Конкретное утверждение:** `PLbasket(x)=PLbasket0+(C+T-S-F)Vx`, где `PLbasket0=PLF0+PLC0+PLT0+PLS0`..
- **Конкретное значение:** `PLbasket(x)=PLbasket0+(C+T-S-F)Vx`, где `PLbasket0=PLF0+PLC0+PLT0+PLS0`.
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Вывод проверки
- **Точная несовместимость:** Стороны описывают разные последовательные уровни или scope и могут сосуществовать; ни одно из приведённых утверждений явно не отрицает другое.
- **Статус:** `NO_DIRECT_CONFLICT_FOUND`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** `не требуется; сохранить результат проверки`
- **Результат:** Проверка темы завершена: прямого междокументного противоречия не найдено; запись не является основанием для пользовательского выбора.
- **Почему выбран именно этот уровень критичности:** `INFORMATIONAL` выбран потому, что тема «Basket Risk preview versus execution» создаёт ограниченный scope/evidence gap без доказанного немедленного runtime ущерба.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-043 — Cycle versus account risk

- **Классификация результата:** `MISSING_DEFINITION`
- **Категория:** `RISK`

#### Сторона A
- **Документ:** `Docs/BASKET_RISK_CONTRACT_RU.md`
- **Раздел:** «3. Термины и соответствие существующей системе»
- **Подраздел:** строка 42 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `/ Cycle Basket Risk / новый будущий слой / Aggregate только активного Symbol+Magic+CycleID /`
- **Конкретное утверждение:** / Cycle Basket Risk / новый будущий слой / Aggregate только активного Symbol+Magic+CycleID /.
- **Конкретное значение:** / Cycle Basket Risk / новый будущий слой / Aggregate только активного Symbol+Magic+CycleID /
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_THREE_LAWS_MATH_MANUAL_RU.md`
- **Раздел:** «Глава 2. Словарь, типы и размерности»
- **Подраздел:** строка 33 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `/ `CycleID` [STATE] / `cycleId` / ulong / неизменен внутри цикла; mismatch = ERROR /`
- **Конкретное утверждение:** / `CycleID` [STATE] / `cycleId` / ulong / неизменен внутри цикла; mismatch = ERROR /.
- **Конкретное значение:** / `CycleID` [STATE] / `cycleId` / ulong / неизменен внутри цикла; mismatch = ERROR /
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/BASKET_RISK_CONTRACT_RU.md` и `Docs/HYBRID_SPLIT_BIG_THREE_LAWS_MATH_MANUAL_RU.md` без profile/scope discriminator даёт два разных правила для темы «Cycle versus account risk»; единая production-норма не определена.
- **Статус:** `OPEN`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** `3.1.3–3.1.6 по теме`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `HIGH` выбран потому, что тема «Cycle versus account risk» создаёт ограниченный scope/evidence gap без доказанного немедленного runtime ущерба.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-044 — Terminal-safe versus mathematically-safe

- **Классификация результата:** `NO_DIRECT_CONFLICT_FOUND`
- **Категория:** `RISK`

#### Сторона A
- **Документ:** `Docs/BASKET_RISK_CONTRACT_RU.md`
- **Раздел:** «5. Место в gate graph»
- **Подраздел:** строка 69 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `→ RISK → MARGIN → WORST_CASE → FUTURE_SMALL`
- **Конкретное утверждение:** → RISK → MARGIN → WORST_CASE → FUTURE_SMALL.
- **Конкретное значение:** → RISK → MARGIN → WORST_CASE → FUTURE_SMALL
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_THREE_LAWS_MATH_MANUAL_RU.md`
- **Раздел:** «Глава 2. Словарь, типы и размерности»
- **Подраздел:** строка 31 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `/ `Risk` [MONEY] / `OldRisk`, `NextRisk` / double / worst-case loss до контрольной цены; неотрицателен /`
- **Конкретное утверждение:** / `Risk` [MONEY] / `OldRisk`, `NextRisk` / double / worst-case loss до контрольной цены; неотрицателен /.
- **Конкретное значение:** / `Risk` [MONEY] / `OldRisk`, `NextRisk` / double / worst-case loss до контрольной цены; неотрицателен /
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Вывод проверки
- **Точная несовместимость:** Стороны описывают разные последовательные уровни или scope и могут сосуществовать; ни одно из приведённых утверждений явно не отрицает другое.
- **Статус:** `NO_DIRECT_CONFLICT_FOUND`
- **Требуется решение пользователя:** `NO`
- **Этап разрешения:** `не требуется; сохранить результат проверки`
- **Результат:** Проверка темы завершена: прямого междокументного противоречия не найдено; запись не является основанием для пользовательского выбора.
- **Почему выбран именно этот уровень критичности:** `INFORMATIONAL` выбран потому, что тема «Terminal-safe versus mathematically-safe» создаёт ограниченный scope/evidence gap без доказанного немедленного runtime ущерба.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

### HSB-DOC-CONFLICT-045 — Source-of-truth competition

- **Классификация результата:** `AUTHORITY_CONFLICT`
- **Категория:** `DUPLICATION`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_COMPLETE_MANUAL_RU.md`
- **Раздел:** «Three laws»
- **Подраздел:** строка 41 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `Law 1: projected coverage slope is `ReserveShare*(C+T-S)` and must exceed F.`
- **Конкретное утверждение:** Law 1: projected coverage slope is `ReserveShare*(C+T-S)` and must exceed F..
- **Конкретное значение:** Law 1: projected coverage slope is `ReserveShare*(C+T-S)` and must exceed F.
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; смешение единиц не предполагается.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`
- **Раздел:** «Hybrid Split Big — System Invariants»
- **Подраздел:** строка 3 / ближайший уникальный контекст
- **Уникальный маркер или формула:** `Нарушение любого `MUST` запрещает необратимое действие и переводит результат в reject/error/reconciliation. Safe default не заменяет failed invariant.`
- **Конкретное утверждение:** Нарушение любого `MUST` запрещает необратимое действие и переводит результат в reject/error/reconciliation. Safe default не заменяет failed invariant..
- **Конкретное значение:** Нарушение любого `MUST` запрещает необратимое действие и переводит результат в reject/error/reconciliation. Safe default не заменяет failed invariant.
- **Единица измерения:** определяется маркером: ratio/lot/money/state/evidence; не переносится между scope.
- **Профиль или режим:** профиль и evidence scope указан самим документом.
- **Контекст применения:** только область раздела и архитектурное поколение документа.


#### Вывод проверки
- **Точная несовместимость:** Одновременное применение утверждений из `Docs/HYBRID_SPLIT_BIG_COMPLETE_MANUAL_RU.md` и `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md` без profile/scope discriminator даёт два разных правила для темы «Source-of-truth competition»; единая production-норма не определена.
- **Статус:** `NEEDS_USER_DECISION`
- **Требуется решение пользователя:** `YES`
- **Этап разрешения:** `3.1.8`
- **Результат:** До указанного этапа оба варианта запрещено использовать как единое runtime-разрешение.
- **Почему выбран именно этот уровень критичности:** `BLOCKER` выбран потому, что тема «Source-of-truth competition» блокирует следующий нормативный документ или способна изменить lot/money/state.
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION` для открытого конфликта; `USE_ONLY_AS_EVIDENCE` для результата без прямого конфликта.

## 3. Индекс по документам

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

### `Docs/SPLIT_GEOMETRY_TEST_PLAN.md`
- HSB-DOC-CONFLICT-032

### `Docs/STAGE_1_2_4_1_EVIDENCE_RU.md`
- HSB-DOC-CONFLICT-029

### `Docs/TEST_PLAN_SPLIT_GEOMETRY.md`
- HSB-DOC-CONFLICT-032

## 4. Покрытие обязательных тем

| № | ID | Тема | Результат |
|---:|---|---|---|
| 1 | HSB-DOC-CONFLICT-001 | BigRatio values | PARAMETER_PROFILE_CONFLICT |
| 2 | HSB-DOC-CONFLICT-002 | SmallRatio values | PARAMETER_PROFILE_CONFLICT |
| 3 | HSB-DOC-CONFLICT-003 | CloseBigOnSmall values | PARAMETER_PROFILE_CONFLICT |
| 4 | HSB-DOC-CONFLICT-004 | RemainBigOnSmall values | PARAMETER_PROFILE_CONFLICT |
| 5 | HSB-DOC-CONFLICT-005 | CloseFarShare values | PARAMETER_PROFILE_CONFLICT |
| 6 | HSB-DOC-CONFLICT-006 | ReserveShare values | PARAMETER_PROFILE_CONFLICT |
| 7 | HSB-DOC-CONFLICT-007 | SmallReserveShare values | NO_DIRECT_CONFLICT_FOUND |
| 8 | HSB-DOC-CONFLICT-008 | Reserve in Partial Far | NO_DIRECT_CONFLICT_FOUND |
| 9 | HSB-DOC-CONFLICT-009 | RecoveryPL includes Reserve | NO_DIRECT_CONFLICT_FOUND |
| 10 | HSB-DOC-CONFLICT-010 | RecoveryPL includes Initial Plus | NO_DIRECT_CONFLICT_FOUND |
| 11 | HSB-DOC-CONFLICT-011 | RecoveryPL Symbol filter | MISSING_DEFINITION |
| 12 | HSB-DOC-CONFLICT-012 | RecoveryPL Magic filter | MISSING_DEFINITION |
| 13 | HSB-DOC-CONFLICT-013 | Gross versus Net Profit | FORMULA_CONFLICT |
| 14 | HSB-DOC-CONFLICT-014 | Commission swap fee | MISSING_DEFINITION |
| 15 | HSB-DOC-CONFLICT-015 | Projected versus Realized Reserve | SCOPE_CONFLICT |
| 16 | HSB-DOC-CONFLICT-016 | Planned versus actual close result | NO_DIRECT_CONFLICT_FOUND |
| 17 | HSB-DOC-CONFLICT-017 | Final Close preview versus actual success | AMBIGUITY |
| 18 | HSB-DOC-CONFLICT-018 | Small close trigger | SCOPE_CONFLICT |
| 19 | HSB-DOC-CONFLICT-019 | Old Far full versus partial close | SCOPE_CONFLICT |
| 20 | HSB-DOC-CONFLICT-020 | New Far source | AUTHORITY_CONFLICT |
| 21 | HSB-DOC-CONFLICT-021 | Next Big base | SCOPE_CONFLICT |
| 22 | HSB-DOC-CONFLICT-022 | new Big less than old Far | MISSING_DEFINITION |
| 23 | HSB-DOC-CONFLICT-023 | Negative Small Reverse Net | MISSING_DEFINITION |
| 24 | HSB-DOC-CONFLICT-024 | Small Far Big close order | ORDERING_CONFLICT |
| 25 | HSB-DOC-CONFLICT-025 | Reserve credit order | AMBIGUITY |
| 26 | HSB-DOC-CONFLICT-026 | State transition order | MISSING_DEFINITION |
| 27 | HSB-DOC-CONFLICT-027 | Requested versus executed volume | NO_DIRECT_CONFLICT_FOUND |
| 28 | HSB-DOC-CONFLICT-028 | FLOOR CEILING NEAREST | FORMULA_CONFLICT |
| 29 | HSB-DOC-CONFLICT-029 | Python PASS versus MT5 NOT_RUN | EVIDENCE_GAP |
| 30 | HSB-DOC-CONFLICT-030 | Production readiness versus missing broker evidence | EVIDENCE_GAP |
| 31 | HSB-DOC-CONFLICT-031 | Legacy Split Hybrid terminology | AUTHORITY_CONFLICT |
| 32 | HSB-DOC-CONFLICT-032 | Split test plan duplicate | DUPLICATION_WITH_DIFFERENCES |
| 33 | HSB-DOC-CONFLICT-033 | Reserve persistence | SCOPE_CONFLICT |
| 34 | HSB-DOC-CONFLICT-034 | Exactly-once Reserve credit | AMBIGUITY |
| 35 | HSB-DOC-CONFLICT-035 | Partial fill | NO_DIRECT_CONFLICT_FOUND |
| 36 | HSB-DOC-CONFLICT-036 | Retry idempotency | SCOPE_CONFLICT |
| 37 | HSB-DOC-CONFLICT-037 | Restart reconciliation | SCOPE_CONFLICT |
| 38 | HSB-DOC-CONFLICT-038 | Final Close partial execution | AMBIGUITY |
| 39 | HSB-DOC-CONFLICT-039 | MaxHarvestLevels behavior | ORDERING_CONFLICT |
| 40 | HSB-DOC-CONFLICT-040 | Reverse limit behavior | MISSING_DEFINITION |
| 41 | HSB-DOC-CONFLICT-041 | Invalid geometry behavior | MISSING_DEFINITION |
| 42 | HSB-DOC-CONFLICT-042 | Basket Risk preview versus execution | NO_DIRECT_CONFLICT_FOUND |
| 43 | HSB-DOC-CONFLICT-043 | Cycle versus account risk | MISSING_DEFINITION |
| 44 | HSB-DOC-CONFLICT-044 | Terminal-safe versus mathematically-safe | NO_DIRECT_CONFLICT_FOUND |
| 45 | HSB-DOC-CONFLICT-045 | Source-of-truth competition | AUTHORITY_CONFLICT |

## 5. Логическая верификация сторон всех обязательных тем

В таблице `PASS` означает, что стороны относятся к заявленной теме и логически сопоставимы; для `NO_DIRECT_CONFLICT_FOUND` и `EVIDENCE_GAP` результат проверки не считается подтверждённым конфликтом.

| ID | Side A topic | Side B topic | Comparable | Result derived |
|---|---|---|---|---|
| HSB-DOC-CONFLICT-001 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-002 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-003 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-004 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-005 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-006 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-007 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-008 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-009 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-010 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-011 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-012 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-013 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-014 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-015 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-016 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-017 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-018 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-019 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-020 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-021 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-022 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-023 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-024 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-025 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-026 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-027 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-028 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-029 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-030 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-031 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-032 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-033 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-034 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-035 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-036 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-037 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-038 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-039 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-040 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-041 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-042 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-043 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-044 | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-045 | PASS | PASS | PASS | PASS |

Проверкой запрещено выводить конфликт из одинаковых значений, отсутствия упоминания, даты audit или evidence разных уровней. Для записей 007, 008, 029, 030 и 035 ложная конфликтная классификация снята.

## 6. Пересчитанная статистика

```text
TOTAL_REVIEWED_TOPICS=45
CONFIRMED_CONFLICTS=34
PARAMETER_PROFILE_CONFLICTS=6
FORMULA_CONFLICTS=2
ORDERING_CONFLICTS=2
SCOPE_CONFLICTS=8
AUTHORITY_CONFLICTS=3
MISSING_DEFINITIONS=9
AMBIGUITIES=4
EVIDENCE_MISMATCHES=0
EVIDENCE_GAP=2
DUPLICATION_WITH_DIFFERENCES=1
NO_DIRECT_CONFLICT_FOUND=9
NEEDS_USER_DECISION=13
MANDATORY_TOPICS_REVIEWED=45
BUSINESS_CONFLICTS_AUTO_RESOLVED=0
STAGE_3_1_2_SECOND_CORRECTION_STATUS=PASS
```

Арифметика: `CONFIRMED_CONFLICTS(34) + NO_DIRECT_CONFLICT_FOUND(9) + EVIDENCE_GAP(2) = 45`. `MISSING_DEFINITIONS`, `AMBIGUITIES`, `FORMULA_CONFLICTS`, `ORDERING_CONFLICTS`, `SCOPE_CONFLICTS`, `AUTHORITY_CONFLICTS` и `DUPLICATION_WITH_DIFFERENCES` входят в `CONFIRMED_CONFLICTS`; `EVIDENCE_GAP` не входит.

## 7. Quality controls

```text
GENERIC_SIDE_TEXT_COUNT=0
GENERIC_CONFLICT_DESCRIPTION_COUNT=0
GENERIC_IMPACT_TEXT_COUNT=0
RECORDS_WITH_CONCRETE_SIDE_A=45
RECORDS_WITH_CONCRETE_SIDE_B=39
RECORDS_WITH_SECTION_OR_UNIQUE_MARKER=45
PARAMETER_RECORDS_WITH_VALUES=7
FALSE_CONFLICT_032_FIXED=PASS
SEVERITY_JUSTIFICATION_PRESENT=45
MANDATORY_TOPICS_REVIEWED=45
BUSINESS_CONFLICTS_AUTO_RESOLVED=0
```

HSB-DOC-CONFLICT-032 теперь сравнивает только `Docs/SPLIT_GEOMETRY_TEST_PLAN.md` и `Docs/TEST_PLAN_SPLIT_GEOMETRY.md`; исходная ложная пара Hybrid manual/invariants удалена.

## 8. Специальные проверки второй коррекции

```text
CONFLICT_007_SAME_VALUE_HANDLED=PASS
CONFLICT_008_TWO_SIDED_PROOF_OR_RECLASSIFIED=PASS
CONFLICT_029_EVIDENCE_LOGIC_FIXED=PASS
CONFLICT_030_TOPIC_RELEVANT_SIDE_B=PASS
SAME_VALUES_MARKED_AS_CONFLICT=0
UNRELATED_SIDE_COMPARISONS=0
AUDIT_DATE_USED_AS_READINESS_CLAIM=0
GENERIC_TWO_RULES_TEXT_IN_EVIDENCE_RECORDS=0
SIDE_A_TOPIC_MATCH=PASS (45/45)
SIDE_B_TOPIC_MATCH=PASS (45/45)
A_AND_B_LOGICALLY_COMPARABLE=PASS (45/45)
CONFLICT_ACTUALLY_DERIVED_FROM_A_AND_B=PASS (45/45)
```

Код, параметры, другие Docs, MQL5, Python, Tests, Tools, Sets, workflows и runtime не менялись. Этап 3.1.3 не выполнялся.

Ожидается повторная проверка пользователя. Этап 3.1.3 не выполнялся.
