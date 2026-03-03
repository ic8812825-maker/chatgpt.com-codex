#ifndef __CALPHASEDIAGRAM_MQH__
#define __CALPHASEDIAGRAM_MQH__

class CALPhaseDiagram
{
public:
   bool IsStable(const double mu,const double mu_crit) const { return mu<mu_crit; }
};

#endif
