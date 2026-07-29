double cycleLot = PositionGetDouble(POSITION_VOLUME);
bool Match(){ return PositionGetString(POSITION_SYMBOL)==_Symbol && PositionGetInteger(POSITION_MAGIC)==MagicNumber && cycleLot>0; }
