#ifndef ALE_DO_CORE_INVARIANTS_INVARIANT_VALIDATOR_MQH_INCLUDED
#define ALE_DO_CORE_INVARIANTS_INVARIANT_VALIDATOR_MQH_INCLUDED

#include "Invariant_Geometry.mqh"
#include "Invariant_Margin.mqh"
#include "Invariant_Ordering.mqh"

class CInvariantValidator
  {
public:
   static bool ValidateAll()
     {
      return(CInvariantGeometry::Check() && CInvariantMargin::Check() && CInvariantOrdering::Check());
     }
  };

#endif // ALE_DO_CORE_INVARIANTS_INVARIANT_VALIDATOR_MQH_INCLUDED
