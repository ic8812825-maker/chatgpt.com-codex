#!/usr/bin/env python3
"""Isolated negative and positive controls for the Stage 3.1.3 validator."""
from validate_stage_3_1_3_glossary import run_control_tests

def main():
    nt,np,pt,pp,details=run_control_tests()
    for name,passed in details: print(f"NEGATIVE_{name}={'PASS' if passed else 'FAIL'}")
    print(f"NEGATIVE_TESTS_TOTAL={nt}"); print(f"NEGATIVE_TESTS_PASSED={np}")
    print(f"POSITIVE_TESTS_TOTAL={pt}"); print(f"POSITIVE_TESTS_PASSED={pp}")
    result=np==nt and pp==pt and nt>=20 and pt>=10
    print("SEMANTIC_MUTATION_TESTS="+("PASS" if result else "FAIL")); return 0 if result else 1
if __name__ == "__main__": raise SystemExit(main())
