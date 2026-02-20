#ifndef ALE_DO_UI_LEFT_LEFTPANEL_MQH_INCLUDED
#define ALE_DO_UI_LEFT_LEFTPANEL_MQH_INCLUDED

#include <Controls\Dialog.mqh>
#include <Controls\Button.mqh>
#include <Controls\Edit.mqh>
#include <Controls\Label.mqh>

#include "../../state/SystemState.mqh"
#include "../../state/DualState.mqh"
#include "../../book/VirtualPosition.mqh"
#include "common/UI_Button.mqh"
#include "common/UI_Input.mqh"
#include "components/VirtualPositionManager.mqh"

enum EVirtualPanelTab
  {
   TAB_TERMINAL=0,
   TAB_BROKER=1,
   TAB_SYMBOL=2
  };

class BrokerConfig
  {
public:
   double leverage;
   double stop_out;
   double margin_call;

          BrokerConfig() : leverage(0.0),stop_out(0.0),margin_call(0.0) {}
  };

class SymbolConfig
  {
public:
   double point;
   double tick_size;
   double tick_value;
   double vol_min;
   double vol_max;
   double vol_step;

          SymbolConfig() : point(0.0),tick_size(0.0),tick_value(0.0),vol_min(0.0),vol_max(0.0),vol_step(0.0) {}
  };

class CBrokerTab
  {
private:
   CLabel m_title;
   CEdit  m_leverage;
   CEdit  m_stop_out;
   CEdit  m_margin_call;
   CButton m_reset;
   CButton m_save;
   bool    m_initialized;

public:
   BrokerConfig config;

            CBrokerTab() : m_initialized(false) {}

   bool     Init(CAppDialog &dlg,const int x,const int y)
     {
      if(m_initialized)
         return(true);

      if(!m_title.Create(0,"ALE_Broker_Title",0,x,y,x+250,y+20)) return(false);
      m_title.Text("Broker parameters");
      if(!UI_Input_Create(&m_leverage,0,"ALE_Broker_Leverage",0,x,y+24,x+220,y+44,"0")) return(false);
      if(!UI_Input_Create(&m_stop_out,0,"ALE_Broker_StopOut",0,x,y+50,x+220,y+70,"0")) return(false);
      if(!UI_Input_Create(&m_margin_call,0,"ALE_Broker_MarginCall",0,x,y+76,x+220,y+96,"0")) return(false);
      if(!UI_Button_Create(m_reset,0,"ALE_Broker_Reset",0,x,y+106,x+100,y+130,"Сбросить")) return(false);
      if(!UI_Button_Create(m_save,0,"ALE_Broker_Save",0,x+120,y+106,x+220,y+130,"Сохранить")) return(false);

      dlg.Add(m_title); dlg.Add(m_leverage); dlg.Add(m_stop_out); dlg.Add(m_margin_call); dlg.Add(m_reset); dlg.Add(m_save);
      LoadFromTerminal();
      m_initialized=true;
      return(true);
     }

   void     LoadFromTerminal()
     {
      config.leverage=(double)AccountInfoInteger(ACCOUNT_LEVERAGE);
      config.stop_out=AccountInfoDouble(ACCOUNT_MARGIN_SO_SO);
      config.margin_call=AccountInfoDouble(ACCOUNT_MARGIN_SO_CALL);
      m_leverage.Text(DoubleToString(config.leverage,2));
      m_stop_out.Text(DoubleToString(config.stop_out,2));
      m_margin_call.Text(DoubleToString(config.margin_call,2));
     }

   void     SaveToMemory()
     {
      config.leverage=StringToDouble(m_leverage.Text());
      config.stop_out=StringToDouble(m_stop_out.Text());
      config.margin_call=StringToDouble(m_margin_call.Text());
     }
  };

