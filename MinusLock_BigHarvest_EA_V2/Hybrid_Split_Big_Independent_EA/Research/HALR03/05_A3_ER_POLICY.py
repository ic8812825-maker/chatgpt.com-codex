"""Service-window admission and dynamic A3 exposure."""
from dataclasses import replace

from pinned import source
source()
from a3rc import choices_a3, target
from ledger2 import TICKS, fee
from risk import close_plan, gate


def exit_status(v,env):
    if not v.book.gross and not v.active:
        return "EXIT_GUARANTEED_WITHIN_CONTRACT"
    next_event=env.next_service(v.step)
    if next_event is None:
        if env.name=="E6":
            return "EXIT_IMPOSSIBLE_IN_SCENARIO"
        return "EXIT_NOT_GUARANTEED"
    if v.step%env.stride==0 and not (
            v.active or v.quote.delay or v.quote.unknown or v.rejects
            or v.capacity<v.book.gross):
        return "EXIT_GUARANTEED_WITHIN_CONTRACT"
    if not v.active and next_event<=v.book.limits.horizon:
        return "EXIT_GUARANTEED_WITHIN_CONTRACT"
    return "EXIT_NOT_GUARANTEED"


def context(v,env):
    if env.stride is None or env.move is None or env.move<=0:
        return None
    return replace(env,window=env.next_service(v.step)-v.step)


def net_room(book,q,ctx):
    distance=ctx.window*ctx.move
    if distance<=0:
        return 0
    expensive=replace(q,spread=ctx.spread,slip=ctx.slip)
    surcharge=max(0,fee(expensive,book.limits)-fee(q,book.limits))*book.gross
    carry=ctx.carry*ctx.window*book.gross
    room=(book.limits.loss-ctx.reserve)*TICKS+book.mark(q)-surcharge-carry
    return min(book.limits.net,max(0,room//(2*distance)))


def observed_contract(v,env):
    q=v.quote
    if (q.spread>env.spread or q.slip>env.slip or q.carry>env.carry
            or abs(q.mid-v.previous_mid)>env.move):
        return False
    if v.step%env.stride:
        return True
    return not (q.delay or q.unknown or v.rejects or v.capacity<v.book.gross)


def er_options(v,p,m,env):
    ctx=context(v,env)
    if ctx is None or not observed_contract(v,env):
        return
    if v.step%env.stride!=0:
        if exit_status(v,env)=="EXIT_GUARANTEED_WITHIN_CONTRACT":
            yield "SERVICE_WAIT",(),m,v.book
        return
    size=int(min(p.net,net_room(v.book,v.quote,ctx)))
    request=[]
    if size:
        request.extend(choices_a3(v,replace(p,net=size),m))
    else:
        request.append(("HOLD",(),m))
    neutral=target(v.book,v.quote,0,p.core,allow_open=False)
    if v.book.net and neutral:
        request.insert(-1,("DE_RISK",neutral,m))
    for label,plan,nxt in request:
        b,_=gate(v,plan,ctx)
        if b is not None:
            yield label,plan,nxt,b


def choose_er(v,p,m,env):
    return next(er_options(v,p,m,env),("SAFE",None,replace(m,exiting=True),None))


def er_close(v,p,m,env,keep_running=False):
    ctx=context(v,env)
    if ctx is None or v.step%env.stride:
        return None
    plan=close_plan(v.book,v.quote)
    b,_=gate(v,plan,ctx)
    if b is None:
        return None
    if keep_running:
        return "SWITCH_B",plan,replace(m,b_mode=True,anchor=v.quote.mid),b
    return "K_EXIT",plan,replace(m,exiting=True),b
