"""Compatibility shim; semantic authority lives in semantic_engine."""
from stage_3_1_3.semantic_engine import evaluate_canonical_mapping

def discover(root, contract, language, symbols=None):
    return evaluate_canonical_mapping(root, contract, language, symbols)
