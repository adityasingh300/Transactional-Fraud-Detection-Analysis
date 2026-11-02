@echo off
cd /d "%~dp0"
echo ======================================================================
echo   Pushing Transactional Fraud Detection Analysis to GitHub
echo ======================================================================
echo.
git push origin main
echo.
echo ======================================================================
echo   Done! Press any key to close this window.
echo ======================================================================
pause
