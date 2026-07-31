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
меняет slope. Все четыре lots имеют unit LOT; slope умножается на direction-aware
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
Net FAIL и отклонить plan.

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

## 9. Law 2 — event boundaries

Continuous monotonicity действует только между events. Для open/close
commission, swap accrual, fee, slippage, spread revision, partial close и
realized/unrealized transfer вычисляются два reconciled snapshots одного EventID:
`RecoveryPL_after-RecoveryPL_before`. Transfer realized↔floating сам по себе
conservative; новые costs являются отрицательным jump. Допустимый action обязан
сохранить требуемый contract, иначе `EVENT_MONOTONICITY=FAIL` и plan reject.
Derivative не используется как доказательство jump.

## 10. Law 3 — NewFar

`OldFar` — reconciled role до transition; `NewFar` создаётся только из явно
разрешённого residual/promoted role после reconciliation. Cache, request и Big
role не являются NewFar. Non-terminal compression требует
`0<NewFarActualLot<OldFarActualLot`; `NewFar=0` — terminal full close,
`NewFar=OldFar` — stagnation, `NewFar>OldFar` — expansion. Этап не выбирает
policy источника NewFar, а классифицирует результат.

## 11. Law 3 — NextBigGross

Pipeline различает Raw→Calculated→Normalized→Requested→Filled→Actual.
Для следующего plan `NormalizedNextBigGross=NormalizedNextBigCore+
NormalizedNextBigTrend`; strict gate сравнивает его с actual OldFar:
`NormalizedNextBigGross<OldFarActualLot`. Raw PASS при normalized `>=` является
`BROKER_ROUNDING_FAILURE`; requested/fill не подменяют proof и после execution
нужна reconciliation actual lots.

## 12. Law 3 — gross exposure

На двух одинаково scoped reconciled lifecycle snapshots
`Gross=Σ abs(ActualManagedPositionLot)` по Symbol+Magic+Cycle. `GrossOld`
фиксируется до transition, `GrossNext` — после partial Far, NewFar creation,
next Big и Small reconciliation. Gate `GrossNext<GrossOld` запрещает сравнивать
preview одного цикла с actual другого или пропускать SmallBase.

## 13. Law 3 — risk

Canonical Risk — broker money loss managed basket до явной control price:
`Risk(snapshot,control)=max(0,-ΣOrderCalcProfitLike(leg,control)-ExitCosts)`.
Это не gross lots. При одинаковом symbol specification, scope, control-price
policy и cost convention проверяется `RiskNext<RiskOld`. Canonical contract определяет `NextFarRiskMoney`, общий control-price/cost scope
и обязательный gate `NextCycleRisk<OldCycleRisk`. Поэтому для admissible plan
`RISK_COMPRESSION=PASS`; candidate без frozen comparable controls является
не admissible и отклоняется, а Risk не подменяется gross lots.

## 14. Worst-case q

Для каждого admissible non-terminal transition определяется
`q_n=NormalizedNewFar_{n+1}/ActualOldFar_n`. Contract требует proof по всему
admissible domain: `q_n<=q_max<1`, не average. Если policy задаёт continuous
`r_max<1`, conservative ceiling normalization даёт
`NewFar<=ceil_step(r_max*F)`; strict post-normalization check необходим, поскольку
при малом F ratio может стать 1. Без frozen bounds ratios/close share и rounding
нет универсального numeric q: validator требует либо explicit `q_max`, либо
terminal/reject для такого candidate.

## 15. Discrete finite termination

При proven `0<q_max<1`, `F_n<=q_max^n F_0`. Первый continuous bound:
`N_cont=ceil(log(MinLot/F_0)/log(q_max))`. Broker proof сильнее: каждый accepted
non-terminal transition обязан уменьшить integer grid index
`m_n=round(F_n/LotStep)` минимум на 1. Поэтому независимо от floating limit
`N_max<=m_0` и точнее минимум geometric bound с последующей grid verification.
Если normalized next lot равен current, transition reject/terminal; бесконечный
plateau невозможен в admitted sequence.

## 16. Rounding pathologies

Обязательные adversarial cases: raw compression/normalized fail; raw NewFar,
округлённый к тому же lot; `q_raw<1,q_normalized=1`; CloseLot<MinLot; Core floor;
Small ceiling; mixed floor/ceiling destruction; residual dust; coarse LotStep.
Каждый публикует `RAW_LAW_STATUS`, `NORMALIZED_LAW_STATUS`, `FINAL_STATUS`.
Единое правило: normalized FAIL ⇒ `FINAL_STATUS=REJECT`, даже при raw PASS.

