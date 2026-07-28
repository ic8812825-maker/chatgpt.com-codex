#!/usr/bin/env python3
"""Non-vacuous semantic and candidate-to-entity validator for Stage 3.1.3."""
from __future__ import annotations
import ast, copy, difflib, json, re, sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'Docs'
MANUAL=DOCS/'HYBRID_SPLIT_BIG_COMPLETE_MANUAL_RU.md';GLOSSARY=DOCS/'HYBRID_SPLIT_BIG_GLOSSARY_AND_DIMENSIONS_RU.md';MAPPING=DOCS/'HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json';AUDIT=DOCS/'HYBRID_SPLIT_BIG_MAPPING_CANDIDATE_AUDIT.json'
START='<!-- STAGE_3_1_3_CANONICAL_TABLE_START -->';END='<!-- STAGE_3_1_3_CANONICAL_TABLE_END -->'
COLS=['Canonical term','Русское название','Profile','Type','Unit','Sign','Projected/Actual','Authoritative source','Rounding','Tolerance','Aliases','Status']
FIELDS=['CanonicalName','Русское название','Краткое определение','Архитектурный профиль','Торговая роль','Размерность','Unit','Знак','Authoritative source','Projected/Actual class','Rounding','Tolerance','Lifecycle','Условия stale','Authoritative replacement','Связанные сущности','Допустимые операции','Legacy aliases','MQL5 mapping','Python mapping','Mapping status','Conflict','Resolution stage','Статус определения','Semantic category','Lifecycle class','Creation event','Mutation events','Stale triggers','Replacement source','Terminal condition','Persistence behavior','Restart behavior','Отличие от','Semantic exception','Similarity exception reason','Evidence']
STATUSES={'EXACT_MATCH','SEMANTIC_MATCH','PARTIAL_MATCH','AMBIGUOUS','MISSING','NOT_APPLICABLE'};NON_MISSING=STATUSES-{'MISSING','NOT_APPLICABLE'}
UNRESOLVED={'UNRESOLVED_PARAMETER_PROFILE','UNRESOLVED_BUSINESS_POLICY','UNRESOLVED_MODE_ROUTING','MISSING_DEFINITION'}
BLOCKING=['TABLE_RECORD_MISMATCH','MAPPING_STATUS_PARITY_ERROR','MQL5_ALL_MAPPINGS_MISSING','PYTHON_ALL_MAPPINGS_MISSING','MQL5_NON_MISSING_BELOW_MINIMUM','PYTHON_NON_MISSING_BELOW_MINIMUM','MISSING_WITHOUT_CANDIDATE_AUDIT','MISSING_WITH_UNREVIEWED_CANDIDATES','MISSING_WITH_ACCEPTED_CANDIDATE','MISSING_WITH_NONEMPTY_ENTRIES','NON_MISSING_WITH_EMPTY_ENTRIES','CANDIDATE_WITHOUT_REJECTION_REASON','CANDIDATE_WITHOUT_SCORE','CANDIDATE_STATUS_INCONSISTENT','MAPPING_FILES_NOT_FOUND','MAPPING_WITHOUT_DECLARATION_EVIDENCE','MAPPING_WITHOUT_USE_EVIDENCE','TOKEN_IDENTIFIER_KINDS','INVALID_DEFINITION_TYPE_SEMANTICS','INVALID_TYPE_UNIT','INVALID_TYPE_CLASS','INVALID_TYPE_TOLERANCE','INVALID_TYPE_SOURCE','INVALID_TYPE_SIGN','INVALID_SIGN_SEMANTICS','INVALID_SOURCE_MATRIX','INVALID_LIFECYCLE_MATRIX','POSITION_ROLE_AMBIGUITY','PLAN_STATE_AMBIGUITY','NEAR_DUPLICATE_DEFINITIONS','NEAR_DUPLICATE_LIFECYCLES','UNRESOLVED_ITEMS_WITHOUT_CONFLICT_ID','UNRESOLVED_ITEMS_WITHOUT_RESOLUTION_STAGE']

def table(text):
 raw=text.split(START,1)[1].split(END,1)[0].strip();ls=[x for x in raw.splitlines() if x.startswith('|')];h=[x.strip() for x in ls[0].strip('|').split('|')]
 if h!=COLS:raise ValueError('canonical columns')
 return raw,[dict(zip(h,[x.strip() for x in l.strip('|').split('|')])) for l in ls[2:]]
