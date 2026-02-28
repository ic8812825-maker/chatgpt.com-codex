#property strict
#property description "Virtual Position Panel (display-only)"

#include "left\\tabs\\Terminal\\CVPanel.mqh"
#include "left\\tabs\\Broker\\CBrokerTab.mqh"
#include "left\\tabs\\Symbol\\CSymbolTab.mqh"

enum ELeftTab
{
   LEFT_TAB_TERMINAL=0,
   LEFT_TAB_BROKER=1,
   LEFT_TAB_SYMBOL=2
};

CVPanel g_terminal_tab;
CBrokerTab g_broker_tab;
CSymbolTab g_symbol_tab;
ELeftTab g_active_tab=LEFT_TAB_TERMINAL;

void LayoutSidePanels()
{
   const int chart_w=(int)ChartGetInteger(0,CHART_WIDTH_IN_PIXELS);
   int panel_x=(chart_w>920 ? chart_w-330 : 560);
   if(panel_x<420) panel_x=420;

   g_broker_tab.Resize(panel_x,40,300,140);
   g_symbol_tab.Resize(panel_x,190,300,140);
}

void SetActiveLeftTab(const ELeftTab tab)
{
   g_active_tab=tab;

   const bool broker_visible=(tab==LEFT_TAB_BROKER);
   const bool symbol_visible=(tab==LEFT_TAB_SYMBOL);

   g_broker_tab.SetVisible(broker_visible);
   g_symbol_tab.SetVisible(symbol_visible);

   ObjectSetInteger(0,"ap_tab_terminal",OBJPROP_STATE,(tab==LEFT_TAB_TERMINAL));
   ObjectSetInteger(0,"ap_tab_broker",OBJPROP_STATE,(tab==LEFT_TAB_BROKER));
   ObjectSetInteger(0,"ap_tab_symbol",OBJPROP_STATE,(tab==LEFT_TAB_SYMBOL));

   ChartRedraw(0);
}

void CreateTabButtons()
{
   EnsureButton("ap_tab_terminal",10,10,80,20,"Terminal");
   EnsureButton("ap_tab_broker",94,10,80,20,"Broker");
   EnsureButton("ap_tab_symbol",178,10,80,20,"Symbol");
}

int OnInit()
{
   const int init_result=g_terminal_tab.Init();

   // left tabs: Terminal (current logic), Broker, Symbol
   g_broker_tab.Init(560,40,300,140);
   g_symbol_tab.Init(560,190,300,140);

   CreateTabButtons();
   LayoutSidePanels();
   SetActiveLeftTab(LEFT_TAB_TERMINAL);

   return init_result;
}

void OnDeinit(const int reason)
{
   DeleteByPrefix("ap_tab_");
   g_symbol_tab.Deinit();
   g_broker_tab.Deinit();
   g_terminal_tab.Deinit();
}

void OnTick()
{
   // reserved for future right-side modules
}

void OnTimer()
{
   g_terminal_tab.OnTimer();

   if(g_active_tab==LEFT_TAB_BROKER)
      g_broker_tab.Update();
   if(g_active_tab==LEFT_TAB_SYMBOL)
      g_symbol_tab.Update();
}

void OnChartEvent(const int id,const long &lparam,const double &dparam,const string &sparam)
{
   if(id==CHARTEVENT_OBJECT_CLICK)
   {
      if(sparam=="ap_tab_terminal") { SetActiveLeftTab(LEFT_TAB_TERMINAL); return; }
      if(sparam=="ap_tab_broker")   { SetActiveLeftTab(LEFT_TAB_BROKER); return; }
      if(sparam=="ap_tab_symbol")   { SetActiveLeftTab(LEFT_TAB_SYMBOL); return; }
   }

   if(id==CHARTEVENT_CHART_CHANGE)
      LayoutSidePanels();

   g_terminal_tab.OnChartEvent(id,lparam,dparam,sparam);
}
