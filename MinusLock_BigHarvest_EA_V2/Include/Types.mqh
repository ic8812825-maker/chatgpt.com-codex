#ifndef __BH_TYPES_MQH__
#define __BH_TYPES_MQH__

enum EAState
{
   STATE_IDLE = 0,
   STATE_INITIAL_LOCK_OPENED,
   STATE_INITIAL_PLUS_CLOSED,
   STATE_FAR_ACTIVE,
   STATE_BIG_SMALL_OPENED,
   STATE_SPLIT_BIG_OPEN_CORE,
   STATE_SPLIT_BIG_OPEN_TREND,
   STATE_SPLIT_BIG_OPEN_SMALL_BASE,
   STATE_SPLIT_GEOMETRY_ACTIVE,
   STATE_SPLIT_BIG_HARVEST_CLOSE_CORE,
   STATE_SPLIT_BIG_HARVEST_CLOSE_TREND,
   STATE_SPLIT_BIG_HARVEST_CLOSE_SMALL_BASE,
   STATE_SPLIT_BIG_HARVEST_CALC_NET,
   STATE_SPLIT_BIG_HARVEST_CHECK_FULL_FAR,
   STATE_SPLIT_BIG_HARVEST_PARTIAL_FAR,
   STATE_SPLIT_BIG_HARVEST_FINAL_CHECK,
   STATE_SPLIT_OPEN_CORE_PENDING,
   STATE_SPLIT_OPEN_SMALL_BASE_PENDING,
   STATE_SPLIT_OPEN_TREND_PENDING,
   STATE_SPLIT_CLOSE_CORE_PENDING,
   STATE_SPLIT_CLOSE_TREND_PENDING,
   STATE_SPLIT_CLOSE_SMALL_BASE_PENDING,
   STATE_SPLIT_CLOSE_FAR_PARTIAL_PENDING,
   STATE_SPLIT_CLOSE_FAR_FULL_PENDING,
   STATE_SPLIT_PARTIAL_HISTORY_PENDING,
   STATE_SPLIT_MAX_LEVELS_DECISION,
   STATE_BIG_HARVEST,
   STATE_BIG_HARVEST_CLOSE_BIG,
   STATE_BIG_HARVEST_CLOSE_CORE,
   STATE_BIG_HARVEST_CLOSE_TREND,
   STATE_BIG_HARVEST_CLOSE_SMALL_BASE,
   STATE_BIG_HARVEST_CLOSE_SMALL,
   STATE_BIG_HARVEST_CALC_NET,
   STATE_BIG_HARVEST_CLOSE_FAR,
   STATE_BIG_HARVEST_CHECK_FINAL,
   STATE_WAIT_SMALL_TO_FAR,
   STATE_REVERSE_CONFIRMATION_WAIT,
   STATE_REVERSE_CLOSE_BIG_TREND,
   STATE_REVERSE_CALCULATE_DYNAMIC_SMALL,
   STATE_REVERSE_OPEN_DYNAMIC_SMALL,
   STATE_REVERSE_WAIT_FAR_TOUCH,
   STATE_REVERSE_SMALL_OPEN_FAILED,
   STATE_SMALL_SCENARIO,
   STATE_SMALL_CLOSE_SMALL,
   STATE_SMALL_CLOSE_SMALL_BASE,
   STATE_SMALL_CLOSE_DYNAMIC_SMALL,
   STATE_SMALL_CLOSE_OLD_FAR,
   STATE_SMALL_CLOSE_BIG_PART,
   STATE_SMALL_CLOSE_BIG_CORE_PART,
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
   STATE_INVALID_SPLIT_GEOMETRY,
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
   STATE_ERROR_OPEN_BIG_CORE,
   STATE_ERROR_OPEN_SMALL_BASE,
   STATE_ERROR_OPEN_BIG_TREND,
   STATE_RECONCILIATION_ERROR,
   STATE_ERROR
};

enum Direction
{
   DIR_NONE = 0,
   DIR_BUY,
   DIR_SELL
};
enum ScenarioMode { SCENARIO_IDLE=0,SCENARIO_BIG_ACTIVE,SCENARIO_BIG_CLOSING,SCENARIO_BIG_ACCOUNTING,SCENARIO_SMALL_SWITCH_PENDING,SCENARIO_SMALL_ACTIVE,SCENARIO_SMALL_CLOSING,SCENARIO_FINAL_CLOSE,SCENARIO_RECOVERY,SCENARIO_ERROR };