## 17. Margin и worst-case separation

Law satisfaction — только один input Decision Engine. Cases
`LOT_LAWS=PASS,MONEY_LAWS=PASS,MARGIN_GATE=FAIL` и аналогичный
`WORST_CASE_GATE=FAIL` обязаны дать `PLAN=REJECT`. Ни oracle, ни manual не
объявляют trade permitted по трём laws без margin, worst-case, freshness,
execution и reconciliation gates.

## 18. Big→Small boundary

Последний Big snapshot, Small transition snapshot, NewFar creation и first next
cycle snapshot имеют разные immutable fingerprints. Reserve transfer сверяется
ledger events; RecoveryPL — before/after reconciled money; OldFar/NewFar и
GrossOld/GrossNext сравниваются только после confirmed fills. Непарные snapshots
дают `BOUNDARY_EVIDENCE_MISSING`, не PASS. Partial execution сохраняет старый
cycle active либо отклоняет promotion.

## 19. Independent UP/DOWN tracks

UP track использует BUY Big close на Bid и SELL Far/Small close на Ask; DOWN —
SELL Big на Ask и BUY Far/Small на Bid. Для каждого независимо строятся price
grid, money trajectory, costs, event jumps и compression snapshots. Transform
`x=direction*(P-P0)` унифицирует slope только после отдельного Bid/Ask расчёта.
Общий PASS требует `UP_THREE_LAWS=PASS` и `DOWN_THREE_LAWS=PASS`; один track не
может маскировать другой.

## 20. Независимый Python oracle

`Tools/three_laws_oracle.py` использует `Decimal` и вычисляет contract, не читая
PASS из документации: normalized lots, каждый broker tick, direction-aware
money, costs, strict pointwise monotonicity, event jump, NewFar/NextBig/Gross,
q и finite bound. Invalid off-grid distances и non-positive broker properties
отклоняются. Spread представлен Bid/Ask-derived initial intercept и не считается
повторно как cost.

## 21. Automated boundary matrix

Matrix использует lots 0.01…5.00, LotStep 0.01/0.1/coarse 0.25, distances
1/10/50/100/200/300/550 points, UP/DOWN, explicit five-part costs, strict PASS,
equality и strict FAIL. Off-grid/min-lot combinations отбрасываются как invalid,
а не пропускаются как PASS. Фактическое число вычисленных valid combinations
публикует test runner.

## 22. Critical counterexamples

Oracle tests обязаны поймать девять именованных ложных proofs:
`CatchUpLotPass_MoneyFail`, `RecoverySlopePass_PointwiseFail`,
`CompressionRawPass_NormalizedFail`, `CompressionPass_RiskFail`,
`qAveragePass_qWorstCaseFail`, `FiniteContinuousPass_DiscreteFail`,
`UPPass_DOWNFail`, `SpreadZeroPass_RealSpreadFail`,
`MarginIgnoredPass_MarginFail`. Они мутируют inputs/assumptions, а не итоговый
PASS, и каждый проходит фактический computation path.

## 23. Canonical law contract

Главный manual дополнен одинаково структурированными контрактами трёх laws:
variables/units/preconditions, analytic necessary, broker-normalized, money,
event, margin/worst-case, PASS/FAIL, terminal и executable evidence. Necessary,
sufficient evidence и trade permission разделены явно.

## 24. Read-only MQL5 mapping

| DOCUMENTED_LAW | EXISTING_MQL5_IMPLEMENTATION | STATUS |
|---|---|---|
| Reserve Catch-Up analytic/net money/levels | `HybridDecisionEngine.mqh` Law1 gate; `HybridGeometrySolver.mqh`; `HybridCatchUpModel.mqh::EvaluateHybridCatchUpLevel`; `BrokerMoneyModel.mqh` | IMPLEMENTED |
| Recovery analytic + broker-grid | `HybridDecisionEngine.mqh` Law2; `ValidateHybridRecoveryMonotonicity`; catch-up row RecoveryPL | IMPLEMENTED |
| Recovery event-boundary universal contract | route/reconciliation checks exist, but not every allowed commission/swap/partial event is exposed as one universal monotonic gate | PARTIAL |
| NewFar/NextBig normalized compression | StateMachine target checks, `HybridCatchUpModel` next geometry, RecoveryMath legacy compression | IMPLEMENTED |
| Gross compression same lifecycle snapshots | fields/checks distributed across plan and StateMachine | PARTIAL |
| Money risk compression to common control price | margin/worst-case gates exist; one universally frozen RiskOld/RiskNext policy is not canonical for every route | PARTIAL |
| Worst-case q + discrete finite bound | finite catch-up engine exists, but universal policy-domain `q_max` is not frozen | PARTIAL |

