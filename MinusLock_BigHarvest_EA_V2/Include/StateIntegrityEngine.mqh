#ifndef __BH_STATEINTEGRITYENGINE_MQH__
#define __BH_STATEINTEGRITYENGINE_MQH__

// V2.4.17 Full Phase-State Integrity Validation.
// Every FSM state is assigned an explicit shape: required legs, forbidden legs,
// and pending/retry context requirements. This engine intentionally validates
// terminal volumes through MT5 POSITION_VOLUME snapshots instead of synthetic math.


bool IsStateIntegrityTerminalState(EAState state)
{
   return (state == STATE_CLOSED_PROFIT ||
           state == STATE_CLOSED_RECOVERY_LOSS ||
           state == STATE_DUAL_TAIL ||
           state == STATE_INVALID_REVERSE_GEOMETRY ||
           state == STATE_INVALID_SPLIT_GEOMETRY ||
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
           state == STATE_ERROR_OPEN_BIG_CORE ||
           state == STATE_ERROR_OPEN_SMALL_BASE ||
           state == STATE_ERROR_OPEN_BIG_TREND ||
           state == STATE_RECONCILIATION_ERROR ||
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
           state == STATE_SPLIT_OPEN_CORE_PENDING ||
           state == STATE_SPLIT_OPEN_SMALL_BASE_PENDING ||
           state == STATE_SPLIT_OPEN_TREND_PENDING ||
           state == STATE_SPLIT_CLOSE_CORE_PENDING ||
           state == STATE_SPLIT_CLOSE_TREND_PENDING ||
           state == STATE_SPLIT_CLOSE_SMALL_BASE_PENDING ||
           state == STATE_SPLIT_CLOSE_FAR_PARTIAL_PENDING ||
           state == STATE_SPLIT_CLOSE_FAR_FULL_PENDING ||
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
           state == STATE_SPLIT_CLOSE_CORE_PENDING ||
           state == STATE_SPLIT_CLOSE_TREND_PENDING ||
           state == STATE_SPLIT_CLOSE_SMALL_BASE_PENDING ||
           state == STATE_SPLIT_CLOSE_FAR_PARTIAL_PENDING ||
           state == STATE_SPLIT_CLOSE_FAR_FULL_PENDING ||
           state == STATE_REVERSE_LIMIT_CLOSE_PENDING ||
           state == STATE_MAX_LEVELS_FINAL_CLOSE_PENDING ||
           state == STATE_STOP_MAX_LEVELS_CLOSE_PENDING);
}

bool IsStateIntegrityRetryState(EAState state)
{
   return IsStateIntegrityPendingState(state);
}


bool HasBigCoreContext()
{
   return (Ctx.bigCoreTicket != 0 || Ctx.bigCoreIdentifier != 0 || Ctx.bigCoreLot > VolumeMismatchToleranceLots || Ctx.bigCoreDirection != DIR_NONE);
}

bool HasBigTrendContext()
{
   return (Ctx.bigTrendTicket != 0 || Ctx.bigTrendIdentifier != 0 || Ctx.bigTrendLot > VolumeMismatchToleranceLots || Ctx.bigTrendDirection != DIR_NONE);
}

bool HasSmallBaseContext()
{
   return (Ctx.smallBaseTicket != 0 || Ctx.smallBaseIdentifier != 0 || Ctx.smallBaseLot > VolumeMismatchToleranceLots || Ctx.smallBaseDirection != DIR_NONE);
}

