#ifndef HSBI_MONEY_STATE_MQH
#define HSBI_MONEY_STATE_MQH
#include "HSBI_MoneyTypes.mqh"
struct HSBI_MoneyState{double realizedCycleNet;double finalReserve;double partialFarBudget;double transitionBudget;double carry;double residual;ulong revision;bool valid;};
bool HSBI_ValidateMoneyState(const HSBI_MoneyState &s){return s.finalReserve>=0&&s.partialFarBudget>=0&&s.transitionBudget>=0&&s.carry>=0&&s.residual>=0;}
#endif