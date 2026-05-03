import csv, random
from datetime import datetime, timedelta
from pathlib import Path
from statistics import mean
from adaptive_lock_ev.calculator import get_recommendation

SEED=42; BARS=450; START_PRICE=1.1000; ATR_LONG_PERIOD=100

def generate_synthetic_bars(seed=SEED, bars=BARS, start_price=START_PRICE):
    random.seed(seed); result=[]; price=start_price; dt=datetime(2026,1,1)
    for i in range(bars):
        open_price=price
        if i<120: phase='warmup_quiet'; price += random.uniform(-0.0002,0.0002)
        elif i<170: phase='down_impulse'; price -= 0.00045
        elif i<220: phase='down_revert'; price += 0.00030
        elif i<270: phase='up_impulse'; price += 0.00045
        elif i<320: phase='up_revert'; price -= 0.00030
        elif i<380: phase='trend'; price += 0.00025
        else: phase='volatile'; price += random.uniform(-0.0015,0.0015)
        close_price=price
        high=max(open_price,close_price)+random.uniform(0,0.0001)
        low=min(open_price,close_price)-random.uniform(0,0.0001)
        result.append({'datetime':dt,'phase':phase,'open':round(open_price,5),'high':round(high,5),'low':round(low,5),'close':round(close_price,5),'volume':100,'spread':2})
        dt += timedelta(minutes=15)
    return result

