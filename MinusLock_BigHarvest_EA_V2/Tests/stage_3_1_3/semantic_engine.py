"""Validator-owned candidate, use, dataflow, lineage and scope discovery.

The module has no JSON dependency.  Mapping documents may serialise its result,
but cannot influence discovery, evidence calculation, ranking, or ambiguity.
"""
from __future__ import annotations

import ast
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

from stage_3_1_3.semantic_inference import UNIT_ANCHORS, UNIT_WORDS
from stage_3_1_3.source_evidence import Symbol, index_mql, index_python, sanitise
from stage_3_1_3.seventh_engine import (
    DeclarationIdentity, build_scoped_mql_use_graphs, build_scoped_python_use_graphs,
    build_resolved_mql_dataflow, build_resolved_python_dataflow,
    compute_candidate_scope_proof, propagate_units,
    entity_nature,
)

VIABLE = {"EXACT_MATCH", "SEMANTIC_MATCH", "PARTIAL_MATCH"}
SCOPE_RELATIONS = {"EXACT", "BROADER", "NARROWER", "TEST_ANALOGUE", "OFFLINE_ANALOGUE", "INCOMPATIBLE"}
_USE_CACHE: dict[tuple[str, str, str, int, str], UseGraph] = {}
_ALL_USE_CACHE: dict[tuple[str,str],dict[str,UseGraph]] = {}


@dataclass
class UseGraph:
    identifier: str
    all_read_sites: list[str] = field(default_factory=list)
    all_write_sites: list[str] = field(default_factory=list)
    call_sites: list[str] = field(default_factory=list)
    comparison_sites: list[str] = field(default_factory=list)
    assignment_sources: list[str] = field(default_factory=list)
    assignment_sinks: list[str] = field(default_factory=list)
    return_sites: list[str] = field(default_factory=list)
    contradictory_sites: list[str] = field(default_factory=list)


@dataclass
class DataflowEdge:
    source: str
    sink: str
    operation: str
    site: str


@dataclass
class Candidate:
    identifier: str
    file: str
    line: int
    kind: str
    score: int
    status: str
    entity_nature: str
    unit: str
    scope: str
    scope_relation: str
    source_lineage: list[str]
    authoritative: bool
    temporal: str
    lifecycle: str
    reads: int
    writes: int
    use_graph: dict
    dataflow_edges: list[dict]
    proof: dict
    declaration_key: str = ""
    unit_confidence: str = "UNKNOWN"
    storage_role: str = "DERIVED"
    authority_class: str = "NON_AUTHORITATIVE_DERIVED"

    @property
    def key(self) -> str:
        return f"{self.file}:{self.line}:{self.identifier}"


def _words(value: str) -> set[str]:
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value)
    words = set(re.findall(r"[a-z0-9]+", value.lower()))
    stems = set()
    for word in words:
        stems.add(word)
        for suffix in ("s", "ed", "ing", "al", "actual", "projected", "requested", "filled"):
            if word.endswith(suffix) and len(word) > len(suffix) + 2:
                stems.add(word[:-len(suffix)])
    return stems - {"the", "value", "data", "current"}


def _line_kind(line: str, identifier: str) -> tuple[bool, bool]:
    token = rf"(?:\b\w+\s*\.\s*)?\b{re.escape(identifier)}\b(?:\s*\[[^]]+\])?"
    write = bool(re.search(token + r"\s*(?:\+\+|--|[+\-*/]?=(?!=))", line) or re.search(r"(?:\+\+|--)\s*" + token, line))
    declaration = bool(re.match(rf"\s*(?:input\s+|static\s+|const\s+)?[\w:<>]+\s+[&*]?\s*{re.escape(identifier)}\b", line))
    occurrences = len(re.findall(rf"\b{re.escape(identifier)}\b", line))
    read = occurrences > int(write) and not (declaration and occurrences == 1 and "=" not in line)
    if write and "=" in line:
        rhs = line.split("=", 1)[1]
        read = read or bool(re.search(rf"\b{re.escape(identifier)}\b", rhs))
    return read, write


