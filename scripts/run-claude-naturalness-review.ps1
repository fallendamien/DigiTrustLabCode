[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$PromptPath,

    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$OutputPath
)

$ErrorActionPreference = 'Stop'

function Stop-FailClosed {
    param([string]$Message)
    [Console]::Error.WriteLine("CLAUDE_REVIEW_FAIL_CLOSED: $Message")
    exit 2
}

$claude = Get-Command claude -ErrorAction SilentlyContinue
if (-not $claude) {
    Stop-FailClosed 'Claude Code CLI is not installed or is not on PATH.'
}

if (-not (Test-Path -LiteralPath $PromptPath -PathType Leaf)) {
    Stop-FailClosed "Review prompt does not exist: $PromptPath"
}

$help = (& $claude.Source --help 2>&1 | Out-String)
$requiredFlags = @(
    '--safe-mode',
    '--model',
    '--effort',
    '--no-chrome',
    '--no-session-persistence',
    '--tools',
    '--output-format',
    '--json-schema'
)
$missingFlags = @($requiredFlags | Where-Object { $help -notmatch [regex]::Escape($_) })
if ($missingFlags.Count -gt 0) {
    Stop-FailClosed ("Installed Claude CLI does not support the required strict flags: " + ($missingFlags -join ', '))
}

$authRaw = (& $claude.Source auth status 2>&1 | Out-String).Trim()
$authExitCode = $LASTEXITCODE
if ($authExitCode -ne 0 -or [string]::IsNullOrWhiteSpace($authRaw)) {
    Stop-FailClosed 'Claude Code CLI authentication status is unavailable or the CLI is not logged in.'
}
try {
    $auth = $authRaw | ConvertFrom-Json
} catch {
    Stop-FailClosed 'Claude Code CLI authentication status was not valid JSON.'
}
if ($auth.loggedIn -ne $true) {
    Stop-FailClosed 'Claude Code CLI is not authenticated.'
}
$authProvider = [string]$auth.apiProvider
$acceptedRuntimeProviders = @('firstParty', 'anthropic')
if ($authProvider -notin $acceptedRuntimeProviders) {
    Stop-FailClosed "Claude Code CLI authentication provider is not an accepted Anthropic-family provider: $authProvider"
}

# The model's structured payload may call the family `anthropic`, while the
# Claude Code runtime truthfully reports its first-party transport as
# `firstParty`. Runtime metadata below is authoritative; the payload provider
# is still constrained to Anthropic-family values so an OpenAI claim fails.
$schema = '{"type":"object","required":["provider","model","status","document_review","segments"],"properties":{"provider":{"enum":["anthropic","firstParty"]},"model":{"type":"string","minLength":1,"pattern":"sonnet"},"status":{"enum":["pass","fail"]},"document_review":{"type":"object"},"segments":{"type":"array"}},"additionalProperties":true}'
$prompt = Get-Content -LiteralPath $PromptPath -Raw

# Keep this argument list explicit. It is the no-history, no-browser, toolless
# terminal contract; do not replace a missing flag with a weaker equivalent.
$cliArgs = @(
    '--print',
    '--safe-mode',
    '--model', 'sonnet',
    '--effort', 'high',
    '--no-chrome',
    '--no-session-persistence',
    '--tools', '',
    '--output-format', 'json',
    '--json-schema', $schema,
    $prompt
)

$raw = (& $claude.Source @cliArgs 2>&1 | Out-String).Trim()
$exitCode = $LASTEXITCODE
if ($exitCode -ne 0) {
    Stop-FailClosed "Claude CLI exited with code $exitCode. Authentication, model availability, or provider evidence is unverified."
}
if ([string]::IsNullOrWhiteSpace($raw)) {
    Stop-FailClosed 'Claude CLI returned no structured output.'
}

try {
    $envelope = $raw | ConvertFrom-Json
} catch {
    Stop-FailClosed 'Claude CLI output was not valid JSON.'
}