enum PersistedUInt64State
{
   PERSISTED_UINT64_ABSENT = 0,
   PERSISTED_UINT64_ZERO,
   PERSISTED_UINT64_ACTIVE,
   PERSISTED_UINT64_MALFORMED
};

struct PersistedUInt64Inspection
{
   PersistedUInt64State state;
   bool highExists;
   bool lowExists;
   uint highValue;
   uint lowValue;
   double highRaw;
   double lowRaw;
   bool highValueValid;
   bool lowValueValid;
   ulong restoredValue;
   string fieldName;
   string reason;
};

struct PersistedRoleInspection
{
   PersistedUInt64Inspection ticket;
   PersistedUInt64Inspection identifier;
   bool active;
   bool malformed;
   bool ticketIdentifierMismatch;
   bool numericContextWithoutIdentity;
   string role;
   string reason;
};

struct RecoveryFailureMarkerInspection
{
   bool active; bool malformed; int reasonCode; datetime failureTime; EAState originalState;
   PersistedUInt64Inspection cycleId; PersistedUInt64Inspection transactionId; PersistedUInt64Inspection eventKey;
   string reason;
};

struct CleanStartEvaluation
{
   bool stateKeyPresent; bool initialActive; bool initialMalformed; bool legacyActive; bool legacyMalformed;
   bool splitActive; bool splitMalformed; bool splitHarvestActive; bool splitHarvestMalformed;
   bool geometryActive; bool geometryMalformed; bool pendingActive; bool pendingMalformed;
   bool retryActive; bool retryMalformed; bool ledgerActive; bool ledgerMalformed;
   bool reserveTransactionActive; bool reserveTransactionMalformed; bool failureMarkerActive; bool failureMarkerMalformed;
   int managedPositions; bool cleanStartAllowed; string primaryReason; string allReasons;
};


enum PositionRole
{
   ROLE_NONE = 0,
   ROLE_INITIAL_BUY,
   ROLE_INITIAL_SELL,
   ROLE_FAR,
   ROLE_BIG_LEGACY,
   ROLE_SMALL_LEGACY,
   ROLE_BIG_CORE,
   ROLE_BIG_TREND,
   ROLE_SMALL_BASE,
   ROLE_REVERSE_SMALL
};

struct LifecycleNetResult
{
   double profit;
   double commission;
   double swap;
   double fee;
   double net;
   int dealCount;
};

enum PendingActionType
{
   PENDING_NONE = 0,
   PENDING_CLOSE_BIG_FULL,
   PENDING_CLOSE_SMALL_FULL,
   PENDING_CLOSE_BIG_CORE_FULL,
   PENDING_CLOSE_BIG_TREND_FULL,
   PENDING_CLOSE_SMALL_BASE_FULL,
   PENDING_CLOSE_REVERSE_SMALL_FULL,
   PENDING_CLOSE_BIG_CORE_PARTIAL,
   PENDING_CLOSE_OLD_FAR_FULL,
   PENDING_CLOSE_FAR_FULL,
   PENDING_CLOSE_FAR_PARTIAL,
   PENDING_CLOSE_BIG_PARTIAL,
   PENDING_OPEN_BIG,
   PENDING_OPEN_SMALL,
   PENDING_OPEN_BIG_CORE,
   PENDING_OPEN_BIG_TREND,
   PENDING_OPEN_SMALL_BASE,
   PENDING_OPEN_REVERSE_SMALL,
   PENDING_MAX_LEVELS_FINAL_CLOSE,
   PENDING_STOP_MAX_LEVELS_CLOSE
};

enum ReserveEventType
{
   RESERVE_EVENT_NONE = 0,
   RESERVE_EVENT_BIG_HARVEST_ADD,
   RESERVE_EVENT_SPLIT_BIG_HARVEST_ADD,
   RESERVE_EVENT_REVERSE_TRANSITION_ADD,
   RESERVE_EVENT_SPLIT_BIG_FINAL_DEBIT,
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
   string symbol;
   long symbolHash;
   uint symbolHashHigh;
   uint symbolHashLow;
   int symbolLength;
   ulong magicNumber;
   ulong cycleId;
   long bigIdentifier;
   long smallIdentifier;
   long farIdentifier;
   long bigCoreIdentifier;
   long bigTrendIdentifier;
   long smallBaseIdentifier;
   long reverseSmallIdentifier;
   int harvestLevel;
   int reverseCycle;
   uint eventKeyHashHigh;
   uint eventKeyHashLow;
   long eventKeyHash;
};

