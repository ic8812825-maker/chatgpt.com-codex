# STRESS / MONTE-CARLO / MULTI-CYCLE TESTING
- account_balance: 10000.0
- MaxTotalLot: 20
- MaxNetLot: 10
- MaxActiveSections: 4

## Violation rules checked
- tail_close_loss > recovery_fund
- section_closed_with_cycle_profit <= 0
- close_lot > tail_lot
- active_sections > max_active_sections
- total_lot > max_total_lot
- net_lot > max_net_lot
- opposite_cascade_opened
- recovery_fund_negative
- reserve_negative
- tail_lot_negative

## trend_up
- steps: 1000
- opens: 4
- closes: 0
- tail_lot_start: 1.0
- tail_lot_end: 1.0
- reserve_start: 0.0
- reserve_end: 0.0
- recovery_start: 0.0
- recovery_end: 0.0
- max_floating_loss: -18180.38
- max_drawdown_money: 18180.38
- max_drawdown_percent: 181.8
- max_total_lot: 4.2
- max_net_lot: 1.0
- max_active_sections: 4
- max_consecutive_no_close_steps: 1000
- violations_count: 0
- final_status: PASS_SAFE_STALL
- tail_reduction: 0.0
- reserve_generated: 0.0
- recovery_cycles_count: 0
- limit_total_used_percent: 21.0
- limit_net_used_percent: 10.0

### Event trace (first 10)
- step 1 price=1.242 event=OPEN_SECTION tail=1.0 sec=1 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-
- step 2 price=1.242 event=OPEN_SECTION tail=1.0 sec=2 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-
- step 3 price=1.242 event=OPEN_SECTION tail=1.0 sec=3 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-
- step 4 price=1.242 event=OPEN_SECTION tail=1.0 sec=4 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-
- step 5 price=1.242 event=WAIT tail=1.0 sec=4 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-
- step 6 price=1.242 event=WAIT tail=1.0 sec=4 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-
- step 7 price=1.241 event=WAIT tail=1.0 sec=4 cycle=-17.58 rec=0.0 res=0.0 close=0.0 violation=-
- step 8 price=1.242 event=WAIT tail=1.0 sec=4 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-
- step 9 price=1.244 event=WAIT tail=1.0 sec=4 cycle=-17.8 rec=0.0 res=0.0 close=0.0 violation=-
- step 10 price=1.242 event=WAIT tail=1.0 sec=4 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-

### Event trace (last 10)
- step 991 price=1.242 event=WAIT tail=1.0 sec=4 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-
- step 992 price=1.242 event=WAIT tail=1.0 sec=4 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-
- step 993 price=1.242 event=WAIT tail=1.0 sec=4 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-
- step 994 price=1.241 event=WAIT tail=1.0 sec=4 cycle=-17.58 rec=0.0 res=0.0 close=0.0 violation=-
- step 995 price=1.242 event=WAIT tail=1.0 sec=4 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-
- step 996 price=1.242 event=WAIT tail=1.0 sec=4 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-
- step 997 price=1.242 event=WAIT tail=1.0 sec=4 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-
- step 998 price=1.242 event=WAIT tail=1.0 sec=4 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-
- step 999 price=1.244 event=WAIT tail=1.0 sec=4 cycle=-17.8 rec=0.0 res=0.0 close=0.0 violation=-
- step 1000 price=1.242 event=WAIT tail=1.0 sec=4 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-

### Violation events
- none

## trend_down
- steps: 1000
- opens: 4
- closes: 0
- tail_lot_start: 1.0
- tail_lot_end: 1.0
- reserve_start: 0.0
- reserve_end: 0.0
- recovery_start: 0.0
- recovery_end: 0.0
- max_floating_loss: -18180.38
- max_drawdown_money: 18180.38
- max_drawdown_percent: 181.8
- max_total_lot: 4.2
- max_net_lot: 1.0
- max_active_sections: 4
- max_consecutive_no_close_steps: 1000
- violations_count: 0
- final_status: PASS_SAFE_STALL
- tail_reduction: 0.0
- reserve_generated: 0.0
- recovery_cycles_count: 0
- limit_total_used_percent: 21.0
- limit_net_used_percent: 10.0

