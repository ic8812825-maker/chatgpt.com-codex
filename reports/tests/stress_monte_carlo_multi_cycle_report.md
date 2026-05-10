# STRESS / MONTE-CARLO / MULTI-CYCLE TESTING
- account_balance: 10000.0
- leverage: 100
- contract_size: 100000
- margin_per_lot: 1000.0
- MaxDDPercent: 60
- MinMarginLevelPercent: 120
- StopOutPercent: 50
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
- max_floating_loss: -18078.57
- max_drawdown_money: 18078.57
- max_drawdown_percent: 180.79
- max_total_lot: 4.2
- max_net_lot: 1.0
- max_active_sections: 4
- max_consecutive_no_close_steps: 1000
- tail_reduction: 0.0
- reserve_generated: 0.0
- recovery_cycles_count: 0
- limit_total_used_percent: 21.0
- limit_net_used_percent: 10.0
- min_equity: -8078.57
- max_used_margin: 4200.0
- min_free_margin: -12278.57
- min_margin_level_percent: -192.35
- stop_out_triggered: True
- violations_count: 0
- final_status: FAIL_STOP_OUT

### Event trace (first 10)
- step 1 price=1.242 event=OPEN_SECTION tail=1.0 sec=1 cycle=-18.52 eq=9981.48 margin=391.43% close=0.0 violation=-
- step 2 price=1.242 event=OPEN_SECTION tail=1.0 sec=2 cycle=-18.52 eq=9962.96 margin=321.39% close=0.0 violation=-
- step 3 price=1.242 event=OPEN_SECTION tail=1.0 sec=3 cycle=-18.52 eq=9944.44 margin=272.45% close=0.0 violation=-
- step 4 price=1.242 event=OPEN_SECTION tail=1.0 sec=4 cycle=-18.52 eq=9925.92 margin=236.33% close=0.0 violation=-
- step 5 price=1.242 event=WAIT tail=1.0 sec=4 cycle=-18.52 eq=9907.4 margin=235.89% close=0.0 violation=-
- step 6 price=1.242 event=WAIT tail=1.0 sec=4 cycle=-18.52 eq=9888.88 margin=235.45% close=0.0 violation=-
- step 7 price=1.241 event=WAIT tail=1.0 sec=4 cycle=-17.15 eq=9871.73 margin=235.04% close=0.0 violation=-
- step 8 price=1.242 event=WAIT tail=1.0 sec=4 cycle=-18.52 eq=9853.21 margin=234.6% close=0.0 violation=-
- step 9 price=1.244 event=WAIT tail=1.0 sec=4 cycle=-17.8 eq=9835.41 margin=234.18% close=0.0 violation=-
- step 10 price=1.242 event=WAIT tail=1.0 sec=4 cycle=-18.52 eq=9816.89 margin=233.74% close=0.0 violation=-

### Event trace (last 10)
- step 991 price=1.242 event=WAIT tail=1.0 sec=4 cycle=-18.52 eq=-7913.98 margin=-188.43% close=0.0 violation=-
- step 992 price=1.242 event=WAIT tail=1.0 sec=4 cycle=-18.52 eq=-7932.5 margin=-188.87% close=0.0 violation=-
- step 993 price=1.242 event=WAIT tail=1.0 sec=4 cycle=-18.52 eq=-7951.02 margin=-189.31% close=0.0 violation=-
- step 994 price=1.241 event=WAIT tail=1.0 sec=4 cycle=-17.15 eq=-7968.17 margin=-189.72% close=0.0 violation=-
- step 995 price=1.242 event=WAIT tail=1.0 sec=4 cycle=-18.52 eq=-7986.69 margin=-190.16% close=0.0 violation=-
- step 996 price=1.242 event=WAIT tail=1.0 sec=4 cycle=-18.52 eq=-8005.21 margin=-190.6% close=0.0 violation=-
- step 997 price=1.242 event=WAIT tail=1.0 sec=4 cycle=-18.52 eq=-8023.73 margin=-191.04% close=0.0 violation=-
- step 998 price=1.242 event=WAIT tail=1.0 sec=4 cycle=-18.52 eq=-8042.25 margin=-191.48% close=0.0 violation=-
- step 999 price=1.244 event=WAIT tail=1.0 sec=4 cycle=-17.8 eq=-8060.05 margin=-191.91% close=0.0 violation=-
- step 1000 price=1.242 event=WAIT tail=1.0 sec=4 cycle=-18.52 eq=-8078.57 margin=-192.35% close=0.0 violation=-

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
- max_floating_loss: -18078.57
- max_drawdown_money: 18078.57
- max_drawdown_percent: 180.79
- max_total_lot: 4.2
- max_net_lot: 1.0
- max_active_sections: 4
- max_consecutive_no_close_steps: 1000
- tail_reduction: 0.0
- reserve_generated: 0.0
- recovery_cycles_count: 0
- limit_total_used_percent: 21.0
- limit_net_used_percent: 10.0
- min_equity: -8078.57
- max_used_margin: 4200.0
- min_free_margin: -12278.57
- min_margin_level_percent: -192.35
- stop_out_triggered: True
- violations_count: 0
- final_status: FAIL_STOP_OUT

