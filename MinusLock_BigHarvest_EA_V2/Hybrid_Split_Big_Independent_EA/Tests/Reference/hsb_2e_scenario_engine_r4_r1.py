#!/usr/bin/env python3
import argparse
BIG=[f'BIG_PHASE_{i}_{x}' for i,x in enumerate(('VALIDATE','PREPARE_BIG_SMALL_INTENTS','PERSIST_INTENTS','CONFIRM_BIG_SMALL_DEALS','CALCULATE_MONEY','CALCULATE_ALLOCATION','PREPARE_FAR_INTENT','CONFIRM_FAR_DEAL','APPLY_LEDGER','COMMIT_FSM'),1)]
SMALL=[f'SMALL_PHASE_{i}_{x}' for i,x in enumerate(('VALIDATE','PREPARE_SMALL_OLD_FAR_INTENTS','PERSIST_INTENTS','CONFIRM_SMALL_OLD_FAR_DEALS','CALCULATE_BIG_CLOSE','PREPARE_BIG_PARTIAL_INTENT','CONFIRM_BIG_DEAL','ASSIGN_NEW_FAR','APPLY_RESERVE','COMMIT_FSM'),1)]
def validate(phases):return {'result':'PASS' if phases in (BIG,SMALL) else 'FAIL','reason':'OK' if phases in (BIG,SMALL) else 'TRANSACTION_PHASE_ORDER'}
def self_test():
 c=[validate(BIG)['result']=='PASS',validate(SMALL)['result']=='PASS',validate(BIG[::-1])['result']=='FAIL'];print('\n'.join(f'R4R1_PHASE_{i}={"PASS" if x else "FAIL"}' for i,x in enumerate(c,1)));return all(c)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