def discover_mql_use(root: Path, symbol: Symbol) -> UseGraph:
    graph = UseGraph(symbol.identifier)
    for path in sorted([*root.rglob("*.mq5"), *root.rglob("*.mqh")]):
        clean = sanitise(path.read_text(errors="ignore"))[0]
        rel = str(path.relative_to(root))
        for number, line in enumerate(clean.splitlines(), 1):
            if not re.search(rf"\b{re.escape(symbol.identifier)}\b", line):
                continue
            if rel == symbol.file and number == symbol.line:
                # Initialisers are writes even on the declaration line.
                if "=" not in line:
                    continue
            site = f"{rel}:{number}"
            read, write = _line_kind(line, symbol.identifier)
            if read: graph.all_read_sites.append(site)
            if write: graph.all_write_sites.append(site)
            if re.search(rf"\([^)]*\b{re.escape(symbol.identifier)}\b", line): graph.call_sites.append(site)
            if re.search(rf"\b{re.escape(symbol.identifier)}\b[^;]*(?:==|!=|<=|>=|<|>)", line): graph.comparison_sites.append(site)
            if re.search(rf"\breturn\b[^;]*\b{re.escape(symbol.identifier)}\b", line): graph.return_sites.append(site)
            assignment = re.search(r"(?P<lhs>[\w.\[\]]+)\s*=\s*(?P<rhs>.+?);", line)
            if assignment:
                lhs, rhs = assignment.group("lhs"), assignment.group("rhs")
                if re.search(rf"\b{re.escape(symbol.identifier)}\b", lhs): graph.assignment_sources.append(f"{site}:{rhs.strip()}")
                if re.search(rf"\b{re.escape(symbol.identifier)}\b", rhs): graph.assignment_sinks.append(f"{site}:{lhs}")
            upper = line.upper()
            inferred = {unit for anchor, unit in UNIT_ANCHORS.items() if anchor in upper}
            if len(inferred) > 1: graph.contradictory_sites.append(site)
    for key in asdict(graph):
        if isinstance(getattr(graph, key), list): setattr(graph, key, sorted(set(getattr(graph, key))))
    return graph


class _PythonUses(ast.NodeVisitor):
    def __init__(self, rel: str, identifier: str): self.rel, self.identifier, self.graph = rel, identifier, UseGraph(identifier); self.parents=[]
    def visit(self, node): self.parents.append(node); super().visit(node); self.parents.pop()
    def _record(self, node, ctx):
        site=f"{self.rel}:{node.lineno}"; parent=self.parents[-2] if len(self.parents)>1 else None
        (self.graph.all_read_sites if isinstance(ctx, ast.Load) else self.graph.all_write_sites).append(site)
        if isinstance(parent,(ast.Call,ast.keyword)): self.graph.call_sites.append(site)
        if isinstance(parent,ast.Compare): self.graph.comparison_sites.append(site)
        if isinstance(parent,ast.Return): self.graph.return_sites.append(site)
    def visit_Name(self,node):
        if node.id==self.identifier:self._record(node,node.ctx)
        self.generic_visit(node)
    def visit_Attribute(self,node):
        if node.attr==self.identifier:self._record(node,node.ctx)
        self.generic_visit(node)


def discover_python_use(root: Path, symbol: Symbol) -> UseGraph:
    graph=UseGraph(symbol.identifier)
    for path in sorted(root.rglob("*.py")):
        try: tree=ast.parse(path.read_text(errors="ignore"))
        except SyntaxError: continue
        visitor=_PythonUses(str(path.relative_to(root)),symbol.identifier);visitor.visit(tree)
        for key,value in asdict(visitor.graph).items():
            if isinstance(value,list):getattr(graph,key).extend(value)
    for key,value in asdict(graph).items():
        if isinstance(value,list):setattr(graph,key,sorted(set(getattr(graph,key))))
    return graph


