# Третье исправление Этапа 3.1.2 — доказательный реестр конфликтов Hybrid Split Big

Статус: `PASS`
Parent SHA: `20d50cecfe1fcc4444c2bf536ad32fe43d4ec44f`

## Ограничение полномочий

> Реестр фиксирует доказанные расхождения, gaps и совместимость, но не выбирает нормативную сторону, не меняет бизнес-логику, не назначает production profile и не создаёт source of truth. Этап 3.1.3 не выполнялся.

## Сводная таблица

| ID | Тема | Классификация | Критичность | RequiresUserDecision |
|---|---|---|---|---|
| HSB-DOC-CONFLICT-001 | BigRatio values | PARAMETER_PROFILE_CONFLICT | BLOCKER | YES |
| HSB-DOC-CONFLICT-002 | SmallRatio values | PARAMETER_PROFILE_CONFLICT | BLOCKER | YES |
| HSB-DOC-CONFLICT-003 | CloseBigOnSmall values | PARAMETER_PROFILE_CONFLICT | BLOCKER | YES |
| HSB-DOC-CONFLICT-004 | RemainBigOnSmall values | PARAMETER_PROFILE_CONFLICT | BLOCKER | YES |
| HSB-DOC-CONFLICT-005 | CloseFarShare values | PARAMETER_PROFILE_CONFLICT | BLOCKER | YES |
| HSB-DOC-CONFLICT-006 | ReserveShare values | PARAMETER_PROFILE_CONFLICT | BLOCKER | YES |
| HSB-DOC-CONFLICT-007 | SmallReserveShare values | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-008 | Reserve in Partial Far | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-009 | RecoveryPL includes Reserve | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-010 | RecoveryPL includes Initial Plus | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-011 | RecoveryPL Symbol filter | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-012 | RecoveryPL Magic filter | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-013 | Gross versus Net Profit | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-014 | Commission swap fee | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-015 | Projected versus Realized Reserve | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-016 | Planned versus actual close result | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-017 | Final Close preview versus actual success | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-018 | Small close trigger | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-019 | Old Far full versus partial close | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-020 | New Far source | SCOPE_CONFLICT | BLOCKER | YES |
| HSB-DOC-CONFLICT-021 | Next Big base | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-022 | new Big less than old Far | MISSING_DEFINITION | HIGH | YES |
| HSB-DOC-CONFLICT-023 | Negative Small Reverse Net | MISSING_DEFINITION | HIGH | YES |
| HSB-DOC-CONFLICT-024 | Small Far Big close order | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-025 | Reserve credit order | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-026 | State transition order | MISSING_DEFINITION | HIGH | NO |
| HSB-DOC-CONFLICT-027 | Requested versus executed volume | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-028 | FLOOR CEILING NEAREST | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-029 | Python PASS versus MT5 NOT_RUN | EVIDENCE_GAP | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-030 | Production readiness versus broker evidence | EVIDENCE_GAP | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-031 | Legacy Split Hybrid terminology | MISSING_DEFINITION | HIGH | YES |
| HSB-DOC-CONFLICT-032 | Split test plan duplicate | DUPLICATION_WITH_DIFFERENCES | LOW | NO |
| HSB-DOC-CONFLICT-033 | Reserve persistence | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-034 | Exactly-once Reserve credit | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-035 | Partial fill | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-036 | Retry idempotency | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-037 | Restart reconciliation | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-038 | Final Close partial execution | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-039 | MaxHarvestLevels behavior | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-040 | Reverse limit behavior | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-041 | Invalid geometry behavior | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-042 | Basket Risk preview versus execution | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-043 | Cycle versus account risk | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-044 | Terminal-safe versus mathematically-safe | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |
| HSB-DOC-CONFLICT-045 | Source-of-truth competition | NO_DIRECT_CONFLICT_FOUND | INFORMATIONAL | NO |

## Подробные доказательные записи

### HSB-DOC-CONFLICT-001 — BigRatio values

- **Категория:** `PARAMETER`
- **Основная классификация:** `PARAMETER_PROFILE_CONFLICT`
- **Критичность:** `BLOCKER`
- **RequiresUserDecision:** `YES`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Параметры / соответствующий profile block»
- **Подраздел:** «BigRatio input»
- **Точный маркер:** `BigRatio = 1.30`
- **Конкретное утверждение:** Manual задаёт BigRatio=1.30 для описанного профиля.
- **Конкретное значение или формула:** `1.30`
- **Размерность:** `RATIO`
- **Профиль:** manual/default or named profile
- **Scope:** Manual; legacy/transition generation; per-cycle input; requested profile

#### Сторона B
- **Документ:** `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md`
- **Раздел:** «Текущие входные параметры»
- **Подраздел:** «baseline лотов/распределения»
- **Точный маркер:** `BigRatio=1.15`
- **Конкретное утверждение:** Money-model baseline задаёт BigRatio=1.15.
- **Конкретное значение или формула:** `1.15`
- **Размерность:** `RATIO`
- **Профиль:** money-model baseline
- **Scope:** Baseline; documented inputs; requested profile

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: один input BigRatio
- **Проверка одной стадии:** PASS: выбор профиля до расчёта
- **Проверка размерностей:** PASS: RATIO/RATIO
- **Проверка scope:** CONFLICT: оба набора претендуют на baseline без единого discriminator
- **Прямое отрицание:** YES: разные числовые значения
- **Доказанный результат:** Значения 1.30 и 1.15 не могут одновременно быть значением одного production-профиля; победитель не выбран.
- **Обоснование классификации:** `PARAMETER_PROFILE_CONFLICT` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** Без выбора profile discriminator нельзя завершить таблицу нормативных параметров; это блокирует этап 3.1.7.
- **Необходимость решения пользователя:** `YES`; нужен выбор business/profile policy.
- **Этап разрешения:** 3.1.7
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`

### HSB-DOC-CONFLICT-002 — SmallRatio values

- **Категория:** `PARAMETER`
- **Основная классификация:** `PARAMETER_PROFILE_CONFLICT`
- **Критичность:** `BLOCKER`
- **RequiresUserDecision:** `YES`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Параметры / соответствующий profile block»
- **Подраздел:** «SmallRatio input»
- **Точный маркер:** `SmallRatio = 0.37`
- **Конкретное утверждение:** Manual задаёт SmallRatio=0.37 для описанного профиля.
- **Конкретное значение или формула:** `0.37`
- **Размерность:** `RATIO`
- **Профиль:** manual/default or named profile
- **Scope:** Manual; legacy/transition generation; per-cycle input; requested profile

#### Сторона B
- **Документ:** `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md`
- **Раздел:** «Текущие входные параметры»
- **Подраздел:** «baseline лотов/распределения»
- **Точный маркер:** `SmallRatio=0.25`
- **Конкретное утверждение:** Money-model baseline задаёт SmallRatio=0.25.
- **Конкретное значение или формула:** `0.25`
- **Размерность:** `RATIO`
- **Профиль:** money-model baseline
- **Scope:** Baseline; documented inputs; requested profile

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: один input SmallRatio
- **Проверка одной стадии:** PASS: выбор профиля до расчёта
- **Проверка размерностей:** PASS: RATIO/RATIO
- **Проверка scope:** CONFLICT: оба набора претендуют на baseline без единого discriminator
- **Прямое отрицание:** YES: разные числовые значения
- **Доказанный результат:** Значения 0.37 и 0.25 не могут одновременно быть значением одного production-профиля; победитель не выбран.
- **Обоснование классификации:** `PARAMETER_PROFILE_CONFLICT` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** Без выбора profile discriminator нельзя завершить таблицу нормативных параметров; это блокирует этап 3.1.7.
- **Необходимость решения пользователя:** `YES`; нужен выбор business/profile policy.
- **Этап разрешения:** 3.1.7
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`

### HSB-DOC-CONFLICT-003 — CloseBigOnSmall values

- **Категория:** `PARAMETER`
- **Основная классификация:** `PARAMETER_PROFILE_CONFLICT`
- **Критичность:** `BLOCKER`
- **RequiresUserDecision:** `YES`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Параметры / соответствующий profile block»
- **Подраздел:** «CloseBigOnSmall input»
- **Точный маркер:** `CloseBigOnSmall = 0.30`
- **Конкретное утверждение:** Manual задаёт CloseBigOnSmall=0.30 для описанного профиля.
- **Конкретное значение или формула:** `0.30`
- **Размерность:** `RATIO`
- **Профиль:** manual/default or named profile
- **Scope:** Manual; legacy/transition generation; per-cycle input; requested profile

