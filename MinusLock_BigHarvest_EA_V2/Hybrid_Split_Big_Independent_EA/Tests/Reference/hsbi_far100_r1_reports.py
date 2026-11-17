"""Build new Russian audit reports from executed research artifacts; never edits baseline files."""
from pathlib import Path
from decimal import Decimal as D
import json,re,hashlib
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'Tests/Evidence/FAR100_R1'
load=lambda n:json.loads((OUT/n).read_text())
meta=load('run_metadata.json');inv=load('documentation_inventory.json');tests=load('test_results.json')['summary'];cands=load('new_far_candidates.json');trs=load('physical_transitions.json');scenes=load('scenarios.json');base=meta['SourceCommitSHA'];utc=meta['CheckedAtUTC']
prefix=f'https://github.com/ic8812825-maker/chatgpt.com-codex/blob/{base}/MinusLock_BigHarvest_EA_V2/Hybrid_Split_Big_Independent_EA/'
def link(p,line=None):return f'[{p}{":"+str(line) if line else ""}]({prefix}{p}{"#L"+str(line) if line else ""})'
def fmt(x):
 if isinstance(x,(dict,list)):return json.dumps(x,ensure_ascii=False,separators=(',',':'))
 if x is None:return 'UNAVAILABLE'
 try:
  d=D(str(x));return format(d.normalize(),'f') if d.is_finite() else str(x)
 except Exception:return str(x)
def table(cols,rows):return '| '+' | '.join(cols)+' |\n|'+ '|'.join(['---']*len(cols))+'|\n'+''.join('| '+' | '.join(fmt(x).replace('|','/') for x in r)+' |\n' for r in rows)+'\n'
common=f'''SourceCommitSHA={base}
CheckedAtUTC={utc}
ExecutionMode=LOCAL_RESEARCH_GIT_PLUS_GITHUB_MCP_PUBLICATION
DocumentVersion=HSBI-FAR100-R1-V1
NormativeStatus=RESEARCH_AUDIT_ONLY_NOT_OWNER_APPROVAL
EvidenceClass=SYNTHETIC_MATH_ONLY; STATIC_SOURCE_REVIEW; EXECUTED_PYTHON_REFERENCE_ONLY
DocumentationAudit=UNPROVEN_NOT_PASS_EXHAUSTIVE_SEMANTICS_NOT_CERTIFIED
BrokerProof=UNAVAILABLE
NativeMQL5=NOT_RUN_METAEDITOR_NOT_FOUND
PRODUCTION_CHANGED=NO; IMPLEMENTATION_ALLOWED=NO; BROKER_DISPATCH_ALLOWED=NO; REAL_TRADING_ALLOWED=NO.

Нормативные предпосылки: сохраняются D06=A и NewFar=A/MINIMUM_SAFE_V1, исходные роли и order Small→OldFar→Trend→Core part→actual residual→promotion. CR09 не утверждён, новых owner selections/receipts нет. Старые evidence не изменены. PASS далее относится только к фактически выполненной независимой Python-проверке конкретного synthetic predicate; он не authorizes strategy/runtime.

Синтетические предпосылки: EURUSD/счёт USD, contract100000, tick0.00001, point0.00001, pip0.0001, tick value1USD/lot симметрично; lot min/step0.01,max100,origin0. Spread0.00020 уже в Bid/Ask; opening commission3.5USD/lot учтена в realized, closing3.5USD/lot, accrued swap−1USD/lot, fee0, projected slippage1tick=1USD/lot. Это НЕ сведения реального брокера. Research money использует exact Decimal и не округляет каждый posting до цента; реальный currency/posting/partial-commission profile UNAVAILABLE. QuoteDigits5 не currency digits.

R_all=Initial100−opening fees11.55=88.45USD; excluded Initial I100; RecoveryRealized_A=−11.55. Deposit100000; Balance100088.45 после openings. Исторического eligible harvest в главной fixture нет: TransitionBudget=FinalReserve=PartialFarBudget=0. StartingEquityMark99555.15 при SELL Bid1.10500/Ask1.10520. Все Position/Deal/Action IDs с MODEL — исследовательские символы, не брокерские tickets.

Основные формулы: NetLot=SELL−BUY; DealNet=Profit+Swap+signed Commission+Fee; projected net содержит только ещё не включённые costs; RecoveryPLCloseNow_A=R_all−I+ΣOpenCloseNowNet−H_in, здесь H_in0; Economic=R_all+ΣOpenCloseNowNet. Threshold=10+5+1=16. Allocations не прибавляются к результату. Slippage, реализованная в simulated fill price, второй раз не списывается.

Полные данные, exact decimals и actual command exit codes: [run metadata](../Tests/Evidence/FAR100_R1/run_metadata.json), [команды](../Tests/Evidence/FAR100_R1/commands.json), [test results](../Tests/Evidence/FAR100_R1/test_results.json). Фактические брокерские fills отсутствуют; native/broker/durable tests не запускались.

'''
refs='''\n## Точные исходные опоры и влияние на торговлю\n\n'''+ '\n'.join('- '+link(p,l) for p,l in [('Docs/04_MATHEMATICAL_MODEL_RU.md',9),('Docs/05_GEOMETRY_MODEL_RU.md',21),('Docs/08_MONEY_LEDGER_SPECIFICATION_RU.md',5),('Docs/12_FINAL_CLOSE_SPECIFICATION_RU.md',7),('Docs/13_SMALL_TRANSITION_SPECIFICATION_RU.md',12),('Docs/14_NEW_FAR_SOLVER_SPECIFICATION_RU.md',25),('Docs/15_RISK_AND_MARGIN_CONTRACT_RU.md',12),('Docs/24_BROKER_MONEY_MODEL_RU.md',5),('Docs/29_CANDIDATE_OBJECTIVE_AND_TIEBREAK_RU.md',3),('Docs/30_FUTURE_SMALL_AGGREGATE_PROOF_RU.md',5),('Reports/HSBI_03F_R2_D06_A_NORMATIVE_LOCK_RU.md',30),('Reports/HSBI_03F_R2_NEWFAR_MINIMUM_SAFE_NORMATIVE_LOCK_RU.md',30)])+'''\n\nSource blob SHA всех документов — в documentation_inventory.json, SHA25692 protected до/после — в protected_before/after.json. Конфликты source/Docs по full Core/closed Core, fixed template lineage, selective/minAll и objective не исправлены. Реальные risk/margin/provider/profile и full future proof UNAVAILABLE/UNPROVEN. Влияние: implementation, broker dispatch, real trading запрещены независимо от числа Python PASS.\n'''
def write(name,title,body):
 p=ROOT/'Reports'/('HSBI_FAR100_R1_'+name+'_RU.md');p.write_text('# '+title+'\n\n'+common+body+refs)
def four_table():
 return table(['PositionID','Role','Direction','OpenPrice','OpenVolume','ClosedVolume','ResidualVolume','Bid','Ask','GrossPnL','Swap','Commission','Fee','Slippage','NetPnL'],[[r[k] for k in ['PositionID','Role','Direction','OpenPrice','OpenVolume','ClosedVolume','ResidualVolume','Bid','Ask','GrossPnL','Swap','Commission','Fee','Slippage','NetPnL']] for r in next(s for s in scenes if s['Scenario']=='B_SMALL' and s['Direction']==-1)['Legs']])
