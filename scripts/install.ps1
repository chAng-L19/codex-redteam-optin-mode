param(
  [string]$CodexHome = "$env:USERPROFILE\.codex",
  [string]$AgentsHome = "$env:USERPROFILE\.agents"
)

$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot

function Backup-IfExists($Path) {
  if (Test-Path -LiteralPath $Path) {
    $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
    Copy-Item -LiteralPath $Path -Destination ($Path + '.bak.' + $stamp) -Recurse -Force
  }
}

New-Item -ItemType Directory -Force -Path "$CodexHome\hooks" | Out-Null
New-Item -ItemType Directory -Force -Path "$AgentsHome\skills\red-team-command-doctrine" | Out-Null

Backup-IfExists "$CodexHome\AGENTS.md"
Backup-IfExists "$CodexHome\hooks.json"
Backup-IfExists "$CodexHome\hooks\session-start-context.py"
Backup-IfExists "$CodexHome\hooks\hook-security-context-hook.py"
Backup-IfExists "$AgentsHome\skills\red-team-command-doctrine\SKILL.md"

Copy-Item "$RepoRoot\.codex\AGENTS.md" "$CodexHome\AGENTS.md" -Force
Copy-Item "$RepoRoot\.codex\hooks\session-start-context.py" "$CodexHome\hooks\session-start-context.py" -Force
Copy-Item "$RepoRoot\.codex\hooks\hook-security-context-hook.py" "$CodexHome\hooks\hook-security-context-hook.py" -Force
Copy-Item "$RepoRoot\.agents\skills\red-team-command-doctrine\SKILL.md" "$AgentsHome\skills\red-team-command-doctrine\SKILL.md" -Force
Copy-Item "$RepoRoot\.agents\skills\red-team-command-doctrine\references" "$AgentsHome\skills\red-team-command-doctrine\references" -Recurse -Force

$template = Get-Content "$RepoRoot\templates\hooks.json.template" -Raw -Encoding UTF8
$rendered = $template.Replace('{{CODEX_HOME_WIN}}', $CodexHome.Replace('\\', '\\\\'))
Set-Content -LiteralPath "$CodexHome\hooks.json" -Value $rendered -Encoding UTF8

Write-Host 'Installed opt-in red-team mode files.' -ForegroundColor Green
Write-Host "Codex home: $CodexHome"
Write-Host "Agents home: $AgentsHome"
Write-Host 'Remember to merge templates\config.toml.example into your real config.toml if needed.' -ForegroundColor Yellow