struct ReserveEventContextSnapshot
{
   string symbol;
   long symbolHash;
   uint symbolHashHigh;
   uint symbolHashLow;
   int symbolLength;
   ulong magicNumber;
   ulong cycleId;
   int harvestLevel;
   int reverseCycle;
   ulong bigIdentifier;
   ulong smallIdentifier;
   ulong farIdentifier;
   ulong bigCoreIdentifier;
   ulong bigTrendIdentifier;
   ulong smallBaseIdentifier;
   ulong reverseSmallIdentifier;
   ReserveEventType eventType;
};


enum RecoveryFailureReason
{
   RECOVERY_FAILURE_NONE = 0,
   RECOVERY_FAILURE_REQUIRED_FIELD_LOAD,
   RECOVERY_FAILURE_TRANSACTION_ID_SEQUENCE,
   RECOVERY_FAILURE_LEDGER_STRUCTURE,
   RECOVERY_FAILURE_TRANSACTION_CONTEXT,
   RECOVERY_FAILURE_PHASE_CONFLICT,
   RECOVERY_FAILURE_STRICT_LEDGER,
   RECOVERY_FAILURE_REQUIRED_STATE_CONTEXT,
   RECOVERY_FAILURE_STATE_INTEGRITY,
   RECOVERY_FAILURE_RECONCILIATION,
   RECOVERY_FAILURE_SYMBOL_MISMATCH,
   RECOVERY_FAILURE_OTHER
};

enum ReserveTransactionPhase
{
   RESERVE_TX_NONE = 0,
   RESERVE_TX_PREPARED,
   RESERVE_TX_LEDGER_WRITTEN,
   RESERVE_TX_CACHE_UPDATED,
   RESERVE_TX_COMPLETED
};

enum ReserveFailPoint
{
   RESERVE_FAIL_NONE = 0,
   RESERVE_FAIL_AFTER_PREPARED,
   RESERVE_FAIL_AFTER_LEDGER_WRITE,
   RESERVE_FAIL_AFTER_CACHE_UPDATE,
   RESERVE_FAIL_BEFORE_COMPLETED
};

struct ReserveTransaction
{
   bool active;
   long transactionId;
   ReserveEventType eventType;
   ReserveTransactionPhase phase;
   double amount;
   double reserveBefore;
   double reserveAfter;
   ReserveEventContextSnapshot snapshot;
   long eventKeyHash;
   uint eventKeyHashHigh;
   uint eventKeyHashLow;
   long expectedLedgerEventId;
   datetime startedAt;
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

struct FinalCloseEvaluation
{
   bool calculationValid;
   double farCloseLossWorstCase;
   double expectedCurrentHarvestNet;
   double reserveAvailable;
   double partialCarryAvailable;
   double totalCoverageAvailable;
   double projectedRecoveryPL;
   double projectedCommission;
   double projectedSpreadCost;
   double projectedSlippageCost;
   double safetyBuffer;
   bool coveragePass;
   bool recoveryPass;
   bool positionsPass;
   bool finalAllowed;
   string reason;
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
   ulong bigCoreTicket;
   ulong bigTrendTicket;
   ulong smallBaseTicket;
   ulong reverseSmallTicket;
   ulong bigCoreIdentifier;
   ulong bigTrendIdentifier;
   ulong smallBaseIdentifier;
   ulong reverseSmallIdentifier;

   double bigCoreLot;
   double bigTrendLot;
   double smallBaseLot;
   double reverseSmallLot;
   double bigCoreOpenPrice;
   double bigTrendOpenPrice;
   double smallBaseOpenPrice;
   double reverseSmallOpenPrice;
   double bigCoverageBefore;
   double bigFarLossBefore;
   double bigFarLotBefore;

   Direction bigCoreDirection;
   Direction bigTrendDirection;
   Direction smallBaseDirection;
   Direction reverseSmallDirection;

   bool splitGeometryActive;
   bool reverseConfirmed;
   bool bigTrendClosedForReverse;
   bool reverseSmallOpened;

