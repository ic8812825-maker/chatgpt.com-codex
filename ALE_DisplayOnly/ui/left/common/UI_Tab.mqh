#ifndef ALE_DO_UI_LEFT_COMMON_UI_TAB_MQH_INCLUDED
#define ALE_DO_UI_LEFT_COMMON_UI_TAB_MQH_INCLUDED

#include <Controls\TabControl.mqh>

bool UI_Tab_Create(CTabControl &tab,
                   const long chart_id,
                   const string name,
                   const int sub_window,
                   const int x1,
                   const int y1,
                   const int x2,
                   const int y2)
  {
   return(tab.Create(chart_id,name,sub_window,x1,y1,x2,y2));
  }

#endif // ALE_DO_UI_LEFT_COMMON_UI_TAB_MQH_INCLUDED
