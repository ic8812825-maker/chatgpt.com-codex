#ifndef __IFSM_MQH__
#define __IFSM_MQH__

#include "..\\core\\CALContext.mqh"

class IFSM
{
public:
   virtual ENUM_ALE_STATE Current() const=0;
   virtual bool Transition(const ENUM_ALE_STATE next_state)=0;
};

#endif
