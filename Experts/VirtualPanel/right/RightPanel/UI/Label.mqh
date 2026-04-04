#ifndef __RIGHTPANEL_UI_LABEL_MQH__
#define __RIGHTPANEL_UI_LABEL_MQH__

class CUILabel
{
private:
   string m_name;

public:
   bool Create(const string name,const int x,const int y,const string text,const color clr=(color)0xE0E0E0,const int size=9)
   {
      m_name=name;
      if(ObjectFind(0,m_name)>=0) ObjectDelete(0,m_name);
      if(!ObjectCreate(0,m_name,OBJ_LABEL,0,0,0)) return false;
      ObjectSetInteger(0,m_name,OBJPROP_XDISTANCE,x);
      ObjectSetInteger(0,m_name,OBJPROP_YDISTANCE,y);
      ObjectSetInteger(0,m_name,OBJPROP_COLOR,clr);
      ObjectSetInteger(0,m_name,OBJPROP_FONTSIZE,size);
      ObjectSetString(0,m_name,OBJPROP_FONT,"Consolas");
      ObjectSetString(0,m_name,OBJPROP_TEXT,text);
      ObjectSetInteger(0,m_name,OBJPROP_SELECTABLE,false);
      ObjectSetInteger(0,m_name,OBJPROP_HIDDEN,true);
      return true;
   }

   void SetText(const string text){ ObjectSetString(0,m_name,OBJPROP_TEXT,text); }
   void SetColor(const color clr){ ObjectSetInteger(0,m_name,OBJPROP_COLOR,clr); }
   void SetVisible(const bool visible){ ObjectSetInteger(0,m_name,OBJPROP_TIMEFRAMES,visible?OBJ_ALL_PERIODS:OBJ_NO_PERIODS); }
   string Name(void) const { return m_name; }
};

#endif
