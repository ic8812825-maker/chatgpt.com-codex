#!/usr/bin/env python3
"""Narrow R0G literal identity/status tests + independent codec golden probes.
--build emits only new R0G decision artifacts. No production or historical writes.
"""
import sys,json,subprocess,hashlib,copy,struct,math,shutil
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];REPO=ROOT.parents[1];BASE='bcaa766568b9fe7eec0781a8c6efbb288cf16dae'
sys.path[:0]=[str(ROOT/'Tests/Reference'),str(ROOT/'Tests/Static')]
import hsbi_02b_r0g_identity_candidate as subject
import hsbi_02b_r0f_independent_fixtures as fixture
import hsbi_02b_r0f_contract_candidate as codec

def now():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def put(name,obj,folder='Tests/Evidence'):(ROOT/folder/f'NEXT_STAGE_02B_R0G_{name}.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def write(name,text,folder='Docs'):(ROOT/folder/f'NEXT_STAGE_02B_R0G_{name}_RU.md').write_text('\n'.join(x.rstrip() for x in text.rstrip().splitlines())+'\n')
def metadata():return dict(BaseSHA=BASE,TestedSHA=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),UTC=now(),SourceHashes={str(Path(p).relative_to(ROOT)):sha(p) for p in [__file__,subject.__file__,codec.__file__,fixture.__file__]},ApprovalStatus='AWAITING_ADMIN_APPROVAL')
def execute():
 rows=[]
 def check(i,expected,fn,inputs=None):
  try:
   actual=fn();result='PASS' if actual==expected else 'FAIL'
  except Exception as e:actual=type(e).__name__+': '+str(e);result='INFRASTRUCTURE_ERROR'
  rows.append(dict(TestID=i,RequirementID='R0G-'+('CODEC' if i.startswith('CODEC') else 'IDENTITY'),Input=inputs or i,Expected=expected,Actual=actual,Result=result,ProofBoundary='PYTHON_REFERENCE_ONLY'))
 r=fixture.record()
 def run(incoming=None,auth=None,reg=None,profile='HSBI-F64Z-1'):
  i=copy.deepcopy(r if incoming is None else incoming);a=copy.deepcopy({'Complete':True,'Record':r} if auth is None else auth);g=copy.deepcopy({'Complete':True,'Records':[r]} if reg is None else reg);before=copy.deepcopy((i,a,g));out=subject.classify(i,a,g,profile);assert (i,a,g)==before;return out
 check('IDENTITY-POSITIVE-EXACT','NO_OP',lambda:run())
 check('IDENTITY-CONFIRMED-ABSENT','NEW',lambda:run(reg={'Complete':True,'Records':[]}))
 check('IDENTITY-UNKNOWN-SOURCE','UNAVAILABLE',lambda:run(auth={'Complete':True,'Record':None}))
 check('IDENTITY-NO-HISTORY','UNAVAILABLE',lambda:run(auth={'Complete':False,'Record':r}))
 check('IDENTITY-NO-ABSENCE-PROOF','UNAVAILABLE',lambda:run(reg={'Complete':False,'Records':[]}))
 check('IDENTITY-LEGACY-UNKNOWN','UNAVAILABLE',lambda:run(reg={'Complete':True,'Records':[None]}))
 check('IDENTITY-DUPLICATE-INDEX','CONFLICT',lambda:run(reg={'Complete':True,'Records':[r,r]}))
 check('IDENTITY-FOREIGN-AUTHORITY','UNAVAILABLE',lambda:run(auth={'Complete':True,'Record':dict(r,AccountLogin=2)}))
 check('IDENTITY-SAME-NET-COMPONENTS','CONFLICT',lambda:run(dict(r,Profit=50.0,Commission=3.0))) # -2 swap -1 fee =>net50
 check('IDENTITY-LITERAL-50-VS-60','CONFLICT',lambda:run(dict(r,Profit=50.0,Swap=0.0,Fee=0.0,Commission=0.0),auth={'Complete':True,'Record':dict(r,Profit=60.0,Swap=0.0,Fee=0.0,Commission=-10.0)}))
 changes={'SchemaVersion':2,'Broker':'B2','Server':'S2','AccountLogin':2,'Symbol':'GBPUSD','Magic':8,'CycleID':2,'DealTicket':12,'OrderTicket':99,'PositionIdentifier':99,'ActionID':2,'EventID':32,'Role':'Small','EntryType':'IN','DealType':'BUY','TimestampMsc':100001,'Volume':2.0,'Price':1.5,'Profit':61.0,'Swap':-3.0,'Commission':-8.0,'Fee':-2.0,'DealNet':49.0,'Currency':'EUR','Precision':3,'SourcePlanApplicable':False,'SourcePlan':2,'SourcePolicyApplicable':False,'SourcePolicyVersion':2}
 for field,value in changes.items():
  changed=dict(r,**{field:value})
  if field=='SourcePlanApplicable':changed['SourcePlan']=None
  if field=='SourcePolicyApplicable':changed['SourcePolicyVersion']=None
  expected='UNAVAILABLE' if field in ('SchemaVersion','Broker','Server','AccountLogin','DealTicket') else 'CONFLICT'
  check('IDENTITY-FIELD-'+field,expected,lambda x=changed:run(x),{'Field':field,'Value':value})
  # Coherent request+authority alteration still conflicts with immutable registry, unless logical key truly differs.
  if field not in ('SchemaVersion','Broker','Server','AccountLogin','DealTicket'):
   check('IDENTITY-REGISTRY-'+field,'CONFLICT',lambda x=changed:run(x,auth={'Complete':True,'Record':x}))
 for name,value in [('bool',True),('zero',0),('negative',-1),('float',1.5),('string','1'),('overflow',2**64)]:
  check('ID-DEAL-'+name,'REJECT',lambda v=value:run(dict(r,DealTicket=v)))
 for field,value in [('AccountLogin',2**63),('Magic',-(2**63)-1),('TimestampMsc',2**63),('Precision',True)]:check('ID-BOUND-'+field,'REJECT',lambda f=field,v=value:run(dict(r,**{f:v})))
 for field,value in [('AccountLogin',2**63-1),('Magic',-(2**63)),('Magic',2**63-1),('DealTicket',2**64-1),('TimestampMsc',2**63-1)]:
  changed=dict(r,**{field:value});check('ID-VALID-'+field+'-'+str(value),'NO_OP',lambda x=changed:run(x,auth={'Complete':True,'Record':x},reg={'Complete':True,'Records':[x]}))
 for label,value in [('none',None),('bool',True),('empty',{}),('list',[])]:check('DTO-'+label,'REJECT',lambda v=value:subject.classify(v,None,None))
 for field in ('Broker','Profit','SourcePlan','Currency'):
  x=dict(r);del x[field];check('DTO-MISSING-'+field,'REJECT',lambda v=x:run(v))
 for field in ('Currency','Precision','SourcePlan'):check('UNKNOWN-'+field,'UNAVAILABLE',lambda f=field:run(dict(r,**{f:None})))
 check('AUTHORITY-MALFORMED','REJECT',lambda:run(auth={'Complete':1,'Record':r}))
 check('REGISTRY-MALFORMED','REJECT',lambda:run(reg={'Complete':True,'Records':{}}))
 check('CODEC-UNKNOWN','UNAVAILABLE',lambda:run(profile='unknown'))
 check('CODEC-A-SAME-SOURCE','NO_OP',lambda:run(profile='HSBI-T17Z-1'))
 for name,value,text,bits in fixture.GOLDENS:
  check('CODEC-B-'+name,bits,lambda v=value:codec.raw64_bits(v).to_bytes(8,'big').hex())
  check('CODEC-A-'+name,text,lambda v=value:codec.text17(v))
  check('CODEC-A-ROUNDTRIP-'+name,True,lambda v=value,t=text:float(t)==v)
 for profile,encoder,decoder in [('A',fixture.text_record,fixture.decoded_text),('B',fixture.binary_record,fixture.decoded_binary)]:
  expected=encoder(r).hex();check('CODEC-FULL-'+profile,expected,lambda p=profile:codec.encode_record(r,p).hex())
  check('CODEC-RECORD-ROUNDTRIP-'+profile,r,lambda p=profile,d=decoder:d(codec.encode_record(r,p)))
 for value in [float('nan'),float('inf'),-float('inf')]:
  check('CODEC-NONFINITE-'+str(value),'REJECT',lambda v=value:run(dict(r,Profit=v)))
 for name,text in [('cyrillic','Брокер'),('delimiter','B|:1'),('emoji','B😀')]:
  x=dict(r,Broker=text);check('CODEC-UTF8-'+name,fixture.binary_record(x).hex(),lambda v=x:codec.encode_record(v,'B').hex())
 check('CODEC-ZERO-EQUIVALENCE','NO_OP',lambda:run(dict(r,Fee=-0.0),auth={'Complete':True,'Record':dict(r,Fee=0.0)},reg={'Complete':True,'Records':[dict(r,Fee=0.0)]}))
 return rows

