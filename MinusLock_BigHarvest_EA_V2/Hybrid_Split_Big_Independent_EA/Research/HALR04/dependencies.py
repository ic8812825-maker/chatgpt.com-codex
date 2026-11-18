"""Load the pinned archives without changing either checkout."""
from pathlib import Path
import os
import sys

def setup():
    h2,h3=(Path(os.environ[k]).resolve() for k in ("HALR02_DIR","HALR03_DIR"))
    if not (h2/"ledger2.py").is_file() or not (h3/"04_EXECUTION_SIMULATOR.py").is_file():
        raise ValueError("Set HALR02_DIR and HALR03_DIR to the pinned archives")
    for path in (h3,h2):
        if str(path) not in sys.path:
            sys.path.append(str(path))
    return h2,h3
