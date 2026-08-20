#!/usr/bin/env python3
"""Fail-closed comment/literal-first MQL5 lexer and conservative guard proof."""
from dataclasses import dataclass
import re
@dataclass(frozen=True)
class Token: kind:str;value:str;active:bool;start:int;end:int
@dataclass
class PPFrame: parent_active:bool;branch_already_taken:bool;current_branch_active:bool;else_seen:bool
class LexerError(ValueError):pass

def _lex_physical(src):
 out=[];i=0;n=len(src)
 while i<n:
  if src.startswith('//',i):
   j=src.find('\n',i);j=n if j<0 else j;out.append(Token('LINE_COMMENT',src[i:j],False,i,j));i=j;continue
  if src.startswith('/*',i):
   j=src.find('*/',i+2)
   if j<0:raise LexerError('unterminated block comment')
   j+=2;out.append(Token('BLOCK_COMMENT',src[i:j],False,i,j));i=j;continue
  if src[i] in ('"',"'"):
   q=src[i];j=i+1;esc=False
   while j<n:
    if src[j]=='\n' and not esc:raise LexerError('unterminated literal')
    if esc:esc=False
    elif src[j]=='\\':esc=True
    elif src[j]==q:break
    j+=1
   if j>=n:raise LexerError('unterminated literal')
   j+=1;out.append(Token('STRING_LITERAL' if q=='"' else 'CHAR_LITERAL',src[i:j],False,i,j));i=j;continue
  j=i+1
  while j<n and not src.startswith('//',j) and not src.startswith('/*',j) and src[j] not in ('"',"'"):j+=1
  out.append(Token('PHYSICAL_CODE',src[i:j],True,i,j));i=j
 return out

def _masked_physical(src):
 chars=list(src)
 for t in _lex_physical(src):
  if not t.active:
   for i in range(t.start,t.end):
    if chars[i]!='\n':chars[i]=' '
 return ''.join(chars)

def _eval(expr,defined):
 e=expr.strip()
 if e=='0':return False
 if e=='1':return True
 m=re.fullmatch(r'defined\s*\(?\s*([A-Za-z_]\w*)\s*\)?',e)
 if m:return m.group(1) in defined
 m=re.fullmatch(r'!\s*defined\s*\(?\s*([A-Za-z_]\w*)\s*\)?',e)
 if m:return m.group(1) not in defined
 raise LexerError('unsupported preprocessor expression')
def _preprocess(src):
 masked=_masked_physical(src);lines=masked.splitlines(True);disabled=set();stack=[];defined=set();off=0
 # exact conventional include guard: first two nonblank directives
 nonblank=[(i,x) for i,x in enumerate(lines) if x.strip()]
 guard=None
 if len(nonblank)>=2:
  a=re.fullmatch(r'\s*#\s*ifndef\s+([A-Za-z_]\w*)\s*(?:\n)?',nonblank[0][1]);b=re.fullmatch(r'\s*#\s*define\s+([A-Za-z_]\w*)\s*(?:\n)?',nonblank[1][1])
  if a and b and a.group(1)==b.group(1):guard=a.group(1)
 for li,line in enumerate(lines):
  m=re.match(r'\s*#\s*(\w+)\b(.*)',line);active=all(f.current_branch_active for f in stack) if stack else True
  if m:
   op,arg=m.group(1),m.group(2).strip();disabled.update(range(off,off+len(line)))
   if op=='define':
    if active and re.fullmatch(r'[A-Za-z_]\w*',arg):defined.add(arg)
   elif op in ('if','ifdef','ifndef'):
    parent=active
    if op=='if':cond=_eval(arg,defined)
    elif op=='ifdef':
     if not re.fullmatch(r'[A-Za-z_]\w*',arg):raise LexerError('invalid ifdef')
     cond=arg in defined
    else:
     if not re.fullmatch(r'[A-Za-z_]\w*',arg):raise LexerError('invalid ifndef')
     cond=(arg not in defined) or (not stack and arg==guard)
    stack.append(PPFrame(parent,parent and cond,parent and cond,False))
   elif op=='elif':
    if not stack:raise LexerError('unmatched elif')
    f=stack[-1]
    if f.else_seen:raise LexerError('elif after else')
    cond=_eval(arg,defined);f.current_branch_active=f.parent_active and not f.branch_already_taken and cond;f.branch_already_taken|=f.current_branch_active
   elif op=='else':
    if not stack:raise LexerError('unmatched else')
    f=stack[-1]
    if f.else_seen:raise LexerError('second else')
    f.else_seen=True;f.current_branch_active=f.parent_active and not f.branch_already_taken;f.branch_already_taken=True
   elif op=='endif':
    if not stack:raise LexerError('unmatched endif')
    stack.pop()
   elif op in ('include','property'):pass
   else:raise LexerError('unsupported preprocessor directive')
  elif not active:disabled.update(range(off,off+len(line)))
  off+=len(line)
 if stack:raise LexerError('unterminated conditional block')
 return disabled

