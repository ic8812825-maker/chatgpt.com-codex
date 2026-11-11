"""New audit-only IO/inventory and conservative lexical graph. No historical writes."""
import sys,re,json,hashlib,subprocess
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2];REPO=ROOT.parents[1];BASE='4185b84f7a6a8847f6a9c5796f07113907be447d';PREFIX=ROOT.relative_to(REPO).as_posix()+'/';TAG='HSBI_FULL_SYSTEM_AUDIT_01_'
sys.path[:0]=[str(ROOT/'Tests/Static'),str(ROOT/'Tests/Reference')]
def now():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(name,obj,folder='Tests/Evidence'):(ROOT/folder/(TAG+name+'.json')).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def load(name,folder='Tests/Evidence'):return json.loads((ROOT/folder/(TAG+name+'.json')).read_text())
def meta(runner):return dict(BaseSHA=BASE,TestedSHA=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),UTC=now(),RunnerSourceHash=sha(runner),ApprovalStatus='AWAITING_ADMIN_APPROVAL')
def inventory():
 out={}
 for line in subprocess.check_output(['git','ls-tree','-rz',BASE,'--',PREFIX],cwd=REPO).split(b'\0'):
  if not line:continue
  m,p=line.split(b'\t');mode,kind,blob=m.decode().split();rel=p.decode()[len(PREFIX):];f=ROOT/rel;b=f.read_bytes()
  if hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()!=blob or bool(f.stat().st_mode&0o111)!=(mode=='100755'):raise ValueError('BASELINE_CHANGED '+rel)
  out[rel]=dict(Mode=mode,Blob=blob,SHA256=sha(f),Bytes=len(b),Lines=len(b.decode('utf-8',errors='replace').splitlines()))
 return out

def masked(text):
 # Preserve length/newlines while removing strings/comments for brace/identifier scans.
 pat=r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/'
 return re.sub(pat,lambda m:''.join('\n' if c=='\n' else ' ' for c in m.group()),text)
def functions(path):
 txt=path.read_text();s=masked(txt);rows=[]
 pat=r'\b(?:bool|int|long|ulong|double|string|void|datetime|HSBI_\w+)\s+((?:HSBI_\w+)|(?:OnInit|OnDeinit|OnTick|OnTimer|OnTradeTransaction))\s*\([^;{}]*\)\s*\{'
 for m in re.finditer(pat,s):
  start=s.index('{',m.start(),m.end());at=start+1;depth=1
  while depth and at<len(s):
   depth+=(s[at]=='{')-(s[at]=='}');at+=1
  name=m.group(1);line=txt.count('\n',0,m.start())+1
  rows.append(dict(Name=name,Line=line,EndLine=txt.count('\n',0,at)+1,Calls=sorted(set(re.findall(r'\b(HSBI_\w+)\s*\(',s[start+1:at-1]))),Source=txt[m.start():at]))
 return rows

def build_inventory():
 start=now();old=inventory();production=[p for p in old if p.startswith('Include/') and p.endswith('.mqh') or '/' not in p and p.endswith('.mq5')];assert len(production)==74
 docs=[p for p in old if p.startswith('Docs/') or p in ('README_RU.md','PROJECT_MAP_RU.md','BUILD_INFO.md','CHANGELOG_RU.md')];reports=[p for p in old if p.startswith('Reports/')];evidence=[p for p in old if p.startswith('Tests/Evidence/')];tests=[p for p in old if p.startswith('Tests/') and p not in evidence]
 includes={};fs={};formula_sites=[];docrows=[]
 for rel in production:
  p=ROOT/rel;text=p.read_text();includes[rel]=[]
  for inc in re.findall(r'#include\s+"([^"]+)"',text):
   dest=(p.parent/inc).resolve();assert dest.is_relative_to(ROOT);includes[rel].append(str(dest.relative_to(ROOT)))
  fs[rel]=functions(p)
  for i,line in enumerate(text.splitlines(),1):
   if re.search(r'(?:=|return).*?(?:\+|\*|/|Math(?:Min|Max|Log|Pow|Floor|Ceil|Round)|\b(?:>=|<=)\b)',masked(line)):
    formula_sites.append(dict(SourceFile=rel,Line=i,Source=line.strip(),Status='LEXICALLY_IDENTIFIED_NOT_SEMANTICALLY_PROVED'))
 closure=set();todo=['Hybrid_Split_Big_Independent_EA.mq5']
 while todo:
  p=todo.pop()
  if p in closure:continue
  closure.add(p);todo+=includes.get(p,[])
 byname={}
 for p,rows in fs.items():
  for row in rows:byname.setdefault(row['Name'],[]).append((p,row))
 reachable=set();todo=['OnInit','OnDeinit','OnTick','OnTimer']
 while todo:
  name=todo.pop()
  for p,row in byname.get(name,[]):
   key=p+':'+str(row['Line'])+':'+name
   if p not in closure or key in reachable:continue
   reachable.add(key);todo+=row['Calls']
 for rel in docs:
  p=ROOT/rel;lines=p.read_text().splitlines();headings=[dict(Line=i,Text=s) for i,s in enumerate(lines,1) if s.startswith('#')];claims=[dict(Line=i,Text=s) for i,s in enumerate(lines,1) if re.search(r'(?:APPROV|ACCEPT|READY|NOT_PROVEN|OPEN_P[012]|source of truth|норматив|Статус)',s,re.I)]
  docrows.append(dict(File=rel,SHA256=sha(p),Lines=len(lines),Headings=headings,StatusClaims=claims,ReviewClass='PRIMARY_OWNER_MANUAL' if re.match(r'Docs/\d\d_',rel) else 'ROOT_OR_HISTORICAL_PROPOSAL',ReviewBoundary='INDEXED_FULL_TEXT; individual requirement verdict in REQUIREMENT_MATRIX; not all historical appendices semantically re-audited'))
 out=dict(meta(__file__),StartedUtc=start,FinishedUtc=now(),Existing=old,Production=production,ProductionCount=74,ProductionLineCount=sum(old[p]['Lines'] for p in production),Docs=docs,Reports=reports,TestFiles=tests,HistoricalEvidence=evidence,DocumentIndex=docrows,Includes=includes,MainIncludeClosure=sorted(closure),Functions=fs,ConservativeReachable=sorted(reachable),FormulaSites=formula_sites,MainOnTradeTransactionPresent='OnTradeTransaction' in byname,GraphMethod='Comment/string-masked lexical direct call graph; overload overapproximation, no runtime/native proof')
 save('INVENTORY',out);print('inventory',len(old),'production',len(production),'lines',out['ProductionLineCount'],'docs',len(docs),'formula sites',len(formula_sites));return out
if __name__=='__main__':build_inventory()
