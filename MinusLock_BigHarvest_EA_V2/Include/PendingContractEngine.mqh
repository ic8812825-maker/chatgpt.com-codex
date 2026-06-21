#ifndef __BH_PENDINGCONTRACTENGINE_MQH__
#define __BH_PENDINGCONTRACTENGINE_MQH__

// V2.4.18 Pending State Contract Architecture.
// Pending State == fully prepared and validated Pending Context.

bool IsPendingContractState(EAState state)
{
   return (state == STATE_OPEN_NEW_BIG_PENDING ||
           state == STATE_OPEN_NEW_SMALL_PENDING ||
           state == STATE_CLOSE_BIG_PENDING ||
           state == STATE_CLOSE_SMALL_PENDING ||
           state == STATE_CLOSE_BIG_PART_PENDING ||
           state == STATE_CLOSE_OLD_FAR_PENDING ||
           state == STATE_CLOSE_NEW_FAR_PENDING ||
           state == STATE_REVERSE_LIMIT_CLOSE_PENDING ||
           state == STATE_MAX_LEVELS_FINAL_CLOSE_PENDING ||
           state == STATE_STOP_MAX_LEVELS_CLOSE_PENDING);
}

bool PendingActionMatchesState(EAState targetState, PendingActionType actionType)
{
   switch(targetState)
   {
      case STATE_OPEN_NEW_BIG_PENDING:
         return actionType == PENDING_OPEN_BIG;
      case STATE_OPEN_NEW_SMALL_PENDING:
         return actionType == PENDING_OPEN_SMALL;
      case STATE_CLOSE_BIG_PENDING:
         return actionType == PENDING_CLOSE_BIG_FULL;
      case STATE_CLOSE_SMALL_PENDING:
         return actionType == PENDING_CLOSE_SMALL_FULL;
      case STATE_CLOSE_BIG_PART_PENDING:
         return actionType == PENDING_CLOSE_BIG_PARTIAL;
      case STATE_CLOSE_OLD_FAR_PENDING:
         return actionType == PENDING_CLOSE_OLD_FAR_FULL;
      case STATE_CLOSE_NEW_FAR_PENDING:
         return (actionType == PENDING_CLOSE_FAR_FULL || actionType == PENDING_CLOSE_FAR_PARTIAL);
      case STATE_REVERSE_LIMIT_CLOSE_PENDING:
         return actionType == PENDING_CLOSE_FAR_FULL;
      case STATE_MAX_LEVELS_FINAL_CLOSE_PENDING:
         return actionType == PENDING_MAX_LEVELS_FINAL_CLOSE;
      case STATE_STOP_MAX_LEVELS_CLOSE_PENDING:
         return actionType == PENDING_STOP_MAX_LEVELS_CLOSE;
      default:
         return false;
   }
}

string PendingContractActionMatrix(EAState targetState)
{
   switch(targetState)
   {
      case STATE_OPEN_NEW_BIG_PENDING: return "STATE_OPEN_NEW_BIG_PENDING <-> PENDING_OPEN_BIG";
      case STATE_OPEN_NEW_SMALL_PENDING: return "STATE_OPEN_NEW_SMALL_PENDING <-> PENDING_OPEN_SMALL";
      case STATE_CLOSE_BIG_PENDING: return "STATE_CLOSE_BIG_PENDING <-> PENDING_CLOSE_BIG_FULL";
      case STATE_CLOSE_SMALL_PENDING: return "STATE_CLOSE_SMALL_PENDING <-> PENDING_CLOSE_SMALL_FULL";
      case STATE_CLOSE_BIG_PART_PENDING: return "STATE_CLOSE_BIG_PART_PENDING <-> PENDING_CLOSE_BIG_PARTIAL";
      case STATE_CLOSE_OLD_FAR_PENDING: return "STATE_CLOSE_OLD_FAR_PENDING <-> PENDING_CLOSE_OLD_FAR_FULL";
      case STATE_CLOSE_NEW_FAR_PENDING: return "STATE_CLOSE_NEW_FAR_PENDING <-> PENDING_CLOSE_FAR_FULL/PENDING_CLOSE_FAR_PARTIAL";
      case STATE_REVERSE_LIMIT_CLOSE_PENDING: return "STATE_REVERSE_LIMIT_CLOSE_PENDING <-> PENDING_CLOSE_FAR_FULL";
      case STATE_MAX_LEVELS_FINAL_CLOSE_PENDING: return "STATE_MAX_LEVELS_FINAL_CLOSE_PENDING <-> PENDING_MAX_LEVELS_FINAL_CLOSE";
      case STATE_STOP_MAX_LEVELS_CLOSE_PENDING: return "STATE_STOP_MAX_LEVELS_CLOSE_PENDING <-> PENDING_STOP_MAX_LEVELS_CLOSE";
      default: return "STATE_ACTION_MATRIX_UNKNOWN";
   }
}

