#ifndef __CALDEBUG_MQH__
#define __CALDEBUG_MQH__

// Enable extended ALE logging with: #define VP_DEBUG 1 before includes.
#ifndef VP_DEBUG
   #define VP_DEBUG 0
#endif

#if VP_DEBUG
   #define VP_DEBUG_LOG(msg) Print("[VP_DEBUG] "+(msg))
#else
   #define VP_DEBUG_LOG(msg)
#endif

#endif
