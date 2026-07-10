#ifndef __BH_TYPES_MQH__
#define __BH_TYPES_MQH__

enum EAState
{
   STATE_IDLE = 0,
   STATE_INITIAL_LOCK_OPENED,
   STATE_INITIAL_PLUS_CLOSED,
   STATE_FAR_ACTIVE,
   STATE_BIG_SMALL_OPENED,
   STATE_BIG_HARVEST,
   STATE_BIG_HARVEST_CLOSE_BIG,
   STATE_BIG_HARVEST_CLOSE_SMALL,
   STATE_BIG_HARVEST_CALC_NET,
   STATE_BIG_HARVEST_CLOSE_FAR,
   STATE_BIG_HARVEST_CHECK_FINAL,
   STATE_WAIT_SMALL_TO_FAR,
   STATE_SMALL_SCENARIO,
   STATE_SMALL_CLOSE_SMALL,
   STATE_SMALL_CLOSE_OLD_FAR,
   STATE_SMALL_CLOSE_BIG_PART,
   STATE_SMALL_BUILD_NEW_FAR,
   STATE_SMALL_CHECK_RESERVE,
   STATE_SMALL_OPEN_NEW_BIG,
   STATE_SMALL_OPEN_NEW_SMALL,
   STATE_FINAL_CLOSE,
   STATE_MAX_LEVELS_DECISION,
   STATE_CLOSED_PROFIT,
   STATE_CLOSED_RECOVERY_LOSS,
   STATE_DUAL_TAIL,
   STATE_INVALID_REVERSE_GEOMETRY,
   STATE_INVALID_SMALL_GEOMETRY,
   STATE_REVERSE_LIMIT,
   STATE_REVERSE_LIMIT_CLOSED,
   STATE_REVERSE_LIMIT_CLOSE_PENDING,
   STATE_MAX_LEVELS_FINAL_CLOSE_PENDING,
   STATE_STOP_MAX_LEVELS_CLOSE_PENDING,
   STATE_REVERSE_WARNING,
   STATE_INVALID_GEOMETRY_CLOSED,
   STATE_CLOSE_BIG_PENDING,
   STATE_CLOSE_SMALL_PENDING,
   STATE_CLOSE_OLD_FAR_PENDING,
   STATE_CLOSE_BIG_PART_PENDING,
   STATE_CLOSE_NEW_FAR_PENDING,
   STATE_OPEN_NEW_BIG_PENDING,
   STATE_OPEN_NEW_SMALL_PENDING,
   STATE_RECOVERY_PENDING,
   STATE_RECOVERY_MISMATCH,
   STATE_INTEGRITY_ERROR,
   STATE_POSITION_RESOLUTION_ERROR,
   STATE_MANUAL_INTERVENTION_REQUIRED,
   STATE_STOP_MAX_LEVELS,
   STATE_UNCLOSED_CYCLE,
   STATE_STOP,
   STATE_ERROR
};

enum Direction
{
   DIR_NONE = 0,
   DIR_BUY,
   DIR_SELL
};

enum PendingActionType
{
   PENDING_NONE = 0,
   PENDING_CLOSE_BIG_FULL,
   PENDING_CLOSE_SMALL_FULL,
   PENDING_CLOSE_OLD_FAR_FULL,
   PENDING_CLOSE_FAR_FULL,
   PENDING_CLOSE_FAR_PARTIAL,
   PENDING_CLOSE_BIG_PARTIAL,
   PENDING_OPEN_BIG,
   PENDING_OPEN_SMALL,
   PENDING_MAX_LEVELS_FINAL_CLOSE,
   PENDING_STOP_MAX_LEVELS_CLOSE
};

enum ReserveEventType
{
   RESERVE_EVENT_NONE = 0,
   RESERVE_EVENT_BIG_HARVEST_ADD,
   RESERVE_EVENT_SMALL_HARVEST_ADD,
   RESERVE_EVENT_FAR_COVER_DEBIT,
   RESERVE_EVENT_BIG_FULL_FAR_CLOSE_DEBIT,
   RESERVE_EVENT_SMALL_FAR_DEBIT,
   RESERVE_EVENT_FINAL_CLOSE_DEBIT,
   RESERVE_EVENT_RESET
};

struct ReserveLedgerEntry
{
   long eventId;
   datetime timestamp;
   ReserveEventType type;
   double amount;
   double reserveBefore;
   double reserveAfter;
   long bigIdentifier;
   long smallIdentifier;
   long farIdentifier;
   int harvestLevel;
   int reverseCycle;
   long eventKeyHash;
};

struct PositionResolutionResult
{
   bool resolved;
   ulong ticket;
   ulong identifier;
   double lot;
   ENUM_POSITION_TYPE type;
   double openPrice;
   datetime openTime;
};

struct PositionSnapshot
{
   bool exists;
   ulong ticket;
   ulong identifier;
   Direction direction;
   double lot;
   double openPrice;
   double profitMoney;
   string comment;
};

struct ClosedDealSnapshot
{
   ulong ticket;
   Direction direction;
   double lot;
   double openPrice;
   double closePrice;
   double profitMoney;
   string comment;
};

