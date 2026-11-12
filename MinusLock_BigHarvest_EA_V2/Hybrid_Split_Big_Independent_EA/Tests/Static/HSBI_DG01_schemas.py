"""Explicit DG01 artifact schemas; never inferred from test outcome rows."""
import HSBI_DG01_common as a
S={'type':'string'};I={'type':'integer'};B={'type':'boolean'};NULL={'type':'null'}
SHA=dict(type='string',pattern='^[0-9a-f]{64}$');GIT=dict(type='string',pattern='^[0-9a-f]{40}$')
def arr(item):return dict(type='array',items=item)
def obj(properties,required=None):return dict(type='object',properties=properties,required=required if required is not None else list(properties))
ANYOBJ={'type':'object'}
RUN=obj(dict(Command=arr(S),ExitCode=I,Stdout=S,Stderr=S),['Command','ExitCode','Stdout','Stderr'])
REFROW=obj(dict(TestID=S,SubjectSHA256=SHA,RunnerSHA256=SHA,Input=S,Expected=ANYOBJ,Actual=ANYOBJ,Status=dict(enum=['PASS','FAIL','INFRASTRUCTURE_ERROR']),ExitCode=dict(type=['integer','null']),Environment=ANYOBJ,ExecutionTimeUTC=S,ProofBoundary=S))
NATIVEROW=obj(dict(TestID=S,SubjectSHA256=dict(type='object',additionalProperties=SHA),RunnerSHA256=SHA,Input=S,Expected=ANYOBJ,Actual=NULL,Status=dict(const='NOT_RUN'),ExitCode=NULL,Environment=S,ExecutionTimeUTC=NULL,ProofBoundary=S))
DECISION=obj(dict(DecisionID=S,DisplayOrdinal=S,CanonicalIDPreserved=dict(const=True),SourceContract=S,Conflict=S,PreferredSemantics=S,Alternatives=dict(type=['string','array']),MathematicalJustification=S,Counterexample=S,DependentDefects=arr(S),ProductionModules=arr(S),RequiredTests=arr(S),RequiredNativeEvidence=S,MigrationRisk=S,StopConditions=arr(S),ApprovalRequired=dict(const=True),ReadinessStatus=dict(enum=['READY_FOR_ADMIN_DECISION','BLOCKED_BY_DEPENDENCY','INSUFFICIENT_EVIDENCE','CONTRACT_CONFLICT']),ApprovalStatus=dict(const='AWAITING_ADMIN_APPROVAL'),AdministratorDecision=dict(const=''),ShortBallot=S,ImplementationReadiness=dict(const='NO_PRODUCTION_PERMISSION')))
PLAN=obj({k:S for k in ['DefectID','ConfirmedFailure','Classification','RootCause','MinimalChangeCandidate','MigrationRisk','RemainingRisk','ProductionScope','ReadinessStatus']}|dict(CurrentSource=ANYOBJ,RequiredContract=arr(S),DependencyGraph=arr(S),RequiredNativeTests=arr(S),RequiredRegressionTests=arr(S),ApprovalRequired=dict(const=True),CurrentImplementationAllowed=dict(const=False)))
FILE=obj(dict(Path=S,BlobID=dict(type='string',pattern='^[0-9a-f]{40}$'),Mode=dict(enum=['100644','100755']),SHA256=SHA,Size=dict(type='integer',minimum=0),Production=B))
def schemas():
 d={}
 def add(n,s,folder='Tests/Evidence'):d[folder+'/'+a.TAG+n+'.json']=s
 add('BASELINE',obj(dict(BASE_SHA=GIT,UTC=S,Branch=dict(const='work'),RemoteSHA=GIT,WorktreeInitiallyClean=dict(const=True),FilesCount=I,ProductionCount=I)))
 add('PRESERVATION',obj(dict(BASE_SHA=GIT,UTC=S,Files=arr(FILE),Method=S)))
 add('FORMATTING_RESULTS',obj(dict(UTC=S,Rows=arr(obj(dict(Source=S,SourceSHA256=SHA,Output=S,OutputSHA256=SHA,Replacement=S,OutputCharacterOffsets=arr(I),TokenCount=I,ReversibleByteEquivalent=dict(const=True),ProtectedContentUnchanged=dict(const=True)))),ProofBoundary=S)))
 add('AUDIT02_PACKAGE_RECHECK',RUN);add('AUDIT02_INTEGRITY_RECHECK',RUN)
 add('DIFF_CHECK',obj(dict(Command=arr(S),ExitCode=I,Stdout=S,Stderr=S,Applied=dict(const=False),Target=S,BaseSHA256=SHA,CandidateBodySHA256=SHA)))
 add('CODEC_GOLDENS',obj(dict(Fields=arr(arr({})),RecordHex=dict(type='string',pattern='^[0-9a-f]+$'),Scalars=arr(obj(dict(ID=S,Input=S,ExpectedBits=dict(type='string',pattern='^[0-9a-f]{16}$'),ExpectedText=S))),GeneratorSHA256=SHA,ProofBoundary=S)))
 add('TEST_RESULTS',obj(dict(BaseSHA=GIT,StartedUTC=S,FinishedUTC=S,Command=arr(S),RunnerSHA256=SHA,Rows=arr(REFROW),Pass=I,Fail=I,InfrastructureErrors=I,FormattingRows=arr(ANYOBJ),FormattingPass=I,ProofBoundary=S)))
 add('DEVELOPMENT_TEST_RESULTS',d['Tests/Evidence/'+a.TAG+'TEST_RESULTS.json'])
 mutationrow=obj(dict(MutationID=S,TestID=S,OriginalSourceSHA256=SHA,RunnerSHA256=SHA,ExactEdit=obj(dict(Old=S,New=S)),Input=S,Expected=S,Environment=ANYOBJ,ExecutionTimeUTC=S,ProofBoundary=S,Status=dict(enum=['UNSAFE_ACCEPTANCE_KILL','STATUS_CONTRACT_KILL','MUTATION_SURVIVED','INFRASTRUCTURE_ERROR']),ExitCode=dict(type=['integer','null'])))
 add('MUTATION_RESULTS',obj(dict(StartedUTC=S,FinishedUTC=S,Rows=arr(mutationrow),Killed=I,Survived=I,InfrastructureErrors=I)))
 add('DEVELOPMENT_MUTATION_RESULTS',d['Tests/Evidence/'+a.TAG+'MUTATION_RESULTS.json'])
 add('DEVELOPMENT_SOURCES',obj(dict(UTC=S,Files=arr(obj(dict(Path=S,SHA256=SHA,Text=S))),Reason=S)))
 add('SOURCE_REFERENCE_REVIEW',obj(dict(Rows=arr(obj(dict(DefectID=S,File=S,Function=dict(type=['string','null']),HistoricalLine=dict(type=['integer','null']),DefinitionLines=arr(I),SourceSHA256=SHA,ClassificationUnchanged=dict(const=True),LocatorStatus=dict(enum=['MATCH','NO_FUNCTION_SOURCE_REFERENCE','DG01_LOCATOR_CORRECTION_REQUIRED'])))),Boundary=S)))
 add('BASELINE_REVIEW',obj(dict(UTC=S,Defects=arr(ANYOBJ),FormulaCount=dict(const=49),FormulaCounts=obj(dict(ConditionalMathematics=dict(const=23),Conflicts=dict(const=11),Unverified=dict(const=15))),OldIntegrityRecheck=dict(const=0),OldScopeFailure=dict(const=1),Note=S)))
 add('DECISION_MATRIX',obj(dict(BaseSHA=GIT,IDMapping=S,Rows=arr(DECISION))),'Tests/Contracts')
 add('P0_REMEDIATION_MATRIX',obj(dict(Rows=arr(PLAN),CompleteLocalFixNotImplied=dict(const=True))),'Tests/Contracts')
 add('ACCEPTANCE_MATRIX',obj(dict(BaseSHA=GIT,Rows=arr(ANYOBJ),Decisions=dict(const=16),P0Plans=dict(const=10),NativeRequiredIDs=arr(S),OneFileLocalAPIFeasible=dict(const=True),OneFileCompleteRemediationFeasible=dict(const=False),ProductionAllowlistCandidate=arr(S),MandatoryBeforeR1=arr(S),NativeStatus=dict(const='NOT_RUN'),Approved=dict(const=False),ApprovalGate=dict(const='READY_FOR_ADMIN_DECISION'),RuntimeGate=dict(const='PARTIAL_NATIVE_PENDING'))),'Tests/Contracts')
 add('NATIVE_RESULTS',obj(dict(BaseSHA=GIT,UTC=S,MQL5_COMPILE=dict(const='NOT_RUN'),MQL5_NATIVE_TESTS=dict(const='NOT_RUN'),NATIVE_VERIFIED=dict(const=False),PowerShellLauncherExecution=dict(const='NOT_RUN'),Searches=arr(RUN),Rows=arr(NATIVEROW),CaseCount=I,NativePass=dict(const=0),NativeFail=dict(const=0),Scope=S)))
 add('CALLSITE_REVIEW',obj(dict(Rows=arr(obj(dict(File=S,Line=I,Text=S,SHA256=SHA))),Scope=S)))
 add('DEVELOPMENT_LOG',obj(dict(Rows=arr(ANYOBJ))))
 add('EXECUTIONS',obj(dict(Rows=arr(RUN),Boundary=S)))
 add('PACKAGE_RESULTS',obj(dict(UTC=S,PositiveErrors=arr(S),NegativeProbes=arr(obj(dict(ProbeID=S,Status=dict(enum=['PASS','FAIL']),Errors=arr(S)))),Pass=I,Fail=I,RunnerSHA256=SHA,Boundary=S)))
 add('FINAL_INTEGRITY',obj(dict(BaseSHA=GIT,UTC=S,Artifacts=arr(obj(dict(Path=S,SHA256=SHA,Size=I))),IndependentInventoryVersion=dict(const=1),Exclusions=arr(S),Scope=S)))
 add('PUBLICATION_REVIEW',obj(dict(UTC=S,SourceChanges=dict(const=False),HistoricalChanges=dict(const=False),NewFilesCount=I,SecretPatternHits=arr(S),Limits=S)))
 add('JSON_SCHEMAS',obj({'$schema':S,'Version':dict(const=1),'Schemas':ANYOBJ}),'Tests/Contracts')
 return d
if __name__=='__main__':a.save('JSON_SCHEMAS',{'$schema':'https://json-schema.org/draft/2020-12/schema','Version':1,'Schemas':schemas()},'Tests/Contracts')
