"""Small pre-fix reproductions and seventh-correction regression controls."""
from pathlib import Path
from tempfile import TemporaryDirectory

from stage_3_1_3.seventh_engine import build_scoped_mql_use_graphs


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


if __name__ == "__main__":
    shadowing_control()
    print("SHADOWING_TESTS=PASS")
