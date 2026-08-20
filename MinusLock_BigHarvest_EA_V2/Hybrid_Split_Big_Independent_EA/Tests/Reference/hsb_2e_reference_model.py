#!/usr/bin/env python3
"""Pure Decimal reference semantics for PREP-R3; never dispatches trades."""
from decimal import Decimal,InvalidOperation,ROUND_FLOOR,ROUND_CEILING
import argparse,hashlib,json
D=lambda x:Decimal(str(x))
def result(status='PASS',reason='OK',**output):return {'status':status,'reason':reason,'output':{k:str(v) if isinstance(v,Decimal) else v for k,v in output.items()}}
def finite(*xs):
 try:return all(D(x).is_finite() for x in xs)
 except (InvalidOperation,ValueError):return False
def identity_validation(x):
 required=('accountLogin','symbol','magic','cycleId')
 return result('PASS','OK',owned=True) if all(x.get(k) not in (None,'',0) for k in required) and (not x.get('positionSpecific') or x.get('ticket',0)>0) else result('REJECT','IDENTITY',owned=False)
def broker_snapshot_validation(x):return result('PASS','OK',fresh=True) if x.get('version',0)>0 and x.get('timestamp',0)>=x.get('minimumTimestamp',0) and finite(x.get('bid'),x.get('ask')) and D(x['ask'])>=D(x['bid']) else result('REJECT','STALE_SNAPSHOT',fresh=False)
def price_grid_normalization(x):
 if not finite(x.get('price'),x.get('tickSize')) or D(x['tickSize'])<=0:return result('REJECT','INVALID_GEOMETRY')
 p,t=D(x['price']),D(x['tickSize']);mode=ROUND_FLOOR if x.get('round')=='DOWN' else ROUND_CEILING;return result(price=(p/t).to_integral_value(rounding=mode)*t)
def volume_grid_normalization(x):
 if not finite(x.get('volume'),x.get('step'),x.get('minimum'),x.get('maximum')) or D(x['step'])<=0 or D(x['volume'])<0:return result('REJECT','INVALID_VOLUME')
 v=(D(x['volume'])/D(x['step'])).to_integral_value(rounding=ROUND_FLOOR)*D(x['step']);return result('PASS','OK',volume=v) if v==0 or D(x['minimum'])<=v<=D(x['maximum']) else result('REJECT','INVALID_VOLUME',volume=v)
def directional_close_price(x):return result(price=D(x['bid']) if x.get('direction')=='BUY' else D(x['ask'])) if x.get('direction') in ('BUY','SELL') and finite(x.get('bid'),x.get('ask')) else result('REJECT','INVALID_GEOMETRY')
def realized_deal_money(x):
 deals=x.get('deals',[]);seen=set();grossProfit=grossLoss=commission=swap=fee=D(0)
 for d in deals:
  if d.get('id') in seen:return result('REJECT','TRANSACTION_CONFLICT')
  seen.add(d.get('id'));p=D(d['profit']);grossProfit+=max(p,D(0));grossLoss+=min(p,D(0));commission+=D(d.get('commission',0));swap+=D(d.get('swap',0));fee+=D(d.get('fee',0))
 return result(grossProfit=grossProfit,grossLoss=grossLoss,commission=commission,swap=swap,fee=fee,netRealized=grossProfit+grossLoss+commission+swap+fee)
def unrealized_far_loss(x):
 if not finite(x.get('openPrice'),x.get('closePrice'),x.get('volume'),x.get('moneyPerPriceLot')):return result('REJECT','INVALID_GEOMETRY')
 sign=D(1) if x.get('direction')=='BUY' else D(-1);pnl=(D(x['closePrice'])-D(x['openPrice']))*sign*D(x['volume'])*D(x['moneyPerPriceLot']);return result(unrealized=pnl,farLoss=max(-pnl,D(0)))
def recovery_pl(x):return result(recoveryPL=D(x['actualRealized'])+D(x['reserve'])-D(x['farLoss'])) if finite(x.get('actualRealized'),x.get('reserve'),x.get('farLoss')) else result('REJECT','INVALID_GEOMETRY')
def reserve_coverage(x):return result(coverage=D(x['bigNet'])+D(x['smallNet'])+D(x['reserve'])-D(x['farLoss']))
def close_far_budget(x):return result(budget=max(D(0),D(x['bigNet'])+D(x['smallNet'])))
def partial_far_volume(x):
 if D(x.get('reserveUsed',0))!=0:return result('REJECT','FINAL_CLOSE_BLOCKED')
 raw=D(x['budget'])/D(x['lossPerLot']) if D(x['lossPerLot'])>0 else D(0);return volume_grid_normalization({'volume':min(raw,D(x['farVolume'])),'step':x['step'],'minimum':x['minimum'],'maximum':x['farVolume']})
