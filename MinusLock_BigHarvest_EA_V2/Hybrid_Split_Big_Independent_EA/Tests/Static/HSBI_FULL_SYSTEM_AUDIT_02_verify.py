"""Audit02 standalone coordinator. Historical inputs are read-only, adapters explicitly shared.
--run creates only Audit02 artifacts; default independently checks Git baseline/preservation.
"""
import sys,os,json,hashlib,subprocess,re,shutil,tempfile,importlib.util
from pathlib import Path
from datetime import datetime,timezone
from fractions import Fraction as Q
ROOT=Path(__file__).resolve().parents[2];REPO=ROOT.parents[1]
BASE="707f51d82217b13613c5d56d9d51d10bac5a2412";TAG="HSBI_FULL_SYSTEM_AUDIT_02_"
sys.dont_write_bytecode=True
sys.path[:0]=[str(ROOT/'Tests/Static'),str(ROOT/'Tests/Reference')]
def utc():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def strict(p):
 def pairs(xs):
  d={}
  for k,v in xs:
   if k in d:raise ValueError('Duplicate JSON key '+k)
   d[k]=v
  return d
 return json.loads(Path(p).read_text(),object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def save(n,o,folder='Tests/Evidence'):
 (ROOT/folder/(TAG+n+'.json')).write_text(json.dumps(o,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def load01(n,folder='Tests/Evidence'):return strict(ROOT/folder/('HSBI_FULL_SYSTEM_AUDIT_01_'+n+'.json'))
def run(cmd,cwd=None):
 t=utc();p=subprocess.run(cmd,cwd=cwd or ROOT,text=True,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),timeout=300)
 return dict(Command=cmd,StartedUtc=t,FinishedUtc=utc(),TestedSHA=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),ExitCode=p.returncode,Stdout=p.stdout,Stderr=p.stderr,RunnerSHA256=sha(__file__))
def inv():
 rows=[];prefix=str(ROOT.relative_to(REPO))+'/'
 for s in subprocess.check_output(['git','ls-tree','-rz',BASE,'--',prefix],cwd=REPO).split(b'\0'):
  if not s:continue
  m,p=s.split(b'\t');mode,kind,blob=m.decode().split();rel=p.decode()[len(prefix):];f=ROOT/rel;b=f.read_bytes()
  actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
  if actual!=blob or bool(f.stat().st_mode&0o111)!=(mode=='100755'):raise ValueError('HISTORICAL_CHANGED '+rel)
  rows.append(dict(File=rel,Mode=mode,GitBlob=blob,SHA256=sha(f),Production=(rel.startswith('Include/') and rel.endswith('.mqh') or '/' not in rel and rel.endswith('.mq5'))))
 return rows
def source_run():
 # Only language adapter glue and dependency ordering reused. No Audit01 fixtures/expected/cases imported.
 import HSBI_FULL_SYSTEM_AUDIT_01_extracted as old
 parts=[old.PRE];sources=[]
 for stem in old.SOURCES:
  f=ROOT/'Include'/(stem+'.mqh');text=f.read_text()
  if stem=='Persistence/HSBI_ExecutionJournal':text=text[:text.index('bool HSBI_ValidateJournalChain')]
  parts.append('\n'.join(s for s in text.splitlines() if not re.match(r'\s*#(?:include|ifndef|endif)',s)));sources.append(dict(File=str(f.relative_to(ROOT)),SHA256=sha(f)))
 fixture=ROOT/'Tests/Reference'/(TAG+'source_cases.cpp');case_text=fixture.read_text()
 if '--extended' in sys.argv:
  extension=ROOT/'Tests/Reference'/(TAG+'extension.cpp');case_text=case_text.replace('return 0;\n}',extension.read_text()+'\nreturn 0;\n}')
 parts.append(case_text);src='\n'.join(parts)
 runs=[];rows=[];mutations=[]
 with tempfile.TemporaryDirectory(prefix='hsbi-audit02-') as d:
  cpp=Path(d)/'source.cpp';binary=Path(d)/'source';cpp.write_text(src)
  c=run(['g++','-std=c++17','-O0','-fno-fast-math',str(cpp),'-o',str(binary)]);runs.append(c)
  if c['ExitCode']==0:
   z=run([str(binary)]);runs.append(z)
   for line in z['Stdout'].splitlines():
    if line.startswith('T|'):
     _,tid,a,e=line.split('|');rows.append(dict(TestID=tid,Actual=a=='1',Expected=e=='1',Result='PASS' if a==e else 'FAIL',Scope='EXTRACTED_CPP_NOT_NATIVE'))
  # Mutate real comparator operations, each with unchanged positive and causal altered-payload control.
  edits=[('ECON_PRICE','&&a.price==b.price',''),('ECON_VOLUME','&&a.volume==b.volume',''),('ALLOC_EVENT','||a.allocationEventId!=b.allocationEventId',''),('TX_OWNERSHIP','||!x.ownershipConfirmed',''),('TX_ACTION','x.transaction.actionId!=x.expectedActionId','false'),('MONEY_NEGATIVE','s.finalReserve>=0','true')]
  for mid,a,b in edits:
   if src.count(a)!=1:
    mutations.append(dict(MutationID=mid,Verdict='INFRASTRUCTURE_ERROR',Matches=src.count(a)));continue
   mutant=src.replace(a,b);cpp.write_text(mutant);c=run(['g++','-std=c++17','-O0','-fno-fast-math',str(cpp),'-o',str(binary)])
   z=run([str(binary)]) if c['ExitCode']==0 else None
   mapped={x.split('|')[1]:x.split('|')[2:] for x in z['Stdout'].splitlines() if x.startswith('T|')} if z else {}
   causal={'ECON_PRICE':'PRICE_CONFLICT','ECON_VOLUME':'VOLUME_CONFLICT','ALLOC_EVENT':'OTHER_ALLOC_EVENT_NEW','TX_OWNERSHIP':'FOREIGN_OWNERSHIP','TX_ACTION':'OTHER_ACTION','MONEY_NEGATIVE':'NEGATIVE_MONEY'}[mid]
   positive={'ECON_PRICE':'ECON_REPLAY','ECON_VOLUME':'ECON_REPLAY','ALLOC_EVENT':'ALLOC_REPLAY','TX_OWNERSHIP':'TX_VALID','TX_ACTION':'TX_VALID','MONEY_NEGATIVE':'MONEY_VALID'}[mid]
   original=next((x for x in rows if x['TestID']==causal),None);mp=mapped.get(positive);mn=mapped.get(causal)
   verdict='INFRASTRUCTURE_ERROR' if not z or z['ExitCode']!=0 or not mp or not mn else 'MUTATION_KILLED' if original and original['Result']=='PASS' and mp[0]==mp[1] and mn[0]!=mn[1] else 'MUTATION_SURVIVED'
   mutations.append(dict(MutationID=mid,ExactEdit=[a,b],OriginalSourceHash=hashlib.sha256(src.encode()).hexdigest(),MutantSourceHash=hashlib.sha256(mutant.encode()).hexdigest(),CausalTestID=causal,PositiveTestID=positive,OriginalNegative=original,MutantPositive=mp,MutantNegative=mn,Verdict=verdict,Compile=c,Run=z))
 return dict(Runs=runs,Rows=rows,Pass=sum(x['Result']=='PASS' for x in rows),Fail=sum(x['Result']=='FAIL' for x in rows),Sources=sources,FixtureSHA256=sha(fixture),ExtensionSHA256=sha(ROOT/'Tests/Reference'/(TAG+'extension.cpp')) if '--extended' in sys.argv else None,SharedAdapterSHA256=sha(old.__file__),Mutations=mutations,Boundary='Unchanged selected production bodies, new fixtures. Shared C++ LP64 adapter is not independent native semantics; NaN rejection expectations from finite domain, not old evaluator. FSA010 solver not fully executed.')
def math_run():
 rows=[]
 def t(i,a,e,b):rows.append(dict(TestID=i,Actual=str(a),Expected=str(e),Result='PASS' if a==e else 'FAIL',ProofBoundary=b))
 t('SIGNED_NET',Q(60)-2-7-1,Q(50),'Signed components; no broker authenticity')
 t('BALANCE_IDENTITY',Q(10)+15+25,Q(50),'G=C+R+F')
 t('REMAINING_GROSS',Q(15)+25,Q(40),'R+F, not OriginalGrant')
 t('NEGATIVE_BUCKET_OFFSET',Q(-50)+100,Q(50),'Sum alone cannot prove component domain')
 t('HARVEST_POSITIVE_CYCLE_NEGATIVE',Q('3.83')-Q('5')-Q('.1')-Q('.37'),Q('-1.64'),'Hedging unit-value fixture, opening costs included once')
 t('BALANCE_UP_EQUITY_DOWN',Q('1003.46')-5,Q('998.46'),'Independent fixture')
 t('SMALL_POSITIVE_BIG_NEGATIVE',Q(10)+Q(-20),Q(-10),'Small10 not Big Reserve10')
 t('BIG_POSITIVE_SMALL_NEGATIVE',Q(20)+Q(-30),Q(-10),'Positive Big not cycle positive')
 t('COMMISSION_SWAP_SIGN',Q(2)-Q(2)-Q(1),Q(-1),'Profit2,commission-2,swap-1')
 t('ABSOLUTE_V_INCREMENTAL',Q(30)-50,Q(-20),'Incremental10 cannot cover absolute50')
 t('ALL_LEVEL_NEGATIVE',min(Q(100)-90-1,Q(10)-20-1),Q(-11),'Control on max transition10 can hide level2')
 t('REUSED_RESERVE',Q(50)-30-30,Q(-10),'Two sequential30 spends cannot use same50')
 t('GROSS_UP_NET_DOWN',(Q(4)+4,Q(4)-4),(Q(8),Q(0)),'Old C3,T0,S1 gross4 net2; newC4,S4 gross8 net0')
 t('PARTIAL_FAR_SLOPE',Q('1.2')+1-Q('.5')-Q('.8'),Q('.9'),'ClosingFar.2 improves fixed-basket slope; rebuilding changes assumptions')
 t('GAP_TWO_LEVELS',(Q(110)-100)//5,Q(2),'Price gap cannot imply two actual fills')
 t('SMALL_DEBITS_BIG_RESERVE',Q(10)**28-Q('.01')-Q('.01'),Q(10)**28-Q('.02'),'Exact reference rational; not binary64 guarantee')
 t('INT64_MAX',(2**63-1)+1,2**63,'Exact math exceeds settled signed64 domain; reject needed')
 t('TRANSITION_CURRENT',max(Q(0),-sum([Q(-15),Q(100)])),Q(0),'Current signed loss after2')
 t('TRANSITION_PEAK',max(Q(0),Q(15),Q(-85)),Q(15),'Peak >cap12; sticky breach true')
 t('PREFIX_NOT_TAIL',Q('.64')<=Q('.8')**3,False,'Firsttwo contractions do not constrain step3')
 t('TERMINAL_NONZERO',Q('.01')>0,True,'Lot floor is not actual fullclose')
 t('UNHEDGED_LOSS_GROWTH',(Q(100)-1000)<(Q(100)-200),True,'SELL unit loss tends -infinity as unrestricted price increases')
 t('ROUNDING_NONCOMMUTES',2*Q('0.01'),Q('.02'),'Two .005 round-up components vs roundedtotal .01 differs; choice requires policy')
 return dict(Rows=rows,Pass=sum(x['Result']=='PASS' for x in rows),Fail=sum(x['Result']=='FAIL' for x in rows),Representation='Exact rational literal calculations; examples disprove implications, do not prove production semantics or profitability')
def main():
 baseline=inv()
 if '--run' not in sys.argv:
  p=ROOT/'Tests/Evidence'/(TAG+'PRESERVATION.json');old=strict(p)
  assert old['Files']==baseline
  for row in strict(ROOT/'Tests/Evidence'/(TAG+'VERIFICATION.json'))['Artifacts']:
   assert sha(ROOT/row['File'])==row['SHA256'],row['File']
  print('READ_ONLY_PACKAGE_PRESERVATION_PASS',len(baseline));return 0
 save('PRESERVATION',dict(BaseSHA=BASE,UTC=utc(),Files=baseline,ProductionCount=sum(x['Production'] for x in baseline)))
 started=utc();x=source_run();x['ExecutionMetadata']=dict(Command=[sys.executable,*sys.argv],StartedUtc=started,FinishedUtc=utc(),RunnerSHA256=sha(__file__),BaseSHA=BASE);save('SOURCE_TESTS_EXTENDED' if '--extended' in sys.argv else 'SOURCE_TESTS_FRESH',x);m=math_run();m['ExecutionMetadata']=dict(Command=[sys.executable,*sys.argv],StartedUtc=started,FinishedUtc=utc(),RunnerSHA256=sha(__file__),BaseSHA=BASE);save('MATH_TESTS_FRESH',m)
 print('SOURCE',len(x['Rows']),x['Pass'],x['Fail'],'MATH',m['Pass'],m['Fail'],'MUTATIONS',[v['Verdict'] for v in x['Mutations']])
 return 0
if __name__=='__main__':raise SystemExit(main())
