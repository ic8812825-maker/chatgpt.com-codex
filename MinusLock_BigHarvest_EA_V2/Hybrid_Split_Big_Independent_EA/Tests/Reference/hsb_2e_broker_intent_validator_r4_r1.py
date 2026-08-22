#!/usr/bin/env python3
import argparse
def validate(intents):
 errors=[];ids=set()
 for x in intents:
  if x['intentId'] in ids:errors.append('DUPLICATE_INTENT')
  ids.add(x['intentId'])
  if x['actionType'].startswith('CLOSE') and x['positionTicket']<=0:errors.append('UNKNOWN_TICKET')
  expected='BID' if x['direction']=='BUY' else 'ASK' if x['direction']=='SELL' else None
  if expected is None or x['expectedPriceSide']!=expected:errors.append('PRICE_SIDE')
 return {'result':'PASS' if not errors else 'FAIL','errors':errors}
def self_test():
 b={'intentId':'I','actionType':'CLOSE_POSITION_FULL','positionTicket':1,'direction':'BUY','expectedPriceSide':'BID'};c=[validate([b])['result']=='PASS',validate([{**b,'expectedPriceSide':'ASK'}])['result']=='FAIL'];print('\n'.join(f'R4R1_INTENT_{i}={"PASS" if x else "FAIL"}' for i,x in enumerate(c,1)));return all(c)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