#### Сторона B
- **Документ:** `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md`
- **Раздел:** «Текущие входные параметры»
- **Подраздел:** «baseline лотов/распределения»
- **Точный маркер:** `CloseBigOnSmall=0.40`
- **Конкретное утверждение:** Money-model baseline задаёт CloseBigOnSmall=0.40.
- **Конкретное значение или формула:** `0.40`
- **Размерность:** `RATIO`
- **Профиль:** money-model baseline
- **Scope:** Baseline; documented inputs; requested profile

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: один input CloseBigOnSmall
- **Проверка одной стадии:** PASS: выбор профиля до расчёта
- **Проверка размерностей:** PASS: RATIO/RATIO
- **Проверка scope:** CONFLICT: оба набора претендуют на baseline без единого discriminator
- **Прямое отрицание:** YES: разные числовые значения
- **Доказанный результат:** Значения 0.30 и 0.40 не могут одновременно быть значением одного production-профиля; победитель не выбран.
- **Обоснование классификации:** `PARAMETER_PROFILE_CONFLICT` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** Без выбора profile discriminator нельзя завершить таблицу нормативных параметров; это блокирует этап 3.1.7.
- **Необходимость решения пользователя:** `YES`; нужен выбор business/profile policy.
- **Этап разрешения:** 3.1.7
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`

### HSB-DOC-CONFLICT-004 — RemainBigOnSmall values

- **Категория:** `PARAMETER`
- **Основная классификация:** `PARAMETER_PROFILE_CONFLICT`
- **Критичность:** `BLOCKER`
- **RequiresUserDecision:** `YES`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Параметры / соответствующий profile block»
- **Подраздел:** «RemainBigOnSmall input»
- **Точный маркер:** `RemainBigOnSmall = 0.70`
- **Конкретное утверждение:** Manual задаёт RemainBigOnSmall=0.70 для описанного профиля.
- **Конкретное значение или формула:** `0.70`
- **Размерность:** `RATIO`
- **Профиль:** manual/default or named profile
- **Scope:** Manual; legacy/transition generation; per-cycle input; requested profile

#### Сторона B
- **Документ:** `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md`
- **Раздел:** «Текущие входные параметры»
- **Подраздел:** «baseline лотов/распределения»
- **Точный маркер:** `RemainBigOnSmall=0.60`
- **Конкретное утверждение:** Money-model baseline задаёт RemainBigOnSmall=0.60.
- **Конкретное значение или формула:** `0.60`
- **Размерность:** `RATIO`
- **Профиль:** money-model baseline
- **Scope:** Baseline; documented inputs; requested profile

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: один input RemainBigOnSmall
- **Проверка одной стадии:** PASS: выбор профиля до расчёта
- **Проверка размерностей:** PASS: RATIO/RATIO
- **Проверка scope:** CONFLICT: оба набора претендуют на baseline без единого discriminator
- **Прямое отрицание:** YES: разные числовые значения
- **Доказанный результат:** Значения 0.70 и 0.60 не могут одновременно быть значением одного production-профиля; победитель не выбран.
- **Обоснование классификации:** `PARAMETER_PROFILE_CONFLICT` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** Без выбора profile discriminator нельзя завершить таблицу нормативных параметров; это блокирует этап 3.1.7.
- **Необходимость решения пользователя:** `YES`; нужен выбор business/profile policy.
- **Этап разрешения:** 3.1.7
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`

### HSB-DOC-CONFLICT-005 — CloseFarShare values

- **Категория:** `PARAMETER`
- **Основная классификация:** `PARAMETER_PROFILE_CONFLICT`
- **Критичность:** `BLOCKER`
- **RequiresUserDecision:** `YES`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Параметры / соответствующий profile block»
- **Подраздел:** «CloseFarShare input»
- **Точный маркер:** `CloseFarShare = 0.90`
- **Конкретное утверждение:** Manual задаёт CloseFarShare=0.90 для описанного профиля.
- **Конкретное значение или формула:** `0.90`
- **Размерность:** `RATIO`
- **Профиль:** manual/default or named profile
- **Scope:** Manual; legacy/transition generation; per-cycle input; requested profile

#### Сторона B
- **Документ:** `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md`
- **Раздел:** «Текущие входные параметры»
- **Подраздел:** «baseline лотов/распределения»
- **Точный маркер:** `CloseFarShare=0.10`
- **Конкретное утверждение:** Money-model baseline задаёт CloseFarShare=0.10.
- **Конкретное значение или формула:** `0.10`
- **Размерность:** `RATIO`
- **Профиль:** money-model baseline
- **Scope:** Baseline; documented inputs; requested profile

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: один input CloseFarShare
- **Проверка одной стадии:** PASS: выбор профиля до расчёта
- **Проверка размерностей:** PASS: RATIO/RATIO
- **Проверка scope:** CONFLICT: оба набора претендуют на baseline без единого discriminator
- **Прямое отрицание:** YES: разные числовые значения
- **Доказанный результат:** Значения 0.90 и 0.10 не могут одновременно быть значением одного production-профиля; победитель не выбран.
- **Обоснование классификации:** `PARAMETER_PROFILE_CONFLICT` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** Без выбора profile discriminator нельзя завершить таблицу нормативных параметров; это блокирует этап 3.1.7.
- **Необходимость решения пользователя:** `YES`; нужен выбор business/profile policy.
- **Этап разрешения:** 3.1.7
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`

### HSB-DOC-CONFLICT-006 — ReserveShare values

- **Категория:** `PARAMETER`
- **Основная классификация:** `PARAMETER_PROFILE_CONFLICT`
- **Критичность:** `BLOCKER`
- **RequiresUserDecision:** `YES`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Параметры / соответствующий profile block»
- **Подраздел:** «ReserveShare input»
- **Точный маркер:** `ReserveShare = 0.10`
- **Конкретное утверждение:** Manual задаёт ReserveShare=0.10 для описанного профиля.
- **Конкретное значение или формула:** `0.10`
- **Размерность:** `RATIO`
- **Профиль:** manual/default or named profile
- **Scope:** Manual; legacy/transition generation; per-cycle input; requested profile

#### Сторона B
- **Документ:** `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md`
- **Раздел:** «Текущие входные параметры»
- **Подраздел:** «baseline лотов/распределения»
- **Точный маркер:** `ReserveShare=0.90`
- **Конкретное утверждение:** Money-model baseline задаёт ReserveShare=0.90.
- **Конкретное значение или формула:** `0.90`
- **Размерность:** `RATIO`
- **Профиль:** money-model baseline
- **Scope:** Baseline; documented inputs; requested profile

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: один input ReserveShare
- **Проверка одной стадии:** PASS: выбор профиля до расчёта
- **Проверка размерностей:** PASS: RATIO/RATIO
- **Проверка scope:** CONFLICT: оба набора претендуют на baseline без единого discriminator
- **Прямое отрицание:** YES: разные числовые значения
- **Доказанный результат:** Значения 0.10 и 0.90 не могут одновременно быть значением одного production-профиля; победитель не выбран.
- **Обоснование классификации:** `PARAMETER_PROFILE_CONFLICT` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** Без выбора profile discriminator нельзя завершить таблицу нормативных параметров; это блокирует этап 3.1.7.
- **Необходимость решения пользователя:** `YES`; нужен выбор business/profile policy.
- **Этап разрешения:** 3.1.7
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`

### HSB-DOC-CONFLICT-007 — SmallReserveShare values

- **Категория:** `PARAMETER`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Small Reserve Logic»
- **Подраздел:** «Risk Compression Reverse»
- **Точный маркер:** `SmallReserveShare = 0.05`
- **Конкретное утверждение:** SmallReserveShare равен 0.05; credit выполняется только для положительного SmallScenarioRealNet.
- **Конкретное значение или формула:** `0.05`
- **Размерность:** `RATIO`
- **Профиль:** manual/runtime input
- **Scope:** Small-at-Far; realized positive net

#### Сторона B
- **Документ:** `Docs/MONEY_MODEL_COMPLETION_BASELINE_RU.md`
- **Раздел:** «Текущие входные параметры»
- **Подраздел:** «baseline распределения»
- **Точный маркер:** `SmallReserveShare=0.05`
- **Конкретное утверждение:** Baseline также фиксирует SmallReserveShare=0.05.
- **Конкретное значение или формула:** `0.05`
- **Размерность:** `RATIO`
- **Профиль:** money-model baseline
- **Scope:** Baseline allocation profile

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: один параметр
- **Проверка одной стадии:** PASS: allocation Small Reserve
- **Проверка размерностей:** PASS: RATIO/RATIO
- **Проверка scope:** PASS: profile labels различаются, значение и назначение совпадают
- **Прямое отрицание:** NO
- **Доказанный результат:** Во всех найденных profile/baseline источниках значение 0.05; противоположного значения нет.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL: согласованность параметра подтверждена.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** не требуется
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-008 — Reserve in Partial Far

