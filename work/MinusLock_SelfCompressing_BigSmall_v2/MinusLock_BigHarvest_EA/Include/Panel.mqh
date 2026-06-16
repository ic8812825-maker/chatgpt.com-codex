#ifndef __BH_PANEL_MQH__
#define __BH_PANEL_MQH__

string PanelObjectName = "ML_BigHarvest_StatusPanel";

string PanelBool(bool value) { return value ? "true" : "false"; }

void PanelInit()
{
   ResetLastError();
   if(ObjectFind(0, PanelObjectName) < 0)
   {
      if(!ObjectCreate(0, PanelObjectName, OBJ_LABEL, 0, 0, 0))
      {
         Print("WARNING_PANEL_INIT_FAILED error=", GetLastError());
         return;
      }
   }
   ObjectSetInteger(0, PanelObjectName, OBJPROP_CORNER, CORNER_RIGHT_UPPER);
   ObjectSetInteger(0, PanelObjectName, OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER);
   ObjectSetInteger(0, PanelObjectName, OBJPROP_XDISTANCE, 10);
   ObjectSetInteger(0, PanelObjectName, OBJPROP_YDISTANCE, 15);
   ObjectSetInteger(0, PanelObjectName, OBJPROP_FONTSIZE, 8);
   ObjectSetInteger(0, PanelObjectName, OBJPROP_COLOR, clrWhite);
   ObjectSetString(0, PanelObjectName, OBJPROP_FONT, "Consolas");
   Ctx.panelState = "PANEL_INIT";
   PanelUpdate();
}

void PanelUpdate()
{
   if(ObjectFind(0, PanelObjectName) < 0)
   {
      if(!ObjectCreate(0, PanelObjectName, OBJ_LABEL, 0, 0, 0))
      {
         Print("WARNING_PANEL_UPDATE_FAILED error=", GetLastError());
         Ctx.panelState = "PANEL_WARN";
         return;
      }
      ObjectSetInteger(0, PanelObjectName, OBJPROP_CORNER, CORNER_RIGHT_UPPER);
      ObjectSetInteger(0, PanelObjectName, OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER);
      ObjectSetInteger(0, PanelObjectName, OBJPROP_XDISTANCE, 10);
      ObjectSetInteger(0, PanelObjectName, OBJPROP_YDISTANCE, 15);
   }
   string text = StringFormat(
      "MinusLock BigHarvest\nState=%s Symbol=%s MagicNumber=%I64u\nAllowRealTrading=%s UseMarketOrders=%s\nStartLot=%.2f WorkBigRatio=%.2f WorkSmallRatio=%.2f\nWorkCloseBigOnSmall=%.2f WorkRemainBigOnSmall=%.2f\nWorkCloseFarShare=%.2f WorkReserveShare=%.2f WorkFarDistanceMode=%s\nLevel=%d ReverseCycleCount=%d MaxHarvestLevels=%d MaxReverseCycles=%d\nFarTicket=%I64u FarDirection=%s FarLot=%.2f FarOpenPrice=%.5f\nEffectiveFarDistancePoints=%.1f\nBigTicket=%I64u BigDirection=%s BigLot=%.2f\nSmallTicket=%I64u SmallDirection=%s SmallLot=%.2f\nTotalReserve=%.2f InitialIgnoredProfit=%.2f\nCycleStartBalance=%.2f RealRecoveryPL=%.2f TheoreticalCyclePL=%.2f\nFinalCloseAllowed=%s\nLastSystemCloseComment=%s\nLastOpenComment=%s\nSpread=%.1f MarginPercent=%.2f\nRiskGateStatus=%s",
      StateToString(State), _Symbol, MagicNumber, PanelBool(AllowRealTrading), PanelBool(UseMarketOrders),
      StartLot, WorkBigRatio, WorkSmallRatio, WorkCloseBigOnSmall, WorkRemainBigOnSmall,
      WorkCloseFarShare, WorkReserveShare, FarDistanceModeToString(WorkFarDistanceMode),
      Ctx.harvestLevel, Ctx.reverseCycleCount, WorkMaxHarvestLevels, WorkMaxReverseCycles,
      Ctx.farTicket, DirectionToString(Ctx.farDirection), Ctx.farLot, Ctx.farOpenPrice,
      Ctx.effectiveFarDistancePoints, Ctx.bigTicket, DirectionToString(Ctx.bigDirection), Ctx.bigLot,
      Ctx.smallTicket, DirectionToString(Ctx.smallDirection), Ctx.smallLot,
      Ctx.totalReserve, Ctx.initialIgnoredProfit, Ctx.cycleStartBalance, Ctx.realRecoveryPL,
      Ctx.theoreticalCyclePL, PanelBool(Ctx.finalCloseAllowed), Ctx.lastSystemCloseComment,
      Ctx.lastOpenComment, CurrentSpreadPoints(), CurrentMarginPercent(), Ctx.riskGateStatus);
   ObjectSetString(0, PanelObjectName, OBJPROP_TEXT, text);
   Ctx.panelState = "PANEL_ONLINE";
}

void PanelDeinit()
{
   if(ObjectFind(0, PanelObjectName) >= 0)
      ObjectDelete(0, PanelObjectName);
   Ctx.panelState = "PANEL_DEINIT";
}

#endif // __BH_PANEL_MQH__
