#property strict
#property script_show_inputs
// ISOLATED TEST SCRIPT. No trading/account/file/network operations.
// Native compile and execution NOT_RUN until real MetaEditor/MT5 logs supplied.
#include "hsbi_02b_r0h_native_codec.mqh"
#include "hsbi_02b_r0h_native_goldens.mqh"
int passed=0,failed=0;
void Check(const string id,const bool ok){if(ok)passed++;else failed++;Print("R0H_ASSERT ",id," ",ok?"PASS":"FAIL");}
int Nibble(const ushort c){if(c>=48&&c<=57)return (int)c-48;if(c>=97&&c<=102)return (int)c-87;return -1;}
bool Unhex(const string s,uchar &b[]){if(StringLen(s)%2!=0)return false;ArrayResize(b,StringLen(s)/2);for(int j=0;j<ArraySize(b);j++){int a=Nibble(StringGetCharacter(s,2*j)),v=Nibble(StringGetCharacter(s,2*j+1));if(a<0||v<0)return false;b[j]=(uchar)(16*a+v);}return true;}
string Hex(const uchar &b[]){string out="";for(int j=0;j<ArraySize(b);j++)out+=StringFormat("%02x",(uint)b[j]);return out;}
ulong HexU64(const string s){ulong out=0;for(int j=0;j<StringLen(s);j++)out=(out<<4)|(ulong)Nibble(StringGetCharacter(s,j));return out;}
void Fixture(R0H_Record &r){
 for(int j=0;j<29;j++)R0H_U(r.f[j],1);
 R0H_S(r.f[1],"B1");R0H_S(r.f[2],"S1");R0H_S(r.f[4],"EURUSD");R0H_U(r.f[5],7);R0H_U(r.f[7],11);R0H_U(r.f[8],12);R0H_U(r.f[9],13);R0H_U(r.f[11],31);
 R0H_S(r.f[12],"BigCore");R0H_S(r.f[13],"OUT");R0H_S(r.f[14],"SELL");R0H_U(r.f[15],100000);
 R0H_D(r.f[16],1);R0H_D(r.f[17],1.25);R0H_D(r.f[18],60);R0H_D(r.f[19],-2);R0H_D(r.f[20],-7);R0H_D(r.f[21],-1);R0H_D(r.f[22],50);R0H_S(r.f[23],"USD");R0H_U(r.f[24],2);R0H_B(r.f[25],true);R0H_B(r.f[27],true);
}
string T17Probe(double x){if(x==0)x=0.0;string s=DoubleToString(x,-16);int e=StringFind(s,"e");if(e<0)e=StringFind(s,"E");if(e<0)return "UNSUPPORTED_FORMAT";string significand=StringSubstr(s,0,e);int power=(int)StringToInteger(StringSubstr(s,e+1));return significand+"e"+(power<0?"-":"+")+StringFormat("%03d",(int)MathAbs(power));}
void Scalar(const string id,const double x,const string expectedBits,const string expectedText){ulong u=0;Check(id+"-bits",R0H_Bits(x,u)&&u==HexU64(expectedBits));double round=1;Check(id+"-roundtrip",R0H_Unbits(u,round)&&round==x);Check(id+"-text-probe",T17Probe(x)==expectedText);}
void OnStart(){
 R0H_Record r;Fixture(r);Check("fixture",R0H_Validate(r)==R0H_NO_OP);
 uchar encoded[];Check("encode-status",R0H_Encode(r,"HSBI-F64Z-1",encoded)==R0H_NO_OP);Check("independent-golden",Hex(encoded)==R0H_GoldenRecordHex);
 R0H_Record output;Fixture(output);Check("decode-roundtrip",R0H_Decode(encoded,"HSBI-F64Z-1",output)==R0H_NO_OP&&R0H_Equal(r,output));
 R0H_Record registry[];ArrayResize(registry,1);registry[0]=r;
 Check("exact",R0H_Classify(r,true,r,true,registry,"HSBI-F64Z-1")==R0H_NO_OP);
 Check("unknown-history",R0H_Classify(r,false,r,true,registry,"HSBI-F64Z-1")==R0H_UNAVAILABLE);
 Check("unknown-registry",R0H_Classify(r,true,r,false,registry,"HSBI-F64Z-1")==R0H_UNAVAILABLE);
 Check("unknown-codec",R0H_Classify(r,true,r,true,registry,"future")==R0H_UNAVAILABLE);
 for(int k=0;k<29;k++){
  R0H_Record m=r;
  if(k==1)R0H_S(m.f[k],"B2");else if(k==2)R0H_S(m.f[k],"S2");else if(k==4)R0H_S(m.f[k],"GBPUSD");else if(k==12)R0H_S(m.f[k],"Small");else if(k==13)R0H_S(m.f[k],"IN");else if(k==14)R0H_S(m.f[k],"BUY");else if(k==23)R0H_S(m.f[k],"EUR");else if(k==25||k==27){m.f[k].b=false;m.f[k+1].kind=110;}else if(k>=16&&k<=22)m.f[k].d+=1;else m.f[k].u++;
  Check("altered-"+R0H_Name(k),!R0H_Equal(r,m));
  R0H_Status expect=(k==0?R0H_UNAVAILABLE:(k==1||k==2||k==3||k==7?R0H_NEW:R0H_CONFLICT));
  Check("classify-"+R0H_Name(k),R0H_Classify(m,true,m,true,registry,"HSBI-F64Z-1")==expect);
 }
 R0H_Record a=r,b=r;R0H_D(a.f[18],50);R0H_D(a.f[19],0);R0H_D(a.f[20],0);R0H_D(a.f[21],0);b=a;R0H_D(b.f[18],60);R0H_D(b.f[20],-10);registry[0]=a;
 Check("same-net-components",R0H_Classify(b,true,b,true,registry,"HSBI-F64Z-1")==R0H_CONFLICT);
 R0H_Record empty[];Check("new-observation-not-funding",R0H_Classify(r,true,r,true,empty,"HSBI-F64Z-1")==R0H_NEW);
 long low=(-9223372036854775807-1),high=9223372036854775807;ulong top=18446744073709551615;
 Check("long-limits",low<0&&high>0);Check("ulong-max",top>9223372036854775807);
 R0H_Value v;v.kind=105;v.i=low;uchar raw[];Check("long-min-token",R0H_Token(v,raw)&&Hex(raw)=="698000000000000000");ArrayResize(raw,0);R0H_U(v,top);Check("ulong-max-token",R0H_Token(v,raw)&&Hex(raw)=="75ffffffffffffffff");
 ArrayResize(raw,0);R0H_U(v,9007199254740993);Check("id-not-double",R0H_Token(v,raw)&&Hex(raw)=="750020000000000001");
 ArrayResize(raw,0);R0H_S(v,"Б");Check("utf8-byte-length",R0H_Token(v,raw)&&Hex(raw)=="7300000002d091");
 Scalar("zero",0.0,R0H_GoldenBits0,R0H_GoldenText0);Scalar("negative-zero",-0.0,R0H_GoldenBits1,R0H_GoldenText1);Scalar("one",1.0,R0H_GoldenBits2,R0H_GoldenText2);Scalar("negative-five",-5.0,R0H_GoldenBits3,R0H_GoldenText3);Scalar("tenth",0.1,R0H_GoldenBits4,R0H_GoldenText4);
 // Inputs independently specified as compiler decimal literals; compare bits and text.
 Scalar("min-normal",2.2250738585072014e-308,R0H_GoldenBits5,R0H_GoldenText5);Scalar("min-subnormal",4.9406564584124654e-324,R0H_GoldenBits6,R0H_GoldenText6);Scalar("max-finite",1.7976931348623157e308,R0H_GoldenBits7,R0H_GoldenText7);
 double negzero=1;Check("negative-zero-wire-reject",!R0H_Unbits(HexU64("8000000000000000"),negzero));Check("infinity-wire-reject",!R0H_Unbits(HexU64("7ff0000000000000"),negzero));Check("nan-wire-reject",!R0H_Unbits(HexU64("7ff8000000000000"),negzero));
 // Each rejection must preserve previously valid record output.
 uchar bad[];ArrayResize(bad,ArraySize(encoded));ArrayCopy(bad,encoded);ArrayResize(bad,ArraySize(bad)-1);output=r;Check("truncated",R0H_Decode(bad,"HSBI-F64Z-1",output)==R0H_REJECT&&R0H_Equal(output,r));
 ArrayResize(bad,ArraySize(encoded));ArrayCopy(bad,encoded);R0H_Push(bad,0);output=r;Check("trailing",R0H_Decode(bad,"HSBI-F64Z-1",output)==R0H_REJECT&&R0H_Equal(output,r));
 ArrayResize(bad,ArraySize(encoded));ArrayCopy(bad,encoded);bad[12]=255;output=r;Check("unknown-tag",R0H_Decode(bad,"HSBI-F64Z-1",output)==R0H_REJECT&&R0H_Equal(output,r));
 ArrayResize(bad,ArraySize(encoded));ArrayCopy(bad,encoded);bad[13]=255;bad[14]=255;bad[15]=255;bad[16]=255;output=r;Check("oversized-length",R0H_Decode(bad,"HSBI-F64Z-1",output)==R0H_UNAVAILABLE&&R0H_Equal(output,r));
 ArrayResize(bad,ArraySize(encoded));ArrayCopy(bad,encoded);bad[38]=2;output=r;Check("unknown-schema",R0H_Decode(bad,"HSBI-F64Z-1",output)==R0H_UNAVAILABLE&&R0H_Equal(output,r));
 output=r;Check("unknown-codec-decode",R0H_Decode(encoded,"future",output)==R0H_UNAVAILABLE&&R0H_Equal(output,r));
 R0H_Record invalid=r;R0H_B(invalid.f[18],true);Check("wrong-wire-field-kind",R0H_Validate(invalid)==R0H_REJECT);
 Check("legacy-no-new",R0H_LegacyFacade("EURUSD|7|1|11|50")==R0H_UNAVAILABLE);
 // Same-size Symbol/Broker name substitution demonstrates a duplicate-field rejection.
 ArrayResize(bad,ArraySize(encoded));ArrayCopy(bad,encoded);for(int j=0;j<ArraySize(bad)-6;j++){if(bad[j]==83&&bad[j+1]==121&&bad[j+2]==109&&bad[j+3]==98&&bad[j+4]==111&&bad[j+5]==108){bad[j]=66;bad[j+1]=114;bad[j+2]=111;bad[j+3]=107;bad[j+4]=101;bad[j+5]=114;break;}}
 output=r;Check("duplicate-field",R0H_Decode(bad,"HSBI-F64Z-1",output)==R0H_REJECT&&R0H_Equal(output,r));
 ArrayResize(bad,ArraySize(encoded));ArrayCopy(bad,encoded);for(int j=0;j<ArraySize(bad)-6;j++){if(bad[j]==83&&bad[j+1]==121&&bad[j+2]==109&&bad[j+3]==98&&bad[j+4]==111&&bad[j+5]==108){bad[j]=70;bad[j+1]=117;bad[j+2]=116;bad[j+3]=117;bad[j+4]=114;bad[j+5]=101;break;}}
 output=r;Check("unknown-field",R0H_Decode(bad,"HSBI-F64Z-1",output)==R0H_REJECT&&R0H_Equal(output,r));
 Print("[R0H_NATIVE_RESULT] PASS=",passed," FAIL=",failed," COMPLETE=",failed==0?"YES":"NO");
 // Harness print marker is not OS exit code. Controller must capture terminal/test logs,
 // missing marker/crash => infrastructure error, any FAIL => NATIVE_CODEC_FAIL.
}
