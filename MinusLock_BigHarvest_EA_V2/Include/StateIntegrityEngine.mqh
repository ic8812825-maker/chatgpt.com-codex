#ifndef __BH_STATEINTEGRITYENGINE_MQH__
#define __BH_STATEINTEGRITYENGINE_MQH__

// V2.4.17 Full Phase-State Integrity Validation.
// Every FSM state is assigned an explicit shape: required legs, forbidden legs,
// and pending/retry context requirements. This engine intentionally validates
// terminal volumes through MT5 POSITION_VOLUME snapshots instead of synthetic math.


bool IsStateIntegrityTerminalState(EAState state)
{
   return (state == STATE_CLOSED_PROFIT ||
           state == STATE_DUAL_TAIL ||
           state == STATE_INVALID_REVERSE_GEOMETRY ||
           state == STATE_INVALID_SMALL_GEOMETRY ||
           state == STATE_REVERSE_LIMIT ||
           state == STATE_REVERSE_LIMIT_CLOSED ||
           state == STATE_REVERSE_WARNING ||
           state == STATE_INVALID_GEOMETRY_CLOSED ||
           state == STATE_RECOVERY_MISMATCH ||
           state == STATE_INTEGRITY_ERROR ||
           state == STATE_POSITION_RESOLUTION_ERROR ||
           state == STATE_MANUAL_INTERVENTION_REQUIRED ||
           state == STATE_STOP_MAX_LEVELS ||
           state == STATE_UNCLOSED_CYCLE ||
           state == STATE_STOP ||
           state == STATE_ERROR);
}

bool IsStateIntegrityPendingState(EAState state)
{
   return (state == STATE_CLOSE_BIG_PENDING ||
           state == STATE_CLOSE_SMALL_PENDING ||
           state == STATE_CLOSE_OLD_FAR_PENDING ||
           state == STATE_CLOSE_BIG_PART_PENDING ||
           state == STATE_CLOSE_NEW_FAR_PENDING ||
           state == STATE_OPEN_NEW_BIG_PENDING ||
           state == STATE_OPEN_NEW_SMALL_PENDING ||
           state == STATE_REVERSE_LIMIT_CLOSE_PENDING ||
           state == STATE_MAX_LEVELS_FINAL_CLOSE_PENDING ||
           state == STATE_STOP_MAX_LEVELS_CLOSE_PENDING);
}

bool IsStateIntegrityClosePendingState(EAState state)
{
   return (state == STATE_CLOSE_BIG_PENDING ||
           state == STATE_CLOSE_SMALL_PENDING ||
           state == STATE_CLOSE_OLD_FAR_PENDING ||
           state == STATE_CLOSE_BIG_PART_PENDING ||
           state == STATE_CLOSE_NEW_FAR_PENDING ||
           state == STATE_REVERSE_LIMIT_CLOSE_PENDING ||
           state == STATE_MAX_LEVELS_FINAL_CLOSE_PENDING ||
           state == STATE_STOP_MAX_LEVELS_CLOSE_PENDING);
}

bool IsStateIntegrityRetryState(EAState state)
{
   return IsStateIntegrityPendingState(state);
}

