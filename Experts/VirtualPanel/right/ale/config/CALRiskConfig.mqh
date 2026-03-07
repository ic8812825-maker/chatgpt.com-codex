#ifndef __CALRISKCONFIG_MQH__
#define __CALRISKCONFIG_MQH__

struct CALRiskConfig
{
   double dd_max;
   double stress_limit;
   double dd_prob_limit;
   double global_margin_limit;
   double global_dd_sum_limit;

   double safe_alpha;
   double safe_beta;
   double safe_gamma;
   double safe_k;

   void SetDefaults()
   {
      dd_max=0.30;
      stress_limit=1.0;
      dd_prob_limit=0.80;
      global_margin_limit=2.0;
      global_dd_sum_limit=0.60;

      safe_alpha=1.0;
      safe_beta=1.0;
      safe_gamma=1.0;
      safe_k=1.0;
   }

   CALRiskConfig(){ SetDefaults(); }
};

#endif
