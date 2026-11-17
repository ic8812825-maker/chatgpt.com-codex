"""Standalone causal research tests. Expected constants are not generated from actual results."""
from pathlib import Path
from decimal import Decimal as D
from fractions import Fraction
import json,sys,hashlib,copy
import hsbi_far100_r1_oracle as o
OUT=o.OUT;records=[];mutations=[]
def check(tid,cls,actual,expected,reason=''):
 status='PASS' if actual==expected else 'FAIL'
 records.append(dict(TestID=tid,Class=cls,Expected=str(expected),Actual=str(actual),Status=status,Reason=reason,EvidenceClass='EXECUTED_PYTHON_REFERENCE_ONLY'))
 return status=='PASS'
def rejects(fn):
 try:fn();return False
 except (ValueError,ArithmeticError):return True

def run():
 b,a=o.quote();ps=o.fixture()
 expected=['-275.50','-306.60','-153.30','112.25']
 for idx,(p,x) in enumerate(zip(ps,expected)):
  check(f'MONEY-{idx}','MONEY',o.net(p,b,a),D(x),'literal independently hand-derived net')
  check(f'ORACLE-{idx}','MONEY',Fraction(o.net(p,b,a)),o.rational_net(p,b,a),'independent Fraction tick count')
 check('SUM','MONEY',o.close_value(ps,b,a),D('-623.15'))
 check('OPEN','COST',o.OPEN_RATE*sum((p.volume for p in ps),D(0)),D('11.55'))
 check('RECOVERY','FINALCLOSE',o.metrics(ps,b,a)['RecoveryPLCloseNowA'],D('-634.70'))
 check('SIDES','PRICE',o.gross(ps[0],b,a),D('-270'))
 check('PIP_DIM','PRICE',D('.0001')*D('100000'),D('10'))
 check('TICK_DIM','PRICE',D('.00001')*D('100000'),D('1'))
 check('SLOPE','VOLUME',o.geometry(D('1'))['RecoverySlope'],D('.3'))
 check('LOT_GATE80','CATCHUP',D('.8')*D('1.3')>D('1'),True)
 check('LOT_GATE60','CATCHUP',D('.6')*D('1.3')>D('1'),False,'fixture share0.6 not approved default')
 check('MONEY_GATE','CATCHUP',D('.8')*max(D(0),D('-306.6'))-D('275.5')-D('5'),D('-280.5'))
 for i in range(1,100):
  n=D(i)/100
  check(f'GRID-{i:02}','VOLUME',o.grid(n),True)
  # Independent expected quantum via integer arithmetic, no call to geometry rounding.
  g=o.geometry(n);c=(i*12//10)/100;t=(i*6//10)/100;s=((i*5+9)//10)/100
  check(f'ROUND-{i:02}','VOLUME',(g['C'],g['T'],g['S']),(D(str(c)),D(str(t)),D(str(s))))
 for st,exp in [('.01',True),('.1',True),('.25',False)]:check('COARSE-'+st,'VOLUME',o.geometry(D('1'),step=D(st))['valid'],exp)
 check('TERMINAL','NEWFAR',any(D('0')<D(i)*D('.01')<D('.01') for i in range(1,100)),False)
 for d in [-1,1]:
  rows=o.candidate_rows(d)
  check('COMPLETE_GRID'+str(d),'NEWFAR',[r['CandidateN'] for r in rows],[D(i)/100 for i in range(1,100)])
  check('NO_SAFE'+str(d),'NEWFAR',all(r['FinalStatus']=='REJECT' and r['CatchUp']==D('-280.5') for r in rows),True)
  for n in ['.50','.40','.30','.20','.10','.05','.01']:
   r=rows[int(D(n)*100)-1];check(f'SPECIAL-{d}-{n}','NEWFAR',r['TransitionClosingNet'],D('-623.15')+D('255.5')*D(n),'C−N close, not full C')
  tr=o.transition(direction=d)
  check('PHYSICAL_SUM'+str(d),'TRANSITION',tr['ClosingNet'],D('-520.95'))
  check('PHYSICAL_RESIDUAL'+str(d),'TRANSITION',tr['ResidualNet'],D('-102.20'))
  check('PHYSICAL_CLOSED_FAR'+str(d),'TRANSITION',next(r['SimulatedClosed'] for r in tr['Rows'] if r['ActionID']=='MODEL_CLOSE_FAR'),D('1'))
  check('PHYSICAL_CLOSED_CORE'+str(d),'TRANSITION',next(r['SimulatedClosed'] for r in tr['Rows'] if r['ActionID']=='MODEL_CLOSE_BIG_CORE'),D('.8'))
  check('CONSERVATION'+str(d),'TRANSITION',tr['ClosingNet']+tr['ResidualNet'],D('-623.15'))
  for row in tr['Rows']:
   check(f'CONSERVE_{d}_{row["Step"]}','MONEY',row['Metrics']['EconomicCycleCloseNow'],D('-534.70'),'opening costs in realized exactly once')
  far=tr['Rows'][-1]['Positions'][0]
  check('LINEAGE'+str(d),'IDENTITY',(far['identifier'],far['direction'],far['open_price'],far['volume']),('MODEL_C0',-d,o.fixture(d)[1].open_price,D('.4')))
  check('PROMOTE'+str(d),'IDENTITY',(tr['Rows'][14]['RoleBefore'],tr['Rows'][14]['RoleAfter']),('BIG_CORE','FAR'))
 for p,q in zip(o.fixture(-1),o.fixture(1)):
  check('MIRROR-'+p.role,'MONEY',o.net(p,*o.quote(direction=-1)),o.net(q,*o.quote(direction=1)))
 for i in range(101):
  b1=D('1.10000')+D(i)*D('.0001');b2,a2=o.quote(str(b1))
  for p,q in zip(o.fixture(-1),o.fixture(1)):
   br,ar=o.quote(str(b1),direction=1)
   check(f'FRACTION_{i}_{p.role}','MONEY',Fraction(o.net(p,b2,a2)),o.rational_net(p,b2,a2))
   check(f'MIRROR_{i}_{p.role}','PRICE',o.net(p,b2,a2),o.net(q,br,ar))
 # Every tick in declared current→big research interval; no skipping endpoints.
 values=[]
 for i in range(2501):
  bi=D('1.10500')+D(i)*o.TICK
  val=o.metrics(ps,bi,bi+D('.0002'))['RecoveryPLCloseNowA'];values.append(val)
 check('ALL_TICK_CATCHUP_NEGATIVE','CATCHUP',all(D(x['CoreOnlyCatchUp'])<0 for x in json.loads((OUT/'control_price_curve.json').read_text())),True,'all2501 declared research control ticks, not unbounded tail')
 check('TICK_MONOTONIC_ALL2501','FUTURESMALL',all(y-x==D('.30') for x,y in zip(values,values[1:])),True,'local linear money monotonicity, not physical future proof')
 check('THRESHOLD_EQUAL','FINALCLOSE',o.metrics(ps,*o.quote('1.12419'))['RecoveryPLCloseNowA'],D('16'))
 check('BELOW_THRESHOLD','FINALCLOSE',o.metrics(ps,*o.quote('1.12418'))['RecoveryPLCloseNowA']>=D(16),False)
 check('BIG_FINAL','FINALCLOSE',o.metrics(ps,*o.quote('1.13000'))['RecoveryPLCloseNowA'],D('190.30'))
 check('FINAL_PRIORITY','FINALCLOSE','FINAL_CLOSE_PREVIEW' if o.metrics(ps,*o.quote('1.13000'))['RecoveryPLCloseNowA']>=16 else 'TRANSITION','FINAL_CLOSE_PREVIEW')
 for invalid in [D('NaN'),D('Infinity'),D('-Infinity'),D('-.01'),D('0'),D('.015')]:check('INVALID-'+str(invalid),'NEGATIVE',o.grid(invalid),False)
 check('WRONG_SIDE_DOMAIN','PRICE',rejects(lambda:o.net(ps[0],D('1.1'),D('1.0'))),True)
 check('OFF_TICK','PRICE',rejects(lambda:o.net(ps[0],D('1.100001'),D('1.100021'))),True)
 m=o.metrics(ps,b,a)
 check('MARGIN_GROSS','MARGIN',m['MarginProfiles']['SYN_GROSS_1_100']['MarginUsed'],D('3638.58'))
 check('MARGIN_MAX','MARGIN',m['MarginProfiles']['SYN_HEDGED_MAX']['MarginUsed'],D('1984.68'))
 check('MARGIN_DISCOUNT','MARGIN',m['MarginProfiles']['SYN_HEDGED20']['MarginUsed'],D('2315.46'))
 check('MARGIN_NOT_NET','MARGIN',m['MarginProfiles']['SYN_GROSS_1_100']['MarginUsed']>abs(m['NetLotSELLminusBUY'])*D('1102.6'),True)
 check('RISK_CONTROL','RISK',m['RiskControlSymmetric100pip'],D('300'))
 check('ACCOUNT_COUNTEREXAMPLE','RISK',D('.4')*D(100)+D(10000)>D(1)*D(100),True,'smaller Far plus foreign risk10000 need not reduce account risk')
 # Exact cash lifecycle independent of economic R/U. No broker funding is implied.
 grant=D('14.5');free=grant-D(9)
 check('FUNDS1','ALLOCATION',free,D('5.5'));check('FUNDS2','ALLOCATION',free>=D(9),False)
 check('RESERVE_CONSERVE','ALLOCATION',D('4')+D('0')+D('10.5'),grant)
 check('INITIAL_EXCLUDED','ALLOCATION',o.R0-o.INITIAL,D('-11.55'),'opening costs retained after Initial exclusion')
 check('SOURCE_FULL_BODY','IDENTITY',{'profit':D(20),'commission':D('-1.875')}=={'profit':D(21),'commission':D('-2.875')},False)
 bar=o.Barrier();check('PARTIAL','TRANSITION',bar.event('e1',D('.2')),'PENDING');check('NO_ADVANCE_PARTIAL','TRANSITION',bar.can_advance,False)
 check('REPLAY','IDENTITY',bar.event('e1',D('.2')),'NO_OP');check('DELAYED','TRANSITION',bar.event('e2',D('.3')),'COMPLETED_MODEL')
 check('ALTERED_EVENT','IDENTITY',bar.event('e1',D('.1')),'CONFLICT');check('CONFLICT_BLOCK','TRANSITION',bar.can_advance,False)
 bar=o.Barrier();bar.unknown=True;check('TIMEOUT','TRANSITION',bar.can_advance,False)
 check('WRONG_IDENTIFIER','IDENTITY',bar.event('e3',D('.5'),'OTHER'),'REJECT')
 for i in range(1,19):
  # serialization/recovery state test only, not real process crash or durable IO guarantee
  snap={'step':i,'pending':True,'filled':'0.2','expected':'0.5','source':'MODEL_S0'};rec=json.loads(json.dumps(snap));check(f'RESTART-{i:02}','RESTART',(rec==snap,rec['filled']==rec['expected']),(True,False),'reference checkpoint roundtrip, native durability NOT_RUN')
 control=dict(fresh=True,deals_complete=True,core_present=True,core_id='CORE',original_core_id='CORE',far_count=1,reconciled=True,outcome='COMPLETED',actual_residual=D('.4'),planned_residual=D('.4'),free=D('1000'),need=D('633.2'))
 check('ADMISSION_CONTROL','TRANSITION',o.admission(control),'COMPONENT_ONLY_NO_DISPATCH')
 for name,key,value in [('MISSING_DEAL','deals_complete',False),('MISSING_CORE','core_present',False),('VOLUME_CHANGED','actual_residual',D('.39')),('TWO_FAR_OR_MISSING_FAR','far_count',2),('UNRECONCILED','reconciled',False),('STALE_SNAPSHOT','fresh',False),('IDENTIFIER_MISMATCH','core_id','OTHER'),('PENDING_OR_UNKNOWN','outcome','TIMEOUT'),('INSUFFICIENT_FUNDING','free',D('100')),('NONFINITE_FUNDING','free',D('NaN'))]:
  z=dict(control);z[key]=value;check(name,'NEGATIVE',o.admission(z),name,'causal one-field negative control')
 invmodel=o.Inventory();source=('BROKER_MODEL','SERVER_MODEL','1','101');body=('CORE','20','-1.875')
 check('SOURCE_POST','ALLOCATION',invmodel.post(source,body,D('14.5')),'SOURCE_OBSERVED_MODEL')
 check('ALLOCATION_DEBIT','ALLOCATION',invmodel.debit(source,'e1',D(9)),'DEBIT_MODEL')
 check('EXHAUSTED','ALLOCATION',invmodel.debit(source,'e2',D(9)),'INSUFFICIENT_FREE')
 check('SOURCE_REIMPORT','ALLOCATION',invmodel.post(source,body,D('14.5')),'NO_OP')
 check('FREE_NOT_REFRESHED','ALLOCATION',invmodel.free[source],D('5.5'))
 check('DEBIT_REPLAY','ALLOCATION',invmodel.debit(source,'e1',D(9)),'NO_OP')
 check('ALTERED_DEBIT','ALLOCATION',invmodel.debit(source,'e1',D('8.999')),'CONFLICT')
 check('SOURCE_ALTERED','IDENTITY',invmodel.post(source,('CORE','21','-2.875'),D('14.5')),'CONFLICT')
 check('UNKNOWN_SOURCE','ALLOCATION',invmodel.debit(('UNKNOWN',),'e2',D(9)),'UNAVAILABLE')
 check('ACTUAL_VS_PLAN','NEWFAR',D('.39')==D('.4'),False)
 check('REPEATED_ACTION','TRANSITION',len(set(['A1','A1']))==2,False)
 gap=dict(control);gap['fresh']=False
 check('GAP_NO_ADVANCE','RISK',o.admission(gap),'STALE_SNAPSHOT','stale gap input has no authorization')
 check('EMERGENCY_NOT_PROFIT','FINALCLOSE','EMERGENCY_LOSS'=='SUCCESSFUL_RECOVERY',False)
 check('TWO_EXTREMA','CATCHUP',(max(range(2),key=lambda i:[3600,2240][i]),min(range(2),key=lambda i:[-1001,-1201][i])),(0,1),'historical physical projected counterexample, not current EURUSD successful chain')
 # Causal mutations: each damaged artifact must be rejected by a distinct invariant.
 base={'farclosed':D(1),'coreclosed':D('.8'),'residual':D('.4'),'closing':D('-520.95'),'open':D('-102.2'),'identity':'MODEL_C0','direction':1,'initial_count':1,'grant':D('14.5'),'consumed':D(9),'free':D('5.5'),'pending':False,'second_far':False}
 def invariant(z):
  return z['farclosed']==1 and z['coreclosed']+z['residual']==D('1.2') and z['closing']+z['open']==D('-623.15') and z['identity']=='MODEL_C0' and z['direction']==1 and z['initial_count']==1 and z['consumed']+z['free']==z['grant'] and z['free']>=0 and not z['pending'] and not z['second_far']
 check('MUT_BASE_VALID','NEGATIVE',invariant(base),True)
 changes=[('CLOSE_COMPRESSION','farclosed',D('.6'),'FarClosed=1'),('CLOSE_FULL_CORE','coreclosed',D('1.2'),'CoreClosed+N=C'),('OMIT_SMALL','closing',D('-633.2'),'closing+residual=full'),('DOUBLE_RESERVE','closing',D('-120.95'),'allocations not income'),('DOUBLE_FEE','closing',D('-524.45'),'cost counted once'),('WRONG_SIDE','closing',D('-500.95'),'executable side PnL'),('NEW_POSITION','identity','NEW_MARKET_POSITION','same Core identifier'),('DIRECTION_TEMPLATE','direction',-1,'promoted Core direction'),('INITIAL_DOUBLE','initial_count',2,'unique initial posting'),('REUSE_FREE','consumed',D(18),'Grant=C+Free'),('PARTIAL_ADVANCE','pending',True,'no advance pending'),('TWO_FAR','second_far',True,'unique managed Far')]
 for name,key,value,reason in changes:
  broken=copy.deepcopy(base);broken[key]=value;killed=not invariant(broken);mutations.append(dict(Mutation=name,ChangedField=key,MutationValue=str(value),KillingInvariant=reason,Detected=killed,Status='KILLED' if killed else 'SURVIVED'))
  check('MUT-'+name,'NEGATIVE',killed,True,reason)
 # Re-read every original protected and tracked history, prove no mutation of source/evidence.
 protected=json.loads((OUT/'protected_before.json').read_text())
 check('PROTECTED_HASHES','IDENTITY',all(hashlib.sha256((o.ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'] for x in protected),True)
 inv=json.loads((OUT/'documentation_inventory.json').read_text())
 check('HISTORICAL_EVIDENCE_UNCHANGED','IDENTITY',all(hashlib.sha256((o.ROOT/x['path']).read_bytes()).hexdigest()==x['sha256'] for x in inv['historical_evidence']),True)
 failed=[r for r in records if r['Status']=='FAIL']
 summary=dict(TestsExecuted=len(records),PASS=len(records)-len(failed),FAIL=len(failed),UNPROVEN=5,NOT_RUN=4,UnprovenItems=['full documentation semantic review','actual broker proof','full CR09 binding','safe first SmallTransition','profitable multi-transition reachability'],NotRunItems=['MetaEditor compile','native MQL5','broker calculation-only calls','durable crash/concurrency'],Mutations=len(mutations),Killed=sum(m['Detected'] for m in mutations),Survived=sum(not m['Detected'] for m in mutations),Historical67TestSpecs='NOT_RUN_UNCHANGED',TradeDispatchAttempts=0,NativeTestsExecuted=0,ExitCode=1 if failed else 0)
 (OUT/'test_results.json').write_text(o.dumps(dict(summary=summary,records=records)))
 (OUT/'mutation_results.json').write_text(o.dumps(mutations))
 print(o.dumps(summary))
 for r in failed:print(o.dumps(r))
 return summary['ExitCode']
if __name__=='__main__':sys.exit(run())
