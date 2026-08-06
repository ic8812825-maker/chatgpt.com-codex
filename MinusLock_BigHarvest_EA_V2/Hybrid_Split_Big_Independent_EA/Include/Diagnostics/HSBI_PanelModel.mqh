#ifndef HSBI_PANEL_MODEL_MQH
#define HSBI_PANEL_MODEL_MQH
#include "HSBI_Diagnostics.mqh"
struct HSBI_PanelModel{string projectName;string stage;string runtimeMode;string state;string identity;string noTradeStatus;string lastReason;string moneySummary;string reconciliationSummary;};
HSBI_PanelModel HSBI_BuildPanelModel(const HSBI_RecoveryContext &c){HSBI_PanelModel p;p.projectName=HSBI_PROJECT_NAME;p.stage=HSBI_STAGE;p.runtimeMode=IntegerToString((int)c.runtimeMode);p.state=IntegerToString((int)c.currentState);p.identity=c.symbol+"/"+LongToString(c.magic)+"/"+IntegerToString((int)c.cycleId);p.noTradeStatus="TRADING_IMPLEMENTED=NO";p.lastReason=HSBI_ReasonToString(c.lastReason);p.moneySummary=DoubleToString(c.realizedCycleNet,2)+"|"+DoubleToString(c.finalReserve,2);p.reconciliationSummary=IntegerToString(c.reconciliationStatus);return p;}
#endif