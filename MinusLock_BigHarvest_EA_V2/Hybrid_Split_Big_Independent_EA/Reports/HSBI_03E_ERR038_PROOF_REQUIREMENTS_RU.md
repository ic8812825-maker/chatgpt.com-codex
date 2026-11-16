# HSBI-03E — ERR-038: предпосылки и план доказательства

Версия: **HSBI-03E-R1**. SOURCE_COMMIT_SHA=`b5ca9d377d454dfbec63ece76dd1c759abc3656d`.
Репозиторий `ic8812825-maker/chatgpt.com-codex`, ветка `work`, все относительные source paths внутри `MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/`.
Статус: **PROPOSED / AWAITING_OWNER_DECISION**. Ни один текст не APPROVED. Нормативный выбор, architecture/provider и implementation evidence — разные gates.
STATIC_REVIEWED означает чтение исходного текста; MATH_DERIVED — вывод при указанных предпосылках; COUNTEREXAMPLE_CONFIRMED — опровержение утверждения, не runtime PASS; HISTORICAL_TEST_RESULT — старый artifact; все новые vectors TEST_SPECIFIED_NOT_RUN; NATIVE_NOT_RUN. Новых compile/runtime/mutation/native tests не выполнялось.
UNAVAILABLE — обязательное evidence отсутствует; CONFLICT — доказательства противоречат; REJECT — доказанное нарушение домена/предусловия. Все три запрещают новый effect; финансовая delta=0. NO_OP возможен только по валидному полному старому receipt.
Публикация отчёта не утверждает контракт, не закрывает P0 и не разрешает production/R1.1/dispatch/trading.

ERR_038_STATUS=OPEN. ProofRequirementsId=HSBI_ERR038_BOUND_REQUIREMENTS_V1/HSBI-03E-R1.
Результат — перечень предпосылок и theorem plan,не фиктивное закрытие.

## Источники

Docs/04_MATHEMATICAL_MODEL_RU.md:21,33–36,42:compression и conditionalq bound;Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md:6–21 risk/gap/margin/emergency;Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md:17–27 future/terminal;Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md:12–20 partial/unknown/restart.
Reports/HSBI_03D_MONEY_INVARIANTS_AND_COUNTEREXAMPLES_RU.md:122–132;HSBI_03D_P0_REMEDIATION_CROSSWALK_RU.md:ERR038 row;HSBI_R11_P0_DEPENDENCY_PLAN_RU.md:ERR038 deployment row.
Include/Risk/HSBI_NewFarGateTypes.mqh:6–16 HSBI_EvaluateNewFarGates;Include/Planning/HSBI_NewFarSolver.mqh:107–151 HSBI_SolveNewFar. Эти gates проверяют inputs/finite projections,не global market theorem.

## Пять разных свойств

| Свойство | Что ограничивает | Чего само по себе не доказывает |
|---|---|---|
| PositionCount≤N | число одновременно открытых позиций | size,price movement,costs,turnover |
| GrossLots≤V | сумму абсолютных активных lots | unbounded price/FX/costs/time;total traded lots |
| MarginUsage≤M | расчёт/использование collateral при текущих assumptions | guaranteed liquidation price,no negative balance,loss bound |
| RealizedLoss≤L_R | подтверждённые убытки выбранного периода | open liability,unfilled stops,future losses,entire-cycle drawdown |
| MaximumMoneyLoss≤L | worst-case realised+unrealized+remainingcosts по stated admissible paths | не выводится из предыдущих без дополнительных assumptions |

Fixed SELL volume1,K1,priceP0+M →lossM,неограничен приM→∞. Bounded positions/lots сохранены.
Дополнительный counterexample: prices ограничены[0,1],volume1,buy1/sell0 повторяетсяn раз→realized lossn. Даже priceband+currentlot bound недостаточны без bounded turnover/action count/time/costs.
Margin cap при gap и unbounded slippage не гарантирует финансовый cap;stop-out — механизм,не contractual price bound.

## Набор необходимых по смыслу assumptions (либо доказанная замена)

Не все конкретные ограничения логически необходимы в любой модели: возможны alternative гарантии (например доказанный payoff cap). Но без хотя бы достаточной замены каждого unbounded loss channel universal claim невозможен.

