#pragma once

bool Flow_SELL_CheckRules(const FlowSnapshot &snapshot)
  {
   return(snapshot.metric<=0.0 || snapshot.metric>=0.0);
  }
