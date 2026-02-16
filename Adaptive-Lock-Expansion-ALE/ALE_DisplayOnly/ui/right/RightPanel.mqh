#ifndef ALE_DO_UI_RIGHT_RIGHTPANEL_MQH_INCLUDED
#define ALE_DO_UI_RIGHT_RIGHTPANEL_MQH_INCLUDED

#include "../../state/SystemState.mqh"
#include "../../state/DualState.mqh"
#include "RightTabs.mqh"

void RightPanel_EnsureRectangle(const string name,const int x,const int y,const int w,const int h,const color bg)
  {
   if(ObjectFind(0,name)<0)
      ObjectCreate(0,name,OBJ_RECTANGLE_LABEL,0,0,0);

   ObjectSetInteger(0,name,OBJPROP_XDISTANCE,x);
   ObjectSetInteger(0,name,OBJPROP_YDISTANCE,y);
   ObjectSetInteger(0,name,OBJPROP_XSIZE,w);
   ObjectSetInteger(0,name,OBJPROP_YSIZE,h);
   ObjectSetInteger(0,name,OBJPROP_BGCOLOR,bg);
   ObjectSetInteger(0,name,OBJPROP_COLOR,clrDimGray);
   ObjectSetInteger(0,name,OBJPROP_BORDER_TYPE,BORDER_FLAT);
   ObjectSetInteger(0,name,OBJPROP_SELECTABLE,false);
   ObjectSetInteger(0,name,OBJPROP_HIDDEN,true);
   ObjectSetInteger(0,name,OBJPROP_ZORDER,1);
  }

void RightPanel_EnsureButton(const string name,const int x,const int y,const int w,const int h)
  {
   if(ObjectFind(0,name)<0)
      ObjectCreate(0,name,OBJ_BUTTON,0,0,0);

   ObjectSetInteger(0,name,OBJPROP_XDISTANCE,x);
   ObjectSetInteger(0,name,OBJPROP_YDISTANCE,y);
   ObjectSetInteger(0,name,OBJPROP_XSIZE,w);
   ObjectSetInteger(0,name,OBJPROP_YSIZE,h);
   ObjectSetInteger(0,name,OBJPROP_BGCOLOR,clrWhiteSmoke);
   ObjectSetInteger(0,name,OBJPROP_COLOR,clrBlack);
   ObjectSetInteger(0,name,OBJPROP_BORDER_COLOR,clrSilver);
   ObjectSetInteger(0,name,OBJPROP_SELECTABLE,false);
   ObjectSetInteger(0,name,OBJPROP_HIDDEN,true);
   ObjectSetInteger(0,name,OBJPROP_ZORDER,3);
   ObjectSetString(0,name,OBJPROP_TEXT,"");
  }

void RightPanel_Render(const SystemState &system_state,const DualState &dual_state)
  {
   const int chart_w=(int)ChartGetInteger(0,CHART_WIDTH_IN_PIXELS,0);
   const int chart_h=(int)ChartGetInteger(0,CHART_HEIGHT_IN_PIXELS,0);

   const int panel_x=chart_w/2;
   const int panel_y=0;
   const int panel_w=chart_w-panel_x;
   const int panel_h=chart_h;

   RightPanel_EnsureRectangle("ALE_RightPanel",panel_x,panel_y,panel_w,panel_h,clrAliceBlue);

   const int margin=10;
   const int spacing=6;
   const int rows=2;
   const int cols=6;
   const int btn_h=24;
   const int available_w=panel_w-margin*2-spacing*(cols-1);
   const int btn_w=(available_w>0 ? available_w/cols : 1);

   for(int row=0; row<rows; row++)
     {
      for(int col=0; col<cols; col++)
        {
         const string name=StringFormat("ALE_RightBtn_%d_%d",row,col);
         const int x=panel_x+margin+col*(btn_w+spacing);
         const int y=panel_y+margin+row*(btn_h+spacing);
         RightPanel_EnsureButton(name,x,y,btn_w,btn_h);
        }
     }
  }

#endif // ALE_DO_UI_RIGHT_RIGHTPANEL_MQH_INCLUDED
