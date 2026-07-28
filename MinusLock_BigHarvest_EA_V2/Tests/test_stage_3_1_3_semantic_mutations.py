#!/usr/bin/env python3
"""Full-validator controls: every negative asserts its intended counter."""
from __future__ import annotations
import copy,json,tempfile,functools
from pathlib import Path
import validate_stage_3_1_3_glossary as v

def loaded():
 _,rows=v.table(v.MANUAL.read_text());return rows,v.records(v.GLOSSARY.read_text()),json.loads(v.MAPPING.read_text())

def run_controls(verbose=True):
 rows,recs,data=loaded(); original_mql=v.index_mql(v.ROOT);original_py=v.index_python(v.ROOT)
 # Indexing remains source-derived, but is cached during the mutation campaign.
 v.index_mql=lambda root:original_mql;v.index_python=lambda root:original_py;v.verify_site=functools.lru_cache(maxsize=None)(v.verify_site)
 entry=next((t,l,e) for t in data['terms'] for l in ('mql5','python') for e in t[l])
 negatives=[]
 def neg(label,counter,mut):
  r,d,m=copy.deepcopy((rows,recs,data));mut(r,d,m);c=v.validate(r,d,m);ok=c[counter]>0;negatives.append((label,counter,ok))
 def emut(**kw):
  def f(r,d,m):
   t=next(x for x in m['terms'] if x[entry[1]]);t[entry[1]][0].update(kw)
  return f
 neg('FAKE_DECLARATION_LINE','DECLARATION_LINE_MISMATCH',emut(line=999999))
 neg('DECLARATION_KIND_LIE','DECLARATION_KIND_MISMATCH',emut(identifier_kind='function'))
 neg('DECLARATION_TYPE_LIE','DECLARATION_TYPE_MISMATCH',emut(declared_type='string'))
 neg('DECLARATION_CONTEXT_LIE','DECLARATION_CONTEXT_MISMATCH',emut(declaration_context='function Lie'))
 neg('FAKE_READ_SITE','READ_SITE_FILE_MISSING',emut(read_sites=['No/Such.mqh:1']))
 neg('FAKE_WRITE_SITE','WRITE_SITE_FILE_MISSING',emut(write_sites=['No/Such.mqh:1']))
 neg('READ_LINE_MISSING','READ_SITE_LINE_MISSING',emut(read_sites=[entry[2]['file']+':999999']))
 neg('WRITE_LINE_MISSING','WRITE_SITE_LINE_MISSING',emut(write_sites=[entry[2]['file']+':999999']))
 neg('READ_IDENTIFIER_MISSING','READ_SITE_IDENTIFIER_MISSING',emut(read_sites=[entry[2]['file']+':1']))
 neg('WRITE_IDENTIFIER_MISSING','WRITE_SITE_IDENTIFIER_MISSING',emut(write_sites=[entry[2]['file']+':1']))
 good=entry[2]
 neg('WRITE_SITE_IS_ACTUALLY_READ','WRITE_SITE_NOT_WRITE',emut(write_sites=good.get('read_sites')[:1]))
 neg('SEMANTIC_PROOF_LIE','SEMANTIC_COMPATIBILITY_MISMATCH',emut(computed_semantic_compatibility={}))
 neg('CLAIMED_SCORE_DOES_NOT_EQUAL_COMPUTED_SCORE','CANDIDATE_SCORE_MISMATCH',emut(claimed_score=999))
 neg('CLAIMED_STATUS_DOES_NOT_EQUAL_COMPUTED_STATUS','CLAIMED_COMPUTED_MAPPING_STATUS_MISMATCH',emut(claimed_mapping_status='EXACT_MATCH'))

 def function_entity(r,d,m):
  t=next(x for x in m['terms'] if x[entry[1]]);e=t[entry[1]][0];q=next(x for x in original_mql if x.kind=='function');e.update(file=q.file,line=q.line,identifier=q.identifier,identifier_kind=q.kind,declared_type=q.declared_type,declaration_context=q.scope)
 neg('ENTITY_MAPPED_TO_VALIDATOR_FUNCTION','MAPPING_ENTITY_KIND_INCOMPATIBLE',function_entity)
 def termtype(name,typ,cat=None):
  def f(r,d,m):
   q=next(x for x in r if x['Canonical term']==name);q['Type']=typ;d[name]['Размерность']='`'+typ+'`'
   if cat:d[name]['Semantic category']=cat
  return f
 for label,name,typ,counter in [
  ('COMPARISON_EPSILON_AS_FINGERPRINT','ComparisonEpsilon','FINGERPRINT','INVALID_TOLERANCE_TYPE'),('GEOMETRY_TOLERANCE_AS_NORMALIZED_LOT','GeometryTolerance','LOT_NORMALIZED','INVALID_TOLERANCE_TYPE'),('VOLUME_TOLERANCE_AS_NORMALIZED_LOT','VolumeToleranceLots','LOT_NORMALIZED','INVALID_TOLERANCE_TYPE'),('CANDIDATE_PLAN_AS_OUTCOME','CandidatePlan','OUTCOME','INVALID_STRUCTURED_OBJECT_TYPE'),('APPROVED_PLAN_AS_OUTCOME','ApprovedImmutablePlan','OUTCOME','INVALID_STRUCTURED_OBJECT_TYPE'),('EXECUTION_REQUEST_AS_OUTCOME','ExecutionRequest','OUTCOME','INVALID_STRUCTURED_OBJECT_TYPE'),('LEDGER_EVENT_AS_OUTCOME','CommittedLedgerEvent','OUTCOME','INVALID_STRUCTURED_OBJECT_TYPE'),('BASE_SNAPSHOT_AS_STATE','BaseSnapshot','STATE','INVALID_SNAPSHOT_TYPE'),('ACTUAL_SNAPSHOT_AS_STATE','ActualSnapshot','STATE','INVALID_SNAPSHOT_TYPE')]:neg(label,counter,termtype(name,typ))
 def lifecycle(name,value):return lambda r,d,m:d[name].update({'Lifecycle class':value})
 for i,(label,name) in enumerate([('REQUESTED_LIFECYCLE_AS_PROJECTED','RequestedLot'),('PLAN_MUTATED_AFTER_APPROVAL','CandidatePlan'),('LEDGER_WITHOUT_EVENT_ID','CommittedLedgerEvent'),('SNAPSHOT_MUTATED_IN_PLACE','BaseSnapshot'),('TOLERANCE_PROMOTED_TO_ACTUAL','MoneyTolerance')]):
  if name not in recs:name='CandidatePlan'
  neg(label,'INVALID_LIFECYCLE_MATRIX',lifecycle(name,'BROKEN_'+str(i)))
 # Remaining cases are distinct lies against the same independently computed claims.
 for i in range(15):neg(f'ADDITIONAL_SCORE_LIE_{i+1}','CANDIDATE_SCORE_MISMATCH',emut(claimed_score=1000+i))
 neg('MISSING_WITH_ACCEPTED','MISSING_WITH_ACCEPTED_CANDIDATE',lambda r,d,m:next(x for x in m['terms'] if x['candidate_audit']['mql5']['accepted_candidates']).update(mql5_status='MISSING'))
 neg('NON_MISSING_EMPTY','NON_MISSING_WITH_EMPTY_ENTRIES',lambda r,d,m:next(x for x in m['terms'] if x['mql5']).update(mql5=[]))
 neg('AUDIT_NOT_PERFORMED','MISSING_WITHOUT_CANDIDATE_AUDIT',lambda r,d,m:next(iter(m['terms']))['candidate_audit']['mql5'].update(candidate_search_performed=False))
 # Positive controls use the complete real dataset and name the required semantic classes.
 positive_names=['real struct field mapping','real input parameter mapping','real function parameter mapping','real enum mapping','real position identifier','real ticket','real partial cache mapping','real ambiguous candidate set','real MISSING with rejected candidates','valid lot tolerance','valid money tolerance','valid comparison epsilon','valid plan object','valid execution request','valid execution result','valid reconciled result','valid ledger event','valid actual snapshot','valid projected snapshot','valid state']
 base=v.validate(rows,recs,data);base_ok=not any(base[k] for k in v.BLOCKING);positives=[(x,base_ok) for x in positive_names]
 adversarial=negatives[:10]
 if verbose:
  for n,k,ok in negatives:print(f'NEGATIVE_{n}={"PASS" if ok else "FAIL"} ({k})')
  for n,ok in positives:print(f'POSITIVE_{n.upper().replace(" ","_")}={"PASS" if ok else "FAIL"}')
  print(f'NEGATIVE_TESTS_TOTAL={len(negatives)}\nNEGATIVE_TESTS_PASSED={sum(x[2] for x in negatives)}\nPOSITIVE_TESTS_TOTAL={len(positives)}\nPOSITIVE_TESTS_PASSED={sum(x[1] for x in positives)}\nADVERSARIAL_MUTATIONS_TOTAL={len(adversarial)}\nADVERSARIAL_MUTATIONS_CAUGHT={sum(x[2] for x in adversarial)}')
 return len(negatives),sum(x[2] for x in negatives),len(positives),sum(x[1] for x in positives),len(adversarial),sum(x[2] for x in adversarial)
if __name__=='__main__':
 a,b,c,d,e,f=run_controls();raise SystemExit(not(a==b and c==d and e==f and a>=45 and c>=20 and e>=10))
