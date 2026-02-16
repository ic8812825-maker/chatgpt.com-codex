#pragma once

#include "../../state/SystemState.mqh"
#include "../../state/DualState.mqh"
#include "components/PositionTable.mqh"
#include "components/AddPositionForm.mqh"
#include "components/BalanceInfo.mqh"

void LeftPanel_EnsureRectangle(const string name,const int x,const int y,const int w,const int h,const color bg)
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

void LeftPanel_EnsureButton(const string name,const string caption,const int x,const int y,const int w,const int h)
  {
   if(ObjectFind(0,name)<0)
      ObjectCreate(0,name,OBJ_BUTTON,0,0,0);

   ObjectSetInteger(0,name,OBJPROP_XDISTANCE,x);
   ObjectSetInteger(0,name,OBJPROP_YDISTANCE,y);
   ObjectSetInteger(0,name,OBJPROP_XSIZE,w);
   ObjectSetInteger(0,name,OBJPROP_YSIZE,h);
   ObjectSetInteger(0,name,OBJPROP_BGCOLOR,clrGainsboro);
   ObjectSetInteger(0,name,OBJPROP_COLOR,clrBlack);
   ObjectSetInteger(0,name,OBJPROP_BORDER_COLOR,clrGray);
   ObjectSetInteger(0,name,OBJPROP_SELECTABLE,false);
   ObjectSetInteger(0,name,OBJPROP_HIDDEN,true);
   ObjectSetInteger(0,name,OBJPROP_ZORDER,3);
   ObjectSetString(0,name,OBJPROP_TEXT,caption);
  }

void LeftPanel_Render(const SystemState &system_state,const DualState &dual_state)
  {
   const int chart_w=(int)ChartGetInteger(0,CHART_WIDTH_IN_PIXELS,0);
   const int chart_h=(int)ChartGetInteger(0,CHART_HEIGHT_IN_PIXELS,0);

   const int panel_x=0;
   const int panel_y=0;
   const int panel_w=chart_w/2;
   const int panel_h=chart_h;

   LeftPanel_EnsureRectangle("ALE_LeftPanel",panel_x,panel_y,panel_w,panel_h,clrLavender);

   const int gap=8;
   const int btn_w=130;
   const int btn_h=24;
   const int top_y=10;
   const int right_edge=panel_x+panel_w-10;

   const int b3_x=right_edge-btn_w;
   const int b2_x=b3_x-gap-btn_w;
   const int b1_x=b2_x-gap-btn_w;

   LeftPanel_EnsureButton("ALE_LeftBtn_Terminal","Терминал",b1_x,top_y,btn_w,btn_h);
   LeftPanel_EnsureButton("ALE_LeftBtn_BrokerParams","Параметры Брокера",b2_x,top_y,btn_w,btn_h);
   LeftPanel_EnsureButton("ALE_LeftBtn_SymbolParams","Параметры Инструмента",b3_x,top_y,btn_w,btn_h);
  }