- **Категория:** `RESERVE`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_MONEY_FLOW.md`
- **Раздел:** «Forbidden edges»
- **Подраздел:** «money-flow edges»
- **Точный маркер:** `FinalReserve -X-> Partial Far`
- **Конкретное утверждение:** FinalReserve не финансирует Partial Far; PartialBudget является отдельным bucket.
- **Конкретное значение или формула:** `forbidden edge`
- **Размерность:** `MONEY`
- **Профиль:** Hybrid money contract
- **Scope:** confirmed Harvest allocation; cycle bucket

#### Сторона B
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Big-сценарий»
- **Подраздел:** «CloseFarBudget calculation»
- **Точный маркер:** `CloseFarBudget = NetProfit × CloseFarShare; ReserveAdd = NetProfit × ReserveShare`
- **Конкретное утверждение:** Partial Far расходует CloseFarBudget, ReserveAdd начисляется отдельно.
- **Конкретное значение или формула:** `separate buckets`
- **Размерность:** `MONEY`
- **Профиль:** manual Big harvest
- **Scope:** realized NetProfit allocation

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: источник Partial Far
- **Проверка одной стадии:** PASS: allocation до partial close
- **Проверка размерностей:** PASS: MONEY/MONEY
- **Проверка scope:** PASS: обе стороны разделяют Partial и Reserve
- **Прямое отрицание:** NO
- **Доказанный результат:** Правила совместимы; отсутствие имени FinalReserve в Manual не является разрешением расхода.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL: двойной расход не доказан.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** не требуется
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-009 — RecoveryPL includes Reserve

- **Категория:** `RECOVERY_PL`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`
- **Раздел:** «Money»
- **Подраздел:** «MONEY-06»
- **Точный маркер:** `Reserve уже входит в RealizedCyclePL`
- **Конкретное утверждение:** Reserve входит в RealizedCyclePL и не добавляется к RecoveryPL повторно.
- **Конкретное значение или формула:** `RecoveryPL excludes duplicate Reserve`
- **Размерность:** `MONEY`
- **Профиль:** Hybrid invariant
- **Scope:** cycle; confirmed accounting

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_FORMULA_REFERENCE.md`
- **Раздел:** «Формулы уровня B»
- **Подраздел:** «RecoveryPLCloseNow»
- **Точный маркер:** `RecoveryPLCloseNow=RealizedCyclePL+FloatingManagedPL-ExpectedExitCosts; no duplicate commission or reserve`
- **Конкретное утверждение:** Формула использует RealizedCyclePL и прямо запрещает повторный Reserve.
- **Конкретное значение или формула:** `formula`
- **Размерность:** `MONEY`
- **Профиль:** Hybrid formula reference
- **Scope:** cycle close-now; projected floating plus confirmed realized

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: RecoveryPL composition
- **Проверка одной стадии:** PASS: close-now composition
- **Проверка размерностей:** PASS: MONEY/MONEY
- **Проверка scope:** PASS: один Hybrid cycle scope
- **Прямое отрицание:** NO
- **Доказанный результат:** Обе стороны запрещают повторное добавление Reserve; прямого конфликта нет.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL: формулы согласованы.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** не требуется
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-010 — RecoveryPL includes Initial Plus

- **Категория:** `RECOVERY_PL`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Real Recovery P/L Validation»
- **Подраздел:** «cycle boundary»
- **Точный маркер:** `first plus remains excluded from TotalReserve, RealRecoveryPL, RealCyclePL and FinalCloseAllowed`
- **Конкретное утверждение:** Manual исключает Initial Plus из RecoveryPL decision money.
- **Конкретное значение или формула:** `excluded`
- **Размерность:** `BOOLEAN`
- **Профиль:** manual/runtime
- **Scope:** cycle starts after profitable initial leg close

#### Сторона B
- **Документ:** `Docs/FULL_AUDIT_REPORT.md`
- **Раздел:** «V2.4.21 Real Recovery Profit + Final Close Pass Criteria»
- **Подраздел:** «InitialIgnoredProfit»
- **Точный маркер:** `InitialIgnoredProfit ... is excluded from realRecoveryPL, reserve accounting, OnTester(), and STATE_CLOSED_PROFIT eligibility`
- **Конкретное утверждение:** Full Audit подтверждает то же исключение.
- **Конкретное значение или формула:** `excluded`
- **Размерность:** `BOOLEAN`
- **Профиль:** audit/runtime evidence
- **Scope:** audited recovery cycle

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: Initial Plus membership
- **Проверка одной стадии:** PASS: cycle boundary
- **Проверка размерностей:** PASS: BOOLEAN/BOOLEAN
- **Проверка scope:** PASS: одинаковый runtime recovery scope
- **Прямое отрицание:** NO
- **Доказанный результат:** Обе стороны явно исключают Initial Plus.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL: согласованность подтверждена.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** не требуется
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-011 — RecoveryPL Symbol filter

- **Категория:** `RECOVERY_PL`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «BigHarvest reserve from HistoryDeals»
- **Подраздел:** «deal filters»
- **Точный маркер:** `HistorySelect ... DEAL_POSITION_ID, MagicNumber, symbol, comments`
- **Конкретное утверждение:** Actual lifecycle net фильтруется по symbol, magic и position identity.
- **Конкретное значение или формула:** `symbol filter required`
- **Размерность:** `SCOPE`
- **Профиль:** manual/runtime
- **Scope:** confirmed deal history; managed cycle

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`
- **Раздел:** «Identity and logic»
- **Подраздел:** «LOGIC-04»
- **Точный маркер:** `roles идентифицируются Symbol+Magic+CycleID+identifier`
- **Конкретное утверждение:** Cycle aggregation изолируется по Symbol+Magic+CycleID+identifier.
- **Конкретное значение или формула:** `Symbol identity required`
- **Размерность:** `SCOPE`
- **Профиль:** Hybrid invariant
- **Scope:** managed cycle identity

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: managed P/L isolation
- **Проверка одной стадии:** PASS: history aggregation
- **Проверка размерностей:** PASS: SCOPE/SCOPE
- **Проверка scope:** PASS: оба требуют symbol isolation
- **Прямое отрицание:** NO
- **Доказанный результат:** Ни один источник не разрешает cross-symbol contamination.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL: совместимые identity rules.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** не требуется
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-012 — RecoveryPL Magic filter

- **Категория:** `RECOVERY_PL`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «BigHarvest reserve from HistoryDeals»
- **Подраздел:** «deal filters»
- **Точный маркер:** `HistoryDealGetDouble ... MagicNumber, symbol, comments`
- **Конкретное утверждение:** History deal aggregation использует MagicNumber.
- **Конкретное значение или формула:** `Magic filter required`
- **Размерность:** `SCOPE`
- **Профиль:** manual/runtime
- **Scope:** confirmed deal history

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`
- **Раздел:** «Identity and logic»
- **Подраздел:** «LOGIC-04»
- **Точный маркер:** `Symbol+Magic+CycleID+identifier`
- **Конкретное утверждение:** Role identity включает Magic.
- **Конкретное значение или формула:** `Magic identity required`
- **Размерность:** `SCOPE`
- **Профиль:** Hybrid invariant
- **Scope:** managed cycle

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: Magic isolation
- **Проверка одной стадии:** PASS: history/cycle identity
- **Проверка размерностей:** PASS: SCOPE/SCOPE
- **Проверка scope:** PASS
- **Прямое отрицание:** NO
- **Доказанный результат:** Обе стороны требуют Magic isolation.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL: прямого конфликта нет.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** не требуется
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-013 — Gross versus Net Profit

- **Категория:** `MONEY_LEDGER`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Big-сценарий»
- **Подраздел:** «NetProfit»
- **Точный маркер:** `NetProfit = ProfitBig - LossSmall - Costs`
- **Конкретное утверждение:** Manual определяет net как gross leg results минус costs.
- **Конкретное значение или формула:** `formula`
- **Размерность:** `MONEY`
- **Профиль:** manual Big harvest
- **Scope:** projected/actual as stated by section

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_FORMULA_REFERENCE.md`
- **Раздел:** «Формулы уровня B»
- **Подраздел:** «LegNet»
- **Точный маркер:** `LegNet=OrderCalcProfit(...)-not-yet-included costs`
- **Конкретное утверждение:** Formula reference также вычитает ещё не учтённые costs.
- **Конкретное значение или формула:** `formula`
- **Размерность:** `MONEY`
- **Профиль:** Hybrid broker-money
- **Scope:** per leg projected net

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: net money derivation
- **Проверка одной стадии:** PASS: cost application
- **Проверка размерностей:** PASS: MONEY/MONEY
- **Проверка scope:** PASS: aggregate vs leg are composable scopes
- **Прямое отрицание:** NO
- **Доказанный результат:** LegNet является компонентом aggregate NetProfit, не альтернативной gross formula.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL: прямой formula conflict не найден.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** не требуется
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-014 — Commission swap fee

