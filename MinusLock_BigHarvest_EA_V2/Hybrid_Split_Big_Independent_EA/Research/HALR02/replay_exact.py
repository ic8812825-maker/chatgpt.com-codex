"""Recompute exact rows from the frozen comparison settings."""
import json
from audit2 import load,configured
from study2 import exhaustive

if __name__=="__main__":
    labels={"A3-selected","M-selected","K-EXECUTABLE"}
    profiles=[(r["label"],configured(r)) for r in load("COMPARISON_RESULTS")
              if r["label"] in labels]
    exhaustive(profiles)