bool ValidatePendingContract(EAState targetState)
{
   if(!IsPendingContractState(targetState))
      return true;

   bool ok = true;
   if(Ctx.pendingActionType == PENDING_NONE || Ctx.pendingOperation == "" || Ctx.pendingOperationStartTime <= 0 || Ctx.pendingNextState == STATE_IDLE)
   {
      LogError(StringFormat("PENDING_CONTRACT_MISSING TargetState=%s pendingActionType=%d pendingOperation=%s pendingNextState=%s pendingOperationStartTime=%I64d",
                            StateToString(targetState),
                            (int)Ctx.pendingActionType,
                            Ctx.pendingOperation,
                            StateToString(Ctx.pendingNextState),
                            (long)Ctx.pendingOperationStartTime));
      ok = false;
   }

   if(!PendingActionMatchesState(targetState, Ctx.pendingActionType))
   {
      LogError(StringFormat("STATE_ACTION_MISMATCH TargetState=%s Action=%d Matrix=%s", StateToString(targetState), (int)Ctx.pendingActionType, PendingContractActionMatrix(targetState)));
      ok = false;
   }

   bool openState = (targetState == STATE_OPEN_NEW_BIG_PENDING || targetState == STATE_OPEN_NEW_SMALL_PENDING);
   if(openState)
   {
      if(Ctx.pendingLot <= VolumeMismatchToleranceLots || Ctx.pendingDirection == DIR_NONE || Ctx.pendingComment == "")
      {
         LogError(StringFormat("PENDING_CONTRACT_INVALID TargetState=%s Action=%d Lot=%.2f Direction=%s Comment=%s", StateToString(targetState), (int)Ctx.pendingActionType, Ctx.pendingLot, DirectionToString(Ctx.pendingDirection), Ctx.pendingComment));
         ok = false;
      }
   }
   else
   {
      if(Ctx.pendingTicket == 0 || Ctx.pendingLot <= VolumeMismatchToleranceLots)
      {
         LogError(StringFormat("PENDING_CONTRACT_INVALID TargetState=%s Action=%d Ticket=%I64u Lot=%.2f", StateToString(targetState), (int)Ctx.pendingActionType, Ctx.pendingTicket, Ctx.pendingLot));
         ok = false;
      }

      if((targetState == STATE_CLOSE_BIG_PENDING || targetState == STATE_CLOSE_BIG_PART_PENDING) && Ctx.pendingTicket != Ctx.bigTicket)
      {
         LogError(StringFormat("PENDING_CONTRACT_INVALID TargetState=%s ticket must equal Big Ticket=%I64u PendingTicket=%I64u", StateToString(targetState), Ctx.bigTicket, Ctx.pendingTicket));
         ok = false;
      }
      if(targetState == STATE_CLOSE_SMALL_PENDING && Ctx.pendingTicket != Ctx.smallTicket)
      {
         LogError(StringFormat("PENDING_CONTRACT_INVALID TargetState=%s ticket must equal Small Ticket=%I64u PendingTicket=%I64u", StateToString(targetState), Ctx.smallTicket, Ctx.pendingTicket));
         ok = false;
      }
      if((targetState == STATE_CLOSE_NEW_FAR_PENDING || targetState == STATE_CLOSE_OLD_FAR_PENDING || targetState == STATE_REVERSE_LIMIT_CLOSE_PENDING || targetState == STATE_MAX_LEVELS_FINAL_CLOSE_PENDING || targetState == STATE_STOP_MAX_LEVELS_CLOSE_PENDING) && Ctx.pendingTicket != Ctx.farTicket)
      {
         LogError(StringFormat("PENDING_CONTRACT_INVALID TargetState=%s ticket must equal Far Ticket=%I64u PendingTicket=%I64u", StateToString(targetState), Ctx.farTicket, Ctx.pendingTicket));
         ok = false;
      }
   }

   if(ok)
      LogInfo(StringFormat("PENDING_CONTRACT_VALID TargetState=%s Matrix=%s Action=%d Ticket=%I64u Lot=%.2f Direction=%s Comment=%s NextState=%s",
                           StateToString(targetState),
                           PendingContractActionMatrix(targetState),
                           (int)Ctx.pendingActionType,
                           Ctx.pendingTicket,
                           Ctx.pendingLot,
                           DirectionToString(Ctx.pendingDirection),
                           Ctx.pendingComment,
                           StateToString(Ctx.pendingNextState)));
   else
      LogError(StringFormat("PENDING_CONTRACT_INVALID TargetState=%s Matrix=%s", StateToString(targetState), PendingContractActionMatrix(targetState)));

   return ok;
}

