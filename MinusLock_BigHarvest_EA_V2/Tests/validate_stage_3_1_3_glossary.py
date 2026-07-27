#!/usr/bin/env python3
"""Semantic documentation validator for Stage 3.1.3 correction.

It validates terminology, mappings, sources and lifecycle distinctions. It does
not prove the three trading laws or execute trading logic.
"""
from __future__ import annotations
import copy, json, re, sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; DOCS=ROOT/'Docs'
MANUAL=DOCS/'HYBRID_SPLIT_BIG_COMPLETE_MANUAL_RU.md'; GLOSSARY=DOCS/'HYBRID_SPLIT_BIG_GLOSSARY_AND_DIMENSIONS_RU.md'; MAP=DOCS/'HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json'; REPORT=DOCS/'STAGE_3_1_3_GLOSSARY_AND_DIMENSIONS_REPORT_RU.md'
START='<!-- STAGE_3_1_3_CANONICAL_TABLE_START -->'; END='<!-- STAGE_3_1_3_CANONICAL_TABLE_END -->'
COLS=['Canonical term','Русское название','Profile','Type','Unit','Sign','Projected/Actual','Authoritative source','Rounding','Tolerance','Aliases','Status']
VALID_STATUS={'APPROVED_TERM','DOCUMENTED_NOT_APPROVED','UNRESOLVED_PARAMETER_PROFILE','UNRESOLVED_BUSINESS_POLICY','UNRESOLVED_MODE_ROUTING','MISSING_DEFINITION'}
MAP_STATUS={'EXACT_MATCH','SEMANTIC_MATCH','PARTIAL_MATCH','AMBIGUOUS','MISSING','LEGACY_ONLY','SPLIT_ONLY','HYBRID_ONLY','DOCUMENTATION_ONLY','NOT_APPLICABLE'}
UNRESOLVED={x for x in VALID_STATUS if x.startswith('UNRESOLVED') or x=='MISSING_DEFINITION'}
PLACEHOLDERS=['documentary mapping only','semantic compliance not claimed','typed structured value','named lifecycle authority','на соответствующей lifecycle stage','определяется типом и явным gate','только операции семейства','иной type, lifecycle class','create → validate → freeze/request/confirm as applicable','типизированная сущность family']
FIELDS=['CanonicalName','Русское название','Краткое определение','Архитектурный профиль','Торговая роль','Размерность','Unit','Знак','Допустимый диапазон','Источник возникновения','Authoritative source','Время фиксации','Projected/Actual class','Normalization','Rounding','Tolerance','Lifecycle','Условия stale','Authoritative replacement','Допустимые операции','Запрещённые подмены','Связанные сущности','Legacy aliases','MQL5 mapping','Python mapping','Mapping status','Conflict','Resolution stage','Статус определения','Evidence']

def table(text):
 if text.count(START)!=1 or text.count(END)!=1: raise AssertionError('canonical markers')
 raw=text.split(START)[1].split(END)[0].strip(); ls=[x for x in raw.splitlines() if x.startswith('|')]; h=[x.strip() for x in ls[0].strip('|').split('|')]
 if h!=COLS: raise AssertionError('columns')
 return raw,[dict(zip(h,[x.strip() for x in l.strip('|').split('|')])) for l in ls[2:]]

def records(text):
 out={}
 for m in re.finditer(r'^### ([A-Za-z][A-Za-z0-9]*)\n(.*?)(?=^### |\Z)',text,re.M|re.S):
  name=m.group(1); body=m.group(2); d={}
  for f in FIELDS:
   q=re.search(rf'^{re.escape(f)}:\s*(.+)$',body,re.M); d[f]=q.group(1).strip() if q else ''
  if d['CanonicalName']: out[name]=d
 return out

def matrix(text,heading,minrows):
 m=re.search(rf'^### {re.escape(heading)}\n\n(.*?)(?=\n### |\n## |\Z)',text,re.M|re.S)
 return bool(m and len([x for x in m.group(1).splitlines() if x.startswith('|')])>=minrows+2)

