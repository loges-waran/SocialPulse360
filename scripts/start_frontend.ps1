# ==============================================================================
# SocialPulse 360 - Start Vite React Frontend (PowerShell)
# ==============================================================================
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location (Join-Path $ScriptDir "..\frontend")
Write-Host "[SocialPulse 360] Starting Vite Dev Server on http://localhost:5173 ..." -ForegroundColor Cyan
npm run dev
