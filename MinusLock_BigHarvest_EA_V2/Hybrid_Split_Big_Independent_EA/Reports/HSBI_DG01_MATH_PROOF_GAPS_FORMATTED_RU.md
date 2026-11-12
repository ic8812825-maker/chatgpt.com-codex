# AUDIT 02 — 49 семейств формул

23 условных математических утверждения; 11 конфликтов code/contract/proposal; 15 UNVERIFIED. В первом аудите было24/11/14: F42 понижен, native codec не доказан. Ни одна условная теорема не подтверждает production по всему domain.

## F01 — Core floor(F*Rc)
Статус: VERIFIED_CONDITIONAL_MATHEMATICS
Источник: Include/Planning/HSBI_BrokerGrid.mqh:26; норматив: Docs/04:9
При step>0 и x>=0 floor(x/step)*step<=x, разница<step. Это арифметика вещественных, не доказательство binary64/grid-origin.
Граница/оставшаяся проверка: Algebra/local rounding only; mandatory minimum checked separately

## F02 — Trend floor(F*Rt),Rt>=0
Статус: CONTRADICTORY_CONTRACT_OR_SOURCE
Источник: Include/Money/HSBI_BasketMoneyEvaluator.mqh:15; норматив: Docs/04:9
См. индивидуальную проблему/границу ниже; численные совпадения не являются доказательством.
Граница/оставшаяся проверка: Inactive-leg integration inconsistency

## F03 — Small ceil(F*Rs)
Статус: VERIFIED_CONDITIONAL_MATHEMATICS
Источник: Include/Planning/HSBI_BrokerGrid.mqh:27; норматив: Docs/04:9
ceil(x/step)*step>=x и <x+step при step>0; broker min/max проверяются отдельно.
Граница/оставшаяся проверка: Post-round risk/margin still needed

## F04 — All active legs min<=V<=max/grid
Статус: CONTRADICTORY_CONTRACT_OR_SOURCE
Источник: Include/Planning/HSBI_GeometrySolver.mqh:32; норматив: Docs/04:9
См. индивидуальную проблему/границу ниже; численные совпадения не являются доказательством.
Граница/оставшаяся проверка: No real orders

## F05 — Bnet=C+T-S; slope=Bnet-F
Статус: VERIFIED_CONDITIONAL_MATHEMATICS
Источник: Include/Planning/HSBI_GeometrySolver.mqh:10; норматив: Docs/04:12
Для одинакового линейного unit-value, фиксированных объёмов производная по движению против Far: C+T-S-F. При иной контрактной стоимости нужна broker модель.
Граница/оставшаяся проверка: Necessary local sensitivity, not profitability

## F06 — reserveShare*Bnet>F
Статус: VERIFIED_CONDITIONAL_MATHEMATICS
Источник: Include/Money/HSBI_CatchUpModel.mqh:12; норматив: Docs/04:15
В линейной симметричной модели рост Reserve r*B и FarLoss F даёт положительную разность slope при rB>F; начальный deficit/costs этим не покрыты.
Граница/оставшаяся проверка: Only necessary symmetric linear filter

## F07 — ActualDealNet=P+Swap+C+Fee
Статус: VERIFIED_CONDITIONAL_MATHEMATICS
Источник: Include/Money/HSBI_CostModel.mqh:13; норматив: Docs/08:6
Net определяется сложением signed денежных компонентов; знак каждого сохраняется. 60-2-7-1=50. Authenticy не следует из равенства.
Граница/оставшаяся проверка: Actual broker receipt authenticity notproved

## F08 — ProjectedNet=gross+swap+comm+fee-spread-slip-buffer
Статус: VERIFIED_CONDITIONAL_MATHEMATICS
Источник: Include/Money/HSBI_CostModel.mqh:18; норматив: Docs/24:7
При независимых непересекающихся deductions projectedNet=gross+signedSwap+signedCommission+signedFee-spread-slip-buffer по определению учёта. Overlap не доказан.
Граница/оставшаяся проверка: Only disjoint cost basis; overlap F09

## F09 — No repeated cost coverage
Статус: UNVERIFIED
Источник: Include/Money/HSBI_CostModel.mqh:4; норматив: D06 awaiting
См. индивидуальную проблему/границу ниже; численные совпадения не являются доказательством.
Граница/оставшаяся проверка: Missing basis/policy; conditional counterexample

