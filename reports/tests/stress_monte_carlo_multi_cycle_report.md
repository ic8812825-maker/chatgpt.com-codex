# STRESS / MONTE-CARLO / MULTI-CYCLE TESTING

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
- max_floating_loss: -20854.0
- max_drawdown_money: 20854.0
- max_drawdown_percent: 0.0
- max_total_lot: 4.2
- max_net_lot: 1.0
- max_active_sections: 4
- max_consecutive_no_close_steps: 1000
- violations_count: 0
- final_status: PASS

### Event trace (first 10)
- step 1 price=1.2381 event=OPEN_SECTION tail=1.0 sec=1 cycle=-21.09 rec=0.0 res=0.0 close=0.0 violation=-
- step 2 price=1.2382 event=OPEN_SECTION tail=1.0 sec=2 cycle=-21.06 rec=0.0 res=0.0 close=0.0 violation=-
- step 3 price=1.2383 event=OPEN_SECTION tail=1.0 sec=3 cycle=-21.04 rec=0.0 res=0.0 close=0.0 violation=-
- step 4 price=1.2384 event=OPEN_SECTION tail=1.0 sec=4 cycle=-21.01 rec=0.0 res=0.0 close=0.0 violation=-
- step 5 price=1.2385 event=WAIT tail=1.0 sec=4 cycle=-20.98 rec=0.0 res=0.0 close=0.0 violation=-
- step 6 price=1.2386 event=WAIT tail=1.0 sec=4 cycle=-20.95 rec=0.0 res=0.0 close=0.0 violation=-
- step 7 price=1.2387 event=WAIT tail=1.0 sec=4 cycle=-20.92 rec=0.0 res=0.0 close=0.0 violation=-
- step 8 price=1.2388 event=WAIT tail=1.0 sec=4 cycle=-20.9 rec=0.0 res=0.0 close=0.0 violation=-
- step 9 price=1.2389 event=WAIT tail=1.0 sec=4 cycle=-20.87 rec=0.0 res=0.0 close=0.0 violation=-
- step 10 price=1.239 event=WAIT tail=1.0 sec=4 cycle=-20.84 rec=0.0 res=0.0 close=0.0 violation=-

### Event trace (last 10)
- step 991 price=1.2391 event=WAIT tail=1.0 sec=4 cycle=-20.81 rec=0.0 res=0.0 close=0.0 violation=-
- step 992 price=1.2392 event=WAIT tail=1.0 sec=4 cycle=-20.78 rec=0.0 res=0.0 close=0.0 violation=-
- step 993 price=1.2393 event=WAIT tail=1.0 sec=4 cycle=-20.76 rec=0.0 res=0.0 close=0.0 violation=-
- step 994 price=1.2394 event=WAIT tail=1.0 sec=4 cycle=-20.73 rec=0.0 res=0.0 close=0.0 violation=-
- step 995 price=1.2395 event=WAIT tail=1.0 sec=4 cycle=-20.7 rec=0.0 res=0.0 close=0.0 violation=-
- step 996 price=1.2396 event=WAIT tail=1.0 sec=4 cycle=-20.67 rec=0.0 res=0.0 close=0.0 violation=-
- step 997 price=1.2397 event=WAIT tail=1.0 sec=4 cycle=-20.64 rec=0.0 res=0.0 close=0.0 violation=-
- step 998 price=1.2398 event=WAIT tail=1.0 sec=4 cycle=-20.62 rec=0.0 res=0.0 close=0.0 violation=-
- step 999 price=1.2399 event=WAIT tail=1.0 sec=4 cycle=-20.59 rec=0.0 res=0.0 close=0.0 violation=-
- step 1000 price=1.238 event=WAIT tail=1.0 sec=4 cycle=-21.12 rec=0.0 res=0.0 close=0.0 violation=-

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
- max_floating_loss: -20854.0
- max_drawdown_money: 20854.0
- max_drawdown_percent: 0.0
- max_total_lot: 4.2
- max_net_lot: 1.0
- max_active_sections: 4
- max_consecutive_no_close_steps: 1000
- violations_count: 0
- final_status: PASS

