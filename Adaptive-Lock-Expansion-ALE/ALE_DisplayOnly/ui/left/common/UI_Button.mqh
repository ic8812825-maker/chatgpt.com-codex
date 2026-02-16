#ifndef ALE_DO_UI_LEFT_COMMON_UI_BUTTON_MQH_INCLUDED
#define ALE_DO_UI_LEFT_COMMON_UI_BUTTON_MQH_INCLUDED

#include <Controls\Button.mqh>

bool UI_Button_Create(CButton &button,
                      const long chart_id,
                      const string name,
                      const int sub_window,
                      const int x1,
                      const int y1,
                      const int x2,
                      const int y2,
                      const string caption)
  {
   if(!button.Create(chart_id,name,sub_window,x1,y1,x2,y2))
      return(false);

   button.Text(caption);
   return(true);
  }

#endif // ALE_DO_UI_LEFT_COMMON_UI_BUTTON_MQH_INCLUDED
