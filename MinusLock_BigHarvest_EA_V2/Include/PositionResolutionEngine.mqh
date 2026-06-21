#ifndef __BH_POSITIONRESOLUTIONENGINE_MQH__
#define __BH_POSITIONRESOLUTIONENGINE_MQH__

// V2.4.19 Position Resolution Architecture.
// OpenPosition success is not enough: a new leg is registered only after ticket,
// identifier, lot, type, open price and open time are resolved from MT5.

PositionResolutionResult EmptyPositionResolutionResult()
{
   PositionResolutionResult result;
   result.resolved = false;
   result.ticket = 0;
   result.identifier = 0;
   result.lot = 0.0;
   result.type = POSITION_TYPE_BUY;
   result.openPrice = 0.0;
   result.openTime = 0;
   return result;
}

PositionResolutionResult ResolutionResultFromSnapshot(PositionSnapshot snapshot, datetime openTime)
{
   PositionResolutionResult result;
   result.resolved = snapshot.exists && snapshot.ticket != 0 && snapshot.identifier != 0 && snapshot.lot > VolumeMismatchToleranceLots;
   result.ticket = snapshot.ticket;
   result.identifier = snapshot.identifier;
   result.lot = NormalizeVolumeToStep(snapshot.lot);
   result.type = (snapshot.direction == DIR_BUY ? POSITION_TYPE_BUY : POSITION_TYPE_SELL);
   result.openPrice = snapshot.openPrice;
   result.openTime = openTime;
   return result;
}

bool PositionResolutionLotMatches(double actualLot, double expectedLot)
{
   double actual = NormalizeVolumeToStep(actualLot);
   double expected = NormalizeVolumeToStep(expectedLot);
   return MathAbs(actual - expected) <= VolumeMismatchToleranceLots;
}

bool PositionResolutionDirectionMatches(Direction actualDirection, Direction expectedDirection)
{
   return expectedDirection == DIR_NONE || actualDirection == expectedDirection;
}

bool ReadSelectedPositionResolution(PositionResolutionResult &result)
{
   PositionSnapshot snapshot;
   if(!ReadSelectedPosition(snapshot))
      return false;

   result = ResolutionResultFromSnapshot(snapshot, (datetime)PositionGetInteger(POSITION_TIME));
   return result.resolved;
}

PositionResolutionResult ResolveOpenedPosition(string comment,
                                                Direction direction,
                                                double expectedLot,
                                                ulong knownIdentifier,
                                                datetime openStartTime)
{
   LogInfo(StringFormat("POSITION_RESOLUTION_START Comment=%s Direction=%s ExpectedLot=%.2f KnownIdentifier=%I64u OpenStartTime=%I64d WindowSeconds=%d",
                        comment,
                        DirectionToString(direction),
                        expectedLot,
                        knownIdentifier,
                        (long)openStartTime,
                        PositionResolutionLookbackSeconds));

   PositionResolutionResult result = EmptyPositionResolutionResult();

   PositionSnapshot byComment;
   if(comment != "" && GetManagedPositionByComment(comment, byComment))
   {
      result = ResolutionResultFromSnapshot(byComment, TimeCurrent());
      if(result.resolved && PositionResolutionDirectionMatches(byComment.direction, direction) && PositionResolutionLotMatches(byComment.lot, expectedLot))
      {
         LogInfo(StringFormat("POSITION_RESOLUTION_BY_COMMENT Ticket=%I64u Identifier=%I64u Lot=%.2f Comment=%s", result.ticket, result.identifier, result.lot, comment));
         LogInfo(StringFormat("POSITION_RESOLUTION_PASS Ticket=%I64u Identifier=%I64u Lot=%.2f", result.ticket, result.identifier, result.lot));
         return result;
      }
   }

   if(IsInternalSimulationMode())
   {
      LogError(StringFormat("POSITION_RESOLUTION_FAIL Comment=%s Reason=simulation_comment_lookup_failed", comment));
      return result;
   }

   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;

      PositionSnapshot candidate;
      if(!ReadSelectedPosition(candidate))
         continue;

      datetime positionTime = (datetime)PositionGetInteger(POSITION_TIME);
      if(PositionResolutionDirectionMatches(candidate.direction, direction) && PositionResolutionLotMatches(candidate.lot, expectedLot))
      {
         result = ResolutionResultFromSnapshot(candidate, positionTime);
         LogInfo(StringFormat("POSITION_RESOLUTION_BY_MAGIC Ticket=%I64u Identifier=%I64u Lot=%.2f Direction=%s", result.ticket, result.identifier, result.lot, DirectionToString(candidate.direction)));
         LogInfo(StringFormat("POSITION_RESOLUTION_PASS Ticket=%I64u Identifier=%I64u Lot=%.2f", result.ticket, result.identifier, result.lot));
         return result;
      }
   }

   if(knownIdentifier != 0)
   {
      for(int i = PositionsTotal() - 1; i >= 0; i--)
      {
         ulong ticket = PositionGetTicket(i);
         if(ticket == 0 || !PositionSelectByTicket(ticket))
            continue;

         PositionSnapshot candidate;
         if(!ReadSelectedPosition(candidate))
            continue;

         if(candidate.identifier == knownIdentifier)
         {
            result = ResolutionResultFromSnapshot(candidate, (datetime)PositionGetInteger(POSITION_TIME));
            LogInfo(StringFormat("POSITION_RESOLUTION_BY_IDENTIFIER Ticket=%I64u Identifier=%I64u Lot=%.2f", result.ticket, result.identifier, result.lot));
            LogInfo(StringFormat("POSITION_RESOLUTION_PASS Ticket=%I64u Identifier=%I64u Lot=%.2f", result.ticket, result.identifier, result.lot));
            return result;
         }
      }
   }

   datetime now = TimeCurrent();
   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;

      PositionSnapshot candidate;
      if(!ReadSelectedPosition(candidate))
         continue;

      datetime positionTime = (datetime)PositionGetInteger(POSITION_TIME);
      bool openedAfterRequest = (openStartTime <= 0 || positionTime >= openStartTime - PositionResolutionLookbackSeconds);
      bool withinRecentWindow = (now - positionTime <= PositionResolutionLookbackSeconds);
      if(openedAfterRequest && withinRecentWindow && PositionResolutionDirectionMatches(candidate.direction, direction) && PositionResolutionLotMatches(candidate.lot, expectedLot))
      {
         result = ResolutionResultFromSnapshot(candidate, positionTime);
         LogInfo(StringFormat("POSITION_RESOLUTION_BY_TIME Ticket=%I64u Identifier=%I64u Lot=%.2f OpenTime=%I64d", result.ticket, result.identifier, result.lot, (long)positionTime));
         LogInfo(StringFormat("POSITION_RESOLUTION_PASS Ticket=%I64u Identifier=%I64u Lot=%.2f", result.ticket, result.identifier, result.lot));
         return result;
      }
   }

   LogError(StringFormat("POSITION_RESOLUTION_FAIL Comment=%s Direction=%s ExpectedLot=%.2f KnownIdentifier=%I64u", comment, DirectionToString(direction), expectedLot, knownIdentifier));
   return result;
}

