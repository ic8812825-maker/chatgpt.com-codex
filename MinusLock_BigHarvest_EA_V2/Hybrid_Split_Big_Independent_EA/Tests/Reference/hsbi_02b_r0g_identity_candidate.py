"""R0G proposed identity gate, pure TEST-ONLY. Frozen R0F codec dependency.
Fixture authority/completeness do not establish broker or durable authenticity.
No balances, broker operations, persistence, approval, or migration writes.
"""
import hsbi_02b_r0f_contract_candidate as frozen
FIELDS=frozen.FIELDS
CODECS={'HSBI-T17Z-1':'A','HSBI-F64Z-1':'B'}

def classify(incoming,authority,registry,codec='HSBI-F64Z-1'):
 """Versioned R0G status API, including independently supplied lookup evidence.
 registry: Complete exact bool; Records list of full immutable records.
 authority: Complete exact bool; Record full29 body or None (unknown).
 Missing independent evidence =>UNAVAILABLE, malformed DTO=>REJECT.
 NEW only confirmed exact source, complete absence registry. No credits.
 """
 try:
  frozen.record_shape(incoming)
  if type(codec) is not str:raise frozen.Invalid('codec type')
  if codec not in CODECS:return 'UNAVAILABLE'
  if authority is None or registry is None:return 'UNAVAILABLE'
  frozen.require(type(authority) is dict and set(authority)=={'Complete','Record'})
  frozen.require(type(registry) is dict and set(registry)=={'Complete','Records'})
  frozen.require(type(authority['Complete']) is bool and type(registry['Complete']) is bool and type(registry['Records']) is list)
  if not authority['Complete'] or not registry['Complete'] or authority['Record'] is None:return 'UNAVAILABLE'
  frozen.record_shape(authority['Record'])
  # Canonical comparison is exact body comparison, not claimed digest authority.
  def body(r):return frozen.encode_record(r,'B')
  expected=authority['Record'];key=frozen.source_key(incoming)
  if frozen.source_key(expected)!=key:return 'UNAVAILABLE'
  if body(incoming)!=body(expected):return 'CONFLICT'
  indexed={}
  for row in registry['Records']:
   if row is None:return 'UNAVAILABLE' # unreconciled legacy entry: no fabricated absence
   frozen.record_shape(row);k=frozen.source_key(row)
   if k in indexed:return 'CONFLICT' # even identical duplicate inventory needs reconciliation
   indexed[k]=row
  if key not in indexed:return 'NEW'
  return 'NO_OP' if body(indexed[key])==body(incoming) else 'CONFLICT'
 except frozen.Invalid:return 'REJECT'
 except frozen.Unavailable:return 'UNAVAILABLE'
