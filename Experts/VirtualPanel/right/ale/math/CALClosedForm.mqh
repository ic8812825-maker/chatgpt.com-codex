#ifndef __CALCLOSEDFORM_MQH__
#define __CALCLOSEDFORM_MQH__

class CALClosedForm
{
public:
   double ExpectedPnL(const double p_return,const double gain,const double loss) const
   { return p_return*gain-(1.0-p_return)*loss; }
};

#endif
