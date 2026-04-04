#ifndef __RIGHTPANEL_UI_CONTAINER_MQH__
#define __RIGHTPANEL_UI_CONTAINER_MQH__

class CUIContainer
{
private:
   string m_name;
   int    m_x;
   int    m_y;
   int    m_w;
   int    m_h;
   color  m_bg;
   bool   m_visible;

public:
   CUIContainer(void): m_name(""), m_x(0), m_y(0), m_w(0), m_h(0), m_bg((color)0x1E1E1E), m_visible(true) {}

   bool Create(const string name,const int x,const int y,const int w,const int h,const color bg=(color)0x1E1E1E)
   {
      m_name=name; m_x=x; m_y=y; m_w=w; m_h=h; m_bg=bg;
      if(ObjectFind(0,m_name)>=0) ObjectDelete(0,m_name);
      if(!ObjectCreate(0,m_name,OBJ_RECTANGLE_LABEL,0,0,0)) return false;
      ObjectSetInteger(0,m_name,OBJPROP_XDISTANCE,m_x);
      ObjectSetInteger(0,m_name,OBJPROP_YDISTANCE,m_y);
      ObjectSetInteger(0,m_name,OBJPROP_XSIZE,m_w);
      ObjectSetInteger(0,m_name,OBJPROP_YSIZE,m_h);
      ObjectSetInteger(0,m_name,OBJPROP_BGCOLOR,m_bg);
      ObjectSetInteger(0,m_name,OBJPROP_COLOR,m_bg);
      ObjectSetInteger(0,m_name,OBJPROP_BORDER_TYPE,BORDER_FLAT);
      ObjectSetInteger(0,m_name,OBJPROP_SELECTABLE,false);
      ObjectSetInteger(0,m_name,OBJPROP_HIDDEN,true);
      return true;
   }

   void SetVisible(const bool visible)
   {
      m_visible=visible;
      ObjectSetInteger(0,m_name,OBJPROP_TIMEFRAMES,visible?OBJ_ALL_PERIODS:OBJ_NO_PERIODS);
   }

   int X(void) const { return m_x; }
   int Y(void) const { return m_y; }
   int W(void) const { return m_w; }
   int H(void) const { return m_h; }
   string Name(void) const { return m_name; }
};

#endif