### Event trace (first 10)
- step 1 price=1.218 event=OPEN_SECTION tail=1.0 sec=1 cycle=-18.52 eq=9981.48 margin=391.43% close=0.0 violation=-
- step 2 price=1.218 event=OPEN_SECTION tail=1.0 sec=2 cycle=-18.52 eq=9962.96 margin=321.39% close=0.0 violation=-
- step 3 price=1.218 event=OPEN_SECTION tail=1.0 sec=3 cycle=-18.52 eq=9944.44 margin=272.45% close=0.0 violation=-
- step 4 price=1.218 event=OPEN_SECTION tail=1.0 sec=4 cycle=-18.52 eq=9925.92 margin=236.33% close=0.0 violation=-
- step 5 price=1.218 event=WAIT tail=1.0 sec=4 cycle=-18.52 eq=9907.4 margin=235.89% close=0.0 violation=-
- step 6 price=1.218 event=WAIT tail=1.0 sec=4 cycle=-18.52 eq=9888.88 margin=235.45% close=0.0 violation=-
- step 7 price=1.219 event=WAIT tail=1.0 sec=4 cycle=-17.15 eq=9871.73 margin=235.04% close=0.0 violation=-
- step 8 price=1.218 event=WAIT tail=1.0 sec=4 cycle=-18.52 eq=9853.21 margin=234.6% close=0.0 violation=-
- step 9 price=1.216 event=WAIT tail=1.0 sec=4 cycle=-17.8 eq=9835.41 margin=234.18% close=0.0 violation=-
- step 10 price=1.218 event=WAIT tail=1.0 sec=4 cycle=-18.52 eq=9816.89 margin=233.74% close=0.0 violation=-

### Event trace (last 10)
- step 991 price=1.218 event=WAIT tail=1.0 sec=4 cycle=-18.52 eq=-7913.98 margin=-188.43% close=0.0 violation=-
- step 992 price=1.218 event=WAIT tail=1.0 sec=4 cycle=-18.52 eq=-7932.5 margin=-188.87% close=0.0 violation=-
- step 993 price=1.218 event=WAIT tail=1.0 sec=4 cycle=-18.52 eq=-7951.02 margin=-189.31% close=0.0 violation=-
- step 994 price=1.219 event=WAIT tail=1.0 sec=4 cycle=-17.15 eq=-7968.17 margin=-189.72% close=0.0 violation=-
- step 995 price=1.218 event=WAIT tail=1.0 sec=4 cycle=-18.52 eq=-7986.69 margin=-190.16% close=0.0 violation=-
- step 996 price=1.218 event=WAIT tail=1.0 sec=4 cycle=-18.52 eq=-8005.21 margin=-190.6% close=0.0 violation=-
- step 997 price=1.218 event=WAIT tail=1.0 sec=4 cycle=-18.52 eq=-8023.73 margin=-191.04% close=0.0 violation=-
- step 998 price=1.218 event=WAIT tail=1.0 sec=4 cycle=-18.52 eq=-8042.25 margin=-191.48% close=0.0 violation=-
- step 999 price=1.216 event=WAIT tail=1.0 sec=4 cycle=-17.8 eq=-8060.05 margin=-191.91% close=0.0 violation=-
- step 1000 price=1.218 event=WAIT tail=1.0 sec=4 cycle=-18.52 eq=-8078.57 margin=-192.35% close=0.0 violation=-

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
- max_floating_loss: -21985.95
- max_drawdown_money: 21985.95
- max_drawdown_percent: 219.86
- max_total_lot: 4.2
- max_net_lot: 1.0
- max_active_sections: 4
- max_consecutive_no_close_steps: 1000
- tail_reduction: 0.0
- reserve_generated: 0.0
- recovery_cycles_count: 0
- limit_total_used_percent: 21.0
- limit_net_used_percent: 10.0
- min_equity: -11985.95
- max_used_margin: 4200.0
- min_free_margin: -16185.95
- min_margin_level_percent: -285.38
- stop_out_triggered: True
- violations_count: 0
- final_status: FAIL_STOP_OUT

