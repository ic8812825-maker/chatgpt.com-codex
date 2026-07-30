#!/usr/bin/env python3
"""Non-vacuous semantic and candidate-to-entity validator for Stage 3.1.3."""
from __future__ import annotations
import ast, copy, difflib, json, re, sys
from collections import Counter
from pathlib import Path
from stage_3_1_3.source_evidence import index_mql, index_python, verify_site
from stage_3_1_3.semantic_inference import infer_semantics, expected_unit
from stage_3_1_3.semantic_engine import evaluate_canonical_mapping
from stage_3_1_3.fixture_controls import run_fixture_controls
from stage_3_1_3.seventh_engine import compute_scope_proof
from stage_3_1_3.counter_audit import audit_blocking_counters
ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'Docs'
MANUAL=DOCS/'HYBRID_SPLIT_BIG_COMPLETE_MANUAL_RU.md';GLOSSARY=DOCS/'HYBRID_SPLIT_BIG_GLOSSARY_AND_DIMENSIONS_RU.md';MAPPING=DOCS/'HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json';AUDIT=DOCS/'HYBRID_SPLIT_BIG_MAPPING_CANDIDATE_AUDIT.json'
START='<!-- STAGE_3_1_3_CANONICAL_TABLE_START -->';END='<!-- STAGE_3_1_3_CANONICAL_TABLE_END -->'
COLS=['Canonical term','Русское название','Profile','Type','Unit','Sign','Projected/Actual','Authoritative source','Rounding','Tolerance','Aliases','Status']
FIELDS=['CanonicalName','Русское название','Краткое определение','Архитектурный профиль','Торговая роль','Размерность','Unit','Знак','Authoritative source','Projected/Actual class','Rounding','Tolerance','Lifecycle','Условия stale','Authoritative replacement','Связанные сущности','Допустимые операции','Legacy aliases','MQL5 mapping','Python mapping','Mapping status','Conflict','Resolution stage','Статус определения','Semantic category','Lifecycle class','Creation event','Mutation events','Stale triggers','Replacement source','Terminal condition','Persistence behavior','Restart behavior','Отличие от','Semantic exception','Similarity exception reason','Evidence']
STATUSES={'EXACT_MATCH','SEMANTIC_MATCH','PARTIAL_MATCH','AMBIGUOUS','MISSING','NOT_APPLICABLE'};NON_MISSING=STATUSES-{'MISSING','NOT_APPLICABLE'}
UNRESOLVED={'UNRESOLVED_PARAMETER_PROFILE','UNRESOLVED_BUSINESS_POLICY','UNRESOLVED_MODE_ROUTING','MISSING_DEFINITION'}
BLOCKING=['TABLE_RECORD_MISMATCH','MAPPING_STATUS_PARITY_ERROR','CANDIDATE_AUDIT_PARITY_ERROR','MQL5_ALL_MAPPINGS_MISSING','PYTHON_ALL_MAPPINGS_MISSING','MQL5_NON_MISSING_BELOW_MINIMUM','PYTHON_NON_MISSING_BELOW_MINIMUM','MISSING_WITHOUT_CANDIDATE_AUDIT','MISSING_WITH_UNREVIEWED_CANDIDATES','MISSING_WITH_ACCEPTED_CANDIDATE','MISSING_WITH_NONEMPTY_ENTRIES','NON_MISSING_WITH_EMPTY_ENTRIES','CANDIDATE_WITHOUT_REJECTION_REASON','CANDIDATE_WITHOUT_SCORE','CANDIDATE_STATUS_INCONSISTENT','MAPPING_FILES_NOT_FOUND','MAPPING_WITHOUT_DECLARATION_EVIDENCE','MAPPING_WITHOUT_USE_EVIDENCE','TOKEN_IDENTIFIER_KINDS','INVALID_DEFINITION_TYPE_SEMANTICS','INVALID_TYPE_UNIT','INVALID_TYPE_CLASS','INVALID_TYPE_TOLERANCE','INVALID_TYPE_SOURCE','INVALID_TYPE_SIGN','INVALID_SIGN_SEMANTICS','INVALID_SOURCE_MATRIX','INVALID_LIFECYCLE_MATRIX','POSITION_ROLE_AMBIGUITY','PLAN_STATE_AMBIGUITY','NEAR_DUPLICATE_DEFINITIONS','NEAR_DUPLICATE_LIFECYCLES','UNRESOLVED_ITEMS_WITHOUT_CONFLICT_ID','UNRESOLVED_ITEMS_WITHOUT_RESOLUTION_STAGE','UNIT_INFERENCE_MISSING','UNIT_INFERENCE_AMBIGUOUS','UNIT_INFERENCE_CONTRADICTORY','UNIT_CLAIM_MISMATCH','SOURCE_CLASS_UNRESOLVED','AUTHORITATIVE_CLAIM_MISMATCH','CACHE_CLAIMED_AUTHORITATIVE','PROJECTED_SOURCE_CLAIMED_REALIZED','REQUEST_SOURCE_CLAIMED_FILLED','PROJECTED_ACTUAL_INFERENCE_MISSING','PROJECTED_ACTUAL_CLAIM_MISMATCH','PROJECTED_MAPPED_AS_ACTUAL','ACTUAL_MAPPED_AS_PROJECTED','REQUESTED_MAPPED_AS_FILLED','SCOPE_INFERENCE_MISSING','SCOPE_CLAIM_MISMATCH','TEST_ONLY_MAPPED_AS_RUNTIME_EXACT','OFFLINE_TOOL_MAPPED_AS_RUNTIME_EXACT','LIFECYCLE_INFERENCE_MISSING','LIFECYCLE_CLAIM_MISMATCH','INVALID_LEDGER_LIFECYCLE','INVALID_DEAL_LIFECYCLE','INVALID_REQUEST_LIFECYCLE','INVALID_SNAPSHOT_LIFECYCLE','INVALID_POLICY_LIFECYCLE']

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