Production sources прочитаны без изменений. Gaps относятся к future implementation/
policy stages; этот этап не меняет MQL5, order sequence, gates или profiles.

## 25. Fail-closed validator contract

`Tests/validate_stage_3_1_4_three_laws.py` исполняет oracle matrix и девять
counterexamples, считает 14 named blockers и возвращает non-zero при любом.
Risk проверяется по canonical money-risk entities и strict Next<Old gate. q
вычисляется как worst-case maximum Target cap всех трёх normative profiles
(`q_max=0.35<1`), а не по удобному test profile или average.

## 26. Final revalidation, commits, limitations и verdict

### Commits

- `b663114f5604dfc2b5693d8f016a471e8f832e81` — `Этап 3.1.4.1: зафиксирован математический baseline трёх законов Hybrid Split Big`
- `4a309351dff3f0b3731d7b51b8f4b0c07c19bad4` — `Этап 3.1.4.2: построена единая знаковая и размерностная модель трёх законов`
- `83ee791b9cf01bc0e507e3907bb1be06124c902a` — `Этап 3.1.4.3: заново выведено необходимое лотовое условие Reserve Catch-Up`
- `44b8fb31aa98881c4f8b4051154ab690bd5f2add` — `Этап 3.1.4.4: доказан level-by-level broker-money Reserve Catch-Up gate`
- `0924b0dbba0cd3def491254707b495b6dca6a311` — `Этап 3.1.4.5: Reserve Catch-Up переведён на net-money proof с учётом торговых издержек`
- `c17cc182fe100993c717fed12a6c975404b0d13d` — `Этап 3.1.4.6: заново выведен аналитический slope RecoveryPL для UP и DOWN сценариев`
- `11ebbb45a2717e1c8e81356ffd4c7c1ba9cb498b` — `Этап 3.1.4.7: доказана broker-grid point-by-point монотонность RecoveryPL`
- `0572879790a4cb19c81bd7a5c2d7f12142354a31` — `Этап 3.1.4.8: проверена монотонность RecoveryPL на торговых event boundaries`
- `1b5fc762a281c2927b54994e2cdf7683e076e649` — `Этап 3.1.4.9: формализовано строгое условие уменьшения NewFar относительно OldFar`
- `176de2b91eb4f988a6b0e3f1faa9a0045a139d36` — `Этап 3.1.4.10: доказано broker-normalized сжатие NextBigGross`
- `fdabe6b2deefa22d2d4d2afdd06acf934abe4ff2` — `Этап 3.1.4.11: доказано строгое уменьшение gross exposure между циклами`
- `8b4f6e8e4725b69981cc28cefefd70d3cf1b9acd` — `Этап 3.1.4.12: перепроверено условие строгого уменьшения риска между циклами`
- `64e08f84685d9bddeef1d1d5d491c51e212dd365` — `Этап 3.1.4.13: выведен строгий worst-case коэффициент сжатия q`
- `98b95123eb9b7f9d8f8f9fe667bde86cd296b9d7` — `Этап 3.1.4.14: доказана broker-rounded конечность числа разворотов Hybrid Split Big`
- `f410240af857a74615f7b437c6972bb4738b108f` — `Этап 3.1.4.15: проверены rounding pathologies трёх законов Hybrid Split Big`
- `dd02dd1c04998e39844a05180da58e97f250b62f` — `Этап 3.1.4.16: отделены математические законы от margin и worst-case разрешения плана`
- `14c4bb18de895fafe0c883a8a7fd9f737b66a1ea` — `Этап 3.1.4.17: доказана сохранность трёх законов при переходе Big в Small`
- `183adfb63ec746be8796efb47a71ab844843fb70` — `Этап 3.1.4.18: отдельно доказаны три закона для UP и DOWN сценариев`
- `3908fc1f7daaf07e4f9836e40806b63ede9338c2` — `Этап 3.1.4.19: создан независимый Python oracle трёх законов Hybrid Split Big`
- `77b4824f326202be099ae5c87bb9598ffbccefa0` — `Этап 3.1.4.20: создана автоматическая boundary и adversarial test matrix трёх законов`
- `03f239d0bb7ce8d41ab03674069c3e73bd22b1fe` — `Этап 3.1.4.20.1: исправлен проверенный минимум фактической матрицы из 210 сценариев`
- `b89c8e0c071c31eb7ce4fb961ac88b6d9e091dd8` — `Этап 3.1.4.21: добавлены контрпримеры против ложного доказательства трёх законов`
- `733a3a5918e465216efe6dabffba679c443dd96f` — `Этап 3.1.4.22: добавлен канонический нормативный контракт трёх законов Hybrid Split Big`
- `fbb631fb6c8724bfb2a274eca6edf8a29db8347c` — `Этап 3.1.4.23: выполнен read-only mapping трёх законов на текущую MQL5 реализацию`
- `a941902c8eaca368b2d6d667b392575565be4360` — `Этап 3.1.4.24: создан финальный validator математических законов Hybrid Split Big`
- `ac2a43e294464498ed27acc3aadc14471b4ba927` — `Этап 3.1.4.24.1: validator вычисляет worst-case q и risk contract из нормативного manual`

