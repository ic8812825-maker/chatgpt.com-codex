"""Hash sources and verify the complete baseline replay against pinned evidence."""
import csv
from datetime import datetime,timezone
from hashlib import file_digest
import json
from pathlib import Path
import subprocess
import sys

from pinned import setup,PINS

NAMES={
    "HALR02_DIR":["a3rc.py","meta_rc.py","execution.py","ledger2.py","runner.py","risk.py","scenarios2.py"],
    "HALR03_DIR":["04_EXECUTION_SIMULATOR.py","05_A3_ER_POLICY.py","06_META_ER_POLICY.py","fetch_histdata.py"],
    "HALR04_DIR":["contract.json","periods.json","replay.py","04_CAUSAL_REPLAY.py","data_scan.py","holdout.py"],
}


def dump(name,record):
    Path(name+".json").write_text(json.dumps(record,indent=2,sort_keys=True)+"\n")


def hashes(paths):
    result={}
    for key,names in NAMES.items():
        for name in names:
            with (paths[key]/name).open("rb") as f:
                result[key+"/"+name]=file_digest(f,"sha256").hexdigest()
    return result


def replay_baseline(paths,data):
    path=paths["HALR04_DIR"]
    table=path/"08_PAIRED_RESULTS.csv"
    expected=table.read_bytes()
    commands=(("final_audit.py",str(data)),("holdout.py",str(data)))
    for cmd in commands:
        subprocess.run([sys.executable,"-B",*cmd],cwd=path,check=True)
    assert expected==table.read_bytes()
    with table.open() as f:
        rows=[r for r in csv.DictReader(f) if r["panel"]=="S2/30" and r["mode"]=="quote_fill"]
    selected={r["policy"]:r for r in rows}
    assert selected["M-ER"]["recoveries"]=="11" and selected["K-EXECUTABLE"]["risk_violations"]=="28"
    a=json.loads((path/"AUDIT_RESULTS.json").read_text())
    return dict(reproduced=True,byte_identical="08_PAIRED_RESULTS.csv",
                activations=int(selected["M-ER"]["n"]),initial_margin=a["initial_margin_failures"],
                m_er_recoveries=int(selected["M-ER"]["recoveries"]),
                audit=a,tests=json.loads((path/"TEST_RESULTS.json").read_text()),python=sys.version)


if __name__=="__main__":
    paths=setup()
    dump("01_DEPENDENCY_HASHES",hashes(paths))
    if len(sys.argv)>1:
        dump("01_REPRODUCTION_RESULTS",replay_baseline(paths,Path(sys.argv[1]).resolve()))
    dump("01_BASELINE_MANIFEST",dict(base="d81c048bac82e7d8fd5e5c872d68a96e6983927f",
         branch="research/halr05",source_shas=PINS,pr={7:PINS["HALR02_DIR"],8:PINS["HALR03_DIR"],
         9:PINS["HALR04_DIR"]},checked_utc=datetime.now(timezone.utc).isoformat(),
         parameters="Exact HALR04 contract.json; Params() and dispatch in pinned replay.py"))