- **Категория:** `MONEY_LEDGER`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «BigHarvest reserve from HistoryDeals»
- **Подраздел:** «actual costs»
- **Точный маркер:** `DEAL_PROFIT/COMMISSION/SWAP`
- **Конкретное утверждение:** Actual reserve update использует confirmed history profit, commission и swap.
- **Конкретное значение или формула:** `actual deal fields`
- **Размерность:** `MONEY`
- **Профиль:** manual/runtime
- **Scope:** confirmed deals

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_FORMULA_REFERENCE.md`
- **Раздел:** «Формулы уровня B»
- **Подраздел:** «LegNet»
- **Точный маркер:** `OrderCalcProfit(...)-not-yet-included costs`
- **Конкретное утверждение:** Projected LegNet вычитает только ещё не включённые costs.
- **Конкретное значение или формула:** `projected net`
- **Размерность:** `MONEY`
- **Профиль:** Hybrid formula
- **Scope:** projected broker money

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: trading costs
- **Проверка одной стадии:** PASS: projected vs actual stages explicit
- **Проверка размерностей:** PASS: MONEY/MONEY
- **Проверка scope:** PASS: sequential projected/confirmed scopes
- **Прямое отрицание:** NO
- **Доказанный результат:** Источники разделяют projected cost estimate и actual deal costs; fee требует будущей broker validation, но отрицания нет.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL: бизнес-конфликт не доказан.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** money model consolidation
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-015 — Projected versus Realized Reserve

- **Категория:** `RESERVE`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_FORMULA_REFERENCE.md`
- **Раздел:** «Формулы уровня B»
- **Подраздел:** «FinalReserveProjected»
- **Точный маркер:** `FinalReserveProjected=FinalReserveReal+β*max(EligibleHarvestCloseNet,0)`
- **Конкретное утверждение:** Projected reserve является forecast поверх confirmed real reserve.
- **Конкретное значение или формула:** `formula`
- **Размерность:** `MONEY`
- **Профиль:** Hybrid formula
- **Scope:** projected pre-close

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_MONEY_FLOW.md`
- **Раздел:** «Forbidden edges»
- **Подраздел:** «projected persistence»
- **Точный маркер:** `Projected money -X-> persisted bucket`
- **Конкретное утверждение:** Projected money запрещено сохранять как confirmed bucket.
- **Конкретное значение или формула:** `forbidden edge`
- **Размерность:** `MONEY`
- **Профиль:** Hybrid money flow
- **Scope:** persisted confirmed ledger

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: Reserve status
- **Проверка одной стадии:** PASS: forecast precedes commit
- **Проверка размерностей:** PASS: MONEY/MONEY
- **Проверка scope:** PASS: projected and confirmed explicitly distinct
- **Прямое отрицание:** NO
- **Доказанный результат:** Последовательные стадии совместимы; projection не объявлен realized credit.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** не требуется
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-016 — Planned versus actual close result

- **Категория:** `EXECUTION`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`
- **Раздел:** «Identity and logic»
- **Подраздел:** «LOGIC-05»
- **Точный маркер:** `Projected result никогда не подменяет confirmed actual result`
- **Конкретное утверждение:** Plan result не является actual result.
- **Конкретное значение или формула:** `projected != confirmed`
- **Размерность:** `BOOLEAN`
- **Профиль:** Hybrid invariant
- **Scope:** pre-open versus post-execution

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_STATE_TRANSITION_TABLE.md`
- **Раздел:** «State transition truth table»
- **Подраздел:** «HARVEST_PENDING»
- **Точный маркер:** `all Harvest deals | all confirmed | actual net then allocation`
- **Конкретное утверждение:** Allocation начинается после confirmed deals и actual net.
- **Конкретное значение или формула:** `confirmed deals`
- **Размерность:** `ORDERING`
- **Профиль:** Hybrid state model
- **Scope:** post-execution

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: close result provenance
- **Проверка одной стадии:** PASS: planned→confirmed stage
- **Проверка размерностей:** PASS: BOOLEAN/ORDERING linked by lifecycle
- **Проверка scope:** PASS
- **Прямое отрицание:** NO
- **Доказанный результат:** Обе стороны требуют actual confirmation.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** не требуется
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-017 — Final Close preview versus actual success

- **Категория:** `FINAL_CLOSE`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_STATE_TRANSITION_TABLE.md`
- **Раздел:** «State transition truth table»
- **Подраздел:** «HARVEST_RECONCILE»
- **Точный маркер:** `Final Close preview | PASS | immutable final plan | FINAL_CLOSE_PENDING`
- **Конкретное утверждение:** Preview PASS только создаёт pending plan.
- **Конкретное значение или формула:** `preview transition`
- **Размерность:** `STATE`
- **Профиль:** Hybrid state model
- **Scope:** pre-execution

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_STATE_TRANSITION_TABLE.md`
- **Раздел:** «State transition truth table»
- **Подраздел:** «FINAL_CLOSE_PENDING»
- **Точный маркер:** `positions=0 and actual threshold PASS | confirmed deals reconciled | CLOSED_PROFIT`
- **Конкретное утверждение:** Success требует отсутствия positions и actual reconciliation.
- **Конкретное значение или формула:** `actual success transition`
- **Размерность:** `STATE`
- **Профиль:** Hybrid state model
- **Scope:** post-execution

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: Final Close lifecycle
- **Проверка одной стадии:** PASS: sequential states
- **Проверка размерностей:** PASS: STATE/STATE
- **Проверка scope:** PASS: preview and actual are distinct stages
- **Прямое отрицание:** NO
- **Доказанный результат:** Preview не приравнен actual success.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** не требуется
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-018 — Small close trigger

- **Категория:** `SMALL_SCENARIO`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Small-at-Far Scenario»
- **Подраздел:** «trigger»
- **Точный маркер:** `STATE_WAIT_SMALL_TO_FAR ... waits until current price reaches old Far open price`
- **Конкретное утверждение:** Small trigger переводит в wait; close происходит после Far touch.
- **Конкретное значение или формула:** `Far-touch trigger`
- **Размерность:** `PRICE`
- **Профиль:** manual/runtime
- **Scope:** Small-at-Far

#### Сторона B
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Small Scenario V2.4»
- **Подраздел:** «ProcessSmallAtFarTouch»
- **Точный маркер:** `waits for Small leg to reach old Far open price, then closes Small`
- **Конкретное утверждение:** V2.4 повторяет тот же Far-touch trigger.
- **Конкретное значение или формула:** `Far-touch trigger`
- **Размерность:** `PRICE`
- **Профиль:** manual V2.4
- **Scope:** Small-at-Far

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: Small close trigger
- **Проверка одной стадии:** PASS
- **Проверка размерностей:** PASS: PRICE/PRICE
- **Проверка scope:** PASS: same scenario
- **Прямое отрицание:** NO
- **Доказанный результат:** Обе формулировки требуют Far touch.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** не требуется
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-019 — Old Far full versus partial close

- **Категория:** `SMALL_SCENARIO`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Small-at-Far Scenario»
- **Подраздел:** «ProcessSmallAtFarTouch»
- **Точный маркер:** `Small закрывается 100%, старый Far закрывается 100%, Big закрывается только на CloseBigOnSmall`
- **Конкретное утверждение:** Old Far full close относится к Small-at-Far transition.
- **Конкретное значение или формула:** `100%`
- **Размерность:** `RATIO`
- **Профиль:** manual Small scenario
- **Scope:** Small-at-Far

#### Сторона B
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Big-сценарий»
- **Подраздел:** «CloseFarLotFinal»
- **Точный маркер:** `CloseFarLotFinal = MIN(FarLot, CloseFarLotRounded)`
- **Конкретное утверждение:** Partial Far относится к Big harvest budget close.
- **Конкретное значение или формула:** `budget-limited`
- **Размерность:** `LOT`
- **Профиль:** manual Big scenario
- **Scope:** Big harvest

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: Old Far close
- **Проверка одной стадии:** PASS: scenario stage differs
- **Проверка размерностей:** PASS: RATIO/LOT behavior is scenario-qualified, not competing formula
- **Проверка scope:** PASS: distinct named scenarios
- **Прямое отрицание:** NO
- **Доказанный результат:** Full close и partial close относятся к разным сценариям; один не отменяет другой.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** не требуется
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-020 — New Far source

- **Категория:** `GEOMETRY`
- **Основная классификация:** `SCOPE_CONFLICT`
- **Критичность:** `BLOCKER`
- **RequiresUserDecision:** `YES`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «New Far Calculation»
- **Подраздел:** «legacy Big remainder»
- **Точный маркер:** `The new Far is the remaining Big after the actual partial close`
- **Конкретное утверждение:** Manual разрешает остаток монолитного Big как New Far.
- **Конкретное значение или формула:** `remaining Big`
- **Размерность:** `LOT`
- **Профиль:** legacy/manual geometry
- **Scope:** Small-at-Far; actual position

#### Сторона B
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Split Big Geometry»
- **Подраздел:** «BigTrendNeverBecomesFar»
- **Точный маркер:** `only the remaining BigCore can become a new Far ... BigTrendNeverBecomesFar=true`
- **Конкретное утверждение:** Split/Hybrid разрешает только остаток BigCore.
- **Конкретное значение или формула:** `remaining BigCore only`
- **Размерность:** `LOT`
- **Профиль:** Split/Hybrid geometry
- **Scope:** confirmed Small transition

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: source position role
- **Проверка одной стадии:** PASS: NewFar promotion
- **Проверка размерностей:** PASS: LOT/LOT
- **Проверка scope:** CONFLICT: оба текста находятся в одном Manual без обязательного mode discriminator на promotion call
- **Прямое отрицание:** YES: monolithic Big versus BigCore-only
- **Доказанный результат:** Для единого runtime пути допустимые role sources различаются; выбор зависит от architecture mode и должен быть нормативно ограждён.
- **Обоснование классификации:** `SCOPE_CONFLICT` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** BLOCKER: без discriminator нельзя определить ownership NewFar.
- **Необходимость решения пользователя:** `YES`; нужен выбор business/profile policy.
- **Этап разрешения:** 3.1.6/3.1.8
- **Временное правило:** `DO_NOT_USE_FOR_IMPLEMENTATION`

### HSB-DOC-CONFLICT-021 — Next Big base

- **Категория:** `GEOMETRY`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Risk Compression Reverse»
- **Подраздел:** «next geometry»
- **Точный маркер:** `NewBig = NewFar * BigRatio`
- **Конкретное утверждение:** Manual рассчитывает следующий Big от NewFar.
- **Конкретное значение или формула:** `formula`
- **Размерность:** `LOT`
- **Профиль:** manual reverse
- **Scope:** post-promotion

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`
- **Раздел:** «Temporal and Far invariants»
- **Подраздел:** «FAR-05»
- **Точный маркер:** `Следующие Core/Trend/Small рассчитываются от residual Far`
- **Конкретное утверждение:** Hybrid split legs также рассчитываются от residual/New Far.
- **Конкретное значение или формула:** `residual Far base`
- **Размерность:** `LOT`
- **Профиль:** Hybrid invariant
- **Scope:** next state

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: next basket base
- **Проверка одной стадии:** PASS
- **Проверка размерностей:** PASS: LOT/LOT
- **Проверка scope:** PASS: monolithic/split formulas share residual Far base
- **Прямое отрицание:** NO
- **Доказанный результат:** Прямого конфликта нет.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** не требуется
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-022 — new Big less than old Far

