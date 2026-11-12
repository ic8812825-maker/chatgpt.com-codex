"""DG01 audit-only IO. Default operations never mutate baseline files."""
import sys,json,hashlib,subprocess,os
from pathlib import Path
from datetime import datetime,timezone
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2];REPO=ROOT.parents[1];BASE='92a55371299439f2ff33494497cde2aa78013d77';TAG='HSBI_DG01_'
sys.path[:0]=[str(ROOT/'Tests/Static'),str(ROOT/'Tests/Reference')]
def now():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def strict(p):
 def pairs(xs):
  d={}
  for k,v in xs:
   if k in d:raise ValueError('duplicate key '+k)
   d[k]=v
  return d
 return json.loads(Path(p).read_text(),object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(ValueError('non-JSON '+v)))
def save(n,data,folder='Tests/Evidence'):
 (ROOT/folder/(TAG+n+'.json')).write_text(json.dumps(data,ensure_ascii=False,allow_nan=False,indent=2)+'\n')
def load(n,folder='Tests/Evidence'):return strict(ROOT/folder/(TAG+n+'.json'))
def run(cmd,input=None,cwd=None):
 start=now();p=subprocess.run(cmd,cwd=cwd or ROOT,input=input,text=True,capture_output=True,timeout=180,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 entry=Path(cmd[1]) if len(cmd)>1 and str(cmd[1]).endswith('.py') else Path(sys.argv[0])
 runner_hash=sha(entry) if entry.is_file() else hashlib.sha256(cmd[2].encode()).hexdigest() if len(cmd)>2 and cmd[1]=='-c' else sha(__file__)
 return dict(Command=cmd,StartedUTC=start,FinishedUTC=now(),ExitCode=p.returncode,Stdout=p.stdout,Stderr=p.stderr,RunnerSHA256=runner_hash,CaptureSHA256=sha(__file__),InputSHA256=hashlib.sha256(input.encode()).hexdigest() if input is not None else None,Environment=dict(OS=sys.platform,Python=sys.version.split()[0]),ProofBoundary='Process output; no native claim unless real MQL tool executed')
def inventory():
 prefix=ROOT.relative_to(REPO).as_posix()+'/';rows=[]
 for raw in subprocess.check_output(['git','ls-tree','-rz',BASE,'--',prefix],cwd=REPO).split(b'\0'):
  if not raw:continue
  info,name=raw.split(b'\t');mode,kind,blob=info.decode().split();rel=name.decode()[len(prefix):];f=ROOT/rel;b=f.read_bytes();actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
  if actual!=blob or bool(f.stat().st_mode&0o111)!=(mode=='100755'):raise ValueError('BASELINE_CHANGED '+rel)
  rows.append(dict(Path=rel,BlobID=blob,Mode=mode,SHA256=sha(f),Size=len(b),Production=rel.startswith('Include/') and rel.endswith('.mqh') or '/' not in rel and rel.endswith('.mq5')))
 return rows