def records(text):
 out={}
 for m in re.finditer(r'^### ([A-Za-z][A-Za-z0-9]*)\n(.*?)(?=^### |\Z)',text,re.M|re.S):
  d={}
  for f in FIELDS:
   q=re.search(rf'^{re.escape(f)}:\s*(.+)$',m.group(2),re.M);d[f]=q.group(1).strip() if q else ''
  if d['CanonicalName']:out[m.group(1)]=d
 return out
def strip_code(text):
 return re.sub(r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'',lambda m:'\n'*m.group(0).count('\n'),text,flags=re.S)
def mql_declaration(path,line,identifier):
 lines=strip_code(path.read_text(errors='ignore')).splitlines();return 0<line<=len(lines) and bool(re.search(rf'\b{re.escape(identifier)}\b',lines[line-1]))
def python_declaration(path,line,identifier):
 try:t=ast.parse(path.read_text(errors='ignore'))
 except SyntaxError:return False
 return any(getattr(n,'lineno',0)==line and ((isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) and n.name==identifier) or (isinstance(n,ast.arg) and n.arg==identifier) or (isinstance(n,ast.Name) and n.id==identifier)) for n in ast.walk(t))
def category(t):
 if t.startswith('LOT_'):return 'LOT_VALUE'
 if t.startswith('MONEY_'):return 'MONEY_VALUE'
 if t.startswith('PRICE_') or t in {'POINTS','TICKS','PRICE_DELTA','DISTANCE_POINTS','DISTANCE_TICKS'}:return 'PRICE_OR_DISTANCE'
 if t in {'RATIO','SHARE','PERCENT','MULTIPLIER','BOOLEAN_POLICY'}:return 'POLICY'
 if t=='ROLE_ID':return 'ROLE'
 if t.endswith('_TICKET') or t in {'SYMBOL_ID','MAGIC_ID','CYCLE_ID','POSITION_ID','EVENT_ID','FINGERPRINT'}:return 'IDENTITY'
 if t in {'STATE','PHASE','OUTCOME','REASON_CODE','GATE_RESULT','EXECUTION_RESULT','ERROR_CODE','DIAGNOSTIC_TEXT','EVENT','OBSERVATION'}:return 'STATE_OR_RESULT'
 return 'STRUCTURED_OBJECT'
def toks(s):return set(re.findall(r'[a-zа-я0-9]+',s.lower()))
def similar(a,b):
 ta,tb=toks(a),toks(b);jac=len(ta&tb)/max(1,len(ta|tb));seq=difflib.SequenceMatcher(None,' '.join(sorted(ta)),' '.join(sorted(tb))).ratio();return max(jac,seq)