- **Категория:** `GEOMETRY`
- **Основная классификация:** `MISSING_DEFINITION`
- **Критичность:** `HIGH`
- **RequiresUserDecision:** `YES`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Risk Compression Reverse»
- **Подраздел:** «geometry rule»
- **Точный маркер:** `NewBig < OldFar`
- **Конкретное утверждение:** Manual требует strict NewBig<OldFar.
- **Конкретное значение или формула:** `strict inequality`
- **Размерность:** `LOT`
- **Профиль:** manual reverse
- **Scope:** next Big gross unspecified

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`
- **Раздел:** «Geometry»
- **Подраздел:** «GEO-02»
- **Точный маркер:** `NextCore + NextTrend < OldFar * MaximumNewBigToOldFarRatio`
- **Конкретное утверждение:** Hybrid сравнивает split Big gross с OldFar, умноженным на configurable ratio.
- **Конкретное значение или формула:** `ratio-bounded inequality`
- **Размерность:** `LOT`
- **Профиль:** Hybrid invariant
- **Scope:** next split basket

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: next Big gross bound
- **Проверка одной стадии:** PASS
- **Проверка размерностей:** PASS: LOT/LOT
- **Проверка scope:** AMBIGUOUS: scopes align only if MaximumNewBigToOldFarRatio semantics/value fixed
- **Прямое отрицание:** NO direct negation
- **Доказанный результат:** Не определено, обязан ли MaximumNewBigToOldFarRatio быть <=1; поэтому эквивалентность strict rule не доказана.
- **Обоснование классификации:** `MISSING_DEFINITION` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** HIGH: отсутствие bound меняет допустимую геометрию.
- **Необходимость решения пользователя:** `YES`; нужен выбор business/profile policy.
- **Этап разрешения:** 3.1.3/3.1.4
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-023 — Negative Small Reverse Net

- **Категория:** `MONEY_LEDGER`
- **Основная классификация:** `MISSING_DEFINITION`
- **Критичность:** `HIGH`
- **RequiresUserDecision:** `YES`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Small-at-Far money validation»
- **Подраздел:** «SmallReverseNet»
- **Точный маркер:** `SmallReverseNet = SmallPL + OldFarPL + ClosedBigPL`
- **Конкретное утверждение:** Manual определяет signed SmallReverseNet и configurable AllowNegativeSmallReverseNet policy.
- **Конкретное значение или формула:** `signed net`
- **Размерность:** `MONEY`
- **Профиль:** manual/runtime
- **Scope:** Small transition

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_FORMULA_REFERENCE.md`
- **Раздел:** «Final Close, allocation and limits»
- **Подраздел:** «TransitionNet cap»
- **Точный маркер:** `TransitionNet ... >= -MaximumAllowedTransitionLoss`
- **Конкретное утверждение:** Hybrid formula допускает loss только в пределах утверждённого cap.
- **Конкретное значение или формула:** `signed net with cap`
- **Размерность:** `MONEY`
- **Профиль:** Hybrid formula
- **Scope:** transition

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: transition net loss
- **Проверка одной стадии:** PASS
- **Проверка размерностей:** PASS: MONEY/MONEY
- **Проверка scope:** MISSING: связь AllowNegativeSmallReverseNet с MaximumAllowedTransitionLoss не определена
- **Прямое отрицание:** NO direct negation
- **Доказанный результат:** Не хватает единого правила precedence между boolean allowance и monetary cap.
- **Обоснование классификации:** `MISSING_DEFINITION` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** HIGH: разные implementations могут принять разный убыточный transition.
- **Необходимость решения пользователя:** `YES`; нужен выбор business/profile policy.
- **Этап разрешения:** 3.1.5/3.1.6
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-024 — Small Far Big close order

- **Категория:** `SMALL_SCENARIO`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Small Scenario V2.4»
- **Подраздел:** «ProcessSmallAtFarTouch»
- **Точный маркер:** `closes Small, closes old Far, partially closes Big`
- **Конкретное утверждение:** Manual order: Small→OldFar→Big partial.
- **Конкретное значение или формула:** `ordered sequence`
- **Размерность:** `ORDERING`
- **Профиль:** manual/runtime
- **Scope:** Small-at-Far

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_COMPLETE_MANUAL_RU.md`
- **Раздел:** «Small»
- **Подраздел:** «transition order»
- **Точный маркер:** `SmallBase close → OldFar close → BigTrend close → staged BigCore close`
- **Конкретное утверждение:** Hybrid order refines Big into Trend/Core after the same Small→Far prefix.
- **Конкретное значение или формула:** `ordered sequence`
- **Размерность:** `ORDERING`
- **Профиль:** Hybrid split
- **Scope:** Small transition

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: same transition
- **Проверка одной стадии:** PASS: refinement explicit
- **Проверка размерностей:** PASS: ORDERING/ORDERING
- **Проверка scope:** PASS: split sequence refines rather than reverses legacy prefix
- **Прямое отрицание:** NO
- **Доказанный результат:** Нет доказанного reversal порядка.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** не требуется
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-025 — Reserve credit order

- **Категория:** `RESERVE`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_MONEY_FLOW.md`
- **Раздел:** «Hybrid Split Big — Money Flow»
- **Подраздел:** «confirmed events»
- **Точный маркер:** `Каждое ребро существует только после confirmed event`
- **Конкретное утверждение:** Bucket credit происходит после confirmed deal event.
- **Конкретное значение или формула:** `confirmed credit`
- **Размерность:** `ORDERING`
- **Профиль:** Hybrid money flow
- **Scope:** post-deal ledger

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_STATE_TRANSITION_TABLE.md`
- **Раздел:** «State transition truth table»
- **Подраздел:** «HARVEST_PENDING»
- **Точный маркер:** `all confirmed | actual net then allocation`
- **Конкретное утверждение:** State model также ставит allocation после confirmed deals и actual net.
- **Конкретное значение или формула:** `actual net then allocation`
- **Размерность:** `ORDERING`
- **Профиль:** Hybrid state model
- **Scope:** Harvest post-execution

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: Reserve credit timing
- **Проверка одной стадии:** PASS
- **Проверка размерностей:** PASS: ORDERING/ORDERING
- **Проверка scope:** PASS
- **Прямое отрицание:** NO
- **Доказанный результат:** Обе стороны требуют confirmed actual result до credit.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** не требуется
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-026 — State transition order

- **Категория:** `STATE_MACHINE`
- **Основная классификация:** `MISSING_DEFINITION`
- **Критичность:** `HIGH`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_STATE_TRANSITION_TABLE.md`
- **Раздел:** «State transition truth table»
- **Подраздел:** «HARVEST lifecycle»
- **Точный маркер:** `HARVEST_PENDING → HARVEST_RECONCILE → FINAL_CLOSE_PENDING/FAR_ACTIVE`
- **Конкретное утверждение:** Truth table задаёт state order Hybrid harvest.
- **Конкретное значение или формула:** `state chain`
- **Размерность:** `STATE`
- **Профиль:** Hybrid state model
- **Scope:** Harvest

#### Сторона B
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Pending FSM and Real Reserve Fix»
- **Подраздел:** «pending states»
- **Точный маркер:** `STATE_BIG_HARVEST_CLOSE_FAR and other pending phases`
- **Конкретное утверждение:** Manual перечисляет runtime phases, но не даёт полного mapping на Hybrid truth-table states.
- **Конкретное значение или формула:** `runtime state names`
- **Размерность:** `STATE`
- **Профиль:** manual/runtime generation
- **Scope:** Big harvest pending FSM

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: state ordering
- **Проверка одной стадии:** PASS
- **Проверка размерностей:** PASS: STATE/STATE
- **Проверка scope:** MISSING: crosswalk between two state vocabularies absent
- **Прямое отрицание:** NO direct negation
- **Доказанный результат:** Нельзя доказать conflict или equivalence без state-name mapping.
- **Обоснование классификации:** `MISSING_DEFINITION` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** HIGH: отсутствующий mapping затрудняет единую реализацию/restart.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** 3.1.6
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-027 — Requested versus executed volume

- **Категория:** `EXECUTION`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/BASKET_RISK_CONTRACT_RU.md`
- **Раздел:** «Partial execution и reconciliation»
- **Подраздел:** «typed observations»
- **Точный маркер:** `OPEN_PARTIAL — requested open исполнен не полностью; actual remaining volumes MUST be checked`
- **Конкретное утверждение:** Contract различает requested и actual filled/remaining volume.
- **Конкретное значение или формула:** `requested vs actual`
- **Размерность:** `LOT`
- **Профиль:** Basket Risk contract
- **Scope:** post-execution; Symbol+Magic+CycleID+role

#### Сторона B
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «V2.4.10 Volume Reconciliation»
- **Подраздел:** «actual position volume»
- **Точный маркер:** `normal Small Reverse flow must populate context from actual MT5 position volume`
- **Конкретное утверждение:** Manual назначает actual MT5 position volume authoritative для context/reconciliation.
- **Конкретное значение или формула:** `actual position volume`
- **Размерность:** `LOT`
- **Профиль:** manual/runtime
- **Scope:** executed position; post-close

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: requested/executed volume
- **Проверка одной стадии:** PASS: post-execution
- **Проверка размерностей:** PASS: LOT/LOT
- **Проверка scope:** PASS: actual scope follows request scope
- **Прямое отрицание:** NO
- **Доказанный результат:** Обе стороны запрещают приравнивать request к execution и требуют reconciliation.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** не требуется
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-028 — FLOOR CEILING NEAREST

- **Категория:** `ROUNDING`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Legacy lot geometry»
- **Подраздел:** «Big/Small rounding»
- **Точный маркер:** `BigLot = NormalizeLotNearest(...); SmallLot = NormalizeLotNearest(...)`
- **Конкретное утверждение:** Legacy monolithic Big/Small используют NEAREST.
- **Конкретное значение или формула:** `NEAREST`
- **Размерность:** `LOT`
- **Профиль:** legacy/manual geometry
- **Scope:** legacy BigLot/SmallLot

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_FORMULA_REFERENCE.md`
- **Раздел:** «Margin and terminal rule»
- **Подраздел:** «Oracle rounding profile»
- **Точный маркер:** `BigCore DOWN, BigTrend DOWN, SmallBase UP and NewFar DOWN`
- **Конкретное утверждение:** Hybrid split roles используют role-specific DOWN/UP.
- **Конкретное значение или формула:** `DOWN/UP`
- **Размерность:** `LOT`
- **Профиль:** Hybrid EA_CURRENT
- **Scope:** Hybrid BigCore/BigTrend/SmallBase/NewFar

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: lot rounding
- **Проверка одной стадии:** PASS: architecture role identified
- **Проверка размерностей:** PASS: LOT/LOT; money/price rounding excluded
- **Проверка scope:** PASS: scopes are different named architectures
- **Прямое отрицание:** NO
- **Доказанный результат:** Monolithic BigLot и Hybrid BigCore не являются одной сущностью; прямой formula conflict не доказан. Нужен future mode routing, не выбор rounding здесь.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** 3.1.3/3.1.8
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-029 — Python PASS versus MT5 NOT_RUN

