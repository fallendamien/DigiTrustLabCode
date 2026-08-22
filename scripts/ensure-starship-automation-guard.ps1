[CmdletBinding()]
param(
    [string]$ProfilePath = $PROFILE
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$resolvedProfilePath = [System.IO.Path]::GetFullPath($ProfilePath)
$profileDirectory = Split-Path -Parent $resolvedProfilePath

if (-not (Test-Path -LiteralPath $profileDirectory)) {
    New-Item -ItemType Directory -Path $profileDirectory -Force | Out-Null
}

if (-not (Test-Path -LiteralPath $resolvedProfilePath)) {
    Write-Output "[INFO] PowerShell profile does not exist: $resolvedProfilePath"
    Write-Output "[INFO] No Starship change was needed."
    exit 0
}

$profileText = [System.IO.File]::ReadAllText($resolvedProfilePath)
$guardPattern = '(?ms)if\s*\(\s*\$env:TERM\s*-ne\s*["'']dumb["'']\s*\)\s*\{\s*Invoke-Expression\s*\(&starship\s+init\s+powershell\)\s*\}'

if ([System.Text.RegularExpressions.Regex]::IsMatch($profileText, $guardPattern)) {
    Write-Output "[OK] Starship TERM guard already exists: $resolvedProfilePath"
    exit 0
}

$oldBlockPattern = '(?m)^[ \t]*# Load Starship for ALL terminals including Cascade\r?\n[ \t]*Invoke-Expression\s*\(&starship\s+init\s+powershell\)\s*$'
$initPattern = '(?m)^[ \t]*Invoke-Expression\s*\(&starship\s+init\s+powershell\)\s*$'
$match = [System.Text.RegularExpressions.Regex]::Match($profileText, $oldBlockPattern)

if (-not $match.Success) {
    $match = [System.Text.RegularExpressions.Regex]::Match($profileText, $initPattern)
}

if (-not $match.Success) {
    Write-Output "[INFO] No unguarded Starship initialization was found: $resolvedProfilePath"
    Write-Output "[INFO] No file was changed."
    exit 0
}

$guardedBlock = @'
# Load Starship only in interactive terminals. Automation shells such as Codex
# advertise TERM=dumb, where Starship cannot render a prompt cleanly.
if ($env:TERM -ne "dumb") {
    Invoke-Expression (&starship init powershell)
}
'@
$guardedBlock = $guardedBlock.Trim("`r", "`n") -replace "`r?`n", [Environment]::NewLine
$updatedProfileText = $profileText.Remove($match.Index, $match.Length).Insert($match.Index, $guardedBlock)
$backupPath = "$resolvedProfilePath.bak-starship-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

Copy-Item -LiteralPath $resolvedProfilePath -Destination $backupPath -Force
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
[System.IO.File]::WriteAllText($resolvedProfilePath, $updatedProfileText, $utf8NoBom)

Write-Output "[OK] Added the TERM=dumb guard: $resolvedProfilePath"
Write-Output "[OK] Backup: $backupPath"
