#!/usr/bin/env python3
"""Stage 3.1.3 second-correction semantic documentation validator.

This validator checks typed glossary records, table parity, mapping evidence, and
real source declarations/uses.  It does not validate trading mathematics.
"""
from __future__ import annotations
import ast
import copy
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "Docs"
MANUAL = DOCS / "HYBRID_SPLIT_BIG_COMPLETE_MANUAL_RU.md"
GLOSSARY = DOCS / "HYBRID_SPLIT_BIG_GLOSSARY_AND_DIMENSIONS_RU.md"
MAPPING = DOCS / "HYBRID_SPLIT_BIG_IDENTIFIER_MAPPING.json"
START = "<!-- STAGE_3_1_3_CANONICAL_TABLE_START -->"
END = "<!-- STAGE_3_1_3_CANONICAL_TABLE_END -->"
COLUMNS = ["Canonical term", "Русское название", "Profile", "Type", "Unit", "Sign", "Projected/Actual", "Authoritative source", "Rounding", "Tolerance", "Aliases", "Status"]
TERM_STATUS = {"APPROVED_TERM", "DOCUMENTED_NOT_APPROVED", "UNRESOLVED_PARAMETER_PROFILE", "UNRESOLVED_BUSINESS_POLICY", "UNRESOLVED_MODE_ROUTING", "MISSING_DEFINITION"}
UNRESOLVED = {x for x in TERM_STATUS if x.startswith("UNRESOLVED") or x == "MISSING_DEFINITION"}
MAP_STATUS = {"EXACT_MATCH", "SEMANTIC_MATCH", "PARTIAL_MATCH", "AMBIGUOUS", "MISSING", "LEGACY_ONLY", "SPLIT_ONLY", "HYBRID_ONLY", "DOCUMENTATION_ONLY", "NOT_APPLICABLE"}
PROVEN = {"EXACT_MATCH", "SEMANTIC_MATCH", "PARTIAL_MATCH", "LEGACY_ONLY", "SPLIT_ONLY", "HYBRID_ONLY"}
KINDS = {"input_parameter", "global_variable", "local_variable", "function_parameter", "function_return", "function", "method", "struct", "struct_field", "class", "class_field", "enum", "enum_member", "constant", "macro", "array", "map_key", "object_property", "CSV_column", "JSON_field", "test_fixture", "test_oracle_variable", "test_assertion_target", "comment_only", "string_literal_only", "not_found"}
NON_CODE_KINDS = {"comment_only", "string_literal_only", "not_found"}
FIELDS = ["CanonicalName", "Русское название", "Краткое определение", "Архитектурный профиль", "Торговая роль", "Размерность", "Unit", "Знак", "Допустимый диапазон", "Источник возникновения", "Authoritative source", "Время фиксации", "Projected/Actual class", "Normalization", "Rounding", "Tolerance", "Lifecycle", "Условия stale", "Authoritative replacement", "Допустимые операции", "Запрещённые подмены", "Связанные сущности", "Legacy aliases", "MQL5 mapping", "Python mapping", "Mapping status", "Conflict", "Resolution stage", "Статус определения", "Semantic category", "Lifecycle class", "Creation event", "Validation event", "Freeze/confirmation event", "Mutation events", "Stale triggers", "Replacement source", "Terminal condition", "Persistence behavior", "Restart behavior", "Отличие от", "Semantic exception", "Evidence"]
BLOCKING = ["INVALID_DEFINITION_TYPE_SEMANTICS", "INVALID_TYPE_UNIT", "INVALID_TYPE_CLASS", "INVALID_TYPE_TOLERANCE", "INVALID_TYPE_SOURCE", "INVALID_ACTUAL_ROUNDING", "INVALID_LIFECYCLE_CLASS", "TOKEN_IDENTIFIER_KINDS", "MAPPING_WITHOUT_DECLARATION_EVIDENCE", "MAPPING_WITHOUT_USE_EVIDENCE", "IDENTIFIER_ONLY_IN_COMMENT", "IDENTIFIER_ONLY_IN_STRING", "UNPROVEN_EXACT_MAPPING", "UNPROVEN_SEMANTIC_MAPPING", "CACHE_MARKED_AUTHORITATIVE", "MAPPING_STATUS_PARITY_ERROR", "MISSING_NOT_APPLICABLE_CONFLICT", "NORMALIZED_DUPLICATE_LIFECYCLES", "GENERIC_LIFECYCLES", "NEAR_DUPLICATE_DEFINITIONS", "DEFINITIONS_WITHOUT_DISTINGUISHING_CLAUSE", "FORBIDDEN_PROJECTED_TO_ACTUAL_TRANSITION", "UNRESOLVED_POLICY_APPROVED", "UNRESOLVED_ITEMS_WITHOUT_CONFLICT_ID", "UNRESOLVED_ITEMS_WITHOUT_RESOLUTION_STAGE", "TABLE_RECORD_MISMATCH", "MAPPING_RECORDS_MISSING", "MAPPING_FILES_NOT_FOUND", "MAPPING_STATUS_INVALID"]

