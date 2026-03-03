#ifndef __CALGBMMODEL_MQH__
#define __CALGBMMODEL_MQH__

class CALGBMModel
{
public:
   double Forward(const double s0,const double mu,const double sigma,const double t) const
   { return s0*MathExp((mu-0.5*sigma*sigma)*t); }
};

#endif