bool ValidateStateIntegrityLeg(string legName,
                               bool required,
                               bool forbidden,
                               bool hasContext,
                               ulong ticket,
                               ulong identifier,
                               double ctxLot,
                               Direction ctxDirection)
{
   bool ok = true;
   if(required && !hasContext)
   {
      LogError(StringFormat("EXPECTED_POSITION_MISSING State=%s Leg=%s Reason=context_absent", StateToString(State), legName));
      ok = false;
   }

   if(forbidden && hasContext)
   {
      LogError(StringFormat("UNEXPECTED_POSITION_PRESENT State=%s Leg=%s Ticket=%I64u Identifier=%I64u Lot=%.2f", StateToString(State), legName, ticket, identifier, ctxLot));
      ok = false;
   }

   if(required && (ticket == 0 || identifier == 0))
   {
      LogError(StringFormat("INVALID_STATE_SHAPE State=%s Leg=%s unresolved ticket/identifier Ticket=%I64u Identifier=%I64u", StateToString(State), legName, ticket, identifier));
      ok = false;
   }

   if(required && ticket != 0)
   {
      PositionSnapshot snapshot;
      if(!GetManagedPositionByTicket(ticket, snapshot))
      {
         LogError(StringFormat("EXPECTED_POSITION_MISSING State=%s Leg=%s Ticket=%I64u", StateToString(State), legName, ticket));
         ok = false;
      }
      else
      {
         double actualLot = NormalizeVolumeToStep(snapshot.lot);
         double expectedLot = NormalizeVolumeToStep(ctxLot);
         double diff = MathAbs(actualLot - expectedLot);
         if(identifier != 0 && snapshot.identifier != identifier)
         {
            LogError(StringFormat("INVALID_STATE_SHAPE State=%s Leg=%s IDENTIFIER_MISMATCH Ticket=%I64u ExpectedIdentifier=%I64u ActualIdentifier=%I64u", StateToString(State), legName, ticket, identifier, snapshot.identifier));
            ok = false;
         }
         if(ctxDirection != DIR_NONE && snapshot.direction != ctxDirection)
         {
            LogError(StringFormat("INVALID_STATE_SHAPE State=%s Leg=%s DIRECTION_MISMATCH Ticket=%I64u ExpectedDirection=%s ActualDirection=%s", StateToString(State), legName, ticket, DirectionToString(ctxDirection), DirectionToString(snapshot.direction)));
            ok = false;
         }
         if(diff > VolumeMismatchToleranceLots)
         {
            LogError(StringFormat("INVALID_STATE_SHAPE State=%s Leg=%s VOLUME_MISMATCH Ticket=%I64u ExpectedVolume=%.2f ActualVolume=%.2f Difference=%.5f", StateToString(State), legName, ticket, expectedLot, actualLot, diff));
            ok = false;
         }
      }
   }

   if(required && ctxLot <= VolumeMismatchToleranceLots)
   {
      LogError(StringFormat("INVALID_STATE_SHAPE State=%s Leg=%s Lot=%.5f VolumeMismatchToleranceLots=%.5f", StateToString(State), legName, ctxLot, VolumeMismatchToleranceLots));
      ok = false;
   }

   return ok;
}

bool ValidatePendingStateIntegrity(EAState state)
{
   if(!IsStateIntegrityPendingState(state))
      return true;

   bool ok = true;
   ok = ValidatePendingStateContract(state) && ok;
   bool pendingOk = (Ctx.pendingActionType != PENDING_NONE &&
                     Ctx.pendingNextState != STATE_IDLE &&
                     Ctx.pendingOperationStartTime > 0);
   if(state == STATE_OPEN_NEW_BIG_PENDING || state == STATE_OPEN_NEW_SMALL_PENDING)
      pendingOk = pendingOk && (Ctx.pendingLot > VolumeMismatchToleranceLots || Ctx.retryLot > VolumeMismatchToleranceLots || Ctx.pendingDirection != DIR_NONE);
   else
      pendingOk = pendingOk && (Ctx.pendingTicket != 0 || Ctx.retryTicket != 0) && (Ctx.pendingLot > VolumeMismatchToleranceLots || Ctx.retryLot > VolumeMismatchToleranceLots);

   if(!pendingOk)
   {
      LogError(StringFormat("INVALID_PENDING_CONTEXT State=%s pendingActionType=%d pendingTicket=%I64u pendingNextState=%s pendingLot=%.2f RetryStartTime=%I64d retryTicket=%I64u retryLot=%.2f",
                            StateToString(state),
                            (int)Ctx.pendingActionType,
                            Ctx.pendingTicket,
                            StateToString(Ctx.pendingNextState),
                            Ctx.pendingLot,
                            (long)Ctx.pendingOperationStartTime,
                            Ctx.retryTicket,
                            Ctx.retryLot));
      ok = false;
   }
   return ok;
}

bool ValidateRetryStateIntegrity(EAState state)
{
   if(!IsStateIntegrityRetryState(state))
      return true;

   bool ok = true;
   bool retryOk = (Ctx.retryAttempts >= 0 && Ctx.pendingOperationStartTime > 0);
   if(IsStateIntegrityClosePendingState(state))
      retryOk = retryOk && (Ctx.retryTicket != 0 || Ctx.pendingTicket != 0) && (Ctx.retryLot > VolumeMismatchToleranceLots || Ctx.pendingLot > VolumeMismatchToleranceLots);
   else
      retryOk = retryOk && (Ctx.retryLot > VolumeMismatchToleranceLots || Ctx.pendingLot > VolumeMismatchToleranceLots || Ctx.pendingDirection != DIR_NONE);

   if(!retryOk)
   {
      LogError(StringFormat("INVALID_RETRY_CONTEXT State=%s retryCounter=%d RetryStartTime=%I64d retryTicket=%I64u retryLot=%.2f pendingTicket=%I64u pendingActionType=%d",
                            StateToString(state),
                            Ctx.retryAttempts,
                            (long)Ctx.pendingOperationStartTime,
                            Ctx.retryTicket,
                            Ctx.retryLot,
                            Ctx.pendingTicket,
                            (int)Ctx.pendingActionType));
      ok = false;
   }
   return ok;
}