## F10 — RecoveryPL=RealizedCycleNet+OpenCloseNowNet
Статус: VERIFIED_CONDITIONAL_MATHEMATICS
Источник: Include/Money/HSBI_MoneyTypes.mqh:9; норматив: Docs/04:18
При едином boundary cycle realized уже включает все проведённые входные/выходные costs; closeNow открытых позиций учитывается один раз. Reserve — метка realised, а не дополнительный доход.
Граница/оставшаяся проверка: No full FinalClose authority implemented

## F11 — Final threshold=minProfit+execBuffer+tolerance
Статус: VERIFIED_CONDITIONAL_MATHEMATICS
Источник: Include/Money/HSBI_MoneyTypes.mqh:7; норматив: Docs/12:7
Порог minProfit+executionBuffer+tolerance — сумма в одной валюте. Сам размер и применимость порога требуют owner policy.
Граница/оставшаяся проверка: Threshold.valid/coverage/lifecycle notestablishedbyalgebra

## F12 — Committed sumGrants=EligibleNet
Статус: CONTRADICTORY_CONTRACT_OR_SOURCE
Источник: Include/Money/HSBI_AllocationLedgerTypes.mqh:7; норматив: Docs/08:12 vs Docs/32:3
См. индивидуальную проблему/границу ниже; численные совпадения не являются доказательством.
Граница/оставшаяся проверка: PREPARED/COMMITTED needsapprovedschema

## F13 — Grant=Consumed+Reserved+Free
Статус: VERIFIED_CONDITIONAL_MATHEMATICS
Источник: No production completebalance API; норматив: R0F D01 proposal
При grants без внешних transfer сохранение G=C+R+F задаёт точный partition. Переход consume d: C+=d,F-=d сохраняет сумму; 0<d<=F необходимо.
Граница/оставшаяся проверка: Abstractmodel only; approval pending

## F14 — RemainingGross=Reserved+Free
Статус: VERIFIED_CONDITIONAL_MATHEMATICS
Источник: No production representation; норматив: R0F BALANCE mapping proposal
RemainingGross=G-C=R+F алгебраически следует из G=C+R+F. Legacy Remaining нельзя считать Free без доказанной схемы.
Граница/оставшаяся проверка: Legacy Remaining ambiguous; not actual migration

## F15 — 0<Amount<=Free; C+=Amount,F-=Amount
Статус: UNVERIFIED
Источник: Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:63; норматив: D07 proposal
См. индивидуальную проблему/границу ниже; численные совпадения не являются доказательством.
Граница/оставшаяся проверка: Full consume API/backend absent

## F16 — Immutable allocation vector != equal total
Статус: CONTRADICTORY_CONTRACT_OR_SOURCE
Источник: Include/Money/HSBI_AllocationLedgerTypes.mqh:8; норматив: Docs/08:15
См. индивидуальную проблему/границу ниже; численные совпадения не являются доказательством.
Граница/оставшаяся проверка: Currentclassifier returnsidentical

## F17 — Immutable components independent of net equality
Статус: CONTRADICTORY_CONTRACT_OR_SOURCE
Источник: Include/Money/HSBI_EconomicLedgerTypes.mqh:9; норматив: Docs/08:6,15
См. индивидуальную проблему/границу ниже; численные совпадения не являются доказательством.
Граница/оставшаяся проверка: Currentvalidator lacksfullimmutablebody

## F18 — sum source funding across allocations <=eligible source
Статус: UNVERIFIED
Источник: No global source allocationregistry; норматив: R0F FUNDING proposal
См. индивидуальную проблему/границу ниже; численные совпадения не являются доказательством.
Граница/оставшаяся проверка: Toy guard not production global conservation

## F19 — Source/bucket consumption bound to remaining grant
Статус: CONTRADICTORY_CONTRACT_OR_SOURCE
Источник: Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:47; норматив: Docs/08:15,24
См. индивидуальную проблему/границу ниже; численные совпадения не являются доказательством.
Граница/оставшаяся проверка: Permission only, no actual ledger update

## F20 — AbsoluteFarLoss=max(0,-CloseNowFarNet)
Статус: VERIFIED_CONDITIONAL_MATHEMATICS
Источник: Include/Money/HSBI_BasketMoneyEvaluator.mqh:17; норматив: D04 proposal
Loss=max(0,-net) равен0 при net>=0 и -net при net<0; только в указанном absolute close-now basis.
Граница/оставшаяся проверка: Executable quote not actual futurefill

