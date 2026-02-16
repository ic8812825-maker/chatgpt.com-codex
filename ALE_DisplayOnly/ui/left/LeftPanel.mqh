#ifndef ALE_DO_UI_LEFT_LEFTPANEL_MQH_INCLUDED
#define ALE_DO_UI_LEFT_LEFTPANEL_MQH_INCLUDED

#include <Controls\Dialog.mqh>
#include <Controls\Button.mqh>

#include "../../state/SystemState.mqh"
#include "../../state/DualState.mqh"
#include "common/UI_Button.mqh"

class CLeftPanelDialog : public CAppDialog
  {
private:
   CButton m_terminal;
   CButton m_broker_params;
   CButton m_symbol_params;
   bool    m_initialized;

public:
            CLeftPanelDialog() : m_initialized(false) {}

   bool     Init(const int x1,const int y1,const int x2,const int y2)
     {
      if(!Create(0,"ALE_LeftPanel",0,x1,y1,x2,y2))
         return(false);

      const int top=10;
      const int bw=130;
      const int bh=24;
      const int gap=8;
      const int right=x2-10;

      const int x3=right-bw;
      const int x2b=x3-gap-bw;
      const int x1b=x2b-gap-bw;

      if(!UI_Button_Create(m_terminal,0,"ALE_LeftBtn_Terminal",0,x1b,top,x1b+bw,top+bh,"Терминал"))
         return(false);
      if(!UI_Button_Create(m_broker_params,0,"ALE_LeftBtn_BrokerParams",0,x2b,top,x2b+bw,top+bh,"Параметры Брокера"))
         return(false);
      if(!UI_Button_Create(m_symbol_params,0,"ALE_LeftBtn_SymbolParams",0,x3,top,x3+bw,top+bh,"Параметры Инструмента"))
         return(false);

      Add(m_terminal);
      Add(m_broker_params);
      Add(m_symbol_params);

      Run();
      m_initialized=true;
      return(true);
     }

   void     UpdateLayout(const int x1,const int y1,const int x2,const int y2)
     {
      if(!m_initialized)
         return;

      Move(x1,y1,x2,y2);

      const int top=10;
      const int bw=130;
      const int bh=24;
      const int gap=8;
      const int right=x2-10;

      const int x3=right-bw;
      const int x2b=x3-gap-bw;
      const int x1b=x2b-gap-bw;

      m_terminal.Move(x1b,top,x1b+bw,top+bh);
      m_broker_params.Move(x2b,top,x2b+bw,top+bh);
      m_symbol_params.Move(x3,top,x3+bw,top+bh);
     }

   void     Shutdown(const int reason)
     {
      if(m_initialized)
         Destroy(reason);
      m_initialized=false;
     }
  };

CLeftPanelDialog g_left_panel;

void LeftPanel_Render(const SystemState &system_state,const DualState &dual_state)
  {
   const int chart_w=(int)ChartGetInteger(0,CHART_WIDTH_IN_PIXELS,0);
   const int chart_h=(int)ChartGetInteger(0,CHART_HEIGHT_IN_PIXELS,0);

   const int x1=0;
   const int y1=0;
   const int x2=chart_w/2;
   const int y2=chart_h;

   static bool created=false;
   if(!created)
      created=g_left_panel.Init(x1,y1,x2,y2);
   else
      g_left_panel.UpdateLayout(x1,y1,x2,y2);
  }

void LeftPanel_OnChartEvent(const int id,const long &lparam,const double &dparam,const string &sparam)
  {
   g_left_panel.ChartEvent(id,lparam,dparam,sparam);
  }

void LeftPanel_Destroy(const int reason)
  {
   g_left_panel.Shutdown(reason);
  }

#endif // ALE_DO_UI_LEFT_LEFTPANEL_MQH_INCLUDED
