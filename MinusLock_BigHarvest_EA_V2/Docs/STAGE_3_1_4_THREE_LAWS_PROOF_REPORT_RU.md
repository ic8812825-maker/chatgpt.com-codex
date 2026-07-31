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

## 3. Единая symbolic/sign model

Вводится directional coordinate `x>=0`: пройденное broker-valid расстояние к
Big. `dP/dx=+1` для UP и `dP/dx=-1` для DOWN. Тогда объёмы всегда неотрицательны,
а знак leg задаёт направление позиции, не знак lot.

| Position | UP move to Big | DOWN move to Big |
|---|---:|---:|
| Far | `-F` | `-F` |
| BigCore | `+C` | `+C` |
| BigTrend | `+T` | `+T` |
| SmallBase | `-S` | `-S` |

UP: Big legs BUY (закрытие Bid), Far/Small SELL (закрытие Ask). DOWN: Big legs
SELL (Ask), Far/Small BUY (Bid). После transform к `x` обе directional slopes
равны `C+T-S-F`; spread меняет intercept и event costs, но при frozen spread не
+меняет slope. Все четыре lots имеют unit LOT; slope умножается на direction-aware
broker money/tick/lot, поэтому результат MONEY/price-distance.

## 4. Law 1 — аналитическая lot-база

На малом движении `dx` Big gross создаёт favorable capacity `B=C+T`; Small
движется с Far и потребляет `S`, поэтому доступная база `B-S`. Только доля `α`
назначается FinalReserve: reserve slope `α(B-S)`. Far deficit растёт со slope
`F`. Разность coverage имеет slope `α(B-S)-F`, откуда необходимое строгое
условие `α(C+T-S)>F`.

Equality даёт нулевой slope и никогда не закрывает положительный initial deficit;
`<` увеличивает deficit; только `>` допускает catch-up за конечную дистанцию.
`α<=0`, `B<=S` и non-terminal `F=0` invalid; `α>1` вне share contract. Малый F
и normalized lots проходят то же строгое сравнение после broker normalization.
Это necessary analytic layer, не production permission.

## 5. Law 1 — level-by-level broker money

Для каждого `P_k` leg money вычисляется как direction-aware close result на Bid
или Ask по семантике `OrderCalcProfit`, а не `lots*points*10`:
`ReserveAdd_k=α*max(0,BC_k+BT_k-SB_k)`; `ReserveTotal_k=R0+ReserveAdd_k`;
`Coverage_k=ReserveTotal_k+FarMoney_k`. Gate требует не только положительный lot
slope, но broker-money coverage на каждом обязательном level и финальный
`Coverage_k>=0`. TickSize/Point/digits и разные positive/negative TickValue
являются inputs. Поэтому EURUSD-like, JPY-like и asymmetric tick-value tracks
вычисляются независимо. `LOT_CATCH_UP=PASS, MONEY_CATCH_UP=FAIL` всегда даёт
`FINAL_PLAN=REJECT`.

## 6. Law 1 — costs

`GrossReservePotential=α*max(0,BigCoreGross+BigTrendGross-SmallGross)`.
`Costs=commission_open+commission_close+swap+fee+slippage_allowance`; spread уже
включён использованием Bid/Ask и второй раз в Costs не добавляется.
`NetReservePotential=GrossReservePotential-Costs`. Final coverage использует
только Net. Adversarial contract требует обнаружить случай Lot PASS + Gross PASS
+ Net FAIL и отклонить plan.

## 7. Law 2 — analytic directional slope

`RecoveryPL(x)=RealizedCyclePL+Σ LegMoney_i(x)-ExpectedExitCosts(x)`.
Между events при frozen costs: UP derivatives равны `+C,+T,-S,-F`; DOWN имеет
противоположные derivatives по absolute price, но `dP/dx=-1`, поэтому после
chain rule снова `+C,+T,-S,-F`. Следовательно
`dRecoveryPL/dx=PV_dir*(C+T-S-F)`. При `PV_dir>0` strict improvement требует
`C+T-S-F>0`. Bid/Ask symmetry доказана transform, а не фразой «аналогично».

## 8. Law 2 — broker-grid monotonicity

Price grid строится целыми ticks: `P_k=P_0+direction*k*TickSize`; Bid/Ask
нормализуются отдельно. Для всех `k` до Big oracle требует
`RecoveryPL(P_{k+1})>RecoveryPL(P_k)` без epsilon, скрывающего plateau. Проверки
включают 1,2,10,50,100,200,300 и 500+ points и non-integer Point/TickSize через
целое число ticks. Analytic slope PASS без exhaustive interval PASS недостаточен.