def tokenize_mql5(src):
 disabled=_preprocess(src);physical=_lex_physical(src);nonactive=[]
 for t in physical:
  if not t.active:nonactive.append(t)
 out=[];i=0;n=len(src);by_start={t.start:t for t in nonactive}
 while i<n:
  if i in by_start:out.append(by_start[i]);i=by_start[i].end;continue
  if i in disabled:
   j=i+1
   while j<n and j in disabled and j not in by_start:j+=1
   out.append(Token('DISABLED_PREPROCESSOR_CODE',src[i:j],False,i,j));i=j;continue
  c=src[i]
  if c.isspace():
   j=i+1
   while j<n and src[j].isspace() and j not in disabled and j not in by_start:j+=1
   out.append(Token('WHITESPACE',src[i:j],True,i,j));i=j;continue
  m=re.match(r'[A-Za-z_]\w*|(?:\d+\.\d*|\.\d+|\d+)',src[i:])
  if m:
   v=m.group();out.append(Token('IDENTIFIER' if v[0].isalpha() or v[0]=='_' else 'NUMERIC_LITERAL',v,True,i,i+len(v)));i+=len(v);continue
  op=next((x for x in ('!=','==','&&','||','<=','>=','++','--','+=','-=','->') if src.startswith(x,i)),None)
  if op:out.append(Token('OPERATOR',op,True,i,i+len(op)));i+=len(op);continue
  out.append(Token('PUNCTUATION' if c in '(){}[];,.' else 'OPERATOR',c,True,i,i+1));i+=1
 return out
def strip_non_active_tokens(src):return ''.join(t.value if t.active and t.kind not in ('STRING_LITERAL','CHAR_LITERAL') else ' '*(t.end-t.start) for t in tokenize_mql5(src))
def active_compact(src):return re.sub(r'\s+','',strip_non_active_tokens(src))
def extract_function(src,name):
 a=active_compact(src);m=re.search(re.escape(name)+r'\([^;]*?\)\{',a)
 if not m:raise LexerError('function not found')
 start=a.find('{',m.start());depth=0
 for i in range(start,len(a)):
  if a[i]=='{':depth+=1
  elif a[i]=='}':
   depth-=1
   if depth==0:return a[m.start():i+1]
 raise LexerError('unterminated function')
def _balanced(s,pos,o='(',c=')'):
 if pos>=len(s) or s[pos]!=o:raise LexerError('expected '+o)
 d=0
 for i in range(pos,len(s)):
  if s[i]==o:d+=1
  elif s[i]==c:
   d-=1
   if d==0:return s[pos+1:i],i+1
 raise LexerError('unbalanced '+o)
def _args(s):
 out=[];start=0;d=0
 for i,ch in enumerate(s):
  if ch in '([{':d+=1
  elif ch in ')]}':d-=1
  elif ch==',' and d==0:out.append(s[start:i]);start=i+1
 out.append(s[start:]);return out
