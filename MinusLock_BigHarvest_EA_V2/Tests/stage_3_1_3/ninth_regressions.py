"""Concrete production-pipeline invariants for the ninth correction."""
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

TESTS_ROOT=Path(__file__).resolve().parents[1]
if str(TESTS_ROOT) not in sys.path:
    sys.path.insert(0, str(TESTS_ROOT))

from stage_3_1_3.seventh_engine import (
    build_resolved_mql_dataflow, build_scoped_mql_use_graphs,
    build_scoped_python_use_graphs, propagate_units,
)


def run() -> None:
    with TemporaryDirectory() as directory:
        root=Path(directory)
        (root/"scoped.mqh").write_text(
            "double LotFn(){\n double same=PositionGetDouble(POSITION_VOLUME);\n return same;\n}\n"
            "double MoneyFn(){\n double same=HistoryDealGetDouble(1,DEAL_PROFIT);\n return same;\n}\n"
            "struct Box {\n double same;\n};\n")
        graphs=build_scoped_mql_use_graphs(root)
        same=[(identity,graph) for identity,graph in graphs.items() if identity.identifier=="same"]
        assert len(same)>=3, "SAME_NAME_LOT_MONEY_CROSS_SCOPE"
        assert len({identity.parent_symbol for identity,_ in same})>=3, "WRONG_STRUCT_OWNER"
        assert all(len(graph.reads)<=1 for identity,graph in same
                   if identity.declaration_kind!="struct_field"), "CROSS_SCOPE_READ_LEAKS"
        flow=build_resolved_mql_dataflow(root); units=propagate_units(flow)
        values={key:value for key,value in units.units.items() if "same" in key}
        assert "LOT" in values.values() and "MONEY" in values.values(), "SCOPED_DATAFLOW"

    with TemporaryDirectory() as directory:
        root=Path(directory); (root/"shadow.py").write_text(
            "value=1\ndef local(value):\n    return value\ndef nested():\n    value=2\n    return value\n")
        graphs=build_scoped_python_use_graphs(root)
        values=[identity for identity in graphs if identity.identifier=="value"]
        assert len(values)==3, "PYTHON_MODULE_LOCAL_SHADOW"
        assert len({identity.scope_id for identity in values})==3, "PYTHON_WRONG_SCOPE"

    print("NINTH_REGRESSION_INVARIANTS=PASS")


if __name__=="__main__": run()