| Channel | Что необходимо явно задать/подтвердить | Если нет |
|---|---|---|
| Adverse price movement | bounded admissible path/priceband либо bounded instrument payoff | SELL counterexample,unproved |
| Gaps | maximum jump или исполнимая worst-case gap price;не дублировать если уже в path bound | stop threshold не bound |
| Slippage/spread | upper executable adverse fill deviation/spread and costs basis | requested price не loss cap |
| Liquidity | достаточная глубина/volume по bounded prices и time;partial-fill worstcase | остаток открыт неограниченно |
| Execution refusal | bounded close delay/retry outcomes либо alternative guaranteed liquidation authority | broker refusal может держать exposure заhorizon |
| Stop execution | market-stop vs guaranteedstop contract,trigger side,latency,gap semantics | stop order alone не guarantee |
| Margin liquidation | leverage/margin formula,portfolio offsets,stop-out trigger/order,fill bound,FX | margin usage alone не loss |
| Stop-out | bounded actual liquidation proceeds и account liability contract | нельзя считать автоматический zero loss/limited debit |
| Commissions/fees | max rate/perfill and bounded number of fees/turnover,conversion | unbounded repeated fees |
| Swap/funding | bounded rate,horizon,cash debit currency and accrued quantities | infinite time costs unbounded |
| Exposure | gross/net distinction;max absolute open lots AND cumulative traded lots | hedge cancellation не cost/short liability cap |
| Currency/contract | finite contract multiplier/tick-value slope/FX bound over allowed price domain | constantK approximation insufficient |
| Fail/restart/unknown | no double dispatch,conservative unknown exposure,independent fills,state receipts | hidden exposure/duplicate loss |
| Time/horizon | bounded exposure duration + actual closure assurance OR explicit theorem beyondhorizon | sampling horizon не guarantee |

Никаких broker values/protective guarantees в этом этапе не получено. Negative balance protection,если существует,нуждается в независимом contractual evidence и scope;оно не предполагается и не равнозначно profitable strategy.

## Одна достаточная условная theorem shape

Предположить:
- весь exposure lifecycle покрыт horizonT и доказанным actual close completion,либо contractually bounded terminal payoff;
- Q_total≤Qmax — cumulative lot-equivalent объём всех opened/closed exposure lots,including projected terminal closure,без double counting partial pieces;
- V_gross(t)≤Vmax и N_fee≤Nmax;
- |ΔPnL_i|≤Kmax×v_i×|ΔP_exec_i| в account currency для каждого contract и FX state;
- executable adverse span D_exec≤D_move+D_gap+2S_max;если D_move уже включаетgaps,использоватьD_gap0;
- fee debit≤fmax percountedfee,swap debit rate≤wmax money/(lot×time),other debit≤C_other,max;
- no unaccounted duplicate/unbounded tail/unclosed unknown positions.

Тогда sufficient conservative bound:
L_max ≤ Kmax×Qmax×D_exec + Nmax×fmax + wmax×Vmax×T + C_other,max.
Все величины finite/nonnegative,общие units;Σvolume and Σfees independent. Условия могут быть заменены более точными perinstrument sums без потери coverage.
Это MATH_DERIVED из triangle/upper-bound inequalities,не доказательство истинности premises в рынке. Netting/hedging и rebates могут уменьшить actual loss,но нельзя использовать их для уменьшения bound без отдельного pathwise proof.
При MIN/MAX numeric overflow bound UNAVAILABLE,не отрицательная/нулевая «граница».
Finite N/F compression не даёт Qmax/finiteT автоматически:нужны rounding/plateau/terminal execution и turnover theorem.

## План доказательства и evidence gates

1. Freeze scope: cycle/account/symbols,directions,horizon,lossdefinition(realised+open+remainingcost),excluded Initial diagnostic отдельно;Economic loss не исчезает от D06-A exclusion.
2. Define admissible market/execution paths и перечислить каждый debit channel;дляunsupportedpath no boundedclaim.
3. Obtain independent broker/instrument/margin/stop/FX/fee/swap/liquidity evidence и owner acceptance конкретных assumptions.
4. Prove Qmax,Vmax,Nmax,T/terminal completion сexact grids и adversarial partial/unknown/restart outcomes.
5. Prove broker payoff/conversion bound Kmax,Dexec и no doubled/omitted cost basis.
6. Prove conservation/source authority/atomic journal не создают duplicate economic effects;это исключает software losses,но не market ones.
7. Derive symbolic bound иexact checked numerical instantiation. Stress/fault tests ищут counterexamples,но finite simulations не доказывают universal theorem.
8. Independent review theorem,premises,limitations;versioned owner acceptance. До этого ERR038 OPEN. R1.1 может будущим отдельным заданием исправлять guards,но не обещать закрытие globalbound.

## Проверяемые отрицательные случаи

No pricebound fixedSELL→unbounded;boundedprice unlimited churn→unbounded;boundedlots unbounded swap horizon→unbounded;stoptrigger with unbounded gap/slippage→no finite cap;valid margin projection + refusal/unknown fills→no completion bound.
Все COUNTEREXAMPLE_CONFIRMED/MATH_DERIVED,не native tests.
Unresolved:все реальные premises/evidence,theorem review и model selection.
Связи:[objective](HSBI_03E_NEWFAR_OBJECTIVE_RESOLUTION_RU.md),[D06](HSBI_03E_D06_POLICY_RESOLUTION_RU.md),[numeric](HSBI_03E_NUMERIC_CONTRACT_MANIFEST_V1_RU.md),[gates](HSBI_03E_R11_GATE_MATRIX_RU.md),[ballot](HSBI_03E_OWNER_FINAL_DECISION_BALLOT_RU.md).
