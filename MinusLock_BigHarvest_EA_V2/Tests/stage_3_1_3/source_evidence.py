"""Source-derived declaration and use evidence for Stage 3.1.3.

This deliberately does not consume mapping JSON.  JSON fields are claims which the
validator compares with the index produced here.
"""
from __future__ import annotations

import ast
import re
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass(frozen=True)
class Symbol:
    identifier: str
    kind: str
    declared_type: str
    file: str
    line: int
    column: int
    scope: str
    parent_symbol: str
    modifiers: tuple[str, ...]
    declaration_text: str

    def dict(self):
        value = asdict(self)
        value["modifiers"] = list(self.modifiers)
        return value


def sanitise(text: str) -> tuple[str, set[int], set[int]]:
    """Blank comments/strings without changing line numbers."""
    out = list(text); comments: set[int] = set(); strings: set[int] = set()
    i = 0; line = 1
    while i < len(out):
        if text.startswith("//", i):
            while i < len(out) and out[i] != "\n": comments.add(line); out[i] = " "; i += 1
        elif text.startswith("/*", i):
            comments.add(line); out[i:i+2] = "  "; i += 2
            while i < len(out) and not text.startswith("*/", i):
                comments.add(line)
                if out[i] == "\n": line += 1
                else: out[i] = " "
                i += 1
            if i < len(out): out[i:i+2] = "  "; i += 2
        elif out[i] in "\"'":
            quote = out[i]; strings.add(line); out[i] = " "; i += 1
            while i < len(out):
                strings.add(line)
                if out[i] == "\\": out[i] = " "; i += 1; out[i] = " " if i < len(out) else ""; i += 1; continue
                if out[i] == quote: out[i] = " "; i += 1; break
                if out[i] == "\n": line += 1
                else: out[i] = " "
                i += 1
        else:
            if out[i] == "\n": line += 1
            i += 1
    return "".join(out), comments, strings


TYPE = r"(?:const\s+)?(?:unsigned\s+)?[A-Za-z_][A-Za-z0-9_:<>]*"
NAME = r"[A-Za-z_][A-Za-z0-9_]*"


def index_mql(root: Path) -> list[Symbol]:
    symbols: list[Symbol] = []
    for path in sorted([*root.rglob("*.mq5"), *root.rglob("*.mqh")]):
        raw = path.read_text(errors="ignore"); clean, _, _ = sanitise(raw); lines = clean.splitlines(); raw_lines = raw.splitlines()
        stack: list[tuple[str, str, int]] = []; pending: tuple[str, str] | None = None; depth = 0
        for no, line in enumerate(lines, 1):
            stripped = line.strip(); scope = stack[-1] if stack else ("module", "", 0)
            macro = re.match(r"\s*#\s*define\s+(%s)\b" % NAME, line)
            aggregate = re.match(r"\s*(struct|class|enum)\s+(%s)\b" % NAME, line)
            func = re.match(rf"\s*(?:{TYPE}\s+)?({NAME})\s*\((.*)\)\s*(?:const\s*)?(?:\{{|$)", line)
            if macro:
                symbols.append(Symbol(macro.group(1), "macro", "macro", str(path.relative_to(root)), no, macro.start(1)+1, "module", "", (), raw_lines[no-1].strip()))
            if aggregate:
                kind, name = aggregate.groups(); symbols.append(Symbol(name, kind, kind, str(path.relative_to(root)), no, aggregate.start(2)+1, "module", "", (), raw_lines[no-1].strip())); pending=(kind,name)
            if func and not re.match(r"\s*(if|for|while|switch|return)\b", line):
                name, params = func.groups(); parent = stack[-1][1] if stack and stack[-1][0] == "class" else ""; kind = "method" if parent else "function"
                rtype = stripped.split(name,1)[0].strip() or "constructor"
                symbols.append(Symbol(name, kind, rtype, str(path.relative_to(root)), no, func.start(1)+1, f"{kind} {name}", parent, (), raw_lines[no-1].strip()))
                for pm in re.finditer(rf"(?:^|,)\s*({TYPE})\s*([&*]?)\s*({NAME})(?:\s*\[.*?\])?", params):
                    typ, ref, pn = pm.groups(); pk="output_reference_parameter" if ref else "function_parameter"; col=max(1,line.find(pn)+1)
                    symbols.append(Symbol(pn,pk,typ.replace("const ",""),str(path.relative_to(root)),no,col,f"{kind} {name}",name,("const",) if typ.startswith("const ") else (),raw_lines[no-1].strip()))
                pending=(kind,name)
            # declarations ending in semicolon, excluding calls/returns/assignments
            dm = re.match(rf"\s*(input\s+|static\s+|const\s+)?({TYPE})\s+([&*]?)\s*({NAME})(\s*\[[^]]*\])?\s*(?:=[^;]*)?;\s*$", line)
            if dm and not func:
                mod, typ, ref, name, array = dm.groups(); parent=scope[1];
                if scope[0] in {"struct","class"}: kind=scope[0]+"_field"
                elif mod and mod.strip()=="input": kind="input_parameter"
                elif mod and mod.strip()=="static": kind="static_variable"
                elif scope[0] in {"function","method"}: kind="local_variable"
                else: kind="constant" if mod and mod.strip()=="const" else "global_variable"
                if array: kind="array"
                symbols.append(Symbol(name,kind,typ.replace("const ",""),str(path.relative_to(root)),no,line.find(name)+1,f"{scope[0]} {parent}" if parent else "module",parent,tuple(x for x in ((mod or '').strip(),"reference" if ref else "") if x),raw_lines[no-1].strip()))
            if scope[0] == "enum" and re.match(rf"\s*{NAME}\s*(?:=|,|$)", line) and not aggregate:
                em=re.match(rf"\s*({NAME})",line); symbols.append(Symbol(em.group(1),"enum_member",scope[1],str(path.relative_to(root)),no,em.start(1)+1,f"enum {scope[1]}",scope[1],(),raw_lines[no-1].strip()))
            opens=line.count("{"); closes=line.count("}")
            if pending and opens: stack.append((pending[0],pending[1],depth+opens)); pending=None
            depth += opens-closes
            while stack and depth < stack[-1][2]: stack.pop()
    return symbols


