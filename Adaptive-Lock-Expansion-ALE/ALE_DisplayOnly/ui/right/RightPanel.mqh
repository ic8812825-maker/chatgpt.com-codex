#ifndef ALE_DO_UI_RIGHT_RIGHTPANEL_MQH_INCLUDED
#define ALE_DO_UI_RIGHT_RIGHTPANEL_MQH_INCLUDED

#include <Controls\Dialog.mqh>
#include <Controls\Button.mqh>

#include "../../state/SystemState.mqh"
#include "../../state/DualState.mqh"
#include "../left/common/UI_Button.mqh"
#include "RightTabs.mqh"

class CRightPanelDialog : public CAppDialog
  {
private:
   CButton m_buttons[12];
   bool    m_initialized;

public:
            CRightPanelDialog() : m_initialized(false) {}

   bool     Init(const int x1,const int y1,const int x2,const int y2)
     {
      if(!Create(0,"ALE_RightPanel",0,x1,y1,x2,y2))
         return(false);

      const int margin=10;
      const int spacing=6;
      const int rows=2;
      const int cols=6;
      const int h=24;
      const int width=(x2-x1)-margin*2-spacing*(cols-1);
      const int w=(width>0 ? width/cols : 1);

      for(int r=0; r<rows; r++)
        {
         for(int c=0; c<cols; c++)
           {
            const int idx=r*cols+c;
            const int bx=x1+margin+c*(w+spacing);
            const int by=y1+margin+r*(h+spacing);
            const string name=StringFormat("ALE_RightBtn_%d_%d",r,c);

            if(!UI_Button_Create(m_buttons[idx],0,name,0,bx,by,bx+w,by+h,""))
               return(false);

            Add(m_buttons[idx]);
           }
        }

      Run();
      m_initialized=true;
      return(true);
     }

   void     UpdateLayout(const int x1,const int y1,const int x2,const int y2)
     {
      // Terminal build exposes only 2-arg Move overloads for these controls.
      // Keep initial geometry set during Init.
     }

   void     Shutdown(const int reason)
     {
      if(m_initialized)
         Destroy(reason);
      m_initialized=false;
     }
  };

CRightPanelDialog g_right_panel;

void RightPanel_Render(const SystemState &system_state,const DualState &dual_state)
  {
   const int chart_w=(int)ChartGetInteger(0,CHART_WIDTH_IN_PIXELS,0);
   const int chart_h=(int)ChartGetInteger(0,CHART_HEIGHT_IN_PIXELS,0);

   const int x1=chart_w/2;
   const int y1=0;
   const int x2=chart_w;
   const int y2=chart_h;

   static bool created=false;
   if(!created)
      created=g_right_panel.Init(x1,y1,x2,y2);
   else
      g_right_panel.UpdateLayout(x1,y1,x2,y2);

   const int tabs_x1=x1+10;
   const int tabs_y1=y1+70;
   const int tabs_x2=x2-10;
   const int tabs_y2=y2-10;
   RightTabs_Render(system_state,dual_state,tabs_x1,tabs_y1,tabs_x2,tabs_y2);
  }

void RightPanel_OnChartEvent(const int id,const long &lparam,const double &dparam,const string &sparam)
  {
   g_right_panel.ChartEvent(id,lparam,dparam,sparam);
   RightTabs_OnChartEvent(id,lparam,dparam,sparam);
  }

void RightPanel_Destroy(const int reason)
  {
   RightTabs_Destroy(reason);
   g_right_panel.Shutdown(reason);
  }

#endif // ALE_DO_UI_RIGHT_RIGHTPANEL_MQH_INCLUDED
