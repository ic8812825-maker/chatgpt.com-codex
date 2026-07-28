double cycleLot=PositionGetDouble(POSITION_VOLUME);
bool F(){return PositionGetString(POSITION_SYMBOL)==_Symbol && cycleLot>0;}
