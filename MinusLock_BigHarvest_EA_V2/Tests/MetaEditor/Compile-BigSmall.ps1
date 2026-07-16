param([Parameter(Mandatory=$true)][string]$MetaEditor,
      [Parameter(Mandatory=$true)][string]$ProjectRoot)
$ErrorActionPreference='Stop'
$targets=@(
 'MinusLock_BigHarvest_EA.mq5',
 'Tests\MQL5\CleanStartPersistenceTest.mq5',
 'Tests\MQL5\BigSmallEvaluatorTest.mq5',
 'Tests\MQL5\BigSmallStateMachineTest.mq5'
)
$logDir=Join-Path $ProjectRoot 'Tests\MetaEditor\logs'
New-Item -ItemType Directory -Force $logDir | Out-Null
$failed=$false
foreach($target in $targets) {
 $source=Join-Path $ProjectRoot $target
 $log=Join-Path $logDir (($target -replace '[\\/.]','_')+'.log')
 & $MetaEditor "/compile:$source" "/log:$log"
 $text=Get-Content $log -Raw
 if($LASTEXITCODE -ne 0 -or $text -notmatch '0 errors, 0 warnings') { $failed=$true }
}
if($failed){ throw 'MetaEditor compile failed; inspect Tests/MetaEditor/logs.' }
Write-Host 'METAEDITOR_COMPILE=PASS (0 errors, 0 warnings)'
