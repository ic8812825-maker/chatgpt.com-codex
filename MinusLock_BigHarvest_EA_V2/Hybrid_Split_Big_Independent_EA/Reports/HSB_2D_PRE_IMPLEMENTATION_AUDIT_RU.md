# HSB.2D — предреализационный аудит

```text
BASELINE_SHA=c5797cc7cdb75594d866807694983aee17da6295
BRANCH=work
ORIGIN_WORK=c5797cc7cdb75594d866807694983aee17da6295
REMOTE_WORK=c5797cc7cdb75594d866807694983aee17da6295
WORKTREE_CLEAN=YES
LAST_TEST_ID=T430
```

Доступны контракты HSB.2A/2B/2B-R/R2/R3/2C-R1-P2: broker money/margin, grid, FutureSmall aggregate, NewFar candidate, MoneyProofIdentity, Reserve Catch-Up, allocation source/consumption key, execution intent, journal, snapshot и reconciliation. Отсутствуют единый immutable runtime decision DTO, admission gate, restart validator и интегральный transaction decision barrier.

Переиспользуются существующие proof DTO без повторного расчёта математики. Планируются новые headers `Runtime/HSBI_RuntimeDecisionTypes.mqh`, `Runtime/HSBI_RuntimeDecisionValidator.mqh`, `Runtime/HSBI_RuntimeRestartValidator.mqh`, `Runtime/HSBI_RuntimeTransactionBarrier.mqh`, тесты T431+ и нормативные документы HSB.2D.

Граница этапа: только чистые validators/decision results. Запрещены broker dispatch, мутация Context/FSM/ledger, изменения старого production EA, торговые вызовы, linear shortcuts и HSB.2E.
