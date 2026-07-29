"""Small pre-fix reproductions and seventh-correction regression controls."""
from pathlib import Path
from tempfile import TemporaryDirectory

from stage_3_1_3.seventh_engine import build_resolved_mql_dataflow, build_resolved_python_dataflow, build_scoped_mql_use_graphs, build_scoped_python_use_graphs, compute_scope_proof, entity_nature, entity_nature_relation, propagate_units, strict_scope_relation
from stage_3_1_3.source_evidence import Symbol
from stage_3_1_3.counter_audit import audit_blocking_counters


def shadowing_control() -> None:
    source = """double lot;
void A(){
 double lot=1;
 Print(lot);
}
void B(){
 double lot=2;
 lot+=1;
}
struct StructX {
 double lot;
};
"""
    with TemporaryDirectory() as directory:
        root = Path(directory); (root / "shadow.mqh").write_text(source)
        graphs = build_scoped_mql_use_graphs(root)
        lots = [graph for identity, graph in graphs.items() if identity.identifier == "lot"]
        assert len(lots) == 4, len(lots)
        assert len({graph.declaration for graph in lots}) == 4
        sites = [site for graph in lots for site in graph.reads + graph.writes]
        assert len(sites) == len(set(sites)), sites


def entity_nature_control() -> None:
    function = Symbol("Money", "function", "double", "x.mqh", 1, 1, "function Money", "", (), "double Money()")
    state = Symbol("CycleState", "enum", "enum", "x.mqh", 2, 1, "module", "", (), "enum CycleState")
    ticket = Symbol("dealTicket", "local_variable", "ulong", "x.mqh", 3, 1, "function A", "A", (), "ulong dealTicket;")
    assert entity_nature_relation("MONEY_VALUE", entity_nature(function, "MONEY")) == "INCOMPATIBLE"
    assert entity_nature_relation("PLAN", entity_nature(state)) == "INCOMPATIBLE"
    assert entity_nature_relation("MONEY_VALUE", entity_nature(ticket)) == "INCOMPATIBLE"


def dataflow_control() -> None:
    source = """void A(){
 double positionVolume=PositionGetDouble(POSITION_VOLUME);
 double farLot=positionVolume;
 double requestLot=farLot;
}
"""
    with TemporaryDirectory() as directory:
        root = Path(directory); (root / "flow.mqh").write_text(source)
        graph = build_resolved_mql_dataflow(root)
        assert len(graph.edges) == 3
        assert any(edge.source.kind == "API_RESULT" for edge in graph.edges)
        assert not graph.unresolved_sinks


def unit_control() -> None:
    source = """input double ratio;
void A(){
 double lot=PositionGetDouble(POSITION_VOLUME);
 double scaled=lot*ratio;
 double money=HistoryDealGetDouble(DEAL_PROFIT);
 double illegal=lot+money;
}
"""
    with TemporaryDirectory() as directory:
        root = Path(directory); (root / "units.mqh").write_text(source)
        graph = build_resolved_mql_dataflow(root)
        ratio = next(key for key, node in graph.nodes.items() if node.declaration and node.declaration.identifier == "ratio")
        result = propagate_units(graph, {ratio: "RATIO"})
        scaled = next(key for key, node in graph.nodes.items() if node.declaration and node.declaration.identifier == "scaled")
        assert result.units[scaled] == "LOT"
        assert result.illegal_operations


def scope_control() -> None:
    symbol_only = "bool A(){ return PositionGetString(POSITION_SYMBOL)==_Symbol; }"
    helper = """bool Managed(string symbol,long magic){
 return PositionGetString(POSITION_SYMBOL)==symbol && PositionGetInteger(POSITION_MAGIC)==magic;
}
bool Caller(){ return Managed(_Symbol,123); }
"""
    with TemporaryDirectory() as directory:
        root = Path(directory); (root / "symbol.mqh").write_text(symbol_only)
        assert compute_scope_proof(root).scope == "PER_SYMBOL"
        assert strict_scope_relation("PER_SYMBOL_MAGIC", "PER_SYMBOL") == "PROVEN_SUBSET"
    with TemporaryDirectory() as directory:
        root = Path(directory); (root / "helper.mqh").write_text(helper)
        proof = compute_scope_proof(root)
        assert proof.scope == "PER_SYMBOL_MAGIC" and proof.symbol_evidence and proof.magic_evidence


def python_shadowing_control() -> None:
    source="""value=1
def A():
    value=2
    return value
def B(value):
    return value
"""
    with TemporaryDirectory() as directory:
        root=Path(directory);(root/"shadow.py").write_text(source)
        graphs=build_scoped_python_use_graphs(root)
        values=[g for i,g in graphs.items() if i.identifier=="value"]
        assert len(values)==3 and len({g.declaration for g in values})==3
        flow=build_resolved_python_dataflow(root);assert flow.nodes


if __name__ == "__main__":
    shadowing_control()
    entity_nature_control()
    dataflow_control()
    unit_control()
    scope_control()
    python_shadowing_control()
    audit = audit_blocking_counters()
    assert audit["VACUOUS_BLOCKING_COUNTERS"] == 0, audit
    print("SHADOWING_TESTS=PASS")
