"""Load the immutable HALR-02 comparison modules from a supplied archive."""
import os
from pathlib import Path
import sys


def source():
    value = os.environ.get("HALR02_DIR")
    if value is None:
        raise RuntimeError("Set HALR02_DIR to the HALR-02 archive at ac17e6a")
    path = Path(value).resolve()
    if not (path/"ledger2.py").is_file():
        raise RuntimeError(f"Missing pinned HALR-02 sources: {path}")
    if str(path) not in sys.path:
        sys.path.append(str(path))
    return path
