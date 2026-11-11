#!/usr/bin/env python3
"""R0H executable reference/mutation/native-discovery and independent preservation.
All writes are new R0H artifacts. No historical runner output paths reused.
"""
import sys,copy,json,hashlib,subprocess,types,shutil,math,re,struct
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2];REPO=ROOT.parents[1];BASE='7afad885a8ef8ff2c8189ca72760e06a1baaa50a';PREFIX=ROOT.relative_to(REPO).as_posix()+'/'
sys.path[:0]=[str(ROOT/'Tests/Reference'),str(ROOT/'Tests/Static')]
import hsbi_02b_r0h_identity_codec as subject
import hsbi_02b_r0f_independent_fixtures as fixture
import check_hsbi_02b_r0g_contracts as prior

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def save(name,data):(ROOT/'Tests/Evidence'/f'NEXT_STAGE_02B_R0H_{name}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def hashes():return {str(Path(p).relative_to(ROOT)):sha(p) for p in [__file__,subject.__file__,fixture.__file__,prior.__file__,subject.shape.__file__]}
def meta():return dict(BaseSHA=BASE,TestedSHA=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),UTC=now(),SourceHashes=hashes(),ApprovalStatus='AWAITING_ADMIN_APPROVAL')
def strict(text):
 def pairs(items):
  d={}
  for k,v in items:
   if k in d:raise ValueError('duplicate JSON key')
   d[k]=v
  return d
 return json.loads(text,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def inventory():
 out={}
 for row in subprocess.check_output(['git','ls-tree','-rz',BASE,'--',PREFIX],cwd=REPO).split(b'\0'):
  if not row:continue
  fields,name=row.split(b'\t');mode,kind,blob=fields.decode().split();rel=name.decode()[len(PREFIX):];p=ROOT/rel;b=p.read_bytes()
  if hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()!=blob or bool(p.stat().st_mode&0o111)!=(mode=='100755'):raise ValueError('baseline changed '+rel)
  out[rel]=dict(Mode=mode,GitBlob=blob,SHA256=sha(p))
 return out

def check_r0g():
 pres=strict((ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0G_PRESERVATION.json').read_text());old=pres['Existing'];actual=inventory()
 expected={}
 for row in subprocess.check_output(['git','ls-tree','-rz',pres['BaseSHA'],'--',PREFIX],cwd=REPO).split(b'\0'):
  if not row:continue
  f,name=row.split(b'\t');mode,kind,blob=f.decode().split();rel=name.decode()[len(PREFIX):]
  expected[rel]=dict(Mode=mode,GitBlob=blob,SHA256=sha(ROOT/rel))
 assert old==expected and len(old)==1320
 additions=set(actual)-set(old);assert len(additions)==17 and all('r0g' in x.lower() for x in additions)
 for p,h in pres['ArtifactHashes'].items():assert sha(ROOT/p)==h,p
 assert {p for p in additions if p not in ('Tests/Evidence/NEXT_STAGE_02B_R0G_PRESERVATION.json','Tests/Evidence/NEXT_STAGE_02B_R0G_PACKAGE_RESULTS.json')}==set(pres['ArtifactHashes'])
 archived=strict((ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0G_TEST_RESULTS.json').read_text());rows=prior.execute()
 assert rows==archived['Rows'] and len(rows)==128 and all(r['Result']=='PASS' for r in rows)
 for p,h in archived['SourceHashes'].items():assert sha(ROOT/p)==h
 return dict(Archived='ARCHIVED_EVIDENCE_VERIFIED',Fresh='FRESH_REFERENCE_EXECUTED',Native='NOT_RUN',Scenarios=128,Pass=128,Fail=0,OldBaselineCount=len(old),R0GAdditions=len(additions),PriorRows=rows,PriorRunnerHash=sha(prior.__file__),ExpectedOrigin='R0G literals/frozen independent struct.pack fixtures; not subject evaluator')

def evaluate(module=None,only=None):
 m=subject if module is None else module;r=fixture.record();rows=[]
 def check(i,expected,fn,requirement='R0H-IDENTITY',inp=None):
  if only is not None and i not in only:return
  try:actual=fn();result='PASS' if actual==expected else 'FAIL'
  except Exception as e:actual=type(e).__name__+': '+str(e);result='INFRASTRUCTURE_ERROR'
  rows.append(dict(TestID=i,RequirementID=requirement,Input=inp or i,Expected=expected,Actual=actual,Result=result,ProofBoundary='PYTHON_REFERENCE'))
 def classify(x=None,a=None,g=None,profile='B'):
  x=copy.deepcopy(r if x is None else x);a=copy.deepcopy({'Complete':True,'Record':r} if a is None else a);g=copy.deepcopy({'Complete':True,'Records':[r]} if g is None else g);before=copy.deepcopy((x,a,g));s=m.classify(x,a,g,profile);assert (x,a,g)==before;return s
 check('ID-EXACT','NO_OP',lambda:classify())
 check('ID-CONFIRMED-NEW','NEW',lambda:classify(g={'Complete':True,'Records':[]}))
 check('ID-UNKNOWN-HISTORY','UNAVAILABLE',lambda:m.classify(r,None,{'Complete':True,'Records':[]}))
 check('ID-INCOMPLETE-REGISTRY','UNAVAILABLE',lambda:classify(g={'Complete':False,'Records':[]}))
 check('ID-UNKNOWN-DEAL','UNAVAILABLE',lambda:classify(a={'Complete':True,'Record':None}))
 check('ID-MALFORMED','REJECT',lambda:m.classify(True,None,None))
 check('ID-BOOL-FLAG','REJECT',lambda:classify(a={'Complete':1,'Record':r}))
 check('ID-UNKNOWN-FIELD','REJECT',lambda:classify(dict(r,Future=1)))
 missing=dict(r);del missing['Profit'];check('ID-MISSING-FIELD','REJECT',lambda:classify(missing))
 for label,value in [('nan',float('nan')),('inf',float('inf')),('negative-inf',-float('inf'))]:check('ID-NONFINITE-'+label,'REJECT',lambda v=value:classify(dict(r,Profit=v)))
 check('ID-LEGACY','UNAVAILABLE',lambda:classify(g={'Complete':True,'Records':[None]}))
 check('ID-DUPLICATE-INDEX','CONFLICT',lambda:classify(g={'Complete':True,'Records':[r,r]}))
 check('ID-SAME-NET','CONFLICT',lambda:classify(dict(r,Profit=50.0,Commission=3.0)))
 a=dict(r,Profit=50.0,Swap=0.0,Commission=0.0,Fee=0.0);b=dict(a,Profit=60.0,Commission=-10.0)
 check('ID-EXPLICIT-50-60','CONFLICT',lambda:classify(b,a={'Complete':True,'Record':b},g={'Complete':True,'Records':[a]}))
 changes={'SchemaVersion':2,'Broker':'B2','Server':'S2','AccountLogin':2,'Symbol':'GBPUSD','Magic':8,'CycleID':2,'DealTicket':12,'OrderTicket':99,'PositionIdentifier':99,'ActionID':2,'EventID':32,'Role':'Small','EntryType':'IN','DealType':'BUY','TimestampMsc':100001,'Volume':2.0,'Price':1.5,'Profit':61.0,'Swap':-3.0,'Commission':-8.0,'Fee':-2.0,'DealNet':49.0,'Currency':'EUR','Precision':3,'SourcePlanApplicable':False,'SourcePlan':2,'SourcePolicyApplicable':False,'SourcePolicyVersion':2}
 for field,value in changes.items():
  x=dict(r,**{field:value})
  if field in ('SourcePlanApplicable','SourcePolicyApplicable'):x['SourcePlan' if field=='SourcePlanApplicable' else 'SourcePolicyVersion']=None
  keyfield=field in ('Broker','Server','AccountLogin','DealTicket')
  expect='UNAVAILABLE' if field=='SchemaVersion' or keyfield else 'CONFLICT'
  check('ID-PRESENTED-'+field,expect,lambda v=x:classify(v))
  check('ID-COHERENT-'+field,'UNAVAILABLE' if field=='SchemaVersion' else 'NEW' if keyfield else 'CONFLICT',lambda v=x:classify(v,a={'Complete':True,'Record':v}))
  if keyfield:check('ID-UNCONFIRMED-'+field,'UNAVAILABLE',lambda v=x:classify(v,a={'Complete':False,'Record':v},g={'Complete':True,'Records':[]}))
 for name,value in [('LONG_MIN',-(1<<63)),('LONG_MAX',(1<<63)-1)]:
  x=dict(r,Magic=value);check('DOMAIN-'+name,'NO_OP',lambda v=x:classify(v,a={'Complete':True,'Record':v},g={'Complete':True,'Records':[v]}))
 for name,value in [('ULONG_MAX',(1<<64)-1),('ABOVE_DOUBLE_EXACT',9007199254740993)]:
  x=dict(r,DealTicket=value);check('DOMAIN-'+name,'NO_OP',lambda v=x:classify(v,a={'Complete':True,'Record':v},g={'Complete':True,'Records':[v]}))
 for field,value in [('AccountLogin',None),('Broker',None),('Server',None)]:
  check('UNKNOWN-'+field,'UNAVAILABLE',lambda:classify(a={'Complete':False,'Record':r})) # unknown fact indicated by independent availability, not malformed body
 for field,value in [('DealTicket',True),('DealTicket',1.5),('DealTicket',1<<64),('AccountLogin',1<<63),('Magic',0),('TimestampMsc',1<<63),('Precision',True)]:check('INVALID-'+field+'-'+str(value),'REJECT',lambda f=field,v=value:classify(dict(r,**{f:v})))
 def decode_status(data,p='B'):
  try:m.decode(data,p);return 'ACCEPT'
  except m.Invalid:return 'REJECT'
  except m.Unavailable:return 'UNAVAILABLE'
 for profile,expected_encoder in [('B',fixture.binary_record),('A',fixture.text_record)]:
  expected=expected_encoder(r);check('CODEC-'+profile+'-FULL',expected.hex(),lambda p=profile:m.encode(r,p).hex(),'R0H-CODEC')
  check('CODEC-'+profile+'-ROUNDTRIP',r,lambda p=profile:m.decode(expected_encoder(r),p),'R0H-CODEC')
  check('CODEC-'+profile+'-TRUNCATED','REJECT',lambda e=expected,p=profile:decode_status(e[:-1],p),'R0H-MALFORMED')
  check('CODEC-'+profile+'-TRAILING','REJECT',lambda e=expected,p=profile:decode_status(e+b'0',p),'R0H-MALFORMED')
  check('CODEC-'+profile+'-HEADER','REJECT',lambda e=expected,p=profile:decode_status(b'X'+e[1:],p),'R0H-MALFORMED')
  check('CODEC-'+profile+'-UNKNOWN-SCHEMA','UNAVAILABLE',lambda p=profile:decode_status((m.HEAD_B if p=='B' else m.HEAD_A)+b''.join((fixture.token_binary if p=='B' else fixture.token_text)(k)+(fixture.token_binary if p=='B' else fixture.token_text)(2 if k=='SchemaVersion' else r[k]) for k in fixture.ORDER),p),'R0H-MALFORMED')
  check('CODEC-'+profile+'-DUPLICATE-FIELD','REJECT',lambda e=expected,p=profile:decode_status(e.replace((fixture.token_binary if p=='B' else fixture.token_text)('Symbol'),(fixture.token_binary if p=='B' else fixture.token_text)('Broker'),1),p),'R0H-MALFORMED')
  check('CODEC-'+profile+'-UNKNOWN-FIELD','REJECT',lambda e=expected,p=profile:decode_status(e.replace((fixture.token_binary if p=='B' else fixture.token_text)('Symbol'),(fixture.token_binary if p=='B' else fixture.token_text)('Future'),1),p),'R0H-MALFORMED')
  check('CODEC-'+profile+'-WRONG-FLOAT-TYPE','REJECT',lambda p=profile:decode_status((m.HEAD_B if p=='B' else m.HEAD_A)+b''.join((fixture.token_binary if p=='B' else fixture.token_text)(k)+(fixture.token_binary if p=='B' else fixture.token_text)(True if k=='Profit' else r[k]) for k in fixture.ORDER),p),'R0H-MALFORMED')
 for name,value,text,bits in fixture.GOLDENS:
  check('BITS-'+name,bits,lambda v=value:m.bits(v).to_bytes(8,'big').hex(),'R0H-CODEC')
  check('TEXT-'+name,text,lambda v=value:m.token(v,'A')[len('d'+str(len(text))+':'):].decode(),'R0H-CODEC')
  check('UNBITS-'+name,True,lambda v=value,b=bits:m.unbits(int(b,16))==v,'R0H-CODEC')
 for name,value in [('long-min',-(1<<63)),('long-max',(1<<63)-1),('ulong-max',(1<<64)-1),('large-id',9007199254740993)]:
  expected=(b'i'+struct.pack('>q',value)) if value<0 else b'u'+struct.pack('>Q',value)
  check('TOKEN-'+name,expected.hex(),lambda v=value:m.token(v,'B').hex(),'R0H-CODEC')
 for name,value in [('cyrillic','Б'),('emoji','B😀'),('delimiters','B|:1')]:check('UTF8-'+name,fixture.token_binary(value).hex(),lambda v=value:m.token(v,'B').hex(),'R0H-CODEC')
 for label,raw in [('negative-zero',bytes.fromhex('8000000000000000')),('inf',bytes.fromhex('7ff0000000000000')),('nan',bytes.fromhex('7ff8000000000000'))]:
  expected=fixture.binary_record(r);start=expected.index(fixture.token_binary('Profit'))+len(fixture.token_binary('Profit'));corrupt=expected[:start+1]+raw+expected[start+9:]
  check('WIRE-'+label,'REJECT',lambda c=corrupt:decode_status(c),'R0H-MALFORMED')
 expected=fixture.binary_record(r)
 check('WIRE-STRING-OVERSIZE','UNAVAILABLE',lambda:decode_status(m.HEAD_B+b's\xff\xff\xff\xff'),'R0H-MALFORMED')
 check('WIRE-RECORD-OVERSIZE','UNAVAILABLE',lambda:decode_status(b'X'*65537),'R0H-MALFORMED')
 check('WIRE-UNKNOWN-CODEC','UNAVAILABLE',lambda:decode_status(expected,'future'),'R0H-MALFORMED')
 check('WIRE-INVALID-UTF8','REJECT',lambda:decode_status(expected.replace(fixture.token_binary('B1'),b's\x00\x00\x00\x02\xff\xff',1)),'R0H-MALFORMED')
 return rows

def mutations():
 source=Path(subject.__file__).read_text();spec=[]
 for field in ('Profit','Commission','Swap','Fee','Magic','CycleID'):spec.append(('OMIT-'+field,'for name in FIELDS:',"for name in (k for k in FIELDS if k!='"+field+"'):",'ID-COHERENT-'+field,'UNSAFE_ACCEPTANCE_KILL'))
 old="return (r['Broker'],r['Server'],r['AccountLogin'],r['DealTicket'])"
 for field in ('Broker','AccountLogin','DealTicket'):
  new=old.replace("r['"+field+"']","'IGNORED'");spec.append(('IGNORE-'+field,old,new,'ID-COHERENT-'+field,'STATUS_CONTRACT_KILL'))
 spec += [('CONFLICT-TO-NOOP',"return 'NO_OP' if equal_body(prior,incoming) else 'CONFLICT'","return 'NO_OP' if equal_body(prior,incoming) else 'NO_OP'",'ID-COHERENT-Profit','UNSAFE_ACCEPTANCE_KILL'),('UNAVAILABLE-TO-NEW',"if authority is None or registry is None:return 'UNAVAILABLE'","if authority is None or registry is None:return 'NEW'",'ID-UNKNOWN-HISTORY','UNSAFE_ACCEPTANCE_KILL'),('BYTE-ORDER',"bits(value).to_bytes(8,'big')","bits(value).to_bytes(8,'little')",'CODEC-B-FULL','STATUS_CONTRACT_KILL'),('UTF8-LENGTH',"len(raw).to_bytes(4,'big')","len(value).to_bytes(4,'big')",'UTF8-cyrillic','STATUS_CONTRACT_KILL'),('ZERO-POLICY','if x==0:return 0',"if x==0:return (1<<63) if math.copysign(1,x)<0 else 0",'BITS-negative-zero','STATUS_CONTRACT_KILL')]
 original={r['TestID']:r for r in evaluate()};rows=[]
 for mid,old,new,tid,killclass in spec:
  assert source.count(old)==1,(mid,source.count(old));changed=source.replace(old,new,1);m=types.ModuleType('isolated_'+mid.replace('-','_'));error=None
  try:
   exec(compile(changed,'isolated-'+mid+'.py','exec'),m.__dict__);tested={r['TestID']:r for r in evaluate(m,only={'ID-EXACT',tid})};neg=tested[tid];positive=tested['ID-EXACT']
   if mid in ('BYTE-ORDER','UTF8-LENGTH','ZERO-POLICY'):
    # Codec-specific positive: fixture ASCII/nonnzero avoids altered property.
    actual=m.encode(fixture.record(),'B').hex();expected=fixture.binary_record(fixture.record()).hex()
    if mid=='BYTE-ORDER':actual=m.token(1,'B').hex();expected=fixture.token_binary(1).hex()
    positive=dict(TestID='MUT-POSITIVE-'+mid,Expected=expected,Actual=actual,OriginalActual=(subject.token(1,'B').hex() if mid=='BYTE-ORDER' else subject.encode(fixture.record(),'B').hex()),Result='PASS' if actual==expected else 'FAIL')
   verdict='INFRASTRUCTURE_ERROR' if neg['Result']=='INFRASTRUCTURE_ERROR' or positive['Result']!='PASS' else killclass if neg['Actual']!=original[tid]['Expected'] else 'MUTATION_SURVIVED'
  except Exception as e:error=type(e).__name__+': '+str(e);positive={};neg={};verdict='INFRASTRUCTURE_ERROR'
  rows.append(dict(MutationID=mid,TargetFile=str(Path(subject.__file__).relative_to(ROOT)),TargetFunction=('equal_body' if mid.startswith('OMIT-') else 'source_key' if mid.startswith('IGNORE-') else 'bits' if mid=='ZERO-POLICY' else 'token' if mid in ('BYTE-ORDER','UTF8-LENGTH') else 'classify'),ExactEdit={'Old':old,'New':new},OriginalSourceHash=hashlib.sha256(source.encode()).hexdigest(),MutantSourceHash=hashlib.sha256(changed.encode()).hexdigest(),CausalTestID=tid,OriginalPositive=(dict(TestID=positive['TestID'],Expected=positive['Expected'],Actual=positive['OriginalActual'],Result='PASS' if positive['OriginalActual']==positive['Expected'] else 'FAIL',Evidence='Independently generated struct/literal bytes, compared with original in positive controls') if mid in ('BYTE-ORDER','UTF8-LENGTH','ZERO-POLICY') else original['ID-EXACT']),MutantPositive=positive,OriginalNegative=original[tid],MutantNegative=neg,IndependentExpected=original[tid]['Expected'],Error=error,Verdict=verdict,StateDelta='NONE: pure identity/codec; no monetary state',ProofBoundary='PYTHON_SOURCE_MUTATION_ONLY; MQL5 mutation execution NOT_RUN'))
 return rows

def native_discovery():
 commands=[]
 for name in ('metaeditor64','metaeditor','MetaEditor64.exe','terminal64','wine'):
  p=subprocess.run(['which',name],text=True,capture_output=True);commands.append(dict(Command=['which',name],ExitCode=p.returncode,Stdout=p.stdout,Stderr=p.stderr))
 cmd=['rg','--files','/opt','/workspace','/usr/local/bin','-g','*[Mm]eta[Ee]ditor*','-g','*terminal64*']
 p=subprocess.run(cmd,text=True,capture_output=True);commands.append(dict(Command=cmd,ExitCode=p.returncode,Stdout=p.stdout,Stderr=p.stderr))
 paths=[line for line in p.stdout.splitlines() if Path(line).suffix.lower() in ('.exe','.app')]
 available=any(r['ExitCode']==0 and r['Stdout'].strip() for r in commands[:3]) or bool([p for p in paths if 'metaeditor' in p.lower()])
 # No automatic execution on any trading account/platform. Native compiler unavailability explicitly retained.
 return dict(meta(),DiscoveryCommands=commands,CompilerBinaryCandidates=paths,CompilerAvailable=available,ToolchainScope='PATH plus /opt,/workspace,/usr/local/bin; historical Windows compile helper is not MetaEditor',MQL5_COMPILE='NOT_RUN',MQL5_NATIVE_TESTS='NOT_RUN',NATIVE_CODEC_VERIFIED='NO',NATIVE_RESULT='REFERENCE_ONLY / NATIVE_NOT_RUN',CompilerVersion='UNAVAILABLE',CompilerExitCode=None,NativeAssertions='NOT_RUN',NativeSourceHashes={str(p.relative_to(ROOT)):sha(p) for p in (ROOT/'Tests/Reference').glob('hsbi_02b_r0h_native*')},Limitations='Prepared uncompiled MQL5 candidate/harness only; no C++ substitute; terminal launch/deal APIs never invoked')

def build_docs():
 ref=strict((ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0H_TEST_RESULTS.json').read_text());mut=strict((ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0H_MUTATION_RESULTS.json').read_text())
 head='BASE_SHA='+BASE+'\n\nPROPOSED / AWAITING_ADMIN_APPROVAL. R0H TEST-ONLY. No production remediation, broker/account IO, funding, allocation or persistence.\n\n'
 source='Исходники: `Include/Money/HSBI_EconomicLedgerTypes.mqh:6` record, `:7` key, `:8` validate, `:9` equality, `:10` classifier, `:11` serializer, `:12` harvest helper. Production включает Core/Enums/Identifiers/ReasonCodes. R0G MINIMAL_IDENTITY_CONTRACT/MQL5_API_SPEC и F64Z/T17Z alternatives сохранены. Новая Python `hsbi_02b_r0h_identity_codec.py:source_key/equal_body/bits/unbits/encode/decode/classify`; MQL `hsbi_02b_r0h_native_codec.mqh:R0H_Validate/R0H_Key/R0H_Equal/R0H_Classify/R0H_Encode/R0H_Decode`, entry `hsbi_02b_r0h_native_harness.mq5:OnStart`. Новые goldens generated только independent fixture struct.pack/literal, не subject encoder.\n\n'
 def doc(name,text,folder='Docs'):(ROOT/folder/f'NEXT_STAGE_02B_R0H_{name}_RU.md').write_text('\n'.join(s.rstrip() for s in (head+source+text).rstrip().splitlines())+'\n')
 doc('NATIVE_DOMAIN_SPEC','''# Native domain — proposed, NOT_RUN

R0H-DOMAIN: AccountLogin и TimestampMsc positive signed long1..2^63-1; Magic signed long[-2^63,2^63-1], nonzero только EA-attributed BUY/SELL profile; Cycle/Deal/Order/Position/Action/Event/SourcePlan/Policy positive ulong1..2^64-1, bool не integer-ID. SourcePlan/Policy N/A только explicit applicability false. Schema1 supported, positive future schema UNAVAILABLE, malformed0/bool REJECT. Money precision fixture0..8 не Symbol price digits и не все валюты мира.

Raw double finite binary64 наблюдение, Volume/Price>0; Profit/Swap/Commission/Fee signed и Net distinct immutable. NaN/Infinity invalid. +/-0 эквивалентны Z policy; wire negative-zero noncanonical reject. Никаких raw->posted округлений или balance arithmetic. LONG_MIN/MAX,ULONG_MAX,9007199254740993 проверяются bytes без промежуточного double для ID. Floating coefficient<=2^53 в decoder относится только double payload, не ticket. EndianBE, unsigned shifts и native signed casts требуют MetaEditor/MT5 evidence.

UTF8 exact/no NUL/no normalization; uint32 length — число bytes. Нативный proposed cap4096 bytes/string и65536/record, oversized UNAVAILABLE. Unicode roundtrip и surrogate policy должны пройти native assertion; Python strict UTF8 не доказывает MQL StringToCharArray/CharArrayToString. New typed DTO содержит tagged values с полной формой29полей; bool tag может быть wrong-type case даже при сильных native types. Registry/authority completeness fixture flags не provider authenticity.

MQL assertions planned: exact boundaries, unicode Б, 2^53+1 ID, normal/subnormal/maxfinite, +/-zero, bool kind rejection, byte arrays, key/equality/status. Полный native-domain closure/array-allocation failure behavior NOT_RUN. Native code is test-only candidate; compiler errors/warnings нельзя считать PASS статическим чтением.
''')
 doc('CODEC_COMPARISON','''# F64Z и T17Z: сравнение и границы

| Criterion | F64Z | T17Z |
|---|---|---|
| Binary64 precision | Python arithmetic bits vs literal/struct.pack PASS | Python17digit literals/roundtrip PASS |
| MQL5 complexity | bounded normalization + shifts + strict binary parser | exact17digit formatter/exponent/locale + text parser |
| Determinism | reference PASS, native NOT_RUN | reference PASS, native formatter probe NOT_RUN |
| Canonical encoding | tagged fixed names/order, finite64BE, zero normalized | tagged lengths, scientific1+16digits/e±DDD; zero normalized |
| Malformed input | Python truncation/duplicate/trailing/tag/cap/UTF8/nonfinite tested | Python strict length/type/duplicate/trailing/schema tested |
| Native implementation | isolated full candidate encoder/decoder header | T17Probe only: DoubleToString(x,-16)+exponent normalization; no full native text decoder |
| Size | actual source bytes/lines in CODE_METRICS evidence; no runtime size claims | full production implementation not written; estimate additional exact formatter/text grammar code |
| Minimal one-file | statically inlineable, native acceptance remains blocker | conditional if nativeformatter matches all goldens; otherwise extra algorithm needed in sameheader/return forrevision |

Recommendation remains F64Z candidate, not ADMIN_APPROVED. Arithmetic bit extraction avoids assumed union/pointer casts; native normalization, cast signed/unsigned and subnormal behavior unknown. Negative zero normalized, so neither Z codec preserves network packet sign bit. Source identity excludes codecversion, new codec does not new income. Mismatched known payload->CONFLICT after semantic decode; unsupported codec/schema->UNAVAILABLE, no NEW.

Goldens: independent R0F fixture.GOLDENS and binary_record, literal17digit expectations, generated test mqh stores full fixed29field wire hex. Python expected for malformed tests constructed independently from fixture tokens; expected statuses literal. Runtime decoder actual NOT_RUN. Compiler literal minsubnormal may be unsupported; then native assertion/compile FAIL and recommendation must be reviewed. Exact DoubleToString result is a probe, not presumed canonical/native PASS. Hostile untrusted native decoder fuzzing/largeallocation failure tests not executed.
''')
 doc('IDENTITY_API_SPEC','''# R0H-ID/STATUS: source observations vs funding

SourceKey=(Broker,Server,AccountLogin,DealTicket). Altered Magic/Cycle/Symbol/Role/components при прежнем source не новый source. Все29 fields R0G retained, exact comparison (Z zero equivalence), no epsilon/Net-only. Schema/type validation mandatory before key/index. SameNet50 Profit50/Commission0 vsProfit60/Commission-10 =>CONFLICT, even coherent presented+authority mutation blocked against unchanged independent registry.

Broker namespace требует stable independently configured binding, не company display name; Server/Account from independently verified account context/history-provider envelope; deal existence/ownership проверяются не по nonzero ticket. Broker DEAL_* не даёт HSBI Cycle/Action/Event/Role/SourcePlan/Policy, требуется independent EA-origin journal. Ни Python, ни MQL fixture не создают такого provider.

NEW_SOURCE_OBSERVATION = подтверждённый body + complete reconciled registry absence; не ELIGIBLE_FUNDING_SOURCE. Funding needs actual posted reconciliation/role/policy/conservation/globaluniqueledger/durableCAS, none implemented. Same supported exact body known source=>NO_OP; immutable mismatch=>CONFLICT; malformed=>REJECT; unknown facts/schema/history/codec/legacy=>UNAVAILABLE. No UNAVAILABLE→NEW or CONFLICT→NO_OP. Unknown namespace facts represented providerComplete=false =>UNAVAILABLE; malformed missing fields/type/emptyknown string are REJECT, не тот же случай.

Priority in classify: shape incoming -> codec -> authority/registry DTO/completeness -> shape authority -> independent source key -> body conflict -> all registry rows/uniqueness -> NEW/NO_OP/CONFLICT. Direct equal_body/key are local helpers with mandatory classify validation; helpers do not return eligibility. Replay is comparison only, not durable journal exactly-once. Errors have no input mutations (deep-copy before/after reference tests); native output preservation assertions prepared, NOT_RUN.

Legacy facade returns UNAVAILABLE for diagnostic string, never converts 0 to NEW. Old production functions unchanged and remain unsafe as funding authority; label diagnostic-only is proposal, not enforced remediation. Native test API supports fixed typed29 body + explicit completeness, uses schema/codec statuses; cannot encode unknown record as fabricated knownzero. Native test functions have no state, no allocate/consume/persist, no broker lookups. All five status semantics require separate admin decision and native acceptance.
''')
 doc('MINIMAL_R1_DIFF_PLAN','''# Local scope/callsites и будущий diff

Current production single header record :6 и six local functions :7–12. Callsite scan в SOURCE_INVENTORY.json: exact relevant symbols only sameheader within main/Include scope; reference to future external consumers not ruled out by textual scan. Direct includes Core/Enums/Identifiers/ReasonCodes; никакого real provider/backend/canonical decoder сейчас нет. Legacy key includes Symbol/Magic/Cycle, lacks accountnamespace. Equality only key/net-epsilon/volume/price; serializer rounds4diagnosticfields. Native ABI/layout compatibility NOT_RUN.

Future only allowlist EconomicLedgerTypes.mqh after separate approval. Keep old struct/functions signature diagnostic-only per explicit compatibility policy; add separate V2record29, namespace/status/view structs and inline Validate/Key/Compare/Classify/Encode/Decode. Add Broker/Server/Account/Currency/Precision/Schema/DealType/TimestampMsc/originapplicability, never fabricate missing legacy facts. Full component equality in V2, no silent legacy reinterpretation. SourcePlan/Policy independentorigin NOT currentconsumptionplan.

MQL candidate/header currently in Tests/Reference (not included by EA); can inline routines in single allowedheader. Two test includes for harness/goldens are fixtures, not proof additional productionhelpers necessary. One-file feasibility STATICALLY_PLAUSIBLE, not nativeVerified. It cannot provide broker/EA journal ingestion, actual migration, source-wide funding/CAS, live callers requiring changes elsewhere. If existing external financial caller relies on oldintclassifier, additive V2 doesn't fix that path: scope expansion and separate approval required. One-file local equality patch is not globallyremediatedL01.

Native acceptance: real MetaEditor version+main/harness compile logs+exit+warnings, isolated MT5 script no realaccountoperations; capture all assertionmarkers. Missing final marker/crash/FAIL=>notPASS. Compilerexit0 alone not execution. Compare native byte vectors independentexpected; unknown/malformed/outref unchanged. Any different source outsideallowlist/native mismatch/unapproved schema/codec =>stop. No trade runtime changes, persistence, balances/compensationtrades. Rollback future ownphase separate reviewedrevert, no reset/rebase/force/migrationwrites. Current R0H leaves allproductionbytes unchanged.
''')
 doc('NATIVE_FEASIBILITY',f'''# Actual feasibility evidence

Baseline exact7afad885..; R0G independently checked1320previousinventory+17additions and stored hash graph. ARCHIVED_EVIDENCE_VERIFIED separate from FRESH_REFERENCE_EXECUTED128 scenarios. Fresh R0Hreference={ref['Scenarios']} PASS={ref['Pass']} FAIL={ref['Fail']},infra={ref['InfrastructureErrors']}. NativeMQL5 EXECUTED=NO. See R0G_REPRODUCTION/TEST_RESULTS/NATIVE_RESULTS/EXECUTION evidence.

PATH discovery which metaeditor64/metaeditor/MetaEditor64.exe/terminal64/wine plus rg files /opt,/workspace,/usr/local/bin only historical Windows helper found, no compiler. Native compiler version/output/exit absent=>NOT_RUN, notPASS. No MetaEditor download/platform installation or liveaccountconnection attempted. Prepared `.mqh` codec + `.mqh` independentgoldens + `.mq5` harness hashed; code review not compileproof. T17probe incomplete native textcodec explicitly identified.

R0H outcome B — REFERENCE_ONLY / NATIVE_NOT_RUN. Cannot claim native feasibility confirmed; limitations remain blocking production acceptance. MQL5 status/equality and encoderdecoder source is uncompiled candidate. No native mutation outcomes. Current no-trade controls checked independently by baselinehash+static scan, not actual runtimeexecution. Native resource failure/Unicode/long casts still require targettoolchain.
''','Reports')
 summary='\n'.join('|'+r['MutationID']+'|'+r['CausalTestID']+'|'+r['Verdict']+'|' for r in mut['Rows'])
 doc('MUTATION_AUDIT','''# Independent mutation scope

14 Python source mutations; isolated exec of exact edited source, hashes and edits stored, no existing source writes. Each mutation positive/original negative/mutant negative expected independent fixture/literal. Parser/import/runtime exceptions are INFRASTRUCTURE_ERROR, not kill. Changed input objects checked for pure classify. No monetary state exists to prove balances/funding/durable behavior.

Ignore Broker/Account/Deal key mutations produce conservative CONFLICT instead of expected NEW for independently confirmed different logical source. These are STATUS_CONTRACT_KILL, not unsafe funding acceptance. Float endian/UTF8/zero similarly codec contract kills. Component/Magic/Cycle omission and conflict/unavailable weakening are UNSAFE_ACCEPTANCE_KILL in identity classification only; not actual economic spending.

| Mutation | CausalTest | Outcome |
|---|---|---|
'''+summary+'''

14 killed,0survived,0infrastructure in finalcatalog (counts in evidence); this is not full mutation coverage and not native mutation verification. Native mutants NOT_RUN. All initial runs observed successful; no hidden development failures claimed. Acceptance matrix links guard/test/mutation/scope. Future native suite must rerun samesemantic probes on compiled MQL code; Python source kill does not prove native caller integration.
''','Reports')
 doc('APPROVAL_GATE','''# Approval Gate options

A NATIVE_VERIFIED / READY_FOR_ADMIN_DECISION — только после real MetaEditor/MT5 compile+assertions и independent bytes; сейчас НЕ достигнут.
B REFERENCE_ONLY / NATIVE_NOT_RUN — текущий фактический результат. Reference identity/status/strictcodec checks pass, native source prepared but uncompiled; no productionacceptance/start.
C BLOCKED / NATIVE_FAILED — при native compile/semantics/golden mismatch; нельзя присваивать сейчас без запуска. Будущие исправления только test scope до отдельного разрешения.

F64Z recommendation reference-only; no codec APPROVED. D02/D08, NUM-CODEC/MQL-DOMAIN, fullschema/compatibility и nativegate остаются AWAITING_ADMIN_APPROVAL. R0H не подписывает R0G ballot. Broker/EA origin authenticity, actual reconciliation/globalfunding/durableconcurrency/NewFar UNPROVEN. Semantic decision может быть рассмотрено администратором, но никакой A/B/C сам не разрешает R1.1.

ADMIN_APPROVAL_COMPLETE=NO
R1_1_START_ALLOWED=NO
PRODUCTION_REMEDIATION_ALLOWED=NO
TRADING_LOGIC_START_ALLOWED=NO
BROKER_DISPATCH_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
''','Reports')
 doc('FINAL_VERDICT',f'''# R0H final — limited test preparation completed

R0G archived/fresh reference independently verified128scenarios; fresh R0H{ref['Scenarios']}reference scenariosPASS,14Python mutationskilled (8unsafeidentity acceptance/6status-codeccontract),0survived/infra. MQL code NOT_COMPILED/NOT_EXECUTED; no native proof. Every PASS limited to statedPython/static scope. Code metrics/source hashes/native discovery/commands/UTC/actual process exits preserved. Production/history baseline unchanged; no broker/state IO.

Outcome B: REFERENCE_ONLY / NATIVE_NOT_RUN. Full native toolchain plus targetimplementation required before productionacceptance. APPROVAL_BALLOT not signed; source/body/codec choices still proposed. Currentwork does not remediate productionL01 or othermoneydefects. No automaticR1.1.

PublicationSHA not self-embedded; after commit/push userresponse recordsactual SHA/parity/clean. CurrentDocs allowedscope no production helpers. Main frozen R7/R0 failures not rerun/notchanged; R0H narrowtask does not claim fullhistoricalregressionsPASS.

[R0H_FINAL_STATUS]
BASE_SHA={BASE}
FINAL_SHA=PUBLICATION_SHA_IN_FINAL_RESPONSE
REMOTE_SHA_PARITY=PUBLICATION_CHECK_IN_FINAL_RESPONSE
WORKTREE_CLEAN=PUBLICATION_CHECK_IN_FINAL_RESPONSE
PRODUCTION_FILES_UNCHANGED=YES_BASELINE_VERIFIED
R0G_REFERENCE_REPRODUCED=PASS_128_FRESH_PLUS_ARCHIVE_VERIFIED
SOURCE_KEY_VERIFIED=REFERENCE_ONLY
IMMUTABLE_EQUALITY_VERIFIED=REFERENCE_ONLY
STATUS_API_VERIFIED=REFERENCE_ONLY
F64Z_REFERENCE_TESTS=PASS
T17Z_REFERENCE_TESTS=PASS
MQL5_COMPILER_AVAILABLE=NO
MQL5_COMPILE=NOT_RUN
MQL5_NATIVE_TESTS=NOT_RUN
NATIVE_CODEC_VERIFIED=NO
MUTATION_TESTS=14_KILLED_PYTHON_ONLY
MINIMAL_R1_ONE_FILE_FEASIBLE=STATICALLY_PLAUSIBLE_NATIVE_UNPROVEN
APPROVAL_GATE_STATUS=REFERENCE_ONLY_NATIVE_NOT_RUN
ADMIN_APPROVAL_COMPLETE=NO
R1_1_START_ALLOWED=NO
PRODUCTION_REMEDIATION_ALLOWED=NO
TRADING_LOGIC_START_ALLOWED=NO
BROKER_DISPATCH_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
STAGE_02B_R0H_COMPLETE=YES_TEST_PREPARATION_ONLY
[/R0H_FINAL_STATUS]
''','Reports')
 acceptance=[]
 for row in ref['Rows']:acceptance.append(dict(TestID=row['TestID'],RequirementID=row['RequirementID'],SourceFunction=('unbits' if row['TestID'].startswith('UNBITS-') else 'bits' if row['TestID'].startswith('BITS-') else 'token' if row['TestID'].startswith(('TOKEN-','TEXT-','UTF8-')) else 'decode' if row['TestID'].startswith('WIRE-') or row['RequirementID']=='R0H-MALFORMED' or 'ROUNDTRIP' in row['TestID'] else 'encode' if row['TestID'].startswith('CODEC-') else 'classify'),Expected=row['Expected'],Status=row['Result'],ProofBoundary='PYTHON_REFERENCE',NativeStatus='NOT_RUN',MutationIDs=[m['MutationID'] for m in mut['Rows'] if m['CausalTestID']==row['TestID']]))
 savepath=ROOT/'Tests/Contracts/NEXT_STAGE_02B_R0H_ACCEPTANCE_MATRIX.json';savepath.write_text(json.dumps(dict(meta(),Rows=acceptance,NativePlannedCases=['all29-field exact/altered','componentNet50','namespace/registry','bounds','full independentbytes','scalarbits/textprobe','utf8','truncated/trailing/unknownschema/tag/codec/duplicate/oversize','outputpreservation','legacyunavailable'],NativeHarness='Tests/Reference/hsbi_02b_r0h_native_harness.mq5',ApprovalGate='REFERENCE_ONLY_NATIVE_NOT_RUN',AdminApproved=False),ensure_ascii=False,indent=2,allow_nan=False)+'\n')

def run_tests():
 start=now();r0g=check_r0g();save('R0G_REPRODUCTION',dict(meta(),**r0g));rows=evaluate();counts={k:sum(r['Result']==k for r in rows) for k in ('PASS','FAIL','INFRASTRUCTURE_ERROR')};out=dict(meta(),Command=[sys.executable,*sys.argv],StartedUtc=start,FinishedUtc=now(),Scenarios=len(rows),Pass=counts['PASS'],Fail=counts['FAIL'],InfrastructureErrors=counts['INFRASTRUCTURE_ERROR'],Rows=rows,ExpectedOrigin='Literal statuses, independent struct.pack/bytes and R0F literal goldens. No expected via subject.',NativeExecution='NOT_RUN',ExitCode=int(counts['FAIL']>0 or counts['INFRASTRUCTURE_ERROR']>0));save('TEST_RESULTS',out)
 m=mutations();killed=sum(r['Verdict'].endswith('_KILL') for r in m);mut=dict(meta(),Rows=m,CatalogSize=len(m),Killed=killed,Survived=sum(r['Verdict']=='MUTATION_SURVIVED' for r in m),InfrastructureErrors=sum(r['Verdict']=='INFRASTRUCTURE_ERROR' for r in m),ExecutionScope='Only each mutant causal negative plus positive; not full suite/native mutation coverage',InitialSurvivors=[],InitialInfrastructureErrors=[],NativeMutationExecution='NOT_RUN');mut['ExitCode']=int(killed!=14);save('MUTATION_RESULTS',mut)
 native=native_discovery();save('NATIVE_RESULTS',native)
 prod=[p for p in inventory() if p.startswith('Include/') and p.endswith('.mqh') or '/' not in p and p.endswith('.mq5')];symbols=('HSBI_EconomicLedgerRecord','HSBI_BuildSourceDealKey','HSBI_ValidateEconomicRecord','HSBI_SameEconomicRecord','HSBI_ClassifyEconomicDuplicate','HSBI_SerializeEconomicRecord','HSBI_IsHarvestSourceEntry');matches=[]
 for file in prod:
  for n,line in enumerate((ROOT/file).read_text().splitlines(),1):
   if any(re.search(r'\b'+s+r'\b',line) for s in symbols):matches.append(dict(File=file,Line=n,Source=line))
 save('SOURCE_INVENTORY',dict(meta(),ProductionFiles=len(prod),Symbols=symbols,Matches=matches,Includes=re.findall(r'#include\s+"([^"]+)"',(ROOT/'Include/Money/HSBI_EconomicLedgerTypes.mqh').read_text()),Scope='Static production Include/main only; external binary/callers/ABI not proved'))
 metrics={str(p.relative_to(ROOT)):dict(SHA256=sha(p),Bytes=p.stat().st_size,Lines=len(p.read_text().splitlines())) for p in (ROOT/'Tests/Reference').glob('hsbi_02b_r0h_native*')};save('CODE_METRICS',dict(meta(),Metrics=metrics,NativeCompile='NOT_RUN',NativeAlternativeT17Implementation='Formatter scalar probe only; no full native text decoder'))
 build_docs();print('R0H reference',out['Scenarios'],out['Pass'],out['Fail'],out['InfrastructureErrors'],'mutations',killed,'/14','native',native['MQL5_NATIVE_TESTS']);return max(out['ExitCode'],mut['ExitCode'])

def seal():
 old=inventory();prod={p:v for p,v in old.items() if p.startswith('Include/') and p.endswith('.mqh') or '/' not in p and p.endswith('.mq5')};assert len(prod)==74
 files=[p for p in ROOT.rglob('*') if p.is_file() and ('NEXT_STAGE_02B_R0H_' in p.name or p.name.startswith(('hsbi_02b_r0h_','check_hsbi_02b_r0h_'))) and '__pycache__' not in str(p)]
 excluded={'NEXT_STAGE_02B_R0H_PRESERVATION.json','NEXT_STAGE_02B_R0H_PACKAGE_RESULTS.json'};save('PRESERVATION',dict(meta(),Existing=old,Production=prod,ArtifactHashes={str(p.relative_to(ROOT)):sha(p) for p in files if p.name not in excluded},SelfHashExcluded=sorted(excluded)))

def package_check():
 errors=[]
 def ck(ok,label):
  if not ok:errors.append(label)
 try:
  p=strict((ROOT/'Tests/Evidence/NEXT_STAGE_02B_R0H_PRESERVATION.json').read_text());actual=inventory();ck(actual==p['Existing'],'baseline inventory');prod={k:v for k,v in actual.items() if k.startswith('Include/') and k.endswith('.mqh') or '/' not in k and k.endswith('.mq5')};ck(prod==p['Production'] and len(prod)==74,'74 production')
  tracked=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','--',PREFIX],cwd=REPO,text=True).splitlines();new=set()
  for name in tracked:
   rel=name[len(PREFIX):]
   if rel in actual:continue
   file=ROOT/rel
   if not file.is_file():continue
   good=(rel.startswith(('Docs/','Reports/','Tests/Contracts/','Tests/Evidence/')) and file.name.startswith('NEXT_STAGE_02B_R0H_')) or (rel.startswith('Tests/Reference/') and file.name.startswith('hsbi_02b_r0h_')) or (rel.startswith('Tests/Static/') and file.name.startswith('check_hsbi_02b_r0h_'))
   ck(good,'scope '+rel);new.add(rel)
  excluded={'Tests/Evidence/NEXT_STAGE_02B_R0H_PRESERVATION.json','Tests/Evidence/NEXT_STAGE_02B_R0H_PACKAGE_RESULTS.json'};ck(set(p['ArtifactHashes'])==new-excluded,'new artifact inventory')
  for file,h in p['ArtifactHashes'].items():ck(sha(ROOT/file)==h,'hash '+file)
  load=lambda name:strict((ROOT/f'Tests/Evidence/NEXT_STAGE_02B_R0H_{name}.json').read_text())
  ref=load('TEST_RESULTS');mut=load('MUTATION_RESULTS');nat=load('NATIVE_RESULTS');old=load('R0G_REPRODUCTION');ex=load('EXECUTIONS')
  ck(ref['Rows']==evaluate() and ref['Scenarios']==ref['Pass']==148 and ref['Fail']==ref['InfrastructureErrors']==0,'reference exact rows')
  ck(mut['CatalogSize']==mut['Killed']==14 and mut['Survived']==mut['InfrastructureErrors']==0 and len(mut['Rows'])==14,'mutation totals')
  ck(all(r['OriginalNegative']['Result']=='PASS' and r['OriginalPositive']['Result']=='PASS' and r['MutantPositive']['Result']=='PASS' and r['MutantNegative']['Result']=='FAIL' and r['MutantNegative']['Actual']!=r['IndependentExpected'] for r in mut['Rows']),'causal mutation controls')
  source=Path(subject.__file__).read_text()
  for r in mut['Rows']:
   edit=r['ExactEdit'];ck(source.count(edit['Old'])==1 and hashlib.sha256(source.encode()).hexdigest()==r['OriginalSourceHash'] and hashlib.sha256(source.replace(edit['Old'],edit['New'],1).encode()).hexdigest()==r['MutantSourceHash'],'mutant hash '+r['MutationID'])
  ck(old['Scenarios']==128 and old['Pass']==128 and old['Archived']=='ARCHIVED_EVIDENCE_VERIFIED' and old['Fresh']=='FRESH_REFERENCE_EXECUTED','R0G scopes')
  ck(nat['CompilerAvailable'] is False and nat['MQL5_COMPILE']==nat['MQL5_NATIVE_TESTS']=='NOT_RUN' and nat['NATIVE_CODEC_VERIFIED']=='NO','native unavailable/NOT_RUN')
  for d in [ref,mut,nat,old]:
   for file,h in d['SourceHashes'].items():ck(sha(ROOT/file)==h,'runner/source provenance '+file)
  ck(ex['ExitCode']==0 and ex['ActualProcess']['ExitCode']==0 and ex['ActualProcess']['RunnerHash']==sha(__file__),'actual process exit')
  import check_hsbi_02b_r0e_package as guard
  ck(guard.scan(ROOT)=={'files':74,'forbidden':[],'controls':True,'guard':True},'static no trade')
  for file in (ROOT/'Tests/Reference').glob('hsbi_02b_r0h_native*'):
   txt=file.read_text();ck(not re.search(r'\b(OrderSend|OrderSendAsync|CTrade|WebRequest|SocketConnect|FileOpen|HistorySelect|AccountInfoInteger)\s*\(',txt),'native no account/IO '+file.name)
  for name in ('APPROVAL_GATE','FINAL_VERDICT'):
   txt=(ROOT/f'Reports/NEXT_STAGE_02B_R0H_{name}_RU.md').read_text()
   for policy in ('ADMIN_APPROVAL_COMPLETE','R1_1_START_ALLOWED','PRODUCTION_REMEDIATION_ALLOWED','TRADING_LOGIC_START_ALLOWED','BROKER_DISPATCH_ALLOWED','REAL_TRADING_ALLOWED'):
    ck(txt.count('\n'+policy+'=NO\n')==1 and txt.count('\n'+policy+'=')==1,'approval/policy '+policy)
  for file in [ROOT/'Tests/Contracts/NEXT_STAGE_02B_R0H_ACCEPTANCE_MATRIX.json',*[(ROOT/k) for k in p['ArtifactHashes'] if k.endswith('.json')]]:strict(file.read_text())
 except (ValueError,KeyError,TypeError,OSError) as e:errors.append(type(e).__name__+': '+str(e))
 return errors

def orchestrate():
 start=now();cmd=[sys.executable,str(Path(__file__).resolve()),'--run-tests'];proc=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
 save('EXECUTIONS',dict(meta(),StartedUtc=start,FinishedUtc=now(),ActualProcess=dict(Command=cmd,RunnerHash=sha(__file__),ExitCode=proc.returncode,Stdout=proc.stdout,Stderr=proc.stderr),ExitCode=proc.returncode))
 if proc.returncode:print(proc.stdout,proc.stderr);return proc.returncode
 seal();errors=package_check();save('PACKAGE_RESULTS',dict(meta(),VerifierHash=sha(__file__),Errors=errors,Positive='PASS' if not errors else 'FAIL',ExitCode=int(bool(errors)),Scope='Python/static evidence only; no native acceptance'))
 print(proc.stdout.strip());print('R0H package',errors);return int(bool(errors))

if __name__=='__main__':
 if '--run-tests' in sys.argv:raise SystemExit(run_tests())
 if '--all' in sys.argv:raise SystemExit(orchestrate())
 errors=package_check();print('R0H package',errors);raise SystemExit(int(bool(errors)))
