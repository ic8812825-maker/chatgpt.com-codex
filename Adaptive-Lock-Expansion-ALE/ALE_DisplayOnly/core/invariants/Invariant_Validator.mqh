#ifndef __ALE_DisplayOnly_CORE_INVARIANTS_INVARIANT_VALIDATOR_MQH__
#define __ALE_DisplayOnly_CORE_INVARIANTS_INVARIANT_VALIDATOR_MQH__

#include "Invariant_Geometry.mqh"
#include "Invariant_Margin.mqh"
#include "Invariant_Ordering.mqh"

bool Invariant_ValidateAll()
  {
   return(Invariant_CheckGeometry() && Invariant_CheckMargin() && Invariant_CheckOrdering());
  }

#endif // __ALE_DisplayOnly_CORE_INVARIANTS_INVARIANT_VALIDATOR_MQH__
