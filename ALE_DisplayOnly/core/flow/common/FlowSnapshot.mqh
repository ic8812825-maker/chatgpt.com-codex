#pragma once

// Immutable DTO: only plain data, no methods/calculations/references.
struct FlowSnapshot
  {
   double metric;
   long version;
  };