if ($envelope.is_error -eq $true -or $envelope.subtype -eq 'error') {
    Stop-FailClosed 'Claude CLI reported an error result.'
}

$sonnetRuntimeEntries = @()
if ($null -ne $envelope.modelUsage) {
    foreach ($property in $envelope.modelUsage.PSObject.Properties) {
        $entry = $property.Value
        $canonicalModel = [string]$entry.canonicalModel
        $runtimeProvider = [string]$entry.provider
        if ($canonicalModel -match '(?i)sonnet') {
            $sonnetRuntimeEntries += [pscustomobject]@{
                model = $canonicalModel
                provider = $runtimeProvider
            }
        }
    }
}
if ($sonnetRuntimeEntries.Count -eq 0) {
    Stop-FailClosed 'Claude CLI output did not contain canonical Sonnet modelUsage evidence.'
}
$runtimeEvidence = @($sonnetRuntimeEntries | Where-Object { $_.provider -in $acceptedRuntimeProviders })
if ($runtimeEvidence.Count -eq 0) {
    Stop-FailClosed 'Claude CLI modelUsage did not prove an accepted Anthropic-family provider for Sonnet.'
}
$runtimeModel = [string]$runtimeEvidence[0].model
$runtimeProvider = [string]$runtimeEvidence[0].provider
if ($runtimeProvider -ne $authProvider) {
    Stop-FailClosed "Claude CLI auth provider ($authProvider) disagrees with modelUsage provider ($runtimeProvider)."
}

$payload = $envelope.structured_output
if ($null -eq $payload) {
    $payload = $envelope
}

$structuredProvider = [string]$payload.provider
$structuredModel = [string]$payload.model
if ($structuredProvider -notin $acceptedRuntimeProviders) {
    Stop-FailClosed 'Structured output did not identify an Anthropic-family provider.'
}
if ([string]::IsNullOrWhiteSpace($structuredModel) -or $structuredModel -notmatch '(?i)sonnet' -or $structuredModel -eq 'sonnet') {
    Stop-FailClosed 'Structured output did not identify a canonical Claude Sonnet model.'
}
if ($null -eq $payload.document_review -or $null -eq $payload.segments) {
    Stop-FailClosed 'Structured output did not contain the required naturalness review payload.'
}

$outputParent = Split-Path -Parent $OutputPath
if (-not (Test-Path -LiteralPath $outputParent -PathType Container)) {
    Stop-FailClosed "Output directory does not exist: $outputParent"
}

$payload | Add-Member -Force -MemberType NoteProperty -Name model_family -Value 'anthropic'
$payload | Add-Member -Force -MemberType NoteProperty -Name provider -Value $runtimeProvider
$payload | Add-Member -Force -MemberType NoteProperty -Name model -Value $runtimeModel
$payload | Add-Member -Force -MemberType NoteProperty -Name runtime_provider -Value $runtimeProvider
$payload | Add-Member -Force -MemberType NoteProperty -Name runtime_model -Value $runtimeModel
$payload | Add-Member -Force -MemberType NoteProperty -Name auth_provider -Value $authProvider
$payload | Add-Member -Force -MemberType NoteProperty -Name structured_provider -Value $structuredProvider
$payload | Add-Member -Force -MemberType NoteProperty -Name structured_model -Value $structuredModel
$payload | Add-Member -Force -MemberType NoteProperty -Name transport -Value 'claude-code-cli'
$payload | Add-Member -Force -MemberType NoteProperty -Name session_persistence -Value $false
$payload | Add-Member -Force -MemberType NoteProperty -Name tools -Value @()
$payload | ConvertTo-Json -Depth 100 | Set-Content -LiteralPath $OutputPath -Encoding utf8NoBOM
Write-Output ("PASS Claude CLI review: provider=$runtimeProvider model=$runtimeModel status=" + [string]$payload.status)
