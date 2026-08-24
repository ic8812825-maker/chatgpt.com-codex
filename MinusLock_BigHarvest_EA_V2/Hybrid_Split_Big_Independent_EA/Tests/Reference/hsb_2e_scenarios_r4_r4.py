#!/usr/bin/env python3
import argparse
ORDER=['VALIDATE_PRIMITIVES','VALIDATE_REGISTRY','VALIDATE_IDENTITY','VALIDATE_LEGS','AGGREGATE_PER_TICKET','PERSIST_PARTIAL_EVIDENCE','PERSIST_REGISTRY','BUILD_PROPOSAL','PERSIST_DECISION','INCREMENT_REVISION','COMMIT_FSM']
SCHEMAS={'INITIAL':{'required':['WINNER'],'partial':[]},'BIG':{'required':['BIG','SMALL'],'partial':[]},'SMALL':{'required':['SMALL','OLD_FAR','BIG'],'partial':['BIG']},'FINAL':{'required':['FAR'],'partial':['FAR']}}
def validate(s,ops):return s in SCHEMAS and ops==ORDER and len(ops)==len(set(ops)) and ops.index('PERSIST_PARTIAL_EVIDENCE')<ops.index('COMMIT_FSM')
def self_test():
 t=[validate(k,ORDER) for k in SCHEMAS]+[not validate('BIG',ORDER[::-1]),not validate('X',ORDER)];
 for i,x in enumerate(t,1):print(f'R4_SCENARIO_{i}={"PASS" if x else "FAIL"}')
 print(f'SCENARIOS_R4_R4_SELF_TESTS={sum(t)}/{len(t)}');return all(t)
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
