@echo off
REM ==============================================================================
REM SocialPulse 360 - Run Complete Application (Backend + Frontend)
REM ==============================================================================
echo =====================================================================
echo  Launching SocialPulse 360 (Social Media Sentiment & Trend Analytics)
echo =====================================================================
echo [1/2] Launching Backend Server on port 8000...
start "SocialPulse360 - Backend" cmd /k "cd /d %~dp0..\backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

timeout /t 3 /nobreak >nul

echo [2/2] Launching Frontend Server on port 5173...
start "SocialPulse360 - Frontend" cmd /k "cd /d %~dp0..\frontend && npm run dev"

echo.
echo Application initialized!
echo Open your browser at: http://localhost:5173
echo API Documentation at: http://127.0.0.1:8000/docs
echo =====================================================================
pause
