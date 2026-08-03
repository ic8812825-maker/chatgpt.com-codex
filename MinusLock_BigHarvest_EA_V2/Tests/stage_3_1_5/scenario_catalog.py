from dataclasses import dataclass
from decimal import Decimal as D
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'Tools'))
from stage_3_1_5_money_oracle import *
@dataclass(frozen=True)
class ScenarioResult:
 scenario_id:str;name:str;category:str;inputs:dict;expected:dict;actual:dict;expected_status:str;actual_status:str;invariants:tuple[str,...]
 @property
 def passed(self):return self.expected==self.actual and self.expected_status==self.actual_status
def run_positive_scenarios():
 out=[];ident=Identity(1,'EURUSD',7,'C1')
 for i in range(50):
  side=PositionSide.BUY if i%2==0 else PositionSide.SELL;spread=D(i%5)*D('.0001');b=Broker(D('1.1000'),D('1.1000')+spread,D('.0001'),D(10+i%4),D(12+i%3));lot=D('.01')*(1+i%10);ticks=D(2+i);op=b.bid-ticks*b.tick_size if side is PositionSide.BUY else b.ask+ticks*b.tick_size;expected=ticks*b.tv_profit*lot;actual=projected_profit(side,lot,op,b);out.append(ScenarioResult(f'PM-{i:03}',f'{side.value} money {i}','MONEY',{'ticks':ticks,'lot':lot},{'money':expected},{'money':actual},'PASS','PASS',('SIDE','GRID','MONEY')))
 b=Broker(D('1'),D('1'),D('.01'),D('1'),D('1'))
 for i in range(20):
  entry=(DealEntry.OUT,DealEntry.INOUT,DealEntry.OUT_BY)[i%3];e=EconomicLedger(ident,b);d=Deal(ident,100+i,'P',entry,DealType.BUY,D('.01'),D(i+1),D('-1'),D('-2'),D('-.5'));e.apply(d);expected=D(i+1)-D('3.5');out.append(ScenarioResult(f'DL-{i:03}',f'deal net {i}','DEAL',{'entry':entry.value},{'realized':expected},{'realized':e.realized_cycle_net},'PASS','PASS',('DEAL_NET','ENTRY')))
 for i in range(10):
  cost=OpenPositionCost(D('1'),D('-10'));v=D(i+1)/D('20');r=cost.close(v,v,1000+i);expected=D('-10')*v;out.append(ScenarioResult(f'PF-{i:03}',f'partial {v}','PARTIAL',{'actual':v},{'allocated':expected,'remaining':D('1')-v},{'allocated':r.allocated_entry_cost,'remaining':r.volume_after},'PASS','PASS',('ACTUAL_FILL','COST')))
 for i,state in enumerate(ReconciliationState):
  k=EventKey(1,'X',2,'C','E',i,state.value,'P',i+1,AllocationType.RESIDUAL);ev=EventRecord(k,state,i);out.append(ScenarioResult(f'RC-{i:03}',f'state {state.value}','STATE',{}, {'state':state.value,'revision':i},{'state':ev.state.value,'revision':ev.revision},'PASS','PASS',('STATE',)))
 return out