void GetStateIntegrityShape(EAState state,
                            bool &requireInitialBuy,
                            bool &requireInitialSell,
                            bool &requireFar,
                            bool &requireBig,
                            bool &requireSmall,
                            bool &forbidInitial,
                            bool &forbidFar,
                            bool &forbidBig,
                            bool &forbidSmall,
                            bool &requirePending,
                            bool &requireRetry)
{
   requireInitialBuy = false;
   requireInitialSell = false;
   requireFar = false;
   requireBig = false;
   requireSmall = false;
   forbidInitial = false;
   forbidFar = false;
   forbidBig = false;
   forbidSmall = false;
   requirePending = IsStateIntegrityPendingState(state);
   requireRetry = IsStateIntegrityRetryState(state);

   switch(state)
   {
      case STATE_IDLE:
      case STATE_RECOVERY_PENDING:
      case STATE_CLOSED_PROFIT:
      case STATE_DUAL_TAIL:
      case STATE_INVALID_REVERSE_GEOMETRY:
      case STATE_INVALID_SMALL_GEOMETRY:
      case STATE_REVERSE_LIMIT:
      case STATE_REVERSE_LIMIT_CLOSED:
      case STATE_REVERSE_WARNING:
      case STATE_INVALID_GEOMETRY_CLOSED:
      case STATE_RECOVERY_MISMATCH:
      case STATE_INTEGRITY_ERROR:
      case STATE_POSITION_RESOLUTION_ERROR:
      case STATE_MANUAL_INTERVENTION_REQUIRED:
      case STATE_STOP_MAX_LEVELS:
      case STATE_UNCLOSED_CYCLE:
      case STATE_STOP:
      case STATE_ERROR:
         break;

      case STATE_INITIAL_LOCK_OPENED:
         requireInitialBuy = true;
         requireInitialSell = true;
         forbidFar = true;
         forbidBig = true;
         forbidSmall = true;
         break;

      case STATE_INITIAL_PLUS_CLOSED:
      case STATE_FAR_ACTIVE:
      case STATE_MAX_LEVELS_DECISION:
      case STATE_FINAL_CLOSE:
         requireFar = true;
         forbidInitial = true;
         forbidBig = true;
         forbidSmall = true;
         break;

      case STATE_BIG_SMALL_OPENED:
      case STATE_BIG_HARVEST:
      case STATE_BIG_HARVEST_CLOSE_BIG:
      case STATE_WAIT_SMALL_TO_FAR:
      case STATE_SMALL_SCENARIO:
      case STATE_SMALL_CLOSE_SMALL:
         requireFar = true;
         requireBig = true;
         requireSmall = true;
         forbidInitial = true;
         break;

      case STATE_BIG_HARVEST_CLOSE_SMALL:
         requireFar = true;
         requireSmall = true;
         forbidInitial = true;
         forbidBig = true;
         break;

      case STATE_BIG_HARVEST_CALC_NET:
      case STATE_BIG_HARVEST_CLOSE_FAR:
      case STATE_BIG_HARVEST_CHECK_FINAL:
         requireFar = true;
         forbidInitial = true;
         forbidBig = true;
         forbidSmall = true;
         break;

      case STATE_SMALL_CLOSE_OLD_FAR:
         requireFar = true;
         requireBig = true;
         forbidInitial = true;
         forbidSmall = true;
         break;

      case STATE_SMALL_CLOSE_BIG_PART:
      case STATE_SMALL_BUILD_NEW_FAR:
         requireBig = true;
         forbidInitial = true;
         forbidFar = true;
         forbidSmall = true;
         break;

      case STATE_SMALL_CHECK_RESERVE:
      case STATE_SMALL_OPEN_NEW_BIG:
         requireFar = true;
         forbidInitial = true;
         forbidBig = true;
         forbidSmall = true;
         break;

      case STATE_SMALL_OPEN_NEW_SMALL:
         requireFar = true;
         requireBig = true;
         forbidInitial = true;
         forbidSmall = true;
         break;

      case STATE_OPEN_NEW_BIG_PENDING:
         requireFar = true;
         forbidInitial = true;
         forbidBig = true;
         forbidSmall = true;
         break;

      case STATE_OPEN_NEW_SMALL_PENDING:
         requireFar = true;
         requireBig = true;
         forbidInitial = true;
         forbidSmall = true;
         break;

      case STATE_CLOSE_BIG_PENDING:
      case STATE_CLOSE_SMALL_PENDING:
      case STATE_CLOSE_OLD_FAR_PENDING:
      case STATE_CLOSE_BIG_PART_PENDING:
      case STATE_CLOSE_NEW_FAR_PENDING:
      case STATE_REVERSE_LIMIT_CLOSE_PENDING:
      case STATE_MAX_LEVELS_FINAL_CLOSE_PENDING:
      case STATE_STOP_MAX_LEVELS_CLOSE_PENDING:
         forbidInitial = true;
         break;

      default:
         LogError(StringFormat("INVALID_STATE_SHAPE State=%s has no explicit integrity matrix entry", StateToString(state)));
         break;
   }
}