PositionResolutionResult ResolveOpenedPositionAfterOpen(string comment,
                                                         Direction direction,
                                                         double expectedLot,
                                                         ulong knownIdentifier,
                                                         datetime openStartTime)
{
   return ResolveOpenedPosition(comment, direction, expectedLot, knownIdentifier, openStartTime);
}

bool ApplyResolvedPositionToBig(PositionResolutionResult result)
{
   if(!result.resolved || result.ticket == 0 || result.identifier == 0 || result.lot <= VolumeMismatchToleranceLots)
   {
      LogError("POSITION_RESOLUTION_FAILED Big leg could not be registered with ticket/identifier/lot");
      SetState(STATE_POSITION_RESOLUTION_ERROR, "POSITION_RESOLUTION_FAILED Big");
      return false;
   }

   Ctx.bigTicket = result.ticket;
   Ctx.bigIdentifier = result.identifier;
   Ctx.bigLot = result.lot;
   Ctx.bigOpenPrice = result.openPrice;
   Ctx.bigDirection = PositionTypeToDirection((long)result.type);
   SaveState();
   return true;
}

bool ApplyResolvedPositionToSmall(PositionResolutionResult result)
{
   if(!result.resolved || result.ticket == 0 || result.identifier == 0 || result.lot <= VolumeMismatchToleranceLots)
   {
      LogError("POSITION_RESOLUTION_FAILED Small leg could not be registered with ticket/identifier/lot");
      SetState(STATE_POSITION_RESOLUTION_ERROR, "POSITION_RESOLUTION_FAILED Small");
      return false;
   }

   Ctx.smallTicket = result.ticket;
   Ctx.smallIdentifier = result.identifier;
   Ctx.smallLot = result.lot;
   Ctx.smallOpenPrice = result.openPrice;
   Ctx.smallDirection = PositionTypeToDirection((long)result.type);
   SaveState();
   return true;
}

bool ValidatePositionResolutionContext()
{
   bool ok = true;
   if(HasBigContext() && (Ctx.bigTicket == 0 || Ctx.bigIdentifier == 0 || Ctx.bigLot <= VolumeMismatchToleranceLots))
   {
      LogError(StringFormat("POSITION_RESOLUTION_FAILED Big context unresolved Ticket=%I64u Identifier=%I64u Lot=%.2f", Ctx.bigTicket, Ctx.bigIdentifier, Ctx.bigLot));
      ok = false;
   }
   if(HasSmallContext() && (Ctx.smallTicket == 0 || Ctx.smallIdentifier == 0 || Ctx.smallLot <= VolumeMismatchToleranceLots))
   {
      LogError(StringFormat("POSITION_RESOLUTION_FAILED Small context unresolved Ticket=%I64u Identifier=%I64u Lot=%.2f", Ctx.smallTicket, Ctx.smallIdentifier, Ctx.smallLot));
      ok = false;
   }
   return ok;
}

#endif // __BH_POSITIONRESOLUTIONENGINE_MQH__
