Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

New-Item -ItemType Directory -Force '.\projects' | Out-Null

$repos = @(
    @{ Url = 'https://github.com/langchain-ai/langgraph.git'; Target = '.\projects\langgraph' },
    @{ Url = 'https://github.com/crewAIInc/crewAI-examples.git'; Target = '.\projects\crewai-examples' },
    @{ Url = 'https://github.com/langchain-ai/deepagents.git'; Target = '.\projects\deepagents' }
)

foreach ($repo in $repos) {
    if (Test-Path $repo.Target) {
        Write-Host "Skip existing: $($repo.Target)"
        continue
    }

    Write-Host "Cloning $($repo.Url) -> $($repo.Target)"
    git clone --depth 1 $repo.Url $repo.Target
}

Write-Host 'Reference repositories are ready under projects/'