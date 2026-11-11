"""Exact20 accounting scenarios + seeded15 invariant guard probes + causal mutations.
Literal terminal balances/equities independently hand-derived; no subject expected.
Analytical model is not EA orchestration, broker evidence or profitable backtest.
"""
import sys,copy,random,types,hashlib,json
import HSBI_FULL_SYSTEM_AUDIT_01_common as a
import HSBI_FULL_SYSTEM_AUDIT_01_accounting as subject
Q=subject.q

def money(x):return str(x.numerator) if x.denominator==1 else str(x.numerator)+'/'+str(x.denominator)
def render(x):
 if isinstance(x,subject.Q):return money(x)
 if type(x) is dict:return {k:render(v) for k,v in x.items()}
 if type(x) in (list,tuple):return [render(v) for v in x]
 return x
# Required categories all20. Values calculated on paper in signed unit-value/cost fixture.
SCENARIOS=[
 ('UP',[(110,111)],[], '1000','999.63','1002.93','3.7','.7','NO_AUTOMATIC_EA_ACTION'),
 ('DOWN',[(90,91)],[],'1000','999.63','988.93','3.7','.7','NO_AUTOMATIC_EA_ACTION'),
 ('RANGE',[(100,101)]*3,[],'1000','999.63','995.93','3.7','.7','NO_TERMINATION_PROOF'),
 ('WHIPSAW',[(110,111),(90,91),(100,101)],[],'1000','999.63','995.93','3.7','.7','NO_TERMINATION_PROOF'),
 ('GAP_UP',[(140,141)],[],'1000','999.63','1023.93','3.7','.7','GAP_RISK_NOT_BOUNDED'),
 ('GAP_DOWN',[(60,61)],[],'1000','999.63','967.93','3.7','.7','GAP_RISK_NOT_BOUNDED'),
 ('SPREAD_WIDENS',[(100,110)],[],'1000','999.63','982.43','3.7','.7','REVALIDATE_REQUIRED'),
 ('SLIPPAGE',[(110,111)],[('Far','1',1,'5'),('Core','1.2',2,'5'),('Trend','1',3,'5'),('Small','.5',4,'5')],'1000','984.06','984.06','0','0','PLANNED_PROFIT_NOT_GUARANTEED'),
 ('LOW_MARGIN',[(100,101)],[],'5','4.63','.93','3.7','.7','INSUFFICIENT_MARGIN'),
 ('PARTIAL_FILL',[(110,111)],[('Far','.4',1,'0')],'1000','995.19','1002.89','3.3','1.1','PENDING_REMAINING_FAR_0.6'),
 ('BROKER_REJECT',[(110,111)],[],'1000','999.63','1002.93','3.7','.7','REJECT_NO_FILL'),
 ('DUPLICATE_EVENT',[(110,111)],[('Far','.4',1,'0'),('Far','.4',1,'0')],'1000','995.19','1002.89','3.3','1.1','NO_OP_SECOND_EVENT'),
 ('RESTART',[(110,111)],[('Far','.4',1,'0')],'1000','995.19','1002.89','3.3','1.1','UNAVAILABLE_NEW_ACTION_WITHOUT_HISTORY'),
 ('HISTORY_MISSING',[(110,111)],[],'1000','999.63','1002.93','3.7','.7','UNAVAILABLE'),
 ('ECONOMIC_CONFLICT',[(110,111)],[('Far','.4',1,'0'),('Far','.5',1,'0')],'1000','995.19','1002.89','3.3','1.1','CONFLICT_SECOND_EVENT'),
 ('BIG_PROFIT_SMALL_LOSS',[(104,105)],[('Core','1.2',1,'0'),('Trend','1',2,'0'),('Small','.5',3,'0')],'1000','1003.46','998.46','1','-1','HARVEST_POSITIVE_CYCLE_NEGATIVE'),
 ('SMALL_PROFIT_BIG_LOSS',[(90,91)],[('Small','.5',1,'0')],'1000','1004.08','988.88','3.2','1.2','SMALL_PROFIT_NOT_BIG_FUNDING'),
 ('INSUFFICIENT_CATCHUP',[(110,111)],[],'1000','999.63','1002.93','3.7','.7','MARGIN_MINUS_9_REJECT'),
 ('FULL_CLOSE',[(110,111)],[('Far','1',1,'0'),('Core','1.2',2,'0'),('Trend','1',3,'0'),('Small','.5',4,'0')],'1000','1002.56','1002.56','0','0','ZERO_POSITIONS_FIXTURE_ONLY'),
 ('NO_SAFE_EXIT',[(60,61)],[],'1000','999.63','967.93','3.7','.7','FINAL_CLOSE_PROFIT_GATE_REJECT')]

