"""Declaration-scoped semantic engine for the Stage 3.1.3 seventh correction.

Unlike the legacy discovery index, every fact in this module is keyed by the
concrete declaration, never by an identifier spelling alone.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import ast
import re

from stage_3_1_3.source_evidence import Symbol, index_mql, index_python, sanitise

ENTITY_RELATIONS = {"EXACT", "COMPATIBLE", "PARTIAL", "INCOMPATIBLE"}


@dataclass(frozen=True, order=True)
class DeclarationIdentity:
    language: str
    file: str
    scope_id: str
    declaration_line: int
    declaration_column: int
    identifier: str
    parent_symbol: str
    declaration_kind: str

    @classmethod
    def from_symbol(cls, language: str, symbol: Symbol) -> "DeclarationIdentity":
        return cls(language, symbol.file, symbol.scope, symbol.line, symbol.column,
                   symbol.identifier, symbol.parent_symbol, symbol.kind)


@dataclass
class ScopedUseGraph:
    declaration: DeclarationIdentity
    reads: list[str] = field(default_factory=list)
    writes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class DataflowNode:
    key: str
    kind: str
    declaration: DeclarationIdentity | None = None


@dataclass(frozen=True)
class ResolvedDataflowEdge:
    source: DataflowNode
    sink: DataflowNode
    operation: str
    site: str
    expression: str = ""


@dataclass
class ResolvedDataflowGraph:
    nodes: dict[str, DataflowNode] = field(default_factory=dict)
    edges: list[ResolvedDataflowEdge] = field(default_factory=list)
    unresolved_sources: list[str] = field(default_factory=list)
    unresolved_sinks: list[str] = field(default_factory=list)


@dataclass
class UnitPropagationResult:
    units: dict[str, str]
    rules: dict[str, str]
    illegal_operations: list[str]
    conflicts: list[str]
    unresolved: list[str]


UNIT_API = {
    "POSITION_VOLUME": "LOT", "DEAL_VOLUME": "LOT", "DEAL_PROFIT": "MONEY",
    "DEAL_COMMISSION": "MONEY", "SYMBOL_BID": "PRICE", "SYMBOL_ASK": "PRICE",
    "SYMBOL_POINT": "POINT_SIZE", "SYMBOL_TRADE_TICK_SIZE": "POINT_SIZE",
}
UNIT_RULES = {
    ("LOT", "*", "RATIO"): ("LOT", "LOT_TIMES_RATIO"),
    ("MONEY", "*", "RATIO"): ("MONEY", "MONEY_TIMES_RATIO"),
    ("LOT", "+", "LOT"): ("LOT", "LOT_PLUS_LOT"),
    ("MONEY", "+", "MONEY"): ("MONEY", "MONEY_PLUS_MONEY"),
    ("PRICE", "-", "PRICE"): ("PRICE_DELTA", "PRICE_MINUS_PRICE"),
    ("PRICE_DELTA", "/", "POINT_SIZE"): ("POINTS", "DELTA_PER_POINT"),
    ("POINTS", "*", "POINT_SIZE"): ("PRICE_DELTA", "POINTS_TIMES_POINT"),
    ("MONEY", "/", "LOT"): ("MONEY_PER_LOT", "MONEY_PER_LOT"),
}


def propagate_units(graph: ResolvedDataflowGraph, seeds: dict[str, str] | None = None) -> UnitPropagationResult:
    units = dict(seeds or {}); rules: dict[str, str] = {}; illegal: list[str] = []; conflicts: list[str] = []
    for key in graph.nodes:
        if key.startswith("API:") and key[4:] in UNIT_API: units[key] = UNIT_API[key[4:]]
    changed = True
    while changed:
        changed = False
        for edge in graph.edges:
            source_unit = units.get(edge.source.key); sink_unit = units.get(edge.sink.key)
            if edge.operation in {"ASSIGN", "COPY"} and source_unit:
                if sink_unit and sink_unit != source_unit: conflicts.append(edge.site)
                elif not sink_unit: units[edge.sink.key] = source_unit; rules[edge.site] = "COPY"; changed = True
            elif edge.operation == "ARITHMETIC":
                operator = next((op for op in ("+", "-", "*", "/") if op in edge.expression), "")
                operands = re.findall(r"\b[A-Za-z_]\w*\b", edge.expression)
                operand_units = []
                for name in operands:
                    matches = [key for key, node in graph.nodes.items() if node.declaration and node.declaration.identifier == name]
                    if matches and units.get(matches[-1]): operand_units.append(units[matches[-1]])
                if len(operand_units) >= 2:
                    rule = UNIT_RULES.get((operand_units[0], operator, operand_units[1]))
                    if not rule: illegal.append(edge.site)
                    elif not sink_unit: units[edge.sink.key] = rule[0]; rules[edge.site] = rule[1]; changed = True
    unresolved = sorted({edge.sink.key for edge in graph.edges if edge.sink.key not in units})
    return UnitPropagationResult(units, rules, sorted(set(illegal)), sorted(set(conflicts)), unresolved)


@dataclass(frozen=True)
class ScopeProof:
    scope: str
    symbol_evidence: tuple[str, ...]
    magic_evidence: tuple[str, ...]
    cycle_evidence: tuple[str, ...]


def compute_scope_proof(root: Path) -> ScopeProof:
    """Prove isolation from filters, including one resolved helper call hop."""
    symbol: list[str] = []; magic: list[str] = []; cycle: list[str] = []
    function_evidence: dict[str, set[str]] = {}
    calls: list[tuple[str, str]] = []
    for path in sorted([*root.rglob("*.mq5"), *root.rglob("*.mqh")]):
        rel = str(path.relative_to(root)); clean = sanitise(path.read_text(errors="ignore"))[0]
        scopes = _scope_lines(clean)
        for number, line in enumerate(clean.splitlines(), 1):
            site = f"{rel}:{number}"; scope = scopes[number]; evidence = function_evidence.setdefault(scope, set())
            if re.search(r"(?:POSITION|DEAL|ORDER)_SYMBOL|\b_symbol\b", line, re.I): evidence.add("symbol"); symbol.append(site)
            if re.search(r"(?:POSITION|DEAL|ORDER)_MAGIC|\bmagic(?:number)?\b", line, re.I): evidence.add("magic"); magic.append(site)
            if re.search(r"\bcycle(?:id)?\b", line, re.I): evidence.add("cycle"); cycle.append(site)
            for called in re.findall(r"\b([A-Za-z_]\w*)\s*\(", line):
                if called not in {"if", "for", "while", "switch"}: calls.append((scope, f"function {called}"))
    changed = True
    while changed:
        changed = False
        for caller, callee in calls:
            before = len(function_evidence.setdefault(caller, set()))
            function_evidence[caller].update(function_evidence.get(callee, set()))
            changed |= len(function_evidence[caller]) != before
    combined = set().union(*function_evidence.values()) if function_evidence else set()
    if {"symbol", "magic", "cycle"} <= combined: scope = "PER_SYMBOL_MAGIC_CYCLE"
    elif {"symbol", "magic"} <= combined: scope = "PER_SYMBOL_MAGIC"
    elif "symbol" in combined: scope = "PER_SYMBOL"
    elif "magic" in combined: scope = "PER_MAGIC"
    elif "cycle" in combined: scope = "PER_CYCLE"
    else: scope = "GLOBAL_RUNTIME"
    return ScopeProof(scope, tuple(sorted(set(symbol))), tuple(sorted(set(magic))), tuple(sorted(set(cycle))))


SCOPE_SETS = {
    "GLOBAL_RUNTIME": frozenset(), "PER_SYMBOL": frozenset({"symbol"}),
    "PER_MAGIC": frozenset({"magic"}), "PER_SYMBOL_MAGIC": frozenset({"symbol", "magic"}),
    "PER_CYCLE": frozenset({"cycle"}), "PER_SYMBOL_MAGIC_CYCLE": frozenset({"symbol", "magic", "cycle"}),
}


def strict_scope_relation(expected: str, actual: str) -> str:
    if expected == actual: return "EXACT"
    if actual == "TEST_ONLY": return "TEST_ANALOGUE"
    if actual == "OFFLINE_TOOL": return "OFFLINE_ANALOGUE"
    if expected not in SCOPE_SETS or actual not in SCOPE_SETS: return "UNKNOWN"
    wanted, found = SCOPE_SETS[expected], SCOPE_SETS[actual]
    if wanted < found: return "PROVEN_SUPERSET"
    if found < wanted: return "PROVEN_SUBSET"
    return "INCOMPATIBLE"


def evaluate_seventh_counters(*, entity_relation="EXACT", expected_entity="VALUE", actual_entity="VALUE",
                              dataflow: ResolvedDataflowGraph | None = None,
                              units: UnitPropagationResult | None = None,
                              expected_scope="GLOBAL_RUNTIME", actual_scope="GLOBAL_RUNTIME") -> dict[str, int]:
    counters = {name: 0 for name in (
        "ENTITY_NATURE_UNKNOWN", "ENTITY_NATURE_INCOMPATIBLE", "ENTITY_NATURE_FALSE_EXACT",
        "FUNCTION_PROMOTED_TO_VALUE", "STATE_PROMOTED_TO_OBJECT", "IDENTITY_ROLE_MISMATCH",
        "UNRESOLVED_DATAFLOW_SOURCE", "UNRESOLVED_DATAFLOW_SINK", "CROSS_SCOPE_DATAFLOW_LEAK",
        "DATAFLOW_IDENTITY_COLLISION", "ILLEGAL_DIMENSION_OPERATION", "UNIT_PROPAGATION_CONFLICT",
        "UNIT_PROPAGATION_UNRESOLVED", "UNIT_SOURCE_CONTRADICTION", "SYMBOL_MAGIC_SCOPE_MISSING")}
    counters["ENTITY_NATURE_UNKNOWN"] += entity_relation == "UNKNOWN"
    counters["ENTITY_NATURE_INCOMPATIBLE"] += entity_relation == "INCOMPATIBLE"
    counters["ENTITY_NATURE_FALSE_EXACT"] += entity_relation == "EXACT" and expected_entity != actual_entity
    counters["FUNCTION_PROMOTED_TO_VALUE"] += actual_entity == "FUNCTION" and expected_entity.endswith("VALUE")
    counters["STATE_PROMOTED_TO_OBJECT"] += actual_entity == "STATE" and expected_entity in {"OBJECT", "PLAN"}
    counters["IDENTITY_ROLE_MISMATCH"] += {actual_entity, expected_entity} <= {"IDENTITY", "TICKET"} and actual_entity != expected_entity
    if dataflow:
        counters["UNRESOLVED_DATAFLOW_SOURCE"] += len(dataflow.unresolved_sources)
        counters["UNRESOLVED_DATAFLOW_SINK"] += len(dataflow.unresolved_sinks)
        ids = [node.declaration for node in dataflow.nodes.values() if node.declaration]
        counters["DATAFLOW_IDENTITY_COLLISION"] += len(ids) - len(set(ids))
    if units:
        counters["ILLEGAL_DIMENSION_OPERATION"] += len(units.illegal_operations)
        counters["UNIT_PROPAGATION_CONFLICT"] += len(units.conflicts)
        counters["UNIT_PROPAGATION_UNRESOLVED"] += len(units.unresolved)
    counters["SYMBOL_MAGIC_SCOPE_MISSING"] += expected_scope in {"PER_SYMBOL_MAGIC", "PER_SYMBOL_MAGIC_CYCLE"} and actual_scope not in {"PER_SYMBOL_MAGIC", "PER_SYMBOL_MAGIC_CYCLE"}
    return counters


def entity_nature(symbol: Symbol, unit: str = "UNKNOWN") -> str:
    """Classify engineering nature solely from parsed source evidence."""
    name = symbol.identifier.lower(); kind = symbol.kind
    if kind in {"function", "method"}: return "FUNCTION"
    if kind == "enum": return "STATE" if "state" in name or "phase" in name else "ENUM"
    if kind == "enum_member": return "STATE" if "state" in symbol.declared_type.lower() else "ENUM"
    if "snapshot" in name: return "SNAPSHOT"
    if "request" in name: return "REQUEST"
    if "result" in name: return "RESULT"
    if "event" in name: return "LEDGER_EVENT"
    if kind in {"struct", "class"}: return "PLAN" if "plan" in name else "STRUCT"
    if "ticket" in name: return "TICKET"
    if name.endswith("id") or "identifier" in name: return "IDENTITY"
    if kind == "input_parameter": return "POLICY"
    if unit in {"LOT", "MONEY", "PRICE", "RATIO"}: return f"{unit}_VALUE"
    if kind in {"struct_field", "class_field", "global_variable", "static_variable"}: return "CACHE"
    return "VALUE"


def entity_nature_relation(expected: str, actual: str) -> str:
    if expected == actual: return "EXACT"
    if expected == "VALUE" and actual.endswith("_VALUE"): return "COMPATIBLE"
    if actual == "CACHE" and expected in {"VALUE", "LOT_VALUE", "MONEY_VALUE", "PRICE_VALUE"}: return "PARTIAL"
    return "INCOMPATIBLE"


def declaration_identities(root: Path, language: str) -> tuple[list[Symbol], list[DeclarationIdentity]]:
    symbols = index_mql(root) if language == "mql5" else index_python(root)
    scopes_by_file = {}
    if language == "mql5":
        for path in [*root.rglob("*.mq5"), *root.rglob("*.mqh")]:
            scopes_by_file[str(path.relative_to(root))] = _scope_lines(sanitise(path.read_text(errors="ignore"))[0])
    identities = [DeclarationIdentity(
        language, symbol.file,
        scopes_by_file.get(symbol.file, {}).get(symbol.line, symbol.scope) if symbol.kind in {"local_variable","function_parameter","output_reference_parameter"} else symbol.scope,
        symbol.line, symbol.column, symbol.identifier, symbol.parent_symbol, symbol.kind,
    ) for symbol in symbols]
    if len(identities) != len(set(identities)):
        raise ValueError("duplicate declaration identity")
    return symbols, identities


def _scope_lines(clean: str) -> dict[int, str]:
    """Resolve the enclosing MQL aggregate/function for each physical line."""
    result: dict[int, str] = {}
    stack: list[tuple[str, int]] = []
    depth = 0
    pending = ""
    header = re.compile(r"\b(?:struct|class|enum)\s+(\w+)|\b(\w+)\s*\([^;]*\)\s*\{")
    for number, line in enumerate(clean.splitlines(), 1):
        match = header.search(line)
        if match:
            name = match.group(1) or match.group(2)
            kind = "struct" if match.group(1) else "function"
            pending = f"{kind} {name}"
        result[number] = "/".join(x[0] for x in stack) if stack else "module"
        opens, closes = line.count("{"), line.count("}")
        if pending and opens:
            stack.append((pending, depth + 1)); result[number] = "/".join(x[0] for x in stack); pending = ""
            opens -= 1
        for index in range(opens):
            block=f"block@{number}:{index+1}";stack.append((block,depth+index+1))
        depth += opens - closes
        while stack and depth < stack[-1][1]: stack.pop()
    return result


def build_scoped_mql_use_graphs(root: Path) -> dict[DeclarationIdentity, ScopedUseGraph]:
    symbols, identities = declaration_identities(root, "mql5")
    pairs = list(zip(symbols, identities))
    graphs = {identity: ScopedUseGraph(identity) for identity in identities}
    by_file_name: dict[tuple[str, str], list[tuple[Symbol, DeclarationIdentity]]] = {}
    for pair in pairs: by_file_name.setdefault((pair[0].file, pair[0].identifier), []).append(pair)
    for path in sorted([*root.rglob("*.mq5"), *root.rglob("*.mqh")]):
        rel = str(path.relative_to(root)); clean = sanitise(path.read_text(errors="ignore"))[0]
        scopes = _scope_lines(clean)
        for number, line in enumerate(clean.splitlines(), 1):
            for name in set(re.findall(r"[A-Za-z_]\w*", line)):
                options = by_file_name.get((rel, name), [])
                if not options: continue
                scope = scopes[number]
                visible = [pair for pair in options if pair[1].scope_id == scope and pair[0].line <= number]
                if not visible:
                    parents=["/".join(scope.split("/")[:i]) for i in range(len(scope.split("/"))-1,0,-1)]+["module"]
                    for parent in parents:
                        visible=[pair for pair in options if pair[1].scope_id==parent and pair[0].line<=number]
                        if visible:break
                if not visible: continue
                symbol, identity = max(visible, key=lambda pair: pair[0].line)
                if number == symbol.line and line.count(name) == 1 and "=" not in line: continue
                site = f"{rel}:{number}"
                lhs = re.search(rf"\b{re.escape(name)}\b\s*(?:[+\-*/]?=|\+\+|--)", line)
                if lhs: graphs[identity].writes.append(site)
                if not lhs or line.count(name) > 1 or "=" in line and line.find(name) > line.find("="):
                    graphs[identity].reads.append(site)
    for graph in graphs.values():
        graph.reads = sorted(set(graph.reads)); graph.writes = sorted(set(graph.writes))
    return graphs


class _PythonScopedUses(ast.NodeVisitor):
    def __init__(self, rel, pairs, graphs):
        self.rel, self.pairs, self.graphs = rel, pairs, graphs
        self.scopes = ["module"]
    @property
    def scope(self): return "/".join(self.scopes)
    def _enter(self, kind, name, node):
        self.scopes.append(f"{kind} {name}@{node.lineno}"); self.generic_visit(node); self.scopes.pop()
    def visit_FunctionDef(self,node): self._enter("function",node.name,node)
    visit_AsyncFunctionDef=visit_FunctionDef
    def visit_ClassDef(self,node): self._enter("class",node.name,node)
    def _record(self,node,name,ctx):
        candidates=[(s,i) for s,i in self.pairs if s.file==self.rel and s.identifier==name and s.line<=node.lineno]
        if not candidates:return
        def rank(pair):
            declared=pair[1].scope_id; current=self.scope
            return (current.startswith(declared),declared.count("/"),pair[0].line)
        _,identity=max(candidates,key=rank);site=f"{self.rel}:{node.lineno}"
        target=self.graphs[identity]
        (target.reads if isinstance(ctx,ast.Load) else target.writes).append(site)
    def visit_Name(self,node): self._record(node,node.id,node.ctx)
    def visit_Attribute(self,node):
        self._record(node,node.attr,node.ctx);self.generic_visit(node.value)


def build_scoped_python_use_graphs(root: Path) -> dict[DeclarationIdentity, ScopedUseGraph]:
    symbols, identities=declaration_identities(root,"python");pairs=list(zip(symbols,identities))
    graphs={identity:ScopedUseGraph(identity) for identity in identities}
    for path in sorted(root.rglob("*.py")):
        try:tree=ast.parse(path.read_text(errors="ignore"))
        except SyntaxError:continue
        _PythonScopedUses(str(path.relative_to(root)),pairs,graphs).visit(tree)
    for graph in graphs.values():graph.reads=sorted(set(graph.reads));graph.writes=sorted(set(graph.writes))
    return graphs


def build_resolved_python_dataflow(root: Path) -> ResolvedDataflowGraph:
    symbols,identities=declaration_identities(root,"python");pairs=list(zip(symbols,identities));graph=ResolvedDataflowGraph()
    for _,identity in pairs:graph.nodes[str(identity)]=DataflowNode(str(identity),"DECLARATION",identity)
    for path in sorted(root.rglob("*.py")):
        try:tree=ast.parse(path.read_text(errors="ignore"))
        except SyntaxError:continue
        rel=str(path.relative_to(root))
        for node in ast.walk(tree):
            if not isinstance(node,(ast.Assign,ast.AnnAssign,ast.AugAssign,ast.NamedExpr)):continue
            targets=node.targets if isinstance(node,ast.Assign) else [node.target]
            value=node.value
            for target in targets:
                if not isinstance(target,(ast.Name,ast.Attribute)):continue
                name=target.id if isinstance(target,ast.Name) else target.attr
                sinks=[(s,i) for s,i in pairs if s.file==rel and s.identifier==name and s.line<=node.lineno]
                if not sinks:graph.unresolved_sinks.append(f"{rel}:{node.lineno}:{name}");continue
                _,sink_id=max(sinks,key=lambda pair:pair[0].line);sink=graph.nodes[str(sink_id)]
                sources=[n for n in ast.walk(value) if isinstance(n,(ast.Name,ast.Attribute))]
                for source_ast in sources:
                    source_name=source_ast.id if isinstance(source_ast,ast.Name) else source_ast.attr
                    found=[(s,i) for s,i in pairs if s.file==rel and s.identifier==source_name and s.line<=node.lineno]
                    if found:
                        _,source_id=max(found,key=lambda pair:pair[0].line)
                        operation="ARITHMETIC" if isinstance(value,ast.BinOp) else "COPY"
                        graph.edges.append(ResolvedDataflowEdge(graph.nodes[str(source_id)],sink,operation,f"{rel}:{node.lineno}",ast.unparse(value)))
    return graph


def build_resolved_mql_dataflow(root: Path) -> ResolvedDataflowGraph:
    symbols, identities = declaration_identities(root, "mql5")
    graph = ResolvedDataflowGraph()
    pairs = list(zip(symbols, identities))
    for _, identity in pairs:
        graph.nodes[str(identity)] = DataflowNode(str(identity), "DECLARATION", identity)
    api_pattern = re.compile(r"(?:PositionGet\w+|HistoryDealGet\w+|SymbolInfo\w+)\s*\(\s*(\w+)")
    for path in sorted([*root.rglob("*.mq5"), *root.rglob("*.mqh")]):
        rel = str(path.relative_to(root)); clean = sanitise(path.read_text(errors="ignore"))[0]
        scopes = _scope_lines(clean)
        for number, line in enumerate(clean.splitlines(), 1):
            assignment = re.search(r"\b(\w+)\s*=\s*(.+?);", line)
            if not assignment: continue
            sink_name, expression = assignment.groups(); scope = scopes[number]
            candidates = [(s, i) for s, i in pairs if s.file == rel and s.identifier == sink_name and i.scope_id in {scope, "module"} and s.line <= number]
            if not candidates: graph.unresolved_sinks.append(f"{rel}:{number}:{sink_name}"); continue
            _, sink_id = max(candidates, key=lambda pair: (pair[0].scope == scope, pair[0].line))
            sink = graph.nodes[str(sink_id)]; site = f"{rel}:{number}"
            api = api_pattern.search(expression)
            if api:
                key = f"API:{api.group(1)}"; source = graph.nodes.setdefault(key, DataflowNode(key, "API_RESULT"))
                graph.edges.append(ResolvedDataflowEdge(source, sink, "ASSIGN", site, expression)); continue
            names = re.findall(r"\b[A-Za-z_]\w*\b", expression)
            resolved = False
            for name in names:
                sources = [(s, i) for s, i in pairs if s.file == rel and s.identifier == name and i.scope_id in {scope, "module"} and s.line <= number]
                if not sources: continue
                _, source_id = max(sources, key=lambda pair: (pair[0].scope == scope, pair[0].line))
                operation = "ARITHMETIC" if re.search(r"[+*/-]", expression) else "COPY"
                graph.edges.append(ResolvedDataflowEdge(graph.nodes[str(source_id)], sink, operation, site, expression)); resolved = True
            if not resolved and not re.fullmatch(r"[\d.\s+-]+", expression): graph.unresolved_sources.append(f"{site}:{expression}")
    return graph
