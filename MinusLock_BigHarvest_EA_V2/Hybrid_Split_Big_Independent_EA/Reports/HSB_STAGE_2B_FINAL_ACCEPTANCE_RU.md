# HSB.2B — финальная статическая приёмка

Дата: 2026-08-11 UTC.

```text
BASELINE_SHA=0614d065db81e9fd2a0c977e92f9a485e4e64bd1
FINAL_LOCAL_SHA=b2ba00f6585419d44427ea0720146c35faf36678
FINAL_REMOTE_SHA=976aa9b089b610ef738cc89c411febbd8322fdd6
BRANCH=work
WORKTREE_STATUS=clean_before_final_report
HEAD_EQUALS_ORIGIN_WORK=YES_AT_VERIFIED_PUBLICATION
CHANGED_FILES=13
CHANGED_FILES_OUTSIDE_SCOPE=0
```

Remote SHA отражает состояние до итогового push; публикационное доказательство добавляется append-only commit без переписывания истории.

## Реализованность

```text
FUTURE_SMALL_SOLVER=STATIC_IMPLEMENTED
EXACT_RECURSION=STATIC_IMPLEMENTED
CONSERVATIVE_BOUND=STATIC_IMPLEMENTED
FINITE_SEQUENCE_PROOF=STATIC_IMPLEMENTED
NEW_FAR_SOLVER=STATIC_IMPLEMENTED
CANDIDATE_ENUMERATION=STATIC_IMPLEMENTED
DETERMINISTIC_OBJECTIVE=STATIC_IMPLEMENTED
ACTUAL_RESIDUAL_VALIDATION=STATIC_IMPLEMENTED
RISK_GATE=STATIC_IMPLEMENTED
MARGIN_GATE=STATIC_IMPLEMENTED
TRANSITION_LOSS_GATE=STATIC_IMPLEMENTED
PLAN_IMMUTABILITY=STATIC_IMPLEMENTED
TRADE_EXECUTION=NO
REAL_TRADING_ALLOWED=NO
```

Future Small сохраняет per-level proof, учитывает broker rounding, geometry/slope, money, reserve, Big gross/exposure compression, risk, margin и transition loss. Bound требует минимум двух exact уровней и не заменяет ближайшую recursion. Plateau/invalid q/no terminal route fail-closed.

NewFar принимает только confirmed actual BigCore residual одного identity scope, перечисляет полный допустимый broker grid, применяет Future Small/money/risk/margin/exposure/loss gates и выбирает детерминированный optimum. Projected/actual DTO разделены; second Far и digest/plan/revision mismatch ведут к rejection/reconciliation contract.

## Unit-test harness

```text
DECLARED_TEST_IDS=120
UNIQUE_TEST_IDS=120
T01_TO_T120_COMPLETE=YES
NO_DUPLICATES=YES
NO_GAPS=YES
```

T71–T91 покрывают recursion/q/bound/finite route/plateau/compression/risk/margin/loss. T92–T120 покрывают actual source identity/grid, enumeration, objective, deterministic digest, snapshots, plan/revision, availability, caps и second-Far rejection.

## Ограничения доказательств

```text
METAEDITOR_COMPILE=USER_VERIFICATION_REQUIRED
MQL5_RUNTIME_TESTS=USER_VERIFICATION_REQUIRED
BROKER_MONEY_RUNTIME_PROOF=USER_VERIFICATION_REQUIRED
STATIC_NO_TRADE_AUDIT=PASS
SCOPE_AUDIT=PASS
```

MetaEditor/MT5 не запускались; compile/runtime PASS не объявляется. Python/ручной review не являются runtime evidence.

## Verdict до публикации

```text
HSB.2B=STATIC_IMPLEMENTED
HSB.2B_PUBLISHED=PASS
FUTURE_SMALL=STATIC_IMPLEMENTED
NEW_FAR_SOLVER=STATIC_IMPLEMENTED
BROKER_MONEY_RUNTIME=USER_VERIFICATION_REQUIRED
METAEDITOR_COMPILE=USER_VERIFICATION_REQUIRED
MQL5_RUNTIME_TESTS=USER_VERIFICATION_REQUIRED
TRADING_IMPLEMENTED=NO
REAL_TRADING_ALLOWED=NO
HSB.2C=NOT_STARTED
```

## Публикация

```text
PUSH_MODE=NORMAL
FORCE_PUSH=NO
PUBLISHED_VERIFIED_SHA=976aa9b089b610ef738cc89c411febbd8322fdd6
HEAD=976aa9b089b610ef738cc89c411febbd8322fdd6
ORIGIN_WORK=976aa9b089b610ef738cc89c411febbd8322fdd6
GITHUB_API_SHA=976aa9b089b610ef738cc89c411febbd8322fdd6
HEAD_EQUALS_ORIGIN_WORK=YES
WORKTREE_CLEAN=YES
HSB.2B_PUBLISHED=PASS
```

Содержательный commit опубликован обычным push и подтверждён fetch/API. Эта append-only запись публикуется следующим обычным commit; её transport SHA проверяется post-push без самоссылки SHA внутри commit.

## Коррекция HSB.2B-R

Линейные per-level/per-lot коэффициенты не являются broker proof и удалены из production solver path. Каждый exact Future Small level заново строит geometry и четыре независимые legs, проверяет Bid/Ask, signed commission/swap/fee, spread/slippage/safety buffer, вызывает calculation-only money/margin wrappers, затем рассчитывает basket money, margin, exposure, basket-derived risk и transition loss. Любой unavailable leg делает уровень недоказанным.

Каждый NewFar candidate создаёт собственный Future Small input и собственные money/margin/risk/Catch-Up digests. Test-only approximation и injected proof без broker confirmation не могут дать VALID/SELECTED/EXACT_PROOF. Plan digest охватывает identity, grid/tick, Bid/Ask/control snapshot, cost snapshot IDs, money/margin/risk proofs и полный candidate-list digest. Fail-closed оставляет runtime проверку администратору.

```text
HSB.2B=STATIC_CORRECTED_IMPLEMENTATION
HSB.2C=NOT_STARTED
METAEDITOR_COMPILE=USER_VERIFICATION_REQUIRED
MQL5_RUNTIME_TESTS=USER_VERIFICATION_REQUIRED
BROKER_MONEY_RUNTIME_PROOF=USER_VERIFICATION_REQUIRED
TRADING_IMPLEMENTED=NO
REAL_TRADING_ALLOWED=NO
```

> SHA correction HSB.2B-R: конечный опубликованный transport SHA этапа HSB.2B до корректирующего подэтапа — `976aa9b089b610ef738cc89c411febbd8322fdd6`. SHA HSB.2B-R фиксируется только после его push verification.
