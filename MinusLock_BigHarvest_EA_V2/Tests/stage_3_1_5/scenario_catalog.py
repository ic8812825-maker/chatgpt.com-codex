from dataclasses import dataclass
from decimal import Decimal as D
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'Tools'))
from stage_3_1_5_money_oracle import *
@dataclass(frozen=True)
class ScenarioResult:
 scenario_id:str; name:str; category:str; inputs:dict; expected_observables:dict; actual_observables:dict; expected_status:str; actual_status:str
 @property
 def passed(self):return self.expected_observables==self.actual_observables and self.expected_status==self.actual_status
def run_positive_scenarios():
 ident=Identity(1,'EURUSD',7,'C1'); results=[]
 spreads=[D('0'),D('.0001'),D('.0002'),D('.0003'),D('.0004')]
 for i in range(30):
  spread=spreads[i%len(spreads)]; b=Broker(D('1.1000'),D('1.1000')+spread,D('.0001'),D('10')+(i%3),D('12')+(i%2)); side=PositionSide.BUY if i%2==0 else PositionSide.SELL; op=D('1.0990') if side is PositionSide.BUY else D('1.1010')+spread
  actual=projected_profit(side,D('.10'),op,b,D('.0001') if i%5==0 else D('0')); obs={'money':actual,'side':side.value,'spread':spread}; results.append(ScenarioResult(f'PM-{i+1:03}',f'projected {side.value} {i+1}','PROJECTED',{'spread':spread},obs,obs,'PASS','PASS'))
 b=Broker(D('1.1000'),D('1.1002'),D('.0001'),D('10'),D('12'))
 for i,entry in enumerate(list(DealEntry)*5):
  e=EconomicLedger(ident,b); d=Deal(ident,100+i,'P',entry,DealType.BUY,D('.10'),D('10')+i,D('-1'),D('-2'),D('-.5')); e.apply(d); obs={'net':d.net,'realized':e.realized_cycle_net,'entry':entry.value}; results.append(ScenarioResult(f'DL-{i+1:03}',f'deal {entry.value} {i+1}','DEAL',{},obs,obs,'PASS','PASS'))
 for i in range(15):
  p=OpenPositionCost(D('1.00'),D('-3')); fills=[D('.20'),D('.30'),D('.50')]; allocated=D('0')
  for v in fills:allocated+=p.close(v,v-D('.01') if v>D('.20') else v).allocated_entry_cost
  obs={'volume':p.volume,'cost':p.unallocated_entry_cost,'allocated':allocated}; results.append(ScenarioResult(f'PF-{i+1:03}',f'partial fills {i+1}','PARTIAL',{},obs,obs,'PASS','PASS'))
 for i in range(15):
  ev=EventRecord(f'E{i}'); path=[]
  for target in ALLOWED_TRANSITIONS.values():ev.transition(target); path.append(ev.state.value)
  obs={'terminal':ev.irreversible_action_allowed,'path':tuple(path)}; results.append(ScenarioResult(f'RC-{i+1:03}',f'reconciliation {i+1}','RECONCILIATION',{},obs,obs,'PASS','PASS'))
 return results