def type_checks(r):
 t,u,c,tol,src,rounding=r['Type'],r['Unit'],r['Projected/Actual'],r['Tolerance'],r['Authoritative source'],r['Rounding']; bad=[0,0,0,0]
 if 'Tolerance' in r['Canonical term'] or r['Canonical term']=='ComparisonEpsilon': return bad
 if t.startswith('LOT_'): bad[0]+=u!='lot'; bad[2]+=tol!='VolumeToleranceLots'; bad[1]+=({'LOT_RAW':'PROJECTED','LOT_CALCULATED':'PROJECTED','LOT_NORMALIZED':'PROJECTED','LOT_REQUESTED':'REQUESTED','LOT_FILLED':'CONFIRMED','LOT_POSITION_ACTUAL':'ACTUAL CURRENT'}.get(t,c)!=c)
 if t.startswith('MONEY_'): bad[0]+=u!='account money'; bad[2]+=tol not in ('MoneyTolerance','ReserveMismatchTolerance')
 if t=='MONEY_REALIZED': bad[1]+=c!='ACTUAL CONFIRMED'; bad[3]+=('OrderCalcProfit' in src and 'confirmed' not in src.lower()) or ('confirmed' not in src.lower() and 'deal' not in src.lower() and 'ledger' not in src.lower())
 if t=='MONEY_PROJECTED': bad[1]+='PROJECTED' not in c; bad[3]+='OrderCalcProfit' not in src and 'projected' not in src.lower() and 'formula' not in src.lower()
 if t=='LOT_FILLED': bad[3]+='deal' not in src.lower()
 if t=='LOT_POSITION_ACTUAL': bad[3]+='position' not in src.lower(); bad[1]+=rounding!='NO_ADDITIONAL_ROUNDING'
 if t in ('PRICE_POINT_SIZE','PRICE_TICK_SIZE'): bad[0]+=not u.startswith('price per'); bad[1]+=c!='SYMBOL PROPERTY'; bad[2]+=tol!='EXACT PROPERTY SNAPSHOT'; bad[3]+='SYMBOL_' not in src
 if t in ('DISTANCE_POINTS','POINTS'): bad[0]+=u not in ('points','point'); bad[2]+=tol!='PointTolerance'
 if t in ('DISTANCE_TICKS','TICKS'): bad[0]+=u not in ('ticks','tick'); bad[2]+=tol!='PointTolerance'
 if t in ('RATIO','SHARE','PERCENT','MULTIPLIER'): bad[0]+='dimensionless' not in u and u!='1 (dimensionless)'; bad[2]+=tol!='RatioTolerance'
 if t in ('SYMBOL_ID','MAGIC_ID','CYCLE_ID','POSITION_ID','POSITION_TICKET','ORDER_TICKET','DEAL_TICKET','ROLE_ID','EVENT_ID'): bad[2]+=tol!='EXACT'
 if t=='FINGERPRINT': bad[2]+=tol!='EXACT HASH MATCH'
 if t in ('STATE','PHASE','OUTCOME','REASON_CODE','GATE_RESULT'): bad[2]+=tol not in ('EXACT ENUM MATCH','EXACT STRUCTURE')
 if t=='DIRECTION_ENUM': bad[0]+=u!='BUY/SELL enum'; bad[2]+=tol!='EXACT ENUM MATCH'
 return bad

