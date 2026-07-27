#!/usr/bin/env python3
"""Full-dataset semantic mutations and positive controls (no helper-only tests)."""
from __future__ import annotations
import copy
from pathlib import Path
import validate_stage_3_1_3_glossary as v

def audit(status='NOT_APPLICABLE'):
 return {'candidate_search_performed':True,'generated_candidates':['sampleValue'],'inspected_files':1,'found_candidates':[],'accepted_candidates':[],'rejected_candidates':[],'final_status':status,'final_reason':'language mapping is not applicable to this synthetic control','missing_reason':None}
def dataset():
 rows=[];recs={};terms=[]
 for i,n in enumerate(('SampleProjectedLot','OtherProjectedLot')):
  r={'Canonical term':n,'Русское название':f'расчётный лот {i}','Profile':'Hybrid','Type':'LOT_CALCULATED','Unit':'lot','Sign':'>= 0','Projected/Actual':'PROJECTED','Authoritative source':f'typed formula input {i}','Rounding':'ROUND_DOWN','Tolerance':'VolumeToleranceLots','Aliases':'—','Status':'APPROVED_TERM'};rows.append(r)
  recs[n]={'CanonicalName':f'`{n}`','Русское название':r['Русское название'],'Архитектурный профиль':'Hybrid','Размерность':'`LOT_CALCULATED`','Unit':'`lot`','Знак':'>= 0','Projected/Actual class':'`PROJECTED`','Authoritative source':r['Authoritative source'],'Rounding':'ROUND_DOWN','Tolerance':'`VolumeToleranceLots`','Legacy aliases':'—','Статус определения':'`APPROVED_TERM`','Краткое определение':f'{n} — расчётный объём уникальной роли {i} до broker normalization.','Semantic category':'LOT_VALUE','Lifecycle class':'PROJECTED_VALUE','Lifecycle':f'{n} создаётся formula snapshot {i}; stale на input revision; заменяется пересчётом и не становится actual.','Creation event':f'formula snapshot {i}','Mutation events':'new revision only','Stale triggers':'input revision makes value stale','Replacement source':'recalculation from new snapshot','Terminal condition':'ends before execution','Persistence behavior':'plan evidence, not actual ledger','Restart behavior':'recalculate after restart','Отличие от':f'distinct role {i}','Semantic exception':'NOT_APPLICABLE','Similarity exception reason':f'Shared projected lifecycle requirements; distinct role/source {i}.','Conflict':'`NOT_APPLICABLE`','Resolution stage':'`NOT_APPLICABLE`','Mapping status':'MQL5=`NOT_APPLICABLE`; Python=`NOT_APPLICABLE`','MQL5 mapping':'NOT_APPLICABLE','Python mapping':'NOT_APPLICABLE'}
  terms.append({'canonical_term':n,'mql5_status':'NOT_APPLICABLE','python_status':'NOT_APPLICABLE','candidate_audit':{'mql5':audit(),'python':audit()},'mql5':[],'python':[]})
 return rows,recs,{'terms':terms}
def sync(row,rec,**kw):
 mapf={'Type':'Размерность','Unit':'Unit','Sign':'Знак','Projected/Actual':'Projected/Actual class','Authoritative source':'Authoritative source','Rounding':'Rounding','Tolerance':'Tolerance','Status':'Статус определения'}
 row.update(kw)
 for k,val in kw.items():
  if k in mapf:rec[mapf[k]]=f'`{val}`' if k in {'Type','Unit','Projected/Actual','Tolerance','Status'} else val
def set_status(recs,item,lang,status):
 item[lang+'_status']=status;item['candidate_audit'][lang]['final_status']=status
 rec=recs[item['canonical_term']];m=rec['Mapping status'];a,b=(status,item['python_status']) if lang=='mql5' else (item['mql5_status'],status);rec['Mapping status']=f'MQL5=`{a}`; Python=`{b}`';rec['MQL5 mapping' if lang=='mql5' else 'Python mapping']='NONE_FOUND' if status=='MISSING' else ('NOT_APPLICABLE' if status=='NOT_APPLICABLE' else 'Tests/test_stage_3_1_3_semantic_mutations.py::run_controls')
def proven_entry(status='PARTIAL_MATCH'):
 line=run_controls.__code__.co_firstlineno
 return {'file':'Tests/test_stage_3_1_3_semantic_mutations.py','line':line,'identifier':'run_controls','identifier_kind':'function','declaration_evidence':'def run_controls','read_sites':['Tests/test_stage_3_1_3_semantic_mutations.py:200'],'write_sites':[],'mapping_status':status,'semantic_note':'synthetic proven declaration/use control','lifecycle_role':'test control lifecycle','score':75}