def run():
    bars=generate_synthetic_bars(); closes=[b['close'] for b in bars]
    positions=[{'id':1,'type':'BUY','open_price':START_PRICE,'lot':0.10},{'id':2,'type':'SELL','open_price':START_PRICE,'lot':0.10}]
    realized=0.0; out=[]; down_rows=[]
    stats=dict(open_buy=0,open_sell=0,partial=0,full=0,no_action=0,vol_block=0,ev_block=0,risk_block=0,max_total=0,max_exp=0,unlock_success=0)
    initial_locked=sum(p['lot'] for p in positions); prev_locked=initial_locked; prev_locked_loss=0.0
    down_diag=dict(z_lt=-0,ev=0,vol=0,exposure=0,projected=0,should_open=0,actual_open=0)

    for i,b in enumerate(bars, start=1):
        c=closes[max(0,i-50):i]; ema=mean(c)
        trs=[abs(bars[j]['high']-bars[j]['low']) for j in range(max(0,i-ATR_LONG_PERIOD),i)]
        atr_s=mean(trs[-14:]) if trs else 0.0001; atr_l=mean(trs[-ATR_LONG_PERIOD:]) if trs else 0.0001
        system={'q_min':0.01,'q_max':0.02,'v_mean_revert_max':1.2,'v_volatile_stop':1.5,'dd_stress_level':0.07,'dd_escape_level':0.15,'dd_beta_protection':0.10,'beta_dd_protection':0.8,'max_total_lot':0.30,'max_exposure':0.05,'safety_cost_multiplier':1.2,'min_ev_required':0.0,'z_entry_level':1.5,'expected_mean_reversion_points':8,'anti_accumulation_q_multiplier':0.5}
        broker={'spread_points':0.2,'commission_per_lot':0.1,'slippage_points':0.1,'swap_buy':0,'swap_sell':0,'lot_step':0.01,'min_lot':0.01,'current_dd':0,'last_10_cycles_pnl':1}
        symbol={'point':0.0001,'digits':5,'pip_value_1_lot':10}

        if i <= ATR_LONG_PERIOD:
            r={'z':0,'v':0,'regime':'WARMUP','state':'FLOW','q':0,'beta':0,'ev':0,'min_move_points':0,'scenario_up':[{'action':'NO_ACTION'}],'scenario_down':[{'action':'NO_ACTION'}]}
            block='BLOCK_WARMUP'; final_allowed=False
            buy_raw=sell_raw=False; regime_ok=ev_ok=risk_ok=state_ok=proj_ok=False
        else:
            r=get_recommendation(b['close'],ema,atr_s,atr_l,positions,broker,symbol,system)
            buy_raw = r['z'] < -system['z_entry_level']; sell_raw = r['z'] > system['z_entry_level']
            regime_ok = r['regime'] != 'VOLATILE'
            ev_ok = r['ev'] > system['min_ev_required']
            buy=sum(p['lot'] for p in positions if p['type']=='BUY'); sell=sum(p['lot'] for p in positions if p['type']=='SELL')
            risk_ok = (buy+sell) <= system['max_total_lot'] and abs(buy-sell) <= system['max_exposure']
            state_ok = r['state'] not in ['STRESS','ESCAPE']
            projected_buy=abs((buy+r['q'])-sell); projected_sell=abs(buy-(sell+r['q']))
            proj_ok = (projected_buy<=system['max_exposure']) if buy_raw else ((projected_sell<=system['max_exposure']) if sell_raw else True)
            final_allowed = (buy_raw or sell_raw) and regime_ok and ev_ok and risk_ok and state_ok and proj_ok
            if not (buy_raw or sell_raw): block='BLOCK_WEAK_Z'
            elif not regime_ok: block='BLOCK_VOLATILE'
            elif not ev_ok: block='BLOCK_EV'
            elif (buy+sell) > system['max_total_lot']: block='BLOCK_TOTAL_LOT'
            elif abs(buy-sell) > system['max_exposure']: block='BLOCK_EXPOSURE'
            elif not proj_ok: block='BLOCK_PROJECTED_EXPOSURE'
            elif r['state']=='STRESS': block='BLOCK_STRESS'
            elif r['state']=='ESCAPE': block='BLOCK_ESCAPE'
            elif broker['last_10_cycles_pnl']<=0: block='BLOCK_ANTI_ACCUMULATION'
            else: block='ALLOW'

        # diagnostics down phase
        if b['phase'] in ['down_impulse','down_revert']:
            down_rows.append([i,b['close'],r['z'],r['v'],r['regime'],r['state'],r['q'],r['beta'],r['ev'],buy_raw,regime_ok,ev_ok,risk_ok,proj_ok,final_allowed,block])
            if r['z'] < -1.5: down_diag['z_lt'] +=1
            if block=='BLOCK_EV': down_diag['ev'] +=1
            if block=='BLOCK_VOLATILE': down_diag['vol'] +=1
            if block=='BLOCK_EXPOSURE': down_diag['exposure'] +=1
            if block=='BLOCK_PROJECTED_EXPOSURE': down_diag['projected'] +=1
            if final_allowed and buy_raw: down_diag['should_open'] +=1

        a_up=r['scenario_up'][0]['action']; a_dn=r['scenario_down'][0]['action']
        if a_up=='NO_ACTION' and a_dn=='NO_ACTION': stats['no_action']+=1
        if r['regime']=='VOLATILE': stats['vol_block']+=1
        if block=='BLOCK_EV': stats['ev_block']+=1

        for rec in r['scenario_up']+r['scenario_down']:
            if rec['action']=='OPEN':
                buy=sum(p['lot'] for p in positions if p['type']=='BUY'); sell=sum(p['lot'] for p in positions if p['type']=='SELL'); lot=rec.get('lot',0)
                projected=abs((buy+lot)-sell) if rec.get('type')=='BUY' else abs(buy-(sell+lot))
                if projected > system['max_exposure']:
                    stats['risk_block']+=1; continue
                positions.append({'id':len(positions)+1,'type':rec['type'],'open_price':rec['price'],'lot':lot})
                if rec['type']=='BUY': stats['open_buy']+=1; down_diag['actual_open'] += 1 if b['phase'] in ['down_impulse','down_revert'] else 0
                if rec['type']=='SELL': stats['open_sell']+=1
            elif rec['action']=='PARTIAL_CLOSE':
                for p in positions:
                    if p['id']==rec.get('id') and p['lot']>0:
                        close=min(p['lot'],rec['lot']); realized += (b['close']-p['open_price'])*(1 if p['type']=='BUY' else -1)*close*10000; p['lot']-=close; stats['partial']+=1
            elif rec['action']=='FULL_CLOSE':
                for p in positions:
                    if p['id']==rec.get('id') and p['lot']>0:
                        realized += (b['close']-p['open_price'])*(1 if p['type']=='BUY' else -1)*p['lot']*10000; p['lot']=0; stats['full']+=1

        buy=sum(p['lot'] for p in positions if p['type']=='BUY'); sell=sum(p['lot'] for p in positions if p['type']=='SELL')
        total=buy+sell; exp=abs(buy-sell); stats['max_total']=max(stats['max_total'],total); stats['max_exp']=max(stats['max_exp'],exp)
        floating=sum((b['close']-p['open_price'])*(1 if p['type']=='BUY' else -1)*p['lot']*10000 for p in positions)
        locked_loss=sum(max(0,(p['open_price']-b['close'])*p['lot']*10000) if p['type']=='BUY' else max(0,(b['close']-p['open_price'])*p['lot']*10000) for p in positions)
        if total < prev_locked or locked_loss < prev_locked_loss: stats['unlock_success'] +=1
        prev_locked, prev_locked_loss = total, locked_loss
        out.append([i,b['datetime'],b['phase'],b['open'],b['high'],b['low'],b['close'],ema,atr_s,atr_l,r['z'],r['v'],r['regime'],r['state'],r['q'],r['beta'],r['ev'],r['min_move_points'],a_up,a_dn,buy,sell,total,exp,floating,realized,locked_loss,buy_raw,sell_raw,regime_ok,ev_ok,risk_ok,state_ok,proj_ok,final_allowed,block])

    final_locked=prev_locked; final_float=out[-1][24]; total_pnl=realized+final_float
    status='PASS'
    if stats['max_total']>0.30 or stats['max_exp']>0.05: status='FAIL'
    elif stats['unlock_success']==0 or final_locked>initial_locked or stats['open_buy']==0 or stats['open_sell']==0: status='MODIFY'

    rep=Path('reports/synthetic'); rep.mkdir(parents=True,exist_ok=True)
    csv_path=rep/'simple_random_test_log.csv'
    with csv_path.open('w',newline='') as f:
        w=csv.writer(f)
        w.writerow(['bar','datetime','phase','open','high','low','close','ema','atr_short','atr_long','z','v','regime','state','q','beta','ev','min_move','action_up','action_down','total_buy_lot','total_sell_lot','total_lot','exposure','floating_pnl','realized_pnl','locked_loss','buy_signal_raw','sell_signal_raw','regime_ok','ev_ok','risk_ok','state_ok','projected_exposure_ok','final_entry_allowed','block_reason_exact'])
        w.writerows(out)

    down_tbl='\n'.join([f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} | {r[7]} | {r[8]} | {r[9]} | {r[10]} | {r[11]} | {r[12]} | {r[13]} | {r[14]} | {r[15]} |" for r in down_rows[:40]])
    report=rep/'simple_random_test_report.md'
    report.write_text(f'''# Simple Random Synthetic Test Report\n\n## 1. Test Info\nVersion: v2.0\nDate: 2026-05-02\nBars: {BARS}\nSeed: {SEED}\nInitial Price: {START_PRICE}\n\n## 3. Summary Metrics\n- OPEN BUY: {stats['open_buy']}\n- OPEN SELL: {stats['open_sell']}\n- PARTIAL_CLOSE: {stats['partial']}\n- FULL_CLOSE: {stats['full']}\n- Max Total Lot: {stats['max_total']:.2f}\n- Max Exposure: {stats['max_exp']:.2f}\n- Initial Locked Volume: {initial_locked:.2f}\n- Final Locked Volume: {final_locked:.2f}\n- Realized PnL: {realized:.2f}\n- Floating PnL: {final_float:.2f}\n- Total PnL: {total_pnl:.2f}\n\n## 4. Down phase table (bars 121-220)\n| bar | close | z | v | regime | state | q | beta | ev | buy_signal_raw | regime_ok | ev_ok | risk_ok | projected_exposure_ok | final_entry_allowed | block_reason_exact |\n|---:|---:|---:|---:|---|---|---:|---:|---:|---|---|---|---|---|---|---|\n{down_tbl}\n\nDown phase diagnosis:\n- Bars with Z < -1.5: {down_diag['z_lt']}\n- Bars blocked by EV: {down_diag['ev']}\n- Bars blocked by VOLATILE: {down_diag['vol']}\n- Bars blocked by exposure: {down_diag['exposure']}\n- Bars blocked by projected exposure: {down_diag['projected']}\n- Bars where BUY should have opened: {down_diag['should_open']}\n- Actual OPEN BUY: {down_diag['actual_open']}\n\n## 8. Conclusion\n{status}\n\nThis synthetic test does not validate profitability.\nIt validates only mechanics, risk gates, recommendation logic, and reporting pipeline.\n''')
    return status, stats, str(report), str(csv_path)

if __name__=='__main__':
    print(run())
