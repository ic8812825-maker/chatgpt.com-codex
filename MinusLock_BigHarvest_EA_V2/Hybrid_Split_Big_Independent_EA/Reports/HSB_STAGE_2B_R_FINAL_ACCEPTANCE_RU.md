# HSB.2B-R — финальная статическая приёмка

Дата: 2026-08-11 UTC.

```text
BASELINE_SHA=976aa9b089b610ef738cc89c411febbd8322fdd6
ACTUAL_APPEND_ONLY_BASELINE=cc80ab6967ac0a387487ce51a03ae29f5a5d2cdd
FINAL_LOCAL_SHA=fdfbc94971c9751c2d40f4e438529df0719ca67c
FINAL_REMOTE_SHA=28ab6cd94d7d5b8fd4a2edb0132ae0c9e11619ba
BRANCH=work
WORKTREE_STATUS=clean_before_final_report
HEAD_EQUALS_ORIGIN_WORK=YES_AT_VERIFIED_PUBLICATION
CHANGED_FILES_OUTSIDE_SCOPE=0
```

## Реализовано

```text
LEVEL_SPECIFIC_BROKER_MONEY=STATIC_IMPLEMENTED
LEVEL_SPECIFIC_MARGIN=STATIC_IMPLEMENTED
LEVEL_SPECIFIC_RISK=STATIC_IMPLEMENTED
LEVEL_SPECIFIC_TRANSITION_LOSS=STATIC_IMPLEMENTED
CANDIDATE_SPECIFIC_MONEY=STATIC_IMPLEMENTED
CANDIDATE_SPECIFIC_MARGIN=STATIC_IMPLEMENTED
CANDIDATE_SPECIFIC_FUTURE_SMALL=STATIC_IMPLEMENTED
CANDIDATE_SPECIFIC_CATCH_UP=STATIC_IMPLEMENTED
LINEAR_SHORTCUT_GUARD=PASS_STATIC
PLAN_DIGEST=STATIC_IMPLEMENTED
NO_TRADE_GUARD=PASS
```

Каждый Future Small exact level строит собственную rounded geometry и четыре независимые legs, использует typed leg money/margin и basket evaluators, затем basket-derived risk/exposure/transition-loss gates. Conservative bound требует минимум двух exact уровней и подтверждённых money/margin/risk/loss flags. Terminal route и linear coefficients сами по себе proof не дают.

Каждый NewFar candidate создаёт собственный Future Small input с `useInjectedBrokerProofs=false`, повторно получает broker money/margin/risk/Catch-Up proofs и только затем участвует в objective. При недоступном broker runtime кандидат отклоняется, а не получает искусственный PASS. Projected/Actual residual остаются разделены.

Plan digest включает Account/Symbol/Magic/Cycle/Plan/Revision, OldFar, original identifier/ticket, actual/projected residual, ratios, volume/tick grid, Bid/Ask/control snapshot, cost snapshot IDs, money/margin/risk proof digests и полный candidate-list digest.

## Test harness

```text
DECLARED_TEST_IDS=160
UNIQUE_TEST_IDS=160
T01_TO_T160_COMPLETE=YES
NO_DUPLICATES=YES
NO_GAPS=YES
LINEAR_APPROXIMATION_CANNOT_PRODUCE_VALID_PROOF=TESTED_STATIC_CONTRACT
```

T121–T160 покрывают leg money/margin, Bid/Ask, signed costs, runtime unavailable, level-specific geometry/proofs, bound prerequisites, candidate-specific evaluation, shortcut guards, identity/ticket и digest sensitivity.

## Не подтверждено без администратора

```text
METAEDITOR_COMPILE=USER_VERIFICATION_REQUIRED
MQL5_RUNTIME_TESTS=USER_VERIFICATION_REQUIRED
ORDER_CALC_PROFIT_RUNTIME=USER_VERIFICATION_REQUIRED
ORDER_CALC_MARGIN_RUNTIME=USER_VERIFICATION_REQUIRED
BROKER_MONEY_RUNTIME_PROOF=USER_VERIFICATION_REQUIRED
```

MetaEditor/MT5 Codex не запускал и не имитировал; compile/runtime PASS не заявляется.

## Не реализовано

```text
HSB.2C=NO
TRADE_EXECUTION=NO
INITIAL_LOCK=NO
BIG_HARVEST=NO
PARTIAL_FAR_EXECUTION=NO
FINAL_CLOSE_EXECUTION=NO
SMALL_TRANSITION_EXECUTION=NO
REAL_TRADING=NO
TRADING_IMPLEMENTED=NO
REAL_TRADING_ALLOWED=NO
```

## Verdict до публикации

```text
HSB.2B_R=STATIC_CORRECTED_IMPLEMENTATION
HSB.2B_R_PUBLISHED=PASS
LEVEL_SPECIFIC_MONEY=STATIC_IMPLEMENTED
CANDIDATE_SPECIFIC_MONEY=STATIC_IMPLEMENTED
METAEDITOR_COMPILE=USER_VERIFICATION_REQUIRED
MQL5_RUNTIME_TESTS=USER_VERIFICATION_REQUIRED
BROKER_MONEY_RUNTIME_PROOF=USER_VERIFICATION_REQUIRED
TRADING_IMPLEMENTED=NO
REAL_TRADING_ALLOWED=NO
HSB.2C=NOT_STARTED
```

## Публикация

```text
PUSH_MODE=NORMAL
FORCE_PUSH=NO
PUBLISHED_VERIFIED_SHA=28ab6cd94d7d5b8fd4a2edb0132ae0c9e11619ba
HEAD=28ab6cd94d7d5b8fd4a2edb0132ae0c9e11619ba
ORIGIN_WORK=28ab6cd94d7d5b8fd4a2edb0132ae0c9e11619ba
GITHUB_API_SHA=28ab6cd94d7d5b8fd4a2edb0132ae0c9e11619ba
HEAD_EQUALS_ORIGIN_WORK=YES
WORKTREE_CLEAN=YES
HSB.2B_R_PUBLISHED=PASS
```

Содержательный commit опубликован обычным push и подтверждён fetch/API. Настоящая append-only запись публикуется следующим обычным commit; transport SHA проверяется post-push без самоссылки.


## Последующая корректировка HSB.2B-R2

Исторический опубликованный SHA HSB.2B-R исправлен на фактический tip этапа `28ab6cd94d7d5b8fd4a2edb0132ae0c9e11619ba`. R2 не изменяет исторический verdict compile/runtime: пользовательская проверка по-прежнему обязательна.