def reserve_addition(x):
 if x.get('allocationKey') in set(x.get('consumedKeys',[])):return result('NO_OP','RETRY',reserve=D(x['reserve']))
 return result(reserve=D(x['reserve'])+D(x['addition']),allocationKey=x['allocationKey'])
def final_far_close_gate(x):
 ok=D(x['farLoss'])<=D(x['bigNet'])+D(x['smallNet'])+D(x['reserve']) and D(x['recoveryPL'])>0 and x.get('actualDeals') is True
 return result('PASS','OK',closeFar=ok) if ok else result('REJECT','FINAL_CLOSE_BLOCKED',closeFar=False)
def big_level_settlement(x):return result(bigClosed=D(x['bigVolume']),smallClosed=D(x['smallVolume']),confirmed=True) if x.get('bigConfirmed') and x.get('smallConfirmed') else result('UNAVAILABLE','PARTIAL_FILL',confirmed=False)
def small_reversal_settlement(x):
 oldBig,closed,newFar=D(x['oldBig']),D(x['closedBig']),D(x['newFar']);ok=oldBig==closed+newFar and newFar<D(x['oldFar']) and not x.get('dualTail') and x.get('persisted')
 return result('PASS','OK',newFar=newFar,closedBig=closed) if ok else result('REJECT','TRANSITION_LOSS')
def new_far_calculation(x):return result(newFar=D(x['bigRemaining'])) if D(x['bigRemaining'])<D(x['oldFar']) and D(x['bigRemaining'])>=0 else result('REJECT','TRANSITION_LOSS')
def future_small_projection(x):return result(projectedSmall=max(D(0),D(x['targetRecovery'])-D(x['reserve'])-D(x['bigProjected'])))
def reserve_catch_up(x):return result(catchUp=max(D(0),D(x['target'])-D(x['reserve'])))
def risk_margin_gate(x):return result('PASS','OK',allowed=True) if D(x['marginFree'])>=D(x['marginRequired']) and D(x['risk'])<=D(x['riskLimit']) else result('UNAVAILABLE','RISK',allowed=False)
def transition_loss(x):return result(loss=max(D(0),D(x['oldFarLoss'])-D(x['newFarLoss'])))
def restart_replay(x):
 if x.get('outcome')=='UNKNOWN':return result('ERROR','RECONCILIATION')
 return result('NO_OP','RETRY',actionId=x['actionId'],stateRevision=x['stateRevision']) if x.get('actionId') in x.get('committedActions',[]) else result('PASS','OK',actionId=x['actionId'],stateRevision=x['stateRevision'])
def exactly_once_allocation(x):
 if x['actionId'] in x.get('consumedActions',[]):return result('NO_OP','RETRY',allocated='0')
 return result(allocated=D(x['amount']),actionId=x['actionId'])
FUNCTIONS={k:v for k,v in globals().copy().items() if callable(v) and k in ('identity_validation','broker_snapshot_validation','price_grid_normalization','volume_grid_normalization','directional_close_price','realized_deal_money','unrealized_far_loss','recovery_pl','reserve_coverage','close_far_budget','partial_far_volume','reserve_addition','final_far_close_gate','big_level_settlement','small_reversal_settlement','new_far_calculation','future_small_projection','reserve_catch_up','risk_margin_gate','transition_loss','restart_replay','exactly_once_allocation')}
def execute(name,input_data):return FUNCTIONS[name](json.loads(json.dumps(input_data))) if name in FUNCTIONS else result('ERROR','UNKNOWN_FUNCTION')
def self_test():
 checks={'decimal':recovery_pl({'actualRealized':'10.10','reserve':'2.00','farLoss':'5.00'})['output']['recoveryPL']=='7.10','buy_bid':directional_close_price({'direction':'BUY','bid':'1.1','ask':'1.2'})['output']['price']=='1.1','sell_ask':directional_close_price({'direction':'SELL','bid':'1.1','ask':'1.2'})['output']['price']=='1.2','reserve_isolation':partial_far_volume({'reserveUsed':'1','budget':'5','lossPerLot':'10','farVolume':'1','step':'0.1','minimum':'0.1'})['status']=='REJECT','compression':new_far_calculation({'bigRemaining':'0.5','oldFar':'1'})['status']=='PASS','exactly_once':exactly_once_allocation({'actionId':1,'consumedActions':[1],'amount':'5'})['status']=='NO_OP'}
 print('\n'.join(f'RM_{k}={"PASS" if v else "FAIL"}' for k,v in checks.items()));print(f'REFERENCE_MODEL_SELF_TESTS={sum(checks.values())}/{len(checks)}');return all(checks.values())
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');a=p.parse_args();raise SystemExit(0 if a.self_test and self_test() else 1)