class CSymbolTab
  {
private:
   CLabel  m_title;
   CEdit   m_point;
   CEdit   m_tick_size;
   CEdit   m_tick_value;
   CEdit   m_vol_min;
   CEdit   m_vol_max;
   CEdit   m_vol_step;
   CButton m_reset;
   CButton m_save;
   bool    m_initialized;

public:
   SymbolConfig config;

            CSymbolTab() : m_initialized(false) {}

   bool     Init(CAppDialog &dlg,const int x,const int y)
     {
      if(m_initialized)
         return(true);

      if(!m_title.Create(0,"ALE_Symbol_Title",0,x,y,x+250,y+20)) return(false);
      m_title.Text("Symbol parameters");
      if(!UI_Input_Create(&m_point,0,"ALE_Symbol_Point",0,x,y+24,x+220,y+44,"0")) return(false);
      if(!UI_Input_Create(&m_tick_size,0,"ALE_Symbol_TickSize",0,x,y+50,x+220,y+70,"0")) return(false);
      if(!UI_Input_Create(&m_tick_value,0,"ALE_Symbol_TickValue",0,x,y+76,x+220,y+96,"0")) return(false);
      if(!UI_Input_Create(&m_vol_min,0,"ALE_Symbol_VolMin",0,x,y+102,x+220,y+122,"0")) return(false);
      if(!UI_Input_Create(&m_vol_max,0,"ALE_Symbol_VolMax",0,x,y+128,x+220,y+148,"0")) return(false);
      if(!UI_Input_Create(&m_vol_step,0,"ALE_Symbol_VolStep",0,x,y+154,x+220,y+174,"0")) return(false);
      if(!UI_Button_Create(m_reset,0,"ALE_Symbol_Reset",0,x,y+184,x+100,y+208,"Сбросить")) return(false);
      if(!UI_Button_Create(m_save,0,"ALE_Symbol_Save",0,x+120,y+184,x+220,y+208,"Сохранить")) return(false);

      dlg.Add(m_title); dlg.Add(m_point); dlg.Add(m_tick_size); dlg.Add(m_tick_value); dlg.Add(m_vol_min); dlg.Add(m_vol_max); dlg.Add(m_vol_step); dlg.Add(m_reset); dlg.Add(m_save);
      LoadFromSymbol();
      m_initialized=true;
      return(true);
     }

   void     LoadFromSymbol()
     {
      config.point=SymbolInfoDouble(_Symbol,SYMBOL_POINT);
      config.tick_size=SymbolInfoDouble(_Symbol,SYMBOL_TRADE_TICK_SIZE);
      config.tick_value=SymbolInfoDouble(_Symbol,SYMBOL_TRADE_TICK_VALUE);
      config.vol_min=SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_MIN);
      config.vol_max=SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_MAX);
      config.vol_step=SymbolInfoDouble(_Symbol,SYMBOL_VOLUME_STEP);

      m_point.Text(DoubleToString(config.point,8));
      m_tick_size.Text(DoubleToString(config.tick_size,8));
      m_tick_value.Text(DoubleToString(config.tick_value,8));
      m_vol_min.Text(DoubleToString(config.vol_min,2));
      m_vol_max.Text(DoubleToString(config.vol_max,2));
      m_vol_step.Text(DoubleToString(config.vol_step,2));
     }

   void     SaveToMemory()
     {
      config.point=StringToDouble(m_point.Text());
      config.tick_size=StringToDouble(m_tick_size.Text());
      config.tick_value=StringToDouble(m_tick_value.Text());
      config.vol_min=StringToDouble(m_vol_min.Text());
      config.vol_max=StringToDouble(m_vol_max.Text());
      config.vol_step=StringToDouble(m_vol_step.Text());
     }
  };