def build_all_use_graphs(root: Path, symbols: list[Symbol], language: str) -> dict[str,UseGraph]:
    """Scan every source once and build complete graphs for every parsed name."""
    cache_key=(str(root.resolve()),language)
    if cache_key in _ALL_USE_CACHE:return _ALL_USE_CACHE[cache_key]
    names={s.identifier for s in symbols}; graphs={name:UseGraph(name) for name in names}
    if language=="mql5":
        for path in sorted([*root.rglob("*.mq5"),*root.rglob("*.mqh")]):
            rel=str(path.relative_to(root));clean=sanitise(path.read_text(errors="ignore"))[0]
            for number,line in enumerate(clean.splitlines(),1):
                for name in set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*",line))&names:
                    graph=graphs[name];site=f"{rel}:{number}";read,write=_line_kind(line,name)
                    if read:graph.all_read_sites.append(site)
                    if write:graph.all_write_sites.append(site)
                    if re.search(rf"\([^)]*\b{re.escape(name)}\b",line):graph.call_sites.append(site)
                    if re.search(rf"\b{re.escape(name)}\b[^;]*(?:==|!=|<=|>=|<|>)",line):graph.comparison_sites.append(site)
                    if re.search(rf"\breturn\b[^;]*\b{re.escape(name)}\b",line):graph.return_sites.append(site)
                    assignment=re.search(r"(?P<lhs>[\w.\[\]]+)\s*=\s*(?P<rhs>.+?);",line)
                    if assignment:
                        lhs,rhs=assignment.group("lhs"),assignment.group("rhs")
                        if re.search(rf"\b{re.escape(name)}\b",lhs):graph.assignment_sources.append(f"{site}:{rhs.strip()}")
                        if re.search(rf"\b{re.escape(name)}\b",rhs):graph.assignment_sinks.append(f"{site}:{lhs}")
    else:
        for path in sorted(root.rglob("*.py")):
            try:tree=ast.parse(path.read_text(errors="ignore"))
            except SyntaxError:continue
            rel=str(path.relative_to(root))
            for node in ast.walk(tree):
                name=node.id if isinstance(node,ast.Name) else node.attr if isinstance(node,ast.Attribute) else None
                if name not in graphs:continue
                site=f"{rel}:{node.lineno}";target=graphs[name]
                (target.all_read_sites if isinstance(node.ctx,ast.Load) else target.all_write_sites).append(site)
    for graph in graphs.values():
        for key,value in asdict(graph).items():
            if isinstance(value,list):setattr(graph,key,sorted(set(value)))
    _ALL_USE_CACHE[cache_key]=graphs;return graphs


def _unit(symbol: Symbol, graph: UseGraph, root: Path, propagated=None,
          declaration_key: str = "") -> tuple[str, bool, str]:
    if symbol.kind in {"struct","class"}: return "OBJECT", False, "POLICY_ANCHORED"
    if propagated and declaration_key in propagated.units:
        confidence = "API_ANCHORED" if propagated.rules.get(declaration_key)=="API_ANCHORED" else "PROPAGATED"
        return propagated.units[declaration_key], declaration_key in propagated.conflicts, confidence
    source=symbol.declaration_text+"\n"+"\n".join(graph.assignment_sources)
    anchored={unit for anchor,unit in UNIT_ANCHORS.items() if anchor in source.upper()}
    name=symbol.identifier.lower().replace("_",""); named={unit for unit,words in UNIT_WORDS.items() if any(w.replace("_","") in name for w in words)}
    if symbol.kind=="input_parameter" and any(x in name for x in ("ratio","share","percent","factor")):
        return "RATIO", False, "POLICY_ANCHORED"
    units=anchored or named
    unit=next(iter(units)) if len(units)==1 else "UNKNOWN" if not units else "CONTRADICTORY"
    confidence="NAME_FALLBACK" if len(units)==1 else unit
    return unit, len(units)>1 or bool(graph.contradictory_sites), confidence