### Event trace (first 10)
- step 1 price=1.2219 event=OPEN_SECTION tail=1.0 sec=1 cycle=-21.09 rec=0.0 res=0.0 close=0.0 violation=-
- step 2 price=1.2218 event=OPEN_SECTION tail=1.0 sec=2 cycle=-21.06 rec=0.0 res=0.0 close=0.0 violation=-
- step 3 price=1.2217 event=OPEN_SECTION tail=1.0 sec=3 cycle=-21.04 rec=0.0 res=0.0 close=0.0 violation=-
- step 4 price=1.2216 event=OPEN_SECTION tail=1.0 sec=4 cycle=-21.01 rec=0.0 res=0.0 close=0.0 violation=-
- step 5 price=1.2215 event=WAIT tail=1.0 sec=4 cycle=-20.98 rec=0.0 res=0.0 close=0.0 violation=-
- step 6 price=1.2214 event=WAIT tail=1.0 sec=4 cycle=-20.95 rec=0.0 res=0.0 close=0.0 violation=-
- step 7 price=1.2213 event=WAIT tail=1.0 sec=4 cycle=-20.92 rec=0.0 res=0.0 close=0.0 violation=-
- step 8 price=1.2212 event=WAIT tail=1.0 sec=4 cycle=-20.9 rec=0.0 res=0.0 close=0.0 violation=-
- step 9 price=1.2211 event=WAIT tail=1.0 sec=4 cycle=-20.87 rec=0.0 res=0.0 close=0.0 violation=-
- step 10 price=1.221 event=WAIT tail=1.0 sec=4 cycle=-20.84 rec=0.0 res=0.0 close=0.0 violation=-

### Event trace (last 10)
- step 991 price=1.2209 event=WAIT tail=1.0 sec=4 cycle=-20.81 rec=0.0 res=0.0 close=0.0 violation=-
- step 992 price=1.2208 event=WAIT tail=1.0 sec=4 cycle=-20.78 rec=0.0 res=0.0 close=0.0 violation=-
- step 993 price=1.2207 event=WAIT tail=1.0 sec=4 cycle=-20.76 rec=0.0 res=0.0 close=0.0 violation=-
- step 994 price=1.2206 event=WAIT tail=1.0 sec=4 cycle=-20.73 rec=0.0 res=0.0 close=0.0 violation=-
- step 995 price=1.2205 event=WAIT tail=1.0 sec=4 cycle=-20.7 rec=0.0 res=0.0 close=0.0 violation=-
- step 996 price=1.2204 event=WAIT tail=1.0 sec=4 cycle=-20.67 rec=0.0 res=0.0 close=0.0 violation=-
- step 997 price=1.2203 event=WAIT tail=1.0 sec=4 cycle=-20.64 rec=0.0 res=0.0 close=0.0 violation=-
- step 998 price=1.2202 event=WAIT tail=1.0 sec=4 cycle=-20.62 rec=0.0 res=0.0 close=0.0 violation=-
- step 999 price=1.2201 event=WAIT tail=1.0 sec=4 cycle=-20.59 rec=0.0 res=0.0 close=0.0 violation=-
- step 1000 price=1.222 event=WAIT tail=1.0 sec=4 cycle=-21.12 rec=0.0 res=0.0 close=0.0 violation=-

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
- max_floating_loss: -22000.0
- max_drawdown_money: 22000.0
- max_drawdown_percent: 0.0
- max_total_lot: 4.2
- max_net_lot: 1.0
- max_active_sections: 4
- max_consecutive_no_close_steps: 1000
- violations_count: 0
- final_status: PASS

### Event trace (first 10)
- step 1 price=1.2305 event=OPEN_SECTION tail=1.0 sec=1 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-
- step 2 price=1.2288 event=OPEN_SECTION tail=1.0 sec=2 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-
- step 3 price=1.2285 event=OPEN_SECTION tail=1.0 sec=3 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-
- step 4 price=1.2308 event=OPEN_SECTION tail=1.0 sec=4 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-
- step 5 price=1.2293 event=WAIT tail=1.0 sec=4 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-
- step 6 price=1.2292 event=WAIT tail=1.0 sec=4 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-
- step 7 price=1.2292 event=WAIT tail=1.0 sec=4 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-
- step 8 price=1.2289 event=WAIT tail=1.0 sec=4 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-
- step 9 price=1.2308 event=WAIT tail=1.0 sec=4 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-
- step 10 price=1.2288 event=WAIT tail=1.0 sec=4 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-