### Event trace (first 10)
- step 1 price=1.231 event=OPEN_SECTION tail=1.0 sec=1 cycle=-22.0 eq=9978.0 margin=391.29% close=0.0 violation=-
- step 2 price=1.2277 event=OPEN_SECTION tail=1.0 sec=2 cycle=-22.01 eq=9955.99 margin=321.16% close=0.0 violation=-
- step 3 price=1.2271 event=OPEN_SECTION tail=1.0 sec=3 cycle=-21.8 eq=9934.19 margin=272.17% close=0.0 violation=-
- step 4 price=1.2317 event=OPEN_SECTION tail=1.0 sec=4 cycle=-22.08 eq=9912.11 margin=236.0% close=0.0 violation=-
- step 5 price=1.2287 event=WAIT tail=1.0 sec=4 cycle=-22.04 eq=9890.07 margin=235.48% close=0.0 violation=-
- step 6 price=1.2285 event=WAIT tail=1.0 sec=4 cycle=-22.06 eq=9868.01 margin=234.95% close=0.0 violation=-
- step 7 price=1.2284 event=WAIT tail=1.0 sec=4 cycle=-22.07 eq=9845.94 margin=234.43% close=0.0 violation=-
- step 8 price=1.2278 event=WAIT tail=1.0 sec=4 cycle=-22.05 eq=9823.89 margin=233.9% close=0.0 violation=-
- step 9 price=1.2317 event=WAIT tail=1.0 sec=4 cycle=-22.08 eq=9801.81 margin=233.38% close=0.0 violation=-
- step 10 price=1.2276 event=WAIT tail=1.0 sec=4 cycle=-21.98 eq=9779.83 margin=232.85% close=0.0 violation=-

### Event trace (last 10)
- step 991 price=1.2323 event=WAIT tail=1.0 sec=4 cycle=-22.01 eq=-11788.6 margin=-280.68% close=0.0 violation=-
- step 992 price=1.2275 event=WAIT tail=1.0 sec=4 cycle=-21.94 eq=-11810.54 margin=-281.2% close=0.0 violation=-
- step 993 price=1.23 event=WAIT tail=1.0 sec=4 cycle=-22.0 eq=-11832.54 margin=-281.73% close=0.0 violation=-
- step 994 price=1.2271 event=WAIT tail=1.0 sec=4 cycle=-21.62 eq=-11854.17 margin=-282.24% close=0.0 violation=-
- step 995 price=1.2317 event=WAIT tail=1.0 sec=4 cycle=-22.08 eq=-11876.25 margin=-282.77% close=0.0 violation=-
- step 996 price=1.2304 event=WAIT tail=1.0 sec=4 cycle=-22.0 eq=-11898.25 margin=-283.29% close=0.0 violation=-
- step 997 price=1.2273 event=WAIT tail=1.0 sec=4 cycle=-21.87 eq=-11920.12 margin=-283.81% close=0.0 violation=-
- step 998 price=1.233 event=WAIT tail=1.0 sec=4 cycle=-21.76 eq=-11941.88 margin=-284.33% close=0.0 violation=-
- step 999 price=1.2292 event=WAIT tail=1.0 sec=4 cycle=-22.0 eq=-11963.88 margin=-284.85% close=0.0 violation=-
- step 1000 price=1.2284 event=WAIT tail=1.0 sec=4 cycle=-22.07 eq=-11985.95 margin=-285.38% close=0.0 violation=-

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
- max_floating_loss: -15684.16
- max_drawdown_money: 15684.16
- max_drawdown_percent: 156.84
- max_total_lot: 4.2
- max_net_lot: 1.0
- max_active_sections: 4
- max_consecutive_no_close_steps: 1000
- tail_reduction: 0.0
- reserve_generated: 0.0
- recovery_cycles_count: 0
- limit_total_used_percent: 21.0
- limit_net_used_percent: 10.0
- min_equity: -5684.16
- max_used_margin: 4200.0
- min_free_margin: -9884.16
- min_margin_level_percent: -135.34
- stop_out_triggered: True
- violations_count: 0
- final_status: FAIL_STOP_OUT