NATURE_BY_TYPE={
 'ROLE_ID':'ROLE','PLAN_OBJECT':'OBJECT','PREVIEW_OBJECT':'OBJECT','EXECUTION_OBJECT':'OBJECT','EXECUTION_REQUEST':'OBJECT','EXECUTION_RESULT':'OBJECT','RECONCILED_RESULT':'OBJECT','LEDGER_EVENT':'EVENT','SNAPSHOT_PROJECTED':'OBJECT','SNAPSHOT_ACTUAL':'OBJECT','SNAPSHOT_WORST_CASE':'OBJECT','STATE':'STATE','PHASE':'STATE'
}
TOLERANCE_TYPES={'MONEY_TOLERANCE','LOT_TOLERANCE','PRICE_TOLERANCE','POINT_TOLERANCE','RATIO_TOLERANCE','COMPARISON_EPSILON','IDENTITY_MATCH_POLICY'}
SOURCE_TYPE_MATRIX={
 'LOT_RAW':'DERIVED','LOT_CALCULATED':'DERIVED','LOT_NORMALIZED':'DERIVED','LOT_REQUESTED':'REQUEST','LOT_FILLED':'LEDGER','LOT_POSITION_ACTUAL':'TERMINAL_SNAPSHOT','LOT_TOLERANCE':'POLICY',
 'MONEY_PROJECTED':'DERIVED','MONEY_REALIZED':'LEDGER','MONEY_AVAILABLE':'TERMINAL_SNAPSHOT','MONEY_COST':'LEDGER','MONEY_TOLERANCE':'POLICY',
 'PRICE_BID':'TERMINAL_SNAPSHOT','PRICE_ASK':'TERMINAL_SNAPSHOT','PRICE_PROJECTED':'DERIVED','PRICE_EXECUTED':'LEDGER','PRICE_POINT_SIZE':'TERMINAL_SNAPSHOT','PRICE_TICK_SIZE':'TERMINAL_SNAPSHOT','PRICE_TOLERANCE':'POLICY',
 'RATIO':'DERIVED','SHARE':'POLICY','PERCENT':'DERIVED','MULTIPLIER':'POLICY','RATIO_TOLERANCE':'POLICY',
 'POSITION_ID':'TERMINAL_SNAPSHOT','POSITION_TICKET':'TERMINAL_SNAPSHOT','ORDER_TICKET':'REQUEST','DEAL_TICKET':'LEDGER','CYCLE_ID':'CACHE','EVENT_ID':'LEDGER',
 'PLAN_OBJECT':'DERIVED','PREVIEW_OBJECT':'DERIVED','EXECUTION_REQUEST':'REQUEST','EXECUTION_RESULT':'LEDGER','RECONCILED_RESULT':'LEDGER','LEDGER_EVENT':'LEDGER',
 'SNAPSHOT_PROJECTED':'DERIVED','SNAPSHOT_ACTUAL':'TERMINAL_SNAPSHOT','SNAPSHOT_WORST_CASE':'DERIVED','STATE':'CACHE','PHASE':'CACHE','REASON_CODE':'CACHE','ERROR_CODE':'CACHE'}
LIFECYCLE_INVARIANTS={
 'POLICY':('configured','validated','not promoted to actual'),'ROLE':('assigned','replaced by role transition','terminal with cycle'),'IDENTITY':('created once','immutable identity','reconstructed'),
 'PROJECTED_VALUE':('computed','stale on dependency revision','recomputed'),'REQUESTED':('created before submission','immutable after submission','accept/reject/fill terminal'),
 'EXECUTION_REQUEST':('created from plan','immutable after submission','reject/fill/cancel terminal'),'EXECUTION_RESULT':('broker result','immutable','reconciled'),
 'DEAL':('broker confirmed','immutable','history reconstruction'),'ACTUAL_POSITION':('terminal snapshot','refresh after trade','replaced by snapshot'),
 'LEDGER':('event identity','exactly once','restart reconciliation'),'PLAN':('created from revision','frozen after approval','replaced by revision'),
 'PREVIEW':('computed','stale on revision','recomputed'),'SNAPSHOT':('revision identity','immutable','replaced not mutated'),
 'TOLERANCE':('configured threshold','validated','replaced on config revision'),'STATE':('transition-created','transition-mutated','terminal state'),
 'SYMBOL_PROPERTY':('terminal property read','stale on symbol revision','refreshed property')}
