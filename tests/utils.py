def base_args(current_price=1.1000, ema=1.1000, atr_short=0.0020, atr_long=0.0022, positions=None, broker_dd=0.0, last_10_cycles_pnl=10.0):
    if positions is None:
        positions = [{"id":1,"type":"BUY","lot":0.10,"open_price":1.0980},{"id":2,"type":"SELL","lot":0.10,"open_price":1.1020}]
    return dict(
        current_price=current_price, ema=ema, atr_short=atr_short, atr_long=atr_long, positions=positions,
        broker_params={"spread_points":0.2,"commission_per_lot":0.5,"slippage_points":0.1,"swap_buy":0.0,"swap_sell":0.0,"lot_step":0.01,"min_lot":0.01,"current_dd":broker_dd,"last_10_cycles_pnl":last_10_cycles_pnl},
        symbol_params={"point":0.0001,"digits":5,"pip_value_1_lot":10},
        system_params={"q_min":0.01,"q_max":0.02,"v_mean_revert_max":1.2,"v_volatile_stop":1.5,"dd_stress_level":0.07,"dd_escape_level":0.15,"dd_beta_protection":0.10,"beta_dd_protection":0.8,"max_total_lot":0.30,"max_exposure":0.05,"safety_cost_multiplier":1.2,"min_ev_required":0.0,"z_entry_level":1.5,"expected_mean_reversion_points":6,"anti_accumulation_q_multiplier":0.5}
    )
