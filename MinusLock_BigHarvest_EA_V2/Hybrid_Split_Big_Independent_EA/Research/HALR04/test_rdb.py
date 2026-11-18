import importlib
import unittest
from replay import run

rdb=importlib.import_module("06_RDB_POLICY")


def case():
    return dict(month="fixture",scheme="S2",interval=30,id="only",
                orientation=1,entry=(0,109690,109710),
                features={"spread":20,"range30":100,"momentum":150},
                obs=[(i*1800000,109990+150*i,110010+150*i) for i in range(13)],
                complete=True)


class RDBTests(unittest.TestCase):
    def test_rdb0_exact_k(self):
        a=run(case(),"K-EXECUTABLE","delayed_partial")
        b=run(case(),"RDB-0","delayed_partial")
        a.pop("decision")
        b.pop("decision")
        self.assertEqual(a,b)

    def test_decision_uses_only_frozen_prefix(self):
        a,b=case(),case()
        b["obs"][2:]=[(i*1800000,110140-250*i,110160-250*i) for i in range(2,13)]
        values={"RECOVER_A3_ER":{"all":{"n":20,"months":4,"shrunk":10,
                                        "valid_all":True,"lower95_block":2}}}
        logs=[]
        for episode in (a,b):
            trace=[]
            run(episode,"RDB-4","quote_fill",rdb.RDBCycle,values,trace)
            logs.append([e for e in trace if e["step"]<=1])
        self.assertEqual(logs[0],logs[1])
        self.assertTrue(any(e["event"]=="RECOVER_A3_ER" for e in logs[0]))

    def test_unavailable_close_keeps_residual(self):
        a=case()
        a["obs"]=a["obs"][:1]
        r=run(a,"RDB-1","delayed_partial",rdb.RDBCycle,{})
        self.assertFalse(r["flat"])
        self.assertEqual(r["decision"],"NO_CERTIFIED_ACTION")
        self.assertEqual(r["residual"],2)

    def test_no_evidence_means_exit_candidate(self):
        self.assertEqual(rdb.decide("RDB-4",case()["features"],{})[0],"EXIT_K")