class CTerminalTab
  {
private:
   CLabel  m_title;
   CEdit   m_price_buy;
   CEdit   m_lot_buy;
   CEdit   m_comment_buy;
   CButton m_type_buy;
   CButton m_auto_buy;
   CButton m_clear_buy;
   CButton m_add_buy;

   CEdit   m_price_sell;
   CEdit   m_lot_sell;
   CEdit   m_comment_sell;
   CButton m_type_sell;
   CButton m_auto_sell;
   CButton m_clear_sell;
   CButton m_add_sell;

   CLabel  m_info;
   bool    m_initialized;
   bool    m_auto_price_buy;
   bool    m_auto_price_sell;

public:
   CVirtualPositionManager manager;

            CTerminalTab() : m_initialized(false),m_auto_price_buy(true),m_auto_price_sell(true) {}

   bool     Init(CAppDialog &dlg,const int x,const int y)
     {
      if(m_initialized)
         return(true);

      if(!m_title.Create(0,"ALE_Terminal_Title",0,x,y,x+320,y+20)) return(false);
      m_title.Text("Terminal / Virtual Position Panel");

      if(!UI_Input_Create(&m_price_buy,0,"ALE_Terminal_PriceBuy",0,x,y+24,x+95,y+44,"0")) return(false);
      if(!UI_Input_Create(&m_lot_buy,0,"ALE_Terminal_LotBuy",0,x+100,y+24,x+165,y+44,"0.01")) return(false);
      if(!UI_Input_Create(&m_comment_buy,0,"ALE_Terminal_CommentBuy",0,x+170,y+24,x+320,y+44,"")) return(false);
      if(!UI_Button_Create(m_type_buy,0,"ALE_Terminal_TypeBuy",0,x,y+48,x+90,y+72,"BUY")) return(false);
      if(!UI_Button_Create(m_auto_buy,0,"ALE_Terminal_AutoBuy",0,x+95,y+48,x+130,y+72,"A")) return(false);
      if(!UI_Button_Create(m_clear_buy,0,"ALE_Terminal_ClearBuy",0,x+135,y+48,x+220,y+72,"Очистить")) return(false);
      if(!UI_Button_Create(m_add_buy,0,"ALE_Terminal_AddBuy",0,x+225,y+48,x+320,y+72,"Добавить")) return(false);

      if(!UI_Input_Create(&m_price_sell,0,"ALE_Terminal_PriceSell",0,x,y+86,x+95,y+106,"0")) return(false);
      if(!UI_Input_Create(&m_lot_sell,0,"ALE_Terminal_LotSell",0,x+100,y+86,x+165,y+106,"0.01")) return(false);
      if(!UI_Input_Create(&m_comment_sell,0,"ALE_Terminal_CommentSell",0,x+170,y+86,x+320,y+106,"")) return(false);
      if(!UI_Button_Create(m_type_sell,0,"ALE_Terminal_TypeSell",0,x,y+110,x+90,y+134,"SELL")) return(false);
      if(!UI_Button_Create(m_auto_sell,0,"ALE_Terminal_AutoSell",0,x+95,y+110,x+130,y+134,"A")) return(false);
      if(!UI_Button_Create(m_clear_sell,0,"ALE_Terminal_ClearSell",0,x+135,y+110,x+220,y+134,"Очистить")) return(false);
      if(!UI_Button_Create(m_add_sell,0,"ALE_Terminal_AddSell",0,x+225,y+110,x+320,y+134,"Добавить")) return(false);

      if(!m_info.Create(0,"ALE_Terminal_Info",0,x,y+142,x+340,y+162)) return(false);
      m_info.Text("Positions: 0 / 100");

      dlg.Add(m_title);
      dlg.Add(m_price_buy); dlg.Add(m_lot_buy); dlg.Add(m_comment_buy); dlg.Add(m_type_buy); dlg.Add(m_auto_buy); dlg.Add(m_clear_buy); dlg.Add(m_add_buy);
      dlg.Add(m_price_sell); dlg.Add(m_lot_sell); dlg.Add(m_comment_sell); dlg.Add(m_type_sell); dlg.Add(m_auto_sell); dlg.Add(m_clear_sell); dlg.Add(m_add_sell);
      dlg.Add(m_info);

      m_initialized=true;
      return(true);
     }

   void     OnTick()
     {
      if(!m_initialized)
         return;

      if(m_auto_price_buy)
         m_price_buy.Text(DoubleToString(SymbolInfoDouble(_Symbol,SYMBOL_ASK),_Digits));
      if(m_auto_price_sell)
         m_price_sell.Text(DoubleToString(SymbolInfoDouble(_Symbol,SYMBOL_BID),_Digits));

      m_info.Text(StringFormat("Positions: %d / 100",manager.Count()));
     }

   void     AddPosition(const int stream,const ENUM_ORDER_TYPE type,CEdit &price_edit,CEdit &lot_edit,CEdit &comment_edit)
     {
      const double price=StringToDouble(price_edit.Text());
      const double lot=StringToDouble(lot_edit.Text());
      if(!manager.Add(stream,type,price,lot,comment_edit.Text()))
         MessageBox(manager.LastError(),"VPP",MB_OK);
     }
  };