### Фактические результаты

```text
FINAL_EVIDENCE_HEAD=ac2a43e294464498ed27acc3aadc14471b4ba927
LAW_1_RESERVE_CATCHUP=PASS
LAW_1_ANALYTIC=PASS
LAW_1_BROKER_MONEY=PASS
LAW_1_COST_ADJUSTED=PASS
LAW_2_RECOVERY_MONOTONICITY=PASS
LAW_2_ANALYTIC_SLOPE=PASS
LAW_2_POINTWISE_MONOTONICITY=PASS
LAW_2_EVENT_BOUNDARY=PASS
LAW_3_COMPRESSION=PASS
LAW_3_NEW_FAR_COMPRESSION=PASS
LAW_3_NEXT_BIG_GROSS_COMPRESSION=PASS
LAW_3_GROSS_COMPRESSION=PASS
RISK_COMPRESSION=PASS
Q_WORST_CASE_BOUND=PASS
Q_MAX_WORST_CASE=0.35
DISCRETE_FINITE_TERMINATION=PASS
BROKER_ROUNDING_SAFETY=PASS
UP_SCENARIO=PASS
DOWN_SCENARIO=PASS
MONEY_MODEL=PASS
EVENT_BOUNDARIES=PASS
COUNTEREXAMPLE_SUITE=PASS
AUTOMATED_MATRIX_CASES=210
COUNTEREXAMPLES_CAUGHT=9
REPOSITORY_SCOPE_VIOLATION=NO
PRODUCTION_TRADING_LOGIC_CHANGED=NO
PARAMETER_PROFILE_CHANGED=NO
STAGE_3_1_5_STARTED=NO
STAGE_3_1_4_VALIDATION=PASS
```

### Unresolved dependencies и known limitations

Доказан математический admissibility contract, а не фактическое исполнение MT5.
`OrderCalcProfit` oracle представлен direction-aware tick-value semantics; exact
broker result, dynamic spread/swap и fills требуют runtime evidence. MQL5 mapping
имеет PARTIAL gaps для universal event/gross/risk orchestration, поэтому law PASS
не означает trade permission. Profile values не менялись: q_max=0.35 вычислен как
worst-case утверждённых SAFE/BALANCED/STRONG_COMPRESSION caps. Margin, worst-case,
freshness, execution и reconciliation остаются independent mandatory gates.

FINAL_VERDICT

STAGE_3_1_4_VALIDATION=PASS
LAW_1_RESERVE_CATCHUP=PASS
LAW_2_RECOVERY_MONOTONICITY=PASS
LAW_3_COMPRESSION=PASS

Q_WORST_CASE_BOUND=PASS
DISCRETE_FINITE_TERMINATION=PASS

UP_SCENARIO=PASS
DOWN_SCENARIO=PASS

REPOSITORY_SCOPE_VIOLATION=NO
PRODUCTION_TRADING_LOGIC_CHANGED=NO
PARAMETER_PROFILE_CHANGED=NO

STAGE_3_1_4_STATUS=CLOSED
NEXT_ALLOWED_STAGE=3.1.5
STAGE_3_1_5_STARTED=NO
AWAITING_USER_APPROVAL=YES