def _lineage(symbol: Symbol, graph: UseGraph) -> list[str]:
    text=(symbol.declaration_text+" "+" ".join(graph.assignment_sources)).upper(); path=symbol.file.replace("\\","/")
    if path.startswith("Tests/"): origin="TEST_ORACLE"
    elif path.startswith("Tools/"): origin="OFFLINE_MODEL"
    elif symbol.kind=="input_parameter" or re.search(r"\bINPUT\b",text): origin="CONFIG_INPUT"
    elif "POSITIONGET" in text or "POSITION_" in text: origin="TERMINAL_POSITION"
    elif "HISTORYDEAL" in text or "DEAL_" in text: origin="DEAL_HISTORY"
    elif "ORDER_" in text or "MQLTRADEREQUEST" in text: origin="ORDER_REQUEST"
    elif "SYMBOLINFO" in text or "SYMBOL_" in text: origin="SYMBOL_PROPERTY"
    else: origin="DERIVED"
    stored=symbol.kind in {"struct_field","class_field","global_variable","static_variable"}
    return [origin,"CACHE"] if stored and origin not in {"CONFIG_INPUT","TEST_ORACLE","OFFLINE_MODEL"} else [origin]


def _resolved_lineage(symbol: Symbol, identity: DeclarationIdentity, dataflow) -> tuple[list[str], str, str]:
    origins=set(); pending=[str(identity)]; seen=set()
    while pending:
        key=pending.pop()
        if key in seen: continue
        seen.add(key)
        for edge in dataflow.edges if dataflow else ():
            if edge.sink.key != key: continue
            if edge.source.kind=="API_RESULT":
                api=edge.source.key.removeprefix("API:")
                if api.startswith("POSITION_"): origins.add("TERMINAL_POSITION")
                elif api.startswith("DEAL_"): origins.add("DEAL_HISTORY")
                elif api.startswith("SYMBOL_"): origins.add("SYMBOL_PROPERTY")
                else: origins.add("API_RESULT")
            else: pending.append(edge.source.key)
    if not origins: origins.add(_lineage(symbol,UseGraph(symbol.identifier))[0])
    stored=symbol.kind in {"struct_field","class_field","global_variable","static_variable"}
    role="CACHE" if stored else "LEDGER" if "DEAL_HISTORY" in origins else "DERIVED"
    if role=="CACHE": authority="NON_AUTHORITATIVE_MIRROR"
    elif role=="LEDGER": authority="AUTHORITATIVE_HISTORICAL"
    elif origins & {"TERMINAL_POSITION","SYMBOL_PROPERTY"}: authority="AUTHORITATIVE_TERMINAL"
    else: authority="NON_AUTHORITATIVE_DERIVED"
    return sorted(origins)+([role] if role=="CACHE" else []),role,authority


def _scope(symbol: Symbol, graph: UseGraph, root: Path) -> str:
    path=symbol.file.replace("\\","/")
    if path.startswith("Tests/"):return "TEST_ONLY"
    if path.startswith("Tools/"):return "OFFLINE_TOOL"
    text=(symbol.declaration_text+" "+" ".join(graph.assignment_sources+graph.assignment_sinks)).lower()
    has_symbol=bool(re.search(r"\b_symbol\b|position_symbol|deal_symbol|symbolinfo|symbol\s*(?:==|!=)",text))
    has_magic=bool(re.search(r"position_magic|deal_magic|order_magic|magicnumber|magic\s*(?:==|!=)",text))
    if has_symbol and has_magic:return "PER_SYMBOL_MAGIC"
    if has_symbol:return "PER_SYMBOL"
    if has_magic:return "PER_MAGIC"
    words=_words(symbol.identifier+" "+symbol.scope)
    for token,value in (("position","PER_POSITION"),("deal","PER_DEAL"),("order","PER_ORDER"),("request","PER_REQUEST"),("plan","PER_PLAN"),("cycle","PER_CYCLE")):
        if token in words:return value
    if symbol.kind in {"local_variable","function_parameter","output_reference_parameter"}:return "PER_FUNCTION_LOCAL"
    return "GLOBAL_RUNTIME"


def scope_relation(expected: str, actual: str) -> str:
    if expected==actual:return "EXACT"
    if actual=="TEST_ONLY":return "TEST_ANALOGUE"
    if actual=="OFFLINE_TOOL":return "OFFLINE_ANALOGUE"
    broad={"GLOBAL_RUNTIME","PER_SYMBOL","PER_MAGIC","PER_CYCLE","PER_FUNCTION_LOCAL"}
    if expected=="PER_SYMBOL_MAGIC" and actual in {"PER_SYMBOL","PER_MAGIC"}:return "BROADER"
    if actual in broad:return "BROADER"
    if expected in broad:return "NARROWER"
    return "INCOMPATIBLE"