### Event trace (last 10)
- step 991 price=1.2299 event=WAIT tail=1.0 sec=4 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-
- step 992 price=1.2295 event=WAIT tail=1.0 sec=4 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-
- step 993 price=1.2295 event=WAIT tail=1.0 sec=4 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-
- step 994 price=1.2309 event=WAIT tail=1.0 sec=4 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-
- step 995 price=1.2313 event=WAIT tail=1.0 sec=4 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-
- step 996 price=1.2297 event=WAIT tail=1.0 sec=4 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-
- step 997 price=1.2293 event=WAIT tail=1.0 sec=4 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-
- step 998 price=1.2309 event=WAIT tail=1.0 sec=4 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-
- step 999 price=1.2315 event=WAIT tail=1.0 sec=4 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-
- step 1000 price=1.2311 event=WAIT tail=1.0 sec=4 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-

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
- max_floating_loss: -18320.0
- max_drawdown_money: 18320.0
- max_drawdown_percent: 0.0
- max_total_lot: 4.2
- max_net_lot: 1.0
- max_active_sections: 4
- max_consecutive_no_close_steps: 1000
- violations_count: 0
- final_status: PASS

### Event trace (first 10)
- step 1 price=1.212 event=OPEN_SECTION tail=1.0 sec=1 cycle=-18.32 rec=0.0 res=0.0 close=0.0 violation=-
- step 2 price=1.248 event=OPEN_SECTION tail=1.0 sec=2 cycle=-18.32 rec=0.0 res=0.0 close=0.0 violation=-
- step 3 price=1.212 event=OPEN_SECTION tail=1.0 sec=3 cycle=-18.32 rec=0.0 res=0.0 close=0.0 violation=-
- step 4 price=1.248 event=OPEN_SECTION tail=1.0 sec=4 cycle=-18.32 rec=0.0 res=0.0 close=0.0 violation=-
- step 5 price=1.212 event=WAIT tail=1.0 sec=4 cycle=-18.32 rec=0.0 res=0.0 close=0.0 violation=-
- step 6 price=1.248 event=WAIT tail=1.0 sec=4 cycle=-18.32 rec=0.0 res=0.0 close=0.0 violation=-
- step 7 price=1.212 event=WAIT tail=1.0 sec=4 cycle=-18.32 rec=0.0 res=0.0 close=0.0 violation=-
- step 8 price=1.248 event=WAIT tail=1.0 sec=4 cycle=-18.32 rec=0.0 res=0.0 close=0.0 violation=-
- step 9 price=1.212 event=WAIT tail=1.0 sec=4 cycle=-18.32 rec=0.0 res=0.0 close=0.0 violation=-
- step 10 price=1.248 event=WAIT tail=1.0 sec=4 cycle=-18.32 rec=0.0 res=0.0 close=0.0 violation=-

### Event trace (last 10)
- step 991 price=1.212 event=WAIT tail=1.0 sec=4 cycle=-18.32 rec=0.0 res=0.0 close=0.0 violation=-
- step 992 price=1.248 event=WAIT tail=1.0 sec=4 cycle=-18.32 rec=0.0 res=0.0 close=0.0 violation=-
- step 993 price=1.212 event=WAIT tail=1.0 sec=4 cycle=-18.32 rec=0.0 res=0.0 close=0.0 violation=-
- step 994 price=1.248 event=WAIT tail=1.0 sec=4 cycle=-18.32 rec=0.0 res=0.0 close=0.0 violation=-
- step 995 price=1.212 event=WAIT tail=1.0 sec=4 cycle=-18.32 rec=0.0 res=0.0 close=0.0 violation=-
- step 996 price=1.248 event=WAIT tail=1.0 sec=4 cycle=-18.32 rec=0.0 res=0.0 close=0.0 violation=-
- step 997 price=1.212 event=WAIT tail=1.0 sec=4 cycle=-18.32 rec=0.0 res=0.0 close=0.0 violation=-
- step 998 price=1.248 event=WAIT tail=1.0 sec=4 cycle=-18.32 rec=0.0 res=0.0 close=0.0 violation=-
- step 999 price=1.212 event=WAIT tail=1.0 sec=4 cycle=-18.32 rec=0.0 res=0.0 close=0.0 violation=-
- step 1000 price=1.248 event=WAIT tail=1.0 sec=4 cycle=-18.32 rec=0.0 res=0.0 close=0.0 violation=-

