#ifndef __BH_HYBRID_ROUNDING_MODEL_MQH__
#define __BH_HYBRID_ROUNDING_MODEL_MQH__

double NormalizeHybridCoreLot(double raw) { return NormalizeLotDown(raw); }
double NormalizeHybridTrendLot(double raw) { return NormalizeLotDown(raw); }
double NormalizeHybridSmallLot(double raw) { return NormalizeLotUp(raw); }
double NormalizeHybridNewFarLot(double raw) { return NormalizeLotDown(raw); }

#endif // __BH_HYBRID_ROUNDING_MODEL_MQH__