bool IsSplitIntegrityState(EAState state)
{
   return (state == STATE_SPLIT_BIG_OPEN_CORE ||
           state == STATE_SPLIT_BIG_OPEN_SMALL_BASE ||
           state == STATE_SPLIT_BIG_OPEN_TREND ||
           state == STATE_SPLIT_GEOMETRY_ACTIVE ||
           state == STATE_SPLIT_BIG_HARVEST_CLOSE_CORE ||
           state == STATE_SPLIT_BIG_HARVEST_CLOSE_TREND ||
           state == STATE_SPLIT_BIG_HARVEST_CLOSE_SMALL_BASE ||
           state == STATE_SPLIT_BIG_HARVEST_CALC_NET ||
           state == STATE_SPLIT_BIG_HARVEST_CHECK_FULL_FAR ||
           state == STATE_SPLIT_BIG_HARVEST_PARTIAL_FAR ||
           state == STATE_SPLIT_BIG_HARVEST_FINAL_CHECK ||
           state == STATE_SPLIT_OPEN_CORE_PENDING ||
           state == STATE_SPLIT_OPEN_SMALL_BASE_PENDING ||
           state == STATE_SPLIT_OPEN_TREND_PENDING ||
           state == STATE_SPLIT_CLOSE_CORE_PENDING ||
           state == STATE_SPLIT_CLOSE_TREND_PENDING ||
           state == STATE_SPLIT_CLOSE_SMALL_BASE_PENDING ||
           state == STATE_SPLIT_CLOSE_FAR_PARTIAL_PENDING ||
           state == STATE_SPLIT_CLOSE_FAR_FULL_PENDING ||
           state == STATE_SPLIT_PARTIAL_HISTORY_PENDING ||
           state == STATE_SPLIT_MAX_LEVELS_DECISION);
}

bool ValidateSplitStateIntegrityLeg(string legName,
                                    bool required,
                                    bool forbidden,
                                    ulong ticket,
                                    ulong identifier,
                                    double lot,
                                    Direction direction)
{
   bool hasContext = (ticket != 0 || identifier != 0 || lot > VolumeMismatchToleranceLots || direction != DIR_NONE);
   bool ok = true;
   if(required && !hasContext)
   {
      LogError(StringFormat("SPLIT_STATE_INTEGRITY Result=FAIL State=%s Leg=%s StopReason=context_absent", StateToString(State), legName));
      ok = false;
   }
   if(forbidden && hasContext)
   {
      LogError(StringFormat("SPLIT_STATE_INTEGRITY Result=FAIL State=%s Leg=%s StopReason=forbidden_context Ticket=%I64u Identifier=%I64u Lot=%.2f", StateToString(State), legName, ticket, identifier, lot));
      ok = false;
   }
   if(required && (ticket == 0 || identifier == 0 || lot <= VolumeMismatchToleranceLots || direction == DIR_NONE))
   {
      LogError(StringFormat("SPLIT_STATE_INTEGRITY Result=FAIL State=%s Leg=%s StopReason=incomplete_context Ticket=%I64u Identifier=%I64u Lot=%.2f Direction=%s", StateToString(State), legName, ticket, identifier, lot, DirectionToString(direction)));
      ok = false;
   }
   if(required && ticket != 0)
   {
      PositionSnapshot snapshot;
      if(!GetManagedPositionByTicket(ticket, snapshot))
      {
         LogError(StringFormat("SPLIT_STATE_INTEGRITY Result=FAIL State=%s Leg=%s StopReason=position_missing Ticket=%I64u Identifier=%I64u", StateToString(State), legName, ticket, identifier));
         ok = false;
      }
      else
      {
         double actualLot = NormalizeVolumeToStep(snapshot.lot);
         double expectedLot = NormalizeVolumeToStep(lot);
         if(identifier != 0 && snapshot.identifier != identifier)
         {
            LogError(StringFormat("SPLIT_STATE_INTEGRITY Result=FAIL State=%s Leg=%s StopReason=identifier_mismatch ExpectedIdentifier=%I64u ActualIdentifier=%I64u", StateToString(State), legName, identifier, snapshot.identifier));
            ok = false;
         }
         if(direction != DIR_NONE && snapshot.direction != direction)
         {
            LogError(StringFormat("SPLIT_STATE_INTEGRITY Result=FAIL State=%s Leg=%s StopReason=direction_mismatch ExpectedDirection=%s ActualDirection=%s", StateToString(State), legName, DirectionToString(direction), DirectionToString(snapshot.direction)));
            ok = false;
         }
         if(MathAbs(actualLot - expectedLot) > VolumeMismatchToleranceLots)
         {
            LogError(StringFormat("SPLIT_STATE_INTEGRITY Result=FAIL State=%s Leg=%s StopReason=volume_mismatch ExpectedLot=%.2f ActualLot=%.2f", StateToString(State), legName, expectedLot, actualLot));
            ok = false;
         }
      }
   }
   if(ok)
      LogInfo(StringFormat("SPLIT_STATE_INTEGRITY Result=PASS State=%s Leg=%s Required=%s Forbidden=%s Ticket=%I64u Identifier=%I64u Lot=%.2f", StateToString(State), legName, required ? "YES" : "NO", forbidden ? "YES" : "NO", ticket, identifier, lot));
   return ok;
}