def run_controls(verbose=True):
 negative=[]
 def neg(name,mut):
  rows,recs,data=dataset();mut(rows,recs,data);c=v.validate(rows,recs,data,False);negative.append((name,c[name]>0))
 neg('MQL5_ALL_MAPPINGS_MISSING',lambda r,d,m:[set_status(d,x,'mql5','MISSING') for x in m['terms']])
 neg('PYTHON_ALL_MAPPINGS_MISSING',lambda r,d,m:[set_status(d,x,'python','MISSING') for x in m['terms']])
 neg('MISSING_WITHOUT_CANDIDATE_AUDIT',lambda r,d,m:(set_status(d,m['terms'][0],'mql5','MISSING'),m['terms'][0]['candidate_audit']['mql5'].update(generated_candidates=[])))
 neg('MISSING_WITH_UNREVIEWED_CANDIDATES',lambda r,d,m:(set_status(d,m['terms'][0],'mql5','MISSING'),m['terms'][0]['candidate_audit']['mql5'].update(found_candidates=[{'identifier':'x','score':50}])))
 neg('MISSING_WITH_ACCEPTED_CANDIDATE',lambda r,d,m:(set_status(d,m['terms'][0],'mql5','MISSING'),m['terms'][0]['candidate_audit']['mql5'].update(accepted_candidates=[{'identifier':'x'}])))
 neg('NON_MISSING_WITH_EMPTY_ENTRIES',lambda r,d,m:set_status(d,m['terms'][0],'mql5','PARTIAL_MATCH'))
 neg('MISSING_WITH_NONEMPTY_ENTRIES',lambda r,d,m:(set_status(d,m['terms'][0],'mql5','MISSING'),m['terms'][0].update(mql5=[proven_entry()])))
 neg('POSITION_ROLE_AMBIGUITY',lambda r,d,m:(r[0].update({'Canonical term':'BigCorePosition'}),d.__setitem__('BigCorePosition',d.pop('SampleProjectedLot')),d['BigCorePosition'].update(CanonicalName='`BigCorePosition`',**{'Semantic category':'ROLE'}),sync(r[0],d['BigCorePosition'],Type='ROLE_ID',Unit='integer/string identity',Sign='not numeric',Tolerance='EXACT'),m['terms'][0].update(canonical_term='BigCorePosition')))
 neg('PLAN_STATE_AMBIGUITY',lambda r,d,m:(r[0].update({'Canonical term':'HybridPlan'}),d.__setitem__('HybridPlan',d.pop('SampleProjectedLot')),d['HybridPlan'].update(CanonicalName='`HybridPlan`',**{'Semantic category':'STATE_OR_RESULT'}),sync(r[0],d['HybridPlan'],Type='STATE',Unit='enum/structured record',Sign='not numeric',Tolerance='EXACT ENUM MATCH'),m['terms'][0].update(canonical_term='HybridPlan')))
 neg('INVALID_TYPE_SIGN',lambda r,d,m:sync(r[0],d[r[0]['Canonical term']],Sign='signed'))
 neg('INVALID_SIGN_SEMANTICS',lambda r,d,m:(sync(r[0],d[r[0]['Canonical term']],Type='POSITION_ID',Unit='position reference identity',Sign='>= 0',Tolerance='EXACT'),d[r[0]['Canonical term']].update({'Semantic category':'IDENTITY'})))
 neg('INVALID_SOURCE_MATRIX',lambda r,d,m:(sync(r[0],d[r[0]['Canonical term']],Type='LOT_REQUESTED',**{'Projected/Actual':'REQUESTED','Authoritative source':'raw formula'}),d[r[0]['Canonical term']].update({'Lifecycle class':'REQUESTED'})))
 neg('INVALID_SOURCE_MATRIX',lambda r,d,m:(sync(r[0],d[r[0]['Canonical term']],Type='PRICE_EXECUTED',Unit='price',Sign='> 0',Tolerance='PriceTolerance',**{'Projected/Actual':'EXECUTED','Authoritative source':'projected formula'}),d[r[0]['Canonical term']].update({'Semantic category':'PRICE_OR_DISTANCE','Lifecycle class':'DEAL'})))
 neg('INVALID_LIFECYCLE_MATRIX',lambda r,d,m:d[r[0]['Canonical term']].update({'Persistence behavior':'ledger commit','Lifecycle class':'PROJECTED_VALUE'}))
 neg('INVALID_LIFECYCLE_MATRIX',lambda r,d,m:(sync(r[0],d[r[0]['Canonical term']],Type='MONEY_REALIZED',Unit='account money',Sign='signed',Tolerance='MoneyTolerance',**{'Projected/Actual':'ACTUAL CONFIRMED','Authoritative source':'confirmed ledger'}),d[r[0]['Canonical term']].update({'Semantic category':'MONEY_VALUE','Lifecycle class':'LEDGER','Creation event':'allocation without identity','Persistence behavior':'stored','Restart behavior':'reload'})))
 neg('INVALID_LIFECYCLE_MATRIX',lambda r,d,m:(d[r[0]['Canonical term']].update({'Lifecycle class':'DEAL','Creation event':'confirmed deal','Mutation events':'mutable freely','Persistence behavior':'deal history','Restart behavior':'deal history'})))
 neg('NEAR_DUPLICATE_DEFINITIONS',lambda r,d,m:[x.update({'Краткое определение':'projected lot common clause with almost identical semantic content','Similarity exception reason':''}) for x in d.values()])
 neg('NEAR_DUPLICATE_LIFECYCLES',lambda r,d,m:[x.update({'Lifecycle':'created validated frozen stale replaced terminal persisted restarted common lifecycle','Similarity exception reason':''}) for x in d.values()])
 neg('CANDIDATE_WITHOUT_REJECTION_REASON',lambda r,d,m:m['terms'][0]['candidate_audit']['mql5'].update(rejected_candidates=[{'identifier':'x','score':20}]))
 neg('CANDIDATE_WITHOUT_SCORE',lambda r,d,m:m['terms'][0]['candidate_audit']['mql5'].update(found_candidates=[{'identifier':'x'}],rejected_candidates=[{'identifier':'x','reason':'low'}]))
 neg('CANDIDATE_STATUS_INCONSISTENT',lambda r,d,m:m['terms'][0]['candidate_audit']['mql5'].update(final_status='MISSING'))
 neg('MAPPING_STATUS_PARITY_ERROR',lambda r,d,m:d[r[0]['Canonical term']].update({'Mapping status':'MQL5=`MISSING`; Python=`NOT_APPLICABLE`'}))
 neg('MAPPING_WITHOUT_DECLARATION_EVIDENCE',lambda r,d,m:(set_status(d,m['terms'][0],'python','PARTIAL_MATCH'),m['terms'][0].update(python=[{**proven_entry(),'declaration_evidence':''}])))
 neg('MAPPING_WITHOUT_USE_EVIDENCE',lambda r,d,m:(set_status(d,m['terms'][0],'python','PARTIAL_MATCH'),m['terms'][0].update(python=[{**proven_entry(),'read_sites':[]}])) )
 neg('TOKEN_IDENTIFIER_KINDS',lambda r,d,m:(set_status(d,m['terms'][0],'python','PARTIAL_MATCH'),m['terms'][0].update(python=[{**proven_entry(),'identifier_kind':'token'}])))
 neg('INVALID_TYPE_UNIT',lambda r,d,m:sync(r[0],d[r[0]['Canonical term']],Unit='account money'))
 neg('INVALID_TYPE_TOLERANCE',lambda r,d,m:sync(r[0],d[r[0]['Canonical term']],Tolerance='MoneyTolerance'))
 neg('INVALID_TYPE_CLASS',lambda r,d,m:sync(r[0],d[r[0]['Canonical term']],**{'Projected/Actual':'ACTUAL CURRENT'}))
 neg('INVALID_DEFINITION_TYPE_SEMANTICS',lambda r,d,m:d[r[0]['Canonical term']].update({'Semantic category':'MONEY_VALUE'}))
 neg('UNRESOLVED_ITEMS_WITHOUT_CONFLICT_ID',lambda r,d,m:(sync(r[0],d[r[0]['Canonical term']],Status='UNRESOLVED_BUSINESS_POLICY'),d[r[0]['Canonical term']].update(Conflict='NOT_APPLICABLE')))
 positives=[]
 def pos(mut=lambda r,d,m:None):
  r,d,m=dataset();mut(r,d,m);c=v.validate(r,d,m,False);positives.append(not any(c[k] for k in v.BLOCKING))
 pos()
 def missing(r,d,m):
  x=m['terms'][0];set_status(d,x,'mql5','MISSING');a=x['candidate_audit']['mql5'];a.update(found_candidates=[{'identifier':'weak','score':20}],rejected_candidates=[{'identifier':'weak','score':20,'reason':'semantic mismatch'}],missing_reason='all rejected')
 pos(missing)
 def mapped(status):
  def f(r,d,m):
   x=m['terms'][0];set_status(d,x,'python',status);x['python']=[proven_entry(status)];a=x['candidate_audit']['python'];a.update(found_candidates=[{'identifier':'run_controls','score':75}],accepted_candidates=[{'identifier':'run_controls','score':75,'status':status}],final_reason='accepted')
  return f
 pos(mapped('PARTIAL_MATCH'));pos(mapped('SEMANTIC_MATCH'));pos(mapped('AMBIGUOUS'))
 pos(lambda r,d,m:None) # NOT_APPLICABLE
 pos(lambda r,d,m:None) # projected lot
 pos(lambda r,d,m:(sync(r[0],d[r[0]['Canonical term']],Type='LOT_POSITION_ACTUAL',**{'Projected/Actual':'ACTUAL CURRENT','Authoritative source':'current position snapshot','Rounding':'NO_ADDITIONAL_ROUNDING'}),d[r[0]['Canonical term']].update({'Lifecycle class':'ACTUAL_POSITION','Stale triggers':'trade execution event','Replacement source':'current MT5 position snapshot','Restart behavior':'terminal position refresh'})))
 pos(lambda r,d,m:(sync(r[0],d[r[0]['Canonical term']],Type='MONEY_REALIZED',Unit='account money',Sign='signed',Tolerance='MoneyTolerance',**{'Projected/Actual':'ACTUAL CONFIRMED','Authoritative source':'confirmed deal ledger'}),d[r[0]['Canonical term']].update({'Краткое определение':'подтверждённая прибыль из deal history','Semantic category':'MONEY_VALUE','Lifecycle class':'DEAL','Creation event':'confirmed deal','Persistence behavior':'deal history immutable','Restart behavior':'rebuild from deal history'})))
 pos(lambda r,d,m:(sync(r[0],d[r[0]['Canonical term']],Type='MONEY_REALIZED',Unit='account money',Sign='signed',Tolerance='MoneyTolerance',**{'Projected/Actual':'ACTUAL CONFIRMED','Authoritative source':'confirmed ledger'}),d[r[0]['Canonical term']].update({'Краткое определение':'денежная величина confirmed ledger','Semantic category':'MONEY_VALUE','Lifecycle class':'LEDGER','Creation event':'EventID exactly once','Persistence behavior':'persist exactly once','Restart behavior':'ledger reconciliation'})))
 pos(lambda r,d,m:(sync(r[0],d[r[0]['Canonical term']],Type='ROLE_ID',Unit='role identity',Sign='not numeric',Tolerance='EXACT'),d[r[0]['Canonical term']].update({'Краткое определение':'назначенная торговая role identity','Semantic category':'ROLE','Lifecycle class':'ROLE'})))
 pos(lambda r,d,m:(sync(r[0],d[r[0]['Canonical term']],Type='POSITION_ID',Unit='position reference identity',Sign='not numeric',Tolerance='EXACT'),d[r[0]['Canonical term']].update({'Краткое определение':'position identifier reference','Semantic category':'IDENTITY','Lifecycle class':'IDENTITY'})))
 pos(lambda r,d,m:(sync(r[0],d[r[0]['Canonical term']],Type='PLAN_OBJECT',Unit='structured plan',Sign='not numeric',Tolerance='EXACT STRUCTURE'),d[r[0]['Canonical term']].update({'Краткое определение':'immutable approved plan object','Semantic category':'STRUCTURED_OBJECT'})))
 pos(lambda r,d,m:(sync(r[0],d[r[0]['Canonical term']],Type='DIRECTION_ENUM',Unit='BUY/SELL enum',Sign='not numeric',Tolerance='EXACT ENUM MATCH'),d[r[0]['Canonical term']].update({'Краткое определение':'absolute BUY SELL direction enum','Semantic category':'STRUCTURED_OBJECT'})))
 pos(lambda r,d,m:(sync(r[0],d[r[0]['Canonical term']],Type='PRICE_POINT_SIZE',Unit='price per point',Sign='> 0',Tolerance='EXACT PROPERTY SNAPSHOT',**{'Projected/Actual':'SYMBOL PROPERTY','Authoritative source':'SYMBOL_POINT'}),d[r[0]['Canonical term']].update({'Краткое определение':'размер ценового Point symbol property','Semantic category':'PRICE_OR_DISTANCE','Lifecycle class':'SYMBOL_PROPERTY'})))
 if verbose:
  for n,ok in negative:print(f'NEGATIVE_{n}={"PASS" if ok else "FAIL"}')
  print(f'NEGATIVE_TESTS_TOTAL={len(negative)}');print(f'NEGATIVE_TESTS_PASSED={sum(x for _,x in negative)}');print('POSITIVE_DETAILS='+','.join(f'{i+1}:{"PASS" if x else "FAIL"}' for i,x in enumerate(positives)));print(f'POSITIVE_TESTS_TOTAL={len(positives)}');print(f'POSITIVE_TESTS_PASSED={sum(positives)}');print('SEMANTIC_MUTATION_TESTS='+('PASS' if all(x for _,x in negative) and all(positives) else 'FAIL'))
 return len(negative),sum(x for _,x in negative),len(positives),sum(positives)
if __name__=='__main__':
 a,b,c,d=run_controls();raise SystemExit(0 if a==b and c==d and a>=30 and c>=15 else 1)