## F21 — IncrementalLoss=AbsoluteLoss-BaselineLoss
Статус: CONTRADICTORY_CONTRACT_OR_SOURCE
Источник: Include/Money/HSBI_BasketMoneyEvaluator.mqh:17; норматив: Docs/04:15 naming vs D04
См. индивидуальную проблему/границу ниже; численные совпадения не являются доказательством.
Граница/оставшаяся проверка: Metric/baseline choice unresolved; code namedincreasecomputesabsolute

## F22 — CatchUpMargin=Reserve-Loss-Buffer>0
Статус: VERIFIED_CONDITIONAL_MATHEMATICS
Источник: Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:74; норматив: Docs/24:9
При известных independent Reserve,L,B coverage со строгим запасом эквивалентно R-L-B>0. Никаких гарантий fill/margin.
Граница/оставшаяся проверка: Requires eligible independent reserve

## F23 — all-level minMargin>0 vs maxTransitionLoss level
Статус: CONTRADICTORY_CONTRACT_OR_SOURCE
Источник: Include/Planning/HSBI_FutureSmallProofAggregator.mqh:50; норматив: proposedCR09 vs Docs/30:5
См. индивидуальную проблему/границу ниже; численные совпадения не являются доказательством.
Граница/оставшаяся проверка: Proposed semantics, not automatically approved replacement

## F24 — TransitionLoss=max(0,-sum signedfills)
Статус: VERIFIED_CONDITIONAL_MATHEMATICS
Источник: No actual fillbatch accumulator; норматив: Docs/13:9
Loss=max(0,-sum signed fills) определяет текущую signed-loss политику. Это не peak/sticky. Fills обязаны принадлежать одному batch.
Граница/оставшаяся проверка: Current signed policy only

## F25 — Sticky breach and peak loss differ from current loss
Статус: UNVERIFIED
Источник: No chosen newpolicy; норматив: D05 awaiting
См. индивидуальную проблему/границу ниже; численные совпадения не являются доказательством.
Граница/оставшаяся проверка: A/B/C no automaticchoice

## F26 — AllowedLoss=min(absolute,equity,oldrisk,cumulative caps)
Статус: VERIFIED_CONDITIONAL_MATHEMATICS
Источник: Include/Risk/HSBI_NewFarGateTypes.mqh:12; норматив: Docs/15:15
Если каждый из четырёх finite caps верхняя граница одной loss, одновременное выполнение loss<=каждый cap эквивалентно loss<=min(caps). Разные risk basis недопустимы.
Граница/оставшаяся проверка: Need knownfiniteinput and actual equity basis

## F27 — compressionLots=F-N; ratio=(F-N)/F
Статус: VERIFIED_CONDITIONAL_MATHEMATICS
Источник: Include/Planning/HSBI_NewFarSolver.mqh:111; норматив: Docs/04:21
При F>0,N>=0 compressionLots=F-N, compressionRatio=(F-N)/F. Строгое уменьшение требует N<F.
Граница/оставшаяся проверка: F>0 afterrounding mandatory

## F28 — N<=maxRatio*F
Статус: VERIFIED_CONDITIONAL_MATHEMATICS
Источник: Include/Planning/HSBI_NewFarSolver.mqh:112; норматив: Docs/14:13
При r in(0,1), F>0 условие N<=rF даёт F-N>0; цена/lot rounding могут нарушить реализуемость.
Граница/оставшаяся проверка: No actual role promotion from projection

## F29 — NextBigGross<OldBigGross
Статус: CONTRADICTORY_CONTRACT_OR_SOURCE
Источник: Include/Planning/HSBI_FutureSmallSolver.mqh:90; норматив: Docs/04:21
См. индивидуальную проблему/границу ниже; численные совпадения не являются доказательством.
Граница/оставшаяся проверка: UnitTestlevel valid; productionselection notexecuted

## F30 — Gross=sum absLots; Net=sum signedLots
Статус: VERIFIED_CONDITIONAL_MATHEMATICS
Источник: Include/Money/HSBI_BasketMoneyEvaluator.mqh:17; норматив: Docs/01 dimensions
Gross=sum abs(signed lots); Net=sum signed lots; triangle inequality abs(Net)<=Gross. Уменьшение absNet не влечёт уменьшения Gross.
Граница/оставшаяся проверка: Direction/sign/brokeraccountsemantics required