### Event trace (first 10)
- step 1 price=1.218 event=OPEN_SECTION tail=1.0 sec=1 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-
- step 2 price=1.218 event=OPEN_SECTION tail=1.0 sec=2 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-
- step 3 price=1.218 event=OPEN_SECTION tail=1.0 sec=3 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-
- step 4 price=1.218 event=OPEN_SECTION tail=1.0 sec=4 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-
- step 5 price=1.218 event=WAIT tail=1.0 sec=4 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-
- step 6 price=1.218 event=WAIT tail=1.0 sec=4 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-
- step 7 price=1.219 event=WAIT tail=1.0 sec=4 cycle=-17.58 rec=0.0 res=0.0 close=0.0 violation=-
- step 8 price=1.218 event=WAIT tail=1.0 sec=4 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-
- step 9 price=1.216 event=WAIT tail=1.0 sec=4 cycle=-17.8 rec=0.0 res=0.0 close=0.0 violation=-
- step 10 price=1.218 event=WAIT tail=1.0 sec=4 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-

### Event trace (last 10)
- step 991 price=1.218 event=WAIT tail=1.0 sec=4 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-
- step 992 price=1.218 event=WAIT tail=1.0 sec=4 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-
- step 993 price=1.218 event=WAIT tail=1.0 sec=4 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-
- step 994 price=1.219 event=WAIT tail=1.0 sec=4 cycle=-17.58 rec=0.0 res=0.0 close=0.0 violation=-
- step 995 price=1.218 event=WAIT tail=1.0 sec=4 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-
- step 996 price=1.218 event=WAIT tail=1.0 sec=4 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-
- step 997 price=1.218 event=WAIT tail=1.0 sec=4 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-
- step 998 price=1.218 event=WAIT tail=1.0 sec=4 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-
- step 999 price=1.216 event=WAIT tail=1.0 sec=4 cycle=-17.8 rec=0.0 res=0.0 close=0.0 violation=-
- step 1000 price=1.218 event=WAIT tail=1.0 sec=4 cycle=-18.52 rec=0.0 res=0.0 close=0.0 violation=-

### Violation events
- none

## flat
- steps: 1000
- opens: 4
- closes: 0
- tail_lot_start: 1.0
- tail_lot_end: 1.0
- reserve_start: 0.0
- reserve_end: 0.0
- recovery_start: 0.0
- recovery_end: 0.0
- max_floating_loss: -21988.1
- max_drawdown_money: 21988.1
- max_drawdown_percent: 219.88
- max_total_lot: 4.2
- max_net_lot: 1.0
- max_active_sections: 4
- max_consecutive_no_close_steps: 1000
- violations_count: 0
- final_status: PASS_SAFE_STALL
- tail_reduction: 0.0
- reserve_generated: 0.0
- recovery_cycles_count: 0
- limit_total_used_percent: 21.0
- limit_net_used_percent: 10.0

### Event trace (first 10)
- step 1 price=1.231 event=OPEN_SECTION tail=1.0 sec=1 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-
- step 2 price=1.2277 event=OPEN_SECTION tail=1.0 sec=2 cycle=-22.01 rec=0.0 res=0.0 close=0.0 violation=-
- step 3 price=1.2271 event=OPEN_SECTION tail=1.0 sec=3 cycle=-21.8 rec=0.0 res=0.0 close=0.0 violation=-
- step 4 price=1.2317 event=OPEN_SECTION tail=1.0 sec=4 cycle=-22.08 rec=0.0 res=0.0 close=0.0 violation=-
- step 5 price=1.2287 event=WAIT tail=1.0 sec=4 cycle=-22.04 rec=0.0 res=0.0 close=0.0 violation=-
- step 6 price=1.2285 event=WAIT tail=1.0 sec=4 cycle=-22.06 rec=0.0 res=0.0 close=0.0 violation=-
- step 7 price=1.2284 event=WAIT tail=1.0 sec=4 cycle=-22.07 rec=0.0 res=0.0 close=0.0 violation=-
- step 8 price=1.2278 event=WAIT tail=1.0 sec=4 cycle=-22.05 rec=0.0 res=0.0 close=0.0 violation=-
- step 9 price=1.2317 event=WAIT tail=1.0 sec=4 cycle=-22.08 rec=0.0 res=0.0 close=0.0 violation=-
- step 10 price=1.2276 event=WAIT tail=1.0 sec=4 cycle=-21.98 rec=0.0 res=0.0 close=0.0 violation=-