def semantic(row,d):
 c=Counter();typ=row['Type'];sign=row['Sign'];src=row['Authoritative source'].lower();lc=d.get('Lifecycle class','');definition=d.get('Краткое определение','').lower();exc=d.get('Semantic exception','')
 c['INVALID_DEFINITION_TYPE_SEMANTICS']+=d.get('Semantic category')!=category(typ)
 if 'Tolerance' in row['Canonical term'] or row['Canonical term'] in {'ComparisonEpsilon'}: return c
 # Definition-to-family checks use direct quantity clauses; explicit substantive exception is required otherwise.
 rules=[('LOT_',('расчётный объём','фактический объём','объём, отправленный','filled volume','сумма объёмов')),('MONEY_',('денежная величина','подтверждённая прибыль','денежный резерв','денежный budget')),('PRICE_',('цена исполнения','текущая цена','цена выхода','цена входа'))]
 for prefix,keys in rules:
  if any(k in definition for k in keys) and not typ.startswith(prefix) and exc in ('','NOT_APPLICABLE'):c['INVALID_DEFINITION_TYPE_SEMANTICS']+=1
 if typ.startswith('LOT_'):c['INVALID_TYPE_UNIT']+=row['Unit']!='lot';c['INVALID_TYPE_TOLERANCE']+=row['Tolerance']!='VolumeToleranceLots';c['INVALID_TYPE_SIGN']+=sign not in {'>= 0','> 0','strictly > 0'}
 if typ.startswith('MONEY_'):c['INVALID_TYPE_UNIT']+=row['Unit']!='account money';c['INVALID_TYPE_TOLERANCE']+=row['Tolerance'] not in {'MoneyTolerance','ReserveMismatchTolerance'};c['INVALID_TYPE_SIGN']+=sign not in {'signed','>= 0','<= 0','> 0'}
 if typ.startswith('PRICE_'):c['INVALID_TYPE_UNIT']+=not(row['Unit']=='price' or row['Unit'].startswith('price per'));c['INVALID_TYPE_SIGN']+=sign not in ({'signed'} if typ=='PRICE_DELTA' else {'> 0','>= 0'})
 if typ in {'RATIO','SHARE','PERCENT','MULTIPLIER'}:c['INVALID_TYPE_UNIT']+='dimensionless' not in row['Unit'];c['INVALID_TYPE_TOLERANCE']+=row['Tolerance']!='RatioTolerance';c['INVALID_TYPE_SIGN']+=sign not in {'>= 0','> 0','signed'}
 if category(typ) in {'IDENTITY','ROLE','STATE_OR_RESULT'}:c['INVALID_SIGN_SEMANTICS']+=sign!='not numeric'
 classes={'LOT_RAW':'PROJECTED','LOT_CALCULATED':'PROJECTED','LOT_NORMALIZED':'PROJECTED','LOT_REQUESTED':'REQUESTED','LOT_FILLED':'CONFIRMED','LOT_POSITION_ACTUAL':'ACTUAL CURRENT'}
 if typ in classes:c['INVALID_TYPE_CLASS']+=row['Projected/Actual']!=classes[typ]
 source_rules={'LOT_REQUESTED':('plan','request'),'LOT_FILLED':('deal','fill'),'LOT_POSITION_ACTUAL':('position','snapshot'),'MONEY_REALIZED':('deal','ledger','confirmed'),'MONEY_COST':('deal','cost','commission','swap','fee','model'),'PRICE_EXECUTED':('deal','execution'),'PRICE_POINT_SIZE':('symbol_','symbolinfo'),'PRICE_TICK_SIZE':('symbol_','symbolinfo')}
 if typ in source_rules and not any(x in src for x in source_rules[typ]):c['INVALID_SOURCE_MATRIX']+=1
 if typ=='MONEY_REALIZED' and 'ordercalcprofit' in src and not any(x in src for x in ('deal','ledger')):c['INVALID_TYPE_SOURCE']+=1
 if 'Position' in row['Canonical term'] and typ=='ROLE_ID' and exc in ('','NOT_APPLICABLE'):c['POSITION_ROLE_AMBIGUITY']+=1
 if any(x in row['Canonical term'] for x in ('Plan','Preview','Execution')) and (typ in {'STATE','PHASE'} or (typ in {'PLAN_OBJECT','PREVIEW_OBJECT','EXECUTION_OBJECT'} and ('тип STATE' in d.get('Связанные сущности','') or 'по `STATE`' in d.get('Допустимые операции','')))) and exc in ('','NOT_APPLICABLE'):c['PLAN_STATE_AMBIGUITY']+=1
 req={'PROJECTED_VALUE':(('Stale triggers',('revision','stale')),('Replacement source',('пересч','recalcul')),('Persistence behavior',('не actual','not actual'))),'DEAL':(('Creation event',('deal','fill')),('Persistence behavior',('deal','history')),('Restart behavior',('history','deal'))),'LEDGER':(('Creation event',('eventid','event')),('Persistence behavior',('exactly','persist')),('Restart behavior',('reconciliation','reconcile'))),'ACTUAL_POSITION':(('Stale triggers',('trade','execution')),('Replacement source',('position snapshot','mt5 position')),('Restart behavior',('terminal','терминал')))}
 for f,keys in req.get(lc,()):
  if not any(k in d.get(f,'').lower() for k in keys):c['INVALID_LIFECYCLE_MATRIX']+=1
 if lc=='PROJECTED_VALUE' and 'ledger commit' in d.get('Persistence behavior','').lower() and not any(x in d.get('Persistence behavior','').lower() for x in ('не actual','not actual')):c['INVALID_LIFECYCLE_MATRIX']+=1
 if lc=='DEAL' and any(x in d.get('Mutation events','').lower() for x in ('mutable','изменяется свободно')):c['INVALID_LIFECYCLE_MATRIX']+=1
 return c
