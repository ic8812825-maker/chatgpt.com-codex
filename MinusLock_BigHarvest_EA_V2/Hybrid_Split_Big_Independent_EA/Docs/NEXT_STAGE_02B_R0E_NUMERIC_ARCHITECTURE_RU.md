# 02B-R0E — архитектура точной арифметики применительно к MQL5

BASE_SHA=2d34c3378edc5f2df064282fa067bb4af2a1e3b0

Статус: PROPOSED / AWAITING_ADMIN_APPROVAL. Только audit/test-only; никаких production-изменений и торговли.

## Выбор для рассмотрения

| Вариант | Exactness | OverflowRisk | BrokerCompatibility | Complexity | MigrationRisk | Testability |
|---|---|---|---|---|---|---|
| Integer minor units signed64 | Точно для известной currency/grid | LONG_MIN/MAX; scale и sums проверяются до операции | Нужен provider digits/posted conversion | Низкая/средняя | Старые double требуют сверки, не cast | Literal vectors, checked boundaries |
| Fixed point с отдельным scale | Точно на утверждённой сетке; projected subunit может не войти | Scale alignment/intermediate products | Scale зависит от величины/API | Средняя | Явная version/schema | Integer coefficient oracle |
| Checked rational | Точно при bounded integers и проверенных сокращениях | Numerator/denominator overflow до сокращения | Broker всё равно double/posted boundaries | Высокая | Python Fraction не переносится автоматически | Fraction reference + независимые coefficients |
| Double на разрешённых границах | Нет общего exactness; нужен интервал/ошибка | Overflow, cancellation, subunit loss | Нативный broker API | Низкая на входе, высокая для гарантий | Незаметный drift | Adversarial conversion / broker reconciliation |

Рекомендуется settled money signed64 minor units с checked arithmetic; projected — отдельный фиксированный/рациональный или консервативный interval domain после архитектурного решения MQL-DOMAIN. Double используется только на явно утверждённых broker/API boundaries; перед созданием posted ledger требуется independently reconciled amount/precision. Фиксированный ROUND_HALF_EVEN не объявляется универсальной broker policy.

## Диапазон и prechecks

LONG_MIN=-9223372036854775808, LONG_MAX=9223372036854775807. Max positive Money=LONG_MAX/10^digits: digits0→9223372036854775807; digits2→92233720368547758.07; digits8→92233720368.54775807. Это предел представления, не broker limit. Отрицательный диапазон асимметричен; запрещено abs(LONG_MIN) и -LONG_MIN без проверки. Source дебиты сохраняют знак, положительные grants/consumptions имеют отдельные nonnegative constraints.

Addition: b>0 требует a<=MAX-b; b<0 требует a>=MIN-b. Проверка до a+b, оба operands уже int64. Multiply: ветвление по знакам с truncation toward zero; сравнение с MAX/b или MIN/b до a*b, special LONG_MIN/-1 исключён. Scaling currency uses checked_mul(value,10^digits) после проверки степени и domain; нельзя сначала переполнить double→long/cast. Промежуточное умножение shares/ratio тоже требует собственного checked domain; безопасный final quotient не оправдывает overflowing intermediate.

Reference checked_add/checked_mul — математические Python counterparts prechecks, не скомпилированная реализация MQL5. Tests MQL-add*/MQL-mul*/NUM-domain-unsupported задают literal limits. R0D reference domain abs<10^65 и scale10^-64 шире int64: 1e28 поддерживается oracle и НЕ объявляется поддержанным MQL5 minor units. Вне будущего MQL-domain — UNAVAILABLE/quarantine, без clamp/усечения.

## Сохранённая арифметика R0D

Frozen Tests/Reference/hsbi_02b_r0d_independent_oracle.py предоставляет number/canonical/allocate/worst/sequential/geometry. R0E импортирует этот subject как проверенную арифметическую зависимость, не переписывает её. Expected значения R0E берутся из literals и независимого integer coefficient/scale helper Tests/Static/check_hsbi_02b_r0d_contracts.py:N/view; evaluator не используется как expected. Восемь сохранённых contexts включают разные precision/rounding/flags/traps/Emax/Emin. До/после contexts сравниваются.

Новые registry операции используют Fraction без Decimal arithmetic. Grant cap и операции с неотрицательным ресурсом сохраняют величины <=grant; aggregate reserve checked на выходе, разные currency/digits дают UNAVAILABLE. Partial-fill aggregations требуют checked domain и не доказывают broker batch. Расход должен оставлять G=C+V+F, owner reservations sum=V. Нулевая/отрицательная сумма не списывается. Restored snapshot проверяется независимым journal replay, а не только checksum.

Precision alternatives: A confirmed broker-posted receipt — приоритетный факт; B versioned local policy только после проверки provider и совпадения с receipt; C insufficient precision/source —UNAVAILABLE. Raw компонентные суммы и posted amounts не приравниваются без reconciliation. Example1.2451 directly half-even digits2→1.25, via digits3→1.245 then2→1.24; повторное округление не замена posted факта. Allocate0.01 с двумя shares0.5 даёт0/0 и ResidualHeld0.01, conservation exact.

## Snapshot fixture contract

R0D snapshot_shape: schemaVersion HSBI-SNAPSHOT-FIXTURE-1; id int ulong (bool запрещён); validUntil nonnegative int; clockDomain FIXTURE_MONOTONIC, timeUnit tick; marketFingerprint nonempty opaque str, None значит unknown/UNAVAILABLE, missing malformed. Независимый receipt content digest связывается с independently supplied snapshot; receipt нельзя пересоздавать после отрицательной подмены. Typed canonical codec различает string/Decimal/int/bool, list/tuple; Decimal/Fraction одного значения эквивалентны. Это fixture schema, не universal broker fingerprint, не криптографическое доказательство authority.

R0E registry snapshot имеет другую явно названную HSBI-R0E-SNAPSHOT-1 schema: payload registry и checksum. Он не заменяет market snapshot, а служит in-memory recovery fixtures. verify_identity проверяет независимые context IDs/fresh attestation, а полный market snapshot binding остаётся в frozen R0D authorize/runtime regression; ни одна из этих fixtures не доказывает broker receipt authenticity.
