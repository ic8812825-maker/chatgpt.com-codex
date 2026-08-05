# Матрица требований и будущего MQL5 mapping

Версия 1.0. Статус: нормативный baseline.

| Requirement | Норма | Будущий owner | MQL5 evidence | Тест |
|---|---|---|---|---|
| HSBI-GEN-010 | Hybrid-only runtime | Core/RuntimeMode | HSB.1 | static dependency |
| HSBI-ID-010 | полный OwnershipGuard | Execution/OwnershipGuard | HSB.3 | foreign/stale identity |
| HSBI-MATH-014 | broker-money catch-up | Planning+Money | HSB.4 | BUY/SELL money grid |
| HSBI-GEO-005 | повтор gates после rounding | Planning/GeometrySolver | HSB.4 | coarse grids |
| HSBI-FSM-002 | advance только actual outcome | Core/FSM | HSB.3/5 | partial/delayed fill |
| HSBI-INIT-002 | Initial Profit excluded | Scenarios/InitialLock | HSB.5 | ledger exclusion |
| HSBI-BIG-003 | exactly-once allocation | BigHarvest+Money | HSB.5 | replay/restart |
| HSBI-PF-001 | Reserve не участвует | PartialFar | HSB.5 | source isolation |
| HSBI-FC-001 | единый RecoveryPL | FinalCloseCalculator | HSB.5 | double count |
| HSBI-SMALL-001 | строгий transition order | SmallTransition | HSB.5 | transaction sequence |
| HSBI-NF-001 | actual Core residual | NewFarSolver | HSB.4/5 | requested≠actual |
| HSBI-MONEY-014 | keys/exactly-once | Ledgers | HSB.2 | duplicates/conflicts |
| HSBI-TX-006 | OnTradeTransaction barrier | TransactionEngine | HSB.3 | no premature state |
| HSBI-PERSIST-001 | atomic snapshot | SnapshotStore | HSB.2 | crash injection |
| HSBI-RECON-002 | Far не угадывается | Reconciliation | HSB.2 | duplicate Far |
| HSBI-RISK-001 | risk в money | Risk/BrokerMoney | HSB.4 | control price |
| HSBI-TEST-001 | MetaEditor evidence | Tests/MQL5 | HSB.6 | 0 errors/warnings |
| HSBI-PROD-001 | all readiness gates | Reports | HSB.8/9 | acceptance |

## Правила матрицы

- `HSBI-GEN-040`: Requirement ID уникален и неизменяем после публикации; изменение смысла создаёт новый ID.
- `HSBI-GEN-041`: статус будущего mapping: NOT_STARTED, MAPPED, IMPLEMENTED, TESTED, EVIDENCED, REJECTED.
- `HSBI-GEN-042`: наличие функции без caller/runtime/transaction/test не является PASS.

Вход: нормативные документы. Выход: связь requirement→owner→evidence. Preconditions: уникальные IDs. Postconditions: ни одно production действие не остаётся без нормы. Restart не применим; owner: architecture/traceability. Тест: автоматический поиск duplicate IDs и missing mapping. Открытый вопрос: machine-readable формат матрицы на HSB.1.