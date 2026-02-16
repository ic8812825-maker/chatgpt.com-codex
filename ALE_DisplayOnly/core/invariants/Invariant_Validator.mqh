#ifndef ALE_DO_CORE_INVARIANTS_INVARIANT_VALIDATOR_MQH_INCLUDED
#define ALE_DO_CORE_INVARIANTS_INVARIANT_VALIDATOR_MQH_INCLUDED

#include "Invariant_Geometry.mqh"
#include "Invariant_Margin.mqh"
#include "Invariant_Ordering.mqh"

bool Invariant_ValidateAll()
  {
   return(Invariant_CheckGeometry() && Invariant_CheckMargin() && Invariant_CheckOrdering());
  }

#endif // ALE_DO_CORE_INVARIANTS_INVARIANT_VALIDATOR_MQH_INCLUDED
