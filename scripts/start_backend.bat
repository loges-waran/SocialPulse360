@echo off
REM ==============================================================================
REM SocialPulse 360 - Start FastAPI Backend Server
REM ==============================================================================
cd /d "%~dp0..\backend"
echo [SocialPulse 360] Starting FastAPI Backend on http://127.0.0.1:8000 ...
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause
