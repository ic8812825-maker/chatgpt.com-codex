"""Independent wire fixture builder: literal field order + struct.pack, no subject encoder."""
import struct,json
import HSBI_DG01_common as a
FIELDS=[('SchemaVersion',1),('Broker','B1'),('Server','S1'),('AccountLogin',1),('Symbol','EURUSD'),('Magic',7),('CycleID',1),('DealTicket',11),('OrderTicket',12),('PositionIdentifier',13),('ActionID',1),('EventID',31),('Role','BigCore'),('EntryType','OUT'),('DealType','SELL'),('TimestampMsc',100000),('Volume',1.0),('Price',1.25),('Profit',60.0),('Swap',-2.0),('Commission',-7.0),('Fee',-1.0),('DealNet',50.0),('Currency','USD'),('Precision',2),('SourcePlanApplicable',True),('SourcePlan',1),('SourcePolicyApplicable',True),('SourcePolicyVersion',1)]
SCALARS=[('zero',0.0,'0000000000000000','0.0000000000000000e+000'),('negative-zero',-0.0,'0000000000000000','0.0000000000000000e+000'),('one',1.0,'3ff0000000000000','1.0000000000000000e+000'),('negative-five',-5.0,'c014000000000000','-5.0000000000000000e+000'),('tenth',0.1,'3fb999999999999a','1.0000000000000001e-001'),('min-normal',2.2250738585072014e-308,'0010000000000000','2.2250738585072014e-308'),('min-subnormal',4.9406564584124654e-324,'0000000000000001','4.9406564584124654e-324'),('max-finite',1.7976931348623157e308,'7fefffffffffffff','1.7976931348623157e+308')]
def token(v):
 if type(v) is str:b=v.encode('utf8');return b's'+len(b).to_bytes(4,'big')+b
 if type(v) is bool:return b'b'+(b'1' if v else b'0')
 if type(v) is int:return (b'u'+v.to_bytes(8,'big')) if v>=0 else b'i'+v.to_bytes(8,'big',signed=True)
 if type(v) is float:return b'd'+struct.pack('>d',0.0 if v==0 else v)
 raise TypeError(type(v))
def main():
 wire=b'HSBI-F64Z-1\0'+b''.join(token(k)+token(v) for k,v in FIELDS)
 assert all(struct.pack('>d',0.0 if n==0 else n).hex()==bits for _,n,bits,_ in SCALARS)
 text='// Independent literals, not native-subject encoder output.\nstring DGGoldenRecordHex="'+wire.hex()+'";\n'
 text+='string DGGoldenBits[8]={'+','.join(json.dumps(x[2]) for x in SCALARS)+'};\n'
 text+='string DGGoldenText[8]={'+','.join(json.dumps(x[3]) for x in SCALARS)+'};\n'
 (a.ROOT/'Tests/Native/HSBI_DG01_goldens.mqh').write_text(text)
 a.save('CODEC_GOLDENS',dict(Fields=FIELDS,RecordHex=wire.hex(),Scalars=[dict(ID=i,Input=repr(n),ExpectedBits=b,ExpectedText=t) for i,n,b,t in SCALARS],GeneratorSHA256=a.sha(__file__),ProofBoundary='Independent struct/integer field framing fixture. Native and T17 formatter have NOT_RUN status; struct.pack agreement is reference evidence only.'))
if __name__=='__main__':main()