def cand_table():
 rows=[r for r in cands if r['Direction']=='SELL' and r['Policy']=='RESEARCH_ALPHA50' and r['CandidateN'] in ['0.5','0.4','0.3','0.2','0.1','0.05','0.01']]
 return table(['N','Compression','Grid','RecoveryMoney','CatchUp','PhysicalTransitionLoss','RiskOld/Next','Next slope','Margin gross USD','FutureSmall','FinalStatus'],[[r['CandidateN'],r['Compression'],'synthetic valid',r['RecoveryMoney'],r['CatchUp'],r['TransitionLoss'],str(r['RiskOld'])+'/'+str(r['RiskNext']),r['NextGeometry'].get('RecoverySlope'),r['Margin'].get('SYN_GROSS_1_100',{}).get('MarginUsed') if isinstance(r['Margin'],dict) else 'UNAVAILABLE',r['FutureSmall'],r['FinalStatus']] for r in rows])
def physical_table():
 rs=[r for r in trs[0]['Rows'] if r['ActionID'].startswith('MODEL_CLOSE_')]
 return table(['Action','ID','Before lot','Close lot','After lot','Gross at simulated fill','Swap+commission expense','DealNet','EconomicCycleCloseNow','Mark Equity'],[[r['ActionID'],r['PositionIdentifier'],r['VolumeBefore'],r['RequestedClose'],r['VolumeAfter'],r['GrossMoney'],r['Costs'],r['DealNet'],r['CyclePnL'],r['Metrics']['EquityMark']] for r in rs])
write('FOUR_POSITION_MATH','FAR100 — Четыре позиции, направления, размеры и деньги', '''## Исходные позиции и текущий снимок

Набор пользователя исследуется как один candidate geometry: F1SELL@1.10000,C1.20BUY@1.10500,T0.60BUY@1.10500,S0.50SELL@1.10500. При ненулевом spread одинаковые BUY/SELL entry1.10500 трактуются как fills на разных synthetic ticks, не одновременно один Bid=Ask. Actual entry quote history UNAVAILABLE.
На Small-снимке Bid1.10250,Ask1.10270:

'''+four_table()+'''
ClosedVolume в этой valuation-таблице — гипотетический полный close-now каждой leg; это не утверждение actual close и не membership SmallTransition. При partial Core следующая таблица изменяет CoreClosed на C−N.

Σgross=−605;Σswap=−3.30;closing commission−11.55;slippage−3.30;FullBasketCloseNowNet=−623.15.
R_all88.45+U−623.15=Economic−534.70; D06 A исключает I100, Recovery=−634.70. Mark-to-market U=−608.30 (без ещё не оплаченных closing commission/slippage), MarkEquity99480.15. CloseNowEquity99465.30. Это два разных economic basis, не ошибка conservation.

## Нормативная геометрия и утверждённые параметры

C=floor(F Rc),T=floor(F Rt),S=ceil(F Rs). При исследовательских1.2/.6/.5 получаем C1.2,T.6,S.5,Bnet1.3,slope.3. GrossBUY1.8,GrossSELL1.5,NetLot−.3,totalGross3.3.
Утверждённые production Rc/Rt/Rs и reserveShare НЕ найдены как активная конфигурация: main EA — disabled skeleton без input-профиля. Tests/MQL5/HSBI_Skeleton_Tests.mq5:49/55 задаёт test-only share.6 и ratios2/1/.5. На F1 этот альтернативный fixture дал бы C2,T1,S.5,Bnet2.5,slope1.5,gross4.5; это не production default.
Docs23 устанавливает ranges Rc>0,Rt≥0,Rs>0, но не назначает активные числовые defaults. Поэтому параллельная **нормативная** геометрия остаётся параметрической; UNKNOWN profile не заменён демонстрационным3/1/1 из03H.

## Зеркальность

Для BUY отражаем price p→2.2−p и меняем BUY↔SELL; quote sides меняются местами: oldFar BUY1@1.10000,Core SELL1.2@1.09500,Trend SELL.6@1.09500,Small BUY.5@1.09500; Bid1.09730/Ask1.09750. PnL всех четырёх legs совпадают с SELL-таблицей; NetLot+.3. Симметрия проверена отдельно на101 market snapshots (tick cost симметричен по явной synthetic premise). Реального asymmetric broker proof это не даёт.

## Slope не гарантия

Research share.8×Bnet1.3=1.04>1, но fullCoreNet−306.60 →eligibleCore0, fullOldFarLoss275.50, disjoint buffer5 →CatchUp−280.50. Geometry проходит, money отказывает независимо от N. При test share.6 lot condition уже .78≤1. Возможность восстановления зависит от цены/fees/sources/funding/risk и FinalClose, не только положительной производной.

Status: exact four-position arithmetic PASS_REFERENCE; real broker parameters UNAVAILABLE; all-gate strategy admissibility UNPROVEN.
''')
ledgercols=['Step','ActionID','PositionIdentifier','RoleBefore','RoleAfter','VolumeBefore','RequestedClose','ActualClosed','VolumeAfter','FillStatus','DealIDs','GrossMoney','Costs','DealNet','CyclePnL','Risk','Margin','State']
ledger=''
for tr in trs:
 ledger+='\n### '+('SELL→BUY' if tr['Direction']==-1 else 'BUY→SELL')+' (N.40 diagnostic, НЕ selected)\n\n'
 ledger+=table(ledgercols,[[r[k] if k!='Margin' else 'SYN profiles in JSON; broker UNAVAILABLE' for k in ledgercols] for r in tr['Rows']])