## F31 — RiskNext<RiskOld-Tolerance
Статус: UNVERIFIED
Источник: Include/Risk/HSBI_FutureSmallRiskEvaluator.mqh:46; норматив: Docs/15:12
См. индивидуальную проблему/границу ниже; численные совпадения не являются доказательством.
Граница/оставшаяся проверка: Inequality elementary; actual risk model/identity missing

## F32 — sum standalone leg margins as account requiredmargin
Статус: UNVERIFIED
Источник: Include/Money/HSBI_BasketMoneyEvaluator.mqh:17; норматив: Docs/15:9
См. индивидуальную проблему/границу ниже; численные совпадения не являются доказательством.
Граница/оставшаяся проверка: Stubmargin not brokerproof

## F33 — marginLevel=100*Equity/Margin
Статус: UNVERIFIED
Источник: RiskInput only, no accountcalculator; норматив: Docs/15 configurablelimits
См. индивидуальную проблему/границу ниже; численные совпадения не являются доказательством.
Граница/оставшаяся проверка: ZeroMargin/netting/broker stopout details unresolved

## F34 — Equity=Balance+Unrealized
Статус: VERIFIED_CONDITIONAL_MATHEMATICS
Источник: No account provider; норматив: account identity
Equity=Balance+floating net при фиксированном broker accounting boundary. Реальные free margin/stopout formulas здесь не выводятся.
Граница/оставшаяся проверка: Analyticalfixture; broker accruedcharges requireprovider

## F35 — CyclePnL=Allrealized+Floating-futureexitcost
Статус: VERIFIED_CONDITIONAL_MATHEMATICS
Источник: No fullaccount/cycle accountingbackend; норматив: Full economic audit identity
CyclePnL=realized net+closeNow net открытых legs включая их exit costs. Все части учитываются по одному разу; Reserve второй раз не прибавляется.
Граница/оставшаяся проверка: Initialexcluded recoverymetric isnot totalaccountPnL

## F36 — unknown/nonfinite risk/outcome cannotPASS
Статус: CONTRADICTORY_CONTRACT_OR_SOURCE
Источник: Include/Risk/HSBI_RiskGateResult.mqh:6; норматив: Docs/15:6; Docs/07:21
См. индивидуальную проблему/границу ниже; численные совпадения не являются доказательством.
Граница/оставшаяся проверка: C++ IEEE adapter; nativeMQLNOT_RUN

## F37 — K=ceil(log(Vmin/F0)/log(q))
Статус: VERIFIED_CONDITIONAL_MATHEMATICS
Источник: Include/Planning/HSBI_FutureSmallSolver.mqh:9; норматив: Docs/04:36
Если Fk<=q^k F0 при каждом переходе, F0>=Vmin>0,0<q<1, то k>=log(Vmin/F0)/log(q) достаточно для Fk<=Vmin. Ceil — первый целый bound; Fk<=Vmin не равно Fk=0.
Граница/оставшаяся проверка: Uniformq afterrounding assumed; notwallclockbound

## F38 — finiteprefix implies global geometric tail
Статус: UNVERIFIED
Источник: Include/Planning/HSBI_FutureSmallSolver.mqh:146; норматив: Docs/27 conservativebound
См. индивидуальную проблему/границу ниже; численные совпадения не являются доказательством.
Граница/оставшаяся проверка: Finiteprefix cannotproveuniversalmodel

## F39 — RecoveryMoney(P+tick)>RecoveryMoney(P) overrange
Статус: UNVERIFIED
Источник: Include/Planning/HSBI_GeometrySolver.mqh:12; норматив: Docs/05:22
См. индивидуальную проблему/границу ниже; численные совпадения не являются доказательством.
Граница/оставшаяся проверка: Helper compares2values, no complete sweep wired

## F40 — PartialClose=floor(Budget/lossPerLot); actual recheck
Статус: UNVERIFIED
Источник: Include/Scenarios/HSBI_PartialFarTypes.mqh:4; норматив: Docs/11:7
См. индивидуальную проблему/границу ниже; численные совпадения не являются доказательством.
Граница/оставшаяся проверка: Only DTO; actualmulti-fillcost/recovery absent

## F41 — checked int64 settled arithmetic
Статус: UNVERIFIED
Источник: ProductionMoneyStateusesdouble; норматив: MQL-DOMAIN proposal
См. индивидуальную проблему/границу ниже; численные совпадения не являются доказательством.
Граница/оставшаяся проверка: No approved settled representation/nativecodec

