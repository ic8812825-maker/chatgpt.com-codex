#!/usr/bin/env python3
"""Conservative comment/string/preprocessor-aware MQL5 lexer."""
from dataclasses import dataclass
import re
@dataclass(frozen=True)
class Token: kind:str; value:str; active:bool; start:int; end:int
class LexerError(ValueError):pass

def _disabled_lines(src):
 lines=src.splitlines(True);disabled=set();stack=[];defines=set();offset=0
 for line in lines:
  m=re.match(r'\s*#\s*(\w+)(?:\s+([A-Za-z_]\w*|0|1))?',line);parent=all(x for x in stack) if stack else True
  if m:
   op,arg=m.group(1),m.group(2)
   if op=='define' and parent and arg:defines.add(arg)
   elif op in ('if','ifdef','ifndef'):
    if op=='if':cond=arg=='1'
    elif op=='ifdef':cond=arg in defines
    else:cond=arg not in defines
    # conventional outer include guard is active
    if op=='ifndef' and not stack and arg and re.search(r'^\s*#\s*define\s+'+re.escape(arg)+r'\b',src[sum(len(x) for x in lines[:lines.index(line)+1]):],re.M):cond=True
    stack.append(parent and cond)
   elif op=='else':
    if not stack:raise LexerError('unmatched #else')
    prior=stack.pop();outer=all(stack) if stack else True;stack.append(outer and not prior)
   elif op=='elif':
    if not stack:raise LexerError('unmatched #elif')
    stack[-1]=(all(stack[:-1]) if len(stack)>1 else True) and arg=='1'
   elif op=='endif':
    if not stack:raise LexerError('unmatched #endif')
    stack.pop()
   disabled.update(range(offset,offset+len(line)))
  elif stack and not all(stack):disabled.update(range(offset,offset+len(line)))
  offset+=len(line)
 if stack:raise LexerError('unterminated preprocessor block')
 return disabled

def tokenize_mql5(src):
 disabled=_disabled_lines(src);out=[];i=0;n=len(src)
 while i<n:
  active=i not in disabled;c=src[i]
  if i in disabled:
   j=i+1
   while j<n and j in disabled:j+=1
   out.append(Token('DISABLED_PREPROCESSOR_CODE',src[i:j],False,i,j));i=j;continue
  if src.startswith('//',i):
   j=src.find('\n',i);j=n if j<0 else j;out.append(Token('LINE_COMMENT',src[i:j],False,i,j));i=j;continue
  if src.startswith('/*',i):
   j=src.find('*/',i+2)
   if j<0:raise LexerError('unterminated block comment')
   j+=2;out.append(Token('BLOCK_COMMENT',src[i:j],False,i,j));i=j;continue
  if c in ('"',"'"):
   quote=c;j=i+1;esc=False
   while j<n:
    if esc:esc=False
    elif src[j]=='\\':esc=True
    elif src[j]==quote:break
    j+=1
   if j>=n:raise LexerError('unterminated literal')
   j+=1;out.append(Token('STRING_LITERAL' if quote=='"' else 'CHAR_LITERAL',src[i:j],False,i,j));i=j;continue
  if c.isspace():
   j=i+1
   while j<n and src[j].isspace() and j not in disabled:j+=1
   out.append(Token('WHITESPACE',src[i:j],True,i,j));i=j;continue
  m=re.match(r'[A-Za-z_]\w*|(?:\d+\.\d*|\.\d+|\d+)',src[i:])
  if m:
   val=m.group();kind='IDENTIFIER' if val[0].isalpha() or val[0]=='_' else 'NUMERIC_LITERAL';out.append(Token(kind,val,True,i,i+len(val)));i+=len(val);continue
  op=next((x for x in ('!=','==','&&','||','<=','>=','++','--','+=','-=','->') if src.startswith(x,i)),None)
  if op:out.append(Token('OPERATOR',op,True,i,i+len(op)));i+=len(op);continue
  out.append(Token('PUNCTUATION' if c in '(){}[];,.' else 'OPERATOR',c,True,i,i+1));i+=1
 return out

def strip_non_active_tokens(src):return ''.join(t.value if t.active and t.kind not in ('STRING_LITERAL','CHAR_LITERAL') else ' '*(t.end-t.start) for t in tokenize_mql5(src))
def active_compact(src):return re.sub(r'\s+','',strip_non_active_tokens(src))
def extract_function(src,name):
 active=strip_non_active_tokens(src);m=re.search(r'\b'+re.escape(name)+r'\s*\([^;]*?\)\s*\{',active,re.S)
 if not m:raise LexerError('function not found: '+name)
 start=active.find('{',m.start());depth=0
 for i in range(start,len(active)):
  if active[i]=='{':depth+=1
  elif active[i]=='}':
   depth-=1
   if depth==0:return active[m.start():i+1]
 raise LexerError('unterminated function')
def find_active_condition(fn,compact_condition):return compact_condition in re.sub(r'\s+','',fn)
def find_active_return(fn,status,reason):
 c=re.sub(r'\s+','',fn);return 'returnHSBI_RuntimeReject(' in c and status in c and reason in c
def prove_guard_before_success(fn,guard):
 c=re.sub(r'\s+','',fn);g=c.find(guard);return g>=0 and not re.search(r'valid=true;return\w+;',c[:g])
def prove_reject_status(fn,status):return status in re.sub(r'\s+','',fn)
def prove_reason_code(fn,reason):return reason in re.sub(r'\s+','',fn)
def lexer_self_tests():
 tests={}
 tests['L001']='//x' not in strip_non_active_tokens('string s="//x";int y;') and 'inty;' in active_compact('string s="//x";int y;')
 tests['L002']='/*x*/' not in strip_non_active_tokens('string s="/*x*/";int y;')
 tests['L003']='bad' not in active_compact('// bad\nint ok;')
 tests['L004']='bad' not in active_compact('/* bad */ int ok;')
 try:tokenize_mql5('/*');tests['L005']=False
 except LexerError:tests['L005']=True
 try:tokenize_mql5('"x');tests['L006']=False
 except LexerError:tests['L006']=True
 tests['L007']='bad' not in active_compact('#if 0\nbad();\n#endif\nok();')
 tests['L008']='ok();' in active_compact('#ifndef G\n#define G\nok();\n#endif')
 tests['L009']='bad' not in active_compact('#if 0\n#if 1\nbad();\n#endif\n#endif\nok();')
 try:tokenize_mql5('#if 0\nx');tests['L010']=False
 except LexerError:tests['L010']=True
 return tests