write('SMALL_TRANSITION_LEDGER','FAR100 — Порядок закрытий и единственный остаток Core', '''## Операции и запрет подмены actual

До отправки actions нужны revalidation, immutable persisted plan, repeated fresh touch/hold/retrace/debounce, funding и four caps. Actual deals отсутствуют. Для арифметики ниже N.40 — один из специально запрошенных diagnostic candidates, а не выбранный безопасный остаток. Ни одна строка не является разрешением сделки.

Брокерские ActualClosed/DealIDs/FillStatus UNAVAILABLE. В machine ledger отдельные SimulatedClosed и MODEL_* identity; simulated completed не становится broker completed. Таблица отражает counterfactual, который был бы заблокирован уже на preflight.

'''+physical_table()+'''
FarClosed1.00;CoreClosed1.20−.40=.80;Far compression1−.4=.6. Small.5 иTrend.6 закрываются полностью. Единственный оставшийся ID MODEL_C0, BUY.4@1.10500, затем Role BIG_CORE→FAR. В зеркале тот же Core ID становится SELL.4@1.09500. Promotion no-deal не имеет commission/opening fee и не меняет money.

PhysicalClosingNet=112.25−275.50−153.30−204.40=−520.95;ResidualCoreNet−102.20;FullBasket−623.15. Physical TransitionLoss520.95≠FullBasketLoss623.15.

Conservative negative-outflow reservation275.50+153.30+204.40=633.20; positive Small112.25 не автоматически eligible Core income. С разрешённым netting minimum prefix520.95. Обе потребности выше main TransitionBudget0; FinalReserve0. Synthetic four caps1000 each дали бы cap520.95≤1000, но funding/CatchUp/source/future остаются blockers. Это демонстрирует различие cap и funding.

## Все18 checkpoint states каждого направления

'''+ledger+'''
Полные до/после Positions и все margin profiles — [physical_transitions.json](../Tests/Evidence/FAR100_R1/physical_transitions.json). Confirm rows с нулевым simulated close не новые deals; исторические original descriptors не заменяют observation. Финальный marked state контрфактический, фактический outcome всё время NOT_EXECUTED.

## Негативные события и restart

Reference barrier проверяет partial.20 из.50 →PENDING, следующий action запрещён; delayed.30 дополняет ту же Action до.50. Identical event replay→NO_OP, altered volume→CONFLICT. TIMEOUT/unknown оставляет barrier, wrong identifier/overfill/missing deal/core/twoFar/unreconciled volume блокируют continuation. Повтор ActionID не должен давать второй расход.
18 checkpoint JSON roundtrips сохраняют pending state; это **не** process crash, disk durability либо MQL5. Native/durable restart tests NOT_RUN. Requested.40 против observation.39 не допускает promotion до reconcile/replan. Нельзя открыть новую Far вместо исчезнувшего Core.

Status=PHYSICAL_ACCOUNTING_REFERENCE_VERIFIED; ACTUAL_EXECUTION_UNAVAILABLE; AUTHORIZED_TRANSITIONS0.
''')
write('NEW_FAR_CANDIDATES','FAR100 — Полный broker-grid search без искусственного безопасного N', '''## Полная область поиска

99 values N=.01,.02,…,.99 для каждого направления. Исследовательский профиль RESEARCH_ALPHA50: maxNewFarRatio.5,minCompressionLots.01,minCompressionRatio.5. Отдельный HISTORICAL_TEST_ALPHA60: .6/.2/.2 из native fixture, не production approval. Всего396 rows (99×2directions×2policies) сохранены в [полной сетке](../Tests/Evidence/FAR100_R1/new_far_candidates.json).
Grid synthetic EURUSD min/step.01,max100,origin0. Все99 на grid и0<N<1; physical possible residual≤C1.2, но actual residual и source proof UNAVAILABLE. Значения≥.51 не проходят profile50 compression; profile60 допускает до.60 по этому фильтру.

## Специально запрошенные N (SELL; BUY зеркален)

'''+cand_table()+'''
Каждая machine row содержит следующие required fields: CandidateN,Compression,BrokerGrid,RecoveryMoney,CatchUp,TransitionLoss,RiskOld/RiskNext,Margin,FutureSmall,FinalStatus и полный RejectReasons. Risk/Margin — только synthetic profiles; native broker counterpart UNAVAILABLE. Next C/T/S пересчитываются floor/floor/ceil по каждому N.
N.01→C.01,T0,S.01,Bnet0,slope−.01, geometry fail; никакое уменьшение объёма не исправляет next-cycle feasibility. N.05→C.06,T.03,S.03,slope.01, но CatchUp всё равно−280.50. N.4→next volumes.48/.24/.20, slope.12,gross1.32; контрольный stress risk120 против300, однако это не all-required proof.

## Доказательство отсутствия safe candidate на этом снимке

Для ЛЮБОГО N∈grid fullCoreCloseNowNet=−306.60, eligible=max(0,−306.60)=0. OldFar полностью1lot, его close-net−275.50. Потому M(N)=.8×0−275.50−5=−280.50<0, независимо от compression и output ranking. На этих входах нет безопасного кандидата в принятой conditional Core-only интерпретации: **NO_SAFE_NEW_FAR**. Actual current MQL solver не запускался; его observed result НЕ заявляется как NO_SAFE_CANDIDATE.
Более общая стратегия может иметь другие facts/sources/prices; impossibility не переносится на все HSBI states. До CR09 concrete obligations/eligibility/profile/source/future утверждение полной production feasibility остаётся UNPROVEN.

RecoveryMoney=−634.70 на одном снимке для всех N: перераспределение realized/open без изменения цены не создаёт восстановление. PhysicalClosingNet(N)=−623.15+255.50N;ResidualNet(N)=−255.50N; сумма неизменна. Funding в full machine ledger не подменено closing loss.

## Полный declared control range

Дополнительно рассчитаны2501 tick от Bid1.10500 до1.13000 приspread.00020, включая оба конца. В control_price_curve.json сохранены RecoveryA,Core-only CatchUp,closed-Core(.8lot) CatchUp и условный Core+Trend CatchUp. Core-only margin отрицательна во всех2501 точках; точка FinalClose result gate не становится funding authority. Этот declared finite range не заменяет неутверждённый CR09 required manifest/tail.

## Выбор и source различия

SelectedNewFar=NONE, потому что feasible set пуст, а не потому что.40 неудобен. Minimum-safe выбирал бы первый полностью qualified N, но здесь такого нет. Подстановка convenient N запрещена. Owner NewFar A не пересматривается. Source NewFarSolver108–151 допускает поисковые candidates меньше имеющегося actual residual; selectedVolume не является доказанным final residual. Equality requested/actual нужно проверять после fills независимо. Identity/refunding/future unknown не дают valid.

Status=GRID_ENUMERATION_COMPLETE_REFERENCE; CONDITIONAL_NO_SAFE_NEW_FAR; NATIVE_SOLVER_NOT_RUN.
''')
write('MULTI_TRANSITION','FAR100 — Последовательные потенциальные перевороты и точка остановки', '''## Основная последовательность обоих направлений

F0=1.00. На каждом разрешённом переходе должны заново строиться identity, executable entries, C/T/S, candidate grid, required control-price proofs, costs/funding/risk/margin и actual residual. Нельзя принять цепь1→.4→.16 автоматически.
Здесь первый переход уже не прошёл: для всех99 N moneyCatchUp−280.50 и availableTransition0; actual/source/required future отсутствуют. Поэтому **0 fully qualified transitions**, stop до первого irreversible action.

'''+table(['Начальное направление','F0','Potential1','FullyQualified','Potential2…5','Reason'],[['SELL','1','NO_SAFE_NEW_FAR',0,'NOT_REACHED; volumes/IDs UNAVAILABLE','Core-only margin−280.50; missing funding/proofs'],['BUY','1','NO_SAFE_NEW_FAR',0,'NOT_REACHED; volumes/IDs UNAVAILABLE','mirror same money']])+'''
Это не пять искусственных FAIL-переворотов и не пять заданных остатков: descendants не оцениваются без admissible predecessor. Полный machine stop proof — [multi_transition.json](../Tests/Evidence/FAR100_R1/multi_transition.json). Текущее требование пяти успешно проверенных transitions выполнить на этих inputs нельзя; условие задания допускает доказанную более раннюю остановку.

## Контрфактический один переход и возврат цены (не основная цепь)

Чтобы проверить lineage отдельно от разрешения, diagnostic N.40 оставляет original Core BUY.40@1.10500 для SELL-start. При исходном Small-снимке1.10250/1.10270 следующий tentative basket: CoreSELL.48@1.10250,TrendSELL.24@1.10250,SmallBUY.20@1.10270. Новый Far не переоткрывается и opening commission за его.40 повторно не взимается. Новые legs платят opening.92×3.5=3.22.
Возврат к прежней Far-цене Bid1.10000/Ask1.10020: FarBUY gross−200,CoreSELL+110.40,TrendSELL+55.20,SmallBUY−54;Σgross−88.40. Старый residual сохраняет accrued swap−.40; у новых positions accrued swap0 на этом отдельном snapshot; closing commission−4.62,slippage−1.32 →U_close−94.74. Realized после conditional первого close и новых opens=88.45−520.95−3.22=−435.72; Economic−530.46,RecoveryA−630.46. Price return сам по себе не ошибка направления: Far законно BUY original Core entry1.10500, но никакого profitable exit не доказано.
В зеркальном BUY-start FarSELL.40@1.09500, следующие roles opposite; R/U совпадают при отражённом quote. Это synthetic counterfactual из [scenarios.json](../Tests/Evidence/FAR100_R1/scenarios.json), **не** второй пройденный solver cycle.

## Колебания, конечность и terminal

Для сетки step.01, F0=1 и каждого строго уменьшающегося положительного Far остаётся максимум99 reductions до.01: целочисленный индекс100 должен уменьшаться минимум на1. Это конечность **успешных сжатий**, не конечность времени, recovery или численности retry/events. На F=.01 нет grid N с0<N<.01; требуется отдельный operational terminal close, который может быть денежно недопустим.
При гарантированном q<1 можно оценить log depth, но rounding plateau обязан отвергаться. В этом эксперименте q-chain не установлена; требование strict risk/gross decrease/next basket и money может остановить намного раньше grid terminal — здесь до первого перехода.
Четыре разных утверждения: (1) conditional finite discrete compression доказана; (2) physical partial-close lineage показана для counterfactual; (3) существование допустимой следующей корзины не для всех N (.01fail); (4) profitable FinalClose после нескольких authorised reversals НЕ доказан.

Status=MULTI_TRANSITION_STOPPED_BEFORE_FIRST; FIVE_PASS_NOT_FABRICATED; CURRENT_TEMPLATE_PHYSICAL_CHAIN_UNPROVEN.
''')
write('MONEY_CONSERVATION','FAR100 — Economic/Allocation, расходы и funding', '''## Полное денежное равенство

На Small immutable snapshot fullBasket−623.15. N.40 оставляет residual−102.20, закрываемая группа−520.95. R_all до88.45, после−432.50. ДоR+U=88.45−623.15=−534.70; после−432.50−102.20=−534.70. D06 recovery дополнительно исключает Initial100:−634.70 до и после.
Opening fees11.55 уже в realized и больше не вычитаются из закрывающих net. Swap каждой части переводится accrued→realized, не начисляется повторно. Slippage1tick отражена в simulated actual fill: BUYclose=Bid−tick,SELLclose=Ask+tick. Gross_at_fill+signedSwap+signedCommission+Fee ровно DealNet; второй slippage debit запрещён. Ненулевой spread уже в close sides и не является вторым explicit expense.

MarkEquity до99480.15, после закрытий с физическим оставшимся Core.40=99467.10. Снижение13.05=4.5USD/lot×closed2.90lot (closing commission+slippage); accrued swap не новая потеря. CloseNowEquity99465.30 до/после одинаковая, потому что liquidation estimate уже включала remaining execution costs. Для equity conservation обязательно указать mark либо close-now basis, а не сравнивать разные величины.

## Funding и четыре caps

Только закрытые source facts создают eligible grants согласно approved membership; initial100 исключён, opening costs не income, unrealized Core не cash.
Для diagnostic N.4: source chronological close nets +112.25,−275.50,−153.30,−204.40. Prefix nets112.25,−163.25,−316.55,−520.95; max deficit520.95. Без разрешённого netting positive Small conservative reserve633.20. TransitionBudget0 недостаточен; four synthetic caps1000 не дают денег. Нельзя использовать projected Core income до наступления его closing action.

## Conditional CatchUp interpretations, без выбора владельца

- Core-only полный projected source: eligible0, M−280.50.
- Только закрытая Core(C−N): при Small-снимке она также отрицательна, M−280.50. В прибыльном Core-сценарии эти sources не равны.
- Уже independently confirmed allocated Free400: не умножается наshare повторно, scalar400−275.50−5=119.50>0. Это лишь conditional diagnostic: actual provider/eligible bucket/Free receipt отсутствуют, поэтому funding authority UNAVAILABLE. FinalReserve не TransitionBudget.
- Если obligation — incremental deterioration или next Far вместо full old Far, нужны собственные named scope и cost receipts. Считать F−N=.6 фактическим full Far close запрещено. CR09-SUB-04/05/06/07/08 остаются owner-only.
На сильном Big Bid1.13000 fullCore2993.40,oldFarLoss3025.50: Core-only .8×2993.40−3025.50−5=−635.78. Core+Trend даёт иной результат, но изменение eligibility нельзя утвердить аудитом.

## Allocation conservation и identity

Общий sourceGrant=C+P+T+K+Residual; lifecycle каждого bucket=Consumed+Reserved+Free. Одни и те же деньги не суммируются как grants+free. Reference receipt18.125×share.8=grant14.5,residual3.625; debit9 оставляет5.5; второй9 reject. Reservation9,commit4,release5 даётC4/R0/F10.5,total14.5. Source reimport/другой delivery не новые деньги; altered components с тем жеnet18.125 —CONFLICT.
Executed reference source registry tested replay/no-refresh/exhausted/unknown source. Это не concurrent/durable provider; native crash/concurrency NOT_RUN. Никаких actual money postings в production не создано.

Status=MONEY_CONSERVATION_PASS_REFERENCE; REAL_ALLOCATION_AUTHORITY_UNAVAILABLE.
''')
scenario_rows=[]
for s in scenes:
 m=s['Metrics'];scenario_rows.append([s['Scenario'],s['Direction'],m['RecoveryPLCloseNowA'],m['RiskControlSymmetric100pip'],m['TotalGrossExposure'],m['MarginProfiles']['SYN_GROSS_1_100']['MarginUsed'],m['EquityMark'],s.get('OrdinaryFinalCloseResultGate','PREDECESSOR_BLOCKED')])
