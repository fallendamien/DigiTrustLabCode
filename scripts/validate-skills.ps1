<#
.SYNOPSIS
  Validates SKILL.md frontmatter across project and/or global skill directories.

.DESCRIPTION
  Scans every SKILL.md file under the configured skill directories and verifies:
    1. File is named exactly SKILL.md (uppercase) - flags lowercase skill.md.
    2. File starts with YAML frontmatter (--- on line 1).
    3. Frontmatter contains a name: field.
    4. The name: value matches the parent directory name (kebab-case).
    5. The name: value is kebab-case (lowercase letters, digits, hyphens only).

  Exits 0 if all skills pass, 1 if any violation is found.
  Intended as a pre-commit guard or manual check after creating/editing skills.

  This is the GLOBAL copy (agent-templates/scripts/validate-skills.ps1), callable
  from any project or from the template root itself. If -SkillRoots is not given,
  it auto-detects:
    - If run from inside a project (cwd has .devin/skills and/or .windsurf/skills),
      those are scanned.
    - Otherwise, falls back to the global skills library at
      agent-templates/workspace/skills (this script's own directory tree).

.PARAMETER SkillRoots
  Array of skill directory roots to scan. Auto-detected if omitted (see above).

.PARAMETER Strict
  Treat warnings (e.g. lowercase skill.md) as errors. Off by default.

.EXAMPLE
  powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate-skills.ps1
  # Run from a project root: scans .devin/skills + .windsurf/skills

.EXAMPLE
  powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codeium\windsurf\agent-templates\scripts\validate-skills.ps1"
  # Run from anywhere with no project skill dirs: scans the global skills library
#>

[CmdletBinding()]
param(
    [string[]]$SkillRoots,
    [switch]$Strict
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

if (-not $SkillRoots) {
    $cwd = (Get-Location).Path
    $projectRoots = @(@('.devin/skills', '.windsurf/skills') | Where-Object {
        Test-Path -LiteralPath (Join-Path $cwd $_) -PathType Container
    })
    if ($projectRoots.Count -gt 0) {
        $SkillRoots = $projectRoots
    } else {
        $globalSkillsRoot = Join-Path (Split-Path -Parent $PSScriptRoot) 'workspace\skills'
        $SkillRoots = @($globalSkillsRoot)
        Write-Host "No project skill dirs found in $cwd - falling back to global skills library: $globalSkillsRoot" -ForegroundColor DarkCyan
    }
}

$repoRoot = (Get-Location).Path
$violations = [System.Collections.Generic.List[pscustomobject]]::new()
$warnings  = [System.Collections.Generic.List[pscustomobject]]::new()
$passed    = [System.Collections.Generic.List[pscustomobject]]::new()

function Test-KebabCase {
    param([string]$Value)
    return $Value -match '^[a-z0-9]+(-[a-z0-9]+)*$'
}

function Get-Frontmatter {
    param([string]$FilePath)
    # Returns a hashtable of frontmatter keys, or $null if no frontmatter.
    $lines = Get-Content -LiteralPath $FilePath -ErrorAction Stop
    if ($lines.Count -eq 0 -or $lines[0].TrimEnd() -ne '---') {
        return $null
    }
    $fm = @{}
    for ($i = 1; $i -lt $lines.Count; $i++) {
        $line = $lines[$i].TrimEnd()
        if ($line -eq '---') { return $fm }
        if ($line -match '^(?<key>[A-Za-z_][A-Za-z0-9_-]*):\s*(?<value>.*)$') {
            $key = $matches['key']
            $value = $matches['value'].Trim('"').Trim("'")
            $fm[$key] = $value
        }
    }
    return $fm
}

foreach ($root in $SkillRoots) {
    $absRoot = if ([System.IO.Path]::IsPathRooted($root)) { $root } else { Join-Path $repoRoot $root }
    if (-not (Test-Path -LiteralPath $absRoot -PathType Container)) {
        Write-Host "? Skipping $root - directory not found" -ForegroundColor DarkYellow
        continue
    }

    $skillDirs = Get-ChildItem -LiteralPath $absRoot -Directory -ErrorAction SilentlyContinue

    foreach ($dir in $skillDirs) {
        $dirName = $dir.Name
        # Skip obvious non-skill dirs (templates, examples, bundled resources)
        if ($dirName -in @('templates', 'examples', 'references', 'assets', 'scripts')) {
            continue
        }

        $skillMd      = Join-Path $dir.FullName 'SKILL.md'
        $skillMdLower = Join-Path $dir.FullName 'skill.md'

        $fileToCheck   = $null
        $filenameLabel = $null
        $isLowercase   = $false

        if (Test-Path -LiteralPath $skillMd) {
            $fileToCheck   = $skillMd
            $filenameLabel = 'SKILL.md'
        }
        elseif (Test-Path -LiteralPath $skillMdLower) {
            $fileToCheck   = $skillMdLower
            $filenameLabel = 'skill.md'
            $isLowercase   = $true
        }
        else {
            $violations.Add([pscustomobject]@{
                Dir      = $dirName
                File     = '(missing)'
                Issue    = 'No SKILL.md file found in skill directory'
                Severity = 'ERROR'
            })
            continue
        }

        $fm = Get-Frontmatter -FilePath $fileToCheck

        if ($null -eq $fm) {
            $violations.Add([pscustomobject]@{
                Dir      = $dirName
                File     = $filenameLabel
                Issue    = 'Missing YAML frontmatter (file must start with ---)'
                Severity = 'ERROR'
            })
            if ($isLowercase) {
                $warnings.Add([pscustomobject]@{
                    Dir      = $dirName
                    File     = $filenameLabel
                    Issue    = 'Filename is lowercase skill.md - rename to SKILL.md'
                    Severity = 'WARN'
                })
            }
            continue
        }

        if (-not $fm.ContainsKey('name')) {
            $violations.Add([pscustomobject]@{
                Dir      = $dirName
                File     = $filenameLabel
                Issue    = 'Missing name: field in frontmatter'
                Severity = 'ERROR'
            })
            if ($isLowercase) {
                $warnings.Add([pscustomobject]@{
                    Dir      = $dirName
                    File     = $filenameLabel
                    Issue    = 'Filename is lowercase skill.md - rename to SKILL.md'
                    Severity = 'WARN'
                })
            }
            continue
        }

        $nameVal = $fm['name']

        if ($nameVal -ne $dirName) {
            $violations.Add([pscustomobject]@{
                Dir      = $dirName
                File     = $filenameLabel
                Issue    = "name:$nameVal does not match directory $dirName"
                Severity = 'ERROR'
            })
        } elseif (-not (Test-KebabCase $nameVal)) {
            $violations.Add([pscustomobject]@{
                Dir      = $dirName
                File     = $filenameLabel
                Issue    = "name:$nameVal is not kebab-case (lowercase letters, digits, hyphens)"
                Severity = 'ERROR'
            })
        } else {
            $passed.Add([pscustomobject]@{
                Dir  = $dirName
                File = $filenameLabel
                Name = $nameVal
            })
        }

        if ($isLowercase) {
            $warnings.Add([pscustomobject]@{
                Dir      = $dirName
                File     = $filenameLabel
                Issue    = 'Filename is lowercase skill.md - rename to SKILL.md'
                Severity = 'WARN'
            })
        }
    }
}

# -- Output --

$totalScanned = $passed.Count + $violations.Count + $warnings.Count

Write-Host ""
Write-Host "===== Skill Frontmatter Validator =====" -ForegroundColor Cyan
Write-Host "Scanned $totalScanned skill(s) across $($SkillRoots.Count) root(s): $($SkillRoots -join ', ')"
Write-Host ""

if ($passed.Count -gt 0) {
    Write-Host "OK Passed ($($passed.Count))" -ForegroundColor Green
    $passed | Format-Table Dir, File, Name -AutoSize
}

if ($warnings.Count -gt 0) {
    Write-Host "WARN Warnings ($($warnings.Count))" -ForegroundColor Yellow
    $warnings | Format-Table Dir, File, Issue -AutoSize
}

if ($violations.Count -gt 0) {
    Write-Host "FAIL Violations ($($violations.Count))" -ForegroundColor Red
    $violations | Format-Table Dir, File, Issue, Severity -AutoSize
}

# -- Summary --

$hasFailures = ($violations.Count -gt 0) -or ($Strict -and $warnings.Count -gt 0)
$summaryColor = if ($hasFailures) { 'Red' } else { 'Green' }
$summaryIcon  = if ($hasFailures) { 'FAIL' } else { 'OK' }

Write-Host ""
Write-Host "$summaryIcon Summary: $($passed.Count) passed, $($warnings.Count) warnings, $($violations.Count) violations" -ForegroundColor $summaryColor

if ($violations.Count -gt 0) { exit 1 }
if ($Strict -and $warnings.Count -gt 0) { exit 1 }
exit 0