def _temporal_lifecycle(lineage: list[str], symbol: Symbol) -> tuple[str,str]:
    text=symbol.identifier.lower(); origin=lineage[0]
    if origin=="CONFIG_INPUT":return "POLICY","POLICY"
    if origin=="DEAL_HISTORY":return "ACTUAL_HISTORICAL","DEAL" if "deal" in text else "LEDGER"
    if origin=="TERMINAL_POSITION":return "ACTUAL_CURRENT","ACTUAL_POSITION"
    if origin in {"ORDER_REQUEST","ORDER_RESULT"}:return ("REQUESTED","REQUESTED") if "request" in text else ("CONFIRMED","EXECUTION_RESULT")
    if "snapshot" in text:return "PROJECTED","SNAPSHOT"
    if "plan" in text:return "PROJECTED","PLAN"
    if "state" in text or "phase" in text:return "PROJECTED","STATE"
    return "PROJECTED","PROJECTED_VALUE"


def _scoped_graph(identity: DeclarationIdentity, scoped) -> UseGraph:
    graph = scoped.get(identity)
    return UseGraph(identity.identifier,
                    all_read_sites=list(graph.reads) if graph else [],
                    all_write_sites=list(graph.writes) if graph else [])


def evaluate(root: Path, symbol: Symbol, expected: dict, language: str,
             use_graphs: dict[DeclarationIdentity, object] | None=None,
             resolved_dataflow=None, propagated_units=None) -> Candidate:
    cache_key=(str(root.resolve()),language,symbol.file,symbol.line,symbol.identifier)
    identity = DeclarationIdentity.from_symbol(language, symbol)
    graph=_scoped_graph(identity, use_graphs) if use_graphs is not None else _USE_CACHE.get(cache_key)
    if graph is None:
        graph=discover_mql_use(root,symbol) if language=="mql5" else discover_python_use(root,symbol)
        _USE_CACHE[cache_key]=graph
    unit,contradiction,unit_confidence=_unit(symbol,graph,root,propagated_units,str(identity))
    lineage,storage_role,authority_class=_resolved_lineage(symbol,identity,resolved_dataflow)
    if language=="mql5" and expected["scope"] in {"PER_SYMBOL_MAGIC","PER_SYMBOL_MAGIC_CYCLE"}:
        identity=DeclarationIdentity.from_symbol(language,symbol);scope=compute_candidate_scope_proof(root,identity).scope
    else:scope=_scope(symbol,graph,root)
    relation=scope_relation(expected["scope"],scope)
    temporal,lifecycle=_temporal_lifecycle(lineage,symbol); authoritative=authority_class.startswith("AUTHORITATIVE_")
    lexical=len(_words(expected["canonical"]+" "+" ".join(expected.get("aliases",[])))&_words(symbol.identifier))*8
    expected_nature=expected.get("entity_nature","VALUE");actual_nature=entity_nature(symbol,unit)
    nature_ok=actual_nature==expected_nature or expected_nature=="VALUE" and actual_nature not in {"FUNCTION","STATE","ENUM","STRUCT","PLAN"}
    proof={"entity_nature_match":nature_ok,"unit_match":unit==expected["unit"],"scope_relation":relation,"source_lineage_match":lineage[0] in expected["lineages"],"authority_match":authoritative==expected["authoritative"],"temporal_match":temporal==expected["temporal"],"lifecycle_match":lifecycle==expected["lifecycle"],"complete_use_graph":True,"no_contradictory_use":not contradiction}
    score=min(100,lexical+15*proof["unit_match"]+10*(relation=="EXACT")+10*proof["source_lineage_match"]+10*proof["authority_match"]+10*proof["temporal_match"]+10*proof["lifecycle_match"]+5*proof["no_contradictory_use"])
    essential=proof["entity_nature_match"] and proof["unit_match"] and relation!="INCOMPATIBLE"
    strict=all(v is True or k=="scope_relation" for k,v in proof.items()) and relation=="EXACT"
    if strict and unit_confidence not in {"NAME_FALLBACK","UNKNOWN","CONTRADICTORY"}:status="EXACT_MATCH" if lexical else "SEMANTIC_MATCH"
    elif unit_confidence in {"UNKNOWN","CONTRADICTORY"}:status="MISSING"
    elif essential:status="PARTIAL_MATCH" if relation in {"BROADER","NARROWER","TEST_ANALOGUE","OFFLINE_ANALOGUE"} or "CACHE" in lineage else "SEMANTIC_MATCH"
    else:status="MISSING"
    edges=[]
    if resolved_dataflow is not None:
        declaration_key=str(identity)
        for edge in resolved_dataflow.edges:
            if edge.source.key == declaration_key or edge.sink.key == declaration_key:
                edges.append({"source":edge.source.key,"sink":edge.sink.key,
                              "operation":edge.operation,"site":edge.site,
                              "evidence_text":edge.expression,
                              "operator":edge.operator,
                              "operand_nodes":list(edge.operand_nodes)})
    return Candidate(symbol.identifier,symbol.file,symbol.line,symbol.kind,score,status,actual_nature,unit,scope,relation,lineage,authoritative,temporal,lifecycle,len(graph.all_read_sites),len(graph.all_write_sites),asdict(graph),edges,proof,str(identity),unit_confidence,storage_role,authority_class)


