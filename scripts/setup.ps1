Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

Write-Host '[1/5] Checking virtual environment...'
if (-not (Test-Path '.\.venv\Scripts\python.exe')) {
    Write-Host 'Creating .venv...'
    python -m venv .venv
}

$pythonExe = '.\.venv\Scripts\python.exe'

Write-Host '[2/5] Preparing stable pip directories...'
New-Item -ItemType Directory -Force '.pip-tmp', '.pip-cache' | Out-Null
$env:TMP = (Resolve-Path '.\.pip-tmp').Path
$env:TEMP = (Resolve-Path '.\.pip-tmp').Path
$env:PIP_CACHE_DIR = (Resolve-Path '.\.pip-cache').Path

Write-Host '[3/5] Upgrading pip tooling...'
& $pythonExe -m pip install --upgrade pip setuptools wheel --disable-pip-version-check

Write-Host '[4/5] Installing requirements...'
& $pythonExe -m pip install -r '.\exercises\requirements.txt' --retries 10 --timeout 120 --disable-pip-version-check

Write-Host '[5/5] Preparing environment file...'
if (-not (Test-Path '.\exercises\.env') -and (Test-Path '.\exercises\.env.example')) {
    Copy-Item '.\exercises\.env.example' '.\exercises\.env'
    Write-Host 'Created exercises/.env from exercises/.env.example'
}

Write-Host ''
Write-Host 'Setup complete.'
Write-Host 'Next steps:'
Write-Host '1. Fill in exercises/.env with your API keys'
Write-Host '2. Select .venv\Scripts\python.exe in VS Code'
Write-Host '3. Run .\.venv\Scripts\python.exe exercises\01-langchain-basics\01_hello_agent.py'