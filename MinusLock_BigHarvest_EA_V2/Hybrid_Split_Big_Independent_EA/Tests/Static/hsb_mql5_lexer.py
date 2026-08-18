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
 exact=[x for x in candidates if x[0]==condition and len(x[1])>=3 and x[1][1]==status and x[1][2]==reason and x[2]]
 return {'FUNCTION':function,'CONDITION':condition,'REJECT_STATUS':status,'REASON_CODE':reason,'REACHABLE':bool(exact),'BEFORE_SUCCESS':bool(exact),'DOMINATES_SUCCESS':bool(exact),'RESULT':'PASS' if exact else 'FAIL'}
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
 return t
