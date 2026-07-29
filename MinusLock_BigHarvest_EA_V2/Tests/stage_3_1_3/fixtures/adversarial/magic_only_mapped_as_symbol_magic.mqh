double cycleLot=PositionGetDouble(POSITION_VOLUME);
bool F(){return PositionGetInteger(POSITION_MAGIC)==MagicNumber && cycleLot>0;}