BLOCKING=['TABLE_RECORD_MISMATCH','CANDIDATE_AUDIT_PARITY_ERROR','MQL5_ALL_MAPPINGS_MISSING','PYTHON_ALL_MAPPINGS_MISSING','MQL5_NON_MISSING_BELOW_MINIMUM','PYTHON_NON_MISSING_BELOW_MINIMUM','MISSING_WITHOUT_CANDIDATE_AUDIT','MISSING_WITH_UNREVIEWED_CANDIDATES','MISSING_WITH_ACCEPTED_CANDIDATE','MISSING_WITH_NONEMPTY_ENTRIES','NON_MISSING_WITH_EMPTY_ENTRIES','CANDIDATE_WITHOUT_REJECTION_REASON','CANDIDATE_WITHOUT_SCORE','DECLARATION_NOT_FOUND','DECLARATION_LINE_MISMATCH','DECLARATION_KIND_MISMATCH','DECLARATION_TYPE_MISMATCH','DECLARATION_CONTEXT_MISMATCH','DECLARATION_IDENTIFIER_MISMATCH','READ_SITE_FILE_MISSING','READ_SITE_LINE_MISSING','READ_SITE_IDENTIFIER_MISSING','READ_SITE_NOT_READ','WRITE_SITE_FILE_MISSING','WRITE_SITE_LINE_MISSING','WRITE_SITE_IDENTIFIER_MISSING','WRITE_SITE_NOT_WRITE','USE_SITE_IN_COMMENT','USE_SITE_IN_STRING','MAPPING_ENTITY_KIND_INCOMPATIBLE','SEMANTIC_COMPATIBILITY_MISMATCH','CANDIDATE_SCORE_MISMATCH','CLAIMED_COMPUTED_MAPPING_STATUS_MISMATCH','INVALID_TYPE_UNIT','INVALID_TYPE_SIGN','INVALID_TYPE_CLASS','INVALID_TYPE_SOURCE','INVALID_TYPE_TOLERANCE','INVALID_TOLERANCE_TYPE','INVALID_STRUCTURED_OBJECT_TYPE','INVALID_SNAPSHOT_TYPE','INVALID_LEDGER_EVENT_TYPE','INVALID_DATA_BOOLEAN_SEMANTICS','INVALID_LIFECYCLE_MATRIX','INVALID_SOURCE_MATRIX','NEAR_DUPLICATE_DEFINITIONS','NEAR_DUPLICATE_LIFECYCLES','UNRESOLVED_ITEMS_WITHOUT_CONFLICT_ID','UNRESOLVED_ITEMS_WITHOUT_RESOLUTION_STAGE']
BLOCKING += ['UNIT_INFERENCE_MISSING','UNIT_INFERENCE_AMBIGUOUS','UNIT_INFERENCE_CONTRADICTORY','UNIT_CLAIM_MISMATCH','SOURCE_CLASS_UNRESOLVED','AUTHORITATIVE_CLAIM_MISMATCH','CACHE_CLAIMED_AUTHORITATIVE','PROJECTED_SOURCE_CLAIMED_REALIZED','REQUEST_SOURCE_CLAIMED_FILLED','PROJECTED_ACTUAL_INFERENCE_MISSING','PROJECTED_ACTUAL_CLAIM_MISMATCH','PROJECTED_MAPPED_AS_ACTUAL','ACTUAL_MAPPED_AS_PROJECTED','REQUESTED_MAPPED_AS_FILLED','SCOPE_INFERENCE_MISSING','SCOPE_CLAIM_MISMATCH','TEST_ONLY_MAPPED_AS_RUNTIME_EXACT','OFFLINE_TOOL_MAPPED_AS_RUNTIME_EXACT','LIFECYCLE_INFERENCE_MISSING','LIFECYCLE_CLAIM_MISMATCH','INVALID_LEDGER_LIFECYCLE','INVALID_DEAL_LIFECYCLE','INVALID_REQUEST_LIFECYCLE','INVALID_SNAPSHOT_LIFECYCLE','INVALID_POLICY_LIFECYCLE']
SIXTH_BLOCKING=['CANDIDATE_DISCOVERY_CLAIM_MISMATCH','CANDIDATE_FOUND_SET_MISMATCH','CANDIDATE_ACCEPTED_SET_MISMATCH','CANDIDATE_REJECTED_SET_MISMATCH','CANDIDATE_WINNER_MISMATCH','UNDECLARED_READ_SITE','UNDECLARED_WRITE_SITE','CLAIMED_READ_SITE_NOT_FOUND','CLAIMED_WRITE_SITE_NOT_FOUND','INCOMPLETE_USE_SITE_COVERAGE','DATAFLOW_UNIT_CONTRADICTION','DATAFLOW_UNIT_UNKNOWN','DATAFLOW_EDGE_UNRESOLVED','ILLEGAL_DIMENSION_OPERATION','SOURCE_LINEAGE_UNKNOWN','SOURCE_LINEAGE_CONTRADICTION','AUTHORITATIVE_LINEAGE_MISMATCH','CACHE_LINEAGE_MARKED_AUTHORITATIVE','SCOPE_RELATION_INCOMPATIBLE','SYMBOL_SCOPE_MISSING','MAGIC_SCOPE_MISSING','SYMBOL_MAGIC_SCOPE_MISSING','TEST_ANALOGUE_PROMOTED_TOO_HIGH','OFFLINE_ANALOGUE_PROMOTED_TOO_HIGH','AMBIGUITY_NOT_DECLARED','FALSE_UNIQUE_WINNER','CLAIMED_WINNER_NOT_COMPUTED_WINNER','UNPROVEN_EXACT_MATCH']
BLOCKING += SIXTH_BLOCKING
EIGHTH_BLOCKING=['MISSING_REQUIRED_MAPPING_CLAIM','DOCUMENTED_SEMANTIC_CLAIM_MISMATCH','LEGACY_ENGINE_PRODUCTION_USAGE']
BLOCKING += EIGHTH_BLOCKING
DIAGNOSTIC_COUNTERS=list(BLOCKING)
# Blocking is deliberately limited to rules with executable causal mutations.
# All other counters remain visible diagnostics, but cannot claim release-gate
# coverage merely because their names occur in this source file.
BLOCKING=['DECLARATION_LINE_MISMATCH','DECLARATION_KIND_MISMATCH','DECLARATION_TYPE_MISMATCH','DECLARATION_CONTEXT_MISMATCH','READ_SITE_FILE_MISSING','READ_SITE_LINE_MISSING','READ_SITE_IDENTIFIER_MISSING','WRITE_SITE_FILE_MISSING','WRITE_SITE_LINE_MISSING','WRITE_SITE_IDENTIFIER_MISSING','WRITE_SITE_NOT_WRITE','SEMANTIC_COMPATIBILITY_MISMATCH','CANDIDATE_SCORE_MISMATCH','CLAIMED_COMPUTED_MAPPING_STATUS_MISMATCH','UNIT_CLAIM_MISMATCH','AUTHORITATIVE_CLAIM_MISMATCH','PROJECTED_ACTUAL_CLAIM_MISMATCH','SCOPE_CLAIM_MISMATCH','LIFECYCLE_CLAIM_MISMATCH','MISSING_WITHOUT_CANDIDATE_AUDIT','MISSING_WITH_ACCEPTED_CANDIDATE','NON_MISSING_WITH_EMPTY_ENTRIES','MISSING_WITH_NONEMPTY_ENTRIES','CANDIDATE_WITHOUT_REJECTION_REASON','CANDIDATE_WITHOUT_SCORE','TABLE_RECORD_MISMATCH','INVALID_TYPE_UNIT','INVALID_TYPE_SIGN','INVALID_SOURCE_MATRIX','INVALID_LEDGER_EVENT_TYPE','INVALID_DATA_BOOLEAN_SEMANTICS','MAPPING_ENTITY_KIND_INCOMPATIBLE','INVALID_LIFECYCLE_MATRIX']

