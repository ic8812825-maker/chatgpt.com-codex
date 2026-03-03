#ifndef __CALEXPECTATIONMODEL_MQH__
#define __CALEXPECTATIONMODEL_MQH__

#include "..\math\CALClosedForm.mqh"

class CALExpectationModel
{
private:
   CALClosedForm m_closed;
public:
   double ForBuy(const double p_return,const double gain,const double loss) const { return m_closed.ExpectedPnL(p_return,gain,loss); }
   double ForSell(const double p_return,const double gain,const double loss) const { return m_closed.ExpectedPnL(p_return,gain,loss); }
};

#endif