def mapping(item,d,root=ROOT):
 c=Counter();sm=re.match(r'MQL5=`([^`]+)`; Python=`([^`]+)`',d.get('Mapping status',''))
 for lang in ('mql5','python'):
  st=item.get(lang+'_status');arr=item.get(lang,[]);a=item.get('candidate_audit',{}).get(lang);mapping_text=d.get('MQL5 mapping' if lang=='mql5' else 'Python mapping','')
  if not sm or sm.group(1 if lang=='mql5' else 2)!=st:c['MAPPING_STATUS_PARITY_ERROR']+=1
  valid_audit=isinstance(a,dict) and a.get('candidate_search_performed') is True and bool(a.get('generated_candidates')) and a.get('inspected_files',0)>0
  if not valid_audit:c['MISSING_WITHOUT_CANDIDATE_AUDIT']+=1
  found=a.get('found_candidates',[]) if isinstance(a,dict) else [];accepted=a.get('accepted_candidates',[]) if isinstance(a,dict) else [];rejected=a.get('rejected_candidates',[]) if isinstance(a,dict) else []
  if st=='MISSING':
   c['MISSING_WITH_UNREVIEWED_CANDIDATES']+=bool(found) and len(accepted)+len(rejected)<len(found);c['MISSING_WITH_ACCEPTED_CANDIDATE']+=bool(accepted);c['MISSING_WITH_NONEMPTY_ENTRIES']+=bool(arr)
  if st in NON_MISSING:c['NON_MISSING_WITH_EMPTY_ENTRIES']+=not arr
  for f in found:c['CANDIDATE_WITHOUT_SCORE']+='score' not in f
  for q in rejected:c['CANDIDATE_WITHOUT_REJECTION_REASON']+=not q.get('reason')
  c['CANDIDATE_STATUS_INCONSISTENT']+=a.get('final_status')!=st if isinstance(a,dict) else 1
  for e in arr:
   c['TOKEN_IDENTIFIER_KINDS']+=e.get('identifier_kind')=='token';path=root/e.get('file','');c['MAPPING_FILES_NOT_FOUND']+=not path.is_file();c['MAPPING_WITHOUT_DECLARATION_EVIDENCE']+=not e.get('declaration_evidence');c['MAPPING_WITHOUT_USE_EVIDENCE']+=not(e.get('read_sites') or e.get('write_sites'))
   if path.is_file() and e.get('line'):
    ok=mql_declaration(path,e['line'],e.get('identifier','')) if lang=='mql5' else python_declaration(path,e['line'],e.get('identifier',''))
    c['MAPPING_WITHOUT_DECLARATION_EVIDENCE']+=not ok
  if st=='MISSING' and mapping_text=='NOT_APPLICABLE':c['MISSING_NOT_APPLICABLE_CONFLICT']+=1
 return c
def validate(rows,recs,data,enforce_floor=True,root=ROOT):
 c=Counter();c['CANONICAL_TERMS']=len(rows);c['EXTENDED_RECORDS']=len(recs);by={x['canonical_term']:x for x in data.get('terms',[])}
 for r in rows:
  n=r['Canonical term'];d=recs.get(n,{});x=by.get(n)
  parity=[('CanonicalName','Canonical term'),('Русское название','Русское название'),('Архитектурный профиль','Profile'),('Размерность','Type'),('Unit','Unit'),('Знак','Sign'),('Projected/Actual class','Projected/Actual'),('Authoritative source','Authoritative source'),('Rounding','Rounding'),('Tolerance','Tolerance'),('Legacy aliases','Aliases'),('Статус определения','Status')]
  c['TABLE_RECORD_MISMATCH']+=sum(d.get(a,'').strip('`')!=r[b] for a,b in parity);c.update(semantic(r,d))
  if x:c.update(mapping(x,d,root))
  else:c['MISSING_WITHOUT_CANDIDATE_AUDIT']+=2
  if r['Status'] in UNRESOLVED:c['UNRESOLVED_ITEMS_WITHOUT_CONFLICT_ID']+='HSB-DOC-CONFLICT-' not in d.get('Conflict','');c['UNRESOLVED_ITEMS_WITHOUT_RESOLUTION_STAGE']+=d.get('Resolution stage','').strip('`') in {'','NOT_APPLICABLE'}
 # real similarity, exceptions must be explicit and substantive
 for i,a in enumerate(rows):
  da=recs[a['Canonical term']]
  for b in rows[i+1:]:
   db=recs[b['Canonical term']]
   if similar(da.get('Краткое определение',''),db.get('Краткое определение',''))>=.85 and not(da.get('Similarity exception reason') and db.get('Similarity exception reason')):c['NEAR_DUPLICATE_DEFINITIONS']+=1
   if similar(da.get('Lifecycle',''),db.get('Lifecycle',''))>=.85 and not(da.get('Similarity exception reason') and db.get('Similarity exception reason')):c['NEAR_DUPLICATE_LIFECYCLES']+=1
 for lang in ('mql5','python'):
  sts=Counter(x.get(lang+'_status') for x in data.get('terms',[]));prefix=lang.upper();non=sum(sts[s] for s in NON_MISSING)
  for s in ('EXACT_MATCH','SEMANTIC_MATCH','PARTIAL_MATCH','AMBIGUOUS','MISSING','NOT_APPLICABLE'):c[f'{prefix}_{s}']=sts[s]
  c[f'{prefix}_NON_MISSING']=non;c[f'{prefix}_ALL_MAPPINGS_MISSING']=int(bool(rows) and sts['MISSING']==len(rows));c[f'{prefix}_NON_MISSING_BELOW_MINIMUM']=int(enforce_floor and non<25)
  c[f'{prefix}_TERMS_WITH_CANDIDATE_AUDIT']=sum(bool(x.get('candidate_audit',{}).get(lang,{}).get('generated_candidates')) for x in data.get('terms',[]));c[f'{prefix}_TERMS_WITH_FOUND_CANDIDATES']=sum(bool(x.get('candidate_audit',{}).get(lang,{}).get('found_candidates')) for x in data.get('terms',[]));c[f'{prefix}_TERMS_WITH_ACCEPTED_CANDIDATES']=sum(bool(x.get('candidate_audit',{}).get(lang,{}).get('accepted_candidates')) for x in data.get('terms',[]));c[f'{prefix}_TERMS_WITH_REJECTED_CANDIDATES']=sum(bool(x.get('candidate_audit',{}).get(lang,{}).get('rejected_candidates')) for x in data.get('terms',[]))
 return c