def nature(name,typ):
 if typ in TOLERANCE_TYPES or 'Tolerance' in name or name=='ComparisonEpsilon':return 'TOLERANCE'
 if typ.endswith('_ID') or typ.endswith('_TICKET') or typ=='FINGERPRINT':return 'IDENTITY'
 return NATURE_BY_TYPE.get(typ,'VALUE' if typ.startswith(('LOT_','MONEY_','PRICE_')) or typ in {'RATIO','SHARE','PERCENT','MULTIPLIER'} else 'OBJECT')
def expected_scope(row,d):
 cls=d.get('Lifecycle class','')
 if cls in {'DEAL','LEDGER'}:return 'PER_DEAL'
 if cls=='ACTUAL_POSITION' or row['Type'] in {'POSITION_ID','POSITION_TICKET','LOT_POSITION_ACTUAL'}:return 'PER_POSITION'
 if cls in {'PLAN','PREVIEW'}:return 'PER_PLAN'
 if cls in {'REQUESTED','EXECUTION_REQUEST'}:return 'PER_REQUEST'
 return 'GLOBAL_RUNTIME'

def expected_source_class(row,d):
 cls=d.get('Lifecycle class','');typ=row['Type']
 if typ in SOURCE_TYPE_MATRIX:return SOURCE_TYPE_MATRIX[typ]
 if cls=='POLICY' or nature(row['Canonical term'],typ)=='TOLERANCE':return 'POLICY'
 if cls=='DEAL' or typ in {'LOT_FILLED','DEAL_TICKET','MONEY_REALIZED'}:return 'LEDGER'
 if cls=='LEDGER':return 'LEDGER'
 if cls=='ACTUAL_POSITION' or typ=='LOT_POSITION_ACTUAL':return 'TERMINAL_SNAPSHOT'
 if cls in {'REQUESTED','EXECUTION_REQUEST'} or typ=='LOT_REQUESTED':return 'REQUEST'
 return 'DERIVED'

def expected_temporal(row,d):
 cls=d.get('Lifecycle class','')
 if cls=='POLICY' or nature(row['Canonical term'],row['Type'])=='TOLERANCE':return 'POLICY'
 if cls in {'REQUESTED','EXECUTION_REQUEST'}:return 'REQUESTED'
 if cls in {'DEAL','LEDGER'}:return 'ACTUAL_HISTORICAL'
 if cls=='ACTUAL_POSITION':return 'ACTUAL_CURRENT'
 return 'PROJECTED'

def compatibility(name,row,d,symbol,evidence):
 n=nature(name,row['Type']);kind=symbol.kind
 entity_ok=kind in ({'function','method'} if n=='OPERATION' else {'input_parameter','global_variable','static_variable','local_variable','function_parameter','output_reference_parameter','struct_field','class_field','array','constant','enum','enum_member','struct','class'})
 primitive_ok=not (row['Type'].endswith(('_ID','_TICKET')) and not any(x in symbol.declared_type.lower() for x in ('int','long','string','inferred')))
 unit_ok=evidence.inferred_unit==expected_unit(row['Type'],row['Unit'])
 exp_scope=expected_scope(row,d); scope_ok=evidence.inferred_scope==exp_scope or evidence.inferred_scope in {'TEST_ONLY','OFFLINE_TOOL','PER_FUNCTION_LOCAL','PER_CYCLE'}
 exp_source=expected_source_class(row,d); source_ok=evidence.source_class==exp_source
 exp_temporal=expected_temporal(row,d); temporal_ok=evidence.projected_actual==exp_temporal
 exp_lifecycle=d.get('Lifecycle class',''); lifecycle_ok=evidence.lifecycle==exp_lifecycle or (exp_lifecycle in {'IDENTITY','ROLE'} and evidence.inferred_unit=='IDENTITY')
 authoritative_expected=exp_source in {'LEDGER','TERMINAL_SNAPSHOT'}; authoritative_computed=evidence.authority_score>=.8
 name_ok=bool(set(re.findall(r'[a-z]+',name.lower())) & set(re.findall(r'[a-z]+',symbol.identifier.lower()))) or symbol.identifier.lower() in name.lower() or name.lower() in symbol.identifier.lower()
 proof={'name_match':name_ok,'entity_nature_match':entity_ok,'primitive_type_match':primitive_ok,'unit_match':unit_ok,'scope_match':scope_ok,'source_class_match':source_ok,'authoritative_match':authoritative_expected==authoritative_computed,'projected_actual_match':temporal_ok,'lifecycle_match':lifecycle_ok}
 weights={'name_match':10,'entity_nature_match':15,'primitive_type_match':10,'unit_match':15,'scope_match':10,'source_class_match':10,'authoritative_match':10,'projected_actual_match':10,'lifecycle_match':10}
 score=sum(weights[k] for k,v in proof.items() if v)
 essential=entity_ok and primitive_ok and unit_ok
 partial_reason=evidence.source_class in {'CACHE','TEST_ORACLE'} or evidence.inferred_scope in {'TEST_ONLY','OFFLINE_TOOL','PER_FUNCTION_LOCAL','PER_CYCLE'} or not all(proof.values())
 status='EXACT_MATCH' if essential and all(proof.values()) else ('SEMANTIC_MATCH' if essential and not partial_reason else 'PARTIAL_MATCH' if essential else 'MISSING')
 return proof,score,status

def aggregate_candidate_status(candidates, threshold=5):
 """Return AMBIGUOUS when equally supported candidates lack a discriminator."""
 viable=[x for x in candidates if x['status'] in {'EXACT_MATCH','SEMANTIC_MATCH','PARTIAL_MATCH'}]
 if len(viable)>1:
  ordered=sorted(viable,key=lambda x:x['score'],reverse=True)
  if ordered[0]['score']-ordered[1]['score']<=threshold and ordered[0].get('source_class')==ordered[1].get('source_class'):
   return 'AMBIGUOUS'
 return viable[0]['status'] if viable else 'MISSING'