## F42 — F64Z rawbits/zero + T17 scientific17
Статус: UNVERIFIED
Источник: Tests/Reference/hsbi_02b_r0h_identity_codec.py; норматив: R0H codecreferenceprofile
См. индивидуальную проблему/границу ниже; численные совпадения не являются доказательством.
Граница/оставшаяся проверка: Reference148PASS only; MQLNOT_RUN

## F43 — small spends near1e28 retain exact decrement
Статус: UNVERIFIED
Источник: moneyfieldsdouble/no actualconsumebackend; норматив: R0D exact proposal
См. индивидуальную проблему/границу ниже; численные совпадения не являются доказательством.
Граница/оставшаяся проверка: ExactFraction does not prove nativeMQL settlement

## F44 — round(price/tick)*tick
Статус: VERIFIED_CONDITIONAL_MATHEMATICS
Источник: Include/Planning/HSBI_BrokerGrid.mqh:13; норматив: Docs/05:16
В точной арифметике tick*round(price/tick) лежит на origin0 grid и имеет error<=tick/2 при заданном tie rule. Binary64 и иные origin требуют отдельной проверки.
Граница/оставшаяся проверка: Bounds/side/freshness revalidation required

## F45 — Level=FarReference±(Start+(k-1)*Step)*Point
Статус: VERIFIED_CONDITIONAL_MATHEMATICS
Источник: GeometrySnapshotfields only; норматив: Docs/05:19
При явно заданных start/step в points и point в price/point, reference±(start+(k-1)step)*point имеет размерность price. Не подтверждает факт исполнения уровня.
Граница/оставшаяся проверка: Algebra verified, full trigger/planner absent

## F46 — BUYcloseBid/SELLcloseAsk
Статус: VERIFIED_CONDITIONAL_MATHEMATICS
Источник: Include/Money/HSBI_BasketMoneyEvaluator.mqh:9; норматив: Docs/03:9
Market BUY ликвидируется продажей по Bid, SELL покупкой по Ask при данной модели quotes; slippage, fees и availability дополнительные факты.
Граница/оставшаяся проверка: Brokerfill/slippage stillunknown

## F47 — Candidate objective minN vsrisk-first
Статус: CONTRADICTORY_CONTRACT_OR_SOURCE
Источник: Include/Planning/HSBI_NewFarCandidate.mqh:35; норматив: Docs/14:22 vs Docs/29:3
См. индивидуальную проблему/границу ниже; численные совпадения не являются доказательством.
Граница/оставшаяся проверка: Requiresprecedence/approvedpolicy

## F48 — Grid origin0 vs min+n*step
Статус: UNVERIFIED
Источник: Include/Planning/HSBI_BrokerGrid.mqh:24; норматив: Docs/04:9 vs Docs/14:9
См. индивидуальную проблему/границу ниже; численные совпадения не являются доказательством.
Граница/оставшаяся проверка: Brokerorigin contract mustbepinned; no universalassumption

## F49 — round(sum components) vs sum(round components)
Статус: UNVERIFIED
Источник: No independently verified brokerposted policy; норматив: NUM precision policyawaiting
См. индивидуальную проблему/границу ниже; численные совпадения не являются доказательством.
Граница/оставшаяся проверка: Decimal illustrativepolicy not brokerfact

### Catch-Up и конечность
Обязательные уровни exact proof представлены provenDepth (2..128), но CR-09 ALL_LEVEL vs SINGLE_LEVEL остаётся owner choice. Проверка all-level: min_i(R_i-L_i-B_i)>0 нужна для одновременного proof, но недостаточна для fills/margin/slippage. Это альтернативные сценарии: один reserve можно оценивать на каждом уровне отдельно; последовательные реальные расходы обязаны уменьшать его. Пример R50, два consumption30 оставляет -10 и должен отвергаться. При partial Far нужен новый actual residual и basis, а не механический старый loss.

Логарифмическая оценка шагов требует uniform q каждого будущего перехода, допустимого broker grid и выполнения всех действий. В ненулевом min lot остаётся экономическая позиция. Бесконечно растущая цена при незащищённом SELL не даёт безусловной конечной границы убытка. Нужны явные ограничения цены/gap, гарантии ликвидности/exit/slippage/маржи или полностью оценённый hedge; stopout сам по себе не математическая гарантия общей суммы.

Не завершены: native численные домены/codecs, all-domain bounded rounding, broker margin/netting formulas, actual cost/window overlap, весь event-level FSM и full integration. Поэтому PARTIAL.