def main():
 mt,rows=table(MANUAL.read_text());gt,grows=table(GLOSSARY.read_text());
 if mt!=gt or rows!=grows:print('CANONICAL_TABLE_EQUALITY=FAIL');return 1
 recs=records(GLOSSARY.read_text());data=json.loads(MAPPING.read_text());audit=json.loads(AUDIT.read_text())
 if data.get('schema_version')!='3.1.3-third-correction-1' or len(audit.get('terms',[]))!=230:print('SCHEMA_OR_AUDIT=FAIL');return 1
 c=validate(rows,recs,data)
 from test_stage_3_1_3_semantic_mutations import run_controls
 nt,np,pt,pp=run_controls(False);c['NEGATIVE_TESTS_TOTAL']=nt;c['NEGATIVE_TESTS_PASSED']=np;c['POSITIVE_TESTS_TOTAL']=pt;c['POSITIVE_TESTS_PASSED']=pp
 keys=['CANONICAL_TERMS','EXTENDED_RECORDS','MQL5_TERMS_WITH_CANDIDATE_AUDIT','PYTHON_TERMS_WITH_CANDIDATE_AUDIT','MQL5_TERMS_WITH_FOUND_CANDIDATES','PYTHON_TERMS_WITH_FOUND_CANDIDATES','MQL5_TERMS_WITH_ACCEPTED_CANDIDATES','PYTHON_TERMS_WITH_ACCEPTED_CANDIDATES','MQL5_TERMS_WITH_REJECTED_CANDIDATES','PYTHON_TERMS_WITH_REJECTED_CANDIDATES']+[f'{l}_{s}' for l in ('MQL5','PYTHON') for s in ('EXACT_MATCH','SEMANTIC_MATCH','PARTIAL_MATCH','AMBIGUOUS','MISSING','NOT_APPLICABLE','NON_MISSING','ALL_MAPPINGS_MISSING')]+BLOCKING+['NEGATIVE_TESTS_TOTAL','NEGATIVE_TESTS_PASSED','POSITIVE_TESTS_TOTAL','POSITIVE_TESTS_PASSED']
 for k in dict.fromkeys(keys):print(f'{k}={c[k]}')
 fail=[k for k in BLOCKING if c[k]];ok=not fail and nt==np and pt==pp and len(rows)==230 and c['MQL5_TERMS_WITH_CANDIDATE_AUDIT']==230 and c['PYTHON_TERMS_WITH_CANDIDATE_AUDIT']==230
 if fail:print('BLOCKING_COUNTERS='+','.join(fail))
 print('STAGE_3_1_3_THIRD_CORRECTION_VALIDATION='+('PASS' if ok else 'FAIL'));return 0 if ok else 1
if __name__=='__main__':raise SystemExit(main())
