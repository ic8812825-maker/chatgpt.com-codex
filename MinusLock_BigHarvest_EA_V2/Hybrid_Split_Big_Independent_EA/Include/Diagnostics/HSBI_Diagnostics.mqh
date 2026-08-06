#ifndef HSBI_DIAGNOSTICS_MQH
#define HSBI_DIAGNOSTICS_MQH
#include "../Core/HSBI_Context.mqh"
struct HSBI_DiagnosticSnapshot{ulong cycleId;ulong stateRevision;HSBI_State state;HSBI_RuntimeMode runtimeMode;HSBI_ReasonCode lastReason;int farCount;double realizedCycleNet;double finalReserve;bool tradingImplemented;datetime timestamp;};
HSBI_DiagnosticSnapshot HSBI_BuildDiagnosticSnapshot(const HSBI_RecoveryContext &c){HSBI_DiagnosticSnapshot d;d.cycleId=c.cycleId;d.stateRevision=c.stateRevision;d.state=c.currentState;d.runtimeMode=c.runtimeMode;d.lastReason=c.lastReason;d.farCount=HSBI_CountFarRoles(c.far,c.bigCore,c.bigTrend,c.smallBase);d.realizedCycleNet=c.realizedCycleNet;d.finalReserve=c.finalReserve;d.tradingImplemented=HSBI_TRADING_IMPLEMENTED;d.timestamp=TimeCurrent();return d;}
void HSBI_UpdateDiagnosticSnapshot(const HSBI_RecoveryContext &c){HSBI_DiagnosticSnapshot d=HSBI_BuildDiagnosticSnapshot(c);Print("HSBI_DIAG|cycle=",d.cycleId,"|rev=",d.stateRevision,"|state=",d.state,"|trade=",d.tradingImplemented);}
#endif