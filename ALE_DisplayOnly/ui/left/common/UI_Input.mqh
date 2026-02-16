#ifndef ALE_DO_UI_LEFT_COMMON_UI_INPUT_MQH_INCLUDED
#define ALE_DO_UI_LEFT_COMMON_UI_INPUT_MQH_INCLUDED

#include <Controls\Edit.mqh>

bool UI_Input_Create(CEdit &input,
                     const long chart_id,
                     const string name,
                     const int sub_window,
                     const int x1,
                     const int y1,
                     const int x2,
                     const int y2,
                     const string value)
  {
   if(!input.Create(chart_id,name,sub_window,x1,y1,x2,y2))
      return(false);

   input.Text(value);
   return(true);
  }

#endif // ALE_DO_UI_LEFT_COMMON_UI_INPUT_MQH_INCLUDED