### Violation events
- none

## spike
- steps: 1000
- opens: 28
- closes: 25
- tail_lot_start: 1.0
- tail_lot_end: 0.84
- reserve_start: 0.0
- reserve_end: 48.73
- recovery_start: 0.0
- recovery_end: 2.91
- max_floating_loss: -19256.56
- max_drawdown_money: 19201.88
- max_drawdown_percent: 0.0
- max_total_lot: 4.2
- max_net_lot: 1.0
- max_active_sections: 4
- max_consecutive_no_close_steps: 39
- violations_count: 0
- final_status: PASS

### Event trace (first 10)
- step 1 price=1.2293 event=OPEN_SECTION tail=1.0 sec=1 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-
- step 2 price=1.2272 event=OPEN_SECTION tail=1.0 sec=2 cycle=-22.1 rec=0.0 res=0.0 close=0.0 violation=-
- step 3 price=1.2346 event=OPEN_SECTION tail=1.0 sec=3 cycle=-22.07 rec=0.0 res=0.0 close=0.0 violation=-
- step 4 price=1.225 event=OPEN_SECTION tail=1.0 sec=4 cycle=-21.96 rec=0.0 res=0.0 close=0.0 violation=-
- step 5 price=1.23 event=WAIT tail=1.0 sec=4 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-
- step 6 price=1.2242 event=WAIT tail=1.0 sec=4 cycle=-21.74 rec=0.0 res=0.0 close=0.0 violation=-
- step 7 price=1.2335 event=WAIT tail=1.0 sec=4 cycle=-22.18 rec=0.0 res=0.0 close=0.0 violation=-
- step 8 price=1.2309 event=WAIT tail=1.0 sec=4 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-
- step 9 price=1.2246 event=WAIT tail=1.0 sec=4 cycle=-21.85 rec=0.0 res=0.0 close=0.0 violation=-
- step 10 price=1.2284 event=WAIT tail=1.0 sec=4 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-

### Event trace (last 10)
- step 991 price=1.2241 event=WAIT tail=0.85 sec=4 cycle=-17.75 rec=7.75 res=46.94 close=0.0 violation=-
- step 992 price=1.2285 event=WAIT tail=0.85 sec=4 cycle=-18.0 rec=7.75 res=46.94 close=0.0 violation=-
- step 993 price=1.2341 event=WAIT tail=0.85 sec=4 cycle=-18.17 rec=7.75 res=46.94 close=0.0 violation=-
- step 994 price=1.234 event=WAIT tail=0.85 sec=4 cycle=-18.19 rec=7.75 res=46.94 close=0.0 violation=-
- step 995 price=1.227 event=WAIT tail=0.85 sec=4 cycle=-18.1 rec=7.75 res=46.94 close=0.0 violation=-
- step 996 price=1.2315 event=WAIT tail=0.85 sec=4 cycle=-18.0 rec=7.75 res=46.94 close=0.0 violation=-
- step 997 price=1.2281 event=WAIT tail=0.85 sec=4 cycle=-18.0 rec=7.75 res=46.94 close=0.0 violation=-
- step 998 price=1.2242 event=WAIT tail=0.85 sec=4 cycle=-17.77 rec=7.75 res=46.94 close=0.0 violation=-
- step 999 price=1.2262 event=WAIT tail=0.85 sec=4 cycle=-18.17 rec=7.75 res=46.94 close=0.0 violation=-
- step 1000 price=1.35 event=CLOSE_TAIL tail=0.84 sec=3 cycle=8.95 rec=2.91 res=48.73 close=0.01 violation=-

### Violation events
- none