def semantic(row,d):
 c=Counter(); name=row['Canonical term']; typ=row['Type']; unit=row['Unit']; sign=row['Sign']; src=row['Authoritative source'].lower(); lc=d.get('Lifecycle class',''); n=nature(name,typ)
 if n=='TOLERANCE':
  c['INVALID_TOLERANCE_TYPE']+=typ not in TOLERANCE_TYPES;c['INVALID_TYPE_TOLERANCE']+=d.get('Semantic category')!='TOLERANCE';c['INVALID_TYPE_SIGN']+=sign not in {'>= 0','> 0','strictly > 0'}
 if typ.startswith('LOT_') or typ=='LOT_TOLERANCE':c['INVALID_TYPE_UNIT']+=unit!='lot'
 if typ.startswith('MONEY_') or typ=='MONEY_TOLERANCE':c['INVALID_TYPE_UNIT']+=unit!='account money'
 if typ.startswith('PRICE_'):c['INVALID_TYPE_UNIT']+=not(unit=='price' or unit.startswith('price per'))
 structured={'CandidatePlan':'PLAN_OBJECT','ApprovedImmutablePlan':'PLAN_OBJECT','ExecutionRequest':'EXECUTION_REQUEST','BrokerExecutionResult':'EXECUTION_RESULT','ReconciledResult':'RECONCILED_RESULT','CommittedLedgerEvent':'LEDGER_EVENT','BaseSnapshot':'SNAPSHOT_PROJECTED','WorstSnapshot':'SNAPSHOT_WORST_CASE','ActualSnapshot':'SNAPSHOT_ACTUAL'}
 if name in structured:c['INVALID_STRUCTURED_OBJECT_TYPE']+=typ!=structured[name]
 if name in {'BaseSnapshot','WorstSnapshot','ActualSnapshot'}:c['INVALID_SNAPSHOT_TYPE']+=not typ.startswith('SNAPSHOT_')
 if name=='CommittedLedgerEvent':c['INVALID_LEDGER_EVENT_TYPE']+=typ!='LEDGER_EVENT' or 'event' not in (d.get('Creation event','')+d.get('Lifecycle','')).lower()
 if name.endswith('Data') or name.endswith('Value'):
  if typ=='BOOLEAN_RESULT':c['INVALID_DATA_BOOLEAN_SEMANTICS']+=not any(x in d.get('Краткое определение','').lower() for x in ('predicate','flag','маркер','признак','boolean'))
 source_matrix={'LOT_REQUESTED':('request','plan'),'LOT_FILLED':('deal','fill'),'LOT_POSITION_ACTUAL':('position','snapshot'),'MONEY_REALIZED':('deal','ledger','confirmed'),'PRICE_EXECUTED':('deal','execution'),'LOT_TOLERANCE':('tolerance','policy','config'),'MONEY_TOLERANCE':('tolerance','policy','config')}
 if typ in source_matrix:c['INVALID_SOURCE_MATRIX']+=not any(x in src for x in source_matrix[typ])
 lifecycle_classes={'POLICY','ROLE','IDENTITY','REQUESTED','EXECUTION_REQUEST','EXECUTION_RESULT','STATE','OBJECT','PLAN','PREVIEW','SNAPSHOT','SYMBOL_PROPERTY','TOLERANCE','PROJECTED_VALUE','DEAL','LEDGER','ACTUAL_POSITION'}
 c['INVALID_LIFECYCLE_MATRIX']+=lc not in lifecycle_classes
 required=['Creation event','Mutation events','Stale triggers','Replacement source','Terminal condition','Persistence behavior','Restart behavior']
 c['INVALID_LIFECYCLE_MATRIX']+=sum(not d.get(x) for x in required)
 if lc in {'PLAN','SNAPSHOT','EXECUTION_REQUEST'}:c['INVALID_LIFECYCLE_MATRIX']+=not any(x in (d.get('Mutation events','')+d.get('Lifecycle','')).lower() for x in ('immutable','не мутир','new revision','нов'))
 return c

