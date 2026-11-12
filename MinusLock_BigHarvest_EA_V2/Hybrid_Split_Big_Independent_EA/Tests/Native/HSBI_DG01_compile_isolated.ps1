# Compile only. NEVER launches terminal64.exe, attaches an EA, passes a login or enables trading.
[CmdletBinding()]
param(
 [Parameter(Mandatory=$true)][string]$MetaEditorPath,
 [Parameter(Mandatory=$true)][string]$TerminalPath,
 [Parameter(Mandatory=$true)][string]$DataPath,
 [string]$OutputRoot=(Join-Path ([IO.Path]::GetTempPath()) ('HSBI_DG01_'+[guid]::NewGuid().ToString('N')))
)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
$report=[ordered]@{SchemaVersion=1;StartedUTC=[DateTime]::UtcNow.ToString('o');CompileStatus='NOT_RUN';NativeRuntimeStatus='NOT_RUN';NativeVerified=$false;TradingLaunched=$false;SourceHashes=@();CompilerExitCode=$null;CompilerLog=$null;Errors=@()}
$root=$null;$created=$false;$exitCode=2
function Assert-PlainPath([string]$Path) {
 $item=Get-Item -LiteralPath $Path -Force
 $parent=$item
 while($null -ne $parent){if(($parent.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0){throw "Reparse ancestor rejected: $($parent.FullName)"};$parent=if($parent -is [IO.DirectoryInfo]){$parent.Parent}else{$parent.Directory}}
 if(($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0){throw "Reparse point rejected: $Path"}
}
function Source-Inventory([string]$Project) {
 $items=@(Get-ChildItem -LiteralPath (Join-Path $Project 'Include') -File -Recurse)
 $items+=Get-Item -LiteralPath (Join-Path $Project 'Hybrid_Split_Big_Independent_EA.mq5')
 $items+=@(Get-ChildItem -LiteralPath (Join-Path $Project 'Tests/Native') -File -Filter 'HSBI_DG01_*')
 $items+=Get-Item -LiteralPath (Join-Path $Project 'Tests/Reference/HSBI_DG01_identity_candidate.mqh')
 $items+=Get-Item -LiteralPath (Join-Path $Project 'Tests/Reference/hsbi_02b_r0h_native_codec.mqh')
 return @($items | Sort-Object FullName -Unique | ForEach-Object {Assert-PlainPath $_.FullName;[ordered]@{Path=$_.FullName.Substring($Project.Length).TrimStart([char[]]'\/');SHA256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}})
}
try {
 foreach($p in @($MetaEditorPath,$TerminalPath,$DataPath)){if(-not (Test-Path -LiteralPath $p)){throw "Missing required path: $p"};Assert-PlainPath $p}
 foreach($exe in @($MetaEditorPath,$TerminalPath)){if(-not (Test-Path -LiteralPath $exe -PathType Leaf)){throw 'Selected executable must be a file'}}
 if([IO.Path]::GetFileName($MetaEditorPath) -notmatch '^metaeditor(64)?\.exe$'){throw 'Selected compiler is not MetaEditor'}
 if([IO.Path]::GetFileName($TerminalPath) -notmatch '^terminal(64)?\.exe$'){throw 'Selected terminal path is invalid'}
 if(-not (Test-Path -LiteralPath (Join-Path $DataPath 'MQL5') -PathType Container)){throw 'Selected data folder has no MQL5 directory'}
 # DataPath is validated but never copied or used as terminal state; account/config files are never read.
 $project=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../..')).TrimEnd([char[]]'\/')
 $root=[IO.Path]::GetFullPath($OutputRoot).TrimEnd([char[]]'\/')
 foreach($forbidden in @($project,[IO.Path]::GetFullPath($DataPath),[IO.Path]::GetDirectoryName([IO.Path]::GetFullPath($TerminalPath)))) {
  $f=$forbidden.TrimEnd([char[]]'\/');if($root.Equals($f,[StringComparison]::OrdinalIgnoreCase) -or $root.StartsWith($f+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'OutputRoot must be outside source, selected terminal and data folders'}
 }
 Assert-PlainPath ([IO.Path]::GetDirectoryName($root))
 if(Test-Path -LiteralPath $root){throw 'OutputRoot must be a new unique directory; refusing overwrite'}
 New-Item -Path $root -ItemType Directory | Out-Null
 $created=$true
 foreach($dir in Get-ChildItem -LiteralPath (Join-Path $project 'Include') -Directory -Recurse){Assert-PlainPath $dir.FullName}
 $before=Source-Inventory $project;$report.SourceHashes=$before
 $stage=Join-Path $root 'project';New-Item -Path (Join-Path $stage 'Tests/Native') -ItemType Directory -Force | Out-Null
 New-Item -Path (Join-Path $stage 'Tests/Reference') -ItemType Directory | Out-Null
 Copy-Item -LiteralPath (Join-Path $project 'Include') -Destination $stage -Recurse
 Get-ChildItem -LiteralPath (Join-Path $project 'Tests/Native') -File -Filter 'HSBI_DG01_*.mq*' | Copy-Item -Destination (Join-Path $stage 'Tests/Native')
 foreach($name in @('HSBI_DG01_identity_candidate.mqh','hsbi_02b_r0h_native_codec.mqh')){Copy-Item -LiteralPath (Join-Path $project "Tests/Reference/$name") -Destination (Join-Path $stage 'Tests/Reference')}
 $harness=Join-Path $stage 'Tests/Native/HSBI_DG01_harness.mq5';$log=Join-Path $root 'HSBI_DG01_compiler.log'
 $report.CompilerVersion=(Get-Item -LiteralPath $MetaEditorPath).VersionInfo.FileVersion
 $report.CompilerSHA256=(Get-FileHash -LiteralPath $MetaEditorPath -Algorithm SHA256).Hash.ToLowerInvariant()
 $report.SelectedTerminal=$TerminalPath;$report.SelectedDataPath=$DataPath;$report.CompilerLog=$log
 $compilerArgs=@('/compile:"'+$harness+'"','/log:"'+$log+'"')
 $report.Command=@($MetaEditorPath)+$compilerArgs
 $proc=Start-Process -FilePath $MetaEditorPath -ArgumentList $compilerArgs -PassThru
 if(-not $proc.WaitForExit(120000)){$proc.Kill();throw 'MetaEditor compile timeout; native runtime NOT_RUN'}
 $report.CompilerExitCode=$proc.ExitCode
 if(-not (Test-Path -LiteralPath $log -PathType Leaf)){throw 'No compiler log: exit code alone is not compilation proof'}
 $text=Get-Content -LiteralPath $log -Raw
 $report.CompilerLogSHA256=(Get-FileHash -LiteralPath $log -Algorithm SHA256).Hash.ToLowerInvariant()
 $report.Diagnostics=$text
 $binary=[IO.Path]::ChangeExtension($harness,'.ex5')
 if($text -match '\b0 errors?,\s*\d+ warnings?' -and (Test-Path -LiteralPath $binary) -and $proc.ExitCode -eq 0){$report.CompileStatus='COMPILED_ONLY';$report.BinarySHA256=(Get-FileHash -LiteralPath $binary -Algorithm SHA256).Hash.ToLowerInvariant();$exitCode=0}
 else {$report.CompileStatus='COMPILE_FAILED_OR_UNRECOGNIZED_DIAGNOSTICS';$exitCode=1}
 $after=Source-Inventory $project
 if(($before|ConvertTo-Json -Depth 5 -Compress) -ne ($after|ConvertTo-Json -Depth 5 -Compress)){throw 'Source preservation mismatch'}
 $report.SourceFilesUnchanged=$true
} catch {$report.Errors+= $_.Exception.Message;$report.CompileStatus='INFRASTRUCTURE_ERROR';$exitCode=2}
finally {
 $report.FinishedUTC=[DateTime]::UtcNow.ToString('o')
 if($created -and $null -ne $root -and (Test-Path -LiteralPath $root -PathType Container)){[IO.File]::WriteAllText((Join-Path $root 'HSBI_DG01_compile_report.json'),($report|ConvertTo-Json -Depth 15),[Text.UTF8Encoding]::new($false))}
 $report|ConvertTo-Json -Depth 15|Write-Output
}
exit $exitCode