- **Категория:** `TEST_EVIDENCE`
- **Основная классификация:** `EVIDENCE_GAP`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/STAGE_1_2_4_1_EVIDENCE_RU.md`
- **Раздел:** «PRIMARY_IMPLEMENTATION_RUN»
- **Подраздел:** «dimension tests»
- **Точный маркер:** `dimension-contract tests=17 passed`
- **Конкретное утверждение:** Python/static dimension tests passed.
- **Конкретное значение или формула:** `17 passed`
- **Размерность:** `EVIDENCE`
- **Профиль:** container test
- **Scope:** Python/static

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_METAEDITOR_COMPILE.md`
- **Раздел:** «MetaEditor compile record»
- **Подраздел:** «build status»
- **Точный маркер:** `MetaTrader build | NOT_RUN_IN_CONTAINER`
- **Конкретное утверждение:** MetaEditor/MT5 build was not run.
- **Конкретное значение или формула:** `NOT_RUN`
- **Размерность:** `EVIDENCE`
- **Профиль:** MT5 compile
- **Scope:** external terminal

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: evidence level
- **Проверка одной стадии:** PASS: independent validation levels
- **Проверка размерностей:** PASS: EVIDENCE/EVIDENCE
- **Проверка scope:** PASS: different sequential evidence levels
- **Прямое отрицание:** NO
- **Доказанный результат:** Python PASS does not replace MT5; no business conflict.
- **Обоснование классификации:** `EVIDENCE_GAP` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL evidence gap.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** future MetaEditor/MT5
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-030 — Production readiness versus broker evidence

- **Категория:** `READINESS`
- **Основная классификация:** `EVIDENCE_GAP`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/BIG_SMALL_PRODUCTION_READINESS_REPORT_RU.md`
- **Раздел:** «Результат»
- **Подраздел:** «readiness»
- **Точный маркер:** `REAL_TRADING_ALLOWED=NO`
- **Конкретное утверждение:** Real trading is not allowed.
- **Конкретное значение или формула:** `NO`
- **Размерность:** `EVIDENCE`
- **Профиль:** readiness report
- **Scope:** production admission

#### Сторона B
- **Документ:** `Docs/FULL_AUDIT_REPORT.md`
- **Раздел:** «V2.4.20 Position Resolution + Small Scenario Promote Fix»
- **Подраздел:** «validation limitation»
- **Точный маркер:** `MetaEditor compilation and Strategy Tester validation still require MT5 and broker history outside this Linux container.`
- **Конкретное утверждение:** Audit explicitly leaves MT5/broker validation outstanding.
- **Конкретное значение или формула:** `required/not run`
- **Размерность:** `EVIDENCE`
- **Профиль:** source audit
- **Scope:** MT5/broker evidence

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: production evidence
- **Проверка одной стадии:** PASS
- **Проверка размерностей:** PASS: EVIDENCE/EVIDENCE
- **Проверка scope:** PASS
- **Прямое отрицание:** NO
- **Доказанный результат:** Both indicate missing broker/runtime evidence.
- **Обоснование классификации:** `EVIDENCE_GAP` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL evidence gap.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** future MT5/broker
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-031 — Legacy Split Hybrid terminology

- **Категория:** `LEGACY_MIXING`
- **Основная классификация:** `MISSING_DEFINITION`
- **Критичность:** `HIGH`
- **RequiresUserDecision:** `YES`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Legacy and Split sections»
- **Подраздел:** «architecture labels»
- **Точный маркер:** `GEOMETRY_MANUAL is the legacy/manual geometry mode`
- **Конкретное утверждение:** Manual names a legacy mode and separately documents Split geometry.
- **Конкретное значение или формула:** `mode labels`
- **Размерность:** `SCOPE`
- **Профиль:** manual multi-generation
- **Scope:** legacy/split

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_COMPLETE_MANUAL_RU.md`
- **Раздел:** «Область и назначение»
- **Подраздел:** «Hybrid roles»
- **Точный маркер:** `BigCore and BigTrend opposite Far; SmallBase with Far`
- **Конкретное утверждение:** Hybrid manual defines split roles but not a repository-wide mode discriminator.
- **Конкретное значение или формула:** `Hybrid role set`
- **Размерность:** `SCOPE`
- **Профиль:** Hybrid
- **Scope:** Hybrid

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: architecture naming
- **Проверка одной стадии:** PASS
- **Проверка размерностей:** PASS: SCOPE/SCOPE
- **Проверка scope:** MISSING: no single cross-document generation/mode precedence table
- **Прямое отрицание:** NO direct negation
- **Доказанный результат:** Термины описывают разные generations; отсутствует обязательный discriminator, поэтому это missing definition, не authority conflict.
- **Обоснование классификации:** `MISSING_DEFINITION` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** HIGH: смешение mode может выбрать неверные roles.
- **Необходимость решения пользователя:** `YES`; нужен выбор business/profile policy.
- **Этап разрешения:** 3.1.3/3.1.8
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-032 — Split test plan duplicate

- **Категория:** `DUPLICATION`
- **Основная классификация:** `DUPLICATION_WITH_DIFFERENCES`
- **Критичность:** `LOW`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/SPLIT_GEOMETRY_TEST_PLAN.md`
- **Раздел:** «Covered checks»
- **Подраздел:** «local pytest plan»
- **Точный маркер:** `BigCore → SmallBase → BigTrend open sequence; BigCore → BigTrend → SmallBase close sequence`
- **Конкретное утверждение:** Первый plan перечисляет static checks и required MT5 statuses.
- **Конкретное значение или формула:** `ordered checks`
- **Размерность:** `EVIDENCE`
- **Профиль:** Split implementation test plan
- **Scope:** local pytest + MT5 not run

#### Сторона B
- **Документ:** `Docs/TEST_PLAN_SPLIT_GEOMETRY.md`
- **Раздел:** «MT5 scenarios for later stages»
- **Подраздел:** «scenario B»
- **Точный маркер:** `One Small reverse ... expected NewFar ≈ 0.96 OldFar`
- **Конкретное утверждение:** Второй plan перечисляет конкретные MT5 scenario vectors и expected geometry.
- **Конкретное значение или формула:** `scenario expectation`
- **Размерность:** `EVIDENCE`
- **Профиль:** Split scenario test plan
- **Scope:** future MT5

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: Split test requirements
- **Проверка одной стадии:** PASS: overlapping test-plan purpose
- **Проверка размерностей:** PASS: EVIDENCE/EVIDENCE
- **Проверка scope:** PASS: same Split validation scope with differing content
- **Прямое отрицание:** NO direct negation; documented differences
- **Доказанный результат:** Документы дублируют title/scope, но один задаёт static coverage, другой MT5 vectors; consolidation needed.
- **Обоснование классификации:** `DUPLICATION_WITH_DIFFERENCES` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** LOW: duplication can confuse coverage reporting but does not change runtime.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** 3.1.8
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-033 — Reserve persistence

- **Категория:** `PERSISTENCE`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`
- **Раздел:** «HybridCatchUpState»
- **Подраздел:** «state fields»
- **Точный маркер:** `double finalReserveReal; double carryAvailable;`
- **Конкретное утверждение:** Temporal model requires Reserve/Carry in state.
- **Конкретное значение или формула:** `state fields`
- **Размерность:** `MONEY`
- **Профиль:** Hybrid temporal
- **Scope:** persisted/projected state

#### Сторона B
- **Документ:** `Docs/SPLIT_BIG_EXACT_PERSISTENCE_REPORT_RU.md`
- **Раздел:** «Reserve Ledger»
- **Подраздел:** «persisted fields»
- **Точный маркер:** `EventId, MagicNumber, CycleId ... EventKeyHash, SymbolHash`
- **Конкретное утверждение:** Persistence report preserves ledger identity and event context exactly.
- **Конкретное значение или формула:** `ledger identity fields`
- **Размерность:** `SCOPE`
- **Профиль:** Split persistence report
- **Scope:** restart persistence

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: Reserve persistence
- **Проверка одной стадии:** PASS: state and serialization stages
- **Проверка размерностей:** PASS: MONEY state/SCOPE identity linked by persistence
- **Проверка scope:** PASS: model→serialization
- **Прямое отрицание:** NO
- **Доказанный результат:** State requirements and persistence evidence are complementary.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** не требуется
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-034 — Exactly-once Reserve credit

- **Категория:** `RESERVE`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_MONEY_FLOW.md`
- **Раздел:** «Sequential Harvest refinement»
- **Подраздел:** «credit uniqueness»
- **Точный маркер:** `Each Harvest credit arises from a new non-overlapping close set`
- **Конкретное утверждение:** Money flow requires disjoint confirmed sources.
- **Конкретное значение или формула:** `non-overlap`
- **Размерность:** `ORDERING`
- **Профиль:** Hybrid money flow
- **Scope:** confirmed deals

#### Сторона B
- **Документ:** `Docs/BASKET_RISK_CONTRACT_RU.md`
- **Раздел:** «Exactly-once contract»
- **Подраздел:** «ledger outcome»
- **Точный маркер:** `each HarvestNet ... has exactly one terminal commit outcome`
- **Конкретное утверждение:** Basket contract requires one terminal commit per event.
- **Конкретное значение или формула:** `exactly once`
- **Размерность:** `ORDERING`
- **Профиль:** Basket contract
- **Scope:** confirmed ledger/restart

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: Reserve credit uniqueness
- **Проверка одной стадии:** PASS
- **Проверка размерностей:** PASS: ORDERING/ORDERING
- **Проверка scope:** PASS
- **Прямое отрицание:** NO
- **Доказанный результат:** Non-overlap and one commit are compatible protections.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** не требуется
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-035 — Partial fill

- **Категория:** `EXECUTION`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`
- **Раздел:** «Identity and logic»
- **Подраздел:** «LOGIC-06»
- **Точный маркер:** `Any partial fill/reject requires reconciliation before next open`
- **Конкретное утверждение:** Partial fill blocks new open.
- **Конкретное значение или формула:** `reconciliation required`
- **Размерность:** `STATE`
- **Профиль:** Hybrid invariant
- **Scope:** post-execution

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_TEST_VECTORS.md`
- **Раздел:** «Test vectors»
- **Подраздел:** «TV-13»
- **Точный маркер:** `requested .70, filled .35; ERROR_PARTIAL_EXECUTION`
- **Конкретное утверждение:** Vector expects partial execution error.
- **Конкретное значение или формула:** `0.70/0.35`
- **Размерность:** `LOT`
- **Профиль:** negative test
- **Scope:** partial fill

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS
- **Проверка одной стадии:** PASS
- **Проверка размерностей:** PASS: STATE rule and LOT observation linked by execution
- **Проверка scope:** PASS
- **Прямое отрицание:** NO
- **Доказанный результат:** Requirements agree.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** runtime validation
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-036 — Retry idempotency

- **Категория:** `EXECUTION`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/BASKET_RISK_CONTRACT_RU.md`
- **Раздел:** «Partial execution и reconciliation»
- **Подраздел:** «retry rule»
- **Точный маркер:** `Risk-reducing retry ... actual ticket/volume and duplicate guard; no new open`
- **Конкретное утверждение:** Retry requires actual identity and duplicate guard.
- **Конкретное значение или формула:** `duplicate guard`
- **Размерность:** `STATE`
- **Профиль:** Basket contract
- **Scope:** post-reconciliation close retry