struct RecoveryContext
{
   ulong farTicket;
   ulong bigTicket;
   ulong smallTicket;
   ulong farIdentifier;
   ulong bigIdentifier;
   ulong smallIdentifier;
   ulong initialBuyTicket;
   ulong initialSellTicket;
   ulong initialBuyIdentifier;
   ulong initialSellIdentifier;

   double farLot;
   double bigLot;
   double smallLot;

   double farOpenPrice;
   double bigOpenPrice;
   double smallOpenPrice;
   double initialBuyLot;
   double initialSellLot;
   double initialBuyOpenPrice;
   double initialSellOpenPrice;

   Direction farDirection;
   Direction bigDirection;
   Direction smallDirection;

   int harvestLevel;
   double totalReserve;
   double cycleFinalPL;

   bool initialProfitIgnored;
   bool initialLockRecovered;
   bool finalCloseAllowed;
   bool dualTailDetected;

   int reverseCycleCount;
   double oldFarLotBeforeReverse;
   double newFarLotAfterReverse;
   double newBigLotAfterReverse;
   double newSmallLotAfterReverse;

   double reverseStrength;
   double reverseQualityScore;
   double projectedReserveCoverage;
   double smallReverseNet;

   bool geometryValid;
   bool reverseLimitReached;
   bool reserveProjectionOk;
   bool smallGeometryValid;

   double cycleATRRaw;
   double cycleATRPoints;
   int geometrySource;
   int geometryFallback;
   int geometryFallbackReasonCode;
   int geometryCleared;
   int geometryClearReasonCode;
   int geometryReady;
   int tradingAllowedByFallback;
   int workInitialTriggerPoints;
   int workBigMoveStartPoints;
   int workBigMoveStepPoints;
   int workFarDistancePoints;
   int geometryModeUsed;
   datetime geometryCalculatedTime;

   double initialFarDistancePoints;
   double currentBigMovePoints;
   double cumulativeBigMovePoints;
   double effectiveFarDistancePoints;
   double currentClosePrice;

   datetime cycleStartTime;
   double initialIgnoredProfit;
   double realRecoveryPL;
   double realCyclePL;
   double realClosedProfit;
   double realClosedLoss;
   double realCommission;
   double realSwap;
   double realCosts;
   double theoreticalCyclePL;
   double cycleStartBalance;
   double cycleCurrentBalance;
   double cycleBalancePL;
   bool realCycleProfitPositive;
   bool lastCloseWasSystemClose;
   string lastSystemCloseComment;
   string lastAction;
   string lastError;
   bool riskGateOk;
   EAState lastRetryState;
   ulong retryTicket;
   double retryLot;
   int retryAttempts;
   datetime lastRetryLogTime;
   PendingActionType pendingActionType;
   string pendingOperation;
   EAState pendingNextState;
   ulong pendingTicket;
   double pendingLot;
   int pendingAttempts;
   datetime pendingOperationStartTime;
   ulong pendingBigPositionId;
   ulong pendingSmallPositionId;
   double pendingRealNet;
   double pendingCloseFarBudget;
   double pendingReserveAdd;
   double pendingSmallReserveAdd;
   bool pendingReserveApplied;
   bool pendingSmallReserveApplied;
   double pendingCloseFarLot;
   bool pendingFullFarClose;
   double partialFarBudgetCarry;
   double pendingPartialFarBudgetAvailable;
   double pendingPartialFarBudgetCarryBefore;
   double pendingProjectedPartialFarLoss;
   Direction pendingDirection;
   string pendingComment;
   Direction savedSmallDirection;
   double savedSmallClosePrice;
   double savedSmallTouchPrice;
   double savedSmallOpenPrice;
   double savedSmallLot;
   ulong oldFarTicket;
   double oldFarLot;
   Direction oldFarDirection;
   double oldFarOpenPrice;
   double smallScenarioRealBefore;
   double smallScenarioRealAfter;
   ulong cycleId;
};

EAState State = STATE_IDLE;
RecoveryContext Ctx;

string DirectionToString(Direction dir)
{
   if(dir == DIR_BUY)
      return "BUY";
   if(dir == DIR_SELL)
      return "SELL";
   return "NONE";
}

