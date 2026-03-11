#ifndef __CALRISKCONFIG_MQH__
#define __CALRISKCONFIG_MQH__

struct CALRiskConfig
{
   double dd_max;
   double stress_limit;
   double dd_prob_limit;
   double global_margin_limit;

   double alpha;
   double beta;
   double gamma;
   double k;

   double sigma;
   double dt;

   double initial_equity;
   double growth_g;

   double min_margin_level;
   double atr_limit;
   double spread_limit;
   double p_safe;

   double risk_fraction;
   double grid_step_R;
   double harvest_target;
   double cluster_target;

   void SetDefaults()
   {
      dd_max=0.30;
      stress_limit=1.0;
      dd_prob_limit=0.95;
      global_margin_limit=2.0;

      alpha=1.0;
      beta=1.0;
      gamma=1.0;
      k=1.0;

      sigma=0.20;
      dt=1.0;

      initial_equity=10000.0;
      growth_g=0.8;

      min_margin_level=0.20;
      atr_limit=0.03;
      spread_limit=0.005;
      p_safe=0.10;

      risk_fraction=0.02;
      grid_step_R=0.01;
      harvest_target=5.0;
      cluster_target=1.0;
   }

   bool IsValid() const
   {
      if(dd_max<=0.0) return false;
      if(stress_limit<=0.0) return false;
      if(dd_prob_limit<0.0 || dd_prob_limit>1.0) return false;
      if(global_margin_limit<=0.0) return false;
      if(sigma<=0.0 || dt<=0.0) return false;
      if(initial_equity<=0.0) return false;
      if(growth_g<=0.0) return false;
      if(min_margin_level<=0.0) return false;
      if(atr_limit<=0.0 || spread_limit<=0.0) return false;
      if(p_safe<0.0 || p_safe>1.0) return false;
      if(risk_fraction<=0.0 || risk_fraction>0.10) return false;
      if(grid_step_R<=0.0) return false;

      const double stability=k*growth_g;
      if(stability<=0.0 || stability>=1.0) return false;
      return true;
   }

   CALRiskConfig(){ SetDefaults(); }
};

#endif
