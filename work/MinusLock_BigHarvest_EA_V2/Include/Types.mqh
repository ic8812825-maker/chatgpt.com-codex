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
   STATE_WAIT_SMALL_TO_FAR,
   STATE_SMALL_SCENARIO,
   STATE_FINAL_CLOSE,
   STATE_CLOSED_PROFIT,
   STATE_DUAL_TAIL,
   STATE_INVALID_REVERSE_GEOMETRY,
   STATE_INVALID_SMALL_GEOMETRY,
   STATE_REVERSE_LIMIT,
   STATE_REVERSE_WARNING,
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

struct PositionSnapshot
{
   bool exists;
   ulong ticket;
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

   double farLot;
   double bigLot;
   double smallLot;

   double farOpenPrice;
   double bigOpenPrice;
   double smallOpenPrice;

   Direction farDirection;
   Direction bigDirection;
   Direction smallDirection;

   int harvestLevel;
   double totalReserve;
   double cycleFinalPL;

   bool initialProfitIgnored;
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
};

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
      case STATE_WAIT_SMALL_TO_FAR:    return "STATE_WAIT_SMALL_TO_FAR";
      case STATE_SMALL_SCENARIO:       return "STATE_SMALL_SCENARIO";
      case STATE_FINAL_CLOSE:          return "STATE_FINAL_CLOSE";
      case STATE_CLOSED_PROFIT:        return "STATE_CLOSED_PROFIT";
      case STATE_DUAL_TAIL:            return "STATE_DUAL_TAIL";
      case STATE_INVALID_REVERSE_GEOMETRY: return "STATE_INVALID_REVERSE_GEOMETRY";
      case STATE_INVALID_SMALL_GEOMETRY:   return "STATE_INVALID_SMALL_GEOMETRY";
      case STATE_REVERSE_LIMIT:            return "STATE_REVERSE_LIMIT";
      case STATE_REVERSE_WARNING:          return "STATE_REVERSE_WARNING";
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
