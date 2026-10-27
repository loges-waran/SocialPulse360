# ==============================================================================
# SocialPulse 360 - Start FastAPI Backend Server (PowerShell)
# ==============================================================================
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location (Join-Path $ScriptDir "..\backend")
Write-Host "[SocialPulse 360] Starting FastAPI Backend on http://127.0.0.1:8000 ..." -ForegroundColor Cyan
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
