"""Полностью независимый Decimal reference oracle без actual-oracle imports."""
from dataclasses import dataclass
from decimal import Decimal as D
@dataclass(frozen=True)
class ReferenceBroker:
 bid:D;ask:D;tick_size:D;tick_value_profit:D;tick_value_loss:D
@dataclass(frozen=True)
class ReferenceScenario:
 side:str='BUY';close_price:D=D('1.1010');actual_volume:D=D('.10');commission:D=D('-2');swap:D=D('-3');fee:D=D('-1');allocation:D=D('4');residual:D=D('0');reconciled:bool=True;preview:bool=False;slippage:D=D('0')
REFERENCE_SCENARIO=ReferenceScenario()
def reference_projected_money(s:ReferenceScenario,b:ReferenceBroker,open_price:D)->D:
 close=b.bid-s.slippage if s.side=='BUY' else b.ask+s.slippage
 movement=close-open_price if s.side=='BUY' else open_price-close;ticks=movement/b.tick_size
 return ticks*(b.tick_value_profit if ticks>=0 else b.tick_value_loss)*s.actual_volume
def calculate_reference(s:ReferenceScenario,b:ReferenceBroker,open_price:D):
 movement=((s.close_price-open_price) if s.side=='BUY' else (open_price-s.close_price))/b.tick_size
 realized=movement*(b.tick_value_profit if movement>=0 else b.tick_value_loss)*s.actual_volume+s.swap+s.commission+s.fee
 return {'projected':reference_projected_money(s,b,open_price),'realized':realized,'allocation':s.allocation,'residual':s.residual,'reconciled':s.reconciled,'preview':s.preview}