def evaluate_canonical_mapping(root: Path, expected: dict, language: str, symbols: list[Symbol] | None=None) -> dict:
    symbols=symbols if symbols is not None else (index_mql(root) if language=="mql5" else index_python(root))
    expected_words=_words(expected["canonical"]+" "+" ".join(expected.get("aliases",[])))
    # Semantic/API candidates are retained even without a lexical match.
    pool=[]
    for symbol in symbols:
        lexical=bool(expected_words&_words(symbol.identifier))
        declaration=symbol.declaration_text.upper()
        semantic=any(UNIT_ANCHORS.get(anchor)==expected["unit"] and anchor in declaration for anchor in UNIT_ANCHORS)
        if lexical or semantic:pool.append(symbol)
    # The production path is keyed by the full declaration identity.  The
    # name-keyed builder remains only for compatibility with historical audits.
    use_graphs=(build_scoped_mql_use_graphs(root) if language=="mql5"
                else build_scoped_python_use_graphs(root))
    resolved_dataflow=(build_resolved_mql_dataflow(root) if language=="mql5"
                       else build_resolved_python_dataflow(root))
    seeds={str(identity):"RATIO" for identity in use_graphs
           if identity.identifier in {"BigRatio","SmallRatio","ReserveShare","CloseFarShare"}}
    propagated=propagate_units(resolved_dataflow,seeds)
    evaluated=[evaluate(root,s,expected,language,use_graphs,resolved_dataflow,propagated) for s in pool]
    evaluated.sort(key=lambda c:(c.score,c.status!="MISSING",-c.line,c.file,c.identifier),reverse=True)
    viable=[c for c in evaluated if c.status in VIABLE]
    winner=viable[0] if viable else None;runner=viable[1] if len(viable)>1 else None
    ambiguous=bool(winner and runner and winner.score-runner.score<=5 and winner.unit==runner.unit and winner.source_lineage==runner.source_lineage)
    status="AMBIGUOUS" if ambiguous else ("SEMANTIC_MATCH" if winner and runner and winner.status=="EXACT_MATCH" else winner.status if winner else "MISSING")
    return {"canonical_term":expected["canonical"],"generated_candidates":[s.identifier for s in pool],"discovered_candidates":[c.key for c in evaluated],"evaluated_candidates":[asdict(c)|{"key":c.key} for c in evaluated],"winner":(asdict(winner)|{"key":winner.key}) if winner else None,"runner_up":(asdict(runner)|{"key":runner.key}) if runner else None,"ambiguous":ambiguous,"computed_status":status}
