# Математические формулы, единицы и ограничения

BASE_SHA=4185b84f7a6a8847f6a9c5796f07113907be447d

Режим READ-ONLY ANALYSIS + AUDIT/TEST-ONLY. Источники не изменены. **AUDIT_COMPLETENESS=PARTIAL.** Native MQL5/MT5/broker/durable execution NOT_RUN. Proposed R0A–R0H не становятся нормативом из-за тестовых PASS. Все административные разрешения остаются NO.

Выделено49 semantic families: **24 VERIFIED при указанных предпосылках**, **11 CONTRADICTORY**, **14 UNVERIFIED**. Отдельно137 lexical source-expression sites (включают string/time/ID arithmetic), не137 независимых финансовых формул. Полная атомарная декомпозиция каждого site не завершена — одно из оснований PARTIAL. Native verified=0.

| FormulaID / expression | Units/domain | Normative / code locator | Status / vector | Evidence / limit |
|---|---|---|---|---|
| F01 Core floor(F*Rc) | lot; finite positive/grid | Docs/04:9; Include/Planning/HSBI_BrokerGrid.mqh:26 | VERIFIED; F.1 Rc2.56 step.01 ->.25 | LOT_FLOOR_CEIL; Algebra/local rounding only; mandatory minimum checked separately |
| F02 Trend floor(F*Rt),Rt>=0 | lot | Docs/04:9; Include/Money/HSBI_BasketMoneyEvaluator.mqh:15 | CONTRADICTORY; geometry acceptsT0, moneyrequires positivevolume | TREND_ZERO_BASKET_ACCEPTED; Inactive-leg integration inconsistency |
| F03 Small ceil(F*Rs) | lot | Docs/04:9; Include/Planning/HSBI_BrokerGrid.mqh:27 | VERIFIED; .256/.01 ->.26 | LOT_FLOOR_CEIL; Post-round risk/margin still needed |
| F04 All active legs min<=V<=max/grid | lot | Docs/04:9; Include/Planning/HSBI_GeometrySolver.mqh:32 | CONTRADICTORY; Core0 orCore.01<min.05 accepted | ZERO_CORE_MINLOT; No real orders |
| F05 Bnet=C+T-S; slope=Bnet-F | lot | Docs/04:12; Include/Planning/HSBI_GeometrySolver.mqh:10 | VERIFIED; C1.2 T1 S.5 F1 ->slope.7 | SCENARIO-UP; Necessary local sensitivity, not profitability |
| F06 reserveShare*Bnet>F | dimensionless*lot | Docs/04:15; Include/Money/HSBI_CatchUpModel.mqh:12 | VERIFIED; .9*3>1 | RESERVE_POSITIVE; Only necessary symmetric linear filter |
| F07 ActualDealNet=P+Swap+C+Fee | account currency signed | Docs/08:6; Include/Money/HSBI_CostModel.mqh:13 | VERIFIED; 60-2-7-1=50; -10-2-7-1=-20 | ACTUAL_SIGNED_NET; Actual broker receipt authenticity notproved |
| F08 ProjectedNet=gross+swap+comm+fee-spread-slip-buffer | money | Docs/24:7; Include/Money/HSBI_CostModel.mqh:18 | VERIFIED; 60-2-7-1-1-2-3=44 | PROJECTED_SIGNED_NET; Only disjoint cost basis; overlap F09 |
| F09 No repeated cost coverage | costID/basis/window | D06 awaiting; Include/Money/HSBI_CostModel.mqh:4 | UNVERIFIED; Bid/AskPL9 minus same spread1 =>8 | COST-OVERLAP; Missing basis/policy; conditional counterexample |
| F10 RecoveryPL=RealizedCycleNet+OpenCloseNowNet | money | Docs/04:18; Include/Money/HSBI_MoneyTypes.mqh:9 | VERIFIED; 500-450=50 | FINAL-50-16; No full FinalClose authority implemented |
| F11 Final threshold=minProfit+execBuffer+tolerance | money allnonnegative | Docs/12:7; Include/Money/HSBI_MoneyTypes.mqh:7 | VERIFIED; 10+5+1=16,50>=16 | FINAL-50-16; Threshold.valid/coverage/lifecycle notestablishedbyalgebra |
| F12 Committed sumGrants=EligibleNet | settled money | Docs/08:12 vs Docs/32:3; Include/Money/HSBI_AllocationLedgerTypes.mqh:7 | CONTRADICTORY; Committed10of50 passesinequality | ALLOC_COMMITTED_UNALLOCATED; PREPARED/COMMITTED needsapprovedschema |
| F13 Grant=Consumed+Reserved+Free | settled money nonnegative | R0F D01 proposal; No production completebalance API | VERIFIED; 50=10+15+25 | PROPERTY-CONSERVATION; Abstractmodel only; approval pending |
| F14 RemainingGross=Reserved+Free | settled money | R0F BALANCE mapping proposal; No production representation | VERIFIED; 40=15+25 | PROPERTY-CONSERVATION; Legacy Remaining ambiguous; not actual migration |
| F15 0<Amount<=Free; C+=Amount,F-=Amount | money/owner | D07 proposal; Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:63 | UNVERIFIED; 50 grant40spent10free cannot spend11 | PROPERTY-AFFORDABILITY; Full consume API/backend absent |
| F16 Immutable allocation vector != equal total | money per bucket | Docs/08:15; Include/Money/HSBI_AllocationLedgerTypes.mqh:8 | CONTRADICTORY; 50/0 vs0/50 same total | L02_VECTOR_CONFLICT; Currentclassifier returnsidentical |
| F17 Immutable components independent of net equality | raw signed money | Docs/08:6,15; Include/Money/HSBI_EconomicLedgerTypes.mqh:9 | CONTRADICTORY; P50 C0 vsP60 C-10 Net50 | L01_COMPONENT_CONFLICT; Currentvalidator lacksfullimmutablebody |
| F18 sum source funding across allocations <=eligible source | account/source money | R0F FUNDING proposal; No global source allocationregistry | UNVERIFIED; two allocations50 each same source50 =>100 | PROPERTY-DOUBLE_FUNDING; Toy guard not production global conservation |
| F19 Source/bucket consumption bound to remaining grant | money identity/state | Docs/08:15,24; Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:47 | CONTRADICTORY; spent50reserve0 can regain45 viaflagfalse | RESERVE_SPENT_SOURCE_REJECT; Permission only, no actual ledger update |
| F20 AbsoluteFarLoss=max(0,-CloseNowFarNet) | money | D04 proposal; Include/Money/HSBI_BasketMoneyEvaluator.mqh:17 | VERIFIED; net-50 ->loss50 | FAR-ABSOLUTE; Executable quote not actual futurefill |
| F21 IncrementalLoss=AbsoluteLoss-BaselineLoss | money/stablebasis | Docs/04:15 naming vs D04; Include/Money/HSBI_BasketMoneyEvaluator.mqh:17 | CONTRADICTORY; Abs50-base40=10,Reserve30 failsabs butpassesdelta | FAR-ABSOLUTE; Metric/baseline choice unresolved; code namedincreasecomputesabsolute |
| F22 CatchUpMargin=Reserve-Loss-Buffer>0 | money | Docs/24:9; Include/Money/HSBI_ReserveCatchUpEvaluator.mqh:74 | VERIFIED; 50-20-1=29,50-50=0 rejected | CATCHUP_ZERO_MARGIN_REJECT; Requires eligible independent reserve |
| F23 all-level minMargin>0 vs maxTransitionLoss level | money/index | proposedCR09 vs Docs/30:5; Include/Planning/HSBI_FutureSmallProofAggregator.mqh:50 | CONTRADICTORY; Trans10 margin9 vsTrans5 margin-11 | CR09-EXTREMA; Proposed semantics, not automatically approved replacement |
| F24 TransitionLoss=max(0,-sum signedfills) | money | Docs/13:9; No actual fillbatch accumulator | VERIFIED; [-15,+100] finalNet85 loss0 | TRANSITION-ABC; Current signed policy only |
| F25 Sticky breach and peak loss differ from current loss | money/time/policy | D05 awaiting; No chosen newpolicy | UNVERIFIED; [-15,+100] cap12 =>peak15,stickytrue,current0 | TRANSITION-ABC; A/B/C no automaticchoice |
| F26 AllowedLoss=min(absolute,equity,oldrisk,cumulative caps) | money | Docs/15:15; Include/Risk/HSBI_NewFarGateTypes.mqh:12 | VERIFIED; min(20,15,12,18)=12 | CAP-MIN; Need knownfiniteinput and actual equity basis |
| F27 compressionLots=F-N; ratio=(F-N)/F | lot/ratio | Docs/04:21; Include/Planning/HSBI_NewFarSolver.mqh:111 | VERIFIED; F1,N.6 ->.4lots/.4ratio | COMPRESSION; F>0 afterrounding mandatory |
| F28 N<=maxRatio*F | lot | Docs/14:13; Include/Planning/HSBI_NewFarSolver.mqh:112 | VERIFIED; .6<=.8*1 | COMPRESSION; No actual role promotion from projection |
| F29 NextBigGross<OldBigGross | lot | Docs/04:21; Include/Planning/HSBI_FutureSmallSolver.mqh:90 | CONTRADICTORY; nextGross1.2/net.2 vspriorGross1 | FS_BIG_GROSS_GROWTH_REJECT; UnitTestlevel valid; productionselection notexecuted |
| F30 Gross=sum absLots; Net=sum signedLots | lot | Docs/01 dimensions; Include/Money/HSBI_BasketMoneyEvaluator.mqh:17 | VERIFIED; buy2.2 sell1.5 =>gross3.7/net.7 | SCENARIO-UP; Direction/sign/brokeraccountsemantics required |
| F31 RiskNext<RiskOld-Tolerance | money | Docs/15:12; Include/Risk/HSBI_FutureSmallRiskEvaluator.mqh:46 | UNVERIFIED; 10<20-1 butruntimeRiskSource notimplemented | NF_GATE_POSITIVE; Inequality elementary; actual risk model/identity missing |
| F32 sum standalone leg margins as account requiredmargin | money | Docs/15:9; Include/Money/HSBI_BasketMoneyEvaluator.mqh:17 | UNVERIFIED; Hedged/netting/tiermargin maydiffer | SCENARIO-LOW_MARGIN; Stubmargin not brokerproof |
| F33 marginLevel=100*Equity/Margin | percent | Docs/15 configurablelimits; RiskInput only, no accountcalculator | UNVERIFIED; 100*1000/100=1000% | MARGIN-LEVEL; ZeroMargin/netting/broker stopout details unresolved |
| F34 Equity=Balance+Unrealized | money excluding futureexitcost | account identity; No account provider | VERIFIED; 1003.46-5=998.46 | SCENARIO-BIG_PROFIT_SMALL_LOSS; Analyticalfixture; broker accruedcharges requireprovider |
| F35 CyclePnL=Allrealized+Floating-futureexitcost | money | Full economic audit identity; No fullaccount/cycle accountingbackend | VERIFIED; positive closed C/T/S Harvest3.83 butliquidationCycle-1.64 | SCENARIO-BIG_PROFIT_SMALL_LOSS; Initialexcluded recoverymetric isnot totalaccountPnL |
| F36 unknown/nonfinite risk/outcome cannotPASS | typed real-valued domain | Docs/15:6; Docs/07:21; Include/Risk/HSBI_RiskGateResult.mqh:6 | CONTRADICTORY; NaN>false comparisonsallfalse | RISK_NAN_REJECT; C++ IEEE adapter; nativeMQLNOT_RUN |
| F37 K=ceil(log(Vmin/F0)/log(q)) | dimensionless steps | Docs/04:36; Include/Planning/HSBI_FutureSmallSolver.mqh:9 | VERIFIED; F01,Vmin.01,q.8 ->K21 | DEPTH-CONDITIONAL; Uniformq afterrounding assumed; notwallclockbound |
| F38 finiteprefix implies global geometric tail | quantifier over future levels | Docs/27 conservativebound; Include/Planning/HSBI_FutureSmallSolver.mqh:146 | UNVERIFIED; .8,.64 thenplateau.64 breaksq^3 | BOUND_FINITE_PREFIX_NOT_GLOBAL_PROOF; Finiteprefix cannotproveuniversalmodel |
| F39 RecoveryMoney(P+tick)>RecoveryMoney(P) overrange | money/price | Docs/05:22; Include/Planning/HSBI_GeometrySolver.mqh:12 | UNVERIFIED; onelevelimprovement notallvalidticks/gaps | RANGE-MONOTONICITY; Helper compares2values, no complete sweep wired |
| F40 PartialClose=floor(Budget/lossPerLot); actual recheck | lot | Docs/11:7; Include/Scenarios/HSBI_PartialFarTypes.mqh:4 | UNVERIFIED; B5,loss20,step.1 ->.2lot costs4<=5 | PARTIAL-FLOOR; Only DTO; actualmulti-fillcost/recovery absent |
| F41 checked int64 settled arithmetic | minor money units | MQL-DOMAIN proposal; ProductionMoneyStateusesdouble | UNVERIFIED; 2^63-1+1 unsupported; not Pythonintdomain | INT64-OVERFLOW; No approved settled representation/nativecodec |
| F42 F64Z rawbits/zero + T17 scientific17 | raw64bytes/not moneyrounding | R0H codecreferenceprofile; Tests/Reference/hsbi_02b_r0h_identity_codec.py | VERIFIED; literal independentvectors minsubnormal etc | R0H_API; Reference148PASS only; MQLNOT_RUN |
| F43 small spends near1e28 retain exact decrement | money domain | R0D exact proposal; moneyfieldsdouble/no actualconsumebackend | UNVERIFIED; binary64(1e28)-.01 == binary64(1e28) | MONEY-RESOLUTION; ExactFraction does not prove nativeMQL settlement |
| F44 round(price/tick)*tick | price | Docs/05:16; Include/Planning/HSBI_BrokerGrid.mqh:13 | VERIFIED; tick.25 price100.12 ->100.0 | PRICE-GRID; Bounds/side/freshness revalidation required |
| F45 Level=FarReference±(Start+(k-1)*Step)*Point | price/points | Docs/05:19; GeometrySnapshotfields only | VERIFIED; 100+(10+2*5)*.01=100.2 | LEVEL-DISTANCE; Algebra verified, full trigger/planner absent |
| F46 BUYcloseBid/SELLcloseAsk | price side | Docs/03:9; Include/Money/HSBI_BasketMoneyEvaluator.mqh:9 | VERIFIED; bid100ask101 ->buy100/sell101 | BASKET_STUB_POSITIVE_VALID; Brokerfill/slippage stillunknown |
| F47 Candidate objective minN vsrisk-first | ordered tuple | Docs/14:22 vs Docs/29:3; Include/Planning/HSBI_NewFarCandidate.mqh:35 | CONTRADICTORY; N.2risk10 vsN.3risk5 | OBJECTIVE-NON_EQUIVALENCE; Requiresprecedence/approvedpolicy |
| F48 Grid origin0 vs min+n*step | lot/lattice | Docs/04:9 vs Docs/14:9; Include/Planning/HSBI_BrokerGrid.mqh:24 | UNVERIFIED; min.03 step.02: offset.03/.05 vsabsolute.04/.06 | GRID-ORIGIN; Brokerorigin contract mustbepinned; no universalassumption |
| F49 round(sum components) vs sum(round components) | money/minor units | NUM precision policyawaiting; No independently verified brokerposted policy | UNVERIFIED; .005+.005 digits2 halfEven =>.01 vs0 | ROUNDING-POLICY; Decimal illustrativepolicy not brokerfact |

