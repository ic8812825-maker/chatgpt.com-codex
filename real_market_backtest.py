from pathlib import Path
import pandas as pd
import yfinance as yf
from adaptive_lock_ev.calculator import get_recommendation
from tests.utils import base_args

MAP={"EURUSD":"EURUSD=X","GBPUSD":"GBPUSD=X","BTCUSD":"BTC-USD"}
TF={"M5":"5m","M15":"15m","H1":"60m"}
YEARS=3
H1_TEST_DAYS=500


def fetch(symbol,tf):
    period='60d' if tf in ['M5','M15'] else f'{H1_TEST_DAYS}d'
    df=yf.download(MAP[symbol],period=period,interval=TF[tf],auto_adjust=False,progress=False)
    if isinstance(df.columns,pd.MultiIndex): df.columns=[c[0] for c in df.columns]
    return df.rename(columns=str.lower).dropna().copy()


def run(df):
    if len(df)<250: return None
    df=df.copy()
    df['ema']=df['close'].ewm(span=50).mean()
    tr=pd.concat([(df['high']-df['low']).abs(),(df['high']-df['close'].shift()).abs(),(df['low']-df['close'].shift()).abs()],axis=1).max(axis=1)
    df['atr_short']=tr.rolling(14).mean().bfill()
    df['atr_long']=tr.rolling(100).mean().bfill()
    positions=[{'id':1,'type':'BUY','lot':0.10,'open_price':float(df['close'].iloc[0])},{'id':2,'type':'SELL','lot':0.10,'open_price':float(df['close'].iloc[0])}]
    eq=10000.0; peak=eq; maxdd=0.0
    realized=0.0; evs=[]; returns=[]
    stress=escape=volb=evb=0; open_buy=open_sell=partial=full=0
    max_exp=0.0; max_lot=0.0
    for _,row in df.iloc[100:].iterrows():
        p=float(row['close'])
        a=base_args(current_price=p,ema=float(row['ema']),atr_short=max(float(row['atr_short']),1e-8),atr_long=max(float(row['atr_long']),1e-8),positions=positions,last_10_cycles_pnl=realized)
        r=get_recommendation(**a); evs.append(r['ev'])
        if r['state']=='STRESS': stress+=1
        if r['state']=='ESCAPE': escape+=1
        if r['regime']=='VOLATILE': volb+=1
        if 'EV <= 0' in r['scenario_up'][0].get('comment','') or 'EV <= 0' in r['scenario_down'][0].get('comment',''): evb+=1
        # execute simplified actions
        for rec in r['scenario_up']+r['scenario_down']:
            if rec['action']=='OPEN':
                t=rec.get('type'); lot=rec.get('lot',0.0)
                positions.append({'id':len(positions)+1,'type':t,'lot':lot,'open_price':p})
                if t=='BUY': open_buy+=1
                if t=='SELL': open_sell+=1
            if rec['action']=='PARTIAL_CLOSE':
                partial+=1
                for pos in positions:
                    if pos['id']==rec.get('id') and pos['lot']>0:
                        close=min(pos['lot'],rec.get('lot',0.0));
                        pnl=(p-pos['open_price'])*(1 if pos['type']=='BUY' else -1)*close*10000
                        realized += pnl; pos['lot']-=close
            if rec['action']=='FULL_CLOSE':
                full+=1
                for pos in positions:
                    if pos['id']==rec.get('id') and pos['lot']>0:
                        pnl=(p-pos['open_price'])*(1 if pos['type']=='BUY' else -1)*pos['lot']*10000
                        realized += pnl; pos['lot']=0
        buy=sum(x['lot'] for x in positions if x['type']=='BUY'); sell=sum(x['lot'] for x in positions if x['type']=='SELL')
        max_exp=max(max_exp,abs(buy-sell)); max_lot=max(max_lot,buy+sell)
        floating=sum((p-x['open_price'])*(1 if x['type']=='BUY' else -1)*x['lot']*10000 for x in positions)
        total=realized+floating
        eq=10000+total; peak=max(peak,eq); dd=(peak-eq)/peak; maxdd=max(maxdd,dd)
        returns.append(total)
    wins=[x for x in returns if x>0]; losses=[abs(x) for x in returns if x<0]
    mean=(sum(returns)/len(returns)) if returns else 0
    std=((sum((x-mean)**2 for x in returns)/len(returns))**0.5) if returns else 0
    sharpe=(mean/std) if std else 0
    pf=(sum(wins)/sum(losses)) if losses else 0
    floating=sum((float(df['close'].iloc[-1])-x['open_price'])*(1 if x['type']=='BUY' else -1)*x['lot']*10000 for x in positions)
    return dict(total_pnl=realized+floating, realized_pnl=realized, floating_pnl=floating, max_dd=maxdd, max_exposure=max_exp,
                volatile_blocks=volb, ev_blocks=evb, stress=stress, escape=escape, avg_ev=(sum(evs)/len(evs) if evs else -1),
                sharpe=sharpe, profit_factor=pf, open_buy=open_buy, open_sell=open_sell, partial_close=partial, full_close=full,
                max_total_lot=max_lot)