void GetSplitStateIntegrityShape(EAState state,
                                 bool &requireFar,
                                 bool &requireBigCore,
                                 bool &requireBigTrend,
                                 bool &requireSmallBase,
                                 bool &forbidBigCore,
                                 bool &forbidBigTrend,
                                 bool &forbidSmallBase,
                                 bool &allowFarAbsent)
{
   requireFar = false;
   requireBigCore = false;
   requireBigTrend = false;
   requireSmallBase = false;
   forbidBigCore = false;
   forbidBigTrend = false;
   forbidSmallBase = false;
   allowFarAbsent = false;

   switch(state)
   {
      case STATE_SPLIT_BIG_OPEN_CORE:
      case STATE_SPLIT_OPEN_CORE_PENDING:
         requireFar = true; forbidBigTrend = true; forbidSmallBase = true; break;
      case STATE_SPLIT_BIG_OPEN_SMALL_BASE:
      case STATE_SPLIT_OPEN_SMALL_BASE_PENDING:
         requireFar = true; requireBigCore = true; forbidBigTrend = true; break;
      case STATE_SPLIT_BIG_OPEN_TREND:
      case STATE_SPLIT_OPEN_TREND_PENDING:
         requireFar = true; requireBigCore = true; requireSmallBase = true; break;
      case STATE_SPLIT_GEOMETRY_ACTIVE:
      case STATE_SPLIT_BIG_HARVEST_CLOSE_CORE:
         requireFar = true; requireBigCore = true; requireBigTrend = true; requireSmallBase = true; break;
      case STATE_SPLIT_CLOSE_CORE_PENDING:
         requireFar = true; requireBigCore = true; requireBigTrend = true; requireSmallBase = true; break;
      case STATE_SPLIT_BIG_HARVEST_CLOSE_TREND:
      case STATE_SPLIT_CLOSE_TREND_PENDING:
         requireFar = true; requireBigTrend = true; requireSmallBase = true; forbidBigCore = true; break;
      case STATE_SPLIT_BIG_HARVEST_CLOSE_SMALL_BASE:
      case STATE_SPLIT_CLOSE_SMALL_BASE_PENDING:
         requireFar = true; requireSmallBase = true; forbidBigCore = true; forbidBigTrend = true; break;
      case STATE_SPLIT_BIG_HARVEST_CALC_NET:
      case STATE_SPLIT_BIG_HARVEST_CHECK_FULL_FAR:
      case STATE_SPLIT_BIG_HARVEST_PARTIAL_FAR:
      case STATE_SPLIT_CLOSE_FAR_PARTIAL_PENDING:
      case STATE_SPLIT_CLOSE_FAR_FULL_PENDING:
      case STATE_SPLIT_PARTIAL_HISTORY_PENDING:
      case STATE_SPLIT_MAX_LEVELS_DECISION:
         requireFar = true; forbidBigCore = true; forbidBigTrend = true; forbidSmallBase = true; break;
      case STATE_SPLIT_BIG_HARVEST_FINAL_CHECK:
         allowFarAbsent = true; forbidBigCore = true; forbidBigTrend = true; forbidSmallBase = true; break;
      default:
         break;
   }
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


bool IsOpenPendingState(EAState state)
{
   return (state == STATE_OPEN_NEW_BIG_PENDING ||
           state == STATE_OPEN_NEW_SMALL_PENDING ||
           state == STATE_SPLIT_OPEN_CORE_PENDING ||
           state == STATE_SPLIT_OPEN_SMALL_BASE_PENDING ||
           state == STATE_SPLIT_OPEN_TREND_PENDING);
}

bool IsClosePendingState(EAState state)
{
   return IsStateIntegrityClosePendingState(state);
}

bool ValidatePendingStateIntegrity(EAState state)
{
   if(!IsStateIntegrityPendingState(state))
      return true;

   bool ok = true;
   ok = ValidatePendingStateContract(state) && ok;
   bool pendingOk = (Ctx.pendingActionType != PENDING_NONE &&
                     Ctx.pendingNextState != STATE_IDLE &&
                     Ctx.pendingOperationStartTime > 0 &&
                     Ctx.pendingAttempts >= 0);
   if(IsOpenPendingState(state))
   {
      pendingOk = pendingOk &&
                  Ctx.pendingLot > VolumeMismatchToleranceLots &&
                  Ctx.pendingDirection != DIR_NONE &&
                  Ctx.pendingComment != "";
   }
   else
   {
      pendingOk = pendingOk &&
                  (Ctx.pendingTicket != 0 || Ctx.retryTicket != 0) &&
                  (Ctx.pendingLot > VolumeMismatchToleranceLots || Ctx.retryLot > VolumeMismatchToleranceLots);
   }

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
      case STATE_REVERSE_SMALL_OPEN_FAILED:
      case STATE_RECOVERY_PENDING:
      case STATE_CLOSED_PROFIT:
      case STATE_CLOSED_RECOVERY_LOSS:
      case STATE_DUAL_TAIL:
      case STATE_INVALID_REVERSE_GEOMETRY:
      case STATE_INVALID_SPLIT_GEOMETRY:
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
      case STATE_ERROR_OPEN_BIG_CORE:
      case STATE_ERROR_OPEN_SMALL_BASE:
      case STATE_ERROR_OPEN_BIG_TREND:
      case STATE_RECONCILIATION_ERROR:
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
      case STATE_BIG_HARVEST_CLOSE_CORE:
      case STATE_BIG_HARVEST_CLOSE_TREND:
      case STATE_BIG_HARVEST_CLOSE_SMALL_BASE:
      case STATE_REVERSE_CONFIRMATION_WAIT:
      case STATE_REVERSE_CLOSE_BIG_TREND:
      case STATE_REVERSE_CALCULATE_DYNAMIC_SMALL:
      case STATE_REVERSE_OPEN_DYNAMIC_SMALL:
      case STATE_REVERSE_WAIT_FAR_TOUCH:
      case STATE_WAIT_SMALL_TO_FAR:
      case STATE_SMALL_SCENARIO:
      case STATE_SMALL_CLOSE_SMALL:
      case STATE_SMALL_CLOSE_SMALL_BASE:
      case STATE_SMALL_CLOSE_DYNAMIC_SMALL:
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
      case STATE_SMALL_CLOSE_BIG_CORE_PART:
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

      case STATE_SPLIT_BIG_OPEN_CORE:
      case STATE_SPLIT_BIG_OPEN_SMALL_BASE:
      case STATE_SPLIT_BIG_OPEN_TREND:
      case STATE_SPLIT_GEOMETRY_ACTIVE:
      case STATE_SPLIT_BIG_HARVEST_CLOSE_CORE:
      case STATE_SPLIT_BIG_HARVEST_CLOSE_TREND:
      case STATE_SPLIT_BIG_HARVEST_CLOSE_SMALL_BASE:
      case STATE_SPLIT_BIG_HARVEST_CALC_NET:
      case STATE_SPLIT_BIG_HARVEST_CHECK_FULL_FAR:
      case STATE_SPLIT_BIG_HARVEST_PARTIAL_FAR:
      case STATE_SPLIT_BIG_HARVEST_FINAL_CHECK:
      case STATE_SPLIT_OPEN_CORE_PENDING:
      case STATE_SPLIT_OPEN_SMALL_BASE_PENDING:
      case STATE_SPLIT_OPEN_TREND_PENDING:
      case STATE_SPLIT_CLOSE_CORE_PENDING:
      case STATE_SPLIT_CLOSE_TREND_PENDING:
      case STATE_SPLIT_CLOSE_SMALL_BASE_PENDING:
      case STATE_SPLIT_CLOSE_FAR_PARTIAL_PENDING:
      case STATE_SPLIT_CLOSE_FAR_FULL_PENDING:
      case STATE_SPLIT_PARTIAL_HISTORY_PENDING:
      case STATE_SPLIT_MAX_LEVELS_DECISION:
         requireFar = (state != STATE_SPLIT_BIG_HARVEST_FINAL_CHECK);
         forbidInitial = true;
         forbidBig = true;
         forbidSmall = true;
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
   bool requireBigCore=false, requireBigTrend=false, requireSmallBase=false;
   bool forbidBigCore=false, forbidBigTrend=false, forbidSmallBase=false, allowFarAbsent=false;

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

   if(IsSplitIntegrityState(State))
      GetSplitStateIntegrityShape(State, requireFar, requireBigCore, requireBigTrend, requireSmallBase, forbidBigCore, forbidBigTrend, forbidSmallBase, allowFarAbsent);

   LogInfo(StringFormat("STATE_INTEGRITY_MATRIX State=%s RequireInitialBuy=%s RequireInitialSell=%s RequireFar=%s RequireBig=%s RequireSmall=%s ForbidInitial=%s ForbidFar=%s ForbidBig=%s ForbidSmall=%s RequireBigCore=%s RequireBigTrend=%s RequireSmallBase=%s ForbidBigCore=%s ForbidBigTrend=%s ForbidSmallBase=%s Pending=%s Retry=%s",
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
                        requireBigCore ? "YES" : "NO",
                        requireBigTrend ? "YES" : "NO",
                        requireSmallBase ? "YES" : "NO",
                        forbidBigCore ? "YES" : "NO",
                        forbidBigTrend ? "YES" : "NO",
                        forbidSmallBase ? "YES" : "NO",
                        requirePending ? "YES" : "NO",
                        requireRetry ? "YES" : "NO"));

   ok = ValidateStateIntegrityLeg("INITIAL_BUY", requireInitialBuy, forbidInitial, HasInitialBuyContext(), Ctx.initialBuyTicket, Ctx.initialBuyIdentifier, Ctx.initialBuyLot, DIR_BUY) && ok;
   ok = ValidateStateIntegrityLeg("INITIAL_SELL", requireInitialSell, forbidInitial, HasInitialSellContext(), Ctx.initialSellTicket, Ctx.initialSellIdentifier, Ctx.initialSellLot, DIR_SELL) && ok;
   ok = ValidateStateIntegrityLeg("FAR", requireFar, forbidFar, HasFarContext(), Ctx.farTicket, Ctx.farIdentifier, Ctx.farLot, Ctx.farDirection) && ok;
   ok = ValidateStateIntegrityLeg("BIG", requireBig, forbidBig, HasBigContext(), Ctx.bigTicket, Ctx.bigIdentifier, Ctx.bigLot, Ctx.bigDirection) && ok;
   ok = ValidateStateIntegrityLeg("SMALL", requireSmall, forbidSmall, HasSmallContext(), Ctx.smallTicket, Ctx.smallIdentifier, Ctx.smallLot, Ctx.smallDirection) && ok;

   if(IsSplitIntegrityState(State))
   {
      if(allowFarAbsent && !HasFarContext())
         LogInfo(StringFormat("SPLIT_STATE_INTEGRITY Result=PASS State=%s Leg=FAR OptionalClosed=YES", StateToString(State)));
      ok = ValidateSplitStateIntegrityLeg("BIG_CORE", requireBigCore, forbidBigCore, Ctx.bigCoreTicket, Ctx.bigCoreIdentifier, Ctx.bigCoreLot, Ctx.bigCoreDirection) && ok;
      ok = ValidateSplitStateIntegrityLeg("BIG_TREND", requireBigTrend, forbidBigTrend, Ctx.bigTrendTicket, Ctx.bigTrendIdentifier, Ctx.bigTrendLot, Ctx.bigTrendDirection) && ok;
      ok = ValidateSplitStateIntegrityLeg("SMALL_BASE", requireSmallBase, forbidSmallBase, Ctx.smallBaseTicket, Ctx.smallBaseIdentifier, Ctx.smallBaseLot, Ctx.smallBaseDirection) && ok;
      if(HasBigContext() || HasSmallContext())
      {
         LogError(StringFormat("SPLIT_STATE_INTEGRITY Result=FAIL State=%s StopReason=legacy_big_small_present BigTicket=%I64u SmallTicket=%I64u", StateToString(State), Ctx.bigTicket, Ctx.smallTicket));
         ok = false;
      }
   }

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