string StateToString(EAState state)
{
   switch(state)
   {
      case STATE_IDLE:                 return "STATE_IDLE";
      case STATE_INITIAL_LOCK_OPENED:  return "STATE_INITIAL_LOCK_OPENED";
      case STATE_INITIAL_PLUS_CLOSED:  return "STATE_INITIAL_PLUS_CLOSED";
      case STATE_FAR_ACTIVE:           return "STATE_FAR_ACTIVE";
      case STATE_BIG_SMALL_OPENED:     return "STATE_BIG_SMALL_OPENED";
      case STATE_BIG_HARVEST:          return "STATE_BIG_HARVEST";
      case STATE_BIG_HARVEST_CLOSE_BIG: return "STATE_BIG_HARVEST_CLOSE_BIG";
      case STATE_BIG_HARVEST_CLOSE_SMALL: return "STATE_BIG_HARVEST_CLOSE_SMALL";
      case STATE_BIG_HARVEST_CALC_NET: return "STATE_BIG_HARVEST_CALC_NET";
      case STATE_BIG_HARVEST_CLOSE_FAR: return "STATE_BIG_HARVEST_CLOSE_FAR";
      case STATE_BIG_HARVEST_CHECK_FINAL: return "STATE_BIG_HARVEST_CHECK_FINAL";
      case STATE_WAIT_SMALL_TO_FAR:    return "STATE_WAIT_SMALL_TO_FAR";
      case STATE_SMALL_SCENARIO:       return "STATE_SMALL_SCENARIO";
      case STATE_SMALL_CLOSE_SMALL:    return "STATE_SMALL_CLOSE_SMALL";
      case STATE_SMALL_CLOSE_OLD_FAR:  return "STATE_SMALL_CLOSE_OLD_FAR";
      case STATE_SMALL_CLOSE_BIG_PART: return "STATE_SMALL_CLOSE_BIG_PART";
      case STATE_SMALL_BUILD_NEW_FAR:  return "STATE_SMALL_BUILD_NEW_FAR";
      case STATE_SMALL_CHECK_RESERVE:  return "STATE_SMALL_CHECK_RESERVE";
      case STATE_SMALL_OPEN_NEW_BIG:   return "STATE_SMALL_OPEN_NEW_BIG";
      case STATE_SMALL_OPEN_NEW_SMALL: return "STATE_SMALL_OPEN_NEW_SMALL";
      case STATE_FINAL_CLOSE:          return "STATE_FINAL_CLOSE";
      case STATE_MAX_LEVELS_DECISION:  return "STATE_MAX_LEVELS_DECISION";
      case STATE_CLOSED_PROFIT:        return "STATE_CLOSED_PROFIT";
      case STATE_CLOSED_RECOVERY_LOSS: return "STATE_CLOSED_RECOVERY_LOSS";
      case STATE_DUAL_TAIL:            return "STATE_DUAL_TAIL";
      case STATE_INVALID_REVERSE_GEOMETRY: return "STATE_INVALID_REVERSE_GEOMETRY";
      case STATE_INVALID_SMALL_GEOMETRY:   return "STATE_INVALID_SMALL_GEOMETRY";
      case STATE_REVERSE_LIMIT:            return "STATE_REVERSE_LIMIT";
      case STATE_REVERSE_LIMIT_CLOSED:     return "STATE_REVERSE_LIMIT_CLOSED";
      case STATE_REVERSE_LIMIT_CLOSE_PENDING: return "STATE_REVERSE_LIMIT_CLOSE_PENDING";
      case STATE_MAX_LEVELS_FINAL_CLOSE_PENDING: return "STATE_MAX_LEVELS_FINAL_CLOSE_PENDING";
      case STATE_STOP_MAX_LEVELS_CLOSE_PENDING: return "STATE_STOP_MAX_LEVELS_CLOSE_PENDING";
      case STATE_REVERSE_WARNING:          return "STATE_REVERSE_WARNING";
      case STATE_INVALID_GEOMETRY_CLOSED:  return "STATE_INVALID_GEOMETRY_CLOSED";
      case STATE_CLOSE_BIG_PENDING:        return "STATE_CLOSE_BIG_PENDING";
      case STATE_CLOSE_SMALL_PENDING:      return "STATE_CLOSE_SMALL_PENDING";
      case STATE_CLOSE_OLD_FAR_PENDING:    return "STATE_CLOSE_OLD_FAR_PENDING";
      case STATE_CLOSE_BIG_PART_PENDING:   return "STATE_CLOSE_BIG_PART_PENDING";
      case STATE_CLOSE_NEW_FAR_PENDING:    return "STATE_CLOSE_NEW_FAR_PENDING";
      case STATE_OPEN_NEW_BIG_PENDING:     return "STATE_OPEN_NEW_BIG_PENDING";
      case STATE_OPEN_NEW_SMALL_PENDING:   return "STATE_OPEN_NEW_SMALL_PENDING";
      case STATE_RECOVERY_PENDING:         return "STATE_RECOVERY_PENDING";
      case STATE_RECOVERY_MISMATCH:         return "STATE_RECOVERY_MISMATCH";
      case STATE_INTEGRITY_ERROR:           return "STATE_INTEGRITY_ERROR";
      case STATE_POSITION_RESOLUTION_ERROR: return "STATE_POSITION_RESOLUTION_ERROR";
      case STATE_MANUAL_INTERVENTION_REQUIRED: return "STATE_MANUAL_INTERVENTION_REQUIRED";
      case STATE_STOP_MAX_LEVELS:      return "STATE_STOP_MAX_LEVELS";
      case STATE_UNCLOSED_CYCLE:       return "STATE_UNCLOSED_CYCLE";
      case STATE_STOP:                 return "STATE_STOP";
      case STATE_ERROR:                return "STATE_ERROR";
   }

   return "STATE_UNKNOWN";
}

Direction OppositeDirection(Direction dir)
{
   if(dir == DIR_BUY)
      return DIR_SELL;
   if(dir == DIR_SELL)
      return DIR_BUY;
   return DIR_NONE;
}

#endif // __BH_TYPES_MQH__
