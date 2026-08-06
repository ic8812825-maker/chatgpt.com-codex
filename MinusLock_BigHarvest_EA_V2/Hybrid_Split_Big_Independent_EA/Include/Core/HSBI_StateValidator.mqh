#ifndef HSBI_STATE_VALIDATOR_MQH
#define HSBI_STATE_VALIDATOR_MQH
#include "HSBI_StateMachine.mqh"
HSBI_ValidationResult HSBI_ValidateStateTopology(const HSBI_RecoveryContext &c){if(c.currentState==HSBI_STATE_CYCLE_CLOSED&&c.pendingActionId!=0)return HSBI_Result(false,HSBI_REASON_PENDING_ACTION,"HSBI-FSM-002","closed state has pending action");if(c.currentState==HSBI_STATE_FAR_ACTIVE&&c.far.role!=HSBI_ROLE_FAR)return HSBI_Result(false,HSBI_REASON_INVALID_STATE_TRANSITION,"HSBI-FSM-002","FAR_ACTIVE without FAR");return HSBI_Result(true,HSBI_REASON_OK,"HSBI-FSM-002","");}
bool HSBI_OutcomeCompletesAction(const HSBI_EventType e){return e==HSBI_EVENT_COMPLETED_FILL;}
#endif