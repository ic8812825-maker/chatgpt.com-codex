#ifndef __RIGHTPANEL_UI_BUTTON_MQH__
#define __RIGHTPANEL_UI_BUTTON_MQH__

class CUIButton
{
private:
   string m_name;

public:
   bool Create(const string name,const int x,const int y,const int w,const int h,const string text)
   {
      m_name=name;
      if(ObjectFind(0,m_name)>=0) ObjectDelete(0,m_name);
      if(!ObjectCreate(0,m_name,OBJ_BUTTON,0,0,0)) return false;
      ObjectSetInteger(0,m_name,OBJPROP_XDISTANCE,x);
      ObjectSetInteger(0,m_name,OBJPROP_YDISTANCE,y);
      ObjectSetInteger(0,m_name,OBJPROP_XSIZE,w);
      ObjectSetInteger(0,m_name,OBJPROP_YSIZE,h);
      ObjectSetString(0,m_name,OBJPROP_TEXT,text);
      ObjectSetInteger(0,m_name,OBJPROP_BGCOLOR,(color)0x2A2A2A);
      ObjectSetInteger(0,m_name,OBJPROP_COLOR,(color)0xD0D0D0);
      ObjectSetInteger(0,m_name,OBJPROP_BORDER_COLOR,(color)0x3A3A3A);
      ObjectSetInteger(0,m_name,OBJPROP_SELECTABLE,false);
      ObjectSetInteger(0,m_name,OBJPROP_HIDDEN,true);
      return true;
   }

   bool IsClicked(const string sparam) const { return sparam==m_name; }
   void SetActive(const bool active)
   {
      ObjectSetInteger(0,m_name,OBJPROP_BGCOLOR,active?(color)0x3A5A8A:(color)0x2A2A2A);
      ObjectSetInteger(0,m_name,OBJPROP_COLOR,active?(color)0xFFFFFF:(color)0xD0D0D0);
   }
   void SetVisible(const bool visible){ ObjectSetInteger(0,m_name,OBJPROP_TIMEFRAMES,visible?OBJ_ALL_PERIODS:OBJ_NO_PERIODS); }
   string Name(void) const { return m_name; }
};

#endif