SAFE_REJECT_STATUSES={'HSBI_DECISION_REJECTED','HSBI_DECISION_UNAVAILABLE','HSBI_DECISION_STALE','HSBI_DECISION_CONFLICT','HSBI_DECISION_RECONCILIATION_REQUIRED','HSBI_DECISION_PERSISTENCE_REQUIRED'}
def normalize_condition(s):
 s=s.strip();
 while s.startswith('(') and s.endswith(')'):
  try:x,e=_balanced(s,0)
  except LexerError:break
  if e!=len(s):break
  s=x
 if s.startswith('!'):
  inner=s[1:]
  while inner.startswith('(') and inner.endswith(')'):
   try:x,e=_balanced(inner,0)
   except LexerError:break
   if e!=len(inner):break
   inner=x
  n=normalize_condition(inner)
  if n.startswith('!'):return normalize_condition(n[1:])
  if '==' in n:return n.replace('==','!=',1)
  if '!=' in n:return n.replace('!=','==',1)
  return '!'+n
 for op in ('||','&&'):
  parts=[];start=0;d=0
  for i,ch in enumerate(s):
   d+=ch=='(';d-=ch==')'
   if d==0 and s.startswith(op,i):parts.append(normalize_condition(s[start:i]));start=i+len(op)
  if parts:parts.append(normalize_condition(s[start:]));return op.join(sorted(parts))
 for op in ('!=','=='):
  d=0
  for i,ch in enumerate(s):
   d+=ch=='(';d-=ch==')'
   if d==0 and s.startswith(op,i):
    left,right=normalize_condition(s[:i]),normalize_condition(s[i+2:])
    if right in ('true','false'):
     positive=(op=='==' and right=='true') or (op=='!=' and right=='false');return left if positive else normalize_condition('!'+left)
    return op.join(sorted((left,right)))
 return s
def conditions_equivalent(a,b):return normalize_condition(a)==normalize_condition(b)
def _return_expression(body,pos):
 i=pos+6;d=0
 while i<len(body):
  c=body[i];d+=c in '([';d-=c in ')]'
  if c==';' and d==0:return body[pos+6:i],i+1
  i+=1
 raise LexerError('unterminated return')
def analyze_return_paths(src,function):
 fn=extract_function(src,function);body=fn[fn.find('{')+1:-1];out=[];i=0;depth=0
 while i<len(body):
  if body[i]=='{':depth+=1;i+=1;continue
  if body[i]=='}':depth-=1;i+=1;continue
  if body.startswith('return',i):
   expr,e=_return_expression(body,i);kind='UNKNOWN_FAIL_CLOSED';status=reason=''
   if expr.startswith('HSBI_RuntimeReject('):
    call,_=_balanced(expr,len('HSBI_RuntimeReject'));args=_args(call);status=args[1] if len(args)>1 else '';reason=args[2] if len(args)>2 else ''
    if re.fullmatch(r'[A-Za-z_]\w*',status) and status in SAFE_REJECT_STATUSES:kind='PROVEN_REJECT'
    elif status=='HSBI_DECISION_NO_OP':kind='UNAUTHORIZED_NO_OP'
    elif status=='HSBI_DECISION_VALID':kind='PROVEN_SUCCESS'
   elif expr=='admission' and body[max(0,i-40):i].endswith('if(!admission.valid)'):kind='PROVEN_REJECT'
   out.append({'FUNCTION':function,'RETURN_INDEX':len(out)+1,'SOURCE_POSITION':i,'ENCLOSING_DEPTH':depth,'RETURN_EXPRESSION':expr,'RETURN_EXPRESSION_KIND':'CALL' if '(' in expr else 'OBJECT','CALLEE':expr.split('(',1)[0] if '(' in expr else '','STATUS_EXPRESSION':status,'REASON_EXPRESSION':reason,'CLASSIFICATION':kind,'SAFE':kind=='PROVEN_REJECT'});i=e;continue
  i+=1
 return out