   double reversePeakPrice;
   double reverseTriggerPrice;
   double reverseConfirmationPrice;
   double projectedReverseSmallLot;
   double projectedReverseSmallMoneyLot;
   double projectedReverseSmallDirectionLot;
   double projectedReverseSmallFinalLot;
   double projectedTransitionNet;
   double actualTransitionNet;
   double actualBigTrendNet;
   double actualSplitHarvestNet;
   bool actualSplitHarvestNetCalculated;
   double actualSmallTransitionNet;

   double bigGrossRatio;
   double bigNetExposureRatio;
   double reserveGrowthRatio;
   double newFarCompressionRatio;
   double actualBigExposureLot;
   double actualSmallExposureLot;

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
      case STATE_SPLIT_BIG_OPEN_CORE: return "STATE_SPLIT_BIG_OPEN_CORE";
      case STATE_SPLIT_BIG_OPEN_TREND: return "STATE_SPLIT_BIG_OPEN_TREND";
      case STATE_SPLIT_BIG_OPEN_SMALL_BASE: return "STATE_SPLIT_BIG_OPEN_SMALL_BASE";
      case STATE_SPLIT_GEOMETRY_ACTIVE: return "STATE_SPLIT_GEOMETRY_ACTIVE";
      case STATE_SPLIT_BIG_HARVEST_CLOSE_CORE: return "STATE_SPLIT_BIG_HARVEST_CLOSE_CORE";
      case STATE_SPLIT_BIG_HARVEST_CLOSE_TREND: return "STATE_SPLIT_BIG_HARVEST_CLOSE_TREND";
      case STATE_SPLIT_BIG_HARVEST_CLOSE_SMALL_BASE: return "STATE_SPLIT_BIG_HARVEST_CLOSE_SMALL_BASE";
      case STATE_SPLIT_BIG_HARVEST_CALC_NET: return "STATE_SPLIT_BIG_HARVEST_CALC_NET";
      case STATE_SPLIT_BIG_HARVEST_CHECK_FULL_FAR: return "STATE_SPLIT_BIG_HARVEST_CHECK_FULL_FAR";
      case STATE_SPLIT_BIG_HARVEST_PARTIAL_FAR: return "STATE_SPLIT_BIG_HARVEST_PARTIAL_FAR";
      case STATE_SPLIT_BIG_HARVEST_FINAL_CHECK: return "STATE_SPLIT_BIG_HARVEST_FINAL_CHECK";
      case STATE_BIG_HARVEST_CLOSE_SMALL: return "STATE_BIG_HARVEST_CLOSE_SMALL";
      case STATE_BIG_HARVEST_CLOSE_CORE: return "STATE_BIG_HARVEST_CLOSE_CORE";
      case STATE_BIG_HARVEST_CLOSE_TREND: return "STATE_BIG_HARVEST_CLOSE_TREND";
      case STATE_BIG_HARVEST_CLOSE_SMALL_BASE: return "STATE_BIG_HARVEST_CLOSE_SMALL_BASE";
      case STATE_BIG_HARVEST_CALC_NET: return "STATE_BIG_HARVEST_CALC_NET";
      case STATE_BIG_HARVEST_CLOSE_FAR: return "STATE_BIG_HARVEST_CLOSE_FAR";
      case STATE_BIG_HARVEST_CHECK_FINAL: return "STATE_BIG_HARVEST_CHECK_FINAL";
      case STATE_WAIT_SMALL_TO_FAR:    return "STATE_WAIT_SMALL_TO_FAR";
      case STATE_SMALL_SCENARIO:       return "STATE_SMALL_SCENARIO";
      case STATE_REVERSE_CONFIRMATION_WAIT: return "STATE_REVERSE_CONFIRMATION_WAIT";
      case STATE_REVERSE_CLOSE_BIG_TREND: return "STATE_REVERSE_CLOSE_BIG_TREND";
      case STATE_REVERSE_CALCULATE_DYNAMIC_SMALL: return "STATE_REVERSE_CALCULATE_DYNAMIC_SMALL";
      case STATE_REVERSE_OPEN_DYNAMIC_SMALL: return "STATE_REVERSE_OPEN_DYNAMIC_SMALL";
      case STATE_REVERSE_WAIT_FAR_TOUCH: return "STATE_REVERSE_WAIT_FAR_TOUCH";
      case STATE_REVERSE_SMALL_OPEN_FAILED: return "STATE_REVERSE_SMALL_OPEN_FAILED";
      case STATE_SMALL_CLOSE_SMALL:    return "STATE_SMALL_CLOSE_SMALL";
      case STATE_SMALL_CLOSE_SMALL_BASE: return "STATE_SMALL_CLOSE_SMALL_BASE";
      case STATE_SMALL_CLOSE_DYNAMIC_SMALL: return "STATE_SMALL_CLOSE_DYNAMIC_SMALL";
      case STATE_SMALL_CLOSE_OLD_FAR:  return "STATE_SMALL_CLOSE_OLD_FAR";
      case STATE_SMALL_CLOSE_BIG_PART: return "STATE_SMALL_CLOSE_BIG_PART";
      case STATE_SMALL_CLOSE_BIG_CORE_PART: return "STATE_SMALL_CLOSE_BIG_CORE_PART";
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
      case STATE_INVALID_SPLIT_GEOMETRY: return "STATE_INVALID_SPLIT_GEOMETRY";
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
      case STATE_ERROR_OPEN_BIG_CORE: return "STATE_ERROR_OPEN_BIG_CORE";
      case STATE_ERROR_OPEN_SMALL_BASE: return "STATE_ERROR_OPEN_SMALL_BASE";
      case STATE_ERROR_OPEN_BIG_TREND: return "STATE_ERROR_OPEN_BIG_TREND";
      case STATE_RECONCILIATION_ERROR: return "STATE_RECONCILIATION_ERROR";
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


string PositionRoleToCode(PositionRole role)
{
   switch(role)
   {
      case ROLE_INITIAL_BUY: return "IB";
      case ROLE_INITIAL_SELL: return "IS";
      case ROLE_FAR: return "F";
      case ROLE_BIG_LEGACY: return "BL";
      case ROLE_SMALL_LEGACY: return "SL";
      case ROLE_BIG_CORE: return "BC";
      case ROLE_BIG_TREND: return "BT";
      case ROLE_SMALL_BASE: return "SB";
      case ROLE_REVERSE_SMALL: return "RS";
      default: return "N";
   }
}

PositionRole PositionRoleFromCode(string code)
{
   if(code == "IB") return ROLE_INITIAL_BUY;
   if(code == "IS") return ROLE_INITIAL_SELL;
   if(code == "F") return ROLE_FAR;
   if(code == "BL") return ROLE_BIG_LEGACY;
   if(code == "SL") return ROLE_SMALL_LEGACY;
   if(code == "BC") return ROLE_BIG_CORE;
   if(code == "BT") return ROLE_BIG_TREND;
   if(code == "SB") return ROLE_SMALL_BASE;
   if(code == "RS") return ROLE_REVERSE_SMALL;
   return ROLE_NONE;
}

string BuildRoleComment(PositionRole role, long cycleId, int level, int reverseCycle)
{
   string comment = StringFormat("ML|%s|C%I64d|L%d|R%d", PositionRoleToCode(role), cycleId, level, reverseCycle);
   if(StringLen(comment) > 31)
      return "";
   return comment;
}

bool ParseRoleComment(string comment, PositionRole &role, long &cycleId, int &level, int &reverseCycle)
{
   role = ROLE_NONE;
   cycleId = 0;
   level = 0;
   reverseCycle = 0;
   string parts[];
   if(StringSplit(comment, '|', parts) != 5)
      return false;
   if(parts[0] != "ML")
      return false;
   role = PositionRoleFromCode(parts[1]);
   if(role == ROLE_NONE)
      return false;
   if(StringLen(parts[2]) < 2 || StringGetCharacter(parts[2], 0) != 'C')
      return false;
   if(StringLen(parts[3]) < 2 || StringGetCharacter(parts[3], 0) != 'L')
      return false;
   if(StringLen(parts[4]) < 2 || StringGetCharacter(parts[4], 0) != 'R')
      return false;
   cycleId = (long)StringToInteger(StringSubstr(parts[2], 1));
   level = (int)StringToInteger(StringSubstr(parts[3], 1));
   reverseCycle = (int)StringToInteger(StringSubstr(parts[4], 1));
   return cycleId >= 0 && level >= 0 && reverseCycle >= 0;
}

#endif // __BH_TYPES_MQH__