bool ValidatePendingStateContract(EAState targetState)
{
   if(!ValidatePendingContract(targetState))
   {
      State = STATE_INTEGRITY_ERROR;
      Ctx.lastError = "INVALID_PENDING_CONTRACT";
      SaveState();
      return false;
   }
   return true;
}

void InitializePendingContract(PendingActionType actionType,
                               string operation,
                               EAState pendingState,
                               ulong ticket,
                               double lot,
                               Direction direction,
                               string comment,
                               EAState nextState)
{
   Ctx.pendingActionType = actionType;
   Ctx.pendingOperation = operation;
   Ctx.pendingNextState = nextState;
   Ctx.pendingTicket = ticket;
   Ctx.pendingLot = lot;
   Ctx.pendingComment = comment;
   Ctx.pendingDirection = direction;
   Ctx.pendingOperationStartTime = TimeCurrent();
   Ctx.retryTicket = ticket;
   Ctx.retryLot = lot;
   Ctx.retryAttempts = 0;
   Ctx.lastRetryState = pendingState;
   Ctx.lastRetryLogTime = 0;
   LogInfo(StringFormat("PENDING_CONTRACT_CREATED TargetState=%s Matrix=%s Action=%d Operation=%s Ticket=%I64u Lot=%.2f Direction=%s Comment=%s NextState=%s",
                        StateToString(pendingState),
                        PendingContractActionMatrix(pendingState),
                        (int)actionType,
                        operation,
                        ticket,
                        lot,
                        DirectionToString(direction),
                        comment,
                        StateToString(nextState)));
   SaveState();
}

bool PreparePendingOpenBigContext()
{
   double lot = CalcBigLot(Ctx.farLot);
   Direction direction = OppositeDirection(Ctx.farDirection);
   string comment = LevelComment("BIG", Ctx.harvestLevel + 1);
   InitializePendingContract(PENDING_OPEN_BIG, "OPEN_NEW_BIG", STATE_OPEN_NEW_BIG_PENDING, 0, lot, direction, comment, STATE_OPEN_NEW_SMALL_PENDING);
   return ValidatePendingContract(STATE_OPEN_NEW_BIG_PENDING);
}

bool PreparePendingOpenSmallContext()
{
   double lot = CalcSmallLot(Ctx.bigLot);
   Direction direction = Ctx.farDirection;
   string comment = LevelComment("SMALL", Ctx.harvestLevel + 1);
   InitializePendingContract(PENDING_OPEN_SMALL, "OPEN_NEW_SMALL", STATE_OPEN_NEW_SMALL_PENDING, 0, lot, direction, comment, STATE_BIG_SMALL_OPENED);
   return ValidatePendingContract(STATE_OPEN_NEW_SMALL_PENDING);
}

bool PreparePendingCloseBigContext()
{
   InitializePendingContract(PENDING_CLOSE_BIG_FULL, "CLOSE_BIG", STATE_CLOSE_BIG_PENDING, Ctx.bigTicket, Ctx.bigLot, Ctx.bigDirection, "RETRY_CLOSE_BIG", STATE_BIG_HARVEST_CLOSE_SMALL);
   return ValidatePendingContract(STATE_CLOSE_BIG_PENDING);
}

bool PreparePendingCloseSmallContext()
{
   InitializePendingContract(PENDING_CLOSE_SMALL_FULL, "CLOSE_SMALL", STATE_CLOSE_SMALL_PENDING, Ctx.smallTicket, Ctx.smallLot, Ctx.smallDirection, "RETRY_CLOSE_SMALL", STATE_BIG_HARVEST_CALC_NET);
   return ValidatePendingContract(STATE_CLOSE_SMALL_PENDING);
}

bool PreparePendingCloseFarContext()
{
   InitializePendingContract(PENDING_CLOSE_FAR_FULL, "CLOSE_FAR", STATE_CLOSE_NEW_FAR_PENDING, Ctx.farTicket, Ctx.farLot, Ctx.farDirection, "RETRY_CLOSE_FAR", STATE_CLOSED_PROFIT);
   return ValidatePendingContract(STATE_CLOSE_NEW_FAR_PENDING);
}

bool PreparePendingFinalCloseContext()
{
   InitializePendingContract(PENDING_CLOSE_FAR_FULL, "FINAL_CLOSE_NEW_FAR", STATE_CLOSE_NEW_FAR_PENDING, Ctx.farTicket, Ctx.farLot, Ctx.farDirection, "RETRY_FINAL_CLOSE", STATE_CLOSED_PROFIT);
   return ValidatePendingContract(STATE_CLOSE_NEW_FAR_PENDING);
}

#endif // __BH_PENDINGCONTRACTENGINE_MQH__