def prove_top_level_guard(src,function,condition,status,reason):
 fn=extract_function(src,function);body=fn[fn.find('{')+1:-1];i=0;depth=0;prior_return=False;candidates=[]
 while i<len(body):
  if body[i]=='{':depth+=1;i+=1;continue
  if body[i]=='}':depth-=1;i+=1;continue
  if depth==0 and body.startswith('return',i):prior_return=True
  if depth==0 and body.startswith('if(',i):
   cond,j=_balanced(body,i+2);k=j
   if body.startswith('returnHSBI_RuntimeReject(',k):
    call,e=_balanced(body,k+len('returnHSBI_RuntimeReject'));args=_args(call)
    candidates.append((cond,args,not prior_return,i));semi=body.find(';',e);i=(semi+1 if semi>=0 else e);continue
   if k<len(body) and body[k]!='{':
    semi=body.find(';',k);i=(semi+1 if semi>=0 else j);continue
  i+=1
 matching=[x for x in candidates if conditions_equivalent(x[0],condition)]
 exact=[x for x in matching if len(x[1])>=3 and x[1][1]==status and x[1][2]==reason and x[2]]
 wrong_status=[x for x in matching if len(x[1])<3 or x[1][1]!=status]
 wrong_reason=[x for x in matching if len(x[1])>=3 and x[1][1]==status and x[1][2]!=reason]
 pos=exact[0][3] if len(exact)==1 else -1;prefix=body[:pos] if pos>=0 else body
 paths=[p for p in analyze_return_paths(src,function) if p['SOURCE_POSITION']<pos] if pos>=0 else analyze_return_paths(src,function)
 early_success=sum(p['CLASSIFICATION']=='PROVEN_SUCCESS' for p in paths)
 noop_paths=sum(p['CLASSIFICATION']=='UNAUTHORIZED_NO_OP' for p in paths)
 unknown_returns=sum(p['CLASSIFICATION'] in ('UNKNOWN_FAIL_CLOSED','UNAUTHORIZED_NO_OP') for p in paths)
 present=bool(matching);unique=len(matching)==1;reachable=len(exact)==1
 dominates=reachable and unique and not early_success and unknown_returns==0
 return {'FUNCTION':function,'CONDITION':condition,'GUARD_PRESENT':present,'GUARD_UNIQUE':unique,
  'GUARD_CONDITION_EXACT':any(x[0]==condition for x in matching),'GUARD_CONDITION_EXACT_OR_SUPPORTED_EQUIVALENT':present,'REJECT_STATUS':status,'REASON_CODE':reason,
  'REJECT_CALL_EXACT':len(exact)==1,'REJECT_STATUS_EXACT':len(exact)==1,
  'REJECT_REASON_EXACT':len(exact)==1,'REACHABLE':reachable,'BEFORE_SUCCESS':dominates,
  'CANONICAL_CONDITION':condition,'NORMALIZED_CONDITION':normalize_condition(condition),'EXPECTED_STATUS':status,'EXPECTED_REASON':reason,'MATCHING_PATHS':len(matching),'EXPECTED_OUTCOME_PATHS':len(exact),'WRONG_STATUS_PATHS':len(wrong_status),'WRONG_REASON_PATHS':len(wrong_reason),'NO_OP_PATHS':noop_paths,'SUCCESS_PATHS':early_success,'UNKNOWN_PATHS':unknown_returns-noop_paths,
  'SUCCESS_RETURNS_FOUND':early_success,'EARLY_SUCCESS_RETURNS':early_success,
  'UNKNOWN_RETURNS':unknown_returns,'GUARD_ON_ALL_SUCCESS_PATHS':dominates,
  'DOMINATES_EXECUTION':dominates,'DOMINATES_EXPECTED_OUTCOME':dominates,'DOMINATES_SUCCESS':dominates,'RESULT':'PASS' if dominates else 'FAIL'}

