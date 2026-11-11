#ifndef HSBI_R0H_TEST_CODEC_MQH
#define HSBI_R0H_TEST_CODEC_MQH
// TEST-ONLY candidate. NOT COMPILED/EXECUTED without MetaEditor evidence.
// No production includes, terminal account lookup, broker, file or network APIs.
enum R0H_Status { R0H_NEW=0,R0H_NO_OP=1,R0H_CONFLICT=2,R0H_REJECT=3,R0H_UNAVAILABLE=4 };
struct R0H_Value { int kind; string s; ulong u; long i; double d; bool b; };
struct R0H_Record { R0H_Value f[29]; };
string R0H_Name(const int i){string n[29]={"SchemaVersion","Broker","Server","AccountLogin","Symbol","Magic","CycleID","DealTicket","OrderTicket","PositionIdentifier","ActionID","EventID","Role","EntryType","DealType","TimestampMsc","Volume","Price","Profit","Swap","Commission","Fee","DealNet","Currency","Precision","SourcePlanApplicable","SourcePlan","SourcePolicyApplicable","SourcePolicyVersion"};return n[i];}
void R0H_U(R0H_Value &v,const ulong u){v.kind=117;v.u=u;}
void R0H_S(R0H_Value &v,const string s){v.kind=115;v.s=s;}
void R0H_D(R0H_Value &v,const double d){v.kind=100;v.d=d;}
void R0H_B(R0H_Value &v,const bool b){v.kind=98;v.b=b;}
bool R0H_UTF8(const string s,uchar &bytes[]){ArrayResize(bytes,0);int n=StringToCharArray(s,bytes,0,-1,CP_UTF8);if(n<=1)return false;ArrayResize(bytes,n-1);for(int j=0;j<n-1;j++)if(bytes[j]==0)return false;return CharArrayToString(bytes,0,n-1,CP_UTF8)==s;}
bool R0H_Positive(const R0H_Value &v){return v.kind==117&&v.u>0;}
R0H_Status R0H_Validate(const R0H_Record &r){
 if(!R0H_Positive(r.f[0]))return R0H_REJECT;
 if(r.f[0].u!=1)return R0H_UNAVAILABLE;
 for(int k=0;k<29;k++){
  if(k==1||k==2||k==4||k==12||k==13||k==14||k==23){uchar raw[];if(r.f[k].kind!=115||!R0H_UTF8(r.f[k].s,raw))return R0H_REJECT;if(ArraySize(raw)>4096)return R0H_UNAVAILABLE;}
  else if(k>=16&&k<=22){if(r.f[k].kind!=100||!MathIsValidNumber(r.f[k].d))return R0H_REJECT;if((k==16||k==17)&&r.f[k].d<=0)return R0H_REJECT;}
  else if(k==25||k==27){if(r.f[k].kind!=98)return R0H_REJECT;}
  else if(k==26||k==28){bool applicable=r.f[k-1].b;if(applicable&&!R0H_Positive(r.f[k]))return r.f[k].kind==110?R0H_UNAVAILABLE:R0H_REJECT;if(!applicable&&r.f[k].kind!=110)return R0H_REJECT;}
  else if(k==24){if(r.f[k].kind!=117)return R0H_REJECT;if(r.f[k].u>8)return R0H_UNAVAILABLE;}
  else if(k==5){if(!((r.f[k].kind==117&&r.f[k].u>0&&r.f[k].u<=9223372036854775807)||(r.f[k].kind==105&&r.f[k].i<0)))return R0H_REJECT;}
  else {if(!R0H_Positive(r.f[k]))return R0H_REJECT;if((k==3||k==15)&&r.f[k].u>9223372036854775807)return R0H_REJECT;}
 }
 if(r.f[12].s!="BigCore"&&r.f[12].s!="BigTrend"&&r.f[12].s!="Small"&&r.f[12].s!="Far"&&r.f[12].s!="Initial")return R0H_REJECT;
 if(r.f[13].s!="IN"&&r.f[13].s!="OUT"&&r.f[13].s!="INOUT"&&r.f[13].s!="OUT_BY")return R0H_REJECT;
 if(r.f[14].s!="BUY"&&r.f[14].s!="SELL")return R0H_REJECT;
 return R0H_NO_OP;
}
bool R0H_SameValue(const R0H_Value &a,const R0H_Value &b){if(a.kind!=b.kind)return false;if(a.kind==115)return a.s==b.s;if(a.kind==117)return a.u==b.u;if(a.kind==105)return a.i==b.i;if(a.kind==100)return a.d==b.d;if(a.kind==98)return a.b==b.b;return a.kind==110;}
bool R0H_Key(const R0H_Record &a,const R0H_Record &b){return R0H_SameValue(a.f[1],b.f[1])&&R0H_SameValue(a.f[2],b.f[2])&&R0H_SameValue(a.f[3],b.f[3])&&R0H_SameValue(a.f[7],b.f[7]);}
bool R0H_Equal(const R0H_Record &a,const R0H_Record &b){for(int k=0;k<29;k++)if(!R0H_SameValue(a.f[k],b.f[k]))return false;return true;}
R0H_Status R0H_Classify(const R0H_Record &incoming,const bool authorityComplete,const R0H_Record &authority,const bool registryComplete,const R0H_Record &records[],const string codec){
 R0H_Status s=R0H_Validate(incoming);if(s!=R0H_NO_OP)return s;
 if(codec!="HSBI-F64Z-1"&&codec!="HSBI-T17Z-1")return R0H_UNAVAILABLE;
 if(!authorityComplete||!registryComplete)return R0H_UNAVAILABLE;
 s=R0H_Validate(authority);if(s!=R0H_NO_OP)return s;
 if(!R0H_Key(incoming,authority))return R0H_UNAVAILABLE;
 if(!R0H_Equal(incoming,authority))return R0H_CONFLICT;
 int found=-1;
 for(int j=0;j<ArraySize(records);j++){
  s=R0H_Validate(records[j]);if(s!=R0H_NO_OP)return s;
  for(int k=0;k<j;k++)if(R0H_Key(records[j],records[k]))return R0H_CONFLICT;
  if(R0H_Key(incoming,records[j]))found=j;
 }
 if(found<0)return R0H_NEW;
 return R0H_Equal(incoming,records[found])?R0H_NO_OP:R0H_CONFLICT;
}
bool R0H_Bits(const double x,ulong &out){
 if(!MathIsValidNumber(x))return false;
 if(x==0){out=0;return true;}
 ulong sign=x<0?((ulong)1<<63):0;double n=MathAbs(x);int e=0;
 while(n>=2){n/=2;e++;if(e>1023)return false;}
 while(n<1){n*=2;e--;if(e< -1074)return false;}
 if(e< -1022){for(int j=0;j<e+1074;j++)n*=2;out=sign|(ulong)n;return true;}
 ulong m=0;n-=1;
 for(int j=0;j<52;j++){n*=2;ulong bit=n>=1?1:0;n-=(double)bit;m=(m<<1)|bit;}
 if(n!=0)return false;
 out=sign|((ulong)(e+1023)<<52)|m;return true;
}
bool R0H_Unbits(const ulong u,double &out){
 ulong e=(u>>52)&2047;ulong m=u&4503599627370495;
 if(e==2047)return false;
 if(e==0&&m==0){if((u>>63)!=0)return false;out=0;return true;}
 double n=(double)(e==0?m:((ulong)4503599627370496+m));int power=e==0?-1074:(int)e-1075;
 while(power>0){n*=2;power--;}while(power<0){n/=2;power++;}
 if((u>>63)!=0)n=-n;
 if(!MathIsValidNumber(n))return false;out=n;return true;
}
bool R0H_Push(uchar &b[],const uchar value){int n=ArraySize(b);if(n>=65536)return false;if(ArrayResize(b,n+1)!=n+1)return false;b[n]=value;return true;}
bool R0H_BE(uchar &b[],const ulong value,const int size){for(int j=size-1;j>=0;j--)if(!R0H_Push(b,(uchar)((value>>(8*j))&255)))return false;return true;}
bool R0H_Token(const R0H_Value &v,uchar &b[]){
 if(!R0H_Push(b,(uchar)v.kind))return false;
 if(v.kind==110)return true;
 if(v.kind==98)return R0H_Push(b,(uchar)(v.b?49:48));
 if(v.kind==115){uchar raw[];if(!R0H_UTF8(v.s,raw)||ArraySize(raw)>4096||!R0H_BE(b,(ulong)ArraySize(raw),4))return false;for(int j=0;j<ArraySize(raw);j++)if(!R0H_Push(b,raw[j]))return false;return true;}
 if(v.kind==117)return R0H_BE(b,v.u,8);
 if(v.kind==105)return v.i<0&&R0H_BE(b,(ulong)v.i,8);
 if(v.kind==100){ulong bits;if(!R0H_Bits(v.d,bits))return false;return R0H_BE(b,bits,8);}
 return false;
}
R0H_Status R0H_Encode(const R0H_Record &r,const string codec,uchar &output[]){
 if(codec!="HSBI-F64Z-1")return R0H_UNAVAILABLE;
 R0H_Status s=R0H_Validate(r);if(s!=R0H_NO_OP)return s;
 uchar b[],head[];if(!R0H_UTF8("HSBI-F64Z-1",head))return R0H_REJECT;
 for(int j=0;j<ArraySize(head);j++)if(!R0H_Push(b,head[j]))return R0H_UNAVAILABLE;
 if(!R0H_Push(b,0))return R0H_UNAVAILABLE;
 for(int k=0;k<29;k++){R0H_Value name;R0H_S(name,R0H_Name(k));if(!R0H_Token(name,b)||!R0H_Token(r.f[k],b))return R0H_UNAVAILABLE;}
 if(!ArraySwap(output,b))return R0H_UNAVAILABLE;return R0H_NO_OP;
}
bool R0H_ReadBE(const uchar &b[],int &at,const int size,ulong &value){if(size>ArraySize(b)-at||at<0)return false;value=0;for(int j=0;j<size;j++)value=(value<<8)|b[at++];return true;}
R0H_Status R0H_ReadToken(const uchar &b[],int &at,R0H_Value &v){
 if(at<0||at>=ArraySize(b))return R0H_REJECT;v.kind=(int)b[at++];ulong u;
 if(v.kind==110)return R0H_NO_OP;
 if(v.kind==98){if(at>=ArraySize(b)||(b[at]!=48&&b[at]!=49))return R0H_REJECT;v.b=b[at++]==49;return R0H_NO_OP;}
 if(v.kind==115){if(!R0H_ReadBE(b,at,4,u))return R0H_REJECT;if(u>4096)return R0H_UNAVAILABLE;if(u==0||u>(ulong)(ArraySize(b)-at))return R0H_REJECT;int n=(int)u;v.s=CharArrayToString(b,at,n,CP_UTF8);uchar check[];if(!R0H_UTF8(v.s,check)||ArraySize(check)!=n)return R0H_REJECT;for(int j=0;j<n;j++)if(check[j]!=b[at+j])return R0H_REJECT;at+=n;return R0H_NO_OP;}
 if(!R0H_ReadBE(b,at,8,u))return R0H_REJECT;
 if(v.kind==117){v.u=u;return R0H_NO_OP;}
 if(v.kind==105){v.i=(long)u;return v.i<0?R0H_NO_OP:R0H_REJECT;}
 if(v.kind==100)return R0H_Unbits(u,v.d)?R0H_NO_OP:R0H_REJECT;
 return R0H_REJECT;
}
R0H_Status R0H_Decode(const uchar &b[],const string codec,R0H_Record &output){
 if(codec!="HSBI-F64Z-1")return R0H_UNAVAILABLE;
 if(ArraySize(b)>65536)return R0H_UNAVAILABLE;
 uchar head[];if(!R0H_UTF8("HSBI-F64Z-1",head))return R0H_REJECT;
 int n=ArraySize(head);if(ArraySize(b)<n+1)return R0H_REJECT;
 for(int j=0;j<n;j++)if(b[j]!=head[j])return R0H_REJECT;
 if(b[n]!=0)return R0H_REJECT;int at=n+1;R0H_Record temp;
 for(int k=0;k<29;k++){R0H_Value name;R0H_Status s=R0H_ReadToken(b,at,name);if(s!=R0H_NO_OP)return s;if(name.kind!=115||name.s!=R0H_Name(k))return R0H_REJECT;s=R0H_ReadToken(b,at,temp.f[k]);if(s!=R0H_NO_OP)return s;}
 if(at!=ArraySize(b))return R0H_REJECT;R0H_Status s=R0H_Validate(temp);if(s!=R0H_NO_OP)return s;output=temp;return R0H_NO_OP;
}
R0H_Status R0H_LegacyFacade(const string diagnostic){return R0H_UNAVAILABLE;}
#endif
