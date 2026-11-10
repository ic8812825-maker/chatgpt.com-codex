"""Independent literal fixtures and struct-based codec oracle. No subject imports."""
import struct,math
# Fixed contract field order, independently transcribed from proposed schema.
ORDER=('SchemaVersion','Broker','Server','AccountLogin','Symbol','Magic','CycleID','DealTicket','OrderTicket','PositionIdentifier','ActionID','EventID','Role','EntryType','DealType','TimestampMsc','Volume','Price','Profit','Swap','Commission','Fee','DealNet','Currency','Precision','SourcePlanApplicable','SourcePlan','SourcePolicyApplicable','SourcePolicyVersion')
GOLDENS=[('zero',0.0,'0.0000000000000000e+000','0000000000000000'),('negative-zero',-0.0,'0.0000000000000000e+000','0000000000000000'),('one',1.0,'1.0000000000000000e+000','3ff0000000000000'),('negative-five',-5.0,'-5.0000000000000000e+000','c014000000000000'),('one-tenth',0.1,'1.0000000000000001e-001','3fb999999999999a'),('min-normal',float.fromhex('0x1p-1022'),'2.2250738585072014e-308','0010000000000000'),('min-subnormal',float.fromhex('0x1p-1074'),'4.9406564584124654e-324','0000000000000001'),('max-finite',float.fromhex('0x1.fffffffffffffp1023'),'1.7976931348623157e+308','7fefffffffffffff')]
def record():return dict(SchemaVersion=1,Broker='B1',Server='S1',AccountLogin=1,Symbol='EURUSD',Magic=7,CycleID=1,DealTicket=11,OrderTicket=12,PositionIdentifier=13,ActionID=1,EventID=31,Role='BigCore',EntryType='OUT',DealType='SELL',TimestampMsc=100000,Volume=1.0,Price=1.25,Profit=60.0,Swap=-2.0,Commission=-7.0,Fee=-1.0,DealNet=50.0,Currency='USD',Precision=2,SourcePlanApplicable=True,SourcePlan=1,SourcePolicyApplicable=True,SourcePolicyVersion=1)
def authority():return dict(Record=record(),Currency='USD',Precision=2,PostedComponents=dict(Profit=6000,Swap=-200,Commission=-700,Fee=-100),PostedNet=5000,PolicyVerified=True)
def token_binary(value):
 if value is None:return b'n'
 if type(value) is bool:return b'b'+(b'1' if value else b'0')
 if type(value) is str:
  raw=value.encode('utf-8');return b's'+struct.pack('>I',len(raw))+raw
 if type(value) is int:return b'i'+struct.pack('>q',value) if value<0 else b'u'+struct.pack('>Q',value)
 if type(value) is float:return b'd'+struct.pack('>d',0.0 if value==0 else value)
 raise ValueError('fixture type')
def binary_record(r):return b'HSBI-F64Z-1\x00'+b''.join(token_binary(k)+token_binary(r[k]) for k in ORDER)
def decode_token(raw,offset=0):
 t=raw[offset:offset+1];offset+=1
 if t==b'n':return None,offset
 if t==b'b':return raw[offset:offset+1]==b'1',offset+1
 if t==b's':n=struct.unpack('>I',raw[offset:offset+4])[0];offset+=4;return raw[offset:offset+n].decode('utf-8'),offset+n
 if t in (b'u',b'i',b'd'):return struct.unpack({b'u':'>Q',b'i':'>q',b'd':'>d'}[t],raw[offset:offset+8])[0],offset+8
 raise ValueError('fixture decoder type')
def decoded_binary(raw):
 assert raw.startswith(b'HSBI-F64Z-1\x00');at=len(b'HSBI-F64Z-1\x00');r={}
 for expected in ORDER:
  name,at=decode_token(raw,at);assert name==expected;value,at=decode_token(raw,at);r[name]=value
 assert at==len(raw);return r
TEXT_LITERAL={0.0:'0.0000000000000000e+000',1.0:'1.0000000000000000e+000',1.25:'1.2500000000000000e+000',60.0:'6.0000000000000000e+001',-2.0:'-2.0000000000000000e+000',-7.0:'-7.0000000000000000e+000',-1.0:'-1.0000000000000000e+000',50.0:'5.0000000000000000e+001'}
def token_text(value):
 if value is None:return b'n0:'
 if type(value) is bool:return b'b'+(b'1' if value else b'0')
 tag=b's' if type(value) is str else b'i' if type(value) is int else b'd';raw=(value if type(value) is str else str(value) if type(value) is int else TEXT_LITERAL[value]).encode('utf-8')
 return tag+str(len(raw)).encode()+b':'+raw

def text_record(r):return b'HSBI-T17Z-1\n'+b''.join(token_text(k)+token_text(r[k]) for k in ORDER)
def decoded_text(raw):
 assert raw.startswith(b'HSBI-T17Z-1\n');at=len(b'HSBI-T17Z-1\n');r={}
 def get(at):
  tag=raw[at:at+1];at+=1
  if tag==b'b':return raw[at:at+1]==b'1',at+1
  end=raw.index(b':',at);n=int(raw[at:end]);at=end+1;v=raw[at:at+n];at+=n
  if tag==b'n':assert n==0;return None,at
  return v.decode('utf-8') if tag==b's' else int(v) if tag==b'i' else float(v),at
 for name in ORDER:
  actual,at=get(at);assert actual==name;value,at=get(at);r[name]=value
 assert at==len(raw);return r
