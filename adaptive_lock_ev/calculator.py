from math import floor

def _round_lot(lot, step, min_lot=0.0):
    if step <= 0:
        return round(max(min_lot, lot), 8)
    v = floor(lot / step) * step
    return round(max(min_lot, v), 8)

def _regime(v, mean_max=1.2, volatile=1.5):
    if v > volatile:
        return "VOLATILE"
    if v < mean_max:
        return "MEAN_REVERT"
    return "NEUTRAL"

def _state(dd, stress=0.07, escape=0.15):
    if dd > escape:
        return "ESCAPE"
    if dd > stress:
        return "STRESS"
    return "FLOW"

def _position_pnl_per_lot(pos, current_price, point, pip_value):
    if pos["type"] == "BUY":
        points = (current_price - pos.get("open_price", current_price)) / point
    else:
        points = (pos.get("open_price", current_price) - current_price) / point
    return points * pip_value

def select_positions_for_closing(positions, direction, current_price, point, pip_value):
    opposite = "BUY" if direction == "SELL" else "SELL"
    candidates = [p for p in positions if p["type"] == opposite and p.get("lot", 0) > 0]
    ranked = sorted(candidates, key=lambda p: _position_pnl_per_lot(p, current_price, point, pip_value), reverse=True)
    return ranked

def get_recommendation(current_price, ema, atr_short, atr_long, positions, broker_params, symbol_params, system_params):
    point = symbol_params["point"]; digits = int(symbol_params["digits"]); pip_value = symbol_params["pip_value_1_lot"]
    z = (current_price - ema) / atr_short if atr_short else 0.0
    v = atr_short / atr_long if atr_long else 0.0
    regime = _regime(v, system_params["v_mean_revert_max"], system_params["v_volatile_stop"])
    confidence = min(abs(z) / 2.0, 1.0)
    q_base = max(system_params["q_min"], min(system_params["q_min"] + system_params["q_min"] * confidence, system_params["q_max"]))
    beta = 0.7 - 0.4 * confidence
    dd = broker_params.get("current_dd", 0.0)
    if dd > system_params["dd_beta_protection"]: beta = system_params["beta_dd_protection"]
    state = _state(dd, system_params["dd_stress_level"], system_params["dd_escape_level"])
    q_final = q_base
    if regime == "NEUTRAL" or state == "STRESS": q_final *= 0.5
    anti_acc = broker_params.get("last_10_cycles_pnl", 0.0) <= 0
    block_new_cycles = False
    if anti_acc:
        q_final *= system_params.get("anti_accumulation_q_multiplier", 0.5)
        beta = 0.8
        block_new_cycles = True
    if regime == "VOLATILE": q_final = 0.0
    total_buy = sum(p["lot"] for p in positions if p["type"] == "BUY")
    total_sell = sum(p["lot"] for p in positions if p["type"] == "SELL")
    l_total = total_buy + total_sell; exposure = abs(total_buy - total_sell)
    risk_ok = l_total <= system_params["max_total_lot"] and exposure <= system_params["max_exposure"] and state != "ESCAPE"
    spread_cost = broker_params["spread_points"] * q_final * pip_value
    slippage_cost = broker_params["slippage_points"] * q_final * pip_value
    commission = broker_params["commission_per_lot"] * q_final
    swap = max(broker_params.get("swap_buy", 0.0), broker_params.get("swap_sell", 0.0)) * q_final
    total_cost = spread_cost + slippage_cost + commission + swap
    min_move_points = (total_cost * system_params["safety_cost_multiplier"]) / (q_final * pip_value) if q_final > 0 else 0.0
    min_move_price = min_move_points * point
    mu = system_params.get("expected_mean_reversion_points", 6.0)
    ev = mu * q_final * pip_value - total_cost
    ev_ok = ev > system_params["min_ev_required"]
    can_open = regime != "VOLATILE" and state != "ESCAPE" and risk_ok and ev_ok and q_final > 0 and not block_new_cycles
    trigger_up = round(current_price + min_move_price, digits); trigger_down = round(current_price - min_move_price, digits)
    q_rounded = _round_lot(q_final, broker_params["lot_step"], broker_params["min_lot"]) if q_final > 0 else 0.0
    scenario_up, scenario_down = [], []
    if not ev_ok:
        scenario_up.append({"action":"NO_ACTION","comment":"EV <= 0, entries blocked"})
        scenario_down.append({"action":"NO_ACTION","comment":"EV <= 0, entries blocked"})
    else:
        if can_open and z >= system_params["z_entry_level"]:
            scenario_up.append({"action":"OPEN","type":"SELL","price":trigger_up,"lot":q_rounded,"comment":"Mean reversion SELL"})
            for p in select_positions_for_closing(positions, "SELL", current_price, point, pip_value)[:1]:
                pnl_per_lot = max(_position_pnl_per_lot(p, trigger_up, point, pip_value), 0.0)
                expected_pnl = max(q_final * min_move_points * pip_value - total_cost, 0.0)
                unlock_money = beta * expected_pnl
                closable = 0.0
                if pnl_per_lot > 0 and unlock_money > 0:
                    raw=min(p.get('lot',0), unlock_money / pnl_per_lot)
                    closable=min(p.get('lot',0), max(broker_params['lot_step'], _round_lot(raw, broker_params['lot_step'], 0.0)))
                if closable > 0:
                    scenario_up.append({"action":"PARTIAL_CLOSE","id":p.get('id'),"type":p['type'],"price":trigger_up,"lot":closable,"comment":"Unlock by beta"})
        else:
            scenario_up.append({"action":"NO_ACTION","comment":"No valid edge or blocked by risk/regime/state"})
        if can_open and z <= -system_params["z_entry_level"]:
            scenario_down.append({"action":"OPEN","type":"BUY","price":trigger_down,"lot":q_rounded,"comment":"Mean reversion BUY"})
        else:
            scenario_down.append({"action":"NO_ACTION","comment":"No valid edge or blocked by risk/regime/state"})
    return {"state":state,"regime":regime,"z":z,"v":v,"q":q_final,"beta":beta,"ev":ev,"min_move_points":min_move_points,
            "scenario_up":scenario_up,"scenario_down":scenario_down,"block_new_cycles":block_new_cycles}