### Event trace (last 10)
- step 991 price=1.2323 event=WAIT tail=1.0 sec=4 cycle=-22.01 rec=0.0 res=0.0 close=0.0 violation=-
- step 992 price=1.2275 event=WAIT tail=1.0 sec=4 cycle=-21.94 rec=0.0 res=0.0 close=0.0 violation=-
- step 993 price=1.23 event=WAIT tail=1.0 sec=4 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-
- step 994 price=1.2271 event=WAIT tail=1.0 sec=4 cycle=-21.67 rec=0.0 res=0.0 close=0.0 violation=-
- step 995 price=1.2317 event=WAIT tail=1.0 sec=4 cycle=-22.08 rec=0.0 res=0.0 close=0.0 violation=-
- step 996 price=1.2304 event=WAIT tail=1.0 sec=4 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-
- step 997 price=1.2273 event=WAIT tail=1.0 sec=4 cycle=-21.87 rec=0.0 res=0.0 close=0.0 violation=-
- step 998 price=1.233 event=WAIT tail=1.0 sec=4 cycle=-21.76 rec=0.0 res=0.0 close=0.0 violation=-
- step 999 price=1.2292 event=WAIT tail=1.0 sec=4 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-
- step 1000 price=1.2284 event=WAIT tail=1.0 sec=4 cycle=-22.07 rec=0.0 res=0.0 close=0.0 violation=-

### Violation events
- none

## whipsaw
- steps: 1000
- opens: 4
- closes: 0
- tail_lot_start: 1.0
- tail_lot_end: 1.0
- reserve_start: 0.0
- reserve_end: 0.0
- recovery_start: 0.0
- recovery_end: 0.0
- max_floating_loss: -15853.12
- max_drawdown_money: 15853.12
- max_drawdown_percent: 158.53
- max_total_lot: 4.2
- max_net_lot: 1.0
- max_active_sections: 4
- max_consecutive_no_close_steps: 1000
- violations_count: 0
- final_status: PASS_SAFE_STALL
- tail_reduction: 0.0
- reserve_generated: 0.0
- recovery_cycles_count: 0
- limit_total_used_percent: 21.0
- limit_net_used_percent: 10.0

### Event trace (first 10)
- step 1 price=1.212 event=OPEN_SECTION tail=1.0 sec=1 cycle=-16.36 rec=0.0 res=0.0 close=0.0 violation=-
- step 2 price=1.248 event=OPEN_SECTION tail=1.0 sec=2 cycle=-16.36 rec=0.0 res=0.0 close=0.0 violation=-
- step 3 price=1.212 event=OPEN_SECTION tail=1.0 sec=3 cycle=-16.36 rec=0.0 res=0.0 close=0.0 violation=-
- step 4 price=1.248 event=OPEN_SECTION tail=1.0 sec=4 cycle=-16.36 rec=0.0 res=0.0 close=0.0 violation=-
- step 5 price=1.212 event=WAIT tail=1.0 sec=4 cycle=-16.36 rec=0.0 res=0.0 close=0.0 violation=-
- step 6 price=1.248 event=WAIT tail=1.0 sec=4 cycle=-16.36 rec=0.0 res=0.0 close=0.0 violation=-
- step 7 price=1.212 event=WAIT tail=1.0 sec=4 cycle=-14.06 rec=0.0 res=0.0 close=0.0 violation=-
- step 8 price=1.248 event=WAIT tail=1.0 sec=4 cycle=-16.36 rec=0.0 res=0.0 close=0.0 violation=-
- step 9 price=1.212 event=WAIT tail=1.0 sec=4 cycle=-16.36 rec=0.0 res=0.0 close=0.0 violation=-
- step 10 price=1.248 event=WAIT tail=1.0 sec=4 cycle=-16.36 rec=0.0 res=0.0 close=0.0 violation=-

### Event trace (last 10)
- step 991 price=1.212 event=WAIT tail=1.0 sec=4 cycle=-16.36 rec=0.0 res=0.0 close=0.0 violation=-
- step 992 price=1.248 event=WAIT tail=1.0 sec=4 cycle=-16.36 rec=0.0 res=0.0 close=0.0 violation=-
- step 993 price=1.212 event=WAIT tail=1.0 sec=4 cycle=-16.36 rec=0.0 res=0.0 close=0.0 violation=-
- step 994 price=1.248 event=WAIT tail=1.0 sec=4 cycle=-14.06 rec=0.0 res=0.0 close=0.0 violation=-
- step 995 price=1.212 event=WAIT tail=1.0 sec=4 cycle=-16.36 rec=0.0 res=0.0 close=0.0 violation=-
- step 996 price=1.248 event=WAIT tail=1.0 sec=4 cycle=-16.36 rec=0.0 res=0.0 close=0.0 violation=-
- step 997 price=1.212 event=WAIT tail=1.0 sec=4 cycle=-16.36 rec=0.0 res=0.0 close=0.0 violation=-
- step 998 price=1.248 event=WAIT tail=1.0 sec=4 cycle=-16.36 rec=0.0 res=0.0 close=0.0 violation=-
- step 999 price=1.212 event=WAIT tail=1.0 sec=4 cycle=-16.36 rec=0.0 res=0.0 close=0.0 violation=-
- step 1000 price=1.248 event=WAIT tail=1.0 sec=4 cycle=-16.36 rec=0.0 res=0.0 close=0.0 violation=-