## Что алгебра действительно доказывает

При неизменных lots и общем линейном money-per-price коэффициенте: dRecovery/dP = C+T−S−F для FarSELL и зеркального favorable движения. Строго положительная slope — локальный directional filter. Она не доказывает favourable movement, достаточность equity/margin, отсутствие gaps, независимость costs, фактическую сделку или прибыль завершённого цикла. В source slope.19 проходит даже при Core0 (FSA-011), то есть одного закона недостаточно для обязательной leg.

G=Cspent+Rreserved+Ffree, все>=0. Consuming a<=F даёт C'=C+a,F'=F-a,R'=R =>sum неизменна. Reserving r<=F даёт R'=R+r,F'=F-r; release делает обратное для того же owner. Это корректный abstract accounting invariant (15 seeded predicate families), но production имеет другую неполную MoneyState/Allocation форму и не реализует этот полный lifecycle. Cannot infer production money conservation from a correct equation.

Если для всех j существует доказанное F(j+1)<=qF(j),0<q<1, то F(k)<=q^k F0; K>=ceil(log(Vmin/F0)/logq) даёт достижение minimum-scale bound. Это условная теорема о successful transitions, не о времени, broker executions или закрытии позиции. Два первых значения .8,.64 не доказывают F3<=.512: допустимое без нового доказательства продолжение .64 нарушает bound. Source проверяет finite prefix/flags и terminal minlot, не общий tail-law/terminal-close affordability (FSA-018/028).

