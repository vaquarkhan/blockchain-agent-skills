param(
    [string]$Target = (Get-Location).Path,
    [string]$ToolMode = "auto"
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Bootstrapping Blockchain Agent Skills"
Write-Host "Target: $Target"
Write-Host "Tool mode: $ToolMode"

python (Join-Path $RepoRoot "scripts/install_toolkit.py") --tool $ToolMode --target $Target
Write-Host "Bootstrap complete."
