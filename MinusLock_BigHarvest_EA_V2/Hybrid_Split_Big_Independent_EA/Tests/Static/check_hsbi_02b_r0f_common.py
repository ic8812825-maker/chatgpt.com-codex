#!/usr/bin/env python3
"""R0F IO and independent immutable Git inventory. New R0F artifacts only."""
import hashlib,json,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2];REPO=ROOT.parents[1];BASE='ad5ce78d74c53b34358cd7508982aa888976057a';PREFIX=ROOT.relative_to(REPO).as_posix()+'/'
sys.path[:0]=[str(ROOT/'Tests/Static'),str(ROOT/'Tests/Reference')]
def now():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def meta(runner):return dict(BaseSHA=BASE,TestedSHA=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),UTC=now(),RunnerSourceHash=sha(runner),SourceHashes={str(Path(runner).relative_to(ROOT)):sha(runner),str(Path(__file__).relative_to(ROOT)):sha(Path(__file__))},ApprovalStatus='AWAITING_ADMIN_APPROVAL')
def save(name,data,folder='Tests/Evidence'):
 p=ROOT/folder/('NEXT_STAGE_02B_R0F_'+name+'.json');p.write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def tree():
 result={}
 for row in subprocess.check_output(['git','ls-tree','-rz',BASE,'--',PREFIX],cwd=REPO).split(b'\0'):
  if not row:continue
  m,p=row.split(b'\t');mode,kind,blob=m.decode().split();rel=p.decode()[len(PREFIX):];f=ROOT/rel;b=f.read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==blob and bool(f.stat().st_mode&0o111)==(mode=='100755'),rel
  result[rel]=dict(Mode=mode,GitBlob=blob,SHA256=sha(f))
 return result
if __name__=='__main__':
 old=tree();prod={p:v for p,v in old.items() if p.startswith('Include/') and p.endswith('.mqh') or '/' not in p and p.endswith('.mq5')};assert len(prod)==74
 save('BASELINE',dict(meta(__file__),Existing=old,Production=prod,NormativeSources={p:v for p,v in old.items() if p.startswith('Docs/') or p.startswith('Tests/Contracts/')},ExistingCount=len(old),Command=[sys.executable,*sys.argv],ExitCode=0));print('BASELINE',len(old),len(prod))