## gap
- steps: 1000
- opens: 12
- closes: 8
- tail_lot_start: 1.0
- tail_lot_end: 0.89
- reserve_start: 0.0
- reserve_end: 72.39
- recovery_start: 0.0
- recovery_end: 14.55
- max_floating_loss: -19733.24
- max_drawdown_money: 19646.3
- max_drawdown_percent: 0.0
- max_total_lot: 4.2
- max_net_lot: 1.0
- max_active_sections: 4
- max_consecutive_no_close_steps: 119
- violations_count: 0
- final_status: PASS

### Event trace (first 10)
- step 1 price=1.2267 event=OPEN_SECTION tail=1.0 sec=1 cycle=-22.16 rec=0.0 res=0.0 close=0.0 violation=-
- step 2 price=1.2213 event=OPEN_SECTION tail=1.0 sec=2 cycle=-20.92 rec=0.0 res=0.0 close=0.0 violation=-
- step 3 price=1.2232 event=OPEN_SECTION tail=1.0 sec=3 cycle=-21.46 rec=0.0 res=0.0 close=0.0 violation=-
- step 4 price=1.2389 event=OPEN_SECTION tail=1.0 sec=4 cycle=-20.87 rec=0.0 res=0.0 close=0.0 violation=-
- step 5 price=1.2307 event=WAIT tail=1.0 sec=4 cycle=-22.0 rec=0.0 res=0.0 close=0.0 violation=-
- step 6 price=1.2334 event=WAIT tail=1.0 sec=4 cycle=-22.17 rec=0.0 res=0.0 close=0.0 violation=-
- step 7 price=1.2229 event=WAIT tail=1.0 sec=4 cycle=-21.37 rec=0.0 res=0.0 close=0.0 violation=-
- step 8 price=1.239 event=WAIT tail=1.0 sec=4 cycle=-20.84 rec=0.0 res=0.0 close=0.0 violation=-
- step 9 price=1.2216 event=WAIT tail=1.0 sec=4 cycle=-21.01 rec=0.0 res=0.0 close=0.0 violation=-
- step 10 price=1.2321 event=WAIT tail=1.0 sec=4 cycle=-22.01 rec=0.0 res=0.0 close=0.0 violation=-

### Event trace (last 10)
- step 991 price=1.2263 event=WAIT tail=0.89 sec=4 cycle=-19.38 rec=14.55 res=72.39 close=0.0 violation=-
- step 992 price=1.224 event=WAIT tail=0.89 sec=4 cycle=-18.92 rec=14.55 res=72.39 close=0.0 violation=-
- step 993 price=1.2283 event=WAIT tail=0.89 sec=4 cycle=-19.2 rec=14.55 res=72.39 close=0.0 violation=-
- step 994 price=1.2347 event=WAIT tail=0.89 sec=4 cycle=-19.24 rec=14.55 res=72.39 close=0.0 violation=-
- step 995 price=1.2384 event=WAIT tail=0.89 sec=4 cycle=-18.33 rec=14.55 res=72.39 close=0.0 violation=-
- step 996 price=1.228 event=WAIT tail=0.89 sec=4 cycle=-19.2 rec=14.55 res=72.39 close=0.0 violation=-
- step 997 price=1.2248 event=WAIT tail=0.89 sec=4 cycle=-19.11 rec=14.55 res=72.39 close=0.0 violation=-
- step 998 price=1.2395 event=WAIT tail=0.89 sec=4 cycle=-18.06 rec=14.55 res=72.39 close=0.0 violation=-
- step 999 price=1.224 event=WAIT tail=0.89 sec=4 cycle=-18.92 rec=14.55 res=72.39 close=0.0 violation=-
- step 1000 price=1.2327 event=WAIT tail=0.89 sec=4 cycle=-19.27 rec=14.55 res=72.39 close=0.0 violation=-

### Violation events
- none

## monte_carlo_summary
- number_of_runs: 200
- seed: 42
- tail_lot_end min/max/avg: 1.0000/1.0000/1.0000
- reserve_end min/max/avg: 0.00/0.00/0.00
- drawdown min/max/avg: 5595.01/5822.43/5718.30
- worst_case_run: mc_150 (drawdown=5822.43)
- violations_total: 0
- runs_with_violations: 0

## Final status
Stress testing: PASS