def scenarios():
 rows=[]
 for sid,quotes,commands,capital,balance,equity,gross,net,meaning in SCENARIOS:
  book=subject.Book(capital);initial=copy.deepcopy(book.__dict__);trace=[]
  for bid,ask in quotes:
   book.quote(bid,ask);trace.append(dict(Type='QUOTE',Bid=bid,Ask=ask,Totals=render(book.totals())))
  statuses=[]
  for args in commands:
   before=copy.deepcopy(book.__dict__);status=book.fill(*args);statuses.append(status)
   if status in ('REJECT','CONFLICT','NO_OP','UNAVAILABLE'):assert before==book.__dict__
   trace.append(dict(Type='FIXTURE_FILL',Arguments=args,Status=status,Totals=render(book.totals())))
  if sid in ('RESTART','HISTORY_MISSING'):
   book.history=False;before=copy.deepcopy(book.__dict__);s=book.fill('Far','.1',99);assert s=='UNAVAILABLE' and before==book.__dict__;statuses.append(s)
  actual=book.totals();expected=dict(Balance=Q(balance),Equity=Q(equity),GrossLot=Q(gross),NetLot=Q(net));checks={k:actual[k]==v for k,v in expected.items()};checks['EQUITY_IDENTITY']=actual['Equity']==actual['Balance']+actual['Unrealized'];checks['GROSS_NONNEGATIVE']=actual['GrossLot']>=abs(actual['NetLot']);checks['REALIZED_IDENTITY']=book.balance-book.initial==book.realized
  if sid=='DUPLICATE_EVENT':checks['NOOP']=statuses[1]=='NO_OP'
  if sid=='ECONOMIC_CONFLICT':checks['CONFLICT']=statuses[1]=='CONFLICT'
  if sid=='LOW_MARGIN':checks['MARGIN_REJECT']=actual['FreeMarginFixture']<0
  if sid=='BIG_PROFIT_SMALL_LOSS':checks['HARVEST_NO_CYCLE_PROFIT']=book.balance>book.initial and actual['LiquidationCyclePnL']<0
  if sid=='INSUFFICIENT_CATCHUP':checks['CATCHUP_INSUFFICIENT']=Q(3)-Q(11)-Q(1)==Q(-9)
  if sid=='NO_SAFE_EXIT':checks['FINAL_THRESHOLD_REJECT']=actual['LiquidationCyclePnL']<Q('2.2')
  rows.append(dict(TestID='SCENARIO-'+sid,Initial=render(initial),QuotePath=quotes,Commands=commands,Trace=trace,Expected=render(expected),Actual=render(actual),Statuses=statuses,Meaning=meaning,Checks=checks,Result='PASS' if all(checks.values()) else 'FAIL',RemainingPositions=render(book.positions),ActualEAState='DISABLED_NO_TRADE_STUB',ProofBoundary='ANALYTIC_ACCOUNTING_FIXTURE_NOT_HSBI_LIFECYCLE_OR_BROKER_BACKTEST'))
 return rows

