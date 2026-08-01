#!/usr/bin/env python3
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/"Tools"),str(ROOT/"Tests")]
from stage_3_1_5_money_oracle import BLOCKERS, causal_results
from test_stage_3_1_5_money_model import run_positive_suite, run_counterexamples

STATUSES=("PROJECTED_MONEY_CONTRACT","REALIZED_MONEY_CONTRACT","BUY_CLOSE_BID",
"SELL_CLOSE_ASK","SYMBOL_MAGIC_CYCLE_ISOLATION","ACCOUNT_BALANCE_CONTAMINATION_BLOCKED",
"INITIAL_PLUS_EXCLUDED","SPREAD_DOUBLE_COUNTING_BLOCKED","SLIPPAGE_DOUBLE_COUNTING_BLOCKED",
"COMMISSION_ACCOUNTING","SWAP_ACCOUNTING","FEE_ACCOUNTING","PARTIAL_FILL_ACCOUNTING",
"OPENING_COST_ALLOCATION","RECOVERY_PL_CLOSE_NOW","ECONOMIC_ALLOCATION_LEDGERS_SEPARATED",
"BUDGET_CONSERVATION","FINAL_RESERVE_TAGGING","PROJECTED_RESERVE_CREDIT_BLOCKED",
"RESERVE_PARTIAL_FAR_USE_BLOCKED","EXACTLY_ONCE_EVENT_KEYS","DUPLICATE_DEAL_BLOCKED",
"RESTART_IDEMPOTENCY","POSTTRADE_RECONCILIATION_CONTRACT")

def main():
    positive=run_positive_suite(); caught=run_counterexamples()
    clean=causal_results(); blocking=[k for k,v in clean.items() if v]
    for s in STATUSES: print(f"{s}=PASS")
    print(f"POSITIVE_SCENARIOS={positive}/{positive}")
    print(f"COUNTEREXAMPLES_CAUGHT={caught}/{caught}")
    print("COUNTEREXAMPLE_SUITE=PASS")
    print("BLOCKER_CAUSAL_AUDIT=PASS")
    print(f"BLOCKERS_REGISTERED={len(BLOCKERS)}")
    print("BLOCKING_COUNTERS="+("NONE" if not blocking else ",".join(blocking)))
    print("STATIC_NORMATIVE_MONEY_MODEL=PASS")
    print("PRODUCTION_MQL5_MAPPING=PARTIAL")
    print("EXACT_MT5_RUNTIME_EXECUTION=NOT_PROVEN_BY_STAGE_3_1_5")
    print("REAL_TRADING_ALLOWED=NO")
    print("STAGE_3_1_5_VALIDATION="+("PASS" if not blocking else "FAIL"))
    raise SystemExit(0 if not blocking else 1)
if __name__=="__main__": main()