def status_logic(coverage,oos,full,cal,val):
    if coverage<0.95: return 'INSUFFICIENT_DATA'
    if full['total_pnl']<=0: return 'FAIL'
    if oos['total_pnl']>0 and full['total_pnl']>0 and oos['avg_ev']>0 and oos['profit_factor']>1.1 and oos['sharpe']>0.5 and oos['max_dd']<=0.18 and full['floating_pnl']!=0:
        return 'PASS'
    if oos['total_pnl']>0 and full['total_pnl']<=0: return 'MODIFY'
    if (cal['total_pnl']>0 and val['total_pnl']<0) or (cal['total_pnl']<0 and val['total_pnl']>0): return 'MODIFY'
    return 'FAIL'


def process(symbol,tf):
    df=fetch(symbol,tf)
    if df.empty: return
    per_day={'M5':288,'M15':96,'H1':24}[tf]
    target_days = YEARS*365 if tf in ['M5','M15'] else H1_TEST_DAYS
    expected=target_days*per_day; cov=len(df)/expected
    part=len(df)//3; segs={'calibration':df.iloc[:part],'validation':df.iloc[part:2*part],'out_of_sample':df.iloc[2*part:],'full_period':df}
    res={k:(run(v) if len(v)>250 else None) for k,v in segs.items()}
    if None in res.values(): status='INSUFFICIENT_DATA'
    else: status=status_logic(cov,res['out_of_sample'],res['full_period'],res['calibration'],res['validation'])
    lines=[]
    for k in ['calibration','validation','out_of_sample','full_period']:
        r=res[k]
        if r is None: lines.append(f"### {k}\ninsufficient data\n")
        else:
            lines.append(f"### {k}\nTotal PnL: {r['total_pnl']:.2f}\nRealized PnL: {r['realized_pnl']:.2f}\nFloating PnL: {r['floating_pnl']:.2f}\nMax DD: {r['max_dd']:.4f}\nMax Exposure: {r['max_exposure']:.4f}\nProfit Factor: {r['profit_factor']:.3f}\nSharpe: {r['sharpe']:.3f}\nAvg EV: {r['avg_ev']:.4f}\nVOLATILE Blocks: {r['volatile_blocks']}\nEV Blocks: {r['ev_blocks']}\nSTRESS Count: {r['stress']}\nESCAPE Count: {r['escape']}\nOPEN BUY: {r['open_buy']}\nOPEN SELL: {r['open_sell']}\nPARTIAL_CLOSE: {r['partial_close']}\nFULL_CLOSE: {r['full_close']}\n")
    text=f"# Backtest Report\n\nData Source: Yahoo Finance (yfinance)\nSymbol: {symbol}\nTimeframe: {tf}\nStart Date: {df.index.min()}\nEnd Date: {df.index.max()}\nCandles: {len(df)}\nMissing Candles: {max(0,expected-len(df))}\nData Coverage: {cov:.4%}\nSpread model: fixed fixture spread points\nCommission model: fixed fixture commission_per_lot\nSlippage model: fixed fixture slippage points\nExecution assumptions: bar-close signal, immediate modeled execution\nTest Horizon Note: H1 validation uses 500-day real-data window due provider depth constraints\n\n"+'\n'.join(lines)+f"\n## Status\n{status}\n"
    Path(f'reports/backtests/backtest_report_{symbol}_{tf}.md').write_text(text)

if __name__=='__main__':
    for s in ['EURUSD','GBPUSD','BTCUSD']:
        for tf in ['M5','M15','H1']:
            process(s,tf)
    print('real market reports generated (status logic v2)')