#### Сторона B
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Pending retry states»
- **Подраздел:** «retry context»
- **Точный маркер:** `retryTicket, retryLot, retryAttempts ... manual intervention after limit`
- **Конкретное утверждение:** Manual persists retry identity/attempts and does not discard context.
- **Конкретное значение или формула:** `retry context`
- **Размерность:** `STATE`
- **Профиль:** manual/runtime
- **Scope:** pending close retry

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS
- **Проверка одной стадии:** PASS
- **Проверка размерностей:** PASS: STATE/STATE
- **Проверка scope:** PASS: contract and runtime detail compatible
- **Прямое отрицание:** NO
- **Доказанный результат:** No source authorizes duplicate retry.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** runtime evidence
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-037 — Restart reconciliation

- **Категория:** `RECONCILIATION`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_STATE_TRANSITION_TABLE.md`
- **Раздел:** «State transition truth table»
- **Подраздел:** «ANY_ACTIVE restart»
- **Точный маркер:** `full identity/ledger reconciliation → previous safe state`
- **Конкретное утверждение:** Restart requires full reconciliation.
- **Конкретное значение или формула:** `state transition`
- **Размерность:** `STATE`
- **Профиль:** Hybrid state model
- **Scope:** restart

#### Сторона B
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Restart recovery reconciliation»
- **Подраздел:** «RecoverState»
- **Точный маркер:** `reconciles ... Symbol, MagicNumber, Ticket, Position identifier, Comment, Direction, Lot and OpenPrice`
- **Конкретное утверждение:** Manual supplies concrete recovery fields.
- **Конкретное значение или формула:** `identity reconciliation`
- **Размерность:** `STATE`
- **Профиль:** manual/runtime
- **Scope:** restart

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS
- **Проверка одной стадии:** PASS
- **Проверка размерностей:** PASS: STATE/STATE
- **Проверка scope:** PASS
- **Прямое отрицание:** NO
- **Доказанный результат:** Manual refines truth-table requirement.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** не требуется
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-038 — Final Close partial execution

- **Категория:** `FINAL_CLOSE`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/BASKET_RISK_CONTRACT_RU.md`
- **Раздел:** «Partial execution и reconciliation»
- **Подраздел:** «FINAL_CLOSE_PARTIAL»
- **Точный маркер:** `Far remains after final-close attempt; reconciliation required`
- **Конкретное утверждение:** Contract treats residual Far as partial execution.
- **Конкретное значение или формула:** `residual position`
- **Размерность:** `STATE`
- **Профиль:** Basket contract
- **Scope:** post-final-close attempt

#### Сторона B
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Full close verification»
- **Подраздел:** «VerifyFullClose»
- **Точный маркер:** `returns success only when position is truly absent within volume tolerance`
- **Конкретное утверждение:** Manual verifies zero actual position before clearing context.
- **Конкретное значение или формула:** `zero remaining volume`
- **Размерность:** `LOT`
- **Профиль:** manual/runtime
- **Scope:** post-close

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS
- **Проверка одной стадии:** PASS
- **Проверка размерностей:** PASS: STATE/LOT linked by actual position
- **Проверка scope:** PASS
- **Прямое отрицание:** NO
- **Доказанный результат:** Both reject false success after partial final close.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** не требуется
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-039 — MaxHarvestLevels behavior

- **Категория:** `STATE_MACHINE`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «V2.4.6 MaxHarvestLevels Final Decision»
- **Подраздел:** «max-level route»
- **Точный маркер:** `must not open another Big/Small; routes to STATE_MAX_LEVELS_DECISION`
- **Конкретное утверждение:** Manual defines terminal decision at max level.
- **Конкретное значение или формула:** `state route`
- **Размерность:** `STATE`
- **Профиль:** manual/runtime
- **Scope:** max level

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`
- **Раздел:** «Recovery and safety»
- **Подраздел:** «SAFE-02»
- **Точный маркер:** `Terminal state forbids opens, NewFar promotion and Reserve transfer`
- **Конкретное утверждение:** Invariant forbids opens in terminal path.
- **Конкретное значение или формула:** `terminal restriction`
- **Размерность:** `STATE`
- **Профиль:** Hybrid invariant
- **Scope:** terminal state

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS
- **Проверка одной стадии:** PASS
- **Проверка размерностей:** PASS: STATE/STATE
- **Проверка scope:** PASS: max-level route is a terminal/safe specialization
- **Прямое отрицание:** NO
- **Доказанный результат:** No opposite max-level behavior found.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** не требуется
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-040 — Reverse limit behavior

- **Категория:** `STATE_MACHINE`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Risk Compression Reverse»
- **Подраздел:** «reverse limit»
- **Точный маркер:** `if reverseCycleCount > MaxReverseCycles ... STATE_REVERSE_LIMIT and no new Big/Small`
- **Конкретное утверждение:** Limit blocks new opens.
- **Конкретное значение или формула:** `state route`
- **Размерность:** `STATE`
- **Профиль:** manual/runtime
- **Scope:** reverse limit

#### Сторона B
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Reverse limit close»
- **Подраздел:** «StopOnReverseLimit»
- **Точный маркер:** `success → STATE_REVERSE_LIMIT_CLOSED; failure → STATE_REVERSE_LIMIT_CLOSE_PENDING`
- **Конкретное утверждение:** Manual defines close outcomes after same limit.
- **Конкретное значение или формула:** `state outcomes`
- **Размерность:** `STATE`
- **Профиль:** manual/runtime
- **Scope:** post-limit close

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS
- **Проверка одной стадии:** PASS
- **Проверка размерностей:** PASS: STATE/STATE
- **Проверка scope:** PASS: sequential stages
- **Прямое отрицание:** NO
- **Доказанный результат:** Rules form one sequence, not conflict.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** не требуется
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-041 — Invalid geometry behavior

- **Категория:** `STATE_MACHINE`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/MANUAL.md`
- **Раздел:** «Geometry Validator»
- **Подраздел:** «invalid compression»
- **Точный маркер:** `NewFarLot >= OldFarLot ... forbidden geometry`
- **Конкретное утверждение:** Manual rejects non-compression.
- **Конкретное значение или формула:** `invalid predicate`
- **Размерность:** `BOOLEAN`
- **Профиль:** manual/runtime
- **Scope:** pre-open geometry

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`
- **Раздел:** «Geometry»
- **Подраздел:** «GEO-01/GEO-04»
- **Точный маркер:** `0 < NewFar < OldFar; after rounding all gates rerun`
- **Конкретное утверждение:** Invariant requires strict compression after rounding.
- **Конкретное значение или формула:** `valid predicate`
- **Размерность:** `BOOLEAN`
- **Профиль:** Hybrid invariant
- **Scope:** normalized geometry

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS
- **Проверка одной стадии:** PASS
- **Проверка размерностей:** PASS: BOOLEAN/BOOLEAN
- **Проверка scope:** PASS
- **Прямое отрицание:** YES logical complement but same policy
- **Доказанный результат:** Both reject invalid geometry.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** не требуется
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-042 — Basket Risk preview versus execution

- **Категория:** `RISK`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/BASKET_RISK_CONTRACT_RU.md`
- **Раздел:** «Read-only boundary and snapshot»
- **Подраздел:** «preview gate»
- **Точный маркер:** `Basket Risk consumes immutable Base/Worst snapshot and returns typed gate outcome; it does not execute orders`
- **Конкретное утверждение:** Preview is read-only and fingerprinted.
- **Конкретное значение или формула:** `preview outcome`
- **Размерность:** `STATE`
- **Профиль:** Basket Risk Stage 2.0
- **Scope:** pre-open projected snapshot

#### Сторона B
- **Документ:** `Docs/BASKET_RISK_CONTRACT_RU.md`
- **Раздел:** «Partial execution и reconciliation»
- **Подраздел:** «post-execution»
- **Точный маркер:** `actual positions/deals are reacquired; revision, fingerprints and snapshot are rebuilt before next open`
- **Конкретное утверждение:** After execution a new actual snapshot is required.
- **Конкретное значение или формула:** `actual reconciliation`
- **Размерность:** `STATE`
- **Профиль:** Basket Risk contract
- **Scope:** post-execution

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: preview/actual lifecycle
- **Проверка одной стадии:** PASS
- **Проверка размерностей:** PASS: STATE/STATE
- **Проверка scope:** PASS: sequential pre/post execution scopes
- **Прямое отрицание:** NO
- **Доказанный результат:** Contract never treats preview as execution success.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** не требуется
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-043 — Cycle versus account risk

