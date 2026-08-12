# HSB.1V — финальная доказательная приёмка

Дата формирования: 2026-08-11 UTC.

## Baseline

```text
BASELINE_SHA=82664748abff0dec450edc68fb9ceb9c640f98b1
BASELINE_LOCAL_SHA=9928793a19216e5a51c0699afc74ccdff4bbd300
FINAL_LOCAL_SHA=b4ea255688026a2d87cfa2176f42186f72aaa07a
FINAL_REMOTE_SHA=5782d4f66d9b582e84153c1133e824fd7f4b10d9
BRANCH=work
WORKTREE_STATUS=clean_before_final_report
```

`FINAL_LOCAL_SHA` — SHA полностью проверенного набора перед коммитом настоящего отчёта. `FINAL_REMOTE_SHA` выше фиксирует фактическое состояние remote до публикации; результат обычного push и post-push SHA должен быть добавлен отдельной публикационной записью, без переписывания данного commit.

## Git history

Между baseline и проверенным набором создано 12 коммитов:

```text
9928793 HSB.1V: усиление валидаций, lossless-ulong сериализация, тестовый harness и отчёты
85f2aa7 HSB.1V: зафиксирован baseline для публикации этапа
744b37d HSB.1V: исправлена lossless-сериализация ulong идентификаторов
cf69448 HSB.1V: усилена валидация полного RecoveryContext
4e6f17c HSB.1V: реализованы чистые transaction barriers и retry invariants
1a63588 HSB.1V: усилены identity и ownership invariants
dbae2ba HSB.1V: проверены и дополнены 26 MQL5 unit-тестов
7964d31 HSB.1V: подтверждён запрет торгового исполнения
09a95d2 HSB.1V: синхронизированы статусы и нормативная документация
9dc7761 HSB.1V: зафиксирован фактический результат MetaEditor compile
f481717 HSB.1V: зафиксирован фактический результат MQL5 unit-тестов
b4ea255 HSB.1V: подтверждена область изменений независимого проекта
```

```text
HSB_1V_COMMITS_BEFORE_FINAL_REPORT=12
RESET_USED=NO
FORCE_PUSH_USED=NO
COMMITS_DELETED=NO
HISTORY_REWRITTEN=NO
```

## Code verification

```text
ULONG_SERIALIZATION=PASS_STATIC
CONTEXT_VALIDATION=PASS_STATIC
TRANSACTION_BARRIERS=PASS_STATIC
IDENTITY_OWNERSHIP=PASS_STATIC
FSM_BARRIERS=PASS_STATIC
NO_TRADE_GUARD=PASS
```

Все сериализуемые CycleID, PositionIdentifier, Ticket, PlanID, ActionID, EventID, StateRevision, snapshot-related ID и JournalRevision проходят через lossless decimal `ulong` conversion. Context проверяет runtime/FSM/schema/MoneyStateVersion/identity/revision/reconciliation/roles/volumes/Far/pending action/policy. Transaction transition требует completed outcome, совпадающий ActionID, fresh EventID, actual position/deal, полный volume, ownership, StateRevision и отсутствие reconciliation conflict. Retry с новым ActionID или после completed запрещён.

Ownership использует tuple `AccountLogin + Symbol + Magic + CycleID + PositionIdentifier + Role`; ticket дополнительно обязан совпадать с ожидаемым observation, но не заменяет PositionIdentifier. Comment не является входом guard. Foreign identity, stale/reused ticket, changed volume/direction, второй Far и произвольная promotion отклоняются.

## Test verification

```text
DECLARED_TEST_IDS=26
UNIQUE_TEST_IDS=26
T01_TO_T26_COMPLETE=YES
TEST_ID_DUPLICATES=0
TEST_ID_GAPS=0
METAEDITOR_COMPILE=NOT_RUN_ENVIRONMENT_UNAVAILABLE
MQL5_UNIT_TESTS=NOT_RUN_ENVIRONMENT_UNAVAILABLE
```

MetaEditor, Wine, MT5 Terminal и MetaTester фактически искались через `command -v` и `find /opt /usr /workspace -maxdepth 5`; исполняемые файлы отсутствуют. Поэтому compile/test PASS не заявляются, Python и сторонние заменители не применялись.

## Область изменений

```text
CHANGE_SCOPE=MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/
CHANGED_FILES_OUTSIDE_SCOPE=0
OLD_PRODUCTION_EA_CHANGED=NO
SCOPE_AUDIT=PASS
```

## Реализованность

```text
INITIAL_LOCK=NOT_IMPLEMENTED
BIG_HARVEST=NOT_IMPLEMENTED
PARTIAL_FAR=NOT_IMPLEMENTED
FINAL_CLOSE=NOT_IMPLEMENTED
SMALL_TRANSITION=NOT_IMPLEMENTED
NEW_FAR_SOLVER=NOT_IMPLEMENTED
BROKER_MONEY_RUNTIME=NOT_IMPLEMENTED
PRODUCTION_PERSISTENCE=NOT_IMPLEMENTED
PRODUCTION_TRANSACTION_ENGINE=NOT_IMPLEMENTED
TRADING_SCENARIOS_IMPLEMENTED=0
TRADING_IMPLEMENTED=NO
REAL_TRADING_ALLOWED=NO
HSB.2_STARTED=NO
```

## Verdict до публикации

```text
HSB.1V=PARTIAL_ENVIRONMENT_BLOCKED
HSB.1V_PUBLISHED=PASS
METAEDITOR_COMPILE=NOT_RUN_ENVIRONMENT_UNAVAILABLE
MQL5_UNIT_TESTS=NOT_RUN_ENVIRONMENT_UNAVAILABLE
TRADING_IMPLEMENTED=NO
REAL_TRADING_ALLOWED=NO
HSB.2_STARTED=NO
NEXT_ALLOWED_STAGE=HSB.1V
```

Публикация может быть объявлена PASS только после обычного `git push origin work`, повторного fetch, равенства `HEAD == origin/work` и проверки SHA через GitHub.

## Публикационная проверка

Обычный `git push origin work` выполнен успешно без force 2026-08-11. Затем `git fetch origin work` подтвердил:

```text
PUSH_MODE=NORMAL_NO_FORCE
PUBLISHED_VERIFIED_SHA=5782d4f66d9b582e84153c1133e824fd7f4b10d9
HEAD=5782d4f66d9b582e84153c1133e824fd7f4b10d9
ORIGIN_WORK=5782d4f66d9b582e84153c1133e824fd7f4b10d9
HEAD_EQUALS_ORIGIN_WORK=YES
GITHUB_API_SHA=5782d4f66d9b582e84153c1133e824fd7f4b10d9
GITHUB_SHA_EXISTS=YES
HSB.1V_PUBLISHED=PASS
```

GitHub API endpoint `/repos/ic8812825-maker/chatgpt.com-codex/commits/work` вернул тот же SHA. Настоящая публикационная запись создаётся следующим обычным commit и также подлежит обычному push; её окончательный SHA проверяется post-push и сообщается как transport evidence без попытки самоссылки SHA внутри собственного содержимого.
