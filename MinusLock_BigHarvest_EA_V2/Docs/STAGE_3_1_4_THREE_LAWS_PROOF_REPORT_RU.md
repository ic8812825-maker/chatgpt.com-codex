PROJECT=MinusLock_BigHarvest_EA_V2
STAGE=3.1.4
PURPOSE=THREE_LAWS_FORMAL_REVALIDATION
BRANCH=work
BASE_COMMIT=c0b2588d96d8e2db6fd009af2cfd7f993dca8383
REPOSITORY_SCOPE=MinusLock_BigHarvest_EA_V2/
STAGE_3_1_3_STATUS=CLOSED
STAGE_3_1_5_STARTED=NO

# Полная математическая перепроверка трёх законов Hybrid Split Big

## 1. Фактический baseline

Ожидаемый `65eccf6` и локальный synthetic commit `66557ea` имели одинаковый
tree, но разные histories. Без reset/rebase опубликованная история была безопасно
интегрирована merge commit `c0b2588d96d8e2db6fd009af2cfd7f993dca8383`,
обычно опубликована в `work`, после чего local/remote parity и clean tree
подтверждены. Это actual baseline Этапа 3.1.4.

## 2. Canonical mathematical baseline

| Величина | Unit / sign | Source и temporal class | Rounding |
|---|---|---|---|
| OldFar, CurrentFar, ResidualFar, NewFar | role/position identity, non-numeric | reconciled Symbol+Magic+Cycle position mapping, ACTUAL | exact identity |
| F = FarActualLot | lot, `>=0` | terminal position snapshot, ACTUAL | broker lot grid |
| C = BigCoreLotNormalized | lot, `>=0` | immutable plan, PROJECTED | floor to LotStep |
| T = BigTrendLotNormalized | lot, `>=0` | immutable plan, PROJECTED | floor to LotStep |
| S = SmallBaseLotNormalized | lot, `>=0` | immutable plan, PROJECTED | conservative broker grid |
| B = BigGross | lot, `>=0` | `C+T` одного plan, PROJECTED | sum normalized components |
| Reserve / FinalReserveReal | account money, `>=0` | confirmed ledger/deals, ACTUAL | money rounding at ledger boundary |
| α = FinalReserveShare | dimensionless, `[0,1]` policy | approved profile, POLICY | no lot rounding |
| RecoveryPLProjected | account money, signed | OrderCalcProfit semantics + explicit costs, PROJECTED | no early money rounding |
| GrossOld, GrossNext | lot, `>=0` | sum of absolute managed-cycle actual/normalized lots at reconciled snapshots | component broker grid |
| RiskOld, RiskNext | account money loss, `>=0` | projected broker loss to explicit control prices | conservative money comparison |
| q | dimensionless, `(0,1)` when proven | ratio of consecutive normalized Far volumes | exact rational/Decimal bound |
| Step / MinLot | lot, `>0` | broker symbol specification | exact broker volume grid |
| Price, Bid, Ask | price, `>0` | immutable tick/snapshot | TickSize grid; BUY closes Bid, SELL closes Ask |
| Point, TickSize | price increment, `>0` | broker symbol specification | exact decimal input |
| TickValue | account money per tick per lot, `>0` | broker profit calculation/symbol specification | direction-aware where asymmetric |

`OldFar`/`NewFar` identities нельзя подменять их lot magnitudes. Requested lots
не являются Filled/Actual. Ни одно policy value на этом этапе не выбирается и не
изменяется.

```text
BRANCH=work
LOCAL_REMOTE_PARITY=PASS
WORKTREE_AT_BASELINE=CLEAN
PRODUCTION_TRADING_LOGIC_CHANGED=NO
PARAMETER_PROFILE_CHANGED=NO
STAGE_3_1_5_STARTED=NO
```
