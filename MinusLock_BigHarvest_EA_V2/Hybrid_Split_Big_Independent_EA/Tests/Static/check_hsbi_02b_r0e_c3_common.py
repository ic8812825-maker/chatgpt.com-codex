#!/usr/bin/env python3
"""C3 audit IO: new artifacts only; independent Git inventory, no production writes."""
import copy,hashlib,json,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2];REPO=ROOT.parents[1];BASE='3737116bff6e2275d674b3dd7b816de93715f27c';PREFIX=ROOT.relative_to(REPO).as_posix()+'/'
sys.path[:0]=[str(ROOT/'Tests/Reference'),str(ROOT/'Tests/Static')]
import check_hsbi_02b_r0e_c2_contracts as c2
import check_hsbi_02b_r0e_c2_mutations as mutants
subject=c2.subject;wire=c2.wire;view=c2.view;fixture=c2.fixture;same=c2.same;checksum=c2.checksum

def now():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pins():
 files=[Path(__file__).resolve(),Path(c2.__file__),Path(mutants.__file__),Path(subject.__file__),Path(subject.dto.__file__),Path(subject.evidence.__file__),Path(subject.exact.__file__),Path(c2.frozen.__file__),Path(wire.__file__)]
 return {str(p.relative_to(ROOT)):sha(p) for p in files}
def metadata(runner):return dict(BaseSHA=BASE,TestedSHA=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),UTC=now(),RunnerSourceHash=sha(runner),SourceHashes={**pins(),str(Path(runner).relative_to(ROOT)):sha(runner)},ApprovalStatus='AWAITING_ADMIN_APPROVAL',ProofBoundary='Audit/test-only; Python/reference/static, no broker or MQL5 runtime')
def save(name,data):
 p=ROOT/'Tests/Evidence'/('NEXT_STAGE_02B_R0E_C3_'+name+'.json');p.write_text(json.dumps(view(data),ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def inventory():
 out={}
 for row in subprocess.check_output(['git','ls-tree','-rz',BASE,'--',PREFIX],cwd=REPO).split(b'\0'):
  if not row:continue
  meta,path=row.split(b'\t');mode,kind,blob=meta.decode().split();rel=path.decode()[len(PREFIX):];p=ROOT/rel;raw=p.read_bytes();actual=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();assert actual==blob and bool(p.stat().st_mode&0o111)==(mode=='100755'),rel
  out[rel]=dict(mode=mode,GitBlob=blob,SHA256=sha(p))
 return out
def trace(fn,module=subject):
 calls=set();lines=set();allowed={module.__file__,module.dto.__file__,module.exact.__file__,module.evidence.__file__}
 def hook(frame,event,arg):
  if frame.f_code.co_filename in allowed:
   if event=='call':calls.add(frame.f_code.co_name)
   if event=='line':lines.add((frame.f_code.co_name,frame.f_lineno))
  return hook
 try:sys.settrace(hook);result=fn()
 finally:sys.settrace(None)
 return result,sorted(calls),[list(p) for p in sorted(lines)]
if __name__=='__main__':
 started=now();old=inventory();prod={p:v for p,v in old.items() if p.startswith('Include/') and p.endswith('.mqh') or '/' not in p and p.endswith('.mq5')};assert len(prod)==74
 save('BASELINE',dict(metadata(__file__),StartedUtc=started,FinishedUtc=now(),Existing=old,Production=prod,ExistingCount=len(old),ProductionCount=len(prod),Command=[sys.executable,*sys.argv],ExitCode=0));print('BASELINE',len(old),len(prod))
