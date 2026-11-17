"""Read-only baseline documentation/protected-file inventory, no trading calculations."""
from pathlib import Path
import hashlib,json,re,subprocess,datetime
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'Tests/Evidence/FAR100_R1'
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def run():
 tracked=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
 docs=[]; protected=[]; evidence=[]; unread=[]
 for name in sorted(filter(None,tracked)):
  p=ROOT/name
  if not p.is_file():continue
  b=p.read_bytes()
  if p.suffix.lower() in {'.mq5','.mqh'} or name.startswith('Include/'):
   protected.append(dict(path=name,sha256=sha(b),blob_sha=blob(b),bytes=len(b)))
  if p.suffix.lower() in {'.md','.txt','.rst'}:
   try:t=b.decode('utf-8-sig')
   except UnicodeDecodeError:unread.append(name);continue
   lines=t.splitlines()
   take=lambda pat:[{'line':i,'text':l[:500]} for i,l in enumerate(lines,1) if re.search(pat,l,re.I)]
   docs.append(dict(FilePath=name,BlobSHA=blob(b),SHA256=sha(b),bytes=len(b),lines=len(lines),Version=take(r'(?:Document)?Version\s*[=:]|Версия')[:2],NormativeStatus=take(r'NormativeStatus|Статус|PROPOSED|NOT_IMPLEMENTED|OWNER_SELECTED')[:2],Priority='CONTRACT' if name.startswith('Docs/') else 'HISTORICAL_EVIDENCE_OR_REVIEW',RelatedFormula=take(r'RecoverySlope|TransitionLoss|CatchUp|RecoveryPL|DealNet|Rc\s*=|Rt\s*=|Rs\s*=')[:2],RelatedInvariant=take(r'invariant|инвариант|сохранени|ровно один|exactly.once')[:2],RelatedTests=take(r'TestID|Tests:|Tests/|test.*(?:PASS|FAIL|NOT_RUN)')[:2],Conflict=take(r'CONFLICT|противореч|расхождени|gap|UNPROVEN')[:2],ResolutionStatus='FULL_BYTES_READ_MACHINE; SEMANTIC_REVIEW_NOT_CERTIFIED_FOR_EVERY_DOCUMENT'))
  elif p.suffix.lower() in {'.json','.csv','.log'}:
   # Full read and hash historical evidence, validate JSON syntax, no replay/PASS reuse.
   valid='TEXT_BYTES_READ'
   if p.suffix.lower()=='.json':
    try:json.loads(b);valid='JSON_PARSED_NOT_REEXECUTED'
    except Exception as e:valid='PARSE_UNAVAILABLE:'+type(e).__name__
   evidence.append(dict(path=name,blob_sha=blob(b),sha256=sha(b),bytes=len(b),status=valid))
 result=dict(source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),documents_found=len(docs)+len(unread),documents_bytes_read=len(docs),documents_unavailable=unread,semantic_exhaustiveness='NOT_CERTIFIED; NO_DOCUMENTATION_AUDIT_PASS',documentation=docs,historical_evidence=evidence,protected=protected)
 OUT.mkdir(parents=True,exist_ok=True)
 (OUT/'documentation_inventory.json').write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n')
 (OUT/'protected_before.json').write_text(json.dumps(protected,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ['documentation','historical_evidence','protected']},ensure_ascii=False))
 print('protected',len(protected),'historical_evidence_full_bytes',len(evidence))
if __name__=='__main__':run()
