#pragma once

#include "SystemState.mqh"
#include "DualState.mqh"

SystemState StateFactory_CreateSystemState()
  {
   SystemState state;
   return(state);
  }

DualState StateFactory_CreateDualState()
  {
   DualState state;
   return(state);
  }
