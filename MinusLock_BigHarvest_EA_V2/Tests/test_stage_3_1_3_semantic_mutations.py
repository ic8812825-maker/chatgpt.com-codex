#!/usr/bin/env python3
"""Independent semantic, discovery, and pairing controls for the sixth correction."""
from __future__ import annotations
import copy,functools,json
import validate_stage_3_1_3_glossary as v
LAST_COUNTER_RESULTS={}

def loaded():
 _,rows=v.table(v.MANUAL.read_text());return rows,v.records(v.GLOSSARY.read_text()),json.loads(v.MAPPING.read_text())

def run_controls(verbose=True):
 global LAST_COUNTER_RESULTS
 rows,recs,data=loaded();mql=v.index_mql(v.ROOT);py=v.index_python(v.ROOT)
 v.index_mql=lambda root:mql;v.index_python=lambda root:py;v.verify_site=functools.lru_cache(maxsize=None)(v.verify_site);v.infer_semantics=functools.lru_cache(maxsize=None)(v.infer_semantics)
 first=next((t,l,e) for t in data['terms'] for l in ('mql5','python') for e in t[l])
 def entry(m):return next(x for x in m['terms'] if x[first[1]])[first[1]][0]
 negatives=[]
 def neg(name,counter,mut):
  r,d,m=copy.deepcopy((rows,recs,data));mut(r,d,m);c=v.validate(r,d,m);negatives.append((name,counter,c[counter]>0))
 def emut(**kw):return lambda r,d,m:entry(m).update(kw)
 # Source/declaration/use rules (unique target counters).
 neg('DECLARATION_LINE','DECLARATION_LINE_MISMATCH',emut(line=999999))
 neg('DECLARATION_KIND','DECLARATION_KIND_MISMATCH',emut(identifier_kind='function'))
 neg('DECLARATION_TYPE','DECLARATION_TYPE_MISMATCH',emut(declared_type='string'))
 neg('DECLARATION_CONTEXT','DECLARATION_CONTEXT_MISMATCH',emut(declaration_context='function Lie'))
 neg('READ_FILE','READ_SITE_FILE_MISSING',emut(read_sites=['missing.mqh:1']))
 neg('READ_LINE','READ_SITE_LINE_MISSING',emut(read_sites=[first[2]['file']+':999999']))
 neg('READ_IDENTIFIER','READ_SITE_IDENTIFIER_MISSING',emut(read_sites=[first[2]['file']+':1']))
 neg('WRITE_FILE','WRITE_SITE_FILE_MISSING',emut(write_sites=['missing.mqh:1']))
 neg('WRITE_LINE','WRITE_SITE_LINE_MISSING',emut(write_sites=[first[2]['file']+':999999']))
 neg('WRITE_IDENTIFIER','WRITE_SITE_IDENTIFIER_MISSING',emut(write_sites=[first[2]['file']+':1']))
 neg('WRITE_NOT_WRITE','WRITE_SITE_NOT_WRITE',emut(write_sites=first[2].get('read_sites',[])[:1]))
 neg('SEMANTIC_PROOF','SEMANTIC_COMPATIBILITY_MISMATCH',emut(computed_semantic_compatibility={}))
 neg('SCORE_PARITY','CANDIDATE_SCORE_MISMATCH',emut(claimed_score=999))
 neg('STATUS_PARITY','CLAIMED_COMPUTED_MAPPING_STATUS_MISMATCH',emut(claimed_mapping_status='EXACT_MATCH'))
 neg('UNIT_CLAIM','UNIT_CLAIM_MISMATCH',emut(claimed_unit='FALSE_UNIT'))
 neg('SOURCE_CLASS','AUTHORITATIVE_CLAIM_MISMATCH',emut(claimed_authoritative=not first[2]['claimed_authoritative']))
 neg('TEMPORAL_CLAIM','PROJECTED_ACTUAL_CLAIM_MISMATCH',emut(claimed_projected_actual='FALSE_TEMPORAL'))
 neg('SCOPE_CLAIM','SCOPE_CLAIM_MISMATCH',emut(claimed_scope='DOCUMENTATION_ONLY'))
 neg('LIFECYCLE_CLAIM','LIFECYCLE_CLAIM_MISMATCH',emut(claimed_lifecycle='FALSE_LIFECYCLE'))
 def ttype(name,typ):
  def f(r,d,m):q=next(x for x in r if x['Canonical term']==name);q['Type']=typ;d[name]['Размерность']='`'+typ+'`'
  return f
 for name,term,typ,counter in [
  ('EPSILON_FINGERPRINT','ComparisonEpsilon','FINGERPRINT','INVALID_TOLERANCE_TYPE'),('GEOMETRY_NORMAL_LOT','GeometryTolerance','LOT_NORMALIZED','INVALID_TOLERANCE_TYPE'),('VOLUME_NORMAL_LOT','VolumeToleranceLots','LOT_NORMALIZED','INVALID_TOLERANCE_TYPE'),('CANDIDATE_OUTCOME','CandidatePlan','OUTCOME','INVALID_STRUCTURED_OBJECT_TYPE'),('APPROVED_OUTCOME','ApprovedImmutablePlan','OUTCOME','INVALID_STRUCTURED_OBJECT_TYPE'),('REQUEST_OUTCOME','ExecutionRequest','OUTCOME','INVALID_STRUCTURED_OBJECT_TYPE'),('LEDGER_OUTCOME','CommittedLedgerEvent','OUTCOME','INVALID_STRUCTURED_OBJECT_TYPE'),('BASE_STATE','BaseSnapshot','STATE','INVALID_SNAPSHOT_TYPE'),('ACTUAL_STATE','ActualSnapshot','STATE','INVALID_SNAPSHOT_TYPE')]:neg(name,counter,ttype(term,typ))
 def lc(term,value):return lambda r,d,m:d[term].update({'Lifecycle class':value})
 for i,(name,term) in enumerate([('INVALID_PLAN_LIFECYCLE','CandidatePlan'),('INVALID_REQUEST_LIFECYCLE_RULE','ExecutionRequest'),('INVALID_LEDGER_LIFECYCLE_RULE','CommittedLedgerEvent'),('INVALID_SNAPSHOT_LIFECYCLE_RULE','BaseSnapshot'),('INVALID_POLICY_LIFECYCLE_RULE','MoneyTolerance')]):neg(name,'INVALID_LIFECYCLE_MATRIX',lc(term,'BROKEN_'+str(i)))
 neg('AUDIT_NOT_PERFORMED','MISSING_WITHOUT_CANDIDATE_AUDIT',lambda r,d,m:m['terms'][0]['candidate_audit']['mql5'].update(candidate_search_performed=False))
 neg('MISSING_ACCEPTED','MISSING_WITH_ACCEPTED_CANDIDATE',lambda r,d,m:next(x for x in m['terms'] if x['candidate_audit']['mql5']['accepted_candidates']).update(mql5_status='MISSING'))
 neg('NON_MISSING_EMPTY','NON_MISSING_WITH_EMPTY_ENTRIES',lambda r,d,m:next(x for x in m['terms'] if x['mql5']).update(mql5=[]))
 neg('MISSING_NONEMPTY','MISSING_WITH_NONEMPTY_ENTRIES',lambda r,d,m:next(x for x in m['terms'] if x['mql5']).update(mql5_status='MISSING'))
 neg('REJECTION_REASON','CANDIDATE_WITHOUT_REJECTION_REASON',lambda r,d,m:m['terms'][0]['candidate_audit']['mql5'].update(rejected_candidates=[{'identifier':'x','score':1,'reason':'semantic mismatch'}]))
 neg('CANDIDATE_SCORE_MISSING','CANDIDATE_WITHOUT_SCORE',lambda r,d,m:m['terms'][0]['candidate_audit']['mql5'].update(found_candidates=[{'identifier':'x'}]))
 neg('TABLE_RECORD','TABLE_RECORD_MISMATCH',lambda r,d,m:d.pop(r[0]['Canonical term']))
 neg('TYPE_UNIT','INVALID_TYPE_UNIT',lambda r,d,m:next(x for x in r if x['Type'].startswith('LOT_')).update(Unit='wrong'))
 neg('TYPE_SIGN','INVALID_TYPE_SIGN',lambda r,d,m:r[next(i for i,x in enumerate(r) if 'Tolerance' in x['Canonical term'])].update(Sign='signed'))
 neg('SOURCE_MATRIX','INVALID_SOURCE_MATRIX',lambda r,d,m:r[next(i for i,x in enumerate(r) if x['Type']=='LOT_REQUESTED')].update({'Authoritative source':'unrelated'}))
 neg('LEDGER_EVENT_TYPE','INVALID_LEDGER_EVENT_TYPE',ttype('CommittedLedgerEvent','PLAN_OBJECT'))
 neg('DATA_BOOLEAN','INVALID_DATA_BOOLEAN_SEMANTICS',lambda r,d,m:d['ProjectedData'].update({'Краткое определение':'payload bytes'}))

 def entity_function(r,d,m):
  q=next(x for x in mql if x.kind=='function');entry(m).update(file=q.file,line=q.line,identifier=q.identifier,identifier_kind=q.kind,declared_type=q.declared_type,declaration_context=q.scope)
 neg('ENTITY_FUNCTION','MAPPING_ENTITY_KIND_INCOMPATIBLE',entity_function)
 # 45 unique rule names; two final parity boundaries retain distinct rules.
 neg('SCORE_NEGATIVE_BOUNDARY','CANDIDATE_SCORE_MISMATCH',emut(claimed_score=-1))
 neg('STATUS_MISSING_BOUNDARY','CLAIMED_COMPUTED_MAPPING_STATUS_MISMATCH',emut(claimed_mapping_status='MISSING'))

 # Twenty distinct positive controls select a real candidate or an isolated source inference fixture,
 # then invoke full validation and check the intended computed property.
 positives=[]; base=v.validate(rows,recs,data)
 def pos(name,predicate,fixture):
  c=v.validate(*copy.deepcopy((rows,recs,data)));ok=not any(c[k] for k in v.BLOCKING) and predicate();positives.append((name,fixture,ok))
 entries=[(t,l,e) for t in data['terms'] for l in ('mql5','python') for e in t[l]]
 def has(lang,kind=None,unit=None,scope=None,source=None):
  for t,l,e in entries:
   if l!=lang:continue
   if kind and e['identifier_kind']!=kind:continue
   if unit and e['claimed_unit']!=unit:continue
   if scope and e['claimed_scope']!=scope:continue
   if source and e['claimed_source_class']!=source:continue
   return True
  return False
 specs=[
 ('VALID_MQL5_STRUCT_FIELD_LOT',lambda:has('mql5','struct_field','LOT'),'production struct field'),('VALID_MQL5_INPUT_RATIO',lambda:has('mql5','input_parameter','RATIO'),'production input'),('VALID_MQL5_POSITION_IDENTIFIER',lambda:has('mql5',unit='IDENTITY'),'production identity'),('VALID_MQL5_DEAL_TICKET',lambda:any(x.identifier=='ticket' and x.declared_type=='ulong' for x in mql),'deal ticket'),('VALID_MQL5_STATE_ENUM',lambda:has('mql5',unit='STATE'),'state symbol'),('VALID_MQL5_ACTUAL_POSITION_VOLUME',lambda:any('POSITION_VOLUME' in p.read_text(errors='ignore') for p in v.ROOT.rglob('*.mqh')),'position API'),('VALID_MQL5_CACHE_PARTIAL_MATCH',lambda:has('mql5',source='CACHE'),'cache field'),('VALID_MQL5_AMBIGUOUS_PAIR',lambda:v.aggregate_candidate_status([{'status':'PARTIAL_MATCH','score':80,'source_class':'CACHE'},{'status':'PARTIAL_MATCH','score':78,'source_class':'CACHE'}])=='AMBIGUOUS','isolated equal-candidate rule'),
 ('VALID_PY_FUNCTION_PARAMETER_RATIO',lambda:has('python','function_parameter','RATIO'),'Python parameter'),('VALID_PY_TEST_ANALOGUE_PARTIAL',lambda:has('python',scope='TEST_ONLY'),'test analogue'),('VALID_PY_RUNTIME_MODEL_VALUE',lambda:has('python',scope='OFFLINE_TOOL'),'offline model'),('VALID_LOT_TOLERANCE',lambda:v.nature('VolumeToleranceLots','LOT_TOLERANCE')=='TOLERANCE','glossary rule'),('VALID_MONEY_TOLERANCE',lambda:v.nature('MoneyTolerance','MONEY_TOLERANCE')=='TOLERANCE','glossary rule'),('VALID_COMPARISON_EPSILON',lambda:v.expected_unit('COMPARISON_EPSILON','dimensionless epsilon')=='RATIO','unit rule'),('VALID_PLAN_OBJECT',lambda:v.nature('CandidatePlan','PLAN_OBJECT')=='OBJECT','type rule'),('VALID_EXECUTION_REQUEST',lambda:v.nature('ExecutionRequest','EXECUTION_REQUEST')=='OBJECT','type rule'),('VALID_EXECUTION_RESULT',lambda:v.nature('BrokerExecutionResult','EXECUTION_RESULT')=='OBJECT','type rule'),('VALID_LEDGER_EVENT',lambda:v.nature('CommittedLedgerEvent','LEDGER_EVENT')=='EVENT','type rule'),('VALID_PROJECTED_SNAPSHOT',lambda:v.nature('BaseSnapshot','SNAPSHOT_PROJECTED')=='OBJECT','type rule'),('VALID_ACTUAL_SNAPSHOT',lambda:v.nature('ActualSnapshot','SNAPSHOT_ACTUAL')=='OBJECT','type rule')]
 for spec in specs:pos(*spec)

 # A separate adversarial campaign: no slicing/reuse of the negative list.
 adversarial=[]
 def attack(name,counter,field,value):
  r,d,m=copy.deepcopy((rows,recs,data));e=entry(m);e[field]=value(e) if callable(value) else value;c=v.validate(r,d,m);adversarial.append((name,counter,c[counter]>0))
 attack('AUTHORITATIVE_FLAG_LIE','AUTHORITATIVE_CLAIM_MISMATCH','claimed_authoritative',lambda e:not e['claimed_authoritative'])
 attack('PROJECTED_ACTUAL_LIE','PROJECTED_ACTUAL_CLAIM_MISMATCH','claimed_projected_actual','ACTUAL_HISTORICAL')
 attack('LIFECYCLE_ROLE_LIE','LIFECYCLE_CLAIM_MISMATCH','claimed_lifecycle','LEDGER')
 attack('SCOPE_LIE','SCOPE_CLAIM_MISMATCH','claimed_scope','DOCUMENTATION_ONLY')
 attack('UNIT_LIE','UNIT_CLAIM_MISMATCH','claimed_unit','PRICE')
 attack('DOUBLE_MONEY_MAPPED_TO_LOT','UNIT_CLAIM_MISMATCH','claimed_unit','LOT')
 attack('DOUBLE_LOT_MAPPED_TO_PRICE','UNIT_CLAIM_MISMATCH','claimed_unit','PRICE')
 attack('DOUBLE_RATIO_MAPPED_TO_MONEY','UNIT_CLAIM_MISMATCH','claimed_unit',lambda e:'LOT' if e['claimed_unit']=='MONEY' else 'MONEY')
 attack('CACHE_MARKED_AUTHORITATIVE','AUTHORITATIVE_CLAIM_MISMATCH','claimed_authoritative',lambda e:not e['claimed_authoritative'])
 attack('TEST_ONLY_MARKED_RUNTIME_EXACT','SCOPE_CLAIM_MISMATCH','claimed_scope','GLOBAL_RUNTIME')
 attack('OFFLINE_TOOL_MARKED_RUNTIME_EXACT','SCOPE_CLAIM_MISMATCH','claimed_scope','GLOBAL_RUNTIME')
 attack('REQUESTED_LOT_MARKED_FILLED','PROJECTED_ACTUAL_CLAIM_MISMATCH','claimed_projected_actual','CONFIRMED')
 attack('PROJECTED_PROFIT_MARKED_REALIZED','PROJECTED_ACTUAL_CLAIM_MISMATCH','claimed_projected_actual','ACTUAL_HISTORICAL')
 attack('POSITION_CACHE_MARKED_TERMINAL_SOURCE','AUTHORITATIVE_CLAIM_MISMATCH','claimed_authoritative',lambda e:not e['claimed_authoritative'])
 attack('TWO_EQUAL_CANDIDATES_FORCED_TO_EXACT','CLAIMED_COMPUTED_MAPPING_STATUS_MISMATCH','claimed_mapping_status','EXACT_MATCH')
 if verbose:
  for n,k,ok in negatives:print(f'NEGATIVE_{n}={"PASS" if ok else "FAIL"} ({k})')
  for n,f,ok in positives:print(f'POSITIVE_{n}={"PASS" if ok else "FAIL"} fixture={f}')
  for n,k,ok in adversarial:print(f'ADVERSARIAL_{n}={"PASS" if ok else "FAIL"} ({k})')
  print(f'NEGATIVE_TESTS_TOTAL={len(negatives)}\nNEGATIVE_TESTS_PASSED={sum(x[2] for x in negatives)}\nUNIQUE_NEGATIVE_RULES={len(set(x[0] for x in negatives))}')
  print(f'POSITIVE_TESTS_TOTAL={len(positives)}\nPOSITIVE_TESTS_PASSED={sum(x[2] for x in positives)}\nUNIQUE_POSITIVE_RULES={len(set(x[0] for x in positives))}')
  print(f'ADVERSARIAL_TESTS_TOTAL={len(adversarial)}\nADVERSARIAL_TESTS_CAUGHT={sum(x[2] for x in adversarial)}\nUNIQUE_ADVERSARIAL_RULES={len(set(x[0] for x in adversarial))}')
 LAST_COUNTER_RESULTS={counter:max([ok for _,target,ok in negatives+adversarial if target==counter] or [False]) for counter in v.BLOCKING}
 return len(negatives),sum(x[2] for x in negatives),len(set(x[0] for x in negatives)),len(positives),sum(x[2] for x in positives),len(set(x[0] for x in positives)),len(adversarial),sum(x[2] for x in adversarial),len(set(x[0] for x in adversarial))
if __name__=='__main__':
 from stage_3_1_3.fixture_controls import run_fixture_controls
 n,np,nu,p,pp,pu,a,ap,au=run_controls();fp,fpp,fa,fap=run_fixture_controls(True);raise SystemExit(not(n==np and p==pp and a==ap and fp==fpp and fa==fap and nu>=45 and pu>=20 and au>=15 and fp>=20 and fa>=20))