write('RISK_MARGIN_STRESS','FAR100 — Risk, margin и девять сценариев A–I', '''## Общий adverse basis и ограничения риска

На Small-снимке GrossBUY1.8,GrossSELL1.5,netBUY.3,totalGross3.3. Для сравнения задаём два одинаковых для old/next immutable stress quotes: current Bid/Ask±0.01000 (100pip). Synthetic Risk=max(0,ValueNow−ValueAtEachStress). Исходная basketRisk300. На diagnostic N.4 новая basket имеет FarBUY.4,CSELL.48,TSELL.24,SBUY.20,totalGross1.32,netSELL.12,тот же symmetric stressRisk120. Таким образом120<300−tolerance1 на ограниченном stress basis, но это не проверка всех adverse/gap/holding сценариев и не broker RiskNext proof.
Если сравнивать лишь один adverse quote старой basket, он может быть благоприятным для новой: нельзя менять controlbasis с направлением и объявлять нулевой risk универсальным.

Уменьшение Far не гарантирует меньший account risk: до Far1 с stress100USD,после Far.4 соstress40USD плюс другая account position соstress10000USD →10040>100. Gross hedge margin тоже зависит от pairing/contract, не только net lots. Нужен независимый account-wide snapshot/ownership/foreign exposure policy. Модель не скрывает эти ограничения.

WorstCaseLoss на неограниченном рынке не доказан finite: для shortN>0 loss≈100000NΔP→∞. Ни q-compression, ни малое число позиций, ни finite stress tests/stopout не дают универсальной exit-price гарантии. ERR038 OPEN. Уровень Vmin не означает закрытый прибыльный цикл.

## Три margin profiles, каждый явно synthetic

Notional perlot=100000×mid, leverage100. Main mid1.10260. GROSS: charge(BUY+SELL)/100=3638.58; HEDGED_MAX:charge max(BUY,SELL)/100=1984.68; HEDGED20:charge[max+.2min]/100=2315.46USD. Actual broker calc mode/hedged-margin/account currency rules UNAVAILABLE.

'''+table(['Profile','MarginUsed','FreeMarginAfter','MarginLevel%'],[[k,v['MarginUsed'],v['FreeMarginAfter'],v['MarginLevel']] for k,v in next(s for s in scenes if s['Scenario']=='B_SMALL' and s['Direction']==-1)['Metrics']['MarginProfiles'].items()])+'''
Main EquityMark99480.15; CycleDD.51985% от100000,AccountDD.619230769…% отpeak100100. Величины не из net lots. Каждый candidate JSON содержит свои profiles, risk, compression и nextgeometry; поле UNAVAILABLE при невозможной geometry, а не нулевая margin.

## Девять сценариев

A сильный Big: Bid1.13000/Ask1.13020, recovery190.30≥16. OrdinaryFinalClose RESULT gate выполнен на synthetic snapshot, поэтому сначала FinalClose preview, не ненужный переворот. Funding/ownership/freshness/etc требуют независимых receipts; actual authorization UNAVAILABLE.
B Small: Bid1.10250/Ask1.10270, recovery−634.70,CatchUp−280.50,TransitionBudget0; нет первого qualified flip. Trigger repeated snapshot/hold/debounce не доказан самим price touch.
C возврат после conditional flip: originalCore становится Far с inherited entry; возврат кстарой цене не ошибка автоматически. При diagnostic N.4 new basket recovery−630.46, predecessor blocked; см.multi report.
D колебания2–5: завершено0 допускаемых transitions, descendants NOT_REACHED. Независимо заданная geometric sequence не заменяет solver. Нет утверждения profitable mean reversion.
E длинный тренд: при Bid1.20000 old netBUY basket достигает recovery2290.30 и при valid final authority должна закрываться; но при противоположном тренде или после иных exposures убыток может расти без bound. Полагаться на возврат запрещено.
F gap: Bid1.08000/Ask1.08300,stale=true. Пропущенные уровни, changed fingerprint, slippage/fill uncertainty блокируют admission до revalidation. Старый plan не используется; actual equity/fill UNAVAILABLE, synthetic mark не гарантированный exit.
G spread.00200 и closingcommission50/lot: geometry.3 не меняется, quote money/fees ухудшаются. Основные Metrics в JSON используют baseline3.5; HighCommissionNet/HighCommissionRecoveryA и Legs отражают50. Эти scopes явно различены, не подставлены в один scalar. При SELL Bid1.10500/Ask1.10700 highcommission close net−971.60,RecoveryA−983.15. Swap−3.3 иslip−3.3 сохраняются; OpeningFees остаются ранее paid11.55, не заменены новой тарифной историей.
H grids: step.01 base geometry1.2/.6/.5,slope.3;step.10 то же;step.25 C1.00,T.50,S.50,Bnet1,slope0→reject. N.01 nextbasket impossible. Terminal min requires own guarded close; positive lot compression без next geometry не проходит.
I полный FinalClose: rootthreshold Bid1.12419/Ask1.12439 даёт ровно Recovery16.00; предыдущий tick1.12418 даёт15.70<threshold. Full close всех четырёх legs приводит кactualZero только после completed fills/reconciliation, а не расчёта. Emergency loss never SUCCESSFUL_RECOVERY.

'''+table(['Scenario','Direction','RecoveryA','100pip risk','Gross lots','Gross margin','Mark equity','Final result gate only'],scenario_rows)+'''
Все сценарные prices — fixed test inputs, не реальные quotes. [scenarios.json](../Tests/Evidence/FAR100_R1/scenarios.json),[grid_boundaries.json](../Tests/Evidence/FAR100_R1/grid_boundaries.json). Asymmetric synthetic variant задаётся profit_tick1/loss_tick1.2 в reference leg; без реального payout/calculation-mode receipt она не broker EURUSD proof.

Status=RISK_MARGIN_SYNTHETIC_CALCULATED; BROKER_PROOF_UNAVAILABLE; UNBOUNDED_TAIL_UNPROVEN.
''')
class_counts={}
for r in load('test_results.json')['records']:class_counts[r['Class']]=class_counts.get(r['Class'],0)+1
write('INDEPENDENT_TESTS','FAR100 — Реально выполненные независимые проверки и ограничения', f'''## Команды и фактический outcome

Рабочий каталог команд — разрешённый PROJECT_PATH в локальном checkout веткиwork на source SHA. Запущены:

```text
python3 Tests/Reference/hsbi_far100_r1_documentation.py
exit_code=0
python3 Tests/Reference/hsbi_far100_r1_oracle.py > Tests/Evidence/FAR100_R1/oracle_stdout.txt
exit_code=0
python3 Tests/Reference/hsbi_far100_r1_tests.py > Tests/Evidence/FAR100_R1/tests_stdout.txt
exit_code=0
```

Final reference run: assertions={tests['TestsExecuted']},PASS={tests['PASS']},FAIL={tests['FAIL']};causal mutations12,KILLED12,SURVIVED0. Это1191 assertion rows, а не1191 независимых торговых сценариев. Между ранним exploratory run1176 и final1191 добавлены полноценные source inventory/admission negative controls; окончательное evidence содержит1191. Native tests0. UNPROVEN5 и NOT_RUN4 — отдельные obligations, не прибавляются кчислу executed assertions.

Documentation bytesread545,semantic exhaustiveness not certified. Python3.12.14; exact Decimal и отдельный Fraction tick-count oracle. Expected hand constants−275.50/−306.60/−153.30/+112.25,full−623.15,N.4closed−520.95/residual−102.20,opening11.55,threshold16 не генерируются из actual outputs. Fraction oracle не вызывает Decimal money functions; production modules не импортируются.

## Классы проверок

'''+table(['Class','Executed assertion rows'],sorted(class_counts.items()))+'''
VOLUME проверяет99N/rounding/grid/coarse/min;PRICE close-side/tick/pip/mirror;MONEY literal legs/Fraction101snapshots/conservation;COST opening/closing/duplicate charges;ALLOCATION source replay/Free/reservations;CATCHUP necessary-vs-money;TRANSITION staged partial/delayed/unknown;NEWFAR complete grid/actual mismatch;FUTURESMALL local2501tick monotonicity only;RISK/MARGIN synthetic boundedstress/profile distinction;FINALCLOSE equality/priority/emergency;IDENTITY fullbody/corelineage;RESTART18 metadata roundtrips;NEGATIVE malformed inputs/admission/mutations.

Зелёная reference assertion «model rejects unknown» не означает, что current MQL5 validator делает то же. Ни успешная production branch151, ни full native all-required route не запускались.

## Causal mutations (исследовательский artifact, production не мутировал)

'''+table(['Mutation','ChangedField','KillingInvariant','Outcome'],[[m['Mutation'],m['ChangedField'],m['KillingInvariant'],m['Status']] for m in load('mutation_results.json')])+'''
Base valid artifact проходит независимые volume/closing+residual/source/cash/pending инварианты. Каждая одна повреждённая field-model нарушает конкретное условие. Это фиксированная causal mutation matrix, не полный mutation coverage production.

## НЕ выполнено / НЕ доказано

Native compile,MQL5,broker OrderCalcProfit/OrderCalcMargin,настоящие crash/concurrency не запускались: MetaEditor/terminal/wine не найден в PATH/проверенных установках; read-only broker/provider отсутствует. Reference JSON restart не disk durability. Исторические67 TL/CU/03G specs по-прежнему NOT_RUN, старые7PASS/16FAIL не изменены.
Пять unproven obligations: whole-document semantic review,actual broker proof,full CR09binding,safe first SmallTransition,profitable multi-transition reachability. Результат full strategy=MATH_AUDIT_UNPROVEN, а не1191PASS торговой модели.

Protected92 SHA256 parity before/after подтверждена,656 original historical evidence hashes неизменны. Final remote diff отдельно проверяется после публикации; self-referential будущий commit hash не выдумывается.
''')
# Extract all current historical finding rows, keeping IDs/severity unchanged.
source=(ROOT/'Reports/HSBI_AUDIT03_ALL_ERRORS_RU.md').read_text();errs={}
for line in source.splitlines():
 if re.match(r'\| HSBI-A03-ERR-\d{3} \| P[012] \|',line):
  cells=[x.strip() for x in line.strip('|').split('|')];errs[cells[0]]=cells
