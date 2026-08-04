"""Независимый immutable reference oracle; mutation-модули не импортируются."""
from dataclasses import dataclass
from decimal import Decimal as D
from stage_3_1_5_money_oracle import Broker,PositionSide,projected_profit
@dataclass(frozen=True)
class ReferenceScenario:
 side:PositionSide=PositionSide.BUY
 close_price:D=D('1.1010')
 actual_volume:D=D('.10')
 commission:D=D('-2')
 swap:D=D('-3')
 fee:D=D('-1')
 allocation:D=D('4')
 residual:D=D('0')
 reconciled:bool=True
 preview:bool=False
REFERENCE_SCENARIO=ReferenceScenario()
def calculate_reference(scenario:ReferenceScenario,broker:Broker,open_price:D):
 movement=((scenario.close_price-open_price) if scenario.side is PositionSide.BUY else (open_price-scenario.close_price))/broker.tick_size
 realized=movement*(broker.tv_profit if movement>=0 else broker.tv_loss)*scenario.actual_volume+scenario.swap+scenario.commission+scenario.fee
 return {'projected':projected_profit(scenario.side,scenario.actual_volume,open_price,broker),'realized':realized,'allocation':scenario.allocation,'residual':scenario.residual,'reconciled':scenario.reconciled,'preview':scenario.preview}