- **Категория:** `RISK`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/BASKET_RISK_CONTRACT_RU.md`
- **Раздел:** «Cycle Basket Risk»
- **Подраздел:** «cycle namespace»
- **Точный маркер:** `exact Symbol+Magic+CycleID+role identifier; foreign cycles excluded`
- **Конкретное утверждение:** Cycle risk aggregates one managed cycle.
- **Конкретное значение или формула:** `cycle aggregate`
- **Размерность:** `MONEY`
- **Профиль:** Basket Risk contract
- **Scope:** one Symbol+Magic+CycleID

#### Сторона B
- **Документ:** `Docs/BASKET_RISK_CONTRACT_RU.md`
- **Раздел:** «Account Basket Risk»
- **Подраздел:** «account inputs»
- **Точный маркер:** `includes all managed cycles plus account balance/equity/margin/drawdown; unmanaged exposure cannot be silently ignored`
- **Конкретное утверждение:** Account risk aggregates account-wide state after cycle PASS.
- **Конкретное значение или формула:** `account aggregate`
- **Размерность:** `MONEY`
- **Профиль:** Basket Risk contract
- **Scope:** all managed cycles/account

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: risk aggregation layer
- **Проверка одной стадии:** PASS: sequential layers
- **Проверка размерностей:** PASS: MONEY/MONEY
- **Проверка scope:** PASS: nested cycle→account scopes explicitly distinct
- **Прямое отрицание:** NO
- **Доказанный результат:** Cycle and Account Risk are conjunctive layers, not substitutes.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** не требуется
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-044 — Terminal-safe versus mathematically-safe

- **Категория:** `RISK`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`
- **Раздел:** «Recovery and safety»
- **Подраздел:** «SAFE-01/SAFE-02»
- **Точный маркер:** `Base PASS without Worst PASS does not allow action; terminal state forbids opens`
- **Конкретное утверждение:** Mathematical gates are necessary but terminal restrictions remain.
- **Конкретное значение или формула:** `gate/state`
- **Размерность:** `STATE`
- **Профиль:** Hybrid invariant
- **Scope:** pre-open/terminal

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_THREE_LAWS_MATH_MANUAL_RU.md`
- **Раздел:** «Terminal-safe state»
- **Подраздел:** «permitted actions»
- **Точный маркер:** `TERMINAL_SAFE_STATE forbids new Big/Small and permits only bounded close/admin routes`
- **Конкретное утверждение:** Terminal-safe is an execution state, not analytic PASS.
- **Конкретное значение или формула:** `terminal policy`
- **Размерность:** `STATE`
- **Профиль:** math manual
- **Scope:** terminal runtime policy

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS
- **Проверка одной стадии:** PASS
- **Проверка размерностей:** PASS: STATE/STATE
- **Проверка scope:** PASS
- **Прямое отрицание:** NO
- **Доказанный результат:** Analytic safety and terminal-safe state are complementary.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** не требуется
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

### HSB-DOC-CONFLICT-045 — Source-of-truth competition

- **Категория:** `AUTHORITY`
- **Основная классификация:** `NO_DIRECT_CONFLICT_FOUND`
- **Критичность:** `INFORMATIONAL`
- **RequiresUserDecision:** `NO`

#### Сторона A
- **Документ:** `Docs/HYBRID_SPLIT_BIG_SYSTEM_INVARIANTS.md`
- **Раздел:** «Temporal and Far invariants»
- **Подраздел:** «authority pointer»
- **Точный маркер:** `Temporal authority: HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`
- **Конкретное утверждение:** Invariants explicitly delegate temporal authority.
- **Конкретное значение или формула:** `authority reference`
- **Размерность:** `AUTHORITY`
- **Профиль:** Hybrid invariants
- **Scope:** temporal semantics

#### Сторона B
- **Документ:** `Docs/HYBRID_SPLIT_BIG_CATCHUP_TEMPORAL_MODEL_RU.md`
- **Раздел:** «Document status»
- **Подраздел:** «normative authority»
- **Точный маркер:** `NORMATIVE. Единственный нормативный источник временной семантики Big Harvest`
- **Конкретное утверждение:** Temporal model accepts that delegated temporal scope.
- **Конкретное значение или формула:** `authority claim`
- **Размерность:** `AUTHORITY`
- **Профиль:** Hybrid temporal model
- **Scope:** Big Harvest temporal semantics

#### Проверка сопоставимости
- **Проверка одной сущности:** PASS: temporal authority
- **Проверка одной стадии:** PASS
- **Проверка размерностей:** PASS: AUTHORITY/AUTHORITY
- **Проверка scope:** PASS: exact same delegated scope
- **Прямое отрицание:** NO
- **Доказанный результат:** Delegation and acceptance agree; no competing authority shown by these sides.
- **Обоснование классификации:** `NO_DIRECT_CONFLICT_FOUND` следует из приведённых сторон; отсутствие текста не трактуется как противоположное правило.
- **Обоснование критичности:** INFORMATIONAL.
- **Необходимость решения пользователя:** `NO`; достаточно документационной консолидации или последующей проверки.
- **Этап разрешения:** не требуется
- **Временное правило:** `USE_ONLY_AS_EVIDENCE`

## Матрица доказательной верификации 45 записей

| ID | A topic match | B topic match | Same entity | Comparable dimensions | Comparable scope | Heading-only | Result supported |
|---|---|---|---|---|---|---|---|
| HSB-DOC-CONFLICT-001 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-002 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-003 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-004 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-005 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-006 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-007 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-008 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-009 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-010 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-011 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-012 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-013 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-014 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-015 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-016 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-017 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-018 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-019 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-020 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-021 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-022 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-023 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-024 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-025 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-026 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-027 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-028 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-029 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-030 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-031 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-032 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-033 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-034 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-035 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-036 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-037 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-038 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-039 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-040 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-041 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-042 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-043 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-044 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HSB-DOC-CONFLICT-045 | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

## Статистика и методология

Каждая запись учитывается ровно в одной основной классификации. `CONFIRMED_CONFLICTS` включает только DIRECT, PARAMETER_PROFILE, FORMULA, ORDERING, SCOPE, AUTHORITY и DUPLICATION_WITH_DIFFERENCES; MISSING_DEFINITION, AMBIGUITY, EVIDENCE_GAP и NO_DIRECT_CONFLICT_FOUND туда не входят.

```text
MANDATORY_TOPICS_REVIEWED=45
DIRECT_CONFLICTS=0
PARAMETER_PROFILE_CONFLICTS=6
FORMULA_CONFLICTS=0
ORDERING_CONFLICTS=0
SCOPE_CONFLICTS=1
AUTHORITY_CONFLICTS=0
DUPLICATION_WITH_DIFFERENCES=1
MISSING_DEFINITION=4
AMBIGUITY=0
EVIDENCE_GAP=2
NO_DIRECT_CONFLICT_FOUND=31
CONFIRMED_CONFLICTS=8
NEEDS_USER_DECISION=10
CLASSIFICATION_TOTAL=45
BUSINESS_CONFLICTS_AUTO_RESOLVED=0
SOURCE_OF_TRUTH_ASSIGNED=NO
STAGE_3_1_3_STARTED=NO
STAGE_3_1_2_THIRD_CORRECTION_STATUS=PASS
```

Арифметика классификаций: `0 + 6 + 0 + 0 + 1 + 0 + 1 + 4 + 0 + 2 + 31 = 45`.

## Итоговые проверки

```text
MANDATORY_RECORDS=45
SEQUENTIAL_IDS=PASS
SUMMARY_DETAIL_CLASSIFICATION_MATCH=PASS
SUMMARY_DETAIL_SEVERITY_MATCH=PASS
SUMMARY_DETAIL_USER_DECISION_MATCH=PASS
SIDE_A_TOPIC_MATCH=PASS
SIDE_B_TOPIC_MATCH=PASS
A_AND_B_LOGICALLY_COMPARABLE=PASS
DIMENSIONS_COMPARABLE=PASS
SCOPES_EXPLICIT=PASS
RESULT_SUPPORTED_BY_SIDES=PASS
HEADING_ONLY_CONCRETE_CLAIMS=0
UNRELATED_SIDE_COMPARISONS=0
SAME_VALUES_MARKED_AS_CONFLICT=0
MISSING_TEXT_INTERPRETED_AS_OPPOSITE_RULE=0
DIFFERENT_DIMENSIONS_MARKED_AS_FORMULA_CONFLICT=0
AUDIT_DATE_USED_AS_NORMATIVE_CLAIM=0
EVIDENCE_GAPS_COUNTED_AS_BUSINESS_CONFLICT=0
GENERIC_TWO_RULES_TEXT_IN_EVIDENCE_RECORDS=0
CONFLICT_009_TOPIC_PROOF=PASS
CONFLICT_010_TOPIC_PROOF=PASS
CONFLICT_027_VOLUME_PROOF=PASS
CONFLICT_028_ROUNDING_DIMENSION_PROOF=PASS
CONFLICT_042_PREVIEW_EXECUTION_PROOF=PASS
CONFLICT_043_CYCLE_ACCOUNT_RISK_PROOF=PASS
CLASSIFICATION_TOTAL=45
STATISTICS_ARITHMETIC=PASS
BUSINESS_CONFLICTS_AUTO_RESOLVED=0
SOURCE_OF_TRUTH_ASSIGNED=NO
STAGE_3_1_3_STARTED=NO
```

Код, параметры, другие Docs, MQL5, Python, Tests, Tools, Sets, workflows и runtime не менялись.

Ожидается повторная проверка пользователя. Этап 3.1.3 не выполнялся.
# Денежная нормативная граница Этапа 3.1.5

Денежные определения `STAGE_3_1_5_NORMATIVE_MONEY_MODEL_RU.md` имеют приоритет только для
projected/actual money, RecoveryPLCloseNow, allocation и exactly-once. Геометрические ratios,
NewFar и profiles не разрешены этим этапом: `STATUS=BLOCKED_BY_USER_DECISION`.
