import random, math

ACCOUNT=10000; LEVERAGE=200; CONTRACT=100000; MARGIN_PER_LOT=CONTRACT/LEVERAGE; STOP_OUT=50

def flr(x,s=0.01): return math.floor(x/s)*s

def move(kind,i,r,gap_mult=1.0):
    if kind=='trend_up': return 120 + (20 if i%10==0 else -15 if i%7==0 else 0)
    if kind=='trend_down': return -(120 + (20 if i%10==0 else -15 if i%7==0 else 0))
    if kind=='flat': return r.randint(-40,40)
    if kind=='flat_with_level_touch': return 170 if i%25==0 else r.randint(-35,35)
    if kind=='whipsaw': return 200 if i%2==0 else -200
    if kind=='spike': return int((900 if i%35==0 else r.randint(-120,120))*gap_mult)
    if kind=='gap': return int((1600 if i%70==0 else r.randint(-140,140))*gap_mult)
    return r.randint(-260,260)

def run(params,kind,steps=10000,seed=1,spread_mult=1.0,gap_mult=1.0,commission=0.0,swap=0.0):
    base,big,small,max_sec,step_pts,max_total,max_net,min_margin,max_dd = params
    tail=base; reserve=0; recovery=0; active=0
    floating=0; peak=ACCOUNT; min_m=float('inf'); maxdd=0; closes=0; viol=0; stop=False
    used_start=max(2*base*MARGIN_PER_LOT,0.01)
    level_hits=sections_opened=price_moves=floating_changes=0; prev=0; close_sum=0
    r=random.Random(seed)
    for i in range(1,steps+1):
        mv=move(kind,i,r,gap_mult)
        if mv!=0: price_moves+=1
        if abs(mv)>=step_pts:
            level_hits+=1
            if active<max_sec and tail>=0.01: active+=1; sections_opened+=1
        b=flr(max(0.01,tail*big)); sm=flr(max(0.01,tail*small))
        total=2*base + active*(b+sm); net=abs((base+active*sm)-(base+active*b))
        used=max(total*MARGIN_PER_LOT,0.01)
        mom=abs(mv)/100
        bonus=1.8 if (i%9==0 or i%14==0) else 1.0
        big_p=max(0,mom-0.12)*b*16*bonus
        sm_p=-max(0,mom-0.04)*sm*2.5
        costs=(b+sm)*(step_pts*0.05*spread_mult + commission + swap)
        cyc=big_p+sm_p-costs
        floating += cyc
        if abs(floating-prev)>1e-9: floating_changes+=1
        prev=floating
        eq=ACCOUNT+reserve+recovery+floating
        peak=max(peak,eq)
        dd=(peak-eq)/ACCOUNT*100; maxdd=max(maxdd,dd)
        margin=eq/used*100; min_m=min(min_m,margin)
        if margin<=STOP_OUT: stop=True
        if cyc>0 and active>0:
            closes+=1
            reserve += cyc*0.2; recovery += cyc*0.8
            loss=max(30,abs(mv)); c=flr(min(tail,recovery/loss))
            if c>=0.01: recovery-=c*loss; tail=max(0,tail-c); close_sum += c
            active=max(0,active-1)
        if total>max_total or net>max_net or recovery<0 or reserve<0 or tail<0: viol+=1
    invalid=(used_start<=0 or price_moves<=0 or level_hits<=0 or sections_opened<=0 or floating_changes<=0)
    return dict(kind=kind,closes=closes,tail_end=round(tail,4),tail_reduction=round(base-tail,4),recovery_close_lot_sum=round(close_sum,4),reserve=round(reserve,2),max_dd=round(maxdd,2),min_margin=round(min_m,2),stop_out=stop,violations=viol,invalid_setup=invalid,used_margin_start=round(used_start,2),price_moves_count=price_moves,level_hits_count=level_hits,sections_opened_count=sections_opened,floating_pnl_changes_count=floating_changes)