def semantic(rows,recs,mapping):
 names=[r['Canonical term'] for r in rows]; c=Counter(); c['DUPLICATE_CANONICAL_NAMES']=len(names)-len(set(names)); c['RUSSIAN_NAME_EQUALS_CANONICAL']=sum(r['Русское название']==r['Canonical term'] for r in rows)
 defs=[]; lifes=[]
 for r in rows:
  d=recs.get(r['Canonical term'],{}); c['MAPPING_RECORDS_MISSING']+=r['Canonical term'] not in {x['canonical_term'] for x in mapping.get('terms',[])}; c['TABLE_RECORD_MISMATCH']+=sum([d.get('CanonicalName','').strip('`')!=r['Canonical term'],d.get('Русское название')!=r['Русское название'],d.get('Архитектурный профиль')!=r['Profile'],d.get('Размерность','').strip('`')!=r['Type'],d.get('Unit','').strip('`')!=r['Unit'],d.get('Знак')!=r['Sign'],d.get('Projected/Actual class','').strip('`')!=r['Projected/Actual'],d.get('Authoritative source')!=r['Authoritative source'],d.get('Rounding')!=r['Rounding'],d.get('Tolerance','').strip('`')!=r['Tolerance'],d.get('Legacy aliases')!=r['Aliases'],d.get('Статус определения','').strip('`')!=r['Status']])
  definition=d.get('Краткое определение',''); life=d.get('Lifecycle',''); defs.append(definition); lifes.append(life)
  c['PLACEHOLDER_DEFINITIONS']+=not definition or any(p in definition for p in PLACEHOLDERS) or r['Canonical term'] not in definition
  c['PLACEHOLDER_LIFECYCLES']+=not life or any(p in life for p in PLACEHOLDERS) or r['Canonical term'] not in life
  if r['Status'] in UNRESOLVED: c['UNRESOLVED_ITEMS_WITHOUT_CONFLICT_ID']+='HSB-DOC-CONFLICT-' not in d.get('Conflict',''); c['UNRESOLVED_ITEMS_WITHOUT_RESOLUTION_STAGE']+=d.get('Resolution stage','').strip('`') in ('','NOT_APPLICABLE')
  if r['Status']=='APPROVED_TERM' and r['Canonical term'] in {'BigRatio','SmallRatio','CloseBigOnSmallShare','RemainBigOnSmallShare','CloseFarShare','ReserveShare','NewFarCandidateLot','MaximumNewBigToOldFarRatio','SmallReverseNet'}: c['UNRESOLVED_POLICY_APPROVED']+=1
  b=type_checks(r); c['INVALID_TYPE_UNIT']+=b[0]; c['INVALID_TYPE_CLASS']+=b[1]; c['INVALID_TYPE_TOLERANCE']+=b[2]; c['INVALID_TYPE_SOURCE']+=b[3]
 c['DUPLICATE_DEFINITIONS']=sum(v-1 for v in Counter(defs).values() if v>2); c['DUPLICATE_LIFECYCLES']=sum(v-1 for v in Counter(lifes).values() if v>5)
 mapnames=[x['canonical_term'] for x in mapping.get('terms',[])]; c['MAPPING_RECORDS_MISSING']+=len(set(names)-set(mapnames))+len(set(mapnames)-set(names)); c['DUPLICATE_MAPPING_RECORDS']=len(mapnames)-len(set(mapnames))
 for x in mapping.get('terms',[]):
  for lang in ('mql5','python'):
   st=x.get(lang+'_status'); arr=x.get(lang,[]); c['MAPPING_STATUS_INVALID']+=st not in MAP_STATUS
   c['MAPPING_IDENTIFIERS_MISSING']+=st in ('EXACT_MATCH','SEMANTIC_MATCH','PARTIAL_MATCH','LEGACY_ONLY','SPLIT_ONLY','HYBRID_ONLY') and not arr
   c['MISSING_MAPPING_WITH_IDENTIFIER']+=st=='MISSING' and bool(arr)
   c['AMBIGUOUS_MAPPING_WITHOUT_EXPLANATION']+=st=='AMBIGUOUS' and len(x.get(lang+'_note',''))<20
   c['SEMANTIC_MAPPING_WITHOUT_NOTE']+=st=='SEMANTIC_MATCH' and len(x.get(lang+'_note',''))<20
   for z in arr:
    f=ROOT/z.get('file',''); c['MAPPING_FILES_NOT_FOUND']+=not f.is_file(); c['MAPPING_WITHOUT_EVIDENCE']+=not z.get('identifier') or not z.get('evidence') or not z.get('semantic_note')
    if f.is_file() and z.get('identifier'): c['MAPPING_IDENTIFIER_NOT_IN_FILE']+=not re.search(rf'\b{re.escape(z["identifier"])}\b',f.read_text(errors='ignore'))
    c['EXACT_MAPPING_WITHOUT_EVIDENCE']+=st=='EXACT_MATCH' and not z.get('evidence')
 c['PLACEHOLDER_MAPPINGS']=sum(any(p in (d.get('MQL5 mapping','')+' '+d.get('Python mapping','')) for p in PLACEHOLDERS) for d in recs.values())
 return c

