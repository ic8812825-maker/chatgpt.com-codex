#ifndef __CALRISKCONFIG_MQH__
#define __CALRISKCONFIG_MQH__

// CALRiskConfig
// Centralized SAFE/risk thresholds and runtime safety invariants for ALE dual-flow runtime.
// Usage example:
//   CALRiskConfig cfg;
//   cfg.SetDefaults();
//   cfg.MAX_DRAWDOWN=0.25;
//   cfg.MAX_POSITIONS=128;
//   cfg.MIN_LOT=0.01;
//   cfg.ENABLE_STRICT_RUNTIME_CHECKS=true;
//   cfg.SyncAliases();
//   engine.SetRiskConfig(cfg);
struct CALRiskConfig
{
   // Canonical uppercase fields requested by spec.
   double MAX_DRAWDOWN;
   double STRESS_LIMIT;
   double DD_PROB_LIMIT;
   double GLOBAL_MARGIN_LIMIT;
   double GLOBAL_DD_SUM_LIMIT;

   double SAFE_ALPHA;
   double SAFE_BETA;
   double SAFE_GAMMA;
   double SAFE_K;

   // Runtime invariant controls (P0).
   int MAX_POSITIONS;
   double MIN_LOT;
   bool ENABLE_STRICT_RUNTIME_CHECKS;

   // Backward-compatible aliases used by existing modules/tests.
   double dd_max;
   double stress_limit;
   double dd_prob_limit;
   double global_margin_limit;
   double global_dd_sum_limit;

   double safe_alpha;
   double safe_beta;
   double safe_gamma;
   double safe_k;

   int max_positions;
   double min_lot;
   bool enable_strict_runtime_checks;

   void SetDefaults()
   {
      MAX_DRAWDOWN=0.30;
      STRESS_LIMIT=1.0;
      DD_PROB_LIMIT=0.80;
      GLOBAL_MARGIN_LIMIT=2.0;
      GLOBAL_DD_SUM_LIMIT=0.60;

      SAFE_ALPHA=1.0;
      SAFE_BETA=1.0;
      SAFE_GAMMA=1.0;
      SAFE_K=1.0;

      MAX_POSITIONS=256;
      MIN_LOT=0.01;
      ENABLE_STRICT_RUNTIME_CHECKS=true;

      SyncAliases();
   }

   // Keep upper/lower naming in sync after runtime edits.
   void SyncAliases()
   {
      dd_max=MAX_DRAWDOWN;
      stress_limit=STRESS_LIMIT;
      dd_prob_limit=DD_PROB_LIMIT;
      global_margin_limit=GLOBAL_MARGIN_LIMIT;
      global_dd_sum_limit=GLOBAL_DD_SUM_LIMIT;

      safe_alpha=SAFE_ALPHA;
      safe_beta=SAFE_BETA;
      safe_gamma=SAFE_GAMMA;
      safe_k=SAFE_K;

      max_positions=MAX_POSITIONS;
      min_lot=MIN_LOT;
      enable_strict_runtime_checks=ENABLE_STRICT_RUNTIME_CHECKS;
   }

   // Promote lowercase aliases to canonical uppercase fields.
   void SyncCanonical()
   {
      MAX_DRAWDOWN=dd_max;
      STRESS_LIMIT=stress_limit;
      DD_PROB_LIMIT=dd_prob_limit;
      GLOBAL_MARGIN_LIMIT=global_margin_limit;
      GLOBAL_DD_SUM_LIMIT=global_dd_sum_limit;

      SAFE_ALPHA=safe_alpha;
      SAFE_BETA=safe_beta;
      SAFE_GAMMA=safe_gamma;
      SAFE_K=safe_k;

      MAX_POSITIONS=max_positions;
      MIN_LOT=min_lot;
      ENABLE_STRICT_RUNTIME_CHECKS=enable_strict_runtime_checks;
   }

   CALRiskConfig(){ SetDefaults(); }
};

#endif
