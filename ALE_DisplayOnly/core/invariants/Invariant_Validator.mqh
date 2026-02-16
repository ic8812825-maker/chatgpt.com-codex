#pragma once

#include "Invariant_Geometry.mqh"
#include "Invariant_Margin.mqh"
#include "Invariant_Ordering.mqh"

bool Invariant_ValidateAll()
  {
   return(Invariant_CheckGeometry() && Invariant_CheckMargin() && Invariant_CheckOrdering());
  }