### Violation events
- none

## spike
- steps: 1000
- opens: 26
- closes: 22
- tail_lot_start: 1.0
- tail_lot_end: 0.71
- reserve_start: 0.0
- reserve_end: 109.34
- recovery_start: 0.0
- recovery_end: 2.34
- max_floating_loss: -13466.21
- max_drawdown_money: 13354.53
- max_drawdown_percent: 133.55
- max_total_lot: 4.2
- max_net_lot: 1.0
- max_active_sections: 4
- max_consecutive_no_close_steps: 44
- violations_count: 0
- final_status: PASS_RECOVERY
- tail_reduction: 0.29
- reserve_generated: 109.34
- recovery_cycles_count: 22
- limit_total_used_percent: 21.0
- limit_net_used_percent: 10.0

### Event trace (first 10)
- step 1 price=1.2373 event=OPEN_SECTION tail=1.0 sec=1 cycle=-20.21 rec=0.0 res=0.0 close=0.0 violation=-
- step 2 price=1.2238 event=OPEN_SECTION tail=1.0 sec=2 cycle=-20.61 rec=0.0 res=0.0 close=0.0 violation=-
- step 3 price=1.2216 event=OPEN_SECTION tail=1.0 sec=3 cycle=-19.82 rec=0.0 res=0.0 close=0.0 violation=-
- step 4 price=1.228 event=OPEN_SECTION tail=1.0 sec=4 cycle=-22.12 rec=0.0 res=0.0 close=0.0 violation=-
- step 5 price=1.2272 event=WAIT tail=1.0 sec=4 cycle=-21.83 rec=0.0 res=0.0 close=0.0 violation=-
- step 6 price=1.2267 event=WAIT tail=1.0 sec=4 cycle=-21.65 rec=0.0 res=0.0 close=0.0 violation=-
- step 7 price=1.2245 event=WAIT tail=1.0 sec=4 cycle=-20.36 rec=0.0 res=0.0 close=0.0 violation=-
- step 8 price=1.2236 event=WAIT tail=1.0 sec=4 cycle=-20.54 rec=0.0 res=0.0 close=0.0 violation=-
- step 9 price=1.2383 event=WAIT tail=1.0 sec=4 cycle=-19.85 rec=0.0 res=0.0 close=0.0 violation=-
- step 10 price=1.2349 event=WAIT tail=1.0 sec=4 cycle=-21.08 rec=0.0 res=0.0 close=0.0 violation=-

### Event trace (last 10)
- step 991 price=1.2351 event=OPEN_SECTION tail=0.71 sec=4 cycle=-3.41 rec=2.34 res=109.34 close=0.0 violation=-
- step 992 price=1.2229 event=WAIT tail=0.71 sec=4 cycle=-3.27 rec=2.34 res=109.34 close=0.0 violation=-
- step 993 price=1.225 event=WAIT tail=0.71 sec=4 cycle=-3.41 rec=2.34 res=109.34 close=0.0 violation=-
- step 994 price=1.221 event=WAIT tail=0.71 sec=4 cycle=-2.96 rec=2.34 res=109.34 close=0.0 violation=-
- step 995 price=1.2314 event=WAIT tail=0.71 sec=4 cycle=-3.61 rec=2.34 res=109.34 close=0.0 violation=-
- step 996 price=1.2325 event=WAIT tail=0.71 sec=4 cycle=-3.58 rec=2.34 res=109.34 close=0.0 violation=-
- step 997 price=1.2386 event=WAIT tail=0.71 sec=4 cycle=-3.17 rec=2.34 res=109.34 close=0.0 violation=-
- step 998 price=1.2362 event=WAIT tail=0.71 sec=4 cycle=-3.33 rec=2.34 res=109.34 close=0.0 violation=-
- step 999 price=1.233 event=WAIT tail=0.71 sec=4 cycle=-3.55 rec=2.34 res=109.34 close=0.0 violation=-
- step 1000 price=1.2284 event=WAIT tail=0.71 sec=4 cycle=-3.61 rec=2.34 res=109.34 close=0.0 violation=-

### Violation events
- none

