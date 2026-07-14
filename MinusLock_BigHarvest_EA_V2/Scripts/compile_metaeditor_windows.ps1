param(
  [string]$MetaEditor = "C:\\Program Files\\MetaTrader 5\\metaeditor64.exe",
  [string]$ProjectRoot = (Resolve-Path "$PSScriptRoot\\..").Path,
  [string]$LogPath = (Join-Path (Resolve-Path "$PSScriptRoot\\..").Path "Logs\\metaeditor_compile_split_big.log")
)

$mq5 = Join-Path $ProjectRoot "MinusLock_BigHarvest_EA.mq5"
$logs = Split-Path $LogPath -Parent
if (!(Test-Path $logs)) { New-Item -ItemType Directory -Path $logs | Out-Null }
if (!(Test-Path $MetaEditor)) { throw "MetaEditor not found: $MetaEditor" }
if (!(Test-Path $mq5)) { throw "Main mq5 not found: $mq5" }

& $MetaEditor /compile:"$mq5" /log:"$LogPath"
$code = $LASTEXITCODE
Write-Host "MetaEditor exit code: $code"
Write-Host "Compile log: $LogPath"
if (Test-Path $LogPath) { Get-Content $LogPath | Select-Object -Last 80 }
exit $code