### Event trace (first 10)
- step 1 price=1.212 event=OPEN_SECTION tail=1.0 sec=1 cycle=-16.36 eq=9983.64 margin=391.52% close=0.0 violation=-
- step 2 price=1.248 event=OPEN_SECTION tail=1.0 sec=2 cycle=-16.36 eq=9967.28 margin=321.53% close=0.0 violation=-
- step 3 price=1.212 event=OPEN_SECTION tail=1.0 sec=3 cycle=-16.36 eq=9950.92 margin=272.63% close=0.0 violation=-
- step 4 price=1.248 event=OPEN_SECTION tail=1.0 sec=4 cycle=-16.36 eq=9934.56 margin=236.54% close=0.0 violation=-
- step 5 price=1.212 event=WAIT tail=1.0 sec=4 cycle=-16.36 eq=9918.2 margin=236.15% close=0.0 violation=-
- step 6 price=1.248 event=WAIT tail=1.0 sec=4 cycle=-16.36 eq=9901.84 margin=235.76% close=0.0 violation=-
- step 7 price=1.212 event=WAIT tail=1.0 sec=4 cycle=-13.29 eq=9888.55 margin=235.44% close=0.0 violation=-
- step 8 price=1.248 event=WAIT tail=1.0 sec=4 cycle=-16.36 eq=9872.19 margin=235.05% close=0.0 violation=-
- step 9 price=1.212 event=WAIT tail=1.0 sec=4 cycle=-16.36 eq=9855.83 margin=234.66% close=0.0 violation=-
- step 10 price=1.248 event=WAIT tail=1.0 sec=4 cycle=-16.36 eq=9839.47 margin=234.27% close=0.0 violation=-

### Event trace (last 10)
- step 991 price=1.212 event=WAIT tail=1.0 sec=4 cycle=-16.36 eq=-5539.99 margin=-131.9% close=0.0 violation=-
- step 992 price=1.248 event=WAIT tail=1.0 sec=4 cycle=-16.36 eq=-5556.35 margin=-132.29% close=0.0 violation=-
- step 993 price=1.212 event=WAIT tail=1.0 sec=4 cycle=-16.36 eq=-5572.71 margin=-132.68% close=0.0 violation=-
- step 994 price=1.248 event=WAIT tail=1.0 sec=4 cycle=-13.29 eq=-5586.0 margin=-133.0% close=0.0 violation=-
- step 995 price=1.212 event=WAIT tail=1.0 sec=4 cycle=-16.36 eq=-5602.36 margin=-133.39% close=0.0 violation=-
- step 996 price=1.248 event=WAIT tail=1.0 sec=4 cycle=-16.36 eq=-5618.72 margin=-133.78% close=0.0 violation=-
- step 997 price=1.212 event=WAIT tail=1.0 sec=4 cycle=-16.36 eq=-5635.08 margin=-134.17% close=0.0 violation=-
- step 998 price=1.248 event=WAIT tail=1.0 sec=4 cycle=-16.36 eq=-5651.44 margin=-134.56% close=0.0 violation=-
- step 999 price=1.212 event=WAIT tail=1.0 sec=4 cycle=-16.36 eq=-5667.8 margin=-134.95% close=0.0 violation=-
- step 1000 price=1.248 event=WAIT tail=1.0 sec=4 cycle=-16.36 eq=-5684.16 margin=-135.34% close=0.0 violation=-

### Violation events
- none

## spike
- steps: 1000
- opens: 26
- closes: 22
- tail_lot_start: 1.0
- tail_lot_end: 0.71
- reserve_start: 0.0
- reserve_end: 109.92
- recovery_start: 0.0
- recovery_end: 4.68
- max_floating_loss: -12915.0
- max_drawdown_money: 12800.4
- max_drawdown_percent: 128.0
- max_total_lot: 4.2
- max_net_lot: 1.0
- max_active_sections: 4
- max_consecutive_no_close_steps: 44
- tail_reduction: 0.29
- reserve_generated: 109.92
- recovery_cycles_count: 22
- limit_total_used_percent: 21.0
- limit_net_used_percent: 10.0
- min_equity: -2800.4
- max_used_margin: 4200.0
- min_free_margin: -5160.4
- min_margin_level_percent: -118.66
- stop_out_triggered: True
- violations_count: 0
- final_status: FAIL_STOP_OUT

