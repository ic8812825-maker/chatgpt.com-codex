#ifndef ALE_DO_CORE_FLOW_COMMON_MARGINCONTEXT_MQH_INCLUDED
#define ALE_DO_CORE_FLOW_COMMON_MARGINCONTEXT_MQH_INCLUDED

class MarginContext
  {
public:
   double free_margin;
   double leverage;

            MarginContext() : free_margin(0.0), leverage(0.0) {}
  };

#endif // ALE_DO_CORE_FLOW_COMMON_MARGINCONTEXT_MQH_INCLUDED