## gap
- steps: 1000
- opens: 13
- closes: 9
- tail_lot_start: 1.0
- tail_lot_end: 0.74
- reserve_start: 0.0
- reserve_end: 185.12
- recovery_start: 0.0
- recovery_end: 12.48
- max_floating_loss: -16445.52
- max_drawdown_money: 16249.95
- max_drawdown_percent: 162.5
- max_total_lot: 4.2
- max_net_lot: 1.0
- max_active_sections: 4
- max_consecutive_no_close_steps: 109
- violations_count: 0
- final_status: PASS_RECOVERY
- tail_reduction: 0.26
- reserve_generated: 185.12
- recovery_cycles_count: 9
- limit_total_used_percent: 21.0
- limit_net_used_percent: 10.0

### Event trace (first 10)
- step 1 price=1.2343 event=OPEN_SECTION tail=1.0 sec=1 cycle=-21.29 rec=0.0 res=0.0 close=0.0 violation=-
- step 2 price=1.2208 event=OPEN_SECTION tail=1.0 sec=2 cycle=-19.53 rec=0.0 res=0.0 close=0.0 violation=-
- step 3 price=1.2186 event=OPEN_SECTION tail=1.0 sec=3 cycle=-18.74 rec=0.0 res=0.0 close=0.0 violation=-
- step 4 price=1.2369 event=OPEN_SECTION tail=1.0 sec=4 cycle=-20.36 rec=0.0 res=0.0 close=0.0 violation=-
- step 5 price=1.225 event=WAIT tail=1.0 sec=4 cycle=-21.04 rec=0.0 res=0.0 close=0.0 violation=-
- step 6 price=1.2242 event=WAIT tail=1.0 sec=4 cycle=-20.75 rec=0.0 res=0.0 close=0.0 violation=-
- step 7 price=1.2237 event=WAIT tail=1.0 sec=4 cycle=-19.95 rec=0.0 res=0.0 close=0.0 violation=-
- step 8 price=1.2215 event=WAIT tail=1.0 sec=4 cycle=-19.78 rec=0.0 res=0.0 close=0.0 violation=-
- step 9 price=1.2368 event=WAIT tail=1.0 sec=4 cycle=-20.39 rec=0.0 res=0.0 close=0.0 violation=-
- step 10 price=1.2206 event=WAIT tail=1.0 sec=4 cycle=-19.46 rec=0.0 res=0.0 close=0.0 violation=-

### Event trace (last 10)
- step 991 price=1.2184 event=OPEN_SECTION tail=0.74 sec=4 cycle=-8.52 rec=12.48 res=185.12 close=0.0 violation=-
- step 992 price=1.2371 event=WAIT tail=0.74 sec=4 cycle=-9.24 rec=12.48 res=185.12 close=0.0 violation=-
- step 993 price=1.2318 event=WAIT tail=0.74 sec=4 cycle=-10.04 rec=12.48 res=185.12 close=0.0 violation=-
- step 994 price=1.2193 event=WAIT tail=0.74 sec=4 cycle=-8.1 rec=12.48 res=185.12 close=0.0 violation=-
- step 995 price=1.2269 event=WAIT tail=0.74 sec=4 cycle=-9.88 rec=12.48 res=185.12 close=0.0 violation=-
- step 996 price=1.2237 event=WAIT tail=0.74 sec=4 cycle=-9.37 rec=12.48 res=185.12 close=0.0 violation=-
- step 997 price=1.2346 event=WAIT tail=0.74 sec=4 cycle=-9.64 rec=12.48 res=185.12 close=0.0 violation=-
- step 998 price=1.2197 event=WAIT tail=0.74 sec=4 cycle=-8.73 rec=12.48 res=185.12 close=0.0 violation=-
- step 999 price=1.2379 event=WAIT tail=0.74 sec=4 cycle=-9.11 rec=12.48 res=185.12 close=0.0 violation=-
- step 1000 price=1.2346 event=WAIT tail=0.74 sec=4 cycle=-9.64 rec=12.48 res=185.12 close=0.0 violation=-

### Violation events
- none

## monte_carlo_summary
- number_of_runs: 200
- seed: 42
- regimes: random_walk, mean_reversion, trend_with_pullbacks, high_volatility, gap_sequence
- tail_lot_end min/max/avg: 0.7400/1.0000/0.9404
- reserve_end min/max/avg: 0.00/64.40/19.08
- drawdown min/max/avg: 2047.63/6338.53/4659.48
- worst_case_run: mean_reversion_27 (drawdown=6338.53)
- violations_total: 0
- runs_with_violations: 0

## Final status
Initial formula validation: PASS
Workbook runtime validation: PASS
Stress test quality: PASS_RECOVERY
Final system validation: NOT YET