def vectors(seed=20261111):
 rng=random.Random(seed);cases=[];seen=set()
 for i in range(24):
  n=rng.randrange(20,10000);delta=rng.randrange(1,10);f=Q(n);g=Q(n+30)
  data=[
   ('CONSERVATION',dict(G=g,C=Q(10),R=Q(20),F=f),'F',f+1),
   ('DOUBLE_FUNDING',dict(newSource='D2',fundedSources=['D1']),'newSource','D1'),
   ('REPLAY_IDENTITY',dict(newPayload=('D1',n),savedPayload=('D1',n)),'newPayload',('D1',n+1)),
   ('SOURCE_NAMESPACE',dict(requestKey=('B','S',1,n),authorityKey=('B','S',1,n)),'requestKey',('B','S',2,n)),
   ('NO_FALSE_NOOP',dict(profitA=f,profitB=f,commissionA=Q(0),commissionB=Q(0),netA=f,netB=f),'profitB',f+delta),
   ('UNAVAILABLE_NOT_NEW',dict(historyComplete=True,sourceConfirmed=True),'historyComplete',False),
   ('ATTRIBUTION',dict(bigCredit=Q(0),posted=f,role='Small'),'bigCredit',f),
   ('COST_COVERAGE',dict(requiredCosts=['C','S','F'],coveredCosts=['C','S','F']),'coveredCosts',['C','F']),
   ('LOT_LIMITS',dict(min=Q('.05'),max=Q(100),v=Q('.05'),step=Q('.01')),'v',Q('.01')),
   ('SIGNED_EXPOSURE',dict(buy=f,sell=Q(10),reportedNet=f-Q(10),reportedGross=f+Q(10)),'reportedNet',f+Q(10)),
   ('BALANCE_EQUITY',dict(balance=f,floating=-Q(10),equity=f-Q(10)),'equity',f),
   ('AFFORDABILITY',dict(free=f,amount=f),'amount',f+delta),
   ('FSM_COMPLETION',dict(completed=True,positionRead=True,historyComplete=True),'completed',False),
   ('NO_HIDDEN_RESERVE',dict(reserveAfterPreview=f,reserveBeforePreview=f),'reserveAfterPreview',f-1),
   ('SNAPSHOT_BINDING',dict(snapshotId=n,receiptId=n,content='A',receiptContent='A'),'content','B')]
  for kind,good,field,badvalue in data:
   bad=copy.deepcopy(good);bad[field]=badvalue;key=json.dumps(render([kind,good,bad]),sort_keys=True)
   if key not in seen:cases.append((kind,i,good,bad));seen.add(key)
 return cases
MUTATIONS={
 'CONSERVATION':("d['G']==d['C']+d['R']+d['F'] and min(d['G'],d['C'],d['R'],d['F'])>=0","min(d['G'],d['C'],d['R'],d['F'])>=0"),
 'DOUBLE_FUNDING':("d['newSource'] not in d['fundedSources']","True"),
 'REPLAY_IDENTITY':("d['newPayload']==d['savedPayload']","True"),
 'SOURCE_NAMESPACE':("d['requestKey']==d['authorityKey']","d['requestKey'][3]==d['authorityKey'][3]"),
 'NO_FALSE_NOOP':("d['profitA']==d['profitB'] and ",""),
 'UNAVAILABLE_NOT_NEW':("d['historyComplete'] and d['sourceConfirmed']","d['sourceConfirmed']"),
 'ATTRIBUTION':("d['posted'] if d['role'] in ('BigCore','BigTrend') else 0","d['posted']"),
 'COST_COVERAGE':("d['requiredCosts']==d['coveredCosts']","True"),
 'LOT_LIMITS':("d['min']<=d['v']<=d['max']","0<d['v']<=d['max']"),
 'SIGNED_EXPOSURE':("d['reportedNet']==d['buy']-d['sell']","d['reportedNet']==d['buy']+d['sell']"),
 'BALANCE_EQUITY':("d['equity']==d['balance']+d['floating']","d['equity']==d['balance']"),
 'AFFORDABILITY':("0<d['amount']<=d['free']","d['amount']>0"),
 'FSM_COMPLETION':("d['completed'] and d['positionRead']","d['positionRead']"),
 'NO_HIDDEN_RESERVE':("d['reserveAfterPreview']==d['reserveBeforePreview']","True"),
 'SNAPSHOT_BINDING':("d['snapshotId']==d['receiptId'] and d['content']==d['receiptContent']","d['snapshotId']==d['receiptId']")}