### Event trace (first 10)
- step 1 price=1.2376 event=OPEN_SECTION tail=1.0 sec=1 cycle=-20.1 eq=9979.9 margin=391.37% close=0.0 violation=-
- step 2 price=1.2227 event=OPEN_SECTION tail=1.0 sec=2 cycle=-20.21 eq=9959.68 margin=321.28% close=0.0 violation=-
- step 3 price=1.2376 event=OPEN_SECTION tail=1.0 sec=3 cycle=-20.1 eq=9939.58 margin=272.32% close=0.0 violation=-
- step 4 price=1.222 event=OPEN_SECTION tail=1.0 sec=4 cycle=-19.96 eq=9919.62 margin=236.18% close=0.0 violation=-
- step 5 price=1.2217 event=WAIT tail=1.0 sec=4 cycle=-19.85 eq=9899.77 margin=235.71% close=0.0 violation=-
- step 6 price=1.2273 event=WAIT tail=1.0 sec=4 cycle=-21.87 eq=9877.9 margin=235.19% close=0.0 violation=-
- step 7 price=1.2261 event=WAIT tail=1.0 sec=4 cycle=-21.07 eq=9856.83 margin=234.69% close=0.0 violation=-
- step 8 price=1.2215 event=WAIT tail=1.0 sec=4 cycle=-19.78 eq=9837.05 margin=234.22% close=0.0 violation=-
- step 9 price=1.2369 event=WAIT tail=1.0 sec=4 cycle=-20.36 eq=9816.69 margin=233.73% close=0.0 violation=-
- step 10 price=1.2249 event=WAIT tail=1.0 sec=4 cycle=-21.0 eq=9795.69 margin=233.23% close=0.0 violation=-

### Event trace (last 10)
- step 991 price=1.2215 event=OPEN_SECTION tail=0.71 sec=4 cycle=-3.17 eq=-2769.68 margin=-117.36% close=0.0 violation=-
- step 992 price=1.2293 event=WAIT tail=0.71 sec=4 cycle=-3.6 eq=-2773.28 margin=-117.51% close=0.0 violation=-
- step 993 price=1.2253 event=WAIT tail=0.71 sec=4 cycle=-3.43 eq=-2776.71 margin=-117.66% close=0.0 violation=-
- step 994 price=1.2368 event=WAIT tail=0.71 sec=4 cycle=-3.13 eq=-2779.84 margin=-117.79% close=0.0 violation=-
- step 995 price=1.2327 event=WAIT tail=0.71 sec=4 cycle=-3.57 eq=-2783.41 margin=-117.94% close=0.0 violation=-
- step 996 price=1.2386 event=WAIT tail=0.71 sec=4 cycle=-3.17 eq=-2786.57 margin=-118.08% close=0.0 violation=-
- step 997 price=1.2302 event=WAIT tail=0.71 sec=4 cycle=-3.6 eq=-2790.17 margin=-118.23% close=0.0 violation=-
- step 998 price=1.2232 event=WAIT tail=0.71 sec=4 cycle=-3.29 eq=-2793.46 margin=-118.37% close=0.0 violation=-
- step 999 price=1.2321 event=WAIT tail=0.71 sec=4 cycle=-3.61 eq=-2797.07 margin=-118.52% close=0.0 violation=-
- step 1000 price=1.2237 event=WAIT tail=0.71 sec=4 cycle=-3.32 eq=-2800.4 margin=-118.66% close=0.0 violation=-

### Violation events
- none

## gap
- steps: 1000
- opens: 13
- closes: 9
- tail_lot_start: 1.0
- tail_lot_end: 0.72
- reserve_start: 0.0
- reserve_end: 196.81
- recovery_start: 0.0
- recovery_end: 3.24
- max_floating_loss: -15510.65
- max_drawdown_money: 15318.37
- max_drawdown_percent: 153.18
- max_total_lot: 4.2
- max_net_lot: 1.0
- max_active_sections: 4
- max_consecutive_no_close_steps: 109
- tail_reduction: 0.28
- reserve_generated: 196.81
- recovery_cycles_count: 9
- limit_total_used_percent: 21.0
- limit_net_used_percent: 10.0
- min_equity: -5318.37
- max_used_margin: 4200.0
- min_free_margin: -8318.37
- min_margin_level_percent: -207.45
- stop_out_triggered: True
- violations_count: 0
- final_status: FAIL_STOP_OUT

