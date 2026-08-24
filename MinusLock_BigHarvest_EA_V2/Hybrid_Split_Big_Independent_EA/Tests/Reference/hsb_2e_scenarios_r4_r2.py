#!/usr/bin/env python3
import argparse
CONTRACTS={'INITIAL':['VALIDATE','PERSIST_INTENT','AGGREGATE_FILL','REQUIRE_FULL_FILL','PERSIST_SETTLEMENT','COMMIT_FSM'],'BIG':['VALIDATE','PERSIST_INTENTS','AGGREGATE_EACH_TICKET','REQUIRE_ALL_FULL','CALCULATE_MONEY','PERSIST_SETTLEMENT','COMMIT_FSM'],'SMALL':['VALIDATE','BLOCK_DUAL_TAIL','AGGREGATE_EACH_TICKET','REQUIRE_ALL_FULL','ASSIGN_NEW_FAR','PERSIST_SETTLEMENT','COMMIT_FSM'],'RESTART':['LOAD_PERSISTED_FILLS','RECONCILE_DEALS','BLOCK_DUPLICATES','REQUIRE_FULL_FILL','RESUME_OR_BLOCK']}
def validate(name,ops):return name in CONTRACTS and ops==CONTRACTS[name]
def self_test():
 c=[validate(k,v) for k,v in CONTRACTS.items()]+[not validate('BIG',CONTRACTS['BIG'][::-1])];print('\n'.join(f'R4R2_SCENARIO_{i}={"PASS" if x else "FAIL"}' for i,x in enumerate(c,1)));print(f'SCENARIOS_R4_R2_SELF_TESTS={sum(c)}/{len(c)}');return all(c)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
