"""Lossless adapters: every historical node survives byte-canonically."""
import copy,hashlib,json
def blob(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def sha(v):return hashlib.sha256(blob(v).encode()).hexdigest()
def leaves(v,path='INPUT'):
    if isinstance(v,dict):
        for k,x in v.items():yield from leaves(x,f'{path}.{k}')
    elif isinstance(v,list):
        for n,x in enumerate(v):yield from leaves(x,f'{path}[{n}]')
    else:yield path,v
def adapt(version,vector):
    if not isinstance(vector,dict) or 'INPUT' not in vector:return {'adapterResult':'UNMAPPED','reason':'INPUT_MISSING'}
    raw=copy.deepcopy(vector['INPUT']);loss=[{'sourcePath':p,'sourceValueSHA256':sha(v),'targetPath':'rawHistoricalInput'+p[5:],'targetValueSHA256':sha(v),'transformation':'IDENTITY_CANONICAL_COPY','lossClassification':'NONE','normativeJustification':'R7_LOSSLESS_ADAPTER'} for p,v in leaves(raw)]
    return {'adapterResult':'ADAPTED','sourceVersion':version,'sourceVectorId':vector.get('VECTOR_ID'),'sourceInputSHA256':sha(raw),'canonicalInput':{'schemaVersion':1,'sourceVersion':version,'sourceVectorId':vector.get('VECTOR_ID'),'rawHistoricalInput':raw,'rawInputDigest':sha(raw)},'lossMap':loss,'silentlyDroppedFields':0,'silentlyDroppedElements':0,'selfHealedDefects':0,'unjustifiedDefaults':0}