def build():
 common='BASE_SHA='+BASE+'\n\nPROPOSED / AWAITING_ADMIN_APPROVAL. Только подготовка Minimal R1.1; ни одного production изменения или утверждения.\n\n'
 source='Источники: `Include/Money/HSBI_EconomicLedgerTypes.mqh:6` struct, `:7` BuildSourceDealKey, `:8` ValidateEconomicRecord, `:9` SameEconomicRecord, `:10` ClassifyEconomicDuplicate, `:11` SerializeEconomicRecord, `:12` IsHarvestSourceEntry. R0F ECONOMIC_IDENTITY_SPEC/NUMERIC_CODEC_OPTIONS/R1_IMPLEMENTATION_SPEC; frozen `hsbi_02b_r0f_contract_candidate.py:record_shape/encode_record`; новые TestID в TEST_RESULTS.json.\n\n'
 admin=json.loads((ROOT/'Tests/Contracts/NEXT_STAGE_02B_R0F_ADMIN_DECISIONS.json').read_text())
 direct={'D-08','D-02','NUM-CODEC','MQL-DOMAIN'}
 reasons={
 'D-08':'Обязательно: key/EA origin нельзя подтверждать предъявленным payload. Применяется только boundary independent provider inputs, не реализация брокерского provider.',
 'D-02':'Обязательно: raw captured/source identity не является projected profit, reconciled posted net или available money. Equality не создаёт grant.',
 'NUM-CODEC':'Обязательно для authoritative serializer в данном candidate ballot. При отказе от codec нужен другой явно урезанный ballot equality-only; нельзя молча считать diagnostic string authoritative.',
 'MQL-DOMAIN':'Обязательно: типы long/ulong/double, finite/UTF8/resource bounds и exact equality должны быть заданы до native implementation.',
 'NUM-EXACT-1':'Ограниченно обязательно: exact immutable raw comparison/no epsilon. Полная арифметика settled/projected money не используется в локальной equality.',
 'NUM-DOMAIN-1':'Ограниченно обязательно: профиль raw binary64 и точные ID bounds; account balance domain/aggregation остаются позже.',
 'SNAP-FIXTURE-1':'Не требуется для pure equality/serialization: snapshot не часть economic body. Будущий provider receipt и current snapshot требуют отдельной интеграции.',
 'D-01':'Не блокирует локальную equality: нет allocate/consume или денег на выходе. Conservation остаётся обязательной при future funding.',
 'D-03':'Не блокирует equality: Role immutable проверяется, но право harvest/перевода не определяется. IsHarvestSourceEntry нельзя использовать как полное разрешение funding.',
 'D-04':'Не блокирует: FarLoss отсутствует в pure source identity API.',
 'D-05':'Не блокирует: batch risk/reset не исполняются, A/B/C остаются невыбранными.',
 'D-06':'Не блокирует: компоненты фиксируются отдельно, размеры/coverage costs и buffers не вычисляются.',
 'D-07':'Не блокирует локальную classification: NO_OP является сравнением, не durable exactly-once. Backend/CAS отсутствуют.',
 'CR-09':'Не блокирует: level/Catch-Up proof не вызывается и не создаётся.',
 'FUNDING-GLOBAL-ATTRIBUTION':'Не блокирует pure equality; глобальная уникальность funding НЕ доказана. NEW не разрешение credit, integration требует source-level unique index/CAS позже.',
 'BALANCE-SCHEMA-MAPPING':'Не блокирует: balance state не читается/не мигрирует. Economic legacy migration отдельно ограничена quarantine.'}
 decisions=[]
 for row in admin['Rows']:
  i=row['DecisionID'];decisions.append(dict(DecisionID=i,Class='DIRECT_BLOCKER' if i in direct else 'NARROW_SUBSET_REQUIRED' if i in ('NUM-EXACT-1','NUM-DOMAIN-1') else 'DEFERRED_FOR_LOCAL_IDENTITY',Reason=reasons[i],ApprovalStatus='AWAITING_ADMIN_APPROVAL'))
 fields=[]
 origin={'CycleID','ActionID','EventID','Role','SourcePlanApplicable','SourcePlan','SourcePolicyApplicable','SourcePolicyVersion'}
 broker={'Symbol','Magic','DealTicket','OrderTicket','PositionIdentifier','EntryType','DealType','TimestampMsc','Volume','Price','Profit','Swap','Commission','Fee'}
 for f in fixture.ORDER:
  authority='Independent EA-origin association journal' if f in origin else 'Broker history DEAL_* observation (scope BUY/SELL only)' if f in broker else 'Independent namespace binding/account currency+precision policy' if f in ('Broker','Server','AccountLogin','Currency','Precision') else 'Versioned approved schema registry' if f=='SchemaVersion' else 'Derived captured aggregate: not a broker DEAL_NET field; independent reconciliation boundary'
  fields.append(dict(Field=f,RequiredForIdentity=True,RequiredForAttribution=f in origin or f in ('Magic','Symbol','Broker','Server','AccountLogin','DealTicket'),RequiredForEconomicReconciliation=f in ('Profit','Swap','Commission','Fee','DealNet','Currency','Precision','Volume','Price','DealTicket','OrderTicket','PositionIdentifier','EntryType','DealType','TimestampMsc'),RequiredForSerialization=True,RequiredForMinimalR1=True,DeferredToLaterStages=False,SourceKey=f in ('Broker','Server','AccountLogin','DealTicket'),Authority=authority,OriginApplicability='Explicit NOT_APPLICABLE may encode None only when corresponding flag=False; unknown is not NOT_APPLICABLE' if f.startswith('Source') else 'Required',NativeType=('long positive' if f in ('AccountLogin','TimestampMsc') else 'long signed nonzero for attributed EA profile' if f=='Magic' else 'double finite (Volume/Price>0)' if f in codec.RAW else 'bool exact' if f.endswith('Applicable') else 'uint digits policy0..8 fixture only' if f=='Precision' else 'string/closed enum' if f in ('Broker','Server','Symbol','Role','EntryType','DealType','Currency') else 'ulong positive / explicit presence flag for optional origin')))
 approval=dict(metadata(),DecisionID='R1_1_MINIMAL_APPROVAL_BALLOT',ProductionBaseline=BASE,ProductionAllowlist=['Include/Money/HSBI_EconomicLedgerTypes.mqh'],IdentitySchemaCandidate='HSBI-EA-ECON-1 (29-field strict)',StatusApiCandidate='HSBI-ECON-CLASSIFY-2',CodecCandidate='HSBI-F64Z-1',AlternativeCodec='HSBI-T17Z-1',CandidateNotAdministratorSelection=True,RequiredDecisions=decisions,AdditionalRequiredContracts=['ECONOMIC-SCHEMA-1','LEGACY-COMPAT-1','NATIVE-ACCEPTANCE-1'],AdministratorDecision='',AllowedDecisions=['APPROVE_MINIMAL_R1_1','REJECT_MINIMAL_R1_1','RETURN_FOR_REVISION'],ApprovalStatus='AWAITING_ADMIN_APPROVAL',R1_1_START_ALLOWED=False)
 put('APPROVAL_MATRIX',approval,'Tests/Contracts');put('IDENTITY_MATRIX',dict(metadata(),Fields=fields,SourceKey=['Broker','Server','AccountLogin','DealTicket'],NoFundingPermission=True,CodecAdminApproved=False),'Tests/Contracts')
 table='| DecisionID | Minimal R1.1 dependency | Обоснование |\n|---|---|---|\n'+'\n'.join('|'+r['DecisionID']+'|'+r['Class']+'|'+r['Reason']+'|' for r in decisions)
 fieldtable='| Field | Identity | Attribution | Reconcile | Serialize | Minimal | Authority |\n|---|---|---|---|---|---|---|\n'+'\n'.join('|'+f['Field']+'|yes|'+str(f['RequiredForAttribution'])+'|'+str(f['RequiredForEconomicReconciliation'])+'|yes|yes|'+f['Authority']+'|' for f in fields)
 write('MINIMAL_IDENTITY_CONTRACT','# R0G — минимальный identity contract\n\n'+common+source+'''## R0G-ID-KEY-1 / R0G-ID-BODY-1

SourceKey=(Broker,Server,AccountLogin,DealTicket), без Symbol/Magic/Cycle/codec/schema в logical key. Broker — устойчивый provider namespace, НЕ автоматически ACCOUNT_COMPANY; Server exact identity без casefold/NFC. Не подставлять текущий terminal account в historical record. Account positive signed long; DealTicket positive ulong. Key tuple сериализуется typed lengths, не через неоднозначные delimiters.

Полный одинаковый supported payload при независимо подтверждённом source и complete registry =>NO_OP. Изменённый immutable body при прежнем key =>CONFLICT. Нет независимого source/ownership/complete registry =>UNAVAILABLE. NEW только когда independently confirmed body и complete logical registry доказывают отсутствие key; это NEW_IDENTITY, не money authorization. Неизвестный legacy не NEW. Codec/schema version никогда не новый доход. Изменение Magic/Cycle/Symbol/Role при прежнем key — conflict даже при согласованном новом proof.

Тесты IDENTITY-FIELD-*/REGISTRY-* меняют каждый field отдельно и согласованно request+authority при frozen ledger. Компоненты Profit50 Commission0 vs Profit60 Commission-10 (остальные0) оба Net50 =>CONFLICT (IDENTITY-LITERAL-50-VS-60). Float equality exact captured finite64; epsilon запрещена. +/-0 эквивалентны только в proposed Z profile; NaN/Infinity отвергаются. Нет raw round->posted и нет проверенного broker DECIMAL net в этой API.

## 29-field минимальный attributed envelope

R0G сознательно сохраняет все29 fields: удаление уже обязательных R0F origin/units/time фактов позволило бы молча ослабить equality или выдать unknown legacy за complete. Это минимальный безопасный envelope ДАННОГО HSBI-EA-ECON-1, не утверждение математической минимальности для всех брокерских сделок. При другой явно approved schema можно уменьшить набор, но нужны новый ballot и cross-schema mapping. SourcePlan/Policy имеют explicit applicability, unknown не FALSE. Ни один field не deferred; deferred именно provider/backend implementation, не типизированные факты.

'''+fieldtable+'''

Broker history даёт DEAL_TICKET/ORDER/POSITION_ID/SYMBOL/MAGIC/ENTRY/TYPE/TIME_MSC/VOLUME/PRICE/PROFIT/SWAP/COMMISSION/FEE. Не содержит HSBI Cycle/Action/EconomicEvent/Role/SourcePlan/Policy. Эти поля нужны из независимого EA-origin journal. DEAL_MAGIC сам по себе не доказывает association. DealNet — производный captured aggregate, не самостоятельный MQL5 DEAL_NET; его signed-components/posted reconciliation обязательно отдельно и не подменяется equal Net. Currency/precision из independent account/provider policy, не SYMBOL_DIGITS. Broker/server стабильность и receipt authenticity остаются UNPROVEN. Manual magic0/nontrade account events вне attributed BUY/SELL profile, но не исчезают из future global economic ledger.

Публичные identity helpers принимают записи, не ходят в History*/AccountInfo*, не создают origin journal и не признают fixture authority брокерским доказательством. Полнота/подтверждение задаются test fixtures, не реализованы в production.
''')
 write('CODEC_DECISION','# R0G — codec ballot alternatives\n\n'+common+source+'''Рекомендация-кандидат: HSBI-F64Z-1, альтернатива HSBI-T17Z-1. CODEC_ADMIN_APPROVED=NO. Оба профиля frozen R0F: порядок29 полей FIELDS/fixture.ORDER, имена typed, exact UTF8 bytes/no NUL, не NFC/casefold. Рекомендация не является выбором администратора.

| Property | F64Z | T17Z |
|---|---|---|
| Header | HSBI-F64Z-1 + NUL | HSBI-T17Z-1 + LF |
| String | s + uint32BE byteLength + UTF8 | s + decimal byteLength + : + UTF8 |
| Integer | u+uint64BE positive/nonnegative; i+signed64BE negative | i+canonical decimal length+:+integer; no leading zeros |
| Float | d+8-byte binary64BE | d+length+:+scientific17:1 digit,16 decimals,e±DDD |
| bool / absent applicable | b0/b1 / n | b0/b1 / n0: |
| +/-0 | normalized +0 (Z) | normalized +0 (Z) |
| Finite/subnormal | exact bits from normalization |17 significant digit roundtrip; canonical formatter must match exactly |
| Unknown schema/codec | UNAVAILABLE, no new source | UNAVAILABLE, no new source |
| Nonfinite/type invalid | REJECT | REJECT |
| UTF8/integer/roundtrip | Python literal + independent struct fixture | Python literal whole fixture + scientific vectors |
| Native implementation | Inline byte helpers possible; checked ulong shifts, no union assumption | Inline possible but exact decimal-digit generation/formatter difficult |
| MetaEditor acceptance | NOT_RUN, required blocker for production acceptance | NOT_RUN, required blocker for production acceptance |

Wire integer bounds не задают field domain: AccountLogin/TimestampMsc positive signed64; Magic signed nonzero EA profile; tickets positive ulong; flags bool; Precision fixture0..8 only. SchemaVersion1 supported; future positive version UNAVAILABLE, bool/0 malformed. Logical key excludes codec, comparison cross-known profiles decode to identical validated schema, unknown mapping UNAVAILABLE. Python status gate receives typed objects, НЕ декодирует недоверенные wire bytes. Fixture roundtrip decoders проверяют только known valid vectors.

F64 candidate основан на bounded exponent [-1074,1023],53significant bits. Native *2,/2 normalization и underflow/subnormal behavior требуется проверить, в том числе ulong>=2^63 и смену endian. Нет предположения, что MQL разрешает C union/pointer punning. T17: произвольная roundtrip строка не canonical; DoubleToString формат не считать доказанным до goldens. При несоответствии formatter минимальный scope надо вернуть на доработку, не добавлять header.

Предложенный native resource cap для обоих кандидатов: <=4096 UTF8 bytes на string, <=65536 bytes на record, prechecked total/length/allocations. Это технический proposed MQL domain для ballot, не broker универсальный limit; wire32 допускает больше, но oversized native input=>UNAVAILABLE без allocation. Проверять UTF16 surrogate→UTF8 mapping/terminating NUL exclusion. Строгий decoder проверяет truncation, exact fields/order/tags, duplicate/unknown/trailing bytes, length caps, canonical exponent/int. В R0G hostile decoder/native cap enforcement NOT_RUN (не реализованы в Python wrapper).

Golden source: R0F independent fixture.GOLDENS (8scalar vectors), literal Text17Expected/BitsExpected в R0F CODEC_GOLDENS.json, новые CODEC-* tests/UTF8/account bounds. Raw negative zero original sign не сохраняется Z; если требуется bit-exact raw packet, ни один Z профиль не подходит без другого решения.

Блокер: без MetaEditor нельзя доказать production compatibility. Это не препятствие подготовить ballot, но запрещает native PASS/приёмку будущего R1.1. Decimal/broker posting/settled integer conversion не часть source codec.
''')
 write('MQL5_API_SPEC','# R0G — предлагаемые MQL5 signatures, не production code\n\n'+common+source+'''## R0G-STATUS-2

Статусы versioned enum `HSBI_EconomicIdentityStatusV2`: NEW=0, NO_OP=1, CONFLICT=2, REJECT=3, UNAVAILABLE=4. Значения0/1/2 исторически совпадают, но V2 enum НЕ совместим семантически с legacy int без явного caller review.

| Status | Precise scope |
|---|---|
| NEW | Полный подтверждённый incoming source, complete reconciled logical registry, key отсутствует; только new identity, не funding |
| NO_OP | Supported exact same immutable body по independently confirmed logical key и existing registry; zero state delta |
| CONFLICT | Изменённый immutable payload при известном key, либо противоречивый/дублированный registry |
| REJECT | Malformed input/type/known invalid enum/nonfinite/out-of-range ID; zero delta |
| UNAVAILABLE | Unknown schema/codec/legacy/missing independent source/namespace/origin/currency/precision/absence proof; не NEW |

Приоритет: shape incoming -> codec support -> shape/completeness authority+registry -> independent source key -> body conflict -> registry validation/uniqueness -> NEW/NO_OP/CONFLICT. Все решения pure; authoritative source с другим logical key не доказывает incoming, даёт UNAVAILABLE. Authority DTO malformed=>REJECT; unknown provider facts=>UNAVAILABLE. Unknown ledger schema/entry blocks absence, unknown key migration не создаёт source. Duplicate registry rows требуют reconciliation даже при одинаковом payload.

## Точные предлагаемые сигнатуры

```cpp
enum HSBI_EconomicIdentityStatusV2 { HSBI_ECON_V2_NEW=0, HSBI_ECON_V2_NO_OP=1, HSBI_ECON_V2_CONFLICT=2, HSBI_ECON_V2_REJECT=3, HSBI_ECON_V2_UNAVAILABLE=4 };
HSBI_EconomicIdentityStatusV2 HSBI_ValidateEconomicRecordV2(const HSBI_EconomicLedgerRecordV2 &record, string &reason);
bool HSBI_SameEconomicSourceKeyV2(const HSBI_EconomicLedgerRecordV2 &a, const HSBI_EconomicLedgerRecordV2 &b);
HSBI_EconomicIdentityStatusV2 HSBI_CompareEconomicPayloadV2(const HSBI_EconomicLedgerRecordV2 &existing, const HSBI_EconomicLedgerRecordV2 &incoming, string &reason);
HSBI_EconomicIdentityStatusV2 HSBI_ClassifyEconomicIdentityV2(const HSBI_EconomicLedgerRecordV2 &incoming, const HSBI_EconomicAuthorityViewV2 &authority, const HSBI_EconomicRegistryViewV2 &registry, const string codecId, string &reason);
HSBI_EconomicIdentityStatusV2 HSBI_EncodeEconomicRecordV2(const HSBI_EconomicLedgerRecordV2 &record, const string codecId, uchar &bytes[], string &reason);
HSBI_EconomicIdentityStatusV2 HSBI_DecodeEconomicRecordV2(const uchar &bytes[], const string codecId, HSBI_EconomicLedgerRecordV2 &record, string &reason);
```

Validate/Encode/Decode successful result=NO_OP как `validated/no state operation`, не NEW credit; Compare same key exact=>NO_OP, altered=>CONFLICT, distinct key=>UNAVAILABLE (caller cannot infer registry absence). Key bool true только validated keys; false не NEW. Classify — единственный identity-level NEW. Все output refs при error остаются неизменными, reason может обновляться; Decode uses temporary validated body then assignment. No exceptions-as-success. Новые structs/views в том же header: V2body29fields, optional SourcePlan/Policy presence bool; RegistryView содержит complete flag+record array; AuthorityView содержит independentConfirmed/available flags+record, namespace receipt reference/provider version. Flags/reference не доказывают broker authenticity: только boundary contract; Classify проверяет shapes и body binding.

Для C-like MQL API нет Python None: unknown namespace/units/origin/legacy задаются explicit typed completeness/presence status в envelope; их нельзя default-initialize в known. Только producer независимого provider может ставить confirmed; в R1.1 provider не реализуется. SourceKey equality не использует sourceDealKey legacy cache. Все helpers inline в одном разрешённом header после отдельного задания.

## Legacy compatibility (R0G-COMPAT-1)

Старая struct и все7 имён/сигнатур сохраняются. BuildSourceDealKey/Validate/Same/Classify/Serialize/IsHarvestSourceEntry/record — diagnostic-only для старой схемы; старая Classify возвращает0/1/2 с прежней diagnostic семантикой. Не переопределять0 как безопасный NEW. Никаких implicit overload/adapters legacy→V2/UNAVAILABLE→NEW. Любой старый diagnostic int не разрешён как proof/funding decision. Только V2 используется новым harness/API. Для неизвестного legacy V2 conversion возвращает UNAVAILABLE, без current account fallback и fabricated milliseconds.

Это additive remediation proposal: устраняет L01 в новом typed approved surface, не делает старую unsafe equality безопасной. Пока есть возможный external consumer старого Classify как financial authority, Minimal approval недостаточно — caller integration/расширение allowlist отдельным заданием. Static rg по текущим Include/main нашёл legacy symbols только в самом header; это не гарантия внешних программ. Сохранение old diagnostic algorithm требует явного принятия compatibility policy администратором; при требовании исправить старый financial path без V2 нужен другой ballot.
''')
 write('MINIMAL_DIFF_PLAN','# R0G — one-file diff и native acceptance plan\n\n'+common+source+'''Единственный future production path: `Include/Money/HSBI_EconomicLedgerTypes.mqh`. Текущий R0G не создаёт production structures/helpers. Статическая возможность one-file есть: все новые structs/enums/functions могут объявляться inline в этом header; нет production external calls найденных rg. Header-only plan не доказательство MetaEditor compatibility.

| Existing / new | Future diff |
|---|---|
| HSBI_EconomicLedgerRecord :6 | Сохранить старую struct/layout. Add separate HSBI_EconomicLedgerRecordV2 с29fields, не дописывать молча old serialized records |
| old Build/Validate/Same/Classify/Serialize :7–11 | Сохранить сигнатуры и диагностическую legacy семантику; пометка diagnostic-only в comments, no new proof callers |
| old IsHarvestSourceEntry :12 | Не менять source-role economics; diagnostic helper не funding gate |
| New namespace/validate/key/compare/classifier | V2 strict contracts/statuses; no epsilon, no implicit identity copies |
| New encode/decode helpers | Approved candidate F64Z inline; bounded lengths, finite double, unsigned/signed checks, buffers temp→output only on success |
| New view/envelope types | Independent authority/registry completeness and explicit unknown; no provider IO/backend/CAS |
| Legacy adapter if needed | Read-only explicit unavailable for missing fields, no invented enrichment; keep raw record bytes outside financial proof |

Добавляются SchemaVersion,Broker,Server,AccountLogin,DealType,TimestampMsc,Currency,Precision,SourcePlanApplicable/SourcePlan/SourcePolicyApplicable/SourcePolicyVersion в отдельный V2, исходные IDs/роль/volume/price/components/net переносятся только при independent validation. `valid=true`/sourceDealKey не authority. EA Role enum↔wire closed string mapping versioned explicit; unsupported role=>UNAVAILABLE or known invalid=>REJECT, no numeric guessing. Timestamp old datetime seconds не равен доказанным millis.

Минимальный patch не реализует двойной funding protection. Он исключает ложный NEW из codec/key/legacy classification в заявленном V2 gate. Существование глобального logical-source unique registry, CAS и funding integration остаётся UNPROVEN; не обещать их исправление одним header. Direct equality API не выдаёт NEW; future funding caller обязан вызывать registry-aware classifier + economic reconciliation + actual durable allocation authorization. В R1.1 никакие balance grants не создаются.

## NATIVE-ACCEPTANCE-1 (будущий отдельный этап)

1. Зафиксировать MetaEditor build, OS, command и compiler logs; production main mq5 compile в copied output workspace, source hashes неизменны кроме allowlisted header. Exit0+0errors обязательны; warnings описать. Не считать g++ equivalent.
2. Новый test-only MQL5 assertion script (после отдельного разрешения Tests path; без OnTick/dispatch): include EconomicLedgerTypes, initialize all explicit facts/views, no broker History/OrderSend.
3. long boundaries ±2^63/Magicnonzero; positive Account/Timestamp; ulong1..2^64-1 и overflow conversion отказ; bool не parse ID. Native DTO typed fields не позволяют некоторые Python bool-integer cases, но wire parser обязан отвергать wrong tags.
4. Все CODEC-GOLDEN vectors, +0/-0/subnormal/maxfinite, NaN/Infinityrejection, exact exponent/UTF8 byte lengths. Native endian, shifts, locale, NUL and Unicode surrogate handling. Unknown schema/codec=>UNAVAILABLE.
5. Source namespace variation, all29 per-field exact/altered comparisons; components50/0 vs60/-10 sameNet=>CONFLICT. Same key changed Magic/Cycle неNEW.
6. NEW только independent confirmed+complete registry absence; missing/legacy/source mismatch=>UNAVAILABLE, malformedREJECT. Empty or duplicate registry semantics verified.
7. Native encoder/decoder positive roundtrip плюс corrupted/truncated/duplicate/trailing/wrong tags/oversize tests (reference fixture decode сейчас не это доказательство). Output refs unchanged on errors.
8. Old struct/function signatures compile compatibility diagnostic-only; adapter never returns NEW for unknown legacy. Existing frozen test failures классифицировать, не переписывать.
9. Assertions pass counts and actual exit/platform/tester logs capture. Нативные assertion failures должны иметь machine-detectable failure status; terminal script stop сам по себе не PASS.
10. Diff onlyone production path; no new include headers/main/runtime edits. Hash/static scan no OrderSend/CTrade/OnTick trading/persistence. No real broker/tests on live account.

MetaEditor/MT5 не найдены в PATH и searched /opt,/workspace,/usr/local/bin; только historical Windows compile script вне scope. Native compile/tests/StrategyTester=NOT_RUN. Native tests — обязательный blocker будущей production приёмки; до отдельного задания не запускать платформу/сделки.

Stop: missing admin decision/baseline drift, malformed authority, required data missing, unknown codec, native mismatch/errors, need other production file, unexplained test failure, security rule bypass requirement. Не расширять allowlist скрыто. Rollback будущего phase commit отдельным reviewed revert; preserve old/new payload/schema. Не reset/rebase/force и не денежные compensation trades. Никаких actual storage migrations в Minimal.
''')
 write('APPROVAL_BALLOT','# R1_1_MINIMAL_APPROVAL_BALLOT\n\n'+common+'''ProductionBaseline: '''+BASE+'''
ProductionAllowlist: Include/Money/HSBI_EconomicLedgerTypes.mqh
IdentitySchemaCandidate: HSBI-EA-ECON-1 (все29 fields, explicit origin applicability)
StatusApiCandidate: HSBI-ECON-CLASSIFY-2 (NEW/NO_OP/CONFLICT/REJECT/UNAVAILABLE)
CodecCandidate: HSBI-F64Z-1
AlternativeCodec: HSBI-T17Z-1
CompatibilityCandidate: additive V2; legacy diagnostic-only; no implicit adapters
NumericAssumptions: positive signed Account/Timestamp; signed nonzero Magic; ulong IDs; finite binary64/Z-zero; known currency/precision; UTF8 native caps4096/65536 bytes proposed
ApprovalStatus: AWAITING_ADMIN_APPROVAL
AdministratorDecision:
AdministratorName:
DecisionTimestamp:

**Формулировка для администратора:** «Рассматриваю HSBI-EA-ECON-1, V2 status API, F64Z candidate и additive diagnostic legacy policy в пределах указанного одного header. Даже при выборе APPROVE_MINIMAL_R1_1 необходимы отдельное явное implementation задание, актуальный baseline gate и успешная native приёмка. Это не разрешение на funding, trading, runtime/persistence/provider integration». Администратор может выбрать альтернативный T17Z только явным изменением ballot candidate/версии и native acceptance требований, не молчаливой подстановкой.

Варианты ответа (ни один не выбран): APPROVE_MINIMAL_R1_1 / REJECT_MINIMAL_R1_1 / RETURN_FOR_REVISION.

KnownLimitations: broker/source-origin authenticity UNPROVEN; full semantic reconciliation/native codec implementation NOT_RUN; source-level/global funding/CAS/durable restart/NewFar not implemented. No flag becomes provider evidence. Full account nontrade/manual events вне EA-attributed profile.

DeferredDependencies: D01/03/04/05/06/07/CR09/funding/balance mapping не утверждаются этим ballot. Узкие NUM-EXACT/DOMAIN assertions нужны, не вся money architecture. Detailed reasons — approval matrix и blocker analysis.

NativeRequirements: main mq5 compile и scoped assertion harness, golden vectors/hostile decode/field mutations/backward compatibility/no trade (NATIVE-ACCEPTANCE-1).
Rollback: separate reviewed revert of own future R1.1 phase, preserve observations, no migration writes/reset/force/compensation trades.
StopConditions: unapproved schema/status/codec/compatibility; missing data; different baseline; native test unavailable for acceptance; out-of-allowlist change; conflicting evidence/security publication refusal.

ADMIN_APPROVAL_COMPLETE=NO
R1_1_START_ALLOWED=NO
PRODUCTION_REMEDIATION_ALLOWED=NO
TRADING_LOGIC_START_ALLOWED=NO
BROKER_DISPATCH_ALLOWED=NO
REAL_TRADING_ALLOWED=NO
''','Reports')
 write('BLOCKER_ANALYSIS','# R0G — узкие предпосылки Minimal R1.1\n\n'+common+source+table+'''

Дополнительные обязательные approvals: ECONOMIC-SCHEMA-1 (29fields/key/provenance envelope), LEGACY-COMPAT-1 (old diagnostics vs V2 financial prohibition), NATIVE-ACCEPTANCE-1. Это технические уточнения R0F, не новая экономическая policy. Все16 прежних decisions остаются AWAITING, в R0G ничего автоматически не approved.

Есть разница между готовностью пакета решения и готовностью production приёмки. Native codec/API tests отсутствуют => production acceptance BLOCKED; администратор может рассмотреть conditional contract decision, но start всё равно NO до отдельного задания. Независимый broker/EA origin provider не реализуется в одном header; future classifier получает типизированные независимые view и доказывает только body/lookup binding. Полная provenance chain не доказана.

C3 cost status gap не блокирует local identity equality, потому cost API в этом scope не вызывается. R7/R0 historical FAIL остаются frozen; R0G не повторяет общий аудит/полную regression suite и не объявляет их исправленными. R0F16/package preservation проверяются новым read-only checker; отдельные нативные/runtime регрессии NOT_RUN.

One-file additive API технически описуем без новых helper headers. Однако если обязательная цель — переподключить действующий external financial consumer, заменить unsafe legacy classifier либо выполнить provider/durable funding, это другой scope и blocker. Нет скрытого объявления старого дефекта исправленным: production неизменён, новая Python модель не remediation.
''','Reports')

if __name__=='__main__':
 if '--build' in sys.argv:build()
 else:
  started=now();rows=execute();out=dict(metadata(),Command=[sys.executable,*sys.argv],StartedUtc=started,FinishedUtc=now(),Scenarios=len(rows),Pass=sum(r['Result']=='PASS' for r in rows),Fail=sum(r['Result']=='FAIL' for r in rows),InfrastructureErrors=sum(r['Result']=='INFRASTRUCTURE_ERROR' for r in rows),Rows=rows,Contexts='NOT_APPLICABLE: raw identity/codec only, no Decimal arithmetic',MQL5_COMPILE='NOT_RUN',MQL5_NATIVE_TESTS='NOT_RUN',STRATEGY_TESTER='NOT_RUN');out['ExitCode']=int(out['Fail'] or out['InfrastructureErrors']);put('TEST_RESULTS',out);print('R0G',out['Scenarios'],out['Pass'],out['Fail'],out['InfrastructureErrors']);print([r for r in rows if r['Result']!='PASS']);raise SystemExit(out['ExitCode'])