bool ValidateCurrentStateIntegrity()
{
   if(StateIntegrityValidationInProgress)
      return true;

   StateIntegrityValidationInProgress = true;
   bool ok = true;
   bool requireInitialBuy, requireInitialSell, requireFar, requireBig, requireSmall;
   bool forbidInitial, forbidFar, forbidBig, forbidSmall, requirePending, requireRetry;

   GetStateIntegrityShape(State,
                          requireInitialBuy,
                          requireInitialSell,
                          requireFar,
                          requireBig,
                          requireSmall,
                          forbidInitial,
                          forbidFar,
                          forbidBig,
                          forbidSmall,
                          requirePending,
                          requireRetry);

   LogInfo(StringFormat("STATE_INTEGRITY_MATRIX State=%s RequireInitialBuy=%s RequireInitialSell=%s RequireFar=%s RequireBig=%s RequireSmall=%s ForbidInitial=%s ForbidFar=%s ForbidBig=%s ForbidSmall=%s Pending=%s Retry=%s",
                        StateToString(State),
                        requireInitialBuy ? "YES" : "NO",
                        requireInitialSell ? "YES" : "NO",
                        requireFar ? "YES" : "NO",
                        requireBig ? "YES" : "NO",
                        requireSmall ? "YES" : "NO",
                        forbidInitial ? "YES" : "NO",
                        forbidFar ? "YES" : "NO",
                        forbidBig ? "YES" : "NO",
                        forbidSmall ? "YES" : "NO",
                        requirePending ? "YES" : "NO",
                        requireRetry ? "YES" : "NO"));

   ok = ValidateStateIntegrityLeg("INITIAL_BUY", requireInitialBuy, forbidInitial, HasInitialBuyContext(), Ctx.initialBuyTicket, Ctx.initialBuyIdentifier, Ctx.initialBuyLot, DIR_BUY) && ok;
   ok = ValidateStateIntegrityLeg("INITIAL_SELL", requireInitialSell, forbidInitial, HasInitialSellContext(), Ctx.initialSellTicket, Ctx.initialSellIdentifier, Ctx.initialSellLot, DIR_SELL) && ok;
   ok = ValidateStateIntegrityLeg("FAR", requireFar, forbidFar, HasFarContext(), Ctx.farTicket, Ctx.farIdentifier, Ctx.farLot, Ctx.farDirection) && ok;
   ok = ValidateStateIntegrityLeg("BIG", requireBig, forbidBig, HasBigContext(), Ctx.bigTicket, Ctx.bigIdentifier, Ctx.bigLot, Ctx.bigDirection) && ok;
   ok = ValidateStateIntegrityLeg("SMALL", requireSmall, forbidSmall, HasSmallContext(), Ctx.smallTicket, Ctx.smallIdentifier, Ctx.smallLot, Ctx.smallDirection) && ok;

   if(!IsStateIntegrityPendingState(State) && HasPendingOperationContext() && !IsStateIntegrityTerminalState(State))
   {
      LogError(StringFormat("PENDING_CONTRACT_INVALID State=%s has Pending Context but is not a Pending State pendingActionType=%d pendingOperation=%s", StateToString(State), (int)Ctx.pendingActionType, Ctx.pendingOperation));
      ok = false;
   }

   if(requirePending)
      ok = ValidatePendingStateIntegrity(State) && ok;
   if(requireRetry)
      ok = ValidateRetryStateIntegrity(State) && ok;

   if(ok)
   {
      LogInfo(StringFormat("STATE_INTEGRITY_PASS State=%s", StateToString(State)));
      StateIntegrityValidationInProgress = false;
      return true;
   }

   LogError(StringFormat("STATE_INTEGRITY_FAIL State=%s -> STATE_INTEGRITY_ERROR", StateToString(State)));
   State = STATE_INTEGRITY_ERROR;
   Ctx.lastError = "STATE_INTEGRITY_FAIL";
   SaveState();
   StateIntegrityValidationInProgress = false;
   return false;
}

#endif // __BH_STATEINTEGRITYENGINE_MQH__
