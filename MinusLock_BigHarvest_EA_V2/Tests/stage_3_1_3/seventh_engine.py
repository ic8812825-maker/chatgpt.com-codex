"""Declaration-scoped semantic engine for the Stage 3.1.3 seventh correction.

Unlike the legacy discovery index, every fact in this module is keyed by the
concrete declaration, never by an identifier spelling alone.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
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


def entity_nature(symbol: Symbol, unit: str = "UNKNOWN") -> str:
    """Classify engineering nature solely from parsed source evidence."""
    name = symbol.identifier.lower(); kind = symbol.kind
    if kind in {"function", "method"}: return "FUNCTION"
    if kind == "enum": return "STATE" if "state" in name or "phase" in name else "ENUM"
    if kind == "enum_member": return "STATE" if "state" in symbol.declared_type.lower() else "ENUM"
    if kind in {"struct", "class"}: return "PLAN" if "plan" in name else "STRUCT"
    if "ticket" in name: return "TICKET"
    if name.endswith("id") or "identifier" in name: return "IDENTITY"
    if kind == "input_parameter": return "POLICY"
    if "snapshot" in name: return "SNAPSHOT"
    if "request" in name: return "REQUEST"
    if "result" in name: return "RESULT"
    if "event" in name: return "LEDGER_EVENT"
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
    identities = [DeclarationIdentity.from_symbol(language, symbol) for symbol in symbols]
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
        result[number] = stack[-1][0] if stack else "module"
        opens, closes = line.count("{"), line.count("}")
        if pending and opens:
            stack.append((pending, depth + opens)); result[number] = pending; pending = ""
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
                visible = [pair for pair in options if pair[0].scope == scope]
                if not visible: visible = [pair for pair in options if pair[0].scope == "module"]
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
            candidates = [(s, i) for s, i in pairs if s.file == rel and s.identifier == sink_name and s.scope in {scope, "module"} and s.line <= number]
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
                sources = [(s, i) for s, i in pairs if s.file == rel and s.identifier == name and s.scope in {scope, "module"} and s.line <= number]
                if not sources: continue
                _, source_id = max(sources, key=lambda pair: (pair[0].scope == scope, pair[0].line))
                operation = "ARITHMETIC" if re.search(r"[+*/-]", expression) else "COPY"
                graph.edges.append(ResolvedDataflowEdge(graph.nodes[str(source_id)], sink, operation, site, expression)); resolved = True
            if not resolved and not re.fullmatch(r"[\d.\s+-]+", expression): graph.unresolved_sources.append(f"{site}:{expression}")
    return graph