Если выбрать worst level по argmax TransitionLoss, это не равно argmin(Reserve−Loss−Buffer). Два допустимых уровня: (Trans10,Reserve100,Loss90,Buffer1)->margin9; (Trans5,Reserve10,Loss20,Buffer1)->margin−11. Старый control выбирает1, all-level contract должен отклонить. Варианты политики требуют административного решения CR09/D04, не самовольной смены.

`SignedNet[-15,+100]=85`, current loss0; peak cumulative loss15; cap12 был нарушен на префиксе. Sticky/peak/current final отличаются. Prefix protection не позволяет задним числом отменить actual loss; reset/order/partial-fill policy не выбраны автоматически.

Raw signed DealNet sum в CostModel корректен на finite inputs. Allocation conservation/immutable equality не вытекают из равенства Net или суммы buckets: P50/C0 иP60/C−10 одинаковы по net, но разные immutable facts; Reserve50/PF0 иReserve0/PF50 одинаковы по total, но разные цели денег. Existing source возвращает identical для обоих (FSA-001/002).

## Численная точность

Независимые spec vectors используют Fraction/integer и Decimal localcontext для маленького explicitly bounded .005+.005 примера. ROUND_HALF_EVEN здесь лишь один proposed profile: round aggregate=.01 vs sum rounded components=0.00. Это не политика реального брокера. Raw binary64 codec наблюдения не settled money; cents на1e28 неразрешимы в binary64. Python arbitrary integers/Fraction не native long MQL. Overflow/subnormal/locale/UTF8/codec ещё NOT_RUN в MetaEditor.

EXTRACTED uses actual selected source bodies with C++ adapters:54 checks,27 PASS,27 normative/integration expectation FAIL. Эти27 не27 уникальных live-exploits и не MQL runtime verdicts; scope каждого failure указан в defect register. Synthetic OrderCalcProfit линейный и margin=notional/100, не broker proof. Все20 independent spec vectors PASS; это проверка примеров/алгебры, не кода каждой production-формулы. Для14 UNVERIFIED families полного независимого runtime oracle нет; они не преобразованы в PASS.