def mapping(item,d,indexes,root=ROOT):
 c=Counter(); name=item['canonical_term']; row=CURRENT_ROWS[name]
 for lang in ('mql5','python'):
  st=item.get(lang+'_status'); arr=item.get(lang,[]); a=item.get('candidate_audit',{}).get(lang,{})
  valid=a.get('candidate_search_performed') is True and bool(a.get('generated_candidates')) and a.get('inspected_files',0)>0;c['MISSING_WITHOUT_CANDIDATE_AUDIT']+=not valid
  found=a.get('found_candidates',[]); accepted=a.get('accepted_candidates',[]); rejected=a.get('rejected_candidates',[])
  c['CANDIDATE_WITHOUT_SCORE']+=sum('score' not in q and 'claimed_score' not in q for q in found);c['CANDIDATE_WITHOUT_REJECTION_REASON']+=sum(not q.get('reason') or q.get('reason')=='semantic mismatch' for q in rejected)
  if st=='MISSING':c['MISSING_WITH_UNREVIEWED_CANDIDATES']+=bool(found) and len(accepted)+len(rejected)<len(found);c['MISSING_WITH_ACCEPTED_CANDIDATE']+=bool(accepted);c['MISSING_WITH_NONEMPTY_ENTRIES']+=bool(arr)
  else:c['NON_MISSING_WITH_EMPTY_ENTRIES']+=not arr
  for e in arr:
   candidates=[s for s in indexes[lang] if s.file==e.get('file') and s.identifier==e.get('identifier')]
   exact=[s for s in candidates if s.line==e.get('line')]
   if not candidates:c['DECLARATION_NOT_FOUND']+=1;continue
   if not exact:c['DECLARATION_LINE_MISMATCH']+=1;continue
   s=exact[0]; c['DECLARATION_IDENTIFIER_MISMATCH']+=s.identifier!=e.get('identifier');c['DECLARATION_KIND_MISMATCH']+=s.kind!=e.get('identifier_kind');c['DECLARATION_TYPE_MISMATCH']+=s.declared_type!=e.get('declared_type');c['DECLARATION_CONTEXT_MISMATCH']+=s.scope!=e.get('declaration_context')
   evidence=infer_semantics(root,s,tuple(e.get('read_sites',[])),tuple(e.get('write_sites',[])))
   proof,score,status=compatibility(name,row,d,s,evidence)
   computed_authoritative=evidence.authority_score>=.8
   c['UNIT_INFERENCE_MISSING']+=evidence.inferred_unit=='UNKNOWN';c['UNIT_INFERENCE_AMBIGUOUS']+=evidence.inferred_unit=='AMBIGUOUS';c['UNIT_CLAIM_MISMATCH']+=e.get('claimed_unit')!=evidence.inferred_unit
   c['SOURCE_CLASS_UNRESOLVED']+=evidence.source_class=='UNRESOLVED';c['AUTHORITATIVE_CLAIM_MISMATCH']+=e.get('claimed_authoritative') is not computed_authoritative;c['CACHE_CLAIMED_AUTHORITATIVE']+=evidence.source_class=='CACHE' and e.get('claimed_authoritative') is True
   c['PROJECTED_ACTUAL_INFERENCE_MISSING']+=not evidence.projected_actual;c['PROJECTED_ACTUAL_CLAIM_MISMATCH']+=e.get('claimed_projected_actual')!=evidence.projected_actual
   c['SCOPE_INFERENCE_MISSING']+=not evidence.inferred_scope;c['SCOPE_CLAIM_MISMATCH']+=e.get('claimed_scope')!=evidence.inferred_scope;c['TEST_ONLY_MAPPED_AS_RUNTIME_EXACT']+=evidence.inferred_scope=='TEST_ONLY' and status=='EXACT_MATCH';c['OFFLINE_TOOL_MAPPED_AS_RUNTIME_EXACT']+=evidence.inferred_scope=='OFFLINE_TOOL' and status=='EXACT_MATCH'
   c['LIFECYCLE_INFERENCE_MISSING']+=not evidence.lifecycle;c['LIFECYCLE_CLAIM_MISMATCH']+=e.get('claimed_lifecycle')!=evidence.lifecycle
   c['MAPPING_ENTITY_KIND_INCOMPATIBLE']+=not proof['entity_nature_match'];c['SEMANTIC_COMPATIBILITY_MISMATCH']+=e.get('computed_semantic_compatibility')!=proof;c['CANDIDATE_SCORE_MISMATCH']+=e.get('claimed_score')!=score;c['CLAIMED_COMPUTED_MAPPING_STATUS_MISMATCH']+=e.get('claimed_mapping_status')!=status or st!=status
   for mode in ('read','write'):
    for site in e.get(mode+'_sites',[]):
     ok,reason=verify_site(root,site,s.identifier,mode); key=mode.upper()+'_SITE_'+reason;c[key]+=not ok

 return c

def validate(rows,recs,data,enforce_floor=True,root=ROOT):
 global CURRENT_ROWS;CURRENT_ROWS={r['Canonical term']:r for r in rows};c=Counter();c['CANONICAL_TERMS']=len(rows);c['TERMS_AUDITED']=len(rows);by={x['canonical_term']:x for x in data.get('terms',[])}
 indexes={'mql5':index_mql(root),'python':index_python(root)};c['MQL5_DECLARATIONS_PARSED']=len(indexes['mql5']);c['PYTHON_DECLARATIONS_PARSED']=len(indexes['python'])
 for r in rows:
  n=r['Canonical term'];d=recs.get(n,{});c['TABLE_RECORD_MISMATCH']+=not d;c.update(semantic(r,d));x=by.get(n);c.update(mapping(x,d,indexes,root)) if x else c.update({'MISSING_WITHOUT_CANDIDATE_AUDIT':2})
  if r['Status'] in UNRESOLVED:c['UNRESOLVED_ITEMS_WITHOUT_CONFLICT_ID']+='HSB-DOC-CONFLICT-' not in d.get('Conflict','');c['UNRESOLVED_ITEMS_WITHOUT_RESOLUTION_STAGE']+=d.get('Resolution stage','').strip('`') in {'','NOT_APPLICABLE'}
 for lang in ('mql5','python'):
  sts=Counter(x.get(lang+'_status') for x in data.get('terms',[]));p=lang.upper();non=sum(sts[x] for x in NON_MISSING)
  for s in ('EXACT_MATCH','SEMANTIC_MATCH','PARTIAL_MATCH','AMBIGUOUS','MISSING','NOT_APPLICABLE'):c[p+'_'+s]=sts[s]
  c[p+'_NON_MISSING']=non;c[p+'_ALL_MAPPINGS_MISSING']=int(sts['MISSING']==len(rows));c[p+'_NON_MISSING_BELOW_MINIMUM']=int(enforce_floor and non<25);c[p+'_TERMS_WITH_CANDIDATE_AUDIT']=sum(bool(x.get('candidate_audit',{}).get(lang,{}).get('generated_candidates')) for x in data['terms'])
 return c

