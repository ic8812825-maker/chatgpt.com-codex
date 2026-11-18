"""Locate immutable pinned research archives."""
from pathlib import Path
import os
import sys

PINS={"HALR02_DIR":"ac17e6a365ec97457b3fd358163f5aab91f15924",
      "HALR03_DIR":"7d12c24192730b27dac92bb8a5bad0c0efa900cc",
      "HALR04_DIR":"dd957384a43253964c906379cf37c0ec80de0828"}


def setup():
    paths={name:Path(os.environ[name]).resolve() for name in PINS}
    for key in ("HALR04_DIR","HALR03_DIR","HALR02_DIR"):
        path=paths[key]
        if not path.is_dir():
            raise ValueError(f"Missing pinned directory {path}")
        if str(path) not in sys.path:
            sys.path.append(str(path))
    return paths
