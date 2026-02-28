#ifndef __UIHELPERS_MQH__
#define __UIHELPERS_MQH__

#include "..\\constants\\PanelConstants.mqh"

void DeleteByPrefix(const string prefix)
{
   const int total=ObjectsTotal(0,0,-1);
   for(int i=total-1;i>=0;i--)
   {
      const string name=ObjectName(0,i,0,-1);
      if(StringFind(name,prefix)==0)
         ObjectDelete(0,name);
   }
}

void EnsureLabel(const string name,const int x,const int y,const int w,const string text,const color clr=clrWhite)
{
   if(ObjectFind(0,name)<0)
      ObjectCreate(0,name,OBJ_LABEL,0,0,0);

   ObjectSetInteger(0,name,OBJPROP_CORNER,CORNER);
   ObjectSetInteger(0,name,OBJPROP_XDISTANCE,x);
   ObjectSetInteger(0,name,OBJPROP_YDISTANCE,y);
   ObjectSetInteger(0,name,OBJPROP_XSIZE,w);
   ObjectSetInteger(0,name,OBJPROP_FONTSIZE,VP_FONT_SIZE);
   ObjectSetString(0,name,OBJPROP_FONT,"Tahoma");
   ObjectSetString(0,name,OBJPROP_TEXT,text);
   ObjectSetInteger(0,name,OBJPROP_COLOR,clr);
}

void EnsureButton(const string name,const int x,const int y,const int w,const int h,const string text)
{
   if(ObjectFind(0,name)<0)
      ObjectCreate(0,name,OBJ_BUTTON,0,0,0);

   ObjectSetInteger(0,name,OBJPROP_CORNER,CORNER);
   ObjectSetInteger(0,name,OBJPROP_XDISTANCE,x);
   ObjectSetInteger(0,name,OBJPROP_YDISTANCE,y);
   ObjectSetInteger(0,name,OBJPROP_XSIZE,w);
   ObjectSetInteger(0,name,OBJPROP_YSIZE,h);
   ObjectSetInteger(0,name,OBJPROP_FONTSIZE,VP_FONT_SIZE);
   ObjectSetString(0,name,OBJPROP_FONT,"Tahoma");
   ObjectSetString(0,name,OBJPROP_TEXT,text);
}

void EnsureEdit(const string name,const int x,const int y,const int w,const int h,const string text)
{
   if(ObjectFind(0,name)<0)
      ObjectCreate(0,name,OBJ_EDIT,0,0,0);

   ObjectSetInteger(0,name,OBJPROP_CORNER,CORNER);
   ObjectSetInteger(0,name,OBJPROP_XDISTANCE,x);
   ObjectSetInteger(0,name,OBJPROP_YDISTANCE,y);
   ObjectSetInteger(0,name,OBJPROP_XSIZE,w);
   ObjectSetInteger(0,name,OBJPROP_YSIZE,h);
   ObjectSetInteger(0,name,OBJPROP_FONTSIZE,VP_FONT_SIZE);
   ObjectSetString(0,name,OBJPROP_FONT,"Tahoma");
   ObjectSetString(0,name,OBJPROP_TEXT,text);
}

#endif // __UIHELPERS_MQH__
