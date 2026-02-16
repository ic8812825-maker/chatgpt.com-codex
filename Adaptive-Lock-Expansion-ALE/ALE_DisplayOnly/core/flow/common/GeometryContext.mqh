#ifndef ALE_DO_CORE_FLOW_COMMON_GEOMETRYCONTEXT_MQH_INCLUDED
#define ALE_DO_CORE_FLOW_COMMON_GEOMETRYCONTEXT_MQH_INCLUDED

class GeometryContext
  {
public:
   double anchor_price;
   double market_price;

            GeometryContext() : anchor_price(0.0), market_price(0.0) {}
  };

#endif // ALE_DO_CORE_FLOW_COMMON_GEOMETRYCONTEXT_MQH_INCLUDED
