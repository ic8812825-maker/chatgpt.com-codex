#property strict
#property description "Virtual Position Panel (display-only)"

#include "left\tabs\Terminal\CVPanel.mqh"
#include "left\tabs\Broker\CBrokerTab.mqh"
#include "left\tabs\Symbol\CSymbolTab.mqh"

enum ELeftTab
{
LEFT_TAB_TERMINAL=0,
LEFT_TAB_BROKER=1,
LEFT_TAB_SYMBOL=2
};

// === ЕДИНЫЕ КООРДИНАТЫ ДЛЯ ВСЕХ ВКЛАДОК ===
#define PANEL_X  10
#define PANEL_Y  40
#define PANEL_W  320
#define PANEL_H  220

CVPanel    g_terminal_tab;
CBrokerTab g_broker_tab;
CSymbolTab g_symbol_tab;

ELeftTab g_active_tab=LEFT_TAB_TERMINAL;

//------------------------------------------------------------------
void SetActiveLeftTab(const ELeftTab tab)
{
g_active_tab=tab;

// скрываем всё
g_terminal_tab.SetVisible(false);
g_broker_tab.SetVisible(false);
g_symbol_tab.SetVisible(false);

// показываем нужную вкладку
if(tab==LEFT_TAB_TERMINAL) g_terminal_tab.SetVisible(true);
if(tab==LEFT_TAB_BROKER)   g_broker_tab.SetVisible(true);
if(tab==LEFT_TAB_SYMBOL)   g_symbol_tab.SetVisible(true);

// подсветка кнопок
ObjectSetInteger(0,"ap_tab_terminal",OBJPROP_STATE,(tab==LEFT_TAB_TERMINAL));
ObjectSetInteger(0,"ap_tab_broker",OBJPROP_STATE,(tab==LEFT_TAB_BROKER));
ObjectSetInteger(0,"ap_tab_symbol",OBJPROP_STATE,(tab==LEFT_TAB_SYMBOL));

ChartRedraw(0);
}

//------------------------------------------------------------------
void CreateTabButtons()
{
EnsureButton("ap_tab_terminal",10,10,90,22,"Terminal");
EnsureButton("ap_tab_broker",105,10,90,22,"Broker");
EnsureButton("ap_tab_symbol",200,10,90,22,"Symbol");
}

//------------------------------------------------------------------
int OnInit()
{
// Terminal
const int result=g_terminal_tab.Init(PANEL_X,PANEL_Y,PANEL_W,PANEL_H);

// Broker
g_broker_tab.Init(PANEL_X,PANEL_Y,PANEL_W,PANEL_H);
g_broker_tab.SetVisible(false);

// Symbol
g_symbol_tab.Init(PANEL_X,PANEL_Y,PANEL_W,PANEL_H);
g_symbol_tab.SetVisible(false);

CreateTabButtons();
SetActiveLeftTab(LEFT_TAB_TERMINAL);

return result;
}

//------------------------------------------------------------------
void OnDeinit(const int reason)
{
DeleteByPrefix("ap_tab_");

g_symbol_tab.Deinit();
g_broker_tab.Deinit();
g_terminal_tab.Deinit();
}

//------------------------------------------------------------------
void OnTimer()
{
// обновляем только активную вкладку
if(g_active_tab==LEFT_TAB_TERMINAL)
g_terminal_tab.OnTimer();

if(g_active_tab==LEFT_TAB_BROKER)
g_broker_tab.Update();

if(g_active_tab==LEFT_TAB_SYMBOL)
g_symbol_tab.Update();
}

//------------------------------------------------------------------
void OnChartEvent(const int id,const long &lparam,const double &dparam,const string &sparam)
{
if(id==CHARTEVENT_OBJECT_CLICK)
{
if(sparam=="ap_tab_terminal"){ SetActiveLeftTab(LEFT_TAB_TERMINAL); return; }
if(sparam=="ap_tab_broker")  { SetActiveLeftTab(LEFT_TAB_BROKER); return; }
if(sparam=="ap_tab_symbol")  { SetActiveLeftTab(LEFT_TAB_SYMBOL); return; }
}

g_terminal_tab.OnChartEvent(id,lparam,dparam,sparam);
}