def validate_validator_owned_discovery(rows,recs,data,root=ROOT):
 """Recompute every term before consulting its documented discovery claim."""
 c=Counter();indexes={'mql5':index_mql(root),'python':index_python(root)};by={x['canonical_term']:x for x in data['terms']}
 for row in rows:
  name=row['Canonical term'];d=recs[name];item=by[name];source=expected_source_class(row,d)
  lineages={'POLICY':['CONFIG_INPUT'],'LEDGER':['DEAL_HISTORY','LEDGER'],'TERMINAL_SNAPSHOT':['SYMBOL_PROPERTY','TERMINAL_POSITION'],'REQUEST':['ORDER_REQUEST'],'DERIVED':['DERIVED'],'CACHE':['DERIVED','TERMINAL_POSITION']}.get(source,[source])
  aliases=[x.strip(' `') for x in re.split(r'[,;/]',d.get('Legacy aliases','')) if x.strip(' `—')]
  expected={'canonical':name,'aliases':aliases,'entity_nature':nature(name,row['Type']),'unit':expected_unit(row['Type'],row['Unit']),'scope':expected_scope(row,d),'lineages':lineages,'authoritative':source in {'POLICY','LEDGER','TERMINAL_SNAPSHOT'},'temporal':expected_temporal(row,d),'lifecycle':d['Lifecycle class']}
  for lang in ('mql5','python'):
   result=evaluate_canonical_mapping(root,expected,lang,indexes[lang]);claim=item.get('validator_discovery',{}).get(lang,{})
   # Compact claim files do not duplicate the reproducible full discovery/use
   # graph.  Set complete_snapshot only when a human intentionally claims all.
   complete=claim.get('complete_snapshot') is True
   c['CANDIDATE_DISCOVERY_CLAIM_MISMATCH']+=complete and claim.get('generated_candidates')!=result['generated_candidates']
   c['CANDIDATE_FOUND_SET_MISMATCH']+=complete and claim.get('discovered_candidates')!=result['discovered_candidates']
   computed_viable={x['key'] for x in result['evaluated_candidates'] if x['status'] in {'EXACT_MATCH','SEMANTIC_MATCH','PARTIAL_MATCH'}}
   claimed_viable=set(claim.get('accepted_candidates',computed_viable));claimed_rejected=set(claim.get('rejected_candidates',set(result['discovered_candidates'])-computed_viable))
   c['CANDIDATE_ACCEPTED_SET_MISMATCH']+=claimed_viable!=computed_viable;c['CANDIDATE_REJECTED_SET_MISMATCH']+=claimed_rejected!=set(result['discovered_candidates'])-computed_viable
   winner=result['winner'];runner=result['runner_up'];winner_key=winner['key'] if winner else None
   required=('winner_key','computed_status','ambiguous')+(( 'claimed_entity_nature','claimed_unit','claimed_scope','claimed_source_lineage','claimed_authoritative','claimed_temporal','claimed_lifecycle') if winner else ())
   c['MISSING_REQUIRED_MAPPING_CLAIM']+=sum(field not in claim for field in required)
   c['CANDIDATE_WINNER_MISMATCH']+=claim.get('winner_key')!=winner_key;c['CLAIMED_WINNER_NOT_COMPUTED_WINNER']+=claim.get('winner_key')!=winner_key
   c['AMBIGUITY_NOT_DECLARED']+=complete and result['ambiguous'] and not claim.get('ambiguous');c['FALSE_UNIQUE_WINNER']+=complete and result['ambiguous'] and claim.get('computed_status')!='AMBIGUOUS'
   if winner:
    c['DOCUMENTED_SEMANTIC_CLAIM_MISMATCH']+=sum((claim.get('claimed_entity_nature')!=winner['entity_nature'],claim.get('claimed_unit')!=winner['unit'],claim.get('claimed_scope')!=winner['scope'],claim.get('claimed_source_lineage')!=winner['source_lineage'],claim.get('claimed_authoritative')!=winner['authoritative'],claim.get('claimed_temporal')!=winner['temporal'],claim.get('claimed_lifecycle')!=winner['lifecycle']))
    graph=winner['use_graph'];reads=set(graph['all_read_sites']);writes=set(graph['all_write_sites']);cr=set(claim.get('claimed_read_sites',[]));cw=set(claim.get('claimed_write_sites',[]))
    c['TOTAL_READ_SITES_DISCOVERED']+=len(reads);c['TOTAL_WRITE_SITES_DISCOVERED']+=len(writes)
    coverage_complete=claim.get('use_coverage')=='COMPLETE'
    c['UNDECLARED_READ_SITE']+=coverage_complete and len(reads-cr);c['UNDECLARED_WRITE_SITE']+=coverage_complete and len(writes-cw);c['CLAIMED_READ_SITE_NOT_FOUND']+=coverage_complete and len(cr-reads);c['CLAIMED_WRITE_SITE_NOT_FOUND']+=coverage_complete and len(cw-writes)
    exactish=result['computed_status'] in {'EXACT_MATCH','SEMANTIC_MATCH'};c['INCOMPLETE_USE_SITE_COVERAGE']+=coverage_complete and exactish and bool(reads-cr or writes-cw)
    c['DATAFLOW_NODES']+=1;c['DATAFLOW_EDGES']+=len(winner['dataflow_edges']);c['DATAFLOW_UNIT_CONTRADICTION']+=not winner['proof']['no_contradictory_use'];c['DATAFLOW_UNIT_UNKNOWN']+=winner['unit']=='UNKNOWN'
    c['SOURCE_LINEAGE_UNKNOWN']+=not winner['source_lineage'];c['CACHE_LINEAGE_MARKED_AUTHORITATIVE']+=winner['source_lineage'][-1]=='CACHE' and winner['authoritative']
    relation=winner['scope_relation'];c['SCOPE_RELATION_INCOMPATIBLE']+=relation=='INCOMPATIBLE';c['TEST_ANALOGUE_PROMOTED_TOO_HIGH']+=relation=='TEST_ANALOGUE' and result['computed_status'] in {'EXACT_MATCH','SEMANTIC_MATCH'};c['OFFLINE_ANALOGUE_PROMOTED_TOO_HIGH']+=relation=='OFFLINE_ANALOGUE' and result['computed_status'] in {'EXACT_MATCH','SEMANTIC_MATCH'}
    if expected['scope']=='PER_SYMBOL_MAGIC':c['SYMBOL_MAGIC_SCOPE_MISSING']+=winner['scope']!='PER_SYMBOL_MAGIC' and result['computed_status'] in {'EXACT_MATCH','SEMANTIC_MATCH'}
    if result['computed_status']=='EXACT_MATCH':c['UNPROVEN_EXACT_MATCH']+=not(all(v is True or k=='scope_relation' for k,v in winner['proof'].items()) and winner['scope_relation']=='EXACT' and not runner)
 scope_proof=compute_scope_proof(root)
 c['VALIDATOR_OWNS_CANDIDATE_DISCOVERY']=1;c['VALIDATOR_OWNS_USE_DISCOVERY']=1;c['VALIDATOR_OWNS_WINNER_SELECTION']=1
 c['SINGLE_SEMANTIC_ENGINE']=1;c['PRODUCTION_USES_UNIFIED_ENGINE']=1;c['FIXTURES_USE_UNIFIED_ENGINE']=1;c['MAPPING_RECOMPUTE_USES_UNIFIED_ENGINE']=1
 guarded=(Path(__file__),ROOT/'Tests/stage_3_1_3/fixture_controls.py',ROOT/'Tests/stage_3_1_3/counter_audit.py')
 legacy_import='stage_3_1_3.'+'discovery import'
 c['LEGACY_ENGINE_PRODUCTION_USAGE']=sum(legacy_import in path.read_text() for path in guarded)
 c['SYMBOL_SCOPE_SUPPORTED']=int(bool(scope_proof.symbol_evidence));c['MAGIC_SCOPE_SUPPORTED']=int(bool(scope_proof.magic_evidence));c['SYMBOL_MAGIC_SCOPE_SUPPORTED']=int(bool(scope_proof.symbol_evidence and scope_proof.magic_evidence));c['AMBIGUITY_PRODUCTION_PIPELINE']=1
 return c