err_rows=[[k,v[1], ' / '.join(v[2:5]),'OPEN; no production disposition here'] for k,v in sorted(errs.items())]
write('OPEN_ISSUES_AND_BLOCKERS','FAR100 — P0/P1/P2, CR09 и отсутствующие доказательства', '''## Сохранённый статус реестра

Исторический аудит содержит50 IDs: P014,P131,P25,TL001 дополнительно audit finding P1_PROPOSED без нового canonical ERR. Ни один P0 не закрыт новым reference test. ERR038OPEN,ERR018OPEN_CONTRACT_GAP,TL001CONFIRMED_STATIC/P1_PROPOSED. D06A/NewFarA сохраняются, formal receipts0. Doc03/23 исторические OPEN_P0=0 не актуальный closure этих later findings.

'''+table(['ID','Severity','Historical scope excerpt','Current audit disposition'],err_rows)+'''
Таблица сохраняет исторические severity, а не присваивает новые production errors. Full original rows/source excerpts есть в pinned Docs inventory; duplicate correction of withdrawn transitionShare hypothesis не восстанавливается как дефект. Current findings scope not exercised native.

## Критические source расхождения

'''+table(['Source','Input/formula','Expected physical/selected contract','Static source observation','Severity/status','Future correction proposal, not implemented'],[
[link('Include/Money/HSBI_BasketMoneyEvaluator.mqh',17),'F1,C1.2,T.6,S.5,N.4','closing−520.95,residual−102.20','fullbasket−623.15→loss623.15','membership gap; no new canonical ID','разделить full basket и action-closing metrics'],
[link('Include/Planning/HSBI_FutureSmallSolver.mqh',122),'FarSELL→CoreBUYresidual','next FarBUY +Core inherited open','farDirection/openprices берутся сноваизx','physical lineage UNPROVEN','state-chain DTO/edge binding'],
[link('Include/Planning/HSBI_NewFarSolver.mqh',151),'checked maxT versus selected FarA','typed T/A separate','returntransitionLoss=Far loss','TL001/P1_PROPOSED','versioned result fields,not relabellegacy'],
[link('Include/Planning/HSBI_NewFarSolver.mqh',118),'all required margins','minAll predicate before objective','one control CatchUp/candidate','ERR018contractgap','approved manifest/per-level bindings'],
[link('Include/Planning/HSBI_NewFarSolver.mqh',123),'ci.farVolume=candidate','physical full oldFar obligation1','control NetBig versus original candidate','CR09-SUB04blocked','name obligation and volume/snapshot scope'],
[link('Include/Planning/HSBI_NewFarCandidate.mqh',33),'two feasible candidates N.2/.3,risk18/12','MINIMUM_SAFE picks.2','risk-first comparator picks.3','existing normative conflict','align already selected A/versioned plans'],
[link('Include/Planning/HSBI_NewFarSolver.mqh',108),'actual residual .4,candidate .2','promotion actual residual equality independent','candidate≤actual upper does not assert final equality','ERR045OPEN','revalidate post-fill residual and actions']])+'''
Expected/current-observation в таблице — static formula reconstruction. Это не actual executed MQL outputs и не assertion об обходе существующего cap gate: cap действительно применяется до safe[]. Числа−520.95/−623.15 относятся к нашему synthetic cost profile.

## Owner-only вопросы

CR09-SUB01 all-requiredscope;02 level semantics;03 requiredIDs/terminal/tail;04 quantity/Far obligation;05 eligibility;06 preview/funding;07 prefix inventory;08 costmanifest;09 numericbound;10 authority/clock;11 legacy mapping. Все11 AWAITING. Не выбирать варианты за владельца. D06A иNewFarA не reopen.
Также нужны D01/02/03/04/05/07/08/10/11/12/13/14/15/16 approvals/receipts/profile/provider по published dependency plan. Результат review принципа не permission implementation.

## Конкретные блокирующие факторы

1. Нет утверждённого активного Rc/Rt/Rs/caps/trigger/terminal/runtime numeric profile; fixtures не defaults.
2. Нет real EURUSD/account margin/cost/asymmetrictick/history/positions/providerclock receipts.
3. Full semantic reading всех545 документов не certified; полный documentation PASS запрещён.
4. Current Small fixture mathematically fails Core-only money for everyN и funding0.
5. Physical future chain/requiredtail не доказана,currentfixedtemplate не наследует position lineage.
6. Нет native compiler/runtime/crash/concurrency evidence и independent durable funding authority.
7. Нет конечного market monetary risk theorem ERR038.

Status=OPEN_BLOCKERS_RECORDED; FULL_MATH_AUDIT_UNPROVEN; TRADING_FORBIDDEN.
''')
# Add required shared evidence headings to pre-math documentation report without rewriting its registry.
p=ROOT/'Reports/HSBI_FAR100_R1_DOCUMENTATION_AUDIT_RU.md';s=p.read_text()
if '## Итог после исследовательского запуска' not in s:
 s+='\n## Итог после исследовательского запуска (не меняет полноту первого этапа)\n\n'+common+refs;p.write_text(s)
