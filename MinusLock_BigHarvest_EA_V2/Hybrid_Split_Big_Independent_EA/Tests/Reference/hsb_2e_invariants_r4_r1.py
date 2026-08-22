#!/usr/bin/env python3
from decimal import Decimal
import argparse
D=lambda x:Decimal(str(x))
def check(name,i,a):
 o=a.get('output',{})
 try:
  rules={
   'BUY_CLOSE_SIDE':lambda:o['buyClosePrice']==str(i['context']['bid']),
   'SELL_CLOSE_SIDE':lambda:o['sellClosePrice']==str(i['context']['ask']),
   'FAR_PRICE_SOURCE':lambda:o['farPriceSource']=='SNAPSHOT_DIRECTIONAL_CLOSE' and D(o['farLoss'])==max(D(0),-(D(i['context']['bid'])-D(next(p['openPrice'] for p in i['positions'] if p['role']=='FAR')))*D(next(p['volume'] for p in i['positions'] if p['role']=='FAR'))*D(next(p.get('moneyPerPriceLot',100) for p in i['positions'] if p['role']=='FAR'))),
   'BIG_ALLOCATION_POLICY':lambda:D(o['closeFarShare'])+D(o['reserveShare'])==1,
   'BIG_PROFIT_SPLIT':lambda:D(o['availableProfit'])==max(D(0),D(o['bigNet'])+D(o['smallNet'])) and D(o['rawCloseFarBudget'])==D(o['availableProfit'])*D(o['closeFarShare']) and D(o['rawReserveAdd'])==D(o['availableProfit'])*D(o['reserveShare']),
   'MONEY_CONSERVATION':lambda:abs(D(o['availableProfit'])-(D(o['actualPartialFarConsumption'])+D(o['reserveAdd'])+D(o['unallocatedRemainder'])))<=D('0.01'),
   'RESERVE_ACCUMULATION':lambda:D(o['reserveAfter'])>=D(o['reserveBefore']) and (o.get('alreadyConsumed') or D(o['reserveAdd'])==D(o['rawReserveAdd'])),
   'PARTIAL_FAR_RESERVE_ISOLATION':lambda:D(o['reserveUsedForPartialFar'])==0 and D(o['closeFarBudget'])==D(o['rawCloseFarBudget']).quantize(D('0.01')), 
   'FINAL_CLOSE_GATES':lambda:not o['finalFarCloseAllowed'] or D(o['recoveryPL'])>0,
   'SMALL_SHARE_SEMANTICS':lambda:D(o['rawBigCloseVolume'])==D(o['bigVolumeBefore'])*D(o['closeBigOnSmall']),
   'SMALL_SHARE_CONSERVATION':lambda:D(o['closeBigOnSmall'])+D(o['remainBigOnSmall'])==1 and D(o['bigVolumeBefore'])==D(o['bigClosedVolume'])+D(o['newFarVolume']) and abs(D(o['newFarVolume'])-D(o['expectedRemainVolume']))<=D(i['context']['volumeStep']),
   'NEW_FAR_COMPRESSION':lambda:D(o['newFarVolume'])<D(next(p['volume'] for p in i['positions'] if p['role']=='FAR')),
   'SMALL_RESERVE_ALLOCATION':lambda:D(o['roundedSmallReserveAdd'])==D(0) if o['alreadyConsumed'] else D(o['roundedSmallReserveAdd'])>=0,
   'INITIAL_LOCK_DIRECTIONS':lambda:o['buyCount']==1 and o['sellCount']==1,
   'INITIAL_LOCK_CONFIRMATION':lambda:o['farAssignedAfterConfirmation'] is True,
   'INITIAL_POSITIVE_PROFIT_IGNORED':lambda:D(o['recoveryBudgetWithInitialProfit'])==D(o['recoveryBudgetWithoutInitialProfit']) and any(x['source']=='IGNORED_INITIAL_POSITIVE_PROFIT' and not x['consumable'] for x in a['ledgerDelta']),
   'TRANSACTION_PHASE_ORDER':lambda:a['transactionPhase'] in ('BIG_PHASE_2_PREPARE_BIG_SMALL_INTENTS','BIG_PHASE_4_CONFIRM_BIG_SMALL_DEALS','BIG_PHASE_7_PREPARE_FAR_INTENT','SMALL_PHASE_2_PREPARE_SMALL_OLD_FAR_INTENTS','SMALL_PHASE_4_CONFIRM_SMALL_OLD_FAR_DEALS','SMALL_PHASE_7_CONFIRM_BIG_DEAL','SMALL_PHASE_9_APPLY_RESERVE','INITIAL_COMMITTED'),
   'EXACTLY_ONCE':lambda:not o.get('alreadyConsumed') or D(o.get('roundedSmallReserveAdd',o.get('reserveAdd',0)))==0,
  }
  return None if name not in rules else bool(rules[name]())
 except (KeyError,TypeError,StopIteration):return False
def self_test():
 c=[check('UNKNOWN',{}, {}) is None,check('RESERVE_ACCUMULATION',{}, {'output':{'reserveAfter':'2','reserveBefore':'1','alreadyConsumed':False,'reserveAdd':'1','rawReserveAdd':'1'}}) is True]
 print('\n'.join(f'R4R1_INV_{i}={"PASS" if x else "FAIL"}' for i,x in enumerate(c,1)));print(f'INVARIANTS_R4_R1_SELF_TESTS={sum(c)}/{len(c)}');return all(c)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