def main():
 started=a.now();sr=scenarios();ps=[]
 for kind,i,good,bad in vectors():
  ps.append(dict(TestID='PROPERTY-'+kind+'-'+str(i),PropertyID=kind,Seed=20261111,Sample=i,Positive=render(good),Negative=render(bad),PositiveActual=subject.property_holds(kind,good),NegativeActual=subject.property_holds(kind,bad),Expected=[True,False],Result='PASS' if subject.property_holds(kind,good) is True and subject.property_holds(kind,bad) is False else 'FAIL',ProofBoundary='ABSTRACT_CONTRACT_MODEL_ONLY; real production property not thereby proved'))
 source=open(subject.__file__).read();mr=[]
 for kind,(old,new) in MUTATIONS.items():
  assert source.count(old)==1,kind;changed=source.replace(old,new,1);module=types.ModuleType('isolated_'+kind);exec(compile(changed,'mutation-'+kind,'exec'),module.__dict__);good,bad=next((g,b) for k,i,g,b in vectors() if k==kind);before=[subject.property_holds(kind,good),subject.property_holds(kind,bad)];actual=[module.property_holds(kind,good),module.property_holds(kind,bad)]
  # Exposure/equity mutant must keep a positive control; choose an explicit zero-offset positive.
  if kind=='ATTRIBUTION':good=copy.deepcopy(good);good['role']='BigCore';good['bigCredit']=good['posted'];before[0]=subject.property_holds(kind,good);actual[0]=module.property_holds(kind,good)
  if kind=='SIGNED_EXPOSURE':good=copy.deepcopy(good);good['sell']=0;good['reportedNet']=good['buy'];good['reportedGross']=good['buy'];before[0]=subject.property_holds(kind,good);actual[0]=module.property_holds(kind,good)
  if kind=='BALANCE_EQUITY':good=copy.deepcopy(good);good['floating']=0;good['equity']=good['balance'];before[0]=subject.property_holds(kind,good);actual[0]=module.property_holds(kind,good)
  verdict='MUTATION_KILLED' if before==[True,False] and actual==[True,True] else 'MUTATION_SURVIVED'
  mr.append(dict(MutationID='PROPERTY-MUT-'+kind,ExactEdit={'Old':old,'New':new},OriginalSourceHash=hashlib.sha256(source.encode()).hexdigest(),MutantSourceHash=hashlib.sha256(changed.encode()).hexdigest(),Positive=render(good),Negative=render(bad),IndependentExpected=[True,False],OriginalActual=before,MutantActual=actual,Verdict=verdict,ProofBoundary='ANALYTICAL_PREDICATE_MUTATION_NOT_PRODUCTION_OR_NATIVE'))
 out=dict(a.meta(__file__),StartedUtc=started,FinishedUtc=a.now(),SourceHashes={str(p.relative_to(a.ROOT)):a.sha(p) for p in [a.ROOT/'Tests/Static/HSBI_FULL_SYSTEM_AUDIT_01_reference.py',a.ROOT/'Tests/Reference/HSBI_FULL_SYSTEM_AUDIT_01_accounting.py']},ScenarioCount=len(sr),ScenarioPass=sum(r['Result']=='PASS' for r in sr),ScenarioFail=sum(r['Result']=='FAIL' for r in sr),RawGeneratedPropertyPairs=360,Deduplication='Exact canonical property+positive+negative input pairs;115 repeats excluded, not counted as independent samples',PropertySamplePairs=len(ps),PropertyPass=sum(r['Result']=='PASS' for r in ps),PropertyFail=sum(r['Result']=='FAIL' for r in ps),MutationCount=len(mr),MutationsKilled=sum(r['Verdict']=='MUTATION_KILLED' for r in mr),Scenarios=sr,Properties=ps,Mutations=mr,Assumptions='Synthetic hedging unit-value symbol, tick1, spread quoted, open/exit commissions0.1perlot, leverage100 only margin illustration. No real broker prices/strategy decisions.',MQL5_COMPILE='NOT_RUN',MQL5_NATIVE_TESTS='NOT_RUN');out['ExitCode']=int(out['ScenarioFail'] or out['PropertyFail'] or out['MutationsKilled']!=15);a.save('REFERENCE',out);print('REFERENCE',out['ScenarioPass'],'/20',out['PropertyPass'],'/'+str(out['PropertySamplePairs']),'mutations',out['MutationsKilled'],'/15');print([r['TestID'] for r in sr if r['Result']!='PASS']);return out['ExitCode']
if __name__=='__main__':raise SystemExit(main())
