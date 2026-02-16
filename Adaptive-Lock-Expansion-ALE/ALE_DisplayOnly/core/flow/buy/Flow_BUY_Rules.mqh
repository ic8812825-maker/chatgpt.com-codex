#pragma once

bool Flow_BUY_CheckRules(const FlowSnapshot &snapshot)
  {
   return(snapshot.metric>=0.0);
  }