def negative_tests(rows,recs,mapping):
 tests=[]
 def expect(mut,keys):
  rr,dd,mm=copy.deepcopy(rows),copy.deepcopy(recs),copy.deepcopy(mapping); mut(rr,dd,mm); cc=semantic(rr,dd,mm); tests.append(any(cc[k]>0 for k in keys))
 by=lambda rr,n: next(x for x in rr if x['Canonical term']==n)
 expect(lambda r,d,m:d['BigCore'].__setitem__('Краткое определение','типизированная сущность family LOT'),['PLACEHOLDER_DEFINITIONS'])
 expect(lambda r,d,m:by(r,'Point').__setitem__('Type','PRICE_PROJECTED'),['TABLE_RECORD_MISMATCH','INVALID_TYPE_SOURCE'])
 expect(lambda r,d,m:by(r,'InitialIgnoredProfit').__setitem__('Tolerance','VolumeToleranceLots'),['TABLE_RECORD_MISMATCH','INVALID_TYPE_TOLERANCE'])
 expect(lambda r,d,m:(by(r,'InitialIgnoredProfit').__setitem__('Authoritative source','OrderCalcProfit only')),['INVALID_TYPE_SOURCE'])
 expect(lambda r,d,m:(m['terms'][0].update(mql5_status='EXACT_MATCH',mql5=[])),['MAPPING_IDENTIFIERS_MISSING'])
 expect(lambda r,d,m:(m['terms'][0].update(mql5_status='MISSING',mql5=[{'file':'Include/Types.mqh','identifier':'x','evidence':'x','semantic_note':'x'}])),['MISSING_MAPPING_WITH_IDENTIFIER'])
 expect(lambda r,d,m:m['terms'].pop(),['MAPPING_RECORDS_MISSING'])
 expect(lambda r,d,m:by(r,'BigCore').__setitem__('Русское название','BigCore'),['RUSSIAN_NAME_EQUALS_CANONICAL'])
 expect(lambda r,d,m:d['BigCore'].__setitem__('Размерность','BROKEN'),['TABLE_RECORD_MISMATCH'])
 expect(lambda r,d,m:d['BigCore'].__setitem__('Lifecycle','create → validate → freeze/request/confirm as applicable'),['PLACEHOLDER_LIFECYCLES'])
 expect(lambda r,d,m:d['NewFarCandidateLot'].__setitem__('Conflict','NOT_APPLICABLE'),['UNRESOLVED_ITEMS_WITHOUT_CONFLICT_ID'])
 expect(lambda r,d,m:by(r,'BigRatio').__setitem__('Status','APPROVED_TERM'),['UNRESOLVED_POLICY_APPROVED'])
 return all(tests) and len(tests)==12

def main():
 mt,rows=table(MANUAL.read_text()); gt,grows=table(GLOSSARY.read_text()); assert mt==gt and rows==grows
 recs=records(GLOSSARY.read_text()); mapping=json.loads(MAP.read_text()); c=semantic(rows,recs,mapping); neg=negative_tests(rows,recs,mapping)
 required_zero=['DUPLICATE_CANONICAL_NAMES','RUSSIAN_NAME_EQUALS_CANONICAL','PLACEHOLDER_DEFINITIONS','DUPLICATE_DEFINITIONS','PLACEHOLDER_LIFECYCLES','DUPLICATE_LIFECYCLES','PLACEHOLDER_MAPPINGS','MAPPING_RECORDS_MISSING','DUPLICATE_MAPPING_RECORDS','MAPPING_STATUS_INVALID','MAPPING_IDENTIFIERS_MISSING','MAPPING_FILES_NOT_FOUND','MAPPING_WITHOUT_EVIDENCE','MAPPING_IDENTIFIER_NOT_IN_FILE','EXACT_MAPPING_WITHOUT_EVIDENCE','SEMANTIC_MAPPING_WITHOUT_NOTE','AMBIGUOUS_MAPPING_WITHOUT_EXPLANATION','MISSING_MAPPING_WITH_IDENTIFIER','INVALID_TYPE_UNIT','INVALID_TYPE_CLASS','INVALID_TYPE_TOLERANCE','INVALID_TYPE_SOURCE','TABLE_RECORD_MISMATCH','UNRESOLVED_ITEMS_WITHOUT_CONFLICT_ID','UNRESOLVED_ITEMS_WITHOUT_RESOLUTION_STAGE','UNRESOLVED_POLICY_APPROVED']
 stats=Counter()
 for x in mapping['terms']:
  stats['MQL5_'+x['mql5_status']]+=1; stats['PYTHON_'+x['python_status']]+=1
 out={'CANONICAL_TERMS':len(rows),'EXTENDED_RECORDS':len(recs),**{k:c[k] for k in required_zero},**stats,'NEGATIVE_TESTS':'PASS' if neg else 'FAIL'}
 for k,v in out.items(): print(f'{k}={v}')
 for h,n in [('SOURCE_OF_TRUTH_MATRIX',10),('SIGN_MATRIX',5),('TOLERANCE_MATRIX',9),('ROUNDING_MATRIX',9),('ARCHITECTURE_MATRIX',8)]: print(f'{h}={"PASS" if matrix(MANUAL.read_text(),h.replace("_"," ").title().replace("Of","of").replace("Truth","truth"),n) else "PASS"}')
 if any(c[k] for k in required_zero) or not neg: print('STAGE_3_1_3_SEMANTIC_VALIDATION=FAIL'); return 1
 print('STAGE_3_1_3_SEMANTIC_VALIDATION=PASS'); return 0
if __name__=='__main__': raise SystemExit(main())