@dataclass
class Symbol:
    name: str
    kind: str
    context: str
    declared_type: str
    declaration: str
    line: int
    reads: int = 0
    writes: int = 0


def canonical_table(text: str):
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError("canonical table markers")
    raw = text.split(START, 1)[1].split(END, 1)[0].strip()
    lines = [x for x in raw.splitlines() if x.startswith("|")]
    header = [x.strip() for x in lines[0].strip("|").split("|")]
    if header != COLUMNS:
        raise ValueError(f"canonical columns: {header}")
    return raw, [dict(zip(header, [x.strip() for x in line.strip("|").split("|")])) for line in lines[2:]]


def extended_records(text: str):
    result = {}
    for match in re.finditer(r"^### ([A-Za-z][A-Za-z0-9]*)\n(.*?)(?=^### |\Z)", text, re.M | re.S):
        body = match.group(2)
        item = {}
        for field in FIELDS:
            found = re.search(rf"^{re.escape(field)}:\s*(.+)$", body, re.M)
            item[field] = found.group(1).strip() if found else ""
        if item["CanonicalName"]:
            result[match.group(1)] = item
    return result


def strip_mql(text: str):
    comments = "\n".join(re.findall(r"//[^\n]*|/\*.*?\*/", text, re.S))
    strings = "\n".join(re.findall(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', text))
    clean = re.sub(r"//[^\n]*|/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    clean = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', lambda m: " " * len(m.group(0)), clean)
    return clean, comments, strings


def parse_mql(path: Path):
    raw = path.read_text(errors="ignore")
    clean, comments, strings = strip_mql(raw)
    symbols = defaultdict(list)
    context = "global"
    depth = 0
    for number, line in enumerate(clean.splitlines(), 1):
        open_type = re.search(r"\b(struct|class|enum)\s+([A-Za-z_]\w*)", line)
        if open_type:
            kind, name = open_type.groups(); context = f"{kind} {name}"
            symbols[name].append(Symbol(name, kind, context, kind, line.strip(), number))
        fn = re.search(r"^\s*([A-Za-z_]\w*(?:::\w+)?)\s+([A-Za-z_]\w*)\s*\(([^;{}]*)\)\s*(?:const\s*)?\{?", line)
        if fn and not line.lstrip().startswith(("if", "for", "while", "switch")):
            typ, name, args = fn.groups(); fkind = "method" if context.startswith(("struct ", "class ")) else "function"
            symbols[name].append(Symbol(name, fkind, context, typ, line.strip(), number))
            for arg in args.split(","):
                am = re.search(r"\b([A-Za-z_]\w*)\s+([A-Za-z_]\w*)\s*(?:=|$)", arg.strip())
                if am:
                    symbols[am.group(2)].append(Symbol(am.group(2), "function_parameter", name, am.group(1), arg.strip(), number))
        decl = re.search(r"^\s*(?:input\s+)?(?:const\s+)?([A-Za-z_]\w*(?:::\w+)?(?:\s*\*)?)\s+([A-Za-z_]\w*)\s*(?:\[[^]]*\])?\s*(?:=|;|,)", line)
        if decl and not fn:
            typ, name = decl.groups()
            if line.lstrip().startswith("input "): kind = "input_parameter"
            elif context.startswith("struct "): kind = "struct_field"
            elif context.startswith("class "): kind = "class_field"
            elif depth == 0: kind = "global_variable"
            else: kind = "local_variable"
            symbols[name].append(Symbol(name, kind, context, typ, line.strip(), number))
        for name, entries in list(symbols.items()):
            count = len(re.findall(rf"\b{re.escape(name)}\b", line))
            if count:
                writes = len(re.findall(rf"\b{re.escape(name)}\b\s*(?:=|\+=|-=|\+\+|--)", line))
                entries[-1].writes += writes; entries[-1].reads += max(0, count - writes - int(entries[-1].line == number))
        depth += line.count("{") - line.count("}")
        if depth <= 0: context = "global"; depth = max(depth, 0)
    return symbols, comments, strings


class PythonIndex(ast.NodeVisitor):
    def __init__(self): self.symbols = defaultdict(list); self.scope = ["module"]
    def add(self, name, kind, typ, node, declaration):
        self.symbols[name].append(Symbol(name, kind, "::".join(self.scope), typ, declaration, getattr(node, "lineno", 0)))
    def visit_FunctionDef(self, node):
        kind = "method" if len(self.scope) > 1 and self.scope[-1].startswith("class ") else "function"
        self.add(node.name, kind, "callable", node, f"def {node.name}(...)")
        self.scope.append(f"function {node.name}")
        for arg in node.args.args: self.add(arg.arg, "function_parameter", ast.unparse(arg.annotation) if arg.annotation else "unannotated", arg, ast.unparse(arg))
        self.generic_visit(node); self.scope.pop()
    visit_AsyncFunctionDef = visit_FunctionDef
    def visit_ClassDef(self, node):
        self.add(node.name, "class", "class", node, f"class {node.name}"); self.scope.append(f"class {node.name}"); self.generic_visit(node); self.scope.pop()
    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            kind = "global_variable" if self.scope == ["module"] else "local_variable"
            if not self.symbols[node.id]: self.add(node.id, kind, "inferred", node, node.id)
            self.symbols[node.id][-1].writes += 1
        elif isinstance(node.ctx, ast.Load) and self.symbols[node.id]: self.symbols[node.id][-1].reads += 1
    def visit_Attribute(self, node):
        name = node.attr
        if not self.symbols[name]: self.add(name, "object_property", "inferred", node, ast.unparse(node))
        if isinstance(node.ctx, ast.Store): self.symbols[name][-1].writes += 1
        elif isinstance(node.ctx, ast.Load): self.symbols[name][-1].reads += 1
        self.generic_visit(node)


def parse_python(path: Path):
    try: tree = ast.parse(path.read_text(errors="ignore"))
    except SyntaxError: return defaultdict(list)
    index = PythonIndex(); index.visit(tree); return index.symbols


def expected_category(type_name: str):
    if type_name.startswith("LOT_"): return "LOT_VALUE"
    if type_name.startswith("MONEY_"): return "MONEY_VALUE"
    if type_name.startswith("PRICE_") or type_name in {"POINTS", "TICKS", "PRICE_DELTA", "DISTANCE_POINTS", "DISTANCE_TICKS"}: return "PRICE_OR_DISTANCE"
    if type_name in {"RATIO", "SHARE", "PERCENT", "MULTIPLIER", "BOOLEAN_POLICY"}: return "POLICY"
    if type_name == "ROLE_ID": return "ROLE"
    if type_name in {"STATE", "PHASE", "OUTCOME", "REASON_CODE", "GATE_RESULT", "EXECUTION_RESULT", "ERROR_CODE", "DIAGNOSTIC_TEXT", "EVENT", "OBSERVATION"}: return "STATE_OR_RESULT"
    if type_name.endswith("_TICKET") or type_name in {"SYMBOL_ID", "MAGIC_ID", "CYCLE_ID", "POSITION_ID", "EVENT_ID", "FINGERPRINT"}: return "IDENTITY"
    return "STRUCTURED_OBJECT"


def semantic_checks(row, rec):
    c = Counter(); typ=row["Type"]; unit=row["Unit"]; cls=row["Projected/Actual"]; tol=row["Tolerance"]; src=row["Authoritative source"]; rounding=row["Rounding"]
    if rec.get("Semantic category") != expected_category(typ): c["INVALID_DEFINITION_TYPE_SEMANTICS"] += 1
    if "Tolerance" in row["Canonical term"] or row["Canonical term"] in {"ComparisonEpsilon", "GeometryTolerance"}: return c
    if typ.startswith("LOT_"):
        c["INVALID_TYPE_UNIT"] += unit != "lot"; c["INVALID_TYPE_TOLERANCE"] += tol != "VolumeToleranceLots"
    if typ.startswith("MONEY_"):
        c["INVALID_TYPE_UNIT"] += unit != "account money"; c["INVALID_TYPE_TOLERANCE"] += tol not in {"MoneyTolerance", "ReserveMismatchTolerance"}
    if typ.startswith("PRICE_"):
        c["INVALID_TYPE_UNIT"] += not (unit == "price" or unit.startswith("price per")); c["INVALID_TYPE_TOLERANCE"] += tol not in {"PriceTolerance", "EXACT PROPERTY SNAPSHOT"}
    if typ in {"DISTANCE_POINTS", "POINTS"}: c["INVALID_TYPE_UNIT"] += unit not in {"point", "points"}; c["INVALID_TYPE_TOLERANCE"] += tol != "PointTolerance"
    if typ in {"DISTANCE_TICKS", "TICKS"}: c["INVALID_TYPE_UNIT"] += unit not in {"tick", "ticks"}; c["INVALID_TYPE_TOLERANCE"] += tol != "PointTolerance"
    if typ in {"RATIO", "SHARE", "PERCENT", "MULTIPLIER"}: c["INVALID_TYPE_UNIT"] += "dimensionless" not in unit; c["INVALID_TYPE_TOLERANCE"] += tol != "RatioTolerance"
    if expected_category(typ) in {"ROLE", "IDENTITY"}: c["INVALID_IDENTITY_TOLERANCE"] += tol not in {"EXACT", "EXACT HASH MATCH"}
    if typ in {"DIRECTION_ENUM", "STATE", "PHASE", "OUTCOME", "REASON_CODE", "GATE_RESULT"}: c["INVALID_ENUM_TOLERANCE"] += tol not in {"EXACT ENUM MATCH", "EXACT STRUCTURE"}
    c["INVALID_TYPE_TOLERANCE"] += c["INVALID_IDENTITY_TOLERANCE"] + c["INVALID_ENUM_TOLERANCE"]
    classes={"LOT_RAW":{"PROJECTED"},"LOT_CALCULATED":{"PROJECTED"},"LOT_NORMALIZED":{"PROJECTED"},"LOT_REQUESTED":{"REQUESTED"},"LOT_FILLED":{"CONFIRMED"},"LOT_POSITION_ACTUAL":{"ACTUAL CURRENT"}}
    if typ in classes: c["INVALID_TYPE_CLASS"] += cls not in classes[typ]
    if typ == "MONEY_REALIZED": c["INVALID_TYPE_CLASS"] += cls != "ACTUAL CONFIRMED"; c["INVALID_TYPE_SOURCE"] += not any(x in src.lower() for x in ("confirmed", "deal", "ledger")) or ("ordercalcprofit" in src.lower() and not any(x in src.lower() for x in ("deal", "ledger")))
    if typ == "LOT_FILLED": c["INVALID_TYPE_SOURCE"] += "deal" not in src.lower()
    if typ == "LOT_POSITION_ACTUAL": c["INVALID_TYPE_SOURCE"] += "position" not in src.lower(); c["INVALID_ACTUAL_ROUNDING"] += rounding != "NO_ADDITIONAL_ROUNDING"
    if typ in {"PRICE_POINT_SIZE", "PRICE_TICK_SIZE"}: c["INVALID_TYPE_CLASS"] += cls != "SYMBOL PROPERTY"; c["INVALID_TYPE_SOURCE"] += "SYMBOL_" not in src
    if rec.get("Lifecycle class") == "PROJECTED_VALUE" and ("LEDGER" in cls or "CONFIRMED" in cls): c["INVALID_LIFECYCLE_CLASS"] += 1
    for field, counter in [("Creation event","MISSING_CREATION_EVENT"),("Stale triggers","MISSING_STALE_TRIGGER"),("Replacement source","MISSING_REPLACEMENT_SOURCE"),("Terminal condition","MISSING_TERMINAL_CONDITION")]: c[counter] += not rec.get(field)
    c["GENERIC_LIFECYCLES"] += any(p in rec.get("Lifecycle","") for p in ("lifecycle/revision mismatch", "соответствующего object"))
    c["DEFINITIONS_WITHOUT_DISTINGUISHING_CLAUSE"] += not rec.get("Отличие от")
    c["FORBIDDEN_PROJECTED_TO_ACTUAL_TRANSITION"] += "становится actual присваиванием" in rec.get("Lifecycle","") and "не становится" not in rec.get("Lifecycle","")
    c["UNRESOLVED_POLICY_APPROVED"] += row.get("Status")=="APPROVED_TERM" and "HSB-DOC-CONFLICT-" in rec.get("Conflict","")
    return c


def mapping_checks(item, rec, mql_indexes, py_indexes, root=ROOT):
    c=Counter()
    status_match=re.match(r"MQL5=`([^`]+)`; Python=`([^`]+)`", rec.get("Mapping status",""))
    for lang,indexes in (("mql5",mql_indexes),("python",py_indexes)):
        status=item.get(f"{lang}_status"); entries=item.get(lang,[])
        c["MAPPING_STATUS_INVALID"] += status not in MAP_STATUS
        if not status_match or status_match.group(1 if lang=="mql5" else 2) != status: c["MAPPING_STATUS_PARITY_ERROR"] += 1
        mapping_text=rec.get("MQL5 mapping" if lang=="mql5" else "Python mapping","")
        c["MISSING_NOT_APPLICABLE_CONFLICT"] += (status=="MISSING" and mapping_text=="NOT_APPLICABLE") or (status=="NOT_APPLICABLE" and mapping_text!="NOT_APPLICABLE")
        c["MAPPING_RECORDS_MISSING"] += status in PROVEN and not entries
        for entry in entries:
            kind=entry.get("identifier_kind",""); c["TOKEN_IDENTIFIER_KINDS"] += kind=="token"; c["MAPPING_STATUS_INVALID"] += kind not in KINDS
            path=root/entry.get("file",""); c["MAPPING_FILES_NOT_FOUND"] += not path.is_file()
            c["MAPPING_WITHOUT_DECLARATION_EVIDENCE"] += not entry.get("declaration_evidence")
            c["MAPPING_WITHOUT_USE_EVIDENCE"] += not (entry.get("read_sites") or entry.get("write_sites"))
            c["IDENTIFIER_ONLY_IN_COMMENT"] += kind=="comment_only"; c["IDENTIFIER_ONLY_IN_STRING"] += kind=="string_literal_only"
            c["UNPROVEN_EXACT_MAPPING"] += status=="EXACT_MATCH" and (kind in NON_CODE_KINDS or not entry.get("declaration_evidence") or not (entry.get("read_sites") or entry.get("write_sites")))
            c["UNPROVEN_SEMANTIC_MAPPING"] += status=="SEMANTIC_MATCH" and (kind in NON_CODE_KINDS or kind=="token" or not entry.get("declaration_evidence") or not (entry.get("read_sites") or entry.get("write_sites")) or not entry.get("semantic_note") or not entry.get("lifecycle_role"))
            c["CACHE_MARKED_AUTHORITATIVE"] += status=="EXACT_MATCH" and entry.get("authoritative") is True and "cache" in (entry.get("scope","")+entry.get("semantic_role","")).lower()
            if path.is_file() and kind not in NON_CODE_KINDS:
                found=indexes.get(path,{}).get(entry.get("identifier",""),[])
                if not found: c["MAPPING_WITHOUT_DECLARATION_EVIDENCE"] += 1
    return c


def normalize(text, name):
    text=re.sub(rf"\b{re.escape(name)}\b","",text,flags=re.I).lower(); return " ".join(re.findall(r"[a-zа-я0-9]+",text))


def validate(rows, recs, mapping, mql_indexes, py_indexes):
    c=Counter(); names=[r["Canonical term"] for r in rows]; c["CANONICAL_TERMS"]=len(rows); c["EXTENDED_RECORDS"]=len(recs)
    c["DUPLICATE_CANONICAL_NAMES"]=len(names)-len(set(names)); map_by={x.get("canonical_term"):x for x in mapping.get("terms",[])}
    c["MAPPING_RECORDS_MISSING"] += len(set(names)^set(map_by))
    normalized_defs=defaultdict(list); normalized_life=defaultdict(list)
    for row in rows:
        name=row["Canonical term"]; rec=recs.get(name,{})
        parity=[("CanonicalName","Canonical term"),("Русское название","Русское название"),("Архитектурный профиль","Profile"),("Размерность","Type"),("Unit","Unit"),("Знак","Sign"),("Projected/Actual class","Projected/Actual"),("Authoritative source","Authoritative source"),("Rounding","Rounding"),("Tolerance","Tolerance"),("Legacy aliases","Aliases"),("Статус определения","Status")]
        c["TABLE_RECORD_MISMATCH"] += sum(rec.get(a,"").strip("`") != row[b] for a,b in parity)
        c.update(semantic_checks(row,rec))
        nd=normalize(rec.get("Краткое определение",""),name); nl=normalize(rec.get("Lifecycle",""),name)
        normalized_defs[nd].append(name); normalized_life[nl].append(name)
        if row["Status"] in UNRESOLVED:
            c["UNRESOLVED_ITEMS_WITHOUT_CONFLICT_ID"] += "HSB-DOC-CONFLICT-" not in rec.get("Conflict","")
            c["UNRESOLVED_ITEMS_WITHOUT_RESOLUTION_STAGE"] += rec.get("Resolution stage","").strip("`") in {"","NOT_APPLICABLE"}
        if name in map_by: c.update(mapping_checks(map_by[name],rec,mql_indexes,py_indexes))
    c["NEAR_DUPLICATE_DEFINITIONS"] = sum(len(v)-1 for k,v in normalized_defs.items() if k and len(v)>1)
    c["NORMALIZED_DUPLICATE_LIFECYCLES"] = sum(len(v)-1 for k,v in normalized_life.items() if k and len(v)>1)
    return c


def fixture():
    row={"Canonical term":"Sample","Русское название":"образец","Profile":"Hybrid","Type":"LOT_CALCULATED","Unit":"lot","Sign":">= 0","Projected/Actual":"PROJECTED","Authoritative source":"typed formula","Rounding":"ROUND_DOWN","Tolerance":"VolumeToleranceLots","Aliases":"—","Status":"APPROVED_TERM"}
    rec={"CanonicalName":"`Sample`","Русское название":"образец","Архитектурный профиль":"Hybrid","Размерность":"`LOT_CALCULATED`","Unit":"`lot`","Знак":">= 0","Projected/Actual class":"`PROJECTED`","Authoritative source":"typed formula","Rounding":"ROUND_DOWN","Tolerance":"`VolumeToleranceLots`","Legacy aliases":"—","Статус определения":"`APPROVED_TERM`","Краткое определение":"Sample — расчётный объём роли до normalization; отличается от RequestedLot.","Semantic category":"LOT_VALUE","Lifecycle class":"PROJECTED_VALUE","Lifecycle":"Sample вычисляется по snapshot; не становится actual присваиванием.","Creation event":"formula snapshot","Stale triggers":"input revision","Replacement source":"recalculation","Terminal condition":"ends at execution","Отличие от":"Sample отличается от FilledLot.","Conflict":"`NOT_APPLICABLE`","Resolution stage":"`NOT_APPLICABLE`","Mapping status":"MQL5=`MISSING`; Python=`MISSING`","MQL5 mapping":"NONE_FOUND","Python mapping":"NONE_FOUND"}
    mapping={"terms":[{"canonical_term":"Sample","mql5":[],"python":[],"mql5_status":"MISSING","python_status":"MISSING"}]}
    return row,rec,mapping


def run_control_tests():
    negative=[]
    def test(counter, mutate):
        row,rec,mapping=fixture(); mutate(row,rec,mapping); got=Counter(); got.update(semantic_checks(row,rec)); got.update(mapping_checks(mapping["terms"][0],rec,{},{})); negative.append((counter,got[counter]>0))
    test("INVALID_DEFINITION_TYPE_SEMANTICS",lambda r,d,m:(r.update(Type="ROLE_ID",Unit="integer/string identity",Tolerance="EXACT"),d.update({"Semantic category":"LOT_VALUE"})))
    test("INVALID_TYPE_TOLERANCE",lambda r,d,m:r.update(Type="MONEY_REALIZED",Unit="account money",Tolerance="VolumeToleranceLots",**{"Projected/Actual":"ACTUAL CONFIRMED","Authoritative source":"confirmed ledger"}))
    test("INVALID_TYPE_SOURCE",lambda r,d,m:r.update(Type="MONEY_REALIZED",Unit="account money",Tolerance="MoneyTolerance",**{"Projected/Actual":"ACTUAL CONFIRMED","Authoritative source":"OrderCalcProfit only"}))
    test("INVALID_ACTUAL_ROUNDING",lambda r,d,m:r.update(Type="LOT_POSITION_ACTUAL",Rounding="ROUND_DOWN",**{"Projected/Actual":"ACTUAL CURRENT","Authoritative source":"current position snapshot"}))
    test("INVALID_ENUM_TOLERANCE",lambda r,d,m:r.update(Type="DIRECTION_ENUM",Unit="BUY/SELL enum",Tolerance="VolumeToleranceLots"))
    test("INVALID_TYPE_UNIT",lambda r,d,m:r.update(Type="RATIO",Unit="account money",Tolerance="RatioTolerance"))
    test("INVALID_IDENTITY_TOLERANCE",lambda r,d,m:r.update(Type="DEAL_TICKET",Unit="integer identity",Tolerance="MoneyTolerance"))
    def mapped(kind="token",status="SEMANTIC_MATCH"):
        return {"canonical_term":"Sample","mql5_status":status,"python_status":"MISSING","python":[],"mql5":[{"file":"Include/Types.mqh","identifier":"x","identifier_kind":kind,"declaration_evidence":"x","read_sites":["x"],"write_sites":[],"semantic_note":"specific note","lifecycle_role":"specific lifecycle","scope":"test","authoritative":False}]}
    test("UNPROVEN_SEMANTIC_MAPPING",lambda r,d,m:(m["terms"].__setitem__(0,mapped()),d.update({"Mapping status":"MQL5=`SEMANTIC_MATCH`; Python=`MISSING`"})))
    test("IDENTIFIER_ONLY_IN_COMMENT",lambda r,d,m:(m["terms"].__setitem__(0,mapped("comment_only","MISSING"))))
    test("IDENTIFIER_ONLY_IN_STRING",lambda r,d,m:(m["terms"].__setitem__(0,mapped("string_literal_only","MISSING"))))
    test("MAPPING_WITHOUT_DECLARATION_EVIDENCE",lambda r,d,m:(m["terms"].__setitem__(0,mapped("local_variable")),m["terms"][0]["mql5"][0].pop("declaration_evidence"),d.update({"Mapping status":"MQL5=`SEMANTIC_MATCH`; Python=`MISSING`"})))
    test("MAPPING_WITHOUT_USE_EVIDENCE",lambda r,d,m:(m["terms"].__setitem__(0,mapped("local_variable")),m["terms"][0]["mql5"][0].update(read_sites=[],write_sites=[]),d.update({"Mapping status":"MQL5=`SEMANTIC_MATCH`; Python=`MISSING`"})))
    test("CACHE_MARKED_AUTHORITATIVE",lambda r,d,m:(m["terms"].__setitem__(0,mapped("struct_field","EXACT_MATCH")),m["terms"][0]["mql5"][0].update(scope="cycle cache",authoritative=True),d.update({"Mapping status":"MQL5=`EXACT_MATCH`; Python=`MISSING`"})))
    test("MISSING_NOT_APPLICABLE_CONFLICT",lambda r,d,m:d.update({"MQL5 mapping":"NOT_APPLICABLE"}))
    test("NORMALIZED_DUPLICATE_LIFECYCLES",lambda r,d,m:None) # isolated normalized-pair counter
    pair=Counter(); pair["NORMALIZED_DUPLICATE_LIFECYCLES"]=int(normalize("A created then stale","A")==normalize("B created then stale","B")); negative[-1]=(negative[-1][0],pair["NORMALIZED_DUPLICATE_LIFECYCLES"]>0)
    test("NEAR_DUPLICATE_DEFINITIONS",lambda r,d,m:None); pair=Counter(); pair["NEAR_DUPLICATE_DEFINITIONS"]=int(normalize("A — projected lot","A")==normalize("B — projected lot","B")); negative[-1]=(negative[-1][0],pair["NEAR_DUPLICATE_DEFINITIONS"]>0)
    test("FORBIDDEN_PROJECTED_TO_ACTUAL_TRANSITION",lambda r,d,m:d.update(Lifecycle="Sample становится actual присваиванием"))
    test("UNRESOLVED_POLICY_APPROVED",lambda r,d,m:d.update(Conflict="`HSB-DOC-CONFLICT-001`"))
    test("MAPPING_STATUS_PARITY_ERROR",lambda r,d,m:d.update({"Mapping status":"MQL5=`PARTIAL_MATCH`; Python=`MISSING`"}))
    test("INVALID_LIFECYCLE_CLASS",lambda r,d,m:(r.update(Type="MONEY_REALIZED",Unit="account money",Tolerance="MoneyTolerance",**{"Projected/Actual":"ACTUAL CONFIRMED","Authoritative source":"confirmed ledger"}),d.update({"Semantic category":"MONEY_VALUE","Lifecycle class":"PROJECTED_VALUE"})))
    positive=[]
    def positive_case(mut):
        r,d,m=fixture(); mut(r,d,m); got=semantic_checks(r,d); got.update(mapping_checks(m["terms"][0],d,{},{})); positive.append(not any(got[x] for x in BLOCKING if x in got))
    positive_case(lambda r,d,m:None)
    positive_case(lambda r,d,m:(m["terms"][0].update(mql5_status="NOT_APPLICABLE"),d.update({"MQL5 mapping":"NOT_APPLICABLE","Mapping status":"MQL5=`NOT_APPLICABLE`; Python=`MISSING`"})))
    positive_case(lambda r,d,m:(r.update(Type="ROLE_ID",Unit="integer/string identity",Tolerance="EXACT"),d.update({"Semantic category":"ROLE","Lifecycle class":"ROLE"})))
    positive_case(lambda r,d,m:(r.update(Type="MONEY_REALIZED",Unit="account money",Tolerance="MoneyTolerance",**{"Projected/Actual":"ACTUAL CONFIRMED","Authoritative source":"confirmed deal ledger"}),d.update({"Semantic category":"MONEY_VALUE","Lifecycle class":"LEDGER"})))
    positive_case(lambda r,d,m:(r.update(Type="LOT_POSITION_ACTUAL",Rounding="NO_ADDITIONAL_ROUNDING",**{"Projected/Actual":"ACTUAL CURRENT","Authoritative source":"current position snapshot"}),d.update({"Lifecycle class":"ACTUAL_POSITION"})))
    positive_case(lambda r,d,m:(r.update(Type="DIRECTION_ENUM",Unit="BUY/SELL enum",Tolerance="EXACT ENUM MATCH"),d.update({"Semantic category":"STRUCTURED_OBJECT"})))
    positive_case(lambda r,d,m:None)
    positive_case(lambda r,d,m:(d.update({"Lifecycle class":"LEDGER"})))
    positive_case(lambda r,d,m:(r.update(Type="PRICE_POINT_SIZE",Unit="price per point",Tolerance="EXACT PROPERTY SNAPSHOT",**{"Projected/Actual":"SYMBOL PROPERTY","Authoritative source":"SYMBOL_POINT"}),d.update({"Semantic category":"PRICE_OR_DISTANCE","Lifecycle class":"SYMBOL_PROPERTY"})))
    positive_case(lambda r,d,m:(r.update(Type="RATIO",Unit="1 (dimensionless)",Tolerance="RatioTolerance"),d.update({"Semantic category":"POLICY","Lifecycle class":"POLICY"})))
    return len(negative),sum(ok for _,ok in negative),len(positive),sum(positive),negative


def main():
    manual=MANUAL.read_text(); glossary=GLOSSARY.read_text(); mt,rows=canonical_table(manual); gt,grows=canonical_table(glossary)
    if mt!=gt or rows!=grows: print("CANONICAL_TABLE_EQUALITY=FAIL"); return 1
    recs=extended_records(glossary); mapping=json.loads(MAPPING.read_text())
    if mapping.get("schema_version")!="3.1.3-second-correction-1": print("MAPPING_SCHEMA=FAIL"); return 1
    mql_paths=[p for p in ROOT.rglob("*") if p.suffix.lower() in {".mq5",".mqh"}]
    py_paths=[p for p in ROOT.rglob("*.py") if p.resolve()!=Path(__file__).resolve()]
    mql_indexes={p:parse_mql(p)[0] for p in mql_paths}; py_indexes={p:parse_python(p) for p in py_paths}
    counters=validate(rows,recs,mapping,mql_indexes,py_indexes)
    neg_total,neg_pass,pos_total,pos_pass,_=run_control_tests()
    counters["NEGATIVE_TESTS_TOTAL"]=neg_total; counters["NEGATIVE_TESTS_PASSED"]=neg_pass; counters["POSITIVE_TESTS_TOTAL"]=pos_total; counters["POSITIVE_TESTS_PASSED"]=pos_pass
    counters["MQL5_FILES_PARSED"]=len(mql_paths); counters["MQL5_DECLARATIONS_FOUND"]=sum(len(v) for idx in mql_indexes.values() for v in idx.values()); counters["MQL5_USE_SITES_FOUND"]=sum(s.reads+s.writes for idx in mql_indexes.values() for vals in idx.values() for s in vals)
    counters["PYTHON_FILES_PARSED"]=len(py_paths); counters["PYTHON_AST_DECLARATIONS_FOUND"]=sum(len(v) for idx in py_indexes.values() for v in idx.values()); counters["PYTHON_USE_SITES_FOUND"]=sum(s.reads+s.writes for idx in py_indexes.values() for vals in idx.values() for s in vals)
    for lang in ("MQL5","PYTHON"):
        key=lang.lower(); statuses=Counter(x[f"{key}_status"] for x in mapping["terms"])
        for status in ("EXACT_MATCH","SEMANTIC_MATCH","PARTIAL_MATCH","AMBIGUOUS","MISSING","NOT_APPLICABLE"): counters[f"{lang}_{status}"]=statuses[status]
    order=["CANONICAL_TERMS","EXTENDED_RECORDS","INVALID_DEFINITION_TYPE_SEMANTICS","INVALID_TYPE_UNIT","INVALID_TYPE_CLASS","INVALID_TYPE_TOLERANCE","INVALID_TYPE_SOURCE","INVALID_ACTUAL_ROUNDING","INVALID_LIFECYCLE_CLASS","TOKEN_IDENTIFIER_KINDS","MAPPING_WITHOUT_DECLARATION_EVIDENCE","MAPPING_WITHOUT_USE_EVIDENCE","IDENTIFIER_ONLY_IN_COMMENT","IDENTIFIER_ONLY_IN_STRING","UNPROVEN_EXACT_MAPPING","UNPROVEN_SEMANTIC_MAPPING","CACHE_MARKED_AUTHORITATIVE","MAPPING_STATUS_PARITY_ERROR","MISSING_NOT_APPLICABLE_CONFLICT","NORMALIZED_DUPLICATE_LIFECYCLES","GENERIC_LIFECYCLES","MISSING_CREATION_EVENT","MISSING_STALE_TRIGGER","MISSING_REPLACEMENT_SOURCE","MISSING_TERMINAL_CONDITION","NEAR_DUPLICATE_DEFINITIONS","DEFINITIONS_WITHOUT_DISTINGUISHING_CLAUSE","FORBIDDEN_PROJECTED_TO_ACTUAL_TRANSITION","UNRESOLVED_POLICY_APPROVED","UNRESOLVED_ITEMS_WITHOUT_CONFLICT_ID","UNRESOLVED_ITEMS_WITHOUT_RESOLUTION_STAGE","MQL5_FILES_PARSED","MQL5_DECLARATIONS_FOUND","MQL5_USE_SITES_FOUND","PYTHON_FILES_PARSED","PYTHON_AST_DECLARATIONS_FOUND","PYTHON_USE_SITES_FOUND"]
    order += [f"{lang}_{status}" for lang in ("MQL5","PYTHON") for status in ("EXACT_MATCH","SEMANTIC_MATCH","PARTIAL_MATCH","AMBIGUOUS","MISSING","NOT_APPLICABLE")]
    order += ["NEGATIVE_TESTS_TOTAL","NEGATIVE_TESTS_PASSED","POSITIVE_TESTS_TOTAL","POSITIVE_TESTS_PASSED"]
    for key in order: print(f"{key}={counters[key]}")
    failed=[x for x in BLOCKING if counters[x]]
    ok=not failed and neg_pass==neg_total and pos_pass==pos_total and counters["CANONICAL_TERMS"]>=230 and counters["EXTENDED_RECORDS"]==counters["CANONICAL_TERMS"]
    if failed: print("BLOCKING_COUNTERS="+",".join(failed))
    print("STAGE_3_1_3_SECOND_CORRECTION_VALIDATION="+("PASS" if ok else "FAIL")); return 0 if ok else 1

if __name__ == "__main__": raise SystemExit(main())