def index_python(root: Path) -> list[Symbol]:
    result=[]
    for path in sorted(root.rglob("*.py")):
        try: tree=ast.parse(path.read_text(errors="ignore"))
        except SyntaxError: continue
        rel=str(path.relative_to(root)); parents={c:p for p in ast.walk(tree) for c in ast.iter_child_nodes(p)}
        def context(n):
            q=n
            while q in parents:
                q=parents[q]
                if isinstance(q,(ast.FunctionDef,ast.AsyncFunctionDef)): return f"function {q.name}",q.name
                if isinstance(q,ast.ClassDef): return f"class {q.name}",q.name
            return "module",""
        for n in ast.walk(tree):
            scope,parent=context(n)
            if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
                kind="class" if isinstance(n,ast.ClassDef) else ("method" if scope.startswith("class ") else "function"); result.append(Symbol(n.name,kind,"callable" if kind!="class" else "class",rel,n.lineno,n.col_offset+1,scope,parent,(),ast.get_source_segment(path.read_text(errors='ignore'),n).splitlines()[0]))
                for a in getattr(getattr(n,"args",None),"args",[]):
                    typ=ast.unparse(a.annotation) if a.annotation else "inferred"; result.append(Symbol(a.arg,"function_parameter",typ,rel,a.lineno,a.col_offset+1,f"function {n.name}",n.name,(),a.arg))
            elif isinstance(n,(ast.Assign,ast.AnnAssign)):
                targets=n.targets if isinstance(n,ast.Assign) else [n.target]
                for t in targets:
                    for z in ast.walk(t):
                        if isinstance(z,ast.Name):
                            typ=ast.unparse(n.annotation) if isinstance(n,ast.AnnAssign) and n.annotation else "inferred"; kind="local_variable" if scope.startswith("function ") else ("class_field" if scope.startswith("class ") else "global_variable")
                            result.append(Symbol(z.id,kind,typ,rel,n.lineno,z.col_offset+1,scope,parent,(),ast.get_source_segment(path.read_text(errors='ignore'),n) or z.id)); break
    return result


def verify_site(root: Path, site: str, identifier: str, mode: str) -> tuple[bool,str]:
    try: file, number=site.rsplit(":",1); number=int(number)
    except ValueError: return False,"LINE_MISSING"
    path=root/file
    if not path.is_file(): return False,"FILE_MISSING"
    raw=path.read_text(errors="ignore"); clean,comments,strings=sanitise(raw); lines=clean.splitlines()
    if not 0<number<=len(lines): return False,"LINE_MISSING"
    if number in comments and not lines[number-1].strip(): return False,"IN_COMMENT"
    if number in strings and not re.search(rf"\b{re.escape(identifier)}\b",lines[number-1]): return False,"IN_STRING"
    line=lines[number-1]
    if not re.search(rf"\b{re.escape(identifier)}\b",line): return False,"IDENTIFIER_MISSING"
    lhs=rf"(?:\b\w+\s*\.\s*)?\b{re.escape(identifier)}\b(?:\s*\[[^]]+\])?"
    write=bool(re.search(lhs+r"\s*(?:\+\+|--|[+\-*/]?=(?!=))",line) or re.search(r"(?:\+\+|--)\s*"+lhs,line))
    if mode=="write": return (write,"OK" if write else "NOT_WRITE")
    # A read is any executable occurrence not solely the declaration or assignment LHS.
    declaration=bool(re.match(rf"\s*(?:input\s+|static\s+|const\s+)?{TYPE}\s+[&*]?\s*{re.escape(identifier)}\b",line))
    rhs=line.split("=",1)[1] if "=" in line and not re.search(r"[=!<>]=",line) else line
    read=bool(re.search(rf"\b{re.escape(identifier)}\b",rhs)) and not (declaration and ";" in line and "=" not in line)
    return (read,"OK" if read else "NOT_READ")
