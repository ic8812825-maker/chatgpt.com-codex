"""Small pre-fix reproductions and seventh-correction regression controls."""
from pathlib import Path
from tempfile import TemporaryDirectory

from stage_3_1_3.seventh_engine import build_resolved_mql_dataflow, build_scoped_mql_use_graphs, entity_nature, entity_nature_relation
from stage_3_1_3.source_evidence import Symbol


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


if __name__ == "__main__":
    shadowing_control()
    entity_nature_control()
    dataflow_control()
    print("SHADOWING_TESTS=PASS")