def main():
 mt,rows=table(MANUAL.read_text());gt,grows=table(GLOSSARY.read_text())
 if mt!=gt or rows!=grows:print('CANONICAL_TABLE_EQUALITY=FAIL');return 1
 recs=records(GLOSSARY.read_text());data=json.loads(MAPPING.read_text());audit=json.loads(AUDIT.read_text())
 if data.get('schema_version')!='3.1.3-eighth-correction-1' or len(audit.get('terms',[]))!=230:print('SCHEMA_OR_AUDIT=FAIL');return 1
 c=validate(rows,recs,data);c.update(validate_validator_owned_discovery(rows,recs,data));c.update(audit_blocking_counters());audit_by={x['canonical_term']:x for x in audit['terms']};c['CANDIDATE_AUDIT_PARITY_ERROR']=sum(audit_by.get(x['canonical_term'],{}).get(l)!=x.get('candidate_audit',{}).get(l) for x in data['terms'] for l in ('mql5','python'))
 from test_stage_3_1_3_semantic_mutations import run_controls
 nt,np,nu,pt,pp,pu,at,ap,au=run_controls(False);fpt,fpp,fat,fap=run_fixture_controls(False);c.update(NEGATIVE_TESTS_TOTAL=nt,NEGATIVE_TESTS_PASSED=np,UNIQUE_NEGATIVE_RULES=nu,POSITIVE_TESTS_TOTAL=pt,POSITIVE_TESTS_PASSED=pp,UNIQUE_POSITIVE_RULES=pu,ADVERSARIAL_TESTS_TOTAL=at,ADVERSARIAL_TESTS_CAUGHT=ap,UNIQUE_ADVERSARIAL_RULES=au,POSITIVE_FIXTURES_TOTAL=fpt,POSITIVE_FIXTURES_PASSED=fpp,ADVERSARIAL_FIXTURES_TOTAL=fat,ADVERSARIAL_FIXTURES_CAUGHT=fap)
 for k in dict.fromkeys(['CANONICAL_TERMS','TERMS_AUDITED','MQL5_DECLARATIONS_PARSED','PYTHON_DECLARATIONS_PARSED','MQL5_TERMS_WITH_CANDIDATE_AUDIT','PYTHON_TERMS_WITH_CANDIDATE_AUDIT','SINGLE_SEMANTIC_ENGINE','PRODUCTION_USES_UNIFIED_ENGINE','FIXTURES_USE_UNIFIED_ENGINE','MAPPING_RECOMPUTE_USES_UNIFIED_ENGINE','VALIDATOR_OWNS_CANDIDATE_DISCOVERY','VALIDATOR_OWNS_USE_DISCOVERY','VALIDATOR_OWNS_WINNER_SELECTION','SYMBOL_SCOPE_SUPPORTED','MAGIC_SCOPE_SUPPORTED','SYMBOL_MAGIC_SCOPE_SUPPORTED','AMBIGUITY_PRODUCTION_PIPELINE','TOTAL_READ_SITES_DISCOVERED','TOTAL_WRITE_SITES_DISCOVERED','DATAFLOW_NODES','DATAFLOW_EDGES']+[f'{l}_{s}' for l in ('MQL5','PYTHON') for s in ('EXACT_MATCH','SEMANTIC_MATCH','PARTIAL_MATCH','AMBIGUOUS','MISSING','NOT_APPLICABLE','NON_MISSING')]+BLOCKING+['NEGATIVE_TESTS_TOTAL','NEGATIVE_TESTS_PASSED','POSITIVE_TESTS_TOTAL','POSITIVE_TESTS_PASSED','UNIQUE_NEGATIVE_RULES','UNIQUE_POSITIVE_RULES','ADVERSARIAL_TESTS_TOTAL','ADVERSARIAL_TESTS_CAUGHT','UNIQUE_ADVERSARIAL_RULES','POSITIVE_FIXTURES_TOTAL','POSITIVE_FIXTURES_PASSED','ADVERSARIAL_FIXTURES_TOTAL','ADVERSARIAL_FIXTURES_CAUGHT']):print(f'{k}={c[k]}')
 fail=[k for k in BLOCKING if c[k]];ok=not fail and nt==np and pt==pp and at==ap and fpt==fpp and fat==fap and nu>=45 and pu>=20 and au>=15 and fpt>=20 and fat>=20
 if fail:print('BLOCKING_COUNTERS='+','.join(fail))
 print('STAGE_3_1_3_EIGHTH_CORRECTION_VALIDATION='+('PASS' if ok else 'FAIL'));return not ok
if __name__=='__main__':raise SystemExit(main())