def prove_reject_constructor(src):
 fn=extract_function(src,'HSBI_RuntimeReject');sw=re.findall(r'r\.status=([^;]+);',fn);rw=re.findall(r'r\.reason=([^;]+);',fn);vw=re.findall(r'r\.valid=([^;]+);',fn);returns=re.findall(r'return([^;]+);',fn)
 controls=sum(fn.count(x) for x in ('if(','while(','for(','switch('));ok=('ZeroMemory(r);' in fn and sw==['status'] and rw==['reason'] and not vw and controls==0 and returns==['r'])
 return {'ZERO_MEMORY_CALLED':'ZeroMemory(r);' in fn,'STATUS_ASSIGNED_EXACTLY_ONCE':len(sw)==1,'STATUS_SOURCE':sw[0] if len(sw)==1 else 'UNPROVEN','REASON_ASSIGNED_EXACTLY_ONCE':len(rw)==1,'REASON_SOURCE':rw[0] if len(rw)==1 else 'UNPROVEN','VALID_WRITES':len(vw),'STATUS_SECONDARY_WRITES':max(0,len(sw)-1),'REASON_SECONDARY_WRITES':max(0,len(rw)-1),'CONDITIONAL_BLOCKS':controls,'RETURN_COUNT':len(returns),'RETURNED_OBJECT':returns[0] if len(returns)==1 else 'UNPROVEN','REJECT_CONSTRUCTOR_PROOF':'PASS' if ok else 'FAIL'}
def parse_enum_map(src,name):
 a=active_compact(src);m=re.search(r'enum'+re.escape(name)+r'\{([^}]*)\}',a)
 if not m:raise LexerError('enum not found')
 value=-1;out={}
 for item in _args(m.group(1)):
  if not item:continue
  if '=' in item:k,v=item.split('=',1);value=int(v,0)
  else:k=item;value+=1
  out[k]=value
 return out

def prove_unique_final_success(src,function,required_conditions):
 fn=extract_function(src,function);body=fn[fn.find('{')+1:-1]
 positions=[body.find('if('+c+')') for c in required_conditions]
 final=body.find('HSBI_RuntimeDecisionResultr=HSBI_RuntimeReject(')
 valid_call=final>=0 and 'HSBI_DECISION_VALID' in body[final:body.find(';',final)]
 valid_flag=body.count('r.valid=true;')==1;unique=body.count('HSBI_DECISION_VALID')==1
 after=final>max(positions) if positions and min(positions)>=0 else False
 top_level=final>=0 and body[:final].count('{')==body[:final].count('}')
 ok=valid_call and valid_flag and unique and after and top_level and body.endswith('returnr;')
 return {'FINAL_SUCCESS_EXISTS':final>=0,'FINAL_SUCCESS_UNIQUE':unique,
  'FINAL_SUCCESS_AFTER_ALL_REQUIRED_GUARDS':after,'FINAL_SUCCESS_TOP_LEVEL':top_level,
  'FINAL_SUCCESS_STATUS':'HSBI_DECISION_VALID' if valid_call else 'UNPROVEN',
  'FINAL_SUCCESS_VALID_FLAG':valid_flag,'RESULT':'PASS' if ok else 'FAIL'}