class CALEBridge
  {
private:
   int m_count;

public:
            CALEBridge() : m_count(0) {}

   void     Bind(CVirtualPositionManager &manager)
     {
      m_count=manager.Count();
     }

   int      Count() const
     {
      return(m_count);
     }
  };

class CVirtualPanel : public CAppDialog
  {
private:
   CButton        m_tab_terminal;
   CButton        m_tab_broker;
   CButton        m_tab_symbol;
   EVirtualPanelTab m_active_tab;
   bool           m_initialized;

   CBrokerTab     m_broker_tab;
   CSymbolTab     m_symbol_tab;
   CTerminalTab   m_terminal_tab;
   CALEBridge     m_ale_bridge;

public:
                 CVirtualPanel() : m_active_tab(TAB_TERMINAL),m_initialized(false) {}

   bool          Init(const int x1,const int y1,const int x2,const int y2)
     {
      if(!Create(0,"ALE_LeftPanel",0,x1,y1,x2,y2))
         return(false);

      if(!UI_Button_Create(m_tab_terminal,0,"ALE_Tab_Terminal",0,10,8,110,30,"Терминал")) return(false);
      if(!UI_Button_Create(m_tab_broker,0,"ALE_Tab_Broker",0,115,8,210,30,"Брокер")) return(false);
      if(!UI_Button_Create(m_tab_symbol,0,"ALE_Tab_Symbol",0,215,8,320,30,"Инструмент")) return(false);

      Add(m_tab_terminal); Add(m_tab_broker); Add(m_tab_symbol);
      m_terminal_tab.Init(*this,10,40);
      m_broker_tab.Init(*this,10,40);
      m_symbol_tab.Init(*this,10,40);

      m_ale_bridge.Bind(m_terminal_tab.manager);
      Run();
      m_initialized=true;
      return(true);
     }

   void          Render(const SystemState &system_state,const DualState &dual_state)
     {
      if(!m_initialized)
         return;
      m_terminal_tab.OnTick();
     }

   void          Shutdown(const int reason)
     {
      if(m_initialized)
         Destroy(reason);
      m_initialized=false;
     }
  };

CVirtualPanel *LeftPanel_Instance()
  {
   static CVirtualPanel panel;
   return(GetPointer(panel));
  }

void LeftPanel_Render(const SystemState &system_state,const DualState &dual_state)
  {
   const int chart_w=(int)ChartGetInteger(0,CHART_WIDTH_IN_PIXELS,0);
   const int chart_h=(int)ChartGetInteger(0,CHART_HEIGHT_IN_PIXELS,0);
   if(chart_w<200 || chart_h<120)
      return;

   CVirtualPanel *panel=LeftPanel_Instance();
   if(CheckPointer(panel)==POINTER_INVALID)
      return;

   static bool created=false;
   if(!created)
      created=panel.Init(0,0,chart_w/2,chart_h);

   panel.Render(system_state,dual_state);
  }

void LeftPanel_OnChartEvent(const int id,const long &lparam,const double &dparam,const string &sparam)
  {
   CVirtualPanel *panel=LeftPanel_Instance();
   if(CheckPointer(panel)==POINTER_INVALID)
      return;
   panel.ChartEvent(id,lparam,dparam,sparam);
  }

void LeftPanel_Destroy(const int reason)
  {
   CVirtualPanel *panel=LeftPanel_Instance();
   if(CheckPointer(panel)==POINTER_INVALID)
      return;
   panel.Shutdown(reason);
  }

#endif // ALE_DO_UI_LEFT_LEFTPANEL_MQH_INCLUDED