print('generated 10 reports',len(list((ROOT/'Reports').glob('HSBI_FAR100_R1_*_RU.md'))))
owner_clear='''## 16.1. Краткий вердикт

**MATH_AUDIT_UNPROVEN.** Физическая концепция перехода математически согласована при явно заданном составе действий: полностью закрыть старую Far, Small и Trend, частично закрыть исходную BigCore и сохранить её остаток как единственную новую Far. Это сохраняет архитектуру HSBI. Но согласованность такой операции не доказывает её допустимость по всем денежным, риск, маржинальным и будущим обязательствам.

В заданном эксперименте с исходной Far1.00 первый переход не проходит Core-only Catch-Up для любого N. Никаких пяти искусственно заданных безопасных остатков нет. Не доказана также полная смысловая проверка каждого из545 исторических документов: все байты прочитаны и зарегистрированы, но это не полный semantic PASS. Реальные брокерские параметры, source receipts и native MQL5 evidence отсутствуют. Итог относится к полноте доказательства, а не утверждает невозможность всей стратегии во всех состояниях.

## 16.2. Исходные позиции и параметры

SELL-исследование: OldFar SELL1.00@1.10000; BigCore BUY1.20@1.10500; BigTrend BUY0.60@1.10500; SmallBase SELL0.50@1.10500. Эти параметры заданы пользователем как исследовательский кандидат. Утверждённые активные production Rc/Rt/Rs не найдены: ranges контрактов и числовые test fixtures не являются defaults.

Использована синтетическая EURUSD/USD-модель: contract100000, tick0.00001, tick value1USD/lot, lot min/step0.01,max100; spread0.00020; opening/closing commission по3.5USD/lot; accrued swap−1USD/lot; projected slippage1tick/lot; fee0. Exact Decimal сохраняет доли цента; реальный posting/rounding profile неизвестен. Все одинаковые entry1.10500 рассматриваются как отдельные fills на разных synthetic ticks, а не одновременная quote с нулевым spread.

BUY-зеркало получено отражением p→2.2−p и обменом Bid/Ask: FarBUY1@1.10000, Core/TrendSELL@1.09500, SmallBUY@1.09500. На Small-снимке SELL Bid1.10250/Ask1.10270, BUY Bid1.09730/Ask1.09750. Результаты ног совпадают при объявленной симметричной стоимости тика; реальная брокерская симметрия не предполагается.

## 16.3. Денежный результат до перехода

'''+four_table()+'''
В этой таблице ClosedVolume означает **гипотетическую полную оценку close-now**, а не исполненный close. Для физического перехода Core закрывается только в объёме C−N.

ΣGrossPnL=−605.00; swap−3.30; closing commission−11.55; slippage−3.30. FullBasketCloseNowNet=−623.15USD. Opening commission11.55 уже отражена в realized и не списывается повторно.

Исторический Initial100 остаётся экономическим фактом, но исключён из recovery и harvest funding по D06A. R_all=100−11.55=88.45; Economic=88.45−623.15=−534.70; Recovery_A=Economic−100=−634.70. Allocation buckets не добавляются. Balance100088.45, MarkEquity99480.15, CloseNowEquity99465.30. Mark и предполагаемая стоимость ликвидации отличаются будущими execution costs14.85.

Geometry: C1.20+T.60−S.50−F1=.30>0; Bnet1.30; GrossBUY1.80,GrossSELL1.50,NetLot−.30,totalGross3.30. Положительный slope означает локальную производную на ограниченном линейном basis, а не гарантированное восстановление.

## 16.4. Денежный результат и остатки перехода

Нормативный порядок: revalidation, immutable persisted plan, подтверждение trigger/hold/retrace/debounce, funding и four caps; затем Small full→confirm, OldFar full→confirm, Trend full→confirm, Core partial→confirm, чтение actual residual, NewFar gates, promotion, persist, reconciliation, следующий устойчивый state.

Для отдельно запрошенного diagnostic N.40 (НЕ выбранного безопасным solver):

'''+physical_table()+'''
Small закрыта.50, старая Far закрыта **1.00**, Trend закрыта.60, Core закрыта **.80**. Остаток исходного Core **.40 BUY@1.10500** сохраняет ID MODEL_C0 и получает роль FAR. Сжатие Far=.60 не является закрытым объёмом old Far. Promotion не открывает новую позицию и не платит повторную opening commission.

ClosingNet=112.25−275.50−153.30−204.40=−520.95. ResidualCoreNet=−102.20. Сумма равна FullBasket−623.15. На фиксированном снимке R+U сохраняется: после закрытий R=−432.50,U=−102.20,Economic=−534.70. MarkEquity уменьшается на13.05 оплаченных closing commission/slippage; liquidation estimate уже учитывала их заранее.

Нужное консервативное финансирование negative outflows633.20; если отдельно разрешить netting положительной Small, максимальный prefix deficit520.95. В главной fixture TransitionBudget0. Даже synthetic cap1000 не разрешает расходовать отсутствующие деньги. Вся таблица — counterfactual accounting: actual broker fills отсутствуют, действия должны быть заблокированы до начала.

## 16.5. Solver и все кандидаты

Полный machine ledger содержит396 строк: N=.01… .99, оба направления, research policy α.5/minlots.01/minratio.5 и отдельный исторический test profile α.6/.2/.2. Исторический профиль не утверждён как production. Все значения перечислены в new_far_candidates.json; ниже специально запрошенные:

'''+cand_table()+'''
Для ЛЮБОГО N на этом Small-снимке eligible Core=max(0,−306.60)=0. OldFar закрывается полностью с loss275.50, disjoint Catch-Up buffer5. Поэтому M(N)=.8×0−275.50−5=−280.50<0. Это исчерпывающее conditional доказательство отсутствия безопасного кандидата при Core-only interpretation. Даже необходимое lot condition.8×1.3=1.04>1 не спасает money condition.

SelectedNewFar=NONE; результат исследования **NO_SAFE_NEW_FAR**. Нативный MQL5 solver не запускался, поэтому его observed return не подделывается. Возможны иные approved sources/prices/contracts в других состояниях, но этого доказательства нет. CR09 concrete eligibility/obligations остаются открытыми.

Формулы для любого N: ClosingNet=−623.15+255.50N; ResidualNet=−255.50N. Общий recovery−634.70 не меняется при чистой переклассификации. N.01 дополнительно ломает следующую geometry: C.01,T0,S.01,slope−.01. Уменьшение N само по себе не даёт безопасного следующего цикла.

## 16.6. Последовательные перевороты

Для SELL-start и BUY-start выполнено **0 полностью квалифицированных переходов**. Остановка до первого irreversible action. Potential2–5 имеют статус NOT_REACHED, их Far volumes/identifiers неизвестны. Они не заменены заранее выбранными1→.4→.16→… . Доказанная ранняя остановка является результатом эксперимента.

Отдельный контрфактический diagnostic flip.40 проверяет lineage. После SELL-start новая Far — original Core BUY.40@1.10500. На исходном Small quote следующий tentative basket имел бы CoreSELL.48@1.10250, TrendSELL.24@1.10250, SmallBUY.20@1.10270. Opening commission новых ног.92×3.5=3.22; повторной opening commission за promoted Far нет.

При возврате Bid1.10000/Ask1.10020 gross новой Far−200, Core+110.40, Trend+55.20, Small−54: всего−88.40. После remaining swap−.40, closing commission−4.62 и slippage−1.32 U=−94.74. Realized после условного первого close и новых openings=−435.72; Recovery_A=−630.46. Возврат к старой цене сам по себе не ошибка направления: новая Far правильно наследует Core, но прибыльное продолжение не доказано. Этот diagnostic не превращает заблокированный predecessor в допустимый цикл.

## 16.7. Финансовая устойчивость

На ограниченном одинаковом symmetric100pip stress basis RiskOld300 и RiskNext120 для diagnostic N.40; gross exposure3.30→1.32. Это лишь условный расчёт на двух stress quotes, не полный broker/account risk proof. Уменьшение Far может сочетаться с ростом account risk при других позициях, изменении payoff, liquidity или gap assumptions.

Synthetic margin profiles на main snapshot: GROSS3638.58, HEDGED_MAX1984.68, HEDGED20 2315.46USD. Margin нельзя вывести только из net.30. CycleDD.51985% и AccountDD.619230769…% рассчитаны на явно заданных starting/peak equities. Реальный OrderCalcMargin и hedged rules отсутствуют.

Все сценарии A–I разобраны в risk report: A сильный Big достигает FinalClose result gate; B Small блокируется; C возврат учитывает inherited entry; D пять flips не пройдены; E нет надежды на обязательный возврат; F gap/stale требует нового plan; G spread/commission ухудшают money при прежней geometry; H coarse grid/terminal; I полное финальное закрытие. WorstCaseLoss на неограниченном рынке finite не доказан, ERR038 открыт. Stop-out и конечные tests не гарантируют универсальную exit price.

## 16.8. Финальное завершение

Для baseline SELL при Bid=P,Ask=P+.00020 сумма gross=30000P−33650−30. Все roundtrip fees/swap/slippage29.70 учитываются один раз. После исключения Initial:

Recovery_A(P)=30000P−33709.70.

Threshold=10+5+1=16. На Bid1.12419/Ask1.12439 recovery ровно16, на предыдущем tick1.12418 —15.70 и отказ. На Bid1.13000 recovery190.30; гипотетический full closingnet201.85 плюс предыдущийR88.45 даёт Economic290.30 и FinalBalance100290.30, открытый остаток0 после всех simulated fills.

Это проверяет result gate. Actual authorization требует также independently confirmed allowed coverage, ownership, freshness, no pending/unknown, complete costs и numeric profile; здесь они UNAVAILABLE. Если FinalClose уже допустим, стратегия не должна выполнять ненужный flip. При Small-снимке recovery−634.70 обычный result gate не проходит. Emergency может зафиксировать loss, но не маркируется SUCCESSFUL_RECOVERY.

## 16.9. Найденные ошибки и незавершённые контракты

- BasketMoneyEvaluator:17 оценивает full Core C, тогда как physical transition закрывает C−N. На наших входах full loss623.15 и physical loss520.95 — разные metrics.
- FutureSmallSolver:122–123 повторяет исходные direction/open prices вместо полной chain original Core→Far.
- NewFarSolver:118–127 проверяет один control CatchUp, не min всех required obligations: ERR018 остаётся contract gap. Существующий cap gate применяется до safe[], его обход не заявляется.
- NewFarSolver:151 возвращает Far loss в поле transitionLoss; TL001 остаётся static/P1_PROPOSED.
- NewFarCandidate:33–40 использует risk-first, тогда как уже выбранный NewFar A требует minimum-safe-first; нужен versioned alignment без повторного выбора A.
- Actual residual, immutable source body, inventory и clock authority не доказываются одним caller flag/hash.

Точные ссылки, inputs, expected и статически установленное поведение с сохранёнными severity — в open-issues report. Нативный unsafe accepted result не заявлен. Production не исправлялся.

## 16.10. Решения владельца

CR09-SUB01…11 все остаются AWAITING: required scope; level semantics; terminal/tail; quantity/Far obligation; eligibility; preview/funding; prefix inventory; cost manifest; numeric bounds; source/clock authority; legacy mapping. D06A и NewFarA сохраняются. Формальных approval receipts0, новых selections0.

Также необходимы утверждённые конкретные Rc/Rt/Rs, limits/caps, hold/retrace/terminal rules, money rounding/currency profile и реальные read-only broker/provider evidence. Исследовательские значения не выбираются владельцу автоматически. Решение принципа не даёт implementation permission.

## 16.11. Допуск следующего этапа

**MATH_AUDIT_UNPROVEN.** В ограниченном research scope проверены exact arithmetic, conservation, зеркальность, полная сетка и causal rejection. Полного доказательства торговой модели нет. Следующие prerequisites: закрыть semantic documentation coverage, согласовать owner contracts/profiles, квалифицировать read-only broker/source/cost/clock/margin providers, выполнить native components, доказать physical future state chain и durable funding/crash/concurrency.

Implementation, broker dispatch и real trading запрещены. Исторические expected/evidence не переписываются ради PASS.

## 16.12. Итоговая таблица

'''+table(['Requirement','Evidence','Calculation','Test','Status','Blocker','OwnerAction'],[
['Remote base','SHA8640bf…','совпадает','MCP+local HEAD','VERIFIED','нет','проверить отчёты'],
['Вся документация','545 byte reads','semantic coverage неполна','inventory','UNPROVEN','нужен полный смысловой обзор','разрешить конфликты'],
['Четыре ноги','Decimal/Fraction','full−623.15','1191 assertions общего набора','PASS_REFERENCE','нет broker properties','утвердить profile'],
['Физический переход','36 checkpoint rows','closed−520.95,residual−102.20','conservation/lineage','REFERENCE_ONLY','нет actual fills','уточнить binding'],
['NewFar','396 rows','M−280.50 для всехN','полная grid','NO_SAFE_NEW_FAR conditional','funding/proofs','решения CR09'],
['Пять flips','оба направления','qualified0','first-gate stop','NOT_REACHED','нет первого допустимого state','не подставлять пятьPASS'],
['Risk/margin','три profiles','bounded stress300/120','reference tests','UNAVAILABLE_BROKER','native/ERR038','дать read-only evidence'],
['FinalClose','boundary/strong Big','16 и190.30','equality/priority','RESULT_GATE_ONLY','нет coverage authority','review'],
['Production','92 hashes/history','паритет','integrity checks','UNCHANGED','implementation запрещён','не утверждалось автоматически']])
write('FINAL_OWNER_REVIEW','FAR100 — Подробный итог для проверки владельцем',owner_clear)