def lexer_self_tests():
 t={};active=lambda s:active_compact(s)
 t['L001']='inty;' in active('string s="//";int y;');t['L002']='inty;' in active('string s="/* */";int y;');t['L003']='bad' not in active('//bad\nok;');t['L004']='bad' not in active('/*bad*/ok;')
 for key,s in [('L005','/*'),('L006','"x')]:
  try:tokenize_mql5(s);t[key]=False
  except LexerError:t[key]=True
 t['L007']='bad' not in active('#if 0\nbad;\n#endif\nok;');t['L008']='ok;' in active('#ifndef G\n#define G\nok;\n#endif');t['L009']='bad' not in active('#if 0\n#if 1\nbad;\n#endif\n#endif');
 try:tokenize_mql5('#if 0\nx');t['L010']=False
 except LexerError:t['L010']=True
 for n,d in [(11,'else'),(12,'elif 1'),(13,'endif'),(14,'if 1')]:t[f'L{n:03}']='guard' not in active('#if 0\n/*\n#'+d+'\n*/\nguard;\n#endif')
 t['L015']='guard' not in active('#if 0\n"#else"\nguard;\n#endif');t['L016']='guard' not in active("#if 0\n'#'\nguard;\n#endif");t['L017']='bad' not in active('#if 0\n#if 0\nbad;\n#endif\n#endif');t['L018']='bad' not in active('#if 1\nok;\n#elif 1\nbad;\n#endif')
 for key,s in [('L019','#if 1\n#else\n#else\n#endif'),('L020','#if 0\n#else\n#elif 1\n#endif'),('L021','#if 1\nx'),('L022','#if X\nx\n#endif')]:
  try:tokenize_mql5(s);t[key]=False
  except LexerError:t[key]=True
 t['L023']='ok;' in active('#ifndef G\n#define G\nok;\n#endif');t['L024']='ok;ok;' in active('#ifndef G\n#define G\nok;\nok;\n#endif')
 canonical='R F(){if(x!=y)return HSBI_RuntimeReject(x,BAD,WHY,"x");HSBI_RuntimeDecisionResult r=HSBI_RuntimeReject(x,HSBI_DECISION_VALID,OK,"v");r.valid=true;return r;}'
 def gp(s):return prove_top_level_guard(s,'F','x!=y','BAD','WHY')
 t['L025']=gp(canonical.replace('if(x!=y)','if(x!=y){R q=HSBI_RuntimeReject(x,HSBI_DECISION_VALID,OK,"b");q.valid=true;return q;}if(x!=y)',1))['RESULT']=='FAIL'
 t['L026']=gp(canonical.replace('if(x!=y)','if(x!=y)return Unknown(x);if(x!=y)',1))['RESULT']=='FAIL'
 t['L027']=gp(canonical.replace('if(x!=y)','if(x==y){}else{R q;q.valid=true;return q;}if(x!=y)',1))['RESULT']=='FAIL'
 t['L028']=gp(canonical.replace('if(x!=y)','R q;q.valid=true;return q;if(x!=y)',1))['RESULT']=='FAIL'
 t['L029']=gp(canonical.replace('if(x!=y)','R q;q.status=HSBI_DECISION_VALID;return q;if(x!=y)',1))['RESULT']=='FAIL'
 t['L030']=gp(canonical.replace('if(x!=y)','return Unknown(x);if(x!=y)',1))['RESULT']=='FAIL'
 t['L031']=prove_unique_final_success(canonical.replace('if(x!=y)','if(z){R q=HSBI_RuntimeReject(x,HSBI_DECISION_VALID,OK,"b");q.valid=true;return q;}if(x!=y)',1),'F',['x!=y'])['RESULT']=='FAIL'
 t['L032']=prove_reject_constructor('R HSBI_RuntimeReject(A x,S status,Q reason,string z){R r;r.status=status;r.reason=reason;r.valid=true;return r;}')['REJECT_CONSTRUCTOR_PROOF']=='FAIL'
 t['L033']=prove_reject_constructor('R HSBI_RuntimeReject(A x,S status,Q reason,string z){R r;r.status=HSBI_DECISION_VALID;r.reason=reason;return r;}')['REJECT_CONSTRUCTOR_PROOF']=='FAIL'
 t['L034']=gp(canonical)['RESULT']=='PASS'
 t['L035']=gp(canonical.replace('if(x!=y)','R q;q.valid=true;return q;if(x!=y)',1))['DOMINATES_SUCCESS'] is False
 t['L036']=prove_unique_final_success(canonical,'F',['x!=y'])['RESULT']=='PASS'
 def unsafe(st):return analyze_return_paths('R F(){return HSBI_RuntimeReject(x,'+st+',WHY,"x");}','F')[0]['CLASSIFICATION']=='UNKNOWN_FAIL_CLOSED'
 t['L037']=unsafe('0');t['L038']=unsafe('(S)0');t['L039']=unsafe('alias');t['L040']=unsafe('c?BAD:HSBI_DECISION_VALID');t['L041']=unsafe('GetStatus()')
 t['L042']=conditions_equivalent('a!=b','b!=a');t['L043']=conditions_equivalent('a==b','b==a')
 base='R HSBI_RuntimeReject(A x,S status,Q reason,string z){R r;ZeroMemory(r);r.status=status;r.reason=reason;return r;}'
 t['L044']=prove_reject_constructor(base.replace('r.status=status;','r.valid=1;r.status=status;'))['REJECT_CONSTRUCTOR_PROOF']=='FAIL'
 t['L045']=prove_reject_constructor(base.replace('r.status=status;','r.valid=(bool)1;r.status=status;'))['REJECT_CONSTRUCTOR_PROOF']=='FAIL'
 t['L046']=prove_reject_constructor(base.replace('r.status=status;','r.valid=(status==HSBI_DECISION_VALID);r.status=status;'))['REJECT_CONSTRUCTOR_PROOF']=='FAIL'
 t['L047']=prove_reject_constructor(base.replace('r.status=status;','r.status=status;r.status=BAD;'))['REJECT_CONSTRUCTOR_PROOF']=='FAIL'
 t['L048']=prove_reject_constructor(base.replace('r.reason=reason;','r.reason=reason;r.reason=OK;'))['REJECT_CONSTRUCTOR_PROOF']=='FAIL'
 t['L049']=prove_reject_constructor(base)['REJECT_CONSTRUCTOR_PROOF']=='PASS'
 bypass=canonical.replace('if(x!=y)','if(y!=x)return HSBI_RuntimeReject(x,(S)0,OK,"b");if(x!=y)',1)
 t['L050']=gp(bypass)['RESULT']=='FAIL' and prove_reject_constructor(base.replace('r.status=status;','r.valid=(status==(S)0);r.status=status;'))['REJECT_CONSTRUCTOR_PROOF']=='FAIL'
 noop='return HSBI_RuntimeReject(x,HSBI_DECISION_NO_OP,HSBI_RD_OK,"n");'
 t['L051']=analyze_return_paths('R F(){'+noop+'}','F')[0]['SAFE'] is False
 s37='R HSBI_ValidateRestartedRuntimeState(){if(s.duplicateConsumption)'+noop+'}'
 t['L052']=prove_top_level_guard(s37,'HSBI_ValidateRestartedRuntimeState','s.duplicateConsumption','HSBI_DECISION_NO_OP','HSBI_RD_OK')['RESULT']=='PASS'
 t['L053']=prove_top_level_guard(s37.replace('HSBI_RD_OK','BAD'),'HSBI_ValidateRestartedRuntimeState','s.duplicateConsumption','HSBI_DECISION_NO_OP','HSBI_RD_OK')['RESULT']=='FAIL'
 t['L054']=analyze_return_paths('R Wrong(){'+noop+'}','Wrong')[0]['CLASSIFICATION']=='UNAUTHORIZED_NO_OP'
 t['L055']=gp(canonical.replace('if(x!=y)','if(!(y==x))'+noop+'if(x!=y)',1))['RESULT']=='FAIL'
 t['L056']=gp(canonical.replace('if(x!=y)','if(p)'+noop+'if(x!=y)',1))['RESULT']=='FAIL'
 t['L057']=conditions_equivalent('!(a==b)','a!=b');t['L058']=conditions_equivalent('!(a!=b)','a==b');t['L059']=conditions_equivalent('!!(a!=b)','a!=b')
 t['L060']=conditions_equivalent('(a==b)==false','a!=b');t['L061']=conditions_equivalent('(a==b)!=true','a!=b')
 t['L062']=not conditions_equivalent('Unknown(a,b,c)','a!=b')
 t['L063']=gp(canonical.replace('if(x!=y)','if(!(y==x))return HSBI_RuntimeReject(x,OTHER,WHY,"b");if(x!=y)',1))['RESULT']=='FAIL'
 t['L064']=gp(canonical.replace('if(x!=y)','if(!(y==x))return HSBI_RuntimeReject(x,BAD,OTHER,"b");if(x!=y)',1))['RESULT']=='FAIL'
 t['L065']=gp(canonical.replace('if(x!=y)','if(!(y==x))'+noop+'if(x!=y)',1))['RESULT']=='FAIL'
 return t
