"""Strict JSON boundary for the entire mandatory C2 evidence graph. No last-wins parsing."""
import json,math
COUNTERS={'Scenarios','SchemaProbes','Executions','Comparisons','Pass','Fail','InfrastructureErrors','ExitCode','CatalogSize','Killed','RedundantSurvivors','UnexplainedSurvivors','ContextID','PassCount','FailCount','ExpectedBaselineExit','ExpectedPass','ExpectedFail','NegativePassed','NegativeFailed'}
def pairs(items):
 out={}
 for k,v in items:
  if k in out:raise ValueError('duplicate JSON key: '+k)  # GUARD:C2-JSON-DUPLICATE
  out[k]=v
 return out
def constant(value):raise ValueError('invalid JSON constant: '+value)
def integer(value):
 if type(value) is not int:raise ValueError('counter must be exact integer')  # GUARD:C2-JSON-COUNTER
 return value
def validate(value):
 if type(value) is dict:
  for k,v in value.items():
   if k in COUNTERS and v is not None:integer(v)
   validate(v)
 elif type(value) is list:
  for v in value:validate(v)
 elif type(value) is float and not math.isfinite(value):raise ValueError('nonfinite JSON number')
def loads(text):
 result=json.loads(text,object_pairs_hook=pairs,parse_constant=constant)
 validate(result);return result
