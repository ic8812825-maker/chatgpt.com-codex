"""PROPOSED_CONTRACT only: Decimal reference, no production imports or broker IO.

History/authority arguments are independent fixtures, never real broker evidence.
In-memory apply is an arithmetic oracle, not a durable commit implementation.
"""
from dataclasses import dataclass, replace
from decimal import Decimal, ROUND_FLOOR, ROUND_HALF_EVEN
from hashlib import sha256
import json
import unicodedata

BUCKETS = ('FinalReserve', 'PartialFar', 'Transition', 'Carry', 'ResidualHeld')


def dec(value):
    if isinstance(value, (float, bool)):
        raise ValueError('implicit binary float/bool conversion forbidden')
    d = Decimal(value)
    if not d.is_finite():
        raise ValueError('nonfinite')
    return d


def quantum(digits):
    if type(digits) is not int or not 0 <= digits <= 8:
        raise ValueError('unknown precision')
    return Decimal(1).scaleb(-digits)


def canonical(value):
    def normalize(x):
        if isinstance(x, Decimal):
            d = dec(x)
            return '0' if d == 0 else format(d.normalize(), 'f')
        if isinstance(x, float):
            raise ValueError('float in canonical record')
        if isinstance(x, str):
            return unicodedata.normalize('NFC', x)
        if isinstance(x, dict):
            return {k: normalize(v) for k, v in sorted(x.items())}
        if isinstance(x, (tuple, list)):
            return [normalize(v) for v in x]
        if x is None:
            raise ValueError('unknown identity')
        return x
    return json.dumps({'schema': 'R0A-CANDIDATE-1', 'payload': normalize(value)},
                      ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def digest(value):
    return sha256(canonical(value).encode('utf-8')).hexdigest()


def namespace(owner):
    return tuple(owner[k] for k in ('broker', 'server', 'account'))


def source_key(record):
    return namespace(record['owner']) + (record['deal'],)


@dataclass(frozen=True)
class Money:
    value: Decimal
    currency: str
    digits: int
    kind: str

    def __post_init__(self):
        d = dec(self.value)
        if not self.currency or d.quantize(quantum(self.digits)) != d:
            raise ValueError('unknown currency or off-precision')


def reconciled_net(record, history, owner, currency='USD', digits=2):
    """Reserve closing-source fixture only, not the general economic ledger.

    Opening fees still belong to actual economic accounting; this helper rejects
    opening entries as harvest sources rather than discarding their ledger value.
    """
    if history is None:
        return 'UNAVAILABLE', None
    if record['owner'] != owner or history.get(source_key(record)) != record:
        return 'REJECT', None
    if record['entry'] != 'CLOSE' or record['event'] == 0:
        return 'REJECT', None
    total = sum((dec(record[k]) for k in ('profit', 'swap', 'commission', 'fee')), Decimal(0))
    if total != dec(record['rawNet']):
        return 'CONFLICT', None
    # Components remain raw and immutable; quantize the total once.
    return 'RECONCILED', Money(total.quantize(quantum(digits), rounding=ROUND_HALF_EVEN), currency, digits, 'ReconciledEconomicNet')


def allocate(actual, shares, role='BigCore'):
    if actual.kind != 'ReconciledEconomicNet':
        raise ValueError('projected cannot create a grant')
    shares = tuple(dec(x) for x in shares)
    if len(shares) != 4 or any(x < 0 or x > 1 for x in shares) or sum(shares) > 1:
        raise ValueError('invalid policy')
    net = max(Decimal(0), actual.value)
    grants = [Decimal(0)] * 5
    if role in ('BigCore', 'BigTrend'):
        grants[:4] = [(net*x).quantize(quantum(actual.digits), rounding=ROUND_FLOOR) for x in shares]
    elif role != 'Small':
        raise ValueError('role not eligible for harvest allocation')
    grants[4] = net - sum(grants[:4])
    return dict(zip(BUCKETS, grants))


def valid_balance(net, grant, remaining, consumed, reserved, unallocated='0', phase='COMMITTED', digits=2):
    maps = (grant, remaining, consumed, reserved)
    if any(set(m) != set(BUCKETS) for m in maps):
        return False
    n, u = dec(net), dec(unallocated)
    all_values = [n, u] + [dec(m[k]) for m in maps for k in BUCKETS]
    if any(v < 0 or v.quantize(quantum(digits)) != v for v in all_values):
        return False
    if phase not in ('PREPARED', 'COMMITTED') or (phase == 'COMMITTED' and u != 0):
        return False
    if sum(grant.values()) + u != n:
        return False
    return all(remaining[k] + consumed[k] == grant[k] and reserved[k] <= remaining[k] for k in BUCKETS)


def authorize(request, state, registry, authority):
    if authority is None or registry is None or not authority['complete'] or not authority['fresh']:
        return 'UNAVAILABLE'
    if state['owner'] != authority['owner'] or request['owner'] != authority['owner']:
        return 'REJECT'
    event = namespace(request['owner']) + (request['event'],)
    # Historical exact replay precedes current balance/revision tests.
    if event in registry:
        return 'NO_OP' if canonical(registry[event]) == canonical(request) else 'CONFLICT'
    if request['event'] == 0 or request['revision'] != authority['revision'] or state['revision'] != authority['revision']:
        return 'REJECT'
    if request['plan'] != authority['plan'] or request['cycle'] != authority['cycle']:
        return 'REJECT'
    if any(request[k] != state[k] for k in ('source', 'allocation', 'allocationEvent', 'policy', 'currency')):
        return 'REJECT'
    if state['phase'] != 'COMMITTED' or request['bucket'] != 'FinalReserve' or request['purpose'] != 'CatchUp':
        return 'REJECT'
    if not valid_balance(state['net'], state['grant'], state['remaining'], state['consumed'], state['reserved']):
        return 'REJECT'
    amount = dec(request['amount'])
    if amount <= 0 or amount.quantize(quantum(2)) != amount:
        return 'REJECT'
    return 'ELIGIBLE_FOR_COMMIT' if amount <= state['remaining']['FinalReserve']-state['reserved']['FinalReserve'] else 'REJECT'


def apply_for_test(request, state, registry, authority):
    import copy
    outcome = authorize(request, state, registry, authority)
    s, j, a = copy.deepcopy(state), copy.deepcopy(registry), copy.deepcopy(authority)
    if outcome == 'ELIGIBLE_FOR_COMMIT':
        amount = dec(request['amount'])
        s['remaining']['FinalReserve'] -= amount
        s['consumed']['FinalReserve'] += amount
        s['revision'] += 1
        a['revision'] = s['revision']
        j[namespace(request['owner'])+(request['event'],)] = copy.deepcopy(request)
        return 'COMMITTED_IN_MEMORY', s, j, a
    return outcome, s, j, a


def verify_proof(proof, record, allocation, history, context):
    status, money = reconciled_net(record, history, context['owner'])
    if status != 'RECONCILED':
        return status
    if allocation['owner'] != context['owner'] or allocation['source'] != source_key(record):
        return 'REJECT'
    if allocation['currency'] != context['currency'] or allocation['revision'] != context['revision'] or record['cycle'] != context['cycle']:
        return 'REJECT'
    if record['symbol'] != context['symbol'] or record['magic'] != context['magic'] or record['role'] not in ('BigCore','BigTrend'):
        return 'REJECT'
    if allocation['remaining']['FinalReserve']-allocation['reserved']['FinalReserve'] <= 0:
        return 'REJECT'
    expected = {k: record[k] for k in ('owner','symbol','magic','deal','event','position','role','direction','cycle','action')}
    expected.update({k:context[k] for k in ('plan','revision','snapshot')})
    if not context['fresh'] or proof['identity'] != expected or dec(proof['net']) != money.value:
        return 'REJECT'
    authoritative_digest = digest({'record':record,'grant':allocation['grant'],'context':context})
    return 'VERIFIED' if proof['digest'] == authoritative_digest else 'REJECT'


def far_loss(current_net, baseline_loss=None, baseline_valid=True):
    absolute = max(Decimal(0), -dec(current_net))
    incremental = None if baseline_loss is None or not baseline_valid else max(Decimal(0), absolute-dec(baseline_loss))
    return absolute, incremental


def baseline_binding(baseline, expected, fresh=True, restored=True):
    keys=('side','volume','cycle','plan','revision','snapshot','costVersion')
    return baseline is not None and fresh and restored and all(k in baseline and baseline[k]==expected[k] for k in keys)


def close_now_net(side, open_price, bid, ask, volume, signed_costs='0'):
    if side not in ('BUY','SELL') or dec(ask) < dec(bid) or dec(volume) <= 0:
        raise ValueError('invalid market/side')
    # Unit-price linear instrument fixture; NOT OrderCalcProfit oracle for brokers.
    close = dec(bid) if side == 'BUY' else dec(ask)
    return (close-dec(open_price)) * dec(volume) * (1 if side=='BUY' else -1) + dec(signed_costs)


def transition(deals, complete, cap):
    if len({d['id'] for d in deals}) != len(deals):
        return 'CONFLICT', None
    if any(not d['confirmed'] for d in deals):
        return 'UNAVAILABLE', None
    loss = max(Decimal(0), -sum((sum((dec(d[k]) for k in ('profit','swap','commission','fee')),Decimal(0)) for d in deals),Decimal(0)))
    return ('SAFE_BLOCKED' if loss > dec(cap) else 'RECONCILED' if complete else 'PENDING'), loss


def buffer_total(items, currency='USD'):
    seen, total = set(), Decimal(0)
    for item in items:
        if item['currency'] != currency or item['policyVersion'] <= 0:
            return 'UNAVAILABLE', None
        key = (item['riskBasis'], item['window'])
        if key in seen:
            return 'CONFLICT', None
        seen.add(key)
        if dec(item['value']) < 0:
            return 'REJECT', None
        if not item['alreadyIncludedInNet']:
            total += dec(item['value'])
    return 'VALID', total


def worst_case(levels, required_ids, variant='A'):
    if len(set(required_ids)) != len(required_ids) or len(levels) != len(required_ids) or {x['id'] for x in levels} != set(required_ids):
        return 'UNAVAILABLE', None, None
    if any(not x['complete'] or not x['fresh'] or not x['sourceProof'] for x in levels):
        return 'UNAVAILABLE', None, None
    if any(dec(x['share'])*dec(x['bnet']) <= dec(x['farVolume']) for x in levels):
        return 'REJECT', None, None
    if len({x['currency'] for x in levels}) != 1:
        return 'UNAVAILABLE', None, None
    if any(dec(x[k])<0 for x in levels for k in ('available','farLoss','buffer')):
        return 'REJECT', None, None
    metrics = [(dec(x['available'])-dec(x['farLoss'])-dec(x['buffer']),x['id']) for x in levels]
    margin, level = min(metrics)
    if variant == 'B':
        selected = max(levels,key=lambda x:(dec(x['transitionLoss']),-x['id']))
        margin,level = next(m for m in metrics if m[1]==selected['id'])
    elif variant != 'A':
        raise ValueError('unapproved variant')
    return ('POSITIVE' if margin>0 else 'REJECT'),level,margin


def core_geometry(far, core_ratio, trend_ratio, small_ratio, vmin, step):
    f,c,t,s,m,g = map(dec,(far,core_ratio,trend_ratio,small_ratio,vmin,step))
    if min(f,c,s,m,g)<=0 or t<0:
        raise ValueError('invalid geometry input')
    core=(f*c/g).to_integral_value(rounding=ROUND_FLOOR)*g
    trend=(f*t/g).to_integral_value(rounding=ROUND_FLOOR)*g
    small=-( -(f*s/g)).to_integral_value(rounding=ROUND_FLOOR)*g
    return dict(core=core,trend=trend,small=small,net=core+trend-small,slope=core+trend-small-f,
                outcome='REJECT' if core<m else 'GEOMETRY_ONLY')