### Event trace (first 10)
- step 1 price=1.2242 event=OPEN_SECTION tail=1.0 sec=1 cycle=-20.75 eq=9979.25 margin=391.34% close=0.0 violation=-
- step 2 price=1.2291 event=OPEN_SECTION tail=1.0 sec=2 cycle=-22.0 eq=9957.25 margin=321.2% close=0.0 violation=-
- step 3 price=1.233 event=OPEN_SECTION tail=1.0 sec=3 cycle=-21.76 eq=9935.49 margin=272.21% close=0.0 violation=-
- step 4 price=1.2282 event=OPEN_SECTION tail=1.0 sec=4 cycle=-22.1 eq=9913.39 margin=236.03% close=0.0 violation=-
- step 5 price=1.2314 event=WAIT tail=1.0 sec=4 cycle=-22.05 eq=9891.34 margin=235.51% close=0.0 violation=-
- step 6 price=1.22 event=WAIT tail=1.0 sec=4 cycle=-19.24 eq=9872.1 margin=235.05% close=0.0 violation=-
- step 7 price=1.2281 event=WAIT tail=1.0 sec=4 cycle=-22.11 eq=9850.0 margin=234.52% close=0.0 violation=-
- step 8 price=1.2402 event=WAIT tail=1.0 sec=4 cycle=-19.17 eq=9830.83 margin=234.07% close=0.0 violation=-
- step 9 price=1.2259 event=WAIT tail=1.0 sec=4 cycle=-21.36 eq=9809.46 margin=233.56% close=0.0 violation=-
- step 10 price=1.237 event=WAIT tail=1.0 sec=4 cycle=-20.32 eq=9789.14 margin=233.07% close=0.0 violation=-

### Event trace (last 10)
- step 991 price=1.2327 event=OPEN_SECTION tail=0.72 sec=4 cycle=-5.57 eq=-5263.05 margin=-205.59% close=0.0 violation=-
- step 992 price=1.2238 event=WAIT tail=0.72 sec=4 cycle=-5.26 eq=-5268.32 margin=-205.79% close=0.0 violation=-
- step 993 price=1.2364 event=WAIT tail=0.72 sec=4 cycle=-5.24 eq=-5273.56 margin=-206.0% close=0.0 violation=-
- step 994 price=1.2193 event=WAIT tail=0.72 sec=4 cycle=-4.45 eq=-5278.01 margin=-206.17% close=0.0 violation=-
- step 995 price=1.2329 event=WAIT tail=0.72 sec=4 cycle=-5.55 eq=-5283.56 margin=-206.39% close=0.0 violation=-
- step 996 price=1.2302 event=WAIT tail=0.72 sec=4 cycle=-5.6 eq=-5289.16 margin=-206.61% close=0.0 violation=-
- step 997 price=1.2223 event=WAIT tail=0.72 sec=4 cycle=-5.13 eq=-5294.29 margin=-206.81% close=0.0 violation=-
- step 998 price=1.2314 event=WAIT tail=0.72 sec=4 cycle=-5.61 eq=-5299.91 margin=-207.03% close=0.0 violation=-
- step 999 price=1.2341 event=WAIT tail=0.72 sec=4 cycle=-5.45 eq=-5305.35 margin=-207.24% close=0.0 violation=-
- step 1000 price=1.2364 event=WAIT tail=0.72 sec=4 cycle=-5.24 eq=-5310.6 margin=-207.45% close=0.0 violation=-

### Violation events
- none

## monte_carlo_summary
- number_of_runs: 200
- seed: 42
- regimes: random_walk, mean_reversion, trend_with_pullbacks, high_volatility, gap_sequence
- tail_lot_end min/max/avg: 0.7100/1.0000/0.9289
- reserve_end min/max/avg: 0.00/64.40/20.59
- drawdown min/max/avg: 1365.22/6329.66/4558.68
- worst_case_run: mean_reversion_27 (drawdown=6329.66)
- violations_total: 0
- runs_with_violations: 0

## Final status
Initial formula validation: PASS
Workbook runtime validation: PASS
Stress report structure: PASS
Stress test quality: ACCEPTED
Final trading readiness: NOT ACCEPTED YET