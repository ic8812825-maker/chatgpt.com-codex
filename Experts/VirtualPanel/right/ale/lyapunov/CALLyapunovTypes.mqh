#ifndef __CALLYAPUNOVTYPES_MQH__
#define __CALLYAPUNOVTYPES_MQH__

struct CALLyapunovState
{
   double drawdown;
   double exposure;
   double margin_usage;
   double depth;
   double distance_to_be;
   double unrealized_loss;
   double pnl_contribution;
   double tail_effect;
};

struct CALLyapunovWeights
{
   double w_drawdown;
   double w_exposure;
   double w_margin;
   double w_depth;
   double w_distance;
   double w_loss;
   double w_tail;
   double w_pnl;

   void SetDefault()
   {
      w_drawdown=0.24;
      w_exposure=0.16;
      w_margin=0.16;
      w_depth=0.10;
      w_distance=0.10;
      w_loss=0.12;
      w_tail=0.07;
      w_pnl=0.05;
   }
};

#endif
